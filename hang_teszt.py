# -*- coding: utf-8 -*-
"""Ellenőrzi, hogy a felolvasó MIT MOND KI a leírt szövegből.

MIÉRT VAN EZ A FÁJL
    A hang.py minden hibája ugyanúgy néz ki: a képernyőn jó a szöveg, csak
    kimondva hibás. Ezt csak úgy lehet észrevenni, ha valaki meghallgatja —
    vagy ha egy ilyen lista végigfut rajta. Minden itteni sor egy valódi
    hiba emléke, amit egyszer már ki kellett javítani.

HASZNÁLAT
    python hang_teszt.py

    Ha mindent kiír "ok"-kal, mehet a push. Ha bármi ROSSZ, a kimenet
    megmutatja, mit várt és mit kapott.

HA ÚJ SZABÁLYT TESZEL A hang.py-BA
    Írj hozzá ide legalább két sort: egyet arra, amit MOSTANTÓL jól mond,
    és egyet arra, amit NEM SZABAD elrontania. A második a fontosabb.
"""

from __future__ import annotations

import sys

import hang

# (bemenet, aminek el kell hangoznia, miért van itt)
ESETEK: list[tuple[str, str, str]] = [
    # ── OSZTÁS: az osztó -val/-vel ragot kap ────────────────────────────
    ("Mennyi 8000 : 1000?", "Mennyi nyolcezer osztva ezerrel?",
     "rag nélkül 'osztva ezer' volt – magyartalan"),
    ("Számold ki: 360 : 9", "Számold ki: háromszázhatvan osztva kilenccel",
     "a rag minden számnál másképp hasonul"),
    ("Mennyi 100 : 20?", "Mennyi száz osztva hússzal?",
     "húsz → hússzal, nem 'húszval'"),
    ("Mennyi 100 : 4?", "Mennyi száz osztva néggyel?",
     "négy → néggyel, a gy megkettőződik"),
    ("Mennyi 12 : 2?", "Mennyi tizenkettő osztva kettővel?",
     "magánhangzóra végződik: -vel marad épen"),
    ("Mennyi 48 ÷ 6?", "Mennyi negyvennyolc osztva hattal?",
     "a ÷ jelnél nem kell szóköz"),

    # ── SZORZÁS ────────────────────────────────────────────────────────
    ("A 8 × 5 helyett gondolj 4 × 10-re.",
     "A nyolcszor öt helyett gondolj négyszer tízre.",
     "nem 'nyolc szorozva öt', hanem nyolcszor"),
    ("A 19 × 4 közel van a 20 × 4-hez.",
     "A tizenkilencszer négy közel van a hússzor négyhez.",
     "húsz → hússzor"),
    ("5 m × 3 m", "öt méter szor három méter",
     "méretnél 'szor', nem 'szorozva' – az ragot vonzana"),

    # ── AMI SZÁMJEGY MARADT ────────────────────────────────────────────
    ("4000 + 2000-re gondolj.", "négyezer meg kétezerre gondolj.",
     "az egyik szám szóban, a másik számjegyben volt"),
    ("80 - 30 = 50", "nyolcvan mínusz harminc egyenlő ötven",
     "a felolvasóra bízva találgatott"),
    ("Van 12 alma és 8 körte.", "Van tizenkét alma és nyolc körte.",
     "főnév előtt 'két', nem 'kettő'"),
    ("22 gyerek van az osztályban.", "huszonkét gyerek van az osztályban.",
     "huszonkettő → huszonkét főnév előtt"),
    ("Hány maradt? 2", "Hány maradt? kettő",
     "magában viszont marad a teljes alak"),
    ("1848-49 a szabadságharc.",
     "ezernyolcszáznegyvennyolc negyvenkilenc a szabadságharc.",
     "évszám-tartomány kötőjellel"),

    # ── AMIHEZ NEM SZABAD NYÚLNI ───────────────────────────────────────
    ("10:30-kor kezdődik az óra.", "10:30-kor kezdődik az óra.",
     "óra, nem osztás – a kettőspont körül nincs szóköz"),
    ("A 3/4 az háromnegyed.", "A 3/4 az háromnegyed.",
     "tört, nem osztás"),
    ("Az 1848-ban történt.", "Az ezernyolcszáznegyvennyolcban történt.",
     "toldalékos évszám: sorszámmá torzult volna"),
    ("Olvasd el a 3. feladatot!", "Olvasd el a 3. feladatot!",
     "ez tényleg sorszám: 'harmadik feladat'"),
    ("A hőmérséklet 3,5 fok.", "A hőmérséklet 3,5 fok.",
     "tizedes tört, nem két külön szám"),
    ("A terület 36 m².", "A terület harminchat négyzetméter.",
     "'harminchat em három' lett volna"),
    ("Ez 25%-a az egésznek.", "Ez huszonöt százaléka az egésznek.",
     "a kötőjeles toldalék külön betűződött volna"),
    ("A K = 4 × a képlet.", "A kerület egyenlő négyszer a képlet.",
     "mértani képletben a K kerületet jelent – ez SZÁNDÉKOS"),
]


def main() -> int:
    rossz = 0
    for be, vart, miert in ESETEK:
        kapott = hang.kiejtes(be, "hu")
        if kapott == vart:
            print(f"  ok    {be}")
            continue
        rossz += 1
        print(f"  ROSSZ {be}")
        print(f"        kapott: {kapott}")
        print(f"        várt:   {vart}")
        print(f"        miért:  {miert}")
    print()
    if rossz:
        print(f"{rossz} hiba a(z) {len(ESETEK)} esetből. NE PUSHOLJ.")
        return 1
    print(f"Mind a(z) {len(ESETEK)} eset rendben.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
