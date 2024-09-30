# amDg
# +JMJ

import datetime
from creator import Propia
import main_hours as lg
from main_hours import Hours, Evening
import user_profile



def pray():
    # today = datetime.datetime.today().date()
    # pp = Propia(today)
    # other = datetime.date(2024, 9, 17)
    # pp = Propia(other)


    for i in range(1, 31):
        print(i)
        other = datetime.date(2024, 10, i)
        pp = Propia(other)

    # while True:
    #     prompt = input(
    #         f"Brewiarz:\n"
    #         f"[1] Wezwanie\n"
    #         f"[2] Jutrznia\n"
    #         f"[3] Jutrznia z Godziną Czytań\n"
    #         f"[4] Godzina Czytań\n"
    #         f"[5] Modlitwa mniejsza\n"
    #         f"[6] Nieszpory\n"
    #         f"[7] Nieszpory z Godziną Czytań\n"
    #         f"[8] Kompleta\n"
    #         "----------------\n"
    #         f"[0] Zakończ\n"
    #         f" >>> "
    #     )
    #
    #     match prompt:
    #         case "1":
    #             inv = lg.Invitatory(pp)
    #             inv.pray()
    #         case "2":
    #             lau = lg.Morning(pp)
    #             lau.pray()
    #         case "3":
    #             print("\"Jutrznia z Godziną Czytań\" is not yet implemented.")
    #         case "4":
    #             lec = lg.Readings(pp)
    #             lec.pray()
    #         case "5":
    #             mh = lg.Daytime(pp)
    #             mh.pray()
    #         case "6":
    #             vis = lg.Evening(pp)
    #             vis.pray()
    #         case "7":
    #             print("\"Nieszpory z Godziną Czytań\" is not yet implemented.")
    #         case "8":
    #             com = lg.Night(pp)
    #             com.pray()
    #         case "0":
    #             print("Exiting...")
    #             exit()
    #         case _:
    #             print("Invalid input. Please enter a number from 0 to 8.")


if __name__ == "__main__":
    pray()
