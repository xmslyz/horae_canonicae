import json
import re

import arrow


def mem(ant_idx: int):
    print("antes de mem")

    def store(ant_int, storage=None):
        if storage is None:
            storage = []
        return storage.append(ant_int)
    print("despues")
    return store(ant_idx)


def open_json_file(jsonfile):
    try:
        with open(jsonfile, encoding="utf-8") as j:
            file = json.load(j)

        return file

    except FileNotFoundError as e:
        raise FileNotFoundError


def save_json_file(jsonfile, sdic):
    with open(jsonfile, "w", encoding="utf-8") as j:
        json.dump(sdic, j, indent=4)


def get_occurences(lsplited, pattern, first=False):
    """
    Find the index of the first occurrence of a pattern in a list of strings.

    Parameters:
        lsplited (list): A list of strings to search through.
        pattern (str): The regular expression pattern to match against each
        element in the list.
        first (bool): True for list, False for first occurence

    Returns:
        int | list | None: The index of the first element [list of
        elements] that matches the pattern, or None if no match is found.
    """

    #
    result = (
        i for i, element in enumerate(lsplited) if re.match(pattern, element)
    )

    if first:
        return next(result, None)
    else:
        return result


def change_key_name(lg_dict):
    di = open_json_file(f"readyfiles/{lg_dict}.json")
    new_di = {}
    for key, value in di.items():
        day, month, year = data_replace(key)
        dd = arrow.Arrow(int(year), int(month), int(day))
        new_key = dd.format("YYYY-MM-DD")
        new_di[new_key] = value
    with open(f"readyfiles/{lg_dict}.json", "w") as new:
        json.dump(new_di, new, indent=4)


def print_scheme(hour_name, month, day, w):
    sptd = split_to_list(hour_name, month, day, w)
    for i, element in enumerate(sptd):
        print(i, element)


def split_to_list(hour_name, year, month: int, day: int, w) -> list:
    di: dict = open_json_file(f"2_clensing/{hour_name}.json")
    try:
        sptd = di[year][str(month)][str(day)][w].split('\n')
        sptd = [x for x in sptd if x != '']
        return sptd
    except KeyError:
        return []


def data_replace(data):
    pl_int = {
        "sierpnia": "8",
        "września": "9",
        "listopada": "11"
    }

    # Replace Polish month names with English month names
    for polish_month, int_month in pl_int.items():
        data = data.replace(polish_month, int_month)

    return data.split(" ")


def weeks_replace(names):
    pl_int = {
        "I": "week_1",
        "II": "week_2",
        "III": "week_3",
        "IV": "week_4",
    }

    # Define a regular expression pattern to find Roman numerals
    pattern = r'\b(?:' + '|'.join(
        re.escape(key) for key in pl_int.keys()) + r')\b'

    # Use re.sub to replace Roman numerals with English representations
    names = re.sub(pattern, lambda match: pl_int[match.group()], names)
    return names


def range_of_memories_depth(e=2):
    """
    głębokość szukania wspomnień tego samego dnia. [p, w1, w2, w3, w4 .... ]

    :param e: int end on
    :return: generator
    """
    wiis = ["", "p", "w"]
    for i in range(1, e):
        wiis.append(f"w{i}")

    return (item for item in wiis)
