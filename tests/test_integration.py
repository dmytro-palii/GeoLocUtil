import sys
import subprocess
import requests
import pytest
from geoloc_util import cache, api

"""
Contains full integration tests that simulate running the entire application (via subprocess) to 
ensure all components work together as expected.
"""

@pytest.mark.integration
def run_util(*args):
    """
    Execute the GeoLoc Util as a subprocess using its unified main module.

    This helper function builds a command to run the 'geoloc_util.main' module with any additional
    command-line arguments provided via *args. It then executes the command using subprocess.run,
    capturing standard output, standard error, and the return code. The function returns a tuple
    containing these three elements.
    """

    command = [sys.executable, "-m", "geoloc_util.main"] + list(args)
    result = subprocess.run(command, capture_output=True, text=True)

    return result.stdout, result.stderr, result.returncode


@pytest.mark.integration
def test_cli_mode_integration():
    """
    Test that the utility can process multiple inputs:
    - "Madison, WI" (city/state)
    - "90210" (ZIP code)
    and that the output contains expected strings.
    """

    stdout, stderr, returncode = run_util("Madison, WI", "90210")
    assert returncode == 0, "Expected return code to be 0 for successful execution"
    assert "Processing: Madison, WI" in stdout, "Expected output to contain 'Processing: Madison, WI'"
    assert "Processing: 90210" in stdout, "Expected output to contain 'Processing: 90210'"
    assert "Latitude:" in stdout, "Expected output to mention 'Latitude:'"
    assert "Longitude:" in stdout, "Expected output to mention 'Longitude:'"


@pytest.mark.integration
def test_cache_hit_prevents_api_call_zip(monkeypatch, temp_cache_file):
    """
    Test that if valid cached data exists for a ZIP code request,
    get_geolocation_by_zip returns the cached data without making an API call.
    """

    key = "zip:90210"
    valid_response = {
        "zip": "90210",
        "name": "Beverly Hills",
        "lat": 34.0901,
        "lon": -118.4065,
        "country": "US"
    }

    cache.set_cached_response(key, valid_response)

    def fake_get(url):
        raise AssertionError("requests.get was called even though valid cache exists")

    monkeypatch.setattr(requests, "get", fake_get)
    result = api.get_geolocation_by_zip("90210")

    assert result == valid_response, "Expected the cached response to be returned without making an API request"


@pytest.mark.integration
def test_cache_hit_prevents_api_call_city_state(monkeypatch, temp_cache_file):
    """
    Test that if valid cached data exists for a city/state request,
    get_geolocation_by_city_state returns the cached data without making an API call.
    """

    key = "city_state:Madison, WI"
    valid_response = {
        "zip": "N/A",
        "name": "Madison",
        "lat": 43.0731,
        "lon": -89.4012,
        "state": "Wisconsin",
        "country": "US"
    }

    cache.set_cached_response(key, valid_response)

    def fake_get(url):
        raise AssertionError("requests.get was called even though a valid cache exists for city/state.")

    monkeypatch.setattr(requests, "get", fake_get)
    result = api.get_geolocation_by_city_state("Madison, WI")

    assert result == valid_response, "Expected cached response to be returned without making an API call for city/state."

