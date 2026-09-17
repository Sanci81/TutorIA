# -*- coding: utf-8 -*-
"""TutorIA – kártyaképek generálása EGY közös stílussal.

MIÉRT VAN EZ
    Eddig kártyánként külön promptot kaptál, és azokat egyesével másoltad be
    valahova. Ettől minden kép MÁS stílusú lett – és pont az veszett el,
    amitől gyűjtemény lenne. Egy Pokémon-szett attól néz ki szettnek, hogy
    mind a hatvan lap ugyanabban a rajzstílusban készült.

    Ez a program ezt csinálja meg: a stílusleírás EGY helyen van (lent, a
    STILUS-ban), és minden kártya ugyanazt kapja. Csak az alany más – azt a
    kartyak.py „prompt" mezője adja, ami már meg van írva mind az 52-höz.

MIT NEM CSINÁL
    NEM ír a static/kartyak mappába. Külön mappába dolgozik
    (kartya_kepek_uj), és te mozgatod át, amit elfogadtál. Ez szándékos:
    a hídon keresztül nem lehet átnevezni és törölni, ezért ott a hibás
    fájl örökre ottmaradna.

HASZNÁLAT
    python kartya_kepek_generalas.py --lista
        Kiírja, milyen prompttal dolgozna. NEM hív API-t, nem kerül semmibe.

    python kartya_kepek_generalas.py --db 3
        Legyárt három képet próbának. Nézd meg, tetszik-e a stílus.

    python kartya_kepek_generalas.py
        Legyártja az ÖSSZES hiányzó képet.

    python kartya_kepek_generalas.py --csak kemia_7_curie --ujra
        Egyetlen képet csinál újra.

    Utána nyisd meg: kartya_kepek_uj/attekinto.html

MI KELL HOZZÁ
    Az OPENAI_API_KEY környezeti változóban a saját kulcsod. Windowsban:
        setx OPENAI_API_KEY "sk-..."
    és nyiss egy ÚJ PowerShell ablakot.
"""

from __future__ import annotations

import argparse
import base64
import html
import io
import os
import sys
import time

GYOKER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, GYOKER)

CEL_MAPPA = os.path.join(GYOKER, "kartya_kepek_uj")

# A modell neve. Ha a fiókodon más érhető el, EZT az egy sort kell átírni.
MODELL = "gpt-image-1"
MERET = "1024x1024"

# ── A KÖZÖS STÍLUS ─────────────────────────────────────────────────────────
# Ez a kártyaműhelyben eldöntött „A – HŐSPILLANAT" irány. Minden kép ezt
# kapja meg, szóról szóra ugyanúgy. Ha a szett stílusát változtatni akarod,
# CSAK ezt írd át – és akkor az egészet újra kell generálni, mert félig
# régi, félig új stílusú szett rosszabb, mint bármelyik önmagában.
STILUS = (
    "dynamic trading card hero art, a decisive moment of discovery, "
    "three-quarter action pose, low heroic camera angle, the subject caught "
    "mid-gesture and leaning into the light, strong dramatic key light with "
    "deep shadows, glowing energy swirling around their hands and their "
    "work, sparks and drifting light motes, bold saturated colours, high "
    "contrast, painterly digital illustration, visible brush strokes, "
    "cinematic depth, the whole figure and head inside a square frame with "
    "margin, centred composition"
)

# Amit SOHA nem akarunk a képen. A modell hajlamos aláírni a művét, és
# feliratot tenni rá – a kártyán viszont a keret adja a szöveget.
TILTAS = (
    "No text, no letters, no numbers, no words, no captions, no signature, "
    "no watermark, no logo, no border, no frame, no modern clothing, "
    "not a photograph."
)


def prompt_kartyahoz(k: dict) -> str:
    """A közös stílus + ennek a kártyának a saját leírása."""
    alany = (k.get("prompt") or "").strip()
    if not alany:
        # Ha nincs kézzel írt leírás, a név és az alcím is elég kiindulásnak.
        alany = f"{k.get('nev', '')}, {k.get('alnev', '')}".strip(" ,")
    return f"{STILUS}. {alany} {TILTAS}"


def fajl_utja(k: dict) -> str:
    return os.path.join(CEL_MAPPA, k.get("oldal", "hu"), f"{k.get('kep')}.png")


def kartyak_listaja() -> list[dict]:
    import kartyak
    lista = getattr(kartyak, "KARTYAK", None)
    if not isinstance(lista, list):
        raise SystemExit("Nem találom a KARTYAK listát a kartyak.py-ban.")
    return lista


def mar_megvan(k: dict) -> bool:
    """Igaz, ha VAGY a végleges helyen, VAGY az új mappában már van kép."""
    vegleges = os.path.join(GYOKER, "static", "kartyak",
                            k.get("oldal", "hu"), f"{k.get('kep')}.png")
    return os.path.exists(vegleges) or os.path.exists(fajl_utja(k))


def generalas(kliens, k: dict) -> bytes:
    """Egy kép. Bájtokat ad vissza, vagy kivételt dob."""
    valasz = kliens.images.generate(
        model=MODELL,
        prompt=prompt_kartyahoz(k),
        size=MERET,
        n=1,
    )
    elem = valasz.data[0]
    b64 = getattr(elem, "b64_json", None)
    if b64:
        return base64.b64decode(b64)
    # Néhány modell URL-t ad vissza b64 helyett.
    url = getattr(elem, "url", None)
    if url:
        import urllib.request
        with urllib.request.urlopen(url, timeout=60) as v:
            return v.read()
    raise RuntimeError("A válaszban nincs se kép, se URL.")


def attekinto_oldal(kartyak_lista: list[dict]) -> str:
    """Egyszerű lap, ahol egyben végignézed, mi készült el."""
    darabok = []
    for k in kartyak_lista:
        ut = fajl_utja(k)
        if not os.path.exists(ut):
            continue
        rel = os.path.relpath(ut, CEL_MAPPA).replace("\\", "/")
        darabok.append(
            f'<figure><img src="{html.escape(rel)}" alt="">'
            f'<figcaption><b>{html.escape(str(k.get("nev", "")))}</b><br>'
            f'<span>{html.escape(str(k.get("alnev", "")))}</span><br>'
            f'<code>{html.escape(str(k.get("kep", "")))}.png</code>'
            f'</figcaption></figure>'
        )
    return (
        '<!doctype html><meta charset="utf-8"><title>Kártyaképek – áttekintő</title>'
        "<style>"
        "body{margin:0;background:#12161c;color:#e8eef5;padding:24px;"
        "font:15px/1.5 system-ui,-apple-system,'Segoe UI',sans-serif}"
        "h1{font-size:20px;margin:0 0 6px}"
        "p.be{color:#93a4b5;margin:0 0 22px;max-width:70ch}"
        ".racs{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:18px}"
        "figure{margin:0;background:#1b212a;border:1px solid #2b3542;"
        "border-radius:14px;overflow:hidden}"
        "img{width:100%;display:block;aspect-ratio:1/1;object-fit:cover}"
        "figcaption{padding:10px 12px;font-size:13px}"
        "figcaption span{color:#93a4b5}"
        "code{color:#7fd4a8;font-size:11.5px}"
        "</style>"
        "<h1>Kártyaképek – áttekintő</h1>"
        "<p class='be'>Ezek MÉG NEM élesek. Amelyik jó, azt másold át a "
        "<code>static/kartyak</code> mappába ugyanezzel a fájlnévvel. "
        "Amelyik nem jó, futtasd újra: "
        "<code>python kartya_kepek_generalas.py --csak &lt;fájlnév&gt; --ujra</code></p>"
        f"<div class='racs'>{''.join(darabok)}</div>"
    )


def main() -> int:
    ert = argparse.ArgumentParser(description="Kártyaképek egy közös stílussal")
    ert.add_argument("--lista", action="store_true",
                     help="csak kiírja a promptokat, nem hív API-t")
    ert.add_argument("--db", type=int, default=0,
                     help="legfeljebb ennyi képet csinál (próbához)")
    ert.add_argument("--csak", default="",
                     help="egyetlen kártya fájlneve, pl. kemia_7_curie")
    ert.add_argument("--ujra", action="store_true",
                     help="a meglévő képet is újragenerálja")
    args = ert.parse_args()

    kartyak_lista = kartyak_listaja()
    if args.csak:
        kartyak_lista = [k for k in kartyak_lista
                         if k.get("kep") == args.csak.replace(".png", "")]
        if not kartyak_lista:
            print(f"Nincs ilyen kártya: {args.csak}")
            return 1

    tennivalo = [k for k in kartyak_lista if args.ujra or not mar_megvan(k)]
    if args.db:
        tennivalo = tennivalo[:args.db]

    if args.lista:
        for k in tennivalo:
            print(f"\n── {k.get('nev')} ({k.get('kep')}.png)")
            print(prompt_kartyahoz(k))
        print(f"\nÖsszesen {len(tennivalo)} kép készülne. "
              f"Ez a felsorolás semmibe nem került.")
        return 0

    if not tennivalo:
        print("Minden kártyának van már képe. (--ujra kapcsolóval újra lehet.)")
        return 0

    try:
        from openai import OpenAI
    except Exception:
        print("Hiányzik az openai csomag. Telepítsd: pip install openai")
        return 1

    kulcs = os.environ.get("OPENAI_API_KEY", "").strip()
    if not kulcs:
        print("Nincs OPENAI_API_KEY környezeti változó.\n"
              '  setx OPENAI_API_KEY "sk-..."\n'
              "  majd NYISS EGY ÚJ PowerShell ablakot.")
        return 1
    kliens = OpenAI(api_key=kulcs)

    print(f"{len(tennivalo)} kép készül, modell: {MODELL}.")
    kesz = hiba = 0
    for i, k in enumerate(tennivalo, 1):
        ut = fajl_utja(k)
        os.makedirs(os.path.dirname(ut), exist_ok=True)
        print(f"[{i}/{len(tennivalo)}] {k.get('nev')} … ", end="", flush=True)
        try:
            adat = generalas(kliens, k)
            with open(ut, "wb") as f:
                f.write(adat)
            kesz += 1
            print("kész")
        except Exception as exc:
            hiba += 1
            print(f"HIBA – {exc!r}")
            # Egy hibás kép ne állítsa meg az egész sort.
            time.sleep(2)

    os.makedirs(CEL_MAPPA, exist_ok=True)
    io.open(os.path.join(CEL_MAPPA, "attekinto.html"), "w",
            encoding="utf-8").write(attekinto_oldal(kartyak_listaja()))

    print(f"\nKész: {kesz}, hiba: {hiba}.")
    print(f"Nézd meg: {os.path.join(CEL_MAPPA, 'attekinto.html')}")
    print("Amelyik jó, azt másold át a static/kartyak mappába.")
    return 1 if hiba else 0


if __name__ == "__main__":
    raise SystemExit(main())
