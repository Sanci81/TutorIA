# -*- coding: utf-8 -*-
"""
TutorIA – tudáskártyák katalógusa.

MI EZ
    A gyűjthető kártyák teljes névsora. Minden kártya EGY konkrét leckéhez
    tartozik: akkor jár érte, ha a gyerek azt a témakört befejezi.

    A kártya képe: static/kartyak/<oldal>/<kep>.png
    Ha a kép még nincs kész, a gyűjteményoldal egy sziluettet mutat helyette,
    a kártya attól még megszerezhető.

ÚJ KÁRTYA FELVÉTELE
    Egyetlen sor a KARTYAK listába. Semmi mást nem kell módosítani.

    "targy"   – a tantárgy neve ÚGY, ahogy a tantervben szerepel
    "evfolyam"– melyik évfolyamon jár érte
    "lecke"   – a témakör neve; ehhez köti a rendszer (kisbetűs részegyezés)
    "ritkasag"– "gyakori" | "ritka" | "nagyon_ritka" | "legendas"
"""

from __future__ import annotations

import unicodedata

# ── ritkasági szintek: keret és erősség-tartomány ───────────────────────────
RITKASAG = {
    "gyakori":      {"cimke": "gyakori",      "csillag": "★",    "keret": "ezust"},
    "ritka":        {"cimke": "ritka",        "csillag": "★★",   "keret": "kek"},
    "nagyon_ritka": {"cimke": "nagyon ritka", "csillag": "★★★",  "keret": "arany"},
    "legendas":     {"cimke": "legendás",     "csillag": "★★★★", "keret": "holo"},
}

# ── tantárgyi alapszínek (a kártya keretéhez és a gyűjteményoldalhoz) ──────
TARGY_SZIN = {
    "Kémia": "#2f8f60",
    "Fizika": "#c9782a",
    "Matematika": "#3f6fd8",
    "Biológia": "#4a8f3f",
    "Földrajz": "#2f86a8",
    "Történelem": "#9c7433",
    "Magyar nyelv és irodalom": "#b4353f",
    "Ének-zene": "#7b4fbf",
    "Digitális kultúra": "#1f8f9e",
    "Vizuális kultúra": "#c94a8a",
}
ALAP_SZIN = "#3f6fd8"


# ══ A KÁRTYÁK ═══════════════════════════════════════════════════════════════
KARTYAK: list[dict] = [
    {
        "id": "hu_kemia_7_curie",
        "oldal": "hu",
        "targy": "Kémia",
        "evfolyam": 7,
        "lecke": "Az atom felépítése",
        "nev": "Marie Curie",
        "alnev": "fizikus és kémikus · 1867–1934",
        "kep": "kemia_7_curie",
        "ritkasag": "nagyon_ritka",
        "ero": 450,
        "kepesseg": "Rádiumsugárzás",
        "kepesseg_ero": 380,
        "becenev": "A SUGÁRZÓ",
        "leiras": (
            "Két új elemet talált – a polóniumot és a rádiumot –, és ő az "
            "egyetlen ember a világon, aki két különböző tudományban is "
            "Nobel-díjat kapott: fizikában és kémiában."
        ),
        "teny": (
            "A jegyzetfüzetei ma is sugároznak. Ólomdobozban őrzik őket "
            "Párizsban, és aki bele akar nézni, előbb alá kell írnia, hogy a "
            "kockázatot maga vállalja."
        ),
        "erdekesseg": (
            "Négy éven át hét tonna kőzetet főzött ki egy huzatos fészerben, "
            "hogy a végén egy tized gramm rádium maradjon a kezében."
        ),
        "idezet": (
            "Az életben semmitől sem kell félni, csak meg kell érteni."
        ),
    },
    {
        "id": "hu_kemia_7_mengyelejev",
        "oldal": "hu",
        "targy": "Kémia",
        "evfolyam": 7,
        "lecke": "A periódusos rendszer és a vegyjelek",
        "nev": "Mengyelejev",
        "alnev": "kémikus · 1834–1907",
        "kep": "kemia_7_mengyelejev",
        "ritkasag": "ritka",
        "ero": 300,
        "kepesseg": "Periódusos rendszer",
        "kepesseg_ero": 240,
        "becenev": "A RENDTEREMTŐ",
        "leiras": (
            "Sorba rakta az összes ismert elemet, és üresen hagyta a helyét "
            "azoknak, amelyeket még meg sem találtak."
        ),
        "teny": (
            "Három elem helyét üresen hagyta a táblázatban, és megjósolta a "
            "tulajdonságaikat. Mindhármat megtalálták még az élete során, "
            "pontosan olyannak, amilyennek leírta."
        ),
        "erdekesseg": (
            "Azt állította, hogy a rendszer álmában állt össze a fejében, és "
            "ébredés után egyetlen papírra leírta az egészet."
        ),
        "idezet": "A tudomány munka, nem szórakozás.",
    },
    {
        "id": "hu_fizika_7_newton",
        "oldal": "hu",
        "targy": "Fizika",
        "evfolyam": 7,
        "lecke": "Lendület és egyensúly",
        "nev": "Isaac Newton",
        "alnev": "fizikus és matematikus · 1643–1727",
        "kep": "fizika_7_newton",
        "ritkasag": "nagyon_ritka",
        "ero": 420,
        "kepesseg": "Gravitáció",
        "kepesseg_ero": 350,
        "becenev": "AZ ÓRIÁS",
        "leiras": (
            "Három törvénybe sűrítette az egész mozgást, és megmutatta, hogy "
            "ugyanaz az erő ejti le az almát, ami a Holdat pályán tartja."
        ),
        "teny": (
            "A pestisjárvány miatt bezárt az egyeteme, és hazaküldték a "
            "falujába. Az ott töltött két év alatt találta ki a gravitációt, a "
            "színek elméletét és a differenciálszámítást."
        ),
        "erdekesseg": (
            "Élete második felében a királyi pénzverde vezetője lett, és "
            "személyesen járta a londoni kocsmákat pénzhamisítók után nyomozva."
        ),
        "idezet": "Ha távolabbra láttam, azért volt, mert óriások vállán álltam.",
    },
    {
        "id": "hu_fizika_7_galilei",
        "oldal": "hu",
        "targy": "Fizika",
        "evfolyam": 7,
        "lecke": "Égi jelenségek megfigyelése és magyarázata",
        "nev": "Galileo Galilei",
        "alnev": "csillagász és fizikus · 1564–1642",
        "kep": "fizika_7_galilei",
        "ritkasag": "ritka",
        "ero": 320,
        "kepesseg": "Távcső",
        "kepesseg_ero": 260,
        "becenev": "AKI ODANÉZETT",
        "leiras": (
            "Elsőként fordította az ég felé a távcsövet, és amit meglátott, az "
            "az egész addigi világképet felborította."
        ),
        "teny": (
            "Négy holdat talált a Jupiter körül. Ezek voltak az első "
            "égitestek, amelyekről bebizonyosodott, hogy nem a Föld körül "
            "keringenek."
        ),
        "erdekesseg": (
            "Élete utolsó nyolc évét házi őrizetben töltötte, és vakon, "
            "diktálva fejezte be legfontosabb könyvét a mozgásról."
        ),
        "idezet": "És mégis mozog.",
    },
    {
        "id": "hu_matek_7_bolyai",
        "oldal": "hu",
        "targy": "Matematika",
        "evfolyam": 7,
        "lecke": "Síkbeli alakzatok",
        "nev": "Bolyai János",
        "alnev": "matematikus · 1802–1860",
        "kep": "matematika_7_bolyai",
        "ritkasag": "nagyon_ritka",
        "ero": 430,
        "kepesseg": "Új geometria",
        "kepesseg_ero": 360,
        "becenev": "A VILÁGTEREMTŐ",
        "leiras": (
            "Kitalált egy geometriát, ahol a párhuzamosok mégis találkozhatnak. "
            "Kétezer év után ő mondta ki, hogy a tér másmilyen is lehet."
        ),
        "teny": (
            "Az egész új geometriát huszonnégy oldalon írta le. Ez a rövid "
            "függelék az apja könyve mögött jelent meg, és megváltoztatta a "
            "matematikát."
        ),
        "erdekesseg": (
            "Kiváló hegedűs és vívó volt. A hagyomány szerint egyszer tizenhárom "
            "tisztet hívott ki egymás után, és a szünetekben hegedült."
        ),
        "idezet": "Semmiből egy új, más világot teremtettem.",
    },
]


# ══ segédfüggvények ═════════════════════════════════════════════════════════
def _norm(s: str) -> str:
    """Ékezet- és kisbetű-független összehasonlításhoz."""
    s = unicodedata.normalize("NFD", (s or "").lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn").strip()


def kartya_by_id(kartya_id: str) -> dict | None:
    for k in KARTYAK:
        if k["id"] == kartya_id:
            return k
    return None


def kartyak_leckehez(
    oldal: str, targy: str, evfolyam: int, lecke: str
) -> list[dict]:
    """A megadott leckéhez tartozó kártyák.

    A lecke nevét részegyezéssel keressük, mert a tantervi témakör neve
    hosszabb lehet, mint amit a katalógusba írtunk.
    """
    if not lecke:
        return []
    l = _norm(lecke)
    t = _norm(targy)
    talalt = []
    for k in KARTYAK:
        if k["oldal"] != oldal or int(k["evfolyam"]) != int(evfolyam or 0):
            continue
        if _norm(k["targy"]) not in t and t not in _norm(k["targy"]):
            continue
        kl = _norm(k["lecke"])
        if kl in l or l in kl:
            talalt.append(k)
            continue
        # tartalék: legalább két érdemi szó egyezik
        jelentos = lambda sz: {w for w in sz.split() if len(w) > 4}
        if len(jelentos(kl) & jelentos(l)) >= 2:
            talalt.append(k)
    return talalt


def kartyak_targyhoz(oldal: str, targy: str, evfolyam: int) -> list[dict]:
    t = _norm(targy)
    return [
        k for k in KARTYAK
        if k["oldal"] == oldal
        and int(k["evfolyam"]) == int(evfolyam or 0)
        and (_norm(k["targy"]) in t or t in _norm(k["targy"]))
    ]


def osszes_kartya(oldal: str | None = None) -> list[dict]:
    if oldal is None:
        return list(KARTYAK)
    return [k for k in KARTYAK if k["oldal"] == oldal]


def targy_szin(targy: str) -> str:
    for nev, szin in TARGY_SZIN.items():
        if _norm(nev) in _norm(targy) or _norm(targy) in _norm(nev):
            return szin
    return ALAP_SZIN


def kep_utvonal(k: dict) -> str:
    """A kártyakép relatív útvonala a static mappán belül."""
    return f"kartyak/{k['oldal']}/{k['kep']}.png"
