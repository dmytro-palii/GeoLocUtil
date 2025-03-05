import os
import json
import pytest
from geoloc_util import config_helper

"""
Verifies that configuration loading and URL-building functions work as expected by 
using temporary files and checking that the correct values are returned.
"""

def test_load_config(tmp_path):
    """
    Test that load_config() properly loads and parses a configuration file.

    This test writes a temporary config file containing specific API settings,
    then verifies that load_config() returns a dictionary with the expected values.
    """

    config_content = {
        "OPENWEATHER_API_KEY": "TEMP_API_KEY",
        "BASE_URL_DIRECT": "http://temp.com/direct",
        "BASE_URL_ZIP": "http://temp.com/zip"
    }

    config_file = tmp_path / 'config.yaml'
    config_file.write_text(json.dumps(config_content))
    config = config_helper.load_config(config_filename=str(config_file))

    assert config["OPENWEATHER_API_KEY"] == "TEMP_API_KEY", "API key should match the temporary value"
    assert config["BASE_URL_DIRECT"] == "http://temp.com/direct", "Direct URL should match the temporary value"
    assert config["BASE_URL_ZIP"] == "http://temp.com/zip", "ZIP URL should match the temporary value"


@pytest.mark.parametrize("zip_code", ["12345", "90210", "55555"])
def test_build_zip_url(monkeypatch, zip_code):
    """
    Test that build_zip_url() constructs the correct URL for a given ZIP code.

    This test uses pytest's parameterization to run with multiple ZIP code values.
    It overrides the load_config() function to return a fixed configuration and then
    verifies that the constructed URL matches the expected format.
    """

    monkeypatch.setattr(
        config_helper, "load_config",
        lambda config_filename="config.yaml": {
            "OPENWEATHER_API_KEY": "TEST_API_KEY",
            "BASE_URL_ZIP": "http://example.com/zip"
        }
    )

    url = config_helper.build_zip_url(zip_code)
    expected = f"http://example.com/zip?zip={zip_code},US&appid=TEST_API_KEY"

    assert url == expected, f"Expected zip URL for {zip_code} to be {expected} but got {url}"


@pytest.mark.parametrize('city, state', [
    ('Madison', 'WI'),
    ('Chicago', 'IL'),
    ('Los Angeles', 'CA')
])
def test_build_direct_url(monkeypatch, city, state):
    """
    Test that build_direct_url() constructs the correct URL for a given city and state.

    This test uses pytest's parameterization to run with multiple (city, state) pairs.
    It overrides load_config() to return a fixed configuration containing a test API key and base URL.
    The function then generates the URL and verifies that it matches the expected format.
    """

    monkeypatch.setattr(
        config_helper, "load_config",
        lambda config_filename="config.yaml": {
            "OPENWEATHER_API_KEY": "TEST_API_KEY",
            "BASE_URL_DIRECT": "http://example.com/direct"
        }
    )

    url = config_helper.build_direct_url(city, state)
    expected = f"http://example.com/direct?q={city},{state},US&limit=1&appid=TEST_API_KEY"

    assert url == expected, f"Expected direct URL to be {expected} but got {url}"
