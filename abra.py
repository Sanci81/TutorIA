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
    return _doboz(szoveg, _oroklott_betumeret(el, szulok),
                  _szam(el.get("x"), 0.0), _szam(el.get("y"), 0.0),
                  (el.get("text-anchor") or "start").strip().lower())


def _doboz(szoveg: str, meret: float, x: float, y: float,
           horgony: str) -> tuple[float, float, float, float]:
    """Egy felirat befoglaló téglalapja a megadott helyen és betűmérettel."""
    szeles = len(szoveg) * meret * _BETU_ARANY
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


def _vilagossag(szin: str) -> float | None:
    """Egy szín világossága 0 (fekete) és 1 (fehér) között. None, ha nem értjük."""
    sz = (szin or "").strip().lower()
    if not sz or sz in ("none", "transparent"):
        return None
    _NEVEK = {"black": 0.0, "white": 1.0, "navy": 0.1, "darkblue": 0.12,
              "gray": 0.5, "grey": 0.5, "silver": 0.75, "red": 0.3,
              "green": 0.35, "blue": 0.15, "yellow": 0.9}
    if sz in _NEVEK:
        return _NEVEK[sz]
    m = re.fullmatch(r"#([0-9a-f]{3}|[0-9a-f]{6})", sz)
    if not m:
        return None
    jegy = m.group(1)
    if len(jegy) == 3:
        jegy = "".join(k * 2 for k in jegy)
    r, g, b = (int(jegy[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _alakzat_doboza(el) -> tuple[float, float, float, float] | None:
    """Egy alakzat befoglaló téglalapja: (bal, teto, jobb, alj)."""
    t = _tag(el)
    if t == "rect":
        x, y = _szam(el.get("x")), _szam(el.get("y"))
        w, h = _szam(el.get("width")), _szam(el.get("height"))
        return (x, y, x + w, y + h) if w > 0 and h > 0 else None
    if t == "circle":
        cx, cy, r = _szam(el.get("cx")), _szam(el.get("cy")), _szam(el.get("r"))
        return (cx - r, cy - r, cx + r, cy + r) if r > 0 else None
    if t == "ellipse":
        cx, cy = _szam(el.get("cx")), _szam(el.get("cy"))
        rx, ry = _szam(el.get("rx")), _szam(el.get("ry"))
        return (cx - rx, cy - ry, cx + rx, cy + ry) if rx > 0 and ry > 0 else None
    if t == "line":
        x1, y1 = _szam(el.get("x1")), _szam(el.get("y1"))
        x2, y2 = _szam(el.get("x2")), _szam(el.get("y2"))
        return (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))
    # polygon / polyline / path: a koordinátákból
    nyers = el.get("points") or el.get("d") or ""
    szamok = [float(v) for v in re.findall(r"-?\d+(?:\.\d+)?", nyers)]
    if len(szamok) < 4:
        return None
    xs, ys = szamok[0::2], szamok[1::2]
    return (min(xs), min(ys), max(xs), max(ys))


_VONAL_FELVASTAG = 3.0                        # a rajzolt vonal fél vastagsága


def _szakasz_dobozai(x1, y1, x2, y2,
                     v: float = _VONAL_FELVASTAG) -> list[tuple[float, float, float, float]]:
    """Egy egyenes szakasz vékony dobozok láncaként.

    A szakasz BEFOGLALÓ téglalapja átlós vonalnál sokkal nagyobb, mint maga a
    vonal – emiatt régen a sarokba írt feliratot is hibásnak láttuk. Ezért a
    vonalat végigpontozzuk, és minden pont köré egy kis dobozt teszünk.
    """
    hossz = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    db = max(1, min(240, int(hossz / v) + 1))
    ki = []
    for i in range(db + 1):
        t = i / db
        px, py = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t
        ki.append((px - v, py - v, px + v, py + v))
    return ki


def _alakzat_vonalai(el) -> list[tuple[float, float, float, float]]:
    """Az alakzat RAJZOLT vonalai vékony dobozokként – a feliratnak ezekre
    nem szabad rácsúsznia. Kör és ellipszis nincs itt: azokat képlettel
    vizsgáljuk (_ellipszis_vonalan), mert dobozokkal pontatlan volna."""
    t = _tag(el)
    v = _VONAL_FELVASTAG
    if t == "rect":
        d = _alakzat_doboza(el)
        if not d:
            return []
        bal, teto, jobb, alj = d
        return [(bal - v, teto - v, jobb + v, teto + v),
                (bal - v, alj - v, jobb + v, alj + v),
                (bal - v, teto - v, bal + v, alj + v),
                (jobb - v, teto - v, jobb + v, alj + v)]
    if t == "line":
        return _szakasz_dobozai(_szam(el.get("x1")), _szam(el.get("y1")),
                                _szam(el.get("x2")), _szam(el.get("y2")))
    if t in ("polygon", "polyline"):
        sz = [float(k) for k in
              re.findall(r"-?\d+(?:\.\d+)?", el.get("points") or "")]
        pontok = list(zip(sz[0::2], sz[1::2]))
        if len(pontok) < 2:
            return []
        if t == "polygon":
            pontok.append(pontok[0])
        ki = []
        for i in range(len(pontok) - 1):
            ki.extend(_szakasz_dobozai(pontok[i][0], pontok[i][1],
                                       pontok[i + 1][0], pontok[i + 1][1]))
            if len(ki) > 1500:
                break
        return ki
    return []                                 # path: nem kockáztatunk


# a régi név, ha máshonnan hivatkoznának rá
_elek = _alakzat_vonalai


def _ellipszis_vonalan(doboz, cx: float, cy: float, rx: float, ry: float,
                       v: float = _VONAL_FELVASTAG) -> bool:
    """Átmetszi-e a felirat doboza a kör / ellipszis VONALÁT.

    Ez volt a lyuk a hálón: a Venn-diagram köreire ráírt felirat („közös
    rész") eddig átment, mert csak téglalapot és egyenest néztünk.
    """
    if rx <= 0 or ry <= 0:
        return False
    bal, teto, jobb, alj = doboz

    def norm(px, py) -> float:
        return (((px - cx) / rx) ** 2 + ((py - cy) / ry) ** 2) ** 0.5

    # a dobozból a középponthoz legközelebbi, illetve legtávolabbi pont
    kozel = norm(min(max(cx, bal), jobb), min(max(cy, teto), alj))
    tavol = max(norm(px, py) for px in (bal, jobb) for py in (teto, alj))
    t = v / min(rx, ry)
    return kozel <= 1 + t and tavol >= 1 - t


def _vonalra_esik(doboz, el) -> bool:
    """A felirat doboza rajta ül-e ennek az alakzatnak a vonalán."""
    t = _tag(el)
    if t in ("circle", "ellipse"):
        if t == "circle":
            r = _szam(el.get("r"))
            cx, cy, rx, ry = _szam(el.get("cx")), _szam(el.get("cy")), r, r
        else:
            cx, cy = _szam(el.get("cx")), _szam(el.get("cy"))
            rx, ry = _szam(el.get("rx")), _szam(el.get("ry"))
        return _ellipszis_vonalan(doboz, cx, cy, rx, ry)
    for e in _alakzat_vonalai(el):
        if _melyen_fedik(doboz, e):
            return True
    return False


_SZAM_A_FELIRATBAN = re.compile(r"\d+")


def _melyen_fedik(a, b, melyseg: float = 3.0) -> bool:
    """Valódi átfedés – az épp összeérő elemeket nem tekintjük hibának."""
    atfedes_x = min(a[2], b[2]) - max(a[0], b[0])
    atfedes_y = min(a[3], b[3]) - max(a[1], b[1])
    return atfedes_x > melyseg and atfedes_y > melyseg


def _tavolsag_dobozig(pont, doboz) -> float:
    """A pont távolsága egy téglalaptól. Belül nulla."""
    px, py = pont
    dx = max(doboz[0] - px, 0, px - doboz[2])
    dy = max(doboz[1] - py, 0, py - doboz[3])
    return (dx * dx + dy * dy) ** 0.5


def _cimkek_gazdaja(teglalapok, feliratok_dobozzal) -> dict:
    """Melyik felirat MELYIK alakzathoz tartozik.

    Két egymás melletti alakzat között álló felirat különben rossz helyre
    kerülne: a négyzet oldalhosszát a téglalapra olvasnánk rá, és emiatt
    hibátlan rajzokat dobnánk el.
    """
    gazda: dict[int, list] = {id(el): [] for el, _ in teglalapok}
    for doboz, szoveg in feliratok_dobozzal:
        if not _SZAM_A_FELIRATBAN.search(szoveg):
            continue
        kozep = ((doboz[0] + doboz[2]) / 2, (doboz[1] + doboz[3]) / 2)
        legkozelebb, tav = None, None
        for el, el_doboz in teglalapok:
            d = _tavolsag_dobozig(kozep, el_doboz)
            if tav is None or d < tav:
                legkozelebb, tav = el, d
        if legkozelebb is not None:
            gazda[id(legkozelebb)].append((doboz, szoveg))
    return gazda


def _rossz_meretaranyu(el, sajat_feliratok) -> bool:
    """A téglalap OLDALARÁNYA mond-e ellent a RÁÍRT méreteknek.

    Élesben előfordult egy NÉGYZET, aminek a tetején „4 cm", az oldalán
    „3 cm" állt. Egy gyereknek ez megtaníthatatlan – ilyen rajzot inkább
    ne lásson. Csak akkor ítélünk, ha KÉT SZOMSZÉDOS oldalon is van szám:
    a feliratot ahhoz az oldalhoz kötjük, amelyik MENTÉN áll, nem ahhoz,
    amelyik történetesen közel esik.
    """
    x, y = _szam(el.get("x")), _szam(el.get("y"))
    w, h = _szam(el.get("width")), _szam(el.get("height"))
    if w <= 0 or h <= 0:
        return False

    kozepek = []
    for doboz, szoveg in sajat_feliratok:
        m = _SZAM_A_FELIRATBAN.search(szoveg)
        if m:
            kozepek.append(((doboz[0] + doboz[2]) / 2,
                            (doboz[1] + doboz[3]) / 2, int(m.group())))

    def oldal(fuggoleges: bool, also_fele: bool) -> int | None:
        """A megadott oldal mentén álló szám, a legközelebbi."""
        legjobb, tav = None, None
        for kx, ky, ertek in kozepek:
            if fuggoleges:                       # bal vagy jobb oldal
                if abs(ky - (y + h / 2)) > h * 0.6:
                    continue
                jo = kx > x + w * 0.75 if also_fele else kx < x + w * 0.25
                d = abs(kx - (x + w if also_fele else x))
            else:                                # felső vagy alsó oldal
                if abs(kx - (x + w / 2)) > w * 0.6:
                    continue
                jo = ky > y + h * 0.75 if also_fele else ky < y + h * 0.25
                d = abs(ky - (y + h if also_fele else y))
            if jo and (tav is None or d < tav):
                legjobb, tav = ertek, d
        return legjobb

    szeles = oldal(False, False) or oldal(False, True)
    magas = oldal(True, False) or oldal(True, True)
    if not szeles or not magas:
        return False
    rajzolt, felirt = w / h, szeles / magas
    return abs(rajzolt - felirt) / max(rajzolt, felirt) > 0.20


# ── a felirat elhúzása a rajzról ────────────────────────────────────────
# Kis lépésekkel próbálkozunk, mindig a legkisebb elmozdítást választva:
# előbb fel-le, aztán jobbra-balra, végül átlósan. Ha semmi sem jó, marad
# a régi szabály: inkább ne lásson a gyerek ábrát, mint zavarosat.
_ELTOLASOK: list[tuple[float, float]] = []
for _lepes in (7, 12, 18, 25, 34, 44):
    for _ix, _iy in ((0, -1), (0, 1), (-1, 0), (1, 0),
                     (-1, -1), (1, -1), (-1, 1), (1, 1)):
        _ELTOLASOK.append((_ix * _lepes, _iy * _lepes))


def _mozgathato_felirat(el) -> bool:
    """Csak azt a feliratot mozdítjuk el, aminél ez biztosan nem tör el
    semmit: saját x/y-a van, nincs elforgatva, és a tspanjai sem helyezik
    el magukat külön."""
    if (el.get("transform") or "").strip():
        return False
    if el.get("x") is None or el.get("y") is None:
        return False
    if (el.get("dx") or el.get("dy")):
        return False
    for gy in el.iter():
        if gy is el:
            continue
        if gy.get("x") or gy.get("y") or gy.get("dx") or gy.get("dy") \
                or (gy.get("transform") or "").strip():
            return False
    return True


def _akadalyok(alakzatok) -> list:
    """A rajzvonalak egyszer kiszámolva – a próbálgatás így nem lassú."""
    ki = []
    for el in alakzatok:
        t = _tag(el)
        if t == "circle":
            r = _szam(el.get("r"))
            if r > 0:
                ki.append(("kor", (_szam(el.get("cx")), _szam(el.get("cy")), r, r)))
        elif t == "ellipse":
            rx, ry = _szam(el.get("rx")), _szam(el.get("ry"))
            if rx > 0 and ry > 0:
                ki.append(("kor", (_szam(el.get("cx")), _szam(el.get("cy")), rx, ry)))
        else:
            vonalak = _alakzat_vonalai(el)
            if vonalak:
                ki.append(("vonalak", vonalak))
    return ki


def _utkozik(doboz, akadalyok, mas_dobozok) -> bool:
    """Ezen a helyen a felirat rálóg-e másik feliratra vagy egy rajzvonalra."""
    for m in mas_dobozok:
        if m is not None and _fedik_egymast(doboz, m):
            return True
    for fajta, adat in akadalyok:
        if fajta == "kor":
            if _ellipszis_vonalan(doboz, *adat):
                return True
        else:
            for e in adat:
                if _melyen_fedik(doboz, e):
                    return True
    return False


# Ha az elmozdítás nem elég (pl. a Venn-diagram metszete keskenyebb, mint a
# ráírt szó), a feliratot egy kicsit kisebb betűvel is megpróbáljuk. Ennél
# jobban nem kicsinyítünk: az olvashatatlan felirat semmivel sem jobb.
_KICSINYITES = (1.0, 0.85, 0.72)
_LEGKISEBB_BETU = 10.0


def _feliratok_elhuzasa(feliratok, dobozok, akadalyok, szulok) -> list:
    """Az ütköző feliratokat elhúzza a rajzról. A helyükre kerülő dobozokat
    adja vissza. Ami eddig is rendben volt, ahhoz hozzá sem nyúl."""
    for i, el in enumerate(feliratok):
        d = dobozok[i]
        if d is None:
            continue
        masok = [dobozok[j] for j in range(len(dobozok)) if j != i]
        if not _utkozik(d, akadalyok, masok):
            continue
        if not _mozgathato_felirat(el):
            continue
        szoveg = "".join(el.itertext()).strip()
        meret = _oroklott_betumeret(el, szulok)
        x, y = _szam(el.get("x"), 0.0), _szam(el.get("y"), 0.0)
        horgony = (el.get("text-anchor") or "start").strip().lower()
        kesz = False
        for arany in _KICSINYITES:
            uj_meret = meret * arany
            if arany < 1.0 and uj_meret < _LEGKISEBB_BETU:
                continue
            for dx, dy in ((0.0, 0.0),) + tuple(_ELTOLASOK):
                if arany == 1.0 and dx == 0 and dy == 0:
                    continue                  # ezt a helyet már elvetettük
                uj = _doboz(szoveg, uj_meret, x + dx, y + dy, horgony)
                if _utkozik(uj, akadalyok, masok):
                    continue
                if dx or dy:
                    el.set("x", f"{x + dx:g}")
                    el.set("y", f"{y + dy:g}")
                if arany < 1.0:
                    el.set("font-size", f"{uj_meret:g}")
                dobozok[i] = uj
                kesz = True
                break
            if kesz:
                break
    return dobozok


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
            _f = (el.get("fill") or "").strip()
            if not _f:
                el.set("fill", "none")
            else:
                # A KIÍRT sötét kitöltés is fekete kockát ad. Élesben így
                # jött két tömör fekete doboz "Hír" és "Meghívó" felirattal:
                # a kerete és a szövege ott volt, csak nem látszott semmi.
                _v = _vilagossag(_f)
                _d = _alakzat_doboza(el)
                if _v is not None and _v < 0.25 and _d:
                    _ter = (_d[2] - _d[0]) * (_d[3] - _d[1])
                    if _ter > 400:
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

    # a feliratok dobozai – a listában ugyanannyi elem, mint a feliratokban
    dobozok = [_felirat_doboza(el, szulok) for el in feliratok]
    alakzatok = [el for el in gyoker.iter()
                 if _tag(el) in _ALAKZATOK + _VONALAK]

    # ── 3. a ráírt méret mond ellent a rajznak → inkább semmi ───────────
    # Ez az EREDETI helyeken dől el, mielőtt bármit elmozdítanánk: a szám
    # ahhoz az oldalhoz tartozik, amelyik mellé az AI odaírta.
    parban = [(d, "".join(el.itertext()))
              for el, d in zip(feliratok, dobozok) if d]
    _teglalapok = [(el, _alakzat_doboza(el)) for el in gyoker.iter()
                   if _tag(el) == "rect" and _alakzat_doboza(el)]
    if _teglalapok:
        _gazda = _cimkek_gazdaja(_teglalapok, parban)
        for el, _ in _teglalapok:
            if _rossz_meretaranyu(el, _gazda.get(id(el), [])):
                return None

    # ── 3/b. a rajzba lógó feliratot ELHÚZZUK ───────────────────────────
    # Eddig csak eldobtuk az ilyen ábrát. Most előbb megpróbáljuk kicsit
    # arrébb tenni a feliratot – így a gyerek látja a rajzot is, a szöveget
    # is. Ami eddig is hibátlan volt, az változatlan marad.
    akadalyok = _akadalyok(alakzatok)
    dobozok = _feliratok_elhuzasa(feliratok, dobozok, akadalyok, szulok)

    # ── 3/c. ami így sem lett olvasható → inkább semmi ──────────────────
    ervenyes = [d for d in dobozok if d]
    for i in range(len(ervenyes)):
        for j in range(i + 1, len(ervenyes)):
            if _fedik_egymast(ervenyes[i], ervenyes[j]):
                return None
    for d in ervenyes:
        if _utkozik(d, akadalyok, []):
            return None
    dobozok = ervenyes

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
