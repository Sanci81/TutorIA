# -*- coding: utf-8 -*-
"""TutorIA – A „MESE SORRENDBEN” (mesesor) feladat képei (fix207, második változat)

Sándor 11.19: az első képek nem jók – hiányzó részletek, a „répa” retek/fehérrépa
lett lila tetővel. Ezért most:
  * minden mesének van egy SZEREPLŐLAPJA (1 kép, mindenki egymás mellett) – a
    jelenetek ebből veszik, hogy néz ki a nagyapó, a malac, a farkas…, így minden
    képen ugyanazok a szereplők;
  * minden jelenet PONTOSAN le van írva: ki van rajta, mit csinál, mi van a háttérben,
    és mi NEM lehet rajta;
  * a répa SÁRGARÉPA (narancssárga, hegyes, zöld leveles) – a spanyol oldalon a mese
    címe ezért „La zanahoria gigante” lett.
A magyar és a spanyol oldal UGYANAZOKAT a képeket használja. A képeken nincs szöveg.
Az új képek új mappába kerülnek (szokep_uj/mese2), a régi rossz képek nem zavarnak.

LÉPÉSEK – EGYENKÉNT futtasd, mindegyik után nézd meg a képet:
    python mese_kepek.py --szereplok repa
        1 kép: a répa szereplői. Nézd meg: szokep_uj/mese2/attekinto.html
        Ha nem jó: futtasd újra ugyanezt (felülírja).
    python mese_kepek.py --mese repa
        4 jelenet a szereplőlapból. Ha egy nem jó, csak azt kérd újra, pl.:
    python mese_kepek.py --mese repa --ujra 3
    (ugyanígy: malac, piroska)

    python mese_kepek.py --jovahagy
        static/figurak/mese/repa_1.webp … lesz belőle (csak ami elkészült).
    git add static/figurak/mese

Költség: mesénként 5 kép (1 szereplőlap + 4 jelenet), összesen 15, közepes minőségben.
MI KELL HOZZÁ: OPENAI_API_KEY és a Pillow (ugyanaz, mint a figura_kepek.py-nál).
"""

from __future__ import annotations

import argparse
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import figura_kepek as fk   # ugyanaz a modell és hívás

GYOKER = os.path.dirname(os.path.abspath(__file__))
MAPPA = os.path.join(GYOKER, "szokep_uj", "mese2")
VEGLEGES = os.path.join(GYOKER, "static", "figurak", "mese")
MERET = "1024x1024"

# A szóképtár (static/szokepek/nyelv) stílusához igazodik. A kép a feladatban
# KICSI (kb. 150 pont), ezért: kevés, nagy, jól látható elem.
STILUS = (
    "Children's picture-book illustration in a simple, friendly cartoon style: clean dark "
    "outlines, soft flat colours with gentle shading, warm cheerful light. Made for 6-year-olds "
    "and shown SMALL on a phone, so: few, large, clearly readable shapes, characters big in the "
    "frame, no tiny clutter. Square picture, plain soft cream background or a very simple setting."
)
TILTAS = (
    "Absolutely no text, no letters, no numbers, no speech bubbles, no watermark, no logo, "
    "no border, no frame, no panels or comic strips (ONE single picture). Nothing scary or "
    "violent: no weapons, no blood, no sharp teeth showing, friendly faces, gentle mood."
)

MESEK = {
    # ── A RÉPA / LA ZANAHORIA GIGANTE ───────────────────────────────────────
    "repa": {
        "szereplok": (
            "GRANDPA: a kind old man, bald on top with short white hair at the sides, a short "
            "white beard, rosy cheeks, red-and-white checked shirt, blue dungarees, brown boots. "
            "GRANDMA: a round, cheerful old woman, grey hair in a bun, small round glasses, a red "
            "headscarf with white polka dots, a green dress and a white apron. "
            "GRANDDAUGHTER: a girl of about 6 with two blond braids and a yellow dress. "
            "DOG: a small brown-and-white dog with floppy ears. CAT: an orange tabby cat. "
            "MOUSE: a tiny grey mouse with big round ears. "
            "THE CARROT: a CARROT (not a radish, not a beet, not a turnip): bright ORANGE, long "
            "and pointed, with faint horizontal lines, and a bushy bright GREEN leafy top. "
            "Nothing on it is purple or white."
        ),
        "jelenetek": [
            "Only GRANDPA. He kneels in a vegetable garden at a bed of dark brown soil and with "
            "both hands plants ONE tiny carrot seedling (a small green sprout). A green watering "
            "can stands next to him. Background: a low wooden fence and a small white cottage "
            "with a red roof, morning sun. No other people or animals.",
            "Only GRANDPA and THE CARROT. In the same garden an ENORMOUS carrot has grown: only "
            "its wide ORANGE top part sticks out of the soil (as wide as grandpa is tall), with a "
            "huge bushy GREEN leafy top much taller than grandpa. Grandpa stands next to it, "
            "scratching his head, mouth open in amazement. The rest of the carrot is still under "
            "the ground.",
            "ALL SIX characters pull the giant carrot together, in ONE ROW from left to right, "
            "everyone shown whole from head to toe: on the far left the orange carrot top with "
            "its green leaves, still stuck in the soil; GRANDPA holds the green leaves with both "
            "hands and leans back; GRANDMA holds grandpa around the waist; the GRANDDAUGHTER "
            "holds grandma's apron; the DOG holds the girl's dress in its mouth; the CAT holds "
            "the dog's tail; the tiny MOUSE holds the cat's tail. All lean back and pull hard, "
            "but they look cheerful and determined. Count them: exactly 6 characters.",
            "The giant ORANGE carrot has just popped out of the ground and lies on the grass, "
            "whole and huge (long pointed tip, green leafy top). GRANDPA, GRANDMA, the "
            "GRANDDAUGHTER, the DOG, the CAT and the MOUSE have tumbled backwards in a happy heap "
            "and laugh; a few small clumps of soil fly in the air. All 6 characters visible.",
        ],
    },
    # ── A HÁROM KISMALAC / LOS TRES CERDITOS ────────────────────────────────
    "malac": {
        "szereplok": (
            "THREE LITTLE PIGS: pink, round, standing upright on two legs like small children, "
            "same size, each easy to tell apart by its shirt: PIG 1 wears a YELLOW shirt, PIG 2 a "
            "BLUE shirt, PIG 3 a RED shirt. "
            "THE WOLF: a big grey cartoon wolf, silly and clumsy, NOT scary: shaggy grey fur, "
            "light grey muzzle, big round eyes, a brown patched waistcoat, mouth closed or "
            "grinning without showing teeth."
        ),
        "jelenetek": [
            "Only the THREE LITTLE PIGS, side by side on a sunny green meadow, ready to build "
            "their houses: PIG 1 (yellow shirt) carries a big bundle of golden straw, PIG 2 "
            "(blue shirt) carries a bundle of wooden sticks, PIG 3 (red shirt) pushes a "
            "wheelbarrow full of red bricks. They smile and wave. No wolf.",
            "Only PIG 1 (yellow shirt), standing proudly in front of his small finished house "
            "made ENTIRELY of golden straw: straw walls, a straw roof, a little round window and "
            "a small wooden door. Sunny meadow. No other pigs, no wolf.",
            "THE WOLF stands on the left with his cheeks puffed up like balloons and blows a big "
            "white swirl of wind at the straw house; the straw house flies apart, bits of straw "
            "whirl in the air; PIG 1 (yellow shirt) runs away to the right, surprised but safe. "
            "Funny, not scary.",
            "A sturdy RED BRICK house with a chimney and a green door. All THREE LITTLE PIGS "
            "(yellow, blue and red shirts) look out happily from the open door and the window, "
            "safe. Outside on the left THE WOLF sits on the ground, exhausted, out of breath, with "
            "a big sweat drop, giving up. Funny, not scary.",
        ],
    },
    # ── PIROSKA ÉS A FARKAS / CAPERUCITA ROJA ───────────────────────────────
    "piroska": {
        "szereplok": (
            "THE GIRL (Little Red Riding Hood): about 6 years old, short brown hair, a bright RED "
            "hooded cape, white blouse, blue skirt, carrying a wicker basket covered with a "
            "red-and-white checked cloth. "
            "MOTHER: a young woman with brown hair in a bun, a green dress and a white apron. "
            "GRANDMA: a small old woman with white hair in a bun, round glasses, a pink dress. "
            "THE WOLF: a big grey cartoon wolf, silly and sly, NOT scary, shaggy grey fur, "
            "light grey muzzle, mouth closed or grinning without teeth. "
            "THE HUNTER: a friendly man with a brown moustache, a green hat with a feather, a "
            "brown jacket and boots, NO gun or weapon."
        ),
        "jelenetek": [
            "THE GIRL in the red hooded cape, with her basket, waves goodbye as she sets off "
            "from the door of a small cottage; MOTHER stands in the doorway and waves back. A "
            "path leads towards a green forest in the background. No wolf.",
            "A sunny forest path between tall trees with flowers at the side. THE GIRL in the "
            "red hooded cape, holding her basket, meets THE WOLF, who bows politely and points "
            "down the path with one paw, smiling slyly. The girl looks curious, not afraid.",
            "Grandma's cosy little bedroom: THE WOLF lies in grandma's bed under a colourful "
            "patchwork quilt, wearing grandma's white lace NIGHTCAP and her round glasses, "
            "pulling the quilt up to his chin; his big ears stick out of the nightcap. THE GIRL "
            "in the red hooded cape stands at the door with her basket, looking surprised. "
            "Grandma is NOT in the picture.",
            "Grandma's cosy room: THE HUNTER, GRANDMA and THE GIRL in the red hooded cape stand "
            "together, hugging and smiling happily. Through the window, far away, THE WOLF runs "
            "off into the forest. No weapons anywhere.",
        ],
    },
}


def _kliens():
    from openai import OpenAI
    return OpenAI()


def _ut(mese: str, n) -> str:
    return os.path.join(MAPPA, f"{mese}_{n}.png")


def attekinto() -> None:
    os.makedirs(MAPPA, exist_ok=True)
    sorok = []
    for mese in MESEK:
        kepek = "".join(
            f'<figure><img src="{mese}_{n}.png"><figcaption>{mese} – '
            f'{"szereplők" if n == "szereplok" else str(n) + "."}</figcaption></figure>'
            for n in ["szereplok", 1, 2, 3, 4] if os.path.exists(_ut(mese, n)))
        if kepek:
            sorok.append(f"<h2>{mese}</h2><main>{kepek}</main>")
    with open(os.path.join(MAPPA, "attekinto.html"), "w", encoding="utf-8") as ki:
        ki.write('<!doctype html><meta charset="utf-8"><title>Mesék</title>'
                 '<style>body{font-family:system-ui;background:#FBF5EA;padding:20px}'
                 'main{display:grid;grid-template-columns:repeat(5,1fr);gap:12px}'
                 'figure{margin:0;background:#fff;border-radius:12px;padding:8px}img{width:100%}'
                 'figcaption{text-align:center;font-weight:700}</style><h1>Mese-képek</h1>'
                 + "".join(sorok))


def szereplok(mese: str, minoseg: str) -> int:
    os.makedirs(MAPPA, exist_ok=True)
    print(f"  {mese}: szereplőlap …", flush=True)
    prompt = (f"{STILUS} A CHARACTER SHEET: all the characters of one fairy tale standing side by "
              f"side in a row, each shown whole from head to toe, facing the viewer, plenty of "
              f"space between them, plain cream background. The characters: "
              f"{MESEK[mese]['szereplok']} {TILTAS}")
    try:
        v = fk._hivas(_kliens().images.generate, model=fk.MODELL, size="1536x1024", n=1,
                      quality=minoseg, prompt=prompt)
        with open(_ut(mese, "szereplok"), "wb") as ki:
            ki.write(fk._kep_bajt(v))
    except Exception as e:
        print(f"   ! nem sikerült: {type(e).__name__}: {str(e)[:200]}")
        return 1
    attekinto()
    print(f"\nNézd meg: szokep_uj/mese2/attekinto.html – ha jó: python mese_kepek.py --mese {mese}")
    return 0


def jelenet(kl, mese: str, n: int, minoseg: str) -> None:
    lap = _ut(mese, "szereplok")
    print(f"  {mese} {n}. kép …", flush=True)
    prompt = (f"Use the attached character sheet ONLY to see what the characters look like (faces, "
              f"clothes, colours, proportions) – keep them exactly like that. Draw a completely NEW "
              f"single scene with its own composition (not a row of characters). "
              f"The characters: {MESEK[mese]['szereplok']} "
              f"THE SCENE: {MESEK[mese]['jelenetek'][n - 1]} {STILUS} {TILTAS}")
    with open(lap, "rb") as ref:
        v = fk._hivas(kl.images.edit, model=fk.MODELL, image=ref, size=MERET, quality=minoseg,
                      input_fidelity="high", prompt=prompt)
    with open(_ut(mese, n), "wb") as ki:
        ki.write(fk._kep_bajt(v))


def jelenetek(mese: str, ujra: int | None, minoseg: str) -> int:
    if not os.path.exists(_ut(mese, "szereplok")):
        print(f"Előbb a szereplőlap kell: python mese_kepek.py --szereplok {mese}")
        return 1
    kl = _kliens()
    for n in ([ujra] if ujra else [1, 2, 3, 4]):
        if not ujra and os.path.exists(_ut(mese, n)):
            print(f"  {mese} {n}. már megvan (újra: python mese_kepek.py --mese {mese} --ujra {n})")
            continue
        try:
            jelenet(kl, mese, n, minoseg)
        except Exception as e:
            print(f"   ! nem sikerült: {type(e).__name__}: {str(e)[:200]}")
    attekinto()
    print("\nNézd meg: szokep_uj/mese2/attekinto.html")
    return 0


def jovahagy() -> int:
    from PIL import Image
    os.makedirs(VEGLEGES, exist_ok=True)
    db = 0
    for mese in MESEK:
        for n in range(1, 5):
            ut = _ut(mese, n)
            if not os.path.exists(ut):
                continue
            k = Image.open(ut).convert("RGB")
            k.thumbnail((512, 512), Image.LANCZOS)
            k.save(os.path.join(VEGLEGES, f"{mese}_{n}.webp"), "WEBP", quality=86, method=6)
            db += 1
    print(f"Kész: {db} kép a static/figurak/mese mappában.")
    print("Egy mese csak akkor vált képre a feladatban, ha a 4. képe is megvan.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--szereplok", choices=list(MESEK))
    ap.add_argument("--mese", choices=list(MESEK))
    ap.add_argument("--ujra", type=int, choices=[1, 2, 3, 4])
    ap.add_argument("--jovahagy", action="store_true")
    ap.add_argument("--minoseg", default="medium", choices=["low", "medium", "high"])
    a = ap.parse_args()
    if a.jovahagy:
        return jovahagy()
    if a.szereplok:
        return szereplok(a.szereplok, a.minoseg)
    if a.mese:
        return jelenetek(a.mese, a.ujra, a.minoseg)
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
