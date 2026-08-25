# -*- coding: utf-8 -*-
"""TutorIA – az ábra ÖSSZEVETÉSE a szöveggel, mielőtt a gyerek meglátja.

MIÉRT KELL
    Az `abra.py` a rajz TECHNIKAI hibáit fogja meg: fekete folt, egymásra
    csúszó felirat, hamis oldalarány. Azt viszont nem tudja megítélni, hogy
    a rajz AZT mutatja-e, amit a szöveg mond.

    Élesben ez jött ki egy trapéznál: a szöveg szerint a párhuzamos oldalak
    8 és 4 cm, a rajzon viszont az alsó oldal volt a hosszabb, az alsó
    feliratban „5 cm és 5 cm" állt (a két szár, egyetlen oldalra írva), a
    „magasság = 3 cm" pedig a ferde szárra mutatott. Négy hiba egy képen,
    és egyik sem SVG-hiba.

MIÉRT NEM LÁTÓ MODELL
    Az ábra nem pixel, hanem FORRÁSKÓD. Az SVG-ben betűre ott áll, hogy
    melyik felirat mit mond és melyik vonal hol van – ezt egy szöveges
    modell pontosan olvassa. Egy látó modellnek ugyanezt a képről kellene
    kitalálnia: lassabb, drágább, és bizonytalanabb.

MIT CSINÁL, HA HIBÁS
    Semmit nem javít – az ábra egyszerűen KIMARAD. A javítás megint csak
    találgatás lenne, és jó eséllyel egy másik rossz rajzot adna. Egy
    hiányzó ábra nem tanít rosszat; egy hibás igen.
"""

from __future__ import annotations

import json
import os
import re

# HÁROM ÜZEMMÓD, és ALAPBÓL a középső fut.
#
#   "naplo"  – az ellenőr lefut és NAPLÓZ, de az ábrát MINDIG átengedi.
#              Ez az alapértelmezés: előbb lássuk fekete-fehéren, mit ítélne
#              hibásnak, és csak akkor kapcsoljuk élesre, ha a napló szerint
#              tényleg a rossz rajzokat fogja meg.
#   "1"      – éles: a hibásnak ítélt ábra kimarad.
#   "0"      – teljesen ki, hívás sincs.
#
# Ezt a leckét drágán tanultam: az előző körben élesre állítva szállítottam,
# és az ábrák egyszerűen eltűntek, mérés nélkül.
def uzemmod() -> str:
    m = (os.environ.get("ABRA_ELLENOR", "naplo") or "naplo").strip().lower()
    if m in ("0", "false", "no", "ki"):
        return "ki"
    if m in ("1", "true", "yes", "eles"):
        return "eles"
    return "naplo"


def bekapcsolva() -> bool:
    """Fusson-e egyáltalán a hívás."""
    return uzemmod() != "ki"


def eldobhat() -> bool:
    """Eltüntetheti-e ténylegesen az ábrát."""
    return uzemmod() == "eles"


MODELL = os.environ.get("ABRA_ELLENOR_MODELL", "gpt-4o-mini")
IDOKORLAT = 12.0
MAX_SVG = 4000          # ennél hosszabb rajzot nem küldünk el, úgyis ritka
MAX_SZOVEG = 1200

# A kérdés SZÁNDÉKOSAN nem az, hogy „bármi eltér-e" – attól a jó ábrákat is
# eldobnánk egy rövidebb vonal miatt. Csak a félrevezető TÁRGYI hibát nézzük.
_KERDES_HU = """Egy általános iskolás gyereknek szánt magyarázatot és a hozzá tartozó SVG ábrát kapod.

Egyetlen dolgot dönts el: tartalmaz-e az ábra olyan TÁRGYI hibát, ami félrevezetheti a gyereket?

Tárgyi hiba például:
- az ábrán szereplő szám vagy felirat ellentmond a szövegnek,
- egy oldalra két méret van írva, vagy egy oldalról hiányzik a mérete,
- a felirat rossz elemre mutat (pl. a magasság a ferde oldalra),
- az alakzat nem az, amiről a szöveg beszél,
- az ábra egy MÁSIK feladatot mutat, mint amit a szöveg a végén kérdez.

NEM tárgyi hiba: a rajz csúnyasága, a színek, kicsit pontatlan arányok, hiányzó díszítés.

Válaszolj CSAK egyetlen JSON objektummal, semmi mással:
{"jo": true}
vagy
{"jo": false, "ok": "egy rövid mondat magyarul, mi az ellentmondás"}"""

_KERDES_ES = """Recibes una explicación para un niño de primaria y el dibujo SVG que la acompaña.

Decide una sola cosa: ¿contiene el dibujo algún error DE CONTENIDO que pueda confundir al niño?

Errores de contenido, por ejemplo:
- un número o una etiqueta del dibujo contradice el texto,
- hay dos medidas escritas en un mismo lado, o falta la medida de un lado,
- una etiqueta señala el elemento equivocado (p. ej. la altura sobre el lado oblicuo),
- la figura no es la que describe el texto,
- el dibujo muestra OTRO ejercicio distinto del que el texto pregunta al final.

NO son errores de contenido: la estética, los colores, proporciones algo imprecisas.

Responde SOLO con un único objeto JSON, nada más:
{"jo": true}
o
{"jo": false, "ok": "una frase breve en español con la contradicción"}"""

_JSON_RE = re.compile(r"\{.*\}", re.S)


def _valasz_ertelmezese(nyers: str) -> tuple[bool, str]:
    """A modell válaszából (bool, indok). Ha nem értjük, ÁTENGEDJÜK az ábrát.

    Szándékos döntés: egy elromlott ellenőr ne tüntesse el az összes rajzot.
    """
    m = _JSON_RE.search(nyers or "")
    if not m:
        return True, ""
    try:
        adat = json.loads(m.group(0))
    except (ValueError, TypeError):
        return True, ""
    if not isinstance(adat, dict) or "jo" not in adat:
        return True, ""
    jo = bool(adat.get("jo"))
    return jo, str(adat.get("ok") or "").strip()[:200]


def keszit_uzenetek(svg: str, szoveg: str, *, es: bool = False) -> list[dict]:
    """A modellnek küldött két üzenet. Külön, hogy tesztelhető legyen."""
    return [
        {"role": "system", "content": _KERDES_ES if es else _KERDES_HU},
        {"role": "user", "content":
            ("TEXTO:\n" if es else "SZÖVEG:\n") + (szoveg or "").strip()[:MAX_SZOVEG]
            + "\n\nSVG:\n" + (svg or "").strip()[:MAX_SVG]},
    ]


def rendben(svg: str, szoveg: str, *, kliens, es: bool = False) -> tuple[bool, str]:
    """Kiadható-e az ábra. (jo, indok). Hibára mindig ÁTENGED.

    A `kliens` az OpenAI kliens – így a hívó dönti el, hogyan épül fel, és
    a teszt egy hamis klienssel is le tudja futtatni.
    """
    if not bekapcsolva() or not svg or not szoveg:
        return True, ""
    try:
        valasz = kliens.chat.completions.create(
            model=MODELL,
            messages=keszit_uzenetek(svg, szoveg, es=es),
        )
        nyers = (valasz.choices[0].message.content or "").strip()
    except Exception as exc:
        print(f"[ABRA-ELLENOR] hiba, az abrat atengedem: {exc}", flush=True)
        return True, ""
    return _valasz_ertelmezese(nyers)


# ---------------------------------------------------------------------------
# SZÁMÜTKÖZÉS – AI NÉLKÜL, biztosan
#
# Élesben ez jött ki: a szöveg végén ÚJ feladat állt („ha a = 6 m, b = 2 m,
# m = 3 m"), a rajzon viszont még a MEGOLDOTT példa számai voltak (a = 5 m,
# b = 4 m). A gyerek a rajzot nézi, és rossz számokkal kezd számolni.
#
# Ezt nem kell modellre bízni: a rajz feliratában ÉS a szövegben is ott áll
# betűre, hogy „a = 5". Összehasonlítani egyszerű, olcsó és BIZTOS – nincs
# találgatás, nincs API-hívás, nincs késleltetés.
#
# A szabály: a rajznak a LEGUTOLSÓ értékadást kell mutatnia, mert a szöveg
# végén álló feladat az, amit a gyereknek most meg kell oldania.
# ---------------------------------------------------------------------------

# Csak EGYBETŰS jelölést nézünk (a, b, c, m, h, r), mert a képletekben ezek
# állnak. A „T = 36" alakot szándékosan kihagyjuk: az eredmény, nem adat.
_ERTEKADAS = re.compile(
    r"(?<![A-Za-z0-9ÁÉÍÓÖŐÚÜŰáéíóöőúüű])([a-hmrxyz])\s*=\s*(\d+(?:[.,]\d+)?)")

_SVG_SZOVEG = re.compile(r"<text[^>]*>(.*?)</text>", re.S | re.I)
_TAG = re.compile(r"<[^>]+>")


def _ertekek(szoveg: str) -> dict[str, str]:
    """Betűjel → a LEGUTOLSÓ hozzá írt szám. Az utolsó számít: a szöveg
    végén álló új feladat írja felül a korábbi kidolgozott példát."""
    ki: dict[str, str] = {}
    for betu, szam in _ERTEKADAS.findall(szoveg or ""):
        ki[betu] = szam.replace(",", ".").rstrip("0").rstrip(".") or "0"
    return ki


def svg_feliratok(svg: str) -> str:
    """A rajz feliratai egyetlen szövegként."""
    return " ".join(_TAG.sub("", r) for r in _SVG_SZOVEG.findall(svg or ""))


def szamutkozes(svg: str, szoveg: str) -> list[tuple[str, str, str]]:
    """(betű, a rajzon, a szövegben) minden ütközésre. Üres lista = rendben.

    Csak azokat a betűket nézzük, amelyeknek MINDKÉT helyen van értéke:
    ha a rajz csak „6 m"-t ír betűjel nélkül, nincs mit összevetni.
    """
    rajz = _ertekek(svg_feliratok(svg))
    if not rajz:
        return []
    doku = _ertekek(szoveg)
    return [(betu, ertek, doku[betu])
            for betu, ertek in rajz.items()
            if betu in doku and doku[betu] != ertek]


def utkozes_leiras(utkozesek: list[tuple[str, str, str]]) -> str:
    """Rövid, ember számára olvasható összefoglaló a naplóhoz."""
    return "; ".join(f"{b}: rajzon {r}, szövegben {s}" for b, r, s in utkozesek)


def kivant_ertekek(svg: str, szoveg: str) -> dict[str, str]:
    """Amit a rajznak mutatnia KELLENE: a rajzon szereplő betűjelek, a
    szövegből vett (legutolsó) értékkel. A hibátlan betűket is beleírjuk,
    különben az újrarajzolásnál azok csúsznának el."""
    rajz = _ertekek(svg_feliratok(svg))
    doku = _ertekek(szoveg)
    return {b: doku[b] for b in rajz if b in doku}


def eloiras_szoveg(ertekpar, *, es: bool = False) -> str:
    """Utasítás az illusztrátornak az ÚJRARAJZOLÁSHOZ.

    Elfogad ütközés-listát és {betű: érték} szótárat is.
    """
    if isinstance(ertekpar, dict):
        ertekek = ", ".join(f"{b} = {s}" for b, s in sorted(ertekpar.items()))
    else:
        ertekek = ", ".join(f"{b} = {s}" for b, _, s in ertekpar)
    if es:
        return ("IMPORTANTE: el dibujo DEBE mostrar exactamente estos valores "
                f"del ejercicio que el texto pregunta al final: {ertekek}. "
                "No uses los números del ejemplo ya resuelto.")
    return ("FONTOS: az ábra PONTOSAN ezeket az értékeket mutassa, mert a "
            f"szöveg a végén ezt kérdezi: {ertekek}. A már megoldott példa "
            "számait NE használd.")


# ---------------------------------------------------------------------------
# A MAGASSÁG FELIRATA – szintén AI nélkül
#
# Élesben ez jött ki egy téglatestnél: a függőleges élre „b" került, a
# mélységet jelző ferde élre pedig „m". A magasság MINDIG a függőleges él –
# ha a gyerek ezt rosszul tanulja meg, a képlet is összekeveredik a fejében.
#
# Ez is mérhető, nem véleményes: megkeressük, melyik szakaszhoz áll a
# legközelebb az „m" felirat, és megnézzük, függőleges-e az a szakasz.
# ---------------------------------------------------------------------------

_MAGASSAG_CIMKEK = {"m", "h", "magasság", "magassag", "altura", "alt"}

_XML_TAG = re.compile(r"\{[^}]*\}")


def _szam(ertek, alap: float = 0.0) -> float:
    try:
        return float(str(ertek).strip().replace("px", ""))
    except (TypeError, ValueError):
        return alap


def _szakaszok(gyoker) -> list[tuple[float, float, float, float]]:
    """Az ábra vonalszakaszai. Csak azt vesszük, ami BIZTOSAN szakasz:
    line, rect oldalai, polygon/polyline csúcsai. A path-t kihagyjuk – ott
    a görbékből rossz irányt olvasnánk ki, és jó rajzot dobnánk el."""
    ki: list[tuple[float, float, float, float]] = []
    for el in gyoker.iter():
        nev = _XML_TAG.sub("", el.tag or "").lower()
        if nev == "line":
            ki.append((_szam(el.get("x1")), _szam(el.get("y1")),
                       _szam(el.get("x2")), _szam(el.get("y2"))))
        elif nev == "rect":
            x, y = _szam(el.get("x")), _szam(el.get("y"))
            sz, ma = _szam(el.get("width")), _szam(el.get("height"))
            ki += [(x, y, x + sz, y), (x, y + ma, x + sz, y + ma),
                   (x, y, x, y + ma), (x + sz, y, x + sz, y + ma)]
        elif nev in ("polygon", "polyline"):
            szamok = [float(s) for s in
                      re.findall(r"-?\d+(?:\.\d+)?", el.get("points") or "")]
            pontok = list(zip(szamok[0::2], szamok[1::2]))
            if nev == "polygon" and len(pontok) > 2:
                pontok.append(pontok[0])
            ki += [(pontok[i][0], pontok[i][1], pontok[i + 1][0], pontok[i + 1][1])
                   for i in range(len(pontok) - 1)]
    return [s for s in ki if (s[0] - s[2]) ** 2 + (s[1] - s[3]) ** 2 > 25]


def _tavolsag_szakasztol(px: float, py: float, sz) -> float:
    x1, y1, x2, y2 = sz
    dx, dy = x2 - x1, y2 - y1
    hossz2 = dx * dx + dy * dy
    t = 0.0 if hossz2 == 0 else max(0.0, min(1.0, ((px - x1) * dx + (py - y1) * dy) / hossz2))
    vx, vy = x1 + t * dx - px, y1 + t * dy - py
    return (vx * vx + vy * vy) ** 0.5


def magassag_rossz_elen(svg: str) -> str:
    """Üres szöveg = rendben. Különben a hiba rövid leírása.

    Csak akkor szólunk, ha a felirat PONTOSAN a magasságot jelöli („m", „h",
    „magasság"). A „3 m" vagy a „T = a × b × m" nem ilyen – azokban az m
    mértékegység, illetve képletrész.
    """
    try:
        import xml.etree.ElementTree as ET
        gyoker = ET.fromstring(svg or "")
    except Exception:
        return ""
    szakaszok = _szakaszok(gyoker)
    if not szakaszok:
        return ""
    for el in gyoker.iter():
        if _XML_TAG.sub("", el.tag or "").lower() != "text":
            continue
        szoveg = "".join(el.itertext()).strip().rstrip(":").lower()
        if szoveg not in _MAGASSAG_CIMKEK:
            continue
        px, py = _szam(el.get("x")), _szam(el.get("y"))
        legkozelebb = min(szakaszok, key=lambda s: _tavolsag_szakasztol(px, py, s))
        dx = abs(legkozelebb[0] - legkozelebb[2])
        dy = abs(legkozelebb[1] - legkozelebb[3])
        if dy <= dx:
            # A magasság FÜGGŐLEGES él. Ha a felirat egy vízszintes vagy ferde
            # élhez tartozik, a rajz mást tanít, mint a képlet.
            return (f"a magasság felirata ({szoveg}) nem függőleges élen áll "
                    f"– a magasságot jelölő él nem lehet ferde vagy fekvő")
    return ""


def tartalmi_hiba(svg: str, szoveg: str, *, es: bool = False) -> tuple[str, str]:
    """A rajz MÉRHETŐ tartalmi hibái. (indok, előírás). Üres indok = rendben.

    Egy helyen gyűjtjük össze, hogy a hívónak egyetlen döntése legyen:
    újrarajzoltatni vagy sem.
    """
    utkozes = szamutkozes(svg, szoveg)
    if utkozes:
        return (utkozes_leiras(utkozes),
                eloiras_szoveg(kivant_ertekek(svg, szoveg), es=es))
    magassag = magassag_rossz_elen(svg)
    if magassag:
        if es:
            return magassag, (
                "IMPORTANTE: la altura (m) es SIEMPRE la arista VERTICAL. "
                "La arista horizontal de delante es a, la de profundidad es b. "
                "Coloca cada etiqueta junto a su arista.")
        return magassag, (
            "FONTOS: a magasság (m) MINDIG a FÜGGŐLEGES él. Az elülső "
            "vízszintes él az a, a mélységet jelző ferde él a b. Mindegyik "
            "felirat a SAJÁT éle mellé kerüljön.")
    return "", ""


# ---------------------------------------------------------------------------
# NAPLÓ – közvetlenül az appban nézhető, nem a Railway naplójában
#
# A Railway-naplóban keresgélni körülményes, és könnyű rossz telepítést
# nézni. Ezért az utolsó néhány ábra-döntést itt tartjuk a memóriában, és
# a /abra-naplo oldalon meg lehet nézni. Újratelepítéskor kiürül – ez így
# jó: a hibakereséshez pár óra bőven elég.
# ---------------------------------------------------------------------------

MAX_NAPLO = 40
_naplo: list[dict] = []


def jegyez(**mezok) -> None:
    """Egy ábra-döntés feljegyzése. Sosem dob hibát."""
    try:
        _naplo.append(mezok)
        if len(_naplo) > MAX_NAPLO:
            del _naplo[: len(_naplo) - MAX_NAPLO]
    except Exception:
        pass


def naplo() -> list[dict]:
    """A feljegyzések, a legfrissebb elöl."""
    return list(reversed(_naplo))
