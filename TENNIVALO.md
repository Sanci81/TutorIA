# TutorIA – tennivalók

Ez a fájl azért van, hogy ne a fejedben kelljen tartani. Ha valamit
elintéztél, húzd ki, vagy töröld a sort.

Utoljára frissítve: 2026-09-03

---

## MIELŐTT BÁRKI MÁS GYEREKE HASZNÁLJA

Ezek nem sürgősek most, amíg csak a saját családod használja. De az első
külsős tesztelő ELŐTT mind a négynek kész kell lennie.

- [ ] **Azure: váltás fizetős szintre (S0).**
      Az ingyenes szint havi 500 000 karakter felolvasás és 5 óra
      hangfelismerés. Ha elfogy, a szolgáltatás NEM kezd el fizetni —
      leáll, HTTP 429 hibával. A gyerek számára ez úgy néz ki, hogy a
      hangos mód a hónap közepén némán abbahagyja. Két gyereknél ez már
      reális.

- [ ] **Railway: fizetős csomag.**
      Sándor döntése: csak akkor, amikor a program kész. Addig marad az,
      ami van.

- [ ] **Railway DPA (adatfeldolgozói szerződés).**
      A railway.com/legal/dpa 13. szakaszában lévő DocuSign-link
      2026-09-02-én "Not Found"-ot ad. Támogatáson keresztül kell kérni.

- [x] **OpenAI DPA** – az űrlap: ironcladapp.com/public-launch/63ffefa2bed6885f4536d0fe
      (Az OpenAI DPA-oldal MAGYAR fordításában nincs benne az aláíró
      link — angolra kell váltani, vagy a fenti címre menni.)

- [x] **Microsoft / Azure DPA** – NINCS TEENDŐ. Automatikusan része az
      előfizetésnek, ingyenes fióknál is. Hivatkozási alap:
      microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA

Ha később vállalkozó leszel, a DPA-kat újra kell kötni a vállalkozás
nevére — magánszemélyként aláírva most rendben van, de nem marad az.

---

## AZ OKTATÁS MINŐSÉGE (ez a fő munka)

- [~] **Óraterv.** A témakörön belül eddig nem volt sorrend: a tanár minden
      fordulóban a nulláról improvizált. Innen jött, hogy a `there is /
      there are` a létige ELŐTT került elő.
      - [x] (1) a `nyelvtan` és `szokincs` mezők visszaszerzése
            (`curriculum_loader._szerkezet`)
      - [x] (2) a terv generálása és tárolása témakörönként
            (`oraterv_keszito.py` → `oratervek/` mappa)
      - [x] (3) a tanári prompt átállítása a tervre (`oraterv.py`, és az
            `app.py`-ban a `_topic_teaching_prompt_block` — EGYETLEN hely)
      - [ ] (4) admin nézet, ahol a terv megnézhető és újragenerálható
      - [ ] a többi tantárgy legenerálása (ma CSAK a matek 4. van kész)

      HOGY MŰKÖDIK: `oratervek/Matematika_1_4__4.json` — tantárgyanként,
      évfolyamonként (nyelveknél nyelvenként) egy fájl. Ha egy témakörhöz
      NINCS terv, az `oraterv.py` üres szöveget ad, és minden pontosan úgy
      megy, ahogy eddig. A terv mellé el van mentve a tantervi szöveg
      lenyomata: ha a kerettanterv változik, a régi terv MAGÁTÓL érvényét
      veszti — nem tanít elavult anyagot.

      FONTOS: az `oratervek/` mappa NINCS a .gitignore-ban, tehát a
      tervek a repóval együtt mennek ki Railwayre. Push után élesek.

      MENNYIBE KERÜL a többi: kb. 110 tantárgy-évfolyam, nagyságrendileg
      40-50 euró. Ezért lett először CSAK a matek: ha a szerkezeten
      igazítani kell, egy tantárgy megy újra, nem száztíz.

- [ ] **A 888 soros tanári utasítás megrövidítése.**
      Önmagának mond ellent (4657. sor: "Taníts meg 3-4 új dolgot
      EGYSZERRE" vs 4858. sor: "EGYSZERRE CSAK EGY új nyelvi elemet").
      Most már az ÓRATERVNEK is ellentmond ("egyszerre egy lépés").
      A terv az utasítás legvégén van, tehát erősebb — de ha a próbán
      azt látod, hogy a tanár továbbra is ömleszt, ez a régi sor a
      bűnös, azt kell kivenni. KÜLÖN lépésben, hogy tudjuk, melyik
      változtatás mit okozott.

---

## TANANYAG-HIÁNY

- [x] **A német tananyag rendben van, és be is töltődik.**
      Kétszer tévedtem vele 2026-09-02-én. Először azt hittem, hiányos a
      JSON (nem az: teljes, sorrenddel és szókinccsel). Aztán azt, hogy a
      program nem tölti be (betölti: a felület ÉKEZET NÉLKÜL küldi a
      nyelvet — `value="nemet"` —, és a betöltő pont ezt várja).
      A hibát a tanar_teszt.py-ba ÉN írtam bele, ékezettel.

- [x] **Viszont három VALÓDI hiba kijött közben, a fordítottja:**
      a hangátírás három helyen csak az ÉKEZETES "német" alakot ismerte,
      miközben a felület ékezet nélkülit küld. Következmény: a német
      beszédet MAGYARKÉNT íratta át, és a német óra kimaradt a kétnyelvű
      átírásból. Javítva: mindhárom hely mindkét alakot elfogadja.

## HIÁNYZÓ FUNKCIÓK

- [ ] A spanyol oldalon nincs album.
- [ ] Versek felolvasása. A lista megvan, mind közkincs: Kölcsey
      (Himnusz, Huszt), Vörösmarty (Szózat, Szép Ilonka), Petőfi
      (Anyám tyúkja, Füstbe ment terv), Arany (Családi kör, A walesi
      bárdok), Ady (Föl-földobott kő, Karácsony), József Attila
      (Altató, Mama), Radnóti (Nem tudhatom, Éjszaka).
      Weöres NEM közkincs — őt nem lehet.
- [ ] Kb. 18 magyar kártyakép hiányzik.
- [ ] Bemutató oldal a szülőknek. NE videó, amíg a felület változik —
      3-4 képernyőkép és a heti szülői levél. Az a levél az, amit a
      szülő valójában vesz.
- [ ] Domain. Még nincs eldöntve.

---

## ELLENŐRZÉS PUSH ELŐTT

```
python hang_teszt.py
```

49 esetet néz: mit LÁT és mit HALL a gyerek. INGYENES, két másodperc,
nem hív AI-t. Mindnek "ok"-nak kell lennie. Minden sor egy valódi hiba
emléke — ha újat találsz, oda kerüljön be, ne csak a javítás.

## HIBAKERESÉS ÓRÁK LEJÁTSZÁSÁVAL

```
python tanar_teszt.py --gyors            3 óra, néhány tíz cent
python tanar_teszt.py --ora 20 --fordulo 6    20 óra, pár euró
```

Ehhez KELL az OpenAI kulcs, egyetlen sorban, sortörés nélkül:
    $env:OPENAI_API_KEY = "sk-proj-..."
Ha elakad: `python tanar_teszt.py --proba` megmondja, hol.

AMIT EDDIG TALÁLT (mind valódi, mind javítva):
  · a tanult szó nem is látszott – a jelölő eltüntette
  · a nyers <VOCAB> jelölő kiment a képernyőre
  · a feleletválasztós kérdésekből eltűntek a válaszlehetőségek
  · a mondat végi szavak összeragadtak: "alreadyyet", "llamarseser"
  · az <FL:en>...</FL:en> jelölők kiszivárogtak angolórán
  · a tanár arról kérdezett, amit két sorral feljebb ő maga mondott ki

## FONTOS: MÉRÉS ÉS JAVÍTÁS NEM EGYSZERRE

2026-09-02-én elrontottam: egyszerre változtattam a programon ÉS az
ellenőrző listáján, ezért a 47 → 54 összehasonlítás semmit nem jelentett.
A "gyanús" 43 → 23 esése is nagyrészt a lista pontosításától volt.

A helyes sorrend, ha MÉRNI akarunk:
  1. az ellenőrző listáját RÖGZÍTJÜK (nem nyúlunk hozzá)
  2. futtatunk → ez a kiindulási szám
  3. javítunk CSAK a programon
  4. újra futtatunk ugyanazzal a paranccsal → ez az igazi összehasonlítás

A tanar_teszt.py HIBAKERESŐNEK kiváló, MÉRŐMŰSZERNEK csak így.

## AMI A JELENTÉSBŐL MÉG HÁTRAVAN

- [~] **Ténybeli hibák.** Erre lett az óraterv: a matek 4. tervében az
      ellenőrző 39 ténybeli hibát javított ki, MIELŐTT gyerek látta
      volna. Köztük igaziak: 245 + ? = 482-t összeadással akarta
      megoldatni (kivonás kell); a 402 − 178 pótlásos lépései hibásak
      voltak; 4 piros és 1 kék korongból akart 10 húzást visszatevés
      nélkül. Ez a tantárgyakra egyenként igaz — ahol nincs terv, ott
      a hiba is megmarad.
      Régi feljegyzés a szabályalapú megoldás korlátairól:
      "az ötvözet több fém keveréke" (az acél vas ÉS szén),
      "az életképes dalok" (helyesen: életképet bemutató dalok),
      "él/ella es – ő van" (a ser igének nem ez a jelentése).
      Ezt SZABÁLLYAL nem lehet megoldani – tudásbeli tévedés, nem
      szabálysértés. Két út van: okosabb modell a tanárnak, vagy
      tantárgyanként egy ellenőrző lépés. Mindkettő pénzbe kerül.
- [ ] **Magyartalan mondatok** (11 biztos). Írtam rá szabályt valódi
      példákkal, de még nem mértük, hogy használt-e.
