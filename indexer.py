import json
import re
import threading
from collections import defaultdict
import calendar
import tools


def make_library_by_month():
    # List of thread arguments
    thread_args = ["inv", "lec", "lau", "ter", "sex", "non", "vis", "com"]
    # thread_args = ["lec"]

    # Create and start threads
    threads = []
    for args in thread_args:
        thread = threading.Thread(target=fill_dict, args=(args, None))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    print("All threads have finished.")


def fill_dict(filename, _):
    """  Makes dictionary with breviary data """
    years = ["23", "24"]
    m_dict = defaultdict(dict)

    try:
        for year in years:
            for month in range(9, 13):
                for day in range(
                        1, calendar.monthrange(int(year), month)[1] + 1
                ):
                    print(month, day)
                    # Each level (year, month, day) is initialized
                    m_dict.setdefault(year, {}).setdefault(str(month),
                                                           {}).setdefault(
                        str(day), {})

                    for w in tools.range_of_memories_depth(10):
                        # dzieli na słownik z listami stringów
                        elements: list = tools.split_to_list(filename, year,
                                                             month, day, w)
                        if elements:
                            m_dict[year][str(month)][str(day)][w] = {}
                            for i, element in enumerate(elements):
                                # place of celebration
                                if re.findall(r"^.*,+\s\d{1,2}.*\s\d{4}$",
                                              element) and filename != "com":
                                    _location = location(elements, i)
                                    if _location:
                                        m_dict[year][str(month)][str(day)][w][
                                            "LOCATION"] = _location
                                # feast rank
                                if re.findall(
                                        "^.*K. \u2020.*$", element
                                ) and filename != "com":
                                    _rank = rank(elements, i)
                                    if _rank:
                                        m_dict[year][str(month)][str(day)][w][
                                            "RANK"] = _rank
                                # feast name
                                if (re.findall("^.*K. \u2020.*$", element) and
                                        filename != "com"):
                                    m_dict[year][str(month)][str(day)][w][
                                        "OFFICIUM"] = conmemoration(filename,
                                                                    elements,
                                                                    i)
                                # make "hymn"
                                if re.findall("^.*HYMN$", element):
                                    m_dict[year][str(month)][str(day)][w][
                                        "HYMN"] = hymns(elements, i)

                                # make "psalmodia"
                                elif re.findall("^.*PSALMODIA.*$", element):
                                    if filename in ["lau", "vis", "lec", "inv"]:
                                        # search in new scope (from PSALMODIA)
                                        for j, prayer in enumerate(
                                                elements[i:]):
                                            # search ant indexes
                                            pattern_ants = "^.*([1-3]) ant.*$"
                                            val = re.findall(pattern_ants,
                                                             prayer)
                                            if val:
                                                if val[0] == "1":
                                                    combined_txt = (
                                                        combine(
                                                            elements, j + i,
                                                            r"^.*2 ant\..*$",
                                                            (-1, 0)))
                                                elif val[0] == "2":
                                                    combined_txt = (
                                                        combine(
                                                            elements, j + i,
                                                            r"^.*3 ant\..*$",
                                                            (-1, 0)))
                                                elif (val[0] == "3" and
                                                      filename == "lec"):
                                                    combined_txt = (
                                                        combine(
                                                            elements,
                                                            j + i,
                                                            r"^.*(Werset|K.).*$",
                                                            (-1, 0)))
                                                else:
                                                    combined_txt = (
                                                        combine(
                                                            elements, j + i,
                                                            "^.*CZYTANIE.*$",
                                                            (-1, 0)))
                                                m_dict[year][str(month)][
                                                    str(day)][w][
                                                    f"PS{val[0]}"
                                                ] = combined_txt

                                    # psalmodia for "ter", "sex", "non"
                                    elif filename in ["ter", "sex", "non"]:
                                        for j, prayer in enumerate(
                                                elements[i:]):
                                            # search ant indexes
                                            pattern_ants = (
                                                r"^.*(\bAnt\.|\b[1|2|3] ant\.).*$")
                                            val = re.findall(pattern_ants,
                                                             prayer)
                                            if val:
                                                if val[0] == "1 ant.":
                                                    combined_txt = (
                                                        combine(
                                                            elements, j + i,
                                                            r"^.*2 ant\..*$",
                                                            (-1, 0)))
                                                    key_name = "1"
                                                elif val[0] == "2 ant.":
                                                    combined_txt = (
                                                        combine(
                                                            elements, j + i,
                                                            r"^.*3 ant\..*$",
                                                            (-1, 0)))
                                                    key_name = "2"
                                                elif val[0] == "3 ant.":
                                                    combined_txt = (
                                                        combine(
                                                            elements, j + i,
                                                            "^.*CZYTANIE.*$",
                                                            (-1, 0)))
                                                    key_name = "3"
                                                else:
                                                    combined_txt = minor_hour_psalm_solemnes(
                                                        elements, i)
                                                    key_name = ""

                                                if combined_txt:
                                                    m_dict[year][str(month)][
                                                        str(day)][w][(f"PS"
                                                                      f"{key_name}")] = combined_txt
                                    elif filename == "com":
                                        combined_txt = combine(
                                            elements, i, "^.*CZYTANIE.*$",
                                            (0, 0))
                                        m_dict[year][str(month)][str(day)][w][
                                            "PSALMODIA"] = combined_txt

                                elif re.findall(r"^CZYTANIE.*$", element):
                                    # zbiera wersety luźne
                                    reading = readings(filename, elements, i)
                                    if reading:
                                        m_dict[year][str(month)][str(day)][w][
                                            "READING"] = reading

                                elif re.findall(r"^I CZYTANIE.*$", element):
                                    # zbiera wersety luźne
                                    verse = verses(elements, i)
                                    if verse:
                                        m_dict[year][str(month)][str(day)][w][
                                            "VERSE"] = verse

                                    reading1_off = readings(filename,
                                                            elements, i)

                                    if reading1_off:
                                        m_dict[year][str(month)][str(day)][w][
                                            "I READING"] = reading1_off

                                    responsorium = responsories(elements, i)
                                    if responsorium:
                                        m_dict[year][str(month)][str(day)][w][
                                            "I READING RESP"] = responsorium

                                elif re.findall(r"^CYKL DWULETNI.*$", element):
                                    reading1_2y = readings(filename,
                                                           elements, i)

                                    if reading1_2y:
                                        m_dict[year][str(month)][str(day)][w][
                                            "I READING [2Y]"] = reading1_2y

                                elif re.findall(r"^II CZYTANIE.*$", element):
                                    # zbiera wersety luźne
                                    verse = verses(elements, i)
                                    if verse:
                                        m_dict[year][str(month)][str(day)][w][
                                            "VERSE"] = verse

                                    reading2_off = readings(filename,
                                                            elements, i)

                                    if reading2_off:
                                        m_dict[year][str(month)][str(day)][w][
                                            "II READING"] = reading2_off

                                    responsorium2 = responsories(elements, i)
                                    if responsorium2:
                                        m_dict[year][str(month)][str(day)][w][
                                            "II READING RESP"] = responsorium2

                                elif re.findall(r"^MODLITWA.*$", element):
                                    # zbiera wersety luźne
                                    last_prayer = prayers(elements, i)
                                    if last_prayer:
                                        m_dict[year][str(month)][str(day)][w][
                                            "PRAYER"] = last_prayer

                                elif filename == "inv" and re.findall(
                                        r"^.*Wszyscy: A usta moje.*$", element):
                                    m_dict[year][str(month)][str(day)][w][
                                        "PSALM"] = elements[i + 1]
                                    m_dict[year][str(month)][str(day)][w][
                                        "PSALM MOTIVE"] = elements[i + 2]
                                    m_dict[year][str(month)][str(day)][w][
                                        "CITATION"] = elements[i + 3]
                                    m_dict[year][str(month)][str(day)][w][
                                        "ANT"] = inv_antiphons(elements, i)

                                elif re.findall(r"^RESPONSORIUM KRÓTKIE.*$", element):

                                    short_responsory = responsories(elements, i)
                                    if short_responsory:
                                        m_dict[year][str(month)][str(day)][w][
                                            "SHORT RESPONSORY"] = (
                                            short_responsory)

                                elif re.findall("^.*PIEŚŃ ZACHARIASZA.*$", element):
                                    m_dict[year][str(month)][str(day)][w][
                                        "CANTICLE ANT"] = (elements[i+1] +
                                                           " Ant. " +
                                                           elements[i+4])

                                elif re.findall("^.*PIEŚŃ MARYI.*$", element):
                                    m_dict[year][str(month)][str(day)][w][
                                        "CANTICLE ANT"] = (elements[i+1] +
                                                           " Ant. " +
                                                           elements[i+4])

                                elif re.findall("^.*PRO\u015aBY.*$", element):
                                    m_dict[year][str(month)][str(day)][w][
                                        "PETITIONS"] = petitions(elements, i)

    except Exception as e:
        print(e)

    with open(f"3_indexing/index_{filename}.json", "w") as s:
        json.dump(m_dict, s, indent=4)


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
        joined = "/n".join([
            elements[i - 5],
            elements[i - 4],
            elements[i - 3],
            elements[i - 2],
            elements[i - 1],
        ])
    else:
        joined = "/n".join([
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
    joined = ""
    if elements[i] == "I CZYTANIE":
        for j, txt in enumerate(elements[i + 1:]):
            if txt == "RESPONSORIUM":
                break
            else:
                joined += txt + "\n"
    elif elements[i] == "II CZYTANIE":
        for j, txt in enumerate(elements[i + 1:]):
            if txt == "RESPONSORIUM":
                break
            else:
                joined += txt + "\n"
    elif elements[i] == "CYKL DWULETNI":
        for j, txt in enumerate(elements[i + 1:]):
            if txt.startswith("RESPONSORIUM"):
                break
            else:
                joined += txt + "\n"
    elif elements[i] == "CZYTANIE" and filename in ["lau", "vis"]:
        for j, txt in enumerate(elements[i + 1:]):
            if txt.startswith("RESPONSORIUM KRÓTKIE"):
                break
            else:
                joined += txt + "\n"
    elif elements[i] == "CZYTANIE" and filename in ["ter", "sex", "non"]:
        for j, txt in enumerate(elements[i + 1:]):
            if txt.startswith("MODLITWA"):
                break
            else:
                joined += txt + "\n"

    return joined


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
    if elements[i] == "PSALMODIA" and elements[i + 1] == "Ant.  ":
        joined = ""
        for j, prayer in enumerate(elements[i:]):
            if prayer == "CZYTANIE":
                break
            elif prayer == "PSALMODIA":
                pass
            else:
                joined += prayer + "\n"
        return joined


def join_lecture(elements, i):
    for j in range(5):
        print(elements[i + j])


def prayers(elements, i):
    joined = ""
    for j, prayer in enumerate(elements[i + 1:]):
        if prayer.startswith("Nast\u0119pnie, przynajmniej w oficjum "):
            break
        elif prayer.startswith("Jeśli kapłan lub diakon przewodniczy"):
            break
        else:
            joined += prayer + "\n"
    return joined


def inv_antiphons(elements, i):
    if elements[i + 4] == "Ant.":
        return " ".join([elements[i + 4], elements[i + 5]])
    else:
        return " ".join([elements[i + 6], elements[i + 7]])
