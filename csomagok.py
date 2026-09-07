# -*- coding: utf-8 -*-
"""TutorIA – előfizetési csomagok: ki mit ér el, és mennyit használhat.

MIÉRT KÜLÖN FÁJL
    Az árak és a havi keretek üzleti döntések, nem programozási kérdések.
    Itt egy helyen állnak, tehát ha változtatsz rajtuk, elég ezt a fájlt
    átírni — a program többi részéhez nem kell hozzányúlni.

MIT DÖNT EL EGY CSOMAG
    1. MELYIK TANTERVET éri el: magyar, spanyol, vagy mind a kettő.
       Aki a magyar csomagra fizet elő, a spanyol oldalra nem jut be.
    2. MENNYI TANULÁSI PERC jár egy hónapra, a szülő ÖSSZES gyerekére.
       A percet mérjük, nem az üzenetszámot: a hang és a válaszok költsége
       is az eltöltött idővel arányos, tehát ez a tisztességes mérőszám.

A TESZTIDŐSZAK
    Akinek nincs csomagja, az a "teszt" csomagot kapja: mindent elér, bő
    kerettel. Amíg ingyenes, ez a helyes viselkedés — a fizetés bekötése
    után elég a szülő csomagját "hu"-ra vagy "es"-re állítani.
"""

from __future__ import annotations

# Mindkét tanterv jele, ahogy az adatbázisban is szerepel.
HU = "HU"
ES = "ES"

TESZT = "teszt"


CSOMAGOK: dict[str, dict] = {
    # ── Tesztidőszak: nincs korlát, mindent elér. ──
    TESZT: {
        "nev_hu": "Teszt időszak",
        "nev_es": "Periodo de prueba",
        "tantervek": (HU, ES),
        "havi_perc": 3000,          # gyakorlatilag korlátlan
        "ar_honap": 0,
        "penznem": "EUR",
        "rejtett": True,            # nem kínáljuk fel megvásárolható csomagként
    },

    # ── Magyar tanterv ──
    "hu_alap": {
        "nev_hu": "Magyar – Alap",
        "nev_es": "Húngaro – Básico",
        "tantervek": (HU,),
        "havi_perc": 300,           # napi ~10 perc
        "ar_honap": 0,              # ÁRAT MÉG NEM DÖNTÖTTÜNK
        "penznem": "EUR",
    },
    "hu_teljes": {
        "nev_hu": "Magyar – Teljes",
        "nev_es": "Húngaro – Completo",
        "tantervek": (HU,),
        "havi_perc": 900,           # napi ~30 perc
        "ar_honap": 0,
        "penznem": "EUR",
    },

    # ── Spanyol tanterv ──
    "es_alap": {
        "nev_hu": "Spanyol – Alap",
        "nev_es": "Español – Básico",
        "tantervek": (ES,),
        "havi_perc": 300,
        "ar_honap": 0,
        "penznem": "EUR",
    },
    "es_teljes": {
        "nev_hu": "Spanyol – Teljes",
        "nev_es": "Español – Completo",
        "tantervek": (ES,),
        "havi_perc": 900,
        "ar_honap": 0,
        "penznem": "EUR",
    },

    # ── Mind a kettő ──
    "ketnyelvu": {
        "nev_hu": "Kétnyelvű",
        "nev_es": "Bilingüe",
        "tantervek": (HU, ES),
        "havi_perc": 1200,
        "ar_honap": 0,
        "penznem": "EUR",
    },
}


def csomag(kulcs: str | None) -> dict:
    """Egy csomag adatai. Ismeretlen vagy üres kulcsra a teszt csomag."""
    return CSOMAGOK.get((kulcs or "").strip() or TESZT, CSOMAGOK[TESZT])


def elerheto_tantervek(kulcs: str | None) -> tuple[str, ...]:
    return tuple(csomag(kulcs)["tantervek"])


def engedi_tantervet(kulcs: str | None, tanterv: str) -> bool:
    """Beléphet-e ezzel a csomaggal az adott tanterv oldalára?"""
    return (tanterv or HU).upper() in elerheto_tantervek(kulcs)


def havi_perc(kulcs: str | None) -> int:
    return int(csomag(kulcs)["havi_perc"])


def nev(kulcs: str | None, nyelv: str = "hu") -> str:
    c = csomag(kulcs)
    return c["nev_es"] if nyelv == "es" else c["nev_hu"]


def valaszthato(nyelv: str = "hu") -> list[dict]:
    """A megvásárolható csomagok listája (a teszt csomag nélkül)."""
    ki = []
    for kulcs, c in CSOMAGOK.items():
        if c.get("rejtett"):
            continue
        ki.append({
            "kulcs": kulcs,
            "nev": c["nev_es"] if nyelv == "es" else c["nev_hu"],
            "tantervek": list(c["tantervek"]),
            "havi_perc": c["havi_perc"],
            "ar_honap": c["ar_honap"],
            "penznem": c["penznem"],
        })
    return ki
