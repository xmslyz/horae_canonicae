# amDg
# +JMJ

import abc
import json
from abc import ABC
import datetime
from colorama import Fore, Style, init

from creator import Skeleton


class Hours:
    def __init__(self):
        self.__rank = None
        self.__joined = False
        self.__is_lent = False
        self.__full = True
        self.__clasic_td = True
        self.calendar = self.calendar()

    @staticmethod
    def calendar():
        sk = Skeleton(datetime.date(2024, 5, 2))
        return sk


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
        """        """
        ant = psalm["antifona"] + "\n"
        ind = psalm["psalm_index"] + "\n" if len(psalm["psalm_index"]) > 0 else ""
        tit = psalm["psalm_title"] + "\n" if len(psalm["psalm_title"]) > 0 else ""
        com = psalm["psalm_comment"] + "\n" if len(psalm["psalm_comment"]) > 0 else ""
        txt = psalm["psalm_txt"] + "\n"

        w = psalm.get("werse", "")
        werse = w if w != "" else ""

        return (
            Fore.RED + "Ant. " + Fore.GREEN + ant +
            Fore.LIGHTRED_EX + ind +
            Fore.LIGHTYELLOW_EX + tit +
            Fore.LIGHTCYAN_EX + com +
            Style.RESET_ALL + txt +
            Fore.RED + "Ant. " + Fore.GREEN + ant +
            Style.RESET_ALL + "\n" + werse
        )


    @abc.abstractmethod
    def readings(self):
        """ """
        raise NotImplementedError

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
    def joined(self, solo: bool = True):
        """ Should be False when with Morning or Evening Prayer """
        self.__joined = solo

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


class Readings(Hours, ABC):
    def __init__(self):
        super().__init__()
        self.const = self.get_const()
        self.base = self.get_base()

    @staticmethod
    def get_const():
        with open("library/cons.json", encoding="utf-8") as f:
            return json.load(f)

    def get_base(self):
        season = self.calendar.season
        if season.startswith("ot"):
            with open(f"base_files/{season[:-1]}/{season[:-1]}_lec.json", encoding="utf-8") as f:
                return json.load(f)
        else:
            with open(f"base_files/{season}/{season}_lec.json", encoding="utf-8") as f:
                return json.load(f)

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
        psalter_str = str(self.calendar.current_psalter_week)
        day_str = str(self.calendar.lg_day.weekday())

        return f"\u2731 HYMN \u2731\n{self.base[psalter_str][day_str]['hymn']}"


    def psalmodia(self):
        """
        0|1|2|3|4|5|6 - psalter
        s|f - propia
        m - psalter *propia
        """
        psalter_str = str(self.calendar.current_psalter_week)
        day_str = str(self.calendar.lg_day.weekday())

        print("\u2731 PSALMODIA \u2731\n")
        psalmody = ''
        for psalm in ["psalm1", "psalm2", "psalm3"]:
            psalmody += self.psalm(self.base[psalter_str][day_str][psalm])

        return psalmody



    def werse(self):
        """
        s|f - propia | comunes
        0-6|m - psalter
        """
        psalter_str = str(self.calendar.current_psalter_week)
        day_str = str(self.calendar.lg_day.weekday())

        werse = self.base[psalter_str][day_str].get('werse', "")
        if werse != "":
            return f"\u2731 WERSET \u2731\n{werse}"
        else:
            return "\n*** no werse for today in database ***\n"

    def readings(self):
        """
        1 lecture + own responsory -> propia de tempore (pdt) | when s|f -> propia|comunes
        2 lecture + own responsory -> date | -> 'pdt'
        """
        psalter_str = str(self.calendar.current_psalter_week)
        day_str = str(self.calendar.lg_day.weekday())

        lectures = ''
        for r in ["i_reading", "ii_reading"]:
            lectures += self.base[psalter_str][day_str].get(r, f"*** no {r} for today in database ***") + "\n"

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
        psalter_str = str(self.calendar.current_psalter_week)
        day_str = str(self.calendar.lg_day.weekday())
        prayer = self.base[psalter_str][day_str].get("prayer", f"*** no prayers for today in database ***")
        return f"MODLITWA\nMódlmy się:\n{prayer}\nAmen.\n" if not self.joined else ""

    def dismisal(self):
        return "K. B\u0142ogos\u0142awmy Panu.\nW.  Bogu niech b\u0119d\u0105 dzi\u0119ki.\n" if not self.joined else ""


class Base:
    def __init__(self):
        self.i_visperas = None
        self.ivitatory = None
        self.morning = None
        self.midday = None
        self.midafternoon = None
        self.evening = None
        self.night = None
        self.reading = None

        self.ii_visperas = None


def save_const(placement, const_txt):
    with open("library/cons.json", encoding="utf-8") as f:
        t = json.load(f)

    t[placement] = const_txt

    with open("library/cons.json", "w", encoding="utf-8") as f:
        json.dump(t, f, indent=4)


if __name__ == "__main__":
    x = Readings()
    x.is_lent = False
    x.joined = False
    x.clasic_td = True
    x.full = True

    x.pray()

