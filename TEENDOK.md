# TutorIA — nyitott teendők

Ez a fájl azért van, hogy semmi ne egy beszélgetés emlékezetén múljon.
Ha egy tétel elkészült, húzd át vagy töröld. Ha újat találsz, írd ide.

Utolsó frissítés: 2026-11-06

---

## TANÍTÓ FEJLESZTÉSE (2026-11-08)
- [ ] fix87: öt szabály a tanítónak (leragadás max. 2 azonos feladat, mindig kérdéssel zár,
      a válasz ne álljon a kérdés előtt, eszközre csak <FELADAT>-tal hivatkozik – a csoport és a
      robot felület MEGVAN, csak nem használta –, helyesírás). Kapcsoló: TANAR_JAVITAS
      (próbaoldalon magától be, élesen csak TANAR_JAVITAS=1). Mérés: tanar_teszt.py
      TANAR_JAVITAS=1-gyel, összevetés a 11-03-i jelentéssel (ugyanaz a véletlen sorrend, seed).
      Ha jobb: Railway főoldal TANAR_JAVITAS=1.
- [ ] fix87 MÉRÉS (11-08, gpt-5.4-mini, TANAR_JAVITAS=1): biztos hiba 12 → 9; nincs kérdés 8 → 1;
      leragadás (biztos) 7 → 0; ígért-de-hiányzó 2 → 0; DE „kérdésben a válasz” 2 → 3 és
      magyartalan 1 → 3. VIGYÁZAT: a 11-03-i mérés gpt-6-luna-val ment, ez gpt-5.4-mini-vel
      (az éles modell) – nem teljesen összevethető. fix88: a 3. és 5. szabály erősítve.
      Teszt ára gpt-5.4-mini-vel kb. 0,95 $ / futás (nem 0,12).
- [x] MÉRÉS ÖSSZEVETVE (11-08, mind gpt-5.4-mini): szabály nélkül 10, szabállyal 9, erősítettel 11
      biztos hiba → a prompt-szabályok nem segítettek mérhetően; a leragadás/hiányzó kérdés a
      luna modell hibája volt. fix89: TANAR_JAVITAS a próbaoldalon is KI (csak =1-gyel él).
      fix89: gépi „a → az” javítás magánhangzó előtt (_a_az_javit) – csak HU tanterv, nem idegen
      nyelvi és nem magyar órán, idézőjelek/FELADAT/jelölők belsejét nem érinti, számot nem.
      Következő tanító-fejlesztés: konkrét, gépileg ellenőrizhető hibák (mint az a/az), és a
      tanar_teszt nagyobb mintán (--ora 16), több futás átlagával.
- [ ] OKOS TANÍTÓ (Sándor víziója, 2026-11-08): minden gyereket a képességei szerint, türelmesen,
      empatikusan; a lecke sorrendje és a tanítás marad, csak a tempó/nehézség/forma igazodik.
      ✔ 1. lépés (fix90, TANAR_TEMPO – próbán magától be, élesen =1): 3/6/9 jó válasz után „ez megy,
        lépj tovább/nehezebbre”; unalom-jelekre („unom”, „vicces”, „fáradt”, „mindegy”) rövidebb,
        játékosabb feladat. Napló: [TANIT] jo_sor/unalom.
      ✔ 2. lépés (fix90): naponta az első üzenetnél leckénként 1–2 rövid ismétlő kérdés, utána
        ugyanott folytatja (napló: [ISMETLES]).
      [ ] 3. Tanulói profil (emlékezet): óra végén pár sor erősségről/gyengeségről, következő órán
        a prompt elejére; melyik feladatforma megy jobban (írós/kattintós).
      [ ] 4. Választható osztályzáró teszt (szülő kéri) → jelentés, szintlépés javaslata (a szülő dönt).
      [ ] tanar_teszt.py: többféle gyerek (gyors, lassú/hibázó, unatkozó) – így mérhető az igazodás.
      [ ] ESZKÖZÖK AZ OKOS TANÍTÓ KEZÉBEN (Sándor kérte felírni, 2026-11-08) – nem külön funkciók,
          a tanító akkor veszi elő, amikor látja, hogy kell; a leckét nem írják felül:
          • „Tanítsd meg te!” – a lecke végén a gyerek magyarázza el, amit tanult (ettől rögzül).
          • Hibavadász – ha a gyerek már nagyon érti, a tanító szándékosan hibázik, ő keresi meg.
          • Saját világ – a szöveges feladatokban a gyerek kedvenc állata/játéka (a szülő adja meg).
          • Villámkvíz a lecke végén – 5 gyors kérdés, pontszámmal.
          • Otthoni küldetés – „Mérd meg az asztalt, és írd be, hány centi!”
      [ ] Facebook-posztok kész (kinézet képek/facebook/posztok, 4 db, utm_source=fb_poszt).
      [ ] Reklámvideó: video_kanape.py (kep → video), utána Claude összerakja (15 mp).
- [ ] FEJLESZTÉSI LISTA (Sándor kérte felírni, 2026-11-08):
      • Tanító folyamatos fejlesztése: tanar_teszt → javítás → újramérés (mindig ugyanazzal
        a modellel, TANAR_JAVITAS=0 és =1 összevetve).
      • Hetente új feladattípusok, MINDKÉT oldalra (HU+ES), Feladat-próba keresőnévvel.
      • Témazáró-felkészítő: tantárgy + témakörök + dátum → felmérés → gyakorlás a módszerrel
        → próbadolgozat; később füzetfotó-feltöltés (adatvédelmi kiegészítés + feldolgozás
        utáni törlés kell).
      • Házifeladat-segítő (külön menü, később).
      • Napi 10 perces „küldetés” sorozattal (széria, mint Duolingo).
      • Új reklámvideó (lent) + heti 2–3 Facebook-poszt (szöveg + kép).
      • Spanyol oldal teljes átnézése (Claude), utána spanyol anyanyelvű szülő olvassa át.
      • Statisztika: robot-gyanús látogatók KÜLÖN soron (nem kiszűrve, csak látni).
      • Visszajelzés: szülői FB-csoportban 5 család egy hónap ingyen, cserébe vélemény.
      • Elutasítva (Sándor): főoldal átalakítása, demo-oldal hirdetésre.
- [ ] Új reklámvideó: a gyerek egyedül tanul, a szülő a kanapén megkapja: „Leila ma 15 percet
      tanult” (mozgáshoz Gemini/Veo kell, kevés kredit – egy jelenet).

## 🆕 2026-11-09 – NYITÓ FELADAT + FELADAT-TIPP (próbán BE, élesen KI)
- [ ] HIBA (éles, 8. o. matek „A függvény fogalmának előkészítése”): a nyitó táblaszöveg
      „nézd meg, melyik szám jön ki a gépből!” – és nem jött feladat. OK: a lecke nyitó
      szövegéből a <FELADAT>-ot a tisztítás kidobta, és nem mentettük. Javítva (app.py
      _nyito_feladat). Kapcsoló: NYITO_FELADAT (próbán magától BE; élesen Railway =1; 0 = ki).
- [ ] FELADAT-TIPP: ha a táblán függvénygép (fgep) van, a tanító megkapja a kipróbált
      segítési lépéseket (0-t, 1-et bedobni / két szomszédos szám → szorzó, aztán a
      hozzáadott szám), és nem kérdezi, hogy „melyik szám a szabály”. Kapcsoló: FELADAT_TIPP
      (próbán BE; élesen =1). Feladat-próba: „fgep”, spanyol oldalon is működik.
- [ ] Próbán ellenőrizni (Sándor), utána: git push origin proba:main + Railway
      NYITO_FELADAT=1 és FELADAT_TIPP=1.
- [ ] OKOSÍTÁS – KÖVETKEZŐ LÉPÉS: minden interaktív feladathoz ugyanilyen kézzel írt
      „ha elakad” tipp (venn, carroll, lift, recept, villam, szamolo…), egyesével, mindkét
      oldalra. Sándor: a magyarázat segítségkérésre nem elég egyértelmű (általános, régi
      példával magyaráz) – ez a lépés pont erre megy.
- [ ] Több interaktív feladat kell (Sándor, 2026-11-09) – lásd ESZKÖZÖK lista.
- [ ] 2026-11-09 este, Sándor próbája után (fix94, mind próbán BE, élesen KI):
      (1) ÁLFELMÉRÉS: új tantárgynál (szint 0, nem a szintfelmérő gombbal) a prompt „5 kérdéses
          szintfelmérőt + kész a felmérés” kért EGY üzenetben → a tanító kitalálta („Jöjjön az öt
          felmérőállítás… Elkészült a felmérés”), a gyerek semmit nem látott. Most: nincs felmérés
          a chatben, rögtön tanít, első válasznál <LEVEL:1>, pont nem jár érte. A gombos
          szintfelmérő a régi. Kapcsoló: NYITO_FELADAT.
      (2) Függvénygép szövegből: ha a tanító gépet ígér jelölő nélkül (5–8. o. matek), mi
          rakjuk ki (új szabállyal). Kapcsoló: NYITO_FELADAT.
      (3) „</assistant>final” a szöveg végén → kiszűrve (mindig).
      (4) KÉRDÉS-LEKTOR: a tanító utolsó kérdését kis modell nyelvtanilag javítja (pl. „Melyik
          adatot mutatja a csapadékot”). Csak magyar oldal, nem magyar/idegen nyelv órán.
          Kapcsoló: KERDES_LEKTOR (élesen =1). A lecke NYITÓ szövegén még nem fut.
      (5) Felsős választós feladat: a jó válasznál eltűnt a betű (zöld a zöldön) → fehér.
      (6) Railway naplóban keresni: [FELADAT-HIANY] – hol ígér feladatot a tanító, ami nem jön.
- [ ] ‼️ KÖVETKEZŐ (Sándor: „ezt csináljuk meg”): nehéz fogalmakhoz (exoterm, katalizátor)
      életszerű, pontos kép a táblára. TABLA_KEPEK kapcsoló van, de ki van kapcsolva (költség) –
      megnézni, mit tud, mennyibe kerül, mindkét oldalra.
- [x] fix95 (2026-11-09): a próbaoldal lecke-oldala 500-as hibát adott – Claude hibája: az új
      _nyito_feladat függvény a child_chat útvonal-jelölői (@app.route, @login_required) közé
      került. Javítva; az útvonal-térkép ellenőrizve (94 útvonal, mind a régi függvényen).
- [x] fix96: a KÉRDÉS-LEKTOR a spanyol oldalon is fut (nem spanyol nyelv órán, nem idegen nyelven).
- [ ] VIDEÓ (tutoria_reel_este.mp4, 2026-11-09) – Sándor javításai:
      (1) a kislány mellett ne gőzölögjön semmi; (2) az anyuka könyvet olvas, teával, a telefon
      felvillan → leteszi a könyvet, felveszi a telefont, mosolyog (a bögre végig a kezében) –
      video_kanape.py átírva: kep --emberek --ujra, aztán video --emberek. Az értesítés a
      telefon felvillanásához igazítva kerül rá.
      (3) a képernyős rész („számgép”, zavaros szöveg) helyett egyszerű, érthető lecke kell –
      Sándor küld képernyőképet (pl. 3–4. o. matek, interaktív feladattal).
- [ ] TANÍTÓ: a függvénygépet „számgépnek” nevezte, és zavarosan magyarázott (2 lépés egy
      mondatban). A tanító ne találjon ki szavakat: „függvénygép” / „gép”.
- [ ] Your Europe Advice: a hosszú szöveg túllépte a karakterkorlátot → rövid változat:
      jogi/yea_rovid.txt (1560 karakter, az autónomo kérdés kimaradt: az a gestoríáé).
      ✔ ELKÜLDVE 2026-11-09 (Sándor). Válasz kb. 1 héten belül az info@tutoriacademia.com
      címre. [ ] Válasz után: ÁSZF, adatvédelem, csomagoldal frissítése. [ ] Gestoríának a
      spanyol levél (jogi/jogi_kerdesek_2026-11-09.txt) még nincs elküldve.
- [ ] VIDEÓ v2 ROSSZ: az új jelenetben két bögre van az anyuka kezében (Claude átnézte, de nem
      vette észre). Sándor: a RÉGI, mobilozós kép a jó (konyha, minden) – azt kell javítani.
      v3: python video_kanape.py javit (a régi képet javítja: könyv, telefon mellette, gőz nincs
      a konyhában) → Claude MEGNÉZI → csak utána video --v3. Videónál Claude képkockánként
      ellenőrzi a kezeket/bögrét, mielőtt összerakja. (Eddig ~4 € ment el a videókra.)
      ✔ kanape_jelenet_v3.png kész és Claude átnézte (1 bögre, könyv, telefon a kanapén, a
      konyhában fedő a lábason, nincs gőz). A videó-prompt bal/jobb kéz nélkül (fix100).
- [x] HIRDETÉS LEÁLLÍTVA (Sándor, 2026-11-09): nem hozott regisztrációt, fogyott a pénz.
      Végleges adat (11.04–11.09, latogatottsag_2026-11-09_1936.json): 834 látogató, ebből 399
      a hirdetésből; 129 jutott a regisztrációs oldalra (99 a hirdetésből), 2 regisztrált
      (11.06 és 11.09; 1 a hirdetésből). A főoldalon a medián idő 6 mp, csak 32 görgetett.
- [x] VIDEÓ v3 KÉSZ (tutoria_reel_este_v3.mp4, 18 mp) – képkockánként ellenőrizve (1 bögre,
      nincs gőz a konyhában). Mehet Facebook-posztba (nem hirdetésbe).
      v4: Sándornak nem tetszett → a v3 a VÉGLEGES (tutoria_reel_este_v3.mp4).
      (Az összerakás ingyenes, csak a „video” parancs fogyaszt Gemini-pénzt.)
- [ ] fix102 (próbán ellenőrizni): (1) a lecke nyitó szövegében a feladat UTÁN írt szöveg
      kimarad („Ügyes voltál, ha ezek ismerősek voltak” – előre dicsért), és a tanító utasítást
      kap, hogy a feladat legyen a végén (NYITO_FELADAT). (2) választós feladatnál a jó
      válasz betűje helyén ✓ jelenik meg.
- [ ] Próbaoldal-ellenőrzés (Sándor, 11.09): a függvénygép megjelent ✔, a jó válasz betűje
      látszik ✔. A halmazok-lecke nyitásánál még álbemelegítés volt (fix102 javítja).
- [ ] Apróság: a tanító „A háztartási lámpákat így kapcsolják be” – helyesen „így kötik be”.
- [ ] fix103: (1) A ✓/konfetti/„Szuper” NEM jött, mert a pótolt választós kérdésnél (a tanár nem
      írt lehetőségeket, a program pótolta) a helyes válasz elveszett a keverésnél → most megmarad
      (POTLAS_JO, próbán BE). (2) Rossz válasz: piros keret; a felsős sötét lapon a „Ez nem jó…”
      szöveg eddig olvashatatlan volt → világos piros.
- [ ] fix104: kategóriába sorolós kérdésnél (pl. fizikai vagy kémiai változás) a tanító a
      csoport-felületet kapja ajánlásként 4–8 példával egy kérdés helyett (FELADAT_TIPP).
      A halmazállapot-felület (allapot, „vízforralás”) a kémián is elérhető, csak a tanító
      nem választotta – az a melegítést/hűtést mutatja, nem a fizikai/kémiai szétválogatást.
- [ ] fix105: (1) CSOPORT: egyetlen 24 betűnél hosszabb kártya az egész feladatot eldobta (ezért
      nem jött a „Válogasd szét…” feladat) → kártya 36 betűig, a túl hosszú kimarad, a feladat
      marad. (2) Ha a tanító szétválogatást ígér, de nem rakja ki → a program pótolja (kis modell,
      FELADAT_TIPP). A ✓ a böngészőben tesztelve működik – a próbaoldalon újra megnézni.
- [ ] FŐOLDALRA (main) MÉG NEM MENT (2026-11-10): minden a „Tanító: öt szabály” committól
      („Csomagok: percek az órák mellett” a main utolsó commitja). Kapcsoló nélkül élesbe megy:
      a/az javítás, „</assistant>final” szűrés, lecke-oldal 500 javítás, ✓ és piros keret,
      olvasható „Ez nem jó”, betűszín, csoport-kártya 36 betű, nyitó-üzenet utasítás, új
      elfogyott-levél, megújítási levél javítás. KAPCSOLÓVAL (élesen Railway =1 kell):
      NYITO_FELADAT, FELADAT_TIPP, POTLAS_JO, KERDES_LEKTOR, TANAR_TEMPO (TANAR_JAVITAS marad KI).
- [ ] ÁREMELÉS (Sándor kérdése, 2026-11-10): futó bérletnél az új ár csak ELŐZETES értesítés
      után (kb. 30 nappal előtte, e-mailben), a következő megújulástól érvényes, és a szülő
      addig díjmentesen lemondhatja. Ezt az ÁSZF-be be kell írni (most nincs benne), és a
      gestoríával/jogásszal megerősíteni. A megújítási levélben mindig a valódi levonás összege.
- [ ] FŐOLDAL-VIDEÓ (fix110): az 1. terv (kisfiú helyére) Sándornak nem tetszett. 2. terv: külön
      szakasz a „Mi a TutorIA?” alatt („Este 7. Te pihensz, ő tanul.” + 3 pont), static/video/.
      Próbaoldalon megnézni, utána élesre. SPANYOL oldalon NEM jelenik meg (magyar feliratú
      videó) – spanyol videó kell (összerakás ingyenes, spanyol lecke-képernyőkép kell hozzá).
      fix111 (Sándor próbája után): teljes képernyőn a videó nem lóg ki (object-fit: contain);
      a telefon a videó ELEJÉTŐL ott van a kanapén (sötét képernyővel, utána világít fel);
      „Heti összefoglaló” helyett „TutorIAcademia · Jelentés – Lili ma 2 leckét végzett el”,
      „E-mailben is látod” (nem csak hetente); háttérrajzok + zöld kör a szakaszban.
      2. lépés: „Nézz bele egy leckébe – regisztráció nélkül” gomb + mintalecke.
- [ ] STRIPE: a megújítási levélben a csomag NEVE és ÁRA most a csomagok.py listaárából jön –
      ha valaki régebbi (más) áron fizet, a levélbe a Stripe-előfizetés valódi összege kell.
- [ ] fix108: elfogyott-levélben a próba teljes kerete (120 perc) áll, nem a mért perc; a
      megújítási levélben TutorIAcademia név, „Ha folytatnád” (HU), „Si quieres seguir” (ES).
- [ ] fix107: „Elfogyott” levél új, vidám HTML formában (mint az emlékeztető): TutorIAcademia
      név, tanító-gif, egy gomb; próbánál nincs album/kártya említés; tesztidőszakban „Érdekel”
      (nem vásárlás). Próbaoldalon: Fiókom → „🧪 Elfogyott az ingyenes próba levél mintája”.
- [x] Feltöltés rendben (git log: minden commit fent van az origin/proba-n, a tanító már a
      csoport-ajánlás szerint beszélt). A régi kinézet oka: a lecke-oldal a feltöltés ELŐTT
      volt megnyitva – a tábla kinézete csak újratöltéskor (F5) frissül.
- [ ] ‼️ A fix102/fix103 chat.html változás (✓, piros keret, olvasható „Ez nem jó”) a 11.09-i
      képeken NEM látszik a próbaoldalon, pedig Sándor feltöltötte. Az app.py a gépen hibátlanul
      elindul (Claude kipróbálta). Ellenőrizni: git status / git log, és hogy a próbaoldal
      forrásában benne van-e: „a rossz válasz legyen PIROS keretes”.
- [ ] TANÍTÓ: ismeretlen szakszó magyarázat nélkül („két oldat összekeverése” – Sándor nem
      tudta, mi az oldat). Új szakszót mindig egy hétköznapi példával kell bevezetni.
- [ ] MINTALECKE regisztráció nélkül + VIDEÓ a főoldal tetején – Sándor: „nagyon profin,
      hiba nélkül”. Élesítés előtt képernyőképek, próbaoldal.
- [ ] ‼️ RENDSZERES HIBAKERESÉS (Sándor: „rengeteg a hiba, évekig javíthatnánk egyenként”):
      admin oldal, ami MINDEN elveszett/hiányzó feladatot, lektor-javítást, ígért-de-nem-jött
      feladatot naplóz okkal együtt (FELADAT ELVESZETT, FELADAT-HIANY, LEKTOR…) → kategóriánként
      javítunk (egy javítás = sok lecke). + tanar_teszt automatikus futás erre a naplóra.
- [ ] REGISZTRÁCIÓ (11.09 adat): 834 látogató → 2 regisztráció. Főoldal: medián 6 mp, 448-ból
      32 görgetett. Regisztrációs oldal: 174 látogató, medián 6 mp. Ötletek: kipróbálás
      regisztráció nélkül (1 rövid mintalecke), videó a főoldal tetején. Ismerős családot
      Sándor nem tud megkérni.
- [ ] TANÍTÓ: a táblára csak az utolsó kérdés kerül ki – legyen önmagában érthető (Sándor nem
      értette: „Melyik a helyes szó: monokultúra vagy fajgazdagság?” – mire?). Megoldást keresni.
      Helyette: ingyenes posztok + videó; új hirdetés csak jobb anyaggal és céllal.
- [ ] Videó/poszt: a zsiráf helyett más figura (Sándor). A „Fáradt este” téma jó →
      python video_kanape.py kep → kanape_jelenet.png legyen az 1. poszt képe is (poszt1.png
      helyett), utána python video_kanape.py video.

## 🔒 BIZTONSÁGI ÁTNÉZÉS (2026-11-10, fix113) – kapcsoló nélkül, azonnal él
JAVÍTVA:
- [x] ‼️ Üzemeltetői jog: az info@tutoriacademia.com (KAPCSOLAT_EMAIL) is admin volt, és a
      regisztráció nem kér e-mail-megerősítést → aki elsőként regisztrál vele, látta volna az összes
      család adatát és letölthette volna az adatbázist. Most: admin csak a két saját cím +
      ADMIN_EMAILEK; admin címmel nem lehet regisztrálni.
- [x] Próbálkozás-korlát kijátszható volt (a hamisítható X-Forwarded-For első elemét nézte) →
      valódi IP (Railway utolsó elem / Cloudflare CF-Connecting-IP). + fiókonként 10 rossz
      jelszó / 15 perc, bárhonnan.
- [x] Idegen gyerek adatai: /api/learning/early-placement/start (más gyerek szintjét nullázhatta),
      /api/learning/today, /weekly, és a hang-keret (más gyerek keretével lehetett hangot kérni)
      → csak a saját gyerek.
- [x] /test-openai bárki számára hívható volt (pénz + belső hibaüzenet) → csak üzemeltető.
- [x] Feltöltés-méret korlát nem volt → 20 MB.
- [x] Sándor kérése: üzemeltetői belépés ÚJ ESZKÖZRŐL → e-mail (idő, IP, ország, böngésző);
      rossz ADMIN_KOD → e-mail.
- [x] ADMIN_KOD (második kulcs): Railway változó; ha be van állítva, az admin oldalakhoz a jelszó
      mellé ez is kell (12 óráig érvényes). [ ] Sándor beállítja mindkét szolgáltatáson.
RENDBEN VOLT: jelszavak hash-elve; szülő csak saját gyereket éri el (get_child_by_id szülőre szűr);
admin oldalak mind ellenőrzöttek; mentés-letöltés névellenőrzéssel; süti HttpOnly+Secure+Lax;
SECRET_KEY figyelmeztetés; nincs kód-ba írt kulcs; /teszt/* csak próbaoldalon.
MÉG HÁTRA (később):
- [ ] Jelszó minimum 6 → 8 karakter (fordítás + register/reset sablon).
- [x] Sándor ellenőrizte a próbaoldalon (11.10): belépés, tanulás, hang, gyerekváltás, admin – jó.
- [ ] TANÍTÓ (angol, „My name is”): „Nem kell a saját nevedet megírnod” – fölösleges, zavaró
      mondat (a személyes-adat szabályt túl óvatosan alkalmazza). Megfigyelni, ismétlődik-e.
- [ ] Hirdetéshez/poszthoz a JAVÍTOTT videó: kinézet képek/facebook/hirdetes/tutoria_reel_este_v6.mp4
      (a v3-ban a telefon hirtelen jelent meg).
- [ ] E-mail-megerősítés regisztrációkor (a fizetés bekötése előtt).
- [ ] A próbálkozás-korlát munkásonként (4 gunicorn) számol → adatbázisba tenni.
- [ ] CSRF-token az űrlapokra (most a SameSite=Lax süti véd).
- [ ] AUTOMATIKUS AI-KÓDELLENŐRZÉS (fix115, Sándor: „most csináljuk”): .github/workflows/
      biztonsagi_ellenorzes.yml + eszkozok/biztonsagi_ellenorzes.py. Minden proba-push után a
      változást egy AI átnézi; komoly hibánál GitHub Issue → e-mail. Becslés: 1–3 cent/push.
      [ ] Sándor: GitHub → repo → Settings → Secrets and variables → Actions → New repository
      secret: OPENAI_API_KEY. Első futás után megnézni az Actions fülön.
- [ ] E-MAIL-MEGERŐSÍTÉS – KEMÉNY (fix116, Sándor döntése): regisztráció után levél gombbal (3 napig
      érvényes), belépni csak megerősítés után lehet; új levél kérhető; ugyanazzal a címmel újra
      regisztrálva a meg nem erősített fiók felülíródik (elgépelés / idegen regisztráció ellen);
      jelszó-visszaállítás e-mailből is megerősít; meg nem erősített címre emlékeztető nem megy.
      RÉGI fiókokat nem érinti. Kapcsoló: EMAIL_MEGEROSITES (próbán BE, élesen Railway =1).
      Teszt: vigh.sandor81+teszt1@gmail.com (ugyanabba a postafiókba érkezik).
      Mérés: a látogatottságban „megerositette” esemény – figyelni, hány regisztráló erősít meg.
- [ ] ÖTLET később: Google-belépés (egy kattintás, nem kell megerősítés).
- [ ] TTS: az angol leckében a „használt angol mondatot” MAGYAR szövegben az „angol” szót (?) az angol
      hang mondta – Sándor üzenete félbeszakadt, pontosítani.
- [x] Biztonsági riasztás (új eszköz, rossz ADMIN_KOD) az info@tutoriacademia.com címre megy (fix118);
      másik cím: RIASZTAS_EMAIL változó. Sándor: ellenőrizni, hogy az info@ leveleit olvassa.
- [x] GitHub OPENAI_API_KEY beállítva (Sándor, 11.10). [ ] A .github/workflows másolás + push.
- [ ] Gmail-szűrő a GitHub biztonsági leveleire (notifications@github.com, „Biztonsági ellenőrzés”)
      → csillag + címke – később, ha sok a levél.
- [x] Szülői jelentés-levél új kinézetben (fix119, level.py): TutorIAcademia fejléc, számdobozok,
      tantárgyi csíkok – zsiráf nélkül.
- [ ] KÖVETKEZŐ (Sándor kérte): mintalecke regisztráció nélkül; képek a nehéz fogalmakhoz.
- [ ] MINTALECKE – terv (fix121, mintalecke_terv2.png, fooldal_gomb_terv.png): főoldalon a „Hogyan
      működik?” helyén „▶ Nézz bele egy leckébe” gomb; évfolyamonként KÜLÖN (1–8, nem párosítva), és
      NEM mindig matek: 1. betűk (magyar), 2. összeadás, 3. évszakok (környezet), 4. szorzás,
      5. szófajok (magyar), 6. törtek, 7. halmazállapot (kémia), 8. függvénygép. Előre megírt
      szöveg (nincs AI-költség), valódi interaktív feladatok, a végén „Regisztrálok” gomb.
      Spanyol oldal: 1–6. Kérdés szövege: „Szerinted hány alma van összesen?”. Jóváhagyásra vár.
- [x] Blog link a láblécben (csak a magyar oldalon; a blog magyar) – fix121.
- [ ] FŐOLDAL DÖNTÉS (Sándor, 11.11): az „1. kép” változat – középen álló csempés kártya (2 oszlop,
      1–8. osztály), a buborék és az ABC kockák MARADNAK, a felső „AI-tanár · …” címke VÁLTOZATLAN, a
      keretes AI-sor NEM kell. Terv: outputs/fix122/index_csempe_abc_terv.html. Megépíteni a
      mintaleckékkel együtt, próbaoldalon.
- [x] MINTALECKE + CSEMPÉK megépítve (fix124): /minta (évfolyam-választó), /minta/<n> (3 lépés, előre megírt,
      AI nélkül), mintalecke.py (HU 1–8, ES 1–6, évfolyamonként más tárgy). Főoldal: középen csempés kártya
      (buborék + ABC marad). Kapcsoló: MINTALECKE (próbán BE, élesen Railway =1; 0 = régi főoldal).
      Mérés: látogatottság „#minta_hu_N”, „#minta_vege” események. [ ] Sándor: próbán végignézni mind a 8-at.
- [x] fix127 (11.11): főoldali kártya 1250–1499 px széles ablakban is 45 px-szel balrább (Sándor 150%-os
      nagyítással ezt látja); telefonos nézet nem változott.
- [x] fix128 (11.11): főoldal fejléce is a lebegő világos kapszula (mint a többi oldalon), gépen és telefonon;
      a telefonos lenyíló menü csempéi változatlanok. (A zöld 10.06 óta volt – a 11.06-i változat is zöld.)
      Visszaállítás: index.html „fix128” blokk törlése.
- [x] fix129 (11.11): mintalecke – almák tányéronként 2×2 rácsban (laptopon kicsúsztak a körből);
      béka (5. o. ige, HU+ES) és fazék (7. o. forrás) emoji helyett saját rajz: static/img/minta/*.svg
      („img:nev” a mintalecke.py-ban). Főoldali fejléc gépen fehérebb + keret (telefon változatlan).
- [x] fix130 (11.11): béka újrarajzolva (szemből, ugrál), fazék mozog (buborék, gőz, láng) – SVG-n belüli
      CSS-animáció, „kevesebb mozgás” beállításnál áll. Mintalecke kártyáján halvány konfetti háttér.
- [x] fix131 (11.11): főoldali fejléc – Sándor a C-t választotta (fehér + színes csík alul), csak gépen.
- [x] fix131: mind a 42 mintalecke-kép saját rajz (27 SVG, static/img/minta; mozognak, ahol van értelme).
      Javítva: ES 1. o. MESA-nál szék volt → asztal. Rajzoló: eszkozok/mintalecke_rajzok.py.
- [x] fix131: TANITO_PONTOS kapcsoló (próbán BE, élesen =1): „annyit sorolj, amennyit ígérsz” + helyes/elfogadható
      választ ne minősítsen rossznak (a spanyol teszt két hibafajtája). HU + ES. Csak a beírt chatnél.
      [ ] Sándor: próbán spanyol leckével kipróbálni; élesen Railway web: TANITO_PONTOS=1.
- [ ] Spanyol tanár-teszt 11.11 (3 óra, gpt-5.4-mini): 5 apró jelzés – „hi” vs „hello” fölösleges javítás,
      „három dolog” ígéret után négy pont (ugyanaz a hibafajta, mint magyarul), 2 kissé természetellenes
      spanyol mondat. Komoly tartalmi hiba nem volt. → döntés: a tanítói szabályokat finomítsuk-e.
- [x] Mintalecke képek: mind kész (fix131).
- [x] fix132 (11.11, Sándor visszajelzése): almás tányérok felülről (a körben), 7+6 és 50+20 és 6×5 képe
      pontosan a kérdés számaival, nyúl farka javítva, 2/7+3/7 egy 7 részes csíkkal, 1/2=2/4=3/6 három körrel,
      függvénygép: bemenet → gép → kimenet (1→3, 2→5, 3→7 váltakozva). „Fent és lent” szöveg helyett
      számláló/nevező (HU + ES).
- [x] fix133 (11.11): HU 1. o. mintalecke – HAL: a betűk összekeverve (L, H, A; eddig a szó sorrendjében álltak);
      SÜN: a kérdés „Hány betűből…” (Sándor: a gyereknek betű, a tanító szövegében marad a hang).
- [x] Sándor 11.11: mintaleckék rendben → élesre (proba:main; Railway web: MINTALECKE=1, TANITO_PONTOS=1).
- [x] fix134 (11.11): ES 1. o. mintalecke – OSO: betűk összekeverve (S, A, O).
- [x] fix135 (11.11): főoldal (HU+ES) – „A tanár kérdezi” buborék gépen keskenyebb és balrább, nem lóg a kisfiúra;
      tableten (761–1180 px) elrejtve, mert a csempés kártyára lógott. Telefon nem változott.
- [x] fix135: HU 1. o. ALMA – a kérdés „betűvel”, a válaszok keverve (labda, mókus, autó).
- [ ] Mintaleckék: sok lépésnél az első gomb a jó válasz (8. o.-ban mindhárom) → Sándor döntsön: keverjük-e mind.
- [ ] 2FA Railway: Sándor képernyőképén látszott a beállító kód → Cancel, újrakezdés (új kód), kézi bevitel.
- [x] fix134: AJANDEK_CIMEK Railway-változó (web): vesszővel elválasztott e-mailek → bő teszt keret, „elfogyott”
      levél nélkül. Clara családjának (Sándor kérése). Visszavonás: cím törlése.
- [x] fix134: kartya_muhely_es.html – spanyol kártyaműhely a 26 ES kártyával (kartyak_es.py), spanyol kártyaszövegek.
- [x] fix137–138 (11.11): kártyák helye – az 1. album marad: static/kartyak/hu/ és static/kartyak/es/
      (Sándor így akarja, semmit nem kell áthelyezni). Generált képek: kartya_kepek_uj/<oldal>/album1/.
      Új albumnál: kartyak.py ALBUM = "album2" → static/kartyak/<oldal>/album2/.
- [ ] Spanyol kártyák: 2 kész és bent (Ramón y Cajal, Mutis – static/kartyak/es). A többi 24:
      python kartya_kesz.py --es (kb. 6 cent/db) → kartya_kepek_uj/es/album1; keret a kartya_muhely_es.html-ben;
      minden fájl: static/kartyak/es/. Végül: spanyol album/tasakbontás a próbán.
- [x] fix138: Coubertin prompt – „olympic charter” helyett kézzel írt charta + „No Olympic rings, no logos”
      (az olimpiai karikák védjegy).
- [ ] ‼️ FELTÖLTÉSRE VÁR (Sándor 11.11 este: még NEM futott le, a kártyagenerálás miatt):
      (1) fejléc: git add static/css/style.css → proba → main;
      (2) kártyák: static/kartyak/es + kartyak.py kartyak_es.py kartya_kesz.py app.py TEENDOK.md.
- [ ] ‼️ SPANYOL KÉPEK – SZÜNET (Sándor 11.12: kb. 100 € ment el képekre, bevétel 0). Ne generáljunk többet, amíg nincs
      regisztráció. Az arcok hasonlósága csak valódi (közkincs) fénykép mintaként való megadásával javítható
      (kartya_kesz.py-ba bekötni, ha egyszer folytatjuk). Promptok javítva: Las Casas (borotvált, kopasz), Elcano és
      Alfonso X (nincs földgömb), Jorge Juan (paróka).
- [x] fix142: ÁSZF 6. pont (HU+ES): a kártyaképek MI-vel készült művészi illusztrációk, nem hiteles portrék; panasz
      esetén levesszük. Spanyol műhely kártyafelirata: „Ilustración creada con IA”. /admin/ (perjellel) is működik.
- [ ] Pinterest-kampány fut (11.11-ig 9,89 €, 97 kattintás, 0 regisztráció) → link a mintaleckére vagy szüneteltetés.
- [x] Látogatottság (11.12, 4 letöltés összevetve): a számok következetesek (a lezárt napok nem változnak).
- [ ] ‼️ FŐ SZIVÁRGÁS: 30 nap alatt 1123 látogató → 157 jutott el a regisztrációs oldalra → csak 2 küldte be.
      A regisztrációs oldal a gond (facebook: 100 a reg. oldalon, 1 regisztrált). Főoldalon a medián idő 5 mp.
      → Regisztráció egyszerűsítése (kevesebb mező, PIN később?) – Sándorral egyeztetni, mielőtt hozzányúlunk.
- [x] fix144 (11.12): főoldali „Kipróbálom ingyen” → mintalecke (/minta), alatta „Ingyenes, semmit nem kell megadni.
      Ha tetszik: 120 perc ingyen, bankkártya nélkül.” (HU+ES, csak MINTALECKE kapcsolóval). Regisztrációs űrlap marad
      (Sándor: két jelszó és PIN kell; a „120 perc ingyen” már ott van).
- [ ] Interaktív feladatok (Sándor 11.12): ~120 típus már van. Hiányok (javaslat, Sándor választ): kémiai egyenlet
      rendezése (7–8.), szövegértés kiemeléssel (minden évf., HU+ES), diktálás/dictado (helyesírás hanggal), tangram /
      alakzat-kirakó (1–4.), növény/sejt részeinek feliratozása (3–6.).
      Sándor 11.12: sorban mind; először 2) szövegértés, aztán 1) kémiai egyenlet. Szövegértés vázlat kész (válasz →
      bizonyító mondat kijelölése, HU+ES) – jóváhagyásra vár, utána bekötés a tanítóba („szovegertes” típus).
- [x] fix147 (11.12): mintalecke vége – B+C ötvözve: lépések (✓ Mintalecke · 2 Fiók · 3 Első igazi óra) +
      lila „🎁 120 tanulási perc ajándékba … Kérem →” gomb (HU+ES), a külön „Bankkártya nem kell” sor törölve.
- [x] fix146 (11.12): SPANYOL ALBUM – album.html eddig magyar tantárgylistával csoportosított, ezért a spanyol
      album üres volt (csak borító+lista). Most a spanyol tantárgyak a kártyákból jönnek, minden felirat
      spanyolul (Álbum, Índice, Pegadas, EL DATO, HABILIDAD, SABER…). Magyar album változatlan (ellenőrizve).
- [x] fix149 (11.12): ÚJ FELADATOK a tanítóban – Sándor teszteli a próbán:
      • „szövegértés, bizonyító mondat” (szovegertes) – minden tárgy, 1–8., HU + ES; ES név: „comprensión lectora, frase-prueba”.
      • „kémiai egyenlet rendezése” (egyenlet) – kémia 7–8., csak HU; a megoldást a szerver számolja (1–9 együttható).
      Új címke: "kemia" (_dm_cimkek). Teszt helyben: Feladat-próbában mindkettő megjelenik, működik.
- [x] fix149: spanyol album képei – a fájlok évfolyamszám nélkül vannak (medio_cajal.png), ezért kartyak_es.py
      "kep" és a kártyaműhely fájlnevei is szám nélkül. Új generált képeknél: kartya_kepek_uj/es/album1/ név szám nélkül.
- [ ] Következő feladatok sorban: 3) diktálás/dictado, 4) tangram, 5) növény/sejt feliratozás.
- [x] fix150 (11.12): spanyol főoldal – spanyol kártyák (doboz, 4. lépés, kártyasor), spanyol albumborító és belső
      albumoldal (static/bemutato/*_es.jpg, es_*.jpg).
- [x] fix151 (11.12): HIBA – a spanyol leckében ÍROTT módban az AI-tájékoztató („Szia! Mesterséges intelligencia…”),
      a kabala dicsérete és pár feladat-tipp MAGYARUL jelent meg (a chat-frame mező csak hangos módban volt).
      Javítva (chat.html). Spanyol telefonos képernyőképek a főoldalra (app_*_es.jpg).
- [x] fix152 (SEO): title HU+ES a főoldalon; JSON-LD a főoldalon (EducationalOrganization + WebSite +
      SoftwareApplication); BlogPosting a /blog oldalon és a cikken. Search Console bekötve (Cloudflare),
      sitemap beküldve. Még nyitott: spanyol útvonalnevek (/es/csomagok → /es/precios),
      GYIK FAQPage csak a valódi GYIK-szövegből generálva.
- [ ] ‼️ JOGI – „Az Ön Európája” válasz (2026-11-15) alapján, a fizetés bekötése ELŐTT:
      • ÁFA: elektronikus szolgáltatás (automatizált távoktatás). Uniós határon átnyúló B2C eladás összesen
        10 000 € (áfa nélkül, naptári év) alatt: spanyol IVA; fölötte a vevő országáé (HU: magyar áfa) – OSS
        (spanyol AEAT) vagy NAV-regisztráció. Spanyol vevőnek mindig spanyol IVA. Számla minden eladásról.
      • ELÁLLÁS: a fizetésnél 3 dolog kell: (1) pipa: kéri, hogy azonnal induljon, (2) pipa: tudomásul veszi az
        elállási jog elvesztését/korlátozását, (3) visszaigazoló e-mail erről. FIGYELEM: a TutorIA inkább
        „digitális SZOLGÁLTATÁS” (előfizetés), ott elálláskor az addig használt rész arányos díja jár, a jog nem
        szűnik meg teljesen – jogász/gestoría döntsön. Új EU-szabály (2023/2673 irányelv, 2026-06-19-től):
        online szerződésnél kötelező „elállás itt” gomb – ellenőrizni.
      • GDPR korhatár: HU 16, ES 14 – nálunk a szülő hozza létre a fiókot és mindig ő járul hozzá → rendben
        (nyilvántartás frissítve 11.16).
      • Emlékeztető levél (7./21. nap): jogos érdek + LIA kész (jogi/LIA_emlekezteto_level.md); reklám NEM
        kerülhet bele.
- [ ] GEO (AI-keresők ajánlása): tényszerű, jól tagolt oldalak és blog, JSON-LD (kész), említés más oldalakon
      (iskolai/szülői fórumok, katalógusok). Később.
- [x] fix153 (spanyol blog): a magyar cikk ES változata (1.º–6.º Primaria, LOMLOE); title/meta/BlogPosting
      inLanguage "es"; lábléc Blog link ES-en is; Pruébalo gratis → /es/minta; sitemap + hreflang
      (HU ↔ ES cikk) már a KERESO_OLDALAK-ból jön.
- [ ] Szövegértés: évfolyamonként a NAT / LOMLOE olvasási szintje szerint (1–2.: 3–5 mondat; 3–4.: 1 bekezdés;
      5–6.: ismeretterjesztő szöveg; 7–8.: tantárgyi forrásszöveg, következtetés). Bekötés a tanítóba ezután.
- [ ] Spanyol kártyák: 14 kész a static/kartyak/es-ben; 8 fájlt át kell nevezni (_2, _3, (1), másolata) – parancs megadva.
      Sorolla új képén a vásznon halvány „Fig. 22” felirat.
- [ ] Spanyol képek ÚJRA átnézve (Claude, 11.11, Sándor jelezte, hogy az első átnézés felületes volt):
      ÚJRA kell 10: Goya, Sorolla, Albéniz (fix140) + Torres Quevedo (szakáll hiányzott), Peral (makett + modern
      tengeralattjáró), Las Casas (rossz szerzetesi ruha – domonkos: fehér + fekete köpeny), Elcano (távcső – akkor
      még nem volt), Lorca (rossz kéz, furcsa bábu), Ibn Firnas (szárny szoknyaként), Azarquiel (gótikus templom
      Toledóban 1087 előtt). Promptok javítva (fix141). Rendben: a többi 14 + Cajal, Mutis.
- [x] fix138: egységes fejléc GÉPEN minden oldalon (fehér kapszula + színes csík, narancs Regisztráció) –
      style.css végén; gyerek-munkamenet és telefon nem változik.
- [ ] Kártyapontok (Sándor kérdése): most a ritkasághoz kötött – ritka 300–360, nagyon ritka 400–450,
      legendás 470–480 (+ magyar gyakori 200–210). Sándor 11.11: a KÖVETKEZŐ ALBUMBAN húzzuk szét
      (pl. 150–500, a legnagyobbak a legtöbbet); az 1. album marad így.
- [ ] Hirdetés link: https://tutoriacademia.com/minta?utm_source=facebook&utm_campaign=mintalecke
      (spanyol: https://tutoriacademia.com/es/minta?utm_source=facebook&utm_campaign=muestra).
- [ ] Spanyol tanár-teszt Sándor gépén: python tanar_teszt.py --oldal es --gyors (jelentés magyarul, ~1 €).
- [x] fix128: gyerekbarát adatvédelmi összefoglaló (GDPR 12. cikk) – adatvedelem.html 8. pont, HU + ES.
- [ ] ‼️ ADMIN_KOD beállítása: Railway → web szolgáltatás → Variables → ADMIN_KOD (próbán is). Sándor.
- [ ] Mintalecke élesítése: Sándor átnézi a 8 HU leckét → Railway web: MINTALECKE=1.
      Spanyol oldal 11.11: a nyilvános oldalak és mind a 6 ES mintalecke gépi ellenőrzéssel magyar szó nélkül.
- [ ] JOGI KÉRDÉSEK – GYEREKEK (Sándor, 11.11; a gestoríának / jogásznak, a fizetés előtt):
      (1) DPIA – utánanézve: az AEPD listája szerint 2+ kritérium esetén kell; nálunk 3 (14 év alatti
          gyerek, MI, értékelés) → KÖTELEZŐ. Vázlat kész: jogi/DPIA_adatvedelmi_hatasvizsgalat_vazlat.md
          (Sándor aláírta 11.11. Kész: szűrő az OpenAI előtt [már megvolt], Railway régió [a tájékoztató
          US West-et ír], nyilvántartás frissítve 11.11, gyerekbarát összefoglaló fix128. Még: ADMIN_KOD + 2FA).
      (2) AI-rendelet III. melléklet 3(b): a szöveg szerint „oktatási és szakképző INTÉZMÉNYEKBEN” használt,
          tanulási eredményt értékelő MI magas kockázatú. Otthoni, szülő által választott gyakorlásra a
          szövegből nem következik – de ha iskolának adnánk el, az már az lehet. Jogásszal megerősíteni.
      (3) Gyerekbarát nyelvű adatvédelmi összefoglaló (GDPR 12. cikk) – rövid változat a gyereknek.
      Rendben van: szülő regisztrál + hozzájárul (GDPR 8. cikk; HU 16, ES 14 év), e-mail-megerősítés,
      a mintalecke nem gyűjt adatot. COPPA (USA) nem vonatkozik ránk.
- [ ] ‼️ TELJES JOGI ELLENŐRZŐLISTA (Sándor: „ha nem kérdezek rá, magadtól nem mondod?”): egy listában
      végigmenni GDPR, AI-rendelet, fogyasztóvédelem (EU/HU/ES), LSSI, adó, gyerekvédelem pontjain, mi kész,
      mi hiányzik – a fizetés bekötése ELŐTT.
- [x] fix126: mintalecke – felül magyarázó sáv („3 perces bemutató… a valódi leckében a tanító beszélget…”),
      a 3. csík is zöld lesz a jó válasz után; főoldal – széles képernyőn a csempés kártya kicsit balra.
- [ ] Facebook-hozzászólás (Ágnes, AI-ellenes): ne rejtsük el; udvarias, egyetértő válasz, név nélkül.
- [x] Videó „Este 7.” helyett „Hosszú nap volt.” (v7), főoldali cím: „Te pihensz, ő tanul.” (fix120).
      Hirdetéshez: kinézet képek/facebook/hirdetes/tutoria_reel_este_v7.mp4.
- [ ] ‼️ ADMIN_KOD beállítása a Railway-en (web + próba) – Sándor: ne felejtsük el.
- [ ] KÉT NYELV EGY FIÓKKAL: most egy fiók egy tantervre fizethet elő (csomag_tanterv: HU vagy ES), a
      másik oldalra fizetés után nem léphet át. Aki mindkettőt akarja: két fiók kell. Döntés a
      fizetés bekötésekor: kombinált bérlet (pl. kedvezménnyel) vagy két külön fiók.
- [ ] 11.11: Sándor nézze meg az új szülői jelentés levelet (Claude emlékeztet). Arcos: szél, lehet net nélkül.
- [ ] ‼️ KÉTLÉPCSŐS AZONOSÍTÁS (2FA) bekapcsolása: Railway, GitHub, Gmail, Cloudflare, OpenAI,
      Resend, Meta – ha ezek valamelyikét feltörik, minden kód és adat veszélyben van.

## ⚠️ SÜRGŐS – SORRENDBEN (2026-11-06, Sándor kérte a rangsort)

1. ✔ RÉSZBEN KÉSZ (fix77): a szerver is számol (database.szerver_lepes: chat üzenet és
   feladat-ellenőrzés között legfeljebb 3 perc), az elszámolt perc ennél nem lehet kevesebb.
   Hátra: élesben összevetni a böngésző és a szerver percét (admin), és ha nagy az eltérés,
   további lépéseket bekötni (teszt-válaszok, widgetek). Ismert kiskapu: aki mindig kivárja a
   3 percet, annak az a szünet nem számít – Sándor: később nézzük meg, kihasználják-e.
   (Eredeti leírás:) **Az időmérés a szerveren is** (fizetés ELŐTT kötelező). Most a böngésző méri és küldi
   a perceket → kijátszható, és vitában nincs mire hivatkozni. Terv: a szerver is számol a
   gyerek tényleges lépéseiből (chat üzenet, feladat-ellenőrzés, felolvasás), két lépés
   között legfeljebb 3 percet számítva; elszámolásnál a kettő közül a nagyobb, de soha nem
   több, mint az óra kezdete óta eltelt idő. Naplózva → panasznál megmutatható, mi történt.
2. ✔ KÉSZ (fix78): az STT is 429-et ad, ha elfogyott; hangos módból 3,5 mp után írásosra vált,
   a hangos mód gombja eltűnik. Próbaoldalon „🧪 Hangkeret: VAN/ELFOGYOTT” gomb a teszthez.
   Kiegészítés: az értesítés felső sávban jön (nem a lecke szövegének helyén), a 🔊 gombok
   a feladatok rövid hangjai (≤200 karakter, pl. „Meghallgatom”) mindig mennek.
   fix79: a 🔊 NEM tűnik el: a már felolvasott üzenet (gyorstár, ingyen) újra szól, és az
   elfogyás pillanatában soron lévő üzenet még egyszer elhangzik (session „hang_kegy”).
   Leírva: ÁSZF 7. pont (HU+ES) és a sárga sávban.
   Fizetés után a hang AZONNAL visszajön: a program minden kérésnél a szülő aktuális
   csomagját nézi (a Stripe-webhook átírja a csomagot → a következő oldalbetöltéstől él).
   (Eredeti:) **Beszédfelismerés (STT) is álljon le**, ha a hangos idő elfogyott (most csak a
   felolvasás áll le; a hangköltség kb. fele az STT).
3. ✔ NEM KELL (ellenőrizve 2026-11-06): hang.py-ban MAX_KARAKTER = MAX_KARAKTER_HANG = 3000,
   tehát a felolvasás mindkét módban ugyanannyit olvas fel – nincs rövidítés-különbség.
   (Eredeti:) **Hangos módban a teljes választ olvassa fel**: a felolvasás nem küldi a mode=voice-ot,
   ezért a szerver a rövidített változatot olvassa fel. (Hangmód – Sándor engedélyével.)
4. **Elsősök (≤7 év, csak hangos profil) az ingyenes próbában**: 30 hangos perc után nekik
   is írásban folytatódik (Sándor döntése: kivétel nincs, mert az életkort a szülő írja be).
   Mivel még nem olvasnak, a szülőnek ezt előre jelezni kell (pl. a gyerek felvételekor).
5. **Hirdetés – adat 11.06. 20:14-ig**: a regisztrációra küldő új hirdetés után a hirdetésből
   jöttek közül 37 jutott a regisztrációs oldalra (reggel még 2), de a medián idő ott 2 mp,
   és senki nem kezdte el kitölteni → továbbra is főleg véletlen/érdektelen kattintás vagy a
   Facebook előtöltése. A/B (fb_regisztracio / fb_fooldal) NEM indult el: a linkben még a
   régi utm_source=facebook_hirdetes van. Meta-ban nézni: elhelyezések, „céloldal-megtekintés”.
   (Eredeti:) **Hirdetés**: új kampány kézi elhelyezéssel (FB + IG hírfolyam/Reels), Audience Network
   nélkül, link a regisztrációra. Adat 11.04–06: a főoldalon 183 látogatóból csak 12
   görgetett egyáltalán, medián 7 mp → nagyrészt véletlen/érdektelen kattintás.
6. **ÁSZF**: fizetés előtt a teljes bérlet-szöveg ügyvéddel/gestoríával átnézetve.
7. **Elsősök szüleinek jelzés** (alacsony): a csomagoldalon már ott van „30 perc hangos,
   utána írásban” – jogilag ez elég; a gyerek felvételekor egy mondat csak kényelmi.
8. **Éves ár**: most nincs. Az első fizetős hónapok adatai után döntünk.
9. **‼️ STRIPE / PAYPAL BEKÖTÉSEKOR – NE FELEJTSD, NAGYON FONTOS (Sándor kérte, 2026-11-06):**
   - A fizetés (webhook) állítsa a szülő `csomag`, `csomag_kezdet`, `csomag_lejar` mezőjét →
     a hang és a keret a következő oldalbetöltéstől azonnal él. Lemondáskor/elmaradt fizetésnél
     csak a `csomag_lejar` kerüljön a kifizetett időszak végére (a megmaradt órák a saját
     3 hónapjukig élnek – _berlet_keret fizetett_ig).
   - Csomagváltáskor a `csomag_kezdet` újraindítása (a program a MOSTANI csomag havi keretével
     számol visszamenőleg is).
   - A hangos idő próbaoldali tesztkapcsolója (session „teszt_hang_elfogyott”) csak a
     próbaoldalon él – élesben nincs.
   - ELFELEJTETT / SIKERTELEN FIZETÉS: a bérlet havonta AUTOMATIKUSAN levonódik (az ÁSZF ezt
     írja). Ha a levonás nem sikerül (lejárt kártya stb.): a Stripe pár napig újrapróbálja, és
     mi levelet küldünk („nem sikerült a levonás – frissítsd a kártyát: link”). Ha végleg nem
     sikerül: csomag_lejar = a kifizetett időszak vége (a megmaradt órák a saját 3 hónapjukig
     élnek).
   - LEMONDÁS GOMB a Fiókom oldalon („Bérlet lemondása”, egy kattintás, megerősítés nélkül
     vagy egy „Biztos?” lépéssel) – Ley 10/2025: akadály nélkül. Stripe: cancel_at_period_end.
   - FIÓK TÖRLÉSE = AZ ELŐFIZETÉS FELMONDÁSA IS (ÁSZF 9. pont, fix85): a törlés hívja meg a Stripe
     előfizetés azonnali leállítását; a törlő oldal ELŐTTE írja ki: „Még X óra van a bérletben –
     a törléssel ezek elvesznek.”
   - ✔ ELŐKÉSZÍTVE (fix84): _megujitas_kor + _megujitas_level – 16 nappal a fordulónap előtt,
     fordulónként egyszer (parents.megujitas_ertesitve), csak ha FIZETES_ELERHETO. ÁSZF 7. pontba
     beírva (HU+ES). HÁTRA a Stripe-nál: a „MEGÚJÍTÁS LEMONDÁSA” gomb most a Fiókom oldalra
     visz → ott kell egy egykattintásos lemondás (Stripe Customer Portal vagy saját gomb),
     ami a csomag_lejar-t a fordulónapra állítja. Próbaoldalon: „🧪 Megújítási értesítő mintája”.
   - ‼️ KÖTELEZŐ ÉRTESÍTÉS MINDEN LEVONÁS ELŐTT: spanyol Ley 10/2025 (Ley de servicios de
     atención a la clientela, BOE 2025.12.27; TRLGDCU 97.1 p) módosítása): az automatikusan
     megújuló szerződésnél a megújítási díj levonása előtt LEGALÁBB 15 NAPPAL értesíteni kell,
     és le kell írni, mi történik, ha nem mondja le. A forrás nem tesz különbséget havi és éves
     között → HAVONTA, minden levonás előtt ≥15 nappal levél (pl. a 14. napon a fordulónap
     előtt 16 nappal): összeg, levonás napja, egykattintásos lemondás linkje. Lemondás:
     egyszerű, akadály nélkül (Fiókom → egy gomb). ÁSZF 7. pontba beírni. Forrás:
     dsca.gob.es „Nota informativa sobre nueva regulación de suscripciones”.
     Fizetés indulása előtt gestoríával megerősíteni.
   - Szövegek: ÁSZF 7. pont (fizetés, megújulás, lemondás, számla), Adatvédelmi tájékoztató
     5. pont (fizetési szolgáltató neve, számlázási adatok, megőrzés), adatkezelési
     nyilvántartás 5. pont kitöltése, csomagoldalon a „Tervezett ár” jelölés levétele,
     FIZETES_ELERHETO=1.
10. ✔ KÉSZ (fix81): _emlekezteto_kor – 7 nap után 1., 21 nap után (és ≥14 nappal az 1. után)
    2. levél, több nincs; újra tanulás nullázza; 90 napnál régebben tétlennek nem; leiratkozott,
    admin, elfogyott próba, lejárt bérlet: nem. Napközben, óránként egyszer (háttérszál,
    MENTES_DIR kell). Visszaállás: EMLEKEZTETO=0. Adatvédelmi tájékoztató 3. pont kiegészítve.
    fix84: a táblán felirat (HU „Várlak!”, ES „¡Te espero!”) – static/email/tanito_hu.gif és
    tanito_es.gif; a régi tanito.gif már nem kell (törölhető). Gyerek neve mező: „Keresztnév
    vagy becenév” (adattakarékosság, egyezik az adatvédelmi tájékoztatóval).
    fix83: Duolingo-szerű HTML levél (nagy zöld gomb, mozgó zsiráf-tanító GIF:
    static/email/tanito.gif ~850 KB a veo_nyito_1.mp4-ből, narancs doboz a maradék idővel),
    a tanító szól; név csak ha a szülő egy szót írt be; gyerek nélkül „Már csak egy lépés”;
    List-Unsubscribe fejléc (Gmail „Leiratkozás” gomb), egykattintásos POST is.
    fix82: új, barátságosabb szöveg (gyerek keresztneve, napok száma, „10 perc is sokat
    számít”), a próbaoldali tesztlevél linkjei a próbaoldalra mutatnak.
    Külön leiratkozás (fix81b): az emlékeztető saját linkje csak az emlékeztetőt kapcsolja ki
    (parents.emlekezteto_ki), a heti jelentés marad; Fiókom oldalon vissza-/kikapcsolható.
    A levél a csomaghoz igazodik: próbánál nincs kártya/album, a maradék ingyenes perc;
    bérletnél a maradék óra + „3 hónapig érvényes”. Próbaoldalon: „🧪 Emlékeztető levél
    küldése most nekem” gomb a Fiókom oldalon.
    (Eredeti:) **„Rég jártál itt” emlékeztető e-mail** (Sándor ötlete, 2026-11-06) – JAVASLAT: 7 nap
    tétlenség után egy levél, 21 nap után még egy, utána nincs több. Csak ha a szülő nem
    iratkozott le (a meglévő ertesites/leiratkozás rendszert használja), minden levélben
    leiratkozó link. Fizetőknek is (a kifizetett órák elvesznének). Szöveg kell az Adatvédelmi
    tájékoztatóba (cél: emlékeztető a szolgáltatás használatára; jogalap: jogos érdek,
    leiratkozható). Sándor döntésére vár.
11. **Látogatottság-letöltés**: a fájlnévben már óra-perc is van (fix80), nem írja felül egymást.


## Azonnal (a poszt már kiment, a cím publikus)

- [x] **Robot elleni védelem.** (KÉSZ – 2026-11-03 ellenőrizve: csapda-mező + időbélyeg + regisztráció 5/óra, belépés 10/10 perc, elfelejtett jelszó 5/óra.) Percenkénti korlát a regisztrációra, a
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

- [x] fix152: title HU+ES; JSON-LD főoldal; BlogPosting (/blog + cikk).
      Search Console bekötve (Cloudflare), sitemap beküldve.
- [ ] **Hreflang sehol nincs kint.** A magyar főoldalon, a spanyol
      főoldalon és a blogcikken sem találtam. A sitemapban sincsenek
      `xhtml:link` sorok. Enélkül a Google két különálló, azonos tartalmú
      oldalnak látja a magyart és a spanyolt.
- [ ] **A blogra semmi nem linkel.** Se a főoldalról, se a láblécből.
      Csak a sitemapból érhető el, azt meg nem ember olvassa.
- [ ] A `/login` és a `/register` fölösleges a sitemapban.
- [ ] A spanyol oldalak magyar útvonalneveket használnak (`/es/csomagok`,
      `/es/gyik`). Spanyol keresésre rossz; később `/es/precios`,
      `/es/preguntas`. (fix152: még nyitott)
- [x] Spanyol blog (fix153).
- [ ] GYIK FAQPage csak a valódi GYIK-szövegből generálva.

## Tartalom

- [ ] **Spanyol album.** A 26 kártya adatai kész (kartyak_es.py), a műhely is (kartya_muhely_es.html, 11.11);
      a képek hiányoznak.
- [ ] **Hiányzó kártyaképek: 52-ből 42.** Addig is kell egy szép
      helyőrző, hogy a hiányzó kép ne tűnjön hibának.

## Növekedéskor

- [ ] **Resend fizetős csomag.** Az ingyenes keret havi 3000 levél;
      kb. 100 családnál fut ki (heti + napi jelentések).
- [ ] **Postgres slow query log** bekapcsolása.
- [ ] Az `info@tutoriacademia.com` postafiók ellenőrzése: tényleg
      megérkezik-e oda a levél (az Azure válasza is oda jön).

## ⏰ FIGYELMEZTETÉSEK — mikor mit kell elővenni (Claude minden munkamenet elején nézze át)

- **Amikor a fizetésen kezdünk dolgozni:** autónomo (vida laboral → tarifa
  plana), ÁSZF fizetős változat, Stripe vagy Paddle döntés, a nyilvántartás
  5. pontja (fizetés), számlázás. Mind lent, a „Fizetés bekötése ELŐTT” részben.
- **FONTOS, MINDENKÉPP MEGCSINÁLNI (Sándor kérte, 2026-11-05), a fizetés
  ELŐTT:** Your Europe Advice kérdés (autónomo, ÁFA, magyar vevők több
  országból, ÁSZF). Claude írja meg magyarul, Sándor küldi be.
  ✔ MEGÍRVA (2026-11-09): jogi/jogi_kerdesek_2026-11-09.txt (magyar → Your Europe
  Advice, spanyol → gestoría). [ ] Sándor elküldi. [ ] Válasz után: ÁSZF, adatvédelem,
  csomagoldal, költségszámítás és ez a lista frissítése a válasz alapján.
- **Ha az autónomo vagy az ÁFA kérdés nem tisztázódik:** Your Europe Advice
  (europa.eu/youreurope/advice) – az EU ingyenes jogi tanácsadása. Űrlapon
  leírod a kérdést, egy héten belül MAGYARUL válaszol egy jogász. Claude
  megírja a kérdést.
- **Ha a nem spanyol EU-s vevőktől jövő éves bevétel 8 000 € fölé megy:** OSS
  vagy Paddle (10 000 €-nál kötelező a vevő országának ÁFÁ-ja).
- **Ha új szolgáltatót kötünk be (pl. Clarity, Stripe):** DPA + adatvédelmi
  oldal + jogi/adatkezelesi_nyilvantartas.md frissítése.
- **Ha adatvédelmi gond van (rossz helyre ment adat, feltörés):** azonnal
  Claude-nak szólni – 72 órán belül be kell jelenteni az AEPD-nek.
- **Railway régió váltásakor:** RAILWAY_REGIO változó + nyilvántartás átírása.

- [x] 2026-11-05 SOS: az élő oldal „szétesett” (óriási fekete ikonok) – az új base.html
      ment ki, de a böngésző/Cloudflare a régi style.css-t adta. Javítva: ?v=<verzió> a
      CSS/JS címeken (app.py _STATIK_V), és az ikonoknak saját méret is van CSS nélkül.

## Jogi / GDPR (2026-11-04 átnézve)

- [x] OpenAI DPA: automatikusan része a szerződésnek (OpenAI Ireland). PDF-mentés
      nem kötelező (Claude nem éri el az openai.com-ot, kihagytuk).
- [x] Látogatottság-mérés: AEPD közönségmérési kivételen belül. 13 hónapos
      automatikus törlés + nyilvános leiratkozás (/ne-merj) kész.
- [x] Adatkezelési nyilvántartás (30. cikk): jogi/adatkezelesi_nyilvantartas.md.
      Railway régiót beírni (Railway → szolgáltatás → Settings → Region);
      fizetés bekötésekor az 5. pontot kitölteni (Claude emlékeztet).
- [ ] VÉDELEM ÁTNÉZÉSE (Sándor: „nagyon fontos”, 2026-11-05) – a számolás és a
      főoldal után: (1) adatbázis-mentés: Railway Postgres → Backups, napi
      automatikus mentés be van-e kapcsolva; (2) oldalvédelem: belépés/regisztráció
      korlát, admin kapu, biztonsági fejlécek, jelszó-hash, titkos kulcsok;
      (3) jogi védelem: ami a FIGYELMEZTETÉSEK részben van.
- [ ] jogi/incidensek.md (üres napló) – adatvédelmi incidens esetén 72 óra.
- [x] Csomagok oldal: a gombok kattintása csomagonként látszik a mérésben
      (data-mer). Bejelentkezett szülőnél az „Érdekel” gomb eddig is mentette.
- [ ] FB hirdetés: elhelyezésnél az Audience Network kikapcsolása (sok
      véletlen kattintás: 61 látogató 1,94 €-ért, 6 mp az oldalon).
      Az „ajánlott beállításos” kampányban ZÁROLT (Meta, 2026-11-05). Előbb
      megnézni: Kimutatás → Bontás → Kézbesítés → Elhelyezés – honnan jött a
      kattintás. Ha főleg Audience Network: új hirdetéssorozat kézi
      elhelyezéssel (Facebook + Instagram), a régit kikapcsolni.
- [ ] SÜRGŐS – REGISZTRÁCIÓS ŰRLAP (2026-11-05 mérés): 3 látogató megnyitotta,
      44 mp-ig ott volt, végig legörgetett, de SENKI nem küldte be. Átnézni az
      űrlapot telefonon: hány mező, mi kötelező, érthető-e, van-e hiba
      (admin/latogatottsag → „hibák” rész), ijesztő-e valami (jelszó, PIN, gyerek adatai).
- [ ] FB hirdetés: fusson tovább kis költséggel; ha az űrlap javítva van, új
      hirdetéssorozat kézi elhelyezéssel (Audience Network nélkül).
- [ ] FEJLÉC EGY SORBAN + telefonon ☰ menü (2026-11-05): „A” változat (alulról
      felcsúszó lap, színes csempék) a gépen, PRÓBAOLDALON nézzük meg. Ha nem
      tetszik: a krémszínű lista-változat mentve: „Claude outputs/fejlec_lista_valtozat/”
      (base.html, style.css) – Claude visszateszi. Képen megmutatva még: „B” sötét
      kártya felül, „C” állandó alsó sáv, „D” kabala (integető fiú) a lapon.
      A CSS-ük: „Claude outputs/fejlec_valtozatok.css”. Sándor dönt.
- [ ] Szülői oldalak (laptop): a zöld fejléc összefolyik a zöld sávval → javaslat:
      sötétebb fejléc (#0E4A38) azokon az oldalakon, ahol zöld sáv van alatta.
      Képen megmutatva, jóváhagyásra vár (ugyanabban a CSS-fájlban). További 3 ötlet
      képen (2026-11-05): krém fejléc / egybeolvasztva vékony csíkkal / zöld fejléc + világos sáv.
- [ ] ÖTLET – ÉLŐ KABALA A MENÜBEN (Sándor kérte, 2026-11-05): a figura a lap
      tetején besétál, beszél (száj mozog, buborék) és gesztikulál, de ne legyen
      „AI-s”. Terv: az integető fiú/lány képét részekre vágni (fej, kar, test,
      láb – avatar_darabolo.py), CSS-animáció: séta, karmozdulat, 2–3 szájállás.
      Csak megnyitáskor fusson ~2–3 mp-ig, utána álljon meg; „mozgás csökkentése”
      beállításnál ne mozogjon. Előbb egy rövid próbavideó, csak utána beépítés.
      2026-11-05: BEÉPÍTVE (base.html + style.css vége + static/kabala/menu/*.webp,
      6 rész, ~60 KB, csak telefonon töltődik). Besétál, köszön, integet, beszél,
      pislog, a végén fejet vakar és gondolkodik. Próbaoldalon nézni.
      DÖNTÉS (2026-11-05): „A” – alulról felcsúszó lap, KABALA NÉLKÜL (kézzel jobban
      elérhető). B, C, kabala kivéve a kódból. A kabala képei megmaradtak
      (static/kabala/menu/, „Claude outputs/kabala_proba/”), ha később kellene.
      Utána: laptopos szülői fejléc (összefolyó zöld). Ötlet még: nem egyforma csempék.
- [x] EU MI-rendelet 50. cikk (2026-08-02 óta él, a Digital Omnibus NEM halasztotta):
      a gyereknek az első beszélgetéstől tudnia kell, hogy AI-val beszél. A tanulóoldal
      fejlécében végig ott a „🤖 AI-tanár” (chat.html, ai-jelzes) → MEGFELEL. A főoldalra
      nem kell külön doboz. (Sándor: a kék doboz-javaslat nem illett az oldalhoz – elvetve.)
- [ ] SZÜLŐI OLDALAK FEJLÉCE (laptop, tablet, telefon – a főoldal kivételével): a zöld
      fejléc beleolvad a zöld sávba. A VILÁGOS lebegő kapszula beépítve (style.css vége,
      csak a zöld sávos oldalakon: body:has(.fp-sav)) – próbaoldalon laptopon, tableten,
      telefonon megnézni. Ha nem jó: a sötétzöld változat, vagy a blokk törlése.
- [ ] KÖLTSÉGLAP (koltsegek_pontos.html) legrosszabb esethez: ÁFA 27% (magyar vevő OSS
      után), jutalék 2,2% (Stripe 1,5% + Stripe Billing 0,7%; + 0,5% ha Stripe Tax),
      kimenő token/perc 3000 → kb. 1000 (mérés: ~430/válasz), könyvelő 80, Railway alap
      +18 (Resend fizetős 100 család felett). Admin: Railway Variables BE_1M=0.75,
      KI_1M=4.50 legyen, különben az admin költség hamis.
- [ ] Főoldal felső rész – javaslat képen (2026-11-05): címke „Türelmes online
      tanító · 1–8. osztály”, a leírás alatt kék doboz: „A tanító mesterséges
      intelligencia (AI). Nem oldja meg a feladatot a gyerek helyett – és te minden
      beszélgetést látsz.” Beépítés ELŐTT ellenőrizni: tényleg látja-e a szülő a
      beszélgetéseket; és hogy a gyerek tanulóoldalán is jól látszik-e, hogy AI-val
      beszél (EU MI-rendelet 50. cikk). Spanyol oldalra ugyanez spanyolul.
- [ ] Hirdetés/főoldal szöveg: sok szülő tart az AI-tól (FB-hozzászólások) →
      kipróbálni, hogy az „AI-tanár” helyett a gyerek haszna és a szülői kontroll
      legyen elöl (pl. „Türelmes online tanító – a szülő mindent lát”).
- [ ] !!! MEGÉRI-E – A KÖVETKEZŐ LÉPÉS (2026-11-05). Legrosszabb esetben (teljes keret,
      végig hangos, 0% gyorsítótár) MINDEN csomag veszteséges: Alap −2, Pro −10,8,
      Max −28,9 €/fő/hó. Ok: az okt. 5-i „megéri” a gpt-6-luna modellel számolt, de a
      tanár maradt gpt-5.4-mini (minőség miatt). A 6–10% kihasználtság Sándor saját
      tesztje volt – NEM valós adat. Sorrend: (1) admin költség most valós áron számol
      (app.py alapár 0.75/4.50 – ha a Railway Variables-ben van BE_1M/KI_1M, törölni);
      Sándor tesztórái után leolvasni: € / tanulási perc; (2) [CACHE] arány a naplóból;
      (3) ELŐSZÖR a gyorsítótár (a prompt ugyanaz marad, csak a változatlan rész kerül
      előre – a tanítást NEM érinti); (4) prompt-diéta CSAK ha tanar_teszt szerint a
      tanítás nem romlik (Sándor: „rosszabb tanár nem ér semmit”); (5) újraszámolás.
      Sándor tette be a Railway-be a BE_1M/KI_1M-et (Claude kérte okt. 5-én) – NEM kell
      törölni; ELLENŐRIZVE: 0.75 / 4.5 → az admin 3,33 € (186 perc) valós: ~1,8 cent/perc.
      Ezzel a legrosszabb eset (27% ÁFA, 2,2% jutalék): csak szöveg: Alap +4,0, Pro +2,7,
      Max −1,9 €/fő/hó; végig hangos (+0,8 cent/perc): Alap +0,8, Pro −4,5, Max −16,3.
      JAVASLAT a csomagokra (legrosszabb esetben is ≥0, havi ÉS éves fizetésnél):
      Alap 400 perc (ebből 250 hangos) · Pro 750 (300 hangos) · Max 1200 (450 hangos).
      Csak csomagok.py: havi_perc / hangos_perc. Előbb a gyorsítótár, utána dönt Sándor.
      Sándor (2026-11-05): ez LOGIKAILAG rossz – a nagyobb csomagban drágább a perc, két
      Alap jobban megéri, mint egy Pro. Új javaslat: a perc ára csökkenjen felfelé:
      Alap 400 (3,72 c/perc) · Pro 750 (3,32) · Max 1300 (3,07); mind lehet hangos;
      + perc-feltöltés 200 perc 7,90 € a sokat tanulóknak. Legrosszabb eset (havi/éves):
      Alap +0,8/−0,9 · Pro −0,6/−3,6 · Max −3,4/−8,2; 50%-os használatnál: Alap +6,0/+4,3 ·
      Pro +9,1/+6,2 · Max +13,5/+8,6 €/fő/hó. Az ingyenes próba marad: 120 perc, 30 hangos.
      Sándornak ez sem tetszik → ki kell dolgozni, versenytársakat megnézni. Talált árak
      (2026): Khanmigo 4 $/hó (44 $/év, max 10 gyerek, nonprofit), Synthesis Tutor 29 $/hó
      (119 $/év, 7 gyerek); magyar magántanár kb. 6000 Ft / 45 perc. A költséglap
      (koltsegek_pontos.html) token/perc alapértéke 16 000 / 1 600 lett (mért); a
      beszélgetés hosszával nő (okt.: 30–60 ezer) → az előzmény rövidítése is megtakarítás.
      295 előfizetős példa (100/95/100): 100% használat −353 €/hó, 50% +2749, 30% +3990.
      KÉT MODELL (2026-11-05, 2,57 cent/hangos perc, 27% ÁFA, 2,2% díj; éves = 11 hónap ára):
      M1 családi keret: Alap 14,90/400 · Család 24,90/800 · Nagycsalád 39,90/1400 → legrosszabb
         +0,9 / −1,8 / −5,7 €; 40%-nál +7,0 / +10,6 / +15,9 €.
      M2 GYEREKENKÉNT (Claude javaslata): 1. gyerek 14,90 € / 400 perc, minden testvér 9,90 € /
         300 perc, saját keret gyerekenként (nem veszik el egymás elől) → legrosszabb +0,9 / −0,1 €;
         40%-nál +7,0 / +4,5 €. + perc-feltöltés 200 perc 7,90 € (+0,7). Opcionális napi
         korlát kor szerint (1–2.: 30, 3–4.: 40, 5–8.: 60 perc).
      Költségcsökkentő, ami a tanítást JAVÍTJA: több interaktív feladat (a böngésző értékel,
      nem kerül tokenbe) – a magyarázat marad.
- [ ] Sándornak egyik modell sem tetszik (2026-11-05). Versenytársak hanggal/AI-jal: Ello (olvasás,
      hang) 14,99 $/hó, évesen 9,99 $/hó; Buddy.ai (3–8 év, hang) 12,49 $/hó, évesen ~4 $/hó,
      ajánlás: heti 3–5 alkalom, 15–30 perc; Synthesis 29 $/hó (főleg előre kész leckék).
      → Az ár (14,90 €) a piacon van; a gond a PERC ÁRA (2,57 cent). Cél: ~1 cent/perc
      a tanítás rontása nélkül: (1) gyorsítótár, (2) beszédfelismerés a böngészőben
      (ingyenes, hu-HU) az OpenAI helyett – minőséget tesztelni, (3) több interaktív feladat
      (nem kerül tokenbe), (4) hosszú beszélgetésnél összefoglaló a teljes előzmény helyett –
      csak tanar_teszt után. ~1 centnél gyerekenként 400 perc ≈ 4 € költség → legrosszabb
      esetben is ~+7 €/gyerek/hó. További ötlet: külföldi magyarok (EUR), hétvégi magyar
      iskolák, pályázat (diaszpóra-oktatás).
- [ ] ÚJ CSOMAGÖTLET (2026-11-05) – „korrepetálás-órák” (1 óra = 45 perc, gyerekenként,
      összevethető a magántanárral, ~6000 Ft/45 perc): Kezdő 8 óra 14,90 € · Szorgalmas
      16 óra 24,90 € · Profi 26 óra 39,90 €; óradíj 1,86 / 1,56 / 1,53 € (felfelé olcsóbb).
      Legrosszabb eset (mind hangos, mind elhasználva): +1,9 / +0,3 / +0,2 €; 40%-nál
      +7,5 / +11,4 / +18,3 €. Éves (11 hónap ára) legrosszabb: +1,2 / −1,1 / −2,1.
      Egyszeri: „Témazáró-felkészítő” 5 óra 9,90 € (+1,5); +1 óra 2,49 € (+0,5).
      200 család (120 Kezdő / 60 Szorgalmas / 20 Profi), havi eredmény a fix költség (440 €)
      után, adó előtt: 100% használat −189 · 60% +940 · 40% +1504 · 25% +1927 €.
      Ha a perc 1,8 cent (gyorsítótár után): 100% +656 · 60% +1447 · 40% +1842 €.
      A négy költségcsökkentőből a „beszélgetés-összefoglaló” EL VAN VETVE (Sándor fél,
      hogy ront); a böngészős beszédfelismerés csak teszt után. Magyarország az első piac.
- [ ] GYIK (2026-11-05 átnézve): a meglévő 6 kérdés rendben. Hiányzik: mennyibe kerül / mi van
      az ingyenes próbában; látja-e a szülő, mit tanul; megoldja-e a házit a gyerek helyett;
      biztonságos-e az AI; napi mennyi tanulás ajánlott. Csomag-döntés UTÁN megírni (HU+ES).
- [ ] GYORSÍTÓTÁR BEÉPÍTVE (2026-11-05, app.py GYORSITOTAR): a percenként változó „A TESZT
      ÁLLAPOTA” bekezdés szóról szóra ugyanaz, csak a tanár utasításainak VÉGÉRE került
      (eddig középen állt, és utána semmi nem lehetett olcsóbb) + gyerekenkénti
      prompt_cache_key. VISSZAÁLLÁS: Railway Variables GYORSITOTAR=0. Ellenőrzés: próbaóra
      után Railway napló „[CACHE]” sorai (ebbol_cache %); hang_teszt.py; rövid tanar_teszt.
- [x] GYIK: a teszt-kérdés pontosítva a kód szerint (HU+ES): szintfelmérő 30 perc tanulás után,
      max. 3 próba, 100% kell; leckezáró a lecke idejének letelte után: 70% fölött megnyílik
      a következő lecke („Tovább” vagy „Még gyakorlok”), 70% alatt +60 perc tanulás, utána újra.
- [ ] ÚJ CSOMAGÖTLET – ÓRA-BÉRLET (előre fizetett órák, 1 óra = 45 perc, pl. 3 hónapig érvényes):
      4 óra 13,90 € · 8 óra 24,90 € · 16 óra 44,90 € (≈1370 / 1230 / 1110 Ft/óra; magántanár
      ~6000 Ft). Haszon akkor is, ha MINDEN órát elhasznál: +5,8 / +9,6 / +15,6 € (55/51/46%).
      200 család, havi 1 bérlet (100/70/30): +1274 €/hó a fix költség után, akkor is, ha
      mindent elhasználnak → nem kell izgulni a használaton. Kényelmi lehetőség: automatikus
      havi megújítás.
      FORINTBAN (2026-11-05, 395 Ft/€-val számolva, 27% ÁFA): 4 óra 5 490 Ft · 8 óra + 2 óra
      írásban ajándék 9 490 Ft · 12 óra + 4 óra írásban 13 490 Ft · plusz 1 óra 1 490 Ft ·
      TANÉV-BÉRLET 80 óra 84 900 Ft (szept.–jún.). Haszon, ha mind elfogy: +5,8 / +7,3 / +8,8 /
      +1,5 / +71,7 €. Az írásos perc olcsóbb (1,79 c vs 2,57 c hangos). „Óra” = 45 perc tanulási
      idő – a csomag oldalon és az ÁSZF-ben egyértelműen kiírni (nem élő tanár). Árfolyamkockázat:
      a költség dollárban jön → évente felülvizsgálni az árakat (a megvett bérlet ára nem változik).
      Házi feladat (fotó) később: ugyanabból az órakeretből.
- [ ] !!! „ÓRA” A CSOMAGOKBAN – JOGI (Sándor kérte felírni): ha az órás/bérletes csomag lesz,
      a csomagoldalon ÉS az ÁSZF-ben egyértelműen: „1 óra = 45 perc tanulási idő a TutorIA
      (mesterséges intelligencia) tanítójával” – nem élő tanár. Az ÁSZF-et ehhez MÓDOSÍTANI kell.
      Kérdés a jogi listára (Your Europe Advice): külföldi (spanyol) eladónál kötelező-e a
      magyar vásárlónak forintban kiírni az árat.
- [ ] PÉNZNEM: Sándor az EURÓT szeretné. Utánanézve (2026-11-05): Magyarországon az üzletekben a
      forintos ár kötelező, a szolgáltatás díjára is – KIVÉVE a határon átnyúló szolgáltatást
      (BFKH, Niveus). Mi spanyol szolgáltató vagyunk → valószínűleg elég az euró. Bizonyosság:
      Your Europe Advice kérdés. Ha kell a „≈ Ft”, azt a program magától frissíti (EKB napi
      árfolyam), kézzel senkinek nem kell. GYIK: egyes bankok átváltási díjat számolhatnak.
- [x] DÖNTÉS (2026-11-06): Sándor elfogadta a BÉRLET modellt (6 / 10 / 18 órás, órakeret bármely
      tárgyra, 1 óra = 45 perc, euróban, ≈ Ft tájékoztató).
- [ ] JOGI BIZTONSÁG A TESZTIDŐSZAKBAN (Gemini figyelmeztetése alapján, 2026-11-06):
      (1) Csomagoldal (Gemini + Meta + Claude egyetért, 2026-11-06): a NYILVÁNOS oldalon NINCS
      ár – „Ingyenes tesztidőszak. A fizetős bérletek hamarosan indulnak.” A tervezett
      árakat CSAK a belépett (regisztrált) szülő látja, „tervezett ár – még nem vásárolható”
      jelöléssel + „Ennyiért kérném” (Érdekel) gomb → így mérjük, ki fizetne.
      Döntési határidő: kb. 4–6 hét teszt, utána autónomo + fizetés, vagy változtatás.
      (2) Impresszum / Aviso legal oldal (spanyol LSSI 10. cikk): név, e-mail, ország; az
      adószám (NIF/NIE) és a cím legkésőbb az autónomo bejelentésekor.
      ✔ KÉSZ (fix73, 2026-11-06): (1) csomagoldal – be nem lépve „Hamarosan”, ár a forrásban
      sincs; belépve „Tervezett ár – még nem vásárolható” + „Ennyiért kérném” (a régi Érdekel
      gomb, data-mer: „Csomag: X – ennyiért kérném”). (2) /impresszum és /aviso-legal + lábléc.
      TEENDŐ az autónomo után: Railway változók UZEMELTETO_CIM és UZEMELTETO_NIF → az
      impresszumon magától megjelenik (kód nem kell).
- [x] KÉSZ (fix74, 2026-11-06): A FEL NEM HASZNÁLT ÓRA 3 HÓNAPIG MEGMARAD (app.py _berlet_keret,
      database.tanulasi_perc_naponta). Minden fordulónapon jár a havi keret; egy hónap órái a
      vásárlás hónapja + 2 fordulóig élnek; mindig a legrégebbi óra fogy. A keret-elfogyott
      levél is ezzel számol. Visszaállás: Railway BERLET_ATVITEL=0. Lemondás után a kifizetett
      hónap végéig minden megmaradt óra használható (csomagoldal GYIK-ben leírva).
      ÁSZF-be BE KELL ÍRNI fizetés előtt: 1 óra = 45 perc, 3 hónapos átvitel, mi lesz lemondáskor.
      FIGYELEM: csomagváltáskor (Stripe) a csomag_kezdet-et újra kell indítani, mert a program a
      MOSTANI csomag havi keretével számol visszamenőleg is.
- [x] KÉSZ (fix75, 2026-11-06):
      • A kifizetett órák a saját 3 hónapjukig megmaradnak akkor is, ha nem fizet tovább
        (_szulo_csomag / _berlet_keret fizetett_ig). Szöveg: csomagoldal, GYIK, ÁSZF 7. pont (HU+ES).
      • HANGOS KORLÁT BEKAPCSOLVA: ha a csomag hangos ideje kevesebb, mint az összes (most csak
        az ingyenes próba: 120-ból 30), elfogyásakor a felolvasás 429-cel elhallgat, a tanítás
        írásban megy tovább, a gyerek üzenetet kap. KIVÉTEL: elsős ≤7 év (csak hangos profil).
        Hangos óra = amelyben hangos módban küldött üzenetet (chat/send mode=voice).
        Fiókom: „Hangos idő még: X / 30 perc”.
      • ÁR: 10 órás 26,90 → 24,90 €; 18 órás mind a 18 óra hangos (nincs „4 írásban”). Óránként:
        2,65 / 2,49 / 2,22 € – felfelé olcsóbb. Haszon végig hangosan: ~5,0 / ~7,2 / ~9,5 €/hó.
      • Időmérés: a tétlen 3 perc már nem számít bele (chat.html); a szerver nem fogad el több
        percet, mint amennyi az óra kezdete óta eltelt, és csak a saját gyerek órájához ír.
- [ ] !!! FIZETÉS ELŐTT: a tanulási időt a BÖNGÉSZŐ méri és küldi – ügyes szülő letilthatja a
      küldést. Biztos megoldás: a szerver is számoljon (pl. a chat üzenetekből). 
- [ ] HANGMÓD – Sándornak megmutatni, NEM javítottam: (1) a felolvasás (playTts) nem küldi a
      mode=voice-ot, ezért a szerver hangos módban is a rövid (MAX_KARAKTER) változatot olvassa
      fel – a kód szerint ezt el akartuk kerülni. (2) A beszédfelismerés (STT) a hangos keret
      elfogyása után is megy – a hangköltség kb. fele.
- [ ] HIRDETÉS-ADAT 11.07. 17:49-ig: a hirdetésből 239 látogató, ebből 83 a regisztrációs oldalon
      (a link most oda visz), medián 5 mp, 0 regisztráció. Ötlet: a hirdetés vigyen a /demo
      oldalra (regisztráció nélküli kipróbálás) – kisebb lépés a hideg látogatónak.
- [ ] HIRDETÉS-ADAT (2026-11-04–06): 148 hirdetésből jött látogató, átlag 6 mp a főoldalon,
      2 jutott a regisztrációig, 0 regisztrált. A gond a hirdetés és a főoldal között van, nem
      az űrlapon. Teendő: új hirdetéssorozat kézi elhelyezéssel (csak Facebook + Instagram
      hírfolyam/Reels, Audience Network NÉLKÜL), a régi leállítva. A videóban (tutoria_reel_4x5.mp4)
      nincs hangsáv – érdemes zenét tenni alá. A jelszó-megerősítés és a 4 jegyű kód MARAD
      (Sándor döntése).
- [x] REGISZTRÁCIÓS ŰRLAP átnézve (2026-11-06): Sándor döntése – a jelszó kétszer és a 4 jegyű
      szülői kód marad. A fő gond, hogy el sem jutnak az űrlapig (lásd HIRDETÉS-ADAT).
      (3) Hirdetés mehet tovább, de CSAK az ingyenes tesztet hirdesse, ár nélkül.
      (4) Autónomo: közvetlenül az első fizetős eladás (Stripe élesítés) ELŐTT; jelzés: ha
      ~25 család megnyomta az „Érdekel”-t. Tarifa plana 80 €/hó jár. „Számlázó szövetkezet”
      (cooperativa de facturación) NEM – Spanyolországban kockázatos/tiltott megoldásnak számít.
- [ ] BÉRLET – PONTOSÍTVA (2026-11-05): hogy a lassabban haladó gyerek se maradjon le, ráhagyással:
      Egy tantárgy 6 óra/hó 15,90 € (10 hónap = 60 óra ≥ matek max. ~45) · Fő tárgyak 10 óra
      26,90 € (100 óra ≥ matek+magyar ~67–77) · Minden tárgy 14 + 4 írásos 39,90 € · plusz 1 óra
      3,90 € · Tanév fő tárgyak 100 óra 229 €. Haszon, ha MIND elfogy, végig hangosan:
      +5,0 / +8,8 / +10,9 / +59 €; ha végig írásban: +7,1 / +12,3 / +15,8 / +94 €.
      A fel nem használt órák a bérlet lejártáig (3 hó) átvihetők a következő hónapra.
      Fizetés EURÓBAN (Stripe), mellette „≈ Ft, tájékoztató” – a program az EKB napi
      árfolyamával frissíti; a bevétel euróban marad → Sándornak nincs árfolyamkockázata.
- [ ] CSOMAGOK: tantárgyanként NEM bontjuk – az órák bármelyik tárgyra mehetnek (a nevek csak
      eligazítanak). Amíg nincs fizetés, a csomagoldalon jelezni: „az árak a fizetős indulásig
      változhatnak” – így nem félrevezető, ha később változik.
- [ ] MENNYI ÓRA KELL EGY TANÉVHEZ (a mi leckehosszainkból számolva, HU tanterv):
      matek 1–2. o. ~39 óra · 3–4. ~45 · 5–6. ~36 · 7–8. ~22; magyar 1–2. ~28 · 3–4. ~32 ·
      5–6. ~18 · 7–8. ~13; környezet 3. ~11 · 4. ~16; angol 5–8. ~36 óra/év (1 óra = 45 perc).
      → Egy tárgy egész éve ≈ 4–5 óra/hó; matek+magyar ≈ 8–9 óra/hó (10 hónappal).
      CÉL SZERINTI BÉRLET-JAVASLAT (EUR): Egy tárgy 5 óra 15,90 € · Fő tárgyak 9 óra 26,90 € ·
      Minden tárgy 14 óra + 4 írásos ajándék 39,90 € · plusz 1 óra 3,90 € · Tanév „fő tárgyak”
      90 óra 229 € · Tanév „minden” 140 óra 349 €. Haszon, ha MIND elfogy: +6,1 / +9,9 / +10,9 /
      +1,6 / +70,9 / +105 €. (A gyakorlás/ismétlés miatt több idő is kellhet – mérni.)
- [ ] TÉMAZÁRÓ-FELKÉSZÍTŐ (Sándor: a tanárnak specifikusan, okosan kell segítenie): a gyerek
      megadja a témazáró témáját/idejét → rövid felmérés, hol hiányos → célzott magyarázat
      és gyakorlás → próbadolgozat → értékelés a szülőnek. Megtervezni.
      Ha a gyereknek EGYÁLTALÁN nem megy (Sándor): a tanár egy HASONLÓ példát végig megold és
      elmagyaráz → az igazi feladatot lépésenként EGYÜTT oldják meg (a gyerek csinálja a
      lépést, a tanár segít) → végül egy új, hasonló feladatot egyedül. Kész választ magyarázat
      nélkül soha. Ugyanez a házi feladat segítőnél.
- [x] Laptop: a kapszula-fejléc gyerek-munkamenetben a színes gyereksávot eltakarta → ott nincs
      kapszula (style.css :not(:has(.gymenu))).
      Sándor kérése: a TANÍTÁS MINŐSÉGE nem romolhat – minden megtakarítás csak tanar_teszt
      összevetés után, és csak ha ugyanolyan jó.
      Becslés: felezett prompt + 80% gyorsítótár → ~1,5 cent/perc → legrosszabb esetben
      is mindhárom csomag nullán felül. Ha nem jön ki: hangos perc korlátozása a nagy
      csomagokban, vagy olcsóbb modell az egyszerű lépésekhez.
- [ ] PROMPT-DIÉTA (a legnagyobb megtakarítás): mért adat (tanar_teszt
      2026-11-03): egy gyerek-üzenetre 22 500 bemenő token megy el, a válasz
      csak ~430. Előbb kimérni, mekkora ebből a tananyag és mekkora a
      szabályok (a magyar oldalon a spanyol szabályok is elmennek, és fordítva);
      a változó részek a prompt VÉGÉRE, hogy az OpenAI gyorsítótára működjön.
      Railway napló [CACHE] sorai mutatják a gyorsítótár %-át.
      BIZTONSÁG: csak próbaoldalon, kis lépésekben; minden lépés előtt és után
      tanar_teszt.py (minőség) + hang_teszt.py; ha romlik, visszavonjuk.
- [ ] ÖTLET (Sándor, 2026-11-05): HÁZI FELADAT / LECKE MEGÉRTŐ. A szülő
      lefényképezi a feladatot vagy a füzetet, az AI elmagyarázza (példákkal),
      és lépésenként VELE oldja meg – nem adja ki kész megoldásként (a TutorIA
      lényege: „megvárja”). Átgondolandó: a fotót ne tároljuk (csak feldolgozás,
      utána törlés – név, iskola lehet rajta) → adatvédelmi oldal + nyilvántartás
      frissítése; költség: egy kép kb. 1–2 ezer token (olcsó); melyik csomagban.
- [x] Főoldal felső címke + megosztási cím (og_cim) átírva (2026-11-05):
      HU „AI-tanár · 1–8. osztály · az évfolyam témakörei szerint”, ES
      „Profesor con IA · de 1.º a 6.º de Primaria · según los temas de cada curso”
      (az ES oldalon is volt „Según el currículo escolar (LOMLOE)” – az is ki).
- [ ] ÚJRASZÁMOLNI a megéri-e számítást VALÓS mért adatokkal (a megerie.html
      2026-10-05-ös, ÁFÁ-val és Stripe-pal már számolt, de a perc-költség még
      becslés volt). Kell hozzá: /admin gyerek-sorok (perc, be/ki token),
      Railway napló [CACHE] sorai, OpenAI és Azure októberi számla.
      Új tételek: autónomo 80 €/hó (tarifa plana) 300 helyett; jövedelemadó
      (IRPF, negyedéves előleg a nyereség 20%-a); Resend fizetős 100 család
      felett.
- [x] OpenAI és Resend DPA PDF a jogi/ mappában (2026-11-05). A gyökérben
      lévő két példány törölhető.
- [ ] Főoldal első képernyője: a hirdetésből jövők 6 mp után elmennek, senki
      nem nézi meg a csomagokat → az első képernyőt erősíteni.
- [ ] Hirdetés: a hirdetést a SZÜLŐNEK szóljon (Meta: 18+ célzás), gyereket
      ne célozzunk; a hirdetésben ne ígérjünk olyat, amit az oldal nem tud.

## Fizetés bekötése ELŐTT (kötelező)

- [ ] Vállalkozói (autónomo) — enélkül a többi nem indulhat. Az ingyenes
      próba alatt (nincs bevétel) még nem kell; az ELSŐ fizetős eladás előtt
      igen. Sándor ~3 éve volt autónomo (Nestlé), azóta kijelentve: a „vida
      laboral” igazolásból (Seguridad Social, online) megnézni a kijelentés
      pontos dátumát → tarifa plana (80 €/hó) jár, ha 2 éve (ha akkor is
      tarifa planán volt: 3 éve) nem volt autónomo. Spanyol levelet Claude ír.
      Sándor szerint: kb. 2023 tavaszán jelentkezett be, 2023 szeptemberében
      ki → 2026 szeptember óta mindkét feltétel teljesül → 80 €/hó az első
      12 hónapban (+12 hónap, ha a nettó jövedelem a minimálbér alatt marad).
      Andalúz „Cuota Cero” (a Junta visszafizeti a 80 €-t): jelenleg ZÁRVA,
      figyelni, újranyílik-e (infoautonomos.com/seguridad-social/cuota-cero-autonomos).
- [ ] Fizetés módja – két út (gestoríával eldönteni):
      a) Stripe: kb. 1,5% + 0,25 € fizetésenként (14,90 €-nál ~0,47 €). 10 000 €
         alatt mindenkinek spanyol 21% ÁFA, a számlát a Stripe küldi.
      b) Paddle / Lemon Squeezy: kb. 5% + 0,50 $ (14,90 €-nál ~1,20 €), de ő
         intéz minden ÁFÁ-t, számlát, OSS-t.
      Javaslat: indulni Stripe-pal, 8 000 € körül átgondolni. Az éves csomag
      kevesebb díjat visz (egy fizetés egy év helyett 12).
- [ ] KÖLTSÉGBE FELVENNI: az árak ÁFÁ-val értendők → 14,90 €-ból 21% ÁFA után
      ~12,31 € marad, ebből megy még a fizetési díj. Ezt a koltseg
      számításba be kell tenni.
- [ ] ÁSZF: Claude írja meg (más oldal szövegét lemásolni nem szabad – szerzői
      jog, és nem illik a mi szolgáltatásunkra).
- [ ] ÁSZF (feltételek) frissítése fizetéshez: ár ÁFÁ-val, lemondás, 14 napos
      elállás digitális szolgáltatásnál (ha azonnal indul: kifejezett
      beleegyezés + tudomásulvétel jelölőnégyzet), panaszkezelés, alkalmazandó
      jog. Magyar és spanyol nyelven.
- [ ] ÁFA: spanyol ÁFA (21%) a számlán; ha a nem spanyol EU-s magánvevők
      éves összege eléri a 10 000 €-t → OSS regisztráció, a vevő országának ÁFÁ-ja.
      Nem EU-s vevő (UK, Svájc, Norvégia, USA…): külön szabály – gestoríával.
- [ ] Számlázás: minden eladásról számla (Stripe/számlázó), 6 év megőrzés.
- [ ] Fizetési adatok: kártyát csak a Stripe kezeljen, mi ne tároljuk.
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

# MEGÉRI-E? — A VÁLASZ MEGVAN (2026-10-05)

A teljes, forrásolt számítás külön lapon: `megerie.html` (nyisd meg
böngészőben). Itt csak a lényeg.

## A válasz: IGEN, de nem úgy, ahogy most fut

A kód a `gpt-5.4-mini` modellt hívja. Ez ma már "legacy", és DRÁGA:
0,75 $ bemenő és 4,50 $ kimenő millió tokenenként. Teljes perckeret-
használat mellett ezzel MIND A HÁROM CSOMAG VESZTESÉGES.

A mai olcsó modellen (`gpt-6-luna`, 0,05 / 0,25 $ millió tokenenként)
ugyanez a szolgáltatás MINDEN csomagnál nyereséges, teljes hangos
használat mellett is:

    csomag        gpt-5.4-mini      gpt-6-luna     nullszaldo (luna)
    Alap havi        +1,09 EUR       +8,26 EUR          48 fo
    Alap eves        -0,70 EUR       +6,47 EUR          61 fo
    Pro  havi        -4,24 EUR      +11,89 EUR          33 fo
    Pro  eves        -7,38 EUR       +8,75 EUR          45 fo
    Max  havi       -16,27 EUR      +16,00 EUR          25 fo
    Max  eves       -21,44 EUR      +10,83 EUR          37 fo

(75% gyorsítótárral számolva, havi 390,67 EUR állandó költség mellett.
Az éves azért hoz kevesebbet, mert tíz hónap árát fizeti tizenkét
hónapnyi percért — ez a kedvezmény ára.)

## Miért nem vészes MOST

A két mért gyerek az Alap keretének 6 és 10 százalékát használta el
harminc nap alatt. Ennyinél még a drága modellel is 11-29 EUR marad
csomagtól függően. A veszély a MEGÍGÉRT KERET: a mostani modellen a Pro
75%, a Max már 50% körüli kihasználtságnál fordul veszteségbe.

## Teendők, fontossági sorrendben

1. MODELLVÁLTÁS KIPRÓBÁLÁSA. Ez önmagában megoldja a kérdést. DE előbb
   tanítási minőségre tesztelni kell — egy butább tanár nem ér 15 eurót.
   Fél napos munka. A modellnév az app.py-ban több helyen szerepel.
2. A ROSSZ ÁRAK JAVÍTÁSA az adminban, hogy a jövőben a valóságot lásd.
   Railway -> web szolgáltatás -> Variables: BE_1M és KI_1M a választott
   modell árára. (Most 0.10 és 0.60 áll ott, ami egyik modellhez sem
   tartozik.)
3. RÖVIDEBB RENDSZERPROMPT. Percenként kb. 30 000 bemenő token megy el,
   mert a TELJES tananyag minden kérésnél újra elmegy. Ha csak az
   aktuális témakör menne, a költség töredékére esne — modellváltás
   nélkül is. Ez a második legnagyobb tétel.
4. A gyorsítótár (`cached_tokens`) mérése — a kód most nem tárolja.
5. A be:ki token arány leolvasása az admin oldalról (mostantól kiírja).
   A számítás 10:1-et feltételez; ez az egyetlen maradék becslés.

## Amit NEM kell tenni

Árat emelni vagy perckeretet vágni. A számok szerint nem az árazás a
baj, hanem egy drága, elavult modell és egy túl hosszú prompt.

## Ellenőrzött árak (2026-10-05)

  - Azure felolvasas: 16 $/1M karakter, havi 500 000 ingyen — HELYES
  - gpt-transcribe: 0,0045 $/perc (OpenAI hivatalos) — HELYES, es a kod
    tenyleg ezt a modellt hivja
  - arfolyam: 1 EUR = 1,119 $ — a kodban levo 0,92 ovatos, rendben
  - afa 21%, Stripe 1,5% + 0,25 EUR tranzakciónként

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

---

# A PRÓBA OLDAL VÉGIGNÉZÉSE LUNÁVAL (2026-10-06)

Sorrendben, amit Sándor talált. A legtöbb NEM modellfüggő: ugyanígy
megvolt a régi modellel is. Külön jelölve, melyik mitől van.

## 1. SÚLYOS: az ábra MÁST mutat, mint a kérdés  [kód / prompt hiba]
Matek, halmazok. A tábla kérdése: "Melyik számok vannak közösen a 3, 5, 7
elemeit tartalmazó és az 5, 7, 9 elemeit tartalmazó halmazban?"
A RAJZON viszont 2, 4, 6, 8 szerepel — semmi köze a kérdéshez. A
válaszlehetőségek pedig megint mások: "5 és 7", "3 és 9", "3, 5, 7 és 9".
Három különböző dolog egyszerre. A gyerek nem tudja megoldani, mert a
rajz ellentmond a szövegnek.
A promptban MÁR BENNE VAN a szabály ("a rajznak azt a feladatot kell
mutatnia, amit a gyereknek MOST kell megoldania") — mégsem tartja be.
Ez a legfontosabb javítandó: inkább NE legyen rajz, mint rossz rajz.

## 2. A tábla és a beszélgetés külön úton jár  [kód / prompt hiba]
Többször is: a táblán az egyik kérdés áll, a chatben a tanár egy másikról
beszél (halmazoknál a táblán a metszet, a chatben a részhalmaz és a piros
alma). A gyerek nem tudja, melyikre válaszoljon.

## 3. A "MONDD UTÁNAM" kártya nem mondja meg, mit kell kimondani
Angolóra: a táblán két mondat van ("What is your name?" és "My name is
Sam."), a kártyán viszont csak ennyi: "name". Nem derül ki, melyiket kell
kimondani. A kártyán a TELJES kimondandó mondatnak kell állnia.

## 4. Értelmetlen ábrák elvont fogalmakra  [prompt hiba]
Hon- és népismeret: három doboz "Családfa / Közösség / Rokon" felirattal,
bennük értelmetlen karika-vonal rajzok. Nem magyaráz semmit.
A prompt EZT IS tiltja már ("ha a fogalom elvont és nem tudsz valódi
dolgot mutatni, NE rajzolj") — nem tartja be.

## 5. Összecsúszó feliratok az ábrán  [prompt / abra.py]
Történelem, "Fénykép / Emléktárgy / Elbeszélés": a dobozok feliratai és
az alattuk lévő magyarázó sor egymásba lógnak.

## 6. Magyartalan kérdés  [prompt hiba]
"Ha valaki integet, az arcjátékot, gesztust vagy testhelyzetet használ?"
Így magyarul nem kérdezünk. Helyesen: "Ha valaki integet, arcjátékot,
gesztust vagy testtartást használ?"

## 7. A gombok lassan vagy egyáltalán nem reagálnak  [kód hiba, RÉGI]
A tantárgyválasztó alján az "AI tanulás és beszélgetés (chat)" és a
"(hangos)" gombra többször rá kell nyomni. Nem a modell lassú: a gomb
kattintáskor nem ad SEMMI visszajelzést, közben a szerver dolgozik, ezért
az ember újra rányom — és néha az újbóli kattintás szakítja meg az
elsőt. MEGOLDÁS: kattintáskor azonnal tiltsuk le a gombot és írjuk ki,
hogy "Indítom…". Ez tiszta felületi javítás, nem kell hozzá modell.

## Nyitott kérdés
A spanyol oldalon ugyanezek megvannak-e? Nem néztük meg.

## Mit NEM okozott a modellváltás
Az 1., 2., 4., 5., 6. pont a rendszerpromptból és az ábragenerálásból jön,
a 7. tiszta felületi hiba. Ezek a régi modellel is megvoltak. A Luna
felelősségét csak úgy lehet eldönteni, ha ugyanazt a leckét lefuttatjuk a
két modellel — a MODELL_TANAR változó átírásával ez öt perc.

---

# EL NE FELEJTSÜK (2026-10-06)

## A Luna az éles oldalon
A `gpt-6-luna` most CSAK a próbán fut. Az élesen marad a `gpt-5.4-mini`,
mert ott nincs beállítva MODELL_TANAR. Ha a próbán kiderül, hogy a Luna
elég jól tanít, akkor az ÉLES Railway projektben kell felvenni:
    MODELL_TANAR = gpt-6-luna
    MODELL_SEGED = gpt-6-luna
    BE_1M = 0.1      (most 0.75, a mini ára)
    KI_1M = 0.5      (most 4.5, a mini ára)
A négyet EGYSZERRE kell átírni, különben az admin hibás eurót mutat.

## Ami a hét hibából megvan
  1. rossz ábra (a rajz számai idegenek)  — KÉSZ (abra_ellenor.py)
  7. lassú/nem reagáló indítógombok       — KÉSZ (select_tasks.html)
Marad: tábla és chat külön úton jár; a „mondd utánam" kártyán csak egy szó;
értelmetlen ábrák elvont fogalmaknál; összecsúszó feliratok; magyartalan
kérdés. Mind a négy-öt a rendszerpromptból jön — egy menetben érdemes.

## Az ábra-ellenőr NAGY lépése, ami még hátravan
Az `abra_ellenor.py` DETERMINISZTIKUS szabályai csak a számos hibákat
fogják meg. Ami nem szám (kémia jelölés, fizikai ábra, kottakép, elvont
fogalom), azt csak az AI-ellenőr (`rendben()`) tudja megítélni — az pedig
MOST "naplo" módban fut, vagyis lát mindent, de nem dob el semmit.
A következő lépés NEM az, hogy élesre kapcsoljuk, hanem hogy MEGNÉZZÜK a
próbán az /abra-naplo oldalt: mit ítélne hibásnak. Ha a napló szerint a
rossz rajzokat fogja meg és nem a jókat, akkor jöhet az ABRA_ELLENOR=1.
(Ezt a leckét egyszer már drágán megtanultuk: élesre állítva az ábrák
mérés nélkül eltűntek.)

## MOBIL ÉS TABLET — a legnagyobb nyitott kérdés
Már használják az oldalt, tehát ez most számít, nem majd.

ELŐSZÖR MÉRNI KELL. Jelenleg SEMMI nem jegyzi fel, ki milyen készülékről
tanul — se az app.py, se az adatbázis. Amíg ez nincs, minden mobilos
fejlesztés vakrepülés. Egy oszlop a tanulási sorba (telefon / tablet /
asztali) és egy sor az admin oldalra: fél nap, és utána tudjuk, hol
érdemes dolgozni.

HÁROM KÜLÖN BAJ, HÁROM KÜLÖN JAVÍTÁS:
  a) A GÉPELÉS maga rossz input egy gyereknek telefonon. Erre már VAN
     válaszunk: a hangos mód. Telefonon a hangos legyen az ELSŐ,
     felkínált út, ne a második gomb. Emellett ahol lehet, koppintható
     válaszlehetőség legyen gépelés helyett — a kvízkártyák már így
     mennek, a beszélgetésben nem.
  b) A BILLENTYŰZET feljövetelekor elcsúszik a kép. Ez tiszta CSS/JS
     kérdés: dvh egységek és a visualViewport figyelése. Kicsi munka.
  c) AZ ELRENDEZÉS asztali gépre készült: három hasáb (leckelista, tábla,
     beszélgetés) összenyomva egy telefonra. A valódi válasz egy
     telefonra tervezett lecke-nézet: a tábla teljes szélességben, a
     beszélgetés alulról felhúzható lapon, a leckelista menü mögött.
     Ez a legnagyobb munka a háromból.

SORREND JAVASLAT: mérés → b) billentyűzet → a) hangos mód előre →
c) elrendezés. Az a) adja a legtöbbet a befektetett munkához képest.

---

# MOBILOS VÉGIGNÉZÉS (2026-10-06, Sándor telefonján)

## Amit MOST megjavítottam
  - A FELADAT mezőiből (válaszgombok, kérdés, szöveg) eltűnnek a tanári
    jelölők. Élesben `<FL:es>Hay un parque.</FL>` állt a gombokon. A
    beszélgetés szövegét eddig is tisztítottuk, a feladatot nem — most
    EGY helyen, minden típusra, hogy új típusnál se lehessen elfelejteni.
  - A felolvasás nem mondja ki az „egyenlő"-t szótári párnál.
    „enfrente de = szemben" → rövid szünet. A matematika érintetlen:
    „2 + 3 = 5" továbbra is „egyenlő".

## Amit még meg kell csinálni — SORBAN

1. BESZÉLGETÉS VISSZANÉZÉSE (6. kép). Telefonon nem lehet visszagörgetni
   a beszélgetésben, nincs görgetősáv. A gyerek nem tudja újraolvasni,
   mit magyarázott a tanár. Ez komoly: tanulni nem lehet enélkül.

2. A KABALA FIGURA BELELÓG A SZÖVEGBE (4., 5. kép). Telefonon és
   tableten legyen MOZGATHATÓ, vagy tűnjön el, ha szöveg kerül alá.

3. SOK AZ ÜRES HELY A KÉPERNYŐ ALJÁN (4., 5. kép). A tábla alatt nagy
   üres sáv marad, a tartalom felül összezsúfolódik.

4. A SZÓJEGYZÉK ÖSSZE VAN TOLVA (5. kép), alig olvasható telefonon.

5. HIBÁS MAGYAR FORDÍTÁS (7. kép): „A kórház a bolt szemben van."
   Helyesen: „A kórház a bolttal szemben van." A promptban kell egy
   szabály a RAGOZÁSRA a példamondatok fordításánál.

6. A VÁLASZLEHETŐSÉGEK NEM LÁTSZANAK (4. kép). „Melyik dal inkább
   párosító dal?" — és nincs mire kattintani.

## ALBUM (nem sürgős, de ne vesszen el)
  - A lapozás egyre rosszabb, az 1. képen a fél lap fekete.
  - A személyek FÜGGŐLEGESEN vannak, ezért nagyon hosszú az album.
    VÍZSZINTES elrendezés kellene.

## A KÉSZÜLÉK MÉRÉSÉRŐL — FONTOS TUDNI
Ha bevezetjük (telefon / tablet / laptop-asztali), az CSAK AZ ÚJ
tanulásokra fog látszani. A már meglévő tanulási sorokban nincs ilyen
adat, és visszamenőleg nem lehet kitalálni. Tehát minél hamarabb kerül
be, annál hamarabb lesz belőle használható kép.

## A KONKURENCIÁRÓL (Smartick, KooBits, MindED)
Sándor képeket küldött. Amiben ők jobbak, és amit érdemes elirigyelni:
  - a feladat MAGA a kép: mérleg, szobrok, tárgyak — nem szöveg + ábra,
    hanem egyetlen, rajzolt jelenet, amire koppintani kell;
  - minden válasz KOPPINTÁS, nem gépelés;
  - felolvasás-gomb minden feladatnál (a kicsik nem olvasnak);
  - látható haladás: csillagok, sáv, szint.
Ezek nem AI-kérdések, hanem FELÜLET-kérdések. A mi erősségünk (igazi
tanár, aki magyaráz) megmarad mellettük — de a feladatok megjelenítésén
sokat lehetne javítani anélkül, hogy a tanítást elrontanánk.

---

## INTERAKTÍV TANÍTÁS – A TERV (2026-10-18, Sándor jóváhagyta az irányt)

ALAPELV: nem leckénként rajzolunk, hanem ÚJRAHASZNÁLHATÓ, kattintható
elemeket építünk (kódban, képgyártás nélkül – használatkor 0 Ft). A tanár
csak a SZÁMOKAT / SZAVAKAT adja meg egy <FELADAT> jelölőben, a program
ellenőrzi őket (rossz értéknél sima kérdés marad). Így egy elem több száz
feladatot fed le, több évfolyamon – a két tantervhez összesen nagyjából
30 elem kell, nem több ezer. Ha a gyerek nem érti, a tanár új számokkal
újat ad. Minden elem MAGYARUL és SPANYOLUL is. A tanár csak az adott
tantárgyhoz és évfolyamhoz illő elemeket látja a promptban.
Minden új elemből ELŐBB kipróbálható minta készül, csak utána kerül be.

Kész minta (Claude outputs/interaktiv_minta.html), Sándornak tetszett:
- [ ] Törtpizza (szeletek kiszínezése) – 1–3. o.
- [ ] Béka a számegyenesen (ugrál, számol) – 1–2. o.
- [ ] Óra húzható mutatókkal (negyed, fél, háromnegyed) – 1–3. o.

Tervezett elemek:
- [ ] Matek 3–4.: írásbeli összeadás/kivonás oszlopban MOZGÓ átvitellel
      és lépésenkénti segítséggel (az oszlopos tábla már megvan, ez a
      bővítése), szorzás téglalap-rácson, törtek a számegyenesen.
- [ ] Matek 5–8.: húzható szögmérő, koordináta-rendszer (pont elhelyezése),
      kerület/terület négyzetrácson (húzható téglalap), egyenlet-mérleg,
      százaléksáv.
- [ ] Környezetismeret, biológia: részek címkézése húzással (növény, test).
- [ ] Földrajz: forgatható iránytű, méretarány-vonalzó.
- [ ] Fizika: áramkör kapcsolóval (az izzó felgyullad).
- [ ] Ének-zene: megszólaló hangjegyek, ritmus koppintással.
- [ ] Történelem: idővonal, amire az eseményeket húzni kell.
- [ ] Memóriajáték (kép ↔ szó): nyelvórán a megtanult szavakkal (176
      szótárkép), környezetismeretben a fogalomképekkel, és SZÜNETJÁTÉKNAK.
- [ ] Szünet-ajánlat: kb. 20 AKTÍV perc után (felső tagozaton 30) kedves
      ajánlat: „Pihensz 2 percet egy memóriajátékkal?" – nem kötelező, a
      szülő átállíthatja vagy kikapcsolhatja. Csak az számít aktív
      percnek, amikor a gyerek tényleg válaszol.

## Később (2026-10-26)

- [ ] Mappa takarítása: a régi `git add -A` óta felkerült próbafájlok (pl. `_css.txt`, `_elonezet.html`, `_elonezet.py`, `_f.json`, `_k.js`, `_kivonat.*`, `euklidesz_*.png`, `minta1-3.png`, `teszt_kep.png`, régi tesztnaplók). Claude előbb összeírja, mi törölhető biztonságosan; törölni Sándor töröl.
- [ ] `kinézet képek\facebook\figyelem_szervek.png` törlése.
- [ ] Teszt eredményoldal: pontösszesítő („7/10, ezeket rontottad, ezt gyakorold”) – jó ötlet, nem sürgős.
- [ ] Kipróbálós demóoldal regisztráció nélkül – akkor kell, ha újra fut a Facebook hirdetés.
- [ ] Képtár: előre legenerált, jóváhagyott képek témakörönként (a gyerek nem vár), a tanár csak a lecke saját képei közül választ.
- [ ] A Cursorral készült 36 feladat részletes átnézése.

## Feladatok átnézése – Sándor listája (2026-10-27)

1. [x] toldalek: „Sok alma ?” nyelvtanilag rossz (sok után nincs többes szám; „almat”, „almaban” rossz alakok a visszajelzésben).
2. [x] csoport (szilárd/folyékony/légnemű): csak szöveg, „gagyi” – a kártyákra kép kell.
3. [x] Nagyított (⛶) módban nincs konfetti; a Feladat-próba választáskor visszaugrik normál módba.
4. [x] kocka: magyarázat kell (tipp → 60 dobás → hány 6-os); a próbából küldött válasz a tanárhoz megy és összezavarja.
5. [x] tortcmp: a tábla címe a lecke neve lett (törtes kérdésnél a cím nem lesz a kérdés).
6. [x] recept: a cím cukrot kérdez, a feladat lisztet.
7. [x] fgep: a számokat a végtelenségig be lehet dobni.
8. [x] vizkor: a víz még mindig elválik a parttól.
9. [x] terkep: a házak a vonalon vannak; 9 kocka = 45 km, de csak 5/10/15/20 állítható.
10. [x] Megoldás után „Szuper”, de a Kész gomb ott marad.
11. [x] atom (szénatom): nem egyértelmű, hogy mindegyikből 6 kell.
12. [x] Mobilon néhány feladatnál nem világos, hogyan kell jelölni (pl. tizedes törtek) – később ellenőrizni.
13. [x] oltoz (maci): a meglévő AI-képekből kivágott, a macira pontosan illesztett ruharétegek (static/figurak/maci/reteg) – bármely két ruha együtt felvehető; a mondat minden tanult nyelven. A gőz ikonja 💨 lett (♨️ tűznek tűnt).
14. [x] elolj (valódi AI-képek: cica, asztal, doboz – 2026-10-27): minden tanult nyelven működik (kész), a cica a dobozba „beül” (kész). MÉG HÁTRA: rendes AI-képek (cica, asztal, doboz) – a maci képeivel együtt.
15. [x] binaris: nem egyértelmű – előtte oktatás kell.
16. [x] HIBA: „< F E L A D A T >{…}</FELADAT>” nyersen kint a lapon (szóközös jelölő).
17. [x] tapl (tápláléklánc): „termelő” szó – magyarázat kell, mit jelent itt.

## Új ötletek / bővítések (2026-10-27)

18. [x] ÚJ FELADAT – számkockák (Sándor videója): „? + ? + ? = 9” – a gyerek pöttyös számkockákat (1–5, színesek, egymásra rakhatók) húz a helyükre, aztán „Ellenőrzés”. Tornyokba rakható kockák, mint a Numberblocks-szerű játékokban.
19. [x] Nyelvi feladatok, amik még CSAK angolul vannak: szamangol (számok), idojaras (időjárás), szoba – legyenek németül, franciául, spanyolul is (mint az arcrész, elöljárók, maci).
20. [x] Maci NADRÁG (4 szín) + „Hol a cica?” rendes képek (cica, asztal, doboz): kep_nadrag_cica.py → Claude kivágja, beköti.

21. [ ] ÉRDEKESSÉG-DOBOZ: lecke közben egy kis sárga dobozban egy érdekesség a témához (pl. kétjegyű szorzásnál: hogyan szoroznak Japánban vonalakkal). A tanár adja egy rejtett jelölővel, ritkán (leckénként 1). Minden tantárgyhoz: történelem – „tudtad?”, nyelv – szó eredete, természet – rekord állatok stb.
22. [ ] HÁTTÉR-ÖTLET (Synthesis Tutor mintájára): sötét „űr” háttér a feladattáblán – finom rácsvonal, csillagpöttyök, néhány vonalas rajz (bolygó, távcső, műhold, ufó). Csak ötlet; saját rajzokkal, nem másolva.
23. [ ] A Feladat-próba listába bekerültek az ALAP feladatok is (memória, pizza, óra, párosítás, szám, válaszgomb…) – ezeket is végig kell nézni.

24. [x] Kabalanevek (Bence/Lili – Hugo/Lucía – Robi – Pixi), a szülő átírhatja; az óra elején bemutatkozik, koppintásra biztat.
25. [x] Memória: legfeljebb 12 pár, évfolyam és tudás szerint több (1–2.: 4–6, 3–4.: 6–8, 5.-től: 8–12).
26. [ ] TANÁRI / ISKOLAI változat (ötlet, Landris mintájára): tanárok órát, feladatlapot, dolgozatot készítenek a tantervhez; havidíjas.
27. [ ] Nyitóoldal: a gyerek nevét már ott be lehet írni (Novakid-ötlet), a regisztrációnál előre kitöltve, a gyerekprofil ezzel jön létre. Hosszú kérdőív NEM kell.

28. [ ] SZÜLŐI KIMUTATÁS (KooBits-ötlet): tantárgyanként a készségek színnel – „Mesteri / Biztos / Kezdő / Még nem”, és mennyi van kész a témakörökből. A szülő egy pillantással látja, hol tart a gyerek.
29. [ ] NAPI CÉL: pl. „ma 10 feladat ~20 perc” – csík, ami betelik; a sorozat (streak) már megvan, ehhez köthető.
30. [ ] HIRDETÉS-FORMA (KooBits): rövid, telefonos videó egy szülő szemszögéből – „3 ok, amiért…” – valódi gyerek a gépnél (saját, engedéllyel).
31. [ ] NYITÓOLDAL (DeepSeek-vélemény alapján): 1) első képernyőn egy mondat: „AI-tanár, ami a gyerek tempójában tanít”; 2) ár / mennyi a próba után; 3) 2–3 szülői vélemény a tesztelőktől; 4) adatvédelmi blokk (GDPR, hol tárolódik, mit lát a szülő); 5) felső tagozatnak szóló rész is (8. osztály, történelem); 6) a magyar/spanyol tanterv viszonya egy mondatban.

32. [ ] KÉPES MONDATKIEGÉSZÍTŐ („Composition” lapok mintájára, Sándor képei 2026-10-28): témánként egy nagy, színes kép (Az iskolám, A kisállatom, A családom, A legjobb barátom, Anyukám, Kedvenc ételem, A kertem, Kedvenc évszakom…), alatta 7–8 mondat egy-egy hiánnyal, lent szóbank – a gyerek a szót a helyére húzza/koppintja. MINDEN tanult nyelven (angol, német, francia, spanyol, és magyar anyanyelvi is). A kép felirat NÉLKÜL készül, így minden nyelvhez ugyanaz jó; a mondatok és a szóbank nyelvenként külön. Figyelni: a szóbankban ne legyen ismétlődő szó (a mintában a „My Garden” lapon kétszer van a garden és a flowers).

## FOLYAMATBAN / KÖVETKEZŐ – a sorrend (2026-11-03, Sándor jóváhagyta)

1. [ ] FEJLÉC C2: lépés-gombok (✓ Tanulás › ● Gyakorlás 2/5 › 3 Teszt › 🏆 Kész), a gyerek figurája a mostani lépésen ül; laptopon második sorban, telefonon csak a mostani lépés neve. Mintakép kész, jóváhagyásra vár.
2. [ ] TANÍTÓ TANÁR 3. rész – GYEREKPROFIL: adatbázisba, melyik magyarázat vált be az adott gyereknél (pelda/tabla/hasonlat/lepesek/elozo), a következő órán a tanár ezzel kezd. Az alap már megvan (a „bevalt” mező a session-ben).
3. [ ] TANÍTÓ TANÁR 4. rész – RENDSZERSZINTŰ TANULÁS: név nélkül összesíteni leckénként, melyik magyarázat után válaszoltak jól; bekerül az óratervbe („ha itt elakad, ez működik”).
4. [x] LÁTOGATOTTSÁG-SZÁMLÁLÓ (kész 2026-11-03: /admin/latogatottsag, kizárás: /nem-szamolj): saját (nem külső szolgáltató), IP nélkül, naponta cserélődő kóddal; Sándor gépei/telefonja egy titkos linkkel kizárva; admin oldalon napi látogató, mobil/gép, honnan (Facebook/Google/UTM), hány regisztráció.
5. [ ] FŐOLDAL FRISSÍTÉSE: „A tábla igazodik hozzá” (Játékbolt + kutatói adatlap), „Másképp magyaráz, ha nem érti” (3 lépés), „Azonnal látja, jól csinálta-e” (párosító konfettivel, igaz-hamis magyarázattal).
6. [ ] ÁTDOLGOZNI jelenetes stílusban: hiányzó szó (hianyzo), mondatépítő (epito), szövegjelölő (szoveg).
7. [ ] 6 ÚJ FELADAT: barkochba, ki vagyok, mondatelemző, igeidő-gép, ok-okozat, forrásnyomozó.
8. [ ] ÓRATERVEK: a készítőt felkészíteni a spanyol oldalra, utána egyben magyar + spanyol, és együtt átnézni a hibákat (a feladatok UTÁN, mert a tervek a feladatokból válogatnak).

## Később – ne vesszen el (2026-11-03)

- [ ] AVATAROK a nagyobbaknak (24 db, fele fiús, fele lányos): Nagy nevek (8, kártyával nyílik), Sport (4), Stílus (6), Saját hősök (6). Stílus: matrica (a Nagy nevek esetleg festett). Villám helyett Szikra – a minta futtatásra vár: `python avatar_minta.py --csak villam --ujra`. Valódi focista, Barbie, Marvel/DC NEM lehet.
- [ ] SAJÁT AVATAR-ÉPÍTŐ bővítése a nagyobbaknak (fénykép-feltöltés helyett): szemüveg, sapka, fejhallgató, mez, dzseki, több frizura.
- [ ] FACEBOOK-BORÍTÓ a zsiráfos képből (1640×624, a lényeg középen).
- [ ] SPANYOL megosztási kép (og_es3) a magyar mintájára – amikor lesz spanyol Facebook-oldal.
- [ ] FACEBOOK-HIRDETÉS: a weboldalra vigyen (nem az oldal-kedvelésre); UTM-címkével, hogy a számláló lássa, hányan jöttek és regisztráltak. Meta Pixelhez sütis hozzájárulás kellene – előbb a saját számláló.
- [ ] TÖBB FELADAT minden tantárgyhoz, csak olyan, amiből tanul a gyerek: helyesírás-választó („melyik írás helyes?”), igepárok képpel (eat – ate), mondatkiegészítő képpel (az „English With FK” lapok mintájára, minden nyelven); fizika és kémia (mérés, kísérlet lépései, anyagok tulajdonságai); testnevelés (képsor vagy rövid videó a gyakorlat bemutatására).
- [ ] KÖLTSÉG: a gyakorló felületek egy hívásban sok tételt küldenek a tanárnak (pl. 4 igaz-hamis = 1 hívás) – ezt kihasználni, hogy kevesebb tanári hívás legyen gyerekenként.
- [ ] ADATVÉDELMI TÁJÉKOZTATÓ: beírni, hogy a nyilvános oldalakon név és IP-cím nélküli, naponta cserélődő kóddal számoljuk a látogatást (jogos érdek, nincs követés, nincs külső szolgáltató).
- [ ] HIRDETÉSI VIDEÓ: rövid (6–8 mp) „életre kelő” nyitókép a zsiráfos képből Google Veo 3.1 Fast-tal (Gemini API, kép→videó, ~0,12 $/mp), utána a valódi felvételek; a végén az oldalra irányít. (A Sora API 2026.09.24-én megszűnt.)
- [ ] TANÁR-MODELL TESZT: Claude Haiku 5.5 (0,10 $ / 0,50 $ – kb. 7× olcsóbb a gpt-5.4-mininél, a BenchLM-ben hasonló pontszám). tanar_teszt.py-jal lemérni (Anthropic-kulcs kell, OpenAI-kompatibilis cím: https://api.anthropic.com/v1/), főleg a MAGYAR nyelvhelyességet nézni.
- [ ] MICROSOFT CLARITY (Sándor kérte, 2026-11-04): visszanézhető látogatások, hőtérkép, „dühös kattintás”. Ingyenes. Feltétele: sütiablak (csak elfogadás után indul), adatvédelmi tájékoztató bővítése (Microsoft mint adatfeldolgozó), CSAK a nyilvános oldalakon (főoldal, csomagok, regisztráció), beírt adatok kitakarva, gyerekoldalakon soha. Sándornak a clarity.microsoft.com-on regisztrálnia kell (azonosító). A saját kattintás/görgetés-mérés már kész – ez a következő lépcső.
- [ ] REELS NYITÁS: a nézők 4 mp-nél lapoztak tovább (átlag 3 mp). Új változat: az első 1 mp-ben mozgás/kérdés („Van gyereked 1–8. osztályban?”), a telefon 1 mp-en belül jelenjen meg.

## fix155 – Fizetés előtti jogi kötelezők (2026-11-16, MIELŐTT élesedik a fizetés)
- [ ] Arányos visszatérítés elálláskor (2011/83 EU irányelv 14. cikk (3)): a felhasznált percek / csomag össz. perc arányában tartunk meg, a többit 14 napon belül, ugyanazzal a fizetési móddal (13. cikk). Ha NINCS meg a kifejezett kérés + tudomásulvétel pipa → a szülő SEMMIT nem fizet (14. cikk (4)).
- [ ] Fizetés előtti 2 pipa (kötelező, nem lehet előre bepipálva):
  HU: "Kérem, hogy a szolgáltatás az elállási határidő (14 nap) lejárta előtt azonnal induljon." + "Tudomásul veszem, hogy ha a 14 napon belül elállok, a már felhasznált percek arányos díját meg kell fizetnem, és a szolgáltatás teljes teljesítése után elállási jogomat elveszítem."
  ES: "Solicito expresamente que el servicio comience de inmediato, antes de que finalice el plazo de desistimiento de 14 días." + "Acepto que, si desisto dentro de los 14 días, deberé abonar la parte proporcional de los minutos ya utilizados, y que pierdo el derecho de desistimiento una vez el servicio se haya prestado por completo."
- [ ] Fizetés gomb felirata: "Fizetési kötelezettséggel járó megrendelés" / "Pedido con obligación de pago" (8. cikk (2)).
- [ ] Visszaigazoló e-mail a pipák tartalmával + ÁSZF + elállási tájékoztató (tartós adathordozó, 8. cikk (7)).
- [ ] ELÁLLÁS GOMB (2023/2673 irányelv, új 11a. cikk, 2026-06-19-től kötelező): "Elállás a szerződéstől itt" / "Desistir del contrato aquí" – jól látható, a 14 nap alatt végig elérhető (Fiókom + lábléc). Lépései: név, melyik csomag/előfizetés, e-mail → "Elállás megerősítése" gomb → automatikus visszaigazoló e-mail dátummal/idővel. A fióktörlés gomb NEM helyettesíti.
- [ ] Árak: áfával/IVA incluido kiírás a csomagok oldalon (HU+ES) – ellenőrizni. Euró HU-nak: EU-jog szerint OK; magyar árfeltüntetési szabály (4/2009 NFGM-SZMM r.) pénznem-kérdése NEM ellenőrzött → gestoría/HU könyvelő kérdés.
- [ ] (fix156) Jelenleg NINCS fizetési rendszer a kódban (nincs Stripe) → a fióktörlés most nem érint fizetést. Stripe bevezetésekor: fióktörlés = Stripe előfizetés automatikus lemondása is (különben tovább vonna le!).
- [ ] (fix156) ÁSZF 8. pont pontosítása (HU+ES): "a felhasznált tanulási percek arányában" (most: "ameddig rendelkezésedre állt"), + az e-mail mellé az online "Elállás a szerződéstől itt" gomb.
- [ ] (fix156) Elállás: a rendszer számolja ki a visszajáró összeget (fizetett × (1 − felhasznált perc / csomag perc)), admin oldalon 1 kattintás a Stripe részleges visszatérítéshez. Határidő: 14 nap az elállás beérkezésétől.
- [ ] (fix156) Csomagok oldal: az ár mellé "áfával" / "IVA incluido" (most egyik nyelven sincs kiírva). HU ÁSZF-ben sincs áfa-mondat (ES-ben van).
- [ ] (fix156) Admin számláló: nem spanyol EU-s vevők éves bevétele (a 10 000 €-s OSS-határhoz); figyelmeztetés 8 000 €-nál.
- [ ] (fix157) Fiókom oldalon 3 külön gomb: "Előfizetés lemondása" (nincs több levonás) · "Elállás a szerződéstől itt" (csak a vásárlástól 14 napig látszik, arányos visszatérítés) · "Fiók törlése" (marad; jelszó + figyelmeztetés: "Aktív előfizetésed van, a törlés azt is lemondja, a maradék perc elvész").
- [ ] (fix157) Elállás → automatikus e-mail Sándornak (Resend) a kiszámolt összeggel + admin "Jóváhagyom" gomb → Stripe részleges visszatérítés. Kezdetben mindig kézi jóváhagyás (pénz-kód), később esetleg automatikus kis összegnél.
- [ ] (fix157) HU oldalon forint ár? A magyar pénznem-szabály NEM ellenőrzött → legbiztosabb: HU-n Ft-ban árazni (Stripe tud HUF-ot). Gestoría/HU könyvelő döntse el.
- [x] (fix157→fix158 KÉSZ: AGENTS.md lett) Rövid PROJEKT_LEIRAS.md a repó gyökerébe (felépítés, fő fájlok, tilalmak, tesztelés) → minden új munkamenet olcsóbb, kevesebb keresés az 1 MB-os app.py-ban.
- [ ] (fix157) Fizetés előtt: automata teszt a pénzes utakra (fizetés, lemondás, elállás, visszatérítés, fióktörlés). Ellenőrizni: Railway-en milyen adatbázis fut (helyi teszt SQLite-on megy).
- [ ] (fix158) Gombok alatti magyarázó szöveg (Fiókom):
  Lemondás: "A hónap végéig használhatod, utána nem vonunk le többet. Visszatérítés nincs." / "Puedes usarlo hasta fin de mes; después no se cobra más. Sin reembolso."
  Elállás (csak 14 napig): "Azonnal megszűnik, a fel nem használt percek arányos részét 14 napon belül visszautaljuk." / "Se cancela ya; te devolvemos la parte proporcional de los minutos no usados en 14 días."
  Fióktörlés: "Minden adat törlődik (gyerekprofilok, haladás, album), az előfizetés is leáll. A számlákat a törvény miatt megőrizzük." / "Se borran todos los datos…; las facturas se conservan por obligación legal."
- [ ] (fix158) SZÁMLÁK MEGŐRZÉSE fióktörlés után is (spanyol könyvelési szabály, gestoríával pontosítani az évek számát). database.delete_parent_account NE törölje a számlákat; adatvédelmi tájékoztatóba + adatkezelési nyilvántartásba beírni (jogalap: jogi kötelezettség, GDPR 6(1)(c), 17(3)(b)).
- [x] (fix158) AGENTS.md frissítve projekttérképnek (régi: 2026-09-03).
- [ ] (fix158) Your Europe Advice levél elküldve? (forint, áfa-kiírás, arányos visszatérítés, számlamegőrzés vs. törlés) – a válasz alapján frissíteni.
- [x] (fix159) Látogatottság oldalon „Ma” (1 nap) nézet.
- [ ] (fix159) Élő adatbázis = PostgreSQL, helyi teszt = SQLite → a pénzes teszteket PostgreSQL-en is futtatni (pl. a próba adatbázis másolatán).
- [x] (fix161 KÉSZ: tölcsérben „Mintaleckét kezdett / Végigcsinálta”, évfolyamonként, forrásonként; /minta oldal is számít) MÉRÉSI VAKFOLT: a főoldali gomb már a mintaleckére visz, de a mintalecke oldalak (mintalecke_valaszt, mintalecke) NINCSENEK a _LATOGATAS_OLDALAK-ban, és a tölcsérben sincs „elkezdte / befejezte a mintaleckét” sor (a minta_vege esemény rögzül, de nem látszik). Pótolni: tölcsér = megnyitotta → mintaleckét kezdett → befejezte → regisztrált.
- [ ] (fix160) Látogatottság 11.12–16 (hirdetés nélkül): 38–63 látogató/nap, többség „közvetlen”, főoldalon medián 3 mp; Google csak 2–4/hét (új domain, SEO hónapok alatt hat). /login sok közvetlen belépés.
- [ ] (fix160) Sorrend: 1) spanyol szülői oldalak magyar szöveg-ellenőrzése (Gyerekeim, Fiókom, riport e-mail, regisztráció utáni lépések) 2) spanyol URL-ek (/es/precios stb. + átirányítás) 3) havi 1 hasznos blogcikk HU+ES 4) GEO: őszinte katalógus-bejegyzések (AI-eszköz listák, szülői fórumok nyílt bemutatkozással).
- [x] (fix162) Spanyol szülői oldalak ellenőrizve (Gyerekeim, Fiókom, gyerek hozzáadás/szerkesztés, feladatok, album, bolt, PIN, jelszó, regisztráció, belépés): nincs magyar szöveg. Hibák javítva: 1) a heti/napi szülői jelentés az ALAP_NYELV szerint ment (spanyol szülő MAGYAR levelet kapott volna) → most a gyerekek tanterve szerint; 2) tasak bontása után a régi magyar „Kártyák” listára vitt → most a Gyűjtőalbumra.
- [ ] (fix162) A Fiókom oldalon a 🧪 próbagombok magyarul vannak – csak próbaoldalon látszanak, élesen nem. Maradhat.
- [x] (fix163) SPANYOL URL-ek: /es/precios, /es/registro, /es/iniciar-sesion, /es/preguntas-frecuentes, /es/privacidad, /es/condiciones, /es/aviso-legal, /es/como-funciona, /es/clase-de-prueba(/1–6), /es/recuperar-contrasena, /es/blog/como-ayuda-la-ia-al-aprendizaje-de-los-ninos. A régi /es/csomagok stb. 301-gyel átirányít. Sitemap + hreflang + robots (/es/ privát oldalak tiltva) frissítve. Ki: nyelv_utvonal.SPANYOL_CIMEK = {}.
- [x] (fix163) HIBA JAVÍTVA: a spanyol oldalak kanonikus címe (canonical, og:url) eddig a MAGYAR címre mutatott → a Google a spanyol lapot a magyar másolatának tekintette. Most a spanyol címre mutat.
- [ ] (fix163) Élesítés után: Search Console → Sitemaps → sitemap.xml „Újraküldés”; 1–2 hét múlva megnézni, hogy a /es/precios stb. indexelve van-e (URL-ellenőrzés).
- [x] (fix164) Szülői oldalak spanyol címe: /es/panel, /es/mi-cuenta, /es/pin-parental, /es/hijos/nuevo (a gyerekek /children/… oldalai szándékosan maradnak – chat-kockázat, keresőnek láthatatlan). PIN utáni visszatérés: előtaggal, üres „?” nélkül.
- [x] (fix164) Levelek nyelve gyerek nélküli szülőnél: eddig MINDIG magyar (emlékeztető, keretlevél, jelentés) → most a regisztráció nyelve (erdeklodes_nyelv oszlop, ha üres). Korábban regisztrált, gyerek nélküli szülőknél nincs adat → magyar marad.
- [x] (fix165) Spanyol oldalon MINDEN látható cím spanyol: /es/hijos/5/clase, /es/hijos/5/tareas, /es/hijos/5/tienda, /es/hijos/5/editar, /es/salir, /es/idioma/hu, /es/baja/…, /es/confirmar/…, /es/restablecer-contrasena/…, /es/no-medir. A levelek linkjei is a levél nyelvén. A régi címek 301-gyel átirányítanak. Chat-teszt: az üzenetküldés útvonala működik (helyben csak az AI nem érhető el).
- [x] (fix165) HIBA: a spanyol oldalon az admin Feladat-próba listája üres volt (a csak-magyar „egyenlet” típus miatt hibára futott). Javítva.
- [ ] (fix166) SPANYOL FACEBOOK-OLDAL (Sándor holnap nyitja; másolni nem lehet, csak új oldal). ELŐTTE Claude: spanyol bemutatkozó szöveg + profil- és borítókép a meglévő spanyol képekből. HA SÁNDOR SZÓL, HOGY KÉSZ („kész a spanyol face”): 1) a spanyol oldal láblécében/linkjeiben a spanyol FB-oldal legyen (a magyar maradjon), 2) a forrás-mérésben külön látsszon (fb_fooldal_es), 3) og-kép/megosztás ellenőrzése spanyol linkkel.
- [ ] (fix166) Látogatottság nyelv szerint kettéválasztva (magyar vs. spanyol oldal) – IP NÉLKÜL: a meglátogatott oldal nyelve (/es/ előtag) alapján. Ország szerint csak ha kell: Cloudflare ország-fejléc (IP-t nem tárolunk), de akkor az adatvédelmi tájékoztatót is bővíteni kell.
- [ ] (fix166) Search Console: sitemap újraküldése = a „Új webhelytérkép hozzáadása” mezőbe beírni: sitemap.xml → Elküldés (külön gomb nincs). Utána URL-ellenőrzés: https://tutoriacademia.com/es/precios.
- [x] (fix167 KÉSZ) Diktálás/dictado feladattípus (1–4. o., HU+ES): a meglévő „hallas” típus felolvasását használná → Sándor OK-ja kell (felolvasás = hangos keret/költség).
- [x] ~~(fix166) Jorge: rövid üzenet~~ – ELVETVE (Sándor, 11-22: nem akarja zaklatni).
- [x] (fix167) TOLLBAMONDÁS / DICTADO feladat: Feladat-próba név „tollbamondás (diktálás)” / „dictado”, 1–4. osztály, magyar nyelv + Lengua (spanyol oldalon is működik). Felolvassa a mondatot (🔊 újrahallgatás ingyen, a böngésző tárából), a gyerek leírja, szóról szóra ellenőriz, megmondja a hiba fajtáját (nagybetű, írásjel, ékezet, ly/j, hosszú mássalhangzó; ES: b/v, h, ll/y, c/z/s, g/j), 1 javítás, utána megmutatja a jót. Ha ma elfogyott a felolvasás: nem indul, a tanár másik feladatot ad. Tanárnak megy: pontszám + hibalista.
- [ ] (fix167) Később: diktálásnál a hibalistát a szülői jelentésbe is („ezekben a szavakban hibázott”) – csak ha Sándor kéri.
- [ ] (fix167) Search Console: „Átirányítást tartalmazó oldal” = SZÁNDÉKOS (régi /es/csomagok → /es/precios, http → https). Nem kell javítani.
- [x] (fix168) Tollbamondás javítások: 💡 „Mutasd, mi a hiba” gomb (első hiba után; a beíró mező ALÁ írja szavanként: amit írt → ahogy helyes, a rossz betűk kiemelve); a szavak párosítása hasonlóság szerint (hoy ↔ Hoy); elsőre hibátlan mondatnál ünneplés („Szuper!”). Idegen nyelvórán is (HU és ES oldal), a célnyelven.
- [ ] (fix168) Kipróbálni valódi eszközön: iPhone (Safari) – az első automatikus felolvasást az iPhone letilthatja koppintás előtt; a 🔊 gomb működik. Android Chrome, Windows/Mac böngésző.
- [x] (fix169) Tollbamondás: a hibás szóban CSAK a rossz betű piros, és ahol betű/írásjel hiányzik, ott kis szaggatott „?” (nem az egész szó aláhúzva). Feladat-próbán idegen nyelvórán (angol/német/spanyol/francia) a próba mondata a tanult nyelven.
- [ ] (fix169) Ötlet (Sándor): a 💡 segítség lehetne fokozatos (1. nyomás: csak a hiba fajtája, 2.: a betű) – csak ha a gyerekeknél kell.
- [ ] (fix170) iPhone/iPad TESZT (Sándornak nincs ilyen eszköze): BrowserStack vagy LambdaTest ingyenes próba → valódi iPhone Safari. Ellenőrizni: főoldal + mintalecke kinézete; regisztráció; chat 🔊 felolvasás (az ELSŐ hang csak koppintás után szólhat – iOS szabály); hangos mód mikrofon-engedély és beszéd → szöveg; diktálás 🔊 + beírás; album, tasakbontás. A program NEM a böngésző beépített beszédfelismerését használja, hanem szerveroldali felismerést és hangfájlt – ez iOS-en megbízhatóbb.
- [x] (fix170) Diktálás: „figyeld meg a piros betűket / letras en rojo” (eddig „szavakat”). Javítási kör: 1. hiba → egyszer javíthat (💡 segítséggel is), 2. hiba → megmutatja a jót, tovább. HU és ES ugyanígy.
- [ ] (fix171) ‼️ NAGYON FONTOS – iPhone/iPad teszt BrowserStacken (lásd fix170 lista). Ha Sándor regisztrált: Claude lépésenként végigvezeti. Enélkül az iPhone-os/iPades szülőket elveszíthetjük.
- [ ] (fix171) ‼️ SPANYOL TANÁRTESZT (Sándor spanyolul nem tudja ellenőrizni → Claude olvassa el a teljes spanyol beszélgetéseket is, nem csak az AI-ellenőrzőt, és magyarul foglalja össze). Utolsó: 2026-11-11, gpt-5.4-mini, csak 3 óra → 5 biztos hiba (jó választ kijavított; válasz a kérdésben; „cuidar la comida”; 3-at ígér, 4-et mond). Terv: 1) Sándor megírja, mi a MODELL_TANAR a Railway élesen; 2) `python tanar_teszt.py --oldal es` (8 óra, ~1–2 €) az éles tanárral; 3) ugyanaz egy erősebb jelölttel → összevetés (ár + hibaszám); 4) a hibák javítása a spanyol promptban, KÜLÖN lépésben, majd UGYANAZZAL a paranccsal újramérés. Spanyol szempontok: spanyolországi spanyol (ordenador, vosotros, „cole”), LOMLOE-tartalom, évfolyamnak megfelelő, tizedesvessző, nincs magyar szó/szokás, a jó választ nem javítja ki.
- [x] (fix171) Spanyol Facebook-oldal szövegei megadva (név, kategória, ≤100 karakteres bemutatkozás, hosszú „Información” szöveg).
- [x] (fix172) tanar_teszt.py: spanyol oldalon GÉPI ellenőrzés is (tizedespont, latin-amerikai szavak, „ustedes”, magyar szó a spanyol órán). Az órák kiválasztása fix (seed 12345) → két tanármodell UGYANAZOKAT az órákat kapja, összevethető. Éles tanár: MODELL_TANAR nincs a Railway-en → a kód alapértéke: gpt-5.4-mini.
- [ ] (fix172) Kimi-ötlet, később: előre megírt „csapda-órák” (a gyerek tökéletesen válaszol → kijavítja-e; magyar szót ír; tizedes) – ha a sima teszt után még kell.
- [x] (fix173) SPANYOL TANÁRTESZT eredménye (2026-11-17, 8 óra, ugyanazok az órák): gpt-5.4-mini 12 biztos + 9 gyanús, 0,73 $, 2,8 mp/válasz · gpt-5.4 14 biztos + 12 gyanús, 6,8 mp/válasz, drágább. Gépi spanyol hiba (tizedespont, latin-amerikai szó, magyar szó) egyik sem. Döntés-javaslat: MARAD a gpt-5.4-mini. Claude átolvasta: a spanyol jó, főleg apró tükörfordítások; több „biztos” hiba a TESZT hibája volt.
- [x] (fix173) tanar_teszt.py javítva: a teszt-gyerek eddig NEM látta a „szám” feladat szövegét és az interaktív feladatok adatait (pl. csoportosítandó elemek) → téves „hiányzik a feladat” hibák. Most látja.
- [x] (fix173) Spanyol prompt: „esto se escribe así de corto” (tükörfordítás, a tanár szó szerint mondta) → „Con la fórmula… / En matemáticas se escribe así…”.
- [ ] (fix173) Újramérés UGYANAZZAL a paranccsal (`python tanar_teszt.py --oldal es`, gpt-5.4-mini) a javítások után.
- [x] (fix174 KÉSZ, HETENTE hétfőn 11:13) Modell-figyelő ütemezett feladat: OpenAI kivezetések/új modellek/árak → Sándornak értesítés; új modellnél tanárteszt-javaslat.
- [x] (fix174) Újramérés (13:42, gpt-5.4-mini): 13 biztos + 8 gyanús – DE 6 ebből a teszt hibája volt (a feladatadatokat JSON-ként mutatta → „technikai szemét”, „nyelvet váltott”). Javítva: olvasható felsorolás. „manejar” kivéve a latin-amerikai listából (Spanyolországban is jelent „kezelni”-t).
- [x] (fix174) FONTOS: a tanárteszt eddig a TANITO_PONTOS blokk NÉLKÜL mérte a tanárt, pedig élesen BE van („annyit sorolj, amennyit ígérsz”, „jó választ ne javíts ki”) → a „3-at ígér, 4-et mond” hibák részben ezért jöttek. Most a teszt is hozzáfűzi (TANITO_PONTOS=0 → nélküle).
- [x] (fix174) Spanyol TANITO_PONTOS blokk bővítve: természetes spanyolországi mondatok („mejor”, nem „más bueno”), good evening = buenas tardes / good night = buenas noches.
- [ ] (fix174) ‼️ SPANYOL MINŐSÉG – Sándor: a spanyol piac nagyobb, a minőség az első, tesztre max. ~20 € mehet. Következő: újramérés (8 óra, ~0,7 $), aztán TELJES spanyol kör `python tanar_teszt.py --oldal es --mind` (minden tárgy × évfolyam, becslés ~4–6 $) → Claude elolvassa, magyar összefoglaló, javítás, újramérés.
- [ ] (fix174) MARKETING spanyolul: Facebook-bejegyzések (spanyol oldal), rövid videók, Pinterest – terv + szövegek.
- [ ] (fix174) PLUSZ LECKÉK / óratervek a spanyol oldalra (oratervek/ csak HU 4. o. matek van) – mely tárgyak/évfolyamok elsőként?
- [ ] (fix174) SPANYOL KÁRTYÁK befejezése (26 kártya; 10 újra: Torres, Peral, Lorca, Las Casas, Elcano, Firnas, Azarquiel, Goya, Sorolla, Albéniz – Goya_2, Albéniz_2, Peral_2 elfogadva; Sorolla_3-on halvány „Fig. 22”). Képgenerálás pénzbe kerül – Sándor dönt.
- [x] (fix174) Felolvasás: a FŐ hang az Azure (Noémi / Elvira), az OpenAI gpt-4o-mini-tts csak tartalék. A diktálás költsége ezért az Azure árán megy (kb. ugyanannyi vagy kevesebb).
- [x] (fix175) Spanyol újramérés (14:53, gpt-5.4-mini, TANITO_PONTOS-szal): 4 biztos + 9 gyanús (előtte 12–13 biztos). Maradt: „¡Sí, verdad!”, „venir al juego” → prompt; „Hello! How are you?” válaszlehetőség hiányzott. Teszt-javítás: a felszólító feladat („Dime…”, „Mondj…”) nem számít „nincs kérdés”-nek; a listában lévő számok (🍎 4) is látszanak.
- [ ] (fix175) Teljes spanyol kör: `python tanar_teszt.py --oldal es --mind` (38 óra; becslés 3,5–12 $, Sándor egyenlege 16,09 $). Utána Claude elolvassa.
- [ ] (fix175) ÚJ FUNKCIÓ ötlet: a szülő NAPI tanulási időkorlátot állíthasson gyerekenként (most NINCS ilyen – Claude tévesen állította). Tanároknak/szülőknek (pl. Jorge) erős érv.
- [ ] (fix175) Árazás ötlet: „annyit fizet, amennyit tanul” – a perccsomagok (bono) már ilyenek; utólagos percdíj jogilag lehetséges, de bonyolultabb (kártya mentése, havi számla). Döntés fizetés előtt.
- [x] (fix176) TELJES spanyol kör (38 óra, 15:11): 37 biztos + 41 gyanús (~1 jelzés/óra, egy része téves). Tanár ára a jelentés szerint 3,50 $ gyorsítótár NÉLKÜL – a valós OpenAI-költség 1,15 $ volt (a gyorsítótár miatt). FONTOS VALÓDI HIBA: a tanári válaszok ~3%-ában (7/228) hiányzott a </FELADAT> → a gyerek nyers kódot látott. JAVÍTVA mindkét oldalon (_feladat_zar: a JSON végénél pótolja). A „magyar szó” gépi találat ennek a mellékterméke volt (a „FELADAT” szó).
- [ ] (fix176) A teljes kör AI-ellenőrzős listájának (37 biztos) átnézése Claude-dal típusonként → prompt-javítások, majd újra --mind.
- [ ] (fix176) LOMLOE kiírás: „Basado en el currículo de la LOMLOE (RD 157/2022)” rendben; NEM szabad: „oficial”, „homologado”, „aprobado por el Ministerio”. Oldalakon ellenőrizni.
- [x] (fix177) Teljes kör típusonként: 16 biztos „idegenszerű spanyol” (apró), 9 „technikai szemét” (főleg a hiányzó </FELADAT> – javítva fix176; plusz a teszt 350 karakternél levágta a feladatot → most 1200), 5 TÉNYBELI: „18 no es divisible entre 2” (!), kontrollkísérlet rossz példa, ever/never „sí”, levél erezete, „buenas noches, todos”.
- [ ] (fix177) TÉNYBELI botlások ellen ötlet: matek/természettudomány órán reasoning_effort „medium” a tanárnak (drágább, lassabb) – előbb tanárteszttel mérni (`--tantargy Matem --oldal es`).
- [x] (fix178) Spanyol matek (6 óra, low): 7 biztos + 8 gyanús. VALÓDI: a tanár mondat közben javítja ki magát („71 … 7 decenas … espera, aquí hay que mirar bien”), „Compueso”, „20, 30 = una decena”. Új kapcsoló: TANAR_EFFORT (low/medium/high, alap low) – a tanár gondolkodási ideje. Mérés: `$env:TANAR_EFFORT="medium"; python tanar_teszt.py --oldal es --tantargy Matem --mind` → összevetni a low-val (hibák + ár). Ha jobb: Railway TANAR_EFFORT=medium.
- [x] (fix178) Teszt: a táblán látható adatoknál nincs kulcsnév („szam 624” téves nyelvváltás-riasztás volt).
- [ ] (fix178) Facebook ES bemutatkozó (255 karakter): rövidített változat megadva, magyar tanterv említése nélkül.
- [x] (fix179) Kimi 2.7 javaslata alapján ELSŐ lépés (ingyenes, nem lassít): TANITO_PONTOS blokk (HU+ES) – „gondold végig előbb, ne javítsd ki magad a gyerek előtt, ellenőrizd a példák számait”. Tanárteszt gépi jelzés: [önjavítás]. TANAR_EFFORT kapcsoló marad, alap low (nem változtat).
- [ ] (fix179) Mérés: `python tanar_teszt.py --oldal es --tantargy Matem --mind` (low) → összevetni a 15:49-es 7 biztos hibával. Ha marad tárgyi hiba: 2. lépés – olcsó ellenőrző hívás csak matek/természettudomány órán (Kimi ötlete), VAGY TANAR_EFFORT=medium csak matekra; mindkettőnél a válaszidőt mérni.
- [ ] (fix179) Kimi „temperature 0,2” ötlete: a gpt-5.4-mini gondolkodó modell, ott (tudomásunk szerint) a temperature nem állítható → nem alkalmazható. Helyesírás-ellenőrző (LanguageTool): 228 válaszból 1 elírás – most nem éri meg.
- [x] (fix180) Matek-újramérés (17:08, low, önjavítás-tiltással): önjavítás 0 (MŰKÖDIK). 11 biztos, ebből ~4 a teszt hibája (a választós feladat KÉRDÉSÉT a teszt-gyerek nem látta – javítva). Valódi: magabiztos tévedés („531 > 528, porque 1 unidad es más que 8”), criba pontatlan, rossz feladattípus (6430 felbontása → dobókocka; „¿Cuánto vale IX?” → „Escribe 9”), idegenszerű „¿qué cifra vale las centenas?”. Szabályok bővítve (HU+ES): bizonytalan példát ne állíts; összehasonlításnál az első eltérő számjegy; a FELADAT pontosan azt kérje, amit a kérdés.
- [ ] (fix180) Következő mérés: low újra (`--tantargy Matem --mind`), majd medium (`$env:TANAR_EFFORT="medium"`) → döntés a válaszidő és a hibák alapján.
- [ ] (fix180) SEO (Cursor fix152/153: címek, JSON-LD, spanyol blog) Sándor szerint NINCS élesen – ellenőrizni: `git status`, `git log --oneline -5`, `git log origin/main --oneline -5`.
- [ ] (fix180) Facebook ES „Hivatkozások”: „Prueba una clase gratis” → https://tutoriacademia.com/es/clase-de-prueba
- [x] (fix181) MATEK low vs medium (spanyol, 6 óra, fix180 után): low 17:28 → 12 biztos (köztük TÁRGYI: „0–5-re végződő lefelé kerekít”, „7.041-ben nincs tízes”, „a négyzet kétszer szorozza önmagát”, és újra önjavítás „espera”), 2,9 mp; medium 17:32 → 4 biztos, 0 önjavítás, 5,8 mp, ár +13% (0,654 vs 0,579 $). Új kapcsoló: TANAR_EFFORT_MATEK (csak matekórán). JAVASLAT: Railway (proba+main) TANAR_EFFORT_MATEK=medium.
- [ ] (fix181) Más tárgyakra (Conocimiento, Lengua) is mérni a medium-ot, ha ott is maradnak tárgyi hibák.
- [ ] (fix181) „OKOS TANÁR” ötlet (Sándor): gyerekenkénti tanulóprofil – a visszatérő hibák (EREDMENY:rossz, diktálás hibalista) eltárolva, és a promptba: „ebben gyenge, magyarázd másképp (rajz, példa, lépésekre bontva)”. Nagyobb fejlesztés, előbb terv.
- [x] (fix181) Facebook ES hivatkozás: a főoldal (https://tutoriacademia.com/es/) – NEM a /es/pin-parental… cím (az belépés utáni oldal).
- [x] (fix182) TANAR_EFFORT_MATEK most matek ÉS természettudomány (Conocimiento, Ciencias, Fizika, Kémia, Biológia, Környezet, Földrajz) órán hat. Railway-en MÉG NINCS beállítva → most mindenhol low.
- [x] (fix182) Éles ES főoldal ellenőrizve: minden link spanyol (/es/precios, /es/registro, /es/clase-de-prueba…). A „Salir” → /es/pin-parental?tovabb=/es/salir SZÁNDÉKOS (kilépéshez szülői PIN kell, hogy a gyerek ne lépjen ki).
- [ ] (fix182) ES főoldal lábléc Facebook-linkje még a MAGYAR oldalra mutat (profile.php?id=61594854042337?) → a spanyol FB-oldal címére cserélni (Sándor küldje el a spanyol oldal linkjét).
- [ ] (fix182) Spanyol hirdetés: Sándor küldje a két magyar videó hirdetési eredményét (Hirdetéskezelő: megjelenés, kattintás, CTR, kattintásonkénti ár) → a jobbat spanyolul elkészíteni. Előtte ajánlott: iPhone-teszt (BrowserStack).
- [x] (fix183) Spanyol lábléc Facebook-link → a spanyol oldal (profile.php?id=61596506557900), a magyar marad. A „?tovabb=” paraméter a spanyol címekben „?volver=” (a régi is működik). Alaposabb tanár (TANAR_EFFORT_MATEK) HANGOS módban NEM kapcsol be (élőszóban a 6 mp csend sok).
- [ ] (fix183) Railway: TANAR_EFFORT_MATEK=medium a PROBA service-nél is (élesen Sándor beállította 11.17).
- [ ] (fix183) Hirdetés: a kampánylista nem mutatja videónként – a kampányon belül „Hirdetések” fül kell (melyik videó hány kattintás). Eddig: kattintás olcsó (0,07–0,09 €/érkezés), a gond a regisztráció.
- [x] (fix184) Esti (anyukás) videó SPANYOLUL kész: kinézet képek/facebook/hirdetes/tutoria_reel_este_es.mp4 (18 mp, 4:5). Szövegek: „Ha sido un día largo. / Sin fuerzas. / Y aún quedan los deberes… / El profe de TutorIAcademia se sienta con tu hijo. / Explica paso a paso y espera su respuesta. / Mientras, tú descansas. / Y por correo ves qué ha aprendido. / 120 minutos gratis, sin tarjeta, tutoriacademia.com/es”. Képernyő: valódi spanyol áramkör-feladat. Javítva a magyarhoz képest: „TutorIA” → „TutorIAcademia”.
- [ ] (fix184) Zsiráfos videó SPANYOLUL: a régi összerakó szkript nincs meg → újra kell építeni: spanyol képernyőfelvételek (csoportosító „polc”, kutatói adatlap, igaz/hamis), a táblán „1–8. osztály” helyett „1.º–6.º”, csoportok: 1.º–3.º / 4.º–6.º, záró: „Profesor particular con IA · 1.º–6.º de Primaria”.
- [ ] (fix184) iPhone-teszt (BrowserStack, iPhone 15 Pro, iOS 17, Safari): a spanyol főoldal RENDBEN. Ingyen eszközönként 1 perc → következő eszközökön: /es/clase-de-prueba/2 végig, majd /es/registro.
- [ ] (fix184) ELLENŐRIZNI: a chat felső sávja kb. 1000 px szélességnél (fekvő tablet) összenyomódik („N… Matemáticas / Profesor de IA / Nivel 1 / Quedan 180 minutos…” egymás alatt) – helyben, próbagombokkal láttam; élesen, tableten megnézni.
- [x] (fix185) Zsiráfos videó SPANYOLUL kész: kinézet képek/facebook/hirdetes/tutoria_reel_zsiraf_es.mp4 (26 mp, 4:5). „No es tu hijo quien tiene que llegar a la pizarra. / Aquí la pizarra se adapta a él.”, táblán „1.º–6.º PRIMARIA”; „Para los pequeños · 1.º–4.º – Jugar en la estantería”; „Para los mayores · 5.º–6.º – El mismo tema, como ficha de investigación”; „¿Verdadero o falso? – Ve al instante si ha acertado — y también por qué.”; záró: „Profesor particular con IA · 1.º–6.º de Primaria · Explica a cada niño a su medida · Pruébalo gratis · tutoriacademia.com/es”. Valódi spanyol feladat-képernyők a programból. Összerakó: Claude felhőben (reel_zsiraf_es.py, cap.py).
- [x] (fix185) HIBA a spanyol feladatokban (videókészítés közben derült ki): a játékbolt felirata („¡Saca los juguetes de la cesta…”) túl hosszú volt, rácsúszott a kártyákra → „¡Pon los juguetes en la estantería!”; a kutatói táblán telefonon az „invertebrado” kilógott → törik, kisebb betű.
- [x] (fix185) Meta „Követés” (képpont/Pixel): NEM kapcsoljuk be – „nincs követő süti” ígéret; a saját mérésünk a Facebook-forrást enélkül is látja.
- [ ] (fix185) BrowserStack: a SmartBear (BitBar) oldal NEM a BrowserStack – a browserstack.com/users/sign_in → Live.
- [x] (fix186) Látogatottság NYELV SZERINT (Sándor 11.16-án kérte): a napi táblában „ebből 🇪🇸” oszlop, a tölcsér alatt Magyar/Spanyol sor (látogató, mintalecke, reg. oldal, regisztrált). IP nélkül: az /es/ előtagot tároljuk az útvonalban. 11.18 előtti adatoknál a spanyol nem látszik külön (akkor még nem tároltuk).
- [x] (fix186) iPhone + iPad teszt (BrowserStack): a főoldali gyakorló feladat (mintalecke) rendben. Hang nem tesztelhető így.
- [x] (fix187) ELLENŐRIZVE: a hirdetés címe JÓ (https://tutoriacademia.com/es, Sándor képe). A gyanú nem igaz; a mai „magyar” szám oka: a látogatók a fix186 feltöltése ELŐTT jöttek. Eredeti gyanú (11.18-i adat): a hirdetésből (forrás „fb”) 22 látogató jött, mind a „/” oldalra, és átlag ~1 mp után eltűntek. Ha a hirdetés „Webhely URL-je” https://tutoriacademia.com/ (előtag nélkül), a spanyol szülő a MAGYAR főoldalt látja. Helyes cím: https://tutoriacademia.com/es/ . Sándor ellenőrzi a Hirdetéskezelőben. Holnapi letöltésben az „ebből 🇪🇸” oszlop megmutatja (a fix186 óta /es-t is tárol).
- [ ] (fix187 ötlet, NEM kész) Biztonsági háló: ha valaki előtag nélküli „/”-re jön, nincs még nyelvválasztása és a böngészője spanyol → átirányítás /es/-re. Csak Sándor OK-ja után.
- [x] (fix187) Látogatásszámláló: a Facebook app / böngésző ELŐTÖLTÉSE (X-Purpose/Purpose/Sec-Purpose: preview/prefetch/prerender) nem számít látogatónak. Ok: a hirdetésből jövők ~1 mp-es „látogatása” lehet előtöltés is.
- [ ] (fix187) Csütörtök/péntek: a Hirdetéskezelő „Linkkattintások” / „Céloldal-megtekintések” számát összevetni a mi „fb” látogatószámunkkal és az „ebből 🇪🇸” oszloppal. Ha a mi számunk jóval nagyobb → még mindig előtöltés/robot; ha a céloldal-megtekintés kicsi a kattintáshoz képest → lassú/nem nyílik meg az oldal a FB appban.
- [ ] (fix188) Fizetés-előkészítés: Sándor döntése 11.18 – VÁR, amíg nincs feliratkozó.
- [ ] (fix188) ÚJ FELADATOK A LECKÉK ALAPJÁN – sorban évfolyamonként (1→6), mindig megnézni, hogy a magyar leckében is benne van-e, és ha igen, oda is. NINCS „célkorosztály”: 1–6 egyformán fontos. Matek 1.º–2.º hiányok (11.18 lista): >/</= összehasonlítás (krokodil), helyzet (encima/debajo/dentro/fuera), alakzatok síkidom/test, színes mintasor (ABAB), mérlegen nehezebb/könnyebb, mérés nem szabványos egységgel (gemkapocs/arasz), strigulás számlálás (recuento, 1. o.), írásbeli összeadás-kivonás átvitellel (2.º; HU 3.), biztos/lehetséges/lehetetlen (zsák golyókkal). Már van: helyiertek, sorozat, szamkocka, kockak, beka, ora, penz, naptar, villam, csop, tukor, robot, diagram, zokni, becsles.
- [ ] (fix188) Chalkie-ötletek (chalkie.ai, tanároknak szóló AI): (1) főoldalon azonnal kipróbálható mini-feladatok gombokkal, regisztráció nélkül (pl. „🐊 ¿Mayor o menor?”) – a widgetek a böngészőben futnak, AI-költség nincs; (2) a „tantervhez igazítva” (LOMLOE / NAT) ígéret jól látható helyen a főoldal tetején; (3) kinyomtatható feladatlap a szülőnek a lecke után (PDF). DÖNTÉS 11.18: (1) elvetve – ugyanaz, mint a mintalecke; (2) megvan már mindkét oldalon („iskolai anyaggal” / „temario escolar”); (3) most nem – sokszorosítható, bevételt vihet el.
- [x] (fix188) KROKODIL feladat kész (Feladat-próba: krokodil; matek 1–4. évf.; MAGYAR ÉS SPANYOL oldalon is). <, =, > két szám közé; 10-ig pöttyök; rossz válasznál tipp (először a tízeseket… / primero las decenas…); 2. hiba után megmutatja és továbblép. Sándor kérésére szebb krokodil (rajzolt fej, fogak, víz) – EZ IS GAGYI (Sándor 11.18). fix190: a krokodil kivéve a tanár listájából (a kód megvan, app.py-ban kikommentezve). Új rajz kell: AI-kép (krokodil tátott szájjal + csukott szájjal, átlátszó háttér), mint az elolj cicájánál (static/figurak/jelenet). Sándor engedélyére vár (képgenerálás szünetel a költség miatt).
- [ ] (fix188) Sándor: a spanyol oldalon a Feladat-próbában nem találta a krokodilt. Helyben működik (/es/... &proba=krokodil). Újra megnézni a proba oldalon, ha nincs: képernyőkép.
- [x] (fix190) VISSZAVONVA, nem került fel – a „Hol van?” (holvan) duplikálta a meglévő elolj feladatot, és gagyi volt (Feladat-próba: holvan; matek 1–2. évf.; MAGYAR ÉS SPANYOL oldalon is). Asztal + doboz; a gyerek oda koppint: asztal tetejére / alá, doboz belsejébe / mellé (encima de / debajo de / dentro de / al lado de). Rossz válasznál elmagyarázza a szót.
- [ ] Következő feladat a listából: síkidom vagy test (kör, négyzet… / kocka, gömb).
- [x] (fix188) Látogatók térképe: NEM kell kódolni – Hirdetéskezelő → Bontás → Kiszállítás → Régió. (Az ott látott számok ELÉRÉS/MEGJELENÉS = hányan LÁTTÁK a hirdetést, nem hányan kattintottak.)
- [x] (fix188) „Magyar látogató nő” – kivizsgálva (11.18 13:54-es letöltés): a fix186 él (délután 4 spanyol látogató már spanyolként számolva); a „magyar” növekedés a „/” és „/login” oldalra jövő közvetlen (robot) látogatók. A hirdetésből jövők („fb”) 22→25.
- [x] (fix190) A TEENDOK.md visszaállása NEM Sándor hibája (a Cursor 3 napja nincs nyitva). Claude oldalán történt (a fájlírás egy régebbi változatot írt vissza). Mostantól Claude minden írás előtt és után ellenőrzi a fájlt. Eredeti, téves feltételezés: egy korábbi változatra (11.18) – valószínűleg nyitva van egy szerkesztőben (Cursor), ami ráírja a régit. Sándor: zárja be a TEENDOK.md fület, mielőtt Claude ír bele.
- [x] (fix190) „Hol van?” – a meglévő ELOLJ (cica, asztal, doboz, valódi képek) feladatot használjuk: mostantól MATEKÓRÁN is (1–5. évf.), a gyerek SAJÁT nyelvén („A cica az asztal alatt van.” / „El gato está debajo de la mesa.”). Nyelvórán változatlan (a tanult nyelven). Feladat-próba: elolj. Magyar és spanyol oldalon is.
- [ ] Meta „Linkkattintások”: Hirdetéskezelő → Kampányok → a kampány sorában az „Eredmények” oszlop (Forgalom kampánynál ez a link- vagy céloldal-kattintás), vagy Oszlopok → „Teljesítmény és kattintások”.
- [x] (fix191) SÍKIDOM VAGY TEST? feladat kész (Feladat-próba: alakzat; matek 1–3. évf.; MAGYAR ÉS SPANYOL oldalon is). Rajzolt alakzatok két csoportba: síkidom LAPOSAN (kör, négyzet, háromszög, téglalap), test TÉRBELIEN, árnyékkal (kocka, téglatest, gömb, henger, kúp). A csoportosító feladat működését használja. Tipp a kártyák alatt.
- [ ] (fix191) KROKODIL – rendesen, AI-képpel (Sándor 11.18: „nem vetjük el, csináljuk meg normálisan”). Sándor futtatja: python krokodil_kepek.py --jeloltek → --valaszt N → --jovahagy → git add static/figurak/krokodil. Utána Claude beépíti a képeket a DM.krokodil-ba (tátott/csukott, tükrözés a < > jelnél), és visszakapcsolja a krokodil sort az app.py-ban.
- [x] (fix191) Meta 11.18: 16 linkkattintás; nálunk 25 „fb” látogató. A különbség oka valószínűleg az előtöltés (fix187 ezt szűri, ha már élesben van) és hogy egy ember a FB-appból és a böngészőből is megnyitja. Pénteken újra összevetni.
- [x] (fix191) Az elolj (cica) matekon: a LOMLOE 1.º matek „Sentido espacial” része (dentro, fuera, encima, debajo), a NAT 1–2. o. matekban „tájékozódás térben” – ezért van matekon.
- [x] (fix192) Szintkérdés (Sándor: „ez nem 1. osztályos?”): a tanterv szerint IGEN 1–2. osztályos. NAT kerettanterv 1–2.: „Mennyiségi viszonyok jelölése nyíllal vagy a <, >, = jelekkel”; „különbséget tesz testek és síkidomok között”. LOMLOE 1.º: „mayor que, menor que”; „círculo, cuadrado… cubo, esfera”. DE a SZÖVEG volt túl nehéz egy 6 évesnek → egyszerűsítve: alakzat csoportjai „✏️ síkidom (lerajzolod)” / „✋ test (megfogod)”, tipp: „Lapos, mint a papír? Akkor síkidom. Kézbe tudod venni? Akkor test.” Krokodil: „A krokodil mindig a nagyobbat eszi meg. Melyik jel kell?”
- [ ] (fix192) KROKODIL „=” jel – Sándor: a csukott száj nem elég ötletes. Javaslatok: (A) a krokodil egyensúlyban lévő MÉRLEGET tart – „ugyanannyi”; (B) két egyforma halat tart, nem tud választani; (C) a két szám alatt egyforma magas pöttyoszlop + a krokodil vállat von. DÖNTÉS (fix193): MÉRLEG, ÁLLÓ krokodillal (a hal Sándornak tetszett, de morbid). A krokodil_kepek.py --valaszt N már a mérleges képet is legyártja (merleg.png → merleg.webp).
- [ ] (fix192) VÁLASZIDŐ (Kimi tanácsai, 11.18) – Claude értékelése: a 6 mp CSAK írásos matekórán van (TANAR_EFFORT_MATEK=medium; low 2,9 mp, medium 5,8 mp volt a tanárteszten), hangmódban low marad. A többlet nagy része a modell GONDOLKODÁSA az első szó előtt, ezért a streaming itt keveset hozna, ráadásul a számellenőrzés és a <FELADAT> javítás a TELJES válaszon fut – streamelve a gyerek az ellenőrzés előtt látná a szöveget. A prompt-cache már mérve van (Railway napló: [CACHE] … %), az előzmény 20 üzenetre van vágva. Következő lépés, ha kell: tanárteszt mérje külön az első szó idejét és a teljes időt (kb. pár cent).
- [x] (fix193) Alakzat csoportnevek újra (Sándor nem értette a „lerajzolod/megfogod”-ot): „📄 síkidom: lapos” / „📦 test: kézbe veszed”; ES „📄 plana: lisa” / „📦 cuerpo: se coge”.
- [ ] (fix193) Railway alvás: NEM a fiók Settings menüjében van, hanem a SZOLGÁLTATÁSNÁL: projekt → a web szolgáltatás kártyája → Settings fül → „Serverless” (régebben „App Sleeping”) kapcsoló. Legyen KI.
- [x] (fix194) Railway „Serverless” ki van kapcsolva (Sándor ellenőrizte 11.18) – a hidegindítás nem lassít.
- [x] (fix194) KROKODIL AI-képekkel beépítve (Feladat-próba: krokodil; matek 1–4.; MAGYAR ÉS SPANYOL): a jó jel után a krokodil kiemelkedik a vízből, és a nagyobb szám felé BEKAP (csukott → tátott kép, kis rugózás); „>” tükrözve; „=”: álló krokodil egyensúlyban lévő mérleggel. Sándor választotta az 1. jelöltet. A tanár listájában újra bekapcsolva.
- [ ] (fix194) Sándor: python krokodil_kepek.py --merleg-ujra → --jovahagy → git add static/figurak/krokodil (a képek NÉLKÜL ne kerüljön fel az app.py/chat.html!).
- [x] (fix195) Krokodil: kisebb (186×100) és lejjebb került, az orra nem lóg bele a kártyába (Sándor képe, 11.18). Sándor: tetszik a gyerekeknek is.
- [ ] (fix195) HANGMÓD + 1–2. OSZTÁLY (Sándor kérdése): a feladat hangmódban is megjelenik, a tanár hangosan bevezeti, a gyerek koppint, az eredmény a tanárhoz megy, aki hangosan reagál. DE a feladat SAJÁT szövegeit (felső utasítás, „Még nem…” tipp, a végén a dicséret) NEM olvassa fel – egy olvasni nem tudó elsős ezeket nem érti. Javaslat: hangmódban (és/vagy 1–2. évf.-on) ezeket a rövid szövegeket a felolvasó mondja ki (a rövid feladathangok a csomag hangidején túl is szólnak; napi keret 30 000 karakter/gyerek). Hanghoz nyúl → Sándor OK-jára vár. → fix196: Sándor OK-t adott, CSAK PRÓBAOLDALON: hangmódban a feladat visszajelzéseit (D.jelez – tipp, dicséret, magyarázat) a felolvasó kimondja (max. 200 karakter). Élesre (main) kapcsolás: a chat.html-ben a D.hangosan sorból a {{ proba_oldal|tojson }} feltételt kell kivenni – Sándor döntése után.
- [x] (fix196) ÖT ÚJ 1–2. OSZTÁLYOS MATEKFELADAT (mind MAGYAR ÉS SPANYOL oldalon is):
      mintasor – színes gyöngysor folytatása (matek 1–3.)
      nehezebb – kétkarú mérleg, melyik nehezebb; lufi–tégla: „a nagy dolog nem mindig nehéz” (matek 1–3.)
      gemkapocs – ceruza hossza gemkapcsokkal (matek 1–2.)
      strigula – állatkák megszámolása strigulával táblázatba, melyikből van a legtöbb (matek 1–3.)
      esely – biztos / lehetséges / lehetetlen, golyók üvegben (matek 1–4.)
  Kihagyva, mert MÁR VAN: írásbeli összeadás-kivonás átvitellel = a meglévő „szamolo” (oszlopos) feladat.
- [ ] Következő kör (matek 2.º / 2. o.): óra – megvan (ora); pénz – megvan (penz, euróval is?) – ellenőrizni; szorzás 2,5,10 – megvan (villam, csop). Utána: magyar/lengua 1–2. o. leckék feladatai.
- [x] (fix197) Mérleg (nehezebb): VÍZSZINTESEN indul, a gyerek tippel, a koppintás után billen le (Sándor kérése). Rossz tippnél megmutatja és továbblép.
- [x] (fix197) Strigula LÉPÉSENKÉNT (Sándor: egy 6 éves nem érti): előbb csak a katicák, aztán a pillangók, végül a méhek; a táblázatban az aktuális sor sárgán kiemelve; ha rossz állatra koppint: „Most még csak a katicákat számoljuk!”.
- [x] (fix197) HANGMÓDBAN (csak próbaoldal) 🔊 gomb a feladat utasítása előtt – a nem olvasó gyerek meghallgathatja (a gombnyomásra az AKTUÁLIS szöveget mondja). Minden új típusú (DM) feladatnál.
- [ ] (fix197) GÉPEN EGÉRREL egy 6 éves nehezen boldogul – minden koppintós feladatnál igaz. Javaslat: 1–2. osztálynak telefon/tablet ajánlása a szülőnek (GYIK / regisztráció után tipp); vagy gépen + hangmódban + 1–2. o. a tanár inkább szóban kérdezzen. Sándor dönt.
- [ ] (fix197) Hangmód próbája: a próbaoldalon a chat fejlécében a „🧪 Hangkeret: ELFOGYOTT/VAN” gombbal visszakapcsolható. Ha VAN-t mutat, és mégis elfogyott → a teszt csomag hangos ideje fogyott el, szólni Claude-nak.
- [x] (fix198) Hangmódban (próba) a feladat utasítását MAGÁTÓL is felolvassa – a tanár beszéde UTÁN (nem beszélnek egymásra); ha a tanár nem szólal meg, 7 mp múlva. A 🔊 gomb megmarad az újrahallgatáshoz.
- [x] (fix198) Mérleg alap-párjai: kivéve az elefánt–egér és cica–egér (ez nem matek, hanem köztudás). Helyette olyan párok, ahol a MÉRET becsap: lufi–tégla, toll–alma, ananász–lufi, labda–ananász. (LOMLOE 1.º „pesado y ligero”, NAT 1–2.: tömeg összehasonlítása.) Ötlet később: hány kocka tart egyensúlyt egy almával (nem szabványos mértékegység).
- [x] (fix198) Gép + egér + 1–2. o.: a strigulát és a koppintós feladatokat szóban NEM lehet (Sándor: belekeveredik) → marad a javaslat: 1–2. osztálynak telefon/tablet (szülői tipp). Sándor dönt, hova kerüljön.
- [x] (fix198→fix199 KÉSZ) INNOVATÍV FELADATOK más országokból: cseresznye-számolás (Japán, tízes átlépés, 1. o.), szalagmodell szöveges feladathoz (Szingapúr, 2–6. o.), szorobán / számológolyós abakusz (Japán–Kína, helyiérték, 1–4. o.), rácsos szorzás (India, 4–5. o.), „Jósold meg, aztán nézd meg!” kísérletek – úszik vagy elsüllyed (japán természettudomány-óra, 2–6. o.), daru–teknős fejek–lábak fejtörő (Japán, 4–6. o.).
- [x] (fix199) HAT INNOVATÍV FELADAT (mind MAGYAR ÉS SPANYOL oldalon is; Feladat-próba név → tananyag):
      cseresznye – japán „sakuranbo”: összeadás 20-ig tízes átlépéssel, tízes kerettel (matek 1–2.; HU 1. o. 20-as számkör, ES 1.º sumar hasta 20)
      szalag – szingapúri szalagmodell szöveges feladathoz: előbb a rajzon megmutatja, mit keresünk, aztán számol; egesz / resz / tobb (matek 1–6.; ES 2.º problemas, HU szöveges feladatok)
      szoroban – japán abakusz, helyiérték (matek 1–4.; HU helyiérték 1–4., ES 1.º–2.º decenas, centenas)
      racsszorzas – indiai rácsos szorzás, átlós összeadás átvitellel (matek 3–6.; HU 4. o. írásbeli szorzás, ES 3.º–4.º multiplicación)
      uszik – „Jósold meg, aztán nézd meg!”: úszik vagy elsüllyed (környezet / Conocimiento / fizika 1–7.); a meglepő tárgyak: szőlőszem elsüllyed, farönk úszik, jég úszik
      fejlab – japán „tsurukame-zan”: csirkék és nyuszik, fejek és lábak (matek 4–6.; problémamegoldás, az egyenlet előfutára)
- [x] (fix199) Hangmód (próba): az utasítást NEM olvassa fel újra, ha a tanár utolsó üzenete már tartalmazza a szavai többségét (Sándor: „sokszor az oktatás részben is benne van”).
- [ ] (fix199) Feladat-próba: a próbában csak a feladat látszik, magyarázat nélkül – élesben a tanár előbb tanít, aztán adja a feladatot. (Sándor kérdése, válasz megadva.)
- [x] (fix200) ÉRTHETŐBB FELADATOK (Sándor 11.18: „a 9 éves sem érti”, „túl gyorsan vált”, „ne írjuk bele, hogy japán”):
      • PÉLDA a feladat előtt („Nézd meg, hogyan kell!”), a program magától lejátssza, aztán „Most te jössz! ▶” / „↺ Még egyszer”: cseresznye (9+4), golyós számoló (7, aztán 23), rácsos szorzás (mit hova kell írni).
      • TOVÁBB GOMB a körök között (nem vált magától): úszik, mérleg, biztos/lehetséges/lehetetlen, cseresznye, golyós számoló.
      • cseresznye: a kék golyók a dobozban beköltöznek a tízes keretbe; kérdés: „Hány üres hely maradt?” – nem kell fejben bontani.
      • golyós számoló: 2 rúd, ha a számok 100 alattiak; rudak fölött a nevük, alattuk a rúd értéke; jelmagyarázat (5 / 1).
      • rácsos szorzás: LÉPÉSRŐL LÉPÉSRE vezetve – sárga négyzet: „Mennyi 4 × 6?”, sárga ferde sáv: „4 + 1 = ?”, átvitel kiírva.
      • úszik: „a szőlő” (a kép egy fürt), a magyarázat kint marad, amíg a gyerek tovább nem lép.
      • csirkék és nyuszik: egész testes állatok, alattuk „2 láb / 4 láb”, egyszerűbb szöveg, nincs „japán”.
      • Ország nevét (japán, indiai, szingapúri) sehol nem írjuk ki a gyereknek, a tanár leírásából is kivéve.
- [ ] (fix200) Szalagmodell: még nincs előtte példa – ha Sándor szerint kell, ugyanígy.
- [x] (fix201) A PÉLDA nem vált magától: a gyerek lépteti (Példa 1/3 … Tovább ▶), a végén „Megpróbálom! ▶” és „↺ Még egyszer” (a „Most te jössz” furcsa volt, mert a gyerek nyomja).
- [x] (fix201) Szalagmodell: nincs több „koppints a részre” lépés (nem volt egyértelmű) – a rajzon piros ? van, alatta azonnal a számbillentyű; ELŐTTE PÉLDA (5 és 2, ugyanolyan fajta feladat). Magyar mondatok javítva: „Hány almája van Bencének?”, „Hány almájuk van összesen?”, „Bencének 3-mal több van.”
- [x] (fix201) Rácsos szorzás: rossz válasznál a segítség FELÜL, pirossal látszik (pl. „Nem 12. Segítség: 4 × 6 = 4 + 4 + 4 + 4 + 4 + 4 = ?”), 3. hiba után a jó szám.
- [x] (fix201) Évfolyamok (Sándor: a szorobán inkább nagyobbaknak): golyós számoló 2–5., rácsos szorzás 4–6., szalagmodell 2–6., úszik 1–6. Az évfolyam azt jelenti, MELYIK osztálynál adhatja a tanár – nem nehézségi fokot.
- [x] (fix201) LOMLOE / NAT kérdés (Sándor): a tanterv azt mondja meg, MIT kell tanulni (tartalom, évfolyam), a módszert a tanárra bízza. A tízes keret, golyós számoló, szalagos rajz a spanyol és a magyar tankönyvekben is megvan (pl. Spanyolországban az ABN- és a szingapúri módszer elterjedt). Ezért nem ellentmondás – csak a tartalom és az évfolyam stimmeljen. (Nem jogi tanács.)
- [ ] (fix201) Hangmódos felolvasás: helyben MŰKÖDIK (hangmódban 7 mp után felolvassa az utasítást, rossz válasznál a tippet). Sándor nem hallotta → próbálja így: proba oldal, HANGOS MÓDRA váltva, „🧪 Hangkeret: VAN”, Feladat-próba: krokodil, vár 7 mp-et. Ha így sem szól: szólni.
- [ ] (fix201) Ötlet (Sándor): úszik-feladatnál a gyerek is indokoljon („Miért úszik? a) könnyű az anyaga b) nagy”) – később.
- [x] (fix202) A PÉLDÁK MEGMUTATJÁK, nem csak leírják (Sándor: „gyerekaggyal nem érthető, csak leírás van”):
      • golyós számoló: KEREK golyók (eddig lencse alakú volt – „ez nem golyó”); a példában egy 👆 kéz odamutat, és a golyó odacsúszik; jelmagyarázat „fent: 5 / lent: 1”.
      • rácsos szorzás: a példa egy valódi szorzást tölt ki lépésenként (23 × 4): nyilak a két számtól a négyzetig, beíródik 12 → 1 | 2, aztán a sárga sávok összege, végül 92.
      • szalagmodell: a szalag KOCKÁKBÓL áll, minden kockában a tárgy képe (🍎/⭐/🔵) – „minden kocka 1 alma”; a példa szövege gyerekes és kérdéssel zárul („Hány almája van Bencének? Megszámoljuk az ő szalagját: 5 + 2 = 7.”).
      • úszik: a magyarázat egy KÉPPEL: ugyanakkora darab tárgy és víz a mérleghintán – amelyik nehezebb, az lent van; szöveg: „Képzeld el: egy kő és ugyanakkora víz. A kő a nehezebb…”.
      • tízes átlépés (cseresznye): a cseresznye helyett a kék szám kettébontása KÉK körökkel, „be” / „kint” felirattal (Sándor: cseresznyét mutatunk, lejjebb golyót).
- [x] (fix202) Hangmód Sándornál: a képen a „Hangos mód” gomb látszik → ez a ÁTVÁLTÓ gomb, vagyis épp CHAT módban volt. Rá kell kattintani, és utána olvas fel.
- [ ] (fix202) Kérdés (Sándor): sokféle módszer → összezavarja-e a gyereket? Válasz: egy órán belül EGY módszer maradjon (a tanári promptban már benne: „EGY FELADAT – EGY MÓDSZER”). Később érdemes lehet: témakörönként rögzíteni, melyik feladatot adja elsőként (pl. tízes átlépés → mindig a tízes keret).
- [x] (fix203) Úszik: „lemegy” → „elsüllyed” (Sándor).
- [x] (fix203) A chat fejlécében a módváltó gomb felirata CSELEKVÉS lett: „🎙️ Váltás hangosra” / „💬 Váltás írásra” (ES: „Pasar a voz” / „Pasar a escribir”). Sándor azt hitte, a gomb a jelenlegi módot mutatja.
- [x] (fix203) Rácsos szorzás a tanárnak: KIEGÉSZÍTŐ módszer – először mindig az iskolai írásbeli szorzás (szamolo); a rácsot csak ellenőrzésre / érdekességként, vagy ha a gyerek az átvitelben rendre elakad. Ok: sem a magyar, sem a spanyol iskola nem ezt tanítja, ne zavarjuk össze.
- [ ] (fix203) KÖVETKEZŐ KÖR (javaslat): Magyar nyelv / Lengua castellana 1–2. osztály (olvasás-írás tanulás) – előbb hiánylista a leckékből, a meglévő feladatokkal (szotag, betukev, maganh, diktalas, rim, nagybetu…) összevetve; aztán Matek 3–4.
- [ ] (fix203) Regisztráció: Sándor csalódott (hirdetés fut, nincs regisztráció). Péntek után a látogatottsági adatból: hányan jutnak el a próbaleckéig / regisztrációig, és hol esnek ki.
- [x] (fix204) ANYANYELV 1–2. osztály – 6 új feladat (mind léptethető példával, 🔊 Meghallgatom gombbal, Tovább gombokkal):
  - hanghely – „Hol hallod a hangot?” (szó elején / végén), 1–2., HU + ES.
  - szokoz – „Hol a szóköz?” (Akutyaugat. → koppint a szóhatárra), 1–2., HU + ES. Mondat max. 14 betű (a túl hosszút a program kihagyja).
  - helyesiras – HU: rövid/hosszú magánhangzó (h_z: a/á), 1–3.; ES: c/qu, m antes de p/b, r/rr (szabaly: cqu|mn|rrr).
  - mesesor – mese 4 képes kártyán sorba rakva (eleje–közepe–vége): HU répa / három kismalac / Piroska; ES nabo / cerditos / caperucita. SAJÁT rövid újramesélés (a népmese közkincs; mások mai átirata, fordítása, illusztrációja NEM).
  - hangsuly – sílaba tónica, CSAK spanyol.
  - signos – ¿? ¡! , CSAK spanyol (a magyar oldalon a meglévő irasjel).
- [ ] (fix204) Feladatszám (Sándor kérdése): 142 feladattípus. Cél NEM több ezer, hanem hogy minden lecke kapjon 2–3 ráillő típust (~150–250). Következő hiánylista: Matek 3–4., majd Magyar/Lengua 3–4.
- [ ] (fix204) Később: további népmesék a mesesorba (pl. A kiskakas gyémánt félkrajcárja; ES: La ratita presumida) – mindig saját, rövid újramesélés.
- [ ] (11.19) VERSENYTÁRS: isiestudio.app (ES, 4–6. Primaria, quiz + vizsgajavítás, pingvin kabala). Árak: 19,99 €/hó, 50,99 €/negyedév, 143,99 €/év; testvér +12,99 €/hó; 7 nap ingyen. Cégadat (név, cím, CIF) nincs az oldalon. Bevétel/felhasználószám nem látszik. Csak ÖTLETET veszünk át, szöveget/képet/figurát nem.
  - [ ] Szülő által megadott VALÓDI jutalom (pl. „fél óra mese”, „fagyi”): a szülő beírja, a gyerek a heti cél teljesítésével feloldja. Olcsó, erős.
  - [ ] Heti szülői jelentés: rövid, AI-fogalmazta szöveges összefoglaló (miben javult, mit érdemes ismételni) a számok mellé.
  - [ ] Figyelemzavaros gyerekek: CSAK visszafogott saját mondat („rövid lépések, egy feladat egyszerre, megvárja a gyereket”), orvosi/terápiás ígéret NÉLKÜL; szervezeti ajánlás csak valódi együttműködéssel.
  - [ ] Árazás tervezésénél viszonyítás: havi/negyedéves/éves váltó, testvérkedvezmény (fizetés még szünetel).
  - [ ] Rövid (20–30 mp) bemutató klipek témánként, később.
  - [ ] Ellenőrizni: a mi oldalunkon (ES és HU) szerepel-e a szolgáltató neve és elérhetősége a jogi oldalon (LSSI / ekertv. kötelező) – ez nálunk bizalmi előny lehet.
  - [ ] Ötletek még az oldalukról (Sándor 11.19): részletes GYIK, rövid videók témánként, ÁSZF/adatvédelem átlátható tagolása. Saját szöveggel!
  - Miért olcsóbbak: előre elkészített tartalom (összefoglaló, kvíz, teszt), az AI csak javításra fut; nincs folyamatos beszélgetés és felolvasás. Nálunk a fő költség a beszélgető tanár + a hang percenként.
  - TDAH-állításuk: egy szervezet ajánlása, orvosi/klinikai bizonyíték az oldalon nincs. A „rövid lépés, egy feladat egyszerre, azonnali visszajelzés” elv általános jó gyakorlat, nem gyógyító ígéret.
- [x] (11.19) EU-s jogi válasz – a FIZETÉS előkészítéséhez:
  - Az árat mindig a TELJES, áfával növelt összeggel kell kiírni (előfizetésnél a számlázási időszak teljes díja); nem elég az „+ áfa %”.
  - Határon átnyúló szolgáltatásnál (spanyol cég → magyar vásárló) NEM kötelező forintban kiírni.
  - Elállás 14 napon belül, ha a szolgáltatás a vevő kérésére már elindult: az addig eltelt idővel arányos díj tartható meg (EUB C-641/19, PE Digital – időarányosan).
  - Fióktörlés / GDPR 17. cikk: a számlákat a törvényes ideig MEG KELL őrizni (GDPR 17(3)(b), jogalap 6(1)(c)); a többi adat törölhető.
  - [ ] Ezt a fizetés bevezetésekor az ÁSZF-be és az adatkezelésibe beírni (nem jogi tanács – könyvelővel átnézni).
- [x] (fix206) Sándor visszajelzése a fix204 feladatokra:
  - A hangmódos 🔊 gomb (CSAK hangmódban, a próbaoldalon látszik, a főoldalon nem) rálógott a szövegre → most az utasítás mellett áll egy sorban.
  - Hangmódban csak a „Nézd meg, hogyan kell!”-t olvasta, a szót előtte → most a PÉLDA SZÖVEGÉT olvassa fel (benne a szóval), lépésenként; a kérdéseket is elmondja („Hol hallod a pé hangot? A szó: kalap.”).
  - Betűnév: a K-t „kö”-nek, az R-t „rö”-nek ejtette → a felolvasó most a betű NEVÉT mondja (ká, er, el, em…; spanyolul ese, erre…). Megoldás: data-mond="…" a szövegben.
  - Egyszavas kimondás elején levágás: rövid szöveg elé 0,3 mp csend (Azure SSML), és a régi mentett hangok helyett újak készülnek.
  - „5 / 5 elsőre jó” → „5 osztva 5” lett belőle, és nem érthető: MINDEN feladatban „5 közül 5 elsőre sikerült” (ES: „5 de 5 bien a la primera”); a „2 / 4 –” körszámlálót nem olvassa fel.
  - Emoji-képek „gagyik”: hanghely, helyesiras, hangsuly, signos → a meglévő szóképtár képei (static/szokepek/nyelv). Szavak ehhez igazítva.
  - mesesor: a 👆 nem takarja a szöveget; képek: mese_kepek.py (12 kép, Sándor futtatja a saját kulcsával). Amíg nincsenek fent, emoji marad.
- [ ] (fix206) Azure magyar hang egyes szavakat „furán” ejt (Sándor). Később: másik magyar hang kipróbálása (Noémi ↔ Tamás) egyszavas kimondásra; ha az sem jó, a feladat-szavakhoz előre felvett/ellenőrzött hang.
- [x] (fix207) Az első mese-képek rosszak (hiányzó részletek; a „répa” retek/fehérrépa lett lila tetővel). Új mese_kepek.py: mesénként SZEREPLŐLAP + 4 pontosan leírt jelenet, a répa SÁRGARÉPA; új mappa: szokep_uj/mese2. A spanyol cím ezért „La zanahoria gigante” (kulcs marad: nabo).
- [ ] (fix207) Mese-képek (Sándor, egyenként): --szereplok repa → megnéz → --mese repa → megnéz → (malac, piroska ugyanígy) → --jovahagy → git add static/figurak/mese
- [x] (fix210) Mese-képek 2. kör: répa KÉSZ (jó). Piroska 2–3: a háttérben ott állt az egész család; malac: 3 ház helyett 2. OK: a jelenet a teljes szereplőlapot kapta mintának. Javítás: jelenetenként CSAK a benne lévő szereplők kivágott képe (szokep_uj/mese2/szereplo_*.png). Malac kártyái: indulnak → szalmaház elfújva → faház elfújva → téglaház áll (HU+ES szöveg is).
- [ ] (fix210) Újra kell (4 kép): piroska 2, 3 és malac 2, 3 → megnézni → --jovahagy. Képgenerálás előtt Claude mindig nézze át a promptot, mert Sándornak pénzbe kerül; ha nem biztos valamiben (mi legyen a képen), KÉRDEZZEN.
- [x] (fix210) GYIK bővítve 10 kérdéssel (HU+ES): mi a TutorIA, osztályok, iskolai anyag, tanár helyett?, elakadás, hangos mód, ár/próba, több gyerek, biztonság, szülői rálátás.
- [x] (fix211) Hirdetés-elemzés (adatok/latogatottsag_2026-11-19_1440.json, 7 nap): 428 látogató (a „közvetlen” nagy része robot), 0 regisztráció. Facebookról ~100 látogató: a főoldalon a fele kb. 2 mp alatt elmegy, a mintaleckéig szinte senki nem jut. Mintalecke: 59 kezdte, 4 fejezte be. Regisztrációs oldal: 20 megnyitás, 0 beküldés. A regisztráció MŰKÖDIK (Claude kipróbálta: megerősítő levél oldal jön). Spanyol: 70 látogató, 25 kezdte a mintaleckét (jó arány!).
- [ ] (fix211) KÖVETKEZŐ: (1) miért esnek ki a mintaleckéből (59→4) – végigjátszani, hol unalmas/hosszú; (2) regisztráció: a szülői PIN-t kell-e már itt kérni (súrlódás) – Sándor döntése; (3) a Facebook-hirdetés és a főoldal első képernyője egyezzen (amit a hirdetés ígér, azt lássa elsőre). A napi 3 €-t addig NEM emelni.
- [x] (fix211) Bukott leckezáró után a kapu eddig NEM figyelte a 60 perc tanulást (csak üzenet volt róla). Most: 60 perc tanulás után írhatja újra, korlát nélkül. A tanár is tudja, hogy addig a gomb nincs ott.
- [x] (fix211) A teszt HIBÁI mentődnek (child_topic_scores.teszt_hibak, új oszlop, magától létrejön), a tanár utána elsősorban ezeket gyakoroltatja, új példákkal (Sándor kérése).
- [ ] (fix211) Régi apróság: ha egy már sikeres leckéből újra tesztet ír és elrontja, a „sikeres” jelzés elveszhet (database.save_topic_test_result: row.passed = passed). Kérdés Sándornak: maradjon-e meg a „sikeres”.
- [x] (fix211) GYIK javítva Sándor szerint: a leckék SORBAN jönnek (nem a gyerek választja); hol lehet hangos/írásos módra váltani; az időmérés (a tétlen 3 perc sem számít); a teszt szabályai.
- [x] (fix212) mesesor: a tanár ELŐTTE elmeséli a mesét 3–4 mondatban, szelíd változatban (senkit nem esznek meg / lőnek le), és mindig megadja, melyik mesét. Piroska Spanyolországban is ismert (Caperucita Roja).
- [x] (fix212) Szülői PIN marad a regisztrációnál (Sándor: fontos, később elfelejtené) – nem ez a fő ok.
- [x] (fix212→215) Eldöntve: minden újabb próba előtt kell tanulás, 30 perc.
- [ ] (fix212) Mintalecke: 59 kezdte, 4 fejezte be. Sándor gyanúja: túl egyszerű, nincs benne igazi magyarázat, és azt hiszik, ezt kapják. Végig kell nézni együtt.
- [ ] (11.19) MINTALECKE-ÁTNÉZÉS (Claude): most 3 választós kérdés (kvíz), beszélgetés és interaktív feladat NÉLKÜL – pont azt nem mutatja, amiben jók vagyunk. Sokan több évfolyamot is megnyitnak (100 megnyitás / 59 ember), de nem fejezik be: belenéznek, „sima kvíz”, mennek. TERV: (1) beszélgetés-forma: a tanító kérdez, a gyerek válaszol, rossz válasznál MÁSKÉPP magyaráz (előre megírt elágazással, AI nélkül); (2) évfolyamonként 1 VALÓDI interaktív feladat (pl. 1.: krokodil, 2.: tízes keret, 3–4.: szorobán / mérleg); (3) az első mondatot fel is olvassa (előre elkészített hangfájl, ingyen); (4) a végén: „a valódi tanító ennél többet tud: …” + regisztráció. Először HU+ES 2. osztály, képernyőképpel Sándornak.
- [x] (fix217) ÚJ, BESZÉLGETŐS MINTALECKE – 2. osztály HU+ES (mintalecke.py CHAT): a tanító gépel és ír, a gyerek gombbal válaszol, rossz válaszra másképp magyaráz; valódi TÍZES KERET (kék pöttyök átrakása koppintással); „Kérdezz bátran” rész (2 kérdés + válasz). AI nélkül, ingyen. A többi évfolyam a régi marad, amíg Sándor jóvá nem hagyja.
- [ ] (fix217) Ha a 2. osztályos tetszik: 1. (krokodil / hangok), 3. (szorzás tányérokkal), 4. (szorobán), 5–8. hasonló beszélgetős változat, HU+ES. Hang: előre elkészített hangfájl az első üzenethez (Sándor kulcsával, fillérek).
- [x] (fix218) KABALA = LUMI (Sándor jóváhagyta): izzófejű kis figura, a feje kigyullad, ha a gyerek rájön valamire. Részletes leírás + képkészítő: lumi_kepek.py (3 jelölt → választás → 6 állapot: aha, gondolkodik, orul, integet, biztat, tapsol). Sándor futtatja. Utána: hol jelenjen meg (mintalecke, videó, lecke – a mostani robot helyett vagy mellett? → Sándor dönt).
- [ ] (fix219) LUMI 2. változat: Sándornak az első leírás nem tetszett – a fej a MI LOGÓNK lámpája legyen (arc nélkül, vagy a T pöttyei adják az arcot). lumi_kepek.py most a logót kapja mintának, 3 változat (arc nélkül / pötty-arc / egyszerű arc), mappa: szokep_uj/lumi2. Az állapotok maradnak. KÜLÖN töltjük fel (Sándor kérése) – a lumi_kepek.py ne kerüljön a többi feltöltésbe, amíg nincs kész.
- [ ] (fix220) LUMI 3. változat: a 2. lámpája sem olyan, mint az oldalon (a minta a 176 pontos PNG volt → „szép üvegizzó” menettel). Most a minta az oldal fejlécének lámpája 1024 pontban (szokep_uj/logo_lampa_1024.png), lapos vonalrajz, 3 arany csík alatta, mappa: lumi3. Ha ez sem jó: Claude a kiválasztott figurára PONTOSAN ráilleszti az oldal lámpáját (ingyen).
- [x] (fix221) LUMI: Sándor a lumi3/jelolt_1-et választotta. A nyakánál hézag volt → Claude összetolta (izzó + 3 csík lejjebb, a csík a kapucni mögé bújik): szokep_uj/lumi3/alap.png. FONTOS: a --valaszt-ot NEM kell futtatni (felülírná), jöhet egyből: python lumi_kepek.py --allapotok. Ha az állapotoknál is hézag lesz, Claude ugyanígy kijavítja.
- [x] (fix222) LUMI állapotok: JÓ: alap, gondolkodik, orul, biztat, tapsol. ROSSZ (Sándor): aha, integet (arcot kaptak – a leírásban „szem”, „mosoly” volt), és a jelolt_1–3. Javítva a leírás: a lámpán SOHA nincs arc, a hangulatot a test és a fény mutatja. Újra: --allapot aha, --allapot integet. Jóváhagyás csak a jókra: --jovahagy --csak alap,gondolkodik,orul,biztat,tapsol(,aha,integet ha jók lettek).
- [x] (fix222) Beszélgetős mintalecke: 1. és 4. osztály HU+ES elkészült (betűk kirakása, tapsolás hangokra/szótagokra, tányérok a szorzáshoz). Csak a próbaoldalon.
- [ ] (fix222) Ha Sándornak tetszik az 1. és 4.: HU 3., 5–8., ES 3., 5–6. ugyanígy.
- [x] (fix223) ROSSZ VÁLASZ UTÁN NEM DICSÉR (Sándor: „leírja a számot ő maga, majd azt írja: ügyes voltál”): Feladat-próba összes felületén (D.jelez) ha előtte hiba volt, a „Ügyes/Szuper/…” helyett „Most már megvan!”; a tanító AI-nak is szabály: segítséggel megoldottat ne dicsérjen hibátlannak, adjon rá egy hasonló új feladatot. Mintalecke: 1. rossz → másképp magyaráz, 2. rossz → lépésenként, 3. rossz → megmutatja, és a végén „Kitartottál!” (nem „Ügyes”).
- [x] (fix223) Mintalecke 1. o.: a „sün” tapsolós feladat új: a gyerek maga tapsolja ki, hány hang van (S-Ü-N), és Kész-t nyom (eddig a program számolta helyette). ES: PE-LO-TA szótagok.
- [x] (fix223) Mintalecke 1. o.: „mindent úgy írunk, ahogy halljuk” javítva (Sándor jól mondta): a legtöbb szót igen, de van kivétel (látja → „láttya”). ES: a h néma, a b és v ugyanúgy hangzik.
- [x] (fix223) Lumi aha.png: a sárga sugarak kiszedve (az eredeti: aha_sugaras.png).
- [x] (fix224) „ADDIG MAGYARÁZ, AMÍG MEG NEM ÉRTI” (Sándor): a megoldás megmutatása NEM zárja le a feladatot. Mintalecke: megmutatás után, és hibák utáni jó válasz után is jön egy HASONLÓ (lépésenként 2), amit a gyerek egyedül old meg; csak ha ezek után is nehéz, mondja ki őszintén: „a valódi órán így folytatnánk”. A záró szöveg nem „Kitartottál”, hanem „Ezt még gyakoroljuk együtt”.
- [x] (fix224) Feladat-próba felületek (mind): hiba utáni jó válasznál dicséret + biztatás („Most már megvan – ügyes vagy, hogy nem adtad fel!”); a záró szöveg hiba esetén „Ami nehezen ment, azt most még gyakoroljuk”; a tanár mindig megkapja, hogy volt segítség. Tanár-szabály: szívből megdicséri, másképp magyaráz, hasonló új feladat – AMÍG EGYEDÜL MEG NEM OLDJA; ha sokáig nehéz, egy könnyebb lépésre visszalép.
- [ ] (fix224, Sándor: FONTOS) ÉLESBEN MEGNÉZNI: a tanár tényleg ad-e hasonló feladatot „segítséggel” eredmény után (a Feladat-próbában nincs tanár, ott csak kiírjuk, mit tenne).
- [x] (fix225) Mintalecke 1. o.: a sün-tapsolás helyett KÉPES feladat („Melyik kép kezdődik L hanggal?”, hasonlók: P, N; ES: M, C, P). 2. o.: a hasonló feladatok is a tízes kerettel (pöttyök átrakása) indulnak. A megoldás a beszélgetésben is látszik, a tábla csak kis szünet után vált. A végén gomb („Tovább az eredményhez”), nem vált át magától. Hiba javítva: „Zárd össze” → a „Z” zöld kiemelésbe csúszott.
- [x] (fix224) Mintalecke 1. o.: „látja” → „láttya”-nak ejtjük, mégis tj-vel írjuk (Sándor javítása).
- [x] (fix224) Gyerekprofil: „A gyerek neme” helyett „Kísérő figura (kabala)”, „Nem kérek figurát”; a név-mező a választott figura nevét mutatja, figura nélkül eltűnik; a kerek jelölő a szöveggel egy vonalban.
- [ ] (fix224) Kísérő figura választó: kis képek a gombokba (Robi – a mozgó robot – állóképe hiányzik hozzá).
- [x] (fix224) Fiók törlése: kiírva, mi törlődik, mi lesz a mentésekkel, az előfizetéssel; link az adatkezelési tájékoztató 6. és az ÁSZF 9. pontjára.
- [x] (fix225) Szövegek átírva úgy, mintha már lenne fizetés (Fiókom, ÁSZF 9., adatkezelési 6.: törlés = előfizetés megszűnik, maradék órák elvesznek, elállás 14 napig, számlák megmaradnak). KÓDBAN MÉG HÁTRA, fizetés indulásakor KÖTELEZŐ: a törlés hívja meg a Stripe-lemondást, és a számlákat ne törölje.
- [ ] (fix224, régi sor) FIZETÉS INDULÁSAKOR KÖTELEZŐ: a fiók törlése automatikusan mondja le az előfizetést (az ÁSZF 9. pont most azt írja, hogy „nem helyettesíti a felmondást” – fizetésnél ez azt jelentené, hogy törölt fiókért is levonunk). A számlákat a törvény szerint meg kell őrizni → adatkezelési tájékoztató 6. pont és a Fiókom törlés-szövegének „Előfizetés” sora átírandó.
- [x] (fix226) Mintalecke 4. o.: a hasonló feladatoknál (3 × 6, 5 × 4) a rajz a feladat számaiból készül (eddig a 4 × 8-as ceruzás kép maradt ott – Sándor vette észre).
- [x] (fix228) Beszélgetős mintalecke MINDEN évfolyamra kész: HU 3. évszakok (sorba rakás), 5. szófajok (válogató), 6. törtek (pizza színezése), 7. halmazállapotok (válogató), 8. függvénygép (titkos gép); ES 3., 5., 6. ugyanígy. Mind: hasonló feladatok, amíg egyedül megy; gép végigjátszotta mindet hibátlan és hibás úton is.
- [ ] (fix228) Sándor nézze át a próbaoldalon; ha jó → élesen is bekapcsolni (Railway: MINTALECKE_BESZELGETES=1 a fő oldalon, vagy a kapu kivétele az app.py-ból).
- [x] (fix229) Mintalecke: a 6. o. kérdésénél a pizza alól lekerült a megoldás (1/4 felirat csak akkor van, ha két pizzát hasonlítunk össze); 8. o. titkos gép: a táblázat sorai mindig növekvő sorrendben, és nem írja ki előre a megoldást („nézd meg a táblázatot, mi történt a számokkal”).
- [x] (fix231) Mintalecke ÉLESEN IS a beszélgetős (minden évfolyam kész; HU és ES felépítése lépésről lépésre azonos – géppel összevetve, mind a 14 lecke végigjátszva jó és rossz úton). Vészfék: Railway MINTALECKE_BESZELGETES=0.
- [x] (fix232) Lumi kesztyűje narancs (mint a cipő) – a fehér nem látszott a mezőkön; a lumi_kepek.py --jovahagy is így készíti (kell hozzá: scipy). Regisztráció címe: „Kezdjétek el még ma!” / „¡Empezad hoy!”.
- [ ] (11.20) JORGE (tanár, Clara apja) felajánlotta: elküldi a TutorIA-t a tanár kollégáinak, ők a családoknak. Tanácsa: közösségi média + alacsonyabb ár („több ember / kisebb ár = több haszon”). → Rövid, továbbküldhető szöveg kell neki (spanyolul, linkkel); az árat átgondolni.
- [ ] (11.20) Élesítés ellenőrzése: a próbaoldalon fent van az új kód; a főoldalon (tutoriacademia.com) 21:40 körül még a régi látszott – Sándor küldjön képet a main parancsok kimenetéről.
- [x] (fix234) Lumi a mező VONALÁN ül (nem alatta), és ha az oldal elmozdul alatta (pl. megjelenik a jelszó-csík), vele megy. A jelszó megerősítő mező alatt: „✓ A két jelszó egyezik” / „✗ nem egyezik” (HU+ES); a szerver eddig is ellenőrizte.
- [x] (fix233) JELSZÓ: új jelszónál (regisztráció, új jelszó) min. 8 karakter + betű + szám (szerver is ellenőrzi); a mező alatt csík: gyenge/közepes/erős (HU+ES); Lumi a gyengénél gondolkodik, a jónál örül. Régi jelszóval a belépés marad.
- [x] (fix238) Lumi NEM lóg oldalt kötélen (Sándor: „ne oldalt a levegőben”): mindig a mező/doboz szélén marad – ha állva takarna, leül (a lába a mező üres részén), ha így is takarna, ott áll, ahol a legkevesebbet takar. Kicsit kisebb lett (gépen 116, telefonon 86 px).
- [x] (fix239) Lumi mozgása (Sándor 6 szabálya): sosem teleportál; ugyanazon a felületen SÉTÁL; szomszédos felületre kicsit UGRIK; messzire KÖTÉLEN megy (a fejléc aljáról ledobja, felmászik, átlendül, lemászik); ha görgetés miatt nem látszik, kötélen ereszkedik le a látható részre; a logóból is kötélen lendül a helyére, és úgy is mászik vissza. A becsukott GYIK-válasz rejtett szövege már nem számít akadálynak; a GYIK nyilait sem takarja; ha egy doboz fölött nincs hely, a következő dobozon áll meg. Tesztelve: gépen és telefonon, regisztráció + GYIK, 0 teleport.
- [x] (fix240) Lumi (Sándor: „belelóg a szövegbe, nem ül le, a főoldalon nem mindig jön elő”): sosem takar szöveget (a menü szövegét sem, a teste a fejlécbe sem lóg); csak LÁTHATÓ felületen áll (kártya, mező, sáv – átlátszó „láthatatlan doboz” tetején nem); ha egy ideje nem történik semmi, LEÜL a felület szélére (rosszul kitöltött mezőn nem); ha a képernyőn sehol nincs szabad hely (pl. sűrű szöveg az ÁSZF közepén), a logóban marad / hazamászik, és görgetéskor kijön, amint van hely; betöltéskor ha nincs hely, görgetéskor jön ki (a főoldalon ezért nem jött elő). Csiklandozásra csak szabad helyre ugrik.
- [x] (fix240) Lumi-ellenőrzés automatikusan: 17 oldal (kijelentkezve + bejelentkezve), HU+ES, 3 képernyőméret (1280, 1840, telefon), oldalanként betöltés/közép/alja/vissza/mezők – 306 állapot: 0 szövegtakarás, 0 levegőben állás, 0 JS-hiba, 0 teleport.
- [ ] Lumi a főoldalon (main) még a RÉGI (fix234) – ott belelóg a szövegbe. A fix240 felküldése után megszűnik.
- [x] (fix241) Lumi a fejléc ALATT halad el (nem „fejezi le” a fejléc, és ő sem lóg rá a fejlécre); ha görgetés után a feje a fejléc alá kerül, vagy alul kilóg, kötélen átmegy egy egészen látható helyre (ha nincs ilyen, visszamászik a logóba). Bejelentkezett vezérlőpult gyerekkártyákkal is tesztelve (telefon + gép).
- [x] (fix241) A lámpa körüli fehér szegély sárga lámpafény lett mind a 12 képen (static/figurak/lumi); lumi_kepek.py --jovahagy is így készíti (fej_sarga).
- [ ] Lumi: a csomagok oldal közepén (és ÁSZF/blog közepén) nincs szöveget nem takaró hely → ott a logóba mászik. Kérdés Sándornak: így maradjon, vagy legyen kisebb Lumi, hogy több helyen elférjen?
- [x] (fix242) Lumi FIGYELŐ (Sándor: „legyen okos, vegyen észre mindent, mint egy igazi kabala”): fél másodpercenként megnézi magát – egészen látszik-e, valódi felületen áll-e, nem takar-e szöveget, nincs-e a fejléc alatt; ha bármi nem stimmel, magától jó helyre megy (séta / ugrás / kötél), ha nincs ilyen hely, a logóba mászik.
- [x] (fix242) Kötél: a fejléchez kötve (görgetéskor a fejléccel megy, nem lóg a semmiben); széles képernyőn csak ott lóg, ahol fölötte tényleg fejléc van – onnan lemászik és odasétál / átugrik; lendülés közben nem bújik a fejléc alá (alacsonyabban lóg, kisebb kilengés).
- [x] (fix242) Hullámos / tépett szélű sávon (svg) a LÁTHATÓ szélére áll, nem a felette lévő üres részre (nem ül a semmibe).
- [x] (fix242) Szülői levél: pontos időszak („Az elmúlt héten (november 14–21.) nem volt tanulás.”, „November 14–21. között nem tanult.”) – HU+ES (level.py).
- [x] (fix242) Teljes ellenőrzés újra: 17 oldal × HU/ES × 3 képernyő (gép, nagy monitor, telefon) – 312 állapot, 266-ban kint van: 0 szövegtakarás, 0 levegőben, 0 fejléc alatt, 0 JS-hiba; a többiben (sűrű szöveg, nincs hely) a logóban vár.
- [x] (fix243) Lumi a talajt a KÉPPONTOK alapján keresi (nem a dobozok méretéből): ott áll, ahol tényleg látható felület kezdődik (kártya, mező, gomb, a hullám / tépett szél rajza, lábléc); az egyszínű folytatás (zöld hullám alatt zöld sáv) nem határ. Ugyanazzal a szabállyal választ és ellenőriz – nem áll a levegőben, és nem mászik vissza értelmetlenül.
- [x] (fix243) Lumi figyel: fejét az egér / ujj felé fordítja, gomb fölött a lámpája ragyog, kattintásra odanéz és bólint. Ha útközben görgetsz, új látható helyet keres (vagy a kötélen a logóba mászik).
- [ ] Lumi: a vezérlőpulton telefonon a „Gyerek hozzáadása” gomb jobb, lekerekített végén ül – nézd meg, tetszik-e.
- [x] (fix244) Lumi visszamászáskor nem mászik a logó fölé, ha közben görgetsz: minden mászás-cél a fejléchez / logóhoz mérve (görgetéskor vele megy).
- [x] (fix244) Szülői levél: „3 NAP” → „3 NAPON TANULT” (ES: „días de estudio”); a spanyol tantárgyak rendes nevükkel („Matemáticas”, „Lengua Extranjera”, „Educación Artística”), nem „Matematicas / Extranjera / Artistica”.
- [x] (fix245) Regisztráció: a „Jelszó megerősítése” mező kikerült (a jelszó a szemecskével megnézhető). A szülői kód marad, mellette kis „i” gomb: rányomva kiírja, mire jó és miért kell (HU+ES). A jelszó-visszaállításnál a megerősítés marad.
- [x] (fix246) Szülői kód „i” magyarázata: elöl, vastagon a lényeg („Hogy a gyerek ne tudjon belenyúlni a te részedbe.”), utána röviden a többi.
- [x] (fix247) Szülői kód „i”: hétköznapi hasonlat – „Ez egy gyerekzár.” / „Es como un control parental.”, utána konkrétan, mit NEM tud a gyerek nélküle (kilépni, a nevét/évfolyamát átírni, a fiókodba belenézni) és mit IGEN (tanulni, gyűjteni).
- [x] (fix247) Mintalecke lépésenkénti mérése: minden lépésnél egy jelzés (99 = a végére ért); az admin Látogatottság oldalon „Mintalecke – meddig jutottak”, a „Letöltés Claude-nak” JSON-ban „minta_lepesek”. Pár nap múlva elemezni: melyik lépésnél esik le a legtöbb (azt rövidíteni / javítani).
- [x] (fix248) Szülői kód „i”: belekerült, hogy a gyerek kód nélkül nem tud fizetni, előfizetést venni vagy módosítani (HU+ES).
- [x] (fix249) Mintalecke képei (Sándor: „ez mi, egy fej? hol a teste? nézd meg az összes képet, profin”): a tárgyak / állatok rajzai a már jóváhagyott képes szótár képeire cserélve (ugyanaz a stílus, háttér nélkül): medve (egész maci), alma, béka, hal, nyúl, asztal, iskola, jég, olvadó jég, őszi fa, labda. A fájlnevek maradtak (static/img/minta/*.svg, benne a kép), kódot nem kellett módosítani. A furcsa sün helyett a HU 1. osztályban: „iskola, labda, nyúl” és „jég, béka, naptár”. A magyarázó ábrák (gép, tízes keret, törtek, pizza, tányérok, évszakok, naptár, forralás) maradtak.
- [ ] FIZETÉS INDÍTÁSAKOR KÖTELEZŐ: minden fizetés / előfizetés-vásárlás / -módosítás / lemondás szülői kódhoz kötve (@pin_required) – ezt ígérjük a regisztrációnál! (Most a /csomagok oldal kód nélkül nézhető, de ott még nem lehet fizetni.)
- [ ] (11.22) 90 napos mérés elemzése: 1789 látogató, 2 regisztráció. A regisztrációs oldalt 183-an nyitották meg, 2-en küldték be; a hirdetésből jövők 2–7 mp után elmennek (a spanyol „fb” 2 mp). Javaslatok Sándornak: (1) hirdetés csak Facebook/Instagram hírfolyamban (Audience Network ki), (2) a hirdetés a regisztráció helyett az ingyenes mintaleckére vigyen, (3) mintalecke: 92 kezdte, 8 fejezte be – rövidíteni / megnézni, hol hagyják abba.
- [x] ~~Jorge felajánlotta, hogy továbbküldi a kollégáinak → rövid spanyol szöveg neki~~ – ELVETVE (Sándor, 11-22: „nem akarom már zaklatni”).
- [ ] Lumi: Sándor új hibáit javítani, ha jelzi (a főoldalon még vannak apró hibák – Sándor jelzi, melyek).
- [x] (fix237) LUMI SOSEM TAKAR SZÖVEGET ÉS NEM LÓG A LEVEGŐBEN: minden oldalon megkeresi azt a helyet a mező/doboz felső szélén, ahol a teste nem takar szöveget, gombot, képet; ha nincs ilyen, a doboz mellett (telefonon a képernyő szélén) kötélen lóg. Csak akkor ül le, ha a mező jó, és a lába sem takar. Hibás kitöltésnél (ha abbahagytad a gépelést) a fejét fogja.
- [ ] (fix237) FEJFOGÁS kép: python lumi_kepek.py --allapot fejfogas, majd --jovahagy --csak fejfogas → a lumi.js magától használja (addig a „gondolkodik” megy helyette).
- [x] (11.20) A main-re vitel eddig NEM sikerült: 4 el nem mentett fájl (avatar_minta.py, hirdetes_kepek.py, tanar_teszt_jelentes.md, veo_nyito.py) miatt a „git checkout main” leállt. Megoldás: git stash → checkout main → pull → merge proba → push → checkout proba → git stash pop.
- [x] (fix236) LUMI ÉLESEN IS (Sándor jóváhagyta): base.html-ből kivéve a próbaoldal-feltétel.
- [x] (fix233) LUMI BEKÖTVE – CSAK A PRÓBAOLDALON (base.html: {% if proba_oldal %}), így a main-re vitel nem teszi ki élesre. Élesre: a feltétel kivétele, ha Sándor jóváhagyja.
- [x] (fix233) Lumi kesztyű: a kész képek (static/figurak/lumi) narancsak; a szokep_uj/lumi3 a nyers, fehér kesztyűs eredeti marad. A --jovahagy scipy nélkül is narancsot ad. Az aha.png forrás: a sugár nélküli (az új, sugaras: aha_uj_sugaras.png).
- [x] (kész: fix233) (fix232) JELSZÓ ERŐSSÉG: most csak min. 6 karakter (szerver + böngésző). Javaslat Sándornak: erősség-jelző a mező alatt + Lumi reagál; döntésre vár.
- [ ] (fix232) Mérés 11.20 (1 nap): 41 látogató, FB 15 – közülük 0 nyitotta meg a mintaleckét, a főoldalon a középidő 4 mp, görgetés alig. Egy nap kevés – a hét végén újra.
- [ ] (fix231) LUMI 4. változat (Sándor: „most jó lett nagyon” – bekötésre vár): a JÓVÁHAGYOTT KÉPEKBŐL (alap, orul, gondolkodik, integet, biztat, tapsol, aha + új: maszik, ul, meglepodik, lenez), a mozgást a program adja; mászáskor a kép felváltva tükröződik (kézen-kézen). Az aha: a régi, sugarak nélküli marad (az új megint sugaras lett). Még NINCS bekötve – Sándor véleménye kell, utána base.html.
- [x] (kész: fix231) (fix230) LUMI ÚJ IRÁNY (Sándor: a 3. „fabábu”, az első kettő jobb volt; „egyszer akarom, de akkor jó legyen”): a mozgó Lumi a JÓVÁHAGYOTT képekből (static/figurak/lumi) áll, a mozgást a program adja (ugrás, lapulás, billegés, kötél). Hiányzó testtartások: python lumi_kepek.py --mozgas (maszik, ul, meglepodik, lenez – 4 kép). Ha megvannak: lumi.js átírása képekre, videó Sándornak.
- [x] (fix230) Spanyol oldal ellenőrizve: regisztráció, GYIK (16/16 kérdés), árak, adatkezelés, feltételek, fiók (csak a próbaoldali üzemeltetői gombok magyarok), gyerekprofil-űrlap, mintalecke 1–6, Feladat-próba (cseresznyés: spanyol szöveg rossz válasz után is).
- [x] (felülírva fix230) (fix229) LUMI 3. változat (még NINCS bekötve): jól látható csíkos nyak a pulóver fölött, kapucni-gallér, zsinór, zseb, mandzsetta, hosszabb karok; mászáskor a két keze fent, együtt fogja a kötelet. Sándor véleménye kell.
- [ ] (fix228) LUMI 2. változat (static/js/lumi.js, még NINCS bekötve): a logóban lakik (a lámpa az ő feje), lenéz, kötelet dob, lemászik, átugrik a mezőre; ha sokáig nincs mozgás, visszamászik, félúton meggondolhatja magát; egérre/ujjra odébb ugrik. A régi logó mentve: static/img/logo_lampa_eredeti.svg. Bekötés Sándor jóváhagyása után (base.html, minden oldalon; tanulós oldalon a logóban marad).
- [x] (fix226) KÖVETKEZŐ: a többi beszélgetős mintalecke (HU 3., 5–8.; ES 3., 5–6.) ugyanígy – Sándor átnézte az 1., 2., 4.-et, „csak a ceruzás kép volt hiba, máshoz ne nyúlj”.
- [ ] (fix227) LUMI 1. VÁLTOZAT: static/js/lumi.js (még SEHOL nincs bekötve, csak videón mutatva: regisztráció gépen + telefonon). Tud: kibújik a logóból, integet, ráugrik a dobozra, mezőről mezőre ugrál, jó kitöltésre örül, hibás/üres mezőre gondolkodik („?”), beküldéskor nagyot ugrik; kötélen ereszkedik, ha a helye kiment a képből; GYIK-nál kinyitott kérdésre „aha!”. Sándor véleménye kell, utána: base.html-be bekötni a nem-tanulós oldalakon.
- [ ] (fix226) LUMI RÉSZLETES TERV (Sándor, 11.20): a tanulási oldalon KÍVÜL (GYIK, regisztráció, csomagok…) Lumi kimászik a fejléc ikonjából, ráugrik az aktuális doboz tetejére, onnan oldalra; belépéskor lenéz, kötelet dob és leereszkedik, vagy leugrik. Reagál: a mező kitöltésekor örül, ha nem jó, gondolkodik; a végén felugrik és örül. Élethű, telefonon/tableten/gépen is jól. Gemini/OpenAI használható, ha kell. Először bemutató videó.
- [ ] (fix225) LUMI = AZ OLDAL ARCA, a fejléc bal felső ikonjában, VALÓDI MOZGÓ FIGURAKÉNT (Sándor: nem képváltás, hanem mint egy videó), ami az oldalon zajló cselekvésre reagál (pl. regisztráció kitöltése közben gondolkodik, sikerkor örül). Terv: vektoros (SVG) Lumi külön mozgatható részekkel (fej-lámpa, fény, karok, lábak), kóddal animálva – képgenerálási költség nincs. Sándor helyet mutat képen; először rövid videót mutatni.
- [x] (fix225) MÉRÉS – megvan a hiba: a felső összesítő MINDIG csak az utolsó 7 napot adta össze (a „90 nap” választásnál is), ezért mutatott kevesebbet. A napi számok rendben voltak (a letöltött JSON-okban egyeznek). Most a választott időszakot adja össze. Megjegyzés: a „látogató” napi szám – aki 3 napon jön, 3-nak számít.
- [ ] (fix224, kész: lásd fix225) MÉRÉS: Sándor szerint nem jó. A kód: app.py ~400–530 (rögzítés), app.py ~19330–19400 és ~19746 (üzemeltetői oldal, letöltés, törlés), database.py ~3990–4170 (tárolás, összesítés), templates/base.html ~200–225 (kattintás/görgetés/idő mérő), templates/admin_latogatottsag.html (megjelenítés). Kérdés: mi nem jó benne?
- [x] (fix221) Beszélgetős mintalecke élesen KI (csak a próbaoldalon), amíg minden évfolyam nincs kész. Élesen: MINTALECKE_BESZELGETES=1.
- [ ] (fix221) Teszt-változások (30 perc, hibák gyakorlása): a szabályokat Claude szimulált gyerekkel kipróbálta (jó); a TESZTÍRÓ AI új utasítását (2–3 kérdés az előző hibákból) élesben még senki nem látta – az első valódi bukott teszt után megnézni.
- [x] (fix220) Fejléc: a gyerek oldalain és a mintaleckén görgetéskor ELTŰNIK (nem marad fent, nem lóg bele semmibe). Mintalecke: a kapszula belépett szülőnél is.
- [x] (fix220) Csomagok: a tervezett ár MINDENKINEK látszik, belépés nélkül is („Tervezett ár – még nem vásárolható”).
- [x] (fix220) Mintalecke: a 💡 emoji és a kis PNG helyett az oldal saját lámpája (ugyanaz a rajz, mint a fejlécben).
- [ ] (fix220) Sándor: „a bemutató jó így, mehet a többi is” → a többi évfolyam beszélgetős mintaleckéje táblával (HU 1, 3–8; ES 1, 3–6), mindegyikhez „másképp magyaráz” rossz válasznál + „kérdezz bátran” + legalább egy megfogható feladat.
- [x] (fix218) Fejléc a gyerek oldalain: a kapszula mögötti sáv TÖMÖR (görgetéskor nem látszik mögötte a tartalom). Album: a gyereksáv lekerekítve, középre.
- [x] (fix218) Mintalecke gépen: bal oldalt TÁBLA (mint a valódi órán), jobbra a beszélgetés; telefonon a rajz a beszélgetésben, a tanító üzenetei után.
- [ ] (fix218) Csomagok: az árakat CSAK belépett szülő látja (2026-11-07-i döntés: „tervezett ár”), kívülről „Hamarosan”. Sándor kérdezte, miért nincs ár → kérdés: mutassuk-e mindenkinek.
- [ ] (11.19) BEMUTATÓ VIDEÓ (terv a válaszban): 45–60 mp, telefonon, valódi programból felvéve, felirattal, hang nélkül is érthető.
- [x] (fix217) Fejléc: a gyerek oldalain (lecke, album, bolt, PIN-oldal) is a fehér kapszula + színes csík, mint a szülői oldalakon (gépen). Eddig szándékosan maradt ott a régi zöld (fix138: „a gyereksáv a kapszula alá csúszna”) – most nem lebeg, így nem csúszik. Visszaállítás: style.css utolsó blokkja.
- [x] (fix219) Gyereksáv: a gyerek SAJÁT avatarja a lámpa helyett; a név 26 karakterig kiírva; a szülői PIN-oldalon nincs gyereksáv.
- [x] (fix212) Ismételt leckezáró: az új teszt MÁS kérdésekből áll (az AI mindig újat ír), és most 2–3 kérdés kifejezetten az előző hibákat nézi, új számokkal/szavakkal (Sándor kérése). Csak írásbeli tesztnél; a szóbelinél még nem.
- [ ] (fix212) FACEBOOK-ELEMZÉS (Sándor: az okot kell megtalálni): a mi adatunkból csak annyi látszik, hogy a FB-ról jövők fele 2 mp alatt elmegy, görgetés nélkül. A Meta Hirdetéskezelőből kell: (1) „Kattintások a linkre” ↔ „Céloldal-megtekintések” (ha az utóbbi sokkal kevesebb: véletlen kattintás vagy lassú betöltés), (2) bontás ELHELYEZÉS szerint (Audience Network / Messenger / Instagram / Facebook hírfolyam – az Audience Network gyakran véletlen kattintás), (3) bontás KOR és NEM szerint, (4) maga a hirdetés szövege/videója. Sándor küld képernyőképet.
- [x] (11.19) Meta-adatok (spanyol hirdetés): 71 kattintás → 64 céloldal-megtekintés (jó, nem véletlen kattintás, nem lassú); csak Facebook hírfolyam (nincs Audience Network). DE KOR: a kattintások ~60%-a 45 év feletti, 1/3-a 65+ (23 a 71-ből). Ők nagy eséllyel nem 6–12 éves gyerek szülei → megnézik, 2 mp alatt mennek. JAVASLAT: korcélzás 28–50 (mint a HU 28-50 sorozatban), ugyanazzal a napi 3 €-val; egy hét után összevetni (2 mp-es kilépők aránya, mintalecke-kezdők, regisztráció).
- [x] (fix215) DÖNTÖTT (Sándor): minden sikertelen leckezáró után 30 perc tanulás (a hibákra), utána új teszt, 70%-tól továbbléphet. GYIK is átírva.
- [x] (11.19) A FB-hirdetés kor-gondja: az Advantage+ célközönség terjesztette ki 65+-ra a 28–50-es beállítást. Sándor kikapcsolta (11.19 20:20). Egy hét múlva összevetni.
- [x] (fix215) Piroska szelíd változata a tanárnak: a nagymama elbújik a szekrényben (így a gyerek érti, hová lett, amikor a farkas az ágyban van).
- [ ] (fix212) Főoldal: a diak.png 237 KB – webp-be téve gyorsabb mobilon (FB-n belüli böngésző).
- [ ] (fix212) Bemutató videó a főoldalra (mint az isiestudio-nál): profi, 30–60 mp, a VALÓDI programot mutatja (beszélgetés + interaktív feladat). És: kell-e egy figura „jelnek” a lámpa helyett – a programban már van kabala, lehet abból.
- [ ] (fix207) Sándor kérése (pontosítva 11.19): a FELADATOKAT kell szétválasztani (pl. feltöltés külön, képkészítés külön), de egy feladat parancsai EGY blokkban jöjjenek – nem soronként.
- [ ] (fix207) Hangmódos felolvasás költsége: Azure karakter, a napi keretbe számít; a példák és a gyakori kérdések szövege mindig ugyanaz → a gyorstárból ingyen jön. Ha sok lesz: csak 1–2. osztálynak.
- [ ] (fix207) Fizetés bekötésekor (EU-levél): ár „áfával együtt” felirattal; digitális szolgáltatásnál a vevő országának áfája (HU 27%, ES 21%) – az árból ennyivel kevesebb marad. Könyvelővel egyeztetni.
- [x] (11.19) ELVETVE (Sándor döntése): előre felvett magyarázat NEM kell – a jó tanár mindig a gyerekhez igazodik, a sablon unalmas, és a tanár sem tudja meg, min kell segíteni. Marad az élő tanár. Ami megmarad belőle: a Volume (1. pont). A régi terv:
  1. [ ] MARAD: a Railway hang-gyorstár Volume (/data/hangcache) – enélkül minden push után kiürül a mentett hang, és újra fizetünk érte. Ez a legolcsóbb nyereség.
  2. Leckénként 1–2 rövid, ELLENŐRZÖTT magyarázó blokk (szöveg + egyszer legenerált hang); a tanár (AI) tudja, hogy ez elhangzott, és onnan folytatja kérdésekkel, feladatokkal.
  3. A gyerek bármikor közbeszólhat / kérdezhet → arra MINDIG élő AI-válasz.
  4. Előbb 1–2 témán kipróbálni, mérni: hány karakter spórolás, és a gyerek érzi-e a különbséget.
- [ ] (11.19) Azure: Sándor szerint JELENLEG NEM fizet az Azure-nak (ingyenes F0 szint?). Ellenőrizni a portálon: F0-n havi ~0,5 millió karakter ingyenes, utána a hang NÉMÁN leáll → idegen családok előtt S0 kell.
- [x] (fix250) A GYEREK KABALÁJA (kislány/kisfiú/robot) telefonon rátakart a lecke címére és szövegére (HU+ES, Sándor képernyőképei). OK: a gyerek egyszer odahúzta a figurát, a hely elmentődött, és a figura a KÉPERNYŐHÖZ ragadt (position:fixed) – görgetéskor ráült mindenre. Javítás (csak templates/chat.html): a húzás kikapcsolva (HUZHATO=false, a régi mentett helyet törli), a figura a magyarázat bal alsó sarkában marad; és – mint Luminál – ha szöveg, gomb, kép vagy mező kerülne alá, félreáll (eltűnik), szabad helyen visszajön. A buborék ugyanígy. Asztali gépen a helye nem változott.
- [ ] TANÍTÁS / UX (Sándor, 11-22): a valódi óra első üzenete hosszú szövegfal – gyereknek unalmas. Ötlet: rövidebb darabok, hamarabb tábla-feladat. Jóváhagyás nélkül NEM módosítjuk (a tanítás minősége nem romolhat).
- [ ] VIDEÓ v2 (spanyol, 9:16): mintalecke + kártyagyűjtés (csomagbontás, album) + szülői rész („¿Cómo va?”, heti e-mail, szülői kód). Kitalált gyerek („Lucía”), valódi név/e-mail nem látszik. Kabala és bolt kimarad.
- [x] (fix251) Telefonos hibák (Sándor képernyőképei, HU+ES közös fájlok, Sándor jóváhagyta): (1) a kabala „Szia, … vagyok!” buboréka a figura MELLÉ került, nem takarja el; (2) a gyerek felső menüsora telefonon EGY sor (kép, 4 gomb, érme, lakat), az érme helyén valódi arany érme-ikon (gépen is); (3) a lecke fejléce telefonon: ← | cím | érme | ⛶ egy sorban, alatta a tantárgy/szint/idő; a ⛶ (teljes képernyő) gomb telefonon újra látszik; (4) ALBUM LASSÚ: a borító hatszögeibe is az eredeti 1–2,4 MB-os PNG-k töltődtek (16 lap ≈ 25 MB). Új útvonal: /kartyakep/<static-útvonal>?w=160|240|400|800 – kicsinyített WebP, a cache/kartya_kicsi mappába (a static/kartyak-hoz nem nyúl). Nagyításkor az eredeti kép jön. Pillow az fpdf2-vel jön; ha mégsem lenne, az eredeti képre irányít át; (5) a kártyalapon a tantárgy felirata lekerült a képről, a jobb oldali szöveg fölé, kis színes betűvel.
- [ ] (fix251 után) Más oldalak is az eredeti nagy kártyaképeket töltik (tasakbontás, gyűjtemény, kinézet?) – ha lassúnak tűnnek, ugyanígy /kartyakep-re váltani.
- [ ] KINÉZET (Aspecto) oldal: Sándor szerint „kicsit gagyi” (hátterek, avatar-figurák, saját avatar szerkesztő). Nem hiba – később szebbre tervezni, előtte látványterv jóváhagyásra.
- [x] (fix252) A LECKE FEJLÉCE – „A” terv (Sándor választotta, HU+ES): gépen ← | cím | érme | Teszt (sárga keretes) | hangos mód | ⛶ egy sorban, mind 38 px; alatta címkék (tantárgy, AI-tanár, szint, „Quedan 180 min” / „Még 180 perc” – új kulcs: lecke_hatra_rovid, a teljes mondat a súgóban); alatta a 4 lépés. Telefonon ← | cím | ⛶; címkék; lépések; alattuk „Már tudod? ⭐ Szintfelmérő teszt” (új kulcs: chat_test_elo). Telefonon az érme csak a felső menüben (az is frissül tanulás közben). A „Hangkeret” próbagomb kikerült a fejlécből, jobbra lent van (csak próbaoldal).
- [x] (fix253) Fejléc + alsó sáv újra (Sándor: „sok helyet foglal”, a teszt nem gomb, a hangos mód gomb rossz helyen, a Hangkeret rátakart): GÉPEN 2 sor – címkék balra, mellettük a 4 lépés a sor végéig kihúzva (1350 px alatt a lépések a címkék alatt, teljes szélességben). TELEFONON ← | cím | 🎙 (zöld kör = hangos módra vált) | ⛶; egy sor kis szöveg (tantárgy, AI, szint, idő); lépések + valódi „⭐ Teszt” gomb (új kulcs: chat_test_rovid). Alsó sáv EGY sor: 💬 | üzenetmező | Küldés (nyelvórán a 📖 is ikon). A Hangkeret próbagomb a Feladat-próba dobozában (formaction), telefonon máshol nem jelenik meg. Hibajavítás: a teszt gomb [hidden] állapota eddig nem rejtette el.
- [x] (fix254) Laptopon (1350 px alatt) a címkék sora is kihúzva a teljes szélességre, egyforma cellákban. Az idő-címke érthetőbb: „Még 121 perc a leckéből” / „Quedan 121 min de lección” (a lecke tervezett tanulási idejéből ennyi van hátra; ha lejár, jöhet a záró teszt).
- [x] (fix255) A táblán a **szó** vastag betű lesz (a csillagok eltűnnek); a fejléc címkéi halványan áttetszők; a Feladat-próba doboz (csak admin) telefonon a „✥” feliratnál elhúzható.
- [ ] A BESZÉLGETÉS buborékaiban is látszhat a **szó** (a spanyol angolórán a tanár markdownt ír). Ott még nincs javítva; jobb lenne a forrásnál: a tanár promptjában tiltani a ** jelölést. Jóváhagyás kell (tanítás).
- [ ] LECKEHOSSZ: a spanyol tantervben nincs óraszám, ezért becslés (évfolyam-alap × nehézség × 3, max. 180 perc) – sok spanyol lecke (pl. Educación Artística, Inglés) 180 percet kap, ami egy gyereknek soknak tűnik. Javaslat: a „kisebb” tantárgyakra (művészet, testnevelés, zene, nyelv) rövidebb plafon, vagy a spanyol becslés csökkentése. Sándor döntése kell.
- [ ] ÁR / KONVERZIÓ (Sándor, 11-23; Jorge is az árat kérdezte): 90 nap alatt 1789 látogató, 83 nézte a csomagokat, 183 jutott a regisztrációs oldalra, 2 regisztrált. Ötletek: olcsóbb, hang nélküli belépő csomag (a hang a fő költség), „órás bérlet” helyett havidíj-érzetű megfogalmazás, napi ár feltüntetése. Előbb mérni: a csomagokat néző látogatók közül hányan mentek tovább a regisztrációra.
- [ ] ÁRAZÁS – HÁROM SZINT (11-23; árak ellenőrizve: gpt-5.4-mini 0,75/0,075/4,50 $, gpt-transcribe 0,0045 $/perc, Stripe 1,5–3,15% + 0,25 € és Billing +0,7%, autónomo 2026 ~300–360 €, tarifa plana nem jár; Azure Neural 16 $/1M – az árlap 11-23-án nem mutatta). Egy perc: MÉRT (napló + /admin) néma 0,9 ct, hangos 1,7 ct · ÓVATOS (30 000 bemenő token, 80% gyorsítótár, 600 karakter hang, 27% áfa, 3,5% Stripe, 0,95 árfolyam) néma 1,3 ct, hangos 2,6 ct · LEGROSSZABB (gyorsítótár sem működik) néma 2,8 ct, hangos 4,2 ct. Maradék egy előfizetőn ÓVATOSAN: 6 órás 15,90 → 4,63 €; 10 órás 24,90 → 6,69 €; 18 órás 39,90 → 8,53 €; írásos 6 óra 11,90 → 5,24 €; írásos 10 óra 17,90 → 7,45 €. LEGROSSZABB esetben minden csomag ~0 vagy veszteség → a gyorsítótárat figyelni kell. Állandó költség óvatosan ~521 €/hó (autónomo 360, könyvelő 80, Railway 40, egyéb 21) → fedezet: ~110 db 6 órás vagy ~75 db 10 órás előfizető; havi 2000 € tiszta haszonhoz ~540 db 6 órás vagy ~375 db 10 órás. A koltsegek_pontos.html ezekkel az óvatos értékekkel van kitöltve (fix259).
- [ ] LECKEHOSSZ – MÉRVE (11-23): a képlet (iskolai óraszám × 60 × 0,3, max. 180) miatt szinte MINDEN lecke 180 perc: a spanyol oldalon az összes (a témakörök 10–30 órásak), magyaron az angol, ének, rajz, testnevelés, magyar 4. o. is. Javaslat (Sándor döntése kell): évfolyam szerinti cél ~4 alkalomra (1–2. o. 80 perc, 3–4. o. 100, 5–6. o. 120, 7–8. o. 140), a témakör súlyával ±25%, a készségtárgyak (rajz, ének, testnevelés, dráma) fele ennyi; kijelzés alkalmakban.
- [ ] EGYSZERŰ KÖLTSÉGSZÁMOLÓ Sándornak: a mért értékek előre beírva, csak az előfizetők számát kell megadni (a koltsegek_pontos.html neki túl bonyolult).
- [ ] HANG CSAK FIZETŐSNEK (ötlet, Sándor kérdezte): hang nélküli csomagnál hangos_perc = 0 → a 🔊 gombok és a hangos mód gombja el sem jelenik. Megoldható, döntés kell (melyik csomag, milyen ár).
- [ ] EGY ÉVFOLYAM IDEJE a javasolt leckehosszal (fő tantárgyak; most / javasolt percben): HU 2. o. matek+magyar+környezet 3470 / 1825 perc (≈30 óra); HU 4. o. +angol 5270 / 3280 (≈55 óra); HU 6. o. matek+magyar+angol+történelem 4915 / 3630 (≈60 óra); ES 2. o. mat+lengua+conocimiento+inglés 3780 / 1675 (≈28 óra); ES 4. o. 3780 / 2105 (≈35 óra); ES 6. o. 3780 / 2520 (≈42 óra). 6 órás bérlettel (270 perc/hó) ez kb. 6–13 hónap, 10 órással 4–8 hónap. Megjegyzés: az ES angol katalógus évfolyamonként csak 1 témakört ad – ellenőrizni.
- [ ] INDULÁSI CÉL (11-23): óvatos számokkal a nullához ~110 db 6 órás / ~75 db 10 órás előfizető kell; lemondásokra 20–30% tartalékkal ~100–150. Az autónomo járulék alacsony jövedelemnél kisebb (~205–300 €) – a gestoríával megbeszélni, MIKOR kell bejelentkezni és mekkora sávval.
- [ ] LEGFONTOSABB MOST: senki nem regisztrál. 183-ból 2 – a magyar hirdetés 131 embert egyenesen a regisztrációs űrlapra vitt, ott átlag 6 mp-et maradtak. Javaslat: a hirdetés a mintaleckére vigyen (regisztráció nélkül kipróbálható), és a végén kérje a regisztrációt; személyes csatornák (tanárok, szülői csoportok, magyar családok Spanyolországban); 5–10 családnak ingyen hozzáférés valódi visszajelzésért.
- [x] (fix256) ÚJ LECKEHOSSZ (Sándor jóváhagyta): 1–2. o. 80 perc, 3–4. o. 100, 5–6. o. 120, 7–8. o. 140; témakör-súly ±25%; készségtárgy (ének, zene, vizuális, artística, testnevelés, Educación Física, dráma) fele. Pl. ES matek 4. o. 90–110 perc, testnevelés 30–55. Visszaállítás: Railway LECKE_HOSSZ_REGI=1. FIGYELEM: aki egy leckében már többet tanult az új hossznál, annál a lecke ideje azonnal letelik (jöhet a záró teszt). Fejléc: új „⏱ Ma 12 perc” / „Hoy 12 min” címke a „Még … perc” mellett (lecke_ma kulcs).
- [ ] 10 TESZTCSALÁD költsége (1 hónap, 450 perc/család): óvatosan (2,6 ct hangos perc, teljes kihasználás) ~118 €, mért árakkal ~77 €; reálisan (60% kihasználás) ~45–70 €.
- [ ] ÖTLETEK (Claude, 11-23): (1) „Az iskolával együtt” – a szülő lefényképezi a heti tanmenetet/házit, a tanár arra a hétre állítja össze a leckéket; (2) Nagyszülő-ajándék – magyar nagyszülők ajándék-tanulást vesznek a külföldön élő unokának (magyar nyelv); (3) Barát-ajánló – mindketten kapnak +2 órát és egy arany kártyát.
- [x] (fix257) VISSZATÉRŐ JELÖLŐ-HIBÁK, TARTÓSAN (Sándor: „5x javítottuk, mindig előjön”): (1) „<FL:en>I have ___ finished</FL>” a beírós feladaton – az OK: a „szövegből kinyert” feladat (_feladat_szovegbol) kimaradt a tisztításból. Most a függvény maga tisztít, ÉS a chat végén egy végső háló minden úton jött feladatot megtisztít (a nyitó feladatnál is). (2) <VOCAB>…</VOCAB> a gyerek kék buborékjában – a gyerek üzenetéből a szerver kiszedi (_gyerek_uzenet_tisztit). (3) A képernyőn is van háló: a tábla, a feladat és a buborékok szövegéből a jelölők eltűnnek (chat.html, MutationObserver). (4) hang_teszt.py 3 új esettel – ha valaha visszajön, a teszt „NE PUSHOLJ”-t ír.
- [x] (fix257) NYELVÓRÁN a lecke ideje mindig 0 volt („Még 179 perc” 20 perc után is): a tanulási időt a nyers fájlnévvel mentjük, a lecke a „fájl::angol@HU” kulccsal kereste. database._tanulas_targy_kulcsok most a nyers nevet is elfogadja. (Kis kockázat: ha egy gyerek ugyanabból a fájlból két nyelvet is tanul, a percek összeadódhatnak – ritka.)
- [x] (fix257) Nyelvválasztó zászlók: zöld csík és világos szegély eltűnt (a .targy-jel svg zöld körvonala ráment a zászlóra).
- [ ] TANULÁSI IDŐ MÉRÉSE (Sándor: a lánya „több mint 21 percet” tanult): a számláló csak az AKTÍV időt méri (megáll, ha a lap háttérben van vagy nincs mozgás; a kitérő nem számít), és bezáráskor az utolsó szívverés utáni pár perc elveszhet. Ha ez kevés, megnézni a tétlenségi küszöböt.
- [ ] ÖTLETEK 2 (Claude, 11-23): „Fizess, ha megtanulta” (lecke-alapú ár, csak a sikeres záró teszt után); „Vacsoraasztali 3 kérdés” – a szülő esténként 3 kérdést kap e-mailben/telefonon, amit megkérdezhet a gyerektől (AI-költség nélkül, a szülő látja az értéket).
- [ ] HOLNAP (11-24) ELLENŐRIZNI a próbaoldalon (fix256–257 push után): (1) angolórán a „Még … perc” beszámítja a korábbi perceket; (2) kilépés/visszalépés után nem ugrik vissza; (3) nincs <FL:en> / <VOCAB> a feladatban és a buborékban; (4) „⏱ Ma … perc” a fejlécben; (5) tiszta zászlók; (6) 2. o. matek lecke 60–100 perc. A hang_teszt.py 11-23-án: 58/58 rendben.
- [ ] NAGYSZÜLŐ-AJÁNDÉK (Sándor: „nézzük meg”) – terv: ajándékkártya (nyomtatható PDF + kód, rajta a gyerek neve), pl. 3 hónap 10 óra ~69 €; a nagyszülő fiók nélkül fizet, e-mailben kapja a kártyát; a szülő a „Szülőknek” részben beváltja. A fizetés bekötése (Stripe) után építhető.
- [-] „Fizess, ha megtanulta” – Sándor: elvetve.
- [ ] Ötletek 3 (Claude): „Iskola spanyolul, otthon magyarul” (a spanyol iskolai anyagot magyarul magyarázza a gyereknek ÉS a szülőnek – Spanyolországban élő magyar családoknak); „Nyáron szünetel ingyen” (csak tanév közben fizet); írásos 10 óra 14,90 € (óvatosan ~5,20 € marad).
- [ ] KARÁCSONY (Sándor, 11-23): a nagyszülő-ajándékkártya most jönne jól, de a fizetős rész még nem működik. Döntés kell: fizetés (Stripe) bekötése karácsony előtt (~4 hét), előtte gestoría (számlázás, autónomo-bejelentkezés időpontja).
- [ ] CSOMAG-ÖTLET „GYŰJTŐ-BÉRLET” (Claude saját): éves előfizetés + a gyerek kártyáiból az év végén NYOMTATOTT album hazapostázva (koltsegek.html: album ~14 € + posta ~5 €). Ajándéknak is: „Egy év tanulás + saját album”. Kérdés: nyomda, postaköltség Spanyolországba és Magyarországra.
- [ ] 10 € ALATTI BELÉPŐ (Jorge kérése): „Írásos 5 óra 9,90 €” (300 perc) – óvatos számokkal ~3,30 € marad, reálisan ~5 €.
- [ ] ÍRÁSOS 6 ÓRA 9,90 € (Sándor kérdése): marad óvatosan (1,28 ct/perc, 27% áfa, 3,5% kártyadíj, teljes kihasználás) ~2,60 €; mért árakkal teljes kihasználásnál ~4,65 €, 60%-nál ~5,90 €.
- [ ] KARÁCSONYI INGYENES AJÁNDÉKKÓD (Claude ötlete, fizetés nélkül is megy): a szülő/nagyszülő ingyen küldhet egy kódot (pl. 5 óra) egy gyereknek → új regisztrációk, karácsonyi ok a megosztásra. Korlát: pl. 50 kód (költség óvatosan ~3–8 €/gyerek). Gestoríának feltenni: eladhatok-e pár ajándékkártyát/előfizetést próbaként autónomo nélkül, és mikortól kell bejelentkezni?
- [ ] ALBUM (Sándor: „mentsük el, jó ötlet”): utánanézni, mennyibe kerül egy egyedi, nyomtatott album matricákkal, és hány darabtól vállalják a nyomdák (minimum példányszám).
- [ ] AJÁNLÓ – „Hozd el a barátod” (most is megcsinálható, fizetés nélkül): minden szülőnek saját meghívó link; ha a barát regisztrál ÉS a gyereke legalább 15 percet tanul, mindkét család +2 órát kap (a gyerek egy arany kártyát). Karácsonyi szöveggel is mehet. Költség óvatosan ~1–3 € / család.
- [-] Ingyenes karácsonyi ajándékkód – elvetve: lényegében ugyanaz, mint a mostani ingyenes próba.
- [ ] AJÁNLÓ csak FIZETÉS UTÁN (Sándor jogos kifogása: kamu e-mail, ismerős meghívása, aki sosem fizet): jutalom csak akkor, ha a meghívott család ELŐFIZET (pl. a meghívó +2 óra vagy egy olcsóbb hónap). Fizetés nélkül nem építjük.
- [ ] FŐ IRÁNY (11-23): árazásban az írásos csomag (pl. 6 óra 9,90 €) a járható út; a legnagyobb gond viszont a regisztráció. A spanyol hirdetés 11-23-tól a mintaleckére visz – pár nap múlva megnézni a mintalecke lépésmérését (meddig jutnak) és a regisztrációkat.
- [x] (fix258) HANG NÉLKÜLI CSOMAGOK (Sándor döntése): a csomagok oldalán kapcsoló „✍️ Hang nélkül / 🔊 Hanggal”, alapból hang nélkül. Hang nélkül: 6 óra 9,90 €, 10 óra 14,90 €, 18 óra 24,90 € (csomagok.py: alap_iras, pro_iras, max_iras; hangos_perc = 0). Hanggal marad 15,90 / 24,90 / 39,90 €. Az óra = 45 perc (tanóra), a lapon mellette a perc is ott áll → nem félrevezető. JAVÍTOTT számok (1 óra = 45 perc!): marad óvatosan ~3,75 / 5,20 / 8,10 €, reálisan ~5,40 / 7,90 / 12,90 €.
- [ ] FIZETÉS INDÍTÁSA ELŐTT: hang nélküli csomagú családnál (hangos_perc = 0) a 🔊 gombok és a hangos mód gombja EGYÁLTALÁN ne jelenjenek meg (most csak a keret 0 lenne → „elfogyott” üzenet).
- [x] (fix259) A hang nélkül / hanggal kapcsoló a csomagok oldalán MINDEN LAPON külön (Sándor kérése), nem közös a lapok fölött. Fölötte egy fehér címke: „Minden bérlet kérhető hang nélkül vagy hanggal – a lapon tudsz váltani.” A lapon vált az ár, a hang-sor és az „Ennyiért kérném” gomb csomag-kulcsa (alap_iras ↔ alap stb.).
- [x] (fix260) A lapon lévő kapcsoló alatt egy rövid sor magyarázza a különbséget (vált a kapcsolóval): „A gyerek olvas és ír – a tanár írásban válaszol.” / „A tanár felolvas, és a gyerek beszélhet is vele.” (ES: „El niño lee y escribe; el profe responde por escrito.” / „El profe lee en voz alta y el niño también puede hablarle.”)
- [x] (fix261) ÓRA → PERC MINDENHOL (Sándor: „az órát alkalomnak értették”, Jorge is): bérletnevek „270 / 450 / 810 perc / hó” (ES „… min / mes”); a lapon „Bármelyik tantárgyra”; átvihető PERCEK; segítő, napi jelentés, GYIK-blokk a csomagok oldalon („Mi számít tanulási percnek?”), fióktörlés szövege, ÁSZF 7. és 9. pont (HU+ES), GYIK oldal („a számláló megáll”). A GYIK „Meddig tart egy lecke?” válasza az új leckehosszra javítva (fix256). A jogi mappa (DPIA, nyilvántartás) nem érintett.
- [ ] PAGESPEED (11-24): gép 98/95/100/100, mobil 97/95/100/100 – nagyon jó. Javítandó: (1) statikus fájlok gyorsítótár-ideje (1,1–1,8 MB ismételt letöltés), (2) a főoldal képei túl nagyok (1–1,9 MB megtakarítható, WebP + méret), (3) „Elkezdem →” gomb (fo-gomb) gyenge színkontraszt, (4) képek width/height hiányzik. A Geekflare 27-es teljesítménye félrevezető (más mérési hely/beállítás) – a Google PageSpeed a mérvadó.
- [x] (fix262) Böngésző-gyorsítótár: betűtípus 1 év, kép 7 nap, verziós CSS/JS 1 év (app.py _biztonsagi_fejlecek). FIGYELEM: azonos néven cserélt képet a visszatérő látogató max. 7 napig a régiként láthatja. GYIK „Meddig tart egy lecke?” pontosítva: 30 perc után szintfelmérő (hibátlan → továbbléphet), különben a leckezáró teszt.
- [ ] GEEKFLARE (11-24): LCP 4,7 s, CLS 0,219 (4 elrendezés-ugrás), TBT 840 ms, 12 hosszú feladat, max. FID 1430 ms – a főoldalon sok a JavaScript-munka (gyanú: Lumi animáció / pixelelemzés) és a képek méret nélkül ugrálnak. Javaslat: képek WebP + width/height, Lumi indítása később (a betöltés után). A hirdetésből érkezők 2–5 mp alatt döntenek – ezért számít.
- [ ] PERC KEREKÍTÉS (Sándor ötlete): 270→300, 450→480, 810→840 perc. Többletköltség előfizetőnként havonta teljes kihasználásnál óvatosan ~0,40 € (írásos) / ~0,80 € (hangos), reálisan ~0,26 / 0,50 €.
- [ ] SZABÁLY (fix262 óta): KÉPET SOHA NE CSERÉLJ UGYANAZZAL A FÁJLNÉVVEL – adj új nevet (pl. kep_2.png), vagy szólj Claude-nak. Különben a visszatérő látogató 7 napig a régit látja. Szöveg-, HTML-, oldalmódosításra ez NEM vonatkozik: az azonnal frissül.
- [ ] FIZETÉS BEKÖTÉSE ELŐTT DÖNTENI: percek felkerekítése (270→300, 450→480, 810→840)? Lásd a fenti számokat.
- [ ] KÖLTSÉGCSÖKKENTÉS – ÖTLET (Claude, 11-24): rövidebb tanári válaszok. A költség nagyobb része (gyorsítótárral ~75%) a tanár SZÖVEGE (kimenő token). Ha a tanár ~30%-kal rövidebben ír, a perc ~20%-kal olcsóbb, ÉS a gyereknek is jobb (Sándor: „szövegfal”, unalmas). Tanítást érint → Sándor jóváhagyása + tanar_teszt kell.
- [x] MODELLCSERE ELLENŐRIZVE (11-24, Gemini cikk-összefoglalója alapján): GPT-6.2 Sol 2,00 / 0,10 / 10,00 $ (be / gyorsítótár / ki, 1M token), Astra 8 / 0,40 / 40 $, GPT-6.1 Terra 1 / 5 $ – a mostani gpt-5.4-mini 0,75 / 0,075 / 4,50 $. A Sol percenként ~2,2× DRÁGÁBB lenne (~1,9 ct a mostani ~0,87 ct helyett), nem olcsóbb. A 6-os modelleket okt–nov-ben a tanar_teszt már kipróbálta (luna, sol, terra). OpenRoutert a TutorIA nem használ (közvetlenül az OpenAI-t hívja).
- [x] (fix263) Csomagok: az ár mellett „/ hó · áfával” („/ mes · IVA incluido”); az ÁSZF 7. pontja is írja: „Az árak véglegesek, az áfát tartalmazzák”. GYIK: „kb. 100 perc, 120 perc…” (HU+ES). Lumi csak az oldal betöltése után indul (max. 4 mp várakozás) – lumi.js. Főoldal: a kisfiú képe előre lefoglalja a helyét (width/height), nem ugrik az oldal.
- [ ] ÉVES ELŐFIZETÉS (Sándor fél tőle): óvatos számokkal (gyorsítótárral) minden csomagon marad pénz (pl. írásos 6 óra 99 €/év → ~2,70 €/hó; hangos 159 €/év → ~2,90 €/hó). Ha a gyorsítótár NEM működne, havonta és évesen is mínusz lenne – ezért a [CACHE] naplót figyelni kell. Döntés a fizetés bekötése előtt.
- [ ] RÖVIDEBB TANÁRI VÁLASZOK: Sándor kérdése, mennyire befolyásolja a tanítást → előbb tanar_teszt (pár €): ugyanazok a leckék rövidebb utasítással, összevetve.
- [x] Gemini 4 Neon ára ~3 / 15 $ (be/ki, 1M token) – kb. 4× drágább a mostaninál.
- [ ] (fix264) RÖVIDEBB TANÁRI ÜZENETEK – PRÓBA: app.py TANAR_ROVID kapcsoló (alapból KI, élesen semmi nem változik). Mérés Sándor gépén: `python tanar_teszt.py --ora 6` kétszer – egyszer simán, egyszer `$env:TANAR_ROVID = "1"` után (ugyanaz a véletlen sorrend, seed 12345). A két jelentést (tanar_teszt_jelentes_hu_…md) Claude összeveti: hiba, érthetőség, kimenő token / ár. Csak akkor élesítjük (Railway: TANAR_ROVID=1), ha a tanítás nem romlik.
- [ ] RAILWAY [CACHE] (11-23 napló): a nagy hívások 88–96%-a gyorsítótárból – rendben. Elég havonta egyszer ránézni.
- [ ] (11-24) TANAR_ROVID MÉRÉS KÉSZ: 6 óra, 36 hívás mindkettőben. Hiba 13 biztos/6 gyanús → 5/3. Átl. tanári üzenet 95 → 60 szó, kimenő token −25%, válaszidő 5,6 → 4,4 mp. Tartalom megmaradt (magyarázat + példa + feladat). Következő: Railway PROBA-n TANAR_ROVID=1, pár valódi óra után döntés a main-ről.
- [x] (11-24, fix265) Robotos feladat „csak számsor”: CSAK a tanar_teszt hibája volt (élesben a 6×6 pálya rendben megjelenik). tanar_teszt.py most érthetően leírja a pályát a teszt-gyereknek.
- [x] (11-24) „Benvesd a kezed”: egyszeri AI-elírás az óra közben, nem sablon/tananyag (sehol nincs a fájlokban). Nincs mit javítani; ha gyakran előjön ilyen, szabály kell.
- [ ] ‼️ ELSŐBBSÉG – FIZETÉS INDÍTÁSA ELŐTT / 20+ GYEREK FÖLÖTT (Sándor: „kapjon prioritást, akár a csomagáron is lehet csökkenteni, vagy több a bevétel”). GYORSÍTÓTÁR-ÁTRENDEZÉS: most minden új óra első üzenete (és 5–10 perc szünet utáni) teljes áron megy (~33 ezer token). MÉRÉS (11-24, helyben, 1 gyerek × 3 tantárgy): a tanári utasítás ~68%-a minden órán azonos, de a változó részek szét vannak szórva: 1. sor a tanár neve (gyerekenként más); „Tanítványod/Tantárgy/Aktuális témakör” sorok; több helyen az évfolyam (pl. 2. osztály 7 helyen); KERETTANTERVI ANYAG blokk; a tantárgyfüggő feladattípus-lista (27-től) középen; ÚJ TANTÁRGY blokk. 4 változat: HU / ES × rendes / nyelvóra. TERV: kapcsoló (alapból KI), a változó részek a végére, közös prompt_cache_key (pl. tutoria-v1); Sándor csak PowerShellben futtat 2× tanar_teszt-et (nem kell az oldalon tesztelnie), Claude helyben méri az azonos előtagot. Haszon: ~1–1,5 ct óránként az elején → ~1 €/gyerek/hó (100 gyereknél ~100 €/hó). A DeepSeek és a Gemini is ezt javasolta (a DeepSeek „1,25× írási ár” állítása az OpenAI-ra NEM igaz). Mérőszkript: /tmp-ben volt (cap.py: a /chat/send hívást elkapja, a promptot kiírja).
- [ ] (11-24) LÁTOGATOTTSÁG: a /login oldalon érkezők (11-24: 29 a 53-ból, pedig csak Sándor lépett be) valószínűleg botok/saját böngésző → a /login-t ne számoljuk az érdeklődők közé (kis munka). Sándor: minden családi eszközön nyissa meg egyszer: tutoriacademia.com/nem-szamolj
- [-] (fix266 → VISSZAÁLLÍTVA fix267, Sándor: „ez nem jó irány”; a „veled együtt” azt sugallja, hogy a szülő is taníthat; az „AI téved” ne legyen kiírva) FŐOLDAL BIZALOM (egy FB-hozzászólás után: „leülök olvasni, tanítás helyett?”): „Te pihensz, ő tanul” → „Ő gyakorol, te látod, mit tanult”; „Kicsiknél együtt”; „Nem helyetted tanít – veled együtt”; új pont „És ha téved?”; „Ki áll mögötte?” (név és fotó NÉLKÜL); ár a 120 perc mellett (9,90 €-tól) a főoldalon és a regisztrációnál. NYITOTT: a 18 mp-es VIDEÓBA bele van égetve a „Te közben pihenhetsz.” felirat (anya a kanapén, gyerek egyedül) – ellentmond az új üzenetnek; döntés: marad / elrejtjük / új videó (pénzbe kerül). FIZETÉS INDÍTÁSAKOR átírni: „így semmi nem terhelődik” (a próbára igaz, a megújuló előfizetésre nem).
- [ ] (11-24) Sándor: a fejléc bal felső „kötél” (Lumi lóg a logón?) továbbra sem jó – képernyőképpel megmutatja, mikor kapja el.
- [x] (fix269, 11-25) GYORSASÁG – adatok (nov. 4–22.): 1789 látogató, a főoldalon a középérték 4 mp (hirdetésből 5 mp), csak 47 görgetett; 183 regisztrációs oldal → 2 beküldés; mintalecke 92 kezdte / 8 befejezte. Mérés lassú 4G + 4× lassabb telefon: első tartalom 3,1 mp → 1,0 mp, teljes betöltés 6,9 → 2,4 mp. Javítás: (1) gzip tömörítés (app.py _tomorit, vészfék TOMORITES=0; style.css 132 → 29 KB, HTML 70 → 22 KB); (2) a 13 Lumi-kép csak Lumi indulásakor töltődik (lumi.js kepekElore); (3) főoldali kisfiú: diak.png 238 KB → diak_v2.webp 36 KB (ÚJ NÉV, a régi fájl marad). Nem tudtuk élesen mérni (a Railway saját tömörítése ismeretlen) – Sándor után: Railway naplóban nincs [TOMORITES] hiba.
- [ ] (11-25) Mintalecke 2. o. végigjátszva (jó és rossz úton): tartalmilag rendben. A fő gond nem a minta, hanem hogy a látogatók 4–5 mp alatt elmennek. Következő: „meleg” látogatók (ismerősök, csoportok); a videó-poszter (142 KB) a hajtás alatt is azonnal töltődik – lehetne lusta betöltésű.
- [ ] (11-25) PROBA [CACHE] 0%: egy órán belül egymás utáni üzenetek is 0% (09:43–09:44, Hon- és népismeret 5., child 5), a rendszer-prompt hossza változott (47577 → 47311 → 47014), de a 3. és 4. azonos hosszú volt, és az is 0%. Helyben (Matematika, 75 mp különbséggel) a rendszer-prompt BITRE AZONOS, prompt_cache_key megvan. Kérdés: a main naplóban mennyi a [CACHE] egy órán belül? Ha ott 80–95%, ez csak a próbán van (kevés forgalom / OpenAI útvonal); ha ott is 0%, ki kell deríteni (pénzbe kerül!). A fix269 tömörítés NEM okozhatja (az a böngésző felé megy, nem az OpenAI felé).
- [x] (fix271, 11-25) Geekflare a próbán fix269 után: LCP 4,7 → 2,7 mp, FCP 1,8 mp, oldalméret 974 KB; Performance 38 (TBT 730 ms, CLS 0,224, Max FID 1500 ms). Okok helyben mérve: (1) CLS = betűcsere (tartalék betű → Nunito, gépen 0,17) → base.html: a Nunito fájlok preload-dal indulnak (latin-ext csak HU) → CLS 0; (2) a leghosszabb blokkolás Lumi helykeresése (induláskor ~6000 elementsFromPoint, fele ismétlés) → lumi.js verem() emlékezik egy lefutáson belül → 2,2 s → 0,9 s (4× lassított CPU), Lumi helye ugyanaz. Ha még kell: Lumi helykeresését tovább gyorsítani (pl. ritkább lépés) – ez már a viselkedését is érintheti, csak Sándor OK-jával.
- [ ] (fix272, 11-25) LUMI VISSZAÁLLÍTVA a fix269 előtti állapotra (Sándor: „kaotikusabb, nem ül le, a kötél a logó fölé megy, Lumi eltűnik, a GYIK-nál ki sem jön – eddig jó volt”). Helyben NEM tudtam előidézni (a GYIK-nál régi és új változatban is kijön; azonos véletlennel ugyanoda áll). Ha a visszaállítás után is így van → régi hiba, nem a fix269/271 okozta (akkor Lumi külön átnézése). Ha megszűnik → a fix269 (képek később) vagy fix271 (verem-emlékezés) volt a hibás, egyenként visszatenni. Geekflare 11-25 fix271 után: Performance 61, CLS 0, TBT 400 ms, LCP 2,9 s; PageSpeed mobil Speed Index 4,2 s.
- [ ] (11-25) LUMI A GYIK-NÁL NEM JÖN KI Sándornál (gépen) – a fix272 visszaállítás UTÁN IS → RÉGI hiba, nem a mai módosítás. Helyben (1350 px, kint és belépve) kijön. Kell: képernyőkép / ablakméret / görgetett-e azonnal. Utána a fix269 (Lumi-képek később) és fix271 (helykeresés gyorsítása) visszatehető egyenként. Csomagok oldal: a „Jelezted – szólunk, amint indul” NEM hiba – Sándor korábban rányomott az „Ennyiért kérném”-re; a felirat szövege Sándornak nem egyértelmű (döntés kell).
- [ ] (fix275, 11-25) A GZIP TÖMÖRÍTÉS (fix269) MIATT LUMI A GYIK-NÁL NEM JÖTT KI a próbán (Sándor: TOMORITES=0 után jó). Helyben nem jön elő. Most ALAPBÓL KI (app.py), a Railway TOMORITES változó törölhető. Ki kell deríteni, miért (lehet, hogy a Railway amúgy is tömörít – akkor nem is kell). A fix269 Lumi-képek-később és a fix271 Lumi-helykeresés-gyorsítás KIVÉVE (fix272) – ezek valószínűleg ártatlanok, a TBT miatt egyenként visszatehetők, Sándor OK-jával. Lumi helyezkedése több oldalon „nem a legjobb” (Sándor) – később.
- [x] (11-26) MAIN [CACHE] rendben: órán belül 93–99% (11-25 13:54–14:04, 11-26 09:04–09:25). 0% csak az óra első üzenete és a kis (~400 token) segédhívások – utóbbiak 1024 token alatt nem is tárolhatók, elhanyagolható költség. A proba 11-25-i 0%-a nem ismétlődött a mainen.
- [ ] (11-26) LUMI A GYIK-NÁL a MAINEN SEM jön ki (Sándor), pedig ott a tömörítés KI van → a gzip-elmélet valószínűleg téves. Helyben 1280–1745 px széles, 560–800 magas ablakban, kint és belépve is kijön. Ha Lumi nem talál helyet (indul(): h == null), bent marad a logóban – valószínű ok. Lumi-javító körben: hibakereső mód (?lumi=nez) + tartalék hely, ha nincs jó felület. Kérdés Sándornak: Ctrl+F5 után is?
- [ ] (11-26) LÁTOGATOTTSÁG: dátumválasztó (naptár) az admin oldalon, hogy tetszőleges napot/időszakot lehessen nézni (Sándor kérése).
- [x] (fix280) MINTALECKE LÉPÉSMÉRÉS – OK: a mérés jó, de a „kezdések” egy részét böngészőnek álcázott gépek (linkbejárók) adták: megnyitják a /minta/N oldalt, JS-t nem futtatnak, így lépés sincs. Most a „kezdte” csak az első lépés jelzésekor számít (app.py mintalecke_lepes n=0). ELŐZMÉNY: a letöltésekben a minta_lepesek mindig üres → nem látszik, hol hagyják abba. 11-25: 21 kezdte (évfolyamonként 3–4, ebből 13 belső – valószínűleg Sándor vagy gép), 0 fejezte be. Javítani, mielőtt a mintaleckéről döntünk.
- [x] (fix290) SZÓJEGYZÉK KERESŐ KÉSZ (chat.html, mindkét oldal): keresőmező a szójegyzék tetején, 6 szótól látszik, mindkét nyelven és ékezet nélkül is keres („viz” → víz), „Nincs ilyen szó” jelzés. ELŐZMÉNY: a szójegyzék tetején keresőmező, a saját nyelven (HU/ES) is lehessen keresni, ha már sok szó van. Mindkét oldal.
- [x] (fix281, csak HU oldal) NYELVÓRA – megoldva: a naplóból kiderült, a 10 szó egy sorban = 10 <VOCAB> jelölő a kérdés után, amit a program „választéknak” vett. Most: 4-nél több jelölő vagy a kérdésben már felsorolt szavak → nem látszik (a szójegyzékbe bekerül). Plusz tanári szabály: választós kérdésben csak EGY jó válasz, közeli jelentésű szó nem lehet rossz lehetőség, ugyanaz a kérdés ne ismétlődjön, egy üzenetben max. 3 VOCAB. NYITOTT: spanyol oldalon (angol óra) is kell? – Sándor dönt. Mérés: python tanar_teszt.py --tantargy idegen --evfolyam 8 --ora 2. ELŐZMÉNY: „Melyik szó jelenti azt, hogy »valószínűleg«: seguramente, probablemente vagy tal vez?” – (1) KÉT jó válasz is van (seguramente ≈ valószínűleg/biztosan, probablemente = valószínűleg) → szabály: választós feladatban csak EGY opció lehet helyes, közeli szinonima nem lehet zavaró opció; (2) utána a szólista („el futuro, seguramente, …, tal ve”) a szövegben – honnan jön? Képernyőkép kell. Sándor: nem ezt az egyet, hanem az ilyen HIBATÍPUST javítani.
- [-] (11-26) Sándor ötlete: a lecke szövegét és hangját egyszer legyártani, AI csak a gyerek kérdésére. Elvetve: a tanítás minden válaszhoz igazodik (rossz válasznál másképp magyaráz), előre gyártott szöveggel ez elveszne; a gyorsítótár már most 93–99%-kal olcsóbbá teszi az ismétlődő részt.
- [ ] (11-26) VIDEÓK helye: kinézet képek/facebook/hirdetes – HU végleges: tutoria_reel_este_v7.mp4 (ugyanez van a főoldalon); ES: tutoria_reel_este_es.mp4 és tutoria_reel_zsiraf_es.mp4 (zsiráfos HU változat nincs). Profi FB-hirdetések: később, ha a csoportokból jön regisztráció.
- [ ] (11-26) FB-csoportok: a régi gyerekruhás oldal (~3000 követő) és az andalúziai/Cádiz csoport (~2100) – ide mehet a „véleményt kérek” bejegyzés (HU / ES).
- [ ] (11-26) LÁTOGATÓSZÁM IS FELFÚJT lehet ugyanezektől a gépektől (pl. 11-24: 29 belépés a /login oldalon, pedig csak Sándor lépett be). Ötlet: „valódi látogató” = akinél a böngésző JS-e is jelzett (pl. görgetés-/időmérő jel). Később.
- [ ] ‼️ (11-26) LÁTOGATOTTSÁG ALAPOS ÁTNÉZÉSE (Sándor: „ez adja nekünk az infót, nincs hőkameránk – pontos, mindenre kiterjedő beállítás kell”). Terv: (1) gépek kiszűrése: „valódi látogató” csak akinél a böngésző JS-e jelzett; (2) minden szám mellé magyarázat; (3) dátumválasztó (naptár); (4) tölcsér: főoldal → mintalecke (lépésenként) → csomagok → regisztráció → első óra; (5) forrás pontosan (FB csoport / hirdetés / Google / közvetlen); (6) régi és új számok összevethetők legyenek.
- [ ] (11-26) Facebook: a feltöltött videót Reelként tette ki (nem a bejegyzések között látszik), a zsiráfosat rendes bejegyzésként. Kétszer is felment – az egyik törölhető.
- [ ] (11-26) Lumi a MAIN GYIK-nál frissítés (Ctrl + ⟳) után sem jön ki → régi hiba, Lumi-körben.
- [x] (fix282) Nyelvóra-szabály a SPANYOL oldalon is (angolóra; Sándor: „ha nem árt, igen”) + kiegészítős mondatnál csak egy lehetőség illhet (a teszt hozta: „I have ___ finished” → already és just is jó). tanar_teszt 11-26 (8. o. spanyol+angol, fix281 után): spanyolnál a lehetőségek már egyértelműen különbözők (el mundo / la tecnología / el futuro); 2 biztos hiba az angolon (kétértelmű kiegészítés, „már minden szót ismersz”, aztán új szó).
- [ ] (fix282) A BETŰ-ELŐTÖLTÉS (fix271, base.html) KIKAPCSOLVA – Sándor szerint 11-25 óta Lumi a GYIK-nál nem jön ki (11-24-én 10/10 jó volt); a 11-25-i változásokból ez maradt az egyetlen minden oldalt érintő. Ha ezután kijön → ez volt; ha nem → tovább keresni (index/app.py többi változása). A gépi elrendezés-ugrás (CLS) ettől visszajöhet.
- [x] (11-26) LUMI GYIK OKA MEGVAN (Sándor gépének böngészőjében, azonos ablakméretben összevetve): a main és a proba GYIK oldala csak a 7 betű-előtöltő sorban különbözik (main: fix271 van, proba: fix282 nélküle). Proba: Lumi kijön; main: Lumi bent marad (nem talál helyet). → a fix282 a javítás, mehet a mainre. Helyben (headless) nem jön elő – időzítésfüggő. Mellékesen: a main a lumi.js-t már TÖMÖRÍTVE kapja (21 KB a 68 KB helyett) – a Railway/edge magától tömörít, a saját gzip (fix269) felesleges, maradjon KI.
- [x] (fix284) LUMI MAIN GYIK – A VALÓDI OK (a betű-előtöltés kivétele után is rossz volt): Sándor gépének böngészőjében a main GYIK-on Lumi induláskor nem talált helyet és többé nem próbálta (window.__lumi.hely() = null), pár mp-cel később ugyanott már talált (__lumi.doboz() = DETAILS.fp-k0). A main Cloudflare-en át megy, más az időzítés. Javítás: lumi.js kijonHaLehet() – ha nincs hely, 0,7 mp-enként még 6-szor próbál. A fix282 (betű-előtöltés ki) ezért visszatehető lenne – később, Sándor OK-jával.
- [x] (11-26) AI-modell figyelő ütemezett feladat MEGVAN (11-17 óta, hétfőnként 11:13, push értesítés; utoljára 11-23, következő 11-30). Claude tévesen mondta, hogy nincs.
- [x] (fix285) LÁTOGATOTTSÁG 1. kör: (1) VALÓDI LÁTOGATÓ = a böngésző jelzett (új „lat” jel 1 mp után, vagy idő/görgetés/kattintás/mintalecke-lépés/űrlap) – a gépek külön számban („+ N gép vagy azonnal távozó”); a tölcsér (Hol akadnak el?) már csak valódiakat számol; a napi táblában „Valódi” oszlop. (2) NAPTÁR: tol–ig dátum, a letöltés is ezt az időszakot adja (max. 400 nap). (3) Magyarázat a tölcsér fölött. Figyelem: a „lat” jel csak a feltöltés után indul – a régebbi napoknál a valódi szám csak azokat mutatja, akik görgettek/kattintottak/elhagyták az oldalt (alacsonyabb lehet).
- [x] (fix287) LÁTOGATOTTSÁG 2. kör KÉSZ: magyarázat a tölcsér minden sora alatt; új lépés „Elkezdte az első órát” (regisztráció napján, ugyanazon eszközön); forrásnevek (fb_hirdetes_hu = „Facebook-hirdetés (magyar)”, fb_hirdetes_es = spanyol; Sándor 11-26-án beállította a két hirdetés linkjét); mintalecke lépésnevek. ELŐZMÉNY: minden szám mellé rövid magyarázat; „első óra elkezdve” lépés a tölcsér végére; forrás pontosítása (melyik FB-csoport – utm_source linkek Sándornak); a mintalecke lépéseinél a lépés NEVE (ne csak sorszám).
- [ ] (fix286) LUMI MAIN GYIK – fix284 után IS rossz (Sándor). Sándor böngészőjében mérve: az új kód kint van, a hely MOST megvan (helyDoboz OK), ugyanaz a kód utólag lefuttatva KIJÖN – tehát betöltéskor akad el. Gyanú: a görgetés-figyelő (bejon) „kijott=true”-t tesz, majd a kijövés hibára fut (nincs hely → h1.y), és utána a „kijott” örökre lezárja az utat. Javítás: hiba/hely nélkül a jelző visszaáll, 4 mp-es újrapróba; HIBAKERESŐ NAPLÓ: tutoriacademia.com/gyik?lumi=nez → window.__lumiNaplo (Claude olvassa ki). Ha ez sem segít, a naplóból látszik az ok.
- [ ] ‼️ SZABÁLY (Sándor, 11-26: „ami működik, ahhoz ne nyúljunk”): (1) ami jól működik (Lumi, lecke, feladatok, regisztráció, csomagok), azt csak külön feltöltésben, egy dologként módosítjuk; (2) közös fájlt (base.html, lumi.js, app.py fejlécek/after_request, style.css) csak kifejezett ok mellett; (3) MINDEN main-feltöltés után Claude Sándor böngészőjében megnézi a main oldalt (főoldal, GYIK + Lumi, csomagok, egy lecke) – a main a Cloudflare miatt másképp viselkedhet, mint a proba; (4) ha valami elromlik: azonnal visszaállítás, utána keresgélés.
- [ ] (11-26) LUMI MAIN GYIK: Sándor saját Chrome-jában 10 betöltésből egyszer sem jön ki (fix286 után is); a Claude-böngészőben (külön profil) kijön. Következő: Claude-in-Chrome bővítménnyel Sándor Chrome-jában megnyitni: tutoriacademia.com/gyik?lumi=nez → window.__lumiNaplo. Tartalék: ha nincs hely, fix biztonságos helyre üljön. Hirdetések 11-26: magyar napi 5 €, spanyol napi 10 € (anyukás videó).
- [x] (fix288→289) Főoldal „Hogyan működik?” 2. lépés: a magyar oldalon a kép helyett rajzolt doboz (mint a spanyolon) – telefonon nem vágja le a Matematikát. Sándor ellenőrizte.
- [ ] ‼️ HIBA (Sándor, 11-26): LUMI A MAIN OLDAL GYIK-JÁN NEM JÖN KI (Sándor Chrome-jában; a proba GYIK-on és a main többi oldalán jó). 11-24-ig jó volt. fix282/284/286 nem oldotta meg. Következő: Sándor Chrome-jában (Claude-in-Chrome bővítmény) megnyitni tutoriacademia.com/gyik?lumi=nez és kiolvasni window.__lumiNaplo; tartalék: ha nincs hely, fix biztonságos helyre üljön.
- [ ] (11-26, Sándor) MAGYAR FELOLVASÁS: a mondatvégi hangsúly/hanglejtés nem jó (pl. kérdésnél, felsorolásnál). Később megnézni: Azure SSML (prosody / mondatvégi írásjel), másik magyar hang (Noémi ↔ Tamás), rövidebb mondatok. A hanghoz csak Sándor OK-jával nyúlunk.
- [ ] (11-26) NÉPSZERŰSÍTÉS – ötletek: (1) külföldön élő magyar családok és magántanulók FB-csoportjai (magyar tananyag külföldön) – legerősebb; (2) otthonoktatók csoportjai; (3) valódi szülői visszajelzések engedéllyel az oldalra; (4) 1–2 tanító ingyen használja és ajánlja; (5) második hirdetésvideó a valódi leckéről. Megfigyelés: sokan jönnek, de félnek az AI-tól – ötlet: a főoldal első képernyőjén az „AI-tanár” felirat helyett/mellett a gyakorlás legyen elöl (A/B mérés a látogatottságon).
- [ ] (11-26) fix292: ÖT ÚJ MATEK-FELÜLET 3–4. o. (HU és ES): irasbeli (írásbeli összeadás/kivonás lépésről lépésre, maradékkal), szamvonal (számegyenes nagyítóval, 100/1000/10000), muveletisor (műveleti sorrend, zárójel), kombinacio (maci öltöztetése, sapka × póló), merlegkg (kétkarú mérleg súlyokkal, kg/dkg/g – ES: kg/g, aztán átváltás). Próbán Sándor nézze meg (Feladat-próba lista), utána külön main deploy. Megjegyzés: a régi "szamegyenes" név a béka felületé, ezért lett az új neve szamvonal.
- [x] (11-26, fix293 kész: az öltöztetős feladat AI-macija és rétegei, 4 szín) KOMBINACIO: a maci rajza „nagyon gagyi” (Sándor). Újra kell rajzolni szebbre (pl. AI-képes figura, mint a krokodil: static/figurak/), a sapka- és pólószínek maradjanak cserélhetők. A többi 4 új felület rendben.
- [ ] (11-26) META HIRDETÉS: Audience Network kikapcsolása a hirdetéssorozatokon (sok robot/véletlen kattintás: 74-ből 53 kattintás a videós HU hirdetésen). Utána a látogatottság oldalon a „Valódi” számot nézni, nem a Meta kattintásait.
- [x] (11-26) fix293 IRASBELI: a maradékot a gyerek MAGA írja be (összeadásnál a következő oszlop tetejére, kivonásnál a lenti szám mellé), ahogy a régi oszlopos táblában (Sándor kérése); a magyarázat megmaradt. muveletisor és kombinacio leírásába: ELŐTTE magyarázza el a tanár.
- [x] (11-26) fix294 IRASBELI: minden művelet-fajta első példája vezetett (lépésenként, magyarázattal), a többit a gyerek EGYEDÜL csinálja, mint a régi oszlopos táblában (bármelyik négyzetbe ír, maradékot is, OK-ra ellenőriz, hibás oszlop piros + magyarázat). Alapból 2 azonos fajta művelet. KOMBINACIO: a kérdés („Hány különböző öltözet lett?”) most a számgombok fölött is ott van.
- [x] (11-27) fix295 KOMBINACIO: a végén számok helyett SZÁMÍTÁSOK közül választ („Melyik számítással kapod meg?” 3 · 2 = 6 / 3 + 2 = 5 / …) – így arra jön rá, hogy ez szorzás (Sándor: a számokat nem értette, a macikat csak meg kellett számolni).
- [x] (11-27, fix296 kész, egyelőre CSAK a magyar oldalon – spanyolra Sándor OK-ja kell) MINTALECKE 8. o. (függvénygép): a „kérdezz bátran” lépésnél az „Értem, jöhet a következő!” gomb után nincs következő feladat, rögtön vége. Sándor kérdése: „kérek még feladatot erre” – tisztázni: gombszöveg javítása, vagy legyen „Kérek még egy feladatot” gomb is (a hasonló feladatokkal). Az összes mintaleckét érinti (_kerdez).
- [ ] (11-27) PINTEREST: Sándor kérdezte, érdemes-e ott hirdetni. Javaslat: előbb ingyenes pinek (letölthető feladatlap → link a mintaleckére), fizetett hirdetés csak ha a FB-n már van regisztráció.
- [x] (11-27) fix297 MINTALECKE: a „Kérek még egy feladatot” gomb a spanyol oldalon is (Sándor OK). 8. o. függvénygép: a kép eddig 1→3, 2→5, 3→7 példákat pörgetett (elárulta a választ), a hasonlóknál 10-et mutatott 5 és 0 helyett → most a kép a feladat számát mutatja (3 → ?, 5 → ?, 0 → ?).
- [ ] (11-27) MINTALECKÉK ÁTNÉZÉSE (Sándor: „lehet az összes feladatot át kellene nézni”): a táblaképek egyeznek a szöveggel, kivéve: 3. o. „befagy a tó” → jégkocka kép (gyenge, nem hibás). Végigjátszani mind (HU 1–8, ES 1–6), szöveg + kép + válaszok.
- [x] (11-27) fix298 MINTALECKE 8. o.: a hiba nem a gomb volt, hanem hogy az „Értem, jöhet a következő!” után nem jött feladat (csak a 8. o.-ban volt a „kérdezz bátran” a lecke végén). Átrakva a titkos gép elé, mint a többi leckében. Biztosíték: ha egy leckében a „kérdezz bátran” után már nincs feladat, a gomb egy hasonló feladatot ad, vagy őszintén „Értem, nézzük, hogy ment!” a felirat. A fix296/297 külön „Kérek még” gombja ezzel megszűnt.
- [ ] (11-27) ÜZENET A SZÜLŐKNEK (Sándor): finoman kiemelni, hogy mi TANÍTUNK (a többi oldal csak feladatlapot ad), és oldani az AI-tól való félelmet. Szövegjavaslatok a chatben – Sándor dönti el, hova (főoldal/FB), és melyik állítás igaz.
