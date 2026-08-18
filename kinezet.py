# -*- coding: utf-8 -*-
"""TutorIA – kinézetek: amire az érme elmegy.

MIÉRT
    Az érme eddig gyűlt, de nem lehetett vele semmit kezdeni. Innentől ez a
    csevegőablak háttere: sima szín olcsóbban, mintás drágábban.

    A pont és az érme így két külön dolgot jelent, és mind a kettő érthető:
        PONT  → tasak, abból jön a kártya (a gyűjtés)
        ÉRME  → kinézet (a saját ízlés)

OLVASHATÓSÁG
    Ez tanulóalkalmazás, nem játék. A minták ezért HALVÁNYAK: a rajz csak
    sejlik a háttérben, a szöveg marad a fontos. Minden minta világos alapon
    fut, sötét betűvel jól olvasható marad.
"""

from __future__ import annotations

# Nincs szükség kódolásra: a mintákat valódi SVG fájlként szolgáljuk ki.

# ── árak ────────────────────────────────────────────────────────────────────
AR_SZIN = 150      # sima színátmenet
AR_MINTA = 350     # rajzos minta
AR_KULON = 600     # különleges

INGYEN = "alap"    # ezt mindenki megkapja


# A minták kiszolgálásának útvonala. NEM adat-URI: azt a böngészőnek
# kódolva, idézőjelek közé zárva kell átadni, és minden lépésnél el tud
# romlani (HTML attribútum, JSON, CSS). Egy sima SVG fájl mindig működik,
# ráadásul a böngésző el is tárolja.
MINTA_UTVONAL = "/kinezet/minta/"


def _minta(nev: str, meret: int = 64) -> str:
    """CSS háttér-réteg egy kiszolgált SVG mintából."""
    return f"url({MINTA_UTVONAL}{nev}.svg) 0 0 / {meret}px {meret}px repeat"


def _svg(belso: str, szin: str, atlatszo: float = 0.16) -> str:
    """Egy 64×64-es mintacsempe. A szín a csoporton van – a data-URI-ban
    a `currentColor` feketére esne vissza, ezért azt nem használjuk."""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
            f'<g fill="{szin}" stroke="{szin}" stroke-width="2" '
            f'fill-opacity="{atlatszo}" stroke-opacity="{atlatszo}">'
            f'{belso}</g></svg>')


# ── a rajzok ────────────────────────────────────────────────────────────────
_SZIV = ('<path d="M16 26c0-5 4-8 8-8 3 0 5 2 6 4 1-2 3-4 6-4 4 0 8 3 8 8 0 8-14 16-14 16'
         'S16 34 16 26z"/>'
         '<path d="M44 52c0-3 2-5 5-5 2 0 3 1 4 2 1-1 2-2 4-2 2 0 5 2 5 5 0 5-9 10-9 10'
         's-9-5-9-10z" fill-opacity="0.10"/>')

_FOCI = (
    # Igazi futball-labda: TÖMÖR fekete ötszög középen, körülötte a szomszédos
    # ötszögek darabjai a peremen – ez a jellegzetes minta, amiről a labda
    # felismerhető. (Az első változatom vékony körvonal volt középen apró
    # ötszöggel, az kerékre hasonlított, nem labdára.)
    '<circle cx="20" cy="20" r="12" fill="none" stroke-width="2.2"/>'
    '<path d="M20 13.4l6.3 4.6-2.4 7.4h-7.8l-2.4-7.4z" stroke="none" fill-opacity="0.55"/>'
    '<path d="M20 13.4V8.2M26.3 18l4.9-3.6M23.9 25.4l3 4.9M16.1 25.4l-3 4.9'
    'M13.7 18l-4.9-3.6" fill="none" stroke-width="2"/>'
    '<circle cx="49" cy="47" r="7.5" fill="none" stroke-width="1.8"/>'
    '<path d="M49 42.9l3.9 2.9-1.5 4.6h-4.8l-1.5-4.6z" stroke="none" fill-opacity="0.55"/>'
    '<path d="M49 42.9v-3.3M52.9 45.8l3.1-2.2M51.4 50.4l1.9 3.1M46.6 50.4l-1.9 3.1'
    'M45.1 45.8l-3.1-2.2" fill="none" stroke-width="1.5"/>')

_CSILLAG = ('<path d="M20 8l3.2 7.4 8 .7-6 5.3 1.8 7.8L20 25.1l-7 4.1 1.8-7.8-6-5.3 8-.7z"/>'
            '<path d="M46 36l2.2 5 5.4.5-4 3.6 1.2 5.3-4.8-2.8-4.8 2.8 1.2-5.3-4-3.6 5.4-.5z"'
            ' fill-opacity="0.11"/>')

_VIRAG = ('<g transform="translate(20 20)">'
          '<circle cx="0" cy="-8" r="5"/><circle cx="8" cy="0" r="5"/>'
          '<circle cx="0" cy="8" r="5"/><circle cx="-8" cy="0" r="5"/>'
          '<circle cx="0" cy="0" r="3.4" fill-opacity="0.34"/></g>'
          '<g transform="translate(48 46) scale(0.62)" fill-opacity="0.10">'
          '<circle cx="0" cy="-8" r="5"/><circle cx="8" cy="0" r="5"/>'
          '<circle cx="0" cy="8" r="5"/><circle cx="-8" cy="0" r="5"/></g>')

_UR = ('<path d="M20 6c4 4 6 9 6 14 0 4-1 7-3 10h-6c-2-3-3-6-3-10 0-5 2-10 6-14z"/>'
       '<path d="M14 24l-4 6h6zM26 24l4 6h-6z" fill-opacity="0.24"/>'
       '<circle cx="20" cy="16" r="2.6" fill-opacity="0.34"/>'
       '<circle cx="48" cy="12" r="1.8" fill-opacity="0.20"/>'
       '<circle cx="54" cy="40" r="1.4" fill-opacity="0.20"/>'
       '<circle cx="42" cy="52" r="2.1" fill-opacity="0.20"/>')

_TUDOMANY = ('<path d="M16 8h10v10l7 16a3 3 0 0 1-3 4H12a3 3 0 0 1-3-4l7-16z" fill="none"/>'
             '<circle cx="17" cy="32" r="2.2" stroke="none"/>'
             '<circle cx="24" cy="36" r="1.6" stroke="none"/>'
             '<circle cx="48" cy="46" r="6" fill="none"/>'
             '<circle cx="48" cy="46" r="1.8" stroke="none"/>')


# ── a kiszolgálható minták ──────────────────────────────────────────────────
# id -> kész SVG szöveg. Az app.py a /kinezet/minta/<id>.svg útvonalon adja
# vissza ezeket, image/svg+xml fejléccel.
MINTAK: dict[str, str] = {
    "szivek":    _svg(_SZIV,     "#e05a7a", 0.16),
    "foci":      _svg(_FOCI,     "#1f6f43", 0.18),
    "csillagok": _svg(_CSILLAG,  "#3f5bd0", 0.15),
    "virag":     _svg(_VIRAG,    "#c04b8f", 0.15),
    "urhajo":    _svg(_UR,       "#4a4b9c", 0.16),
    "tudomany":  _svg(_TUDOMANY, "#0f7b86", 0.17),
}


def minta_svg(nev: str) -> str | None:
    """Egy minta SVG szövege, vagy None, ha nincs ilyen."""
    return MINTAK.get((nev or "").strip())


# ── a kínálat ───────────────────────────────────────────────────────────────
# `hatter`: teljes CSS background érték. A mintásaknál elöl a minta, mögötte
# a színátmenet – így a rajz a színen úszik.
KINEZETEK: list[dict] = [
    {
        "id": "alap", "ar": 0, "fajta": "szin",
        "nev": "Alap", "nev_es": "Básico",
        "hatter": "linear-gradient(160deg,#ffffff,#f4f6fb)",
    },
    # ── sima színek ────────────────────────────────────────────────────────
    {
        "id": "ejkek", "ar": AR_SZIN, "fajta": "szin",
        "nev": "Éjkék", "nev_es": "Azul noche",
        "hatter": "linear-gradient(160deg,#e8effb,#cddcf5)",
    },
    {
        "id": "erdo", "ar": AR_SZIN, "fajta": "szin",
        "nev": "Erdőzöld", "nev_es": "Verde bosque",
        "hatter": "linear-gradient(160deg,#e9f6ec,#cfe9d8)",
    },
    {
        "id": "naplemente", "ar": AR_SZIN, "fajta": "szin",
        "nev": "Naplemente", "nev_es": "Atardecer",
        "hatter": "linear-gradient(160deg,#fff1e6,#ffd9c9)",
    },
    {
        "id": "levendula", "ar": AR_SZIN, "fajta": "szin",
        "nev": "Levendula", "nev_es": "Lavanda",
        "hatter": "linear-gradient(160deg,#f2ecfb,#ddd0f2)",
    },
    # ── mintások ───────────────────────────────────────────────────────────
    {
        "id": "szivek", "ar": AR_MINTA, "fajta": "minta",
        "nev": "Szívecskék", "nev_es": "Corazones",
        "hatter": _minta("szivek") + ",linear-gradient(160deg,#fff2f5,#ffe0e8)",
    },
    {
        "id": "foci", "ar": AR_MINTA, "fajta": "minta",
        "nev": "Focis", "nev_es": "Fútbol",
        "hatter": _minta("foci") + ",linear-gradient(160deg,#effaf1,#d6efdf)",
    },
    {
        "id": "csillagok", "ar": AR_MINTA, "fajta": "minta",
        "nev": "Csillagos ég", "nev_es": "Cielo estrellado",
        "hatter": _minta("csillagok") + ",linear-gradient(160deg,#eef2fd,#d5def8)",
    },
    {
        "id": "virag", "ar": AR_MINTA, "fajta": "minta",
        "nev": "Virágos", "nev_es": "Flores",
        "hatter": _minta("virag") + ",linear-gradient(160deg,#fdf0f8,#f6ddee)",
    },
    {
        "id": "urhajo", "ar": AR_MINTA, "fajta": "minta",
        "nev": "Űrutazás", "nev_es": "Viaje espacial",
        "hatter": _minta("urhajo") + ",linear-gradient(160deg,#f0eefb,#dcd8f4)",
    },
    # ── különleges ─────────────────────────────────────────────────────────
    {
        "id": "tudomany", "ar": AR_KULON, "fajta": "kulon",
        "nev": "Laboratórium", "nev_es": "Laboratorio",
        "hatter": _minta("tudomany") + ",linear-gradient(160deg,#eafafb,#cdeef1)",
    },
]

_INDEX = {k["id"]: k for k in KINEZETEK}


def by_id(kinezet_id: str | None) -> dict:
    """Egy kinézet, vagy az alap, ha nincs ilyen."""
    return _INDEX.get((kinezet_id or "").strip()) or _INDEX[INGYEN]


def hatter(kinezet_id: str | None) -> str:
    """A CSS background érték – ezt írjuk be a csevegőablakra."""
    return by_id(kinezet_id)["hatter"]


def feloldva(nyers: str | None) -> list[str]:
    """A 'alap,szivek' szövegből tiszta lista. Az alap mindig benne van."""
    lista = [s.strip() for s in (nyers or "").split(",") if s.strip()]
    if INGYEN not in lista:
        lista.insert(0, INGYEN)
    return [s for s in lista if s in _INDEX]


def lista_a_bolthoz(es: bool, feloldott: list[str], aktiv: str) -> list[dict]:
    """A bolt csempéi – név a megfelelő nyelven, állapottal együtt."""
    return [
        {
            "id": k["id"],
            "nev": k["nev_es"] if es else k["nev"],
            "ar": k["ar"],
            "fajta": k["fajta"],
            "hatter": k["hatter"],
            "megvan": k["id"] in feloldott,
            "aktiv": k["id"] == aktiv,
        }
        for k in KINEZETEK
    ]
