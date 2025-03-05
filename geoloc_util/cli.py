import argparse

"""
Handles CLI argument parsing and interactive input.
"""

def parse_arguments():
    """
    Parse command-line arguments for the Geolocation Utility.
    """

    parser = argparse.ArgumentParser(
        description="Geolocation Utility using OpenWeather Geocoding API"
    )
    parser.add_argument(
        "locations",
        nargs="*",
        help="Location inputs (City, State e.g., 'Madison, WI' or Zip Code e.g., '12345')"
    )

    return parser.parse_args()


def get_locations_interactively():
    """
    Prompt the user for location inputs interactively.
    """

    print("Enter location inputs one at a time (type 'done' to finish):")
    print("✅ For city/state, use the format: 'City, State' (e.g., Madison, WI)")
    print("✅ For ZIP code, enter the ZIP (e.g., 90210)")
    print("❌ Do not use any special characters")
    locations_list = []
    while True:
        user_input = input("Enter location: ")
        if user_input.lower() in ("done", ""):
            break
        locations_list.append(user_input)

    return locations_list
