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
# Egy gyereknek szánt hangos válasz 2-3 mondat. 420 karakter bőven ennyi.
# Ha ennél hosszabb, MONDATHATÁRON vágunk – nem a szó közepén.
MAX_KARAKTER = 420

# ── 3. napi keret gyerekenként ──────────────────────────────────────────────
# 12 000 karakter kb. 25-30 tanári forduló: egy bőséges tanulónap.
# Fölötte a felolvasás kikapcsol aznapra, a szöveges tanítás megy tovább.
NAPI_KERET = 12_000

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
           "/": " osztva ", "÷": " osztva ", "%": " százalék ",
           "x": " szorozva ", "X": " szorozva ",
           "<": " kisebb mint ", ">": " nagyobb mint "},
    "es": {"=": " igual a ", "+": " más ", "-": " menos ",
           "*": " por ", "×": " por ", "⋅": " por ",
           "/": " entre ", "÷": " entre ", "%": " por ciento ",
           "x": " por ", "X": " por ",
           "<": " menor que ", ">": " mayor que "},
}

# Ezek a jelek SOHA nem jelentenek mást magyar szövegben, így bárhol cserélhetők.
_MINDIG = ("×", "⋅", "÷", "=", "%", "<", ">")
# Ezek viszont igen: a "-" toldalékot köt ("1848-ban"), a "/" dátumot választ
# el, a "*" pedig kiemelés lehet. Ezért CSAK két szám között, szóközökkel.
# Az "x" is lehet szorzásjel ("9 x 10"), de csak akkor, ha KÉT szám között
# áll, szóközökkel. Az algebrai "3x" így érintetlen marad.
_OVATOS = re.compile(r"(?<=\d)\s+([-+*/xX])\s+(?=\d)")
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


def kiejtes(szoveg: str, nyelv: str = "hu") -> str:
    """A felolvasás előtti utolsó simítás: jelekből szavak."""
    szoveg = szoveg or ""
    jelek = _MUVELET.get(nyelv) or _MUVELET["hu"]

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
        szoveg = _SZAM_MONDATVEGEN.sub(lambda m: hu_szam(int(m.group(1))) + ".",
                                       szoveg)
    return szoveg
