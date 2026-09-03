# -*- coding: utf-8 -*-
"""Óratervet készít minden témakörhöz, EGYSZER, és ellenőrzi a tényeit.

MIÉRT VAN EZ A FÁJL
    A tanár ma minden fordulóban a nulláról találja ki, mit tanítson és
    milyen sorrendben. Innen jött a "there is / there are" a létige előtt,
    és innen jönnek a ténybeli tévedések is ("az ötvözet több fém keveréke").

    Ez a program témakörönként EGYSZER megcsinálja azt a munkát, amit eddig
    óránként újra elvégeztetettünk:
      1. a tantervi szövegből kiolvassa a tanítás lépéseit, sorrendben,
      2. egy OKOSABB modellel átnézeti, hogy amit a lépések állítanak,
         az IGAZ-E,
      3. és elmenti egy fájlba.

    Ami egyszer megvan, azt nem kell újra: az acél összetétele ugyanaz
    minden gyereknek, minden órán, örökre.

AMIT EZ A PROGRAM NEM CSINÁL
    Nem nyúl az app.py-hoz, nem ír át semmit, nem kapcsol be semmit.
    CSAK FÁJLOKAT KÉSZÍT az oratervek/ mappába. A működő oldal ettől
    egy hajszálnyit sem változik. Ha a végeredmény nem tetszik, töröld a
    mappát, és minden pontosan úgy marad, ahogy volt.

HASZNÁLAT
    python oraterv_keszito.py --tantargy Matematika --evfolyam 4
        egyetlen tantárgy egyetlen évfolyama – ezzel kezdj

    python oraterv_keszito.py --tantargy Matematika
        minden évfolyam ehhez a tantárgyhoz

    python oraterv_keszito.py --mind
        MINDEN tantárgy, minden évfolyam – ez a drága

    python oraterv_keszito.py --tantargy Matematika --evfolyam 4 --ujra
        újragenerálja azt is, ami már kész

    Ami már kész, azt magától kihagyja, tehát bármikor megszakíthatod
    (Ctrl+C), és később ott folytatja, ahol abbahagyta.

MENNYIBE KERÜL
    Témakörönként két AI-hívás. Egy tantárgy egy évfolyama nagyjából
    8-10 témakör, tehát 16-20 hívás — néhány tíz cent. Indítás előtt
    kiírja, hány témakör jön, és megkérdezi, indulhat-e.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import re
import sys
from datetime import date
from pathlib import Path

logging.getLogger().setLevel(logging.CRITICAL)
os.environ.setdefault("SECRET_KEY", "oraterv")

try:
    import app
    import curriculum_loader as cl
    import oraterv
except Exception as hiba:                              # pragma: no cover
    print("Nem sikerült betölteni a programot:", hiba)
    print("Az oraterv_keszito.py-t a TutorIA mappából futtasd.")
    sys.exit(1)


KESZITO_MODELL = "gpt-5.4"        # a tervet ő írja
ELLENOR_MODELL = "gpt-5.4"        # a tényeket ő nézi át
NYELVEK = ("angol", "nemet", "spanyol")
MAPPA = oraterv.MAPPA


def _kliens(idokorlat: float = 180.0):
    kulcs = (os.environ.get("OPENAI_API_KEY")
             or os.environ.get("OPENAI_KEY") or "").strip().strip("'\"")
    if not kulcs:
        print("Nincs OPENAI_API_KEY a környezetben.")
        print('PowerShellben:  $env:OPENAI_API_KEY = "sk-proj-..."')
        sys.exit(1)
    from openai import OpenAI
    return OpenAI(api_key=kulcs, timeout=idokorlat, max_retries=2)


def _json_valasz(kliens, modell: str, keres: str) -> dict:
    v = kliens.chat.completions.create(
        model=modell,
        messages=[{"role": "user", "content": keres}],
        response_format={"type": "json_object"})
    return json.loads(v.choices[0].message.content or "{}")


# A lenyomatot és a fájlnevet AZ oraterv.py adja, nem itt számoljuk újra.
# MIÉRT: ha a két fájl külön-külön számolná, egy apró eltérés után a kész
# tervek némán érvénytelenné válnának, és senki nem venné észre.
_ujjlenyomat = oraterv.ujjlenyomat


_fajlnev = oraterv.fajlnev


# ── 1. A TERV MEGÍRÁSA ──────────────────────────────────────────────────────
def _terv_keres(cimke, evfolyam, nyelv, temakor) -> str:
    kor = evfolyam + 6
    sorrend = temakor.get("nyelvtan") or []
    sorrend_szoveg = ""
    if sorrend:
        sorrend_szoveg = (
            "\nA KERETTANTERV MEGADJA A NYELVTAN SORRENDJÉT. EZT KÖVESD, "
            "ne találj ki másikat:\n"
            + "\n".join(f"  {i}. {p}" for i, p in enumerate(sorrend, 1)))
    szokincs = temakor.get("szokincs") or []
    szokincs_szoveg = ("\nA témakör szókincse: " + ", ".join(szokincs)
                       if szokincs else "")

    return f"""Magyar általános iskolai tanár vagy. Egy {evfolyam}. osztályos,
{kor} éves gyereknek készítesz ÓRATERVET egyetlen témakörhöz.

TANTÁRGY: {cimke}{f" ({nyelv} nyelv)" if nyelv else ""}
TÉMAKÖR: {temakor['name']}
{sorrend_szoveg}{szokincs_szoveg}

A KERETTANTERV SZÖVEGE:
{(temakor.get('text') or '')[:9000]}

FELADAT: bontsd a témakört 5-8 LÉPÉSRE, olyan sorrendben, hogy MINDEN lépés
csak az előzőkre épüljön. Ez a legfontosabb: ha a 4. lépés megértéséhez kell
a 2., akkor a 2. NEM jöhet később.

MINDEN LÉPÉSHEZ:
  cim      – rövid, a gyerek is érti
  mit      – EGY mondat: mit tanul meg ebben a lépésben
  epul     – mely korábbi lépések számai kellenek hozzá (üres lista, ha egyik sem)
  pelda    – EGY konkrét példa, amit a tanár mutathat. FONTOS: a példa csak
             olyan tudást használhat, ami az ELŐZŐ lépésekben már szerepelt.
             Nyelvnél: ne írj olyan mondatot, aminek a nyelvtanát még nem vették.
  kerdes   – EGY ellenőrző kérdés. NEM ugyanarról a példáról, amit fentebb
             mutattál – MÁSIK esetről, hogy a gyerek ne másolhassa a választ.

Adj vissza json választ:
{{"lepesek": [{{"cim": "...", "mit": "...", "epul": [1], "pelda": "...",
"kerdes": "..."}}]}}

Magyarul írj{f", a {nyelv} szavakat és mondatokat viszont {nyelv}ul" if nyelv else ""}."""


# ── 2. A TÉNYEK ÁTNÉZÉSE ────────────────────────────────────────────────────
def _ellenor_keres(cimke, evfolyam, temakor, terv) -> str:
    return f"""Egy {evfolyam}. osztályos {cimke} óraterv TÉNYBELI HELYESSÉGÉT
ellenőrzöd. A témakör: {temakor['name']}.

MIND A NÉGY SZÖVEGES MEZŐT NÉZD ÁT KÜLÖN-KÜLÖN, minden lépésben:
  cim, mit, pelda, kerdes
A "kerdes" mezőt is. Egy korábbi futásban a magyarázatot és a példát
kijavítottad, a kérdésben viszont bennehagytad ugyanazt a hibát
(„Mi lehet ugyanannyi, mint 2 hatod?” — helyesen: két hatod).
Ha egy megfogalmazást az egyik mezőben javítasz, nézd meg, hogy
ugyanaz a hiba nincs-e benne a lépés többi mezőjében és a többi
lépésben is — MINDENHOL javítsd ki.

Amit keresel:
  · rossz meghatározás (pl. "az ötvözet több fém keveréke" — az acél vas ÉS
    szén ötvözete, tehát nem csak fémeké)
  · rossz évszám, képlet, mértékegység, tudós neve
  · rossz fordítás vagy nyelvtani állítás (pl. "él/ella es – ő van", holott
    a ser ige itt nem ezt jelenti)
  · pontatlan magyar szóhasználat (pl. "életképes dalok" a "életképet
    bemutató dalok" helyett)
  · olyan példa vagy kérdés, aminek nincs helyes válasza

Ha találsz hibát, JAVÍTSD KI a lépést, és írd le, mit javítottál.
Ha valami helyes, NE nyúlj hozzá — a fölösleges átírás is kár.

AZ ÓRATERV:
{json.dumps(terv, ensure_ascii=False, indent=1)}

Adj vissza json választ, a TELJES javított tervvel:
{{"lepesek": [...ugyanaz a szerkezet...],
  "javitasok": ["mit javítottál – egy mondat javításonként"]}}"""


# ── 3. UTÓELLENŐRZÉS AI NÉLKÜL ──────────────────────────────────────────────
_TORT_SZAMJEGGYEL = re.compile(
    r"\b\d+\s+(ketted|harmad|negyed|ötöd|hatod|heted|nyolcad|kilenced|tized)",
    re.IGNORECASE)
_MEZOK = ("cim", "mit", "pelda", "kerdes")


def _gyanus(lepesek: list) -> list[str]:
    """Amit gépi szabállyal is látunk. Nem javít, csak SZÓL — hogy ne
    higgyük azt, hogy az ellenőrző mindent megtalált."""
    talalatok = []
    for i, lep in enumerate(lepesek, 1):
        for mezo in _MEZOK:
            szoveg = str(lep.get(mezo) or "")
            m = _TORT_SZAMJEGGYEL.search(szoveg)
            if m:
                talalatok.append(f"{i}. lépés / {mezo}: „{m.group(0)}” "
                                 "— a törtet szóval kell kiírni")
    return talalatok


def _egy_temakor(kliens, cimke, evfolyam, nyelv, temakor) -> dict:
    terv = _json_valasz(kliens, KESZITO_MODELL,
                        _terv_keres(cimke, evfolyam, nyelv, temakor))
    lepesek = terv.get("lepesek") or []
    if not lepesek:
        raise RuntimeError("a terv üres lett")

    ell = _json_valasz(kliens, ELLENOR_MODELL,
                       _ellenor_keres(cimke, evfolyam, temakor, lepesek))
    javitott = ell.get("lepesek") or lepesek
    javitasok = ell.get("javitasok") or []

    return {
        "temakor_id": temakor["id"],
        "temakor": temakor["name"],
        "ujjlenyomat": _ujjlenyomat(temakor.get("text") or ""),
        "lepesek": javitott,
        "tenyellenorzes": {
            "modell": ELLENOR_MODELL,
            "javitasok": javitasok,
            "gyanus_maradt": _gyanus(javitott),
        },
    }


def main() -> int:
    p = argparse.ArgumentParser(
        description="Óratervet készít témakörönként, egyszer.")
    p.add_argument("--tantargy", help="a tantárgy nevének egy részlete")
    p.add_argument("--evfolyam", type=int, action="append")
    p.add_argument("--mind", action="store_true", help="minden tantárgy")
    p.add_argument("--ujra", action="store_true",
                   help="a már kész fájlokat is újragenerálja")
    a = p.parse_args()

    if not (a.tantargy or a.mind):
        print("Adj meg egy tantárgyat, vagy a --mind kapcsolót.")
        print('Például:  python oraterv_keszito.py --tantargy Matematika --evfolyam 4')
        return 1

    evfolyamok = a.evfolyam or [1, 2, 3, 4, 5, 6, 7, 8]
    munka: list[tuple] = []
    for evf in evfolyamok:
        try:
            tantargyak = cl.get_hu_subjects_for_grade(evf) or []
        except Exception:
            continue
        for t in tantargyak:
            fajl, cimke = t.get("value"), t.get("label")
            if not fajl:
                continue
            if a.tantargy and a.tantargy.lower() not in (cimke or "").lower():
                continue
            try:
                idegen = cl.is_elo_idegen_subject(fajl)
            except Exception:
                idegen = False
            if idegen:
                munka.extend((fajl, cimke, evf, ny) for ny in NYELVEK)
            else:
                munka.append((fajl, cimke, evf, None))

    if not munka:
        print("Nincs ilyen tantárgy. Ellenőrizd a nevet.")
        return 1

    MAPPA.mkdir(exist_ok=True)
    tennivalo = []
    for fajl, cimke, evf, nyelv in munka:
        ki = _fajlnev(fajl, evf, nyelv)
        if ki.exists() and not a.ujra:
            continue
        tennivalo.append((fajl, cimke, evf, nyelv, ki))

    kesz = len(munka) - len(tennivalo)
    if kesz:
        print(f"{kesz} fájl már kész, azokat kihagyom.")
    if not tennivalo:
        print("Minden kész. (Az --ujra kapcsolóval újragenerálható.)")
        return 0

    print(f"\n{len(tennivalo)} tantárgy-évfolyam következik.")
    print("Ez körülbelül " + ", ".join(
        f"{c} {e}. o." + (f" ({n})" if n else "")
        for _, c, e, n, _ in tennivalo[:6])
        + ("…" if len(tennivalo) > 6 else ""))
    print("\nTémakörönként két AI-hívás. Indulhat? (i/n) ", end="")
    if input().strip().lower() not in ("i", "igen", "y", "yes"):
        print("Nem csináltam semmit.")
        return 0

    kliens = _kliens()
    osszes_javitas = 0
    for i, (fajl, cimke, evf, nyelv, ki) in enumerate(tennivalo, 1):
        jel = f"{cimke} {evf}. o." + (f" ({nyelv})" if nyelv else "")
        try:
            adat = app._chat_load_curriculum(fajl, evf, language=nyelv)
            katalogus = (adat or {}).get("topic_catalog") or []
        except Exception:
            katalogus = []
        if not katalogus:
            print(f"[{i}/{len(tennivalo)}] {jel} – nincs tananyag, kihagyva")
            continue

        print(f"[{i}/{len(tennivalo)}] {jel} – {len(katalogus)} témakör")
        tervek = []
        for t in katalogus:
            try:
                terv = _egy_temakor(kliens, cimke, evf, nyelv, t)
            except KeyboardInterrupt:
                print("\nMegszakítva. Ami kész, az megmaradt.")
                return 0
            except Exception as hiba:
                print(f"      ! {t['name'][:40]}: {type(hiba).__name__}: "
                      f"{str(hiba)[:120]}")
                continue
            db = len(terv["tenyellenorzes"]["javitasok"])
            osszes_javitas += db
            print(f"      · {t['name'][:44]:44} {len(terv['lepesek'])} lépés"
                  + (f", {db} ténybeli javítás" if db else ""))
            for gy in terv["tenyellenorzes"]["gyanus_maradt"]:
                print(f"        ! bennemaradt: {gy}")
            tervek.append(terv)

        if not tervek:
            continue
        ki.write_text(json.dumps({
            "tantargy_fajl": fajl,
            "tantargy": cimke,
            "evfolyam": evf,
            "nyelv": nyelv,
            "keszult": date.today().isoformat(),
            "keszito_modell": KESZITO_MODELL,
            "temakorok": tervek,
        }, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"      → {ki.name}")

    print(f"\nKész. Összesen {osszes_javitas} ténybeli hibát javított ki az "
          "ellenőrző, MIELŐTT bármelyik gyerek látta volna.")
    print(f"A tervek itt vannak: {MAPPA}")
    print("Az OLDAL ettől nem változott semmit — az app.py-hoz ez a program "
          "hozzá sem nyúlt. A bekötés külön lépés lesz.")
    print("Ha van fent '! bennemaradt' sor, azt az ellenőrző nem vette észre.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
