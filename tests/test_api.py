from geoloc_util import api
import requests


class DummyResponse:
    """
    A dummy response class for simulating HTTP responses in tests.
    """
    def __init__(self, json_data, status_code, text=""):
        self._json = json_data
        self.status_code = status_code
        self.text = text

    def json(self):
        return self._json


def test_get_geolocation_by_zip(monkeypatch):
    """
    Test that get_geolocation_by_zip returns the correct geolocation data
    for a valid ZIP code ("90210"). This test uses monkeypatch to simulate
    an HTTP response from the API and verifies that the returned data matches
    the expected values.
    """

    def fake_get(url):
        assert "zip=90210" in url, "URL must contain 'zip=90210' for a ZIP code query"
        return DummyResponse({
            "lat": 34.0901,
            "lon": -118.4065,
            "name": "Beverly Hills",
            "state": "California",
            "country": "US"
        }, 200)

    monkeypatch.setattr(requests, "get", fake_get)
    result = api.get_geolocation_by_zip("90210")

    assert result["name"] == "Beverly Hills", "Expected name to be 'Beverly Hills'"
    assert result["state"] == "California", "Expected state to be 'California'"
    assert result["lat"] == 34.0901, "Expected latitude to be 34.0901"


def test_get_geolocation_by_city_state(monkeypatch):
    """
    Test that get_geolocation_by_city_state returns the correct geolocation data
    for a valid city/state input ("Madison, WI"). This test uses monkeypatch to simulate
    an HTTP response from the API and verifies that the returned data matches the expected values.
    """

    def fake_get(url):
        assert "q=Madison,WI,US" in url, "URL must contain 'q=Madison,WI,US' for a city/state query"
        return DummyResponse([{
            "lat": 43.0731,
            "lon": -89.4012,
            "name": "Madison",
            "state": "Wisconsin",
            "country": "US"
        }], 200)

    monkeypatch.setattr(requests, "get", fake_get)
    result = api.get_geolocation_by_city_state("Madison, WI")

    assert result["name"] == "Madison", "Expected name to be 'Madison'"
    assert result["state"] == "Wisconsin", "Expected state to be 'Wisconsin'"
    assert result["lat"] == 43.0731, "Expected latitude to be 43.0731"


def test_geolocate_location(monkeypatch):
    """
    Test that geolocate_location dispatches correctly based on input format:
    - Numeric input (ZIP) calls get_geolocation_by_zip with the correct ZIP.
    - City/state input calls get_geolocation_by_city_state with the correct string.
    """

    called = {"zip": False, "city": False}
    captured_zip = None
    captured_city_state = None

    def fake_get_geolocation_by_zip(zip_code):
        nonlocal captured_zip
        captured_zip = zip_code
        called["zip"] = True
        return {"lat": 1, "lon": 2, "name": "TestZip", "state": "TestState", "country": "US"}

    def fake_get_geolocation_by_city_state(city_state):
        nonlocal captured_city_state
        captured_city_state = city_state
        called["city"] = True
        return {"lat": 3, "lon": 4, "name": "TestCity", "state": "TestState", "country": "US"}

    monkeypatch.setattr(api, "get_geolocation_by_zip", fake_get_geolocation_by_zip)
    monkeypatch.setattr(api, "get_geolocation_by_city_state", fake_get_geolocation_by_city_state)

    result_zip = api.geolocate_location("90210")
    assert called["zip"] is True, "Expected get_geolocation_by_zip to be called for numeric input"
    assert called["city"] is False, "Expected get_geolocation_by_city_state not to be called for numeric input"
    assert captured_zip == "90210", "Expected the ZIP code argument to be passed correctly"
    assert result_zip == {"lat": 1, "lon": 2, "name": "TestZip", "state": "TestState", "country": "US"}, \
        "Unexpected result for ZIP code input"

    called["zip"] = False
    called["city"] = False
    captured_zip = None
    captured_city_state = None

    result_city = api.geolocate_location("Madison, WI")
    assert called["city"] is True, "Expected get_geolocation_by_city_state to be called for city/state input"
    assert captured_city_state == "Madison, WI", "Expected the city/state argument to be passed correctly"
    assert result_city == {"lat": 3, "lon": 4, "name": "TestCity", "state": "TestState", "country": "US"}, \
        "Unexpected result for city/state input"


def test_get_geolocation_by_city_state_invalid_format(monkeypatch):
    """
    When the city/state input does not contain a comma (e.g., "Madison WI"),
    the function should return None.
    """

    result = api.get_geolocation_by_city_state("Madison WI")
    assert result is None, "Expected None for city/state input without a comma"


def test_get_geolocation_by_city_state_missing_state(monkeypatch):
    """
    When only a city is provided (e.g., "Madison"),
    the function should return None because the state is missing.
    """

    result = api.get_geolocation_by_city_state("Madison")
    assert result is None, "Expected None for city/state input missing the state"


def test_get_geolocation_by_zip_invalid(monkeypatch):
    """
    When a non-numeric ZIP code is provided (e.g., "ABC123"),
    the function should return None.
    """

    result = api.get_geolocation_by_zip("ABC123")
    assert result is None, "Expected None for non-numeric ZIP input"


def test_geolocate_location_multiple(monkeypatch):
    """
    Verify that geolocate_location handles multiple inputs:
    - Valid ZIP code: "90210"
    - Valid city/state: "Madison, WI"
    - Invalid input: "InvalidCity" (which should return None)
    """

    def fake_get_geolocation_by_zip(zip_code):
        return {"lat": 1, "lon": 2, "name": "TestZip", "state": "TestState", "country": "US"}

    def fake_get_geolocation_by_city_state(city_state):
        if ',' not in city_state:
            return None
        return {"lat": 3, "lon": 4, "name": "TestCity", "state": "TestState", "country": "US"}

    monkeypatch.setattr(api, "get_geolocation_by_zip", fake_get_geolocation_by_zip)
    monkeypatch.setattr(api, "get_geolocation_by_city_state", fake_get_geolocation_by_city_state)

    result_zip = api.geolocate_location("90210")
    result_city = api.geolocate_location("Madison, WI")
    result_invalid = api.geolocate_location("InvalidCity")

    assert result_zip is not None, "Expected a valid result for a proper ZIP code input"
    assert result_city is not None, "Expected a valid result for a proper city/state input"
    assert result_invalid is None, "Expected None for an invalid input format"


