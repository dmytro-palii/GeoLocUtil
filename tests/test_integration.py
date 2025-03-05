import sys
import subprocess
import pytest

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
