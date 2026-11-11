# -*- coding: utf-8 -*-
"""MINTALECKÉK regisztráció nélkül (2026-11-11, Sándor).

A főoldal évfolyam-csempéiről indulnak. ELŐRE MEGÍRT szöveg – nincs AI-hívás,
nincs költség, nem mentünk el semmit. Évfolyamonként MÁS tantárgy (nem mindig
matek), 3 lépés: rövid magyarázat → választós feladat (✓ / konfetti / „Szuper”,
rossz válasznál piros keret) → rövid indoklás.

Lépés: tanit (HTML, saját szöveg), kep (emoji; a „|” külön tányérokra bont), kerdes, opciok, jo (sorszám 0-tól),
miert (a válasz után megjelenő 1 mondat).
"""

LECKEK = {
    "hu": {
        1: {"targy": "Magyar nyelv", "tema": "Betűk és hangok", "lepesek": [
            {"tanit": "Minden szó <b>hangokból</b> áll. Mondd ki lassan: <b>a-l-m-a</b>. Az <b>alma</b> első hangja: <b>a</b>.",
             "kep": "img:alma", "kerdes": "Melyik szó kezdődik ugyanazzal a hanggal, mint az ALMA?",
             "opciok": ["autó", "labda", "mókus"], "jo": 0, "miert": "Az <b>a</b>utó is <b>a</b> hanggal kezdődik."},
            {"tanit": "Figyeld meg a szó elejét! A <b>hal</b> szót így mondjuk ki: <b>h-a-l</b>.",
             "kep": "img:hal", "kerdes": "Melyik betűvel kezdődik a HAL szó?",
             "opciok": ["L", "H", "A"], "jo": 1, "miert": "<b>H</b>-a-l: az első betű a <b>H</b>."},
            {"tanit": "Meg is számolhatjuk a hangokat. Tapsolj minden hangnál: <b>s – ü – n</b>.",
             "kep": "img:sun", "kerdes": "Hány betűből áll a SÜN szó?",
             "opciok": ["2", "3", "4"], "jo": 1, "miert": "S – ü – n: három betű, három taps."},
        ]},
        2: {"targy": "Matematika", "tema": "Összeadás tízesátlépéssel", "lepesek": [
            {"tanit": "A <b>8 + 5</b>-öt könnyebb két lépésben: először <b>10-ig</b> megyünk (8 + 2 = 10), aztán a maradék: 10 + 3 = <b>13</b>.",
             "kep": "img:tizes", "kerdes": "Szerinted mennyi 7 + 6?",
             "opciok": ["12", "13", "14"], "jo": 1, "miert": "7 + 3 = 10, aztán 10 + 3 = <b>13</b>."},
            {"tanit": "Kerek tízesekkel is így megy: <b>30 + 40 = 70</b>, mert 3 tízes + 4 tízes = 7 tízes.",
             "kep": "img:tizesek", "kerdes": "Mennyi 50 + 20?",
             "opciok": ["70", "520", "25"], "jo": 0, "miert": "5 tízes + 2 tízes = 7 tízes, vagyis <b>70</b>."},
            {"tanit": "Most egy kis történet: <b>Pannának 24 matricája van, és kap még 5-öt.</b>",
             "kep": "img:matrica", "kerdes": "Hány matricája lesz Pannának?",
             "opciok": ["29", "19", "28"], "jo": 0, "miert": "24 + 5 = <b>29</b>: a tízesek maradnak, az egyesek 4 + 5 = 9."},
        ]},
        3: {"targy": "Környezetismeret", "tema": "Az évszakok", "lepesek": [
            {"tanit": "Egy évben <b>négy évszak</b> van: tavasz, nyár, ősz és tél. Mindegyiknek megvannak a jelei.",
             "kep": "img:osz", "kerdes": "Melyik évszakban hullanak le a falevelek?",
             "opciok": ["tavasz", "ősz", "nyár"], "jo": 1, "miert": "<b>Ősszel</b> a fák elszíneződnek, és lehullajtják a leveleiket."},
            {"tanit": "Az évszakok mindig ugyanabban a sorrendben jönnek: tavasz → nyár → ősz → tél → és újra tavasz.",
             "kep": "img:evszakok", "kerdes": "Melyik évszak jön a tél után?",
             "opciok": ["ősz", "nyár", "tavasz"], "jo": 2, "miert": "A tél után <b>tavasz</b> jön: kezd melegedni, nyílnak az első virágok."},
            {"tanit": "Minden évszakhoz három hónap tartozik. A <b>tél</b> hónapjai: december, január, február.",
             "kep": "img:naptar", "kerdes": "Melyik hónap van télen?",
             "opciok": ["július", "január", "május"], "jo": 1, "miert": "A <b>január</b> téli hónap. A július nyári, a május tavaszi."},
        ]},
        4: {"targy": "Matematika", "tema": "Szorzás", "lepesek": [
            {"tanit": "Ha <b>3 tányéron 4-4 alma</b> van, nem kell egyenként számolni. Mondhatjuk így is: <b>3 × 4</b>.",
             "kep": "img:tanyerok", "kerdes": "Szerinted hány alma van összesen?",
             "opciok": ["7", "12", "10", "34"], "jo": 1, "miert": "3 × 4 = 4 + 4 + 4 = <b>12</b>."},
            {"tanit": "A szorzásnál a számok <b>helyet cserélhetnek</b>: 3 × 4 ugyanannyi, mint 4 × 3.",
             "kep": "img:forgas", "kerdes": "Mennyi 6 × 5?",
             "opciok": ["30", "11", "35"], "jo": 0, "miert": "6 × 5 = 5 × 6 = <b>30</b>."},
            {"tanit": "Szöveges feladat: <b>egy dobozban 8 ceruza van.</b>",
             "kep": "img:ceruzak", "kerdes": "Hány ceruza van 4 dobozban?",
             "opciok": ["12", "32", "36"], "jo": 1, "miert": "4 × 8 = <b>32</b> ceruza."},
        ]},
        5: {"targy": "Magyar nyelv", "tema": "Szófajok", "lepesek": [
            {"tanit": "A <b>főnév</b> élőlényt, tárgyat vagy fogalmat nevez meg: kutya, asztal, öröm.",
             "kep": "img:iskola", "kerdes": "Melyik szó főnév?",
             "opciok": ["szalad", "iskola", "piros"], "jo": 1, "miert": "Az <b>iskola</b> egy dolgot nevez meg, ezért főnév."},
            {"tanit": "Az <b>ige</b> cselekvést vagy történést jelent: fut, olvas, esik.",
             "kep": "img:beka", "kerdes": "Melyik szó ige?",
             "opciok": ["ugrik", "ház", "zöld"], "jo": 0, "miert": "Az <b>ugrik</b> azt mondja meg, mit csinál valaki: ez ige."},
            {"tanit": "A <b>melléknév</b> tulajdonságot fejez ki: magas, kék, gyors.",
             "kep": "img:nyul", "kerdes": "Melyik szó melléknév ebben a mondatban: „A gyors nyúl elfutott.”?",
             "opciok": ["nyúl", "gyors", "elfutott"], "jo": 1, "miert": "A <b>gyors</b> azt mondja meg, milyen a nyúl."},
        ]},
        6: {"targy": "Matematika", "tema": "Törtek", "lepesek": [
            {"tanit": "A tört megmutatja, <b>hány egyenlő részre</b> osztottunk valamit (alul), és <b>hányat vettünk</b> belőle (felül).",
             "kep": "img:pizza", "kerdes": "Egy pizzát 8 egyenlő szeletre vágtunk, és 3 szeletet megettünk. Mekkora részét ettük meg?",
             "opciok": ["3/8", "8/3", "3/5"], "jo": 0, "miert": "8 részből 3-at: <b>3/8</b>."},
            {"tanit": "Ha a törtek alul (a nevezőben) egyformák, csak a felső számokat adjuk össze: 1/5 + 2/5 = 3/5.",
             "kep": "img:tortek", "kerdes": "Mennyi 2/7 + 3/7?",
             "opciok": ["5/7", "5/14", "6/7"], "jo": 0, "miert": "2 + 3 = 5, a nevező marad 7: <b>5/7</b>."},
            {"tanit": "Ugyanaz a rész többféleképpen is leírható: <b>1/2 = 2/4 = 3/6</b> – nézd, mindhárom körnek a fele színes. Ha a számlálót és a nevezőt is ugyanazzal a számmal szorozzuk, a tört értéke nem változik.",
             "kep": "img:fele", "kerdes": "Melyik egyenlő 1/2-del?",
             "opciok": ["2/3", "4/8", "3/4"], "jo": 1, "miert": "1/2 = <b>4/8</b>, mert a 4 a 8-nak pont a fele."},
        ]},
        7: {"targy": "Kémia", "tema": "Halmazállapotok", "lepesek": [
            {"tanit": "Az anyagok három fő halmazállapota: <b>szilárd</b>, <b>folyékony</b> és <b>légnemű</b>.",
             "kep": "img:jeg", "kerdes": "Milyen halmazállapotú a jég?",
             "opciok": ["szilárd", "folyékony", "légnemű"], "jo": 0, "miert": "A jég megtartja az alakját: <b>szilárd</b>."},
            {"tanit": "<b>Olvadás</b>: a szilárd anyagból folyékony lesz. <b>Fagyás</b>: fordítva.",
             "kep": "img:olvadas", "kerdes": "Mi történik, amikor a jégkocka elolvad?",
             "opciok": ["szilárdból folyékony lesz", "folyékonyból légnemű lesz", "légneműből szilárd lesz"], "jo": 0,
             "miert": "Olvadáskor a <b>szilárd</b> jégből <b>folyékony</b> víz lesz."},
            {"tanit": "<b>Forrás</b>kor a folyadék belsejében is gőzbuborékok keletkeznek, és légnemű lesz belőle.",
             "kep": "img:forras", "kerdes": "Hány fokon forr a víz normál légköri nyomáson?",
             "opciok": ["0 °C", "50 °C", "100 °C"], "jo": 2, "miert": "A víz <b>100 °C</b>-on forr, 0 °C-on fagy meg."},
        ]},
        8: {"targy": "Matematika", "tema": "Függvénygép", "lepesek": [
            {"tanit": "A <b>függvénygép</b> minden bedobott számmal ugyanazt csinálja. Figyeld: <b>1 → 3, 2 → 5, 3 → 7</b>.",
             "kep": "img:gep", "kerdes": "Mit csinál a gép a számmal?",
             "opciok": ["x · 2 + 1", "x + 2", "x · 3"], "jo": 0,
             "miert": "1 · 2 + 1 = 3, 2 · 2 + 1 = 5, 3 · 2 + 1 = 7 – mindháromra jó. Az x + 2 és az x · 3 csak az elsőre."},
            {"tanit": "Ha ismerjük a szabályt (<b>x · 2 + 1</b>), bármilyen számra ki tudjuk számolni, mi jön ki.",
             "kep": "img:gep_be", "kerdes": "Mi jön ki, ha 10-et dobunk be?",
             "opciok": ["21", "20", "12"], "jo": 0, "miert": "10 · 2 + 1 = <b>21</b>."},
            {"tanit": "Visszafelé is lehet: ha tudjuk, mi jött ki, kitalálhatjuk, mit dobtunk be.",
             "kep": "img:gep_vissza", "kerdes": "Mit dobtunk be, ha 15 jött ki?",
             "opciok": ["7", "8", "30"], "jo": 0, "miert": "Előbb kivonjuk az 1-et (14), aztán felezünk: <b>7</b>. Próba: 7 · 2 + 1 = 15."},
        ]},
    },
    "es": {
        1: {"targy": "Lengua", "tema": "Letras y sonidos", "lepesek": [
            {"tanit": "Las palabras están hechas de <b>sonidos</b>. Dilo despacio: <b>o-s-o</b>. La primera letra de <b>oso</b> es la <b>o</b>.",
             "kep": "img:medve", "kerdes": "¿Con qué letra empieza OSO?",
             "opciok": ["S", "A", "O"], "jo": 2, "miert": "<b>O</b>-s-o: empieza por <b>o</b>."},
            {"tanit": "Fíjate en el principio de la palabra: <b>m</b>esa.",
             "kep": "img:asztal", "kerdes": "¿Qué palabra empieza como MESA?",
             "opciok": ["mano", "sol", "pato"], "jo": 0, "miert": "<b>M</b>ano y <b>m</b>esa empiezan por <b>m</b>."},
            {"tanit": "Las palabras se dividen en <b>sílabas</b>. Da una palmada en cada una: <b>pe – lo – ta</b>.",
             "kep": "img:labda", "kerdes": "¿Cuántas sílabas tiene PELOTA?",
             "opciok": ["2", "3", "4"], "jo": 1, "miert": "Pe – lo – ta: <b>tres</b> sílabas, tres palmadas."},
        ]},
        2: {"targy": "Matemáticas", "tema": "Sumas llegando a la decena", "lepesek": [
            {"tanit": "<b>8 + 5</b> es más fácil en dos pasos: primero llegamos a <b>10</b> (8 + 2 = 10) y luego lo que falta: 10 + 3 = <b>13</b>.",
             "kep": "img:tizes", "kerdes": "¿Cuánto crees que es 7 + 6?",
             "opciok": ["12", "13", "14"], "jo": 1, "miert": "7 + 3 = 10, y 10 + 3 = <b>13</b>."},
            {"tanit": "Con decenas también: <b>30 + 40 = 70</b>, porque 3 decenas + 4 decenas = 7 decenas.",
             "kep": "img:tizesek", "kerdes": "¿Cuánto es 50 + 20?",
             "opciok": ["70", "520", "25"], "jo": 0, "miert": "5 decenas + 2 decenas = 7 decenas: <b>70</b>."},
            {"tanit": "Un problema: <b>Lucía tiene 24 pegatinas y le dan 5 más.</b>",
             "kep": "img:matrica", "kerdes": "¿Cuántas pegatinas tiene ahora Lucía?",
             "opciok": ["29", "19", "28"], "jo": 0, "miert": "24 + 5 = <b>29</b>: las decenas se quedan, las unidades 4 + 5 = 9."},
        ]},
        3: {"targy": "Conocimiento del Medio", "tema": "Las estaciones", "lepesek": [
            {"tanit": "El año tiene <b>cuatro estaciones</b>: primavera, verano, otoño e invierno.",
             "kep": "img:osz", "kerdes": "¿En qué estación se caen las hojas de los árboles?",
             "opciok": ["primavera", "otoño", "verano"], "jo": 1, "miert": "En <b>otoño</b> las hojas cambian de color y se caen."},
            {"tanit": "Siempre van en el mismo orden: primavera → verano → otoño → invierno → y otra vez primavera.",
             "kep": "img:evszakok", "kerdes": "¿Qué estación viene después del invierno?",
             "opciok": ["otoño", "verano", "primavera"], "jo": 2, "miert": "Después del invierno llega la <b>primavera</b>."},
            {"tanit": "Cada estación dura unos tres meses. El <b>invierno</b>: diciembre, enero y febrero.",
             "kep": "img:naptar", "kerdes": "¿Qué mes es de invierno?",
             "opciok": ["julio", "enero", "mayo"], "jo": 1, "miert": "<b>Enero</b> es de invierno; julio es de verano y mayo de primavera."},
        ]},
        4: {"targy": "Matemáticas", "tema": "La multiplicación", "lepesek": [
            {"tanit": "Si hay <b>3 platos con 4 manzanas</b> cada uno, no hace falta contarlas una a una: es <b>3 × 4</b>.",
             "kep": "img:tanyerok", "kerdes": "¿Cuántas manzanas crees que hay en total?",
             "opciok": ["7", "12", "10", "34"], "jo": 1, "miert": "3 × 4 = 4 + 4 + 4 = <b>12</b>."},
            {"tanit": "En la multiplicación el orden <b>no cambia</b> el resultado: 3 × 4 = 4 × 3.",
             "kep": "img:forgas", "kerdes": "¿Cuánto es 6 × 5?",
             "opciok": ["30", "11", "35"], "jo": 0, "miert": "6 × 5 = 5 × 6 = <b>30</b>."},
            {"tanit": "Un problema: <b>en una caja hay 8 lápices.</b>",
             "kep": "img:ceruzak", "kerdes": "¿Cuántos lápices hay en 4 cajas?",
             "opciok": ["12", "32", "36"], "jo": 1, "miert": "4 × 8 = <b>32</b> lápices."},
        ]},
        5: {"targy": "Lengua", "tema": "Clases de palabras", "lepesek": [
            {"tanit": "El <b>sustantivo</b> nombra personas, animales, cosas o ideas: perro, mesa, alegría.",
             "kep": "img:iskola", "kerdes": "¿Cuál es un sustantivo?",
             "opciok": ["correr", "escuela", "rojo"], "jo": 1, "miert": "<b>Escuela</b> nombra un lugar: es un sustantivo."},
            {"tanit": "El <b>verbo</b> expresa acciones: corre, lee, llueve.",
             "kep": "img:beka", "kerdes": "¿Cuál es un verbo?",
             "opciok": ["salta", "casa", "verde"], "jo": 0, "miert": "<b>Salta</b> dice lo que hace alguien: es un verbo."},
            {"tanit": "El <b>adjetivo</b> dice cómo es algo: alto, azul, rápido.",
             "kep": "img:nyul", "kerdes": "¿Cuál es el adjetivo en «El conejo rápido corrió»?",
             "opciok": ["conejo", "rápido", "corrió"], "jo": 1, "miert": "<b>Rápido</b> dice cómo es el conejo."},
        ]},
        6: {"targy": "Matemáticas", "tema": "Fracciones", "lepesek": [
            {"tanit": "Una fracción dice en <b>cuántas partes iguales</b> dividimos algo (abajo) y <b>cuántas tomamos</b> (arriba).",
             "kep": "img:pizza", "kerdes": "Cortamos una pizza en 8 trozos iguales y nos comemos 3. ¿Qué parte nos hemos comido?",
             "opciok": ["3/8", "8/3", "3/5"], "jo": 0, "miert": "3 de 8 partes: <b>3/8</b>."},
            {"tanit": "Si las fracciones tienen el mismo denominador (abajo), solo sumamos los numeradores: 1/5 + 2/5 = 3/5.",
             "kep": "img:tortek", "kerdes": "¿Cuánto es 2/7 + 3/7?",
             "opciok": ["5/7", "5/14", "6/7"], "jo": 0, "miert": "2 + 3 = 5 y el denominador sigue siendo 7: <b>5/7</b>."},
            {"tanit": "La misma parte se puede escribir de varias formas: <b>1/2 = 2/4 = 3/6</b> – mira, los tres círculos tienen la mitad coloreada. Si multiplicamos el numerador y el denominador por el mismo número, la fracción vale lo mismo.",
             "kep": "img:fele", "kerdes": "¿Cuál es igual a 1/2?",
             "opciok": ["2/3", "4/8", "3/4"], "jo": 1, "miert": "1/2 = <b>4/8</b>, porque 4 es justo la mitad de 8."},
        ]},
    },
}


def lecke(nyelv: str, evfolyam: int) -> dict | None:
    return (LECKEK.get(nyelv) or {}).get(int(evfolyam))


def evfolyamok(nyelv: str) -> list[int]:
    return sorted((LECKEK.get(nyelv) or {}).keys())


def ellenoriz() -> list[str]:
    """Saját ellenőrzés: minden lépésben a „jo” sorszám létezik, nincs ismétlődő opció."""
    hibak = []
    for ny, lk in LECKEK.items():
        for e, l in lk.items():
            for i, s in enumerate(l["lepesek"]):
                if not (0 <= s["jo"] < len(s["opciok"])):
                    hibak.append(f"{ny}/{e}/{i}: jo index")
                if len(set(s["opciok"])) != len(s["opciok"]):
                    hibak.append(f"{ny}/{e}/{i}: ismétlődő opció")
    return hibak
