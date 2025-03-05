import os
import yaml

"""
Loads configuration from a YAML file and builds API URLs.
"""

def load_config(config_filename='config.yaml'):
    """
    Load configuration settings from a YAML file.
    """

    config_path = os.path.join(os.path.dirname(__file__), config_filename)
    try:
        with open(config_path, 'r') as config_file:
            config = yaml.safe_load(config_file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    return config


def build_zip_url(zip_code: str) -> str:
    """
    Build and return the complete URL for retrieving geolocation data using a ZIP code.
    """

    config = load_config()
    api_key = config.get("OPENWEATHER_API_KEY")
    base_url_zip = config.get("BASE_URL_ZIP", "http://api.openweathermap.org/geo/1.0/zip")

    return f"{base_url_zip}?zip={zip_code},US&appid={api_key}"


def build_direct_url(city: str, state: str) -> str:
    """
    Build and return the complete URL for retrieving geolocation data using a city and state.
    """

    config = load_config()
    api_key = config.get("OPENWEATHER_API_KEY")
    base_url_direct = config.get("BASE_URL_DIRECT", "http://api.openweathermap.org/geo/1.0/direct")

    return f"{base_url_direct}?q={city},{state},US&limit=1&appid={api_key}"


