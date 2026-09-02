# -*- coding: utf-8 -*-
"""TutorIA – a hangos mód költségének kordában tartása.

MIÉRT KELL EZ
    A felolvasás KARAKTERRE megy: a mért adat szerint egy sokat beszélgető
    gyerek havi 7,4 €-t visz el, aminek kétharmada a felolvasás. Egy 16 €-s
    előfizetésnél ez még belefér, de idegen családoknál nem mindegy.

HÁROM FOGÁS, KETTŐ JAVÍTJA IS AZ ÉLMÉNYT
    1. RÖVIDEBB MONDAT. A hosszú felolvasott monológ egy gyereknek amúgy is
       sok — itt vágjuk el, ha a tanár elszaladt.
    2. GYORSTÁR. A visszatérő mondatokat ("Ügyes vagy!", "Kezdjük!") egyszer
       olvastatjuk fel, aztán a mentett hangot adjuk vissza. Ingyen, és
       gyorsabb is: nincs várakozás.
    3. NAPI KERET. Ha egy gyerek egy nap alatt elhasználja a keretet, a
       felolvasás kikapcsol, a tanítás pedig szövegben megy tovább.
       A tanulás soha nem áll meg — csak a hang.
"""

from __future__ import annotations

import hashlib
import os
import re

# ── 1. a felolvasott szöveg hossza ──────────────────────────────────────────
# SZÖVEGMÓDBAN a felolvasás kiegészítés: a gyerek olvassa is a választ, ezért
# 420 karakter után mondathatáron elvágjuk – így nem fizetünk azért, amit a
# gyerek amúgy is lát.
MAX_KARAKTER = 420

# HANGOS MÓDBAN viszont a felolvasás MAGA a tanítás. Ott a levágás azt
# jelentette, hogy a magyarázat vége – sokszor maga a kérdés – soha nem
# hangzott el, és a gyerek csendben maradt, nem tudva, mit kérdeztek tőle.
# Itt tehát végigolvassuk a választ; a 3000 karakter csak azért van, hogy egy
# elszabadult, több oldalas válasz ne vigye el a napi keretet egyetlen körben.
MAX_KARAKTER_HANG = 3_000

# ── 3. napi keret gyerekenként ──────────────────────────────────────────────
# A teljes hosszú felolvasás körönként kb. háromszor annyi karakter, ezért a
# napi keret is nő. 30 000 karakter így is kb. 30 tanári forduló hangos módban.
# Fölötte a felolvasás kikapcsol aznapra, a szöveges tanítás megy tovább.
NAPI_KERET = 30_000

_MONDATVEG = re.compile(r"(?<=[.!?…])\s+")


def rovidit(szoveg: str, max_karakter: int = MAX_KARAKTER) -> str:
    """A felolvasandó szöveg levágása mondathatáron.

    Sosem vág szó közepén, és mindig marad legalább egy teljes mondat.
    """
    szoveg = (szoveg or "").strip()
    if len(szoveg) <= max_karakter:
        return szoveg
    ki = ""
    for mondat in _MONDATVEG.split(szoveg):
        if not mondat:
            continue
        if len(ki) + len(mondat) + 1 > max_karakter:
            break
        ki = f"{ki} {mondat}".strip()
    if ki:
        return ki
    # Ha már az ELSŐ mondat hosszabb a keretnél (a tanár egy lélegzetvétellel
    # elmondott egy bekezdést), szóhatáron vágunk. A keretet így sem lépjük túl:
    # azért fizetünk, amit felolvasunk.
    return szoveg[:max_karakter].rsplit(" ", 1)[0] or szoveg[:max_karakter]


# ── 2. gyorstár ─────────────────────────────────────────────────────────────
def _kulcs(szoveg: str, hang: str) -> str:
    nyers = f"{hang}|{szoveg}".encode("utf-8")
    return hashlib.sha256(nyers).hexdigest()[:32]


class Gyorstar:
    """Felolvasott hangok a lemezen. A visszatérő mondatok ingyen mennek.

    Szándékosan buta: fájl a lemezen, név a szöveg ujjlenyomata. Nincs
    lejárat – ha a szöveg ugyanaz, a hang is ugyanaz marad.
    """

    def __init__(self, mappa: str, max_fajl: int = 4000) -> None:
        self.mappa = mappa
        self.max_fajl = max_fajl
        os.makedirs(mappa, exist_ok=True)

    def _ut(self, szoveg: str, hang: str) -> str:
        return os.path.join(self.mappa, _kulcs(szoveg, hang) + ".mp3")

    def olvas(self, szoveg: str, hang: str) -> bytes | None:
        ut = self._ut(szoveg, hang)
        try:
            if os.path.isfile(ut):
                with open(ut, "rb") as f:
                    return f.read()
        except OSError:
            pass
        return None

    def ir(self, szoveg: str, hang: str, adat: bytes) -> None:
        if not adat:
            return
        try:
            # Csak a RÖVID, ismétlődő mondatokat érdemes eltenni. Egy hosszú,
            # egyedi magyarázat úgysem hangzik el még egyszer ugyanúgy.
            if len(szoveg) > 240:
                return
            self._takarit()
            with open(self._ut(szoveg, hang), "wb") as f:
                f.write(adat)
        except OSError:
            pass

    def _takarit(self) -> None:
        """Ha túl sok fájl gyűlt össze, a legrégebbieket kidobjuk."""
        try:
            fajlok = [os.path.join(self.mappa, n) for n in os.listdir(self.mappa)
                      if n.endswith(".mp3")]
            if len(fajlok) <= self.max_fajl:
                return
            fajlok.sort(key=lambda p: os.path.getmtime(p))
            for p in fajlok[: len(fajlok) - self.max_fajl + 200]:
                os.remove(p)
        except OSError:
            pass


def keret_maradek(mai_karakter: int, keret: int = NAPI_KERET) -> int:
    """Mennyi felolvasás van még ma. Nulla alá nem megy."""
    return max(0, keret - max(0, int(mai_karakter or 0)))


# ── 4. matematikai jelek kimondása ──────────────────────────────────────────
# MIÉRT: az Azure a "80 - 30 = 50" szövegből a jeleket NEM mondja ki, a végén
# álló "50."-et pedig magyarul SORSZÁMNAK olvassa: "nyolcvan harminc ötvenedik".
# A gyerek ebből semmit nem ért. Itt szavakká írjuk a jeleket, mielőtt a
# felolvasóhoz kerülne.

_MUVELET = {
    "hu": {"=": " egyenlő ", "+": " meg ", "-": " mínusz ",
           "*": " szorozva ", "×": " szorozva ", "⋅": " szorozva ",
           "/": " osztva ", "÷": " osztva ", ":": " osztva ",
           "%": " százalék ",
           "x": " szorozva ", "X": " szorozva ",
           "<": " kisebb mint ", ">": " nagyobb mint "},
    "es": {"=": " igual a ", "+": " más ", "-": " menos ",
           "*": " por ", "×": " por ", "⋅": " por ",
           "/": " entre ", "÷": " entre ", ":": " entre ",
           "%": " por ciento ",
           "x": " por ", "X": " por ",
           "<": " menor que ", ">": " mayor que "},
}

# Ezek a jelek SOHA nem jelentenek mást magyar szövegben, így bárhol cserélhetők.
_MINDIG = ("×", "⋅", "÷", "=", "%", "<", ">")
# Ezek viszont igen: a "-" toldalékot köt ("1848-ban"), a "/" dátumot választ
# el, a "*" pedig kiemelés lehet. Ezért CSAK két szám között, szóközökkel.
# Az "x" is lehet szorzásjel ("9 x 10"), de csak akkor, ha KÉT szám között
# áll, szóközökkel. Az algebrai "3x" így érintetlen marad.
# A ":" is osztásjel, ha KÉT SZÁM KÖZÖTT áll szóközökkel ("360 : 9").
# Szóköz nélkül ("10:30") óra, azt nem bántjuk.
_OVATOS = re.compile(r"(?<=\d)\s+([-+*/xX:])\s+(?=\d)")
# A "8+3" alakot is értjük, ha nincs körülötte szóköz – a + soha nem toldalék.
_PLUSZ = re.compile(r"(?<=\d)\+(?=\d)")

# Mondat VÉGÉN álló szám: itt olvassa az Azure sorszámnak. A "3. feladat"
# viszont tényleg sorszám, azt nem bántjuk – ezért kell a szigorú feltétel:
# a szám előtt van másik szó, utána pedig mondatvég vagy új mondat kezdődik.
_SZAM_MONDATVEGEN = re.compile(
    r"(?<=\S\s)(\d{1,6})\.(?=\s+[A-ZÁÉÍÓÖŐÚÜŰ]|\s*$)")

_HU_EGYES = ["nulla", "egy", "kettő", "három", "négy",
             "öt", "hat", "hét", "nyolc", "kilenc"]
_HU_TIZES = ["", "tíz", "húsz", "harminc", "negyven",
             "ötven", "hatvan", "hetven", "nyolcvan", "kilencven"]
_HU_ELOTAG = ["", "tizen", "huszon", "harminc", "negyven",
              "ötven", "hatvan", "hetven", "nyolcvan", "kilencven"]


def _ket(szo: str) -> str:
    """Összetételben a 'kettő' rövidül: kétszáz, kétezer."""
    return szo[:-5] + "két" if szo.endswith("kettő") else szo


def _hu_100(n: int) -> str:
    if n < 10:
        return _HU_EGYES[n]
    tizes, egyes = divmod(n, 10)
    if egyes == 0:
        return _HU_TIZES[tizes]
    return _HU_ELOTAG[tizes] + _HU_EGYES[egyes]


def _hu_1000(n: int) -> str:
    if n < 100:
        return _hu_100(n)
    szaz, maradek = divmod(n, 100)
    ki = ("" if szaz == 1 else _ket(_HU_EGYES[szaz])) + "száz"
    return ki + (_hu_100(maradek) if maradek else "")


def hu_szam(n: int) -> str:
    """Magyar számnév. Enélkül a mondatvégi szám sorszámmá torzul."""
    if n < 0:
        return "mínusz " + hu_szam(-n)
    if n < 1000:
        return _hu_1000(n)
    if n < 1_000_000:
        ezres, maradek = divmod(n, 1000)
        ki = ("" if ezres == 1 else _ket(_hu_1000(ezres))) + "ezer"
        return ki + (_hu_1000(maradek) if maradek else "")
    return str(n)


# ── 4/b. SZORZÁS ÉS TOLDALÉKOS SZÁM ─────────────────────────────────────────
# MIÉRT: magyarul a "8 × 5" nem "nyolc szorozva öt", hanem NYOLCSZOR ÖT.
# A toldalékos szám pedig ("10-re", "4-hez") a felolvasónál sorszámmá torzul:
# "a tizediken", "a negyedikhez". A gyerek ebből semmit nem ért, és rosszul
# is rögzül. Mindkettőt SZÓVÁ írjuk, mielőtt a hang elmegy.

# A -szor / -szer / -ször a szó utolsó magánhangzójától függ.
_SZOR_HATSO = "aáoóuú"      # → -szor
_SZOR_ELSO = "eéií"         # → -szer
_SZOR_AJAK = "öőüű"         # → -ször


def szorzoszam(n: int) -> str:
    """8 → 'nyolcszor', 5 → 'ötször', 2 → 'kétszer'."""
    szo = _ket(hu_szam(n))
    if szo.endswith("húsz"):
        return szo[:-1] + "szor"        # húsz → hússzor
    for betu in reversed(szo):
        if betu in _SZOR_HATSO:
            return szo + "szor"
        if betu in _SZOR_ELSO:
            return szo + "szer"
        if betu in _SZOR_AJAK:
            return szo + "ször"
    return szo + "szor"


# "8 × 5", "4 × 10-re", "12x3" — a toldalékot is magához veszi, különben
# a csere után árván maradna: "négyszer tíz-re".
_SZORZAS = re.compile(
    r"(?<!\d)(\d{1,6})\s*[×⋅*]\s*(\d{1,6})(-[a-záéíóöőúüű]{1,6})?")

# Képletben a második tag betű: "K = 4 × a" → "négyszer a".
_SZORZAS_BETU = re.compile(r"(?<!\w)(\d{1,6})\s*[×⋅]\s*([a-zA-Z])(?!\w)")

# Toldalékos szám: "10-re", "4-hez", "1848-ban". A toldalékot a szöveg írója
# már helyesen választotta meg, ezért elég a számot szóvá írni és hozzáragasztani.
# A ":" is tiltott előzmény: a "10:30-kor" időpont, nem toldalékos szám.
_TOLDALEKOS_SZAM = re.compile(
    r"(?<![\w:-])(\d{1,6})-([a-záéíóöőúüű]{1,8})(?![\w-])")


def szorzas_szoval(szoveg: str) -> str:
    """"8 × 5" → "nyolcszor öt". A jelcserék ELŐTT kell futnia."""
    def csere(m: "re.Match[str]") -> str:
        elso, masodik, told = m.group(1), m.group(2), m.group(3) or ""
        ki = f"{szorzoszam(int(elso))} {hu_szam(int(masodik))}"
        return ki + told[1:] if told else ki

    szoveg = _SZORZAS.sub(csere, szoveg)
    return _SZORZAS_BETU.sub(
        lambda m: f"{szorzoszam(int(m.group(1)))} {m.group(2)}", szoveg)


# ── OSZTÁS: az OSZTÓ -val/-vel ragot kap ────────────────────────────────────
# MIÉRT: magyarul a "8000 : 1000" nem "nyolcezer osztva ezer", hanem
# NYOLCEZER OSZTVA EZERREL. A ragot leírni nem szoktuk, de kimondani igen —
# és a gyerek a HANGOT hallja, nem a leírt alakot. Rag nélkül idegenül szól,
# és rosszul is rögzül.
#
# MIÉRT TÁBLÁZAT ÉS NEM SZABÁLY: a -val/-vel a szó végén hasonul (ezer →
# ezerREL, húsz → húSSZal, egy → eGGYel), a mély/magas választás pedig
# összetett számnévnél az UTOLSÓ tagot követi ("nyolcezerrel" magas, pedig
# van benne "o"). Egy általános hangrend-szabály ezen elcsúszna. A hu_szam()
# viszont mindig e HUSZONKÉT szó valamelyikére végződik, így a teljes esetet
# fel tudjuk sorolni – ez rövidebb is, és nem téved.
_OSZTO_RAG = {
    "nulla": "nullával", "egy": "eggyel", "kettő": "kettővel",
    "három": "hárommal", "négy": "néggyel", "öt": "öttel",
    "hat": "hattal", "hét": "héttel", "nyolc": "nyolccal",
    "kilenc": "kilenccel", "tíz": "tízzel", "húsz": "hússzal",
    "harminc": "harminccal", "negyven": "negyvennel", "ötven": "ötvennel",
    "hatvan": "hatvannal", "hetven": "hetvennel", "nyolcvan": "nyolcvannal",
    "kilencven": "kilencvennel", "száz": "százzal", "ezer": "ezerrel",
}
# A HOSSZABB végződés nyer: a "kilencven" nem a "kilenc" ága, és a
# "huszonöt" nem az "öt"-é... de igen, annak épp az: "huszonöttel".
_OSZTO_VEGEK = sorted(_OSZTO_RAG, key=len, reverse=True)


def oszto_raggal(n: int) -> str:
    """1000 → 'ezerrel', 9 → 'kilenccel', 20 → 'hússzal'."""
    szo = hu_szam(n)
    for veg in _OSZTO_VEGEK:
        if szo.endswith(veg):
            return szo[: -len(veg)] + _OSZTO_RAG[veg]
    return szo                      # nem tudjuk ragozni: inkább rag nélkül


# ── "80-hoz", "90-hez", "100-hoz" ───────────────────────────────────────────
# MIÉRT ITT: a rag attól függ, hogyan MONDJUK ki a számot, nem attól, hogyan
# írjuk. A "80" azért kap -hoz-t, mert "nyolcvan", a "90" azért -hez-t, mert
# "kilencven". Ezt a tudást ez a modul őrzi, ezért itt a helye — a becslő
# kérdéseket író szamellenor.py innen kéri el.
#
# A -hoz/-hez/-höz nem hasonul, csak hangrendet választ; a magánhangzóra
# végződő szó viszont nyújt: nulla → nulláHOZ.
_HOZ_RAG = {
    "nulla": "hoz", "egy": "hez", "kettő": "höz", "három": "hoz",
    "négy": "hez", "öt": "höz", "hat": "hoz", "hét": "hez",
    "nyolc": "hoz", "kilenc": "hez", "tíz": "hez", "húsz": "hoz",
    "harminc": "hoz", "negyven": "hez", "ötven": "hez", "hatvan": "hoz",
    "hetven": "hez", "nyolcvan": "hoz", "kilencven": "hez",
    "száz": "hoz", "ezer": "hez",
}
_HOZ_VEGEK = sorted(_HOZ_RAG, key=len, reverse=True)


def hoz_rag(n: int) -> str:
    """Melyik rag illik a számhoz: 80 → 'hoz', 90 → 'hez', 5 → 'höz'.

    A hívó maga ragasztja a leírt számhoz: f"{80}-{hoz_rag(80)}" → "80-hoz".
    """
    szo = hu_szam(n)
    for veg in _HOZ_VEGEK:
        if szo.endswith(veg):
            return _HOZ_RAG[veg]
    return "hoz"


# Csak SZÓKÖZÖKKEL körülvett ":" és "/" – a "10:30" óra, a "3/4" tört.
# A "÷" viszont mindig osztás, ott a szóköz nem feltétel.
_OSZTAS = re.compile(
    r"(?<![\w.,])(\d{1,6})(?:\s+[:/]\s+|\s*÷\s*)(\d{1,6})"
    r"(-[a-záéíóöőúüű]{1,6})?(?![\w])")


def osztas_szoval(szoveg: str) -> str:
    """"8000 : 1000" → "nyolcezer osztva ezerrel". A jelcserék ELŐTT fut."""
    def csere(m: "re.Match[str]") -> str:
        oszt, oszto, told = m.group(1), m.group(2), m.group(3) or ""
        if told:
            # A szöveg írója maga tett rá toldalékot ("... : 4-hez"), azt
            # nem írjuk felül – ő tudja, mit akart mondani.
            return f"{hu_szam(int(oszt))} osztva {hu_szam(int(oszto))}{told[1:]}"
        return f"{hu_szam(int(oszt))} osztva {oszto_raggal(int(oszto))}"

    return _OSZTAS.sub(csere, szoveg)


# ── MÉRETSZORZÁS: "5 m × 3 m" ───────────────────────────────────────────────
# MIÉRT: a mértékegység cseréje ELŐBB fut (különben a "szorozva" beékelődne a
# szám és az egység közé), így viszont a "×" már nem két SZÁM között áll, és
# a szorzas_szoval() nem találja meg. Ami maradt: "öt méter SZOROZVA három
# méter" — ez magyarul hibás, mert a "szorozva" -val/-vel ragot vonz
# ("három méterREL"). Méretnél viszont nem is ezt mondjuk: "öt méter SZOR
# három méter". Ezért itt a "×"-ből "szor" lesz, nem "szorozva".
_SZOR_EGYSEG = re.compile(r"(?<=[a-záéíóöőúüű])\s*[×⋅*]\s*(?=\d)")


def meretszorzas_szoval(szoveg: str) -> str:
    """"5 méter × 3 méter" → "5 méter szor 3 méter"."""
    return _SZOR_EGYSEG.sub(" szor ", szoveg)


# ── ÉVSZÁM-TARTOMÁNY: "1848-49" ─────────────────────────────────────────────
# Kötőjel van benne, ezért a toldalékos-szám szabály nem nyúl hozzá, és
# számjegyként megy a felolvasóhoz. Kimondva: "ezernyolcszáznegyvennyolc
# negyvenkilenc".
_EVKOR = re.compile(r"(?<![\w-])((?:1\d|20)\d{2})\s*[-–—]\s*(\d{2,4})(?![\w-])")


def evkor_szoval(szoveg: str) -> str:
    return _EVKOR.sub(
        lambda m: f"{hu_szam(int(m.group(1)))} {hu_szam(int(m.group(2)))}",
        szoveg)


# ── ARÁNY: "2 : 3" ─────────────────────────────────────────────────────────
# MIÉRT: az arányt magyarul nem osztásként mondjuk ki. A "2 : 3" nem "kettő
# osztva hárommal", hanem "KETTŐ A HÁROMHOZ". Az osztás-szabály viszont ugyanezt
# az alakot látja, ezért ennek ELŐBB kell futnia.
#
# HONNAN TUDJUK, HOGY ARÁNY: az "arány" szó ott áll a mondatban. Enélkül nem
# találgatunk – a "6 : 2" az esetek túlnyomó részében tényleg osztás.
_ARANY_SZO = re.compile(r"ar[áa]ny", re.IGNORECASE)
_ARANY = re.compile(r"(?<![\w.,:])(\d{1,6})\s+:\s+(\d{1,6})(?![\w])")


def arany_szoval(szoveg: str) -> str:
    """"Az arány 2 : 3" → "Az arány kettő a háromhoz"."""
    if not _ARANY_SZO.search(szoveg):
        return szoveg
    def csere(m: "re.Match[str]") -> str:
        elso = hu_szam(int(m.group(1)))
        masodik = hu_szam(int(m.group(2)))
        # "három AZ öthöz", nem "három A öthöz": a névelő magánhangzó előtt
        # "az". Az öt, az egy és az ezer magánhangzóval kezdődik.
        nevelo = "az" if masodik[0] in "aáeéiíoóöőuúüű" else "a"
        return f"{elso} {nevelo} {masodik}{hoz_rag(int(m.group(2)))}"

    return _ARANY.sub(csere, szoveg)


# ── AMI SZÁMJEGY MARADT ─────────────────────────────────────────────────────
# MIÉRT KELL: eddig csak a szorzás, az osztás, a toldalékos és a mondatvégi
# szám lett szóvá írva. A TÖBBIT a felolvasóra bíztuk — az pedig találgat.
# Így lett a "4000 + 2000-re"-ből "4000 meg kétezerre": az egyik szám szóban,
# a másik számjegyben. Ez nem csak csúnya, hanem megbízhatatlan is.
#
# EZ A SZABÁLY FUT UTOLSÓNAK, amikor minden más már elvégezte a dolgát, és
# ami maradt, az tényleg sima tőszámnév.
#
# AMIHEZ NEM NYÚL, és miért:
#   "3. feladat"  – pont követi: SORSZÁM, azt így is jól mondja
#   "10:30"       – kettőspont: óra
#   "3,5"         – vessző: tizedes tört
#   "3/4"         – perjel: tört (a valódi osztást a jelcsere már elvitte)
#   "1848-ban"    – kötőjel: azt a toldalékos szabály már elintézte
#   "-5"          – kötőjel előtte: lehet negatív szám vagy tartomány vége
_MARADEK_SZAM = re.compile(r"(?<![\w.,:%/-])(\d{1,6})(?![\w.,:%°/-])")

# KETTŐ VAGY KÉT. Magyarul MEGSZÁMLÁLT FŐNÉV előtt "két alma", minden más
# helyzetben "kettő". A felolvasónak ez mindegy volna, a gyereknek nem: a
# "tizenkettő alma" hallhatóan idegen, és így is rögzülne.
#
# AZ ELSŐ VÁLTOZAT ITT HIBÁS VOLT: azt néztem, követi-e SZÓ a számot, és ha
# igen, rövidítettem. Ettől lett a "80 - 2 = 78"-ból "nyolcvan mínusz KÉT
# egyenlő hetvennyolc". A "két" ugyanis nem az bármi előtt áll, hanem amit
# MEGSZÁMLÁL. Az "egyenlő" nem megszámlálható.
#
# Főnevet szótár nélkül nem tudunk felismerni, viszont az ELLENKEZŐJE zárt
# lista: azok a szavak, amik számot követhetnek anélkül, hogy a szám őket
# számlálná. Ezek nagyrészt olyan szavak, amiket EZ A MODUL tesz a szövegbe
# (egyenlő, meg, mínusz, osztva), a többi kötőszó és létige.
_NEM_FONEV = {
    # amit a jelcsere ír be
    "egyenlő", "meg", "mínusz", "szorozva", "osztva", "szor", "százalék",
    "plusz", "kisebb", "nagyobb",
    # kötőszó, névelő, partikula
    "és", "vagy", "is", "se", "sem", "de", "hanem", "pedig", "azaz",
    "tehát", "illetve", "a", "az", "hogy", "mert", "míg", "ha",
    # létige és gyakori állítmány szám után
    "van", "volt", "lesz", "lett", "marad", "maradt", "jön", "jött",
    "nem", "már", "majd", "csak", "épp", "éppen",
    # összehasonlítás
    "mint", "több", "kevesebb", "közelebb", "távolabb", "jobb", "rosszabb",
}
_KOVETKEZO_SZO = re.compile(r"\s+([a-záéíóöőúüű]+)")


def szamok_szoval(szoveg: str) -> str:
    """"Van 12 alma" → "Van tizenkét alma". UTOLSÓNAK fut."""
    def csere(m: "re.Match[str]") -> str:
        szo = hu_szam(int(m.group(1)))
        if not szo.endswith("kettő"):
            return szo
        # Csak akkor rövidül, ha MEGSZÁMLÁLT SZÓ követi. A mondat végén álló
        # szám ("Marad 2.") és az operátor előtti ("2 egyenlő") marad teljes.
        kovet = _KOVETKEZO_SZO.match(szoveg, m.end())
        if kovet and kovet.group(1) not in _NEM_FONEV:
            return _ket(szo)
        return szo

    return _MARADEK_SZAM.sub(csere, szoveg)


def toldalekos_szam_szoval(szoveg: str) -> str:
    """"10-re" → "tízre". A jelcserék UTÁN kell futnia, különben a "2000-re"
    szóvá írása után a mellette álló "+" már nem két szám között állna, és
    kimondatlan maradna."""
    return _TOLDALEKOS_SZAM.sub(
        lambda m: hu_szam(int(m.group(1))) + m.group(2), szoveg)


# ── 5. mértékegységek kimondása ─────────────────────────────────────────────
# MIÉRT: az Azure az "5 m" szövegből BETŰT olvas: "öt em". A gyerek nem érti,
# és rosszul is rögzül. A "36 m³"-ből pedig "harminchat em három" lesz.
# Csak SZÁM UTÁN cserélünk, így a "T = a × b × m" képletben az m érintetlen
# marad – ott tényleg betűjel, nem méter.

_MERTEK_HU = {
    "mm": "milliméter", "cm": "centiméter", "dm": "deciméter",
    "m": "méter", "km": "kilométer",
    "mm²": "négyzetmilliméter", "cm²": "négyzetcentiméter",
    "dm²": "négyzetdeciméter", "m²": "négyzetméter", "km²": "négyzetkilométer",
    "mm2": "négyzetmilliméter", "cm2": "négyzetcentiméter",
    "dm2": "négyzetdeciméter", "m2": "négyzetméter", "km2": "négyzetkilométer",
    "mm³": "köbmilliméter", "cm³": "köbcentiméter",
    "dm³": "köbdeciméter", "m³": "köbméter",
    "mm3": "köbmilliméter", "cm3": "köbcentiméter",
    "dm3": "köbdeciméter", "m3": "köbméter",
    "g": "gramm", "dkg": "dekagramm", "kg": "kilogramm",
    "ml": "milliliter", "cl": "centiliter", "dl": "deciliter",
    "l": "liter", "hl": "hektoliter",
    "Ft": "forint", "€": "euró",
}

# Spanyolban a mennyiség számít: „1 metro", de „5 metros".
_MERTEK_ES = {
    "mm": ("milímetro", "milímetros"), "cm": ("centímetro", "centímetros"),
    "dm": ("decímetro", "decímetros"), "m": ("metro", "metros"),
    "km": ("kilómetro", "kilómetros"),
    "mm²": ("milímetro cuadrado", "milímetros cuadrados"),
    "cm²": ("centímetro cuadrado", "centímetros cuadrados"),
    "dm²": ("decímetro cuadrado", "decímetros cuadrados"),
    "m²": ("metro cuadrado", "metros cuadrados"),
    "km²": ("kilómetro cuadrado", "kilómetros cuadrados"),
    "mm³": ("milímetro cúbico", "milímetros cúbicos"),
    "cm³": ("centímetro cúbico", "centímetros cúbicos"),
    "dm³": ("decímetro cúbico", "decímetros cúbicos"),
    "m³": ("metro cúbico", "metros cúbicos"),
    "g": ("gramo", "gramos"), "kg": ("kilogramo", "kilogramos"),
    "ml": ("mililitro", "mililitros"), "cl": ("centilitro", "centilitros"),
    "dl": ("decilitro", "decilitros"), "l": ("litro", "litros"),
    "€": ("euro", "euros"),
}
_MERTEK_ES.update({
    "mm2": _MERTEK_ES["mm²"], "cm2": _MERTEK_ES["cm²"],
    "dm2": _MERTEK_ES["dm²"], "m2": _MERTEK_ES["m²"], "km2": _MERTEK_ES["km²"],
    "mm3": _MERTEK_ES["mm³"], "cm3": _MERTEK_ES["cm³"],
    "dm3": _MERTEK_ES["dm³"], "m3": _MERTEK_ES["m³"],
})

_BETUK = "A-Za-zÁÉÍÓÖŐÚÜŰáéíóöőúüű"


def _mertek_minta(tabla: dict) -> "re.Pattern[str]":
    """A HOSSZABB egység előbb: különben az „m³"-ból „m" lenne, és a ³ ott
    maradna. A kötőjelet kihagyjuk („5 m-es"), azt a toldalék miatt nem
    bántjuk."""
    egysegek = sorted(tabla, key=len, reverse=True)
    minta = "|".join(re.escape(e) for e in egysegek)
    return re.compile(
        r"(\d+(?:[.,]\d+)?)\s*(" + minta + r")(?![" + _BETUK + r"0-9²³·-])")


_MERTEK_RE_HU = _mertek_minta(_MERTEK_HU)
_MERTEK_RE_ES = _mertek_minta(_MERTEK_ES)


# Magyarban az egység toldalékot kap: „80 km-t", „5 m-es". A kötőjelet
# eltüntetjük, a toldalékot pedig HOZZÁRAGASZTJUK a kimondott szóhoz:
# „80 kilométert", „5 méteres". Kötőjellel hagyva az Azure külön betűzné.
_MERTEK_TOLDALEK_HU = re.compile(
    r"(\d+(?:[.,]\d+)?)\s*("
    + "|".join(re.escape(e) for e in sorted(_MERTEK_HU, key=len, reverse=True))
    + r")-([a-záéíóöőúüű]{1,5})(?![" + _BETUK + r"])")


def mertekegysegek(szoveg: str, nyelv: str = "hu") -> str:
    """„5 m" → „5 méter", „36 m³" → „36 köbméter"."""
    if nyelv != "es":
        szoveg = _MERTEK_TOLDALEK_HU.sub(
            lambda m: f"{m.group(1)} {_MERTEK_HU[m.group(2)]}{m.group(3)}", szoveg)
    if nyelv == "es":
        def csere(m: "re.Match[str]") -> str:
            szam, egyseg = m.group(1), m.group(2)
            egyes, tobbes = _MERTEK_ES[egyseg]
            return f"{szam} {egyes if szam in ('1', '1,0', '1.0') else tobbes}"
        return _MERTEK_RE_ES.sub(csere, szoveg)
    return _MERTEK_RE_HU.sub(
        lambda m: f"{m.group(1)} {_MERTEK_HU[m.group(2)]}", szoveg)


# ── 6. képletek betűjele ────────────────────────────────────────────────────
# MIÉRT: a "K = 4 × a"-ból az Azure "kö egyenlő..."-t mond, mert a K-t
# BETŰNEK olvassa. A gyerek fejében így nem kapcsolódik össze a képlet a
# fogalommal. Csak akkor cserélünk, ha a betű után egyenlőségjel áll –
# tehát tényleg képlet, nem mondatkezdő nagybetű.

_KEPLET_BETU = re.compile(r"(?<![" + _BETUK + r"])([KTAVP])(?=\s*=)")


def _kepletjel_hu(betu: str, szoveg: str) -> str | None:
    """A T kétértelmű: lehet terület és térfogat is. A szöveg dönti el, és ha
    a szöveg sem árulja el, INKÁBB NEM cseréljük – a rossz szó félrevezet."""
    also = (szoveg or "").lower()
    if betu == "K":
        return "kerület"
    if betu == "V":
        return "térfogat"
    if betu in ("T", "A"):
        terfogat = also.count("térfogat")
        terulet = also.count("terület")
        if terfogat > terulet:
            return "térfogat"
        if terulet > terfogat:
            return "terület"
        # Ha a szöveg egyik szót sem mondja ki, a mértékegység árulkodik:
        # a köbméter térfogat, a négyzetméter terület.
        if re.search(r"\d\s*[a-z]{1,2}³|\d\s*[a-z]{1,2}3\b|köb", also):
            return "térfogat"
        if re.search(r"\d\s*[a-z]{1,2}²|\d\s*[a-z]{1,2}2\b|négyzet", also):
            return "terület"
    return None


def _kepletjel_es(betu: str, szoveg: str) -> str | None:
    return {"P": "perímetro", "A": "área", "V": "volumen"}.get(betu)


def kepletjelek(szoveg: str, nyelv: str = "hu") -> str:
    """„K = 4 × a" → „kerület = 4 × a"."""
    jel = _kepletjel_es if nyelv == "es" else _kepletjel_hu

    def csere(m: "re.Match[str]") -> str:
        szo = jel(m.group(1), szoveg)
        return szo if szo else m.group(0)

    return _KEPLET_BETU.sub(csere, szoveg)


def kiejtes(szoveg: str, nyelv: str = "hu") -> str:
    """A felolvasás előtti utolsó simítás: jelekből szavak."""
    szoveg = szoveg or ""
    jelek = _MUVELET.get(nyelv) or _MUVELET["hu"]

    # A képletjel ELŐBB, amíg az egyenlőségjel még a helyén van: erről
    # ismerjük fel, hogy a betű képletet kezd, nem mondatot.
    szoveg = kepletjelek(szoveg, nyelv)
    if nyelv != "es":
        # „25%-a" → „25 százaléka". Kötőjellel hagyva külön betűzné.
        szoveg = re.sub(r"%\s*-\s*([a-záéíóöőúüű]{1,4})",
                        lambda m: " százalék" + m.group(1), szoveg)
    # A mértékegység is ELŐBB: az "×" cseréje után az "5 m × 3 m" alakban
    # a szám és az egység közé beékelődne a "szorozva".
    szoveg = mertekegysegek(szoveg, nyelv)

    # A SZORZÁS még a jelcserék előtt: utána a "×" már " szorozva " lenne.
    if nyelv == "hu":
        # ELŐBB a méretszorzás: a mértékegység cseréje már megtörtént, így a
        # "méter × 3" alakot csak itt tudjuk elkapni.
        szoveg = meretszorzas_szoval(szoveg)
        # Az ARÁNY az osztás ELŐTT: ugyanazt az alakot látják, és az arány a
        # szűkebb eset ("2 : 3" az arány szó társaságában).
        szoveg = arany_szoval(szoveg)
        szoveg = szorzas_szoval(szoveg)
        # Az OSZTÁS is: a ":" cseréje után már nem tudnánk, melyik szám az
        # osztó, és a ragot nem tudnánk hova tenni.
        szoveg = osztas_szoval(szoveg)
        szoveg = evkor_szoval(szoveg)

    for jel in _MINDIG:
        if jel in szoveg:
            szoveg = szoveg.replace(jel, jelek[jel])
    szoveg = _PLUSZ.sub(jelek["+"], szoveg)
    szoveg = _OVATOS.sub(lambda m: jelek[m.group(1)], szoveg)

    # A cseréket dupla szóköz követi (" = " → "  egyenlő  "). Ezt MOST kell
    # eltakarítani: a mondatvégi szám felismerése szóközre is illeszkedik,
    # és a dupla szóköztől nem találná meg az "egyenlő 50." alakot.
    szoveg = re.sub(r"[ \t]{2,}", " ", szoveg).strip()

    if nyelv == "hu":
        # A TOLDALÉKOS SZÁM csak most: a "+" és a "-" cseréje már megtörtént,
        # tehát a "4000 + 2000-re" plusza nem vész el.
        szoveg = toldalekos_szam_szoval(szoveg)
        szoveg = _SZAM_MONDATVEGEN.sub(lambda m: hu_szam(int(m.group(1))) + ".",
                                       szoveg)
        # UTOLSÓ LÉPÉS: ami eddig számjegy maradt, az sima tőszámnév.
        # Innentől a felolvasónak nincs mit találgatnia.
        szoveg = szamok_szoval(szoveg)
    return szoveg
