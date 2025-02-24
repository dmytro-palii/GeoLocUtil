import requests
from .logger_setup import setup_logger
from .config_helper import build_zip_url, build_direct_url

logger = setup_logger()


def get_geolocation_by_zip(zip_code: str):
    """
    Constructs the request URL for the provided ZIP code, sends an HTTP GET request,
    and returns the parsed JSON data if successful. If the HTTP status code is not 200 or if JSON
    parsing fails, it logs an error and returns None.
    """

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

    return lat_lon_by_zip_data


def get_geolocation_by_city_state(city_state: str):
    """
    This function expects a string in the format "City, State". It splits the string,
    validates the format, constructs the appropriate request URL using build_direct_url(),
    and sends an HTTP GET request to the API. If the response is successful and the JSON
    data is parsed correctly, it returns the first result from the list of geolocation data.
    If any error occurs (e.g., invalid format, HTTP error, JSON parsing error, or no results),
    the function logs the error and returns None.
    """

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

    return lat_lon_by_city_state_data[0]


def geolocate_location(location: str):
    """
    Dispatch geolocation retrieval based on the input format.
    """

    if location.replace(' ', '').isdigit():
        return get_geolocation_by_zip(location)
    else:
        return get_geolocation_by_city_state(location)
