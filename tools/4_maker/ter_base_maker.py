# amDg
# +JMJ

import datetime
import json
import re

from creator import Skeleton


def clean_line(txt):
    # LG tom IV: Piątek I, str. 603; LG skrócone: Piątek I, str. 803
    t = txt.split("\n")
    # print(t)
    try:
        search = re.findall(r"^.*(Ant\..*)$", t[0])
        if search:
            if search[0]:
                return search[0] + "\n"
            #
        else:
            return "\n".join(t[1:])
    except Exception as e:
        print(e)

    # return txt


def split_petitions(text):
    t = text.split("\n")
    try:
        pp = {
            "intro": t[1],
            "resp": t[2]

        }
        t_spec = t[3:-1]
        px: int = int(len(t_spec) / 3)
        kk, ii = 0, 1
        for x in range(px):
            insert = x + 1
            pp[f"pet{insert}"] = {
                "k": t_spec[kk],
                "w": t_spec[ii]
            }
            kk += 3
            ii += 3

        return pp

    except Exception as ee:
        print(ee)


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

with open("index_ter.json", encoding="utf-8") as f:
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
                                                    psalter: str = splited[splited.index(day) + 1]
                                                    weekday: str = index[i][j_str][k_str][m]["WEEKDAY"]
                                                    off: str = index[i][j_str][k_str][m]["OFFICIUM"]
                                                    if day in splited:
                                                        if weekday == day:
                                                            if rip.lower() in ["psalm1", "psalm2", "psalm3"]:
                                                                base_file[psalter_map[psalter]][days_map[day]][rip.lower()] = split_psalm(txt)
                                                            elif rip.lower() in ["petitions"]:
                                                                base_file[psalter_map[psalter]][days_map[day]][rip.lower()] = split_petitions(txt)
                                                            else:
                                                                if rip.lower() not in base_file[psalter_map[psalter]][days_map[day]].keys():
                                                                    base_file[psalter_map[psalter]][days_map[day]][rip.lower()] = clean_line(txt)

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

with open("ot/ot_daytime_psalter.json", "w", encoding="utf-8") as f:
    json.dump(base_file, f, indent=4, ensure_ascii=True)
