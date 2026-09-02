# -*- coding: utf-8 -*-
"""Ellenőrzi, MIT LÁT és MIT HALL a gyerek a tanár válaszából.

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
import szamellenor

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
    ("80 - 2 = 78", "nyolcvan mínusz kettő egyenlő hetvennyolc",
     "'mínusz KÉT egyenlő' volt – a 'két' csak megszámlált szó előtt áll"),
    ("2 meg 3 az 5", "kettő meg három az öt",
     "az operátor nem megszámlálható"),
    ("A 2 nagyobb mint az 1.", "A kettő nagyobb mint az egy.",
     "összehasonlításban sem rövidül"),
    ("Vegyél 2 tojást!", "Vegyél két tojást!",
     "megszámlált főnév előtt viszont IGEN"),
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

    # ── ARÁNY: nem osztás ──────────────────────────────────────────────
    ("Az arány 2 : 3 volt.", "Az arány kettő a háromhoz volt.",
     "'kettő osztva hárommal' volt – az arányt nem így mondjuk"),
    ("A fiúk és lányok aránya 3 : 5.",
     "A fiúk és lányok aránya három az öthöz.",
     "magánhangzó előtt 'az', nem 'a'"),
    ("Mennyi 6 : 2?", "Mennyi hat osztva kettővel?",
     "az 'arány' szó nélkül ez tényleg osztás – nem találgatunk"),
]

# Amit a gyerek LÁT: a szamellenor átírja a tanár mondatát, mielőtt kimegy.
# (bemenet, aminek látszania kell, miért van itt)
SZOVEG_ESETEK: list[tuple[str, str, str]] = [
    ("Most jön egy kis becslés: 48 × 2 inkább 80, 90 vagy 100?",
     "Most jön egy kis becslés: 48 × 2 inkább 80-hoz, 90-hez vagy 100-hoz "
     "van közelebb?",
     "rag és 'van közelebb' nélkül úgy hangzik, mintha 80/90/100 valamelyike "
     "lenne a pontos eredmény – pedig 96"),
    ("Szerinted a 19 × 4 inkább 60, 70 vagy 80?",
     "Szerinted a 19 × 4 inkább 60-hoz, 70-hez vagy 80-hoz van közelebb?",
     "ugyanaz a hiba, ez volt az első bejelentett esete"),
    ("Mennyi 5 × 5 inkább 20 vagy 25?",
     "Mennyi 5 × 5 inkább 20-hoz vagy 25-höz van közelebb?",
     "két lehetőségnél is működnie kell; 25 → -höz"),
    ("A 48 × 2 inkább 80-hoz, 90-hez vagy 100-hoz van közelebb?",
     "A 48 × 2 inkább 80-hoz, 90-hez vagy 100-hoz van közelebb?",
     "ha a tanár már jól fogalmazott, NEM írjuk át másodszor"),
    ("Szerinted ez inkább 2,5 vagy 3,5?",
     "Szerinted ez inkább 2,5 vagy 3,5?",
     "tizedes törtet nem ragozunk – inkább hagyjuk, mint elrontsuk"),
    ("Melyik tetszik jobban, inkább a piros vagy a kék?",
     "Melyik tetszik jobban, inkább a piros vagy a kék?",
     "nem számokról szól: hozzá se nyúlunk"),
    ("6 × 5 valóban 31?", "6 × 5 valóban 30?",
     "a hamis egyenlőséget javítjuk – a szorzás értéke nem vélemény"),
]

# A SZÓJEGYZÉK-JELÖLŐ. Ezt a lejátszott órák hozták elő: a jelölő ELTÜNTETTE
# a szót, amit a gyereknek meg kellett volna tanulnia.
JELOLO_ESETEK: list[tuple[str, str, str]] = [
    ("- <VOCAB>ma=hoy</VOCAB> = azt jelenti, hogy ma.",
     "- hoy = azt jelenti, hogy ma.",
     "a szó ELTŰNT: a gyerek '-  = azt jelenti, hogy ma'-t látott"),
    ("Nagyon jó! A <VOCAB>hoy</VOCAB> azt jelenti, hogy ma.",
     "Nagyon jó! A hoy azt jelenti, hogy ma.",
     "az '=' nélküli alakot semmi nem ismerte fel: a NYERS jelölő ment ki"),
    ("Most te jössz: melyik a „látott”? <VOCAB>látott=visto</VOCAB>"
     "<VOCAB>írt=escrito</VOCAB><VOCAB>készített=hecho</VOCAB>",
     "Most te jössz: melyik a „látott”? visto, escrito, hecho",
     "kérdés után a jelölők a VÁLASZLEHETŐSÉGEK – eltűntek, és a kérdésre "
     "nem lehetett válaszolni. A magyar megfelelő NEM látszhat: elárulná."),
    ("Ma két új szót tanulunk: <VOCAB>alma=manzana</VOCAB> és "
     "<VOCAB>körte=pera</VOCAB>.",
     "Ma két új szót tanulunk: manzana és pera.",
     "mondat közepén is a szó marad, nem a jelölés"),
    ("Az already azt mondja: „már”, a yet pedig: „még”. "
     "<VOCAB>már=already</VOCAB><VOCAB>még=yet</VOCAB>",
     "Az already azt mondja: „már”, a yet pedig: „még”.",
     "a mondat végi ÖSSZEFOGLALÓ szavai összeragadtak: „alreadyyet”. Ha a "
     "mondat már kimondta őket, a felsorolás felesleges — de a szójegyzékbe "
     "attól még bekerül"),
    ("Have you ever been to <FL:en>London</FL:en>? "
     "(Jártál már <FL:en>London</FL:en>ban?)",
     "Have you ever been to London? (Jártál már Londonban?)",
     "a záró tag NYELVKÓDDAL is jöhet: </FL:en>. A régi minta csak a </FL> "
     "alakot ismerte, ezért a NYERS jelölő ment ki a gyerekhez"),
    ("melyik objektív és melyik <FL:la>szubjektív>:",
     "melyik objektív és melyik szubjektív>:",
     "félbehagyott, záró pár nélküli jelölő – a szöveg marad, a tag megy"),
    ("Két új szó jön: <VOCAB>alma=manzana</VOCAB><VOCAB>körte=pera</VOCAB>",
     "Két új szó jön: manzana, pera",
     "ha a szavak MÉG NEM hangzottak el, látszaniuk kell — de vesszővel"),
]

# Ugyanaz a hiba a SPANYOL oldalon. Ott nincs rag: a "está más cerca de"
# fordulat hordozza, hogy közelséget kérdezünk, nem egyenlőséget.
SPANYOL_ESETEK: list[tuple[str, str, str]] = [
    ("Estimemos: ¿48 × 2 es más bien 80, 90 o 100?",
     "Estimemos: ¿48 × 2 está más cerca de 80, 90 o 100?",
     "'es más bien' egyenlőséget állít – a 48 × 2 az 96"),
    ("¿19 × 4 más bien 60, 70 o 80?",
     "¿19 × 4 está más cerca de 60, 70 o 80?",
     "ugyanaz kötőszó nélkül"),
    ("¿48 × 2 está más cerca de 80, 90 o 100?",
     "¿48 × 2 está más cerca de 80, 90 o 100?",
     "ha már jó, nem írjuk át másodszor"),
    ("¿Prefieres más bien el rojo o el azul?",
     "¿Prefieres más bien el rojo o el azul?",
     "nem számokról szól: hozzá se nyúlunk"),
]


def main() -> int:
    rossz = 0
    print("AMIT A GYEREK HALL (hang.py)")
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
    print("AMIT A GYEREK LÁT (szamellenor.py)")
    for be, vart, miert in SZOVEG_ESETEK:
        kapott, _ = szamellenor.chat_ellenoriz(be)
        if kapott == vart:
            print(f"  ok    {be}")
            continue
        rossz += 1
        print(f"  ROSSZ {be}")
        print(f"        kapott: {kapott}")
        print(f"        várt:   {vart}")
        print(f"        miért:  {miert}")

    print()
    print("AMIT A GYEREK LÁT (jelölők, app.py)")
    try:
        import logging
        import os
        logging.disable(logging.CRITICAL)
        os.environ.setdefault("SECRET_KEY", "hang-teszt")
        import app
        for be, vart, miert in JELOLO_ESETEK:
            kapott = app._parse_chat_markers(be)[0].strip()
            if kapott == vart:
                print(f"  ok    {be[:60]}")
                continue
            rossz += 1
            print(f"  ROSSZ {be[:60]}")
            print(f"        kapott: {kapott}")
            print(f"        várt:   {vart}")
            print(f"        miért:  {miert}")
    except Exception as _h:
        print(f"  (kihagyva – az app nem tölthető be: {_h})")

    print()
    print("A SPANYOL OLDAL (szamellenor.py)")
    for be, vart, miert in SPANYOL_ESETEK:
        kapott, _ = szamellenor.chat_ellenoriz(be, "es")
        if kapott == vart:
            print(f"  ok    {be}")
            continue
        rossz += 1
        print(f"  ROSSZ {be}")
        print(f"        kapott: {kapott}")
        print(f"        várt:   {vart}")
        print(f"        miért:  {miert}")

    osszes = (len(ESETEK) + len(SZOVEG_ESETEK) + len(SPANYOL_ESETEK)
              + len(JELOLO_ESETEK))
    print()
    if rossz:
        print(f"{rossz} hiba a(z) {osszes} esetből. NE PUSHOLJ.")
        return 1
    print(f"Mind a(z) {osszes} eset rendben.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
