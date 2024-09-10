import calendar
import os.path
import re
import threading
import tools


def clear_data():
    # List of thread arguments
    thread_horas = ["inv", "lec", "lau", "ter", "sex", "non", "vis", "com"]

    # Create and start threads
    threads = []
    for hora in thread_horas:
        thread = threading.Thread(target=_delete_in_thread, args=(hora, None))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()


def _delete_in_thread(*args):
    # FORLOOP to remove all residence of junk in [0] index
    for _ in range(4):
        delete_junk(args[0])


def delete_junk(filename):
    years = ["23", "24"]
    # years = ["24"]
    filename_to_fullname = {
        "com": "Kompleta",
        "inv": "Wezwanie",
        "lau": "Jutrznia",
        "lec": "Godzina Czytań",
        "ter": "Modlitwa przedpołudniowa",
        "sex": "Modlitwa południowa",
        "non": "Modlitwa popołudniowa",
        "vis": "Nieszpory"
    }

    if filename in filename_to_fullname:
        fullname = filename_to_fullname[filename]
    else:
        fullname = "QWERTY"

    JUNK_1_CLASS = [
        "WERSJA PREMIUM:",
        "Przejdź do wersji premium",
        "Czym jest wersja premium?",
        "Dostęp do wersji premium",
        "Tu jesteś:",
        "ILG",
        "Menu:",
        "STRONA GŁÓWNA",
        "WESPRZYJ ROZWÓJ SERWISU",
        "TEKSTY ILG -",
        (
            "Kartka z kalendarzaCzytania liturgicznePatron dniaTabele "
            "stronWydanie czterotomoweWydanie skróconeMała LGBrewiarz dla "
            "świeckichLG dla osób świeckich 2000LG dla osób świeckich "
            "2003Teksty LG"
        ),
        "Teksty Monastycznej LG",
        "WPROWADZENIE DO LG",
        "LITURGIA HORARUM",
        "KALENDARZ LITURGICZNY",
        "DODATEK",
        "INDEKSY",
        "POMOC",
        "CZYTELNIA",
        "Wokół Liturgii Godzin",
        "Obchody liturgiczne",
        "Rocznice i wydarzenia",
        "Święci i błogosławieni",
        "Download",
        "ANKIETA",
        "Wesprzyj rozwój serwisu"
        "Możliwość wydruku dostępna wyłączniedla użytkowników wersji premium"
        "Pomoc",
        "Hymn |",
        "Psalmodia |",
        "Czytanie |",
        "Responsorium krótkie",
        "Pieśń Symeona |",
        "Modlitwa |",
        "Modlitwa",
        "Kolor szat:",
        "Antyfona do NMP",
        "W wersji PREMIUM znajdziesz tutaj propozycję melodii oraz plik mp3 z "
        "jej wykonaniem",
        "W wersji PREMIUM znajdziesz tutaj propozycje melodii Wezwania oraz "
        "przykładowe pliki mp3.",
        "TEKSTY ILG |",
        "OWLG |",
        "LITURGIA HORARUM |",
        "KALENDARZ LITURGICZNY |",
        "DODATEK |",
        "INDEKSY |",
        "Wesprzyj rozwój serwisu",
        "Módl się słuchając",
        "W wersji PREMIUMdostępne jest nagranie tej Godzinyw formacie MP3.",
        "Dowiedz się więcej...",
        "Teksty Liturgia Horarum",
        "I VesperæCompletorium",
        "Możliwość wydruku dostępna wyłączniedla użytkowników wersji premium",
        "W wersji PREMIUM dostępne jest nagranie tej Godziny w formacie MP3(w "
        "lewym górnym rogu strony).",
        "W wersji PREMIUM znajdziesz tutaj propozycję melodii oraz plik mp3 z "
        "jej wykonaniem.",
        "Kartka z kalendarzaPatron dniaTeksty LG",
        "Kartka z kalendarzaCzytania liturgiczneKomentarze do czytańPatron "
        "dniaTabele stronWydanie czterotomoweWydanie skróconeMała LGBrewiarz "
        "dla świeckichLG dla osób świeckich 2000LG dla osób świeckich "
        "2003Teksty LG",
        "Kartka z kalendarzaCzytania liturgiczneTeksty LG",
        "Wigilia tego obchoduJutrznia",
        "Invitatorium",
        "Officium lectionis",
        "Laudes matutinæ",
        "Tertia",
        "Sexta",
        "Nona",
        "VesperæCompletorium",
        "II VesperæCompletorium",
        "Kartka z kalendarzaCzytania liturgicznePatron dniaTeksty LG",
        "Kartka z kalendarzaPatron dniaTabele stronWydanie "
        "czterotomoweWydanie skróconeMała LGBrewiarz dla świeckichLG dla osób "
        "świeckich 2000LG dla osób świeckich 2003Teksty LG",
        "W tym miejscu przewidziany jest rachunek sumienia.We wspólnie "
        "odprawianym oficjum można użyć jednej z formuł aktu pokuty.",
        "W wersji PREMIUM znajdziesz tutaj link do papieskiej katechezy na "
        "temat tego psalmu.",
        "W wersji PREMIUM znajdziesz tutaj link do papieskiej katechezy na "
        "temat tej pieśni.",
        "W wersji PREMIUMdostępne jest nagranie tej Godzinyw formacie "
        "MP3(opracowane przy użyciusyntezatora mowy).",
        "Kartka z kalendarzaTeksty LG",
        "Kartka z kalendarzaCzytania liturgicznePatron dniaTabele "
        "stronWydanie czterotomoweWydanie skróconeBrewiarz dla świeckichLG "
        "dla osób świeckich 2000LG dla osób świeckich 2003Teksty LG",
        "Kartka z kalendarzaTabele stronWydanie czterotomoweWydanie "
        "skróconeMała LGBrewiarz dla świeckichLG dla osób świeckich 2000LG "
        "dla osób świeckich 2003Teksty LG",
        "- KOMENTARZ",
        "- ROZWAŻANIE",
        "Dalej - Kompleta",
        "Dalej - Modlitwa południowa, popołudniowa lub Nieszpory",
        "Dalej - Modlitwa popołudniowa lub Nieszpory",
        "Dalej - Nieszpory",
        "Dalej - Godzina Czytań lub Jutrznia",
        "Tekst oficjalny",
        "Tekst ludowy",
        "W wersji PREMIUM znajdziesz tutaj wprowadzenie do niniejszego "
        "czytania.",
        "W wersji PREMIUM dostępne jest nagranie tej Godziny w formacie MP3("
        "lewy górny róg strony).",
        "Jeżeli poniżej nie wyświetliły się teksty czytań i Te Deum, kliknij "
        "tutaj i przeładuj tę stronę(dotyczy głównie użytkowników urządzeń "
        "mobilnych).",
        "Hymn |",
        "Psalmodia |",
        "I Czytanie |",
        "Responsorium",
        "II Czytanie |",
        "Responsorium |",
        "Te Deum | Modlitwa",
        "Pomoc",
        "Pieśń Zachariasza |",
        "Prośby |",
        "Modlitwa w ciągu dnia:przedpołudniowa",
        "Modlitwa w ciągu dnia:popołudniowa",
        "Modlitwa w ciągu dnia:południowa",
        "Pieśń Maryi |"

    ]
    JUNK_3_CLASS = [
        "Wezwanie",
        "Godzina Czytań",
        "Jutrznia",
        "Modlitwa przedpołudniowa",
        "Modlitwa południowa",
        "Modlitwa popołudniowa",
        "Nieszpory",
        "I Nieszpory",
        "II Nieszpory",
        "Kompleta",
    ]

    scraped_dir = "1_scrapping"
    scraped_path = f"{scraped_dir}/{filename}.json"

    clensed_dir = "2_clensing"
    clensed_path = f"{clensed_dir}/{filename}.json"

    if not os.path.exists(clensed_dir):
        os.makedirs(clensed_dir)

    try:
        jsdic = tools.open_json_file(scraped_path)
        for year in years:
            for month in range(1, 13):
                for day in range(1, calendar.monthrange(
                        int(year), month)[1] + 1):
                    print(month, day, filename)
                    for w in tools.range_of_memories_depth(10):
                        cleared_str = ''
                        try:
                            raw_data = jsdic[year][str(month)][str(day)][w]

                            # Regular expression to match the DD.MM.YYYY format
                            patterns = [r"\b\d{2}\.\d{2}\.\d{4}\b",
                                        r"\u00A0"
                                        ]

                            for pattern in patterns:
                                # whipe all occurrences of the date
                                raw_data = re.sub(pattern, '', raw_data)

                            splited = raw_data.split("\n")

                            # # eliminate irregular format in web data
                            # re.findall(r"^\d{2}.\d{2}.\d{4}$", splited)

                            # eliminate
                            if re.findall(
                                    rf"^.*{fullname}$", splited[0]):
                                splited.pop(0)

                            for line in splited:
                                if (
                                        line.strip() not in JUNK_1_CLASS and
                                        line.strip() not in JUNK_3_CLASS and
                                        line != "" and
                                        line != "\n\n" and
                                        not line.strip().startswith(
                                            "Teksty ILG - ")
                                ):
                                    cleared_str += re.sub(
                                        r'\n+', '\n', re.sub(
                                            r'\r', '', line)) + "\n"

                            cleared_str = cleared_str.split("\n")
                            second = ''
                            for line in cleared_str:
                                if line != "":
                                    second += line.strip() + "\n"

                            jsdic[year][str(month)][str(day)][w] = second

                        except KeyError:
                            pass

        tools.save_json_file(clensed_path, jsdic)

    except Exception as e:
        print(e)
