# TutorIA — nyitott teendők

Ez a fájl azért van, hogy semmi ne egy beszélgetés emlékezetén múljon.
Ha egy tétel elkészült, húzd át vagy töröld. Ha újat találsz, írd ide.

Utolsó frissítés: 2026-10-03 (este)

---

## Azonnal (a poszt már kiment, a cím publikus)

- [ ] **Robot elleni védelem.** Percenkénti korlát a regisztrációra, a
      belépésre és a chatre. Enélkül valaki robottal fiókokat gyárthat és
      égetheti a hangperceket. Ez a legsürgősebb.
- [ ] **Próba (staging) oldal.** Külön Railway service a `proba` ágról,
      SAJÁT adatbázissal. Részletes leírás: `PROBA_KORNYEZET.md`.
      Amíg nincs, minden push azonnal az éles oldalra megy.

## Leckeoldal — megtalált, még javítatlan hibák

- [ ] **Nincs feladat az "oldd meg ezt" után.** A tábla azzal zárul, hogy
      "Most figyelj jól, és oldd meg ezt!", és NEM JÖN utána semmi. Közben
      a jobb oldali doboz azt írja: "A kérdés a táblán van. Ide írd a
      választ." A gyerek tehát válaszolni köteles, de nincs mire.
      (Matek, 2026-10-03, képernyőkép Sándortól.)
      GYANÚ: a tábla szövege és a feladat külön lépésben érkezik, és a
      feladat elvész. Ott kell nézni, ahol a tábla tartalma összeáll.
- [ ] **A halmazos ábra három hibát vét egyszerre.** (2026-10-03)
      * a szilva a NAGY KÖRÖN KÍVÜL van, pedig a lecke szerint eleme a
        halmaznak — az ábra az ellenkezőjét tanítja a szövegnek;
      * az "alma" és a "körte" felirat nem tapad a saját köréhez, köztük
        egy harmadik, névtelen kör áll;
      * az ábra alján ott a MEGOLDÁS ("Az alma benne van"), közvetlenül a
        kérdés alatt, hogy "Az alma elem a gyümölcsök halmazában?".
      Ez nem stíluskérdés. Szabály kell: felirat mindig a saját alakzata
      mellé, elem mindig a halmazon BELÜLRE, és megoldás SOHA nem kerülhet
      az ábrára.

- [ ] **Választós feladatnál hiányzik a mondat.** A tanár azt írja
      „nézd meg a mondatot", de csak a két szó jelenik meg, mondat nélkül.
      Így a kérdés megválaszolhatatlan. (Nyelvóra, 2026-09-21)
- [ ] **„Még 30 perc ebből a leckéből" nem csökken.** MEGNÉZVE 2026-09-21,
      az ok tisztázva:
      * A szám = a lecke ajánlott hossza mínusz az ebben a témakörben
        eltöltött percek (`app.py`: `_hatra_perc`, a `child_chat` nézetben).
      * A tanult perceket 30 másodpercenként MENTI a program
        (`/api/learning/heartbeat`), tehát az adatbázisban HELYESEN nő.
      * A felirat viszont a Jinja sablonba van beégetve OLDALBETÖLTÉSKOR
        (`chat.html` 816-817. sor), és utána SOHA nem frissül. Ezért áll
        egy helyben, akármennyit tanul a gyerek.
      * JAVÍTÁS: a heartbeat válasza adja vissza a hátralévő percet, és a
        `.lecke-hatra` felirat frissüljön belőle. Kb. 15 perc munka.
- [ ] **Írásos módban túl sok szót kérdez egyszerre.** Egy kérdésben tíz
      szó is szerepelt. A HANGOS módra ez már meg van oldva, az írásosra
      nem. Ugyanott javítható.
- [ ] **A „Gondolkodom…" jelző kint ragad.** ELHALASZTVA, NEM MEGOLDOTT.
      Félbehagyva 2026-09-20, akkor kellett a vizsgálatot abbahagyni.
      A tanár válasza már kint van a táblán, a gyerek mégis azt látja,
      hogy a tanár gondolkodik. Amit már KIZÁRTUNK, hogy ne kelljen újra:
      * NEM elmentett üzenet, hanem tényleg a jelző. A tanári buborék
        zöld és balra igazított (`static/css/style.css` 1889. és 1903.
        sor), és a jelző ezt az osztályt viseli (`chat.html` 859. sor).
      * A frontend mindkét küldési útvonalán VAN hibakezelés, és
        mindkettő a válasz elején elrejti a jelzőt (`chat.html`: szöveges
        `sendMessage` 3217. és 3257. sor, hangos `sendVoiceChat` 3634. és
        3680. sor). Tehát ha a válasz megjön, a jelző eltűnik — vagyis a
        beragadás azt jelenti, hogy a VÁLASZ NEM JÖTT MEG.
      * Két védőháló van rá (`chat.html` 2812–2878. sor): egy
        másodpercenkénti és egy 110 másodperces. Ezeket Claude tette be
        2026-09-20-án a `2eeae18` commitban — nem mértük meg, segít-e.
      KÖVETKEZŐ LÉPÉS, mérés előbb: idézd elő, és NE nyúlj hozzá, csak
      figyeld az órát. Ha 1-2 másodpercen belül eltűnik, nincs hiba (a
      kép készült rossz pillanatban). Ha 30 mp-en túl is ott van, de 2
      perc körül eltűnik, akkor a kérésszámláló ragadt be, és a javítás
      helye a `chat.html` 2850. sora (a `fetch` hívás try/catch-be).
      GYANÚ, amit nem vizsgáltunk végig: a `Procfile`-ban 4 munkás × 12
      szál fut a Railway-en. Ha a memória elfogy, a munkást kilövik, és a
      kérés válasz nélkül hal meg — ez pontosan ezt a tünetet adná.
      (A kabala-figura eltűnése ehhez NEM tartozik, azt Sándor megtalálta.)

## Bemutató oldal (index) — még javítatlan

- [ ] **"Az első hónap ingyenes" — nem igaz.** A hero ezt írja, a meta
      leírás, a GYIK és a regisztráció viszont már a helyes 120 percet.
      Így ugyanazon az oldalon mond mást a nagybetűs ígéret és a többi.
      JAVASLAT a szövegre: "Négy teljes lecke ingyen. Bankkártya nem kell."
      — ugyanaz a keret, de nem hangzik kicsinek, és igaz.
- [ ] **A nyolc évfolyamgomb mind a regisztrációra visz**, és a választott
      évfolyamot nem viszi magával. A szülő választ egyet, aztán újra
      elkérünk tőle mindent. Legalább legyen előre kitöltve.
- [ ] **A szülői kód a legelső űrlapon van.** Ki lehetne kérni később,
      amikor először benéz a szülői részbe — kevesebb gondolkodás az
      első képernyőn.

## Demó oldal

- [ ] **A mostani demó nem jó, és ZÁRVA van az éles cím elől.**
      (2026-10-03) Egy kerekítős feladat és egy rajzoló mező — ez nem
      mutatja meg, amit a TutorIA tud. A program maga zárja ki az éles
      gépnéven: `_demo_engedve()` az `app.py`-ban, és a "/demo" kikerült
      a `KERESO_OLDALAK` listából, hogy a Google se indexelje.
      AMI IDE KÉNE HELYETTE: egy 60-90 másodperces képernyőfelvétel egy
      igazi leckéről. Ha az megvan, az `_demo_engedve()` függvényt ki kell
      venni, és a "/demo" sort visszatenni a `KERESO_OLDALAK` listába.
      FIGYELEM a költségre: a rajzoló mező `gpt-image-1`, 1024x1024,
      quality="high" — ez képenként nagyságrendileg 0,17-0,19 dollár, nem
      pár cent. IP-nként óránként 5 kép a korlát (`_KEP_MAX`).

## Album

- [ ] **A könyv-érzés nincs feltéve.** Megcsináltuk és le is teszteltük
      (gördülő lapozás a gerinc körül, halk papírhang, "Tartalom" gomb
      ugrólistával), de a gépre NEM került fel, mert megszakadt a
      kapcsolat. Újra el kell végezni az `album.html`-en.

## Oktatási ötletek — ezeket NE felejtsük el (2026-10-03)

Négy ötlet, sorrendben aszerint, hogy mennyit ad vissza. Egyik sem
"még egy funkció": mind a jelenlegi fájó pontokra válasz.

### 1. Élő tábla — a tanár RAJZOL, nem képet mutat
Ne kész képet tegyen ki a rendszer, hanem a gyerek szeme előtt rajzolja
meg, vonalról vonalra, miközben magyarázza — ahogy egy tanár a táblánál.
Technikailag az AI NEM képet készít, hanem néhány egyszerű utasítást küld
(kör ide, nyíl oda, felirat alá), és a böngésző kirajzolja.
MIÉRT EZ A JÓ VÁLASZ az ábrás gondra:
  * nem kell sablon minden témához — az AI összerakja az alapelemekből
    bármit, amit a gyerek kérdez;
  * nem kerül pénzbe, mert szöveg megy át, nem kép;
  * nem tud rossz számot a képre írni, mert a parancskészletet mi
    szabjuk meg;
  * SOHA nem árulhatja el a megoldást, mert azt a parancskészlet tiltja.
  * a mostani halmazos hibák (szilva kívül, felirat elcsúszva, megoldás
    a képen) ezzel mind megszűnnek.

### 2. A gyerek is a táblához megy
Ne csak nézze az ábrát: húzza be az almát a halmazba, jelölje be a 3/4-et
a számegyenesen, tegye sorba a számokat. A helyességet a GEOMETRIA dönti
el, nem AI — ingyen van és azonnal válaszol. Ez a különbség az
"elolvastam" és az "én csináltam" között.

### 3. "Most te magyarázd el nekem."
A lecke végén a tanár szerepet cserél: megjátssza, hogy ő a kisebb, aki
nem érti, és a gyerek tanítja meg neki ("De miért kell ott kerekíteni?").
A tanítás a legerősebb ismert tanulási mód, és gyerekeknek szinte senki
nem építette meg. Egy AI-hívásba kerül. Ez egyben kész demóvideó is:
ebben a pillanatban mondja azt egy szülő, hogy ilyet máshol nem látott.

### 4. A felejtés elleni gép
Minden lecke EGYETLEN kérdéssel kezdődjön egy három hete tanult témából.
Nem külön gyakorlás, nem plusz feladat — egy kérdés. A szülői jelentés
pedig ne azt mondja, hogy "befejezte", hanem hogy "a három hete tanult
törtek még megvannak". A szülőt nem az érdekli, hogy haladt-e, hanem
hogy MEGMARADT-e. Ezt senki nem mondja meg neki — és ezért fizet tovább
a második hónapban.
Kell hozzá: témakörönként (utolsó_siker, következő_esedékes) — egy tábla.

### Amit megvizsgáltunk és ELVETETTÜNK
- **Tanulási stílusok** (vizuális / auditív / olvasó / cselekvő szerinti
  személyre szabás): ez az oktatás legszívósabb tévhite, sokszor
  megvizsgálták, és NEM javítja a tanulást. Hónapokat vinne el. Helyette
  a gyerek VÁLASSZON az adott pillanatban: "mutassam képpel? mondjam el
  máshogy?".
- **Globális osztályterem** (magyar és spanyol gyerekek közös munkája):
  gyerekek kapcsolatba lépnének idegen gyerekekkel — gyermekvédelmi és
  GDPR-kockázat egy egyszemélyes cégnek, és pont azt rombolja le, amin a
  bizalom áll: "Nincs benne idegen. Se csevegés más gyerekekkel."
- **Játékosítás, hangos beszélgetés**: ezek NAGYRÉSZT MÁR MEGVANNAK
  (érme, kártya, album; hangmód kiejtés-visszajelzéssel). Nem új
  fejlesztés kell, hanem hogy LÁTSZÓDJANAK az oldalon.

## Album — a lapozás még nem jó (2026-10-03 este)

- [ ] **Függőleges csíkok a fényképen lapozás közben.** MEGMÉRVE:
      egyszínű lapon EGYETLEN vonal sem jelenik meg, tehát NEM hézag van
      a szeletek közt. A hajló lap 24 LAPOS szeletből áll, és a hajlat
      közepén a szomszédos szeletek dőlése közt ~18 fok a különbség —
      fényképen ez töréspontként látszik. Teljesen sima ívhez WebGL
      kellene, CSS-sel nem megy.
      VÁLASZTÁS: (a) több szelet + szélesebb hajlat (kisebb törés, de nem
      tűnik el, telefonon lassabb); (b) hajlás nélkül, egy darabban
      forduló lap — nulla törés, gyors; (c) címsor-kapcsoló
      (`?csik=40`, `?hajlat=0.9`, `?lapozas=egyszeru`), hogy Sándor a
      valódi kártyáin próbálhassa ki.
- [ ] **A lapozógombokhoz le kell görgetni.** A lap 640 képpont magas, a
      gombok alatta vannak. Letapadó (sticky) gombsor kell, ami a
      képernyő alján marad, miközben az albumot görgeti.
- [ ] **Telefonon nem jó.** Pontosítani kell, mi romlik el: a 3D hajlás,
      az elrendezés, vagy mindkettő.

## SEO — amit a 2026-09-27-i kör NEM ért el

- [ ] **Hreflang sehol nincs kint.** A magyar főoldalon, a spanyol
      főoldalon és a blogcikken sem találtam. A sitemapban sincsenek
      `xhtml:link` sorok. Enélkül a Google két különálló, azonos tartalmú
      oldalnak látja a magyart és a spanyolt.
- [ ] **A blogra semmi nem linkel.** Se a főoldalról, se a láblécből.
      Csak a sitemapból érhető el, azt meg nem ember olvassa.
- [ ] A `/login` és a `/register` fölösleges a sitemapban.
- [ ] A spanyol oldalak magyar útvonalneveket használnak (`/es/csomagok`,
      `/es/gyik`). Spanyol keresésre rossz; később `/es/precios`,
      `/es/preguntas`.

## Tartalom

- [ ] **Spanyol album.** Nincs kész: spanyol, az ottani tanterv szerinti
      kártyák kellenek. Kártyaműhely sincs hozzá, mint a magyarhoz.
- [ ] **Hiányzó kártyaképek: 52-ből 42.** Addig is kell egy szép
      helyőrző, hogy a hiányzó kép ne tűnjön hibának.

## Növekedéskor

- [ ] **Resend fizetős csomag.** Az ingyenes keret havi 3000 levél;
      kb. 100 családnál fut ki (heti + napi jelentések).
- [ ] **Postgres slow query log** bekapcsolása.
- [ ] Az `info@tutoriacademia.com` postafiók ellenőrzése: tényleg
      megérkezik-e oda a levél (az Azure válasza is oda jön).

## Fizetés bekötése ELŐTT (kötelező)

- [ ] Vállalkozói (autónomo) — enélkül a többi nem indulhat.
- [ ] Bankkártyás fizetés (Stripe) + számlázás.
- [ ] **A tanterv rögzítése fizetéskor.** A kód kész (`csomag_tanterv`),
      egyetlen sort kell hozzáadni a fizetés lezárásánál. Szabály:
      az INGYENES próbában mindkét tanterv használható, de a 120 perc a
      kettőre ÖSSZESEN jár; a fizetős előfizetés viszont CSAK arra a
      tantervre szól, amelyikre megkötötték.

## Amire várunk

- [ ] **Azure TTS kvóta.** Kérelem beadva 2026-09-21, válasz 5 munkanapon
      belül. Alapérték 30 TPS, kértünk 300-at. A levél a
      `maccount@microsoft.com` és a `csgate@microsoft.com` címről jön.

## Megfigyelendő (egyszer előfordult, azóta nem)

- [ ] Üres oldalsó témakör-lista. Ha előjön: melyik tantárgy, és
      telefonon vagy gépen?

---

## Ami 2026-09-20/21 éjjel ELKÉSZÜLT

- Kabala-hiba: egy JavaScript-kivétel megállította az egész
  oldalbetöltést (`kabalaAllapot` a `KABALA_ALLAPOT` táblázat előtt futott).
- A gondolkodás-jelző nem kap többé hangszóró gombot.
- A gondolkodás-jelző TÉNYLEG eltűnik: a `hidden` attribútumot egy CSS
  `display:flex` írta felül, ezért maradt a képernyőn.
- A jelző csak a tanár válaszára vár (`valaszVarakozik`), nem bármilyen
  háttérkérésre.
- 20 másodperc után szöveget kap a gyerek, és visszakapja a beírómezőt.
- Fejben számolásnál nincs többé írásbeli, egymás alá írós tábla.
- Nagyításban a kabala ugyanakkora, mint rendes nézetben.
- Az `<FL:xx>` nyelvjelölők nem kerülnek ki a feladatok gombjaira.
- ÁSZF: előfizetés, elállási jog, elérhetőség/karbantartás, panasz.
- Facebook-előnézet (Open Graph) + 1200x630-as, középre komponált kép.

## 2026-09-22 – új ötletek, amiket NEM szabad elfelejteni

### 1. Elakadás-lista az admin oldalra  (kb. 1-1,5 óra)
Aggregált, névtelen kimutatás a MÁR MEGLÉVŐ adatokból: témakörönként
hányan kezdték el, hányan fejezték be, mennyi az átlagos idő, hányan
buktak el a teszten. Ebből látszik, hol akad el mindenki.
ÁSZF nem kell hozzá (nincs új adatgyűjtés). Az adatvédelmi
tájékoztatóba viszont kell egy mondat a névtelen statisztikáról.
NEM külső hőtérkép-szolgáltatás (Hotjar és társai) – gyerekoldalon
az külön adatfeldolgozói szerződést és tájékoztatást igényelne.

### 2. Kiejtés-javítás felolvasással  (közepes munka)
Az Azure Speech "Pronunciation Assessment" szolgáltatásával: a gyerek
felolvas egy ismert szöveget, a program szavanként pontozza, és
megmutatja, hol akadt meg.
FIGYELEM, két dolog:
  – a magyar nyelvi támogatást még ELLENŐRIZNI kell az Azure
    nyelvlistáján; a spanyol és az angol biztosan megy;
  – a modellek felnőtt beszéden tanultak, ezért gyereknél hamis hibát
    jelezhetnek. Csak NAGYON alacsony pontszámnál szóljon, és akkor is
    biztatva: "mondjuk ki még egyszer együtt", soha nem azt, hogy rossz.

### 3. Egy mondat az album oldalra (apró)
Halványan, kicsiben, az album alján:
"A kártyák képei művészi ábrázolások, nem hiteles portrék."
Fontos, mert pl. Bolyai Jánosról nem maradt fenn hiteles arckép.


---

# A LEGFONTOSABB NYITOTT KÉRDÉS: MEGÉRI-E? (2026-10-04)

Ezt HOLNAP kell végigszámolni, mindennel együtt. Itt van minden, ami
eddig kiderült, hogy ne kelljen újrakezdeni a gondolkodást.

## Mi derült ki ma

**1. A tokenárak a programban rosszak voltak.**
Az `app.py` a `gpt-5.4-mini` modellt hívja, a költségszámításban viszont
`BE_1M = 0.10` és `KI_1M = 0.60` állt. A gpt-5.4-mini valódi listaára
ennél jóval magasabb: nagyjából **0,75 dollár / millió bemenő token** és
**4,50 dollár / millió kimenő token**, a gyorsítótárazott bemenő pedig
**0,075**. A kimenőnél tehát HÉTSZERES az eltérés.

Következmény: az /admin oldal eurói ALACSONYABBAK a valóságnál. A
"0,19 €" és a "0,22 €" nem a tényleges költség.

Javítás kód nélkül, mert a program környezeti változóból olvassa:
Railway → a `web` szolgáltatás → Variables:
    BE_1M = 0.75
    KI_1M = 4.5

**2. A többi ár viszont stimmel.** Ellenőrizve:
  – Azure felolvasás: 16 USD / 1M karakter, és a havi 500 000 karakter
    ingyenes keret valós;
  – beszédfelismerés: a kód a `gpt-transcribe` modellt hívja, annak a
    közzétett ára pontosan 0,0045 USD / perc — a konstans helyes;
  – EUR/USD 0,92 — nagyjából rendben, néha ellenőrizni kell.

**3. A költséget nem a PERC hajtja, hanem a TOKEN.**
Az admin oldalon az egyik gyerek 42 percet tanult 0,19 €-ért, a másik
25 percet 0,22 €-ért. Nem hiba: a tokenek száma attól függ, hányszor
szólalt meg a gyerek, és milyen hosszú volt közben az előzmény, amit
minden kérésnél újraküldünk. A történelem hosszú magyarázatokat ad, a
kimenő token pedig hatszor drágább a bemenőnél.

**4. A veszély nem az átlagos gyerek, hanem a MEGÍGÉRT PERCKERET.**
A két mért gyerek az Alap keretének kb. a TIZEDÉT használta el 30 nap
alatt. Ennyi használatnál minden csomag bőven nyereséges. De ha valaki
TÉNYLEG elhasználja a keretét:
  – 100% kihasználtságnál, a valódi tokenárakkal, mind a három csomag
    VESZTESÉGES — még 90% gyorsítótárazással is;
  – a Max a legrosszabb, mert ott a legtöbb a perc.

## Amit holnap meg kell nézni

**a) Mennyi megy gyorsítótárból.** Ez dönti el a kérdést. A tananyag
minden kérésnél újra elmegy; ha a szolgáltató felismeri az ismétlődést,
tized árat fizetünk érte. A kód jelenleg NEM méri a `cached_tokens`
értéket — ezt be kellene vezetni a ChildUsage-be.

**b) A valódi be/ki token arány.** Az /admin oldalon mostantól ott van a
gyerek sorában a bemenő és a kimenő token, meg a kérések száma. Ebből
pontosan kiszámolható a valódi perc-költség, nem kell becsülni. ELŐBB
ezt kell leolvasni, és csak utána dönteni bármiről.

**c) Három lehetséges válasz, ha tényleg veszteséges:**
  – lejjebb vinni a perckereteket (400 / 900 / 1800 helyett kevesebb);
  – feljebb vinni az árat;
  – olcsóbbra venni a beszélgetést: rövidebb rendszerprompt, kevesebb
    előzmény visszaküldése, kisebb modell a könnyű kérdésekre.

**d) A számolólap.** `koltsegek_pontos.html` — minden mező átírható,
a valódi tokenárakkal és a gyorsítótár-százalékkal. A régi
`koltsegek.html` érintetlen maradt.

## Amit MÁR TUDUNK a saját adatainkból
  – autónomo 300 €/hó, könyvelő kb. 50 €/hó (bizonytalan, két főre 60
    volt), Railway kb. 40 €/hó, domain 8 €/év;
  – áfa 21% (spanyol magánszemély vásárlónál), fizetési jutalék
    kb. 1,5% + 0,25 € fix tranzakciónként;
  – az ingyenes próba 30 hangos perce gyerekenként kb. 31 cent — ez NEM
    az a tétel, ami megfog; a havi fix az.
