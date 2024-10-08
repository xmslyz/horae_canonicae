# amDg
# +JMJ

import json
import re
from calendar import weekday
from random import random
import indexer

def make_ageda():
    with open("../litcalendar/10_2024.json", encoding="utf-8") as f:
        txt = json.load(f)
    with open("../litcalendar/anual_agenda.json", encoding="utf-8") as f:
        agenda = json.load(f)
        for day in range(1, 31):
            numerator = 1
            for i in txt.keys():
                try:
                    if txt[i]["date"] == str(day):
                        if txt[i]["feast"] == "Dzie\u0144 powszedni":
                            pass
                        elif re.findall(r"^.*(\bNiedziela Zwykła\b).*$", txt[i]["feast"]):
                            pass
                        else:
                            klasa = ''
                            if re.findall(r"^.*(\bm\u0119czennik\u00f3w|m\u0119czennic\b).*$", txt[i]["feast"]):
                                klasa += "MM|"
                            if re.findall(r"^.*(\bm\u0119czennika\b).*$", txt[i]["feast"]):
                                klasa += "M|"
                            if re.findall(r"^.*(\bdoktora Ko\u015bcio\u0142a\b).*$", txt[i]["feast"]):
                                klasa += "D|"
                            if re.findall(r"^.*(\bMaryi\b).*$", txt[i]["feast"]):
                                klasa += "NMP|"
                            if txt[i]["where"] is None:
                                where = "omnia"
                            else:
                                where = txt[i]["where"]
                            agenda["10"][str(day)][numerator] = {
                                "feast": txt[i]["feast"],
                                "rank": rank_mapper(txt[i]["feast_type"]),
                                "class": klasa,
                                "where": where,
                            }
                            numerator += 1
                except KeyError as e:
                    print("x", e)
    with open("../litcalendar/anual_agenda.json", "w", encoding="utf-8") as f:
        json.dump(agenda, f, indent=4)


def rank_mapper(rank):
    try:
        rank_map = {
            "\u015awi\u0119to": "F",
            "Wsp. obowi\u0105zkowe": "MO",
            "Wsp. dowolne": "ML",
            "Wsp. dodatkowe": "MA",
            "Uroczysto\u015b\u0107": "S",
            "Komem. dowolna": "KL"
        }

        return rank_map[rank]
    except KeyError:
        return ""


def clear_agenda():
    with open("anual_agenda_.json", encoding="utf-8") as f:
        agenda = json.load(f)
        for month in range(1, 13):
            for day in range(1, 32):
                try:
                    str_m = str(month)
                    str_d = str(day)
                    del agenda[str_m][str_d]["MF"]
                    del agenda[str_m][str_d]["OP"]
                except KeyError:
                    pass

    with open("anual_agenda.json", "w", encoding="utf-8") as f:
        json.dump(agenda, f, indent=4)


def scrap():
    with open("../tools/2_clensing/lau.json", encoding="utf-8") as f:
        lau = json.load(f)

    with open("../base_files/ot/ot_lau.json", encoding="utf-8") as f:
        ot_lau = json.load(f)

    with open("../base_files/common/common.json", encoding="utf-8") as f:
        common = json.load(f)

    with open("../base_files/propia/pro.json", encoding="utf-8") as f:
        pro = json.load(f)

    # new_dict["Z"].setdefault("lau", {}).setdefault("hymn", "")

    for year in ["23", "24"]:
        for month in range(1, 13):
            for day in range(1, 32):
                try:
                    scooped = lau[year][str(month)][str(day)]  # Access the nested dictionary for the given date
                    for key, value in scooped.items():  # Loop through the scooped dictionary

                        # If you want to match specific content, for example, "MĘCZENNIKÓW":
                        res = re.findall(r".*DZIEWICY.*", value)

                        # Debug output to check what's being matched
                        # Each level (year, month, day) is initialized
                        # m_dict.setdefault(year, {}).setdefault(str(month), {}).setdefault(str(day), {})

                        if res:
                            scraped_list = value.split("\n")
                            for i, content in enumerate(scraped_list):
                                if re.findall("^.*HYMN$", content):
                                    result = indexer.hymns(scraped_list, i).split("\n")
                                    if re.findall(r"^.*LG tom.*$", result[0]):
                                        print(year, month, day, key)
                                        print(result)
                                        if year == "24" and str(month) == "10" and str(day) == "15" and key == "p":
                                            # common["D"].setdefault("lau", {}).setdefault("hymn", "")
                                            # common["D"]["lau"]["hymn"] = "\n".join(result[1:])

                                            pro.setdefault(str(month), {}).setdefault(str(day), {}).setdefault("teresa", {}).setdefault("lau", {}).setdefault("hymn", "")
                                            pro[str(month)][str(day)]["teresa"]["lau"]["hymn"] = "\n".join(result[1:])



                except KeyError as ke:
                    # print(f"KeyError: {ke} - The key '{ke}' does not exist in the provided data structure.")
                    pass

    with open("../base_files/common/common.json", "w", encoding="utf-8") as f:
        json.dump(common, f, indent=4)

    with open("../base_files/propia/pro.json", "w", encoding="utf-8") as f:
        json.dump(pro, f, indent=4)


if __name__ == "__main__":
    scrap()
    # make_ageda()
