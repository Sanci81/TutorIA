# -*- coding: utf-8 -*-
"""A kvízkérdések számtani megoldókulcsának ellenőrzése.

MIÉRT KELL
    A kérdéseket és a válaszokat is a nyelvi modell írja. Szöveges kérdésnél
    ez rendben van, számtani kérdésnél viszont nincs: a modell FEJBŐL számol,
    és téved. Éles teszten a 4. osztályos szintfelmérőn négy kérdésből négyszer
    a PROGRAM tévedett, nem a gyerek:

        1500 + 2500  →  a kulcs 3000 volt   (helyesen 4000)
         800 -  235  →  a kulcs  575 volt   (helyesen  565)
         360 :    9  →  a kulcs   30 volt   (helyesen   40)
        4500 :  150  →  a kulcs   25 volt   (helyesen   30)

    Ez a lehető legrosszabb hiba: a gyerek jól számol, a program pirosra
    festi. Egyszer megbocsátja, másodszor nem hisz többé a programnak.

MIT CSINÁL
    Kikeresi a kérdés szövegéből a számtani műveletet, KISZÁMOLJA, és
    összeveti a modell válaszával. Ha eltér, a SAJÁT számítása nyer.

MIT NEM CSINÁL
    Nem próbál okos lenni. Ha a kérdés nem egyértelmű – szöveges feladat,
    becslés, több különböző művelet –, hozzá sem nyúl. Inkább maradjon
    ellenőrizetlen egy kérdés, mint hogy egy jót elrontsunk.
"""

from __future__ import annotations

import re

import hang

# A művelet jelei, ahogy egy magyar vagy spanyol feladatlapon előfordulnak.
# Az osztás lehet ":", "/" vagy "÷", a szorzás "×", "x", "*" vagy "·".
_JELEK = {
    "+": "+", "-": "-", "−": "-", "–": "-", "—": "-",
    "*": "*", "×": "*", "x": "*", "X": "*", "·": "*",
    "/": "/", ":": "/", "÷": "/",
}

# Egy művelet: szám, jel, szám, és ez ismételhető.
# A számban lehet ezres szóköz (1 500) vagy pont (1.500) – a magyar és a
# spanyol írásmód is. Tizedesjegy vesszővel vagy ponttal.
_SZAM = r"(?:" + r"\d{1,3}(?:[  .]\d{3})+" + r"|\d+(?:[.,]\d+)?" + r")"
_JEL = r"[+\-−–—*×xX·/:÷]"

# A SZÓKÖZ ITT BIZTONSÁGI KÉRDÉS, nem szépészeti.
#   "1848-49"  évszám, nem kivonás
#   "10:30"    óra, nem osztás
#   "3/4"      tört, nem osztás
# Ezek mind értelmes műveletnek látszanak, és ha kiszámolnánk őket, egy jó
# kérdés megoldókulcsát írnánk felül. Ezért a +, -, /, :, x jelek KÖRÜL
# szóközt követelünk – így csak az számít műveletnek, amit a modell tényleg
# feladatnak szánt ("Mennyi 800 - 235?"). A ×, ÷ és · félreérthetetlen
# matematikai jel, azoknál nem kell szóköz.
_MUVELET = r"(?:\s*[×÷·]\s*|\s+[-+*/:xX–—−]\s+)"
_KIFEJEZES = re.compile(rf"(?<![\w.,]){_SZAM}(?:{_MUVELET}{_SZAM})+(?![\w])")

# Ha ezek bármelyike szerepel a kérdésben, NEM nyúlunk hozzá: nem a pontos
# érték a várt válasz, hanem egy becslés vagy egy magyarázat.
_KIVETEL = re.compile(
    r"becs[üu]l|k[öo]zel[íi]t|nagyj[áa]b[óa]l|k[öo]r[üu]lbel[üu]l|kerek[íi]t"
    r"|aproxim|estim|redonde|cerca de|m[áa]s o menos",
    re.IGNORECASE,
)


def _szamma(s: str) -> float:
    """'1 500' → 1500.0, '2,5' → 2.5, '1.500' → 1500.0"""
    s = s.strip().replace(" ", " ")
    if re.fullmatch(r"\d{1,3}(?:[ .]\d{3})+", s):      # ezres elválasztó
        return float(s.replace(" ", "").replace(".", ""))
    return float(s.replace(" ", "").replace(",", "."))


def _kiertekel(kif: str) -> float | None:
    """Egy műveletsor értéke. Csak + - * / , helyes precedenciával.

    Nem eval() – az bármit lefuttatna, amit a modell a kérdésbe írt.
    """
    darabok = re.findall(rf"{_SZAM}|{_JEL}", kif)
    if len(darabok) < 3 or len(darabok) % 2 == 0:
        return None
    try:
        ertekek = [_szamma(darabok[0])]
        jelek: list[str] = []
        for i in range(1, len(darabok), 2):
            jel = _JELEK.get(darabok[i])
            if jel is None:
                return None
            szam = _szamma(darabok[i + 1])
            if jel in ("*", "/"):                       # előbb szoroz-oszt
                if jel == "/":
                    if szam == 0:
                        return None
                    ertekek[-1] /= szam
                else:
                    ertekek[-1] *= szam
            else:
                jelek.append(jel)
                ertekek.append(szam)
        ossz = ertekek[0]
        for jel, szam in zip(jelek, ertekek[1:]):
            ossz = ossz + szam if jel == "+" else ossz - szam
        return ossz
    except (ValueError, IndexError, ZeroDivisionError):
        return None


def szamitott_valasz(kerdes: str) -> float | None:
    """A kérdésben szereplő művelet eredménye, vagy None, ha nem egyértelmű."""
    if not kerdes or _KIVETEL.search(kerdes):
        return None
    talalatok = _KIFEJEZES.findall(kerdes)
    # Csak akkor nyúlunk hozzá, ha PONTOSAN EGY művelet van a kérdésben.
    # Kettőnél nem tudjuk, melyikre kérdez rá.
    if len(talalatok) != 1:
        return None
    # "x" csak akkor szorzás, ha tényleg két szám között áll – nem ismeretlen.
    return _kiertekel(talalatok[0])


def _mint_szam(szoveg: str) -> float | None:
    """A válaszszövegből a szám, ha a válasz LÉNYEGE egy szám."""
    if szoveg is None:
        return None
    t = str(szoveg).strip()
    if not t:
        return None
    t = re.sub(r"[^\d\s., -]", "", t).strip(" .,-")
    if not t:
        return None
    try:
        return _szamma(t)
    except ValueError:
        return None


def _szoveg(ertek: float) -> str:
    return str(int(ertek)) if float(ertek).is_integer() else f"{ertek:g}"


def _egyezik(a: float | None, b: float | None) -> bool:
    return a is not None and b is not None and abs(a - b) < 1e-6


def ellenoriz(kerdesek: list[dict]) -> tuple[list[dict], list[str]]:
    """Végigmegy a kérdéseken, és javítja a rossz számtani megoldókulcsot.

    Visszaad: (kérdések, napló). A napló csak a fejlesztői logba megy.
    """
    naplo: list[str] = []
    kimenet: list[dict] = []

    for k in kerdesek:
        varhato = szamitott_valasz(k.get("q", ""))
        if varhato is None:
            kimenet.append(k)
            continue

        helyes = _szoveg(varhato)

        if k.get("type") == "mc":
            opciok = list(k.get("options") or [])
            if not opciok:
                kimenet.append(k)
                continue
            jo_index = next(
                (i for i, o in enumerate(opciok)
                 if _egyezik(_mint_szam(o), varhato)), None)
            if jo_index is not None:
                if jo_index != k.get("correct"):
                    naplo.append(f"{k['q']!r}: correct {k.get('correct')} → {jo_index}")
                    k = {**k, "correct": jo_index}
            else:
                # Egyik válaszlehetőség sem a helyes eredmény. A megjelöltet
                # cseréljük ki a valódi értékre – így a kérdés használható
                # marad, és biztosan van jó válasz.
                jelolt = k.get("correct", 0)
                if not isinstance(jelolt, int) or not 0 <= jelolt < len(opciok):
                    jelolt = 0
                if helyes in opciok:                     # ne legyen két azonos
                    naplo.append(f"{k['q']!r}: eldobva (nem javítható)")
                    continue
                naplo.append(f"{k['q']!r}: {opciok[jelolt]!r} → {helyes!r}")
                opciok[jelolt] = helyes
                k = {**k, "options": opciok, "correct": jelolt}
            kimenet.append(k)
            continue

        # fill / sent: egyetlen válasz van, azt írjuk felül
        adott = _mint_szam(k.get("answer"))
        if adott is None:
            # A kérdés számtani, de a válasz nem szám – ez gyanús, de nem
            # tudjuk biztosan, hogy hiba. Meghagyjuk.
            kimenet.append(k)
            continue
        if not _egyezik(adott, varhato):
            naplo.append(f"{k.get('q')!r}: {k.get('answer')!r} → {helyes!r}")
            k = {**k, "answer": helyes}
        kimenet.append(k)

    return kimenet, naplo


def azonos_szam(a, b) -> bool:
    """Két válasz ugyanaz a SZÁM-e, az írásmódtól függetlenül.

    "4 000", "4000", "4000." és "4.000" mind ugyanaz. A gyerek nem azért
    kap pirosat, mert szóközzel tagolta az ezreseket.
    """
    x, y = _mint_szam(a), _mint_szam(b)
    return _egyezik(x, y)


# ── A TANÁR SAJÁT SZÁMÍTÁSAI A BESZÉLGETÉSBEN ───────────────────────────────
# A kvíz megoldókulcsát már ellenőrizzük. A tanár viszont a CHATBEN is állít
# dolgokat a számokról, és ott eddig semmi nem nézte meg. Élesben ez jött ki:
#
#     "Szerinted a 19 × 4 inkább 60, 70 vagy 80?"
#
# A 19 × 4 az 76. Egyik felkínált szám sem az. A gyerek vagy talál, vagy
# elhiszi, hogy 80 — és mindkettő rosszabb, mintha meg sem kérdezték volna.

_ALLITAS = re.compile(
    rf"({_SZAM}(?:{_MUVELET}{_SZAM})+)\s*"
    r"(?:=|\bval[óo]ban\b|\baz\b|\bannyi,? mint\b|\bes igual a\b|\bes\b)\s*"
    rf"({_SZAM})",
    re.IGNORECASE,
)

# "…60, 70 vagy 80?" – két-négy felkínált szám a mondat végén.
_VALASZTAS = re.compile(
    rf"({_SZAM})(?:\s*,\s*({_SZAM}))?(?:\s*,\s*({_SZAM}))?"
    r"\s*(?:vagy|o|or)\s*"
    rf"({_SZAM})\s*\?",
    re.IGNORECASE,
)


# ── A BECSLŐ KÉRDÉS MEGFOGALMAZÁSA ──────────────────────────────────────────
# ÉLES PÉLDA, amit a gyerek kapott:
#
#     "Most jön egy kis becslés: 48 × 2 inkább 80, 90 vagy 100?"
#
# A 48 × 2 az 96. Egyik felkínált szám sem az — és a kérdésből nem derül ki,
# hogy nem is kell, hogy az legyen. A gyerek azt hallja, hogy "mennyi 48 × 2:
# 80, 90 vagy 100?", amire NINCS jó válasz. Emiatt vagy tippel, vagy elhiszi,
# hogy a 100 a helyes eredmény.
#
# Magyarul a kérdés így teljes:
#
#     "48 × 2 inkább 80-hoz, 90-hez vagy 100-hoz van közelebb?"
#
# Ettől lesz nyilvánvaló, hogy KÖZELSÉGET kérdezünk, nem egyenlőséget. A rag
# is kell hozzá: rag nélkül ("inkább 80, 90 vagy 100") a mondat befejezetlen.
#
# MIÉRT ÁTÍRÁS ÉS NEM UTASÍTÁS A TANÁRNAK: a promptban leírt szabályt a modell
# nem mindig tartja be — ez a kérdés is így jutott el a gyerekig. Az átírás
# viszont mindig megtörténik.
_BECSLES_KERDES = re.compile(
    r"\binkább\b\s+((?:" + _SZAM + r")(?:\s*,\s*(?:" + _SZAM + r"))*"
    r"\s+(?:vagy|avagy)\s+(?:" + _SZAM + r"))\s*\?",
    re.IGNORECASE,
)
# Ha ez már benne van, a tanár jól fogalmazott – nem nyúlunk hozzá.
_MAR_JO = re.compile(r"k[öo]zelebb|k[öo]zel[íi]t", re.IGNORECASE)


def becsles_kerdes_javit(szoveg: str) -> tuple[str, list[str]]:
    """"inkább 80, 90 vagy 100?" → "inkább 80-hoz, 90-hez vagy 100-hoz van közelebb?"

    Csak akkor ír át, ha a felkínáltak MIND egész számok. Tizedes törtnél és
    mértékegységnél inkább nem nyúlunk hozzá, mint hogy elrontsuk.
    """
    naplo: list[str] = []
    if not szoveg or "inkább" not in szoveg.lower():
        return szoveg, naplo

    def csere(m: "re.Match[str]") -> str:
        egesz = m.group(0)
        if _MAR_JO.search(egesz):
            return egesz
        szamok = re.findall(_SZAM, m.group(1))
        if not 2 <= len(szamok) <= 4:
            return egesz
        ertekek = []
        for sz in szamok:
            v = _szamma(sz)
            if v != int(v):                 # tizedes tört: nem ragozunk
                return egesz
            ertekek.append(int(v))
        raggal = [f"{sz}-{hang.hoz_rag(e)}" for sz, e in zip(szamok, ertekek)]
        ki = ("inkább " + ", ".join(raggal[:-1]) + " vagy " + raggal[-1]
              + " van közelebb?")
        naplo.append(f"becslo kerdes atirva: {egesz!r} → {ki!r}")
        return ki

    return _BECSLES_KERDES.sub(csere, szoveg), naplo


def chat_ellenoriz(szoveg: str) -> tuple[str, list[str]]:
    """A tanár chat-üzenetében a számtani állítások ellenőrzése.

    Két dolgot csinál:
      1. A HAMIS EGYENLŐSÉGET javítja ("6 × 5 valóban 31" → "30"). Ez
         egyértelmű: a szorzás értéke nem vélemény.
      2. A VÁLASZTÁSOS KÉRDÉST csak JELZI, ha a helyes érték nincs a
         felkínáltak között. Ezt SZÁNDÉKOSAN nem írjuk át: lehet, hogy a
         tanár becslést kért, és a kérdés átírásával mi rontanánk el.
    """
    naplo: list[str] = []
    if not szoveg:
        return szoveg, naplo

    def javit(m: "re.Match[str]") -> str:
        ertek = _kiertekel(m.group(1))
        allitott = _szamma(m.group(2))
        if ertek is None or _egyezik(ertek, allitott):
            return m.group(0)
        naplo.append(f"hamis allitas: {m.group(0)!r} → {_szoveg(ertek)}")
        return m.group(0).replace(m.group(2), _szoveg(ertek))

    javitott = _ALLITAS.sub(javit, szoveg)

    # A becslő kérdés megfogalmazása. ELŐBB, mint a választhatatlanság
    # vizsgálata: az átírt kérdésre már VAN jó válasz, tehát nincs mit jelezni.
    javitott, becsles_naplo = becsles_kerdes_javit(javitott)
    naplo.extend(becsles_naplo)

    mondatok = re.split(r"(?<=[.!?…])\s+", javitott)
    for i, mondat in enumerate(mondatok):
        if _KIVETEL.search(mondat):
            continue                      # becslést kért – ott nem baj
        valasztas = _VALASZTAS.search(mondat)
        if not valasztas:
            continue
        # A művelet gyakran az ELŐZŐ mondatban áll: "Mennyi 8 × 7?
        # Szerinted 54, 56 vagy 58?" Ezért egy mondatot visszanézünk.
        kifejezes = _KIFEJEZES.search(mondat)
        if not kifejezes and i > 0:
            if _KIVETEL.search(mondatok[i - 1]):
                continue
            kifejezes = _KIFEJEZES.search(mondatok[i - 1])
        if not kifejezes:
            continue
        ertek = _kiertekel(kifejezes.group(0))
        if ertek is None:
            continue
        opciok = [_szamma(x) for x in valasztas.groups() if x]
        if not any(_egyezik(ertek, o) for o in opciok):
            naplo.append(
                f"valaszthatatlan kerdes: {kifejezes.group(0)} = {_szoveg(ertek)}, "
                f"felkinalva: {[_szoveg(o) for o in opciok]}")

    return javitott, naplo
