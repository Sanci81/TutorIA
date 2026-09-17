# -*- coding: utf-8 -*-
"""TutorIA – NÉMA ELLENŐR. AI nélkül, ezért ingyen és gyorsan.

MI EZ
    Végigmegy a projekt adatain, és listát ad arról, hol van baj. Nem javít
    semmit: csak megmutatja. Azért készült, mert a hibákat eddig a képernyőn
    kerestük egyesével, és úgy nyolc évfolyam × tizenkét tantárgy × két
    nyelv sosem lesz kész.

    Amit AI nélkül is meg lehet nézni, azt itt nézzük meg. Ami csak élő
    órából derül ki (a tanár mit mond), az NEM ide tartozik.

HASZNÁLAT
    python ellenor.py                 – minden ellenőrzés, emberi lista
    python ellenor.py --md jelentes.md – ugyanaz fájlba, Markdownban

MIT NÉZ MEG
    1. TANTERV     – van-e minden évfolyamhoz lecke, és értelmes-e az
                     óraszám. Innen derült ki a 4192 perces lecke.
    2. FORDÍTÁS    – minden kulcs megvan-e magyarul ÉS spanyolul, és
                     egyeznek-e a helyettesítők ({perc}, {napok}).
                     Ez az, ami miatt a spanyol oldal lemaradhat.
    3. SABLONOK    – minden .html értelmes Jinja-e.
    4. KIEJTÉS     – a leckecímeken és a szövegeken lefuttatjuk a
                     felolvasó előkészítőjét, és megnézzük, marad-e benne
                     olyan jel, amit rosszul mondana ki.
    5. KÁRTYÁK     – melyik kártyának nincs képe.

A kilépési kód 1, ha SÚLYOS hibát talált – így éjszakai futtatásnál is
látszik, hogy baj van.
"""

from __future__ import annotations

import argparse
import glob
import io
import json
import os
import re
import sys

GYOKER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, GYOKER)

# A lecke ennél hosszabb ideje biztosan tantervi ÉVES óraszám, nem egy lecke.
LECKE_MAX_PERC = 180


class Jelentes:
    """Összegyűjti a találatokat, és emberi sorrendben írja ki."""

    def __init__(self) -> None:
        self.tetelek: list[tuple[str, str, str]] = []   # (szint, terulet, szoveg)

    def hiba(self, terulet: str, szoveg: str) -> None:
        self.tetelek.append(("HIBA", terulet, szoveg))

    def figyelem(self, terulet: str, szoveg: str) -> None:
        self.tetelek.append(("FIGYELEM", terulet, szoveg))

    def rendben(self, terulet: str, szoveg: str) -> None:
        self.tetelek.append(("RENDBEN", terulet, szoveg))

    @property
    def sulyos(self) -> int:
        return sum(1 for sz, _, _ in self.tetelek if sz == "HIBA")

    def szoveg(self) -> str:
        sorok: list[str] = []
        for szint in ("HIBA", "FIGYELEM", "RENDBEN"):
            csoport = [t for t in self.tetelek if t[0] == szint]
            if not csoport:
                continue
            sorok.append(f"\n{'=' * 70}\n{szint}  ({len(csoport)} tétel)\n{'=' * 70}")
            terulet_elozo = ""
            for _, terulet, szov in csoport:
                if terulet != terulet_elozo:
                    sorok.append(f"\n-- {terulet} " + "-" * max(0, 66 - len(terulet)))
                    terulet_elozo = terulet
                sorok.append(f"   {szov}")
        return "\n".join(sorok)

    def markdown(self) -> str:
        sorok = ["# TutorIA – ellenőrzés", ""]
        for szint, cim in (("HIBA", "Hibák"), ("FIGYELEM", "Figyelmeztetések"),
                           ("RENDBEN", "Rendben")):
            csoport = [t for t in self.tetelek if t[0] == szint]
            if not csoport:
                continue
            sorok.append(f"## {cim} ({len(csoport)})")
            sorok.append("")
            terulet_elozo = ""
            for _, terulet, szov in csoport:
                if terulet != terulet_elozo:
                    sorok.append(f"**{terulet}**")
                    sorok.append("")
                    terulet_elozo = terulet
                sorok.append(f"- {szov}")
            sorok.append("")
        return "\n".join(sorok)


# ── 1. TANTERV ──────────────────────────────────────────────────────────────

def _tanterv_fajlok() -> list[tuple[str, tuple[int, ...]]]:
    """(fájl, mely évfolyamokon nézzük) párok."""
    ki: list[tuple[str, tuple[int, ...]]] = []
    for minta, evek in (
        ("hu_kerettanterv_1_4_TELJES/hu_kerettanterv_1_4_TELJES/*.json", (1, 2, 3, 4)),
        ("hu_kerettanterv_1_4_TELJES/*.json", (1, 2, 3, 4)),
        ("hu_kerettanterv_5_8_TELJES/*.json", (5, 6, 7, 8)),
    ):
        for f in sorted(glob.glob(os.path.join(GYOKER, minta))):
            if os.path.basename(f) == "index.json":
                continue
            ki.append((f, evek))
    return ki


def ellenoriz_tanterv(j: Jelentes) -> None:
    terulet = "Tanterv"
    try:
        import curriculum_loader as cl
    except Exception as exc:
        j.hiba(terulet, f"A curriculum_loader nem tölthető be: {exc!r}")
        return

    latott: set[str] = set()
    hosszu = 0
    ures_oraszam = 0
    ures_katalogus = 0
    osszes_lecke = 0

    for f, evek in _tanterv_fajlok():
        nev = os.path.basename(f)
        # A kisbetűs és a nagybetűs változat ugyanaz a tantárgy: elég egyszer.
        kulcs = re.sub(r"[^a-z]", "", nev.lower())[:18]
        if kulcs in latott:
            continue
        latott.add(kulcs)
        try:
            raw = json.load(io.open(f, encoding="utf-8"))
        except Exception as exc:
            j.hiba(terulet, f"{nev}: nem olvasható JSON – {exc!r}")
            continue

        for ev in evek:
            try:
                katalogus = cl.extract_topic_catalog(raw, ev, raw_data=raw)
            except Exception as exc:
                j.hiba(terulet, f"{nev} / {ev}. évfolyam: hibára fut – {exc!r}")
                continue
            if not katalogus:
                ures_katalogus += 1
                continue
            osszes_lecke += len(katalogus)
            for t in katalogus:
                ora = t.get("ora_szam") or 0
                perc = int(ora) * 60
                if perc > LECKE_MAX_PERC:
                    hosszu += 1
                    j.hiba(
                        terulet,
                        f"{nev} / {ev}. évf. / „{t.get('name', '')[:42]}”: "
                        f"{ora} óra = {perc} perc egy leckére. "
                        f"Ez évi óraszám, nem lecke.",
                    )
                elif perc == 0:
                    ures_oraszam += 1

    if ures_oraszam:
        j.figyelem(terulet, f"{ures_oraszam} leckénél nincs óraszám (0). "
                            f"Ezeknél nem tudjuk, mikor van vége a leckének.")
    if ures_katalogus:
        j.figyelem(terulet, f"{ures_katalogus} tantárgy-évfolyam párnál üres a "
                            f"leckelista. Ezeket a gyerek nem látja.")
    if not hosszu:
        j.rendben(terulet, f"Egyetlen lecke sem hosszabb {LECKE_MAX_PERC} percnél.")
    j.rendben(terulet, f"Összesen {osszes_lecke} lecke, {len(latott)} tantárgyfájl.")


# ── 2. FORDÍTÁSOK ───────────────────────────────────────────────────────────

_HELYETTESITO = re.compile(r"\{[a-zA-Z_]+\}")


def ellenoriz_forditasok(j: Jelentes) -> None:
    terulet = "Fordítások"
    try:
        import translations as tr
    except Exception as exc:
        j.hiba(terulet, f"A translations nem tölthető be: {exc!r}")
        return

    szotar = None
    for nev in ("TRANSLATIONS", "FORDITASOK", "T"):
        ertek = getattr(tr, nev, None)
        if isinstance(ertek, dict) and ertek:
            szotar = ertek
            break
    if szotar is None:
        j.hiba(terulet, "Nem találom a fordítási szótárat a translations.py-ban.")
        return

    hianyzo_es = hianyzo_hu = ures = 0
    for kulcs, ertek in szotar.items():
        if not isinstance(ertek, dict):
            continue
        hu = (ertek.get("hu") or "").strip()
        es = (ertek.get("es") or "").strip()
        if not hu:
            hianyzo_hu += 1
            j.hiba(terulet, f"„{kulcs}”: nincs magyar szöveg.")
        if not es:
            hianyzo_es += 1
            j.hiba(terulet, f"„{kulcs}”: NINCS SPANYOL SZÖVEG. "
                            f"A spanyol oldalon ez üresen vagy magyarul jelenik meg.")
        if hu and es:
            h_hu = sorted(_HELYETTESITO.findall(hu))
            h_es = sorted(_HELYETTESITO.findall(es))
            if h_hu != h_es:
                j.hiba(terulet, f"„{kulcs}”: a helyettesítők nem egyeznek – "
                                f"magyar {h_hu}, spanyol {h_es}. "
                                f"A spanyol szövegbe nem kerül bele az érték.")
        if hu and hu == es and len(hu) > 12:
            ures += 1

    if ures:
        j.figyelem(terulet, f"{ures} kulcsnál a spanyol szöveg SZÓ SZERINT "
                            f"ugyanaz, mint a magyar. Valószínűleg le se lett "
                            f"fordítva.")
    if not (hianyzo_es or hianyzo_hu):
        j.rendben(terulet, f"Mind a {len(szotar)} kulcs megvan mindkét nyelven.")


# ── 3. SABLONOK ─────────────────────────────────────────────────────────────

def ellenoriz_sablonok(j: Jelentes) -> None:
    terulet = "Sablonok"
    try:
        import jinja2
    except Exception:
        j.figyelem(terulet, "A jinja2 nincs telepítve, a sablonokat kihagyom.")
        return
    kornyezet = jinja2.Environment()
    hiba = 0
    fajlok = sorted(glob.glob(os.path.join(GYOKER, "templates", "*.html")))
    for f in fajlok:
        try:
            kornyezet.parse(io.open(f, encoding="utf-8").read())
        except Exception as exc:
            hiba += 1
            j.hiba(terulet, f"{os.path.basename(f)}: {exc}")
    if not hiba:
        j.rendben(terulet, f"Mind a {len(fajlok)} sablon értelmes.")


# ── 4. KIEJTÉS ──────────────────────────────────────────────────────────────
# Ezek a jelek a felolvasás után is bent maradva rossz kiejtést okoznak:
# a felolvasó vagy kihagyja őket, vagy betűzi.
_GYANUS = {
    "×": "szorzásjel", "·": "középpont", "÷": "osztásjel", "≈": "kb. jel",
    "≤": "kisebb-egyenlő", "≥": "nagyobb-egyenlő", "√": "gyökjel",
    "^": "hatványjel", "∑": "szumma", "π": "pí", "°": "fok",
    "%": "százalékjel", "‰": "ezrelék",
}
_SZAM_X_SZAM = re.compile(r"\d\s*[xX*]\s*\d")


def ellenoriz_kiejtes(j: Jelentes) -> None:
    terulet = "Kiejtés"
    try:
        import hang
        import curriculum_loader as cl
    except Exception as exc:
        j.figyelem(terulet, f"Nem futtatható: {exc!r}")
        return

    talalat: dict[str, int] = {}
    minta_pelda: dict[str, str] = {}
    vizsgalt = 0

    latott: set[str] = set()
    for f, evek in _tanterv_fajlok():
        kulcs = re.sub(r"[^a-z]", "", os.path.basename(f).lower())[:18]
        if kulcs in latott:
            continue
        latott.add(kulcs)
        try:
            raw = json.load(io.open(f, encoding="utf-8"))
        except Exception:
            continue
        for ev in evek:
            try:
                katalogus = cl.extract_topic_catalog(raw, ev, raw_data=raw)
            except Exception:
                continue
            for t in katalogus:
                szoveg = f"{t.get('name', '')} {(t.get('text') or '')[:1200]}"
                vizsgalt += 1
                try:
                    ki = hang.kiejtes(szoveg, "hu")
                except Exception as exc:
                    j.hiba(terulet, f"A kiejtés hibára fut: {exc!r}")
                    return
                for jel, nev in _GYANUS.items():
                    if jel in ki:
                        talalat[nev] = talalat.get(nev, 0) + 1
                        minta_pelda.setdefault(nev, _korny(ki, jel))
                if _SZAM_X_SZAM.search(ki):
                    talalat["szám x szám"] = talalat.get("szám x szám", 0) + 1
                    minta_pelda.setdefault("szám x szám",
                                           _korny(ki, _SZAM_X_SZAM.search(ki).group()))

    for nev, db in sorted(talalat.items(), key=lambda x: -x[1]):
        j.figyelem(terulet, f"{nev}: {db} leckeszövegben marad bent a "
                            f"felolvasás után. Például: „{minta_pelda[nev]}”")
    if not talalat:
        j.rendben(terulet, f"{vizsgalt} leckeszövegben nincs félrehangzó jel.")
    else:
        j.rendben(terulet, f"{vizsgalt} leckeszöveget néztem át.")


def _korny(szoveg: str, mi: str, sugar: int = 28) -> str:
    i = szoveg.find(mi)
    if i < 0:
        return mi
    a = max(0, i - sugar)
    b = min(len(szoveg), i + len(mi) + sugar)
    return szoveg[a:b].replace("\n", " ").strip()


# ── 5. KÁRTYÁK ──────────────────────────────────────────────────────────────

def ellenoriz_kartyak(j: Jelentes) -> None:
    terulet = "Kártyák"
    try:
        import kartyak
    except Exception as exc:
        j.figyelem(terulet, f"A kartyak.py nem tölthető be: {exc!r}")
        return
    lista = getattr(kartyak, "KARTYAK", None)
    if not isinstance(lista, list) or not lista:
        j.figyelem(terulet, "Nem találom a kártyalistát.")
        return

    hianyzo: list[str] = []
    for k in lista:
        oldal = k.get("oldal", "hu")
        kep = k.get("kep") or ""
        ut = os.path.join(GYOKER, "static", "kartyak", oldal, f"{kep}.png")
        if not os.path.exists(ut):
            hianyzo.append(f"{k.get('nev', kep)} → static/kartyak/{oldal}/{kep}.png")

    if hianyzo:
        j.figyelem(terulet, f"{len(hianyzo)} kártyának NINCS képe "
                            f"({len(lista)}-ból). A gyerek sziluettet lát.")
        for sor in hianyzo[:40]:
            j.figyelem(terulet, f"    {sor}")
    else:
        j.rendben(terulet, f"Mind a {len(lista)} kártyának van képe.")

    # Az album 52 helyes; ha kevesebb kártya van, sosem telik meg.
    if len(lista) < 52:
        j.hiba(terulet, f"Csak {len(lista)} kártya van 52 helyre. "
                        f"Az album SOSEM telhet meg – vagy több kártya kell, "
                        f"vagy kisebb album.")


# ── futtatás ────────────────────────────────────────────────────────────────

def main() -> int:
    ertelmezo = argparse.ArgumentParser(description="TutorIA néma ellenőr")
    ertelmezo.add_argument("--md", metavar="FÁJL",
                           help="a jelentés Markdownban ebbe a fájlba")
    ertelmezo.add_argument("--csak", metavar="TERÜLET", default="",
                           help="tanterv | forditas | sablon | kiejtes | kartya")
    args = ertelmezo.parse_args()

    j = Jelentes()
    futtatando = {
        "tanterv": ellenoriz_tanterv,
        "forditas": ellenoriz_forditasok,
        "sablon": ellenoriz_sablonok,
        "kiejtes": ellenoriz_kiejtes,
        "kartya": ellenoriz_kartyak,
    }
    valasztott = (args.csak or "").strip().lower()
    for nev, fv in futtatando.items():
        if valasztott and nev != valasztott:
            continue
        fv(j)

    print(j.szoveg())
    print(f"\n{'=' * 70}")
    print(f"Súlyos hiba: {j.sulyos} db")
    if args.md:
        io.open(args.md, "w", encoding="utf-8").write(j.markdown())
        print(f"A jelentés fájlban: {args.md}")
    return 1 if j.sulyos else 0


if __name__ == "__main__":
    raise SystemExit(main())
