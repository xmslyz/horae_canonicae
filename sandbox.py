# amDg
import json
import calendar


def ask_for_place():
    return "poza Polską"


def ask_for_congregation():
    return None


def generate_year_dictionary():
    year_dict = {}

    # Iterate over each month and year
    for month in range(1, 13):  # months 1 to 12
        month_name = calendar.month_name[month]  # Get the month's name
        # Get the number of days in the month for the year
        _, num_days = calendar.monthrange(2024, month)

        month_dict = {}
        # Add each day to the month's dictionary
        for day in range(1, num_days + 1):
            day_str = str(day)
            month_dict[day_str] = {
                "MF": {
                    "feast": "",
                    "rank": ""
                },
                "OP": {}
            }
        year_dict[month_name] = month_dict

    with open("liturgical_agenda.json", "w", encoding="utf-8") as f:
        json.dump(year_dict, f, indent=4, ensure_ascii=True)


def find_officium():
    # look for a day of week
    # look for a liturgical week
    # look in general calendar
    ...


def make_json_files():
    months = [
        "january",
        "february",
        "march",
        "abril",
        "may",
        "june",
        "july",
        "august",
        "september",
        "october",
        "november",
        "december"
    ]

    new_dict = dict()

    for month in months:
        with open(f"{month}.json", "w", encoding="utf-8") as f:
            json.dump(new_dict, f, indent=4, ensure_ascii=True)


def make_month_agenda():
    # with open("3_indexing/index_lau.json", encoding="utf8") as f:
    with open("litcalendar/liturgical_agenda.json", encoding="utf8") as f:
        file: dict = json.load(f)

    find_off_and_rank(file)


def find_off_and_rank(d, path=""):
    ftype = "MO"

    # If the current level is a dictionary
    if isinstance(d, dict):
        # Check if "Off" is in the current dictionary
        if "rank" in d and d["rank"] == ftype:
            # Find the "rank" key at the same level
            # loc_value = d.get("LOCATION")
            # name_value = d.get("OFFICIUM")
            rank_value = d.get("feast")
            if rank_value is not None:
                print(
                    # f'[{path}] {ftype} {name_value} {loc_value}')
                    f'[{path}] {ftype} {rank_value}')
                    # f'{loc_value}')

        # Recursively search in nested dictionaries
        for key, value in d.items():
            if isinstance(value, (dict, list)):
                find_off_and_rank(value, path + key + "|")
    # If the value is a list, iterate through its elements
    elif isinstance(d, list):
        for index, item in enumerate(d):
            find_off_and_rank(item, path + f"[{index}] -> ")


def make_loc_litings():
    # List of entries with duplicates
    entries = [
        "U bonifratrów",
        "U franciszkanów konwentualnych",
        "U jezuitów",
        "U kapucynów",
        "U karmelitów",
        "U pasjonistów",
        "U paulinów",
        "U redemptorystów",
        "U salezjanów",
        "W II Zakonie Franciszkańskim",
        "W Rodzinie św.Pawła",
        "W Zgromadzeniu Księży Najświętszego Serca Jezusowego",
        "W prowincjach OFM",
        "W zgromadzeniu Księży Misjonarzy i Sióstr Miłosierdzia",
        "W zgromadzeniu Misjonarzy Oblatów Maryi Niepokalanej",
    ]

    # Create a set to remove duplicates
    unique_entries = set(entries)

    # Print the unique entries
    for entry in sorted(unique_entries):
        print(entry)


def main_menu():
    tu = {
        "LOC": None,
        "ORG": None,
        "DIOC": None,
        "HOUSE": None
    }

    while True:
        user_input = input("Znajdujesz się w Polsce [t/n]? >>> ").lower()
        if user_input == "t":
            tu["LOC"] = True
            user_input = input("W [a]rchidiecezji, [d]iecezji, "
                               "[o]rdynariacie? >>> "
                               "").lower()
            if user_input == "a":
                i = input(
                    "[1]  białostockiej\t\t"
                    "[2]  częstochowskiej\t"
                    "[3]  gdańskiej\t\t"
                    "[4]  gnieźnieńskiej\n"
                    "[5]  katowickiej\t\t"
                    "[6]  krakowskiej\t\t"
                    "[7]  lubelskiej\t\t"
                    "[8]  łódzkiej\n"
                    "[9]  poznańskiej\t\t"
                    "[10] przemyskiej\t\t"
                    "[11] szczecińsko-kamieńskiej\n"
                    "[12] warmińskiej\t\t"
                    "[13] warszawskiej\t\t"
                    "[14] wrocławskiej\n >>> ",
                )

                archi = [
                    "białostockiej",
                    "częstochowskiej",
                    "gdańskiej",
                    "gnieźnieńskiej",
                    "katowicki",
                    "krakowskiej",
                    "lubelskiej",
                    "łódzkiej",
                    "poznańskiej",
                    "przemyski",
                    "szczecińsko-kamieńskiej",
                    "warmińskiej",
                    "warszawskiej",
                    "wrocławskiej"]
                tu["DIOC"] = archi[int(i) - 1]
                tu["ORG"] = "archidiecezji "
            elif user_input == "d":
                i = input(
                    "[1]  bielsko-żywieckiej\t\t\t"
                    "[2]  bydgoskiej\t\t\t\t"
                    "[3]  drohiczyńskiej\t\t"
                    "[4]  elbląskiej\t\t\t\t\t\t"
                    "[5]  ełckiej\n"
                    "[6]  gliwickiej\t\t\t\t\t"
                    "[7]  kaliskiej\t\t\t\t"
                    "[8]  kieleckiej\t\t\t"
                    "[9]  koszalińsko-kołobrzeskiej\t\t"
                    "[10] legnickiej\n"
                    "[11] łomżyńskiej\t\t\t\t"
                    "[12] łowickiej\t\t\t\t"
                    "[13] opolskiej\t\t\t"
                    "[14] pelplińskiej\t\t\t\t\t"
                    "[15] płockiej\n"
                    "[16] radomskiej\t\t\t\t\t"
                    "[17] rzeszowskiej\t\t\t"
                    "[18] sandomierskiej\t\t"
                    "[19] siedleckiej\t\t\t\t\t"
                    "[20] sosnowieckiej\n"
                    "[21] świdnickiej\t\t\t\t"
                    "[22] tarnowskiej\t\t\t"
                    "[23] toruńskiej\t\t\t"
                    "[24] warszawsko-praskiej\t\t\t"
                    "[25] włocławskiej\n"
                    "[26] zamojsko-lubaczowskiej\t\t"
                    "[27] zielonogórsko-gorzowskiej\n >>> ")

                dioc = [
                    "bielsko-żywieckiej",
                    "bydgoskiej",
                    "drohiczyńskiej",
                    "elbląskiej",
                    "ełckiej",
                    "gliwickiej",
                    "kaliskiej",
                    "kieleckiej",
                    "koszalińsko-kołobrzeskiej",
                    "legnickiej",
                    "łomżyńskiej",
                    "łowickiej",
                    "opolskiej",
                    "pelplińskiej",
                    "płockiej",
                    "radomskiej",
                    "rzeszowskiej",
                    "sandomierskiej",
                    "siedleckiej",
                    "sosnowieckiej",
                    "świdnickiej",
                    "tarnowskiej",
                    "toruńskiej",
                    "warszawsko-praskiej",
                    "włocławskiej",
                    "zamojsko-lubaczowskiej",
                    "zielonogórsko-gorzowskiej"
                ]
                tu["DIOC"] = dioc[int(i) - 1]
                tu["ORG"] = "diecezji "
            elif user_input == "o":
                tu["DIOC"] = "Ordynariacie Polowym"
                tu["ORG"] = ""
        elif user_input == "n":
            tu["LOC"] = False
            tu["DIOC"] = "człowiekiem!"
            tu["ORG"] = "wolnym "

        break

    print(f"Jesteś w {tu['ORG']}{tu['DIOC']}!")


if __name__ == "__main__":
    # make_json_files()
    make_month_agenda()
    # generate_year_dictionary()
    # make_loc_litings()
