# -*- coding: utf-8 -*-
"""TutorIA – előfizetési csomagok: ki mit ér el, és mennyit használhat.

MIÉRT KÜLÖN FÁJL
    Az árak és a havi keretek üzleti döntések, nem programozási kérdések.
    Itt egy helyen állnak, tehát ha változtatsz rajtuk, elég ezt a fájlt
    átírni — a program többi részéhez nem kell hozzányúlni.

MIN ALAPUL AZ ÁRAZÁS
    A PERC kerül pénzbe, nem a gyerek. Egy új profil létrehozása nulla
    euró, egy tanulási perc viszont valódi költség — a hangos perc a
    tizenkétszerese a némának. Ezért a csomagok között a perc a
    különbség, a profilok száma csak kényelmi korlát. Így nincs olyan
    csomag, amit egy másik helyett ki lehetne trükközni: aki több percet
    akar, az többet fizet, mindegy, hány profilra osztja.

    A HAVI KERET A CSALÁDÉ, közösen. Öt profil ugyanabból a keretből
    tanul — nem ötször annyit kap.

A TESZTIDŐSZAK
    Akinek nincs csomagja, az a "teszt" csomagot kapja: mindent elér, bő
    kerettel. A teszt végén elég a szülőket "free"-re állítani, és
    mindenki a kis keretre esik vissza — senkit nem zárunk ki.
"""

from __future__ import annotations

# Mindkét tanterv jele, ahogy az adatbázisban is szerepel.
HU = "HU"
ES = "ES"

TESZT = "teszt"
FREE = "free"

# Az árak euróban. Az éves díj tíz hónap ára: aki előre fizet, két hónapot
# nyer, mi pedig előre megkapjuk a pénzt — az induláskor ez tartja el a
# vállalkozást, amíg nő a létszám.
CSOMAGOK: dict[str, dict] = {
    # ── Tesztidőszak: nincs korlát, mindent elér. ──
    TESZT: {
        "nev_hu": "Teszt időszak",
        "nev_es": "Periodo de prueba",
        "tantervek": (HU, ES),
        "havi_perc": 3000,
        "hangos_perc": 3000,
        "profil": 5,
        "napi_jelentes": True,
        "ar_honap": 0.0,
        "ar_ev": 0.0,
        "rejtett": True,          # nem kínáljuk fel megvásárolható csomagként
    },

    # ── Ingyenes próba: EGYSZERI keret, nem havi. ──
    # MIÉRT NEM HAVI: ha minden hónap elsején újratöltődne, a család
    # örökre tanulhatna havi egy keveset, és soha nem fizetne. A próbának
    # az a dolga, hogy a szülő eldönthesse, megéri-e — nem az, hogy
    # kiváltsa az előfizetést.
    FREE: {
        "nev_hu": "Ingyenes próba",
        "nev_es": "Prueba gratuita",
        "tantervek": (HU, ES),
        # 50 perc: két-három tanóra. Ennyiből a szülő el tudja dönteni,
        # megéri-e, de egy tanévhez meg sem közelíti az elegendőt.
        "havi_perc": 50,
        # Hang AZÉRT van benne, mert enélkül a szülő nem tudja, mit venne
        # meg. Csak kevés: a hangos perc tizenkétszer annyiba kerül.
        "hangos_perc": 15,
        "profil": 1,
        "napi_jelentes": False,
        "ar_honap": 0.0,
        "ar_ev": 0.0,
        "egyszeri": True,
    },

    "alap": {
        "nev_hu": "Alap",
        "nev_es": "Básico",
        "tantervek": (HU, ES),
        "havi_perc": 400,         # napi ~13 perc
        "hangos_perc": 400,
        "profil": 3,
        "napi_jelentes": False,
        "ar_honap": 14.90,
        "ar_ev": 149.0,
    },
    "pro": {
        "nev_hu": "Pro",
        "nev_es": "Pro",
        "tantervek": (HU, ES),
        "havi_perc": 900,         # napi ~30 perc
        "hangos_perc": 900,
        "profil": 5,
        "napi_jelentes": True,
        "ar_honap": 24.90,
        "ar_ev": 249.0,
    },
    "max": {
        "nev_hu": "Max",
        "nev_es": "Max",
        "tantervek": (HU, ES),
        "havi_perc": 1800,        # napi ~60 perc
        "hangos_perc": 1800,
        "profil": 5,
        "napi_jelentes": True,
        "ar_honap": 39.90,
        "ar_ev": 399.0,
    },
}

# Milyen sorrendben mutatjuk őket az előfizetés oldalon.
SORREND = (FREE, "alap", "pro", "max")

# Melyiket emeljük ki. Nem a legdrágább: azt ajánljuk, ami a legtöbb
# családnak tényleg jó — a hamis ajánlás egyszer működik, utána soha.
AJANLOTT = "alap"


def csomag(kulcs: str | None) -> dict:
    """Egy csomag adatai. Ismeretlen vagy üres kulcsra a teszt csomag."""
    return CSOMAGOK.get((kulcs or "").strip() or TESZT, CSOMAGOK[TESZT])


def elerheto_tantervek(kulcs: str | None) -> tuple[str, ...]:
    return tuple(csomag(kulcs)["tantervek"])


def engedi_tantervet(kulcs: str | None, tanterv: str) -> bool:
    """Beléphet-e ezzel a csomaggal az adott tanterv oldalára?

    Jelenleg minden csomag mindkét tantervet tartalmazza. A kétnyelvűség a
    termék LÉNYEGE — pont a külföldön élő magyar családoknak szól —, ezért
    nem felár. Ha mégis szét kell választani, elég a "tantervek" mezőt
    átírni a fenti táblázatban.
    """
    return (tanterv or HU).upper() in elerheto_tantervek(kulcs)


def havi_perc(kulcs: str | None) -> int:
    return int(csomag(kulcs)["havi_perc"])


def hangos_perc(kulcs: str | None) -> int:
    """Ebből a keretből mennyi szólalhat meg. A hangos perc tizenkétszer
    annyiba kerül, mint a néma — a Free-nél ezért van külön korlátja."""
    c = csomag(kulcs)
    return int(c.get("hangos_perc", c["havi_perc"]))


def egyszeri(kulcs: str | None) -> bool:
    """Egyszeri próbakeret-e, vagy havonta újrainduló?

    Az ingyenes próba EGYSZER jár. A fizetős csomagok kerete a hónap
    első napján áll vissza.
    """
    return bool(csomag(kulcs).get("egyszeri"))


def napi_jelentes(kulcs: str | None) -> bool:
    """Kérhet-e NAPI haladási jelentést a szülő.

    A heti és a havi mindenkinek jár. A napi valódi többletmunka a
    rendszernek (minden reggel levél minden családnak), ezért a nagyobb
    csomagokban van benne – és mert ez az egyetlen különbség, ami nem a
    percről szól, de már ma is működik. Amit nem tudunk kiszolgálni, azt
    nem írjuk ki a csomaglapra.
    """
    return bool(csomag(kulcs).get("napi_jelentes"))


def max_profil(kulcs: str | None) -> int:
    """Hány gyerekprofilt hozhat létre. Nem költség, csak kényelmi korlát —
    a keret úgyis közös."""
    return int(csomag(kulcs).get("profil", 1))


def nev(kulcs: str | None, nyelv: str = "hu") -> str:
    c = csomag(kulcs)
    return c["nev_es"] if nyelv == "es" else c["nev_hu"]


def ar(kulcs: str | None, eves: bool = False) -> float:
    c = csomag(kulcs)
    return float(c["ar_ev"] if eves else c["ar_honap"])


def fizetos(kulcs: str | None) -> bool:
    return ar(kulcs) > 0


def valaszthato(nyelv: str = "hu") -> list[dict]:
    """A megjelenítendő csomagok, a megadott sorrendben."""
    ki = []
    for kulcs in SORREND:
        c = CSOMAGOK.get(kulcs)
        if not c or c.get("rejtett"):
            continue
        ki.append({
            "kulcs": kulcs,
            "nev": c["nev_es"] if nyelv == "es" else c["nev_hu"],
            "tantervek": list(c["tantervek"]),
            "havi_perc": c["havi_perc"],
            "hangos_perc": c.get("hangos_perc", c["havi_perc"]),
            "profil": c.get("profil", 1),
            "egyszeri": bool(c.get("egyszeri")),
            "napi_jelentes": bool(c.get("napi_jelentes")),
            "ar_honap": c["ar_honap"],
            "ar_ev": c["ar_ev"],
            # Az éves díj havi bontásban – ezt hasonlítja össze a szülő.
            "ar_ev_havonta": round(c["ar_ev"] / 12.0, 2) if c["ar_ev"] else 0.0,
            "ajanlott": kulcs == AJANLOTT,
            "fizetos": c["ar_honap"] > 0,
        })
    return ki
