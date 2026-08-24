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

# Kikapcsolható egyetlen környezeti változóval, ha lassúnak bizonyulna:
# ABRA_ELLENOR=0
def bekapcsolva() -> bool:
    return (os.environ.get("ABRA_ELLENOR", "1") or "1").strip() not in ("0", "false", "no")


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
