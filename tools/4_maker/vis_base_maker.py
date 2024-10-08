# amDg
# +JMJ

import datetime
import json
import re


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
            temp = ""
            for t in t[1:]:
                if not t.startswith("PIEŚŃ"):
                    temp += t + "\n"
                else:
                    break

            return temp

    except Exception as e:
        print(e)


def split_petitions(text):
    t = text.split("\n")
    try:
        pp = {
            "intro": t[2],
            "resp": t[3]

        }
        t_spec = t[4:-1]
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
    return {
        "antifona": t[1],
        "psalm_index": t[2],
        "psalm_title": t[3],
        "psalm_comment": t[4],
        "psalm_txt": "\n".join(t[5:-2])
    }


def process_psalm(base_file, psalter_map, psalter, weekday_number, rip, txt):
    """
    Helper function to process psalms and assign them to the correct weekday.
    """
    if rip in ["psalm1", "psalm2", "psalm3"]:
        base_file[psalter_map[psalter]][str(weekday_number)][rip] = split_psalm(txt)
    else:
        base_file[psalter_map[psalter]][str(weekday_number)][rip] = txt

    return base_filevis_base_maker.py


with open("index_vis.json", encoding="utf-8") as f:
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
    to_rip = ['HYMN', 'PSALM1', 'PSALM2', 'PSALM3', 'LECTURE', 'RESPONSORY', 'PETITIONS', 'PRAYER', "MARIA"]

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
                                                    hymn_spliter: str = index[i][j_str][k_str][m]["HYMN"]
                                                    splited: list[str] = hymn_spliter.split(" ")
                                                    psalter: str = splited[splited.index(day) + 1]
                                                    weekday: str = index[i][j_str][k_str][m]["WEEKDAY"]
                                                    # if day in splited:
                                                    if weekday == day:
                                                        if rip.lower() in ["psalm1", "psalm2", "psalm3"]:
                                                            base_file[psalter_map[psalter]][days_map[day]][rip.lower()] = split_psalm(txt)
                                                        elif rip.lower() in ["petitions"]:
                                                            base_file[psalter_map[psalter]][days_map[day]][rip.lower()] = split_petitions(txt)
                                                        else:
                                                            if rip.lower() not in base_file[psalter_map[psalter]][days_map[day]].keys():
                                                                base_file[psalter_map[psalter]][days_map[day]][rip.lower()] = clean_line(txt)
                                                    elif weekday == "Sobota":
                                                        if rip.lower() in ["psalm1", "psalm2", "psalm3"]:
                                                            base_file[psalter_map[psalter]][days_map["Sobota"]][rip.lower()] = split_psalm(txt)
                                                        elif rip.lower() in ["petitions"]:
                                                            base_file[psalter_map[psalter]][days_map["Sobota"]][rip.lower()] = split_petitions(txt)
                                                        else:
                                                            if rip.lower() not in base_file[psalter_map[psalter]][days_map["Sobota"]].keys():
                                                                base_file[psalter_map[psalter]][days_map["Sobota"]][rip.lower()] = clean_line(txt)


                                                except ValueError as e:
                                                    # print(e, 11)
                                                    pass
                                                except KeyError as e:
                                                    print(e, 22)
                                                    pass
                                                except Exception as e:
                                                    print(e, 33)
                                # else:
                                # print(f"Key {k_str} not found in index[{i}][{j_str}]")
#                         else:
#                             print(f"Key {j_str} not found in index[{i}]")
#                 else:
#                     print(f"Key {i} not found in index")
except KeyError as e:
    print(f"KeyError: {e}")

with open("ot/ot_vis.json", "w", encoding="utf-8") as f:
    json.dump(base_file, f, indent=4, ensure_ascii=True)
