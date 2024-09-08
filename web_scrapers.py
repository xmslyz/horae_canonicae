import calendar
import json
import os
import pathlib
import re
import threading
import time
from collections import defaultdict
from pprint import pprint

import requests
from bs4 import BeautifulSoup

import logging
import tools

# Get the current script's filename without the extension
filename = os.path.basename(__file__).split('.')[0]
# Set the log file path in the current working directory
logger_dir = pathlib.Path.cwd() / f'__{filename}.log'
# Create the logger
logger = logging.getLogger(__name__)
# Avoid adding duplicate handlers if the logger is already configured
if not logger.hasHandlers():
    # Create the file handler with delayed file creation
    f_handler = logging.FileHandler(str(logger_dir), delay=True)
    f_handler.setLevel(logging.WARNING)
    # Set the format for log messages
    f_format = logging.Formatter(
        '%(message)s')
    f_handler.setFormatter(f_format)
    # Add the handler to the logger
    logger.addHandler(f_handler)
    # Optionally, set the logger's level if it's not already set
    logger.setLevel(logging.DEBUG)  # Or a different level if desired


def www_scrapping():
    """
    Scrapes and downloads all office hours and append (if exist) to json file

    """

    # List of thread arguments
    thread_args = [
        # ("inv", "wezw"),
        ("lec", "godzczyt"),
        # ("lau", "jutrznia"),
        # ("ter", "modlitwa1"),
        # ("sex", "modlitwa2"),
        # ("non", "modlitwa3"),
        # ("vis", "nieszpory"),
        # ("com", "kompleta")
    ]

    # Create and start threads
    threads = []
    for args in thread_args:
        thread = threading.Thread(target=scrape_and_save, args=args)
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    print("All threads have finished.")


def scrape_and_save(filename: str, hour: str):
    """
        Generate and save liturgical data for Laudes to a JSON file.

        This function generates liturgical data for the Laudes prayer for
        specified months and days, then saves it to a JSON file with the
        given filename.

        Args:
            filename (str): The name of the JSON file to save the data to.
            hour (str): The filename of the liturgical prayer.


        Example:
            To generate and save Laudes data for the months of August,
            September, and November, and filename 'morning':
            generate_laudes_data("lau.json", "morning")
            :param hour:
            :param filename:

        """
    YEAR = "24"

    if os.path.exists(f"1_scrapping/{filename}.json"):
        with open(f"1_scrapping/{filename}.json") as f:
            lg = json.load(f)
            if YEAR not in lg:  # Ensure the YEAR exists in lg
                lg[YEAR] = {}
    else:
        lg = defaultdict(dict)
        lg[YEAR] = {}  # Ensure the YEAR exists in lg

    for month in range(9, 10):  # You can modify the range of months as needed
        # Initialize the dictionary for the month
        lg[YEAR][str(month)] = {}

        for day in range(1, calendar.monthrange(2000+int(YEAR), month)[1] + 1):
        # for day in range(1, 2):
            # Modify the day range as necessary
            count_404 = 0

            for w in tools.range_of_memories_depth(10):
                result = _search_for_lg(day, month, int(YEAR), hour, w)

                if result == 404:
                    count_404 += 1
                    if count_404 >= 3:
                        break  # Exit if too many 404 responses
                    continue

                if result and result not in [401, 404]:
                    if str(day) not in lg[YEAR][str(month)]:
                        lg[YEAR][str(month)][str(day)] = {}

                    tables = result.find_all("table")
                    if filename == "lec":
                        if tables:  # Check if table is not empty
                            txt = "/n".join([tables[0].text,
                                             tables[9].text,
                                             tables[11].text,
                                             "CYKL DWULETNI",
                                             tables[10].text,
                                             ])
                            lg[YEAR][str(month)][str(day)][str(w)] = txt
                    else:
                        if tables:
                            txt = tables[0].text
                            lg[YEAR][str(month)][str(day)][str(w)] = txt

    # Save to a JSON file
    # with open(f"1_scrapping/{filename}.json", "w") as f:
    #     json.dump(lg, f, indent=4)


def _make_index_file(filename):
    """
        Generate and save liturgical data for Laudes to a JSON file.

        This function generates liturgical data for the Laudes prayer for
        specified months and days, then saves it to a JSON file with the
        given filename.

        Args:
            filename (str): The name of the JSON file to save the data to.

        Returns:
            None

        Example:
            To generate and save Laudes data for the months of August,
            September, and November, and hour 'morning':
            generate_laudes_data("lau.json", "morning")

        """
    months = [8, 9, 11]
    year = 24
    lg = defaultdict(dict)
    for month in months:
        lg[month] = {}
        for day in range(1, 32):
            lg[month][day] = {}
            result = _search_for_lg(day, month, year)
            if result:
                table = result.find_all("table")
                txt = table[0].text
                if "WYBIERZ OFICJUM:" in txt:
                    lg[month][day] = txt
                    print(month, day)

    with open(f"readyfiles/__{filename}.json", "a+") as f:
        json.dump(lg, f, indent=4)

    print(f"{filename} ready!")


def _search_for_lg(day: int, month: int, year: int, hour=None, w=None,
                   index=False):
    """
    Fetches and parses the webpage from the brewiarz.pl website for a given date
    and optional parameters (hour, w, and index).

    :param day: Day of the month (1-31)
    :param month: Month of the year (1-12)
    :param year: Year as a four-digit integer
    :param hour: (auto) Hour to fetch a specific page
    :param w: (auto) Additional URL parameter
    :param index: (auto) If True, fetches the index page for the date

    :return: 404, 401 error, or parsed BeautifulSoup object
    """

    # Validate month and day inputs
    if month < 1 or month > 12:
        raise ValueError(f"Invalid month: {month}. Must be between 1 and 12.")
    if day < 1 or day > 31:
        raise ValueError(f"Invalid day: {day}. Must be between 1 and 31.")

    # Dictionary for converting month number to Roman numeral
    months_dict = {
        1: "i", 2: "ii", 3: "iii", 4: "iv", 5: "v", 6: "vi",
        7: "vii", 8: "viii", 9: "ix", 10: "x", 11: "xi", 12: "xii"
    }
    m_rom = months_dict[month]

    # Construct the URL based on index flag
    if index:
        url = (f"https://brewiarz.pl/{m_rom}_{year}/{day:02d}{month:02d}"
               f"/index.php3")
    else:
        if hour is None or w is None:
            raise ValueError(
                "When index is False, both 'hour' and 'w' must be provided.")
        url = (f"https://brewiarz.pl/{m_rom}_{year}/{day:02d}{month:02d}"
               f"{w}/{hour}.php3")

    try:
        # Make the request
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        # (4xx, 5xx)
        enc = response.encoding
        page_content = response.text.encode(enc)

        # Check for specific HTTP errors
        if response.status_code == 401:
            print("Error 401: Unauthorized access")
            return 401
        elif response.status_code == 404:
            print("Error 404: Page not found")
            return 404

        # Parse and return the HTML content using BeautifulSoup
        print(f"Found >>>> {month:02d} {day:02d} {hour} {w} >>>> writing")
        return BeautifulSoup(page_content, "html.parser")

    except requests.exceptions.RequestException:
        # Handle all exceptions from the requests library
        # logger.exception(f"An error occurred: {url}")
        pass
