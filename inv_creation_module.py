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

officium_date = datetime.date.today()
sk = Skeleton(officium_date)

# inv skeleton
no_ant = True
cons = constans["inv"]
ant_map = {
    "1": "95", "2": "100", "3": "24", "4": "67"
}
aperies = cons["APERIES"]
current_week_str = str(sk.current_psalter_week)
mapped_value = ant_map.get(current_week_str)
base = base[mapped_value]
psalm_no = base["num"]
psalm_title = base["mot"]
psalm_cita = base["cit"]
ant = antiphones[str(sk.current_psalter_week)][str(sk.lg_day.weekday())]
estr = base["est"]

print(aperies)

print(psalm_no)
print(psalm_title)
print(psalm_cita)

print(ant)
for x in range(len(estr)):
    print(estr[x])
    if no_ant is False:
        print(ant)
if no_ant:
    print(ant)
