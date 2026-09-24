# -*- coding: utf-8 -*-
"""TutorIA – egy KÉSZ kép átrajzolása a meglévő kártyák stílusában.

MIÉRT VAN EZ
    Előfordul, hogy a kép TARTALMA már jó – jó a beállítás, a kéz, a
    háttér, minden a helyén van –, csak a rajzstílus nem illik a
    szetthez. Ilyenkor kár újat generálni: könnyen elveszik a jó
    kompozíció is.

    Ez a program megtartja a képet, és CSAK a stílusát cseréli le.
    Odaadja a modellnek a kész képet, mellé mintának néhány meglévő
    kártyát, és azt kéri: ugyanez a kép, de az ő rajzstílusukban.

MIT NEM CSINÁL
    Nem ír felül semmit. Az eredmény új fájlba kerül, a bemeneti kép
    mellé, "_atrajzolva" végződéssel. A static/kartyak mappát csak
    olvassa.

HASZNÁLAT
    python kartya_atstilizal.py kartya_kepek_uj\\stilusproba\\foldrajz_7_kolumbusz__1_festett_3.png

    python kartya_atstilizal.py <kep.png> --minta fizika_7_newton kemia_7_curie
"""

from __future__ import annotations

import argparse
import base64
import os
import sys

GYOKER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, GYOKER)

KESZ_MAPPA = os.path.join(GYOKER, "static", "kartyak")
MODELL = "gpt-image-2"
MERET = "1024x1024"

ALAP_MINTAK = ["fizika_7_newton", "kemia_7_mengyelejev", "kemia_7_arrhenius"]

UTASITAS = (
    "The FIRST image is the artwork to restyle. Redraw it completely, "
    "keeping the SAME person, the same face, the same pose, the same "
    "clothing, the same objects in their hands, the same background "
    "scene and the same composition. Change ONLY the art style: match "
    "exactly the style of the other reference images — their brushwork, "
    "their flat angular colour facets, their bold saturated palette, "
    "their strong coloured rim light, their level of stylisation. "
    "The result must look like it belongs to the same card set as the "
    "reference images, not like a realistic oil painting or photograph. "
    "No text, no letters, no numbers, no signature, no watermark, "
    "no border, no frame."
)


def minta_utak(nevek: list[str]) -> list[str]:
    utak = []
    for n in nevek:
        n = n.replace(".png", "")
        for o in ("hu", "es"):
            ut = os.path.join(KESZ_MAPPA, o, f"{n}.png")
            if os.path.exists(ut):
                utak.append(ut)
                break
        else:
            print(f"  (nem találom a mintát: {n}.png – kihagyom)")
    return utak


def szabad_nev(ut: str) -> str:
    torzs = ut[:-4] if ut.lower().endswith(".png") else ut
    jelolt = f"{torzs}_atrajzolva.png"
    n = 2
    while os.path.exists(jelolt):
        jelolt = f"{torzs}_atrajzolva_{n}.png"
        n += 1
    return jelolt


def main() -> int:
    ert = argparse.ArgumentParser(
        description="Kész kép átrajzolása a kártyák stílusában")
    ert.add_argument("kep", help="a jó kép útvonala (png)")
    ert.add_argument("--minta", nargs="*", default=None,
                     help="mintakártyák fájlnevei")
    args = ert.parse_args()

    if not os.path.exists(args.kep):
        print(f"Nincs ilyen fájl: {args.kep}")
        return 1

    mintak = minta_utak(args.minta or ALAP_MINTAK)
    if not mintak:
        print("Egyetlen mintaképet sem találok a static/kartyak mappában.")
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
    print("Átrajzolandó:", os.path.basename(args.kep))
    print("Minta:", ", ".join(os.path.basename(m) for m in mintak))
    print("Készül…", flush=True)

    fajlok = [open(args.kep, "rb")] + [open(m, "rb") for m in mintak]
    try:
        valasz = kliens.images.edit(
            model=MODELL, image=fajlok, prompt=UTASITAS, size=MERET, n=1)
    except Exception as exc:
        print(f"HIBA: {exc}")
        return 1
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

    ki = szabad_nev(args.kep)
    try:
        with open(ki, "wb") as f:
            f.write(adat)
    except Exception as exc:
        print(f"HIBA a mentésnél: {exc}")
        print("Zárd be a képnézegetőt, és futtasd újra.")
        return 1
    print(f"Kész: {ki}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
