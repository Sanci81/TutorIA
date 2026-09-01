# -*- coding: utf-8 -*-
"""A Leonardo-figurákat mozgatható részekre bontja.

MIT CSINÁL
    1. Kiveszi a szürke hátteret és a talajárnyékot.
    2. Megkeresi a nyakat (a fej és a váll közti legkeskenyebb sor).
    3. Megkeresi, hol válik el a kar a testtől (az első sor, ahol HÁROM
       különálló folt van: bal kar | törzs | jobb kar).
    4. Szétvágja: fej, törzs, felkar és alkar oldalanként.
    5. Kiszámolja a váll- és könyök-csuklópontot.

MIÉRT ÍGY
    A kar felül összeér a törzzsel, ezért ott ferde vágással választjuk el:
    a hónaljtól a váll széléig húzott egyenes mentén. Lejjebb már a valódi
    rés dönt, ott nem kell találgatni.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

MAPPA = Path(__file__).parent / "avatar"

# A lábak közötti rést NEM szabad betömni – csak a rajzhibából eredő apró
# lyukakat. Élesben ez okozta, hogy szürke sáv maradt a lábak között.
MAX_LYUK = 400          # pixel²


def _hatter_nelkul(ut: Path) -> np.ndarray:
    """RGBA tömb, a háttér és a talajárnyék nélkül."""
    im = Image.open(ut).convert("RGB")
    a = np.array(im).astype(int)

    szeg = np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]])
    hatter = np.median(szeg, axis=0)
    vil = a.mean(axis=2)
    szurkes = (a.max(axis=2) - a.min(axis=2)) < 26
    # A háttér nem csak a pontos színe: a lábak közé eső VETETT ÁRNYÉK is oda
    # tartozik. Az árnyék szürke és sötétebb, de nem olyan sötét, mint a cipő.
    jelolt = szurkes & (vil > hatter.mean() - 78) & (vil < hatter.mean() + 34)

    cimke, _ = ndimage.label(jelolt)
    szelen = set(cimke[0]) | set(cimke[-1]) | set(cimke[:, 0]) | set(cimke[:, -1])
    szelen.discard(0)
    alak = ~np.isin(cimke, list(szelen))

    # A lábak közé zárt árnyékfolt nem ér el a szegélyig, ezért külön kell
    # kivenni: ami elég NAGY és végig háttérszerű, az nem a figura része.
    zart, zdb = ndimage.label(jelolt & alak)
    if zdb:
        meret = ndimage.sum(np.ones_like(zart), zart, range(1, zdb + 1))
        nagyok = [i + 1 for i, m in enumerate(meret) if m > 900]
        if nagyok:
            alak = alak & ~np.isin(zart, nagyok)

    # apró lyukak betömése – de a lábak közti nagy rés maradjon lyuk
    lyuk = ndimage.binary_fill_holes(alak) & ~alak
    lcimke, ldb = ndimage.label(lyuk)
    if ldb:
        meret = ndimage.sum(np.ones_like(lcimke), lcimke, range(1, ldb + 1))
        kicsik = np.isin(lcimke, [i + 1 for i, m in enumerate(meret) if m <= MAX_LYUK])
        alak = alak | kicsik

    alak = ndimage.binary_opening(alak, np.ones((3, 3)))

    # talajárnyék: ott kezdődik, ahol a sor szélessége hirtelen megugrik
    szel = np.array([(np.where(s)[0][-1] - np.where(s)[0][0] + 1) if s.any() else 0
                     for s in alak])
    ys = np.where(alak.any(axis=1))[0]
    ugras = next((y for y in range(int(ys[-1] * .93), ys[-1])
                  if szel[y] > 1.4 * np.median(szel[y - 30:y])), None)
    if ugras:
        sav = slice(ugras - 4, None)
        px = a[sav]
        arnyek = (px.max(axis=2) - px.min(axis=2) < 22) & (px.mean(axis=2) > 68)
        alak[sav] = alak[sav] & ~arnyek

    # csak a legnagyobb összefüggő folt marad
    cimke, db = ndimage.label(alak)
    if db > 1:
        meret = ndimage.sum(np.ones_like(cimke), cimke, range(1, db + 1))
        alak = cimke == (int(np.argmax(meret)) + 1)

    alfa = (alak * 255).astype(np.uint8)
    return np.dstack([np.array(im), alfa])


def _foltok(sor: np.ndarray) -> list[np.ndarray]:
    c, db = ndimage.label(sor)
    return [np.where(c == i)[0] for i in range(1, db + 1)]


def darabol(nev: str) -> dict:
    rgba = _hatter_nelkul(MAPPA / f"{nev}.jpg")
    Image.fromarray(rgba).save(MAPPA / f"{nev}_tiszta.png")
    m = rgba[..., 3] > 128
    ys = np.where(m.any(axis=1))[0]
    teto, alj = int(ys[0]), int(ys[-1])
    mag = alj - teto

    szel = np.array([(np.where(s)[0][-1] - np.where(s)[0][0] + 1) if s.any() else 0
                     for s in m])
    y_nyak = int(min(range(teto + int(mag * .12), teto + int(mag * .30)),
                     key=lambda y: szel[y]))
    # A kar a VÁLL ALATT válik el, sosem a fej magasságában. A korlát
    # nélkül a haj vagy a gallér világos foltja adna hamis találatot.
    y_kezd = max(y_nyak, teto + int(mag * .28))
    y_szet = next(y for y in range(y_kezd, alj) if len(_foltok(m[y])) >= 3)

    kar = {"bal": np.zeros_like(m), "jobb": np.zeros_like(m)}
    y_kez = y_szet
    for y in range(y_szet, alj):
        k = _foltok(m[y])
        # CSAK három folt esetén vágunk: kettőnél a törzs is beleragadna a karba
        if len(k) < 3:
            if y > y_szet + 40:
                break
            continue
        sorszel = k[-1][-1] - k[0][0] + 1
        if len(k[0]) < sorszel * .35:
            kar["bal"][y, k[0]] = True
        if len(k[-1]) < sorszel * .35:
            kar["jobb"][y, k[-1]] = True
        y_kez = y

    # ── VÁLL: KÖR alakú sapka, nem háromszög ────────────────────────────
    # A háromszög elfordulva hegyes tüskét csinál a vállnál. A csuklópont
    # köré rajzolt KÖR viszont elforgatva önmaga marad, ezért a váll minden
    # kartartásnál ugyanúgy néz ki, és mindig takarja az ízületet.
    k0 = _foltok(m[y_szet])
    honalj_b, honalj_j = int(k0[0][-1]), int(k0[-1][0])
    y_vall = max(teto, y_szet - int(mag * .11))
    yy, xx = np.mgrid[0:m.shape[0], 0:m.shape[1]]
    csuklo: dict[str, list[int]] = {}
    for o, honalj in (("bal", honalj_b), ("jobb", honalj_j)):
        van = np.where(kar[o].any(axis=1))[0]
        if len(van) == 0:
            continue
        # a váll közepe: a kar teteje, vízszintesen a kar közepén
        sor = kar[o][van[0]]
        kx = np.where(sor)[0]
        cx, cy = float(kx.mean()), float(van[0])
        r = max(abs(cx - honalj), (kx[-1] - kx[0]) * .62) * 1.12
        korong = ((xx - cx) ** 2 + (yy - cy) ** 2) <= r * r
        kar[o] |= korong & m
        kar[o][:max(teto, int(cy - r))] = False
        csuklo[o] = [int(cx), int(cy)]      # a korong KÖZEPE a forgáspont

    y_fej = min(alj, y_nyak + int(mag * .035))
    fejm = np.zeros_like(m)
    fejm[:y_fej] = m[:y_fej]
    # A TÖRZS MEGTARTJA A VÁLLÁT. Ez a lényeg: korábban a váll ferde
    # háromszögét is kivágtam belőle, ezért amikor a kar elfordult, fehér
    # lyuk maradt a helyén. Most csak a hónalj ALATTI részt vesszük el – a
    # váll megmarad a törzsön is, és a kar rajta forog.
    kar_also = {o: kar[o].copy() for o in kar}
    for o in kar_also:
        kar_also[o][:y_szet] = False
    torzs = m & ~kar_also["bal"] & ~kar_also["jobb"]
    torzs[:y_nyak] = False
    # a kézből leszakadt apró foltok ne maradjanak a törzsön lebegve
    tc, tdb = ndimage.label(torzs)
    if tdb > 1:
        tm = ndimage.sum(np.ones_like(tc), tc, range(1, tdb + 1))
        torzs = tc == (int(np.argmax(tm)) + 1)

    adat: dict = {"kep": [int(rgba.shape[1]), int(rgba.shape[0])], "mag": int(mag)}

    def ment(mask, fajl):
        r = rgba.copy()
        r[..., 3] = np.where(mask, rgba[..., 3], 0)
        yy = np.where(mask.any(axis=1))[0]
        xx = np.where(mask.any(axis=0))[0]
        d = (int(xx[0]), int(yy[0]), int(xx[-1]) + 1, int(yy[-1]) + 1)
        Image.fromarray(r).crop(d).save(MAPPA / f"{fajl}.png")
        return d

    adat["fej"] = ment(fejm, f"{nev}_fej")
    adat["torzs"] = ment(torzs, f"{nev}_torzs")

    for o in ("bal", "jobb"):
        d = ment(kar[o], f"{nev}_kar_{o}")
        im = Image.open(MAPPA / f"{nev}_kar_{o}.png")
        h = im.height
        ky = int(h * .48)
        ATFED = 26
        # 14 px átfedés, hogy hajlításkor ne nyíljon szét a varrat
        im.crop((0, 0, im.width, min(h, ky + ATFED))).save(MAPPA / f"{nev}_felkar_{o}.png")
        im.crop((0, max(0, ky - ATFED), im.width, h)).save(MAPPA / f"{nev}_alkar_{o}.png")
        adat[f"felkar_{o}"] = [d[0], d[1], d[0] + im.width, d[1] + min(h, ky + ATFED)]
        adat[f"alkar_{o}"] = [d[0], d[1] + max(0, ky - ATFED), d[0] + im.width, d[1] + h]

        adat[f"vall_{o}"] = csuklo[o]
        sor = np.array(im)[..., 3][min(ky, h - 1)] > 128
        kx = np.where(sor)[0]
        adat[f"konyok_{o}"] = [d[0] + int(kx.mean()) if len(kx) else d[0], d[1] + ky]

    adat.update(y_nyak=y_nyak, y_szet=int(y_szet), y_kez=int(y_kez), y_vall=int(y_vall))
    return adat


if __name__ == "__main__":
    SZAJ = {"no": [.500, .645, .19], "ferfi": [.515, .700, .22]}
    ki = {}
    for n in ("no", "ferfi"):
        a = darabol(n)
        a["szaj_kp"] = SZAJ[n]
        ki[n] = a
        print(f"{n}: fej {a['fej'][2]-a['fej'][0]}px | "
              f"torzs {a['torzs'][2]-a['torzs'][0]}px | "
              f"vall {a['vall_bal']} {a['vall_jobb']} | "
              f"konyok {a['konyok_bal']} {a['konyok_jobb']}")
    (MAPPA / "adatok.json").write_text(json.dumps(ki, indent=1))
