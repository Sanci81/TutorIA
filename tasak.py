# -*- coding: utf-8 -*-
"""TutorIA – tasakrendszer.

MI EZ
    A tasak megvásárlása és kibontása. A húzás EGYENLETES az adott oldal
    minden kész kártyája között: nem számít, ki hányadik osztályba jár.
    Egy elsős is húzhat nyolcadikos lapot – a leírásból akkor is tanul,
    és az album csak így tehető teljessé.

    Egyetlen szűrés van: a kártyának KÉSZ kell lennie, vagyis léteznie kell
    a képfájljának. Így elég feltölteni a képet a static/kartyak mappába,
    és a kártya magától játékba kerül – nincs külön lista, amit karban kell
    tartani.

RITKASÁG
    A ritkaság NEM az évfolyamhoz kötődik, hanem a lap értékéhez. A háromlapos
    tasakban az utolsó lap garantáltan ritka vagy jobb – ez adja a bontás
    izgalmát. Egy tasakon belül ugyanaz a lap nem jön ki kétszer.
"""

from __future__ import annotations

import os
import random
from typing import Any, Iterable

import kartyak

# ── a bolt kínálata ─────────────────────────────────────────────────────────
# Egy jó nap ~150–200 pont: lecke 50 + teszt 100–150.
# Ezért az egy lap megfizethető szinte minden lecke után, a nagy tasakra
# viszont gyűjteni kell – és a gyűjtés maga is motivál.
#
# SZÍN: minden tasakméretnek SAJÁT SZÍNE van, mint a Top Elevenben. A gyerek
# már a színről tudja, hány lap van benne – nem kell elolvasnia. A `szin1` a
# világosabb, a `szin2` a sötétebb árnyalat: ebből lesz a rombuszminta.
TASAKOK: list[dict] = [
    {
        "id": "egy",
        "nev": "Egy lap",
        "nev_es": "Un cromo",
        "ar": 100,
        "meret": 1,
        "garancia": None,
        "leiras": "Egy véletlen lap. Bármi lehet.",
        "leiras_es": "Un cromo al azar. Puede ser cualquiera.",
        "szin1": "#7ed0f4", "szin2": "#2f9fd4", "peremszin": "#d8eefb",
    },
    {
        "id": "ketto",
        "nev": "Két lap",
        "nev_es": "Dos cromos",
        "ar": 180,
        "meret": 2,
        "garancia": None,
        "leiras": "Két lap, olcsóbban, mintha külön vennéd.",
        "leiras_es": "Dos cromos, más barato que por separado.",
        "szin1": "#4f66d8", "szin2": "#26307e", "peremszin": "#c9d2f5",
    },
    {
        "id": "harom",
        "nev": "Három lap",
        "nev_es": "Tres cromos",
        "ar": 250,
        "meret": 3,
        "garancia": "ritka",
        "leiras": "Három lap, és az utolsó garantáltan ritka vagy jobb.",
        "leiras_es": "Tres cromos, y el último es raro o mejor.",
        "szin1": "#ffb43f", "szin2": "#e8722a", "peremszin": "#ffe6c2",
    },
]

# Kapcsoló: kapjon-e a gyerek kártyát KÖZVETLENÜL a leckéből is.
# Alapból ki van kapcsolva – a lapok a boltból, tasakból jönnek. Ha a régi
# működést vissza akarod, elég ezt True-ra állítani.
KARTYA_LECKEBOL = False

# Az ARANY változat: minden emberhez tartozik egy sima és egy arany lap, és
# az albumban is két hely van neki. Az arany ritkább – ez adja a gyűjtés
# hosszát. Csak akkor húzható, ha a keretes arany kép tényleg elkészült.
ARANY_ESELY = 0.15       # ekkora eséllyel arany a kihúzott lap
ARANY_JEL = "#arany"     # a tárolt azonosító vége arany lapnál

DUPLA_ERME = 25          # duplikátumért járó érme
DUPLA_HATAR = 3          # ennyi azonos ritkaságú duplikátum = egy ingyen tasak
INGYEN_TASAK = "ketto"     # a három duplából járó ingyen tasak fajtája

# ── ritkasági esélyek ───────────────────────────────────────────────────────
# A szokásos merítés. A ritkaság a lap ÉRTÉKÉHEZ kötődik, nem az évfolyamhoz.
ESELY_NORMAL = {"gyakori": 60, "ritka": 30, "nagyon_ritka": 8, "legendas": 2}
# Garanciás lapok merítése – csak a megadott szinttől felfelé.
ESELY_GARANCIA = {
    "ritka":        {"ritka": 60, "nagyon_ritka": 33, "legendas": 7},
    "nagyon_ritka": {"nagyon_ritka": 82, "legendas": 18},
    "legendas":     {"legendas": 100},
}


def tasak_by_id(tasak_id: str) -> dict | None:
    for t in TASAKOK:
        if t["id"] == tasak_id:
            return t
    return None


_STATIC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")


def arany_letezik(k: dict, static_dir: str | None = None) -> bool:
    """Van-e KÉSZ arany lapja ennek a kártyának."""
    gyoker = static_dir or _STATIC
    return os.path.isfile(os.path.join(gyoker, kartyak.kartya_utvonal(k, True)))


def kartya_azonosito(k: dict, arany: bool) -> str:
    """A tárolt azonosító. Az arany külön lapnak számít – külön is gyűjthető."""
    return k["id"] + ARANY_JEL if arany else k["id"]


def kep_letezik(k: dict, static_dir: str | None = None) -> bool:
    """Kész van-e a kártya. Ez dönti el, hogy a kártya játékban van-e.

    NEM a portré megléte számít, hanem a KERETES lapé (`_kartya.png`), mert a
    gyerek a bontáskor és az albumban azt látja. Ha csak a portré van fent, a
    lap még nem húzható – így nem kaphat törött képet.
    """
    gyoker = static_dir or _STATIC
    return os.path.isfile(os.path.join(gyoker, kartyak.kartya_utvonal(k)))


def kesz_kartyak(oldal: str, static_dir: str | None = None) -> list[dict]:
    """Az adott oldal játékban lévő kártyái – akiknek már van képük."""
    return [k for k in kartyak.osszes_kartya(oldal)
            if kep_letezik(k, static_dir)]


def _valassz_ritkasagot(esely: dict[str, int], rnd: random.Random) -> str:
    tetel = list(esely.items())
    return rnd.choices([r for r, _ in tetel], weights=[w for _, w in tetel])[0]


def huzas(
    oldal: str,
    meglevo: Iterable[str] = (),
    tasak_id: str = "egy",
    static_dir: str | None = None,
    rnd: random.Random | None = None,
) -> list[dict]:
    """Egy megvásárolt tasak tartalma.

    `meglevo` a gyerek eddigi kártya-azonosítói. Ha van még megszerezhető
    lap, a tasak GARANTÁLTAN tartalmaz legalább egy újat – enélkül az a
    gyerek, akinek már sok lapja van, csupa duplikátumot kapna.
    """
    rnd = rnd or random.Random()
    t = tasak_by_id(tasak_id) or TASAKOK[0]
    keszlet = kesz_kartyak(oldal, static_dir)
    if not keszlet:
        return []

    meglevo = set(meglevo)
    hianyzo = [k for k in keszlet if k["id"] not in meglevo]


    szerint: dict[str, list[dict]] = {}
    for k in keszlet:
        szerint.setdefault(k["ritkasag"], []).append(k)

    # EGY TASAKON BELÜL nem jön ki kétszer ugyanaz a lap. Két Arrhenius egy
    # háromlapos tasakban rossz élmény: a gyerek úgy érzi, becsapták. Csak
    # akkor engedünk duplikátumot a tasakon belül, ha tényleg elfogyott a
    # merítés (kevesebb kész lap van, mint amennyi a tasakba kell).
    kivalasztott: set[str] = set()

    def huzz_egyet(esely: dict[str, int]) -> dict:
        szabad: dict[str, list[dict]] = {}
        for r, lista in szerint.items():
            maradt = [k for k in lista if k["id"] not in kivalasztott]
            if maradt:
                szabad[r] = maradt
        if not szabad:                        # minden kész lap benne van már
            szabad = szerint
        elerheto = {r: w for r, w in esely.items() if szabad.get(r)}
        if not elerheto:                      # nincs ilyen ritkaságú lap még
            osszes = [k for lista in szabad.values() for k in lista]
            return rnd.choice(osszes)
        return rnd.choice(szabad[_valassz_ritkasagot(elerheto, rnd)])

    meret = max(1, int(t["meret"]))
    lapok: list[dict] = []
    for i in range(meret):
        utolso = (i == meret - 1) and t.get("garancia")
        lap = huzz_egyet(
            ESELY_GARANCIA.get(t["garancia"], ESELY_NORMAL) if utolso
            else ESELY_NORMAL)
        # Arany változat: ritkán, és csak ha a keretes arany kép elkészült.
        arany = (rnd.random() < ARANY_ESELY) and arany_letezik(lap, static_dir)
        lapok.append({**lap, "arany": arany})
        kivalasztott.add(lap["id"])

    # Ha csupa duplikátum jött ki, de van még megszerezhető lap, az egyiket
    # kicseréljük egy hiányzóra – enélkül a nagy gyűjtemény frusztráló lenne.
    # Az "új-e" itt már az ARANY változatot is figyelembe veszi: egy embernek
    # a sima és az arany lapja két külön gyűjthető darab.
    if hianyzo and all(kartya_azonosito(k, k.get("arany", False)) in meglevo
                       for k in lapok):
        csere = [k for k in hianyzo if k["id"] not in kivalasztott] or hianyzo
        uj_lap = rnd.choice(csere)
        lapok[rnd.randrange(len(lapok))] = {**uj_lap, "arany": False}

    return lapok


def bontas_eredmenye(
    lapok: list[dict], meglevo: dict[str, dict] | Iterable[str] = ()
) -> dict[str, Any]:
    """A kibontott tasak feldolgozása – mit kapott a gyerek.

    Visszaad:
        lapok        – laponként: kártya + uj? + hanyadik példány
        uj_darab     – hány új lap volt
        erme         – duplikátumokért járó érme
        ingyen_tasak – hány ingyen tasakot érdemelt ki
    """
    van = set(meglevo if not isinstance(meglevo, dict) else meglevo.keys())
    ki: list[dict] = []
    erme = 0
    duplak_ritkasag: dict[str, int] = {}

    for k in lapok:
        uj = k["id"] not in van
        if uj:
            van.add(k["id"])
        else:
            erme += DUPLA_ERME
            duplak_ritkasag[k["ritkasag"]] = duplak_ritkasag.get(k["ritkasag"], 0) + 1
        ki.append({"kartya": k, "uj": uj})

    ingyen = sum(n // DUPLA_HATAR for n in duplak_ritkasag.values())
    return {
        "lapok": ki,
        "uj_darab": sum(1 for x in ki if x["uj"]),
        "erme": erme,
        "ingyen_tasak": ingyen,
    }


def allapot(oldal: str, meglevo: Iterable[str] = (),
            static_dir: str | None = None) -> dict[str, Any]:
    """Mennyi van meg – a bolt és az album fejlécéhez."""
    keszlet = kesz_kartyak(oldal, static_dir)
    van = set(meglevo)
    megvan = sum(1 for k in keszlet if k["id"] in van)
    return {
        "kesz": len(keszlet),
        "osszes": len(kartyak.osszes_kartya(oldal)),
        "megvan": megvan,
        "szazalek": round(megvan * 100 / len(keszlet)) if keszlet else 0,
    }
