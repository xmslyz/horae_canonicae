# amDg
# +JMJ
import datetime
import json
from creator import Skeleton

with open("base_files/index_inv.json", encoding="utf-8") as f:
    index = json.load(f)

with open("base_files/CONST.json", encoding="utf-8") as f:
    constans = json.load(f)

with open("base_files/invitatory.json", encoding="utf-8") as f:
    base = json.load(f)

with open("base_files/invitatorium_antifonarium.json", encoding="utf-8") as f:
    antiphones = json.load(f)

# officium_date = datetime.date.today()
# sk = Skeleton(officium_date)

my_list = []
for x in range(2012, 2030)[::3]:
    sk = Skeleton(datetime.date(x, 1, 1))
    my_list.append(sk.eas_start)

# print(my_list)

for y in my_list:
    sk = Skeleton(y)
    print(sk)
    print()
    # print(sk.current_psalter_week)
    # print(y)
    # print(sk.eas_start)
    # print(sk.sunday_dates)

# sk = Skeleton(datetime.date(2024, 2, 18))
# print(sk)


# inv skeleton
no_ant = False
cons = constans["inv"]
base = base["95"]

aperies = cons["APERIES"]
psalm_no = base["num"]
psalm_title = base["mot"]
psalm_cita = base["cit"]
ant = "antyfona"  # antiphones[creator.find_proper_week()]
estr = base["est"]

# print(aperies)
# print(psalm_no)
# print(psalm_title)
# print(psalm_cita)
# print(ant)
# for x in range(len(estr)):
#     print(estr[x])
#     if no_ant is False:
#         print(ant)
# if no_ant:
#     print(ant)








"""
Przewodniczący: † Panie, otwórz wargi moje.
Wszyscy: A usta moje będą głosić Twoją chwałę.

Psalm 24
Pan wkracza do świątyni
Bramy niebios zostały otwarte dla Chrystusa ze względu na wywyższenie Jego ludzkiej natury (św. Ireneusz)

Antyfona - LG tom IV: Poniedziałek III, str. 764; LG skrócone: Poniedziałek III, str. 964
Psalm - LG tom IV: Psalm 24, str. 490-491; LG skrócone: Psalm 24, str. 694

W wersji PREMIUM znajdziesz tutaj propozycje melodii Wezwania oraz przykładowe pliki mp3.

Ant. Przyjdźcie, uwielbiajmy Pana, / do którego należy ziemia i wszystko, co ją napełnia.

Do Pana należy ziemia i wszystko, co ją napełnia, *
świat cały i jego mieszkańcy.
Albowiem On go na morzach osadził *
i utwierdził ponad rzekami.

Ant. Przyjdźcie, uwielbiajmy Pana, / do którego należy ziemia i wszystko, co ją napełnia.

Kto wstąpi na górę Pana, *
kto stanie w Jego świętym miejscu?
Człowiek rąk nieskalanych i czystego serca, †
którego dusza nie lgnęła do marności *
i nie przysięgał kłamliwie.

Ant. Przyjdźcie, uwielbiajmy Pana, / do którego należy ziemia i wszystko, co ją napełnia.

On otrzyma błogosławieństwo od Pana *
i zapłatę od Boga, swego Zbawcy.
Oto pokolenie tych, którzy Go szukają, *
którzy szukają oblicza Boga Jakuba.

Ant. Przyjdźcie, uwielbiajmy Pana, / do którego należy ziemia i wszystko, co ją napełnia.

Bramy, podnieście swe szczyty, †
unieście się, odwieczne podwoje, *
aby mógł wkroczyć Król chwały!
"Któż jest tym Królem chwały?" †
Pan dzielny i potężny, *
Pan potężny w boju.

Ant. Przyjdźcie, uwielbiajmy Pana, / do którego należy ziemia i wszystko, co ją napełnia.

Bramy, podnieście swe szczyty, †
unieście się, odwieczne podwoje, *
aby mógł wkroczyć Król chwały!
"Któż jest tym Królem chwały?" *
Pan Zastępów, On jest Królem chwały.

Ant. Przyjdźcie, uwielbiajmy Pana, / do którego należy ziemia i wszystko, co ją napełnia.

Chwała Ojcu i Synowi, *
i Duchowi Świętemu.
Jak była na początku, teraz i zawsze, *
i na wieki wieków. Amen.

Ant. Przyjdźcie, uwielbiajmy Pana, / do którego należy ziemia i wszystko, co ją napełnia.

Jeśli psalm Wezwania ze swoją antyfoną ma poprzedzać Jutrznię, można go opuścić ze słusznej przyczyny.
"""



