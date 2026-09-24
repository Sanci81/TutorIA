# TutorIA — nyitott teendők

Ez a fájl azért van, hogy semmi ne egy beszélgetés emlékezetén múljon.
Ha egy tétel elkészült, húzd át vagy töröld. Ha újat találsz, írd ide.

Utolsó frissítés: 2026-09-23

---

## Azonnal (a poszt már kiment, a cím publikus)

- [ ] **Robot elleni védelem.** Percenkénti korlát a regisztrációra, a
      belépésre és a chatre. Enélkül valaki robottal fiókokat gyárthat és
      égetheti a hangperceket. Ez a legsürgősebb.
- [ ] **Próba (staging) oldal.** Külön Railway service a `proba` ágról,
      SAJÁT adatbázissal. Részletes leírás: `PROBA_KORNYEZET.md`.
      Amíg nincs, minden push azonnal az éles oldalra megy.

## Leckeoldal — megtalált, még javítatlan hibák

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
