# amDg
# +JMJ

import datetime
from creator import Propia
import main_classes as lg
from main_classes import Hours, Evening


def pray():
    today = datetime.datetime.today().date()
    pp = Propia(today)

    while True:
        prompt = input(
            f"Brewiarz:\n"
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
                inv.pray()
            case "2":
                lau = lg.Morning(pp)
                lau.pray()
            case "3":
                print("\"Jutrznia z Godziną Czytań\" is not yet implemented.")
            case "4":
                lec = lg.Readings(pp)
                lec.pray()
            case "5":
                now = datetime.datetime.now()
                print(f"Current time: {now}")
            case "6":
                vis = lg.Evening(pp)
                vis.pray()
            case "7":
                print("\"Nieszpory z Godziną Czytań\" is not yet implemented.")
            case "8":
                com = lg.Night(pp)
                com.pray()
            case "0":
                print("Exiting...")
                exit()
            case _:
                print("Invalid input. Please enter a number from 0 to 8.")


if __name__ == "__main__":
    pray()
