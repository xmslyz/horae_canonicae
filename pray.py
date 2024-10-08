# amDg
# +JMJ

import datetime
from creator import Officium
import main_hours as lg
from user_profile import User


def opis():
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
    ...


def start():
    # today = datetime.datetime.today().date()
    # off = Officium(today)

    other = datetime.date(2024, 10, 7)
    off = Officium(other)

    # inv = lg.Invitatory(off)
    # inv.pray()

    lau = lg.Morning(off)
    lau.pray()


if __name__ == "__main__":
    start()



