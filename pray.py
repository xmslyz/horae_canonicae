# amDg
# +JMJ

import datetime
from pickle import PROTO

from creator import Officium
import main_hours as lg
from user_profile import User


"""
TOM IV
ECC 1430
NMP 1455
NMPS 1481

A 1494

MM 1508
M 1527
P 1549
D 1579
V 1587

VS 1608
MS 1634
    Z 1656 VS+ | MS+
    DM 1663 VS+ | MS+
    ED 1667 VS+ | MS+
"""


if __name__ == "__main__":
    # today = datetime.datetime.today().date()
    # off = Officium(today)

    other = datetime.date(2024, 9, 7)
    for x in range(3):
        off = Officium(other, 6, x)
        pray = lg.Morning(off)
        pray.with_inv = True
        pray.no_ant = True
        pray.default_inter = False
        pray.pater_intro = True
        pray.joined = True
        print(pray)
        print(pray.opening())
        print(pray.hymn())
        print(pray.psalmodia())
        print(pray.readings())
        print(pray.responsory())
        print(pray.canticle())
        print(pray.paternoster())
        print(pray.intercessions())
        print(pray.prayer())
        print(pray.dismisal())





