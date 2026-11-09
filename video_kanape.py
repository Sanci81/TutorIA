"""KANAPÉS JELENET a reklámvideóhoz (2026-11-08) – két lépésben.

A videó története (15 mp): „Este 7. Te főzöl. Ő tanul – egyedül.” → a TutorIA
képernyője → a szülő a kanapén, megjön az e-mail („Leila ma 15 percet tanult”)
→ logó, „120 perc ingyen”. Ebből EZ a fájl a kanapés, mozgó jelenetet készíti.
A szereplők a hirdetés mesekönyves állatai (nem valódi emberek).

1. LÉPÉS – a kép (OpenAI, kb. 0,2 $):
    python video_kanape.py kep
    → kinézet képek/facebook/hirdetes/kanape_jelenet.png   (nézd meg; ha nem tetszik:
      python video_kanape.py kep --ujra)

2. LÉPÉS – életre keltés (Gemini, 720p, 8 mp, kb. 0,9 $):
    python video_kanape.py video
    → kinézet képek/facebook/hirdetes/kanape_video.mp4

ELŐTTE (ugyanúgy, mint a nyitóképnél):
    pip install -U google-genai openai
    $env:OPENAI_API_KEY = "ide-a-sajat-kulcsod"
    $env:GEMINI_API_KEY = "ide-a-sajat-kulcsod"

EMBERES VÁLTOZAT (2026-11-09, Sándor kérte – a mackós marad, ez külön):
    python video_kanape.py kep --emberek --ujra   → kanape_jelenet_emberek.png (új kép)
    python video_kanape.py video --emberek   → kanape_video_emberek.mp4
    Ugyanaz a mesekönyves festett stílus, de anyuka és a kislánya (nem fotószerű:
    valódinak tűnő gyerek-arcot nem készítünk, és így nem kell „AI-kép” címke sem).

3. VÁLTOZAT (2026-11-09, Sándor: „a régi, mobilozós kép a jó, csak a módosításokkal”):
    python video_kanape.py javit      → a RÉGI képet (kanape_jelenet_emberek_regi.png) javítja:
                                         könyv a kezében, telefon mellette, gőz nincs a konyhában
                                         → kanape_jelenet_v3.png   (kb. 0,25 $)
    ELŐBB SZÓLJ CLAUDE-NAK, megnézi a képet – csak ha jó:
    python video_kanape.py video --v3 → kanape_video_v3.mp4      (kb. 0,9 $)

Utána szólj Claude-nak: összerakja a videót (felirat, értesítés, képernyő, logó).
"""
import argparse
import base64
import os
import sys
import time

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

GYOKER = os.path.dirname(os.path.abspath(__file__))
MAPPA = os.path.join(GYOKER, "kinézet képek", "facebook", "hirdetes")
BEMENET = os.path.join(MAPPA, "kanape_jelenet.png")
# A modell neve változhat – sorban próbáljuk, az első elérhető nyer.
MODELL = "gemini-omni-1.1-flash"

KEP_PROMPT = (
    "Hand-painted children's picture-book illustration in gouache and transparent watercolor with "
    "delicate, slightly uneven visible pencil linework, on textured cotton watercolor paper. Soft, warm "
    "evening light from a table lamp, harmonious gentle palette, fine hand-made detail. NOT digital 3D, "
    "no glossy plastic look. Wide 3:2 composition. "
    "Scene: a cozy family living room in the evening. In the LOWER RIGHT, a kind, relaxed mother bear "
    "sits curled up on a soft sofa with a knitted blanket and a cup of tea, smiling while she looks at "
    "her phone, whose screen glows softly. In the LEFT background, through a wide open doorway, the warm "
    "kitchen is visible: a small friendly monkey child sits at the kitchen table and happily learns on a "
    "tablet that glows. A pot simmers on the stove behind it. Bookshelves, a potted plant, a rug. "
    "The TOP quarter of the image is calm, simple wall and ceiling with no strong details (text goes "
    "there). Absolutely no text, no letters, no numbers, no logos, no watermark, no frame.")

PROMPT = (
    "Bring this hand-painted storybook illustration gently to life. Keep EXACTLY the same picture, "
    "characters, colors and the soft gouache-and-watercolor picture-book style with visible paper texture. "
    "The mother bear on the sofa looks at her glowing phone, reads, then smiles warmly and relaxes back "
    "into the cushions with a contented sigh; she sips her tea. In the kitchen in the background the "
    "little monkey taps the glowing tablet, nods and does a tiny happy wiggle. Steam rises softly from the "
    "tea cup and the pot; the lamp light flickers gently. All movements are subtle, slow and natural. "
    "Static locked-off camera: no zoom, no pan. The clip is 8 seconds: [0-3s] the phone lights up and the "
    "bear looks at it, [3-6s] she smiles and leans back, [6-8s] calm and cozy. Keep it hand-painted, not "
    "photorealistic, not 3D. No text, no letters, no writing on any screen, no new characters, no "
    "morphing faces. No dialogue, no music, only quiet evening room ambience.")


VIDEO_NEV = "kanape_video"
# 2. változat (2026-11-09, Sándor): az anyuka KÖNYVET olvas, teával; a telefon mellette
# fekszik, felvillan → leteszi a könyvet, felveszi a telefont, elolvassa, mosolyog.
# A kislány mellett SEMMI ne gőzölögjön (az előzőn a tablet mellett gőz szállt fel).
KEP_PROMPT_EMBER = (
    "Hand-painted children's picture-book illustration in gouache and transparent watercolor with "
    "delicate, slightly uneven visible pencil linework, on textured cotton watercolor paper. Soft, warm "
    "evening light from a table lamp, harmonious gentle palette. NOT digital 3D, NOT photorealistic. "
    "Wide 3:2 composition. Scene: a cozy family living room in the evening. In the LOWER RIGHT, a kind, "
    "relaxed young mother (about 35, casual home clothes) sits curled up on a soft sofa under a knitted "
    "blanket. She is reading an open paperback book held in her LEFT hand and holds a mug of tea in her "
    "RIGHT hand. Her smartphone lies face-up on the sofa cushion right beside her, screen dark. In the "
    "LEFT background, through a wide open doorway, the tidy kitchen is visible: her daughter, a cheerful "
    "girl of about nine, sits at the kitchen table and learns on a tablet whose screen glows softly. "
    "Nothing on the kitchen table except the tablet; the stove is off; there is NO steam, NO smoke and "
    "NO cups anywhere in the kitchen. Bookshelves, a potted plant, a rug. People drawn in a simple "
    "storybook style with soft, stylized faces. The TOP quarter of the image is calm, simple wall and "
    "ceiling with no strong details (text goes there). Absolutely no text, no letters, no numbers, no "
    "logos, no watermark, no frame.")
PROMPT_EMBER = (
    "Bring this hand-painted storybook illustration gently to life. Keep EXACTLY the same picture, "
    "characters, colors and the soft gouache-and-watercolor picture-book style with visible paper texture. "
    "Static locked-off camera: no zoom, no pan. The clip is 8 seconds: "
    "[0-2s] the mother calmly reads her book and takes a small sip of tea. "
    "[2-4s] the phone lying on the sofa beside her lights up softly; she notices it. "
    "[4-6s] she lowers the book onto her lap, picks up the phone with that free hand and looks at the "
    "screen; she keeps holding the tea mug in her other hand the whole time. "
    "[6-8s] she reads the phone and smiles warmly, relaxed. "
    "Meanwhile in the kitchen in the background the girl keeps tapping the glowing tablet and nods "
    "happily. Only a faint wisp of steam from the mother's mug; NO steam or smoke in the kitchen, nothing "
    "steaming near the girl. All movements subtle, slow and natural. Keep it hand-painted, not "
    "photorealistic, not 3D. No text, no letters, no writing on any screen, no new characters, no "
    "morphing faces or hands. No dialogue, no music, only quiet evening room ambience.")


REGI_KEP = os.path.join(MAPPA, "kanape_jelenet_emberek_regi.png")
V3_KEP = os.path.join(MAPPA, "kanape_jelenet_v3.png")
JAVIT_PROMPT = (
    "Edit this hand-painted storybook illustration. Keep EVERYTHING else exactly the same: the style, "
    "paper texture, colors, light, composition, the room, the kitchen, the girl, the sofa, the lamp and "
    "the mother's face, hair and clothes. Make ONLY these changes: "
    "1) The mother now holds an open paperback book in her LEFT hand (instead of the phone) and is "
    "reading it. "
    "2) Her smartphone lies face-up on the sofa cushion right beside her, its screen dark. "
    "3) She keeps holding the SAME single tea mug in her RIGHT hand – there is exactly ONE mug in the "
    "whole picture on the sofa side. "
    "4) Remove ALL steam in the kitchen: no steam above the pot, no steam near the girl. The pot has its "
    "lid on. Nothing steams anywhere near the girl. "
    "No text, no letters, no logos.")
PROMPT_V3 = (
    # Bal/jobb kéz NINCS a szövegben: a képen a könyv a néző felőli bal oldalon, a bögre a jobb
    # oldalon van – a „left/right hand” összezavarná a modellt (előző videón két bögre lett).
    "Bring this hand-painted storybook illustration gently to life. Keep EXACTLY the same picture, "
    "characters, colors and the soft gouache-and-watercolor picture-book style with visible paper texture. "
    "Static locked-off camera: no zoom, no pan. "
    "IMPORTANT: the mother has exactly ONE tea mug. The hand that holds the mug keeps holding that same "
    "mug for the whole clip; the mug never moves to the other hand and no second mug ever appears. "
    "The clip is 8 seconds: "
    "[0-2s] she calmly reads the book and takes a small sip from the mug. "
    "[2-4s] the phone lying on the sofa cushion beside her lights up softly; she glances down at it. "
    "[4-6s] she lays the open book down on her lap with the hand that was holding it, and with that same "
    "free hand she picks up the glowing phone and looks at the screen. The mug stays in its hand. "
    "[6-8s] she reads the phone and smiles warmly, relaxed. "
    "In the kitchen in the background the girl keeps tapping the glowing tablet and smiles. "
    "NO steam or smoke in the kitchen, the pot keeps its lid on and does not steam, nothing steams near "
    "the girl; only a faint wisp of steam from the mother's mug. All movements subtle, slow and natural. "
    "Keep it hand-painted, not photorealistic, not 3D. No text, no writing on any screen, no new "
    "characters or objects, no morphing faces or hands. No dialogue, no music, only quiet evening room "
    "ambience.")


def javit() -> int:
    """3. változat képe: a RÉGI (jó) képet javítja, nem újat rajzol."""
    if not os.path.exists(REGI_KEP):
        print("Nincs meg a régi kép:", REGI_KEP)
        return 1
    k = os.environ.get("OPENAI_API_KEY")
    if not k:
        print('Nincs OPENAI_API_KEY. PowerShellben: $env:OPENAI_API_KEY = "ide-a-sajat-kulcsod"')
        return 1
    import figura_kepek as fk
    from openai import OpenAI
    print("Kép javítása… (kb. 1 perc)", flush=True)
    try:
        with open(REGI_KEP, "rb") as kep:
            v = fk._hivas(OpenAI(api_key=k).images.edit, model=fk.MODELL, image=kep, size="1536x1024",
                          prompt=JAVIT_PROMPT, input_fidelity="high", quality="high")
        with open(V3_KEP, "wb") as f:
            f.write(fk._kep_bajt(v))
        print("OK →", V3_KEP, "\nSzólj Claude-nak, megnézi. Csak utána: python video_kanape.py video --v3")
        return 0
    except Exception as e:
        print(f"! nem sikerült: {type(e).__name__}: {str(e)[:300]}")
        return 1


def emberes():
    """--emberek: ugyanaz a jelenet emberekkel, KÜLÖN fájlokba (a mackós megmarad)."""
    global BEMENET, KEP_PROMPT, PROMPT, VIDEO_NEV
    if "--v3" in sys.argv:
        sys.argv.remove("--v3")
        BEMENET, PROMPT, VIDEO_NEV = V3_KEP, PROMPT_V3, "kanape_video_v3"
        return
    if "--emberek" in sys.argv:
        sys.argv.remove("--emberek")
        BEMENET = os.path.join(MAPPA, "kanape_jelenet_emberek.png")
        KEP_PROMPT, PROMPT, VIDEO_NEV = KEP_PROMPT_EMBER, PROMPT_EMBER, "kanape_video_emberek"


def kulcs():
    for v in ("GEMINI_API_KEY", "GOOGLE_API_KEY", "TANAR_API_KEY"):
        k = (os.environ.get(v) or "").strip().strip("'\"")
        if k and not k.startswith("sk-"):
            return k
    return ""


def kep_keszit(ujra: bool) -> int:
    """1. lépés: a kanapés kép OpenAI-jal (ugyanaz a modell, mint a hirdetés képeinél)."""
    if os.path.exists(BEMENET) and not ujra:
        print("A kép már megvan:", BEMENET, "(újra: --ujra)")
        return 0
    k = os.environ.get("OPENAI_API_KEY")
    if not k:
        print('Nincs OPENAI_API_KEY. PowerShellben: $env:OPENAI_API_KEY = "ide-a-sajat-kulcsod"')
        return 1
    import figura_kepek as fk
    from openai import OpenAI
    os.makedirs(MAPPA, exist_ok=True)
    print("Kép készül… (kb. 1 perc)", flush=True)
    try:
        v = fk._hivas(OpenAI(api_key=k).images.generate, model=fk.MODELL, size="1536x1024", n=1,
                      quality="high", prompt=KEP_PROMPT)
        with open(BEMENET, "wb") as f:
            f.write(fk._kep_bajt(v))
        print("OK →", BEMENET, "\nNézd meg. Ha jó: python video_kanape.py video")
        return 0
    except Exception as e:
        print(f"! nem sikerült: {type(e).__name__}: {str(e)[:300]}")
        return 1


def main():
    emberes()
    if len(sys.argv) > 1 and sys.argv[1] == "javit":
        return javit()
    if len(sys.argv) > 1 and sys.argv[1] == "kep":
        return kep_keszit("--ujra" in sys.argv)
    if len(sys.argv) > 1 and sys.argv[1] == "video":
        sys.argv.pop(1)
    else:
        print(__doc__)
        return 0
    p = argparse.ArgumentParser()
    p.add_argument("--db", type=int, default=1, help="hány változat (mindegyik kb. 0,9 $)")
    p.add_argument("--felbontas", default="720p", choices=["720p", "1080p"],
                   help="720p elég (a Reelben 1080 széles sávban áll); az 1080p csak felskálázott")
    a = p.parse_args()
    k = kulcs()
    if not k:
        print('Nincs Gemini-kulcs. PowerShellben: $env:GEMINI_API_KEY = "ide-a-sajat-kulcsod"')
        return 1
    try:
        from google import genai
    except ImportError:
        print("Hiányzik a csomag. Futtasd:  pip install -U google-genai")
        return 1
    from google.genai import types
    try:
        from importlib.metadata import version
        print("google-genai:", version("google-genai"))
    except Exception:
        pass
    # 2026-11-04: „JSONDecodeError” – a videó készítése perceken át tart, és az
    # alap időkorlát hamarabb lejárt (üres válasz jött). A Google saját mintája
    # 600–900 mp-es korlátot ad meg, ezredmásodpercben.
    kliens = genai.Client(api_key=k, http_options=types.HttpOptions(timeout=900 * 1000))
    if not hasattr(kliens, "interactions"):
        print("Régi a google-genai csomag (2.19 vagy újabb kell). Futtasd:  pip install -U google-genai")
        return 1
    if not os.path.exists(BEMENET):
        print("Nem találom a képet:", BEMENET)
        return 1
    # A képet a Google saját mintája szerint FELTÖLTJÜK (Files API), nem a
    # kérésbe ágyazzuk: a 2,4 MB-os kép base64-ben túl nagy volt.
    print("Kép feltöltése…", flush=True)
    try:
        feltoltott = kliens.files.upload(file=BEMENET, config={"mime_type": "image/png"})
        while getattr(feltoltott.state, "name", str(feltoltott.state)) == "PROCESSING":
            time.sleep(2)
            feltoltott = kliens.files.get(name=feltoltott.name)
    except Exception as e:
        print(f"   ! a kép feltöltése nem sikerült: {type(e).__name__}: {str(e)[:400]}")
        return 1
    kep_resz = {"type": "image", "uri": feltoltott.uri, "mime_type": "image/png"}

    for n in range(1, a.db + 1):
        ki = os.path.join(MAPPA, f"{VIDEO_NEV}.mp4" if n == 1 else f"{VIDEO_NEV}_{n}.mp4")
        print(f"\n{n}. változat készül… (1–3 perc, ne zárd be)", flush=True)
        try:
            # HÁTTÉRBEN indítjuk (background), és 10 mp-enként rákérdezünk: így nem
            # tud lejárni az időkorlát, amíg a Google perceken át készíti a videót.
            inter = kliens.interactions.create(
                model=MODELL,
                input=[kep_resz, {"type": "text", "text": PROMPT}],
                response_format={"type": "video", "aspect_ratio": "16:9", "duration": "8s",
                                 "resolution": a.felbontas, "delivery": "uri"},
                generation_config={"video_config": {"task": "image_to_video"}},
                background=True,
            )
            print("   elindult, azonosító:", getattr(inter, "id", "?"), flush=True)
            kezd = time.time()
            while str(getattr(inter, "status", "")) in ("in_progress", "queued", "requires_continuation") \
                    and time.time() - kezd < 1500:
                time.sleep(10)
                print(f"   … {int(time.time() - kezd)} mp", flush=True)
                inter = kliens.interactions.get(inter.id)
            allapot = str(getattr(inter, "status", ""))
            if allapot != "completed":
                print("   ! nem készült el. Állapot:", allapot, "| hiba:", str(getattr(inter, "errors", ""))[:500])
                continue
            ov = getattr(inter, "output_video", None)
            if ov is None:
                print("   ! nem jött videó (lehet, hogy a szűrő elutasította):", str(inter)[:500])
                continue
            if getattr(ov, "data", None):
                with open(ki, "wb") as f:
                    f.write(base64.b64decode(ov.data))
            else:
                nev = "files/" + ov.uri.split("/")[-1].split("?")[0].split(":")[0]
                for _ in range(120):
                    try:
                        info = kliens.files.get(name=nev)
                        if getattr(info.state, "name", str(info.state)) != "PROCESSING":
                            break
                    except Exception:
                        break
                    time.sleep(5)
                adat = kliens.files.download(file=ov.uri)
                with open(ki, "wb") as f:
                    f.write(adat)
            print("   OK →", ki)
        except Exception as e:
            import traceback
            print(f"   ! nem sikerült: {type(e).__name__}: {str(e)[:500]}")
            print("   részletek (ezt küldd el Claude-nak):")
            print("   " + " | ".join(traceback.format_exc().strip().splitlines()[-6:])[:1500])
    print("\nKész. Szólj Claude-nak: összerakja a videót (felirat, értesítés, képernyő, logó).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
