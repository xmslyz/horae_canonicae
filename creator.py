# amDg
import json
import calendar


def ask_for_place():
    return "poza Polską"


def ask_for_congregation():
    return None


def find_officium():
    # look for a day of week
    # look for a liturgical week
    # look in general calendar
    ...


def main_menu():
    tu = {
        "LOC": None,
        "ORG": None,
        "DIOC": None,
        "HOUSE": None
    }

    while True:
        user_input = input("Znajdujesz się w Polsce [t/n]? >>> ").lower()
        if user_input == "t":
            tu["LOC"] = True
            user_input = input("W [a]rchidiecezji, [d]iecezji, "
                               "[o]rdynariacie? >>> "
                               "").lower()
            if user_input == "a":
                i = input(
                    "[1]  białostockiej\t\t"
                    "[2]  częstochowskiej\t"
                    "[3]  gdańskiej\t\t"
                    "[4]  gnieźnieńskiej\n"
                    "[5]  katowickiej\t\t"
                    "[6]  krakowskiej\t\t"
                    "[7]  lubelskiej\t\t"
                    "[8]  łódzkiej\n"
                    "[9]  poznańskiej\t\t"
                    "[10] przemyskiej\t\t"
                    "[11] szczecińsko-kamieńskiej\n"
                    "[12] warmińskiej\t\t"
                    "[13] warszawskiej\t\t"
                    "[14] wrocławskiej\n >>> ",
                )

                archi = [
                    "białostockiej",
                    "częstochowskiej",
                    "gdańskiej",
                    "gnieźnieńskiej",
                    "katowicki",
                    "krakowskiej",
                    "lubelskiej",
                    "łódzkiej",
                    "poznańskiej",
                    "przemyski",
                    "szczecińsko-kamieńskiej",
                    "warmińskiej",
                    "warszawskiej",
                    "wrocławskiej"]
                tu["DIOC"] = archi[int(i) - 1]
                tu["ORG"] = "archidiecezji "
            elif user_input == "d":
                i = input(
                    "[1]  bielsko-żywieckiej\t\t\t"
                    "[2]  bydgoskiej\t\t\t\t"
                    "[3]  drohiczyńskiej\t\t"
                    "[4]  elbląskiej\t\t\t\t\t\t"
                    "[5]  ełckiej\n"
                    "[6]  gliwickiej\t\t\t\t\t"
                    "[7]  kaliskiej\t\t\t\t"
                    "[8]  kieleckiej\t\t\t"
                    "[9]  koszalińsko-kołobrzeskiej\t\t"
                    "[10] legnickiej\n"
                    "[11] łomżyńskiej\t\t\t\t"
                    "[12] łowickiej\t\t\t\t"
                    "[13] opolskiej\t\t\t"
                    "[14] pelplińskiej\t\t\t\t\t"
                    "[15] płockiej\n"
                    "[16] radomskiej\t\t\t\t\t"
                    "[17] rzeszowskiej\t\t\t"
                    "[18] sandomierskiej\t\t"
                    "[19] siedleckiej\t\t\t\t\t"
                    "[20] sosnowieckiej\n"
                    "[21] świdnickiej\t\t\t\t"
                    "[22] tarnowskiej\t\t\t"
                    "[23] toruńskiej\t\t\t"
                    "[24] warszawsko-praskiej\t\t\t"
                    "[25] włocławskiej\n"
                    "[26] zamojsko-lubaczowskiej\t\t"
                    "[27] zielonogórsko-gorzowskiej\n >>> ")

                dioc = [
                    "bielsko-żywieckiej",
                    "bydgoskiej",
                    "drohiczyńskiej",
                    "elbląskiej",
                    "ełckiej",
                    "gliwickiej",
                    "kaliskiej",
                    "kieleckiej",
                    "koszalińsko-kołobrzeskiej",
                    "legnickiej",
                    "łomżyńskiej",
                    "łowickiej",
                    "opolskiej",
                    "pelplińskiej",
                    "płockiej",
                    "radomskiej",
                    "rzeszowskiej",
                    "sandomierskiej",
                    "siedleckiej",
                    "sosnowieckiej",
                    "świdnickiej",
                    "tarnowskiej",
                    "toruńskiej",
                    "warszawsko-praskiej",
                    "włocławskiej",
                    "zamojsko-lubaczowskiej",
                    "zielonogórsko-gorzowskiej"
                ]
                tu["DIOC"] = dioc[int(i) - 1]
                tu["ORG"] = "diecezji "
            elif user_input == "o":
                tu["DIOC"] = "Ordynariacie Polowym"
                tu["ORG"] = ""
        elif user_input == "n":
            tu["LOC"] = False
            tu["DIOC"] = "człowiekiem!"
            tu["ORG"] = "wolnym "


        break

    print(f"Jesteś w {tu['ORG']}{tu['DIOC']}!")


if __name__ == "__main__":
    main_menu()
