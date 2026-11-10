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
- [ ] Automatikus AI-kódellenőrzés minden push után (becslés: havi 1–5 $) – fizetés előtt.

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
