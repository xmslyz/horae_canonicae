# amDg
# +JMJ

import abc
from abc import ABC


class Hours:
    def __init__(self):
        self.inicio = None
        self.is_lent = False
        self.with_inv = True
        self.joined = True

    @abc.abstractmethod
    def pray(self):
        """ """

    @abc.abstractmethod
    def opening(self):
        """Load in the data set"""
        raise NotImplementedError

    def hymn(self):
        """Load in the data set"""

    @abc.abstractmethod
    def psalmodia(self):
        """Load in the data set"""
        raise NotImplementedError

    @abc.abstractmethod
    def readings(self):
        """Load in the data set"""
        raise NotImplementedError

    @abc.abstractmethod
    def prayer(self):
        """Load in the data set"""
        raise NotImplementedError

    @abc.abstractmethod
    def dismisal(self):
        """Load in the data set"""
        raise NotImplementedError


class Readings(Hours, ABC):
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
        aleluya = " Alleluja."

        txt = (f"K. Bo\u017ce, wejrzyj ku wspomo\u017ceniu memu.\n"
               f"W. Panie, po\u015bpiesz ku ratunkowi memu.\n\n"
               f"Chwa\u0142a Ojcu i Synowi, i Duchowi \u015awi\u0119temu.\n"
               f"Jak by\u0142a na pocz\u0105tku, teraz i zawsze,\ni na wieki wiek\u00f3w. Amen.{aleluya}\n")

        return "" if self.with_inv else txt

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

    def tedeum(self, is_feast=False, clasic_type=True, full=True):
        poetic = (
            "HYMN\n"
            "Ciebie, Boga, wys\u0142awiamy,\n"
            "Tobie, Panu, wieczna chwa\u0142a.\n"
            "    Ciebie, Ojca, niebios bramy,\n"
            "    Ciebie wielbi ziemia ca\u0142a.\n"
            "Tobie wszyscy Anio\u0142owie,\n"
            "Tobie Moce i niebiosy,\n"
            "Cheruby, Serafinowie\n"
            "\u015bl\u0105 wieczystej pie\u015bni g\u0142osy:\n"
            "\u015awi\u0119ty, \u015awi\u0119ty nad \u015awi\u0119tymi\n"
            "B\u00f3g Zast\u0119p\u00f3w, Kr\u00f3l \u0142askawy,\n"
            "Pe\u0142ne niebo z kr\u0119giem ziemi\n"
            "majestatu Twojej s\u0142awy.\n"
            "Aposto\u0142\u00f3w Tobie rzesza,\n"
            "ch\u00f3r Prorok\u00f3w pe\u0142en chwa\u0142y,\n"
            "Tobie ho\u0142dy nie\u015b\u0107 po\u015bpiesza\n"
            "M\u0119czennik\u00f3w orszak bia\u0142y.\n"
            "Ciebie poprzez okr\u0105g ziemi\n"
            "z g\u0142\u0119bi serca, ile zdo\u0142a,\n"
            "G\u0142osy lud\u00f3w zgodzonymi\n"
            "wielbi \u015bwi\u0119ta pie\u015b\u0144 Ko\u015bcio\u0142a.\n"
            "Niezmierzonej Ojca chwa\u0142y,\nSyna, S\u0142owo wiekuiste,\n"
            "Z Duchem, wszech\u015bwiat wielbi ca\u0142y:\n"
            "Kr\u00f3lem chwa\u0142y Ty\u015b, o Chryste!\n"
            "Ty\u015b Rodzica Syn z wiek wieka.\n"
            "By \u015bwiat zbawi\u0107 swoim zgonem,\n"
            "Przyobl\u00f3k\u0142szy si\u0119 w cz\u0142owieka,\n"
            "nie wzgardzi\u0142e\u015b Panny \u0142onem.\n"
            "Ty\u015b pokruszy\u0142 \u015bmierci wrota,\n"
            "star\u0142 jej o\u015bcie\u0144 w m\u0119ki dobie\n"
            "I rajskiego kraj \u017cywota\notworzy\u0142e\u015b wiernym sobie.\n"
            "Po prawicy siedzisz Boga,\nw chwale Ojca, Syn Jedyny,\n"
            "Lecz gdy zabrzmi tr\u0105ba sroga,\n"
            "przyjdziesz s\u0105dzi\u0107 ludzkie czyny.\n"
            "Prosim, s\u0142udzy \u0142ask niegodni,\n"
            "wspom\u00f3\u017c, obmyj grzech, co plami,\n"
            "Gdy\u015b odkupi\u0142 nas od zbrodni\n"
            "drogiej swojej Krwi strugami.\n"
            "Ze \u015bwi\u0119tymi w blaskach mocy\n"
            "wiecznej chwa\u0142y zlej nam zdroje,\n"
            "Zbaw, o Panie, lud sierocy,\n"
            "b\u0142ogos\u0142aw dziedzictwo swoje!\n")

        poetic_extra = (
            "Rz\u0105d\u017a je, bro\u0144 po wszystkie lata,\n"
            "prowad\u017a w niebios b\u0142ogie bramy.\n"
            "My w dzie\u0144 ka\u017cdy, W\u0142adco \u015bwiata,\n"
            "Imi\u0119 Twoje wys\u0142awiamy.\n"
            "Po wiek wiek\u00f3w nie ustanie\n"
            "pie\u015b\u0144, co s\u0142awi Twoje czyny.\n"
            "O, w dniu onym racz nas, Panie,\n"
            "od wszelakiej ustrzec winy.\n"
            "Zjaw sw\u0105 lito\u015b\u0107 w \u017cyciu ca\u0142ym\n"
            "tym, co \u017cebrz\u0105 Twej opieki;\n"
            "W Tobie, Panie, zaufa\u0142em,\n"
            "nie zawstydz\u0119 si\u0119 na wieki.\n")

        clasic = (
            "HYMN\n"
            "Ciebie, Bo\u017ce, chwalimy,\n"
            "Ciebie, Panie, wys\u0142awiamy.\n"
            "Tobie, Ojcu Przedwiecznemu,\n"
            "wszystka ziemia cze\u015b\u0107 oddaje.\n"
            "Tobie wszyscy Anio\u0142owie,\n"
            "Tobie niebiosa i wszystkie Moce:\n"
            "Tobie Cherubini i Serafini\n"
            "nieustannym g\u0142osz\u0105 pieniem:\n"
            "\u015awi\u0119ty, \u015awi\u0119ty, \u015awi\u0119ty\n"
            "Pan B\u00f3g Zast\u0119p\u00f3w!\n"
            "Pe\u0142ne s\u0105 niebiosa i ziemia\n"
            "majestatu chwa\u0142y Twojej.\n"
            "Ciebie przes\u0142awny ch\u00f3r Aposto\u0142\u00f3w,\n"
            "Ciebie Prorok\u00f3w poczet chwalebny,\n"
            "Ciebie wychwala\n"
            "M\u0119czennik\u00f3w zast\u0119p \u015bwietlany.\n"
            "Ciebie po wszystkiej ziemi\n"
            "wys\u0142awia Ko\u015bci\u00f3\u0142 \u015bwi\u0119ty:\n"
            "Ojca niezmierzonego majestatu,\n"
            "godnego uwielbienia, prawdziwego\n"
            "i Jedynego Twojego Syna,\n"
            "\u015awi\u0119tego tak\u017ce\n"
            "Ducha Pocieszyciela.\n"
            "Ty\u015b Kr\u00f3lem chwa\u0142y, o Chryste,\n"
            "Ty\u015b Ojca Synem Przedwiecznym.\n"
            "Ty, dla zbawienia naszego bior\u0105c cz\u0142owiecze\u0144stwo,\n"
            "nie waha\u0142e\u015b si\u0119 wst\u0105pi\u0107 w \u0142ono Dziewicy.\n"
            "Ty, skruszywszy \u017c\u0105d\u0142o \u015bmierci,\n"
            "otworzy\u0142e\u015b wierz\u0105cym kr\u00f3lestwo niebios.\n"
            "Ty po prawicy Boga zasiadasz\nw Ojcowskiej chwale.\n"
            "Ty przyjdziesz jako S\u0119dzia:\n"
            "tak wszyscy wierzymy.\n"
            "B\u0142agamy Ci\u0119 przeto: dopom\u00f3\u017c swym s\u0142ugom,\n"
            "kt\u00f3rych najdro\u017csz\u0105 Krwi\u0105 odkupi\u0142e\u015b.\n"
            "Policz ich mi\u0119dzy \u015bwi\u0119tych Twoich\n"
            "w wiekuistej chwale.\n")

        clasic_extra = (
            "Zachowaj lud sw\u00f3j, o Panie,\n"
            "i b\u0142ogos\u0142aw dziedzictwu swojemu.\n"
            "I rz\u0105d\u017a nimi,\n"
            "i wywy\u017cszaj ich a\u017c na wieki.\n"
            "Po wszystkie dni\nb\u0142ogos\u0142awimy Ciebie\n"
            "I wys\u0142awiamy imi\u0119 Twe na wieki,\n"
            "na wieki bez ko\u0144ca.\nRacz, Panie, w dniu dzisiejszym\n"
            "zachowa\u0107 nas od grzechu.\n"
            "Zmi\u0142uj si\u0119 nad nami, Panie,\n"
            "zmi\u0142uj si\u0119 nad nami.\n"
            "Niech mi\u0142osierdzie Twoje, Panie, oka\u017ce si\u0119 nad nami,\n"
            "jako my w Tobie ufno\u015b\u0107 pok\u0142adamy.\n"
            "W Tobie, o Panie, z\u0142o\u017cy\u0142em nadziej\u0119,\n"
            "nie b\u0119d\u0119 zawstydzon na wieki.\n")

        if full:
            clasic += clasic_extra
            poetic += poetic_extra

        if is_feast:
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


x = Readings()
x.pray()
