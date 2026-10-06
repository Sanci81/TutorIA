# -*- coding: utf-8 -*-
"""TutorIA – KÉPES SZÓTÁR: a nyelvórák szavainak képei, egy közös stílusban.

MIT CSINÁL
    Az alsós nyelvi tanterv (angol_1-4, nemet_1-4, spanyol_1-4) szavaiból
    – ezek témakörönként, sorban EGYMÁSNAK MEGFELELNEK: apple = Apfel =
    manzana – összeállítja a fogalmak listáját, és mindegyikhez legyárt
    EGY képet. Egy kép szolgál ki mindhárom nyelvet.

    Csak a lerajzolható szavak kapnak képet (alma, kutya, esik az eső…).
    A köszönések, kérdések, elvont szavak nem – azok listája lent, az
    ALANY szótárban látszik: ami nincs benne, az nem kap képet.

MIT NEM CSINÁL
    NEM ír a static/kartyak mappába, és a static/szokepek mappába is
    CSAK akkor, ha te jóváhagytad a képet (--jovahagy). Előbb minden a
    szokep_uj mappába kerül, ott nézed át.

HASZNÁLAT
    python szokep_generalas.py --lista
        Kiírja, melyik szóhoz milyen képet kérne. NEM hív API-t, ingyenes.

    python szokep_generalas.py --db 5
        Öt képet gyárt próbának. Nézd meg, tetszik-e a stílus.

    python szokep_generalas.py
        Legyártja az összes hiányzó képet (kb. 176 db).

    Utána nyisd meg: szokep_uj/attekinto.html
        Pipáld ki, ami JÓ, és a lap alján lévő gomb kiírja a parancsot,
        amit be kell másolnod. Például:
    python szokep_generalas.py --jovahagy apple,cat,dog
        A jóváhagyott képek kicsinyítve (512 px, webp) a static/szokepek/nyelv
        mappába kerülnek, és az ottani szokepek.json listába.

    python szokep_generalas.py --csak apple --ujra
        Egyetlen képet csinál újra (ha nem tetszett).

MI KELL HOZZÁ
    Az OPENAI_API_KEY környezeti változóban a saját kulcsod (ugyanaz, mint a
    kártyaképekhez), és a Pillow csomag (pip install pillow).
"""

from __future__ import annotations

import argparse
import base64
import html
import io
import json
import os
import re
import shutil
import sys
import time

GYOKER = os.path.dirname(os.path.abspath(__file__))
UJ_MAPPA = os.path.join(GYOKER, "szokep_uj")
# TANTÁRGYANKÉNT külön mappa: ez a nyelvórák képes szótára. A többi tárgy
# képei majd a saját mappájukba kerülnek (static/szokepek/kornyezet, …).
VEGLEGES = os.path.join(GYOKER, "static", "szokepek", "nyelv")
TANTERV = os.path.join(GYOKER, "hu_kerettanterv_1_4_TELJES", "hu_kerettanterv_1_4_TELJES")
NYELVEK = {"en": "angol_1-4.json", "de": "nemet_1-4.json", "es": "spanyol_1-4.json"}

# Ugyanaz a modell, mint a kártyaképeknél. Ha a fiókodon más érhető el,
# EZT az egy sort kell átírni.
MODELL = "gpt-image-2"
MERET = "1024x1024"

# ── A KÖZÖS STÍLUS ─────────────────────────────────────────────────────
# Képes szótár egy 6–10 éves gyereknek: egyetlen, azonnal felismerhető
# tárgy vagy jelenet, a főoldal színeihez illő meleg, tiszta rajz. Ha a
# stílust változtatod, az egészet újra kell generálni – a félig régi,
# félig új szótár rosszabb, mint bármelyik önmagában.
STILUS = (
    "simple friendly illustration for a children's picture dictionary, "
    "flat vector style with soft rounded shapes and clean dark outlines, "
    "warm cheerful colours, one single clearly recognisable subject in the "
    "centre, plain cream background (#FBF5EA), generous empty margin around "
    "the subject, square composition"
)
TILTAS = (
    "No text, no letters, no numbers written anywhere, no words, no captions, "
    "no watermark, no logo, no border, no frame. Not a photograph, not "
    "photorealistic, not 3D render, no scary or dark elements, no brand "
    "names, no real recognisable people."
)

# ── MIT RAJZOLJON ──────────────────────────────────────────────────────
# angol szó -> mit rajzoljon (angolul). Ami nincs itt, az nem kap képet
# (köszönések, kérdések, elvont szavak).
ALANY = {
 # számok: megszámolható tárgyak
 "one":"exactly one red apple","two":"exactly two red apples arranged in one row, not overlapping, each apple clearly separate and easy to count","three":"exactly three red apples arranged in one row, not overlapping, each apple clearly separate and easy to count","four":"exactly four red apples arranged in one row, not overlapping, each apple clearly separate and easy to count",
 "five":"exactly five red apples arranged in one row, not overlapping, each apple clearly separate and easy to count","six":"exactly six red apples arranged in two rows of three, not overlapping, each apple clearly separate and easy to count","seven":"exactly seven red apples arranged in a row of four above a row of three, not overlapping, each apple clearly separate and easy to count","eight":"exactly eight red apples arranged in two rows of four, not overlapping, each apple clearly separate and easy to count",
 "nine":"exactly nine red apples arranged in three rows of three, not overlapping, each apple clearly separate and easy to count","ten":"exactly ten red apples arranged in two rows of five, not overlapping, each apple clearly separate and easy to count",
 # színek
 "red":"a big red paint splash","blue":"a big blue paint splash","yellow":"a big yellow paint splash",
 "green":"a big green paint splash","black":"a big black paint splash","white":"a big white paint splash with a thin grey outline",
 "orange":"a big orange paint splash","pink":"a big pink paint splash","brown":"a big brown paint splash",
 # a testem
 "head":"a child's head, the head is highlighted","hand":"an open child's hand","foot":"a child's bare foot seen from the side, standing flat on the ground, toes clearly visible",
 "eye":"one friendly eye","ear":"a child's ear","nose":"a child's nose","mouth":"a smiling mouth",
 "hair":"the back of a child's head with long braided hair and a hair clip, the hair fills most of the picture","arm":"a child's arm flexing",
 # család
 "mum":"a smiling mother","dad":"a smiling father","brother":"a young boy, a brother","sister":"a young girl, a sister",
 "grandma":"a smiling grandmother with glasses","grandpa":"a smiling grandfather with a cap","baby":"a happy baby",
 "family":"a happy family of four standing together","love":"a big red heart",
 # állatok
 "dog":"a friendly dog","cat":"a cat","bird":"a small bird","fish":"a colourful fish","horse":"a horse",
 "cow":"a cow","rabbit":"a rabbit","mouse":"a small mouse","big":"a big elephant next to a tiny mouse",
 # játékok
 "toy":"a pile of toys","ball":"a colourful ball","doll":"a doll","car":"a small toy car","teddy bear":"a teddy bear",
 "game":"a board game with dice","play":"children playing with a ball",
 # étel, ital
 "bread":"a loaf of bread","milk":"a milk carton with a cow picture on it pouring white milk into a glass","water":"a glass of water","apple":"a red apple",
 "banana":"a banana","cheese":"a piece of cheese","egg":"an egg","juice":"an orange cut in half next to a glass of orange juice with a straw, so it is clear the juice is made from the fruit",
 # ruhák
 "T-shirt":"a T-shirt","trousers":"a pair of trousers","shoes":"a pair of shoes","dress":"a dress","hat":"a hat",
 "jacket":"a jacket","socks":"a pair of socks","warm":"a child sitting cosily wrapped in a blanket next to a warm glowing fireplace, holding a cup of hot chocolate",
 # tanterem
 "book":"a book","pencil":"a pencil","bag":"a school bag","desk":"a school desk","chair":"a chair",
 "door":"a door","window":"a window","board":"a green classroom chalkboard",
 "open":"a wooden door standing wide open, seen straight from the front, the hinges are on the door frame and the door handle is on the free outer edge of the door, light coming through the opening","close":"a hand closing a door",
 # számok 11–20 és társai
 "count":"a child counting on fingers","more":"two plates side by side: the left plate has one cookie, the right plate has many cookies, a child's finger points at the plate with many cookies",
 "less":"two glasses side by side: the left glass is full of water, the right glass has only a little water at the bottom, a child's finger points at the glass with little water",
 # időjárás, évszakok
 "sunny":"a bright sun","rainy":"a rainy day: a child in a yellow raincoat with an umbrella walking through puddles while it rains","cloudy":"grey clouds","windy":"a tree bending in the wind",
 "hot":"a hot sun and a thermometer showing heat","cold":"a shivering snowman and a thermometer showing cold",
 "snow":"falling snowflakes","spring":"a spring meadow with flowers","summer":"a sunny summer beach day: blue sea waves, sand, a sandcastle with a bucket, and a bright sun",
 "winter":"a snowy winter landscape","autumn":"a tree with orange autumn leaves","rain":"rain falling from a cloud",
 # iskola
 "school":"a school building","teacher":"a friendly teacher at the board","classroom":"a classroom with desks",
 "lesson":"a lesson in a classroom: a teacher explains at the chalkboard and children sit at desks raising their hands","break":"school break time: children in the school yard eating sandwiches and chatting, a school bell on the wall of the school building",
 "maths":"numbers and a plus sign on a board","music":"musical notes","learn":"a child reading and learning",
 "homework":"a child doing homework at a desk",
 # otthon
 "house":"a house","room":"a child's bedroom interior: a bed, a window, a shelf with toys and a rug on the floor","kitchen":"a kitchen","bathroom":"a small bathroom interior with a bathtub, a washbasin with a mirror and a toilet, seen from the doorway",
 "bed":"a bed","table":"a table","garden":"a family house garden: green lawn, a small wooden fence, a flower bed, a vegetable patch and a watering can, the house wall at the edge",
 "in":"a ball in a box","on":"a ball on a box",
 # étkezések
 "breakfast":"breakfast on a table: cereal and orange juice","lunch":"lunch time at noon: a child at a table eating soup and bread, a bright sun high in the sky seen through the window",
 "dinner":"a family dinner plate at evening","hungry":"a hungry child holding an empty plate",
 "thirsty":"a thirsty child reaching for a glass of water","eat":"a child eating","drink":"a child drinking",
 "plate":"a plate","cup":"a cup","tasty":"a child happily tasting a cake",
 # napirend
 "get up":"a child getting out of bed and stretching","wash":"a child washing their face",
 "go to school":"a child walking to school with a school bag","read":"a child reading a book",
 "sleep":"a child sleeping in bed","morning":"a sunrise in the morning","evening":"an evening sky with the moon",
 # szabadidő
 "football":"a football","swim":"a child swimming","draw":"a child drawing a picture","sing":"a child singing",
 "dance":"a child dancing","ride a bike":"a child riding a bike","together":"two friends holding hands",
 "hobby":"a child painting as a hobby",
 # ünnepek, idő
 "Christmas":"a decorated Christmas tree","Easter":"colourful Easter eggs in a basket",
 "birthday":"a birthday cake with candles","present":"a wrapped present","party":"a party with balloons",
 "card":"an open folded greeting card standing upright, decorated with a big heart and flowers, nothing written on it","celebrate":"children celebrating with confetti",
 
 # város
 "town":"a small town","street":"a street with houses","shop":"a small shop front","park":"a park with trees and a bench",
 "hospital":"a hospital building","bus":"a bus","near":"a house close to a tree","far":"a house far away on a hill",
 # vásárlás
 "money":"coins and banknotes","buy":"a child buying fruit at a market stall","price":"a price tag",
 "expensive":"a price tag with a big price and gold coins","pay":"a hand paying with coins",
 # kedvencek
 "food":"a plate of healthy food","colour":"a colourful paint palette","animal":"a group of animals",
 "song":"a child singing with music notes around","film":"a cinema screen with popcorn",
 # természet
 "tree":"a tree","flower":"a flower","leaf":"a green leaf","river":"a river","mountain":"a mountain",
 "forest":"a forest","grow":"a small plant growing from soil","nature":"a wide nature landscape with mountains, a river, a forest, a meadow with flowers and a deer",
 # tegnap és ma, érzések
 "happy":"a happy child smiling","school trip":"a class on a school trip with a teacher",
}


# Ahol a három nyelvi lista sorrendje NEM egyezik (a spanyolban egy szóval
# kevesebb áll előrébb), ott kézzel adjuk meg a párt.
KIVETEL = {
    "happy": {"es": "contento"},
    "school trip": {"es": "la excursión"},
}


def _slug(szo: str) -> str:
    s = szo.lower().replace("'", "")
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    return s


def fogalmak() -> list[dict]:
    """A három nyelvi fájlból: [{kulcs, en, de, es, alany}], ismétlés nélkül."""
    adat = {}
    for kod, fajl in NYELVEK.items():
        with open(os.path.join(TANTERV, fajl), encoding="utf-8") as f:
            adat[kod] = json.load(f)
    lista, latott = [], set()
    blokkok = sorted(adat["en"]["evfolyam_blokkok"].items())
    for evf, blokk in blokkok:
        for ti, tema in enumerate(blokk["temakorok"]):
            en_szavak = tema.get("szokincs", [])
            for si, en in enumerate(en_szavak):
                if en not in ALANY:
                    continue
                kulcs = _slug(en)
                if kulcs in latott:
                    continue
                latott.add(kulcs)
                elem = {"kulcs": kulcs, "en": en, "alany": ALANY[en], "evfolyam": int(evf)}
                for kod in ("de", "es"):
                    try:
                        elem[kod] = adat[kod]["evfolyam_blokkok"][evf]["temakorok"][ti]["szokincs"][si]
                    except (KeyError, IndexError):
                        elem[kod] = ""
                elem.update(KIVETEL.get(en, {}))
                lista.append(elem)
    return lista


def prompt(f: dict) -> str:
    return f"{f['alany'].capitalize()}. {STILUS}. {TILTAS}"


def uj_ut(f: dict) -> str:
    return os.path.join(UJ_MAPPA, f["kulcs"] + ".png")


def vegleges_ut(f: dict) -> str:
    return os.path.join(VEGLEGES, f["kulcs"] + ".webp")


def generalas(kliens, f: dict) -> bytes:
    valasz = kliens.images.generate(model=MODELL, prompt=prompt(f), size=MERET, n=1)
    elem = valasz.data[0]
    b64 = getattr(elem, "b64_json", None)
    if b64:
        return base64.b64decode(b64)
    url = getattr(elem, "url", None)
    if url:
        import urllib.request
        with urllib.request.urlopen(url, timeout=60) as v:
            return v.read()
    raise RuntimeError("A válaszban nincs se kép, se URL.")


def attekinto(lista: list[dict]) -> None:
    """Átnéző lap: kipipálod, ami jó, és kiírja a jóváhagyó parancsot."""
    kartyak = []
    for f in lista:
        if not os.path.exists(uj_ut(f)):
            continue
        kesz = os.path.exists(vegleges_ut(f))
        kartyak.append(
            f'<label class="k{" kesz" if kesz else ""}"><img src="{f["kulcs"]}.png" loading="lazy">'
            f'<span><input type="checkbox" value="{f["kulcs"]}"{" checked" if kesz else ""}> '
            f'<b>{html.escape(f["en"])}</b> · {html.escape(f.get("de",""))} · {html.escape(f.get("es",""))}'
            f'{" ✓ már jóváhagyva" if kesz else ""}</span></label>')
    lap = f"""<!doctype html><meta charset="utf-8"><title>Képes szótár – átnézés</title>
<style>body{{font-family:system-ui;background:#FBF5EA;margin:0;padding:20px}}
h1{{color:#0E2A1E}}.racs{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:14px}}
.k{{background:#fff;border-radius:16px;padding:10px;cursor:pointer;box-shadow:0 4px 12px rgba(0,0,0,.08)}}
.k img{{width:100%;border-radius:10px;display:block}}.k span{{display:block;margin-top:8px;font-size:14px}}
.k.kesz{{outline:3px solid #3DDC97}}#ki{{position:sticky;bottom:0;background:#0E2A1E;color:#fff;padding:14px;
border-radius:14px;margin-top:20px}}#ki code{{display:block;background:#fff;color:#000;padding:8px;margin-top:8px;
word-break:break-all}}button{{background:#F5A01E;color:#fff;border:0;border-radius:99px;padding:10px 18px;font-weight:800}}</style>
<h1>Képes szótár – {len(kartyak)} kép</h1><p>Pipáld ki a JÓ képeket, aztán nyomd meg a gombot, és másold be a parancsot.</p>
<div class="racs">{"".join(kartyak)}</div>
<div id="ki"><button onclick="ir()">Parancs a kipipáltakhoz</button><code id="p"></code></div>
<script>function ir(){{var v=[].map.call(document.querySelectorAll('input:checked'),function(x){{return x.value}});
document.getElementById('p').textContent='python szokep_generalas.py --jovahagy '+v.join(',');}}</script>"""
    with open(os.path.join(UJ_MAPPA, "attekinto.html"), "w", encoding="utf-8") as f:
        f.write(lap)


def jovahagy(lista: list[dict], kulcsok: list[str]) -> int:
    from PIL import Image
    os.makedirs(VEGLEGES, exist_ok=True)
    index_ut = os.path.join(VEGLEGES, "szokepek.json")
    index = {}
    if os.path.exists(index_ut):
        with open(index_ut, encoding="utf-8") as f:
            index = json.load(f)
    szerint = {f["kulcs"]: f for f in lista}
    db = 0
    for k in kulcsok:
        f = szerint.get(k)
        if not f or not os.path.exists(uj_ut(f)):
            print(f"  ! nincs ilyen kép: {k}")
            continue
        kep = Image.open(uj_ut(f)).convert("RGB")
        kep.thumbnail((512, 512))
        kep.save(vegleges_ut(f), "WEBP", quality=82, method=6)
        index[k] = {"en": f["en"], "de": f.get("de", ""), "es": f.get("es", "")}
        db += 1
        print(f"  ✓ {k}")
    with open(index_ut, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=1, sort_keys=True)
    print(f"\n{db} kép jóváhagyva → static/szokepek/nyelv. Ne felejtsd el feltölteni (git add static/szokepek).")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="Képes szótár képei")
    p.add_argument("--lista", action="store_true", help="csak kiírja, nem hív API-t")
    p.add_argument("--db", type=int, default=0, help="legfeljebb ennyi képet gyárt")
    p.add_argument("--csak", default="", help="vesszővel elválasztott kulcsok")
    p.add_argument("--ujra", action="store_true", help="a meglévő képet is újragyártja")
    p.add_argument("--jovahagy", default="", help="vesszővel elválasztott kulcsok, vagy MIND")
    a = p.parse_args()

    lista = fogalmak()
    if a.csak:
        csak = {x.strip() for x in a.csak.split(",") if x.strip()}
        lista_cel = [f for f in lista if f["kulcs"] in csak]
    else:
        lista_cel = lista

    if a.jovahagy:
        kulcsok = ([f["kulcs"] for f in lista if os.path.exists(uj_ut(f))]
                   if a.jovahagy.strip().upper() == "MIND"
                   else [x.strip() for x in a.jovahagy.split(",") if x.strip()])
        return jovahagy(lista, kulcsok)

    if a.lista:
        for f in lista_cel:
            print(f"{f['kulcs']:16} {f['en']:14} {f.get('de',''):16} {f.get('es',''):16} → {f['alany']}")
        print(f"\nÖsszesen {len(lista_cel)} kép. Becsült költség: kb. {len(lista_cel)*0.02:.0f}–{len(lista_cel)*0.04:.0f} $.")
        return 0

    kulcs = os.environ.get("OPENAI_API_KEY")
    if not kulcs:
        print("Nincs OPENAI_API_KEY. Windowsban: setx OPENAI_API_KEY \"ide-a-sajat-kulcsod\" – és új ablak.")
        return 1
    from openai import OpenAI
    kliens = OpenAI(api_key=kulcs)
    os.makedirs(UJ_MAPPA, exist_ok=True)

    tennivalo = [f for f in lista_cel if a.ujra or not os.path.exists(uj_ut(f))]
    if a.db:
        tennivalo = tennivalo[: a.db]
    print(f"{len(tennivalo)} kép készül, modell: {MODELL}\n")
    hiba = 0
    for i, f in enumerate(tennivalo, 1):
        print(f"[{i}/{len(tennivalo)}] {f['en']} …", flush=True)
        try:
            adat = generalas(kliens, f)
            with open(uj_ut(f), "wb") as ki:
                ki.write(adat)
        except Exception as e:
            hiba += 1
            print(f"   ! nem sikerült: {type(e).__name__}: {str(e)[:160]}")
            if "model" in str(e).lower() and i == 1:
                print("   A modell nevét a MODELL sorban kell átírni.")
                return 1
            time.sleep(2)
    attekinto(lista)
    print(f"\nKész ({hiba} hiba). Nyisd meg: szokep_uj/attekinto.html")
    return 0


if __name__ == "__main__":
    sys.exit(main())
