"""Halloweeni Facebook-posztok RAJZAI – szöveg NÉLKÜL (a szöveget Claude teszi rá,
mert a képgenerátor elrontja a betűket). 3 kép, kb. 0,5 $ (high minőség).

Futtatás a TutorIA mappában:
    python halloween_kepek.py
Egyet újra (ha nem tetszik):
    python halloween_kepek.py --csak macskak --ujra

Eredmény: kinézet képek/facebook/halloween/<név>.png  (1024x1536, álló)
"""
import argparse
import os
import sys
import time

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import figura_kepek as fk

MAPPA = os.path.join(fk.GYOKER, "kinézet képek", "facebook", "halloween")
STILUS = (
    "Premium children's picture-book illustration, warm painterly digital art with soft "
    "lighting and rich texture, friendly and cute, NOT scary, cheerful Halloween mood, "
    "deep purple and midnight-blue night sky with a big glowing full moon, warm orange "
    "highlights, clean composition. Leave the TOP THIRD of the picture as calm, simple "
    "night sky with no objects (text will be placed there). Absolutely no text, no letters, "
    "no numbers, no watermark, no logo, no signature, no frame.")
KEPEK = {
    "tok": "A big, cute, smiling carved jack-o'-lantern pumpkin glowing warmly from inside, "
           "sitting on a mossy hill in the bottom half of the picture, a few small pumpkins "
           "and autumn leaves around it, two little bats flying near the moon.",
    "csontvaz": "A friendly, goofy cartoon skeleton boy (cute, round head, big smile, clearly "
                "a kid-friendly character, not creepy) sitting at a small school desk in the "
                "bottom half of the picture, scratching his head over an open math notebook "
                "and a pencil, a small glowing pumpkin on the desk.",
    "macskak": "Exactly THREE flying witch broomsticks, one above the other diagonally across "
               "the middle and lower part of the picture, and on EACH broomstick sit EXACTLY "
               "FOUR small cute black kittens in a row (so 12 kittens in total, count them "
               "carefully: 4 + 4 + 4), each kitten with big yellow eyes, no witch, no other "
               "animals.",
}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--csak", default="")
    p.add_argument("--ujra", action="store_true")
    p.add_argument("--minoseg", default="high", choices=["low", "medium", "high"])
    a = p.parse_args()
    kulcs = os.environ.get("OPENAI_API_KEY")
    if not kulcs:
        print('Nincs OPENAI_API_KEY. Windowsban: setx OPENAI_API_KEY "ide-a-sajat-kulcsod" – és új ablak.')
        return 1
    from openai import OpenAI
    kliens = OpenAI(api_key=kulcs)
    csak = {x.strip() for x in a.csak.split(",") if x.strip()}
    os.makedirs(MAPPA, exist_ok=True)
    for nev, leiras in KEPEK.items():
        if csak and nev not in csak:
            continue
        ki = os.path.join(MAPPA, nev + ".png")
        if os.path.exists(ki) and not a.ujra:
            print("   megvan:", nev)
            continue
        print(f"{nev} …", flush=True)
        try:
            v = fk._hivas(kliens.images.generate, model=fk.MODELL, size="1024x1536", n=1,
                          quality=a.minoseg, prompt=f"{leiras} {STILUS}")
            with open(ki, "wb") as f:
                f.write(fk._kep_bajt(v))
            print("   OK")
        except Exception as e:
            print(f"   ! nem sikerült: {type(e).__name__}: {str(e)[:200]}")
            time.sleep(2)
    print("\nKész. Szólj Claude-nak: ráteszi a szöveget, és Facebook-méretre vágja.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
