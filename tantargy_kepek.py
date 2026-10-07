# -*- coding: utf-8 -*-
"""TutorIA – KÉPEK A TÖBBI TANTÁRGYHOZ (környezet, természet, történelem…)

Ugyanaz a stílus és ugyanaz a menet, mint a nyelvi képes szótárnál
(szokep_generalas.py), csak itt a szavakat NEM kézzel írjuk össze, hanem
a tantervből szedi ki a program, három lépésben.

1. LÉPÉS – MIRŐL LEGYEN KÉP? (olcsó, kb. 1–2 $ az egész)
    python tantargy_kepek.py --fogalmak
        Végigmegy minden tantárgy minden témakörén (magyar 1–8, spanyol
        1–6), és egy AI-val kiíratja, mi az a néhány LERAJZOLHATÓ dolog,
        amit a gyerek abban a témakörben tanul (pl. „Az emberi test" →
        szív, tüdő, csontváz). A lista a kep_fogalmak mappába kerül,
        tantárgyanként egy fájlba. Kép még NEM készül.
    python tantargy_kepek.py --fogalmak --tantargy kornyezetismeret
        Csak egy tantárgy (a fájlnév eleje elég, ékezet nélkül).

    Nézd meg a kep_fogalmak/*.json fájlokat (Jegyzettömbbel megnyithatók).
    Ami nem kell, azt egyszerűen töröld ki a fájlból, vagy hagyd, és a
    képnél dobd ki.

2. LÉPÉS – KÉPEK GYÁRTÁSA (képenként kb. 2–4 cent)
    python tantargy_kepek.py --lista
        Kiírja, hány kép készülne, mennyibe kerülne. Ingyenes.
    python tantargy_kepek.py --gyart --db 5
        Öt próbakép. Ha tetszik:
    python tantargy_kepek.py --gyart
        Az összes hiányzó kép. Tantárgyanként külön mappába kerülnek:
        szokep_uj/<tantárgy>/…png. Amihez a nyelvi szótárban MÁR VAN kép
        (pl. alma, fa), azt nem gyártja le újra.
    python tantargy_kepek.py --gyart --tantargy biologia

3. LÉPÉS – ÁTNÉZÉS, JÓVÁHAGYÁS
    Nyisd meg: szokep_uj/<tantárgy>/attekinto.html
    Pipáld ki a jókat, a gomb kiírja a parancsot, például:
    python tantargy_kepek.py --jovahagy biologia:heart,lungs,skeleton
        A jó képek kicsinyítve a static/szokepek/<tantárgy> mappába kerülnek.
    Rossz képet újra lehet kérni:
    python tantargy_kepek.py --gyart --tantargy biologia --csak heart --ujra

MI KELL HOZZÁ: ugyanaz, mint a szótárnál – OPENAI_API_KEY és a Pillow.
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys
import time

GYOKER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, GYOKER)
# A stílus, a tiltólista és a képgyártás UGYANAZ, mint a nyelvi szótárnál –
# így az összes kép egy szettnek látszik.
import szokep_generalas as SZ  # noqa: E402

FOGALOM_MAPPA = os.path.join(GYOKER, "kep_fogalmak")
UJ_MAPPA = os.path.join(GYOKER, "szokep_uj")
VEGLEGES = os.path.join(GYOKER, "static", "szokepek")
SZOVEG_MODELL = "gpt-5.4-mini"   # a fogalmak kiírásához – olcsó és elég
PER_TEMA = 5                     # legfeljebb ennyi kép témakörönként

# Mely tantervi fájlok kellenek. A nyelvieket kihagyjuk – azokhoz a
# szokep_generalas.py csinál képet.
KIHAGY = ("idegen", "angol", "nemet", "spanyol", "extranjera", "kozossegi")


def _ascii(s: str) -> str:
    t = s.lower()
    for a, b in zip("áéíóöőúüűñ", "aeiooouuun"):
        t = t.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "_", t).strip("_")


def tanterv_fajlok() -> list[tuple[str, str, str]]:
    """[(tantárgy-kulcs, oldal 'hu'/'es', fájl útja)]"""
    ki = []
    for ut in glob.glob(os.path.join(GYOKER, "hu_kerettanterv_1_4_TELJES", "hu_kerettanterv_1_4_TELJES", "*_1_4.json")):
        ki.append(("hu", ut))
    for ut in glob.glob(os.path.join(GYOKER, "hu_kerettanterv_5_8_TELJES", "*-5-8.json")):
        ki.append(("hu", ut))
    for ut in glob.glob(os.path.join(GYOKER, "es_kerettanterv", "*.json")):
        ki.append(("es", ut))
    lista = []
    for oldal, ut in sorted(ki):
        nev = os.path.basename(ut)
        if any(x in nev.lower() for x in KIHAGY):
            continue
        kulcs = _ascii(re.sub(r"(_1_4|-5-8|_1-6|_5-6|\.json|es_lomloe_)", "", nev.lower()))
        if oldal == "es":
            kulcs = "es_" + kulcs
        else:                       # a matematika 1–4 és 5–8 két külön fájl
            kulcs += "_1_4" if "_1_4" in nev else "_5_8"
        lista.append((kulcs, oldal, ut))
    return lista


def temakorok(ut: str) -> list[dict]:
    """A fájl összes témaköre: [{evfolyam, nev, szoveg}] – bármilyen szerkezetből."""
    with open(ut, encoding="utf-8") as f:
        adat = json.load(f)
    ki = []

    def bejar(o, evf=None):
        if isinstance(o, dict):
            if "temakorok_by_grade" in o and isinstance(o["temakorok_by_grade"], dict):
                for g, lst in o["temakorok_by_grade"].items():
                    for t in lst or []:
                        felvesz(t, g)
                return          # a ciklus-szintű összefoglalót kihagyjuk
            for k, v in o.items():
                if k == "temakorok" and isinstance(v, list):
                    for t in v:
                        felvesz(t, evf)
                elif isinstance(v, (dict, list)):
                    bejar(v, k if k.isdigit() else evf)
        elif isinstance(o, list):
            for v in o:
                bejar(v, evf)

    def felvesz(t, evf):
        if not isinstance(t, dict) or not t.get("nev"):
            return
        reszek = [str(t.get("nev"))]
        if isinstance(t.get("fogalmak"), list):
            reszek.append("Fogalmak: " + ", ".join(map(str, t["fogalmak"])))
        if t.get("objetivo"):
            reszek.append(str(t["objetivo"]))
        reszek.append(str(t.get("teljes_szoveg", ""))[:1200])
        ki.append({"evfolyam": evf, "nev": str(t["nev"]), "szoveg": "\n".join(reszek)})

    bejar(adat)
    return ki


UTASITAS = (
    "You help build a picture dictionary for school children (age 6-14). "
    "Read the curriculum topic below and list at most {n} CONCRETE things the "
    "child learns about in this topic that can be drawn as ONE clear, "
    "unmistakable picture without any text (objects, animals, plants, body "
    "parts, tools, buildings, places, historical objects, natural phenomena). "
    "Skip abstract ideas, skills, feelings and anything that would need words "
    "or numbers to understand. If nothing is drawable, return an empty list. "
    "Answer ONLY with JSON: {{\"kepek\": [{{\"kulcs\": \"english_snake_case\", "
    "\"en\": \"english name\", \"hu\": \"magyar név\", \"es\": \"nombre en español\", "
    "\"alany\": \"short English description of exactly what to draw\"}}]}}"
)


def fogalmak_kiirasa(kliens, csak: str) -> int:
    os.makedirs(FOGALOM_MAPPA, exist_ok=True)
    for tkulcs, oldal, ut in tanterv_fajlok():
        if csak and not tkulcs.startswith(csak):
            continue
        cel = os.path.join(FOGALOM_MAPPA, tkulcs + ".json")
        if os.path.exists(cel):
            print(f"{tkulcs}: már megvan ({cel}) – töröld, ha újra kell")
            continue
        temak = temakorok(ut)
        print(f"{tkulcs}: {len(temak)} témakör …", flush=True)
        osszes, latott = [], set()
        for i, t in enumerate(temak, 1):
            try:
                v = kliens.chat.completions.create(
                    model=SZOVEG_MODELL,
                    response_format={"type": "json_object"},
                    messages=[{"role": "system", "content": UTASITAS.format(n=PER_TEMA)},
                              {"role": "user", "content": t["szoveg"]}],
                )
                kepek = json.loads(v.choices[0].message.content or "{}").get("kepek", [])
            except Exception as e:
                print(f"   ! {t['nev'][:50]}: {type(e).__name__}: {str(e)[:120]}")
                kepek = []
            for k in kepek[:PER_TEMA]:
                kk = _ascii(str(k.get("kulcs") or k.get("en") or ""))
                if not kk or kk in latott or not k.get("alany"):
                    continue
                latott.add(kk)
                osszes.append({"kulcs": kk, "en": k.get("en", ""), "hu": k.get("hu", ""),
                               "es": k.get("es", ""), "alany": k["alany"],
                               "evfolyam": t["evfolyam"], "temakor": t["nev"]})
            if i % 10 == 0:
                print(f"   {i}/{len(temak)} témakör, eddig {len(osszes)} kép", flush=True)
        with open(cel, "w", encoding="utf-8") as f:
            json.dump(osszes, f, ensure_ascii=False, indent=1)
        print(f"   → {len(osszes)} kép terve: {cel}")
    return 0


def tervek(csak: str) -> dict[str, list[dict]]:
    ki = {}
    for ut in sorted(glob.glob(os.path.join(FOGALOM_MAPPA, "*.json"))):
        t = os.path.splitext(os.path.basename(ut))[0]
        if csak and not t.startswith(csak):
            continue
        with open(ut, encoding="utf-8") as f:
            ki[t] = json.load(f)
    return ki


def mar_van_kep(kulcs: str) -> bool:
    """Bármelyik tantárgynál (vagy a nyelvi szótárban) van már ilyen kép?"""
    return bool(glob.glob(os.path.join(VEGLEGES, "*", kulcs + ".webp"))
                or glob.glob(os.path.join(UJ_MAPPA, "**", kulcs + ".png"), recursive=True))


def attekinto(tkulcs: str, lista: list[dict]) -> None:
    mappa = os.path.join(UJ_MAPPA, tkulcs)
    sz = []
    for f in lista:
        if os.path.exists(os.path.join(mappa, f["kulcs"] + ".png")):
            sz.append(f)
    # A nyelvi szótár átnézője jó ehhez is: csak a parancs más.
    import html as h
    kartyak = "".join(
        f'<label class="k"><img src="{f["kulcs"]}.png" loading="lazy"><span>'
        f'<input type="checkbox" value="{f["kulcs"]}"> <b>{h.escape(f.get("hu",""))}</b> · '
        f'{h.escape(f.get("es",""))} <small>({h.escape(str(f.get("temakor",""))[:60])})</small></span></label>'
        for f in sz)
    lap = f"""<!doctype html><meta charset="utf-8"><title>{tkulcs} – képek</title>
<style>body{{font-family:system-ui;background:#FBF5EA;margin:0;padding:20px}}
.racs{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:14px}}
.k{{background:#fff;border-radius:16px;padding:10px;cursor:pointer;box-shadow:0 4px 12px rgba(0,0,0,.08)}}
.k img{{width:100%;border-radius:10px;display:block}}.k span{{display:block;margin-top:8px;font-size:14px}}
#ki{{position:sticky;bottom:0;background:#0E2A1E;color:#fff;padding:14px;border-radius:14px;margin-top:20px}}
#ki code{{display:block;background:#fff;color:#000;padding:8px;margin-top:8px;word-break:break-all}}
button{{background:#F5A01E;color:#fff;border:0;border-radius:99px;padding:10px 18px;font-weight:800}}</style>
<h1>{tkulcs} – {len(sz)} kép</h1><p>Pipáld ki a JÓ képeket, nyomd meg a gombot, és másold be a parancsot.</p>
<div class="racs">{kartyak}</div>
<div id="ki"><button onclick="ir()">Parancs a kipipáltakhoz</button><code id="p"></code></div>
<script>function ir(){{var v=[].map.call(document.querySelectorAll('input:checked'),function(x){{return x.value}});
document.getElementById('p').textContent='python tantargy_kepek.py --jovahagy {tkulcs}:'+v.join(',');}}</script>"""
    with open(os.path.join(mappa, "attekinto.html"), "w", encoding="utf-8") as f:
        f.write(lap)


def gyartas(kliens, csak_t: str, csak_k: set, ujra: bool, db: int, csak_lista: bool) -> int:
    osszes = tervek(csak_t)
    if not osszes:
        print("Nincs még terv. Előbb: python tantargy_kepek.py --fogalmak")
        return 1
    tennivalo = []
    for tk, lista in osszes.items():
        for f in lista:
            if csak_k and f["kulcs"] not in csak_k:
                continue
            ut = os.path.join(UJ_MAPPA, tk, f["kulcs"] + ".png")
            if os.path.exists(ut) and not ujra:
                continue
            if not os.path.exists(ut) and not csak_k and mar_van_kep(f["kulcs"]):
                continue
            tennivalo.append((tk, f, ut))
    if db:
        tennivalo = tennivalo[:db]
    if csak_lista:
        for tk, f, _ in tennivalo:
            print(f"{tk:22} {f['kulcs']:24} {f.get('hu',''):22} → {f['alany'][:70]}")
        print(f"\n{len(tennivalo)} kép készülne. Becsült költség: kb. "
              f"{len(tennivalo)*0.02:.0f}–{len(tennivalo)*0.04:.0f} $.")
        return 0
    print(f"{len(tennivalo)} kép készül\n")
    for i, (tk, f, ut) in enumerate(tennivalo, 1):
        os.makedirs(os.path.dirname(ut), exist_ok=True)
        print(f"[{i}/{len(tennivalo)}] {tk}: {f.get('hu') or f['en']} …", flush=True)
        try:
            with open(ut, "wb") as ki:
                ki.write(SZ.generalas(kliens, {"alany": f["alany"], "kulcs": f["kulcs"]}))
        except Exception as e:
            print(f"   ! nem sikerült: {type(e).__name__}: {str(e)[:160]}")
            time.sleep(2)
    for tk, lista in osszes.items():
        if os.path.isdir(os.path.join(UJ_MAPPA, tk)):
            attekinto(tk, lista)
    print("\nKész. Nyisd meg: szokep_uj/<tantárgy>/attekinto.html")
    return 0


def jovahagyas(parancs: str) -> int:
    from PIL import Image
    tk, _, kulcsok = parancs.partition(":")
    lista = {f["kulcs"]: f for f in tervek(tk).get(tk, [])}
    cel = os.path.join(VEGLEGES, tk)
    os.makedirs(cel, exist_ok=True)
    index_ut = os.path.join(cel, "kepek.json")
    index = json.load(open(index_ut, encoding="utf-8")) if os.path.exists(index_ut) else {}
    db = 0
    for k in [x.strip() for x in kulcsok.split(",") if x.strip()]:
        forras = os.path.join(UJ_MAPPA, tk, k + ".png")
        if not os.path.exists(forras):
            print(f"  ! nincs ilyen kép: {tk}/{k}")
            continue
        kep = Image.open(forras).convert("RGB")
        kep.thumbnail((512, 512))
        kep.save(os.path.join(cel, k + ".webp"), "WEBP", quality=82, method=6)
        f = lista.get(k, {})
        index[k] = {x: f.get(x, "") for x in ("en", "hu", "es", "temakor", "evfolyam")}
        db += 1
        print(f"  ✓ {tk}/{k}")
    with open(index_ut, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=1, sort_keys=True)
    print(f"\n{db} kép jóváhagyva → static/szokepek/{tk}. Töltsd fel: git add static/szokepek")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="Tantárgyi képek")
    p.add_argument("--fogalmak", action="store_true", help="1. lépés: mire legyen kép")
    p.add_argument("--lista", action="store_true", help="kiírja, mi készülne (ingyenes)")
    p.add_argument("--gyart", action="store_true", help="2. lépés: képek gyártása")
    p.add_argument("--jovahagy", default="", help="3. lépés: tantargy:kulcs1,kulcs2")
    p.add_argument("--tantargy", default="", help="csak ez a tantárgy (a név eleje)")
    p.add_argument("--csak", default="", help="csak ezek a kulcsok, vesszővel")
    p.add_argument("--ujra", action="store_true")
    p.add_argument("--db", type=int, default=0)
    a = p.parse_args()

    if a.jovahagy:
        return jovahagyas(a.jovahagy)
    csak_k = {x.strip() for x in a.csak.split(",") if x.strip()}
    if a.lista:
        return gyartas(None, a.tantargy, csak_k, a.ujra, a.db, True)
    if not (a.fogalmak or a.gyart):
        p.print_help()
        return 0
    kulcs = os.environ.get("OPENAI_API_KEY")
    if not kulcs:
        print('Nincs OPENAI_API_KEY. Windowsban: setx OPENAI_API_KEY "ide-a-sajat-kulcsod" – és új ablak.')
        return 1
    from openai import OpenAI
    kliens = OpenAI(api_key=kulcs)
    if a.fogalmak:
        return fogalmak_kiirasa(kliens, a.tantargy)
    return gyartas(kliens, a.tantargy, csak_k, a.ujra, a.db, False)


if __name__ == "__main__":
    sys.exit(main())
