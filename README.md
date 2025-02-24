GeoLoc Util is a versatile geolocation retrieval utility that interfaces with the OpenWeather Geocoding API. 
It supports both command-line (CLI) and graphical user interface (GUI) modes for retrieving geographic 
coordinates based on either city/state combinations or ZIP code inputs.


## FEATURES ##

- **Dual Interface:** Supports both CLI and GUI modes.
- **Flexible Input:** Accepts location inputs in two formats:
  - **City/State:** e.g., "Madison, WI"
  - **ZIP Code:** e.g., "90210"
- **Configuration Driven:** Uses a YAML configuration file for API keys and endpoint URLs.
- **Comprehensive Logging:** Logs are written to a common log file to avoid scattering log files across the project.
- **Testing & Visualization:** Includes unit and integration tests (using pytest) with a visual summary of test results.
- **Modular Design:** Clean separation between API handling, CLI/GUI interfaces, configuration, and logging.


## PROJECT STRUCTURE ##

GeoLocUtil/                # Project root
├── geoloc_util/           # Main application package
│   ├── __init__.py
│   ├── api.py             # API-related functions (retrieving geolocation data)
│   ├── cli.py             # CLI argument parsing and interactive input helpers
│   ├── cli_runner.py      # CLI mode execution logic
│   ├── config_helper.py   # Helper functions for configuration loading and URL building
│   ├── config.yaml        # YAML configuration file (API key, endpoints)
│   ├── gui_runner.py      # GUI mode implementation using Tkinter
│   ├── logger_setup.py    # Logger configuration (writes to a common log file)
│   └── main.py            # Unified entry point (dispatches to CLI or GUI based on args)
├── tests/                 # Test suite
│   ├── conftest.py        # Pytest configuration and test result visualization hook
│   ├── test_api.py        # Unit tests for API functions (simulated responses)
│   ├── test_cli.py        # Unit tests for CLI helper functions
│   ├── test_config_helper.py  # Unit tests for configuration helper functions
│   └── test_integration.py    # Integration tests for end-to-end functionality
├── logs/                  # Directory for log files (created at runtime)
├── reports/               # Directory for test result visualizations (created at runtime)
├── requirements.txt       # List of project dependencies
└── README.md              # This file (project documentation)



## INSTALLATION INSTRUCTIONS ##

1. **Clone the Repository:**

   ```bash
   RUN: git clone <repository-url>
   RUN: cd GeoLocUtil

2. **CSet Up a Virtual Environment (Optional):**

    ```bash
    RUN: python -m venv venv
    # On Windows: venv\Scripts\activate
    # Linux or Mac: source venv/bin/activate    

3. **Install Dependencies:**
    
    ```bash
    RUN: pip install -r requirements.txt
    Note: Tkinter is usually included with Python.

## CONFIGURATION DETAILS ##

    The utility uses a YAML configuration file located at 
    geoloc_util/config.yaml to store API settings. Update the file as needed:
    
    OPENWEATHER_API_KEY: "f897a99d971b5eef57be6fafa0d83239"
    BASE_URL_DIRECT: "http://api.openweathermap.org/geo/1.0/direct"
    BASE_URL_ZIP: "http://api.openweathermap.org/geo/1.0/zip"

## USAGE GUIDELINES ##

## Graphical User Interface (GUI):
    
    Force GUI Mode:
    python -m geoloc_util.main --gui
    
    The GUI launches a window with:
    An input area (with detailed instructions and emojis)
    "Enter location(s) (one per line):\n"
    " ✅ For city/state, use the format: 'City, State' (e.g., Madison, WI)\n"
    " ✅ For ZIP code, enter the ZIP (e.g., 90210)\n"
    " ❌ Do not use any special character ❌"
    "Search" and "Clear" buttons
    A scrollable results area showing geolocation information

## Command-Line Interface (CLI):

    Run with Location Arguments:
    python -m geoloc_util.main "Madison, WI" "90210"
    This will process the provided locations and print geolocation data to the terminal.

## Interactive Mode:

    Run without arguments to be prompted for input:
    python -m geoloc_util.main

    The interactive prompt will display instructions:
    ✅ For city/state, use the format: City, State (e.g., Madison, WI)
    ✅ For ZIP code, enter the ZIP (e.g., 90210)
    ❌ Do not use any special characters

## TESTING INSTRUCTIONS ##

1. **Run All Tests:**
    
    ```bash
    From the project root, execute:

    pytest
    
    After the tests run, a visual summary of test outcomes is generated and saved in the 
    reports/ directory as test_results.png.


## DEPENDENCY INFORMATION ##

    Python: 3.6 or later
    Tkinter: (Included with standard Python distributions)

    This project requires the following Python packages:
    (You can install all required packages by running)
    
    ```bash
    pip install -r requirements.txt

    - **certifi==2025.1.31**
    - **charset-normalizer==3.4.1**
    - **colorama==0.4.6**
    - **contourpy==1.3.1**
    - **cycler==0.12.1**
    - **fonttools==4.56.0**
    - **idna==3.10**
    - **iniconfig==2.0.0**
    - **kiwisolver==1.4.8**
    - **matplotlib==3.10.0**
    - **numpy==2.2.3**
    - **packaging==24.2**
    - **pillow==11.1.0**
    - **pluggy==1.5.0**
    - **pyparsing==3.2.1**
    - **pytest==8.3.4**
    - **python-dateutil==2.9.0.post0**
    - **PyYAML==6.0.2**
    - **requests==2.32.3**
    - **six==1.17.0**
    - **urllib3==2.3.0**

## ADDITIONAL NOTES ##

    Logging:
    All logs are written to a common log file located in the logs/ directory, ensuring consistent 
    regardless of which module is executed.
    
    Modular Design:
    The project is designed with a clear separation between API handling, 
    CLI/GUI interfaces, configuration, and logging.
    
    Error Handling:
    Invalid inputs are handled gracefully with appropriate user feedback and log messages.
    
    Test Visualization:
    A custom pytest hook (in tests/conftest.py) generates a bar chart summarizing test outcomes, 
    which is saved in the reports/ directory.
    
    Bootstrap Code:
    The main.py file includes bootstrap code to enable direct execution with proper relative imports.



