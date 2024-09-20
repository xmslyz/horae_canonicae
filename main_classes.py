# amDg
# +JMJ

import abc
import json
from abc import ABC
import datetime
import random
from webbrowser import Error

from colorama import Fore, Style, init

from creator import Skeleton


class Hours:
    def __init__(self, propiae):
        self.__rank = None
        self.__joined = False
        self.__with_inv = True
        self.__is_lent = False
        self.__full = True
        self.__clasic_td = True
        # self.propiae = self.propiae()
        self.propiae = propiae
        self.propia = self.propiae.lg_day
        self.hour = None

    # @staticmethod
    # def propiae():
    #     sk = Skeleton(datetime.datetime.today().date())
    #     return sk

    @staticmethod
    def get_const():
        with open("library/cons.json", encoding="utf-8") as f:
            return json.load(f)

    def get_base(self):
        season = self.propiae.season
        try:
            if season.startswith("ot"):
                with open(f"base_files/{season[:-1]}/{season[:-1]}_{self.hour}.json", encoding="utf-8") as f:
                    return json.load(f)
            else:
                with open(f"base_files/{season}/{season}_{self.hour}.json", encoding="utf-8") as f:
                    return json.load(f)
        except FileNotFoundError:
            raise Exception

    @abc.abstractmethod
    def pray(self):
        """ """

    @abc.abstractmethod
    def opening(self):
        """ """
        raise NotImplementedError

    def hymn(self):
        """ """

    @abc.abstractmethod
    def psalmodia(self):
        """ """
        raise NotImplementedError

    @abc.abstractmethod
    def psalm(self, psalm):
        """ """
        ant = psalm["antifona"] + "\n"
        ind = psalm["psalm_index"] + "\n" if len(psalm["psalm_index"]) > 0 else ""
        tit = psalm["psalm_title"] + "\n" if len(psalm["psalm_title"]) > 0 else ""
        com = psalm["psalm_comment"] + "\n" if len(psalm["psalm_comment"]) > 0 else ""
        txt = psalm["psalm_txt"] + "\n"

        indented = ''
        txt_splited = txt.split("\n")
        if self.hour == "lau":
            indent = True
        else:
            indent = False

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


    @abc.abstractmethod
    def readings(self):
        """ """
        raise NotImplementedError

    @abc.abstractmethod
    def canticle(self):
        """ for Morning and Evening """

    @abc.abstractmethod
    def intercessions(self):
        """ for Morning and Evening """

    @abc.abstractmethod
    def paternoster(self):
        """ for Morning and Evening """

    @abc.abstractmethod
    def prayer(self):
        """ """
        raise NotImplementedError

    @abc.abstractmethod
    def dismisal(self):
        """ """
        raise NotImplementedError

    @property
    def rank(self):
        return self.__rank

    @rank.getter
    def rank(self):
        return self.__rank

    @rank.setter
    def rank(self, rank_type: str = "o"):
        """
        s - solemnity, f - feast, m - memory obligatory, l - memory free, a - aditional memory, o - ordinary
        """
        self.__rank = rank_type

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
    def __init__(self, propiae):
        super().__init__(propiae)
        self.hour = "inv"
        self.const = self.get_const()
        self.psalter_week = str(propiae.current_psalter_week)
        # self.psalter_week = str(self.propiae.current_psalter_week)
        self.weekday_no = str(propiae.lg_day.weekday())
        # self.weekday_no = str(self.propiae.lg_day.weekday())
        self.__no_ant = False

    @property
    def no_ant(self):
        return self.__no_ant

    @no_ant.getter
    def no_ant(self):
        return self.__no_ant

    @no_ant.setter
    def no_ant(self, no_ant: bool = False):
        self.__no_ant = no_ant

    def pray(self):
        print("\u2554" + "\u2550" * 11 + "\u2557")
        print("\u272A WEZWANIE \u272A")
        print("\u255A" + "\u2550" * 11 + "\u255D")

        print(self.opening())
        print(self.psalmodia())

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

        ant_map = {"1": "95", "2": "100", "3": "24", "4": "67"}
        mapped_value = ant_map.get(self.psalter_week)
        base = self.inv_base()[mapped_value]
        psalm_no = base["num"]
        psalm_title = base["mot"]
        psalm_cita = base["cit"]
        estr = base["est"]

        ant = self.inv_ant()[self.psalter_week][self.weekday_no]

        estribillos = ''
        for e in range(len(estr)):
            estribillos += estr[e]
            if self.no_ant is False:
                estribillos += "\n" + ant + "\n"
        if self.no_ant:
            estribillos += "\n" + ant

        psalmody = (
            psalm_no + psalm_title + psalm_cita + "\n" + "Ant." + ant + "\n" + estribillos
        )

        return psalmody


class Readings(Hours, ABC):
    def __init__(self, propiae):
        super().__init__(propiae)
        self.propiae = propiae
        self.hour = "lec"
        self.const = self.get_const()
        self.base = self.get_base()
        self.psalter_week = str(self.propiae.current_psalter_week)
        self.weekday_no = str(self.propiae.lg_day.weekday())

    def pray(self):
        print("\u2554" + "\u2550" * 17 + "\u2557")
        print("\u272A GODZINA CZYTAŃ \u272A")
        print("\u255A" + "\u2550" * 17 + "\u255D")

        print(self.opening())
        print(self.hymn())
        print(self.psalmodia())
        print(self.werse())
        print(self.readings())
        print(self.tedeum())
        print(self.prayer())
        print(self.dismisal())

    def opening(self):
        aleluya = " Alleluja." if not self.is_lent else ""
        return "" if self.joined else f"{self.const["opening"]}{aleluya}\n"

    def hymn(self):
        """
        0|1|2|3|4|5|6 - psalter
        s|f - propia | comunes
        m - comunes | psalter
        """
        return f"\u2731 HYMN \u2731\n{self.base[self.psalter_week][self.weekday_no]['hymn']}"

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

    def werse(self):
        """
        s|f - propia | comunes
        0-6|m - psalter
        """
        werse = self.base[self.psalter_week][self.weekday_no].get('werse', "")
        if werse != "":
            return f"\u2731 WERSET \u2731\n{werse}"
        else:
            return "\n*** no werse for today in database ***\n"

    def readings(self):
        """
        1 lecture + own responsory -> propia de tempore (pdt) | when s|f -> propia|comunes
        2 lecture + own responsory -> date | -> 'pdt'
        """
        lectures = ''
        for r in ["i_reading", "ii_reading"]:
            lectures += self.base[self.psalter_week][self.weekday_no].get(r, f"*** no {r} for today in database ***") + "\n"

        return lectures

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

    def prayer(self):
        """ pdt|propia|comunes """
        ...
        prayer = self.base[self.psalter_week][self.weekday_no].get("prayer", f"*** no prayers for today in database ***")
        return f"MODLITWA\nMódlmy się:\n{prayer}\nAmen.\n" if not self.joined else ""

    def dismisal(self):
        return "K. B\u0142ogos\u0142awmy Panu.\nW.  Bogu niech b\u0119d\u0105 dzi\u0119ki.\n" if not self.joined else ""


class Morning(Hours, ABC):
    def __init__(self, propiae):
        super().__init__(propiae)
        self.hour = "lau"
        self.const = self.get_const()
        self.base = self.get_base()
        self.solo = True
        self.def_inter = True
        self.pater_intro = False
        self.propiae = propiae
        self.psalter_week = str(self.propiae.current_psalter_week)
        self.weekday_no = str(self.propiae.lg_day.weekday())

    def pray(self):
        print("\u2554" + "\u2550" * 11 + "\u2557")
        print("\u272A JUTRZNIA \u272A")
        print("\u255A" + "\u2550" * 11 + "\u255D")

        print(self.opening())
        print(self.hymn())
        print(self.psalmodia())
        print(self.readings())
        print(self.responsory())
        print(self.canticle())
        print(self.intercessions())
        print(self.paternoster())
        print(self.prayer())
        print(self.dismisal())

    def opening(self):
        """ """
        if self.with_inv:
            inv = Invitatory(self.propiae)
            return f"{inv.opening()}\n{inv.psalmodia()}"

        else:
            aleluya = " Alleluja." if not self.is_lent else ""
            return "" if self.joined else f"{self.const["opening"]}{aleluya}\n"


    def hymn(self):
        """   """
        return f"\u2731 HYMN \u2731\n{self.base[self.psalter_week][self.weekday_no]['hymn']}"

    def psalm(self, psalm):
        """        """
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
        return lectures

    def canticle(self):
        canticle = self.base[self.psalter_week][self.weekday_no].get('zachary', "")
        if canticle != "":
            return (f"\u2731 PIEŚŃ ZACHARIASZA (Łk 1, 68-79) \u2731\n\n"
                    f"{canticle}\n{self.const["zac_txt"]}\n{canticle}\n")
        else:
            return "\n*** no Antiphone for Canticle of Zacariach for today in database ***\n"

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


class Daytime(Hours, ABC):
    def __init__(self, propiae):
        super().__init__(propiae)
        self.propiae = propiae
        self.hour = hour
        self.const = self.get_const()
        self.psalter_base = self.get_psalter()
        self.fixed_base = self.get_fixed()
        self.solo = True
        self.def_inter = True
        self.psalter_week = str(self.propiae.current_psalter_week)
        self.weekday_no = str(self.propiae.lg_day.weekday())

    def get_psalter(self):
        season = self.propiae.season
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
        season = self.propiae.season
        try:
            if season.startswith("ot"):
                with open(f"base_files/{season[:-1]}/{season[:-1]}_daytime_fixed.json", encoding="utf-8") as f:
                    return json.load(f)
            else:
                with open(f"base_files/{season}/{season}_daytime_fixed.json", encoding="utf-8") as f:
                    return json.load(f)
        except FileNotFoundError:
            raise Exception

    def pray(self):

        if self.hour == "ter":
            h = "MODLITWA PREZEDPOŁUDNIOWA"
        elif self.hour == "sex":
            h = "MODLITWA POŁUDNIOWA"
        elif self.hour == "non":
            h = "MODLITWA POPOŁUDNIOWA"
        else:
            raise ValueError("No such daytime hour")

        print("\u2554" + "\u2550" * 12 + "\u2557")
        print(f"\u272A {h} \u272A")
        print("\u255A" + "\u2550" * 12 + "\u255D")

        print(self.opening())
        print(self.hymn())
        print(self.psalmodia())
        print(self.readings())
        print(self.prayer())
        print(self.dismisal())

    def opening(self):
        """ """
        aleluya = " Alleluja." if not self.is_lent else ""
        return "" if self.joined else f"{self.const["opening"]}{aleluya}\n"


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
    def __init__(self, propiae):
        super().__init__(propiae)
        self.propiae = propiae
        self.hour = "vis"
        self.const = self.get_const()
        self.base = self.get_base()
        self.solo = True
        self.def_inter = True
        self.pater_intro = False
        self.psalter_week = str(self.propiae.current_psalter_week)
        self.weekday_no = str(self.propiae.lg_day.weekday())

    def pray(self):
        print("\u2554" + "\u2550" * 12 + "\u2557")
        print("\u272A NIESZPORY \u272A")
        print("\u255A" + "\u2550" * 12 + "\u255D")

        print(self.opening())
        print(self.hymn())
        print(self.psalmodia())
        print(self.readings())
        print(self.responsory())
        print(self.canticle())
        print(self.intercessions())
        print(self.paternoster())
        print(self.prayer())
        print(self.dismisal())

    def opening(self):
        """ """
        aleluya = " Alleluja." if not self.is_lent else ""
        return "" if self.joined else f"{self.const["opening"]}{aleluya}\n"


    def hymn(self):
        """   """
        return f"\u2731 HYMN \u2731\n{self.base[self.psalter_week][self.weekday_no]['hymn']}"

    def psalm(self, psalm):
        """        """
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
                        f"{canticle}\n{self.const["maria_txt"]}\n{canticle}\n")
            else:
                # take from other part of base .. from Propia !!
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
    def __init__(self, propiae):
        super().__init__(propiae)
        self.propiae = propiae
        self.const = self.get_const()
        self.solo = True
        self.def_inter = True
        self.psalter_week = str(self.propiae.current_psalter_week)
        self.weekday_no = str(self.propiae.lg_day.weekday())

    def get_base(self):
        try:
            with open(f"base_files/com/com.json", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            raise Exception

    def pray(self):
        print("\u2554" + "\u2550" * 11 + "\u2557")
        print(f"\u272A KOMPLETA \u272A")
        print("\u255A" + "\u2550" * 11 + "\u255D")

        print(self.opening())
        print(self.confesion())
        print(self.hymn())
        print(self.psalmodia())
        print(self.readings())
        print(self.prayer())
        print(self.dismisal())
        print(self.maria())

    def opening(self):
        """ """
        aleluya = " Alleluja." if not self.is_lent else ""
        return "" if self.joined else f"{self.get_base()["inicium"]}{aleluya}\n"

    def confesion(self):
        intro = f"\u2731 RACHUNEK SUMIENIA \u2731\n"
        act = self.get_base()["actus"][str(random.choice(range(1, 4)))]
        return intro + act

    def hymn(self):
        """ ALWAYS FROM FIXED """
        return f"\u2731 HYMN \u2731\n\n{self.get_base()["hymn"][self.psalter_week]}"

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
        if not self.propiae.season == "eas":
            return title + "\n" + self.get_base()["maria"][str(random.choice(range(1, 6)))]
        else:
            return title + "\n" + self.get_base()["maria"]["eas"]


def save_const(placement, const_txt):
    with open("library/cons.json", encoding="utf-8") as f:
        t = json.load(f)

    t[placement] = const_txt

    with open("library/cons.json", "w", encoding="utf-8") as f:
        json.dump(t, f, indent=4)


