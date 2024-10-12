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
    pp = Officium(ddate, 6)

    while True:
        prompt = input(
            f"Wybierz:\n"
            f"[1] Wezwanie\n"
            f"[2] Jutrznia\n"
            f"[3] Jutrznia z Godziną Czytań\n"
            f"[4] Godzina Czytań\n"
            f"[5] Modlitwa mniejsza\n"
            f"[6] Nieszpory\n"
            f"[7] Nieszpory z Godziną Czytań\n"
            f"[8] Kompleta\n"
            "----------------\n"
            f"[0] Zakończ\n"
            f" >>> "
        )

        match prompt:
            case "1":
                inv = lg.Invitatory(pp)
                print(inv)
            case "2":
                lau = lg.Morning(pp)
                print(lau)
            case "3":
                print("\"Jutrznia z Godziną Czytań\" is not yet implemented.")
            case "4":
                lec = lg.Readings(pp)
            case "5":
                mh = lg.Daytime(pp)
            case "6":
                vis = lg.Evening(pp)
                print(vis)
            case "7":
                print("\"Nieszpory z Godziną Czytań\" is not yet implemented.")
            case "8":
                com = lg.Night(pp)
            case "0":
                print("Exiting...")
                exit()
            case _:
                print("Invalid input. Please enter a number from 0 to 8.")




# finished in 778 main_hours
# 1 >lau -> ?
# 2 i vis | ii vis ??







