# TutorIA — amit tudnod kell, mielőtt hozzányúlsz

Ez a fájl AZ AI-ASSZISZTENSNEK szól (Cursor, Composer, bármelyik modell).
Olvasd el végig, mielőtt bármit módosítasz. Magyarul válaszolj.

## MI EZ

Kétnyelvű (magyar/spanyol) AI-tanár gyerekeknek. Flask + PostgreSQL,
Railway-en fut. A tulajdonos: Sándor, NEM programozó. Magyarul beszélj vele,
és úgy magyarázz, ahogy egy türelmes kollégának — ne szórd tele szakszóval.

A cél NEM a gyors szállítás. A cél az, hogy amit a gyerek lát, az HIBÁTLAN
legyen. Egyetlen rossz mondat többet árt, mint amennyit tíz új funkció használ.

## HÁROM SZABÁLY, AMIT NEM SZEGHETSZ MEG

1. **Külalak-változtatás előtt MUTASD MEG.**
   Ha a felületen bármi látszani fog másképp (szín, elrendezés, gomb, betű),
   előbb készíts egy önálló HTML mintát, és kérdezd meg, jó-e. Csak utána
   nyúlj a valódi fájlhoz. Ez nem udvariasság: már volt olyan, hogy egy
   „gyors" módosítás elrontotta a fejlécet, és nem derült ki napokig.

2. **Push előtt kötelező:** `python hang_teszt.py`
   49 esetet néz meg AI nélkül, két másodperc, ingyenes. MINDNEK "ok"-nak
   kell lennie. Minden sor egy VALÓDI hiba emléke, amit egy gyerek talált
   meg használat közben. Ha új hibát javítasz, oda is vedd fel — a javítás
   önmagában kevés, az emlék kell.

3. **Ne nyúlj ahhoz, amiről nem kérdeztek.**
   Ez a program 438 KB-os `app.py`-t tartalmaz, sok egymásra épülő résszel.
   Ha valami útban van, SZÓLJ, ne javítsd ki magadtól. Sándor kifejezett
   kérése: „csak kérlek máshoz ne nyúlj, mást ne tegyünk tönkre".

## TECHNIKAI TUDNIVALÓK, AMIK IDŐT SPÓROLNAK

- Az `app.py` **csak Python 3.12-vel fordul**: `python3.12 -m py_compile app.py`
- A felület a nyelvet **ékezet nélkül** küldi (`value="nemet"`), a régi kód
  helyenként ékezetest várt. Mindkét alakot fogadd el.
- Az OpenAI JSON-válaszhoz a kérésben szerepelnie kell a "json" szónak.
- Egy sortörést tartalmazó API-kulcs félrevezető `APIConnectionError:
  Connection error.` hibát ad. Ha ilyet látsz, ELŐSZÖR a kulcsot nézd.
- A böngésző kb. 6 AudioContextet enged. Újat NE hozz létre hívásonként.

## A FÁJLOK, AMIK SZÁMÍTANAK

| fájl | mit csinál |
|---|---|
| `app.py` | minden: útvonalak, a tanári prompt, a chat |
| `curriculum_loader.py` | a kerettantervi JSON-ok betöltése |
| `oraterv.py` | az előre elkészített óratervet teszi a promptba |
| `oraterv_keszito.py` | a terveket készíti (külön futtatva, pénzbe kerül) |
| `oratervek/` | a kész tervek. Csak a matek 4. osztály van meg |
| `hang.py` | AMIT A GYEREK HALL: számok, ragok kiejtése |
| `szamellenor.py` | AMIT A GYEREK LÁT: rossz kérdésformák javítása |
| `hang_teszt.py` | a fenti kettő regressziós tesztje – INGYENES |
| `tanar_teszt.py` | órákat játszik le hibakeresésre – PÉNZBE KERÜL |
| `TENNIVALO.md` | a nyitott feladatok. Ha lezársz egyet, húzd ki |

## MÉRÉS ÉS JAVÍTÁS NEM EGYSZERRE

Ha azt akarod tudni, hogy egy változtatás segített-e:
1. az ellenőrző listáját RÖGZÍTED (nem nyúlsz hozzá),
2. futtatsz → ez a kiindulás,
3. javítasz CSAK a programon,
4. újra futtatsz UGYANAZZAL a paranccsal.

Ha közben az ellenőrzőt is módosítod, a két szám nem hasonlítható össze.
Ez már egyszer megtörtént, és egy egész napi mérés lett tőle értéktelen.

## A PÉNZ SZÁMÍT

Sándor nem cég, magánszemélyként fizeti. Minden AI-hívásnak ára van.
- Ne futtass olyat, ami pénzbe kerül, amíg meg nem kérdezted.
- Az ingyenes ellenőrzést (`hang_teszt.py`) futtasd bátran.
- Ha drágább modellt javasolsz, írd oda, körülbelül mennyivel drágább.

## HOL TART MOST (2026-09-03)

Kész és él: a témakörönkénti óraterv. A tanár már nem improvizál — előre
elkészített, tényellenőrzött lépéssorrendet követ, egyszerre egy lépést.
DE ez EGYELŐRE CSAK a 4. osztályos matekra van meg (`oratervek/`).

A következő lépések, fontossági sorrendben:
1. Egyetlen évfolyam végigvitele hibátlanra — nem az összes.
2. A 888 soros tanári utasítás megrövidítése. Önmagának mond ellent
   („taníts 3-4 dolgot egyszerre" vs. „egyszerre csak egyet"), és most már
   az óratervnek is. CSAK külön lépésben, hogy mérhető legyen.
3. A spanyol oldalon nincs album.
4. Kb. 18 magyar kártyakép hiányzik.

A részletek a `TENNIVALO.md`-ben vannak. Azt olvasd el másodikként.
