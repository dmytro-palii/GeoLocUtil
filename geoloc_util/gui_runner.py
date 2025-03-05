import tkinter as tk
from tkinter import scrolledtext
from .api import geolocate_location
from .logger_setup import setup_logger

"""
Separate modules for running the application in GUI mode.
"""

def run_gui():
    """
    Launch the graphical user interface (GUI) for the Geolocation Utility.
    """

    logger = setup_logger()

    def search_locations():
        input_text = input_text_box.get("1.0", tk.END).strip()
        locations = input_text.splitlines()
        result_text_box.delete("1.0", tk.END)

        if not locations:
            result_text_box.insert(tk.END, "No locations provided.\n")
            return

        for loc in locations:
            result_text_box.insert(tk.END, f"Processing: {loc}\n")
            logger.info("Processing location (GUI): %s", loc)
            result_location_data = geolocate_location(loc)
            if result_location_data:
                lat = result_location_data.get("lat")
                lon = result_location_data.get("lon")
                name = result_location_data.get("name", "Unknown")
                state = result_location_data.get("state", "")
                country = result_location_data.get("country", "US")
                output = (
                    f"Result: {name} ({country})\n"
                    f"ZIP: {loc}\n"
                    f"Latitude: {lat}\n"
                    f"Longitude: {lon}\n\n"
                )
            else:
                output = f"No data available for: {loc}\n\n"
            result_text_box.insert(tk.END, output)

    def clear_input():
        input_text_box.delete("1.0", tk.END)
        result_text_box.delete("1.0", tk.END)

    window = tk.Tk()
    window.title("GeoLoc Utility")

    input_label = tk.Label(
        window,
        text=(
            "Enter location(s) (one per line):\n"
            " ✅ For city/state, use the format: 'City, State' (e.g., Madison, WI)\n"
            " ✅ For ZIP code, enter the ZIP (e.g., 90210)\n"
            " ❌ Do not use any special character ❌"
        ),
        justify="left",
        anchor="w"
    )
    input_label.pack(pady=(10, 0))

    input_text_box = tk.Text(window, height=5, width=50)
    input_text_box.pack(pady=(0, 10))

    button_frame = tk.Frame(window)
    button_frame.pack(pady=(0, 10))
    search_button = tk.Button(button_frame, text="Search", command=search_locations)
    search_button.pack(side=tk.LEFT, padx=5)
    clear_button = tk.Button(button_frame, text="Clear", command=clear_input)
    clear_button.pack(side=tk.LEFT, padx=5)

    result_label = tk.Label(window, text="Results:")
    result_label.pack()
    result_text_box = scrolledtext.ScrolledText(window, height=10, width=60)
    result_text_box.pack(pady=(0, 10))

    window.mainloop()
