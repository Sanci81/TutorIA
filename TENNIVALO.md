# TutorIA – tennivalók

Ez a fájl azért van, hogy ne a fejedben kelljen tartani. Ha valamit
elintéztél, húzd ki, vagy töröld a sort.

Utoljára frissítve: 2026-09-02

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

- [ ] **Óraterv.** A témakörön belül ma nincs sorrend: a tanár minden
      fordulóban a nulláról improvizál. Innen jön, hogy a `there is /
      there are` a létige ELŐTT került elő.
      A tantervi fájlokban ott a helyes sorrend (pl. angol 5. osztály:
      1. létige, 2. kérdőszavak, 3. rövid válaszok), de a
      `curriculum_loader.extract_topic_catalog()` eldobja — csak
      `id, name, text, index, ora_szam` marad.
      Négy lépés: (1) a `nyelvtan` és `szokincs` mezők visszaszerzése,
      (2) a terv generálása és tárolása témakörönként, (3) a tanári
      prompt átállítása a tervre, (4) admin nézet, ahol a terv
      megnézhető és újragenerálható.

- [ ] **A 888 soros tanári utasítás megrövidítése.**
      Önmagának mond ellent (4657. sor: "Taníts meg 3-4 új dolgot
      EGYSZERRE" vs 4858. sor: "EGYSZERRE CSAK EGY új nyelvi elemet").
      CSAK az óraterv élesedése UTÁN — külön lépésben, hogy tudjuk,
      melyik változtatás mit okozott.

---

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

41 esetet néz: mit LÁT és mit HALL a gyerek. Mindnek "ok"-nak kell
lennie. Minden sor egy valódi hiba emléke, amit egyszer már ki kellett
javítani — ha új hibát találsz a felolvasásban vagy a feladatokban,
oda kerüljön be, ne csak a javítás.
