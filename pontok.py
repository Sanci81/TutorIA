# -*- coding: utf-8 -*-
"""TutorIA – pontszerzés.

MI EZ
    Egyetlen hely, ahol az áll, hogy miért hány pont jár. A pont a bolt
    fizetőeszköze: ebből vesz a gyerek tasakot, a tasakból jön a kártya.

    Itt SEMMI adatbázis nincs – csak számok és szabályok. Így egy helyen
    lehet hangolni a gazdaságot anélkül, hogy az app.py-hoz hozzá kellene nyúlni.

MENNYI EGY NAP
    Egy lecke végigvitele + a hozzá tartozó teszt jó eredménnyel:
        50 + 100 = 150 pont, kiváló eredménnyel 50 + 150 = 200 pont.
    Az egy lapos tasak 100, a három lapos 250 pont.
    Vagyis egy szorgalmas nap egy-két lapot ér – a gyűjtemény hetekig tart.

ISMÉTLÉS
    Ugyanazt a leckét újra letesztelni sokkal kevesebbet ér. Nem tiltjuk –
    az ismétlés hasznos –, de nem lehet vele pontot farmolni.
"""

from __future__ import annotations

# ── lecke ───────────────────────────────────────────────────────────────────
PONT_LECKE = 50            # egy témakör végigvitele a csevegésben
PONT_LECKE_ISMETLES = 10   # ha ugyanazt a leckét már egyszer befejezte

# ── témakör-teszt ───────────────────────────────────────────────────────────
TESZT_HATAR_JO = 70        # ennyitől számít sikeresnek
TESZT_HATAR_KIVALO = 90    # ennyitől jár a nagyobb jutalom
PONT_TESZT_JO = 100
PONT_TESZT_KIVALO = 150
# Ha a témakör MÁR teljesítve volt, és a gyerek újra letesztelte:
PONT_TESZT_ISMETLES = [60, 40]   # első ismétlés 60, onnantól 40

# ── szintfelmérő ────────────────────────────────────────────────────────────
# Próbálkozásonként csökken: az első felmérő ér a legtöbbet.
PONT_SZINTFELMERO = [150, 100, 60]


def lecke_pont(mar_volt: bool = False) -> int:
    """A csevegésben befejezett lecke pontja."""
    return PONT_LECKE_ISMETLES if mar_volt else PONT_LECKE


def teszt_pont(szazalek: int, mar_teljesitve: bool = False,
               ismetles_szam: int = 0) -> int:
    """A témakör-teszt pontja.

    szazalek       – az elért eredmény 0–100
    mar_teljesitve – volt-e már sikeres teszt ebből a témakörből
    ismetles_szam  – hányadik ismétlés ez (0 = ez az első ismétlés)
    """
    try:
        szazalek = int(szazalek)
    except (TypeError, ValueError):
        return 0
    if szazalek < TESZT_HATAR_JO:
        return 0
    if not mar_teljesitve:
        return PONT_TESZT_KIVALO if szazalek >= TESZT_HATAR_KIVALO else PONT_TESZT_JO
    i = max(0, int(ismetles_szam))
    return PONT_TESZT_ISMETLES[min(i, len(PONT_TESZT_ISMETLES) - 1)]


def szintfelmero_pont(probalkozas: int = 1) -> int:
    """A szintfelmérő pontja. `probalkozas` 1-től számol."""
    i = max(1, int(probalkozas or 1)) - 1
    return PONT_SZINTFELMERO[min(i, len(PONT_SZINTFELMERO) - 1)]


def indoklas(fajta: str, pont: int, nyelv: str = "hu") -> str:
    """Rövid szöveg a gyereknek: miért kapta a pontot."""
    if nyelv == "es":
        szotar = {
            "lecke": "por terminar la lección",
            "lecke_ismetles": "por repasar la lección",
            "teszt": "por el examen",
            "teszt_kivalo": "por un examen excelente",
            "teszt_ismetles": "por repetir el examen",
            "szintfelmero": "por la prueba de nivel",
        }
    else:
        szotar = {
            "lecke": "a lecke befejezéséért",
            "lecke_ismetles": "a lecke ismétléséért",
            "teszt": "a tesztért",
            "teszt_kivalo": "a kiváló tesztért",
            "teszt_ismetles": "a teszt ismétléséért",
            "szintfelmero": "a szintfelmérőért",
        }
    return f"+{pont} {szotar.get(fajta, '')}".strip()
