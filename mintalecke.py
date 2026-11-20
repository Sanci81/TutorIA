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
             "kep": "img:alma", "kerdes": "Melyik szó kezdődik ugyanazzal a betűvel, mint az ALMA?",
             "opciok": ["labda", "mókus", "autó"], "jo": 2, "miert": "Az <b>a</b>utó is <b>a</b> betűvel kezdődik."},
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


# ── BESZÉLGETŐS MINTALECKE (fix217, Sándor 11.19) ───────────────────────────
# A régi mintalecke 3 választós kérdés volt – „sima kvíznek” látszott, és pont
# azt nem mutatta, amiben jók vagyunk: a tanító BESZÉLGET, a rossz válaszra
# MÁSKÉPP magyaráz, és van valódi, megfogható feladat (tízes keret).
# Továbbra is előre megírt, AI nélkül, ingyen. Lépésfajták:
#   {"tan": [üzenetek]}                       – a tanító ír (gépelés-jelzővel)
#   {"val": [opciók], "jo": i, "ha_jo": [...], "ha_rossz": [...]}
#        – a gyerek válaszgombjai; rossznál a tanító másképp magyaráz, és újra kérdez
#   {"tizes": [a, b], "tan": [üzenet a feladathoz]} – tízes keret: a kék pöttyöket
#        koppintással átrakja, amíg 10 nem lesz
#   {"kerdez": [[kérdés, válasz], ...], "tovabb": felirat}
#        – „te is kérdezhetsz”: a gyerek választ egy kérdést, a tanító válaszol
CHAT = {
    "hu": {
        # ── 1. OSZTÁLY: betűk és hangok (fix222) ──
        1: [
            {"tan": ["Szia! 👋 Én vagyok a tanítód.",
                     "Ma a <b>hangokkal és a betűkkel</b> játszunk.",
                     "Nézd a táblát: ez egy <b>alma</b>. Mondd ki nagyon lassan: <b>aaa – l – m – a</b>."],
             "tabla": {"cim": "ALMA", "kep": "alma"}},
            {"tan": ["Melyik hanggal kezdődik az <b>alma</b>?"]},
            {"val": ["L", "A", "M"], "jo": 1,
             "ha_jo": ["Igen, <b>A</b>-val! 🎉 Jól figyeltél: <b>a</b>-lma."], "tabla_jo": "<span class=\"mc-zold\">A</span>LMA",
             "ha_rossz": ["Figyeld, mi jön ki <b>legelőször</b> a szádon: <b>aaa</b>-lma. Próbáld újra!"]},
            {"betuk": "HAL", "lapok": ["L", "O", "H", "A"], "kep": "hal", "cim": "_ _ _",
             "tan": ["Most rakd ki te a <b>hal</b> szót a táblán!", "Mondd lassan: <b>h – a – l</b>, és koppints a betűkre sorban."],
             "tipp": "Mondd lassan: h – a – l. Melyik hang jön most?",
             "kesz": "Ügyes! <b>H – A – L</b>. 🎉 Te raktad ki!"},
            {"kerdez": [["Mi a különbség a hang és a betű között? 🤔",
                         "A <b>hangot</b> halljuk és kimondjuk, a <b>betűt</b> leírjuk és látjuk. Az „a” hangot az <b>A</b> betűvel írjuk le."],
                        ["Miért jó ezt tudni?",
                         "Mert ha hallod, milyen hangokból áll egy szó, akkor el is tudod <b>olvasni</b> és le is tudod <b>írni</b>! 📖"]],
             "tovabb": "Értem, jöhet a következő! ✅",
             "tan": ["Ha valami nem világos, <b>kérdezz bátran</b> – válaszolok. 🙂"],
             "tabla": {"cim": "Hang 👂 → betű ✏️", "lista": ["Hallom: <b>a – l – m – a</b>", "Leírom: <b>ALMA</b>"]}},
            {"taps": ["S", "Ü", "N"], "kep": "sun", "gomb": "👏 Taps!", "cim": "? ? ?",
             "tan": ["Most tapsoljunk! Ez egy <b>sün</b>.", "Minden hangnál tapsolj egyet: koppints a <b>👏 Taps</b> gombra!"],
             "kesz": "Három taps, három hang: <b>S – Ü – N</b>! 👏"},
            {"tan": ["Ügyes voltál! 💪 A valódi órán így tanulunk tovább: játékosan, és ha elakadsz, másképp is elmagyarázom."],
             "tabla": {"cim": "Ügyes voltál! 🏆", "lista": ["<b>A</b>LMA – az első hang: A ✓", "H – A – L ✓", "S – Ü – N: 3 hang ✓"]}},
        ],
        # ── 4. OSZTÁLY: szorzás (fix222) ──
        4: [
            {"tan": ["Szia! 👋 Én vagyok a tanítód.",
                     "Ma a <b>szorzást</b> nézzük meg: ez a „gyors összeadás”.",
                     "Kérdés: <b>3 tányéron 4-4 alma</b> van. Hány alma van összesen?"],
             "tabla": {"cim": "3 × 4 = ?", "kep": "tanyerok"}},
            {"val": ["7", "12", "34"], "jo": 1,
             "ha_jo": ["Igen, <b>12</b>! 🎉 Nézzük meg, miért."],
             "ha_rossz": ["Majdnem! Rakjuk ki együtt a tányérokat. 🙂"], "tovabb_rosszra": True},
            {"tanyer": [3, 4], "gomb": "➕ Tányér", "cim": "3 × 4 = ?",
             "tan": ["Koppints a <b>➕ Tányér</b> gombra: mindegyik tányéron <b>4 alma</b> van.", "Összesen <b>3 tányér</b> kell!"],
             "kesz": "4 + 4 + 4 = 12. Ezt rövidebben így írjuk: <b>3 × 4 = 12</b>. ✨"},
            {"kerdez": [["Miért jobb szorozni, mint összeadni? 🤔",
                         "Mert <b>gyorsabb</b>! 10 tányérnál tízszer leírni, hogy 4 + 4 + 4 + … hosszú – a <b>10 × 4 = 40</b> egy pillanat."],
                        ["Mindegy, hogy 3 × 4 vagy 4 × 3?",
                         "Igen, <b>ugyanannyi</b>! 3 tányér 4 almával és 4 tányér 3 almával is 12 alma. A szorzásnál a számok helyet cserélhetnek."]],
             "tovabb": "Értem, jöhet a következő! ✅",
             "tan": ["Ha valami nem világos, <b>kérdezz bátran</b> – válaszolok. 🙂"],
             "tabla": {"cim": "Szorzás = gyors összeadás", "lista": ["4 + 4 + 4 = 12", "<b>3 × 4 = 12</b>", "4 × 3 = 12 (ugyanannyi!)"]}},
            {"tan": ["Most egy szöveges feladat: egy dobozban <b>8 ceruza</b> van.", "Hány ceruza van <b>4 dobozban</b>?"],
             "tabla": {"cim": "4 × 8 = ?", "kep": "ceruzak"}},
            {"val": ["12", "32", "36"], "jo": 1,
             "ha_jo": ["Szuper! 🎉 <b>4 × 8 = 32</b> ceruza."], "tabla_jo": "4 × 8 = <span class=\"mc-zold\">32 ✓</span>",
             "ha_rossz": ["Gondolj a tányérokra: 4 doboz, mindegyikben 8. <b>8 + 8 + 8 + 8</b> = ? Próbáld újra!"]},
            {"tan": ["Ügyes voltál! 💪 A valódi órán így haladunk tovább: egyre nehezebb feladatokkal, és ha elakadsz, másképp is elmagyarázom."],
             "tabla": {"cim": "Ügyes voltál! 🏆", "lista": ["3 × 4 = 12 ✓", "4 × 8 = 32 ✓", "Szorzás = gyors összeadás 💡"]}},
        ],
        2: [
            {"tan": ["Szia! 👋 Én vagyok a tanítód.",
                     "Ma egy ügyes trükköt tanulunk: hogyan adjunk össze, ha <b>átlépjük a 10-et</b>.",
                     "Kezdjük egy kérdéssel: mennyi <b>8 + 5</b>?"],
             "tabla": {"cim": "8 + 5 = ?", "keret": [8, 5]}},
            {"val": ["12", "13", "14"], "jo": 1,
             "ha_jo": ["Igen, <b>13</b>! 🎉 Most megmutatom, hogyan lehet ezt fejben is könnyen kiszámolni."],
             "ha_rossz": ["Majdnem! Semmi baj – nézzük meg együtt, lépésenként. 🙂"], "tovabb_rosszra": True},
            {"tizes": [8, 5], "cim": "8 + 5 = ?", "tan": ["Nézd a táblát: <b>8 piros</b> pötty van a tízes keretben, és <b>5 kék</b> mellette.",
                                       "Koppints a kék pöttyökre, és rakd át őket, amíg <b>tele nem lesz a keret</b>!"],
             "kesz": "Pont <b>10</b> lett! 🙌 Kint maradt még <b>3</b> kék."},
            {"tan": ["Tehát 8 + 5 ugyanannyi, mint <b>10 + 3</b>. Mennyi az?"], "tabla_cim": "8 + 5 = 10 + 3 = ?"},
            {"val": ["103", "13", "11"], "jo": 1,
             "ha_jo": ["Úgy van, <b>13</b>! A 10-hez könnyű hozzáadni: 10 + 3 = 13."], "tabla_jo": "8 + 5 = 10 + 3 = <span class=\"mc-zold\">13 ✓</span>",
             "ha_rossz": ["Nézd meg így: <b>1 teli tízes</b> és még <b>3</b>. A tízes 10, mellé 3: az <b>13</b>. Próbáld újra!"]},
            {"kerdez": [["Miért pont 10-ig töltjük fel? 🤔",
                         "Mert a 10-hez a legkönnyebb hozzáadni! 10 + 3, 10 + 6 – ezt már számolni sem kell. Ezért előbb kiegészítjük 10-re, és csak utána jön a maradék."],
                        ["Az ujjaimon is lehet?",
                         "Persze! A két kezeden pont 10 ujj van – ez is egy tízes keret. 😊 De a trükk nagy számoknál is működik, ott már nem lesz elég az ujj."]],
             "tovabb": "Értem, jöhet a következő! ✅",
             "tan": ["Ha valami nem világos, <b>kérdezz bátran</b> – válaszolok. 🙂"],
             "tabla": {"cim": "A trükk 💡", "lista": ["1. Töltsd fel <b>10-ig</b>", "2. Add hozzá, ami <b>kimaradt</b>", "8 + 5 → 10 + 3 = 13"]}},
            {"tizes": [7, 6], "cim": "7 + 6 = ?", "tan": ["Most te jössz egyedül: <b>7 + 6</b>.", "Töltsd fel a tízes keretet a táblán!"],
             "kesz": "Tele van! Kint maradt <b>3</b>. Mennyi lett összesen?"},
            {"val": ["12", "13", "14"], "jo": 1,
             "ha_jo": ["Szuper! 🎉 <b>7 + 6 = 13</b>. Először 10-ig (7 + 3), aztán a maradék 3."], "tabla_jo": "7 + 6 = 10 + 3 = <span class=\"mc-zold\">13 ✓</span>",
             "ha_rossz": ["Számold meg a kintieket: <b>3</b> maradt. 10 + 3 = ? Próbáld újra!"]},
            {"tan": ["Ügyes voltál! 💪 A valódi órán így haladunk tovább: egyre nehezebb feladatokkal, és ha elakadsz, másképp is elmagyarázom."],
             "tabla": {"cim": "Ügyes voltál! 🏆", "lista": ["8 + 5 = 13 ✓", "7 + 6 = 13 ✓", "Megtanultad a tízes trükköt 💡"]}},
        ],
    },
    "es": {
        # ── 1.º: letras y sonidos (fix222) ──
        1: [
            {"tan": ["¡Hola! 👋 Soy tu profe.",
                     "Hoy jugamos con los <b>sonidos y las letras</b>.",
                     "Mira la pizarra: es un <b>oso</b>. Dilo muy despacio: <b>ooo – s – o</b>."],
             "tabla": {"cim": "OSO", "kep": "medve"}},
            {"tan": ["¿Con qué letra empieza <b>oso</b>?"]},
            {"val": ["S", "A", "O"], "jo": 2,
             "ha_jo": ["¡Sí, con la <b>O</b>! 🎉 Has escuchado muy bien: <b>o</b>-so."], "tabla_jo": "<span class=\"mc-zold\">O</span>SO",
             "ha_rossz": ["Fíjate en lo que sale <b>primero</b> de tu boca: <b>ooo</b>-so. ¡Prueba otra vez!"]},
            {"betuk": "MESA", "lapok": ["S", "A", "M", "P", "E"], "kep": "asztal", "cim": "_ _ _ _",
             "tan": ["Ahora forma tú la palabra <b>mesa</b> en la pizarra.", "Dilo despacio: <b>m – e – s – a</b>, y toca las letras en orden."],
             "tipp": "Dilo despacio: m – e – s – a. ¿Qué sonido va ahora?",
             "kesz": "¡Muy bien! <b>M – E – S – A</b>. 🎉 ¡La has formado tú!"},
            {"kerdez": [["¿Qué es una sílaba? 🤔",
                         "Es un trocito de palabra que decimos de <b>un solo golpe de voz</b>: pe – lo – ta. ¡Cada palmada, una sílaba!"],
                        ["¿Sonido y letra es lo mismo?",
                         "Casi: el <b>sonido</b> lo oímos y lo decimos; la <b>letra</b> la escribimos y la vemos. El sonido «m» se escribe con la letra <b>M</b>."]],
             "tovabb": "¡Entendido, sigamos! ✅",
             "tan": ["Si algo no está claro, <b>pregúntame</b>: te contesto. 🙂"],
             "tabla": {"cim": "Sonido 👂 → letra ✏️", "lista": ["Oigo: <b>m – e – s – a</b>", "Escribo: <b>MESA</b>"]}},
            {"taps": ["PE", "LO", "TA"], "kep": "labda", "gomb": "👏 ¡Palmada!", "cim": "? ? ?",
             "tan": ["¡Ahora damos palmadas! Es una <b>pelota</b>.", "Da una palmada por cada <b>sílaba</b>: toca el botón <b>👏 ¡Palmada!</b>"],
             "kesz": "Tres palmadas, tres sílabas: <b>PE – LO – TA</b>! 👏"},
            {"tan": ["¡Muy bien! 💪 En la clase de verdad seguimos así: jugando y, si te atascas, te lo explico de otra manera."],
             "tabla": {"cim": "¡Muy bien! 🏆", "lista": ["<b>O</b>SO – empieza por O ✓", "M – E – S – A ✓", "PE – LO – TA: 3 sílabas ✓"]}},
        ],
        # ── 4.º: la multiplicación (fix222) ──
        4: [
            {"tan": ["¡Hola! 👋 Soy tu profe.",
                     "Hoy vemos la <b>multiplicación</b>: es una «suma rápida».",
                     "Pregunta: hay <b>3 platos con 4 manzanas</b> cada uno. ¿Cuántas manzanas hay en total?"],
             "tabla": {"cim": "3 × 4 = ?", "kep": "tanyerok"}},
            {"val": ["7", "12", "34"], "jo": 1,
             "ha_jo": ["¡Sí, <b>12</b>! 🎉 Vamos a ver por qué."],
             "ha_rossz": ["¡Casi! Vamos a poner los platos juntos. 🙂"], "tovabb_rosszra": True},
            {"tanyer": [3, 4], "gomb": "➕ Plato", "cim": "3 × 4 = ?",
             "tan": ["Toca el botón <b>➕ Plato</b>: en cada plato hay <b>4 manzanas</b>.", "¡Hacen falta <b>3 platos</b>!"],
             "kesz": "4 + 4 + 4 = 12. Más corto se escribe así: <b>3 × 4 = 12</b>. ✨"},
            {"kerdez": [["¿Por qué es mejor multiplicar que sumar? 🤔",
                         "¡Porque es <b>más rápido</b>! Con 10 platos, escribir 4 + 4 + 4 + … diez veces es muy largo; <b>10 × 4 = 40</b> es un momento."],
                        ["¿Es lo mismo 3 × 4 que 4 × 3?",
                         "¡Sí, da <b>lo mismo</b>! 3 platos de 4 manzanas y 4 platos de 3 manzanas son 12 manzanas. En la multiplicación el orden no cambia el resultado."]],
             "tovabb": "¡Entendido, sigamos! ✅",
             "tan": ["Si algo no está claro, <b>pregúntame</b>: te contesto. 🙂"],
             "tabla": {"cim": "Multiplicar = sumar rápido", "lista": ["4 + 4 + 4 = 12", "<b>3 × 4 = 12</b>", "4 × 3 = 12 (¡lo mismo!)"]}},
            {"tan": ["Ahora un problema: en una caja hay <b>8 lápices</b>.", "¿Cuántos lápices hay en <b>4 cajas</b>?"],
             "tabla": {"cim": "4 × 8 = ?", "kep": "ceruzak"}},
            {"val": ["12", "32", "36"], "jo": 1,
             "ha_jo": ["¡Genial! 🎉 <b>4 × 8 = 32</b> lápices."], "tabla_jo": "4 × 8 = <span class=\"mc-zold\">32 ✓</span>",
             "ha_rossz": ["Piensa en los platos: 4 cajas con 8 en cada una. <b>8 + 8 + 8 + 8</b> = ? ¡Prueba otra vez!"]},
            {"tan": ["¡Muy bien! 💪 En la clase de verdad seguimos así: con ejercicios cada vez más difíciles y, si te atascas, te lo explico de otra manera."],
             "tabla": {"cim": "¡Muy bien! 🏆", "lista": ["3 × 4 = 12 ✓", "4 × 8 = 32 ✓", "Multiplicar = sumar rápido 💡"]}},
        ],
        2: [
            {"tan": ["¡Hola! 👋 Soy tu profe.",
                     "Hoy aprendemos un truco para sumar cuando <b>pasamos del 10</b>.",
                     "Empezamos con una pregunta: ¿cuánto es <b>8 + 5</b>?"],
             "tabla": {"cim": "8 + 5 = ?", "keret": [8, 5]}},
            {"val": ["12", "13", "14"], "jo": 1,
             "ha_jo": ["¡Sí, <b>13</b>! 🎉 Ahora te enseño cómo calcularlo fácil, de cabeza."],
             "ha_rossz": ["¡Casi! No pasa nada: lo vemos juntos, paso a paso. 🙂"], "tovabb_rosszra": True},
            {"tizes": [8, 5], "cim": "8 + 5 = ?", "tan": ["Mira la pizarra: hay <b>8 puntos rojos</b> en la caja de diez y <b>5 azules</b> al lado.",
                                       "Toca los puntos azules para pasarlos hasta que <b>la caja esté llena</b>."],
             "kesz": "¡Justo <b>10</b>! 🙌 Fuera quedan <b>3</b> azules."},
            {"tan": ["Entonces 8 + 5 es lo mismo que <b>10 + 3</b>. ¿Cuánto es?"], "tabla_cim": "8 + 5 = 10 + 3 = ?"},
            {"val": ["103", "13", "11"], "jo": 1,
             "ha_jo": ["¡Eso es, <b>13</b>! Al 10 es fácil sumarle: 10 + 3 = 13."], "tabla_jo": "8 + 5 = 10 + 3 = <span class=\"mc-zold\">13 ✓</span>",
             "ha_rossz": ["Míralo así: <b>una decena llena</b> y <b>3</b> más. La decena es 10, y 3 más: <b>13</b>. ¡Prueba otra vez!"]},
            {"kerdez": [["¿Por qué llenamos hasta 10? 🤔",
                         "¡Porque al 10 es lo más fácil sumarle! 10 + 3, 10 + 6… eso casi ni se calcula. Por eso primero completamos el 10 y luego sumamos lo que queda."],
                        ["¿Puedo usar los dedos?",
                         "¡Claro! En las dos manos tienes justo 10 dedos: también es una caja de diez. 😊 Pero el truco sirve también con números grandes, donde los dedos ya no llegan."]],
             "tovabb": "¡Entendido, sigamos! ✅",
             "tan": ["Si algo no está claro, <b>pregúntame</b>: te contesto. 🙂"],
             "tabla": {"cim": "El truco 💡", "lista": ["1. Llena hasta <b>10</b>", "2. Suma lo que <b>queda</b>", "8 + 5 → 10 + 3 = 13"]}},
            {"tizes": [7, 6], "cim": "7 + 6 = ?", "tan": ["Ahora tú solo: <b>7 + 6</b>.", "¡Llena la caja de diez en la pizarra!"],
             "kesz": "¡Llena! Fuera quedan <b>3</b>. ¿Cuánto es en total?"},
            {"val": ["12", "13", "14"], "jo": 1,
             "ha_jo": ["¡Genial! 🎉 <b>7 + 6 = 13</b>. Primero hasta 10 (7 + 3) y luego lo que queda, 3."], "tabla_jo": "7 + 6 = 10 + 3 = <span class=\"mc-zold\">13 ✓</span>",
             "ha_rossz": ["Cuenta los de fuera: quedan <b>3</b>. 10 + 3 = ? ¡Prueba otra vez!"]},
            {"tan": ["¡Muy bien! 💪 En la clase de verdad seguimos así: con ejercicios cada vez más difíciles y, si te atascas, te lo explico de otra manera."],
             "tabla": {"cim": "¡Muy bien! 🏆", "lista": ["8 + 5 = 13 ✓", "7 + 6 = 13 ✓", "Has aprendido el truco del 10 💡"]}},
        ],
    },
}


def chat(nyelv: str, evfolyam: int) -> list | None:
    return (CHAT.get(nyelv) or {}).get(int(evfolyam))
