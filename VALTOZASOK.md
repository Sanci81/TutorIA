# TutorIA – mi változott, és mihez NE nyúljunk

Ez a lista azért van, hogy ne rontsunk el újra olyat, ami már jó volt.
Minden módosítás előtt EZT kell elolvasni, és ami itt „LEZÁRT", ahhoz csak
akkor szabad hozzányúlni, ha Sándor külön kéri.

Frissítve: 2026-09-17

---

## LEZÁRT – NE NYÚLJ HOZZÁ

Ezek működnek, Sándor jóváhagyta, és többször is elrontottuk már őket.

### A kabala figura oszlopa
- A `.chat-layout` rács oszlopaihoz (`grid-template-columns`) **TILOS**
  hozzányúlni. Egyszer felülírtam két oszlopra, és a figura egy új sorba
  csúszott, a képernyőn kívülre.
- Az eredeti stíluslap minden esetet helyesen kezel: szójegyzékkel,
  anélkül, nagyításban és normál nézetben is.
- A figura 1121 képpont alatt szándékosan eltűnik; nyelvórán 1421 alatt.
  Ez RÉGI, szándékos szabály, nem hiba.

### A mikrofon gomb mérete
- 80 × 80 képpont. **TILOS** kisebbre venni: kisebb méretben a gyerek nem
  találja meg. A körülötte lévő üres helyet el lehet venni, a gombot nem.

### A lecke-sín (Tanulás / Gyakorlás / Teszt / Kész)
- Mindig látszik, akkor is, ha a gyereknek még nem volt szintfelmérője.
  Ezt egyszer eltüntettem, Sándor visszakérte.

### A témakör címe a fejlécben
- Mindig látszik. Ugyanaz a hiba volt, mint a sínnél.

### A fejléc magassága és a Szintfelmérő gomb
- Egyszer a gombot egy „zárolva" feliratra cseréltem, és ettől a fejléc
  megnőtt. Sándor: „miért rontod el, ami eddig jó volt". Visszaállítva.

### A `static/kartyak` mappa
- **SOHA ne írj bele.** A híd tud írni, de átnevezni és törölni nem, ezért
  az „átnevezés" némán duplikátumot csinál. Ha kép kell oda, meg kell
  mondani Sándornak, mit nevezzen át.

---

## MEGVÁLTOZTATVA – 2026-09-15 … 09-17

Fájl szerint, hogy vissza lehessen keresni.

### `app.py`
- **Teszt kapuja.** A tanár megkapja a kapu állapotát (`_teszt_kapu_szoveg`),
  és csak azt mondhatja, ami igaz. Korábban egy nem létező gombra küldte a
  gyereket.
- **Küszöb 60 → 30 perc** (`TESZT_MIN_PERC`). A leckezáró tesztet továbbra
  is a lecke saját ideje nyitja.
- **Új munkafelület kapcsolója.** `?felulet=uj`, illetve a `/uj-felulet` és
  `/regi-felulet` címek. Kikapcsolva minden a régi.
- **Hátralévő idő** a sablonnak: `lecke_hossz_perc`, `lecke_tanult_perc`,
  `lecke_hatra_perc`.
- **Kapcsolattartási cím** `info@tutoriacademia.com` (a `KAPCSOLAT_EMAIL`
  környezeti változó felülírja).
- **Jogi dátum** nyelvenként: `JOGI_FRISSITVE_ISO` + `_jogi_datum()`.
  Magyarul „2026. szeptember 17.", spanyolul „17 de septiembre de 2026".
- **Idegen szó felismerése.** Minden tantárgynál fut, DE az utasítás most
  kimondja, hogy a magyar szakszavak (metszet, unió, halmaz, energia…)
  magyar szavak. Korábban ezeket angolul ejtette ki.
- **Gyerek törlése** (`/children/<id>/torles`) – az előfizetést NEM érinti.
- **Hogy megy? oldal** (`/hogy-megy`) – nap/hét/hónap.

### `hang.py`
- **A felolvasás végigmegy.** `MAX_KARAKTER` 420 → 3000. A napi keret
  (30 000) változatlan.
- **Minden szorzásjel egyformán szól.** `×`, `·`, `*`, `x`, `X` két szám
  között mind „háromszor négy" lesz, nem „három szorozva négy".
- **Szerkesztőjelek kiszedése** (`szerkesztojelek_le`): lábjegyzetek
  (`[^1]`), félkövér csillagok, címsor-jelek. Ezeket a felolvasó betűzte.

### `database.py`
- **Megőrzési idő 12 hónap** (`MEGORZES_HONAP`). Csak a beszélgetések
  törlődnek; a haladás megmarad.
- **Tanulási idő kulcs-javítás** (`_tanulas_targy_kulcsok`). Emiatt volt
  `tanult=0`, és emiatt zárult be véglegesen egy témakör.

### `templates/chat.html`
- **Új munkafelület** (csak `uj_felulet` esetén): tábla balra, keskeny
  beszélgetés jobbra, összecsukható.
- **A kérdés nem ismétlődik**: a legutolsó tanári üzenet csak a táblán van,
  a sávban egy halvány sor mutat rá.
- **Kinézet a munkasáv keretén** (nem a szöveg alatt – a szöveg fehér
  lapon marad, hogy minden minta mellett olvasható legyen).
- **Hangos mód**: a mikrofon tömör alsó sávban, a felirat mellette.
  Összecsukva a tábla sarkába úszik, ugyanakkorán.
- **Hátralévő idő** a sín alatt. 180 percnél hosszabb értéket NEM írunk ki
  (addig, amíg a leckehossz számítása nincs kész).

### `static/css/style.css`
- **Telefonos indítósáv**: 820 képpont alatt a két gomb a képernyő aljához
  tapad, rövid felirattal. Asztali gépen az indítósáv MINDIG ott van,
  választás előtt halványan.
- **Széles képernyő**: 1200 képponttól a tanulás felülete 1860-ig nyúlik.
- **Nagyításban ugyanaz a háttér**, mint egyébként.

### `kinezet.py`
- **Olcsóbb kinézetek**: szín 150 → 50, mintás 350 → 80, különleges
  600 → 150.
- **Nyolc új kinézet**: menta, homok, rózsaszín, grafit, zenés, mancsok,
  hullámok, levelek. Összesen 19.

### `level.py`
- **„Ebben az időszakban nem tanult."** (korábban „Ezen az időszakon".)
- Logó a levél tetején, és a tárgysor a választott gyakoriságot követi.

### `translations.py`
- Új kulcsok: `hogymegy_*`, `uj_*`, `lecke_hatra`, `tasks_selected_prefix`,
  `btn_ai_chat_rovid`, `btn_ai_voice_rovid`.
- A szintfelmérő üzenete „fél órát"-ra változott.

### `ellenor.py` (ÚJ)
- Néma ellenőr, AI nélkül: tanterv, fordítás, sablon, kiejtés, kártya.

### `.gitignore`
- A „Claude outputs" mappa és a próbaképek nem mennek a GitHubra.

---

## NYITOTT – erről még nincs döntés

1. **A lecke hossza.** A tantervi óraszám az egész ÉVRE szól, ezért jön ki
   4200 perc. 541 lecke érintett az 598-ból. Sándor kérése: a hossz a lecke
   NEHÉZSÉGÉHEZ igazodjon, ne egy mechanikus szorzóhoz.
2. **A kártyaképek.** 52 kártyából 42-nek nincs képe. A műhelyben a stílus
   „A – HŐSPILLANAT"-ra van írva, de a kártyánkénti promptok még a régi
   portré-receptet használják. Ezért nem egységes a szett.
3. **Az album mérete.** 52 hely, 52 kártya – de csak 10 képpel. Amíg nincs
   meg mind, az albumot nem érdemes hirdetni.
4. **A hosszú lecke görgetése.** Most az egész lap görög; csak a tábla
   belsejének kellene.
5. **A gondolkodás-jelző.** Sándor szerint korábban szöveg volt, most
   pöttyök. NEM tudjuk, mi változtatta meg. Konzol-kép kell hozzá.
6. **Visszajelzés gomb** a teszt idejére.
7. **Számbillentyűzet** telefonra és tabletre.
8. **Bemutató oldal** a szülőknek (videó NEM, amíg a felület mozog).
