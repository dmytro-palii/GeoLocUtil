import requests
from .logger_setup import setup_logger
from .config_helper import build_zip_url, build_direct_url
from .cache import get_cache_response, set_cached_response

logger = setup_logger()

"""
Contains functions that interact with the OpenWeather Geocoding API.
"""

def get_geolocation_by_zip(zip_code: str):
    """
    Retrieve geolocation data for a given ZIP code using the OpenWeather Geocoding API.
    First, check if a valid response is cached; if so, return that. Otherwise, make the API
    request, cache the response if valid, and then return it.
    """

    key = f'zip:{zip_code}'
    cached_data = get_cache_response(key)
    if cached_data is not None:
        logger.info("Cache hit for ZIP code: %s", zip_code)
        return cached_data

    logger.info("Fetching geolocation for ZIP code: %s", zip_code)
    url = build_zip_url(zip_code)
    logger.debug("Request URL: %s", url)
    response = requests.get(url)

    if response.status_code != 200:
        logger.error("Error fetching data for %s: %s", zip_code, response.text)
        return None

    try:
        lat_lon_by_zip_data = response.json()
        logger.debug("Response JSON for %s: %s", zip_code, lat_lon_by_zip_data)
    except Exception as e:
        logger.error("Error parsing JSON for %s: %s", zip_code, e)
        return None

    set_cached_response(key, lat_lon_by_zip_data)
    return lat_lon_by_zip_data


def get_geolocation_by_city_state(city_state: str):
    """
    Retrieve geolocation data for a given city and state using the OpenWeather Geocoding API.
    The input should be a string in the format "City, State".
    First, check if a valid response is cached; if so, return that. Otherwise, make the API
    request, cache the response if valid, and then return the first result from the list of
    geolocation data.
    If any error occurs (e.g., invalid format, HTTP error, JSON parsing error, or no results),
    the function logs the error and returns None.
    """

    key = f'city_state:{city_state}'
    cached_data = get_cache_response(key)
    if cached_data is not None:
        logger.info("Cache hit for ZIP code: %s", city_state)
        return cached_data

    logger.info("Fetching geolocation for city/state: %s", city_state)
    city_state_list = [city_state_str.strip() for city_state_str in city_state.split(',')]
    if len(city_state_list) < 2:
        logger.error("Invalid city/state format: %s", city_state)
        return None

    city, state = city_state_list[0], city_state_list[1]
    url = build_direct_url(city, state)
    logger.debug("Request URL: %s", url)
    response = requests.get(url)

    if response.status_code != 200:
        logger.error("Error fetching data for %s: %s", city_state, response.text)
        return None

    try:
        lat_lon_by_city_state_data = response.json()
        logger.debug("Response JSON for %s: %s", city_state, lat_lon_by_city_state_data)
    except Exception as e:
        logger.error("Error parsing JSON for %s: %s", city_state, e)
        return None

    if not lat_lon_by_city_state_data:
        logger.error("No results found for %s", city_state)
        return None

    set_cached_response(key, lat_lon_by_city_state_data[0])
    return lat_lon_by_city_state_data[0]


def geolocate_location(location: str):
    """
    Dispatch geolocation retrieval based on the input format.
    """

    if location.replace(' ', '').isdigit():
        return get_geolocation_by_zip(location)
    else:
        return get_geolocation_by_city_state(location)
