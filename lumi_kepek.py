# -*- coding: utf-8 -*-
"""TutorIA – LUMI, a kabalánk (fix220 – harmadik változat)

fix220 (Sándor): a 2. változat lámpája sem olyan, mint az oldalon. OK: mintának a
kicsi, homályos PNG-t kapta (176 pont), és a gép „szép üvegizzót” rajzolt menetes
foglalattal. Most a minta az OLDAL FEJLÉCÉBEN lévő lámpa, nagy felbontásban
(szokep_uj/logo_lampa_1024.png – ugyanabból a rajzból készült, ami az oldalon van),
és a leírás szóról szóra megmondja: lapos vonalrajz, menta-zöld körvonal, ALATTA
3 rövid arany csík (nem menetes foglalat), benne az arany pöttyös T. Új mappa: lumi3.

ELŐZŐ VÁLTOZAT (fix219):

fix219 (Sándor): az első leírás nem tetszett – a fej a MI LOGÓNK lámpája legyen,
nem egy idegen izzó. Arc nem kell rá, vagy úgy, mintha a lámpa maga lenne az arc.
Ezért a képkészítő most a logót (static/img/tutoria_logo.png) kapja MINTÁNAK,
és 3 változatot kér: (1) arc nélkül, (2) a logó T-betűjének pöttyei adják az
arcot, (3) nagyon egyszerű arc az üvegen. Az állapotok (aha, gondolkodik, örül,
integet, biztat, tapsol) maradnak – azok tetszettek.

ELŐZŐ LEÍRÁS (fix218):

Sándor 11.19: „lámpafejű kis figura” + Claude: a feje egy IZZÓ (a logónkból jön),
és KIGYULLAD, amikor a gyerek rájön valamire. Aranyos, részletesen kidolgozott.

KI LUMI?
  * Kicsi, gyerek-arányú (nagy fej, kis test), barátságos, kíváncsi.
  * A feje egy kerek ÜVEG IZZÓ, benne halvány meleg fény; az üvegen az arca:
    nagy, csillogó szemek, rózsás pofi, kis mosoly. A „nyaka” az izzó
    sárgaréz menetes foglalata.
  * Ruhája: puha menta-zöld (a logó zöldje) kapucnis pulóver, a mellén kis
    sárga villám-csillag; narancs cipő. Rövid kar, kesztyűs kerek kéz.
  * Állapotai: nyugodt (halvány fény) → „AHA!” (az izzó fényesen kigyullad,
    körülötte apró fénysugarak) → gondolkodik → örül → biztat (sosem szomorú-
    sírós, sosem gúnyos).
  * Neve nyelvfüggetlen: Lumi (luz / lumen) – magyarul és spanyolul is jól mondható.

fix230 – A MOZGÓ LUMI 4 ÚJ TESTTARTÁSA (az alap.png-ből, ugyanaz a figura):
    python lumi_kepek.py --mozgas
        maszik, ul, meglepodik, lenez, fejfogas (fix237) – a már meglévőket átugorja. Nézd meg: szokep_uj/lumi3/attekinto.html
        Ha egy nem jó: töröld a képet, és újra: python lumi_kepek.py --allapot maszik

LÉPÉSEK (egyenként; a képek a szokep_uj/lumi mappába kerülnek):
    python lumi_kepek.py --jeloltek
        3 jelölt (3 kép). Nézd meg: szokep_uj/lumi3/attekinto.html
    python lumi_kepek.py --valaszt 2
        A 2. jelölt lesz Lumi. Ebből készülnek az állapotok:
    python lumi_kepek.py --allapotok
        aha (világít), gondolkodik, orul, integet, biztat, tapsol (6 kép)
    python lumi_kepek.py --allapot aha
        Csak egyet kér újra.
    python lumi_kepek.py --jovahagy
        static/figurak/lumi/*.webp (átlátszó háttérrel)
        git add static/figurak/lumi

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

import figura_kepek as fk

GYOKER = os.path.dirname(os.path.abspath(__file__))
MAPPA = os.path.join(GYOKER, "szokep_uj", "lumi3")
VEGLEGES = os.path.join(GYOKER, "static", "figurak", "lumi")
MERET = "1024x1536"

LOGO = os.path.join(GYOKER, "szokep_uj", "logo_lampa_1024.png")
LUMI = (
    "LUMI, an adorable little mascot character for a children's learning app. Its HEAD IS EXACTLY THE "
    "LIGHT BULB OF THE ATTACHED LOGO, copied faithfully, as a FLAT line drawing: the same rounded bulb "
    "outline drawn as one thick mint-green line (#3DDC97) with a slightly darker, softly glowing inside; "
    "inside the bulb the pale-golden letter 'T' made of a straight line with FOUR round dots (three dots "
    "on the top bar – left, middle, right – and one dot at the bottom of the stem); UNDER the bulb THREE "
    "short horizontal pale-golden rounded bars stacked, each a bit shorter than the one above. NO glass "
    "shine, NO screw thread, NO metal socket, NO filament – only these shapes. Do NOT copy the dark square "
    "background of the logo. Chibi proportions: big bulb head, "
    "small soft body, about three heads tall. Body: a soft mint-green hoodie with a tiny golden star on "
    "the chest, short arms with round white mitten-like hands, short legs and little orange sneakers. "
    "Friendly, curious, kind, warm. "
)
# A három változat abban különbözik, hogyan „néz” a lámpa.
ARCOK = [
    "NO FACE at all: the bulb stays exactly like the logo; the character shows its mood only with its "
    "body language and the glow of the bulb",
    "the dots of the golden 'T' inside the bulb subtly work as a face: the two outer top dots are the "
    "eyes (slightly bigger, with a tiny white sparkle), the bottom dot is a small mouth – it should still "
    "clearly read as the 'T' of the logo",
    "a very simple, minimal face drawn softly on the glass under the 'T': two small dark dot eyes and a "
    "tiny smile, nothing else",
]
STILUS = (
    "Cute children's mascot in a clean FLAT vector style that matches the logo: simple shapes, even "
    "line thickness, flat colours with only very soft shading, no 3D render, no glossy plastic look; "
    "whole figure from head to toe, front view, centred, plenty of empty space around it, plain pure "
    "white background, no floor, no shadow on the ground"
)
TILTAS = ("No text, no letters, no numbers, no logo, no watermark, no border, no other characters, "
          "no props.")
POZ = "standing cheerfully, one hand slightly raised in a friendly hello, the bulb glows softly"
ALLAPOTOK = {
    "aha": "the 'AHA!' moment: the inside of the bulb head lights up BRIGHT warm yellow and small light "
           "rays shine around it; one finger raised as if it just understood something, body slightly "
           "bouncing with joy",
    "gondolkodik": "thinking: one mitten hand on the chin, eyes looking up, the bulb glows only faintly",
    "orul": "jumping for joy with both arms raised high, big open happy smile, bulb glowing brightly",
    "integet": "waving hello with one hand raised high, the other hand on the hip, cheerful posture, soft glow",
    "biztat": "kind and encouraging: a gentle smile and a thumbs up, head slightly tilted, soft glow "
              "(warm, not sad, not crying)",
    "tapsol": "clapping both hands in front of the chest, proud happy smile, bulb glowing",
}
# fix230 (Sándor: „a rajzolt Lumi olyan, mint egy fabábu – az eredeti képből legyen”): a mozgó Lumi
# a JÓVÁHAGYOTT képekből áll; a mozgáshoz még 4 testtartás kell. Kötél, polc NEM kerül a képre –
# a kötelet a program rajzolja a kép mögé, pont a kép közepére (ezért a kezek a középvonalon vannak).
MOZGAS = {
    "maszik": "climbing an INVISIBLE vertical rope, seen from the front: both mitten hands closed into fists and placed "
              "one directly above the other EXACTLY on the vertical centre line of the body, at the height of the bottom "
              "of the bulb (the left hand a little higher than the right hand), elbows bent outwards; both legs bent and "
              "pressed together around the same vertical centre line, the sneakers crossed over each other, as if "
              "hugging a rope. Do NOT draw any rope",
    "ul": "sitting on the edge of an INVISIBLE shelf: the bottom rests on an invisible horizontal edge at hip height, both "
          "legs hang down in front, relaxed, the sneakers dangling; both mitten hands rest on the invisible edge beside "
          "the hips; calm and content, soft glow. Do NOT draw the shelf, any seat or any line",
    "meglepodik": "playfully surprised, as if someone tickled it: hopping a little backwards with knees bent, both arms "
                  "raised up and slightly to the sides with open mittens, the body leaning back, the bulb glowing a bit "
                  "brighter (playful, not scared)",
    # fix237 (Sándor: „ha nem jó valami, fogja a fejét”)
    "fejfogas": "an 'oh no!' moment: both mitten hands pressed against the two sides of the bulb head, as if holding its "
                "head in mild dismay, knees slightly bent, the body leaning a little forward; playful and cute, not crying, "
                "not scared, the bulb glows only faintly",
    "lenez": "leaning forward and peering down curiously: the body bent forward at the hips, the bulb head tilted down, one "
             "mitten hand held flat above the bulb as if shading its eyes, the other hand resting on the knee",
}
UGYANAZ = ("IMPORTANT: the bulb head has NO FACE – no eyes, no mouth, no cheeks, nothing drawn on the glass "
           "except the golden dotted 'T'; the mood is shown only by the body pose and the glow. "
           "This is the same character as in the attached picture. Keep EVERYTHING identical: the same "
           "logo light-bulb head (with the golden dotted 'T'), the same face or no face, colours, hoodie, proportions and style, the same plain white "
           "background. Change only the pose and expression: ")


def _kliens():
    from openai import OpenAI
    return OpenAI()


def attekinto() -> None:
    os.makedirs(MAPPA, exist_ok=True)
    kepek = [n for n in sorted(os.listdir(MAPPA)) if n.endswith(".png")]
    sor = "".join(f'<figure><img src="{n}"><figcaption>{n}</figcaption></figure>' for n in kepek)
    with open(os.path.join(MAPPA, "attekinto.html"), "w", encoding="utf-8") as ki:
        ki.write('<!doctype html><meta charset="utf-8"><title>Lumi</title>'
                 '<style>body{font-family:system-ui;background:#FBF5EA;padding:20px}'
                 'main{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px}'
                 'figure{margin:0;background:#fff;border-radius:12px;padding:8px}img{width:100%}'
                 'figcaption{text-align:center;font-weight:700}</style><h1>Lumi</h1><main>' + sor + "</main>")


def jeloltek(minoseg: str) -> int:
    os.makedirs(MAPPA, exist_ok=True)
    kl = _kliens()
    if not os.path.exists(LOGO):
        print(f"Nincs meg a logó: {LOGO}")
        return 1
    for i, arc in enumerate(ARCOK, 1):
        ut = os.path.join(MAPPA, f"jelolt_{i}.png")
        if os.path.exists(ut):
            print(f"  {i}. jelölt már megvan (töröld, ha újat kérsz)")
            continue
        print(f"  {i}. jelölt …", flush=True)
        try:
            with open(LOGO, "rb") as logo:
                v = fk._hivas(kl.images.edit, model=fk.MODELL, image=logo, size=MERET, quality=minoseg,
                              input_fidelity="high",
                              prompt=f"{LUMI}Face: {arc}. Pose: {POZ}. {STILUS}. {TILTAS}")
            with open(ut, "wb") as ki:
                ki.write(fk._kep_bajt(v))
        except Exception as e:
            print(f"   ! nem sikerült: {type(e).__name__}: {str(e)[:200]}")
    attekinto()
    print("\nNézd meg: szokep_uj/lumi3/attekinto.html, aztán: python lumi_kepek.py --valaszt <szám>")
    return 0


def valaszt(sz: int) -> int:
    forras = os.path.join(MAPPA, f"jelolt_{sz}.png")
    if not os.path.exists(forras):
        print(f"Nincs ilyen jelölt: {forras}")
        return 1
    shutil.copyfile(forras, os.path.join(MAPPA, "alap.png"))
    attekinto()
    print(f"OK: a {sz}. jelölt lett Lumi. Most: python lumi_kepek.py --allapotok")
    return 0


def allapotok(csak: list[str], minoseg: str) -> int:
    alap = os.path.join(MAPPA, "alap.png")
    if not os.path.exists(alap):
        print("Előbb: python lumi_kepek.py --valaszt <szám>")
        return 1
    kl = _kliens()
    for nev in csak:
        if nev in MOZGAS and os.path.exists(os.path.join(MAPPA, f"{nev}.png")):
            print(f"  {nev} már megvan (töröld, ha újat kérsz)")
            continue
        print(f"  {nev} …", flush=True)
        try:
            with open(alap, "rb") as kep:
                v = fk._hivas(kl.images.edit, model=fk.MODELL, image=kep, size=MERET, quality=minoseg,
                              input_fidelity="high", prompt=UGYANAZ + (ALLAPOTOK.get(nev) or MOZGAS[nev]) + ". " + TILTAS)
            with open(os.path.join(MAPPA, f"{nev}.png"), "wb") as ki:
                ki.write(fk._kep_bajt(v))
        except Exception as e:
            print(f"   ! nem sikerült: {type(e).__name__}: {str(e)[:200]}")
    attekinto()
    print("\nNézd meg: szokep_uj/lumi3/attekinto.html – ha jó: python lumi_kepek.py --jovahagy")
    return 0


# fix232 (Sándor: „a fehér kesztyű nem látszik – legyen olyan színű, mint a cipője”)
class _NdPotlo:
    """fix233: ha a gépen nincs scipy, ez végzi ugyanazt (lassabb, de működik)."""
    @staticmethod
    def _szomszed(m, es):
        import numpy as np
        p = np.pad(m, 1, constant_values=not es)
        t = [p[1 + dy:p.shape[0] - 1 + dy, 1 + dx:p.shape[1] - 1 + dx] for dy in (-1, 0, 1) for dx in (-1, 0, 1)]
        o = t[0].copy()
        for x in t[1:]:
            o = (o & x) if es else (o | x)
        return o
    def binary_dilation(self, m, iterations=1):
        for _ in range(iterations):
            m = self._szomszed(m, False)
        return m
    def binary_erosion(self, m, iterations=1):
        for _ in range(iterations):
            m = self._szomszed(m, True)
        return m
    def binary_opening(self, m, iterations=1):
        return self.binary_dilation(self.binary_erosion(m, iterations), iterations)
    def label(self, m):
        import numpy as np
        from collections import deque
        lab = np.zeros(m.shape, dtype=np.int32); n = 0; H, W = m.shape
        for y0, x0 in zip(*np.nonzero(m)):
            if lab[y0, x0]:
                continue
            n += 1; lab[y0, x0] = n; q = deque([(y0, x0)])
            while q:
                y, x = q.popleft()
                for yy, xx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
                    if 0 <= yy < H and 0 <= xx < W and m[yy, xx] and not lab[yy, xx]:
                        lab[yy, xx] = n; q.append((yy, xx))
        return lab, n
    def find_objects(self, lab):
        import numpy as np
        o = []
        for i in range(1, int(lab.max()) + 1):
            ys, xs = np.nonzero(lab == i)
            o.append((slice(ys.min(), ys.max() + 1), slice(xs.min(), xs.max() + 1)) if len(ys) else None)
        return o


def kesztyu_narancs(k):
    import numpy as np
    from PIL import Image
    try:
        from scipy import ndimage
    except ImportError:
        ndimage = _NdPotlo()
    """fix232 (Sándor: a fehér kesztyű nem látszik a fehér mezőkön): a kesztyű a cipő narancsát kapja.
    Csak a teljesen fedő, szinte fehér/szürke képpontok (a kesztyű és árnyéka), a cipő sorai alatt nem
    (ott a talp és a fűző fehér marad)."""
    a = np.array(k.convert('RGBA')).astype(np.int32)
    r, g, b, al = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
    mx, mn = np.maximum(np.maximum(r, g), b), np.minimum(np.minimum(r, g), b)
    h = a.shape[0]
    nar = (r > 220) & (g > 100) & (g < 175) & (b < 90) & (al > 200)
    sorok = np.where(nar.sum(1) > 2)[0]
    cipo = sorok[sorok > h * .6].min() if (sorok > h * .6).any() else h
    feher = (al > 215) & (mx - mn < 13) & (mx > 150)
    feher[max(0, cipo - 3):, :] = False
    # a fej (izzó) körüli világos szegély ne legyen narancs: a felső 40%-ban csak, ha nincs mellette menta-zöld
    menta = (g > 170) & (r < 150) & (b > 110) & (b < 210)
    menta_kozel = ndimage.binary_dilation(menta, iterations=3)
    # a kesztyű nagyobb, összefüggő foltok: apró darabok (csillogás) maradnak
    # a kesztyű kerek, tömör folt; a lámpa körüli világos gyűrű és az izzó belseje nem az
    nyitott = ndimage.binary_opening(feher, iterations=3)          # a vékony kapcsolatok (gyűrű ↔ kéz) szétválnak
    lab, n = ndimage.label(nyitott)
    jo = np.zeros_like(feher)
    for i, sl in enumerate(ndimage.find_objects(lab), 1):
        if sl is None:
            continue
        hh, ww = sl[0].stop - sl[0].start, sl[1].stop - sl[1].start
        db = (lab[sl] == i).sum()
        if db > 700 and max(hh, ww) < h * .19 and min(hh, ww) > .45 * max(hh, ww) and db / float(hh * ww) > .3:
            jo[sl] |= (lab[sl] == i)
    jo = ndimage.binary_dilation(jo, iterations=4) & feher
    vil = mx[jo] / 255.0                                 # árnyalás megtartása
    a[..., 0][jo] = np.clip(242 * vil + 13 * (1 - vil) * 0, 0, 255)
    a[..., 1][jo] = np.clip(140 * vil, 0, 255)
    a[..., 2][jo] = np.clip(40 * vil, 0, 255)
    return Image.fromarray(a.astype(np.uint8))


def jovahagy(csak: list[str] | None = None) -> int:
    from PIL import Image
    os.makedirs(VEGLEGES, exist_ok=True)
    db = 0
    for nev in (csak or ["alap"] + list(ALLAPOTOK) + list(MOZGAS)):
        ut = os.path.join(MAPPA, nev + ".png")
        if not os.path.exists(ut):
            continue
        k = fk._hatter_le(Image.open(ut))
        bb = k.getchannel("A").getbbox()
        if bb:
            k = k.crop((max(0, bb[0] - 8), max(0, bb[1] - 8), bb[2] + 8, bb[3] + 8))
        k.thumbnail((640, 640), Image.LANCZOS)
        k = kesztyu_narancs(k)                    # fix232/233: narancs kesztyű (scipy nélkül is)
        k.save(os.path.join(VEGLEGES, nev + ".webp"), "WEBP", quality=88, method=6)
        db += 1
        print(f"  kész: static/figurak/lumi/{nev}.webp")
    print(f"\n{db} kép. Töltsd fel: git add static/figurak/lumi")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--jeloltek", action="store_true")
    ap.add_argument("--valaszt", type=int)
    ap.add_argument("--allapotok", action="store_true")
    ap.add_argument("--allapot", choices=list(ALLAPOTOK) + list(MOZGAS))
    ap.add_argument("--mozgas", action="store_true", help="fix230: a mozgó Lumi 4 testtartása (mászik, ül, meglepődik, lenéz)")
    ap.add_argument("--jovahagy", action="store_true")
    ap.add_argument("--csak", help="csak ezeket hagyja jóvá, vesszővel: alap,gondolkodik,orul")
    ap.add_argument("--minoseg", default="medium", choices=["low", "medium", "high"])
    a = ap.parse_args()
    if a.jeloltek:
        return jeloltek(a.minoseg)
    if a.valaszt:
        return valaszt(a.valaszt)
    if a.allapotok:
        return allapotok(list(ALLAPOTOK), a.minoseg)
    if a.mozgas:
        return allapotok(list(MOZGAS), a.minoseg)
    if a.allapot:
        return allapotok([a.allapot], a.minoseg)
    if a.jovahagy:
        return jovahagy([x.strip() for x in a.csak.split(",") if x.strip()] if a.csak else None)
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
