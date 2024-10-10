# amDg
# +JMJ

import abc
import inspect
import datetime
import json
import logging
import os
import pathlib
import random
from abc import ABC
from pickle import PROTO
from random import choice

from colorama import Fore, Style

filename = os.path.basename(__file__).split('.')[0]
logger_dir = pathlib.Path.cwd() / f'__{filename}.log'
logger = logging.getLogger(__name__)
f_handler = logging.FileHandler(str(logger_dir), delay=True)
f_handler.setLevel(logging.WARNING)
f_format = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s() - %(message)s')
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)

TEST = True
# print("context:", inspect.stack()[0].function, "| line:", inspect.stack()[0].lineno) if TEST else None


class Hours:
    def __init__(self, officium):
        self.office = officium
        self.const = self.get_const()
        self.psalter_week = str(officium.current_psalter_week)
        self.weekday_no = str(officium.lg_date.weekday())

        self.__joined = False
        self.__with_inv = True
        self.__is_lent = False
        self.__full = True
        self.__clasic_td = True
        self.no_ant = False  # if False invitatory has only ant in begining and end
        self.ask_always = False  # will always ask you when more than 1 option
        self.solo = True
        self.will_be_sung = False
        self.hour = None
        self.check_for_propia()

    @staticmethod
    def get_const():
        with open("library/cons.json", encoding="utf-8") as f:
            return json.load(f)

    def get_base(self):
        season = self.office.season
        try:
            if season.startswith("ot"):
                with open(f"base_files/{season[:-1]}/{season[:-1]}_{self.hour}.json", encoding="utf-8") as f:
                    return json.load(f)
            else:
                with open(f"base_files/{season}/{season}_{self.hour}.json", encoding="utf-8") as f:
                    return json.load(f)

        except FileNotFoundError as e:
            logger.error(e)
            raise Exception

    @staticmethod
    def get_common():
        with open(f"base_files/common/common.json", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def get_propia():
        with open("base_files/propia/pro.json", encoding="utf-8") as f:
            return json.load(f)

    def check_optional(self, entry) -> str | dict:
        """
        Checks if the dictionary has multiple keys (optional texts). If so, returns a random choice.
        Otherwise, returns the only key's value. If `entry` is a string, returns it as is.
        """
        if isinstance(entry, dict):
            # as for now, cases from common M
            if [x for x in entry.keys() if x.startswith("#")] and self.office.commons[0] == "M":
                return self.hashed_options(entry)
            elif [x for x in entry.keys() if x.isdigit()]:
                return self.numeric_options(entry)
            else:
                # Only one key in the dictionary, return its value
                return entry

        elif isinstance(entry, str):
            return entry
        elif not entry:
            return f"*** no text for today in database ***"
        else:
            logger.error(f"Entry not dictionary nor a string but {type(entry)}")
            raise TypeError("Entry must be a dictionary or a string.")

    @staticmethod
    def numeric_options(entry):
        try:
            # Choose a random key from the dictionary
            random_key = choice([x for x in entry.keys() if x.isdigit()])
            print(f"[check optional] -> got [no. {random_key}] | total number of optional texts available ({len(entry)})")
            return entry[random_key]

        except Exception as e:
            logger.exception(e)
            raise Exception

    def hashed_options(self, entry):
        # Choose a correct key from the dictionary
        try:
            return entry[f"#{self.office.subclass}"]

        except KeyError:
            return self.numeric_options(entry)

        except Exception as e:
            logger.exception(e)
            raise Exception

    def check_for_propia(self):
        month = self.office.lg_date.month
        day = self.office.lg_date.day
        propia = self.get_propia()
        try:
            if self.office.feast in propia[str(month)][str(day)].keys():
                return True

        except KeyError:
            return False

        except Exception as e:
            logger.exception(e)

    def get_proper_text(self, off_part_name=None) -> dict | str:
        """
        Retrieves the proper prayer text based on the office date, feast, hour, and optional part name like "hymn" or "prayer".

        Args:
            off_part_name (str, optional): The specific part of the office for which to retrieve the prayer text.
                                           If None, retrieves all dictionary for a specific hour.

        Returns:
            str or None: The appropriate prayer text if found, or None if the text cannot be located.

        Logic:
        - First, it checks if the `propia` is available.
        - If `propia` is available, it tries to return the relevant text from the `propia_base` dictionary.
        - If `propia` is not available, it falls back to the psalter (seasonal) prayers and may mix in common prayers.
        - The user’s slider choice may affect which text is chosen if multiple sources are available.
        """

        def get_propia_text():
            """
            Retrieves the text from the propia (specific feast day prayers).
            Returns None if the text is not found in `propia_base`.
            """
            try:
                # Get the base text for the date, feast, and hour
                text = self.propia_base[str(self.office.lg_date.month)][str(self.office.lg_date.day)][self.office.feast].get(self.hour)

                # If a specific office part is requested, attempt to retrieve it
                if not off_part_name:
                    return text
                else:
                    if isinstance(text, dict):
                        return text.get(off_part_name, "empty")
                    else:
                        return "empty"

            except KeyError:
                # Return None if no matching text is found
                return None

            except Exception as e:
                logger.exception(e)

        def get_psalter_text():
            """
            Retrieves the text from the psalter (seasonal prayers), possibly with common prayer texts mixed in.
            If the common prayer is available, the user’s slider setting may affect the final selection.
            """
            # Retrieve the psalter text for the current week and weekday
            psalter = self.season_base[self.psalter_week][self.weekday_no]
            psalter_part = psalter if not off_part_name else psalter.get(off_part_name, None)

            try:
                # Try to retrieve common prayers for the current feast
                if self.office.commons:
                    common = self.get_common()[self.office.commons[0]].get(self.hour, "@")

                    # If a specific office part is requested, attempt to retrieve it
                    if off_part_name:
                        if isinstance(common, dict):
                            common = common.get(off_part_name, f"*** no {off_part_name} for today in database ***")
                        else:
                            logger.debug("common is not a dictionary")

                    # Use the user's slider choice to decide between a psalter and common prayer
                    return self.office.user.slider_choice(psalter_part, common)

                # if there are no commons for a day, return psalter text
                else:
                    return psalter_part

            except TypeError:
                # If there's an error retrieving common prayers, return psalter text
                logger.warning(
                    "There's an error retrieving common prayers from:\n"
                    f"{self.office.commons} | "
                    f"{self.office.rank} | "
                    f"{self.office.feast} | "
                    f"{self.office.subclass} --> returning psalter text"
                )
                return psalter_part

            except Exception as e:
                logger.exception(e)

        # First check if we can use the propia prayers
        if self.check_for_propia():
            propia = get_propia_text()
            return propia if propia != "empty" else get_psalter_text()
        else:
            #
            # Otherwise, use the psalter or common prayers
            return get_psalter_text()

    @abc.abstractmethod
    def opening(self):
        """ """

    def hymn(self):
        """
        [lau & lec]
        0-6 OT  : from a psalter.
        S & F   : from propia | common
        M       : if not propia -> choice (common | psalter)

        """
        h = self.get_proper_text("hymn")
        hymn = self.check_optional(h)
        fomated_hymn = self.format_hymn(hymn)
        return f"\u2731 HYMN \u2731\n{fomated_hymn}\n\n"

    def format_hymn(self, hymn):
        try:
            lines = hymn.split("\n")
            new_str = ''

            for line in lines:
                if line and line[0].isdigit():
                    new_str += line[0] + "\n" + line[2:] + "\n"
                else:
                    new_str += line + "\n"

            return self.coloured_hymn(new_str)

        except IndexError as ie:
            logger.exception(ie)
            print(f"{Fore.RED}Ocurred error while formating. Returned original format{Style.RESET_ALL}")
            return hymn

        except Exception as e:
            logger.exception(e)
            return 'Ocurred error during formating'

    @staticmethod
    def coloured_hymn(hymn: str) -> str:
        coloured_txt = ''
        next_line = None
        lines = hymn.split("\n")
        for i, line in enumerate(lines):
            if line.isdigit() and i != next_line:
                next_line = i + 1
                spacer = "" if i == 0 else "\n"
                coloured_txt += (
                        spacer + Fore.YELLOW + line + Style.RESET_ALL + " " + lines[next_line] + "\n"
                )
            elif i != next_line:
                coloured_txt += line + "\n"

            else:
                pass

        return coloured_txt.strip()

    @abc.abstractmethod
    def psalmodia(self):
        """
        [lau]
        0-6 OT  : psalter
        S & F   : psalms from psalter[1][6]
                : antiphons from propia | common
        M       : propia if not propia

        [lec]
        0-6     : psalter
        S & F   : propia
        M       : psalter if not propia

        """
        psalmody = "\u2731 PSALMODIA \u2731\n"
        ps = self.get_proper_text()

        for i, psalm in enumerate(["psalm1", "psalm2", "psalm3"], 1):
            psalmody += self._psalm(ps[psalm], i)

        return psalmody

    def _psalm(self, psalm, i):
        """ """
        ant = psalm["antifona"] + "\n"
        psalm = self.checking_psalms(psalm, i)  # checking if shoudn't be solemn psalm

        ind = psalm.get("psalm_index", "") + "\n" if len(psalm.get("psalm_index", "")) > 0 else ""
        tit = psalm.get("psalm_title", "") + "\n" if len(psalm.get("psalm_title", "")) > 0 else ""
        com = psalm.get("psalm_comment", "") + "\n" if len(psalm.get("psalm_comment", "")) > 0 else ""
        txt = psalm.get("psalm_txt", "") + "\n"
        indented_txt = self.indent_psalm(txt)

        return (
                Fore.YELLOW + "Ant. " + Style.RESET_ALL + ant +
                Fore.LIGHTRED_EX + ind +
                Fore.LIGHTYELLOW_EX + tit +
                Fore.LIGHTCYAN_EX + com +
                Style.RESET_ALL + indented_txt.rstrip() + "\n" +
                Fore.YELLOW + "Ant. " + Style.RESET_ALL + ant + "\n" +
                Style.RESET_ALL
        )

    @staticmethod
    def indent_psalm(txt):
        indented = ''
        txt_splited = txt.split("\n")
        indent = True
        cross = 0
        extra_line = ""
        for i in range(len(txt_splited)):
            if txt_splited[i] in ["I", "II", "III"]:
                indent = not indent
                cross = i
                extra_line = "\n"
            elif txt_splited[i].endswith("*"):
                if cross + 1 == i:
                    extra_line = ""
                    pass
                else:
                    indent = not indent
                    extra_line = ""
            elif txt_splited[i].endswith("†"):
                indent = not indent
                cross = i
                extra_line = ""

            spacer = "\t" if indent else ""
            indented += f"{extra_line}{spacer}{txt_splited[i]}{extra_line}\n"

        return indented

    def checking_psalms(self, psalm, i):
        # for Feasts and Solemnities (and some propias) psalms are taken from Sunday of 1st week of psalter
        if self.rank in ["F", "S"] or psalm.get("solemn"):
            psalm = self.get_base()["1"]["6"][f"psalm{i}"]
        else:
            psalm = self.get_base()[self.psalter_week][self.weekday_no][f"psalm{i}"]
        return psalm

    @abc.abstractmethod
    def readings(self):
        """ """

    def formated_reading(self, text, reading_no):
        try:
            maper = {"i reading": "I CZYTANIE", "ii reading": "II CZYTANIE"}

            title = text.get("title") + "\t" if text.get("title") != "" else ""
            sigla = text.get("sigla") + "\n" if text.get("sigla") != "" else ""
            comment = text.get("comment") + "\n\n" if text.get("comment") != "" else "\n"
            reading = self.check_optional(text.get("txt")) + "\n\n"

            formated_text = (
                Fore.LIGHTRED_EX + f"{maper[reading_no]}\n" + Style.RESET_ALL +
                title + Fore.LIGHTRED_EX + sigla + Fore.LIGHTRED_EX + comment +
                Style.RESET_ALL + reading +
                Fore.LIGHTRED_EX + "RESPONSORIUM\t" + text["responsory sigla"] + "\n" +
                Style.RESET_ALL + f"{self.colour_responsory(text["responsory txt"])}\n"
            )
            return formated_text

        except Exception as e:
            logger.exception(e)
            print(f"{Fore.RED}Ocurred error while formating.")
            return ""


    @staticmethod
    def colour_lecture(txt: str) -> str:
        sigla, lecture, *excess = txt.split("\n")
        return Fore.YELLOW + sigla + "\n" + Style.RESET_ALL + lecture

    @abc.abstractmethod
    def responsory(self):
        """ """

    @staticmethod
    def colour_responsory(res: str) -> str:
        txt = ""
        try:
            if isinstance(res, str):
                lines = res.split("\n")
                for i, line in enumerate(lines, 1):
                    if i != 2:
                        line = line.replace("*", "/")
                    if i % 2 != 0:
                        txt += Fore.YELLOW + line + Style.RESET_ALL + " "
                    elif i % 2 == 0:
                        txt += line + "\n"
                return txt
            elif isinstance(res, dict):
                print(res.keys())
            else:
                return res

        except Exception as e:
            logger.exception(e)
            print(f"{Fore.RED}Ocurred error while formating.")
            return res




    @abc.abstractmethod
    def canticle(self):
        """ for Morning and Evening """

    @staticmethod
    def colour_canticle_ant(canticle_ant):
        return Fore.YELLOW + "Ant. " + Style.RESET_ALL + f"{canticle_ant}\n"

    @abc.abstractmethod
    def intercessions(self):
        """ for Morning and Evening """

    def colour_intercessions(self, intercessions):
        petis = ""
        response = Fore.LIGHTGREEN_EX + intercessions["resp"] + Style.RESET_ALL

        if self.default_inter:
            intro = f"{intercessions['intro']}" + f" {response}\n\n"
        else:
            intro = f"{intercessions['intro']}\n\n"
        for i in range(len(intercessions.keys()) - 1):
            pet_dict = intercessions.get(f"pet{i}")
            if pet_dict:
                if self.default_inter:
                    resp = f"{pet_dict['w'].replace('-', '')}\n" + response
                    petis += f"{pet_dict['k']}{resp}\n"
                else:
                    resp = Fore.LIGHTBLACK_EX + f"{pet_dict['w'].replace('-', '')}" + Style.RESET_ALL + "\n"
                    petis += f"{pet_dict['k']}{resp}\n"

        return intro, petis

    def paternoster(self):
        """ for Morning and Evening """
        intro = self.const[f"pn_{random.choice(range(1, 10))}"] if self.pater_intro else ""
        paternoster = self.const["paternoster"]
        return f"\u2731 MODLITWA PAŃSKA \u2731\n" + Fore.LIGHTBLUE_EX + intro + Style.RESET_ALL + "\n" + paternoster

    def tedeum(self):
        poetic = self.const["lec_tedeum_poetic"]
        poetic_extra = self.const["lec_tedeum_poetic_extra"]
        clasic = self.const["lec_tedeum_clasic"]
        clasic_extra = self.const["lec_tedeum_clasic_extra"]

        if self.full:
            clasic += clasic_extra
            poetic += poetic_extra

        if self.rank in ["f", "s"] and not self.is_lent:
            return clasic if self.clasic_td else poetic
        else:
            return ""

    @abc.abstractmethod
    def prayer(self):
        """ """

    @abc.abstractmethod
    def dismisal(self):
        """ """

    @property
    def rank(self):
        return self.office.rank

    @rank.getter
    def rank(self):
        return self.office.rank

    @rank.setter
    def rank(self, rank_type: str = "o"):
        """
        s - solemnity, f - feast, m - memory obligatory, l - memory free, a - aditional memory, o - ordinary
        """
        self.office.rank = rank_type

    @property
    def joined(self):
        return self.__joined

    @joined.getter
    def joined(self):
        return self.__joined

    @joined.setter
    def joined(self, joined: bool = True):
        """ Should be False when with Morning or Evening Prayer """
        self.__joined = joined

    @property
    def with_inv(self):
        return self.__with_inv

    @with_inv.getter
    def with_inv(self):
        return self.__with_inv

    @with_inv.setter
    def with_inv(self, with_inv: bool = True):
        """ Should be False when with Morning or Evening Prayer """
        self.__with_inv = with_inv

    @property
    def is_lent(self):
        return self.__is_lent

    @is_lent.getter
    def is_lent(self):
        return self.__is_lent

    @is_lent.setter
    def is_lent(self, solo: bool = False):
        """ Should be True in lent season (no TeDeum and Aleluia) """
        self.__is_lent = solo

    @property
    def full(self):
        return self.__full

    @full.getter
    def full(self):
        return self.__full

    @full.setter
    def full(self, full_version: bool = False):
        """ Should be True in lent season (no TeDeum and Aleluia) """
        self.__full = full_version

    @property
    def clasic_td(self):
        return self.__clasic_td

    @clasic_td.getter
    def clasic_td(self):
        return self.__clasic_td

    @clasic_td.setter
    def clasic_td(self, is_clasic: bool = True):
        """ True for clasic version of Te Deum, False for poetic """
        self.__clasic_td = is_clasic


class Invitatory(Hours, ABC):
    def __init__(self, officium):
        super().__init__(officium)
        self.hour = "inv"

    def __str__(self):
        return (
                "\u2554" + "\u2550" * 11 + "\u2557\n"
                                           "\u272A WEZWANIE \u272A\n"
                                           "\u255A" + "\u2550" * 11 + "\u255D\n"
                                                                      f"{self.opening()}"
                                                                      f"{self.psalmodia()}"
        )

    @property
    def no_ant(self):
        return self.__no_ant

    @no_ant.getter
    def no_ant(self):
        return self.__no_ant

    @no_ant.setter
    def no_ant(self, no_ant: bool = False):
        self.__no_ant = no_ant

    def opening(self):
        return self.const["aperies"]

    @staticmethod
    def inv_base():
        with open(f"base_files/inv/inv_base.json", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def inv_ant():
        with open(f"base_files/inv/inv_antifonarium.json", encoding="utf-8") as f:
            return json.load(f)

    def psalmodia(self):
        """
        0|1|2|3|4|5|6 - psalter
        s|f - propia
        m - psalter *propia
        """
        ant = ''
        ant_map = {"1": "95", "2": "100", "3": "24", "4": "67"}
        mapped_value = ant_map.get(self.psalter_week)
        base = self.inv_base()[mapped_value]
        psalm_no = Fore.LIGHTRED_EX + base["num"] + "\n"
        psalm_title = Fore.LIGHTYELLOW_EX +base["mot"] + "\n"
        psalm_cita = Fore.LIGHTCYAN_EX + base["cit"] + "\n" + Style.RESET_ALL
        estr = base["est"]

        psalter_ant = self.inv_ant()[self.psalter_week][self.weekday_no]
        ant = psalter_ant
        if self.office.feast == "Dzień powszedni":
            ant = psalter_ant

        elif self.check_for_propia():
            try:
                ant = self.get_propia()[str(self.office.lg_date.month)][str(self.office.lg_date.day)][self.office.feast]["inv"]
            except KeyError:
                ant = "!!! Not in database yet !!!"

        else:
            try:
                common_ant = self.get_common()[self.office.commons[0]]["inv"]
                if isinstance(common_ant, dict):
                    common_ant = choice([x for x in common_ant.values()])
            except TypeError:
                common_ant = "!!! Not in database yet !!!"

            # for feasts and solemnities
            if self.rank in ["S", "F"]:
                ant = common_ant

            # for memories aut-aut
            elif self.rank in ["MO", "ML"]:
                ant = self.office.user.slider_choice(psalter_ant, common_ant)

        estribillos = ''
        for e in range(len(estr)):
            estribillos += estr[e] + "\n\n"

            if not self.no_ant and e != len(estr) - 1:
                estribillos += Fore.LIGHTYELLOW_EX + "Ant." + Style.RESET_ALL + " " + ant + "\n\n"

        psalmody = (
                psalm_no + psalm_title + psalm_cita + "\n" +
                Fore.LIGHTYELLOW_EX + "Ant." + Style.RESET_ALL + " " + ant + "\n\n" +
                estribillos
                + Fore.LIGHTYELLOW_EX + "Ant." + Style.RESET_ALL + " " + ant + "\n"
        )

        return psalmody


class Readings(Hours, ABC):
    def __init__(self, officium):
        super().__init__(officium)
        self.hour = "lec"
        self.season_base = self.get_base()
        self.common_base = self.get_common()
        self.propia_base = self.get_propia()

    def __str__(self):
        return (
                "\u2554" + "\u2550" * 17 + "\u2557\n"
                                           "\u272A GODZINA CZYTAŃ \u272A\n"
                                           "\u255A" + "\u2550" * 17 + "\u255D\n"
                                                                      f"{self.opening()}"
                                                                      f"{self.hymn()}"
                                                                      f"{self.psalmodia()}"
                                                                      f"{self.verse()}"
                                                                      f"{self.readings()}"
                                                                      f"{self.tedeum()}"
                                                                      f"{self.prayer()}"
                                                                      f"{self.dismisal()}"
        )

    def opening(self):
        aleluya = " Alleluja." if not self.is_lent else ""
        return "" if self.joined else f"{self.const['opening']}{aleluya}\n"

    def hymn(self):
        """
        0|1|2|3|4|5|6 - psalter
        s|f - propia | comunes
        m - comunes | psalter
        """
        h = self.get_proper_text("hymn")
        hymn = self.check_optional(h)
        fomated_hymn = self.format_hymn(hymn)
        return f"\u2731 HYMN \u2731\n{fomated_hymn}\n\n"

    def __psalmodia__(self):
        """

        """
        psalmody = "\u2731 PSALMODIA \u2731\n"
        for psalm in ["psalm1", "psalm2", "psalm3"]:
            psalmody += self.psalm(self.base[self.psalter_week][self.weekday_no][psalm])

        return psalmody

    def verse(self):
        """
        Przed czytaniami odmawia się werset, który stanowi przejście
        od modlitewnej psalmodii do słuchania słowa Bożego.
        Werset na uroczystości i święta podano przed czytaniami
        w Tekstach własnych lub wspólnych.
        Werset na niedziele i dni powszednie Okresu Zwykłego oraz
        na wspomnienia świętych wypadające w tym okresie podano
        w psałterzu po psalmodii.
        """
        v = self.get_proper_text("verse")
        verse = self.check_optional(v)

        if verse != "":
            coloured = self.colour_responsory(verse)
            return f"\u2731 WERSET \u2731\n{coloured}"
        else:
            return "\n*** no werse for today in database ***\n"

    def readings(self):
        """
        i_reading
                : lecture + responsory from psalter
        S & F   : propia | common

        ii reading
                : psalter
        S,F,M   : propia
        """
        lectures = ''
        for r in ["i reading", "ii reading"]:
            lec = self.get_proper_text(r)
            if lec:
                lecture = self.check_optional(lec)
                formated_lecture = self.formated_reading(lecture, r)
                lectures += formated_lecture
        return lectures



    def prayer(self):
        """ pdt|propia|comunes """
        ...
        text = self.get_proper_text("prayer")
        prayer = self.check_optional(text)

        if prayer.startswith(">"):
            redirect = prayer[1:]

            redirected_txt = self.get_proper_text(redirect)

            # here i finished

        return f"MODLITWA\nMódlmy się:\n{prayer}\nAmen.\n" if not self.joined else ""

    def dismisal(self):
        return "K. B\u0142ogos\u0142awmy Panu.\nW.  Bogu niech b\u0119d\u0105 dzi\u0119ki.\n" if not self.joined else ""


class Morning(Hours, ABC):
    def __init__(self, officium):
        super().__init__(officium)
        self.hour = "lau"
        self.season_base = self.get_base()
        self.common_base = self.get_common()
        self.propia_base = self.get_propia()
        self.default_inter = True  # default intercesions style
        self.pater_intro = False  # introduction for Our Father

    def __str__(self):
        return (
                "\u2554" + "\u2550" * 11 + "\u2557\n"
                                           "\u272A JUTRZNIA \u272A\n"
                                           "\u255A" + "\u2550" * 11 + "\u255D\n"
                                                                      f"{self.opening()}"
                                                                      f"{self.hymn()}"
                                                                      f"{self.psalmodia()}"
                                                                      f"{self.readings()}"
                                                                      f"{self.responsory()}"
                                                                      f"{self.canticle()}"
                                                                      f"{self.intercessions()}"
                                                                      f"{self.paternoster()}"
                                                                      f"{self.prayer()}"
                                                                      f"{self.dismisal()}"
        )

    def opening(self):
        """ """
        if self.with_inv:
            inv = Invitatory(self.office)
            inv.no_ant = self.no_ant
            return f"{inv.opening()}\n{inv.psalmodia()}"

        else:
            aleluya = " Alleluja." if not self.is_lent else ""
            return "" if self.joined else f"{self.const['opening']}{aleluya}\n"

    def readings(self):
        """
        Czytanie na niedziele i dni powszednie Okresu Zwykłego znajduje się w psałterzu.
        W uroczystości i święta czytanie podano w Tekstach własnych lub wspólnych.
        We wspomnienia świętych czytanie krótkie bierze się albo z Tekstów wspólnych, albo z bieżącego dnia, chyba że podano czytanie własne.

        """
        txt = self.get_proper_text("lecture")
        if txt:
            try:
                coloured = self.colour_lecture(txt)
                return f"\u2731 CZYTANIE \u2731\n" + coloured + "\n\n"

            except ValueError:
                return f"*** no lecture for today in database ***"

    def responsory(self):
        """
        s|f - propia | comunes
        0-6|m - psalter
        """
        resp = self.get_proper_text("responsory")
        if resp:
            coloured = self.colour_responsory(resp)
            return f"\u2731 RESPONSORIUM KRÓTKIE \u2731\n{coloured}\n"
        else:
            return "\n*** no responsory for today in database ***\n"

    def canticle(self):
        """
        Następnie odmawia się pieśń z Ewangelii z odpowiednią antyfoną.
        W niedziele Okresu Zwykłego antyfonę do pieśni Zachariasza bierze się z Tekstów okresowych; w dni powszednie z psałterza.
        Przy obchodach świętych, jeśli nie mają antyfony własnej, bierze się ją z Tekstów wspólnych, a we wspomnienia świętych albo z Tekstów wspólnych, albo z dnia bieżącego.

        """
        canticle_ant = self.get_proper_text("zachary")

        if canticle_ant:
            return (
                    f"\u2731 PIEŚŃ ZACHARIASZA" + Fore.LIGHTYELLOW_EX + " (Łk 1, 68-79) " + Style.RESET_ALL + "\u2731\n" +
                    self.colour_canticle_ant(canticle_ant)
                    + f"{self.const['zac_txt']}" +
                    self.colour_canticle_ant(canticle_ant)
                    + "\n"
            )
        else:
            return "\n*** no Antiphone for Canticle of Zacariach for today in database ***\n"

    def intercessions(self):
        """
        Po skończeniu pieśni Zachariasza odmawia się prośby.
        Prośby na niedziele i dni powszednie Okresu Zwykłego podano w psałterzu.
        Prośby na uroczystości i święta znajdują się w Tekstach własnych lub wspólnych.
        We wspomnienia świętych prośby bierze się albo z Tekstów wspólnych, albo z bieżącego dnia, chyba że są własne.

        """
        inter = self.get_proper_text("petitions")

        if inter:
            intercessions = self.check_optional(inter)
            intro, petitions = self.colour_intercessions(intercessions)
            return f"\u2731 PROŚBY \u2731\n" + intro + petitions
        else:
            return "\n*** no Intercessions for today in database ***\n"



    def prayer(self):
        """
        Po "Ojcze nasz" odmawia się modlitwę, której nie poprzedza się wezwaniem "Módlmy się".
        Tę modlitwę końcową w niedziele Okresu Zwykłego bierze się z Tekstów okresowych,
        w dni powszednie z psałterza, w oficjach o świętych z Tekstów własnych lub wspólnych.
        """
        prayers = self.get_proper_text("prayer")
        prayer = self.check_optional(prayers)
        return f"\u2731 MODLITWA \u2731\n{prayer}"

    def dismisal(self):
        return "\n" + self.const["lau_ending_one"] if self.solo else "\n" + self.const["lau_ending_priest"]


class Daytime(Hours, ABC):
    def __init__(self, officium):
        super().__init__(officium)
        self.hour = self.time_of_day_category()

        self.psalter_base = self.get_psalter()
        self.fixed_base = self.get_fixed()
        self.solo = True
        self.def_inter = True

    def __str__(self):
        if self.hour == "ter":
            h = "MODLITWA PREZEDPOŁUDNIOWA"
        elif self.hour == "sex":
            h = "MODLITWA POŁUDNIOWA"
        elif self.hour == "non":
            h = "MODLITWA POPOŁUDNIOWA"
        else:
            raise ValueError("No such daytime hour")

        return (
                "\u2554" + "\u2550" * 12 + "\u2557\n"
                                           f"\u272A {h} \u272A\n"
                                           "\u255A" + "\u2550" * 12 + "\u255D\n"
                                                                      f"{self.opening()}"
                                                                      f"{self.hymn()}"
                                                                      f"{self.psalmodia()}"
                                                                      f"{self.readings()}"
                                                                      f"{self.prayer()}"
                                                                      f"{self.dismisal()}"
        )

    @staticmethod
    def time_of_day_category():
        current_hour = datetime.datetime.now().hour

        if current_hour < 12:
            return "ter"  # Before 12:00 PM
        elif 12 <= current_hour < 15:
            return "sex"  # Between 12:00 PM and 3:00 PM
        else:
            return "non"  # After 3:00 PM

    def get_psalter(self):
        season = self.office.season
        try:
            if season.startswith("ot"):
                with open(f"base_files/{season[:-1]}/{season[:-1]}_daytime_psalter.json", encoding="utf-8") as f:
                    return json.load(f)
            else:
                with open(f"base_files/{season}/{season}_daytime_psalter.json", encoding="utf-8") as f:
                    return json.load(f)
        except FileNotFoundError:
            raise Exception

    def get_fixed(self):
        season = self.office.season
        try:
            if season.startswith("ot"):
                with open(f"base_files/{season[:-1]}/{season[:-1]}_daytime_fixed.json", encoding="utf-8") as f:
                    return json.load(f)
            else:
                with open(f"base_files/{season}/{season}_daytime_fixed.json", encoding="utf-8") as f:
                    return json.load(f)
        except FileNotFoundError:
            raise Exception

    def opening(self):
        """ """
        aleluya = " Alleluja." if not self.is_lent else ""
        return "" if self.joined else f"{self.const['opening']}{aleluya}\n"

    def hymn(self):
        """ ALWAYS FROM FIXED """
        return f"\u2731 HYMN \u2731\n{self.fixed_base[self.hour][self.psalter_week][self.weekday_no]['hymn']}"

    def psalm(self, psalm):
        """ ALWAYS FROM PSALTERY """
        ant = psalm["antifona"] + "\n"
        ind = psalm["psalm_index"] + "\n" if len(psalm["psalm_index"]) > 0 else ""
        tit = psalm["psalm_title"] + "\n" if len(psalm["psalm_title"]) > 0 else ""
        com = psalm["psalm_comment"] + "\n" if len(psalm["psalm_comment"]) > 0 else ""

        txt = psalm["psalm_txt"] + "\n"
        indented = ''
        txt_splited = txt.split("\n")
        indent = True
        cross = 0

        for i in range(len(txt_splited)):
            if txt_splited[i].endswith("*"):
                if cross + 1 == i:
                    pass
                else:
                    indent = not indent
            elif txt_splited[i].endswith("†"):
                indent = not indent
                cross = i

            spacer = "\t" if indent else ""
            indented += f"{spacer}{txt_splited[i]}\n"

        w = psalm.get("werse", "")
        werse = w if w != "" else ""

        return (
                Fore.RED + "Ant. " + Fore.GREEN + ant +
                Fore.LIGHTRED_EX + ind +
                Fore.LIGHTYELLOW_EX + tit +
                Fore.LIGHTCYAN_EX + com +
                Style.RESET_ALL + indented +
                Fore.RED + "Ant. " + Fore.GREEN + ant +
                Style.RESET_ALL + "\n" + werse
        )

    def psalmodia(self):
        """
        ALWAYS FROM PSALTERY
        0|1|2|3|4|5|6 - psalter
        s|f - propia
        m - psalter *propia
        """
        psalmody = "\u2731 PSALMODIA \u2731\n"
        for psalm in ["psalm1", "psalm2", "psalm3"]:
            psalmody += self.psalm(self.psalter_base["psalter"][self.psalter_week][self.weekday_no][psalm])

        return psalmody

    def readings(self):
        """
/
        1 lecture + own responsory -> propia de tempore (pdt) | when s|f -> propia|comunes
        2 lecture + own responsory -> date | -> 'pdt'
        """
        lectures = ''
        lectures += self.psalter_base[self.hour][self.psalter_week][self.weekday_no].get("lecture", f"*** no lecture for today in database ***") + "\n"
        return "\u2731 CZYTANIE \u2731\n" + lectures

    def prayer(self):
        """ pdt|propia|comunes """
        ...
        prayer = self.fixed_base[self.hour][self.psalter_week][self.weekday_no].get("prayer", f"*** no prayers for today in database ***")
        return f"MODLITWA\n{prayer}" if not self.joined else ""

    def dismisal(self):
        return self.const["lau_ending_one"] if self.solo else self.const["lau_ending_priest"]


class Evening(Hours, ABC):
    def __init__(self, officium):
        super().__init__(officium)
        self.hour = "vis"
        self.season_base = self.get_base()
        self.common_base = self.get_common()
        self.propia_base = self.get_propia()
        self.default_inter = True  # default intercesions style
        self.pater_intro = False  # introduction for Our Father

    def __str__(self):
        return (
                "\u2554" + "\u2550" * 12 + "\u2557"
                                           "\u272A NIESZPORY \u272A"
                                           "\u255A" + "\u2550" * 12 + "\u255D"
                                                                      f"{self.opening()}"
                                                                      f"{self.hymn()}"
                                                                      f"{self.psalmodia()}"
                                                                      f"{self.readings()}"
                                                                      f"{self.responsory()}"
                                                                      f"{self.canticle()}"
                                                                      f"{self.intercessions()}"
                                                                      f"{self.paternoster()}"
                                                                      f"{self.prayer()}"
                                                                      f"{self.dismisal()}"
        )

    def opening(self):
        """ """
        aleluya = " Alleluja." if not self.is_lent else ""
        oor = Readings(self.office)  # office of readings
        return oor if self.joined else f"{self.const['opening']}{aleluya}\n"

    def hymn(self):
        """   """
        h = self.get_proper_text("hymn")
        hymn = self.check_optional(h)
        print(hymn)
        fomated_hymn = self.format_hymn(hymn)
        return f"\u2731 HYMN \u2731\n{fomated_hymn}\n\n"

    def psalm(self, psalm):
        """        """

        # use regex to eliminate (W. Alleluja) when self.will_be_sung == False

        ant = psalm["antifona"] + "\n"
        ind = psalm["psalm_index"] + "\n" if len(psalm["psalm_index"]) > 0 else ""
        tit = psalm["psalm_title"] + "\n" if len(psalm["psalm_title"]) > 0 else ""
        com = psalm["psalm_comment"] + "\n" if len(psalm["psalm_comment"]) > 0 else ""

        txt = psalm["psalm_txt"] + "\n"
        indented = ''
        txt_splited = txt.split("\n")
        indent = True
        cross = 0

        for i in range(len(txt_splited)):
            if txt_splited[i].endswith("*"):
                if cross + 1 == i:
                    pass
                else:
                    indent = not indent
            elif txt_splited[i].endswith("†"):
                indent = not indent
                cross = i

            spacer = "\t" if indent else ""
            indented += f"{spacer}{txt_splited[i]}\n"

        w = psalm.get("werse", "")
        werse = w if w != "" else ""

        return (
                Fore.RED + "Ant. " + Fore.GREEN + ant +
                Fore.LIGHTRED_EX + ind +
                Fore.LIGHTYELLOW_EX + tit +
                Fore.LIGHTCYAN_EX + com +
                Style.RESET_ALL + indented +
                Fore.RED + "Ant. " + Fore.GREEN + ant +
                Style.RESET_ALL + "\n" + werse
        )

    def psalmodia(self):
        """
        0|1|2|3|4|5|6 - psalter
        s|f - propia
        m - psalter *propia
        """
        psalmody = "\u2731 PSALMODIA \u2731\n"
        for psalm in ["psalm1", "psalm2", "psalm3"]:
            psalmody += self.psalm(self.base[self.psalter_week][self.weekday_no][psalm])

        return psalmody

    def responsory(self):
        """
        s|f - propia | comunes
        0-6|m - psalter
        """
        respons = self.base[self.psalter_week][self.weekday_no].get('responsory', "")
        if respons != "":
            return f"\u2731 RESPONSORIUM KRÓTKIE \u2731\n{respons}"
        else:
            return "\n*** no responsory for today in database ***\n"

    def readings(self):
        """
        1 lecture + own responsory -> propia de tempore (pdt) | when s|f -> propia|comunes
        2 lecture + own responsory -> date | -> 'pdt'
        """
        lectures = ''
        lectures += self.base[self.psalter_week][self.weekday_no].get("lecture", f"*** no lecture for today in database ***") + "\n"
        return "\u2731 CZYTANIE \u2731\n" + lectures

    def canticle(self):
        canticle = self.base[self.psalter_week][self.weekday_no].get('maria', "")
        if canticle != "":
            if self.weekday_no not in ["5", "6"]:
                return (f"\u2731 PIEŚŃ MARYI (Łk 1, 46-55) \u2731\n\n"
                        f"{canticle}\n{self.const['maria_txt']}\n{canticle}\n")
            else:
                # take from other part of base .. from Officium !!
                return "\n*** no Antiphone for Canticle of Maria for today in database ***\n"
        else:
            return "\n*** no Antiphone for Canticle of Maria for today in database ***\n"

    def intercessions(self):
        intercessions = self.base[self.psalter_week][self.weekday_no].get('petitions', "")
        if intercessions:
            petis = ""
            resp_template = Fore.LIGHTGREEN_EX + intercessions["resp"] + Style.RESET_ALL

            for xx in range(1, 10):
                pet_dict = intercessions.get(f"pet{xx}")

                if pet_dict:
                    resp = f"{pet_dict['w'].replace('-', '')}\n" + resp_template
                    petis += f"{pet_dict['k']}{resp}\n"

            return (
                    f"\u2731 PROŚBY \u2731\n"
                    f"{intercessions['intro']}\n{resp_template}\n\n" +
                    petis
            )
        else:
            return "\n*** no Intercessions for today in database ***\n"

    def paternoster(self):
        intro = self.const[f"pn_{random.choice(range(1, 10))}"] if self.pater_intro else ""
        paternoster = self.const["paternoster"]
        return intro + "\n\n" + paternoster

    def prayer(self):
        """ pdt|propia|comunes """
        ...
        prayer = self.base[self.psalter_week][self.weekday_no].get("prayer", f"*** no prayers for today in database ***")
        return f"MODLITWA\nMódlmy się:\n{prayer}" if not self.joined else ""

    def dismisal(self):
        return self.const["lau_ending_one"] if self.solo else self.const["lau_ending_priest"]


class Night(Hours, ABC):
    def __init__(self, officium):
        super().__init__(officium)

        self.solo = True
        self.def_inter = True

    def __str__(self):
        return (
                "\u2554" + "\u2550" * 11 + "\u2557\n"
                                           f"\u272A KOMPLETA \u272A\n"
                                           "\u255A" + "\u2550" * 11 + "\u255D\n"
                                                                      f"{self.opening()}"
                                                                      f"{self.confesion()}"
                                                                      f"{self.hymn()}"
                                                                      f"{self.psalmodia()}"
                                                                      f"{self.readings()}"
                                                                      f"{self.prayer()}"
                                                                      f"{self.dismisal()}"
                                                                      f"{self.maria()}"
        )

    def get_base(self):
        try:
            with open(f"base_files/com/com.json", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            raise Exception

    def opening(self):
        """ """
        aleluya = " Alleluja." if not self.is_lent else ""
        return "" if self.joined else f"{self.get_base()['inicium']}{aleluya}\n"

    def confesion(self):
        intro = f"\u2731 RACHUNEK SUMIENIA \u2731\n"
        act = self.get_base()["actus"][str(random.choice(range(1, 4)))]
        return intro + act

    def hymn(self):
        """ ALWAYS FROM FIXED """
        return f"\u2731 HYMN \u2731\n\n{self.get_base()['hymn'][self.psalter_week]}"

    def psalm(self, psalm):
        """ ALWAYS FROM PSALTERY """
        ant = psalm["antifona"] + "\n"
        ind = psalm["psalm_index"] if len(psalm["psalm_index"]) > 0 else ""
        tit = psalm["psalm_title"] if len(psalm["psalm_title"]) > 0 else ""
        com = psalm["psalm_comment"] + "\n" if len(psalm["psalm_comment"]) > 0 else ""

        txt = psalm["psalm_txt"]
        indented = ''
        txt_splited = txt.split("\n")
        indent = True
        cross = 0

        for i in range(len(txt_splited)):
            if txt_splited[i].endswith("*"):
                if cross + 1 == i:
                    pass
                else:
                    indent = not indent
            elif txt_splited[i].endswith("†"):
                indent = not indent
                cross = i

            spacer = "\t" if indent else ""
            indented += f"{spacer}{txt_splited[i]}\n"

        return (
                Fore.RED + "Ant. " + Fore.GREEN + ant +
                Fore.LIGHTRED_EX + ind +
                Fore.LIGHTYELLOW_EX + tit +
                Fore.LIGHTCYAN_EX + com +
                Style.RESET_ALL + indented +
                Fore.RED + "Ant. " + Fore.GREEN + ant +
                Style.RESET_ALL
        )

    def psalmodia(self):
        """ """
        psalmody = "\u2731 PSALMODIA \u2731\n"
        for psalm in ["psalm1", "psalm2"]:
            try:
                psalmody += self.psalm(self.get_base()["psalmodia"][self.weekday_no][psalm])
            except KeyError:
                pass

        return psalmody

    def readings(self):
        """ """
        sigla = self.get_base()["psalmodia"][self.psalter_week].get("lecture_s", None) + "\n"
        lecture = self.get_base()["psalmodia"][self.psalter_week].get("lecture", f"*** no lecture for today in database ***") + "\n"

        txt = sigla + lecture if sigla else lecture
        return f"\u2731 CZYTANIE\u2731\n{txt}"

    def prayer(self):
        """ pdt|propia|comunes """
        ...
        prayer = self.get_base()["psalmodia"][self.weekday_no].get("prayer", f"*** no prayers for today in database ***")
        return f"\u2731 MODLITWA\u2731 \n{prayer}"

    def dismisal(self):
        return self.get_base()["terminus"]

    def maria(self):
        title = f"\u2731 ANTYFONA KOŃCOWA DO NAJŚWIĘTSZEJ MARYI PANNY \u2731\n"
        if not self.office.season == "eas":
            return title + "\n" + self.get_base()["maria"][str(random.choice(range(1, 6)))]
        else:
            return title + "\n" + self.get_base()["maria"]["eas"]


def save_const(placement, const_txt):
    with open("library/cons.json", encoding="utf-8") as f:
        t = json.load(f)

    t[placement] = const_txt

    with open("library/cons.json", "w", encoding="utf-8") as f:
        json.dump(t, f, indent=4)
