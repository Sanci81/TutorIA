# Cursor-promptok – 2. rész (a kabala és a maradék 48 elem)

## Így használd (lépésről lépésre)
1. Nyisd meg a Cursort a TutorIA mappával.
2. Jobb oldalt a csevegőablak tetején válaszd az **Agent** módot. A modellnél hagyd az alapot („Auto”) – ha a listában látsz „DeepSeek” vagy „Kimi” nevűt, az olcsóbb, azt is választhatod.
3. Másolj be **EGY** promptot (a ``` jelek KÖZÖTTI részt, a jelek nélkül), és nyomd meg az Entert. Várd meg, amíg kész.
4. A végén a Cursor kiírja, mit ellenőrzött. Ha valamelyik ellenőrzés hiányzik, írd neki: „Nem csináltad meg az ellenőrzést, csináld meg most.”
5. Ha kész, ezeket írd be a PowerShellbe (a TutorIA mappában):
```
git checkout proba
git add -A
git commit -m "Cursor: <a prompt száma>"
git push origin proba
```
6. Nézd meg a próbán (lásd lent). Ha valami elromlott és nem javítható: `git checkout -- .` (ez eldobja a be nem küldött változást), és szólj nekem.

Sorrend: 1, 2, 3 … 13. Egyszerre csak egyet!

**Ellenőrzés a próbán minden elem-prompt után:** egy órán kérd a tanártól az új feladatot (pl. „Adj egy feladatot a kör részeiről!”), telefonon is nézd meg: megjelenik-e, működik-e, a Kész után válaszol-e a tanár. Ha megjelenik, de rossz: ne küldd tovább a mainre, és írd meg nekem, melyik.

---

## 1. PROMPT – A kabala nyugodtabb legyen

```
Feladat a templates/chat.html fájlban: a képes kabala (kisfiú/kislány, a "kabalaKepEl" és "KABALA_KEP" részek) túl gyakran és túl hirtelen vált arcot. Legyen nyugodtabb. Csak a kabala JavaScriptjéhez és CSS-éhez nyúlj, máshoz NE. A fájl CRLF sorvégű, így is maradjon.

1. A KABALA_KEP táblában a 'gepies' értéke legyen 'alap' (ne lepődjön meg minden új feladatnál), a 'cuki' maradjon 'nevet', a 'kivancsi' maradjon 'alap'.
2. A kabalaUnatkozik függvényben: ha kabalaKepEl létezik (képes kabala), az üresjárati váltás 30–50 másodpercenként legyen (30000 + véletlen 0–20000 ms), és csak a 'koszon' vagy 'cuki' közül válasszon. A robotnál (kabalaVaszon) minden maradjon a régi.
3. A kabalaKepValt függvényben: ha az előző váltás óta 1500 ms-nél kevesebb telt el, és az új állapot NEM 'orul', 'szomoru' vagy 'kesz', akkor ne váltson (hagyja ki). Ehhez jegyezd meg az utolsó váltás idejét (Date.now()).
4. Lágyabb áttűnés: a .chat-kabala.kabala-allapotos CSS átmenete legyen "opacity .35s ease", és a kabalaKepValt-ban a setTimeout késleltetése 140 helyett 350 ms.
5. A kabalaVillan függvényben, ha képes kabala van, az alap visszaállás ideje legalább 3500 ms legyen.

ELLENŐRZÉS (kötelező, írd ki): sorold fel a megváltoztatott sorokat (előtte/utána). Nézd meg, hogy a <script> blokkban nincs szintaktikai hiba.
```
**Ellenőrzés:** egy órán a kabala ritkábban váltson, és ne „villogjon”.

---

## 2. PROMPT – kor, maganh, jly, irasjel

```
ELEMEK: kor, maganh, jly, irasjel
MINTAOLDAL: "Claude outputs/interaktiv_minta6.html"

Feladat: a MINTAOLDAL sorban megadott mintaoldal fenti elemeit (a <section id="..."> azonosítók) beépíteni a TutorIA chat-táblájára, magyarul és spanyolul. Ugyanúgy, ahogy az előző 40 elem be van építve – azokat kövesd PONTOSAN mintának.

HOL VAN A MINTA
- templates/chat.html: a "var DM = {};" sornál kezdődik a futtató rész (dmKornyezet: a D objektum – D.T, D.$, D.html, D.el, D.txt, D.ellenoriz, D.vege, D.kuld, D.kartyaHuzas, D.huzosLista, D.billentyuzet, D.mond …). Utána jönnek a kész elemek: DM.csoport, DM.tortcmp, DM.kerekit, DM.romai, DM.naptar, DM.szervek, DM.venn stb. A "// ── 2. csomag (5–6. minta) ──" megjegyzés után a legújabbak.
- templates/chat.html CSS: a ".dm .dm-kesz-sor{margin-top:12px}" sor környékén vannak a .dm-es szabályok.
- app.py: a _feladat_parse_belso függvényben az `if tipus == "csoport":` … `if tipus == "akcio":` blokkok (az `if tipus == "modell":` ELŐTT) – ezek ellenőrzik szerveroldalon a tanár által küldött adatot.
- app.py: _DM_FELULETEK lista (tuple-ok: tipus, címkék, évfolyam-tól, -ig, magyar leírás + <FELADAT> példa, spanyol leírás + példa, magyar választó-sor, spanyol választó-sor) és a _dm_cimkek függvény.
- tanar_teszt.py: a `if tipus in ("csoport", "szotag", ...` sor.

MIT CSINÁLJ ELEMENKÉNT (a tipus neve = a section id)
1. chat.html: `DM.<tipus> = function (f, D) { ... };` a "2. csomag" blokk UTÁN, a `function feladatElem(f) {` sor ELÉ, egy új "// ── 3. csomag (6. minta) ──" megjegyzés alá. ES5 (var, function), 4 szóköz behúzás.
   - A rajz és a működés a mintaoldalé legyen (Sándor jóváhagyta), de: NINCS „Új feladat” gomb, egy feladat = egy elem; a lényeges adatot a tanár adja (f.*), véletlen csak a nem lényeges dolgokhoz.
   - id-k helyett data-id + D.$('…'); minden látható szöveg D.T('magyar', 'español'), természetes spanyolországi spanyollal. Spanyol tantervnél (D.es) a tartalom is spanyol.
   - Befejezés: D.ellenoriz(fn) – a Kész gomb; fn {hianyzik, jo, uzenet, valasz}-t ad vissza –, vagy önmagától eldőlő feladatnál D.vege(jo, uzenet, valasz); a második rossz próbálkozás után a válasz mindenképp elmegy (nézd meg DM.tortcmp-ben). A `valasz` egyes szám első személyű mondat a gyerek nevében (ez megy a tanárnak), az `uzenet` rövid magyarázat a gyereknek.
   - Hang: SOHA ne speechSynthesis. Ha kimondás kell, csak D.mond(szöveg). A hangrendszerhez nyúlni TILOS.
   - Ha több SVG-ben ugyanaz a gradiens/szűrő id lenne, tedd egyedivé.
   - Gyereknek (6–12 év) érthető legyen; nincs tagadó vagy dupla tagadó kérdés; a feliratok nem lóghatnak egymásra; 320 px széles telefonon se lógjon ki semmi.
2. CSS: csak ami hiányzik, minden szelektor ".dm " előtaggal, a ".dm .dm-kesz-sor" sor UTÁN. Globális szabály (body, button stb. előtag nélkül) TILOS.
3. app.py: `if tipus == "<tipus>":` blokk az `if tipus == "akcio":` blokk UTÁN, az `if tipus == "modell":` ELŐTT. Ellenőrizd, hogy a feladat megoldható és egyértelmű; gyanús → return None. A kérdés: _rov(adat.get("kerdes"), 120) vagy jó magyar/spanyol alapértelmezés (es_tanterv szerint); figyelj a ragozásra (ne „a(z)”, ne „5-os”).
4. app.py: új tuple a _DM_FELULETEK lista VÉGÉRE, a meglévők mintájára. Címkék: "matek", "kornyezet", "magyar", "enek", "nyelv", "digit". Ha az elem történelem (korszak), vegyél fel egy "tortenelem" címkét: a _dm_cimkek függvényben `if any(k in s for k in ("tortenelem", "historia")): c.add("tortenelem")`.
5. tanar_teszt.py: az új típusneveket add hozzá a `if tipus in ("csoport", "szotag", ...` felsoroláshoz.

SZIGORÚ SZABÁLYOK
- Meglévő elemekhez, a dmKornyezet-hez, a hang-rendszerhez és a static/kartyak mappához NE nyúlj. Ne formázd át a meglévő kódot. A fájlok CRLF sorvégűek, így is maradjanak.
- Ne találj ki új D-függvényt a közös részbe; ha valami kell, az elemen belül írd meg.

ELLENŐRZÉS (kötelező, írd ki az eredményt – ha valamelyik nem sikerül, mondd meg őszintén)
- python -m py_compile app.py tanar_teszt.py → hibátlan.
- Keresd vissza és írd ki a sorszámmal: minden "DM.<tipus> = function" a chat.html-ben, minden `if tipus == "<tipus>":` az app.py-ban, minden ("<tipus>", tuple a _DM_FELULETEK-ben.
- Írj egy ideiglenes Python-szkriptet (NE a projektbe), amely `import app` után minden új típusra meghívja: app._feladat_parse_belso('<FELADAT>{...}</FELADAT>', grade=4, es_tanterv=False/True, temakor='x') – egy jó magyar, egy jó spanyol és egy hibás bemenettel. Írd ki a kimenetet: a jónál dict, a hibásnál None kell.
- Nézd át a chat.html-t: a <script> blokkban nincs szintaktikai hiba (pl. `node -e` -vel a blokk kiszedése és new Function-nel ellenőrzése).
```

---

## 3. PROMPT – elolj, rovar, foto, korszak

```
ELEMEK: elolj, rovar, foto, korszak
MINTAOLDAL: "Claude outputs/interaktiv_minta6.html"
KÜLÖN MEGJEGYZÉS: Az "elolj" angol elöljárószók ("nyelv" címke). A "korszak" történelem: vegyél fel "tortenelem" címkét a _dm_cimkek függvényben: if any(k in s for k in ("tortenelem", "historia")): c.add("tortenelem"). Spanyolul: Prehistoria, Edad Antigua, Edad Media, Edad Moderna, Edad Contemporánea.

Feladat: a MINTAOLDAL sorban megadott mintaoldal fenti elemeit (a <section id="..."> azonosítók) beépíteni a TutorIA chat-táblájára, magyarul és spanyolul. Ugyanúgy, ahogy az előző 40 elem be van építve – azokat kövesd PONTOSAN mintának.

HOL VAN A MINTA
- templates/chat.html: a "var DM = {};" sornál kezdődik a futtató rész (dmKornyezet: a D objektum – D.T, D.$, D.html, D.el, D.txt, D.ellenoriz, D.vege, D.kuld, D.kartyaHuzas, D.huzosLista, D.billentyuzet, D.mond …). Utána jönnek a kész elemek: DM.csoport, DM.tortcmp, DM.kerekit, DM.romai, DM.naptar, DM.szervek, DM.venn stb. A "// ── 2. csomag (5–6. minta) ──" megjegyzés után a legújabbak.
- templates/chat.html CSS: a ".dm .dm-kesz-sor{margin-top:12px}" sor környékén vannak a .dm-es szabályok.
- app.py: a _feladat_parse_belso függvényben az `if tipus == "csoport":` … `if tipus == "akcio":` blokkok (az `if tipus == "modell":` ELŐTT) – ezek ellenőrzik szerveroldalon a tanár által küldött adatot.
- app.py: _DM_FELULETEK lista (tuple-ok: tipus, címkék, évfolyam-tól, -ig, magyar leírás + <FELADAT> példa, spanyol leírás + példa, magyar választó-sor, spanyol választó-sor) és a _dm_cimkek függvény.
- tanar_teszt.py: a `if tipus in ("csoport", "szotag", ...` sor.

MIT CSINÁLJ ELEMENKÉNT (a tipus neve = a section id)
1. chat.html: `DM.<tipus> = function (f, D) { ... };` a "2. csomag" blokk UTÁN, a `function feladatElem(f) {` sor ELÉ, egy új "// ── 3. csomag (6. minta) ──" megjegyzés alá. ES5 (var, function), 4 szóköz behúzás.
   - A rajz és a működés a mintaoldalé legyen (Sándor jóváhagyta), de: NINCS „Új feladat” gomb, egy feladat = egy elem; a lényeges adatot a tanár adja (f.*), véletlen csak a nem lényeges dolgokhoz.
   - id-k helyett data-id + D.$('…'); minden látható szöveg D.T('magyar', 'español'), természetes spanyolországi spanyollal. Spanyol tantervnél (D.es) a tartalom is spanyol.
   - Befejezés: D.ellenoriz(fn) – a Kész gomb; fn {hianyzik, jo, uzenet, valasz}-t ad vissza –, vagy önmagától eldőlő feladatnál D.vege(jo, uzenet, valasz); a második rossz próbálkozás után a válasz mindenképp elmegy (nézd meg DM.tortcmp-ben). A `valasz` egyes szám első személyű mondat a gyerek nevében (ez megy a tanárnak), az `uzenet` rövid magyarázat a gyereknek.
   - Hang: SOHA ne speechSynthesis. Ha kimondás kell, csak D.mond(szöveg). A hangrendszerhez nyúlni TILOS.
   - Ha több SVG-ben ugyanaz a gradiens/szűrő id lenne, tedd egyedivé.
   - Gyereknek (6–12 év) érthető legyen; nincs tagadó vagy dupla tagadó kérdés; a feliratok nem lóghatnak egymásra; 320 px széles telefonon se lógjon ki semmi.
2. CSS: csak ami hiányzik, minden szelektor ".dm " előtaggal, a ".dm .dm-kesz-sor" sor UTÁN. Globális szabály (body, button stb. előtag nélkül) TILOS.
3. app.py: `if tipus == "<tipus>":` blokk az `if tipus == "akcio":` blokk UTÁN, az `if tipus == "modell":` ELŐTT. Ellenőrizd, hogy a feladat megoldható és egyértelmű; gyanús → return None. A kérdés: _rov(adat.get("kerdes"), 120) vagy jó magyar/spanyol alapértelmezés (es_tanterv szerint); figyelj a ragozásra (ne „a(z)”, ne „5-os”).
4. app.py: új tuple a _DM_FELULETEK lista VÉGÉRE, a meglévők mintájára. Címkék: "matek", "kornyezet", "magyar", "enek", "nyelv", "digit". Ha az elem történelem (korszak), vegyél fel egy "tortenelem" címkét: a _dm_cimkek függvényben `if any(k in s for k in ("tortenelem", "historia")): c.add("tortenelem")`.
5. tanar_teszt.py: az új típusneveket add hozzá a `if tipus in ("csoport", "szotag", ...` felsoroláshoz.

SZIGORÚ SZABÁLYOK
- Meglévő elemekhez, a dmKornyezet-hez, a hang-rendszerhez és a static/kartyak mappához NE nyúlj. Ne formázd át a meglévő kódot. A fájlok CRLF sorvégűek, így is maradjanak.
- Ne találj ki új D-függvényt a közös részbe; ha valami kell, az elemen belül írd meg.

ELLENŐRZÉS (kötelező, írd ki az eredményt – ha valamelyik nem sikerül, mondd meg őszintén)
- python -m py_compile app.py tanar_teszt.py → hibátlan.
- Keresd vissza és írd ki a sorszámmal: minden "DM.<tipus> = function" a chat.html-ben, minden `if tipus == "<tipus>":` az app.py-ban, minden ("<tipus>", tuple a _DM_FELULETEK-ben.
- Írj egy ideiglenes Python-szkriptet (NE a projektbe), amely `import app` után minden új típusra meghívja: app._feladat_parse_belso('<FELADAT>{...}</FELADAT>', grade=4, es_tanterv=False/True, temakor='x') – egy jó magyar, egy jó spanyol és egy hibás bemenettel. Írd ki a kimenetet: a jónál dict, a hibásnál None kell.
- Nézd át a chat.html-t: a <script> blokkban nincs szintaktikai hiba (pl. `node -e` -vel a blokk kiszedése és new Function-nel ellenőrzése).
```

---

## 4. PROMPT – kresz, binaris, magnes, ph

```
ELEMEK: kresz, binaris, magnes, ph
MINTAOLDAL: "Claude outputs/interaktiv_minta6.html"
KÜLÖN MEGJEGYZÉS: A "binaris" digitális kultúra: vegyél fel "digit" címkét, ha még nincs (a _dm_cimkek függvényben: "digit", "informatik", "tecnolog" szavakra). A spanyol oldalon a spanyol közlekedési táblák legyenek.

Feladat: a MINTAOLDAL sorban megadott mintaoldal fenti elemeit (a <section id="..."> azonosítók) beépíteni a TutorIA chat-táblájára, magyarul és spanyolul. Ugyanúgy, ahogy az előző 40 elem be van építve – azokat kövesd PONTOSAN mintának.

HOL VAN A MINTA
- templates/chat.html: a "var DM = {};" sornál kezdődik a futtató rész (dmKornyezet: a D objektum – D.T, D.$, D.html, D.el, D.txt, D.ellenoriz, D.vege, D.kuld, D.kartyaHuzas, D.huzosLista, D.billentyuzet, D.mond …). Utána jönnek a kész elemek: DM.csoport, DM.tortcmp, DM.kerekit, DM.romai, DM.naptar, DM.szervek, DM.venn stb. A "// ── 2. csomag (5–6. minta) ──" megjegyzés után a legújabbak.
- templates/chat.html CSS: a ".dm .dm-kesz-sor{margin-top:12px}" sor környékén vannak a .dm-es szabályok.
- app.py: a _feladat_parse_belso függvényben az `if tipus == "csoport":` … `if tipus == "akcio":` blokkok (az `if tipus == "modell":` ELŐTT) – ezek ellenőrzik szerveroldalon a tanár által küldött adatot.
- app.py: _DM_FELULETEK lista (tuple-ok: tipus, címkék, évfolyam-tól, -ig, magyar leírás + <FELADAT> példa, spanyol leírás + példa, magyar választó-sor, spanyol választó-sor) és a _dm_cimkek függvény.
- tanar_teszt.py: a `if tipus in ("csoport", "szotag", ...` sor.

MIT CSINÁLJ ELEMENKÉNT (a tipus neve = a section id)
1. chat.html: `DM.<tipus> = function (f, D) { ... };` a "2. csomag" blokk UTÁN, a `function feladatElem(f) {` sor ELÉ, egy új "// ── 3. csomag (6. minta) ──" megjegyzés alá. ES5 (var, function), 4 szóköz behúzás.
   - A rajz és a működés a mintaoldalé legyen (Sándor jóváhagyta), de: NINCS „Új feladat” gomb, egy feladat = egy elem; a lényeges adatot a tanár adja (f.*), véletlen csak a nem lényeges dolgokhoz.
   - id-k helyett data-id + D.$('…'); minden látható szöveg D.T('magyar', 'español'), természetes spanyolországi spanyollal. Spanyol tantervnél (D.es) a tartalom is spanyol.
   - Befejezés: D.ellenoriz(fn) – a Kész gomb; fn {hianyzik, jo, uzenet, valasz}-t ad vissza –, vagy önmagától eldőlő feladatnál D.vege(jo, uzenet, valasz); a második rossz próbálkozás után a válasz mindenképp elmegy (nézd meg DM.tortcmp-ben). A `valasz` egyes szám első személyű mondat a gyerek nevében (ez megy a tanárnak), az `uzenet` rövid magyarázat a gyereknek.
   - Hang: SOHA ne speechSynthesis. Ha kimondás kell, csak D.mond(szöveg). A hangrendszerhez nyúlni TILOS.
   - Ha több SVG-ben ugyanaz a gradiens/szűrő id lenne, tedd egyedivé.
   - Gyereknek (6–12 év) érthető legyen; nincs tagadó vagy dupla tagadó kérdés; a feliratok nem lóghatnak egymásra; 320 px széles telefonon se lógjon ki semmi.
2. CSS: csak ami hiányzik, minden szelektor ".dm " előtaggal, a ".dm .dm-kesz-sor" sor UTÁN. Globális szabály (body, button stb. előtag nélkül) TILOS.
3. app.py: `if tipus == "<tipus>":` blokk az `if tipus == "akcio":` blokk UTÁN, az `if tipus == "modell":` ELŐTT. Ellenőrizd, hogy a feladat megoldható és egyértelmű; gyanús → return None. A kérdés: _rov(adat.get("kerdes"), 120) vagy jó magyar/spanyol alapértelmezés (es_tanterv szerint); figyelj a ragozásra (ne „a(z)”, ne „5-os”).
4. app.py: új tuple a _DM_FELULETEK lista VÉGÉRE, a meglévők mintájára. Címkék: "matek", "kornyezet", "magyar", "enek", "nyelv", "digit". Ha az elem történelem (korszak), vegyél fel egy "tortenelem" címkét: a _dm_cimkek függvényben `if any(k in s for k in ("tortenelem", "historia")): c.add("tortenelem")`.
5. tanar_teszt.py: az új típusneveket add hozzá a `if tipus in ("csoport", "szotag", ...` felsoroláshoz.

SZIGORÚ SZABÁLYOK
- Meglévő elemekhez, a dmKornyezet-hez, a hang-rendszerhez és a static/kartyak mappához NE nyúlj. Ne formázd át a meglévő kódot. A fájlok CRLF sorvégűek, így is maradjanak.
- Ne találj ki új D-függvényt a közös részbe; ha valami kell, az elemen belül írd meg.

ELLENŐRZÉS (kötelező, írd ki az eredményt – ha valamelyik nem sikerül, mondd meg őszintén)
- python -m py_compile app.py tanar_teszt.py → hibátlan.
- Keresd vissza és írd ki a sorszámmal: minden "DM.<tipus> = function" a chat.html-ben, minden `if tipus == "<tipus>":` az app.py-ban, minden ("<tipus>", tuple a _DM_FELULETEK-ben.
- Írj egy ideiglenes Python-szkriptet (NE a projektbe), amely `import app` után minden új típusra meghívja: app._feladat_parse_belso('<FELADAT>{...}</FELADAT>', grade=4, es_tanterv=False/True, temakor='x') – egy jó magyar, egy jó spanyol és egy hibás bemenettel. Írd ki a kimenetet: a jónál dict, a hibásnál None kell.
- Nézd át a chat.html-t: a <script> blokkban nincs szintaktikai hiba (pl. `node -e` -vel a blokk kiszedése és new Function-nel ellenőrzése).
```

---

## 5. PROMPT – euro, csop, tortfal, tengely

```
ELEMEK: euro, csop, tortfal, tengely
MINTAOLDAL: "Claude outputs/interaktiv_minta7.html"
KÜLÖN MEGJEGYZÉS: Az "euro" lehet, hogy ugyanaz, mint a meglévő DM.penz (spanyol tantervnél euróval fizet), a "csop" pedig, mint a meglévő DM.csoport. Ha ugyanaz, NE építsd be, csak írd meg, miért hagytad ki.

Feladat: a MINTAOLDAL sorban megadott mintaoldal fenti elemeit (a <section id="..."> azonosítók) beépíteni a TutorIA chat-táblájára, magyarul és spanyolul. Ugyanúgy, ahogy az előző 40 elem be van építve – azokat kövesd PONTOSAN mintának.

HOL VAN A MINTA
- templates/chat.html: a "var DM = {};" sornál kezdődik a futtató rész (dmKornyezet: a D objektum – D.T, D.$, D.html, D.el, D.txt, D.ellenoriz, D.vege, D.kuld, D.kartyaHuzas, D.huzosLista, D.billentyuzet, D.mond …). Utána jönnek a kész elemek: DM.csoport, DM.tortcmp, DM.kerekit, DM.romai, DM.naptar, DM.szervek, DM.venn stb. A "// ── 2. csomag (5–6. minta) ──" megjegyzés után a legújabbak.
- templates/chat.html CSS: a ".dm .dm-kesz-sor{margin-top:12px}" sor környékén vannak a .dm-es szabályok.
- app.py: a _feladat_parse_belso függvényben az `if tipus == "csoport":` … `if tipus == "akcio":` blokkok (az `if tipus == "modell":` ELŐTT) – ezek ellenőrzik szerveroldalon a tanár által küldött adatot.
- app.py: _DM_FELULETEK lista (tuple-ok: tipus, címkék, évfolyam-tól, -ig, magyar leírás + <FELADAT> példa, spanyol leírás + példa, magyar választó-sor, spanyol választó-sor) és a _dm_cimkek függvény.
- tanar_teszt.py: a `if tipus in ("csoport", "szotag", ...` sor.

MIT CSINÁLJ ELEMENKÉNT (a tipus neve = a section id)
1. chat.html: `DM.<tipus> = function (f, D) { ... };` a "2. csomag" blokk UTÁN, a `function feladatElem(f) {` sor ELÉ, egy új "// ── 3. csomag (6. minta) ──" megjegyzés alá. ES5 (var, function), 4 szóköz behúzás.
   - A rajz és a működés a mintaoldalé legyen (Sándor jóváhagyta), de: NINCS „Új feladat” gomb, egy feladat = egy elem; a lényeges adatot a tanár adja (f.*), véletlen csak a nem lényeges dolgokhoz.
   - id-k helyett data-id + D.$('…'); minden látható szöveg D.T('magyar', 'español'), természetes spanyolországi spanyollal. Spanyol tantervnél (D.es) a tartalom is spanyol.
   - Befejezés: D.ellenoriz(fn) – a Kész gomb; fn {hianyzik, jo, uzenet, valasz}-t ad vissza –, vagy önmagától eldőlő feladatnál D.vege(jo, uzenet, valasz); a második rossz próbálkozás után a válasz mindenképp elmegy (nézd meg DM.tortcmp-ben). A `valasz` egyes szám első személyű mondat a gyerek nevében (ez megy a tanárnak), az `uzenet` rövid magyarázat a gyereknek.
   - Hang: SOHA ne speechSynthesis. Ha kimondás kell, csak D.mond(szöveg). A hangrendszerhez nyúlni TILOS.
   - Ha több SVG-ben ugyanaz a gradiens/szűrő id lenne, tedd egyedivé.
   - Gyereknek (6–12 év) érthető legyen; nincs tagadó vagy dupla tagadó kérdés; a feliratok nem lóghatnak egymásra; 320 px széles telefonon se lógjon ki semmi.
2. CSS: csak ami hiányzik, minden szelektor ".dm " előtaggal, a ".dm .dm-kesz-sor" sor UTÁN. Globális szabály (body, button stb. előtag nélkül) TILOS.
3. app.py: `if tipus == "<tipus>":` blokk az `if tipus == "akcio":` blokk UTÁN, az `if tipus == "modell":` ELŐTT. Ellenőrizd, hogy a feladat megoldható és egyértelmű; gyanús → return None. A kérdés: _rov(adat.get("kerdes"), 120) vagy jó magyar/spanyol alapértelmezés (es_tanterv szerint); figyelj a ragozásra (ne „a(z)”, ne „5-os”).
4. app.py: új tuple a _DM_FELULETEK lista VÉGÉRE, a meglévők mintájára. Címkék: "matek", "kornyezet", "magyar", "enek", "nyelv", "digit". Ha az elem történelem (korszak), vegyél fel egy "tortenelem" címkét: a _dm_cimkek függvényben `if any(k in s for k in ("tortenelem", "historia")): c.add("tortenelem")`.
5. tanar_teszt.py: az új típusneveket add hozzá a `if tipus in ("csoport", "szotag", ...` felsoroláshoz.

SZIGORÚ SZABÁLYOK
- Meglévő elemekhez, a dmKornyezet-hez, a hang-rendszerhez és a static/kartyak mappához NE nyúlj. Ne formázd át a meglévő kódot. A fájlok CRLF sorvégűek, így is maradjanak.
- Ne találj ki új D-függvényt a közös részbe; ha valami kell, az elemen belül írd meg.

ELLENŐRZÉS (kötelező, írd ki az eredményt – ha valamelyik nem sikerül, mondd meg őszintén)
- python -m py_compile app.py tanar_teszt.py → hibátlan.
- Keresd vissza és írd ki a sorszámmal: minden "DM.<tipus> = function" a chat.html-ben, minden `if tipus == "<tipus>":` az app.py-ban, minden ("<tipus>", tuple a _DM_FELULETEK-ben.
- Írj egy ideiglenes Python-szkriptet (NE a projektbe), amely `import app` után minden új típusra meghívja: app._feladat_parse_belso('<FELADAT>{...}</FELADAT>', grade=4, es_tanterv=False/True, temakor='x') – egy jó magyar, egy jó spanyol és egy hibás bemenettel. Írd ki a kimenetet: a jónál dict, a hibásnál None kell.
- Nézd át a chat.html-t: a <script> blokkban nincs szintaktikai hiba (pl. `node -e` -vel a blokk kiszedése és new Function-nel ellenőrzése).
```

---

## 6. PROMPT – halo, atlag, zsak, rim

```
ELEMEK: halo, atlag, zsak, rim
MINTAOLDAL: "Claude outputs/interaktiv_minta7.html"
KÜLÖN MEGJEGYZÉS: A "rim" (rímek): spanyolul spanyol rímpárok kellenek.

Feladat: a MINTAOLDAL sorban megadott mintaoldal fenti elemeit (a <section id="..."> azonosítók) beépíteni a TutorIA chat-táblájára, magyarul és spanyolul. Ugyanúgy, ahogy az előző 40 elem be van építve – azokat kövesd PONTOSAN mintának.

HOL VAN A MINTA
- templates/chat.html: a "var DM = {};" sornál kezdődik a futtató rész (dmKornyezet: a D objektum – D.T, D.$, D.html, D.el, D.txt, D.ellenoriz, D.vege, D.kuld, D.kartyaHuzas, D.huzosLista, D.billentyuzet, D.mond …). Utána jönnek a kész elemek: DM.csoport, DM.tortcmp, DM.kerekit, DM.romai, DM.naptar, DM.szervek, DM.venn stb. A "// ── 2. csomag (5–6. minta) ──" megjegyzés után a legújabbak.
- templates/chat.html CSS: a ".dm .dm-kesz-sor{margin-top:12px}" sor környékén vannak a .dm-es szabályok.
- app.py: a _feladat_parse_belso függvényben az `if tipus == "csoport":` … `if tipus == "akcio":` blokkok (az `if tipus == "modell":` ELŐTT) – ezek ellenőrzik szerveroldalon a tanár által küldött adatot.
- app.py: _DM_FELULETEK lista (tuple-ok: tipus, címkék, évfolyam-tól, -ig, magyar leírás + <FELADAT> példa, spanyol leírás + példa, magyar választó-sor, spanyol választó-sor) és a _dm_cimkek függvény.
- tanar_teszt.py: a `if tipus in ("csoport", "szotag", ...` sor.

MIT CSINÁLJ ELEMENKÉNT (a tipus neve = a section id)
1. chat.html: `DM.<tipus> = function (f, D) { ... };` a "2. csomag" blokk UTÁN, a `function feladatElem(f) {` sor ELÉ, egy új "// ── 3. csomag (6. minta) ──" megjegyzés alá. ES5 (var, function), 4 szóköz behúzás.
   - A rajz és a működés a mintaoldalé legyen (Sándor jóváhagyta), de: NINCS „Új feladat” gomb, egy feladat = egy elem; a lényeges adatot a tanár adja (f.*), véletlen csak a nem lényeges dolgokhoz.
   - id-k helyett data-id + D.$('…'); minden látható szöveg D.T('magyar', 'español'), természetes spanyolországi spanyollal. Spanyol tantervnél (D.es) a tartalom is spanyol.
   - Befejezés: D.ellenoriz(fn) – a Kész gomb; fn {hianyzik, jo, uzenet, valasz}-t ad vissza –, vagy önmagától eldőlő feladatnál D.vege(jo, uzenet, valasz); a második rossz próbálkozás után a válasz mindenképp elmegy (nézd meg DM.tortcmp-ben). A `valasz` egyes szám első személyű mondat a gyerek nevében (ez megy a tanárnak), az `uzenet` rövid magyarázat a gyereknek.
   - Hang: SOHA ne speechSynthesis. Ha kimondás kell, csak D.mond(szöveg). A hangrendszerhez nyúlni TILOS.
   - Ha több SVG-ben ugyanaz a gradiens/szűrő id lenne, tedd egyedivé.
   - Gyereknek (6–12 év) érthető legyen; nincs tagadó vagy dupla tagadó kérdés; a feliratok nem lóghatnak egymásra; 320 px széles telefonon se lógjon ki semmi.
2. CSS: csak ami hiányzik, minden szelektor ".dm " előtaggal, a ".dm .dm-kesz-sor" sor UTÁN. Globális szabály (body, button stb. előtag nélkül) TILOS.
3. app.py: `if tipus == "<tipus>":` blokk az `if tipus == "akcio":` blokk UTÁN, az `if tipus == "modell":` ELŐTT. Ellenőrizd, hogy a feladat megoldható és egyértelmű; gyanús → return None. A kérdés: _rov(adat.get("kerdes"), 120) vagy jó magyar/spanyol alapértelmezés (es_tanterv szerint); figyelj a ragozásra (ne „a(z)”, ne „5-os”).
4. app.py: új tuple a _DM_FELULETEK lista VÉGÉRE, a meglévők mintájára. Címkék: "matek", "kornyezet", "magyar", "enek", "nyelv", "digit". Ha az elem történelem (korszak), vegyél fel egy "tortenelem" címkét: a _dm_cimkek függvényben `if any(k in s for k in ("tortenelem", "historia")): c.add("tortenelem")`.
5. tanar_teszt.py: az új típusneveket add hozzá a `if tipus in ("csoport", "szotag", ...` felsoroláshoz.

SZIGORÚ SZABÁLYOK
- Meglévő elemekhez, a dmKornyezet-hez, a hang-rendszerhez és a static/kartyak mappához NE nyúlj. Ne formázd át a meglévő kódot. A fájlok CRLF sorvégűek, így is maradjanak.
- Ne találj ki új D-függvényt a közös részbe; ha valami kell, az elemen belül írd meg.

ELLENŐRZÉS (kötelező, írd ki az eredményt – ha valamelyik nem sikerül, mondd meg őszintén)
- python -m py_compile app.py tanar_teszt.py → hibátlan.
- Keresd vissza és írd ki a sorszámmal: minden "DM.<tipus> = function" a chat.html-ben, minden `if tipus == "<tipus>":` az app.py-ban, minden ("<tipus>", tuple a _DM_FELULETEK-ben.
- Írj egy ideiglenes Python-szkriptet (NE a projektbe), amely `import app` után minden új típusra meghívja: app._feladat_parse_belso('<FELADAT>{...}</FELADAT>', grade=4, es_tanterv=False/True, temakor='x') – egy jó magyar, egy jó spanyol és egy hibás bemenettel. Írd ki a kimenetet: a jónál dict, a hibásnál None kell.
- Nézd át a chat.html-t: a <script> blokkban nincs szintaktikai hiba (pl. `node -e` -vel a blokk kiszedése és new Function-nel ellenőrzése).
```

---

## 7. PROMPT – toldalek, kepsor, szamangol, idojaras

```
ELEMEK: toldalek, kepsor, szamangol, idojaras
MINTAOLDAL: "Claude outputs/interaktiv_minta7.html"
KÜLÖN MEGJEGYZÉS: A "szamangol" angol számok, kimondás csak D.mond-dal. A "toldalek" magyar nyelvtan: spanyolul a spanyol megfelelője (pl. végződések), vagy ha nincs értelmes, csak magyar tantervre ajánld.

Feladat: a MINTAOLDAL sorban megadott mintaoldal fenti elemeit (a <section id="..."> azonosítók) beépíteni a TutorIA chat-táblájára, magyarul és spanyolul. Ugyanúgy, ahogy az előző 40 elem be van építve – azokat kövesd PONTOSAN mintának.

HOL VAN A MINTA
- templates/chat.html: a "var DM = {};" sornál kezdődik a futtató rész (dmKornyezet: a D objektum – D.T, D.$, D.html, D.el, D.txt, D.ellenoriz, D.vege, D.kuld, D.kartyaHuzas, D.huzosLista, D.billentyuzet, D.mond …). Utána jönnek a kész elemek: DM.csoport, DM.tortcmp, DM.kerekit, DM.romai, DM.naptar, DM.szervek, DM.venn stb. A "// ── 2. csomag (5–6. minta) ──" megjegyzés után a legújabbak.
- templates/chat.html CSS: a ".dm .dm-kesz-sor{margin-top:12px}" sor környékén vannak a .dm-es szabályok.
- app.py: a _feladat_parse_belso függvényben az `if tipus == "csoport":` … `if tipus == "akcio":` blokkok (az `if tipus == "modell":` ELŐTT) – ezek ellenőrzik szerveroldalon a tanár által küldött adatot.
- app.py: _DM_FELULETEK lista (tuple-ok: tipus, címkék, évfolyam-tól, -ig, magyar leírás + <FELADAT> példa, spanyol leírás + példa, magyar választó-sor, spanyol választó-sor) és a _dm_cimkek függvény.
- tanar_teszt.py: a `if tipus in ("csoport", "szotag", ...` sor.

MIT CSINÁLJ ELEMENKÉNT (a tipus neve = a section id)
1. chat.html: `DM.<tipus> = function (f, D) { ... };` a "2. csomag" blokk UTÁN, a `function feladatElem(f) {` sor ELÉ, egy új "// ── 3. csomag (6. minta) ──" megjegyzés alá. ES5 (var, function), 4 szóköz behúzás.
   - A rajz és a működés a mintaoldalé legyen (Sándor jóváhagyta), de: NINCS „Új feladat” gomb, egy feladat = egy elem; a lényeges adatot a tanár adja (f.*), véletlen csak a nem lényeges dolgokhoz.
   - id-k helyett data-id + D.$('…'); minden látható szöveg D.T('magyar', 'español'), természetes spanyolországi spanyollal. Spanyol tantervnél (D.es) a tartalom is spanyol.
   - Befejezés: D.ellenoriz(fn) – a Kész gomb; fn {hianyzik, jo, uzenet, valasz}-t ad vissza –, vagy önmagától eldőlő feladatnál D.vege(jo, uzenet, valasz); a második rossz próbálkozás után a válasz mindenképp elmegy (nézd meg DM.tortcmp-ben). A `valasz` egyes szám első személyű mondat a gyerek nevében (ez megy a tanárnak), az `uzenet` rövid magyarázat a gyereknek.
   - Hang: SOHA ne speechSynthesis. Ha kimondás kell, csak D.mond(szöveg). A hangrendszerhez nyúlni TILOS.
   - Ha több SVG-ben ugyanaz a gradiens/szűrő id lenne, tedd egyedivé.
   - Gyereknek (6–12 év) érthető legyen; nincs tagadó vagy dupla tagadó kérdés; a feliratok nem lóghatnak egymásra; 320 px széles telefonon se lógjon ki semmi.
2. CSS: csak ami hiányzik, minden szelektor ".dm " előtaggal, a ".dm .dm-kesz-sor" sor UTÁN. Globális szabály (body, button stb. előtag nélkül) TILOS.
3. app.py: `if tipus == "<tipus>":` blokk az `if tipus == "akcio":` blokk UTÁN, az `if tipus == "modell":` ELŐTT. Ellenőrizd, hogy a feladat megoldható és egyértelmű; gyanús → return None. A kérdés: _rov(adat.get("kerdes"), 120) vagy jó magyar/spanyol alapértelmezés (es_tanterv szerint); figyelj a ragozásra (ne „a(z)”, ne „5-os”).
4. app.py: új tuple a _DM_FELULETEK lista VÉGÉRE, a meglévők mintájára. Címkék: "matek", "kornyezet", "magyar", "enek", "nyelv", "digit". Ha az elem történelem (korszak), vegyél fel egy "tortenelem" címkét: a _dm_cimkek függvényben `if any(k in s for k in ("tortenelem", "historia")): c.add("tortenelem")`.
5. tanar_teszt.py: az új típusneveket add hozzá a `if tipus in ("csoport", "szotag", ...` felsoroláshoz.

SZIGORÚ SZABÁLYOK
- Meglévő elemekhez, a dmKornyezet-hez, a hang-rendszerhez és a static/kartyak mappához NE nyúlj. Ne formázd át a meglévő kódot. A fájlok CRLF sorvégűek, így is maradjanak.
- Ne találj ki új D-függvényt a közös részbe; ha valami kell, az elemen belül írd meg.

ELLENŐRZÉS (kötelező, írd ki az eredményt – ha valamelyik nem sikerül, mondd meg őszintén)
- python -m py_compile app.py tanar_teszt.py → hibátlan.
- Keresd vissza és írd ki a sorszámmal: minden "DM.<tipus> = function" a chat.html-ben, minden `if tipus == "<tipus>":` az app.py-ban, minden ("<tipus>", tuple a _DM_FELULETEK-ben.
- Írj egy ideiglenes Python-szkriptet (NE a projektbe), amely `import app` után minden új típusra meghívja: app._feladat_parse_belso('<FELADAT>{...}</FELADAT>', grade=4, es_tanterv=False/True, temakor='x') – egy jó magyar, egy jó spanyol és egy hibás bemenettel. Írd ki a kimenetet: a jónál dict, a hibásnál None kell.
- Nézd át a chat.html-t: a <script> blokkban nincs szintaktikai hiba (pl. `node -e` -vel a blokk kiszedése és new Function-nel ellenőrzése).
```

---

## 8. PROMPT – evszak, elohely, tanyer, bolygo

```
ELEMEK: evszak, elohely, tanyer, bolygo
MINTAOLDAL: "Claude outputs/interaktiv_minta7.html"

Feladat: a MINTAOLDAL sorban megadott mintaoldal fenti elemeit (a <section id="..."> azonosítók) beépíteni a TutorIA chat-táblájára, magyarul és spanyolul. Ugyanúgy, ahogy az előző 40 elem be van építve – azokat kövesd PONTOSAN mintának.

HOL VAN A MINTA
- templates/chat.html: a "var DM = {};" sornál kezdődik a futtató rész (dmKornyezet: a D objektum – D.T, D.$, D.html, D.el, D.txt, D.ellenoriz, D.vege, D.kuld, D.kartyaHuzas, D.huzosLista, D.billentyuzet, D.mond …). Utána jönnek a kész elemek: DM.csoport, DM.tortcmp, DM.kerekit, DM.romai, DM.naptar, DM.szervek, DM.venn stb. A "// ── 2. csomag (5–6. minta) ──" megjegyzés után a legújabbak.
- templates/chat.html CSS: a ".dm .dm-kesz-sor{margin-top:12px}" sor környékén vannak a .dm-es szabályok.
- app.py: a _feladat_parse_belso függvényben az `if tipus == "csoport":` … `if tipus == "akcio":` blokkok (az `if tipus == "modell":` ELŐTT) – ezek ellenőrzik szerveroldalon a tanár által küldött adatot.
- app.py: _DM_FELULETEK lista (tuple-ok: tipus, címkék, évfolyam-tól, -ig, magyar leírás + <FELADAT> példa, spanyol leírás + példa, magyar választó-sor, spanyol választó-sor) és a _dm_cimkek függvény.
- tanar_teszt.py: a `if tipus in ("csoport", "szotag", ...` sor.

MIT CSINÁLJ ELEMENKÉNT (a tipus neve = a section id)
1. chat.html: `DM.<tipus> = function (f, D) { ... };` a "2. csomag" blokk UTÁN, a `function feladatElem(f) {` sor ELÉ, egy új "// ── 3. csomag (6. minta) ──" megjegyzés alá. ES5 (var, function), 4 szóköz behúzás.
   - A rajz és a működés a mintaoldalé legyen (Sándor jóváhagyta), de: NINCS „Új feladat” gomb, egy feladat = egy elem; a lényeges adatot a tanár adja (f.*), véletlen csak a nem lényeges dolgokhoz.
   - id-k helyett data-id + D.$('…'); minden látható szöveg D.T('magyar', 'español'), természetes spanyolországi spanyollal. Spanyol tantervnél (D.es) a tartalom is spanyol.
   - Befejezés: D.ellenoriz(fn) – a Kész gomb; fn {hianyzik, jo, uzenet, valasz}-t ad vissza –, vagy önmagától eldőlő feladatnál D.vege(jo, uzenet, valasz); a második rossz próbálkozás után a válasz mindenképp elmegy (nézd meg DM.tortcmp-ben). A `valasz` egyes szám első személyű mondat a gyerek nevében (ez megy a tanárnak), az `uzenet` rövid magyarázat a gyereknek.
   - Hang: SOHA ne speechSynthesis. Ha kimondás kell, csak D.mond(szöveg). A hangrendszerhez nyúlni TILOS.
   - Ha több SVG-ben ugyanaz a gradiens/szűrő id lenne, tedd egyedivé.
   - Gyereknek (6–12 év) érthető legyen; nincs tagadó vagy dupla tagadó kérdés; a feliratok nem lóghatnak egymásra; 320 px széles telefonon se lógjon ki semmi.
2. CSS: csak ami hiányzik, minden szelektor ".dm " előtaggal, a ".dm .dm-kesz-sor" sor UTÁN. Globális szabály (body, button stb. előtag nélkül) TILOS.
3. app.py: `if tipus == "<tipus>":` blokk az `if tipus == "akcio":` blokk UTÁN, az `if tipus == "modell":` ELŐTT. Ellenőrizd, hogy a feladat megoldható és egyértelmű; gyanús → return None. A kérdés: _rov(adat.get("kerdes"), 120) vagy jó magyar/spanyol alapértelmezés (es_tanterv szerint); figyelj a ragozásra (ne „a(z)”, ne „5-os”).
4. app.py: új tuple a _DM_FELULETEK lista VÉGÉRE, a meglévők mintájára. Címkék: "matek", "kornyezet", "magyar", "enek", "nyelv", "digit". Ha az elem történelem (korszak), vegyél fel egy "tortenelem" címkét: a _dm_cimkek függvényben `if any(k in s for k in ("tortenelem", "historia")): c.add("tortenelem")`.
5. tanar_teszt.py: az új típusneveket add hozzá a `if tipus in ("csoport", "szotag", ...` felsoroláshoz.

SZIGORÚ SZABÁLYOK
- Meglévő elemekhez, a dmKornyezet-hez, a hang-rendszerhez és a static/kartyak mappához NE nyúlj. Ne formázd át a meglévő kódot. A fájlok CRLF sorvégűek, így is maradjanak.
- Ne találj ki új D-függvényt a közös részbe; ha valami kell, az elemen belül írd meg.

ELLENŐRZÉS (kötelező, írd ki az eredményt – ha valamelyik nem sikerül, mondd meg őszintén)
- python -m py_compile app.py tanar_teszt.py → hibátlan.
- Keresd vissza és írd ki a sorszámmal: minden "DM.<tipus> = function" a chat.html-ben, minden `if tipus == "<tipus>":` az app.py-ban, minden ("<tipus>", tuple a _DM_FELULETEK-ben.
- Írj egy ideiglenes Python-szkriptet (NE a projektbe), amely `import app` után minden új típusra meghívja: app._feladat_parse_belso('<FELADAT>{...}</FELADAT>', grade=4, es_tanterv=False/True, temakor='x') – egy jó magyar, egy jó spanyol és egy hibás bemenettel. Írd ki a kimenetet: a jónál dict, a hibásnál None kell.
- Nézd át a chat.html-t: a <script> blokkban nincs szintaktikai hiba (pl. `node -e` -vel a blokk kiszedése és new Function-nel ellenőrzése).
```

---

## 9. PROMPT – vezeto, poharak, domb

```
ELEMEK: vezeto, poharak, domb
MINTAOLDAL: "Claude outputs/interaktiv_minta7.html"
KÜLÖN MEGJEGYZÉS: A "domb" (domborzati térkép) a mintaoldal canvas-os, valósághű változata – azt vidd át hűen, ne egyszerűsítsd.

Feladat: a MINTAOLDAL sorban megadott mintaoldal fenti elemeit (a <section id="..."> azonosítók) beépíteni a TutorIA chat-táblájára, magyarul és spanyolul. Ugyanúgy, ahogy az előző 40 elem be van építve – azokat kövesd PONTOSAN mintának.

HOL VAN A MINTA
- templates/chat.html: a "var DM = {};" sornál kezdődik a futtató rész (dmKornyezet: a D objektum – D.T, D.$, D.html, D.el, D.txt, D.ellenoriz, D.vege, D.kuld, D.kartyaHuzas, D.huzosLista, D.billentyuzet, D.mond …). Utána jönnek a kész elemek: DM.csoport, DM.tortcmp, DM.kerekit, DM.romai, DM.naptar, DM.szervek, DM.venn stb. A "// ── 2. csomag (5–6. minta) ──" megjegyzés után a legújabbak.
- templates/chat.html CSS: a ".dm .dm-kesz-sor{margin-top:12px}" sor környékén vannak a .dm-es szabályok.
- app.py: a _feladat_parse_belso függvényben az `if tipus == "csoport":` … `if tipus == "akcio":` blokkok (az `if tipus == "modell":` ELŐTT) – ezek ellenőrzik szerveroldalon a tanár által küldött adatot.
- app.py: _DM_FELULETEK lista (tuple-ok: tipus, címkék, évfolyam-tól, -ig, magyar leírás + <FELADAT> példa, spanyol leírás + példa, magyar választó-sor, spanyol választó-sor) és a _dm_cimkek függvény.
- tanar_teszt.py: a `if tipus in ("csoport", "szotag", ...` sor.

MIT CSINÁLJ ELEMENKÉNT (a tipus neve = a section id)
1. chat.html: `DM.<tipus> = function (f, D) { ... };` a "2. csomag" blokk UTÁN, a `function feladatElem(f) {` sor ELÉ, egy új "// ── 3. csomag (6. minta) ──" megjegyzés alá. ES5 (var, function), 4 szóköz behúzás.
   - A rajz és a működés a mintaoldalé legyen (Sándor jóváhagyta), de: NINCS „Új feladat” gomb, egy feladat = egy elem; a lényeges adatot a tanár adja (f.*), véletlen csak a nem lényeges dolgokhoz.
   - id-k helyett data-id + D.$('…'); minden látható szöveg D.T('magyar', 'español'), természetes spanyolországi spanyollal. Spanyol tantervnél (D.es) a tartalom is spanyol.
   - Befejezés: D.ellenoriz(fn) – a Kész gomb; fn {hianyzik, jo, uzenet, valasz}-t ad vissza –, vagy önmagától eldőlő feladatnál D.vege(jo, uzenet, valasz); a második rossz próbálkozás után a válasz mindenképp elmegy (nézd meg DM.tortcmp-ben). A `valasz` egyes szám első személyű mondat a gyerek nevében (ez megy a tanárnak), az `uzenet` rövid magyarázat a gyereknek.
   - Hang: SOHA ne speechSynthesis. Ha kimondás kell, csak D.mond(szöveg). A hangrendszerhez nyúlni TILOS.
   - Ha több SVG-ben ugyanaz a gradiens/szűrő id lenne, tedd egyedivé.
   - Gyereknek (6–12 év) érthető legyen; nincs tagadó vagy dupla tagadó kérdés; a feliratok nem lóghatnak egymásra; 320 px széles telefonon se lógjon ki semmi.
2. CSS: csak ami hiányzik, minden szelektor ".dm " előtaggal, a ".dm .dm-kesz-sor" sor UTÁN. Globális szabály (body, button stb. előtag nélkül) TILOS.
3. app.py: `if tipus == "<tipus>":` blokk az `if tipus == "akcio":` blokk UTÁN, az `if tipus == "modell":` ELŐTT. Ellenőrizd, hogy a feladat megoldható és egyértelmű; gyanús → return None. A kérdés: _rov(adat.get("kerdes"), 120) vagy jó magyar/spanyol alapértelmezés (es_tanterv szerint); figyelj a ragozásra (ne „a(z)”, ne „5-os”).
4. app.py: új tuple a _DM_FELULETEK lista VÉGÉRE, a meglévők mintájára. Címkék: "matek", "kornyezet", "magyar", "enek", "nyelv", "digit". Ha az elem történelem (korszak), vegyél fel egy "tortenelem" címkét: a _dm_cimkek függvényben `if any(k in s for k in ("tortenelem", "historia")): c.add("tortenelem")`.
5. tanar_teszt.py: az új típusneveket add hozzá a `if tipus in ("csoport", "szotag", ...` felsoroláshoz.

SZIGORÚ SZABÁLYOK
- Meglévő elemekhez, a dmKornyezet-hez, a hang-rendszerhez és a static/kartyak mappához NE nyúlj. Ne formázd át a meglévő kódot. A fájlok CRLF sorvégűek, így is maradjanak.
- Ne találj ki új D-függvényt a közös részbe; ha valami kell, az elemen belül írd meg.

ELLENŐRZÉS (kötelező, írd ki az eredményt – ha valamelyik nem sikerül, mondd meg őszintén)
- python -m py_compile app.py tanar_teszt.py → hibátlan.
- Keresd vissza és írd ki a sorszámmal: minden "DM.<tipus> = function" a chat.html-ben, minden `if tipus == "<tipus>":` az app.py-ban, minden ("<tipus>", tuple a _DM_FELULETEK-ben.
- Írj egy ideiglenes Python-szkriptet (NE a projektbe), amely `import app` után minden új típusra meghívja: app._feladat_parse_belso('<FELADAT>{...}</FELADAT>', grade=4, es_tanterv=False/True, temakor='x') – egy jó magyar, egy jó spanyol és egy hibás bemenettel. Írd ki a kimenetet: a jónál dict, a hibásnál None kell.
- Nézd át a chat.html-t: a <script> blokkban nincs szintaktikai hiba (pl. `node -e` -vel a blokk kiszedése és new Function-nel ellenőrzése).
```

---

## 10. PROMPT – sorozat, zokni, becsles, allitas

```
ELEMEK: sorozat, zokni, becsles, allitas
MINTAOLDAL: "Claude outputs/interaktiv_minta8.html"
KÜLÖN MEGJEGYZÉS: A "sorozat" vonata jó válasz után ROSSZ IRÁNYBA indul a mintaoldalon (hátrafelé). Javítsd: a vonat a mozdony felé, BALRA menjen (a translate x értéke negatív legyen).

Feladat: a MINTAOLDAL sorban megadott mintaoldal fenti elemeit (a <section id="..."> azonosítók) beépíteni a TutorIA chat-táblájára, magyarul és spanyolul. Ugyanúgy, ahogy az előző 40 elem be van építve – azokat kövesd PONTOSAN mintának.

HOL VAN A MINTA
- templates/chat.html: a "var DM = {};" sornál kezdődik a futtató rész (dmKornyezet: a D objektum – D.T, D.$, D.html, D.el, D.txt, D.ellenoriz, D.vege, D.kuld, D.kartyaHuzas, D.huzosLista, D.billentyuzet, D.mond …). Utána jönnek a kész elemek: DM.csoport, DM.tortcmp, DM.kerekit, DM.romai, DM.naptar, DM.szervek, DM.venn stb. A "// ── 2. csomag (5–6. minta) ──" megjegyzés után a legújabbak.
- templates/chat.html CSS: a ".dm .dm-kesz-sor{margin-top:12px}" sor környékén vannak a .dm-es szabályok.
- app.py: a _feladat_parse_belso függvényben az `if tipus == "csoport":` … `if tipus == "akcio":` blokkok (az `if tipus == "modell":` ELŐTT) – ezek ellenőrzik szerveroldalon a tanár által küldött adatot.
- app.py: _DM_FELULETEK lista (tuple-ok: tipus, címkék, évfolyam-tól, -ig, magyar leírás + <FELADAT> példa, spanyol leírás + példa, magyar választó-sor, spanyol választó-sor) és a _dm_cimkek függvény.
- tanar_teszt.py: a `if tipus in ("csoport", "szotag", ...` sor.

MIT CSINÁLJ ELEMENKÉNT (a tipus neve = a section id)
1. chat.html: `DM.<tipus> = function (f, D) { ... };` a "2. csomag" blokk UTÁN, a `function feladatElem(f) {` sor ELÉ, egy új "// ── 3. csomag (6. minta) ──" megjegyzés alá. ES5 (var, function), 4 szóköz behúzás.
   - A rajz és a működés a mintaoldalé legyen (Sándor jóváhagyta), de: NINCS „Új feladat” gomb, egy feladat = egy elem; a lényeges adatot a tanár adja (f.*), véletlen csak a nem lényeges dolgokhoz.
   - id-k helyett data-id + D.$('…'); minden látható szöveg D.T('magyar', 'español'), természetes spanyolországi spanyollal. Spanyol tantervnél (D.es) a tartalom is spanyol.
   - Befejezés: D.ellenoriz(fn) – a Kész gomb; fn {hianyzik, jo, uzenet, valasz}-t ad vissza –, vagy önmagától eldőlő feladatnál D.vege(jo, uzenet, valasz); a második rossz próbálkozás után a válasz mindenképp elmegy (nézd meg DM.tortcmp-ben). A `valasz` egyes szám első személyű mondat a gyerek nevében (ez megy a tanárnak), az `uzenet` rövid magyarázat a gyereknek.
   - Hang: SOHA ne speechSynthesis. Ha kimondás kell, csak D.mond(szöveg). A hangrendszerhez nyúlni TILOS.
   - Ha több SVG-ben ugyanaz a gradiens/szűrő id lenne, tedd egyedivé.
   - Gyereknek (6–12 év) érthető legyen; nincs tagadó vagy dupla tagadó kérdés; a feliratok nem lóghatnak egymásra; 320 px széles telefonon se lógjon ki semmi.
2. CSS: csak ami hiányzik, minden szelektor ".dm " előtaggal, a ".dm .dm-kesz-sor" sor UTÁN. Globális szabály (body, button stb. előtag nélkül) TILOS.
3. app.py: `if tipus == "<tipus>":` blokk az `if tipus == "akcio":` blokk UTÁN, az `if tipus == "modell":` ELŐTT. Ellenőrizd, hogy a feladat megoldható és egyértelmű; gyanús → return None. A kérdés: _rov(adat.get("kerdes"), 120) vagy jó magyar/spanyol alapértelmezés (es_tanterv szerint); figyelj a ragozásra (ne „a(z)”, ne „5-os”).
4. app.py: új tuple a _DM_FELULETEK lista VÉGÉRE, a meglévők mintájára. Címkék: "matek", "kornyezet", "magyar", "enek", "nyelv", "digit". Ha az elem történelem (korszak), vegyél fel egy "tortenelem" címkét: a _dm_cimkek függvényben `if any(k in s for k in ("tortenelem", "historia")): c.add("tortenelem")`.
5. tanar_teszt.py: az új típusneveket add hozzá a `if tipus in ("csoport", "szotag", ...` felsoroláshoz.

SZIGORÚ SZABÁLYOK
- Meglévő elemekhez, a dmKornyezet-hez, a hang-rendszerhez és a static/kartyak mappához NE nyúlj. Ne formázd át a meglévő kódot. A fájlok CRLF sorvégűek, így is maradjanak.
- Ne találj ki új D-függvényt a közös részbe; ha valami kell, az elemen belül írd meg.

ELLENŐRZÉS (kötelező, írd ki az eredményt – ha valamelyik nem sikerül, mondd meg őszintén)
- python -m py_compile app.py tanar_teszt.py → hibátlan.
- Keresd vissza és írd ki a sorszámmal: minden "DM.<tipus> = function" a chat.html-ben, minden `if tipus == "<tipus>":` az app.py-ban, minden ("<tipus>", tuple a _DM_FELULETEK-ben.
- Írj egy ideiglenes Python-szkriptet (NE a projektbe), amely `import app` után minden új típusra meghívja: app._feladat_parse_belso('<FELADAT>{...}</FELADAT>', grade=4, es_tanterv=False/True, temakor='x') – egy jó magyar, egy jó spanyol és egy hibás bemenettel. Írd ki a kimenetet: a jónál dict, a hibásnál None kell.
- Nézd át a chat.html-t: a <script> blokkban nincs szintaktikai hiba (pl. `node -e` -vel a blokk kiszedése és new Function-nel ellenőrzése).
```

---

## 11. PROMPT – urmertek, nezet, betu, szofaj

```
ELEMEK: urmertek, nezet, betu, szofaj
MINTAOLDAL: "Claude outputs/interaktiv_minta8.html"
KÜLÖN MEGJEGYZÉS: A "nezet"-nél a „Nézd a kisfiú szemével” gombos változatot vidd át. A "betu" és "szofaj" magyar nyelvtan: spanyolul a spanyol nyelvtan megfelelőjével.

Feladat: a MINTAOLDAL sorban megadott mintaoldal fenti elemeit (a <section id="..."> azonosítók) beépíteni a TutorIA chat-táblájára, magyarul és spanyolul. Ugyanúgy, ahogy az előző 40 elem be van építve – azokat kövesd PONTOSAN mintának.

HOL VAN A MINTA
- templates/chat.html: a "var DM = {};" sornál kezdődik a futtató rész (dmKornyezet: a D objektum – D.T, D.$, D.html, D.el, D.txt, D.ellenoriz, D.vege, D.kuld, D.kartyaHuzas, D.huzosLista, D.billentyuzet, D.mond …). Utána jönnek a kész elemek: DM.csoport, DM.tortcmp, DM.kerekit, DM.romai, DM.naptar, DM.szervek, DM.venn stb. A "// ── 2. csomag (5–6. minta) ──" megjegyzés után a legújabbak.
- templates/chat.html CSS: a ".dm .dm-kesz-sor{margin-top:12px}" sor környékén vannak a .dm-es szabályok.
- app.py: a _feladat_parse_belso függvényben az `if tipus == "csoport":` … `if tipus == "akcio":` blokkok (az `if tipus == "modell":` ELŐTT) – ezek ellenőrzik szerveroldalon a tanár által küldött adatot.
- app.py: _DM_FELULETEK lista (tuple-ok: tipus, címkék, évfolyam-tól, -ig, magyar leírás + <FELADAT> példa, spanyol leírás + példa, magyar választó-sor, spanyol választó-sor) és a _dm_cimkek függvény.
- tanar_teszt.py: a `if tipus in ("csoport", "szotag", ...` sor.

MIT CSINÁLJ ELEMENKÉNT (a tipus neve = a section id)
1. chat.html: `DM.<tipus> = function (f, D) { ... };` a "2. csomag" blokk UTÁN, a `function feladatElem(f) {` sor ELÉ, egy új "// ── 3. csomag (6. minta) ──" megjegyzés alá. ES5 (var, function), 4 szóköz behúzás.
   - A rajz és a működés a mintaoldalé legyen (Sándor jóváhagyta), de: NINCS „Új feladat” gomb, egy feladat = egy elem; a lényeges adatot a tanár adja (f.*), véletlen csak a nem lényeges dolgokhoz.
   - id-k helyett data-id + D.$('…'); minden látható szöveg D.T('magyar', 'español'), természetes spanyolországi spanyollal. Spanyol tantervnél (D.es) a tartalom is spanyol.
   - Befejezés: D.ellenoriz(fn) – a Kész gomb; fn {hianyzik, jo, uzenet, valasz}-t ad vissza –, vagy önmagától eldőlő feladatnál D.vege(jo, uzenet, valasz); a második rossz próbálkozás után a válasz mindenképp elmegy (nézd meg DM.tortcmp-ben). A `valasz` egyes szám első személyű mondat a gyerek nevében (ez megy a tanárnak), az `uzenet` rövid magyarázat a gyereknek.
   - Hang: SOHA ne speechSynthesis. Ha kimondás kell, csak D.mond(szöveg). A hangrendszerhez nyúlni TILOS.
   - Ha több SVG-ben ugyanaz a gradiens/szűrő id lenne, tedd egyedivé.
   - Gyereknek (6–12 év) érthető legyen; nincs tagadó vagy dupla tagadó kérdés; a feliratok nem lóghatnak egymásra; 320 px széles telefonon se lógjon ki semmi.
2. CSS: csak ami hiányzik, minden szelektor ".dm " előtaggal, a ".dm .dm-kesz-sor" sor UTÁN. Globális szabály (body, button stb. előtag nélkül) TILOS.
3. app.py: `if tipus == "<tipus>":` blokk az `if tipus == "akcio":` blokk UTÁN, az `if tipus == "modell":` ELŐTT. Ellenőrizd, hogy a feladat megoldható és egyértelmű; gyanús → return None. A kérdés: _rov(adat.get("kerdes"), 120) vagy jó magyar/spanyol alapértelmezés (es_tanterv szerint); figyelj a ragozásra (ne „a(z)”, ne „5-os”).
4. app.py: új tuple a _DM_FELULETEK lista VÉGÉRE, a meglévők mintájára. Címkék: "matek", "kornyezet", "magyar", "enek", "nyelv", "digit". Ha az elem történelem (korszak), vegyél fel egy "tortenelem" címkét: a _dm_cimkek függvényben `if any(k in s for k in ("tortenelem", "historia")): c.add("tortenelem")`.
5. tanar_teszt.py: az új típusneveket add hozzá a `if tipus in ("csoport", "szotag", ...` felsoroláshoz.

SZIGORÚ SZABÁLYOK
- Meglévő elemekhez, a dmKornyezet-hez, a hang-rendszerhez és a static/kartyak mappához NE nyúlj. Ne formázd át a meglévő kódot. A fájlok CRLF sorvégűek, így is maradjanak.
- Ne találj ki új D-függvényt a közös részbe; ha valami kell, az elemen belül írd meg.

ELLENŐRZÉS (kötelező, írd ki az eredményt – ha valamelyik nem sikerül, mondd meg őszintén)
- python -m py_compile app.py tanar_teszt.py → hibátlan.
- Keresd vissza és írd ki a sorszámmal: minden "DM.<tipus> = function" a chat.html-ben, minden `if tipus == "<tipus>":` az app.py-ban, minden ("<tipus>", tuple a _DM_FELULETEK-ben.
- Írj egy ideiglenes Python-szkriptet (NE a projektbe), amely `import app` után minden új típusra meghívja: app._feladat_parse_belso('<FELADAT>{...}</FELADAT>', grade=4, es_tanterv=False/True, temakor='x') – egy jó magyar, egy jó spanyol és egy hibás bemenettel. Írd ki a kimenetet: a jónál dict, a hibásnál None kell.
- Nézd át a chat.html-t: a <script> blokkban nincs szintaktikai hiba (pl. `node -e` -vel a blokk kiszedése és new Function-nel ellenőrzése).
```

---

## 12. PROMPT – nagybetu, tilde, nevelo, gerinces

```
ELEMEK: nagybetu, tilde, nevelo, gerinces
MINTAOLDAL: "Claude outputs/interaktiv_minta8.html"
KÜLÖN MEGJEGYZÉS: A "tilde" spanyol ékezetszabály: csak spanyol tantervhez illik, a magyar leírásban ezt jelezd. A "nevelo" névelők (a/az; angolul a/an; spanyolul el/la/los/las).

Feladat: a MINTAOLDAL sorban megadott mintaoldal fenti elemeit (a <section id="..."> azonosítók) beépíteni a TutorIA chat-táblájára, magyarul és spanyolul. Ugyanúgy, ahogy az előző 40 elem be van építve – azokat kövesd PONTOSAN mintának.

HOL VAN A MINTA
- templates/chat.html: a "var DM = {};" sornál kezdődik a futtató rész (dmKornyezet: a D objektum – D.T, D.$, D.html, D.el, D.txt, D.ellenoriz, D.vege, D.kuld, D.kartyaHuzas, D.huzosLista, D.billentyuzet, D.mond …). Utána jönnek a kész elemek: DM.csoport, DM.tortcmp, DM.kerekit, DM.romai, DM.naptar, DM.szervek, DM.venn stb. A "// ── 2. csomag (5–6. minta) ──" megjegyzés után a legújabbak.
- templates/chat.html CSS: a ".dm .dm-kesz-sor{margin-top:12px}" sor környékén vannak a .dm-es szabályok.
- app.py: a _feladat_parse_belso függvényben az `if tipus == "csoport":` … `if tipus == "akcio":` blokkok (az `if tipus == "modell":` ELŐTT) – ezek ellenőrzik szerveroldalon a tanár által küldött adatot.
- app.py: _DM_FELULETEK lista (tuple-ok: tipus, címkék, évfolyam-tól, -ig, magyar leírás + <FELADAT> példa, spanyol leírás + példa, magyar választó-sor, spanyol választó-sor) és a _dm_cimkek függvény.
- tanar_teszt.py: a `if tipus in ("csoport", "szotag", ...` sor.

MIT CSINÁLJ ELEMENKÉNT (a tipus neve = a section id)
1. chat.html: `DM.<tipus> = function (f, D) { ... };` a "2. csomag" blokk UTÁN, a `function feladatElem(f) {` sor ELÉ, egy új "// ── 3. csomag (6. minta) ──" megjegyzés alá. ES5 (var, function), 4 szóköz behúzás.
   - A rajz és a működés a mintaoldalé legyen (Sándor jóváhagyta), de: NINCS „Új feladat” gomb, egy feladat = egy elem; a lényeges adatot a tanár adja (f.*), véletlen csak a nem lényeges dolgokhoz.
   - id-k helyett data-id + D.$('…'); minden látható szöveg D.T('magyar', 'español'), természetes spanyolországi spanyollal. Spanyol tantervnél (D.es) a tartalom is spanyol.
   - Befejezés: D.ellenoriz(fn) – a Kész gomb; fn {hianyzik, jo, uzenet, valasz}-t ad vissza –, vagy önmagától eldőlő feladatnál D.vege(jo, uzenet, valasz); a második rossz próbálkozás után a válasz mindenképp elmegy (nézd meg DM.tortcmp-ben). A `valasz` egyes szám első személyű mondat a gyerek nevében (ez megy a tanárnak), az `uzenet` rövid magyarázat a gyereknek.
   - Hang: SOHA ne speechSynthesis. Ha kimondás kell, csak D.mond(szöveg). A hangrendszerhez nyúlni TILOS.
   - Ha több SVG-ben ugyanaz a gradiens/szűrő id lenne, tedd egyedivé.
   - Gyereknek (6–12 év) érthető legyen; nincs tagadó vagy dupla tagadó kérdés; a feliratok nem lóghatnak egymásra; 320 px széles telefonon se lógjon ki semmi.
2. CSS: csak ami hiányzik, minden szelektor ".dm " előtaggal, a ".dm .dm-kesz-sor" sor UTÁN. Globális szabály (body, button stb. előtag nélkül) TILOS.
3. app.py: `if tipus == "<tipus>":` blokk az `if tipus == "akcio":` blokk UTÁN, az `if tipus == "modell":` ELŐTT. Ellenőrizd, hogy a feladat megoldható és egyértelmű; gyanús → return None. A kérdés: _rov(adat.get("kerdes"), 120) vagy jó magyar/spanyol alapértelmezés (es_tanterv szerint); figyelj a ragozásra (ne „a(z)”, ne „5-os”).
4. app.py: új tuple a _DM_FELULETEK lista VÉGÉRE, a meglévők mintájára. Címkék: "matek", "kornyezet", "magyar", "enek", "nyelv", "digit". Ha az elem történelem (korszak), vegyél fel egy "tortenelem" címkét: a _dm_cimkek függvényben `if any(k in s for k in ("tortenelem", "historia")): c.add("tortenelem")`.
5. tanar_teszt.py: az új típusneveket add hozzá a `if tipus in ("csoport", "szotag", ...` felsoroláshoz.

SZIGORÚ SZABÁLYOK
- Meglévő elemekhez, a dmKornyezet-hez, a hang-rendszerhez és a static/kartyak mappához NE nyúlj. Ne formázd át a meglévő kódot. A fájlok CRLF sorvégűek, így is maradjanak.
- Ne találj ki új D-függvényt a közös részbe; ha valami kell, az elemen belül írd meg.

ELLENŐRZÉS (kötelező, írd ki az eredményt – ha valamelyik nem sikerül, mondd meg őszintén)
- python -m py_compile app.py tanar_teszt.py → hibátlan.
- Keresd vissza és írd ki a sorszámmal: minden "DM.<tipus> = function" a chat.html-ben, minden `if tipus == "<tipus>":` az app.py-ban, minden ("<tipus>", tuple a _DM_FELULETEK-ben.
- Írj egy ideiglenes Python-szkriptet (NE a projektbe), amely `import app` után minden új típusra meghívja: app._feladat_parse_belso('<FELADAT>{...}</FELADAT>', grade=4, es_tanterv=False/True, temakor='x') – egy jó magyar, egy jó spanyol és egy hibás bemenettel. Írd ki a kimenetet: a jónál dict, a hibásnál None kell.
- Nézd át a chat.html-t: a <script> blokkban nincs szintaktikai hiba (pl. `node -e` -vel a blokk kiszedése és new Function-nel ellenőrzése).
```

---

## 13. PROMPT – ciklus, szin, hangszer, szoba, tapl

```
ELEMEK: ciklus, szin, hangszer, szoba, tapl
MINTAOLDAL: "Claude outputs/interaktiv_minta8.html"
KÜLÖN MEGJEGYZÉS: A "ciklus" (életciklus, pl. lepke) rajzai GYENGÉK voltak – rajzold meg őket gondosabban, részletesebben (egybefüggő, szép formák), vagy ha nem megy szépen, használj emojit. A "hangszer" WebAudio-s hangja (nem beszéd) maradhat.

Feladat: a MINTAOLDAL sorban megadott mintaoldal fenti elemeit (a <section id="..."> azonosítók) beépíteni a TutorIA chat-táblájára, magyarul és spanyolul. Ugyanúgy, ahogy az előző 40 elem be van építve – azokat kövesd PONTOSAN mintának.

HOL VAN A MINTA
- templates/chat.html: a "var DM = {};" sornál kezdődik a futtató rész (dmKornyezet: a D objektum – D.T, D.$, D.html, D.el, D.txt, D.ellenoriz, D.vege, D.kuld, D.kartyaHuzas, D.huzosLista, D.billentyuzet, D.mond …). Utána jönnek a kész elemek: DM.csoport, DM.tortcmp, DM.kerekit, DM.romai, DM.naptar, DM.szervek, DM.venn stb. A "// ── 2. csomag (5–6. minta) ──" megjegyzés után a legújabbak.
- templates/chat.html CSS: a ".dm .dm-kesz-sor{margin-top:12px}" sor környékén vannak a .dm-es szabályok.
- app.py: a _feladat_parse_belso függvényben az `if tipus == "csoport":` … `if tipus == "akcio":` blokkok (az `if tipus == "modell":` ELŐTT) – ezek ellenőrzik szerveroldalon a tanár által küldött adatot.
- app.py: _DM_FELULETEK lista (tuple-ok: tipus, címkék, évfolyam-tól, -ig, magyar leírás + <FELADAT> példa, spanyol leírás + példa, magyar választó-sor, spanyol választó-sor) és a _dm_cimkek függvény.
- tanar_teszt.py: a `if tipus in ("csoport", "szotag", ...` sor.

MIT CSINÁLJ ELEMENKÉNT (a tipus neve = a section id)
1. chat.html: `DM.<tipus> = function (f, D) { ... };` a "2. csomag" blokk UTÁN, a `function feladatElem(f) {` sor ELÉ, egy új "// ── 3. csomag (6. minta) ──" megjegyzés alá. ES5 (var, function), 4 szóköz behúzás.
   - A rajz és a működés a mintaoldalé legyen (Sándor jóváhagyta), de: NINCS „Új feladat” gomb, egy feladat = egy elem; a lényeges adatot a tanár adja (f.*), véletlen csak a nem lényeges dolgokhoz.
   - id-k helyett data-id + D.$('…'); minden látható szöveg D.T('magyar', 'español'), természetes spanyolországi spanyollal. Spanyol tantervnél (D.es) a tartalom is spanyol.
   - Befejezés: D.ellenoriz(fn) – a Kész gomb; fn {hianyzik, jo, uzenet, valasz}-t ad vissza –, vagy önmagától eldőlő feladatnál D.vege(jo, uzenet, valasz); a második rossz próbálkozás után a válasz mindenképp elmegy (nézd meg DM.tortcmp-ben). A `valasz` egyes szám első személyű mondat a gyerek nevében (ez megy a tanárnak), az `uzenet` rövid magyarázat a gyereknek.
   - Hang: SOHA ne speechSynthesis. Ha kimondás kell, csak D.mond(szöveg). A hangrendszerhez nyúlni TILOS.
   - Ha több SVG-ben ugyanaz a gradiens/szűrő id lenne, tedd egyedivé.
   - Gyereknek (6–12 év) érthető legyen; nincs tagadó vagy dupla tagadó kérdés; a feliratok nem lóghatnak egymásra; 320 px széles telefonon se lógjon ki semmi.
2. CSS: csak ami hiányzik, minden szelektor ".dm " előtaggal, a ".dm .dm-kesz-sor" sor UTÁN. Globális szabály (body, button stb. előtag nélkül) TILOS.
3. app.py: `if tipus == "<tipus>":` blokk az `if tipus == "akcio":` blokk UTÁN, az `if tipus == "modell":` ELŐTT. Ellenőrizd, hogy a feladat megoldható és egyértelmű; gyanús → return None. A kérdés: _rov(adat.get("kerdes"), 120) vagy jó magyar/spanyol alapértelmezés (es_tanterv szerint); figyelj a ragozásra (ne „a(z)”, ne „5-os”).
4. app.py: új tuple a _DM_FELULETEK lista VÉGÉRE, a meglévők mintájára. Címkék: "matek", "kornyezet", "magyar", "enek", "nyelv", "digit". Ha az elem történelem (korszak), vegyél fel egy "tortenelem" címkét: a _dm_cimkek függvényben `if any(k in s for k in ("tortenelem", "historia")): c.add("tortenelem")`.
5. tanar_teszt.py: az új típusneveket add hozzá a `if tipus in ("csoport", "szotag", ...` felsoroláshoz.

SZIGORÚ SZABÁLYOK
- Meglévő elemekhez, a dmKornyezet-hez, a hang-rendszerhez és a static/kartyak mappához NE nyúlj. Ne formázd át a meglévő kódot. A fájlok CRLF sorvégűek, így is maradjanak.
- Ne találj ki új D-függvényt a közös részbe; ha valami kell, az elemen belül írd meg.

ELLENŐRZÉS (kötelező, írd ki az eredményt – ha valamelyik nem sikerül, mondd meg őszintén)
- python -m py_compile app.py tanar_teszt.py → hibátlan.
- Keresd vissza és írd ki a sorszámmal: minden "DM.<tipus> = function" a chat.html-ben, minden `if tipus == "<tipus>":` az app.py-ban, minden ("<tipus>", tuple a _DM_FELULETEK-ben.
- Írj egy ideiglenes Python-szkriptet (NE a projektbe), amely `import app` után minden új típusra meghívja: app._feladat_parse_belso('<FELADAT>{...}</FELADAT>', grade=4, es_tanterv=False/True, temakor='x') – egy jó magyar, egy jó spanyol és egy hibás bemenettel. Írd ki a kimenetet: a jónál dict, a hibásnál None kell.
- Nézd át a chat.html-t: a <script> blokkban nincs szintaktikai hiba (pl. `node -e` -vel a blokk kiszedése és new Function-nel ellenőrzése).
```

---

## Ami nem Cursorra megy
- A kisfiú („arc”) és a maci („oltoz”) elem – ezeket a kész AI-képekkel én építem be.
- Az „arnyek”, „hold” és „terulet” a 8. mintaoldalon már bent van az appban, ezek kimaradnak.
