# amDg
# +JMJ

import abc
import json
from abc import ABC


class Hours:
    def __init__(self):
        self.__rank = None
        self.__joined = False
        self.__is_lent = False

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
    def rank(self, rank_type: str):
        """
        s - solemnity, f - feast, m - memory obligatory, l - memory free, a - aditional memory
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


class Readings(Hours, ABC):
    def __init__(self):
        super().__init__()
        self.const = self.get_const()

    @staticmethod
    def get_const():
        with open("library/cons.json", encoding="utf-8") as f:
            return json.load(f)

    def pray(self):
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

        txt = (f"K. Bo\u017ce, wejrzyj ku wspomo\u017ceniu memu.\n"
               f"W. Panie, po\u015bpiesz ku ratunkowi memu.\n\n"
               f"Chwa\u0142a Ojcu i Synowi, i Duchowi \u015awi\u0119temu.\n"
               f"Jak by\u0142a na pocz\u0105tku, teraz i zawsze,\ni na wieki wiek\u00f3w. Amen.{aleluya}\n")

        return "" if self.joined else txt

    def hymn(self):
        """
        0|1|2|3|4|5|6 - psalter
        s|f - propia | comunes
        m - comunes | psalter
        """
        return "HYMN"

    def psalmodia(self):
        """
        0|1|2|3|4|5|6 - psalter
        s|f - propia
        m - psalter *propia
        """
        return "PSALMODIA"

    def werse(self):
        """
        s|f - propia | comunes
        0-6|m - psalter
        """
        return "WERSET"

    def readings(self):
        """
        1 lecture + own responsory
        from propia de  tempore (pdt)

        s|f - propia|comunes

        2 lecture + own responsory
        from date

        else from 'pdt'

        """
        return "CZYTANIA"

    def tedeum(self, clasic_type=True, full=True):
        poetic = self.const["lec_tedeum_poetic"]
        poetic_extra = self.const["lec_tedeum_poetic_extra"]
        clasic = self.const["lec_tedeum_clasic"]
        clasic_extra = self.const["lec_tedeum_clasic_extra"]

        if full:
            clasic += clasic_extra
            poetic += poetic_extra

        if self.rank in ["f", "s"]:
            return clasic if clasic_type else poetic
        else:
            return ""

    def prayer(self):
        """
        pdt|propia|comunes

        """
        ...
        prayer = ""

        return f"MODLITWA\nMódlmy się:\n{prayer}\nAmen." if self.joined else ""

    def dismisal(self):
        return "K. B\u0142ogos\u0142awmy Panu.\nW.  Bogu niech b\u0119d\u0105 dzi\u0119ki.\n" if self.joined else ""


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
    x.rank = "m"
    x.is_lent = True
    x.joined = False
    x.pray()
