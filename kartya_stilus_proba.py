# -*- coding: utf-8 -*-
"""TutorIA – STÍLUSVÁLASZTÓ egyetlen kártyához.

MIÉRT VAN EZ
    Szavakkal körbetapogatni a stílust drága és lassú: minden kör egy új
    találgatás, és minden találgatás pénz. Ez a program ehelyett UGYANAZT
    a kártyát legyártja több, egymástól ÉLESEN eltérő stílusban, egyszerre.
    Utána a gyerek rábök, melyik tetszik – és onnantól nincs többé vita.

    Ez a program NEM nyúl semmihez. Külön mappába dolgozik
    (kartya_kepek_uj/stilusproba), a meglévő képeket nem írja felül.

HASZNÁLAT
    python kartya_stilus_proba.py --lista
        Kiírja a stílusokat. NEM hív API-t, nem kerül semmibe.

    python kartya_stilus_proba.py foldrajz_7_kolumbusz
        Legyártja ezt az egy kártyát MINDEN stílusban.

    python kartya_stilus_proba.py foldrajz_7_kolumbusz --stilus 3
        Csak a 3-as stílusban.

    Utána nyisd meg: kartya_kepek_uj/stilusproba/valaszto.html
"""

from __future__ import annotations

import argparse
import base64
import html
import os
import sys

GYOKER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, GYOKER)

CEL_MAPPA = os.path.join(GYOKER, "kartya_kepek_uj", "stilusproba")
MODELL = "gpt-image-2"
MERET = "1024x1024"

# ── A STÍLUSOK ─────────────────────────────────────────────────────────────
# Szándékosan TÁVOL vannak egymástól. Nem az a cél, hogy mind jó legyen,
# hanem hogy a gyerek egyértelműen tudjon választani közülük.
STILUSOK = [
    # 2026-09-21: az 1-es tetszett, de „kicsit olyan mint a festmény".
    # A meglévő kártyákon (Newton, Mengyelejev) az arc LAPOS, ÉLES
    # színsíkokból áll, nem elmosott ecsetvonásokból. Ezért ki az
    # ecsetkezelés, be a szögletes, posterizált színfolt.
    # 2026-09-21 este: Sándornak az EREDETI 1-es tetszett. Az „élesebb"
    # változat rosszabb lett. Ezért visszaállítva az eredeti szöveg, és
    # csak KÉT szó jött hozzá a meglévő kártyák felé: sötétebb háttér és
    # merészebb szín az árnyékban. Ennél többet nem mozdítunk rajta.
    ("festett",
     "Festett hős – mint a mostani kártyáid",
     # 2026-09-21: a „sötétebb hangulat" és a „merészebb árnyékszín"
     # klasszikus olajfestménybe fordította. VISSZA az eredetire, és
     # ide többet NEM írunk hozzá – ez az a szöveg, ami tetszett.
     "rich painterly digital illustration, confident brushwork, deep "
     "saturated colours, strong rim light, dramatic contrast, the person "
     "at work with their real instrument, detailed background"),

    ("kepregeny",
     "Képregény – vastag tus, erős árnyék",
     "bold american comic book illustration, heavy black ink outlines, "
     "flat cel shading, halftone dot texture, punchy primary colours, "
     "dramatic low angle, dynamic action pose, speed lines"),

    ("retro",
     "Retro plakát – lapos formák, kevés szín",
     "retro screen print poster art, flat geometric shapes, limited "
     "palette of four bold colours, thick clean outlines, strong "
     "silhouette, mid-century graphic design, slight paper grain"),

    ("rajzfilm3d",
     "3D rajzfilm – mint egy animációs film",
     "stylised 3d animated film character, soft rounded forms, appealing "
     "friendly design, subsurface skin shading, cinematic studio "
     "lighting, shallow depth of field, polished render"),

    ("sotet_kartya",
     "Sötét gyűjtőkártya – drámai, felnőttes",
     "dramatic fantasy trading card illustration, dark moody background, "
     "single strong light source, volumetric light rays, intricate "
     "detail, epic heroic framing, muted background and one vivid accent "
     "colour"),

    ("pixel",
     "Pixelgrafika – retro játék",
     "detailed pixel art character portrait, 64 by 64 pixel grid look, "
     "limited retro game palette, crisp hard pixel edges, simple flat "
     "background, 16-bit video game sprite style"),
]

KOZOS = ("square composition with margin, the whole head and shoulders "
         "inside the frame, face clearly visible")

TILTAS = ("No text, no letters, no numbers, no words, no captions, no "
          "signature, no watermark, no logo, no border, no frame, "
          "no modern clothing.")


def kartya_keres(nev: str) -> dict:
    import kartyak
    nev = nev.replace(".png", "")
    for k in kartyak.KARTYAK:
        if k.get("kep") == nev:
            return k
    raise SystemExit(f"Nincs ilyen kártya: {nev}")


def prompt(k: dict, stilus: str) -> str:
    alany = (k.get("prompt") or "").strip()
    if not alany:
        alany = f"{k.get('nev', '')}, {k.get('alnev', '')}".strip(" ,")
    return f"{stilus}, {KOZOS}. {alany} {TILTAS}"


def fajl(k: dict, i: int, kulcs: str) -> str:
    return os.path.join(CEL_MAPPA, f"{k.get('kep')}__{i}_{kulcs}.png")


def szabad_fajl(k: dict, i: int, kulcs: str) -> str:
    """Mindig SZABAD fájlnevet ad, soha nem ír felül semmit.

    Windowson a felülírás elszállt [Errno 22]-vel, ha a képet épp nyitva
    tartotta egy képnézegető – és akkor a kész, KIFIZETETT kép veszett el.
    Ráadásul így a régi változat is megmarad összehasonlításnak.
    """
    alap = fajl(k, i, kulcs)
    if not os.path.exists(alap):
        return alap
    torzs = alap[:-4]
    n = 2
    while os.path.exists(f"{torzs}_{n}.png"):
        n += 1
    return f"{torzs}_{n}.png"


def valaszto_oldal(k: dict) -> str:
    # Minden képet felsorolunk, ami ehhez a kártyához készült – az újabb
    # változatokat is (…_2.png, …_3.png), hogy össze tudd hasonlítani.
    elotag = f"{k.get('kep')}__"
    nevek = sorted(f for f in os.listdir(CEL_MAPPA)
                   if f.startswith(elotag) and f.endswith(".png"))
    darabok = []
    for nev in nevek:
        darabok.append(
            f'<figure><img src="{html.escape(nev)}" alt="">'
            f'<figcaption>{html.escape(nev[len(elotag):-4])}</figcaption></figure>'
        )
    return (
        '<!doctype html><meta charset="utf-8"><title>Stílusválasztó</title>'
        "<style>body{margin:0;background:#12161c;color:#e8eef5;padding:24px;"
        "font:15px/1.5 system-ui,-apple-system,'Segoe UI',sans-serif}"
        "h1{font-size:20px;margin:0 0 4px}p{color:#93a4b5;margin:0 0 20px}"
        ".racs{display:grid;grid-template-columns:repeat(auto-fill,"
        "minmax(260px,1fr));gap:18px}"
        "figure{margin:0;background:#1b212a;border:1px solid #2b3542;"
        "border-radius:14px;overflow:hidden}"
        "img{width:100%;display:block;aspect-ratio:1/1;object-fit:cover}"
        "figcaption{padding:10px 12px;font-size:14px}</style>"
        f"<h1>Melyik tetszik a legjobban?</h1>"
        f"<p>{html.escape(str(k.get('nev','')))} – ugyanaz a kártya, "
        f"{len(darabok)} stílusban. Mondd meg a SZÁMÁT.</p>"
        f"<div class='racs'>{''.join(darabok)}</div>"
    )


def main() -> int:
    ert = argparse.ArgumentParser(description="Egy kártya több stílusban")
    ert.add_argument("kartya", nargs="?", default="",
                     help="a kártya fájlneve, pl. foldrajz_7_kolumbusz")
    ert.add_argument("--stilus", type=int, default=0,
                     help="csak ez az egy stílus (1-től)")
    ert.add_argument("--lista", action="store_true",
                     help="csak kiírja a stílusokat, nem hív API-t")
    args = ert.parse_args()

    if args.lista or not args.kartya:
        print("Stílusok:")
        for i, (_, cim, szoveg) in enumerate(STILUSOK, 1):
            print(f"  {i}. {cim}\n     {szoveg}\n")
        if not args.kartya:
            print("Adj meg egy kártyát, pl.:")
            print("  python kartya_stilus_proba.py foldrajz_7_kolumbusz")
        return 0

    k = kartya_keres(args.kartya)
    valasztott = list(enumerate(STILUSOK, 1))
    if args.stilus:
        valasztott = [x for x in valasztott if x[0] == args.stilus]
        if not valasztott:
            print(f"Nincs {args.stilus}. stílus.")
            return 1

    kulcs = os.environ.get("OPENAI_API_KEY", "").strip()
    if not kulcs:
        print("Hiányzik az OPENAI_API_KEY.")
        return 1
    try:
        from openai import OpenAI
    except ImportError:
        print("Hiányzik az openai csomag. Telepítsd: pip install openai")
        return 1

    kliens = OpenAI(api_key=kulcs)
    os.makedirs(CEL_MAPPA, exist_ok=True)
    print(f"{k.get('nev')} – {len(valasztott)} kép készül.")

    sikeres = []
    for i, (kcs, cim, szoveg) in valasztott:
        print(f"  {i}. {cim} …", flush=True)
        try:
            valasz = kliens.images.generate(
                model=MODELL, prompt=prompt(k, szoveg), size=MERET, n=1)
            elem = valasz.data[0]
            b64 = getattr(elem, "b64_json", None)
            if b64:
                adat = base64.b64decode(b64)
            else:
                import urllib.request
                with urllib.request.urlopen(elem.url, timeout=60) as v:
                    adat = v.read()
            ut_kep = szabad_fajl(k, i, kcs)
            with open(ut_kep, "wb") as f:
                f.write(adat)
            sikeres.append(ut_kep)
            print(f"     -> {os.path.basename(ut_kep)}")
        except Exception as exc:
            print(f"     HIBA: {exc}")
            print("     A kép NEM készült el. Ha a hiba [Errno 22] vagy")
            print("     [Errno 13], zárd be a képnézegetőt, és futtasd újra.")

    if not sikeres:
        print("\nNEM KÉSZÜLT EGYETLEN KÉP SEM. Lásd a fenti HIBA sorokat.")
        return 1

    ut = os.path.join(CEL_MAPPA, "valaszto.html")
    try:
        with open(ut, "w", encoding="utf-8") as f:
            f.write(valaszto_oldal(k))
        print(f"\n{len(sikeres)} kép kész. Nyisd meg: {ut}")
    except Exception as exc:
        print(f"\n{len(sikeres)} kép kész, de a valaszto.html nem: {exc}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
