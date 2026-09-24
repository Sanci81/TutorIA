# -*- coding: utf-8 -*-
"""TutorIA – EGY kártyakép elkészítése, a bevált két lépésben.

MIÉRT VAN EZ
    2026-09-21-én sok kör után kiderült, hogy egy lépésben nem megy: a
    modell vagy jó kompozíciót ad rossz stílusban, vagy fordítva. Ami
    működött:

      1. lépés – legyártjuk a képet a „festett hős" szöveggel. Ez adja a
         jó beállítást, a kezet, a hátteret, a tárgyakat.
      2. lépés – ugyanezt a képet átrajzoltatjuk, mintának odaadva a már
         kész kártyákat. Ez adja a szett egységes stílusát.

    Ez a program ezt a kettőt futtatja le egymás után, EGY kártyára.
    Két kép, nagyjából hat cent.

MIT NEM CSINÁL
    Nem ír a static/kartyak mappába – azt csak OLVASSA, mintaként.
    Semmit nem ír felül: ha a fájl már létezik, új nevet kap.

HASZNÁLAT
    python kartya_kesz.py --hiany
        Kiírja, melyik kártyának nincs még végleges képe. INGYEN.

    python kartya_kesz.py magyar_7_petofi
        Elkészíti EZT az egyet, mindkét lépéssel.

    Az eredmény:  kartya_kepek_uj/kesz/<fajlnev>.png
    Ha jónak találod, másold át:  static/kartyak/<oldal>/<fajlnev>.png
"""

from __future__ import annotations

import argparse
import base64
import os
import sys

GYOKER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, GYOKER)

KESZ_MAPPA = os.path.join(GYOKER, "static", "kartyak")
CEL_MAPPA = os.path.join(GYOKER, "kartya_kepek_uj", "kesz")
MODELL = "gpt-image-2"
MERET = "1024x1024"

# Mintakártyák a 2. lépéshez. Ezek adják a szett stílusát.
MINTAK = ["fizika_7_newton", "kemia_7_mengyelejev", "kemia_7_arrhenius"]

# 1. LÉPÉS – ez a szöveg adta a jó kompozíciót. NE bővítsd: minden
# hozzátoldás (sötétebb, merészebb, hangulatosabb) olajfestménybe vitte.
STILUS = ("rich painterly digital illustration, confident brushwork, deep "
          "saturated colours, strong rim light, dramatic contrast, the "
          "person at work with their real instrument, detailed background, "
          "square composition with margin, the whole head and shoulders "
          "inside the frame, face clearly visible, "
          # 2026-09-21: a Kolumbusznál levágta a kezét, máshol eltűnt a
          # tárgy, ami miatt a kártya egyáltalán szól róla. A kártya
          # KÉPESSÉGE mindig abban a tárgyban látszik, ezért ez a két
          # mondat minden kártyánál ott van.
          "the object in their hands is large, prominent and fully "
          "visible, both hands complete and inside the frame, "
          "no cropped or cut-off hands")

TILTAS = ("No text, no letters, no numbers, no words, no captions, no "
          "signature, no watermark, no logo, no border, no frame, "
          "no modern clothing.")

# 2. LÉPÉS – az átrajzolás utasítása.
ATRAJZ = (
    "The FIRST image is the artwork to restyle. Redraw it completely, "
    "keeping the SAME person, the same face, the same pose, the same "
    "clothing, the same objects in their hands, the same background "
    "scene and the same composition. Change ONLY the art style: match "
    "exactly the style of the other reference images — their brushwork, "
    "their flat angular colour facets, their bold saturated palette, "
    "their strong coloured rim light, their level of stylisation. "
    "The result must look like it belongs to the same card set as the "
    "reference images, not like a realistic oil painting or photograph. "
    + TILTAS
)


def kartyak_listaja() -> list[dict]:
    import kartyak
    return kartyak.KARTYAK


def vegleges_ut(k: dict) -> str:
    return os.path.join(KESZ_MAPPA, k.get("oldal", "hu"), f"{k.get('kep')}.png")


def hianyzok() -> list[dict]:
    """Akinek NINCS képe a static/kartyak mappában."""
    return [k for k in kartyak_listaja() if not os.path.exists(vegleges_ut(k))]


def szabad_nev(ut: str) -> str:
    torzs = ut[:-4]
    jelolt = ut
    n = 2
    while os.path.exists(jelolt):
        jelolt = f"{torzs}_{n}.png"
        n += 1
    return jelolt


def minta_utak() -> list[str]:
    utak = []
    for n in MINTAK:
        for o in ("hu", "es"):
            ut = os.path.join(KESZ_MAPPA, o, f"{n}.png")
            if os.path.exists(ut):
                utak.append(ut)
                break
    return utak


def kep_bajtok(valasz) -> bytes:
    elem = valasz.data[0]
    b64 = getattr(elem, "b64_json", None)
    if b64:
        return base64.b64decode(b64)
    import urllib.request
    with urllib.request.urlopen(elem.url, timeout=60) as v:
        return v.read()


def main() -> int:
    ert = argparse.ArgumentParser(description="Egy kártyakép, két lépésben")
    ert.add_argument("kartya", nargs="?", default="",
                     help="a kártya fájlneve, pl. magyar_7_petofi")
    ert.add_argument("--hiany", action="store_true",
                     help="csak kiírja, mi hiányzik – nem kerül semmibe")
    args = ert.parse_args()

    if args.hiany or not args.kartya:
        h = hianyzok()
        print(f"Még {len(h)} kártyának nincs végleges képe:\n")
        for k in h:
            print(f"  {k.get('kep'):32} {k.get('nev')}")
        print("\nEgyet így készítesz el:")
        print(f"  python kartya_kesz.py {h[0].get('kep') if h else '<fajlnev>'}")
        return 0

    nev = args.kartya.replace(".png", "")
    talalt = [k for k in kartyak_listaja() if k.get("kep") == nev]
    if not talalt:
        print(f"Nincs ilyen kártya: {nev}")
        return 1
    k = talalt[0]

    if os.path.exists(vegleges_ut(k)):
        print(f"Ennek MÁR VAN végleges képe: {vegleges_ut(k)}")
        print("Ha mégis újat akarsz, előbb nevezd át a meglévőt.")
        return 0

    mintak = minta_utak()
    if not mintak:
        print("Nem találok mintakártyát a static/kartyak mappában.")
        return 1

    kulcs = os.environ.get("OPENAI_API_KEY", "").strip()
    if not kulcs:
        print("Hiányzik az OPENAI_API_KEY.")
        return 1
    try:
        from openai import OpenAI
    except ImportError:
        print("Hiányzik az openai csomag. Telepítsd: pip install openai")
        return 1

    kliens = OpenAI(api_key=kulcs)
    os.makedirs(CEL_MAPPA, exist_ok=True)

    alany = (k.get("prompt") or "").strip() or \
        f"{k.get('nev','')}, {k.get('alnev','')}".strip(" ,")

    print(f"{k.get('nev')} – két lépés, kb. hat cent.\n")

    # ── 1. lépés ───────────────────────────────────────────────────────
    print("1/2  A kompozíció készül…", flush=True)
    try:
        v1 = kliens.images.generate(
            model=MODELL, prompt=f"{STILUS}. {alany} {TILTAS}",
            size=MERET, n=1)
        adat1 = kep_bajtok(v1)
    except Exception as exc:
        print(f"     HIBA: {exc}")
        return 1

    ut1 = szabad_nev(os.path.join(CEL_MAPPA, f"{k.get('kep')}__1_alap.png"))
    try:
        with open(ut1, "wb") as f:
            f.write(adat1)
    except Exception as exc:
        print(f"     HIBA a mentésnél: {exc}")
        print("     Zárd be a képnézegetőt, és futtasd újra.")
        return 1
    print(f"     -> {os.path.basename(ut1)}")

    # ── 2. lépés ───────────────────────────────────────────────────────
    print("2/2  Átrajzolás a szett stílusára…", flush=True)
    fajlok = [open(ut1, "rb")] + [open(m, "rb") for m in mintak]
    try:
        v2 = kliens.images.edit(
            model=MODELL, image=fajlok, prompt=ATRAJZ, size=MERET, n=1)
        adat2 = kep_bajtok(v2)
    except Exception as exc:
        print(f"     HIBA: {exc}")
        print(f"     Az 1. lépés képe megvan: {ut1}")
        return 1
    finally:
        for f in fajlok:
            f.close()

    ut2 = szabad_nev(os.path.join(CEL_MAPPA, f"{k.get('kep')}.png"))
    try:
        with open(ut2, "wb") as f:
            f.write(adat2)
    except Exception as exc:
        print(f"     HIBA a mentésnél: {exc}")
        return 1

    print(f"\nKÉSZ: {ut2}")
    print("Ha jó, másold ide:")
    print(f"  {vegleges_ut(k)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
