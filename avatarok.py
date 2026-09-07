"""Profil-avatarok a gyerekeknek — KÓDBÓL RAJZOLVA, nem képgenerálással.

Miért így?
- Nem kerül pénzbe, és nem kell naponta tíz képet generálni ahhoz, hogy egy
  használható legyen.
- Vektoros (SVG), ezért a 44 képpontos profilkörben és a 160 képpontos
  Kinézet-kártyán is éles.
- PARAMÉTERES: a gyerekarcok bőrszínből, frizurából és hajszínből állnak
  össze, tehát később könnyű avatar-készítőt csinálni belőle, ahol a gyerek
  maga kever ki egyet.

Stílus: kör keret, vastag sötét körvonal, lapos színek + EGY halvány
árnyaltóny a mélységhez. Ugyanaz a világ, mint a kabala figuráké.

Használat:
    avatarok.svg("roka")   -> SVG szöveg
    avatarok.LISTA         -> [{"kulcs", "nev_hu", "nev_es", "ar"}, ...]
"""

from __future__ import annotations

KONTUR = "#22201e"
V = 4.2                      # körvonal vastagsága

# Bőrtónusok: alap + árnyék
BOR = [
    ("#fbdcc0", "#f0c6a4"),
    ("#f2c8a0", "#e0ac80"),
    ("#d79c6e", "#c1834f"),
    ("#a9714a", "#8e5a37"),
    ("#7a4d31", "#633d26"),
]
# Hajszínek: alap + világos csillanás
HAJ = [
    ("#2b2622", "#453c35"),   # fekete
    ("#5b3a24", "#79523a"),   # barna
    ("#8a5a2b", "#a87643"),   # világosbarna
    ("#d9a441", "#efc46a"),   # szőke
    ("#b9422c", "#d15f45"),   # vörös
    ("#6d6a66", "#8a8783"),   # hamvas
]


def _keret(hatter: str, tartalom: str) -> str:
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" '
        'width="200" height="200">'
        '<defs><clipPath id="kor"><circle cx="100" cy="100" r="93"/></clipPath></defs>'
        f'<circle cx="100" cy="100" r="93" fill="{hatter}"/>'
        f'<g clip-path="url(#kor)">{tartalom}</g>'
        f'<circle cx="100" cy="100" r="93" fill="none" stroke="{KONTUR}" stroke-width="6"/>'
        '</svg>'
    )


def _szemek(y: float = 104, tav: float = 21, r: float = 9.5) -> str:
    """Nagy, barátságos szemek csillanással."""
    b, j = 100 - tav, 100 + tav
    return (
        f'<ellipse cx="{b}" cy="{y}" rx="{r*0.92}" ry="{r}" fill="#fff" '
        f'stroke="{KONTUR}" stroke-width="2.6"/>'
        f'<ellipse cx="{j}" cy="{y}" rx="{r*0.92}" ry="{r}" fill="#fff" '
        f'stroke="{KONTUR}" stroke-width="2.6"/>'
        f'<circle cx="{b+1}" cy="{y+1}" r="{r*0.5}" fill="{KONTUR}"/>'
        f'<circle cx="{j+1}" cy="{y+1}" r="{r*0.5}" fill="{KONTUR}"/>'
        f'<circle cx="{b+3}" cy="{y-2}" r="{r*0.18}" fill="#fff"/>'
        f'<circle cx="{j+3}" cy="{y-2}" r="{r*0.18}" fill="#fff"/>'
    )


def _szemoldok(y: float = 88, tav: float = 21) -> str:
    b, j = 100 - tav, 100 + tav
    return (f'<path d="M{b-10} {y} q10 -6 20 0" fill="none" stroke="{KONTUR}" '
            f'stroke-width="3.4" stroke-linecap="round"/>'
            f'<path d="M{j-10} {y} q10 -6 20 0" fill="none" stroke="{KONTUR}" '
            f'stroke-width="3.4" stroke-linecap="round"/>')


def _orr(y: float = 116) -> str:
    return (f'<path d="M97 {y-5} q3 6 6 0" fill="none" stroke="{KONTUR}" '
            f'stroke-width="3" stroke-linecap="round"/>')


def _szaj(y: float = 128, szel: float = 15) -> str:
    return (f'<path d="M{100-szel} {y} q{szel} {szel*0.85} {szel*2} 0" fill="none" '
            f'stroke="{KONTUR}" stroke-width="3.8" stroke-linecap="round"/>')


def _pir(y: float = 122, tav: float = 36) -> str:
    return (f'<ellipse cx="{100-tav}" cy="{y}" rx="10" ry="6" fill="#ef8f8f" opacity=".5"/>'
            f'<ellipse cx="{100+tav}" cy="{y}" rx="10" ry="6" fill="#ef8f8f" opacity=".5"/>')


# ── GYEREKARCOK ──────────────────────────────────────────────────────
def _frizura(nev: str, alap: str, vilagos: str) -> tuple[str, str]:
    """(hátsó réteg, elülső réteg) — a hátsó a fej MÖGÖTT rajzolódik."""
    hatso, elulso = "", ""
    k = f'fill="{alap}" stroke="{KONTUR}" stroke-width="{V}"'

    if nev == "rovid":
        elulso = (f'<path d="M46 100c0-32 24-54 54-54s54 22 54 54c-4-8-8-14-14-16'
                  f'-10 8-70 8-80 0-6 2-10 8-14 16Z" {k}/>'
                  f'<path d="M62 68q14-12 38-12t38 12" fill="none" stroke="{vilagos}" '
                  f'stroke-width="6" stroke-linecap="round" opacity=".85"/>')
    elif nev == "frufru":
        elulso = (f'<path d="M44 104c0-34 25-58 56-58s56 24 56 58c-3-12-8-20-13-24'
                  f'-2 10-10 14-18 12-3-10-12-14-21-12-9-2-18 2-21 12-8 2-16-2-18-12'
                  f'-5 4-10 12-13 24Z" {k}/>')
    elif nev == "hosszu":
        hatso = (f'<path d="M40 108c0-40 26-62 60-62s60 22 60 62v76H40Z" {k}/>')
        # Középen elválasztva, hogy ne sisaknak nézzen ki.
        elulso = (f'<path d="M44 102c0-32 25-56 56-56s56 24 56 56c-4-14-10-22-16-26'
                  f'-10 10-26 14-40 12-14 2-30-2-40-12-6 4-12 12-16 26Z" {k}/>'
                  )
    elif nev == "copf":
        # A copfok FÖNT vannak, a fej két oldalán – ha fülmagasságban
        # állnak, fülvédőnek látszanak.
        hatso = (f'<circle cx="46" cy="72" r="16" {k}/><circle cx="154" cy="72" r="16" {k}/>'
                 f'<path d="M56 78q10 14 22 18M144 78q-10 14-22 18" fill="none" '
                 f'stroke="{alap}" stroke-width="11" stroke-linecap="round"/>')
        elulso = (f'<path d="M46 100c0-32 24-54 54-54s54 22 54 54c-4-10-10-16-16-18'
                  f'-10 8-66 8-76 0-6 2-12 8-16 18Z" {k}/>')
    elif nev == "kontyos":
        hatso = (f'<circle cx="100" cy="42" r="22" {k}/>')
        elulso = (f'<path d="M46 100c0-32 24-54 54-54s54 22 54 54c-4-10-10-16-16-18'
                  f'-10 8-66 8-76 0-6 2-12 8-16 18Z" {k}/>')
    else:  # gondor
        hatso = ('<g %s>' % k + ''.join(
            f'<circle cx="{cx}" cy="{cy}" r="{r}"/>'
            for cx, cy, r in [(56, 88, 22), (72, 62, 22), (100, 52, 24),
                              (128, 62, 22), (144, 88, 22)]) + '</g>')
        elulso = (f'<path d="M50 98c0-28 22-48 50-48s50 20 50 48c-6-8-14-12-22-10'
                  f'-8-8-48-8-56 0-8-2-16 2-22 10Z" {k}/>')
    return hatso, elulso


def _gyerek(hatter: str, bor_i: int, haj_i: int, frizura: str, ruha: str) -> str:
    bor, bor_arny = BOR[bor_i]
    haj, haj_vil = HAJ[haj_i]
    hatso, elulso = _frizura(frizura, haj, haj_vil)

    t = (
        # váll / ruha
        f'<path d="M32 200c0-34 30-52 68-52s68 18 68 52Z" fill="{ruha}" '
        f'stroke="{KONTUR}" stroke-width="{V}"/>'
        # nyak
        f'<path d="M84 138h32v26q0 8-16 8t-16-8Z" fill="{bor_arny}" '
        f'stroke="{KONTUR}" stroke-width="{V}"/>'
        + hatso +
        # fülek
        f'<circle cx="46" cy="108" r="11" fill="{bor}" stroke="{KONTUR}" stroke-width="{V}"/>'
        f'<circle cx="154" cy="108" r="11" fill="{bor}" stroke="{KONTUR}" stroke-width="{V}"/>'
        # arc
        f'<path d="M50 96c0-28 22-50 50-50s50 22 50 50v18c0 30-22 50-50 50'
        f's-50-20-50-50Z" fill="{bor}" stroke="{KONTUR}" stroke-width="{V}"/>'
        # halvány árnyék az áll körül
        f'<path d="M50 118v-4c0 30 22 50 50 50s50-20 50-50v4c0 30-22 50-50 50'
        f's-50-20-50-50Z" fill="{bor_arny}" opacity=".5"/>'
        + elulso + _szemoldok() + _szemek() + _orr() + _szaj() + _pir()
    )
    return _keret(hatter, t)


# ── ÁLLATOK ──────────────────────────────────────────────────────────
def _roka() -> str:
    t = (f'<path d="M50 88 40 28l40 26Z" fill="#e0722a" stroke="{KONTUR}" stroke-width="{V}"/>'
         f'<path d="M150 88 160 28l-40 26Z" fill="#e0722a" stroke="{KONTUR}" stroke-width="{V}"/>'
         f'<path d="M60 82 54 50l24 16Z" fill="#f7d9c0"/>'
         f'<path d="M140 82 146 50l-24 16Z" fill="#f7d9c0"/>'
         f'<path d="M48 100c0-28 23-48 52-48s52 20 52 48c0 34-24 58-52 58s-52-24-52-58Z" '
         f'fill="#f0863a" stroke="{KONTUR}" stroke-width="{V}"/>'
         f'<path d="M64 122c0-18 16-28 36-28s36 10 36 28c0 22-16 36-36 36s-36-14-36-36Z" '
         f'fill="#fff3e6"/>'
         + _szemek(102, 22, 10) +
         f'<path d="M100 122q-9 0-9 6t9 8q9 0 9-8t-9-6Z" fill="{KONTUR}"/>'
         f'<path d="M100 136v6M100 142q-9 8-16 2M100 142q9 8 16 2" fill="none" '
         f'stroke="{KONTUR}" stroke-width="3.4" stroke-linecap="round"/>')
    return _keret("#ffeedd", t)


def _bagoly() -> str:
    t = (f'<path d="M44 78 60 40l16 22Z" fill="#6f4fd0" stroke="{KONTUR}" stroke-width="{V}"/>'
         f'<path d="M156 78 140 40l-16 22Z" fill="#6f4fd0" stroke="{KONTUR}" stroke-width="{V}"/>'
         f'<ellipse cx="100" cy="112" rx="56" ry="54" fill="#7b5bd6" '
         f'stroke="{KONTUR}" stroke-width="{V}"/>'
         f'<path d="M52 124c0-10 4-16 10-16 6 22 70 22 76 0 6 0 10 6 10 16'
         f'-4 26-24 42-48 42s-44-16-48-42Z" fill="#9a80e4"/>'
         f'<circle cx="78" cy="100" r="25" fill="#fff" stroke="{KONTUR}" stroke-width="3.4"/>'
         f'<circle cx="122" cy="100" r="25" fill="#fff" stroke="{KONTUR}" stroke-width="3.4"/>'
         f'<circle cx="80" cy="102" r="11" fill="{KONTUR}"/>'
         f'<circle cx="120" cy="102" r="11" fill="{KONTUR}"/>'
         f'<circle cx="84" cy="98" r="3.4" fill="#fff"/>'
         f'<circle cx="124" cy="98" r="3.4" fill="#fff"/>'
         f'<path d="M100 116 90 130h20Z" fill="#f5a623" stroke="{KONTUR}" stroke-width="3"/>')
    return _keret("#eae4ff", t)


def _macska() -> str:
    t = (f'<path d="M54 84 48 34l40 24Z" fill="#9a9a9a" stroke="{KONTUR}" stroke-width="{V}"/>'
         f'<path d="M146 84 152 34l-40 24Z" fill="#9a9a9a" stroke="{KONTUR}" stroke-width="{V}"/>'
         f'<path d="M64 76 60 50l22 14Z" fill="#f4bccd"/>'
         f'<path d="M136 76 140 50l-22 14Z" fill="#f4bccd"/>'
         f'<ellipse cx="100" cy="110" rx="54" ry="52" fill="#adadad" '
         f'stroke="{KONTUR}" stroke-width="{V}"/>'
         f'<path d="M52 122c8 26 26 40 48 40s40-14 48-40c0 30-20 50-48 50s-48-20-48-50Z" '
         f'fill="#8f8f8f" opacity=".45"/>'
         f'<ellipse cx="79" cy="104" rx="8.5" ry="13" fill="{KONTUR}"/>'
         f'<ellipse cx="121" cy="104" rx="8.5" ry="13" fill="{KONTUR}"/>'
         f'<circle cx="82" cy="99" r="3" fill="#fff"/><circle cx="124" cy="99" r="3" fill="#fff"/>'
         f'<path d="M100 122q-8 0-8 5t8 7q8 0 8-7t-8-5Z" fill="#f28fb0" '
         f'stroke="{KONTUR}" stroke-width="2.4"/>'
         f'<path d="M100 134v5M100 139q-9 8-16 2M100 139q9 8 16 2" fill="none" '
         f'stroke="{KONTUR}" stroke-width="3.4" stroke-linecap="round"/>'
         f'<path d="M44 116h24M44 128h24M156 116h-24M156 128h-24" fill="none" '
         f'stroke="{KONTUR}" stroke-width="2.6" stroke-linecap="round" opacity=".8"/>')
    return _keret("#ffeaf3", t)


def _panda() -> str:
    t = (f'<circle cx="56" cy="66" r="21" fill="{KONTUR}"/>'
         f'<circle cx="144" cy="66" r="21" fill="{KONTUR}"/>'
         f'<circle cx="56" cy="66" r="10" fill="#5b514c"/>'
         f'<circle cx="144" cy="66" r="10" fill="#5b514c"/>'
         f'<ellipse cx="100" cy="110" rx="55" ry="52" fill="#ffffff" '
         f'stroke="{KONTUR}" stroke-width="{V}"/>'
         f'<ellipse cx="78" cy="104" rx="18" ry="22" fill="{KONTUR}" transform="rotate(-12 78 104)"/>'
         f'<ellipse cx="122" cy="104" rx="18" ry="22" fill="{KONTUR}" transform="rotate(12 122 104)"/>'
         f'<circle cx="78" cy="104" r="7" fill="#fff"/><circle cx="122" cy="104" r="7" fill="#fff"/>'
         f'<circle cx="80" cy="101" r="2.6" fill="{KONTUR}"/>'
         f'<circle cx="124" cy="101" r="2.6" fill="{KONTUR}"/>'
         f'<ellipse cx="100" cy="128" rx="11" ry="8" fill="{KONTUR}"/>'
         + _szaj(140, 13))
    return _keret("#eef6ee", t)


def _beka() -> str:
    t = (f'<circle cx="70" cy="64" r="24" fill="#5cb85c" stroke="{KONTUR}" stroke-width="{V}"/>'
         f'<circle cx="130" cy="64" r="24" fill="#5cb85c" stroke="{KONTUR}" stroke-width="{V}"/>'
         f'<circle cx="70" cy="66" r="12" fill="#fff" stroke="{KONTUR}" stroke-width="2.6"/>'
         f'<circle cx="130" cy="66" r="12" fill="#fff" stroke="{KONTUR}" stroke-width="2.6"/>'
         f'<circle cx="71" cy="67" r="6" fill="{KONTUR}"/><circle cx="131" cy="67" r="6" fill="{KONTUR}"/>'
         f'<ellipse cx="100" cy="122" rx="56" ry="50" fill="#6ec46e" '
         f'stroke="{KONTUR}" stroke-width="{V}"/>'
         f'<ellipse cx="100" cy="140" rx="44" ry="26" fill="#8ed58e" opacity=".7"/>'
         f'<circle cx="80" cy="112" r="4" fill="{KONTUR}"/>'
         f'<circle cx="120" cy="112" r="4" fill="{KONTUR}"/>'
         f'<path d="M72 130q28 24 56 0" fill="none" stroke="{KONTUR}" '
         f'stroke-width="4" stroke-linecap="round"/>')
    return _keret("#e6f7e6", t)


def _dino() -> str:
    t = (f'<path d="M58 68 70 40l12 24M92 56l8-22 10 22M124 64l12-24 10 26" '
         f'fill="#f5a623" stroke="{KONTUR}" stroke-width="3.2" stroke-linejoin="round"/>'
         f'<ellipse cx="100" cy="112" rx="55" ry="52" fill="#17b8a6" '
         f'stroke="{KONTUR}" stroke-width="{V}"/>'
         f'<ellipse cx="100" cy="132" rx="40" ry="26" fill="#4fd2c2" opacity=".7"/>'
         + _szemek(102, 22, 10) +
         f'<circle cx="76" cy="126" r="3.6" fill="{KONTUR}"/>'
         f'<circle cx="124" cy="126" r="3.6" fill="{KONTUR}"/>'
         + _szaj(134, 16))
    return _keret("#e4fbf6", t)


# ── VIDÁM FIGURÁK ────────────────────────────────────────────────────
def _robot() -> str:
    t = (f'<path d="M100 30v18" stroke="{KONTUR}" stroke-width="4"/>'
         f'<circle cx="100" cy="26" r="9" fill="#ef5f5f" stroke="{KONTUR}" stroke-width="3"/>'
         f'<rect x="30" y="92" width="14" height="34" rx="7" fill="#9fb0da" '
         f'stroke="{KONTUR}" stroke-width="3.4"/>'
         f'<rect x="156" y="92" width="14" height="34" rx="7" fill="#9fb0da" '
         f'stroke="{KONTUR}" stroke-width="3.4"/>'
         f'<rect x="46" y="52" width="108" height="104" rx="26" fill="#c3cfec" '
         f'stroke="{KONTUR}" stroke-width="{V}"/>'
         f'<rect x="46" y="112" width="108" height="44" rx="26" fill="#adbce0" opacity=".8"/>'
         f'<rect x="62" y="76" width="76" height="42" rx="16" fill="#22314f" '
         f'stroke="{KONTUR}" stroke-width="3"/>'
         f'<circle cx="83" cy="97" r="9" fill="#63dcff"/>'
         f'<circle cx="117" cy="97" r="9" fill="#63dcff"/>'
         f'<circle cx="86" cy="93" r="3" fill="#fff"/><circle cx="120" cy="93" r="3" fill="#fff"/>'
         f'<path d="M82 134h36" stroke="{KONTUR}" stroke-width="4" stroke-linecap="round"/>')
    return _keret("#e8edfa", t)


def _urhajos() -> str:
    t = ('<circle cx="40" cy="46" r="3" fill="#fff"/><circle cx="168" cy="60" r="4" fill="#fff"/>'
         '<circle cx="150" cy="30" r="2.5" fill="#fff"/><circle cx="30" cy="140" r="2.5" fill="#fff"/>'
         '<circle cx="172" cy="150" r="3" fill="#fff"/>'
         f'<path d="M28 200c0-32 32-50 72-50s72 18 72 50Z" fill="#e7ecf5" '
         f'stroke="{KONTUR}" stroke-width="{V}"/>'
         f'<circle cx="100" cy="104" r="60" fill="#f2f5fa" stroke="{KONTUR}" stroke-width="{V}"/>'
         f'<path d="M46 104a54 54 0 0 1 108 0 54 54 0 0 1-108 0Z" fill="#25355e" '
         f'stroke="{KONTUR}" stroke-width="3.4"/>'
         f'<path d="M62 84q22-16 46-8-26 4-38 22Z" fill="#8fd6ff" opacity=".65"/>'
         + _szemek(108, 19, 8.5) +
         f'<path d="M92 128q8 8 16 0" fill="none" stroke="#cfe3ff" stroke-width="4" '
         f'stroke-linecap="round"/>')
    return _keret("#131c33", t)


def _varazslo() -> str:
    bor, bor_arny = BOR[1]
    t = (f'<path d="M32 200c0-34 30-52 68-52s68 18 68 52Z" fill="#4a3390" '
         f'stroke="{KONTUR}" stroke-width="{V}"/>'
         f'<circle cx="46" cy="112" r="10" fill="{bor}" stroke="{KONTUR}" stroke-width="{V}"/>'
         f'<circle cx="154" cy="112" r="10" fill="{bor}" stroke="{KONTUR}" stroke-width="{V}"/>'
         f'<path d="M54 104c0-26 20-46 46-46s46 20 46 46v14c0 28-20 46-46 46'
         f's-46-18-46-46Z" fill="{bor}" stroke="{KONTUR}" stroke-width="{V}"/>'
         f'<path d="M54 120v-4c0 28 20 46 46 46s46-18 46-46v4c0 28-20 46-46 46'
         f's-46-18-46-46Z" fill="{bor_arny}" opacity=".5"/>'
         f'<path d="M34 84h132L100 8Z" fill="#5b3fa8" stroke="{KONTUR}" stroke-width="{V}"/>'
         f'<path d="M34 84h132l-8 14H42Z" fill="#7a5cc9" stroke="{KONTUR}" stroke-width="3"/>'
         f'<path d="M100 34l6 13 14 2-10 10 2 14-12-7-12 7 2-14-10-10 14-2Z" fill="#f5d24a" '
         f'stroke="{KONTUR}" stroke-width="2.4"/>'
         + _szemek(112, 20, 9) + _orr(124) + _szaj(136, 14) + _pir(130, 34))
    return _keret("#efe8ff", t)


def _szuperhos() -> str:
    bor, bor_arny = BOR[0]
    t = (f'<path d="M32 200c0-34 30-52 68-52s68 18 68 52Z" fill="#2f6fd0" '
         f'stroke="{KONTUR}" stroke-width="{V}"/>'
         f'<path d="M100 148l14 10-14 14-14-14Z" fill="#f5d24a" stroke="{KONTUR}" stroke-width="3"/>'
         f'<circle cx="46" cy="110" r="10" fill="{bor}" stroke="{KONTUR}" stroke-width="{V}"/>'
         f'<circle cx="154" cy="110" r="10" fill="{bor}" stroke="{KONTUR}" stroke-width="{V}"/>'
         f'<path d="M50 100c0-28 22-50 50-50s50 22 50 50v14c0 30-22 50-50 50'
         f's-50-20-50-50Z" fill="{bor}" stroke="{KONTUR}" stroke-width="{V}"/>'
         f'<path d="M50 118v-4c0 30 22 50 50 50s50-20 50-50v4c0 30-22 50-50 50'
         f's-50-20-50-50Z" fill="{bor_arny}" opacity=".5"/>'
         f'<path d="M46 96c0-30 24-50 54-50s54 20 54 50c-6-6-12-10-18-10-10 8-72 8-82 0'
         f'-6 0-12 4-8 10Z" fill="#2b2622" stroke="{KONTUR}" stroke-width="{V}"/>'
         # maszk
         f'<path d="M52 92h96q6 0 6 8-2 16-14 18-14 2-22-8h-36q-8 10-22 8'
         f'-12-2-14-18 0-8 6-8Z" fill="#e23b4f" stroke="{KONTUR}" stroke-width="3.4"/>'
         f'<ellipse cx="79" cy="104" rx="10" ry="7" fill="#fff"/>'
         f'<ellipse cx="121" cy="104" rx="10" ry="7" fill="#fff"/>'
         f'<circle cx="80" cy="104" r="3.6" fill="{KONTUR}"/>'
         f'<circle cx="122" cy="104" r="3.6" fill="{KONTUR}"/>'
         + _orr(122) + _szaj(132, 15))
    return _keret("#ffe9e9", t)


# ── A KÍNÁLAT ────────────────────────────────────────────────────────
_KESZITOK = {
    "gyerek1": lambda: _gyerek("#e3f0ff", 0, 1, "rovid", "#2f8fd8"),
    "gyerek2": lambda: _gyerek("#ffeaf3", 1, 0, "frufru", "#e0609b"),
    "gyerek3": lambda: _gyerek("#fff2e2", 3, 0, "gondor", "#f5a623"),
    "gyerek4": lambda: _gyerek("#e9f7ef", 2, 3, "copf", "#17b8a6"),
    "gyerek5": lambda: _gyerek("#f0edff", 4, 0, "hosszu", "#7b5bd6"),
    "gyerek6": lambda: _gyerek("#ffece8", 0, 4, "kontyos", "#ef5f5f"),
    "roka": _roka,
    "bagoly": _bagoly,
    "macska": _macska,
    "panda": _panda,
    "beka": _beka,
    "dino": _dino,
    "robot": _robot,
    "urhajos": _urhajos,
    "varazslo": _varazslo,
    "szuperhos": _szuperhos,
}

LISTA = [
    {"kulcs": "gyerek1", "nev_hu": "Barna hajú", "nev_es": "Pelo castaño", "ar": 0},
    {"kulcs": "gyerek2", "nev_hu": "Frufrus", "nev_es": "Con flequillo", "ar": 0},
    {"kulcs": "gyerek3", "nev_hu": "Göndör", "nev_es": "Pelo rizado", "ar": 0},
    {"kulcs": "gyerek4", "nev_hu": "Copfos", "nev_es": "Con coletas", "ar": 0},
    {"kulcs": "gyerek5", "nev_hu": "Hosszú hajú", "nev_es": "Pelo largo", "ar": 60},
    {"kulcs": "gyerek6", "nev_hu": "Kontyos", "nev_es": "Con moño", "ar": 60},
    {"kulcs": "macska", "nev_hu": "Cica", "nev_es": "Gato", "ar": 120},
    {"kulcs": "beka", "nev_hu": "Béka", "nev_es": "Rana", "ar": 120},
    {"kulcs": "roka", "nev_hu": "Róka", "nev_es": "Zorro", "ar": 180},
    {"kulcs": "panda", "nev_hu": "Panda", "nev_es": "Panda", "ar": 180},
    {"kulcs": "bagoly", "nev_hu": "Bagoly", "nev_es": "Búho", "ar": 240},
    {"kulcs": "dino", "nev_hu": "Dínó", "nev_es": "Dino", "ar": 240},
    {"kulcs": "robot", "nev_hu": "Robot", "nev_es": "Robot", "ar": 320},
    {"kulcs": "szuperhos", "nev_hu": "Szuperhős", "nev_es": "Superhéroe", "ar": 320},
    {"kulcs": "varazslo", "nev_hu": "Varázsló", "nev_es": "Mago", "ar": 400},
    {"kulcs": "urhajos", "nev_hu": "Űrhajós", "nev_es": "Astronauta", "ar": 400},
]

INGYENES = [a["kulcs"] for a in LISTA if a["ar"] == 0]
KULCSOK = {a["kulcs"] for a in LISTA}


# ── AVATAR-KÉSZÍTŐ ───────────────────────────────────────────────────
# A gyerek maga keveri ki: bőrszín, frizura, hajszín, ruhaszín.
# A kulcs alakja: "sajat:<bor>-<frizura>-<haj>-<ruha>", pl. "sajat:2-copf-3-1".
# Fénykép helyett ez adja meg a „ez én vagyok" érzést — személyes adat nélkül.

FRIZURAK = [
    {"kulcs": "rovid", "nev_hu": "Rövid", "nev_es": "Corto"},
    {"kulcs": "frufru", "nev_hu": "Frufrus", "nev_es": "Flequillo"},
    {"kulcs": "gondor", "nev_hu": "Göndör", "nev_es": "Rizado"},
    {"kulcs": "copf", "nev_hu": "Copfos", "nev_es": "Coletas"},
    {"kulcs": "kontyos", "nev_hu": "Kontyos", "nev_es": "Moño"},
    {"kulcs": "hosszu", "nev_hu": "Hosszú", "nev_es": "Largo"},
]

RUHAK = ["#2f8fd8", "#ef5f5f", "#17b8a6", "#7b5bd6",
         "#f5a623", "#e0609b", "#0e8a7c", "#3d4a5c"]

HATTEREK = ["#e3f0ff", "#ffeaf3", "#e9f7ef", "#fff2e2",
            "#f0edff", "#ffece8", "#e4fbf6", "#eef1f6"]

SAJAT_ELOTAG = "sajat:"
SAJAT_AR = 200          # egyszeri feloldás; utána bármikor újrakeverhető


def sajat_kulcs(bor: int, frizura: str, haj: int, ruha: int) -> str:
    """Ellenőrzött kulcs a kevert avatarhoz."""
    bor = max(0, min(int(bor), len(BOR) - 1))
    haj = max(0, min(int(haj), len(HAJ) - 1))
    ruha = max(0, min(int(ruha), len(RUHAK) - 1))
    ervenyes = {f["kulcs"] for f in FRIZURAK}
    if frizura not in ervenyes:
        frizura = FRIZURAK[0]["kulcs"]
    return f"{SAJAT_ELOTAG}{bor}-{frizura}-{haj}-{ruha}"


def _sajat_svg(kulcs: str) -> str | None:
    """A „sajat:..." kulcsból rajzol. Hibás kulcsra None."""
    if not kulcs.startswith(SAJAT_ELOTAG):
        return None
    reszek = kulcs[len(SAJAT_ELOTAG):].split("-")
    if len(reszek) != 4:
        return None
    try:
        bor, frizura, haj, ruha = int(reszek[0]), reszek[1], int(reszek[2]), int(reszek[3])
    except ValueError:
        return None
    if not (0 <= bor < len(BOR) and 0 <= haj < len(HAJ) and 0 <= ruha < len(RUHAK)):
        return None
    if frizura not in {f["kulcs"] for f in FRIZURAK}:
        return None
    return _gyerek(HATTEREK[ruha % len(HATTEREK)], bor, haj, frizura, RUHAK[ruha])


def sajat_e(kulcs: str) -> bool:
    return bool(kulcs) and kulcs.startswith(SAJAT_ELOTAG)


def svg(kulcs: str) -> str:
    """Egy avatar SVG-je. Ismeretlen kulcsra az első ingyeneset adja."""
    sajat = _sajat_svg(kulcs or "")
    if sajat:
        return sajat
    keszito = _KESZITOK.get(kulcs) or _KESZITOK[INGYENES[0]]
    return keszito()


def ar(kulcs: str) -> int:
    if sajat_e(kulcs):
        return SAJAT_AR
    for a in LISTA:
        if a["kulcs"] == kulcs:
            return int(a["ar"])
    return 0


def nev(kulcs: str, nyelv: str = "hu") -> str:
    if sajat_e(kulcs):
        return "Mi avatar" if nyelv == "es" else "Saját avatar"
    mezo = "nev_es" if nyelv == "es" else "nev_hu"
    for a in LISTA:
        if a["kulcs"] == kulcs:
            return a[mezo]
    return ""
