"""AVATAR-MINTÁK a nagyobbaknak (10–14 év) – 3 figura × 2 stílus = 6 kép.

Futtatás a TutorIA mappában:
    python avatar_minta.py
Egyet újra (ha nem tetszik):
    python avatar_minta.py --csak curie --ujra

Eredmény: kinézet képek/avatar_minta/<figura>_<stílus>.png  (1024x1024)
Kb. 0,4–0,6 $ (medium minőség). Ha a stílus eldőlt, a teljes 24-es sor jön.
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

MAPPA = os.path.join(fk.GYOKER, "kinézet képek", "avatar_minta")

# KÖZÖS: kerek profilkép, a fej és a váll látszik, a háttér egy színes korong.
# Kifejezetten NEM óvodás: 10–14 éveseknek, akik a cukit már cikinek tartják.
ALAP = ("Round profile avatar for a learning app for 10–14 year olds: head and shoulders, centered, "
        "facing slightly to the side with a confident friendly expression, on a single solid colored "
        "circle background that fills the square. Cool and age-appropriate, NOT babyish, NOT cute-chibi. "
        "No text, no letters, no numbers, no logos, no brand marks, no watermark, no frame.")

STILUSOK = {
    # A) mint a tudáskártyák: festett, meleg, részletes
    "festett": ("Style: premium hand-painted digital illustration like a collectible trading card portrait, "
                "soft painterly brushwork, warm rim light, rich but harmonious colors, detailed and polished."),
    # B) modern matrica: tiszta vonal, lapos színek, erős formák – mint egy menő játék profilképe
    "matrica": ("Style: modern bold flat vector sticker illustration, clean thick outlines, flat colors with "
                "one soft shadow tone, strong simple shapes, like a stylish video game profile icon."),
}

FIGURAK = {
    # Nagy nevek (az albumból) – a kártya megszerzésekor nyílna meg
    "curie": ("Subject: a young Marie Curie as a scientist, dark hair in a simple updo, dark late-1800s "
              "dress with a white collar, holding a small glowing green-blue test tube, lab glassware softly "
              "in the background. Background circle: deep teal."),
    # Sport – kitalált focista, valódi játékos, klub, mez-felirat NÉLKÜL
    "focista": ("Subject: an original fictional teenage football player boy, short fade haircut, plain "
                "red-and-white striped jersey with NO crest, NO sponsor, NO number, a football under his arm, "
                "determined grin. Background circle: bright green like a pitch."),
    # Saját hős – nem létező szuperhős, semmi Marvel/DC
    "villam": ("Subject: an original superhero girl called 'Lightning' (no text on image): sleek purple and "
               "gold suit with a simple lightning-bolt shape on the chest, short cape, a small eye mask, "
               "tiny electric sparks around her raised hand, windswept hair. Completely original design, not "
               "resembling any existing comic character. Background circle: midnight blue."),
}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--csak", default="", help="figura neve(i), vesszővel: curie,focista,villam")
    p.add_argument("--ujra", action="store_true")
    p.add_argument("--minoseg", default="medium", choices=["low", "medium", "high"])
    a = p.parse_args()
    kulcs = os.environ.get("OPENAI_API_KEY")
    if not kulcs:
        print('Nincs OPENAI_API_KEY. Windowsban: setx OPENAI_API_KEY "ide-a-sajat-kulcsod" – és új ablak.')
        return 1
    from openai import OpenAI
    kliens = OpenAI(api_key=kulcs)
    csak = {x.strip() for x in a.csak.split(",") if x.strip()}
    os.makedirs(MAPPA, exist_ok=True)
    for nev, figura in FIGURAK.items():
        if csak and nev not in csak:
            continue
        for stilus, leiras in STILUSOK.items():
            ki = os.path.join(MAPPA, f"{nev}_{stilus}.png")
            if os.path.exists(ki) and not a.ujra:
                print("   megvan:", nev, stilus)
                continue
            print(f"{nev} – {stilus} …", flush=True)
            try:
                v = fk._hivas(kliens.images.generate, model=fk.MODELL, size="1024x1024", n=1,
                              quality=a.minoseg, prompt=f"{figura} {leiras} {ALAP}")
                with open(ki, "wb") as f:
                    f.write(fk._kep_bajt(v))
                print("   OK")
            except Exception as e:
                print(f"   ! nem sikerült: {type(e).__name__}: {str(e)[:200]}")
                time.sleep(2)
    print("\nKész. Szólj Claude-nak, vagy küldd el a képeket.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
