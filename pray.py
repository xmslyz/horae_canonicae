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


def test():
    o = datetime.date(2024, 9, 7)
    for x in range(3):
        of = Officium(o, 6, x)
        p = lg.Morning(of)
        # p = lg.Readings(of)
        p.with_inv = True
        p.no_ant = True
        p.default_inter = False
        p.pater_intro = True
        p.joined = True
        print(p)
        print(p.opening())
        print(p.hymn())
        print(p.psalmodia())
        print(p.verse())
        print(p.readings())
        print(p.canticle())
        print(p.paternoster())
        print(p.intercessions())
        print(p.prayer())
        print(p.dismisal())


if __name__ == "__main__":
    ddate = datetime.datetime.today().date()
    # ddate = datetime.date(2024, 9, 7)
    off = Officium(ddate, 6)
    # pray = lg.Invitatory(off)
    pray = lg.Morning(off)
    pray.joined = True
    # pray.pater_intro = True
    print(pray)



# finished in 778 main_hours
# 1 >lau -> ?
# 2 i vis | ii vis ??







