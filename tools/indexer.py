import json
import re
import os
import threading
from collections import defaultdict
import calendar
from operator import truth

import tools




def make_propia_json():
    # Define the structure for each day
    day_structure = {
        **{str(i): {
            "lec": {
                "i reading": "",
                "i responsory": "",
                "ii reading": "",
                "ii responsory": "",
                "prayer": ""
            }} for i in range(6)},  # Keys 0 to 5 with "lec" structure
        "6": {
            "i vis": {
                "ant A": "",
                "ant B": "",
                "ant C": "",
                "prayer": ""
            },
            "lec": {
                "i reading": "",
                "i responsory": "",
                "ii reading": "",
                "ii responsory": "",
            },
            "lau": {
                "ant A": "",
                "ant B": "",
                "ant C": "",
                "prayer": ""
            },
            "ii vis": {
                "ant A": "",
                "ant B": "",
                "ant C": ""
            }
        }
    }

    # Generate the full JSON structure with keys from 1 to 34
    data = {str(i): day_structure for i in range(1, 35)}

    # Save to a JSON file
    with open("../tools/3_indexing/propia_index.json", "w") as outfile:
        json.dump(data, outfile, indent=4)


def make_library_by_month(h=None, month_no=None):
    # List of thread arguments
    thread_args = [h] if h else ["inv", "lec", "lau", "ter", "sex", "non", "vis", "com"]


    # Create and start threads
    threads = []
    for args in thread_args:
        thread = threading.Thread(target=fill_dict, args=(args, month_no))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    print("All threads have finished.")


def sunday_to_saturday(filename, year, month, day, w) -> list:
    """  Makes dictionary with breviary data """
    new_elements = []

    try:
        # dzieli na słownik z listami stringów
        elements: list = tools.split_to_list(filename, year, month, day, w)
        if len(elements) > 0:
            for i, element in enumerate(elements):
                if re.findall(r"^(.*) (.*) ZWYKŁA (.*)$", element):
                    updated_text = re.sub(r'NIEDZIELA', 'SOBOTA', element)
                    new_elements.append(updated_text)
                else:
                    new_elements.append(element)

    except Exception as e:
        print(e)

    return new_elements


def fill_dict(hora_canonica, month_no):
    """  Makes dictionary with breviary data """
    years = ["24"]
    m_dict = defaultdict(dict)
    try:
        for year in years:
            for month in range(month_no, month_no + 1):
                for day in range(
                        1, calendar.monthrange(int(year), month)[1] + 1):

                    # Each level (year, month, day) is initialized
                    m_dict.setdefault(year, {}).setdefault(str(month), {}).setdefault(str(day), {})

                    for w in tools.range_of_memories_depth(20):
                        # dzieli na słownik z listami stringów
                        # scraped_str: list = tools.split_to_list(hora_canonica, year, month, day, w)

                        if hora_canonica == "vis":
                            # podmień Niedziela na Sobota dla nieszporów
                            elements: list = sunday_to_saturday(hora_canonica, year, str(month), str(day), w)
                        else:
                            # dzieli na słownik z listami stringów
                            elements: list = tools.split_to_list(hora_canonica, year, month, day, w)

                        if len(elements) > 0:
                            m_dict[year][str(month)][str(day)][w] = {}

                            for i, element in enumerate(elements):
                                if re.findall(r"^(.*),+\s\d{1,2}.*\s\d{4}$", element) and hora_canonica != "com":
                                    m_dict[year][str(month)][str(day)][w]["WEEKDAY"] = re.findall(r"^(.*),+\s\d{1,2}.*\s\d{4}$", element)[0]
                                # place of celebration
                                if re.findall(r"^.*,+\s\d{1,2}.*\s\d{4}$", element) and hora_canonica != "com":
                                    _location = location(elements, i)
                                    if _location:
                                        m_dict[year][str(month)][str(day)][w]["LOCATION"] = _location

                                # feast rank
                                if re.findall("^.*K. \u2020.*$", element) and hora_canonica != "com":
                                    _rank = rank(elements, i)
                                    if _rank:
                                        m_dict[year][str(month)][str(day)][w]["RANK"] = _rank

                                    # feast name
                                    if re.findall("^.*K. \u2020.*$", element) and hora_canonica != "com":
                                        m_dict[year][str(month)][str(day)][w]["OFFICIUM"] = conmemoration(hora_canonica, elements, i)

                                # make "hymn"
                                if re.findall("^.*HYMN$", element):
                                    m_dict[year][str(month)][str(day)][w]["HYMN"] = hymns(elements, i)

                                # make "psalmodia"
                                elif re.findall("^.*PSALMODIA.*$", element):
                                    if hora_canonica in ["lau", "vis", "lec", "inv"]:
                                        # search in new scope (from PSALMODIA)
                                        for j, prayer in enumerate(elements[i:]):

                                            # search ant indexes
                                            pattern_ants = "^.*([1-3]) ant.*$"
                                            val = re.findall(pattern_ants, prayer)

                                            if val:
                                                if val[0] == "1":
                                                    combined_txt = (combine(elements, j + i, r"^.*2 ant\..*$", (-1, 0)))
                                                elif val[0] == "2":
                                                    combined_txt = (combine(elements, j + i, r"^.*3 ant\..*$", (-1, 0)))
                                                    # combined_txt = "hi"
                                                elif val[0] == "3" and hora_canonica == "lec":
                                                    ini = j + i
                                                    combined_txt = "\n".join(elements[ini:])

                                                else:
                                                    combined_txt = (combine(elements, j + i, "^.*CZYTANIE.*$", (-1, 0)))

                                                m_dict[year][str(month)][str(day)][w][f"PSALM{val[0]}"] = combined_txt

                                    # psalmodia for "ter", "sex", "non"
                                    elif hora_canonica in ["ter", "sex", "non"]:
                                        for j, prayer in enumerate(elements[i:]):
                                            # search ant indexes Antyfony - LG tom IV: Niedziela II, str. 641-643; LG skrócone: wg tabeli stron
                                            pattern_ants = r"^.*(\bAntyfony - LG\b|\bAnt\.\b|[1|2|3] ant\.).*$"
                                            val = re.findall(pattern_ants, prayer)
                                            if val:
                                                if val[0] == "1 ant.":
                                                    combined_txt = (combine(elements, j + i, r"^.*2 ant\..*$", (-1, 0)))
                                                    key_name = "1"
                                                elif val[0] == "2 ant.":
                                                    combined_txt = (combine(elements, j + i, r"^.*3 ant\..*$", (-1, 0)))
                                                    key_name = "2"
                                                elif val[0] == "3 ant.":
                                                    combined_txt = (
                                                        combine(elements, j + i, "^.*CZYTANIE.*$", (-1, 0)))
                                                    key_name = "3"
                                                else:
                                                    combined_txt = minor_hour_psalm_solemnes(elements, i)
                                                    key_name = ""

                                                if combined_txt:
                                                    m_dict[year][str(month)][
                                                        str(day)][w][(f"PSALM"
                                                                      f"{key_name}")] = combined_txt

                                    elif hora_canonica == "com":
                                        combined_txt = combine(
                                            elements, i, "^.*CZYTANIE.*$",
                                            (0, 0))
                                        m_dict[year][str(month)][str(day)][w][
                                            "PSALMODIA"] = combined_txt

                                elif re.findall(r"^CZYTANIE.*$", element):
                                    # zbiera wersety luźne
                                    reading = readings(hora_canonica, elements, i)
                                    if reading:
                                        m_dict[year][str(month)][str(day)][w][
                                            "LECTURE"] = reading

                                elif re.findall(r"^I CZYTANIE.*$", element):
                                    # zbiera wersety luźne
                                    verse = verses(elements, i)
                                    if verse:
                                        m_dict[year][str(month)][str(day)][w][
                                            "VERSE"] = verse

                                    reading1_off = readings(hora_canonica, elements, i)

                                    if reading1_off:
                                        m_dict[year][str(month)][str(day)][w]["I READING"] = reading1_off

                                    responsorium = responsories(elements, i)
                                    if responsorium:
                                        m_dict[year][str(month)][str(day)][w]["I READING RESP"] = responsorium

                                elif re.findall(r"^CYKL DWULETNI.*$", element):
                                    reading1_2y = readings(hora_canonica, elements, i)

                                    if reading1_2y:
                                        m_dict[year][str(month)][str(day)][w]["I READING [2Y]"] = reading1_2y

                                elif re.findall(r"^II CZYTANIE.*$", element):
                                    # zbiera wersety luźne
                                    verse = verses(elements, i)
                                    if verse:
                                        m_dict[year][str(month)][str(day)][w]["VERSE"] = verse

                                    reading2_off = readings(hora_canonica, elements, i)

                                    if reading2_off:
                                        m_dict[year][str(month)][str(day)][w]["II READING"] = reading2_off

                                    responsorium2 = responsories(elements, i)
                                    if responsorium2:
                                        m_dict[year][str(month)][str(day)][w]["II READING RESP"] = responsorium2

                                elif re.findall(r"^MODLITWA.*$", element):
                                    # zbiera wersety luźne
                                    last_prayer = prayers(hora_canonica, elements, i)
                                    if last_prayer:
                                        m_dict[year][str(month)][str(day)][w]["PRAYER"] = last_prayer

                                elif hora_canonica == "inv" and re.findall(
                                        r"^.*Wszyscy: A usta moje.*$", element):
                                    m_dict[year][str(month)][str(day)][w]["PSALM"] = elements[i + 1]
                                    m_dict[year][str(month)][str(day)][w]["PSALM MOTIVE"] = elements[i + 2]
                                    m_dict[year][str(month)][str(day)][w]["CITATION"] = elements[i + 3]
                                    m_dict[year][str(month)][str(day)][w]["ANT"] = inv_antiphons(elements, i)

                                elif re.findall(r"^RESPONSORIUM KRÓTKIE.*$", element):

                                    short_responsory = responsories(elements, i)
                                    if short_responsory:
                                        m_dict[year][str(month)][str(day)][w]["RESPONSORY"] = (
                                            short_responsory)

                                elif re.findall("^.*PIEŚŃ ZACHARIASZA.*$", element):
                                    m_dict[year][str(month)][str(day)][w]["ZACHARY"] = (elements[i + 1] + " Ant. " + elements[i + 4])

                                elif re.findall("^.*PIEŚŃ MARYI.*$", element):
                                    m_dict[year][str(month)][str(day)][w]["MARIA"] = (elements[i + 1] + " Ant. " + elements[i + 4])

                                elif re.findall("^.*PRO\u015aBY.*$", element):
                                    m_dict[year][str(month)][str(day)][w]["PETITIONS"] = petitions(elements, i)

                print(f"Month {month}/{year}: Completed \u2714")
            print(f"Year {year}: Completed \u2714")

    except Exception as e:
        print(e)

    directory = f"3_indexing"
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(f"3_indexing/index_{hora_canonica}.json", "w") as s:
        json.dump(m_dict, s, indent=4)


def _make_propia():
    # List of thread arguments
    thread_args = ["lec", "lau", "vis"]

    # Create and start threads
    threads = []
    for args in thread_args:
        thread = threading.Thread(target=_make_propia, args=(args, None))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    print("All threads have finished.")


def make_propia():
    """  Makes dictionary with breviary data """
    make_propia_json()
    lg_dict = tools.open_json_file("../tools/3_indexing/propia_index.json")
    lit_year = ""
    # horas_canonicas = ["lau", "vis", "lec"]
    horas_canonicas = ["lec", "lau"]
    years = ["23", "24"]
    try:
        for hc in horas_canonicas:
            for year in years:
                for month in range(8, 12):
                    try:
                        for day in range(1, calendar.monthrange(int(year), month)[1] + 1):
                            keys = tools.search_for_keys(hc, year, month, day)
                            if keys:
                                try:
                                    for w in keys:
                                        weekday_no = ""
                                        # dzieli na słownik z listami stringów
                                        elements: list = tools.split_to_list(hc, year, month, day, w)

                                        if len(elements) > 0:
                                            week = 0
                                            for i, element in enumerate(elements):
                                                reg_str = re.findall(r"^(.*)\s(\btydzień Okresu Zwykłego\b).*$", element)
                                                if reg_str:
                                                    week = tools.roman_to_int(reg_str[0][0])
                                                reg_dom = re.findall(r"^(.*)\s(\bNIEDZIELA ZWYKŁA\b) (.*)$", element)
                                                if reg_dom:
                                                    week = tools.roman_to_int(reg_dom[0][0])
                                                    lit_year = reg_dom[0][2]
                                                reg_weekday = re.findall(r"^(.*),+\s\d{1,2}.*\s\d{4}$", element)
                                                if reg_weekday:
                                                    weekday_no = tools.map_weekdays(reg_weekday[0])
                                                if hc == "lec":
                                                    if re.findall(r"^.*(\bI\b) CZYTANIE.*$", element):
                                                        reading = readings(hc, elements, i)
                                                        if reading:
                                                            lg_dict[week][weekday_no][hc].update(reading)
                                                    if re.findall(r"^.*(\bII\b) CZYTANIE.*$", element):
                                                        reading = readings(hc, elements, i)
                                                        if reading:
                                                            lg_dict[week][weekday_no][hc].update(reading)
                                                    if re.findall(r"^MODLITWA.*$", element):
                                                        last_prayer = prayers(hc, elements, i)
                                                        if last_prayer:
                                                            lg_dict[week][weekday_no][hc]["prayer"] = last_prayer
                                                elif hc == "lau":
                                                    if re.findall(r"^.*MODLITWA.*$", element):
                                                        last_prayer = prayers(hc, elements, i)
                                                        if last_prayer:
                                                            lg_dict[week][weekday_no][hc]["prayer"] = last_prayer
                                                    if re.findall(r"^.*PIE\u015a\u0143 ZACHARIASZA.*$", element):
                                                        ant = canticle_anthiphones(elements, i)
                                                        if ant:
                                                            lg_dict[week][weekday_no][hc][f"ant {lit_year}"] = ant
                                                elif hc == "vis":
                                                    ant = canticle_anthiphones(elements, i)
                                                    if ant:
                                                        if weekday_no == "5":
                                                            lg_dict[week]["6"]["i vis"][f"ant {lit_year}"] = ant
                                                        elif weekday_no == "6":
                                                            lg_dict[week]["6"]["ii vis"][f"ant {lit_year}"] = ant
                                except KeyError:
                                    pass
                    except KeyError:
                        pass
                    print(f"Month {month}/{year}: Completed {hc} \u2714")
                print(f"Year {year}: Completed {hc} \u2714")
            print(f"{hc}: Completed ")

    except KeyError:
        pass

    directory = f"3_indexing"
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(f"3_indexing/propia_index.json", "w") as s:
        json.dump(lg_dict, s, indent=4)


def make_propia_json_file():
    # Load existing breviary data
    # lg_dict = tools.open_json_file("../tools/3_indexing/propia_index.json")
    lit_year = ""
    day = "?"
    horas_canonicas = ["lec", "lau"]
    years = ["23", "24"]
    lg_dict = {}
    try:
        for hc in horas_canonicas:  # ['lec', 'lau']
            for year in years:
                year_int = int(year)  # Ensure year is used as an integer
                for month in range(10, 11):
                    try:
                        for day in range(1, calendar.monthrange(year_int, month)[1] + 1):
                            keys = tools.search_for_keys(hc, year, month, day)
                            if keys:
                                for w in keys:
                                    weekday_no = ""
                                    elements = tools.split_to_list(hc, year, month, day, w)

                                    if elements:
                                        week = 0
                                        for i, element in enumerate(elements):
                                            reg_str = re.findall(r"^(.*)\s(\btydzień Okresu Zwykłego\b).*$", element)
                                            if reg_str:
                                                week = tools.roman_to_int(reg_str[0][0])
                                            reg_dom = re.findall(r"^(.*)\s(\bNIEDZIELA ZWYKŁA\b) (.*)$", element)
                                            if reg_dom:
                                                week = tools.roman_to_int(reg_dom[0][0])
                                                lit_year = reg_dom[0][2]
                                            reg_weekday = re.findall(r"^(.*),+\s\d{1,2}.*\s\d{4}$", element)
                                            if reg_weekday:
                                                weekday_no = tools.map_weekdays(reg_weekday[0])

                                            # Ensure 'lec' and 'lau' have separate branches in the dictionary
                                            lg_dict.setdefault(week, {}).setdefault(weekday_no, {}).setdefault(hc, {})

                                            if hc == "lec":
                                                if re.findall(r"^.*(\bI\b) CZYTANIE.*$", element):
                                                    reading = readings(hc, elements, i)
                                                    if reading:
                                                        lg_dict[week][weekday_no][hc].update(reading)
                                                if re.findall(r"^.*(\bII\b) CZYTANIE.*$", element):
                                                    reading = readings(hc, elements, i)
                                                    if reading:
                                                        lg_dict[week][weekday_no][hc].update(reading)
                                                if re.findall(r"^MODLITWA.*$", element):
                                                    last_prayer = prayers(hc, elements, i)
                                                    if last_prayer:
                                                        lg_dict[week][weekday_no][hc]["prayer"] = last_prayer

                                            elif hc == "lau":
                                                if re.findall(r"^.*MODLITWA.*$", element):
                                                    last_prayer = prayers(hc, elements, i)
                                                    if last_prayer:
                                                        lg_dict[week][weekday_no][hc]["prayer"] = last_prayer
                                                if re.findall(r"^.*PIEŚŃ ZACHARIASZA.*$", element):
                                                    ant = canticle_anthiphones(elements, i)
                                                    if ant:
                                                        lg_dict[week][weekday_no][hc][f"ant {lit_year}"] = ant

                    except KeyError as e:
                        print(f"KeyError for Month {month}/{year}: {e}")
                    except Exception as e:
                        print(f"Error processing {day}/{month}/{year} for {hc}: {e}")

                    print(f"Month {month}/{year}: Completed {hc} ✔")
                print(f"Year {year}: Completed {hc} ✔")
            print(f"{hc}: Completed ✔")

    except Exception as e:
        print(f"General error: {e}")

    # Ensure directory exists and write JSON data
    directory = "3_indexing"
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(f"{directory}/propia_index_10.json", "w") as s:
        json.dump(lg_dict, s, indent=4)


def canticle_anthiphones(elements, i):
    if re.findall(r"^.*PIE\u015a\u0143 ZACHARIASZA.*$", elements[i]):
        return elements[i + 4]

    elif re.findall(r"^.*PIE\u015a\u0143 MARYI.*$", elements[i]):
        if re.findall(r"^.*LG.*$", elements[i+1]):
            for x in range(10):
                if elements[i + x] == "albo:":
                    return elements[i + 4], elements[i + x + 1]
                else:
                    return elements[i + 4]

        else:
            for x in range(10):
                if elements[i + x] == "albo:":
                    return elements[i + 3], elements[i + x + 1]
                else:
                    return elements[i + 3]


def combine(elements, i, pattern, shift=(1, 0)):
    start_shift, end_shift = shift
    prayer_end = []

    for j, prayer in enumerate(elements[i:]):
        if pattern == "^.*Modlitwę Pańską.*$":
            start_shift = 0
        if re.findall(pattern, prayer):
            prayer_end.append(j)
    joined = ''
    try:
        element_list = elements[
                       i + 1 + start_shift:i + prayer_end[0] + end_shift]
        joined = '\n'.join(element_list)



    except IndexError:
        pass
    finally:
        return joined


def location(elements, i):
    if i != 0:
        return elements[0]


def conmemoration(filename, elements, i):
    if filename != "com":
        if filename == "vis":
            if elements[i - 2] == "I Nieszpory uroczysto\u015bci":
                return elements[i - 4]
        if elements[i - 1] in [
            "Wspomnienie dowolne",
            "Wspomnienie obowiązkowe",
            "Uroczystość",
            "Święto"
        ]:
            return elements[i - 2]
        else:
            return elements[i - 1]


def verses(elements, i: int):
    if elements[i - 5].startswith("Werset"):
        joined = "\n".join([
            elements[i - 5],
            elements[i - 4],
            elements[i - 3],
            elements[i - 2],
            elements[i - 1],
        ])
    else:
        joined = "\n".join([
            "Werset - ",
            elements[i - 4],
            elements[i - 3],
            elements[i - 2],
            elements[i - 1],
        ])
    return joined


def rank(elements, i):
    if elements[i - 1] in [
        "Wspomnienie dowolne",
        "Wspomnienie obowiązkowe",
        "Uroczystość",
        "Święto"
    ]:
        return f"{elements[i - 1]}"


def hymns(elements, i):
    if elements[i] == "HYMN":
        joined = ""
        for j, txt in enumerate(elements[i + 1:]):
            if txt == "PSALMODIA":
                break
            else:
                joined += txt + "\n"
        return joined


def psalmodia(elements, i):
    if elements[i] == "PSALMODIA":
        joined = ""
        for j, txt in enumerate(elements[i + 1:]):
            if txt == "PSALMODIA":
                break
            else:
                joined += txt + "\n"
        return joined


def petitions(elements, i):
    if elements[i] == "PRO\u015aBY":
        joined = ""
        for j, txt in enumerate(elements[i + 1:]):
            if txt.startswith("Modlitw\u0119 Pa\u0144sk\u0105 mo\u017cna"):
                break
            else:
                joined += txt + "\n"
        return joined


def readings(filename, elements, i):
    # print(scraped_str[i:])
    joined = ""
    stoper = 0
    a, b, c = None, None, None
    reg_readings = re.findall(r"^.*(\bI|II\b) CZYTANIE.*$", elements[i])
    if reg_readings:
        r_no = reg_readings[0]

        # Collect psalm information from scraped_str[i+1:i+4]
        if re.findall(r"^.*LG.*$", elements[i + 1]):
            psalm_info = elements[i + 2:i + 5]
        else:
            psalm_info = elements[i + 1:i + 4]

        if len(psalm_info) == 3:
            a, b, c = psalm_info

        # Find where the "RESPONSORIUM" starts and stop before it
        for j, txt in enumerate(elements[i + 4:]):
            if re.findall(r"^.*RESPONSORIUM.*$", txt):
                stoper = j + 4  # Adjust stoper relative to original i
                break

        joined = "\n".join(elements[i + 4:i + stoper])

        # Return result depending on presence of a, b, and c
        if all([a, b, c]):
            return {f"{r_no} reading".lower(): {
                "book": a,
                "sigla": b,
                "title": c,
                "reading": joined
            },
                f"{r_no} responsory".lower(): responsory(elements, i + stoper)}
        else:
            return {f"{r_no} reading".lower(): {
                "book": "",
                "sigla": "",
                "title": "",
                "reading": joined
            }, f"{r_no} responsory".lower(): responsory(elements, i + stoper)}

    # elif scraped_str[i] == "CYKL DWULETNI":
    #     for j, txt in enumerate(scraped_str[i + 1:]):
    #         if txt.startswith("RESPONSORIUM"):
    #             break
    #         else:
    #             joined += txt + "\n"
    # elif scraped_str[i] == "CZYTANIE" and filename in ["lau", "vis"]:
    #     for j, txt in enumerate(scraped_str[i + 1:]):
    #         if txt.startswith("RESPONSORIUM KRÓTKIE"):
    #             break
    #         else:
    #             joined += txt + "\n"
    # elif scraped_str[i] == "CZYTANIE" and filename in ["ter", "sex", "non"]:
    #     for j, txt in enumerate(scraped_str[i + 1:]):
    #         if txt.startswith("MODLITWA"):
    #             break
    #         else:
    #             joined += txt + "\n"
    #
    # return joined


def responsory(elements, stoper):
    for x in range(1, 7):
        if elements[stoper + 1] == "W.":
            w = elements[stoper + 2]
            k = elements[stoper + 4].split("W.")[0].strip()
            r = elements[stoper + 4].split("W.")[1].strip()
            return {"sigla": "", "W": w, "K": k, "R": r}
        else:
            sigla = elements[stoper + 1]
            w = elements[stoper + 3]
            k = elements[stoper + 5].split("W.")[0].strip()
            r = elements[stoper + 5].split("W.")[1].strip()
            return {"sigla": sigla, "W": w, "K": k, "R": r}


def responsories(elements, i):
    joined = ""
    if elements[i] == "I CZYTANIE":
        for j, txt in enumerate(elements[i + 1:]):
            if txt == "II CZYTANIE":
                break
            else:
                joined += txt + "\n"
    elif elements[i] == "II CZYTANIE":
        for j, txt in enumerate(elements[i + 1:]):
            if txt.startswith("Je\u015bli pragnie si\u0119"):
                pass
            elif txt.startswith("HYMN CIEBIE,"):
                break
            else:
                joined += txt + "\n"
    elif elements[i] == "RESPONSORIUM KRÓTKIE":
        joined = ""
        for j, prayer in enumerate(elements[i + 1:]):
            if prayer == "PIEŚŃ ZACHARIASZA":
                break
            else:
                joined += prayer + "\n"
        return joined


def minor_hour_psalm_solemnes(elements, i):
    if elements[i] == "PSALMODIA" and elements[i + 1] == "Ant.":
        new_list = elements[i + 1:]
        end_of_psalm = 0
        for j, elem in enumerate(new_list[1:]):
            if elem == "Ant.":
                end_of_psalm = j + 4
        z = "\n".join(elements[i + 1:i + end_of_psalm])
        return z
    elif elements[i] == "PSALMODIA" and elements[i + 1].startswith("Antyfony - LG"):
        new_list = elements[i + 1:]
        end_of_psalm = 0
        for j, elem in enumerate(new_list[1:]):
            if elem == "CZYTANIE":
                end_of_psalm = j + 3
        z = "\n".join(elements[i + 1:i + end_of_psalm])
        return z


def join_lecture(elements, i):
    for j in range(5):
        print(elements[i + j])


def prayers(hc, elements, i):
    starter = 0
    stoper = 0

    for j, prayer in enumerate(elements[i + 1:]):
        if hc == "lec":
            if re.findall(r"^.*Módlmy się.*$", elements[i + j]):
                starter = j

            if prayer.startswith("Nast\u0119pnie, przynajmniej w oficjum "):
                stoper = j
                break
            elif prayer.startswith("Jeśli kapłan lub diakon przewodniczy"):
                stoper = j
                break

        elif hc in ["lau", "vis"]:

            if re.findall(r"^.*MODLITWA.*$", elements[i + j]):
                starter = i + j

            if prayer.startswith("Nast\u0119pnie, przynajmniej w oficjum "):
                stoper = i + j
                break
            elif prayer.startswith("Jeśli kapłan lub diakon przewodniczy"):
                stoper = i + j
                break

    if hc == "lau":
        if re.findall(r"^.*LG.*$", elements[starter + 1]):
            return " ".join(elements[starter + 2:stoper + 1])
        else:
            return " ".join(elements[starter + 1:stoper + 1])
    elif hc == "lec":
        return " ".join(elements[i + 2 + starter:i + stoper])



def inv_antiphons(elements, i):
    if elements[i + 4] == "Ant.":
        return " ".join([elements[i + 4], elements[i + 5]])
    else:
        return " ".join([elements[i + 6], elements[i + 7]])


def index_lg(d, key_line='', diki=None):
    """
    Przeszukuje słownik rekurencyjnie, zapamiętuje ścieżkę kluczy
    i zapisuje wartości w słowniku 'diki', jeśli znajdzie wzorzec.
    """
    if diki is None:
        diki = {}  # Inicjalizacja słownika, jeśli nie został przekazany

    if isinstance(d, dict):
        # Iteracja przez klucze i wartości w słowniku
        for key, value in d.items():
            new_key_line = f"{key_line}-{key}"  # Tworzenie ścieżki kluczy
            if isinstance(value, dict):
                # Rekurencyjne przetwarzanie wartości, jeśli jest to słownik
                index_lg(value, new_key_line, diki)
            elif isinstance(value, str):
                start, end = 0, 0
                splited = value.split("\n")
                for i, x in enumerate(splited):
                    if re.findall(r"^.*HYMN.*$", x):
                        start = i + 1
                        for j, y in enumerate(splited[i:]):
                            if re.findall(r"^.*PSALMODIA.*$", y):
                                end = start + j - 1
                                break

                # Jeśli znaleziono przedział, przetwarzamy tekst
                if start < end:
                    ready = splited[start:end]

                    # Tworzenie struktury w 'diki'
                    diki[new_key_line.lstrip("-")] = {}

                    for o in range(9):
                        if splited[o].startswith("K. †"):
                            break
                        print(splited[o])
                    print("***")

                    diki[new_key_line.lstrip("-")]["hymn"] = "\n".join(ready)
                    diki[new_key_line.lstrip("-")]["feast"] = splited[2]
                    diki[new_key_line.lstrip("-")]["rank"] = splited[3]
                    diki[new_key_line.lstrip("-")]["class"] = "??"
                    diki[new_key_line.lstrip("-")]["where"] = splited[0]

                    # result = re.findall(r": ([^,]+),.*$", ready[0])
                    # # Tworzenie struktury w 'diki'
                    # diki[new_key_line.lstrip("-")] = {}
                    # if result:
                    #     for o in range(9):
                    #         if splited[o].startswith("K. †"):
                    #             break
                    #         if splited[o].isupper():
                    #             # Dodanie danych do słownika 'diki'
                    #             diki[new_key_line.lstrip("-")]["hymn"] = "\n".join(ready[1:])
                    #             diki[new_key_line.lstrip("-")]["feast"] = splited[o]
                    #             diki[new_key_line.lstrip("-")]["rank"] = splited[o + 1]
                    #             diki[new_key_line.lstrip("-")]["class"] = result[0]
                    #         if ":" in splited[o]:
                    #             diki[new_key_line.lstrip("-")]["where"] = splited[o]
                    # else:
                    #     diki[new_key_line.lstrip("-")]["hymn"] = "\n".join(ready)
                    #     diki[new_key_line.lstrip("-")]["feast"] = splited[2]
                    #     diki[new_key_line.lstrip("-")]["rank"] = splited[3]
                    #     diki[new_key_line.lstrip("-")]["class"] = "??"
                    #     diki[new_key_line.lstrip("-")]["where"] = splited[0]

    return diki




