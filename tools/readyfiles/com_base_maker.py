# amDg
# +JMJ

import datetime
import json
import re

from creator import Skeleton


def split_psalm(psalm_text):
    t = psalm_text.split("\n")
    return {
        "antifona": t[1],
        "psalm_index": t[2],
        "psalm_title": t[3],
        "psalm_comment": t[4],
        "psalm_txt": "\n".join(t[5:-2])
    }


with open("index_com.json", encoding="utf-8") as f:
    index = json.load(f)

lg_file = "ot/ot_c.json"

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

try:
    to_rip = ['HYMN', 'PSALMODIA', 'LECTURE', 'RESPONSORY', 'PRAYER']


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
                                                    for d in days:
                                                        if rip == "hymn":
                                                            print(txt)
                                                        base_file[days_map[d]][rip] = "\n".join(txt.split("\n")[1:])

                                                except ValueError as e:
                                                    print(e, 11)
                                                    pass
                                                except KeyError as e:
                                                    print(e, 22)
                                                    pass
                                                except Exception as e:
                                                    print(e, 33)

except KeyError as e:
    print(f"KeyError: {e}")

with open("ot/ot_com.json", "w", encoding="utf-8") as f:
    json.dump(base_file, f, indent=4, ensure_ascii=True)
