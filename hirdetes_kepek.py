"""Facebook-hirdetés RAJZAI – a „zsiráf és majom" kép stílusában, szöveg NÉLKÜL.
(A szöveget Claude teszi rá, mert a képgenerátor elrontja a betűket.)
3 kép, kb. 0,5 $ (high minőség).

Futtatás a TutorIA mappában:
    python hirdetes_kepek.py
Egyet újra (ha nem tetszik):
    python hirdetes_kepek.py --csak bagoly --ujra
Világos, színes változat (a feketék megmaradnak):
    python hirdetes_kepek.py --szines

Eredmény: kinézet képek/facebook/hirdetes/<név>.png  (1024x1024, négyzet)
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

MAPPA = os.path.join(fk.GYOKER, "kinézet képek", "facebook", "hirdetes")

# A minta (Sándor képe, 2026-10-30): fekete háttér, rajta halvány csillagpöttyök,
# fehér krétás / tollas KÖRVONALAS rajz, a figurák belseje halvány szürkés
# akvarell-lavírozás. Egyszerű, kedves, de NEM gyerekes rajzfilm.
STILUS = (
    "Hand-drawn illustration on a pure black background with a few faint tiny white "
    "specks like stars. Clean confident WHITE ink outline drawing, like white gel pen "
    "or chalk on black paper, with soft muted grey watercolor wash inside the shapes "
    "(very limited palette: black, white, soft greys, at most one small touch of warm "
    "ochre). Cute, friendly, expressive cartoon animals with big eyes, simple and "
    "elegant, lots of empty black space. Leave the TOP fifth and the BOTTOM fifth of "
    "the picture completely empty black (text will be placed there). Absolutely no "
    "text, no letters, no numbers, no speech bubbles, no watermark, no logo, no frame.")

# SZÍNES változat (--szines): a fekete helyett a TutorIA saját világa – meleg,
# világos, mesekönyves, mint a főoldal bézs háttere és a rajzai.
STILUS_SZINES = (
    "Premium children's picture-book illustration, warm painterly digital art with soft "
    "natural light, rich but gentle colours, friendly expressive cartoon animals with big "
    "eyes, on a warm light cream / beige paper background (#FBF5EA) with a subtle paper "
    "texture and a soft ground shadow, simple and elegant with lots of calm empty space. "
    "Leave the TOP fifth and the BOTTOM fifth of the picture empty cream background (text "
    "will be placed there). Absolutely no text, no letters, no numbers, no speech bubbles, "
    "no watermark, no logo, no frame.")

KEPEK = {
    # „Ugyanaz a tábla – más magasság." Mindenkinek máshonnan kell elmagyarázni.
    "tabla": "A small school chalkboard on legs standing in the middle. A tall friendly "
             "giraffe stands on the left and easily looks at the board from above. On the "
             "right a small monkey stands on tiptoe on top of a wobbly stack of three thick "
             "books to be able to see the same board. Both look at the board, curious. "
             "Whole figures visible, centered in the middle three fifths of the picture.",
    # „Tizedszer is elmondod?" – „Ahányszor csak kell." A türelem nem fogy el.
    "bagoly": "A wise kind owl teacher with round glasses sits on a branch next to a small "
              "fox cub who holds an open exercise book and looks a bit unsure. A small desk "
              "lamp on the branch gives a warm ochre glow on both of them. The owl leans "
              "toward the fox patiently, smiling. Whole figures visible, centered in the "
              "middle three fifths of the picture.",
    # „Én már kész vagyok!" – „Én meg értem is." Nem a gyorsaság a lényeg.
    "teknos": "A finish line ribbon on the right. A rabbit has already crossed it and "
              "stands there proudly, but looks a little confused. On the left a calm smiling "
              "turtle walks steadily towards the finish wearing a tiny school backpack, with "
              "a small glowing lightbulb floating above its head. Whole figures visible, "
              "centered in the middle three fifths of the picture.",
}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--csak", default="")
    p.add_argument("--ujra", action="store_true")
    p.add_argument("--minoseg", default="high", choices=["low", "medium", "high"])
    p.add_argument("--szines", action="store_true", help="világos, színes változat (<név>_szines.png)")
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
        ki = os.path.join(MAPPA, nev + ("_szines" if a.szines else "") + ".png")
        if os.path.exists(ki) and not a.ujra:
            print("   megvan:", nev)
            continue
        print(f"{nev} …", flush=True)
        try:
            v = fk._hivas(kliens.images.generate, model=fk.MODELL, size="1024x1024", n=1,
                          quality=a.minoseg, prompt=f"{leiras} {STILUS_SZINES if a.szines else STILUS}")
            with open(ki, "wb") as f:
                f.write(fk._kep_bajt(v))
            print("   OK")
        except Exception as e:
            print(f"   ! nem sikerült: {type(e).__name__}: {str(e)[:200]}")
            time.sleep(2)
    print("\nKész. Szólj Claude-nak: ráteszi a szöveget.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
