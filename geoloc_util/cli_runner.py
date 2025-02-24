import sys
from .cli import parse_arguments, get_locations_interactively
from .api import geolocate_location
from .logger_setup import setup_logger


def run_cli():
    """
    Run the command-line interface (CLI) version of the Geolocation Utility.
    """

    logger = setup_logger()
    args = parse_arguments()
    locations = args.locations

    if not locations:
        locations = get_locations_interactively()

    if not locations:
        print("No locations provided. Exiting.")
        sys.exit(1)

    for loc in locations:
        print(f"\nProcessing: {loc}")
        result_location_data = geolocate_location(loc)
        if result_location_data:
            lat = result_location_data.get('lat')
            lon = result_location_data.get('lon')
            name = result_location_data.get('name')
            state = result_location_data.get('state')
            country = result_location_data.get('country', 'US')
            output = (
                f"Result: {name} ({country})\n"
                f"Latitude: {lat}\n"
                f"Longitude: {lon}"
            )
            print(output)
            logger.debug("Output for %s:\n%s", loc, output)
        else:
            message = f"No data available for: {loc}"
            print(message)
            logger.warning(message)