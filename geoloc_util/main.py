if __name__ == "__main__" and __package__ is None:
    # Bootstrap code to enable running this module directly.
    # It adds the project root to sys.path and sets __package__ to "geoloc_util"
    # so that relative imports work correctly.
    import os
    import sys

    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    __package__ = "geoloc_util"

import sys
import argparse
from .cli_runner import run_cli
from .gui_runner import run_gui


def main():
    """
    Unified entry point for the GeoLoc Utility supporting both CLI and GUI modes.
    """

    parser = argparse.ArgumentParser(
        description="GeoLoc Utility with CLI and GUI modes"
    )
    parser.add_argument("--gui", action="store_true", help="Run in GUI mode")
    parser.add_argument(
        "locations",
        nargs="*",
        help=(
            "Location inputs for CLI mode. For city/state, use the format 'City, State' (e.g., Madison, WI); "
            "for ZIP codes, simply provide the ZIP (e.g., 90210). You can supply multiple locations as separate arguments."
            "❌Do not use any special character"
        )
    )
    args = parser.parse_args()

    if args.gui:
        run_gui()
    else:
        if args.locations:
            run_cli()
        else:
            if sys.stdout.isatty():
                run_cli()
            else:
                run_gui()


if __name__ == "__main__":
    main()
