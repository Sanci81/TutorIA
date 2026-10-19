# -*- coding: utf-8 -*-
"""TutorIA – A KISFIÚ ÉS A MACI KÉPEI (AI-rajz a bábu helyett)

A mintaoldalon a kisfiú és a maci SVG-ből volt összerakva, és bábunak
látszott. Itt az OpenAI képgenerálója rajzolja meg őket, ugyanabban a
mesekönyv-stílusban, mint a többi képet.

KISFIÚ: egy alapkép, aztán UGYANAZ a fiú különböző pózokban (megfogja az
orrát, a fülét, integet …). Az oldal a két kép között áttűnéssel vált,
így úgy látszik, mintha megmozdulna.

MACI: egy ruha nélküli maci, aztán UGYANARRA a macira rárajzolja a ruhákat
(sapka, sál, póló, csizma, négy színben). A program minden ruhát kivág
külön rétegnek, így a ruhák pontosan illenek, és bármilyen összeállításban
ráadhatók – nem páncélként lógnak rajta.

1. LÉPÉS – AZ ALAPKÉP (3 jelölt, ebből választasz)
    python figura_kepek.py --alap fiu
    python figura_kepek.py --alap maci
        Nyisd meg: szokep_uj/figurak/attekinto.html
    python figura_kepek.py --valaszt fiu:2
        A 2. jelölt lesz a fiú. (Ugyanígy: --valaszt maci:1)

2. LÉPÉS – PÓZOK ÉS RUHÁK (az alapképből)
    python figura_kepek.py --lista
        Kiírja, mi készülne. Ingyenes.
    python figura_kepek.py --gyart fiu --db 1
        Egy próbapóz. Ha jó:
    python figura_kepek.py --gyart fiu
    python figura_kepek.py --gyart maci
        Nyisd meg újra az attekinto.html-t: a macin ki lehet próbálni a
        ruhákat, a fiúnál látszik minden póz.
    Rossz képet újra lehet kérni:
    python figura_kepek.py --gyart fiu --csak nose --ujra

3. LÉPÉS – JÓVÁHAGYÁS
    python figura_kepek.py --jovahagy fiu
    python figura_kepek.py --jovahagy maci
        A képek a static/figurak/fiu és static/figurak/maci mappába
        kerülnek (webp). Töltsd fel: git add static/figurak

MI KELL HOZZÁ: OPENAI_API_KEY és a Pillow (ugyanaz, mint a szótárnál).
--minoseg medium (alap) vagy high: a high részletesebb, de drágább.
"""

from __future__ import annotations

import argparse
import base64
import io
import json
import os
import sys
import time

GYOKER = os.path.dirname(os.path.abspath(__file__))
UJ_MAPPA = os.path.join(GYOKER, "szokep_uj", "figurak")
VEGLEGES = os.path.join(GYOKER, "static", "figurak")
MODELL = "gpt-image-2"

STILUS = (
    "high-quality children's picture-book illustration, soft painterly "
    "shading, gentle warm light, clean confident outlines, rich but soft "
    "colours, friendly and lively, one single character shown whole from "
    "head to toe, centred, front view, plenty of empty space around it, "
    "plain pure white background, no floor, no shadow on the ground"
)
TILTAS = (
    "No text, no letters, no numbers, no watermark, no logo, no border, no "
    "frame, no other characters, no props. Not a photograph, not a 3D render, "
    "not a puppet, not made of separate parts: one natural, cohesive body."
)

FIGURAK = {
    "fiu": {
        "meret": "1024x1536",
        "alany": (
            "a cheerful 7-year-old boy with short tousled brown hair, warm "
            "brown eyes and a friendly smile, wearing a plain blue T-shirt, "
            "navy shorts and white sneakers, standing relaxed with both arms "
            "hanging naturally at his sides, the whole body visible, the head "
            "takes about one fifth of the picture height, natural child "
            "proportions"
        ),
    },
    "maci": {
        "meret": "1024x1024",
        "alany": (
            "a soft cuddly light-brown teddy bear with a cream-coloured "
            "muzzle and tummy, round ears and small dark eyes, plush fur "
            "texture, standing upright on its two legs, arms held slightly "
            "away from the body, no clothes at all; the bear fills the picture "
            "from near the top edge to near the bottom edge"
        ),
    },
}

# A fiú pózai. A kulcs ugyanaz, amit az oldal használ (angol testrész).
POZOK = {
    "eyes": "pointing with both index fingers to his own two eyes, eyes wide open, smiling",
    "ears": "touching both of his own ears with his hands, smiling",
    "eyebrows": "touching his own two eyebrows with his index fingers, eyebrows raised high",
    "nose": "touching the tip of his own nose with his right index finger, smiling",
    "mouth": "pointing with his right index finger at his own open smiling mouth",
    "chin": "touching his own chin with his right hand, as if thinking",
    "hair": "patting the top of his own hair with his right hand, smiling",
    "integet": "waving hello with his right hand raised high, big friendly smile",
    "nem": "gently shaking his head no, head tilted a little, kind and slightly puzzled face, both arms down",
    "igen": "giving a happy thumbs up with his right hand, big proud smile",
    "orul": "jumping for joy with both arms raised, very happy",
}

# A maci ruhái: (kulcs, angol leírás, hol van a képen: felső–alsó arány)
RUHAK = {
    "hat": ("a knitted winter beanie hat with a pompom, worn on its head between the ears", (0.00, 0.38)),
    "scarf": ("a knitted scarf wrapped once around its neck, the ends hanging down its chest", (0.25, 0.62)),
    "tshirt": ("a short-sleeved cotton T-shirt that fits its round tummy and arms", (0.28, 0.78)),
    "boots": ("a pair of short rubber boots on its two feet", (0.66, 1.00)),
}
SZINEK = {"red": "red", "blue": "blue", "yellow": "bright yellow", "green": "green"}
# Ebben a sorrendben kerülnek egymásra a rétegek az oldalon.
SORREND = ["tshirt", "boots", "scarf", "hat"]


def _kep_bajt(valasz) -> bytes:
    elem = valasz.data[0]
    b64 = getattr(elem, "b64_json", None)
    if b64:
        return base64.b64decode(b64)
    url = getattr(elem, "url", None)
    if url:
        import urllib.request
        with urllib.request.urlopen(url, timeout=90) as v:
            return v.read()
    raise RuntimeError("A válaszban nincs se kép, se URL.")


def _hivas(fv, **kw):
    """Régebbi openai csomagnál egyes beállítások hiányoznak – akkor nélkülük."""
    for elhagy in ([], ["input_fidelity"], ["input_fidelity", "quality"]):
        try:
            return fv(**{k: v for k, v in kw.items() if k not in elhagy})
        except TypeError:
            continue
        except Exception as e:
            if any(k in str(e) for k in ("input_fidelity", "quality")) and elhagy != ["input_fidelity", "quality"]:
                continue
            raise
    return fv(**{k: v for k, v in kw.items() if k not in ("input_fidelity", "quality")})


def mappa(fig: str) -> str:
    return os.path.join(UJ_MAPPA, fig)


def alap_ut(fig: str) -> str:
    return os.path.join(mappa(fig), "alap.png")


# ── 1. LÉPÉS ────────────────────────────────────────────────────────────
def alap_jeloltek(kliens, fig: str, minoseg: str, db: int) -> int:
    os.makedirs(mappa(fig), exist_ok=True)
    f = FIGURAK[fig]
    for i in range(1, db + 1):
        ut = os.path.join(mappa(fig), f"jelolt_{i}.png")
        if os.path.exists(ut):
            print(f"  {fig} {i}. jelölt már megvan (töröld, ha újat kérsz)")
            continue
        print(f"  {fig} {i}. jelölt …", flush=True)
        try:
            v = _hivas(kliens.images.generate, model=MODELL, size=f["meret"], n=1, quality=minoseg,
                       prompt=f"{STILUS}. Subject: {f['alany']}. {TILTAS}")
            with open(ut, "wb") as ki:
                ki.write(_kep_bajt(v))
        except Exception as e:
            print(f"   ! nem sikerült: {type(e).__name__}: {str(e)[:200]}")
    attekinto()
    print("\nNyisd meg: szokep_uj/figurak/attekinto.html, aztán: "
          f"python figura_kepek.py --valaszt {fig}:<szám>")
    return 0


def valaszt(parancs: str) -> int:
    fig, _, sz = parancs.partition(":")
    forras = os.path.join(mappa(fig), f"jelolt_{sz.strip()}.png")
    if fig not in FIGURAK or not os.path.exists(forras):
        print(f"Nincs ilyen jelölt: {parancs}")
        return 1
    with open(forras, "rb") as a, open(alap_ut(fig), "wb") as b:
        b.write(a.read())
    print(f"✓ A(z) {sz}. jelölt lett a {fig} alapképe. Jöhet: python figura_kepek.py --gyart {fig}")
    attekinto()
    return 0


# ── 2. LÉPÉS: A FIÚ PÓZAI ───────────────────────────────────────────────
def poz_prompt(leiras: str) -> str:
    return (f"The very same boy as in the picture, drawn by the same illustrator in "
            f"exactly the same style: same face, same hair, same clothes and colours, "
            f"same size, standing on the same spot, whole body visible, same plain white "
            f"background. Now he is {leiras}. The pose must be natural and clearly "
            f"readable for a 6-year-old. {TILTAS}")


def fiu_pozok(kliens, csak: set, ujra: bool, db: int, minoseg: str) -> int:
    if not os.path.exists(alap_ut("fiu")):
        print("Előbb válassz alapképet: --alap fiu, aztán --valaszt fiu:<szám>")
        return 1
    teendo = [k for k in POZOK if (not csak or k in csak)
              and (ujra or not os.path.exists(os.path.join(mappa("fiu"), k + ".png")))]
    if db:
        teendo = teendo[:db]
    for i, k in enumerate(teendo, 1):
        print(f"[{i}/{len(teendo)}] fiú: {k} …", flush=True)
        try:
            with open(alap_ut("fiu"), "rb") as kep:
                v = _hivas(kliens.images.edit, model=MODELL, image=kep, size=FIGURAK["fiu"]["meret"],
                           prompt=poz_prompt(POZOK[k]), input_fidelity="high", quality=minoseg)
            with open(os.path.join(mappa("fiu"), k + ".png"), "wb") as ki:
                ki.write(_kep_bajt(v))
        except Exception as e:
            print(f"   ! nem sikerült: {type(e).__name__}: {str(e)[:200]}")
            time.sleep(2)
    attekinto()
    print("\nKész. Nyisd meg: szokep_uj/figurak/attekinto.html")
    return 0


# ── 2. LÉPÉS: A MACI RUHÁI ──────────────────────────────────────────────
def _maszk_png(meret, savok) -> bytes:
    """OpenAI-maszk: ahol ÁTLÁTSZÓ, ott szabad rajzolni."""
    from PIL import Image, ImageDraw
    w, h = meret
    m = Image.new("RGBA", (w, h), (0, 0, 0, 255))
    d = ImageDraw.Draw(m)
    d.rectangle([0, int(savok[0] * h), w, int(savok[1] * h)], fill=(0, 0, 0, 0))
    b = io.BytesIO()
    m.save(b, "PNG")
    return b.getvalue()


def reteg_kivag(alap, uj, savok):
    """A ruha rétege: ami a ruha sávjában megváltozott az alapképhez képest.

    Az új kép néha 1-2 képponttal elcsúszik – előbb visszaigazítjuk, aztán
    csak a különbséget tartjuk meg, lágy szélekkel. Visszaadja a réteget
    (RGBA) és azt, mennyire tér el a kép a sávon KÍVÜL (ha sok, a gép
    nem csak a ruhát rajzolta át – azt érdemes újrakérni).
    """
    from PIL import Image, ImageChops, ImageFilter, ImageStat
    alap = alap.convert("RGB")
    uj = uj.convert("RGB").resize(alap.size)
    w, h = alap.size
    y0, y1 = int(savok[0] * h), int(savok[1] * h)
    kint = Image.new("L", (w, h), 255)
    kint.paste(0, (0, max(0, y0 - 20), w, min(h, y1 + 20)))

    def elteres(kep):
        d = ImageChops.difference(alap, kep).convert("L")
        return ImageStat.Stat(d, mask=kint).mean[0]

    legjobb, eltolas = None, (0, 0)
    for dx in range(-6, 7, 2):
        for dy in range(-6, 7, 2):
            e = elteres(ImageChops.offset(uj, dx, dy))
            if legjobb is None or e < legjobb:
                legjobb, eltolas = e, (dx, dy)
    uj = ImageChops.offset(uj, *eltolas)

    d = ImageChops.difference(alap, uj).convert("L")
    d = d.point(lambda v: 255 if v > 30 else 0)
    d = d.filter(ImageFilter.MinFilter(5)).filter(ImageFilter.MaxFilter(5))      # pöttyök ki
    d = d.filter(ImageFilter.MaxFilter(11)).filter(ImageFilter.MinFilter(11))    # lyukak be
    sav = Image.new("L", (w, h), 0)
    sav.paste(255, (0, y0, w, y1))
    sav = sav.filter(ImageFilter.GaussianBlur(12))
    alfa = ImageChops.multiply(d.filter(ImageFilter.GaussianBlur(1.5)), sav)
    reteg = uj.convert("RGBA")
    reteg.putalpha(alfa)
    return reteg, legjobb


def ruha_prompt(szin: str, leiras: str) -> str:
    return (f"The very same teddy bear as in the picture, unchanged: same pose, same "
            f"position, same size, same fur, same face, same lighting, same plain white "
            f"background. Only add {szin} {leiras}. The clothing is soft fabric that "
            f"follows the bear's round body naturally, with gentle folds and shading, "
            f"drawn in the same illustration style. {TILTAS}")


def maci_ruhak(kliens, csak: set, ujra: bool, db: int, minoseg: str) -> int:
    from PIL import Image
    if not os.path.exists(alap_ut("maci")):
        print("Előbb válassz alapképet: --alap maci, aztán --valaszt maci:<szám>")
        return 1
    alap = Image.open(alap_ut("maci"))
    teendo = []
    for r in RUHAK:
        for sz in SZINEK:
            k = f"{r}_{sz}"
            if csak and k not in csak and r not in csak:
                continue
            if not ujra and os.path.exists(os.path.join(mappa("maci"), k + ".png")):
                continue
            teendo.append((r, sz, k))
    if db:
        teendo = teendo[:db]
    for i, (r, sz, k) in enumerate(teendo, 1):
        print(f"[{i}/{len(teendo)}] maci: {SZINEK[sz]} {r} …", flush=True)
        try:
            with open(alap_ut("maci"), "rb") as kep:
                v = _hivas(kliens.images.edit, model=MODELL, image=kep,
                           mask=("maszk.png", _maszk_png(alap.size, RUHAK[r][1]), "image/png"),
                           size=FIGURAK["maci"]["meret"], prompt=ruha_prompt(SZINEK[sz], RUHAK[r][0]),
                           input_fidelity="high", quality=minoseg)
            nyers = Image.open(io.BytesIO(_kep_bajt(v)))
            nyers.save(os.path.join(mappa("maci"), k + "_teljes.png"))
            reteg, kint = reteg_kivag(alap, nyers, RUHAK[r][1])
            reteg.save(os.path.join(mappa("maci"), k + ".png"))
            if kint > 10:
                print(f"   ! a ruhán kívül is sokat változott ({kint:.0f}) – nézd meg, "
                      f"lehet, hogy újra kell kérni: --gyart maci --csak {k} --ujra")
        except Exception as e:
            print(f"   ! nem sikerült: {type(e).__name__}: {str(e)[:200]}")
            time.sleep(2)
    attekinto()
    print("\nKész. Nyisd meg: szokep_uj/figurak/attekinto.html – ott ki is próbálhatod a ruhákat.")
    return 0


# ── ÁTNÉZŐ ──────────────────────────────────────────────────────────────
def attekinto() -> None:
    os.makedirs(UJ_MAPPA, exist_ok=True)
    resz = []
    for fig in FIGURAK:
        jel = sorted(x for x in os.listdir(mappa(fig)) if x.startswith("jelolt_")) if os.path.isdir(mappa(fig)) else []
        if jel:
            kepek = "".join(f'<figure><img src="{fig}/{x}"><figcaption>{x[7:-4]}. jelölt</figcaption></figure>' for x in jel)
            resz.append(f"<h2>{fig} – alapkép-jelöltek</h2><p>Válassz: <code>python figura_kepek.py "
                        f"--valaszt {fig}:&lt;szám&gt;</code></p><div class='racs'>{kepek}</div>")
    if os.path.exists(alap_ut("fiu")):
        kepek = '<figure><img src="fiu/alap.png"><figcaption>alap</figcaption></figure>' + "".join(
            f'<figure><img src="fiu/{k}.png"><figcaption>{k}</figcaption></figure>'
            for k in POZOK if os.path.exists(os.path.join(mappa("fiu"), k + ".png")))
        resz.append(f"<h2>Kisfiú – pózok</h2><div class='racs'>{kepek}</div>")
    if os.path.exists(alap_ut("maci")):
        gombok = ""
        for r in SORREND:
            for sz in SZINEK:
                if os.path.exists(os.path.join(mappa("maci"), f"{r}_{sz}.png")):
                    gombok += f'<button data-r="{r}" data-sz="{sz}" style="background:{sz}">{r}</button>'
        resz.append(
            "<h2>Maci – próbáld fel a ruhákat</h2><div class='maci'><div id='m'><img src='maci/alap.png'>"
            + "".join(f"<img id='r_{r}' hidden>" for r in SORREND)
            + f"</div><div class='gombok'>{gombok}</div></div>")
    lap = """<!doctype html><meta charset="utf-8"><title>Kisfiú és maci – képek</title>
<style>body{font-family:system-ui;background:#FBF5EA;margin:0;padding:20px;color:#0E2A1E}
.racs{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:14px}
figure{margin:0;background:#fff;border-radius:14px;padding:8px;box-shadow:0 4px 12px rgba(0,0,0,.08)}
figure img{width:100%;display:block;border-radius:8px}figcaption{text-align:center;font-weight:700;margin-top:6px}
.maci{display:flex;gap:20px;flex-wrap:wrap}#m{position:relative;width:min(420px,100%);background:#fff;border-radius:14px}
#m img{width:100%;display:block}#m img+img{position:absolute;left:0;top:0}
.gombok{display:grid;grid-template-columns:repeat(4,90px);gap:8px;align-content:start}
.gombok button{color:#fff;border:0;border-radius:10px;padding:10px 4px;font-weight:800;text-shadow:0 1px 2px #000;cursor:pointer}
code{background:#fff;padding:2px 6px;border-radius:6px}</style>
<h1>Kisfiú és maci</h1>""" + "".join(resz) + """
<script>document.querySelectorAll('.gombok button').forEach(function(b){b.onclick=function(){
var i=document.getElementById('r_'+b.dataset.r),u='maci/'+b.dataset.r+'_'+b.dataset.sz+'.png';
if(!i.hidden&&i.getAttribute('src')===u){i.hidden=true;return;}i.src=u;i.hidden=false;};});</script>"""
    with open(os.path.join(UJ_MAPPA, "attekinto.html"), "w", encoding="utf-8") as f:
        f.write(lap)


# ── 3. LÉPÉS ────────────────────────────────────────────────────────────
def jovahagy(fig: str) -> int:
    from PIL import Image
    if fig not in FIGURAK or not os.path.exists(alap_ut(fig)):
        print(f"Nincs még {fig} alapkép.")
        return 1
    cel = os.path.join(VEGLEGES, fig)
    os.makedirs(cel, exist_ok=True)
    kulcsok = ["alap"] + (list(POZOK) if fig == "fiu" else [f"{r}_{sz}" for r in RUHAK for sz in SZINEK])
    meret = (512, 768) if fig == "fiu" else (640, 640)
    megvan = []
    for k in kulcsok:
        forras = os.path.join(mappa(fig), k + ".png")
        if not os.path.exists(forras):
            continue
        kep = Image.open(forras)
        kep = kep.convert("RGBA" if (fig == "maci" and k != "alap") else "RGB").resize(meret, Image.LANCZOS)
        kep.save(os.path.join(cel, k + ".webp"), "WEBP", quality=85, method=6)
        megvan.append(k)
        print(f"  ✓ {fig}/{k}")
    with open(os.path.join(cel, "kepek.json"), "w", encoding="utf-8") as f:
        json.dump({"kepek": megvan, "sorrend": SORREND if fig == "maci" else []}, f, indent=1)
    print(f"\n{len(megvan)} kép → static/figurak/{fig}. Töltsd fel: git add static/figurak")
    return 0


def lista() -> int:
    print("fiú:  3 alapkép-jelölt + " + str(len(POZOK)) + " póz: " + ", ".join(POZOK))
    print("maci: 3 alapkép-jelölt + " + str(len(RUHAK) * len(SZINEK)) + " ruha (" +
          ", ".join(RUHAK) + " × " + ", ".join(SZINEK) + ")")
    print("Összesen kb. " + str(6 + len(POZOK) + len(RUHAK) * len(SZINEK)) + " kép. Előbb próbáld --db 1-gyel, "
          "és nézd meg az OpenAI fiókodban, mennyibe került.")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="A kisfiú és a maci képei")
    p.add_argument("--alap", choices=list(FIGURAK), help="1. lépés: alapkép-jelöltek")
    p.add_argument("--valaszt", default="", help="melyik jelölt legyen az alap, pl. fiu:2")
    p.add_argument("--gyart", choices=list(FIGURAK), help="2. lépés: pózok / ruhák")
    p.add_argument("--jovahagy", choices=list(FIGURAK), help="3. lépés: a static/figurak mappába")
    p.add_argument("--lista", action="store_true")
    p.add_argument("--csak", default="", help="csak ezek, vesszővel (pl. nose,ears vagy hat_red)")
    p.add_argument("--ujra", action="store_true")
    p.add_argument("--db", type=int, default=0, help="legfeljebb ennyi kép (próbának)")
    p.add_argument("--jeloltek", type=int, default=3, help="hány alapkép-jelölt legyen")
    p.add_argument("--minoseg", default="medium", choices=["low", "medium", "high"])
    a = p.parse_args()

    if a.lista:
        return lista()
    if a.valaszt:
        return valaszt(a.valaszt)
    if a.jovahagy:
        return jovahagy(a.jovahagy)
    if not (a.alap or a.gyart):
        p.print_help()
        return 0
    kulcs = os.environ.get("OPENAI_API_KEY")
    if not kulcs:
        print('Nincs OPENAI_API_KEY. Windowsban: setx OPENAI_API_KEY "ide-a-sajat-kulcsod" – és új ablak.')
        return 1
    from openai import OpenAI
    kliens = OpenAI(api_key=kulcs)
    csak = {x.strip() for x in a.csak.split(",") if x.strip()}
    if a.alap:
        return alap_jeloltek(kliens, a.alap, a.minoseg, a.jeloltek)
    if a.gyart == "fiu":
        return fiu_pozok(kliens, csak, a.ujra, a.db, a.minoseg)
    return maci_ruhak(kliens, csak, a.ujra, a.db, a.minoseg)


if __name__ == "__main__":
    sys.exit(main())
