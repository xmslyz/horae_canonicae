import json
from collections import defaultdict


def make_json_file_ivitatorium():

    my_lg = defaultdict()
    with open("dd.txt", encoding="utf-8") as d:
        txt = d.read()

    scraped = txt.split("|")
    for i in range(4):
        psalm_number, right_part_1 = scraped[i].split("#")
        psalm_title, right_part_2 = right_part_1.split("$")
        bible_reference, invitatorium_psalm = right_part_2.split("%")
        estrofas = invitatorium_psalm.split("^")

        my_lg[psalm_number] = {
            "num": psalm_number,
            "mot": psalm_title,
            "cit": bible_reference,
            "est": estrofas
        }

    with open("readyfiles/invitatory.json", "w") as d:
        json.dump(my_lg, d, indent=4)


def parse_canonical_hour(canonical_hour, quick=False):
    """
    Parse liturgical data from JSON files and extract psalms.

    This function extracts psalms from JSON files containing liturgical data,
    such as 'lau.json'. It iterates through specified months and days and
    attempts to extract psalms for each day.

    This function will raise error if you will parse invitatorium or complete

    Args:
        canonical_hour: name of filename to parse.
        quick (bool, optional): If True, only processes a subset of data (for
        testing or quick execution).
            Defaults to False.

    Returns:
        defaultdict: A dictionary containing extracted psalms organized by
        month and day.
            The keys are in the format 'month_day' (e.g., '8_1' for August 1st).
            The values are dictionaries with psalm data.

    Example:
        If 'lau.json' contains liturgical data, and quick=False, the
        function will extract psalms for specified months and days, and the
        resulting dictionary may look +like this:
        {
            '8_1': {
                'psalm_1': 'Text of Psalm 1',
                'psalm_2': 'Text of Psalm 2',
                # ...
            },
            '8_2': {
                'psalm_1': 'Text of Psalm 1',
                'psalm_2': 'Text of Psalm 2',
                # ...
            },
            # ...
        }

    """
    if canonical_hour == "com" or canonical_hour == "inv":
        print("Funkcja nie obsługuje parsowania komplety i wezwania")
        raise NameError

    psalm_dict = defaultdict(dict)
    months = [8, 9, 11] if not quick else [8]
    days = range(1, 32) if not quick else [2]
    for month in months:
        for day in days:
            try:

                laudes = edit_txt(f"readyfiles/{canonical_hour}.json")[str(
                    month)][str(
                    day)]
                lsplited = laudes.split("\n")
                lsplited = [x for x in lsplited if x.strip() != ""]
                lsplited = [x for x in lsplited if
                            not x.startswith("W wersji PREMIUM")]
                psalms_data = extract_psalm(lsplited)
                psalm_dict.update(psalms_data)
            except KeyError:
                pass

    with open(f"{canonical_hour}_dict.json", "w") as ch:
        json.dump(psalm_dict, ch, indent=4)


def extract_psalm(splited):
    """
    Process liturgical data for Laudes and extract psalms. Except comletas

    This function takes a list of strings 'splited' containing liturgical data
    for Laudes. It extracts information such as color, date, antyfons, and
    psalms, and organizes them into a dictionary.

    Args:
        splited (list of str): A list of strings containing liturgical data.

    Returns:
        defaultdict: A dictionary containing extracted information organized by
        date and psalm.
            The structure is as follows:
            {
                'date': {
                    'ps-1': {
                        'feria': 'Feria Name',
                        'period': 'Liturgical Period',
                        'meta-ant': 'Meta Antyfony',
                        'meta-psalm': 'Meta Psalm',
                        'antifona': 'Antyfona's text',
                        'number': 'Psalm Number',
                        'title': 'Psalm Title',
                        'quote': 'Psalm Quote',
                        'psalm': 'Text of the Psalm'
                    },
                    # Additional psalms for the same date if available
                },
                # Additional dates and psalms
            }

    Example:
        If 'lsplited' contains liturgical data, the function will extract and
        structure the data as described above.
    """
    ...


def make_dict_with_psalm_names(lg_dict):
    di = edit_txt(f"readyfiles/{lg_dict}.json")
    year = 2023
    psalms_names = set()
    for month in [8, 9, 11]:
        for day in range(1, 32):
            format_date = f"{year}-{month:02d}-{day:02d}"
            try:
                for i in range(1, 4):
                    # print(di[format_date][f"ps-{i}"].keys())
                    # print(di[format_date][f"ps-{i}"]["feria"])
                    meta_psalm: str = di[format_date][f"ps-{i}"]["meta-psalm"]
                    # print(meta_psalm)

            except KeyError:
                pass
    # print(psalms_names)
    #
    ll = sorted(psalms_names, key=lambda x: x[0])
    new_dict = defaultdict()
    for element in ll:
        new_dict[element[1]] = element[0]
    with open(f"readyfiles/lau_ps.json", "w") as new:
        json.dump(new_dict, new, indent=4)


def scrap_CONST():
    di = edit_txt(f"readyfiles/lau.json")
    sptd = di["8"]["1"].split('\n')
    txt = ''
    for i, element in enumerate(sptd):
        if 0 <= i < 127:
            pass
        # elif 459 <= i <= 470:
        elif i == 368:
            txt += element + "\n"
            print(i, element)
        else:
            print(i, element)
    t = {"PRAYER": txt}
    with open(f"q.json", "w") as ne:
        json.dump(t, ne, indent=4)
