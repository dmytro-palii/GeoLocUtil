import sys
import pytest
from geoloc_util import cli

"""
Test CLI helper functions such as argument parsing and interactive input collection. 
It uses monkeypatching to simulate user inputs
"""

def test_parse_arguments(monkeypatch):
    """
    Test the CLI argument parser, verifies that
    the parse_arguments() function correctly extracts the location inputs from sys.argv.
    """

    test_args = ["prog", "Madison, WI", "90210"]
    monkeypatch.setattr(sys, "argv", test_args)
    args = cli.parse_arguments()

    assert args.locations == ["Madison, WI", "90210"], "Expected parsed locations to match provided arguments"


def test_get_locations_interactively(monkeypatch):
    """
    Test the interactive location input function. It ensures that
    get_locations_interactively() correctly collects location inputs until "done" is entered,
    and returns the expected list of locations.
    """

    inputs = iter(["90210", "Madison, WI", "done"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(inputs))
    locations = cli.get_locations_interactively()

    assert locations == ["90210", "Madison, WI"], "Expected interactive input to yield the correct list of locations"
