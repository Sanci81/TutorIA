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
_SZIV = ('<path d="M20.0 30.21C9.79 22.79,7.0 15.36,11.64 11.64C15.36 8.86,19.07 10.71,20.0 13.5C20.93 10.71,24.64 8.86,28.36 11.64C33.0 15.36,30.21 22.79,20.0 30.21Z" stroke="none"/><path d="M48.0 53.29C41.71 48.71,40.0 44.14,42.86 41.86C45.14 40.14,47.43 41.29,48.0 43.0C48.57 41.29,50.86 40.14,53.14 41.86C56.0 44.14,54.29 48.71,48.0 53.29Z" stroke="none" fill-opacity="0.55"/>')

_FOCI = ('<clipPath id="l1"><circle cx="21" cy="21" r="13"/></clipPath><g clip-path="url(#l1)"><path d="M21.0 16.06L25.7 19.47L23.9 25.0L18.1 25.0L16.3 19.47Z" stroke="none"/><path d="M21.0 16.06L21.0 11.9" fill="none" stroke-width="2.0"/><path d="M28.8 5.92L23.41 13.34L14.69 10.5L14.69 1.34L23.41 -1.5Z" stroke="none"/><path d="M25.7 19.47L29.65 18.19" fill="none" stroke-width="2.0"/><path d="M37.75 23.76L29.03 20.92L29.03 11.76L37.75 8.92L43.14 16.34Z" stroke="none"/><path d="M23.9 25.0L26.35 28.36" fill="none" stroke-width="2.0"/><path d="M23.55 37.78L23.55 28.62L32.27 25.78L37.66 33.2L32.27 40.62Z" stroke="none"/><path d="M18.1 25.0L15.65 28.36" fill="none" stroke-width="2.0"/><path d="M5.83 28.62L14.55 25.78L19.94 33.2L14.55 40.62L5.83 37.78Z" stroke="none"/><path d="M16.3 19.47L12.35 18.19" fill="none" stroke-width="2.0"/><path d="M9.07 8.92L14.46 16.34L9.07 23.76L0.35 20.92L0.35 11.76Z" stroke="none"/></g><circle cx="21" cy="21" r="13" fill="none" stroke-width="2.0"/><clipPath id="l2"><circle cx="49" cy="48" r="7.5"/></clipPath><g clip-path="url(#l2)"><path d="M49.0 45.15L51.71 47.12L50.68 50.31L47.32 50.31L46.29 47.12Z" stroke="none"/><path d="M49.0 45.15L49.0 42.75" fill="none" stroke-width="1.5"/><path d="M53.5 39.3L50.39 43.58L45.36 41.95L45.36 36.65L50.39 35.02Z" stroke="none"/><path d="M51.71 47.12L53.99 46.38" fill="none" stroke-width="1.5"/><path d="M58.66 49.59L53.63 47.96L53.63 42.66L58.66 41.03L61.77 45.31Z" stroke="none"/><path d="M50.68 50.31L52.09 52.25" fill="none" stroke-width="1.5"/><path d="M50.47 57.69L50.47 52.39L55.5 50.76L58.61 55.04L55.5 59.32Z" stroke="none"/><path d="M47.32 50.31L45.91 52.25" fill="none" stroke-width="1.5"/><path d="M40.25 52.39L45.28 50.76L48.39 55.04L45.28 59.32L40.25 57.69Z" stroke="none"/><path d="M46.29 47.12L44.01 46.38" fill="none" stroke-width="1.5"/><path d="M42.12 41.03L45.23 45.31L42.12 49.59L37.09 47.96L37.09 42.66Z" stroke="none"/></g><circle cx="49" cy="48" r="7.5" fill="none" stroke-width="1.5"/>')

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
