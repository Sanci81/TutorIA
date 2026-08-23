# -*- coding: utf-8 -*-
"""TutorIA – az AI válaszának ellenőrzése, MIELŐTT a gyerek elolvassa.

MIÉRT VAN EZ
    Két hiba fordult elő élesben, és mindkettő rosszabb a semminél:

      1. ROSSZ VÁLASZ MEGDICSÉRVE. A gyerek 18-at írt egy 6 cm oldalú
         négyzet kerületére, a tanár pedig ezt felelte:
             „Nagyon ügyes! Pontosan 18 cm. Mert: 6 + 6 + 6 + 6 = 24"
         A saját levezetése mond ellent a saját dicséretének. Egy gyerek
         ilyenkor a DICSÉRETET hiszi el, és rosszul tanulja meg.

      2. IDEGEN ÍRÁSJEL. Egy gratulációban ez állt: „интернетen".
         A nyelvi modell néha átvált egy másik írásrendszerre egy-egy szó
         közepén. Egy magyar vagy spanyol tanulószövegben ennek nincs helye.

    Egyik hiba sem javítható promptban megbízhatóan – a modell néha akkor is
    hibázik, ha kértük, hogy ne. Ezért ITT, számolással ellenőrizzük.

MIT NEM TUD
    Azt nem tudja megmondani, hogy a MAGYARÁZAT jó-e, csak azt, hogy a
    leírt számolás stimmel-e, és hogy a kimondott eredmény egyezik-e vele.
"""

from __future__ import annotations

import re
import unicodedata

# ── 1. idegen írásrendszer ──────────────────────────────────────────────────
# Cirill betűk latinra. A modell néha egy szó közepén vált írásrendszert
# ("интернет"), a jelentés viszont ilyenkor is a latin olvasat.
_CIRILL = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "jo",
    "ж": "zs", "з": "z", "и": "i", "й": "j", "к": "k", "л": "l", "м": "m",
    "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u",
    "ф": "f", "х": "h", "ц": "c", "ч": "cs", "ш": "s", "щ": "scs",
    "ъ": "", "ы": "i", "ь": "", "э": "e", "ю": "ju", "я": "ja",
}
_CIRILL_TARTOMANY = re.compile(r"[Ѐ-ӿ]+")


def _cirill_at(szo: str) -> str:
    ki = []
    for betu in szo:
        kicsi = betu.lower()
        latin = _CIRILL.get(kicsi, betu)
        ki.append(latin.upper() if betu != kicsi and latin else latin)
    return "".join(ki)


def latinra(szoveg: str) -> str:
    """Cirill betűs részek latinra írása. A magyar ékezeteket nem bántja."""
    if not szoveg:
        return szoveg
    return _CIRILL_TARTOMANY.sub(lambda m: _cirill_at(m.group(0)), szoveg)


def van_idegen_iras(szoveg: str) -> bool:
    """Van-e a szövegben nem latin (és nem írásjel) betű."""
    for betu in szoveg or "":
        if not betu.isalpha():
            continue
        try:
            nev = unicodedata.name(betu)
        except ValueError:
            return True
        if not nev.startswith("LATIN"):
            return True
    return False


# ── 2. a leírt számolás ellenőrzése ─────────────────────────────────────────
# Csak egész számok és a négy alapművelet. Ennél többet szándékosan nem
# vállalunk: amit nem értünk biztosan, azt nem is minősítjük hibásnak.
_SZORZAS = "×⋅*x"
_OSZTAS = "÷/:"
_EGYENLET = re.compile(
    r"(?<![\d.,])(\d{1,6}(?:\s*[-+" + _SZORZAS + _OSZTAS + r"]\s*\d{1,6})+)"
    r"\s*=\s*(\d{1,7})(?![\d.,])"
)
_TAG = re.compile(r"\d+|[-+" + _SZORZAS + _OSZTAS + r"]")


def _kiszamol(kifejezes: str) -> int | None:
    """Balról jobbra, a szorzás/osztás előbb. None, ha nem tiszta eset."""
    tagok = _TAG.findall(kifejezes.replace(" ", ""))
    if not tagok or len(tagok) % 2 == 0:
        return None
    # elsőbbség: szorzás és osztás
    szint1: list = [int(tagok[0])]
    i = 1
    while i < len(tagok) - 1:
        jel, szam = tagok[i], int(tagok[i + 1])
        if jel in _SZORZAS:
            szint1[-1] = szint1[-1] * szam
        elif jel in _OSZTAS:
            if szam == 0 or szint1[-1] % szam:
                return None               # törtet nem vállalunk
            szint1[-1] = szint1[-1] // szam
        else:
            szint1.append(jel)
            szint1.append(szam)
        i += 2
    # majd összeadás és kivonás
    ki = szint1[0]
    j = 1
    while j < len(szint1) - 1:
        jel, szam = szint1[j], szint1[j + 1]
        ki = ki + szam if jel == "+" else ki - szam
        j += 2
    return ki


def hibas_egyenletek(szoveg: str) -> list[tuple[str, int, int]]:
    """A szövegben szereplő ROSSZ számolások: (kifejezés, leírt, helyes)."""
    rossz = []
    for m in _EGYENLET.finditer(szoveg or ""):
        helyes = _kiszamol(m.group(1))
        if helyes is None:
            continue
        leirt = int(m.group(2))
        if helyes != leirt:
            rossz.append((m.group(0), leirt, helyes))
    return rossz


# ── 3. a dicséret és a levezetés ellentmondása ──────────────────────────────
# "Pontosan 18 cm." + "6 + 6 + 6 + 6 = 24" – a kettő nem lehet egyszerre igaz.
_ALLITAS = re.compile(
    r"(?:pontosan|helyes(?:en)?|az eredmény|a kerülete|a válasz"
    r"|exactamente|correcto|el resultado|el perímetro)"
    r"[^.\n\d]{0,20}(\d{1,7})",
    re.IGNORECASE,
)


def ellentmondas(szoveg: str) -> str | None:
    """Ellentmond-e a válasz önmagának. Visszaadja az okot, vagy None-t."""
    szoveg = szoveg or ""

    rossz = hibas_egyenletek(szoveg)
    if rossz:
        kif, leirt, helyes = rossz[0]
        return f"a leírt számolás hibás: „{kif}”, helyesen {helyes}"

    eredmenyek = set()
    for m in _EGYENLET.finditer(szoveg):
        if _kiszamol(m.group(1)) is not None:
            eredmenyek.add(int(m.group(2)))
    if not eredmenyek:
        return None

    for m in _ALLITAS.finditer(szoveg):
        allitott = int(m.group(1))
        if allitott not in eredmenyek:
            return (f"a válasz {allitott}-t állít, de a levezetés "
                    f"{sorted(eredmenyek)} eredményt ad")
    return None


def rendben(szoveg: str) -> bool:
    """Kiadható-e a gyereknek. Csak akkor False, ha BIZTOSAN hibás."""
    return ellentmondas(szoveg) is None and not van_idegen_iras(szoveg)
