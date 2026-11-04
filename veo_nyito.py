"""ÉLETRE KELŐ NYITÓKÉP a Reels-hirdetéshez – Google Veo 3.1 Fast (Gemini API).

Az erdei zsiráfos képből 8 másodperces, 16:9-es, 1080p videót csinál: a zsiráf
pislog és lehajol, a majom lábujjhegyre áll és integet, az állatok a tábla felé
fordulnak. A kamera áll, a tábla ÜRES marad (a „1–8. osztály” feliratot Claude
teszi rá, hogy hibátlan legyen), és a stílus a kép mesekönyves stílusa marad.

ÁR: kb. 0,12 $ / mp → egy 8 mp-es klip kb. 1 $. Csak fizetős Gemini-kulccsal
működik (az ingyenes kerethez a Veo nem jár).

ELŐTTE EGYSZER:
    pip install google-genai
    $env:GEMINI_API_KEY = "ide-a-sajat-kulcsod"

FUTTATÁS (a TutorIA mappában):
    python veo_nyito.py              1 klip  (kb. 1 $)
    python veo_nyito.py --db 2       2 változat, a jobbat választjuk (kb. 2 $)
    python veo_nyito.py --modellek   csak kiírja, melyik Veo modelleket éri el a kulcsod (ingyenes)

Eredmény: kinézet képek/facebook/hirdetes/veo_nyito_<n>.mp4
"""
import argparse
import os
import sys
import time

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

GYOKER = os.path.dirname(os.path.abspath(__file__))
MAPPA = os.path.join(GYOKER, "kinézet képek", "facebook", "hirdetes")
BEMENET = os.path.join(MAPPA, "veo_bemenet_erdei.png")
# A modell neve változhat – sorban próbáljuk, az első elérhető nyer.
MODELLEK = ["veo-3.1-fast-generate-001", "veo-3.1-fast-generate-preview",
            "veo-3.1-generate-001", "veo-3.1-generate-preview"]

PROMPT = (
    "Bring this hand-painted storybook illustration gently to life. Keep EXACTLY the same picture, "
    "characters, colors and the soft gouache-and-watercolor picture-book style with visible paper texture. "
    "The tall giraffe slowly blinks, smiles and lowers its head a little closer to the chalkboard with "
    "curiosity. The little monkey standing on the stack of books rises on tiptoe, peeks at the board and "
    "gives a small happy wave. The fox, the owl, the bear cub, the rabbit and the hedgehog sitting on the "
    "tree stumps turn their heads toward the board with delight; the owl blinks; the rabbit's ears twitch. "
    "The lantern on the branch flickers softly, a few fireflies drift, leaves sway in a light evening breeze, "
    "and the first stars twinkle in the violet sky. All movements are subtle, slow, natural and charming. "
    "Static locked-off camera: no zoom, no pan, no camera movement. The chalkboard stays perfectly still and "
    "COMPLETELY EMPTY. No text, no letters, no new characters, no objects appearing.")
NEGATIV = ("text, letters, words, writing on the chalkboard, camera movement, zoom, pan, new characters, "
           "photorealistic, 3D render, cartoon outline change, morphing faces, extra limbs, flicker, blur")


def kulcs():
    for v in ("GEMINI_API_KEY", "GOOGLE_API_KEY", "TANAR_API_KEY"):
        k = (os.environ.get(v) or "").strip().strip("'\"")
        if k and not k.startswith("sk-"):
            return k
    return ""


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--db", type=int, default=1, help="hány változat (mindegyik kb. 1 $)")
    p.add_argument("--modellek", action="store_true", help="csak listázza az elérhető Veo modelleket")
    a = p.parse_args()
    k = kulcs()
    if not k:
        print('Nincs Gemini-kulcs. PowerShellben: $env:GEMINI_API_KEY = "ide-a-sajat-kulcsod"')
        print("A kulcs itt van: https://aistudio.google.com/apikey")
        return 1
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        print("Hiányzik a csomag. Futtasd:  pip install google-genai")
        return 1
    kliens = genai.Client(api_key=k)

    # A modell-lista nem mindig mutatja a Veót, ezért nem csak arra hagyatkozunk:
    # ha a listában nincs, sorban MEGPRÓBÁLJUK a neveket (a rossz név azonnal,
    # ingyen hibát ad).
    try:
        osszes = [m.name.split("/")[-1] for m in kliens.models.list()]
    except Exception as e:
        print("Nem sikerült lekérni a modelleket:", type(e).__name__, str(e)[:300])
        osszes = []
    elerheto = [m for m in osszes if "veo" in m.lower()]
    if a.modellek:
        print("Elérhető Veo modellek a listában:", ", ".join(elerheto) or "a lista nem mutat Veót")
        print("Összes modell száma a listában:", len(osszes))
        return 0
    jeloltek = [m for m in MODELLEK if m in elerheto] + [m for m in elerheto if m not in MODELLEK] + \
               [m for m in MODELLEK if m not in elerheto]
    if not os.path.exists(BEMENET):
        print("Nem találom a képet:", BEMENET)
        return 1
    with open(BEMENET, "rb") as f:
        kep = types.Image(image_bytes=f.read(), mime_type="image/png")

    def indit(modell):
        return kliens.models.generate_videos(
            model=modell, prompt=PROMPT, image=kep,
            config=types.GenerateVideosConfig(aspect_ratio="16:9", resolution="1080p",
                                              duration_seconds=8, negative_prompt=NEGATIV,
                                              number_of_videos=1))

    modell = None
    for n in range(1, a.db + 1):
        ki = os.path.join(MAPPA, f"veo_nyito_{n}.mp4")
        print(f"\n{n}. változat készül… (1–3 perc)", flush=True)
        op = None
        for m in ([modell] if modell else jeloltek):
            try:
                op = indit(m)
                modell = m
                print("   modell:", m, flush=True)
                break
            except Exception as e:
                uz = str(e)
                print(f"   – {m}: {type(e).__name__}: {uz[:220]}")
                if "404" not in uz and "not found" not in uz.lower() and "not supported" not in uz.lower():
                    break
        if op is None:
            print("   ! egyik Veo modellt sem sikerült elindítani – küldd el Claude-nak a fenti sorokat.")
            return 1
        try:
            while not op.done:
                time.sleep(10)
                print("   …", flush=True)
                op = kliens.operations.get(op)
            if getattr(op, "error", None):
                print("   ! hiba:", op.error)
                continue
            vids = (op.response.generated_videos if op.response else None) or []
            if not vids:
                print("   ! nem jött videó (lehet, hogy a szűrő elutasította).")
                continue
            kliens.files.download(file=vids[0].video)
            vids[0].video.save(ki)
            print("   OK →", ki)
        except Exception as e:
            print(f"   ! nem sikerült: {type(e).__name__}: {str(e)[:400]}")
    print("\nKész. Szólj Claude-nak: beépíti a Reel elejére, ráteszi a feliratot és a krétát.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
