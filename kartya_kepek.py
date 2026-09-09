# -*- coding: utf-8 -*-
"""
TutorIA – tudáskártya-képek legyártása sorban, OpenAI kép-API-val.

MIÉRT VAN EZ
    A Leonardo szövegből próbálja kitalálni, KI van a képen, és a kevésbé
    ismert alakoknál (Bolyai, Kőrösi Csoma, Semmelweis) rendre mellényúl.
    Egy kártya így két nap. Az OpenAI kép-modellje sokkal pontosabban követi
    a leírást, és mivel API-ból hívható, egyszerre végig lehet menni az
    összes hiányzó kártyán.

MIT CSINÁL
    1. Végigmegy a kartyak.py (és kartyak_es.py) listáján.
    2. Megnézi, melyik kártyához NINCS még kép a static/kartyak alatt.
    3. Mindegyikhez összerak egy promptot: a kártya saját "prompt" mezője
       + egy KÖZÖS stílusblokk, hogy minden kártya egyforma legyen.
    4. Legenerálja, és egy ÚJ mappába menti: kartya_kepek_uj/<oldal>/

    A static/kartyak mappához HOZZÁ SEM NYÚL. Te nézed át a kész képeket,
    és te mozgatod be azokat, amik tetszenek.

HASZNÁLAT
    python kartya_kepek.py                  – minden hiányzó kártya
    python kartya_kepek.py --db 3           – csak az első 3 (próbának!)
    python kartya_kepek.py --csak curie     – csak amiben benne van a szó
    python kartya_kepek.py --ujra           – a meglévőket is újragyártja
    python kartya_kepek.py --minta a.png b.png
                                            – stílusminta-képek: a modell
                                              ezek festésmódját veszi át

    ELSŐ ALKALOMMAL mindig --db 2 -vel indítsd. Nézd meg a két képet, és
    csak utána engedd rá a többire.

KÖLTSÉG
    Kártyánként durván 4 amerikai cent. A 26 magyar kártya kb. egy euró.
    A script minden kép után kiírja, hol tart, tehát bármikor megállíthatod
    Ctrl+C-vel – a kész képek megmaradnak.
"""

from __future__ import annotations

import argparse
import base64
import os
import sys
import time
from pathlib import Path

GYOKER = Path(__file__).resolve().parent
KIMENET = GYOKER / "kartya_kepek_uj"
MEGLEVO = GYOKER / "static" / "kartyak"


# ── A KÖZÖS STÍLUS ──────────────────────────────────────────────────────────
# Ez a rész MINDEN kártyához hozzáfűződik, ezért néz ki az összes egyformán.
# A megfogalmazás a már elkészült, jónak ítélt kártyáid alapján készült:
# festett digitális illusztráció, meleg fény szemben hideg háttérrel, erős
# kontúrfény a bőrön és a hajon, sötét háttér, derékig érő beállítás.
#
# HA MÁSMILYEN STÍLUST AKARSZ, csak ezt a szöveget írd át – a script többi
# részéhez nem kell hozzányúlni.
STILUS = (
    "Painterly digital illustration in the style of a collectible trading card. "
    "Waist-up portrait, subject turned slightly to one side, looking off-camera "
    "with a calm, serious expression. Rich oil-paint brushwork with visible "
    "strokes. Dramatic lighting: a warm golden key light on the face and hands, "
    "set against a deep teal and dark blue background. Strong rim light along "
    "the hair and shoulders. Saturated but harmonious colours. Period-accurate "
    "clothing and setting, historically researched. No text, no letters, no "
    "numbers, no watermark, no signature, no border, no frame. Square "
    "composition, the head in the upper third."
)

# Amit biztosan NE csináljon. A kép-modellek egy része figyelembe veszi.
TILTOTT = (
    "Avoid: cartoon, anime, 3D render, photograph, modern clothing, "
    "text or lettering anywhere in the image, deformed hands, extra fingers."
)


def _stilus_prompt(kartya: dict) -> str:
    """A kártya saját leírása + a közös stílus. Ez megy ki a modellnek."""
    sajat = (kartya.get("prompt") or "").strip()
    nev = (kartya.get("nev") or "").strip()
    alnev = (kartya.get("alnev") or "").strip()

    # A nevet KÜLÖN is kiírjuk az elejére: a modell így nagyobb eséllyel a
    # valódi arcot idézi fel, nem csak a ruhaleírásból épít valakit.
    fej = f"A portrait of {nev}"
    if alnev:
        fej += f" ({alnev})"
    fej += "."

    return f"{fej} {sajat}\n\n{STILUS}\n\n{TILTOTT}"


# ── A KÁRTYALISTA ÖSSZESZEDÉSE ──────────────────────────────────────────────
def _kartyak() -> list[dict]:
    """A magyar és (ha van) a spanyol kártyalista egyben."""
    sys.path.insert(0, str(GYOKER))
    osszes: list[dict] = []

    import kartyak  # noqa: E402
    osszes.extend(kartyak.KARTYAK)

    try:
        import kartyak_es  # noqa: E402
        osszes.extend(kartyak_es.KARTYAK)
    except Exception:
        print("[i] kartyak_es.py nincs meg vagy nem olvasható – kihagyva.")

    return osszes


def _van_mar_kepe(kartya: dict) -> bool:
    """Van-e már kész kép ehhez a kártyához a static/kartyak alatt?"""
    oldal = kartya.get("oldal") or "hu"
    kep = kartya.get("kep") or ""
    if not kep:
        return True  # nincs fájlnév → nem tudjuk generálni, hagyjuk békén
    for kit in (".png", ".jpg", ".jpeg", ".webp"):
        if (MEGLEVO / oldal / f"{kep}{kit}").exists():
            return True
    return False


# ── A GENERÁLÁS ─────────────────────────────────────────────────────────────
def _kliens():
    kulcs = os.environ.get("OPENAI_API_KEY")
    if not kulcs:
        print("HIBA: nincs OPENAI_API_KEY környezeti változó.\n"
              "Windows PowerShell-ben egy alkalomra:\n"
              '    $env:OPENAI_API_KEY = "sk-..."')
        sys.exit(1)
    try:
        from openai import OpenAI
    except ImportError:
        print("HIBA: nincs telepítve az openai csomag.  pip install openai")
        sys.exit(1)
    return OpenAI(api_key=kulcs, timeout=180.0, max_retries=1)


def _general(kliens, prompt: str, minta: list[Path], meret: str,
             minoseg: str) -> bytes:
    """Egy kép legyártása. Ha van stílusminta, azzal dolgozik."""
    if minta:
        # Stílusminta-mód: a modell megkapja a mintaképeket, és azok
        # festésmódját viszi tovább. Ez a legbiztosabb út ahhoz, hogy az
        # összes kártya EGYFORMA legyen.
        fajlok = [open(p, "rb") for p in minta]
        try:
            valasz = kliens.images.edit(
                model="gpt-image-1",
                image=fajlok,
                prompt=("Create a NEW illustration described below, painted in "
                        "exactly the same style, palette and lighting as the "
                        "reference images.\n\n" + prompt),
                size=meret,
                quality=minoseg,
            )
        finally:
            for f in fajlok:
                f.close()
    else:
        valasz = kliens.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size=meret,
            quality=minoseg,
        )
    return base64.b64decode(valasz.data[0].b64_json)


def main() -> None:
    ap = argparse.ArgumentParser(description="TutorIA kártyaképek gyártása")
    ap.add_argument("--db", type=int, default=0,
                    help="legfeljebb ennyi kártyát csinál (0 = mind)")
    ap.add_argument("--csak", default="",
                    help="csak azok, amiknek a nevében/azonosítójában benne van")
    ap.add_argument("--ujra", action="store_true",
                    help="a már meglévő képűeket is újragyártja")
    ap.add_argument("--minta", nargs="*", default=[],
                    help="stílusminta-képek (1-3 fájl)")
    ap.add_argument("--meret", default="1024x1024")
    ap.add_argument("--minoseg", default="high", choices=["low", "medium", "high"])
    args = ap.parse_args()

    minta = [Path(m) for m in args.minta]
    for m in minta:
        if not m.exists():
            print(f"HIBA: nincs meg a mintakép: {m}")
            sys.exit(1)
    if len(minta) > 3:
        print("HIBA: legfeljebb 3 mintaképet adj meg.")
        sys.exit(1)

    osszes = _kartyak()
    szuro = args.csak.strip().lower()

    tennivalo = []
    for k in osszes:
        if not (k.get("prompt") or "").strip():
            continue
        if szuro and szuro not in (
                (k.get("id", "") + " " + k.get("nev", "") + " "
                 + k.get("kep", "")).lower()):
            continue
        if not args.ujra and _van_mar_kepe(k):
            continue
        tennivalo.append(k)

    if args.db > 0:
        tennivalo = tennivalo[:args.db]

    if not tennivalo:
        print("Nincs mit csinálni: minden kártyának van már képe.\n"
              "(Ha mégis újra akarod gyártani: --ujra)")
        return

    print(f"Legyártandó: {len(tennivalo)} kártya"
          + (f"  |  stílusminta: {len(minta)} kép" if minta else "")
          + f"  |  minőség: {args.minoseg}")
    print(f"A kész képek ide kerülnek: {KIMENET}")
    print("A static/kartyak mappához a script NEM nyúl.\n")

    kliens = _kliens()
    kesz, hiba = 0, 0

    for i, k in enumerate(tennivalo, 1):
        oldal = k.get("oldal") or "hu"
        nev = k.get("nev") or k.get("kep")
        cel_mappa = KIMENET / oldal
        cel_mappa.mkdir(parents=True, exist_ok=True)
        cel = cel_mappa / f"{k['kep']}.png"

        print(f"[{i}/{len(tennivalo)}] {nev} … ", end="", flush=True)
        t0 = time.monotonic()
        try:
            adat = _general(kliens, _stilus_prompt(k), minta,
                            args.meret, args.minoseg)
            cel.write_bytes(adat)
            kesz += 1
            print(f"kész ({time.monotonic() - t0:.0f}s)  →  {cel.name}")
        except KeyboardInterrupt:
            print("\nMegszakítva. A már kész képek megmaradtak.")
            break
        except Exception as exc:
            hiba += 1
            print(f"HIBA: {type(exc).__name__}: {exc}")
            # Az OpenAI kliens egymásba csomagolja a hibákat, és a külső
            # réteg ("Connection error") semmit nem mond meg. A valódi ok
            # (tanúsítvány, tűzfal, DNS, proxy) beljebb van – kibontjuk.
            _e = exc.__cause__ or exc.__context__
            _melyseg = 0
            while _e is not None and _melyseg < 5:
                print(f"        oka: {type(_e).__name__}: {_e}")
                _e = _e.__cause__ or _e.__context__
                _melyseg += 1
            continue

    print(f"\nVége. Kész: {kesz}, hiba: {hiba}.")
    if kesz:
        print(f"Nézd át őket itt: {KIMENET}")
        print("Ami tetszik, azt te másold be a static/kartyak megfelelő "
              "mappájába – a fájlnév már jó, nem kell átnevezni.")


if __name__ == "__main__":
    main()
