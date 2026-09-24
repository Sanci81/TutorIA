# -*- coding: utf-8 -*-
"""TutorIA – új kártyakép a MEGLÉVŐ kártyák stílusában, MINTAKÉP alapján.

MIÉRT VAN EZ
    Szavakkal nem lehet pontosan leírni egy rajzstílust. Öt körön át
    próbáltuk – hol festmény lett, hol mese, hol képregény. A modell
    viszont KÉPET is tud bemenetként fogadni: ha megmutatjuk neki a már
    kész kártyákat, és azt kérjük, hogy ugyanabban a stílusban rajzoljon
    újat, akkor nem a mi szavainkból kell kitalálnia, hanem LÁTJA.

    A minta: static/kartyak/<oldal>/ néhány kész kártya. Ezeket a program
    CSAK OLVASSA, hozzájuk nem nyúl.

HASZNÁLAT
    python kartya_kep_minta.py foldrajz_7_kolumbusz
        Egy kép, a meglévő kártyák stílusában.

    python kartya_kep_minta.py foldrajz_7_kolumbusz --minta fizika_7_newton kemia_7_curie
        Te választod meg, melyik kártyák legyenek a minták.

    Az eredmény ide kerül:
        kartya_kepek_uj/mintaval/<fajlnev>.png
"""

from __future__ import annotations

import argparse
import base64
import os
import sys

GYOKER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, GYOKER)

CEL_MAPPA = os.path.join(GYOKER, "kartya_kepek_uj", "mintaval")
KESZ_MAPPA = os.path.join(GYOKER, "static", "kartyak")
MODELL = "gpt-image-2"
MERET = "1024x1024"

# Alapértelmezett minták. Ezek a legjellemzőbbek a meglévő szettre.
ALAP_MINTAK = ["fizika_7_newton", "kemia_7_curie", "kemia_7_mengyelejev"]


def kartya_keres(nev: str) -> dict:
    import kartyak
    nev = nev.replace(".png", "")
    for k in kartyak.KARTYAK:
        if k.get("kep") == nev:
            return k
    raise SystemExit(f"Nincs ilyen kártya: {nev}")


def minta_utak(nevek: list[str], oldal: str) -> list[str]:
    utak = []
    for n in nevek:
        n = n.replace(".png", "")
        for o in (oldal, "hu", "es"):
            ut = os.path.join(KESZ_MAPPA, o, f"{n}.png")
            if os.path.exists(ut):
                utak.append(ut)
                break
        else:
            print(f"  (nem találom a mintát: {n}.png – kihagyom)")
    return utak


def utasitas(k: dict) -> str:
    """A modellnek szóló szöveg. A STÍLUST a mintaképek adják, nem ez."""
    alany = (k.get("prompt") or "").strip()
    if not alany:
        alany = f"{k.get('nev', '')}, {k.get('alnev', '')}".strip(" ,")
    return (
        "Draw a COMPLETELY NEW single-character portrait illustration in "
        "EXACTLY the same art style as the reference images: the same "
        "brushwork, the same flat angular colour facets, the same colour "
        "palette, the same lighting and contrast, the same level of "
        "stylisation, the same square framing of head and shoulders. "
        "Do NOT copy any person, object or background from the "
        "references — only their art style. "
        # 2026-09-21: a mintaképes kör technikailag eltalálta az ecsetet,
        # de „túl modern" lett. A különbség pontosan ez a kettő volt:
        # a meglévő kártyákon az ARCON is vad, természetellenes színek
        # vannak (kék, zöld, magenta foltok), a háttér pedig majdnem
        # fekete, zöldes-türkiz, durva textúrával – nem szép, természetes
        # égbolt. Ezt szavakkal kell hozzátenni, mert a modell magától a
        # természeteshez húz.
        "Very important: paint the skin and face with bold UNNATURAL "
        "colour patches — blue, green, magenta and turquoise reflections "
        "across the face — exactly as in the references, not natural "
        "skin tone. Keep the background very dark, almost black, with a "
        "green-teal tint and rough scratchy texture; no pretty natural "
        "sky, no sunset, no bright daylight. Moody and high contrast. "
        f"The new subject is: {alany} "
        "No text, no letters, no numbers, no signature, no watermark, "
        "no border, no frame."
    )


def main() -> int:
    ert = argparse.ArgumentParser(
        description="Kártyakép a meglévő kártyák stílusában")
    ert.add_argument("kartya", help="a kártya fájlneve, pl. foldrajz_7_kolumbusz")
    ert.add_argument("--minta", nargs="*", default=None,
                     help="mintakártyák fájlnevei (alapból Newton, Curie, Mengyelejev)")
    args = ert.parse_args()

    k = kartya_keres(args.kartya)
    mintak = minta_utak(args.minta or ALAP_MINTAK, k.get("oldal", "hu"))
    if not mintak:
        print("Egyetlen mintaképet sem találok. Nézd meg a static/kartyak mappát.")
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

    print(f"{k.get('nev')} – minta: " +
          ", ".join(os.path.basename(m) for m in mintak))
    print("Készül…", flush=True)

    fajlok = [open(m, "rb") for m in mintak]
    try:
        valasz = kliens.images.edit(
            model=MODELL,
            image=fajlok,
            prompt=utasitas(k),
            size=MERET,
            n=1,
        )
    finally:
        for f in fajlok:
            f.close()

    elem = valasz.data[0]
    b64 = getattr(elem, "b64_json", None)
    if b64:
        adat = base64.b64decode(b64)
    else:
        import urllib.request
        with urllib.request.urlopen(elem.url, timeout=60) as v:
            adat = v.read()

    ut = os.path.join(CEL_MAPPA, f"{k.get('kep')}.png")
    with open(ut, "wb") as f:
        f.write(adat)
    print(f"Kész: {ut}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
