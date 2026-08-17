# -*- coding: utf-8 -*-
"""TutorIA – az AI által rajzolt ábrák ellenőrzése és javítása.

MIÉRT VAN EZ
    Az AI néha hibás SVG-t ad vissza. A leggyakoribb hibák:

      1. FEKETE KOCKA. Az SVG-ben egy alakzat alapértelmezésben FEKETÉVEL
         KITÖLTÖTT. Ha az AI elfelejti kiírni a `fill="none"`-t, tömör fekete
         doboz lesz belőle. Ez nem véletlen és nem "képernyőhiba" – ez a
         szabvány. Itt kényszerítjük ki, így többé nem fordulhat elő.

      2. EGYMÁSRA CSÚSZÓ FELIRATOK. Két szöveg egymáson olvashatatlan.
         Ilyenkor NEM mutatjuk meg az ábrát. Jobb, ha nincs rajz, mint ha
         rossz van: a gyereket a zavaros ábra összezavarja, a hiánya nem.

      3. KILÓGÓ SZÖVEG. A felirat kifut a rajzterületről és levágódik.
         Ezt meg tudjuk javítani: kitágítjuk a rajzterületet.

MIT NEM TUD EZ A FÁJL
    Azt nem tudja megítélni, hogy a rajz ÖTLETE jó-e. Ha az AI a „biztos"
    mellé napot rajzol, miközben hóról van szó, az itt hibátlan SVG. A
    tartalmi helyességet a rajzolási szabályok (prompt) terelik, nem ez.
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET

NS = "http://www.w3.org/2000/svg"

# Ezeken az elemeken a hiányzó fill FEKETE kitöltést jelent.
_ALAKZATOK = ("rect", "circle", "ellipse", "polygon", "path")
# Ezeken a hiányzó fill nem zavaró (nincs belsejük), de a stroke kell.
_VONALAK = ("line", "polyline")

# Egy átlagos betű szélessége a betűmérethez képest, sans-serif fontnál.
# Mérve: a „Lehetséges" 16 pixeles Segoe UI-ban ~84 px = 0.53 × 16 × 10.
_BETU_ARANY = 0.55
_ALAP_BETU = 16.0


def _tag(el) -> str:
    """Névtér nélküli elemnév kisbetűvel."""
    t = el.tag
    if isinstance(t, str) and t.startswith("{"):
        t = t.split("}", 1)[1]
    return (t or "").lower()


def _szam(ertek, alap: float = 0.0) -> float:
    try:
        return float(str(ertek).strip().replace("px", ""))
    except (TypeError, ValueError):
        return alap


def _oroklott_betumeret(el, szulok: dict) -> float:
    """A felirat betűmérete, a szülőktől örökölve, ha nincs sajátja."""
    mostani = el
    while mostani is not None:
        m = mostani.get("font-size")
        if m:
            return _szam(m, _ALAP_BETU) or _ALAP_BETU
        mostani = szulok.get(id(mostani))
    return _ALAP_BETU


def _felirat_doboza(el, szulok: dict) -> tuple[float, float, float, float] | None:
    """Egy <text> befoglaló téglalapja: (bal, teto, jobb, alj).

    Becslés, nem pixelpontos – de a fedéshez bőven elég, és mindig a
    biztonság felé téved (inkább nagyobbnak méri a szöveget).
    """
    szoveg = "".join(el.itertext()).strip()
    if not szoveg:
        return None
    meret = _oroklott_betumeret(el, szulok)
    x = _szam(el.get("x"), 0.0)
    y = _szam(el.get("y"), 0.0)
    szeles = len(szoveg) * meret * _BETU_ARANY
    horgony = (el.get("text-anchor") or "start").strip().lower()
    if horgony == "middle":
        bal = x - szeles / 2
    elif horgony == "end":
        bal = x - szeles
    else:
        bal = x
    # Az y a betű alapvonala: fölötte ~0.78, alatta ~0.22 betűméretnyi rész.
    return (bal, y - meret * 0.78, bal + szeles, y + meret * 0.22)


def _fedik_egymast(a, b, tures: float = 1.5) -> bool:
    """Két doboz átfed-e. A tűrés miatt az épp összeérő feliratok még jók."""
    return not (
        a[2] - tures <= b[0]
        or b[2] - tures <= a[0]
        or a[3] - tures <= b[1]
        or b[3] - tures <= a[1]
    )


def javit(svg: str, *, max_feliratok: int = 40) -> str | None:
    """Ellenőrzi és megjavítja az AI ábráját.

    Visszaad javított SVG-t, vagy None-t, ha az ábra menthetetlen –
    ilyenkor a gyerek egyszerűen nem lát rajzot.
    """
    if not svg or not svg.strip():
        return None

    try:
        ET.register_namespace("", NS)
        gyoker = ET.fromstring(svg)
    except ET.ParseError:
        return None                       # hibás XML – nem mutatjuk meg

    if _tag(gyoker) != "svg":
        return None

    # szülő-térkép a betűméret örökléséhez
    szulok: dict[int, object] = {}
    for el in gyoker.iter():
        for gy in list(el):
            szulok[id(gy)] = el

    # ── 1. a fekete kocka kiiktatása ────────────────────────────────────
    for el in gyoker.iter():
        t = _tag(el)
        if t in _ALAKZATOK:
            if not (el.get("fill") or "").strip():
                el.set("fill", "none")
            if not (el.get("stroke") or "").strip():
                el.set("stroke", "#222")
                if not (el.get("stroke-width") or "").strip():
                    el.set("stroke-width", "3")
        elif t in _VONALAK:
            if not (el.get("stroke") or "").strip():
                el.set("stroke", "#222")
                if not (el.get("stroke-width") or "").strip():
                    el.set("stroke-width", "3")
        elif t == "text":
            if not (el.get("fill") or "").strip():
                el.set("fill", "#222")

    # ── 2. van-e egyáltalán rajz? ───────────────────────────────────────
    alakzat_db = sum(1 for el in gyoker.iter()
                     if _tag(el) in _ALAKZATOK + _VONALAK)
    feliratok = [el for el in gyoker.iter() if _tag(el) == "text"]
    if alakzat_db == 0:
        return None                       # csak szöveg – az nem ábra
    if len(feliratok) > max_feliratok:
        return None                       # zsúfolt, olvashatatlan

    # ── 3. egymásra csúszó feliratok → inkább semmi ─────────────────────
    dobozok = []
    for el in feliratok:
        d = _felirat_doboza(el, szulok)
        if d:
            dobozok.append(d)
    for i in range(len(dobozok)):
        for j in range(i + 1, len(dobozok)):
            if _fedik_egymast(dobozok[i], dobozok[j]):
                return None

    # ── 4. kilógó felirat → a rajzterület kitágítása ────────────────────
    vb = (gyoker.get("viewBox") or "").replace(",", " ").split()
    if len(vb) != 4:
        return None
    x0, y0, sz, ma = (_szam(v) for v in vb)
    if sz <= 0 or ma <= 0:
        return None

    x1, y1 = x0 + sz, y0 + ma
    for bal, teto, jobb, alj in dobozok:
        x0 = min(x0, bal - 4)
        y0 = min(y0, teto - 4)
        x1 = max(x1, jobb + 4)
        y1 = max(y1, alj + 4)

    uj_sz, uj_ma = x1 - x0, y1 - y0
    # Ha a kitágítás eltorzítaná az ábrát (több mint a duplájára nő), az azt
    # jelenti, hogy a felirat valahol az űrben van – az nem jó rajz.
    if uj_sz > sz * 2.2 or uj_ma > ma * 2.2:
        return None
    gyoker.set("viewBox", f"{x0:g} {y0:g} {uj_sz:g} {uj_ma:g}")

    # a méretet a böngésző adja, ne feszítse szét a chatbuborékot
    for attr in ("width", "height"):
        if gyoker.get(attr):
            del gyoker.attrib[attr]

    ki = ET.tostring(gyoker, encoding="unicode")
    # az ElementTree néha ns0: előtagot tesz ki – azt takarítjuk
    ki = re.sub(r"\bns\d+:", "", ki)
    ki = ki.replace(f' xmlns:ns0="{NS}"', "")
    if "xmlns=" not in ki:
        ki = ki.replace("<svg", f'<svg xmlns="{NS}"', 1)
    return ki
