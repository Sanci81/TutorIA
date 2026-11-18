# -*- coding: utf-8 -*-
"""TutorIA – A KROKODIL KÉPEI a „nagyobb, kisebb, egyenlő” feladathoz (fix191)

Sándor 11.18: a rajzolt (SVG) krokodil „ultra gagyi”. Ezért ugyanúgy
AI-képet kap, mint a cica-feladat cicája: mesekönyv-stílus, átlátszó háttér.
Három kép kell, ugyanaz a krokodil: TÁTOTT szájú, CSUKOTT szájú, és az
EGYENLŐ jelhez (=) ÁLLÓ krokodil, kezében egyensúlyban lévő mérleggel.
A < és a > jelnél a program tükrözi a képet, nem kell külön kép.

1. LÉPÉS – 3 JELÖLT (ebből választasz)
    python krokodil_kepek.py --jeloltek
        Nyisd meg: szokep_uj/krokodil/attekinto.html

2. LÉPÉS – A KIVÁLASZTOTT + A CSUKOTT SZÁJÚ VÁLTOZAT
    python krokodil_kepek.py --valaszt 2
        A 2. jelölt lesz a tátott szájú; ebből készül a csukott szájú és a mérleges.
        Nézd meg újra az attekinto.html-t. Ha a csukott nem jó:
    python krokodil_kepek.py --csukott-ujra
    python krokodil_kepek.py --merleg-ujra

3. LÉPÉS – JÓVÁHAGYÁS
    python krokodil_kepek.py --jovahagy
        static/figurak/krokodil/nyitott.webp, csukott.webp és merleg.webp lesz belőle.
        Töltsd fel: git add static/figurak/krokodil

MI KELL HOZZÁ: OPENAI_API_KEY és a Pillow (ugyanaz, mint a figura_kepek.py-nál).
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import figura_kepek as fk   # ugyanaz a modell, hívás és háttér-levevő

GYOKER = os.path.dirname(os.path.abspath(__file__))
MAPPA = os.path.join(GYOKER, "szokep_uj", "krokodil")
VEGLEGES = os.path.join(GYOKER, "static", "figurak", "krokodil")
MERET = "1536x1024"

ALANY = (
    "one cute friendly cartoon crocodile for a children's maths app, seen exactly "
    "from the side, facing RIGHT, whole body visible, chunky short body, big head, "
    "short legs, a short curled tail, bright fresh green with a lighter yellow-green "
    "belly, soft rounded scales on the back, big friendly eyes on top of the head. "
    "Its jaws are opened VERY WIDE towards the right, like the letter V lying on its "
    "side, showing a pink tongue and a neat row of small white rounded teeth, a "
    "happy hungry expression"
)
# A figura_kepek STILUS-a „front view”-t kér – itt OLDALNÉZET kell, ezért saját.
STILUS = (
    "high-quality children's picture-book illustration, soft painterly shading, "
    "gentle warm light, clean confident outlines, rich but soft colours, friendly "
    "and lively, one single character, centred, plenty of empty space around it, "
    "plain pure white background, no floor, no shadow on the ground"
)
CSUKOTT = (
    "This is the same crocodile. Keep EVERYTHING identical: same character, same "
    "colours, same size, same position in the picture, same body, legs, tail, eyes, "
    "same plain white background. Only change one thing: its mouth is now CLOSED, "
    "the two jaws lie together in a gentle happy smile, no teeth gaps, calm and content."
)
MERLEG = (
    "This is the same crocodile character. Keep the same character, the same colours, "
    "the same friendly face and the same picture-book style, the same plain white "
    "background. Now it STANDS upright on its two hind legs like a cartoon character, "
    "facing the viewer, smiling, and holds in its front paws a small golden balance "
    "scale. The scale is perfectly LEVEL: both pans hang at exactly the same height "
    "and each pan holds one identical red apple. Mouth closed, calm and pleased. "
    "Whole body visible from head to feet, centred."
)


def _kliens():
    from openai import OpenAI
    return OpenAI()


def attekinto() -> None:
    os.makedirs(MAPPA, exist_ok=True)
    kepek = [n for n in sorted(os.listdir(MAPPA)) if n.endswith(".png")]
    sor = "".join(f'<figure><img src="{n}"><figcaption>{n}</figcaption></figure>' for n in kepek)
    with open(os.path.join(MAPPA, "attekinto.html"), "w", encoding="utf-8") as ki:
        ki.write('<!doctype html><meta charset="utf-8"><title>Krokodil</title>'
                 '<style>body{font-family:system-ui;background:#FBF5EA;padding:20px}'
                 'main{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:16px}'
                 'figure{margin:0;background:#fff;border-radius:12px;padding:8px}img{width:100%}'
                 'figcaption{text-align:center;font-weight:700}</style><h1>Krokodil-képek</h1><main>'
                 + sor + "</main>")


def jeloltek(db: int, minoseg: str) -> int:
    os.makedirs(MAPPA, exist_ok=True)
    kl = _kliens()
    for i in range(1, db + 1):
        ut = os.path.join(MAPPA, f"jelolt_{i}.png")
        if os.path.exists(ut):
            print(f"  {i}. jelölt már megvan (töröld, ha újat kérsz)")
            continue
        print(f"  {i}. jelölt …", flush=True)
        try:
            v = fk._hivas(kl.images.generate, model=fk.MODELL, size=MERET, n=1, quality=minoseg,
                          prompt=f"{STILUS}. Subject: {ALANY}. {fk.TILTAS}")
            with open(ut, "wb") as ki:
                ki.write(fk._kep_bajt(v))
        except Exception as e:
            print(f"   ! nem sikerült: {type(e).__name__}: {str(e)[:200]}")
    attekinto()
    print("\nNyisd meg: szokep_uj/krokodil/attekinto.html, aztán: python krokodil_kepek.py --valaszt <szám>")
    return 0


def csukott(minoseg: str) -> int:
    alap = os.path.join(MAPPA, "nyitott.png")
    if not os.path.exists(alap):
        print("Előbb: python krokodil_kepek.py --valaszt <szám>")
        return 1
    print("  csukott szájú változat …", flush=True)
    kl = _kliens()
    with open(alap, "rb") as kep:
        v = fk._hivas(kl.images.edit, model=fk.MODELL, image=kep, size=MERET,
                      prompt=CSUKOTT, input_fidelity="high", quality=minoseg)
    with open(os.path.join(MAPPA, "csukott.png"), "wb") as ki:
        ki.write(fk._kep_bajt(v))
    attekinto()
    print("OK. Nézd meg az attekinto.html-t (nyitott.png és csukott.png). Ha jó: python krokodil_kepek.py --jovahagy")
    return 0


def merleg(minoseg: str) -> int:
    alap = os.path.join(MAPPA, "nyitott.png")
    if not os.path.exists(alap):
        print("Előbb: python krokodil_kepek.py --valaszt <szám>")
        return 1
    print("  mérleges (egyenlő) változat …", flush=True)
    kl = _kliens()
    with open(alap, "rb") as kep:
        v = fk._hivas(kl.images.edit, model=fk.MODELL, image=kep, size="1024x1536",
                      prompt=MERLEG, input_fidelity="high", quality=minoseg)
    with open(os.path.join(MAPPA, "merleg.png"), "wb") as ki:
        ki.write(fk._kep_bajt(v))
    attekinto()
    print("OK: merleg.png. Ha jó: python krokodil_kepek.py --jovahagy")
    return 0


def valaszt(sz: int, minoseg: str) -> int:
    forras = os.path.join(MAPPA, f"jelolt_{sz}.png")
    if not os.path.exists(forras):
        print(f"Nincs ilyen jelölt: {forras}")
        return 1
    shutil.copyfile(forras, os.path.join(MAPPA, "nyitott.png"))
    print(f"OK: a {sz}. jelölt lett a tátott szájú.")
    return csukott(minoseg) or merleg(minoseg)


def jovahagy() -> int:
    from PIL import Image
    os.makedirs(VEGLEGES, exist_ok=True)
    kepek = {}
    for nev in ("nyitott", "csukott"):
        ut = os.path.join(MAPPA, nev + ".png")
        if not os.path.exists(ut):
            print(f"Hiányzik: {ut}")
            return 1
        kepek[nev] = fk._hatter_le(Image.open(ut))
    # Közös kivágás: a két kép UGYANOTT álljon, különben váltáskor ugrana.
    dobozok = [k.getchannel("A").getbbox() for k in kepek.values()]
    x0 = min(d[0] for d in dobozok); y0 = min(d[1] for d in dobozok)
    x1 = max(d[2] for d in dobozok); y1 = max(d[3] for d in dobozok)
    for nev, kep in kepek.items():
        k = kep.crop((max(0, x0 - 8), max(0, y0 - 8), x1 + 8, y1 + 8))
        k.thumbnail((640, 640), Image.LANCZOS)
        k.save(os.path.join(VEGLEGES, nev + ".webp"), "WEBP", quality=88, method=6)
        print(f"  kész: static/figurak/krokodil/{nev}.webp  {k.size}")
    # A mérleges külön kép (álló krokodil) – saját kivágással.
    ut = os.path.join(MAPPA, "merleg.png")
    if os.path.exists(ut):
        k = fk._hatter_le(Image.open(ut))
        d = k.getchannel("A").getbbox()
        k = k.crop((max(0, d[0] - 8), max(0, d[1] - 8), d[2] + 8, d[3] + 8))
        k.thumbnail((640, 640), Image.LANCZOS)
        k.save(os.path.join(VEGLEGES, "merleg.webp"), "WEBP", quality=88, method=6)
        print(f"  kész: static/figurak/krokodil/merleg.webp  {k.size}")
    else:
        print("  ! merleg.png hiányzik: python krokodil_kepek.py --merleg-ujra")
    print("\nTöltsd fel: git add static/figurak/krokodil  – és szólj Claude-nak, beépíti a feladatba.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--jeloltek", action="store_true")
    ap.add_argument("--db", type=int, default=3)
    ap.add_argument("--valaszt", type=int)
    ap.add_argument("--csukott-ujra", action="store_true")
    ap.add_argument("--merleg-ujra", action="store_true")
    ap.add_argument("--jovahagy", action="store_true")
    ap.add_argument("--minoseg", default="medium", choices=["low", "medium", "high"])
    a = ap.parse_args()
    if a.jeloltek:
        return jeloltek(a.db, a.minoseg)
    if a.valaszt:
        return valaszt(a.valaszt, a.minoseg)
    if a.csukott_ujra:
        return csukott(a.minoseg)
    if a.merleg_ujra:
        return merleg(a.minoseg)
    if a.jovahagy:
        return jovahagy()
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
