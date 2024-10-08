# amDg
# +JMJ

import datetime
import json
import re

from creator import Skeleton


def split_psalm(psalm_text):
    try:
        t = psalm_text.split("\n")
        end = 0
        for i, tt in enumerate(t):
            if re.findall(r"^.*Ant\..*$", tt):
                end = i

        if len(t) <= 1:
            return 1
        else:
            if t[2] in ["I", "II", "III"]:
                return {
                    "antifona": t[1],
                    "psalm_index": "",
                    "psalm_title": "",
                    "psalm_comment": "",
                    "psalm_txt": "\n".join(t[2:end]),
                    "werse": "\n".join(t[end + 3:end + 7])
                }
            else:
                return {
                    "antifona": t[1],
                    "psalm_index": t[2],
                    "psalm_title": t[3],
                    "psalm_comment": t[4],
                    "psalm_txt": "\n".join(t[5:-2])
                }
    except IndexError as ie:
        print(ie)
        pass


def base_maker():
    with open("index_lec.json", encoding="utf-8") as f:
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
        to_rip = ['HYMN', 'PSALM1', 'PSALM2', 'PSALM3', 'VERSE', 'I READING', 'II READING', 'PRAYER', 'I READING [2Y]']

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
                for i in ["23", "24"]:
                    if i in index.keys():

                        for j in range(8, 12):
                            j_str = str(j)
                            if j_str in index[i].keys():

                                for k in range(1, 32):
                                    k_str = str(k)
                                    if k_str in index[i][j_str].keys():

                                        for m in ["x", "p", "w1", "w2", "w3", "w4", "w5", "w6", "w7", "w8", "w9"]:
                                            if m in index[i][j_str][k_str].keys():
                                                if rip in index[i][j_str][k_str][m].keys():
                                                    try:
                                                        txt: str = index[i][j_str][k_str][m][rip]
                                                        hymn_spliter: str = index[i][j_str][k_str][m]["HYMN"]
                                                        splited: list[str] = hymn_spliter.split(" ")
                                                        psalter: str = splited[splited.index(day) + 1]
                                                        weekday: str = index[i][j_str][k_str][m]["WEEKDAY"]
                                                        if day in splited:

                                                            if weekday == "Poniedziałek":
                                                                if rip.lower() in ["psalm1", "psalm2", "psalm3"]:
                                                                    base_file[psalter_map[psalter]]["0"][rip.lower()] = split_psalm(txt)
                                                                else:
                                                                    if rip.lower() not in base_file[psalter_map[psalter]]["0"].keys():
                                                                        base_file[psalter_map[psalter]]["0"][rip.lower()] = txt

                                                            if weekday == "Wtorek":
                                                                if rip.lower() in ["psalm1", "psalm2", "psalm3"]:
                                                                    base_file[psalter_map[psalter]]["1"][rip.lower()] = split_psalm(txt)
                                                                else:
                                                                    base_file[psalter_map[psalter]]["1"][rip.lower()] = txt

                                                            if weekday == "Środa":
                                                                if rip.lower() in ["psalm1", "psalm2", "psalm3"]:
                                                                    base_file[psalter_map[psalter]]["2"][rip.lower()] = split_psalm(txt)
                                                                else:
                                                                    base_file[psalter_map[psalter]]["2"][rip.lower()] = txt

                                                            if weekday == "Czwartek":
                                                                if rip.lower() in ["psalm1", "psalm2", "psalm3"]:
                                                                    base_file[psalter_map[psalter]]["3"][rip.lower()] = split_psalm(txt)
                                                                else:
                                                                    base_file[psalter_map[psalter]]["3"][rip.lower()] = txt

                                                            if weekday == "Piątek":
                                                                if rip.lower() in ["psalm1", "psalm2", "psalm3"]:
                                                                    base_file[psalter_map[psalter]]["4"][rip.lower()] = split_psalm(txt)
                                                                else:
                                                                    base_file[psalter_map[psalter]]["4"][rip.lower()] = txt

                                                            if weekday == "Sobota":
                                                                if rip.lower() in ["psalm1", "psalm2", "psalm3"]:
                                                                    base_file[psalter_map[psalter]]["5"][rip.lower()] = split_psalm(txt)
                                                                else:
                                                                    base_file[psalter_map[psalter]]["5"][rip.lower()] = txt

                                                            elif weekday == "Niedziela":
                                                                if rip.lower() in ["psalm1", "psalm2", "psalm3"]:
                                                                    base_file[psalter_map[psalter]]["6"][rip.lower()] = split_psalm(txt)
                                                                else:
                                                                    base_file[psalter_map[psalter]]["6"][rip.lower()] = txt

                                                    except ValueError as e:
                                                        # print(e)
                                                        pass
                                                    except KeyError as e:
                                                        # print(e)
                                                        pass
                #                 else:
                #                     print(
                #                         f"Key {k_str} not found in index[{i}][{j_str}]")
                #         else:
                #             print(f"Key {j_str} not found in index[{i}]")
                # else:
                #     print(f"Key {i} not found in index")
    except KeyError as e:
        print(f"KeyError: {e}")
    with open("ot/ot_lec.json", "w", encoding="utf-8") as f:
        json.dump(base_file, f, indent=4, ensure_ascii=True)


if __name__ == "__main__":
    base_maker()
