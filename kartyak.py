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
STILUS_PROMPT = (
    'dynamic trading card hero art, edge to edge full bleed illustration, no border, no frame, half figure from the waist up with space above the head, wide awestruck eyes and slightly parted lips, wonder not anger, the light falling on the face and hands, deep shadows, warm rim light behind, bold saturated colours, high contrast, painterly digital illustration, no text, no letters, no signature, no watermark, no flame unless described'
)

KARTYAK: list[dict] = [
    {
        "id": "hu_kemia_7_curie",
        "oldal": "hu", "targy": 'Kémia', "evfolyam": 7,
        "lecke": 'Az atom felépítése',
        "nev": 'Marie Curie', "alnev": 'fizikus és kémikus · 1867–1934',
        "kep": "kemia_7_curie",
        "ritkasag": 'nagyon_ritka', "ero": 450,
        "kepesseg": 'Rádiumsugárzás', "kepesseg_ero": 380,
        "becenev": 'A SUGÁRZÓ',
        "leiras": 'Két új elemet talált – a polóniumot és a rádiumot –, és ő az egyetlen ember, aki két különböző tudományban kapott Nobel-díjat.',
        "teny": 'A jegyzetfüzetei ma is sugároznak. Ólomdobozban őrzik őket Párizsban, és aki bele akar nézni, előbb alá kell írnia, hogy a kockázatot maga vállalja.',
        "erdekesseg": 'Négy éven át hét tonna kőzetet főzött ki egy huzatos fészerben, hogy a végén egy tized gramm rádium maradjon a kezében.',
        "idezet": 'Az életben semmitől sem kell félni, csak meg kell érteni.',
        "prompt": 'a large glass flask on a laboratory bench with the liquid inside glowing from within with a cold green-white light, Marie Curie leaning over it holding a dropper, gaunt careworn face with a high forehead, dark chestnut hair waved and pinned up loosely, plain black high-necked long-sleeved dress of the 1900s with a small white collar, shelves of glass bottles and apparatus in the shadows behind her',
    },
    {
        "id": "hu_kemia_7_mengyelejev",
        "oldal": "hu", "targy": 'Kémia', "evfolyam": 7,
        "lecke": 'A periódusos rendszer és a vegyjelek',
        "nev": 'Mengyelejev', "alnev": 'kémikus · 1834–1907',
        "kep": "kemia_7_mengyelejev",
        "ritkasag": 'ritka', "ero": 310,
        "kepesseg": 'Periódusos rendszer', "kepesseg_ero": 250,
        "becenev": 'A RENDTEREMTŐ',
        "leiras": 'Sorba rakta az összes ismert elemet, és üresen hagyta a helyét azoknak, amelyeket még meg sem találtak.',
        "teny": 'Három elem helyét üresen hagyta a táblázatban, és megjósolta a tulajdonságaikat. Mindhármat megtalálták még az élete során, pontosan olyannak, amilyennek leírta.',
        "erdekesseg": 'Azt állította, hogy a rendszer álmában állt össze a fejében, és ébredés után egyetlen papírra leírta az egészet.',
        "idezet": 'A tudomány munka, nem szórakozás.',
        "prompt": 'a huge hand-drawn periodic table on a large sheet of paper covering the whole desk, a grid of ruled squares filled with element symbols, three squares left empty and glowing faintly golden, Dmitri Mendeleev leaning over it with one hand flat on the paper, long wild grey hair and a very long full grey beard, deep-set intense eyes looking straight at the viewer, dark 19th-century Russian academic coat, an oil lamp on the corner of the desk, no church, no castle',

    },
    {
        "id": "hu_kemia_7_lavoisier",
        "oldal": "hu", "targy": 'Kémia', "evfolyam": 7,
        "lecke": 'Tiszta anyagok: elemek és vegyületek',
        "nev": 'Antoine Lavoisier', "alnev": 'kémikus · 1743–1794',
        "kep": "kemia_7_lavoisier",
        "ritkasag": 'ritka', "ero": 300,
        "kepesseg": 'Anyagmegmaradás', "kepesseg_ero": 240,
        "becenev": 'A MÉRLEG EMBERE',
        "leiras": 'Ő mondta ki, hogy az anyag nem vész el: ami a reakció előtt megvolt, az utána is megvan, csak más alakban.',
        "teny": 'Mindent lemért, grammra pontosan. Ezzel bizonyította be, hogy az égés nem elvesz valamit az anyagból, hanem hozzáad – az oxigént.',
        "erdekesseg": 'A francia forradalom idején kivégezték. A kortársa azt mondta: egy pillanat kellett a fej levágásához, és száz év kell majd egy hasonlóhoz.',
        "idezet": 'Semmi sem vész el, semmi sem keletkezik, minden átalakul.',
        "prompt": 'a large brass balance scale in the centre of the image with a tiny weight being placed on the pan, Antoine Lavoisier behind it in a powdered wig and deep blue silk coat, glass retorts and bell jars around him, an open ledger of measurements on the table, candlelight in an elegant 18th-century French laboratory',
    },
    {
        "id": "hu_kemia_7_arrhenius",
        "oldal": "hu", "targy": 'Kémia', "evfolyam": 7,
        "lecke": 'Oldatok: oldódás, oldhatóság, töménység',
        "nev": 'Svante Arrhenius', "alnev": 'kémikus · 1859–1927',
        "kep": "kemia_7_arrhenius",
        "ritkasag": 'gyakori', "ero": 200,
        "kepesseg": 'Ionok az oldatban', "kepesseg_ero": 160,
        "becenev": 'AKIT KINEVETTEK',
        "leiras": 'Ő magyarázta meg, mi történik, amikor a só feloldódik a vízben: az anyag apró töltött részecskékre esik szét.',
        "teny": 'A doktori dolgozatára a legrosszabb elfogadható osztályzatot kapta, mert a bírálók képtelenségnek tartották. Ugyanezért a munkáért kapott később Nobel-díjat.',
        "erdekesseg": 'Elsőként számolta ki, hogy a levegőbe kerülő szén-dioxid felmelegítheti a Földet – 1896-ban.',
        "idezet": 'Aki új utat tör, annak elsőként a gúnyt kell kibírnia.',
        "prompt": 'a beaker of clear solution held up to the light with two metal electrodes dipped into it and faint blue sparks crossing between them, Svante Arrhenius holding it, neat short hair and moustache, dark late-19th-century suit, a voltaic pile and glass jars on the bench, cool blue-white glow',
    },
    {
        "id": "hu_fizika_7_newton",
        "oldal": "hu", "targy": 'Fizika', "evfolyam": 7,
        "lecke": 'Lendület és egyensúly',
        "nev": 'Isaac Newton', "alnev": 'fizikus és matematikus · 1643–1727',
        "kep": "fizika_7_newton",
        "ritkasag": 'nagyon_ritka', "ero": 430,
        "kepesseg": 'Gravitáció', "kepesseg_ero": 360,
        "becenev": 'AZ ÓRIÁS',
        "leiras": 'Három törvénybe sűrítette az egész mozgást, és megmutatta, hogy ugyanaz az erő ejti le az almát, ami a Holdat pályán tartja.',
        "teny": 'A pestisjárvány miatt bezárt az egyeteme, és hazaküldték a falujába. Az ott töltött két év alatt találta ki a gravitációt, a színek elméletét és a differenciálszámítást.',
        "erdekesseg": 'Élete második felében a királyi pénzverde vezetője lett, és személyesen járta a londoni kocsmákat pénzhamisítók után nyomozva.',
        "idezet": 'Ha távolabbra láttam, azért volt, mert óriások vállán álltam.',
        "prompt": 'a single red apple frozen in mid-fall in the centre of the image, Isaac Newton beneath it with one hand outstretched, long flowing auburn-grey curled hair to the shoulders, deep crimson 17th-century coat with a white cravat, an autumn orchard at dusk behind him and a huge pale moon on the same curved path, warm amber rim light',
    },
    {
        "id": "hu_fizika_7_galilei",
        "oldal": "hu", "targy": 'Fizika', "evfolyam": 7,
        "lecke": 'Mozgás közlekedés és sportolás közben',
        "nev": 'Galileo Galilei', "alnev": 'csillagász és fizikus · 1564–1642',
        "kep": "fizika_7_galilei",
        "ritkasag": 'ritka', "ero": 330,
        "kepesseg": 'Szabadesés', "kepesseg_ero": 270,
        "becenev": 'AKI ODANÉZETT',
        "leiras": 'Kimérte, hogyan gyorsul a leguruló golyó, és rájött, hogy a nehéz meg a könnyű test ugyanúgy esik.',
        "teny": 'Elsőként fordította az ég felé a távcsövet, és négy holdat talált a Jupiter körül. Ezek voltak az első égitestek, amelyekről kiderült, hogy nem a Föld körül keringenek.',
        "erdekesseg": 'Élete utolsó nyolc évét házi őrizetben töltötte, és vakon, diktálva fejezte be legfontosabb könyvét a mozgásról.',
        "idezet": 'És mégis mozog.',
        "prompt": "a long inclined wooden ramp across the foreground with a bronze ball rolling down it, Galileo Galilei crouching beside it holding a water clock, balding head and full grey beard, dark scholar's robe, a brass telescope leaning against the wall, night sky with Jupiter and four small moons through an arched window",
    },
    {
        "id": "hu_fizika_7_watt",
        "oldal": "hu", "targy": 'Fizika', "evfolyam": 7,
        "lecke": 'Az energia',
        "nev": 'James Watt', "alnev": 'mérnök · 1736–1819',
        "kep": "fizika_7_watt",
        "ritkasag": 'ritka', "ero": 320,
        "kepesseg": 'Gőzgép', "kepesseg_ero": 260,
        "becenev": 'AKI MEGMOZGATTA A VILÁGOT',
        "leiras": 'Úgy javította meg a gőzgépet, hogy az végre gazdaságos lett – ezzel indult el az ipari forradalom.',
        "teny": 'A teljesítmény mértékegységét, a wattot róla nevezték el. Minden villanykörtén és minden töltőn az ő neve áll.',
        "erdekesseg": 'A javítás ötlete séta közben jutott eszébe egy vasárnap délután, egy glasgow-i park füvén.',
        "idezet": 'Nem tudok másra gondolni, csak erre a gépre.',
        "prompt": 'a huge steam engine filling the background with white steam billowing and backlit, James Watt in front of it adjusting a brass valve, long grey hair tied back, plain brown coat with rolled sleeves, iron gears and a heavy flywheel, warm amber furnace glow in a Scottish workshop',
    },
    {
        "id": "hu_matemati_7_bolyai",
        "oldal": "hu", "targy": 'Matematika', "evfolyam": 7,
        "lecke": 'Halmazok, számhalmazok',
        "nev": 'Bolyai János', "alnev": 'matematikus · 1802–1860',
        "kep": "matemati_7_bolyai",
        "ritkasag": 'nagyon_ritka', "ero": 440,
        "kepesseg": 'Új geometria', "kepesseg_ero": 370,
        "becenev": 'A VILÁGTEREMTŐ',
        "leiras": 'Kitalált egy geometriát, ahol a párhuzamosok mégis találkozhatnak. Kétezer év után ő mondta ki, hogy a tér másmilyen is lehet.',
        "teny": 'Az egész új geometriát huszonnégy oldalon írta le. Ez a rövid függelék az apja könyve mögött jelent meg, és megváltoztatta a matematikát.',
        "erdekesseg": 'Kiváló hegedűs és vívó volt. A hagyomány szerint egyszer tizenhárom tisztet hívott ki egymás után, és a szünetekben hegedült.',
        "idezet": 'Semmiből egy új, más világot teremtettem.',
        "prompt": 'a dark wall covered in glowing chalk-drawn hyperbolic curves and parallel lines bending towards each other, Janos Bolyai standing before it holding a brass drawing compass, a young 19th-century Hungarian hussar officer, short dark hair, clean-shaven determined face, dark blue hussar jacket with gold braid frogging across the chest, cool indigo light',
    },
    {
        "id": "hu_matemati_7_euklidesz",
        "oldal": "hu", "targy": 'Matematika', "evfolyam": 7,
        "lecke": 'Matematikai logika, kombinatorika, gráfok',
        "nev": 'Euklidész', "alnev": 'matematikus · kb. i. e. 300',
        "kep": "matemati_7_euklidesz",
        "ritkasag": 'ritka', "ero": 330,
        "kepesseg": 'Bizonyítás', "kepesseg_ero": 270,
        "becenev": 'AKI SORBA RAKTA',
        "leiras": 'Öt egyszerű alapszabályból vezette le az egész geometriát. Ezt a módszert – állítás, bizonyítás, következmény – azóta is így tanítjuk.',
        "teny": 'A könyve, az Elemek, több mint kétezer évig volt tankönyv. A Biblia után ez a legtöbbször kiadott könyv a világon.',
        "erdekesseg": 'Amikor a király rövidebb utat kért a tanuláshoz, azt felelte neki: a geometriához nem vezet királyi út.',
        "idezet": 'A geometriához nem vezet királyi út.',
        "prompt": 'a wide tray of fine sand in the foreground with precise geometric figures drawn into it by a compass, Euclid of Alexandria kneeling over it, short white beard and simple cream linen robe, papyrus scrolls stacked beside him, faint glowing geometric constructions rising in the air, warm Mediterranean sunlight through a stone colonnade',
    },
    {
        "id": "hu_matemati_7_pitagorasz",
        "oldal": "hu", "targy": 'Matematika', "evfolyam": 7,
        "lecke": 'Számelméleti ismeretek, hatvány, négyzetgyök',
        "nev": 'Pitagorasz', "alnev": 'matematikus · kb. i. e. 570–495',
        "kep": "matemati_7_pitagorasz",
        "ritkasag": 'ritka', "ero": 340,
        "kepesseg": 'Pitagorasz-tétel', "kepesseg_ero": 280,
        "becenev": 'A SZÁMOK PAPJA',
        "leiras": 'Ő mondta ki, hogy a derékszögű háromszögben a két rövidebb oldal négyzetének összege pont a leghosszabbé.',
        "teny": 'A tanítványai titkos közösséget alkottak, és azt hitték, minden a számokból áll. Amikor kiderült, hogy a négyzet átlója nem írható fel törtként, a felfedezést titokban akarták tartani.',
        "erdekesseg": 'Az iskolájában a nők ugyanúgy taníthattak, mint a férfiak – ami akkoriban szinte példátlan volt.',
        "idezet": 'Minden szám.',
        "prompt": 'a large glowing right-angled triangle drawn in the air with a square of light growing out of each of its three sides, Pythagoras standing beside it with one hand raised, long dark beard and white draped robe, a stone terrace with columns and the sea behind, golden sunrise light',
    },
    {
        "id": "hu_biologia_7_darwin",
        "oldal": "hu", "targy": 'Biológia', "evfolyam": 7,
        "lecke": 'Az élővilág fejlődése',
        "nev": 'Charles Darwin', "alnev": 'természettudós · 1809–1882',
        "kep": "biologia_7_darwin",
        "ritkasag": 'nagyon_ritka', "ero": 420,
        "kepesseg": 'Természetes kiválasztódás', "kepesseg_ero": 350,
        "becenev": 'A HAJÓS',
        "leiras": 'Öt évig hajózott a világ körül, és megértette: az él tovább, aki jobban alkalmazkodik. Ebből lett az egész mai biológia alapja.',
        "teny": 'A Galápagos-szigeteken apró pintyeket gyűjtött. A csőrük szigetenként más volt – ebből jött rá, hogy a fajok változnak.',
        "erdekesseg": 'Húsz évig ült a kész elméletén, mielőtt kiadta volna. Csak akkor szánta rá magát, amikor egy másik kutató ugyanarra jutott.',
        "idezet": 'Nem a legerősebb marad fenn, hanem aki a legjobban alkalmazkodik.',
        "prompt": 'a small brown finch perched on an outstretched hand in the foreground, Charles Darwin behind it, bald high forehead and very long white beard, dark victorian coat, giant tortoises and black volcanic rock on a Galapagos shore, the sailing ship Beagle anchored on the horizon, warm green and gold light',
    },
    {
        "id": "hu_biologia_7_linne",
        "oldal": "hu", "targy": 'Biológia', "evfolyam": 7,
        "lecke": 'Az élővilág országai',
        "nev": 'Carl Linné', "alnev": 'botanikus · 1707–1778',
        "kep": "biologia_7_linne",
        "ritkasag": 'gyakori', "ero": 210,
        "kepesseg": 'Rendszertan', "kepesseg_ero": 170,
        "becenev": 'A NÉVADÓ',
        "leiras": 'Ő találta ki, hogy minden élőlénynek két nevet adjunk – nemzetség és faj –, és így ma is nevezzük őket.',
        "teny": 'Több mint hétezer növényt és négyezer állatot nevezett el. A saját magának adott név: Homo sapiens, vagyis a bölcs ember.',
        "erdekesseg": 'A tanítványait a világ minden tájára kiküldte gyűjteni. Tizenhét indult el, és csak tíz tért vissza élve.',
        "idezet": 'Isten teremtett, Linné rendszerezett.',
        "prompt": 'an open wooden specimen cabinet of small labelled drawers with pressed plants pinned inside, Carl Linnaeus in front of it holding a specimen sheet and a quill, shoulder-length light hair and a simple dark green coat, exotic flowers and butterflies around him, soft green sunlight through leaves in an 18th-century botanical garden',
    },
    {
        "id": "hu_biologia_7_szentgyorgyi",
        "oldal": "hu", "targy": 'Biológia', "evfolyam": 7,
        "lecke": 'A természeti értékek védelme',
        "nev": 'Szent-Györgyi Albert', "alnev": 'biokémikus · 1893–1986',
        "kep": "biologia_7_szentgyorgyi",
        "ritkasag": 'ritka', "ero": 350,
        "kepesseg": 'C-vitamin', "kepesseg_ero": 290,
        "becenev": 'A PAPRIKÁS',
        "leiras": 'Ő fedezte fel a C-vitamint, és ezért kapott Nobel-díjat – az egyetlen magyar, aki itthon végzett munkáért kapta.',
        "teny": 'A döntő kísérlethez kilónyi C-vitamint vont ki – szegedi paprikából. A világ akkori teljes készletét ő állította elő.',
        "erdekesseg": 'A második világháború alatt titkos béketárgyalást vállalt Isztambulban, és Hitler személyesen adott parancsot az elfogatására.',
        "idezet": 'A felfedezés abból áll, hogy meglátjuk, amit mindenki lát, és közben arra gondolunk, amire még senki.',
        "prompt": 'a pile of bright red paprika peppers on a laboratory bench beside a test tube of pale white crystals held up to the light, Albert Szent-Gyorgyi holding the tube, short dark hair and round glasses, white lab coat over a 1930s suit, microscope and glass flasks around, warm amber light',
    },
    {
        "id": "hu_foldrajz_7_kolumbusz",
        "oldal": "hu", "targy": 'Földrajz', "evfolyam": 7,
        "lecke": 'Tájékozódás a térképen – fokhálózat és méretarány',
        "nev": 'Kolumbusz Kristóf', "alnev": 'hajós · 1451–1506',
        "kep": "foldrajz_7_kolumbusz",
        "ritkasag": 'ritka', "ero": 320,
        "kepesseg": 'Nyugati út', "kepesseg_ero": 260,
        "becenev": 'AKI ELTÉVEDT',
        "leiras": 'Indiába akart eljutni nyugat felé, és közben egy addig ismeretlen földrészbe ütközött.',
        "teny": 'Rosszul számolta ki a Föld méretét – sokkal kisebbnek hitte. Ha jól számol, el sem indul, mert reménytelennek látta volna az utat.',
        "erdekesseg": 'Élete végéig meg volt győződve róla, hogy Ázsiában járt. Sosem tudta meg, hogy egy új kontinenst talált.',
        "idezet": 'Következtem a tengert, és a tenger vezetett.',
        "prompt": "an unrolled sea chart flapping in the wind across the foreground with a brass astrolabe resting on it, Christopher Columbus at the ship's rail behind it, weathered face and shoulder-length greying hair, red velvet cap and coat, billowing sails, open ocean and an unknown coastline just appearing on the horizon at dawn",
    },
    {
        "id": "hu_foldrajz_7_koroscsoma",
        "oldal": "hu", "targy": 'Földrajz', "evfolyam": 7,
        "lecke": 'A Kárpát-medence tájai és népei',
        "nev": 'Kőrösi Csoma Sándor', "alnev": 'nyelvtudós · 1784–1842',
        "kep": "foldrajz_7_koroscsoma",
        "ritkasag": 'ritka', "ero": 340,
        "kepesseg": 'A szótár', "kepesseg_ero": 280,
        "becenev": 'A GYALOGOS',
        "leiras": 'Gyalog indult el Ázsiába, hogy megkeresse a magyarok őshazáját. Nem találta meg – de közben megírta a világ első tibeti szótárát.',
        "teny": 'Éveket töltött jéghideg kolostorcellákban, napi néhány csésze vajas tea mellett, kéziratok fölé hajolva.',
        "erdekesseg": 'Japánban buddhista szentként tisztelik. A világ első nyugati tibetológusa lett egy magyar székely fiúból.',
        "idezet": 'Elindultam, hogy megkeressem a nemzetem bölcsőjét.',
        "prompt": 'a huge handwritten Tibetan-Hungarian dictionary open on a low table lit by a single butter lamp, Sandor Korosi Csoma bent over it writing, gaunt bearded face, worn dark travelling coat and blanket, Tibetan manuscripts stacked around, freezing blue light from a small stone window of a Himalayan monastery cell',
    },
    {
        "id": "hu_tortenel_7_szechenyi",
        "oldal": "hu", "targy": 'Történelem', "evfolyam": 7,
        "lecke": 'A dualizmus kora: felzárkózás Európához',
        "nev": 'Széchenyi István', "alnev": 'reformer · 1791–1860',
        "kep": "tortenel_7_szechenyi",
        "ritkasag": 'nagyon_ritka', "ero": 410,
        "kepesseg": 'A legnagyobb magyar', "kepesseg_ero": 340,
        "becenev": 'A HÍDÉPÍTŐ',
        "leiras": 'Egyévi jövedelmét ajánlotta fel a Tudományos Akadémiára, és nekiállt hidat, gőzhajót és vasutat építeni az országnak.',
        "teny": 'A Lánchíd megépítése előtt Pest és Buda között télen sokszor hetekig nem lehetett átkelni a jégzajlás miatt.',
        "erdekesseg": 'Ő szabályoztatta a Tiszát és a Dunát, és ő hozatta az első lóversenyt is – mert a lótenyésztést is fel akarta emelni.',
        "idezet": 'Magyarország nem volt, hanem lesz.',
        "prompt": 'the half-built Chain Bridge of Budapest filling the background with scaffolding and stone lions, Istvan Szechenyi standing on the riverbank in front of it, dark hair and full sideburns, elegant dark tailcoat with a high white collar and cravat, a steamboat on the Danube, warm golden hour light',
    },
    {
        "id": "hu_tortenel_7_semmelweis",
        "oldal": "hu", "targy": 'Történelem', "evfolyam": 7,
        "lecke": 'A modern kor születése',
        "nev": 'Semmelweis Ignác', "alnev": 'orvos · 1818–1865',
        "kep": "tortenel_7_semmelweis",
        "ritkasag": 'nagyon_ritka', "ero": 400,
        "kepesseg": 'Kézmosás', "kepesseg_ero": 330,
        "becenev": 'AZ ANYÁK MEGMENTŐJE',
        "leiras": 'Rájött, hogy az orvosok viszik át a fertőzést a betegekre, és bevezette a kézmosást. Ezzel évente több ezer anya életét mentette meg.',
        "teny": 'A klinikáján a halálozás tíz százalékról egy alá esett, miután klóros vízzel kezdték mosni a kezüket.',
        "erdekesseg": 'A kortársai kinevették és elüldözték. Csak halála után igazolta a tudomány, hogy végig igaza volt.',
        "idezet": 'Ha valaki megérti, mit tettem, annak nem az én nevemre kell emlékeznie, hanem a kézmosásra.',
        "prompt": 'a white basin of chlorinated water in the foreground with hands being washed in it, Ignaz Semmelweis above it with his sleeves rolled up, dark receding hair and side whiskers, dark frock coat, a long row of white hospital beds softly lit behind him, cool clean light with one warm lamp in the distance',
    },
    {
        "id": "hu_tortenel_7_marconi",
        "oldal": "hu", "targy": 'Történelem', "evfolyam": 7,
        "lecke": 'Az első világháború és következményei',
        "nev": 'Guglielmo Marconi', "alnev": 'feltaláló · 1874–1937',
        "kep": "tortenel_7_marconi",
        "ritkasag": 'ritka', "ero": 330,
        "kepesseg": 'Rádióhullám', "kepesseg_ero": 270,
        "becenev": 'A HANGTALAN ÜZENET',
        "leiras": 'Elsőként küldött üzenetet vezeték nélkül az óceánon át. Innentől a hír gyorsabban ért célba, mint a hajó.',
        "teny": 'A Titanic utasainak egy részét az ő rádiója mentette meg: a segélykérést egy másik hajó fogta, és odaért.',
        "erdekesseg": 'A saját padlásán kezdte kísérletezni, tizenévesen. Az olasz posta elutasította az ötletét, ezért Angliába ment.',
        "idezet": 'A rádióhullámok mindenütt ott vannak, csak hallani kell őket.',
        "prompt": 'a brass telegraph key on a table with bright electric sparks jumping across a coil beside it, Guglielmo Marconi with his hand on the key, neat dark hair and moustache, formal early-1900s suit, a tall antenna mast through the window against a stormy sea, blue-white electric glow',
    },
    {
        "id": "hu_magyar_n_7_petofi",
        "oldal": "hu", "targy": 'Magyar nyelv és irodalom', "evfolyam": 7,
        "lecke": 'I. Korok és portrék',
        "nev": 'Petőfi Sándor', "alnev": 'költő · 1823–1849',
        "kep": "magyar_n_7_petofi",
        "ritkasag": 'nagyon_ritka', "ero": 420,
        "kepesseg": 'Nemzeti dal', "kepesseg_ero": 350,
        "becenev": 'A LÁNGOLÓ',
        "leiras": 'Huszonöt évesen írt verse egy egész forradalmat indított el. Egyszerű, tiszta magyar nyelven írt, ezért érti ma is mindenki.',
        "teny": '1848. március 15-én a Nemzeti dalt a Pilvax kávéház előtt szavalta el, és aznap estére az egész város énekelte.',
        "erdekesseg": 'Vándorszínész, katona és házitanító is volt, mielőtt költőként befutott. Huszonhat évesen tűnt el a segesvári csatában.',
        "idezet": 'Talpra magyar, hí a haza!',
        "prompt": 'a printed sheet of poetry held up in a raised fist above a crowd, Sandor Petofi below it on the stone steps of a cafe mid-speech, young 19th-century Hungarian poet with dark wavy hair and a small beard, open-collared white shirt and dark coat, cockades and flags in the crowd, dramatic overcast March light',
    },
    {
        "id": "hu_magyar_n_7_arany",
        "oldal": "hu", "targy": 'Magyar nyelv és irodalom', "evfolyam": 7,
        "lecke": 'II. Magyar vagy világirodalmi ifjúsági regény',
        "nev": 'Arany János', "alnev": 'költő · 1817–1882',
        "kep": "magyar_n_7_arany",
        "ritkasag": 'ritka', "ero": 340,
        "kepesseg": 'A ballada', "kepesseg_ero": 280,
        "becenev": 'A HALLGATÓ',
        "leiras": 'Olyan verseket írt, amelyek úgy húznak, mint egy krimi: kevés szóval, sejtetve mesél el egy egész tragédiát.',
        "teny": 'A balladáiban sosem mondja ki, mi történt – az olvasónak kell rájönnie. Ezért hívják a magyar ballada mesterének.',
        "erdekesseg": 'Barátja, Petőfi halála után évekig szinte semmit nem írt. A gyász hallgatásba fordult nála.',
        "idezet": 'Ki nem tud írni, olvasni sem tud igazán.',
        "prompt": "a half-written page under a paused quill on a candlelit desk, Janos Arany sitting behind it deep in thought, receding hairline and neat beard, dark scholar's coat, the shadowy figures of his ballad's characters faintly suggested in the darkness behind him, muted warm light in a quiet room",
    },
    {
        "id": "hu_enek_zen_7_bach",
        "oldal": "hu", "targy": 'Ének-zene', "evfolyam": 7,
        "lecke": 'A barokk zene',
        "nev": 'Johann Sebastian Bach', "alnev": 'zeneszerző · 1685–1750',
        "kep": "enek_zen_7_bach",
        "ritkasag": 'nagyon_ritka', "ero": 410,
        "kepesseg": 'Fúga', "kepesseg_ero": 340,
        "becenev": 'A KÁNTOR',
        "leiras": 'A barokk zene csúcsa. Úgy építette a szólamokat egymásra, mint egy matematikus – mégis gyönyörű.',
        "teny": 'Húsz gyermeke született, és közben minden vasárnapra új művet írt a templomnak. Több mint ezer műve maradt fenn.',
        "erdekesseg": 'Fiatalon négyszáz kilométert gyalogolt, hogy meghallgathasson egy híres orgonistát.',
        "idezet": 'A cél nem más, mint Isten dicsősége és a lélek felüdülése.',
        "prompt": "towering gilded organ pipes rising into shadow above a baroque church organ console, Johann Sebastian Bach seated at the keys with his head turned slightly towards the viewer, curled grey wig and dark cantor's coat, candlelight on the open manuscript, a choir of boys faintly visible below, warm gold and deep brown",
    },
    {
        "id": "hu_enek_zen_7_beethoven",
        "oldal": "hu", "targy": 'Ének-zene', "evfolyam": 7,
        "lecke": 'Beethoven és a szimfónia',
        "nev": 'Ludwig van Beethoven', "alnev": 'zeneszerző · 1770–1827',
        "kep": "enek_zen_7_beethoven",
        "ritkasag": 'nagyon_ritka', "ero": 430,
        "kepesseg": 'Kilencedik', "kepesseg_ero": 360,
        "becenev": 'A SÜKET ZENÉSZ',
        "leiras": 'Kiszélesítette a szimfóniát, és beleírta az emberi szabadság gondolatát. A IX. szimfónia zárótétele ma az Európai Unió himnusza.',
        "teny": 'A legnagyobb műveit már süketen írta. A hangokat csak a fejében hallotta.',
        "erdekesseg": 'A IX. szimfónia bemutatóján háttal állt a közönségnek. Egy énekesnő fordította meg, hogy lássa a tapsot, amit nem hallott.',
        "idezet": 'A zene magasabb kinyilatkoztatás, mint minden bölcsesség.',
        "prompt": 'an open piano with scattered manuscript pages spilling onto the floor around it, Ludwig van Beethoven leaning over it with one hand pressed flat on the wooden case to feel the vibration, wild grey hair and an intense scowling face, dark coat, stormy grey light from a tall window in a cluttered Vienna room',
    },
    {
        "id": "hu_enek_zen_7_bartok",
        "oldal": "hu", "targy": 'Ének-zene', "evfolyam": 7,
        "lecke": 'Műdalok és kórusművek',
        "nev": 'Bartók Béla', "alnev": 'zeneszerző · 1881–1945',
        "kep": "enek_zen_7_bartok",
        "ritkasag": 'ritka', "ero": 350,
        "kepesseg": 'Népdalgyűjtés', "kepesseg_ero": 290,
        "becenev": 'A FONOGRÁFOS',
        "leiras": 'Fonográffal járta a falvakat, és több ezer népdalt mentett meg. Ezekből épített olyan zenét, amit az egész világ játszik.',
        "teny": 'Több mint tízezer dallamot gyűjtött össze Magyarországon, Romániában, Szlovákiában, sőt Észak-Afrikában is.',
        "erdekesseg": 'Az öreg parasztasszonyok eleinte féltek a fonográf tölcsérétől, és nem akartak beleénekelni.',
        "idezet": 'A falusi zene a legtisztább forrás.',
        "prompt": 'a large brass phonograph horn on a wooden stand in the foreground, an old woman in a headscarf singing into it, Bela Bartok crouching beside it writing down the melody, dark hair and sharp features, plain travelling suit, whitewashed cottage wall and dirt yard of a Hungarian village, warm late afternoon light',
    },
    {
        "id": "hu_digitali_7_neumann",
        "oldal": "hu", "targy": 'Digitális kultúra', "evfolyam": 7,
        "lecke": 'Algoritmus tervezése és leírása',
        "nev": 'Neumann János', "alnev": 'matematikus · 1903–1957',
        "kep": "digitali_7_neumann",
        "ritkasag": 'nagyon_ritka', "ero": 440,
        "kepesseg": 'Tárolt program', "kepesseg_ero": 370,
        "becenev": 'A GÉP ATYJA',
        "leiras": 'Ő találta ki, hogy a gép ne csak az adatokat, hanem magát a programot is a memóriájában tárolja. Minden mai számítógép így működik.',
        "teny": 'A ma használt számítógépek felépítését máig róla nevezik: Neumann-architektúra.',
        "erdekesseg": 'Hatéves korában fejben osztott össze nyolcjegyű számokat, és szó szerint memorizált egész könyveket.',
        "idezet": 'Ha valaki nem hiszi, hogy a matematika egyszerű, az csak azért van, mert nem érti, milyen bonyolult az élet.',
        "prompt": 'a room-sized computer of glowing vacuum tubes and cables filling the background, John von Neumann in front of it holding a punched card, neat dark hair and a round friendly face, immaculate grey three-piece suit, soft cyan glow and warm ceiling lamps in a 1940s computer hall',
    },
    {
        "id": "hu_digitali_7_lovelace",
        "oldal": "hu", "targy": 'Digitális kultúra', "evfolyam": 7,
        "lecke": 'Vezérlési szerkezetek: szekvencia, elágazás, ciklus',
        "nev": 'Ada Lovelace', "alnev": 'matematikus · 1815–1852',
        "kep": "digitali_7_lovelace",
        "ritkasag": 'nagyon_ritka', "ero": 400,
        "kepesseg": 'Az első program', "kepesseg_ero": 330,
        "becenev": 'AKI ELŐRE LÁTOTT',
        "leiras": 'Száz évvel a számítógépek előtt leírta, hogyan lehet egy gépnek lépésről lépésre utasítást adni. Ő volt a világ első programozója.',
        "teny": 'Ő ismerte fel elsőként, hogy a gép nemcsak számolni tud majd, hanem zenét is szerkeszthet, ha a hangokat számokká alakítjuk.',
        "erdekesseg": 'Az édesapja Byron, a híres költő volt. Az édesanyja kifejezetten matematikára taníttatta, nehogy költő legyen belőle.',
        "idezet": 'A gép csak azt teheti, amit megparancsolunk neki.',
        "prompt": 'a brass mechanical calculating engine of gears and wheels on a desk covered in handwritten tables of numbers, Ada Lovelace seated beside it with one hand on the page, dark hair in a braided updo, elegant blue-grey Victorian gown, candlelight and cool daylight mixing in a drawing room',
    },
    {
        "id": "hu_digitali_7_turing",
        "oldal": "hu", "targy": 'Digitális kultúra', "evfolyam": 7,
        "lecke": 'Robot érzékelőkkel',
        "nev": 'Alan Turing', "alnev": 'matematikus · 1912–1954',
        "kep": "digitali_7_turing",
        "ritkasag": 'ritka', "ero": 360,
        "kepesseg": 'Kódfejtés', "kepesseg_ero": 300,
        "becenev": 'A KÓDTÖRŐ',
        "leiras": 'Ő fogalmazta meg, mit jelent egyáltalán, hogy egy gép mit jelent „számolni”, és ő tette fel a kérdést: gondolkodhat-e egy gép?',
        "teny": 'A második világháborúban feltörte a német Enigma kódot. A történészek szerint ezzel évekkel rövidítette meg a háborút.',
        "erdekesseg": 'Hosszútávfutó volt, olyan jó, hogy majdnem bekerült az olimpiai válogatottba. Néha kilométereket futott a megbeszélésekre.',
        "idezet": 'Néha azok érnek el elképzelhetetlent, akiktől senki nem várja.',
        "prompt": 'a huge rotating code-breaking machine of wheels and wiring filling the background, Alan Turing in front of it holding a strip of paper tape, tousled dark hair and a tweed jacket, cipher sheets scattered on the desk, a dim green desk lamp and the glow of rotating dials in a wartime hut',
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


def teljes_prompt(k: dict) -> str:
    """A kártyaképhez tartozó teljes Leonardo-prompt."""
    return f"{STILUS_PROMPT}, {k.get('prompt', '')}"


def kep_utvonal(k: dict) -> str:
    """A kártyakép relatív útvonala a static mappán belül."""
    return f"kartyak/{k['oldal']}/{k['kep']}.png"
