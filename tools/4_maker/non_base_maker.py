# amDg
# +JMJ

import datetime
import json
import re

from creator import Skeleton


def split_psalm(psalm_text):
    t = psalm_text.split("\n")
    if t[0] not in ["1 ant.", "2 ant.", "3 ant."]:
        return {
            "antifona": t[3],
            "psalm_index": t[4],
            "psalm_title": t[5],
            "psalm_comment": t[6],
            "psalm_txt": "\n".join(t[6:-1])
        }
    else:
        return {
            "antifona": t[1],
            "psalm_index": t[2],
            "psalm_title": t[3],
            "psalm_comment": t[4],
            "psalm_txt": "\n".join(t[5:-2])
        }

with open("index_non.json", encoding="utf-8") as f:
    index = json.load(f)

lg_file = "ot/ot_.json"

with open(lg_file, encoding="utf-8") as f:
    base_file = json.load(f)

days_map = {
    "Poniedziałek": "0",
    "Wtorek": "1",
    "Środa": "2",
    "Czwartek": "3",
    "Piątek": "4",
    "Sobota": "5",
    "Niedziela": "6"
}

psalter_map = {
    "II,": "2",
    "III,": "3",
    "IV,": "4",
    "I,": "1"
}

try:
    to_rip = ['HYMN', 'PSALM1', 'PSALM2', 'PSALM3', 'PSALM', 'LECTURE', 'PRAYER']

    days = [
        "Poniedziałek",
        "Wtorek",
        "Środa",
        "Czwartek",
        "Piątek",
        "Sobota",
        "Niedziela"
    ]
    for day in days:
        for rip in to_rip:
            rip = rip.lower()
            for i in ["23", "24"]:
                if i in index.keys():

                    for j in range(8, 12):
                        j_str = str(j)
                        if j_str in index[i].keys():

                            for k in range(1, 32):
                                k_str = str(k)
                                if k_str in index[i][j_str].keys():

                                    for m in ["x", "p", "w1", "w2", "w3", "w4", "w5", "w6", "w7", "w8", "w9", "w10"]:
                                        if m in index[i][j_str][k_str].keys():
                                            if rip.upper() in index[i][j_str][k_str][m]:
                                                try:
                                                    txt: str = index[i][j_str][k_str][m][rip.upper()]
                                                    hymn_spliter: str = index[i][j_str][k_str][m]["LECTURE"]
                                                    splited: list[str] = hymn_spliter.split(" ")
                                                    if day == "Niedziela":
                                                        print(splited)
                                                    psalter: str = splited[splited.index(day) + 1]
                                                    weekday: str = index[i][j_str][k_str][m]["WEEKDAY"]
                                                    off: str = index[i][j_str][k_str][m]["OFFICIUM"]
                                                    if day in splited:
                                                        if weekday == "Poniedziałek":
                                                            if rip == "psalm1":
                                                                base_file[psalter_map[psalter]]["0"][rip] = split_psalm(txt)
                                                            elif rip == "psalm2":
                                                                base_file[psalter_map[psalter]]["0"][rip] = split_psalm(txt)
                                                            elif rip == "psalm3":
                                                                base_file[psalter_map[psalter]]["0"][rip] = split_psalm(txt)
                                                            else:
                                                                base_file[psalter_map[psalter]]["0"][rip] = txt
                                                        if weekday == "Wtorek":
                                                            if rip == "psalm1":
                                                                base_file[psalter_map[psalter]]["1"][rip] = split_psalm(txt)
                                                            elif rip == "psalm2":
                                                                base_file[psalter_map[psalter]]["1"][rip] = split_psalm(txt)
                                                            elif rip == "psalm3":
                                                                base_file[psalter_map[psalter]]["1"][rip] = split_psalm(txt)
                                                            else:
                                                                base_file[psalter_map[psalter]]["1"][rip] = txt
                                                        if weekday == "Środa":
                                                            if rip == "psalm1":
                                                                base_file[psalter_map[psalter]]["2"][rip] = split_psalm(txt)
                                                            elif rip == "psalm2":
                                                                base_file[psalter_map[psalter]]["2"][rip] = split_psalm(txt)
                                                            elif rip == "psalm3":
                                                                base_file[psalter_map[psalter]]["2"][rip] = split_psalm(txt)
                                                            else:
                                                                base_file[psalter_map[psalter]]["2"][rip] = txt
                                                        if weekday == "Czwartek":
                                                            if rip == "psalm1":
                                                                base_file[psalter_map[psalter]]["3"][rip] = split_psalm(txt)
                                                            elif rip == "psalm2":
                                                                base_file[psalter_map[psalter]]["3"][rip] = split_psalm(txt)
                                                            elif rip == "psalm3":
                                                                base_file[psalter_map[psalter]]["3"][rip] = split_psalm(txt)
                                                            else:
                                                                base_file[psalter_map[psalter]]["3"][rip] = txt
                                                        if weekday == "Piątek":
                                                            if rip == "psalm1":
                                                                base_file[psalter_map[psalter]]["4"][rip] = split_psalm(txt)
                                                            elif rip == "psalm2":
                                                                base_file[psalter_map[psalter]]["4"][rip] = split_psalm(txt)
                                                            elif rip == "psalm3":
                                                                base_file[psalter_map[psalter]]["4"][rip] = split_psalm(txt)
                                                            else:
                                                                base_file[psalter_map[psalter]]["4"][rip] = txt
                                                        if weekday == "Sobota":
                                                            if rip == "psalm1":
                                                                base_file[psalter_map[psalter]]["5"][rip] = split_psalm(txt)
                                                            elif rip == "psalm2":
                                                                base_file[psalter_map[psalter]]["5"][rip] = split_psalm(txt)
                                                            elif rip == "psalm3":
                                                                base_file[psalter_map[psalter]]["5"][rip] = split_psalm(txt)
                                                            else:
                                                                base_file[psalter_map[psalter]]["5"][rip] = txt
                                                        elif weekday == "Niedziela":
                                                            if rip.lower() in ["psalm1", "psalm2", "psalm3", "psalm"]:
                                                                base_file[psalter_map[psalter]]["6"][rip.lower()] = split_psalm(txt)
                                                            else:
                                                                if rip.lower() not in base_file[psalter_map[psalter]]["6"].keys():
                                                                    base_file[psalter_map[psalter]]["6"][rip] = txt

                                                except ValueError as e:
                                                    # print(e, 11)
                                                    pass
                                                except KeyError as e:
                                                    # print(e, 22)
                                                    pass
                                                except Exception as e:
                                                    pass
                                                    # print(e, 33)

            #                 else:
            #                     print(
            #                         f"Key {k_str} not found in index[{i}][{j_str}]")
            #         else:
            #             print(f"Key {j_str} not found in index[{i}]")
            # else:
            #     print(f"Key {i} not found in index")
except KeyError as e:
    print(f"KeyError: {e}")

with open("ot/ot_non.json", "w", encoding="utf-8") as f:
    json.dump(base_file, f, indent=4, ensure_ascii=True)
