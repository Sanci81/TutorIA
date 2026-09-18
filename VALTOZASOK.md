# TutorIA – mi változott, és mihez NE nyúljunk

Ez a lista azért van, hogy ne rontsunk el újra olyat, ami már jó volt.
Minden módosítás előtt EZT kell elolvasni, és ami itt „LEZÁRT", ahhoz csak
akkor szabad hozzányúlni, ha Sándor külön kéri.

Frissítve: 2026-09-18

---

## LEZÁRT – NE NYÚLJ HOZZÁ

Ezek működnek, Sándor jóváhagyta, és többször is elrontottuk már őket.

### A nagyított nézet (`.teljes-mod`)
- **Az új felület MINDEN szabálya `:not(.teljes-mod)`.** Egyszer a
  szójegyzék oszlopszabályát nem zártam ki innen, és nagyításban a
  szójegyzék széthúzódott az egész képernyőre, a tanulás felülete meg
  260 képpontra szorult. Nagyításban csak két dolgot csinálunk: a
  háttér és a kabala figura helye. Az oszlopokhoz TILOS hozzányúlni.

### A kabala figura
- **Kivéve a rácsból**, `position:absolute`, a felület bal alsó sarkában;
  nagyításban a jobb oldali üres sávban, középen.
- **Magassága korlátos: 300 képpont.** Enélkül a kisfiú képe 325 magas
  lett, és rálógott a témalistára, illetve a szójegyzékre.
- **Kép (fiú, lány): 150 széles. Robot: a DOBOZA 280.** Egy közös
  max-width mindkettőre a robotot felezte meg.
- A témalista 320 képponttal rövidebb, hogy a figurának saját helye
  legyen. 560 képpontnál alacsonyabb felületen a figura eltűnik.

### A mikrofon gomb mérete
- 80 × 80 képpont. **TILOS** kisebbre venni.

### A lecke-sín és a témakör címe a fejlécben
- Mindig látszik. Mindkettőt eltüntettem már egyszer, Sándor visszakérte.

### A fejléc magassága és a Szintfelmérő gomb
- Nem nőhet. A gombot egyszer „zárolva" feliratra cseréltem, ettől
  megnőtt a fejléc. Visszaállítva.

### A `static/kartyak` mappa
- **SOHA ne írj bele.** A híd tud írni, de átnevezni és törölni nem,
  ezért az „átnevezés" némán duplikátumot csinál. Ha kép kell oda, meg
  kell mondani Sándornak, mit nevezzen át.

### A híd (device_commit_files)
- A visszajelzése HAZUDIK: „written" akkor is, ha a fájl nem ért oda.
  **Minden írás után vissza kell olvasni és ellenőrző-összeget nézni**,
  és ha nem egyezik, újra kell írni. Ez ma háromszor fordult elő.

---

## MEGVÁLTOZTATVA – 2026-09-15 … 09-18

### `app.py`
- **A lecke hossza a témakör NEHÉZSÉGÉBŐL** (`_lecke_hossz_perc`), 30–90
  perc között. A régi `óraszám × 60` az egész ÉVRE szólt, ezért jött ki
  4200 perc. Az óraszám mostantól ARÁNY a tantárgy többi témaköréhez
  képest, nem szorzó. Az alap az évfolyamból jön: 1–4. 30, 5–6. 40,
  7–8. 45 perc. Mind a 603 témakörre lefuttatva: leghosszabb 80, átlag 37.
  **Négy helyen kellett átírni** (kapu-szöveg, chat oldal, teszt indítás,
  fázis-számítás) – ha az egyik kimarad, a kapu mást gondol, mint amit
  a gyerek lát.
- **Az új felület alapból be van kapcsolva** (`session.get("uj_felulet", True)`).
  A `/regi-felulet` és `/uj-felulet` címek továbbra is váltanak.
- **Teszt kapuja**: a tanár megkapja a kapu állapotát, és csak azt
  mondhatja, ami igaz. Küszöb 60 → 30 perc (`TESZT_MIN_PERC`).
- **Hátralévő idő** a sablonnak: `lecke_hossz_perc`, `lecke_tanult_perc`,
  `lecke_hatra_perc`.
- Kapcsolattartási cím `info@tutoriacademia.com`; jogi dátum nyelvenként.
- Idegen szó felismerése: a magyar szakszavak (metszet, unió, halmaz…)
  magyar szavak maradnak.
- Gyerek törlése; Hogy megy? oldal (nap/hét/hónap).

### `Procfile`
- **`--workers 1 --threads 8 --timeout 180`.** Eddig EGY soros
  munkafolyamat futott: az egész oldal egyszerre EGY kérést szolgált ki,
  és ettől jött a Cloudflare 502. Nyolc szál ≈ nyolc gyerek egyszerre,
  kb. 50–100 gyerekig elég. Ezer gyerekhez több példány kell.

### `templates/chat.html` – az új munkafelület
- Tábla balra, keskeny beszélgetés jobbra, a kérdés nem ismétlődik.
- **A lap nem görög, csak a tábla belseje.** A magasságot egy kis
  szkript méri ki (`--munka-magas`), mert a fejléc és a lábléc magassága
  oldalanként más. Alsó határ 800 képpont – ha nem fér ki, az oldal
  görög, és ez így jó.
- **A feladat (`.munkater`) NEM görög külön.** Volt rajta egy régi
  `overflow:auto`, ettől lett alul egy külön kis doboz levágva.
- **Nyelvórán a szójegyzék a FEJLÉC sávjában van**, jobb oldalt, a
  magassága a fejléc magassága (`--fejlec-magas`). Alatta a tanulás
  felülete teljes szélességben kimegy a szélig: 747 → 961 képpont.
  Nagyításban marad oszlopnak.
- **A lecke-sín doboza is megáll a szójegyzék előtt.** A sín a fejlécen
  KÍVÜL van, ezért kellett neki külön szabály – enélkül benyúlt alá.
- Az érme-csík 30 képponttal a sín alatt, hogy ne menjen át a
  „Tanulás / Gyakorlás / Teszt" feliratokon.
- Hangos mód: a mikrofon tömör alsó sávban, összecsukva a tábla sarkába
  úszik, ugyanakkorán.

### `hang.py`
- A felolvasás végigmegy: `MAX_KARAKTER` 420 → 3000.
- Minden szorzásjel (`×`, `·`, `*`, `x`, `X`) „háromszor négy"-ként szól.
- Szerkesztőjelek kiszedése (lábjegyzet, félkövér, címsor).

### `database.py`
- Megőrzési idő 12 hónap; tanulási idő kulcs-javítás.

### `static/css/style.css`
- Telefonos indítósáv 820 alatt; asztali indítósáv mindig ott van.
- 1200 képponttól a tanulás felülete 1860-ig nyúlik.

### `kinezet.py`
- Olcsóbb kinézetek (50 / 80 / 150) és nyolc új, összesen 19.

### `level.py`, `translations.py`, `ellenor.py`, `.gitignore`
- Levél szövegjavítás és logó; új fordítási kulcsok; néma ellenőr
  (tanterv, fordítás, sablon, kiejtés, kártya); próbaképek kizárva.

---

## NYITOTT – ez van még hátra

1. **Telefon és tablet.** Az új felület minden szabálya 901 képpont
   FÖLÖTT él, ezért telefonon a régi elrendezés jön. A témalista fiókja
   ott nem is csukható be. Ez a következő munka, és ez a legfontosabb:
   a gyerekek fele telefonon vagy tableten fog tanulni.
2. **Kártyaképek.** 52-ből 42 hiányzik. A kép abból a tettből készüljön,
   amiről az illető híres – ami a kártyán is olvasható –, egy közös
   stílussal. A műhely kész: `kartya_kepek_generalas.py`.
3. **Gondolkodás-jelző.** Sándor szerint korábban szöveg volt, most
   pöttyök. NEM tudjuk, mi változtatta meg. Konzol-kép kell hozzá.
4. **Számbillentyűzet** telefonra és tabletre.
5. **Visszajelzés gomb** a teszt idejére.
6. **Bemutató oldal** a szülőknek (videó NEM, amíg a felület mozog).
7. **Skálázás 100 gyerek fölé** – több példány a Railway-en, adatbázis-
   kapcsolatkezelés, az AI-szolgáltatónál percenkénti korlát.
