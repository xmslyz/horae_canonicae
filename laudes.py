# amDg
# +JMJ

import datetime
import json
from creator import Skeleton

with open("base_files/CONST.json", encoding="utf-8") as f:
    constans = json.load(f)

officium_date = datetime.date.today()
sk = Skeleton(officium_date)

lau_const = constans["lau"]
print(lau_const.keys())

lord_come = lau_const["BEGINING"]
hymn = lau_const["HYMN"]
psalmody = lau_const["PSALMODY"]
lecture = lau_const["LECTURE"]
responsory = lau_const["SHORT_RESPONSORY"]
zacariah = lau_const["ZACARIAH"]
sigla_zac = lau_const["SIGLA_ZAC"]
txt_zacariah = lau_const["TXT_ZACARIAH"]
paternoster = lau_const["OUR_FATHER"]
prayer = lau_const["PRAYER"]
# ---------------------
print(lord_come)
print(hymn)
print(psalmody)
print(lecture)
print(responsory)
print(zacariah)
print(sigla_zac)
print(txt_zacariah)
print(paternoster)
print(prayer)
"""
BEGINING
RUBRICA001
HYMN
meta_hymn = ""
txt_hymn = ""
PSALMODY
meta_ant_psalmody = ""
meta_psalms_psalmody = ""
ant_1 = "1 ant."
ant_1_txt = ""
psalm_1_title = ""
psalm_1_quote = ""
psalm_1_bible = ""
psalm_1 = ""
ANT
ant_1_txt
ant_02 = "2 ant."
ant_2_txt = ""
psalm_2_title = ""
psalm_2_quote = ""
psalm_2_bible = ""
psalm_2 = ""
ANT
ant_2_txt = ""
ant_03 = "3 ant."
ant_3_txt = ""
psalm_3_title = ""
psalm_3_quote = ""
psalm_3_bible = ""
psalm_3 = ""
ANT
ant_3_txt = ""
LECTURE
meta_lecture = ""
sigle_lecture = ""
txt_lecture = ""
SHORT_RESPONSORY
meta_responsory = ""
txt_responsory = ""
ZACARIAH
meta_zacariah = ""
ant_zacariah0 = "Ant."
ant_zacariah = ""
TXT_ZACARIAH
ANT
ant_zacariah
PETITIONS
meta_petitions = ""
txt_petitions = ""
OUR_FATHER
PRAYER
meta_prayer = ""
txt_prayer = ""
END

"""

