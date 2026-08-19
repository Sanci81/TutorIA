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
