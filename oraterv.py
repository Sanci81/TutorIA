# -*- coding: utf-8 -*-
"""Az előre elkészített óratervek betöltése és beillesztése a tanári promptba.

MIÉRT VAN EZ A FÁJL
    A tanár eddig minden fordulóban a nulláról találta ki, mit tanítson és
    milyen sorrendben. Innen jött a "there is / there are" a létige ELŐTT, és
    innen jöttek a ténybeli tévedések is.

    Az oraterv_keszito.py témakörönként EGYSZER megírja a tanítás lépéseit,
    és egy okosabb modellel átnézeti a tényeit. Ez a fájl azt a kész tervet
    keresi elő, és teszi be a promptba.

HA NINCS TERV, MINDEN MEGY ÚGY, AHOGY EDDIG
    Ha a témakörhöz nincs kész terv, vagy a tanterv időközben megváltozott,
    ez a modul ÜRES SZÖVEGET ad vissza. Az oldal ilyenkor pontosan úgy
    működik, mint eddig. Ez szándékos: a bekötés nem vehet el semmit.
"""

from __future__ import annotations

import hashlib
import json
import logging
from pathlib import Path

log = logging.getLogger(__name__)

MAPPA = Path(__file__).parent / "oratervek"

# Betöltött fájlok. A tervek nem változnak futás közben, elég egyszer
# beolvasni őket. Kulcs: (tantargy_fajl, evfolyam, nyelv).
_GYORSITO: dict[tuple, dict] = {}


def ujjlenyomat(szoveg: str) -> str:
    """A tantervi szöveg lenyomata.

    Ha a kerettantervi JSON szövege megváltozik, ez a lenyomat is más lesz,
    és a régi terv MAGÁTÓL érvényét veszti. Így nem fordulhat elő, hogy egy
    elavult terv szerint tanítunk egy időközben átírt témakört.
    """
    return hashlib.sha256((szoveg or "").encode("utf-8")).hexdigest()[:16]


def fajlnev(tantargy_fajl: str, evfolyam, nyelv: str | None) -> Path:
    alap = (tantargy_fajl or "").replace(".json", "")
    nev = f"{alap}__{evfolyam}" + (f"__{nyelv}" if nyelv else "") + ".json"
    return MAPPA / nev


def _betolt(tantargy_fajl: str, evfolyam, nyelv: str | None) -> dict:
    kulcs = (tantargy_fajl, str(evfolyam), nyelv or "")
    if kulcs in _GYORSITO:
        return _GYORSITO[kulcs]
    adat: dict = {}
    ut = fajlnev(tantargy_fajl, evfolyam, nyelv)
    try:
        if ut.is_file():
            adat = json.loads(ut.read_text(encoding="utf-8")) or {}
    except Exception as hiba:                              # pragma: no cover
        log.warning("ORATERV: %s nem olvasható: %s", ut.name, hiba)
        adat = {}
    _GYORSITO[kulcs] = adat
    return adat


def lepesek(tantargy_fajl: str, evfolyam, nyelv: str | None,
            temakor: dict | None) -> list[dict]:
    """A témakörhöz tartozó tanítási lépések, vagy üres lista.

    Üres listát ad, ha nincs fájl, nincs benne ez a témakör, vagy a témakör
    tantervi szövege időközben megváltozott.
    """
    if not temakor:
        return []
    adat = _betolt(tantargy_fajl, evfolyam, nyelv)
    tervek = adat.get("temakorok") or []
    if not tervek:
        return []

    azonosito = temakor.get("id")
    nev = (temakor.get("name") or "").strip()
    talalat = None
    for t in tervek:
        if azonosito and t.get("temakor_id") == azonosito:
            talalat = t
            break
    if talalat is None:
        for t in tervek:
            if nev and (t.get("temakor") or "").strip() == nev:
                talalat = t
                break
    if talalat is None:
        return []

    regi = talalat.get("ujjlenyomat")
    mostani = ujjlenyomat(temakor.get("text") or "")
    if regi and regi != mostani:
        log.info("ORATERV: %r terve elavult (a tanterv szövege megváltozott), "
                 "nem használom.", nev)
        return []

    return [l for l in (talalat.get("lepesek") or []) if isinstance(l, dict)]


# ── A promptba kerülő szöveg ────────────────────────────────────────────────
_HASZNALAT_HU = """
HOGYAN HASZNÁLD A TERVET
· Nézd meg a beszélgetés előzményében, hol tartotok. Ha még nem kezdtétek el,
  az 1. lépéssel kezdj.
· EGYSZERRE EGY LÉPÉS. Elmagyarázod, mutatod a példát, felteszed az ellenőrző
  kérdést — és MEGVÁROD a választ. Ne told egymás után két lépést.
· Csak akkor lépj tovább, ha a gyerek az ellenőrző kérdésre jól válaszolt. Ha
  nem, UGYANAZT a lépést magyarázd el másképp, más példával.
· A "példa" és a "kérdés" MINTA, nem felolvasandó szöveg. Mondhatod a saját
  szavaiddal, de a TARTALMÁTÓL ne térj el: ezeket a tényeket ellenőriztük.
· Ha a gyerek egy későbbi lépésre kérdez rá, válaszolj röviden, aztán térj
  vissza oda, ahol tartotok.
· NE MONDD MEG a gyereknek, hogy terv szerint haladtok, és ne számozd neki a
  lépéseket. Ez a te jegyzeted, nem az övé.
· Amikor az utolsó lépés is megvan, kínáld fel a tesztet.
"""

_HASZNALAT_ES = """
CÓMO USAR EL PLAN
· Mira en el historial de la conversación por dónde vais. Si aún no habéis
  empezado, empieza por el paso 1.
· UN PASO CADA VEZ. Explicas, muestras el ejemplo, haces la pregunta de
  comprobación — y ESPERAS la respuesta. No juntes dos pasos.
· Solo avanza si el niño ha respondido bien a la pregunta. Si no, explica EL
  MISMO paso de otra manera, con otro ejemplo.
· El "ejemplo" y la "pregunta" son MODELOS, no un texto para leer en voz alta.
  Puedes decirlo con tus palabras, pero no cambies el CONTENIDO: estos datos
  están verificados.
· Si el niño pregunta por un paso posterior, respóndele brevemente y vuelve al
  punto en el que estáis.
· NO le digas al niño que seguís un plan, y no le numeres los pasos. Esto es
  tu guion, no el suyo.
· Cuando termines el último paso, ofrécele el test.
"""


def prompt_blokk(lepes_lista: list[dict], *, spanyol: bool = False) -> str:
    """A tervből a promptba illeszthető szöveg. Üres lista → üres szöveg."""
    if not lepes_lista:
        return ""

    sorok: list[str] = []
    if spanyol:
        sorok.append("\n=== PLAN DE ENSEÑANZA DEL TEMA ===")
        sorok.append(
            "Este plan ya está hecho y un revisor ha comprobado sus datos. NO "
            "lo reinventes y no te desvíes de él. El orden es obligatorio: "
            "cada paso se apoya en el anterior.")
        cimke = ("qué aprende", "ejemplo", "pregunta")
    else:
        sorok.append("\n=== A TÉMAKÖR TANÍTÁSI TERVE ===")
        sorok.append(
            "Ez a terv előre elkészült, és egy ellenőrző átnézte a tényeit. NE "
            "TALÁLD KI ÚJRA, és ne térj el tőle. A sorrend kötelező: minden "
            "lépés az előzőre épül.")
        cimke = ("mit tanul", "példa", "kérdés")

    for i, lep in enumerate(lepes_lista, 1):
        sorok.append(f"\n  {i}. {(lep.get('cim') or '').strip()}")
        for kulcs, szo in zip(("mit", "pelda", "kerdes"), cimke):
            ertek = (lep.get(kulcs) or "").strip()
            if ertek:
                sorok.append(f"     {szo}: {ertek}")

    sorok.append(_HASZNALAT_ES if spanyol else _HASZNALAT_HU)
    return "\n".join(sorok)
