# Cursor-promptok – délutánig (kb. 4 óra munka)

## Hogyan használd
1. Cursorban nyisd meg a TutorIA mappát, kapcsold **Agent** módba, és a legerősebb elérhető modellt válaszd (ha van Kimi K2 vagy DeepSeek a Cursorban, az is jó). A DeepSeek/Kimi **sima chat-ablakban** nem tudja szerkeszteni a fájljaidat – oda ne ezeket másold.
2. **Egyszerre EGY promptot** adj be (a ``` közötti részt), és várd meg, amíg kész.
3. Minden prompt végén a modellnek ki kell írnia az ELLENŐRZÉS részt. Ha bármelyik pont hiányzik, írd neki: „Nem csináltad meg az ellenőrzést, csináld meg most."
4. Utána a saját ellenőrzés (minden prompt alatt ott van), és csak akkor git:
```
git checkout proba
git add -A
git commit -m "<a prompt címe>"
git push origin proba
```
5. Ha valami elromlott, és nem tudod javíttatni: `git checkout -- .` (minden be nem commitolt változást eldob), és hagyd délutánra.

Sorrend: 1 → 2 → 3 → 4. Az 1. a legfontosabb (robot elleni védelem), a 2–4. a 3. csomag elemei (12 új elem, 4-esével).

---

## 1. PROMPT – Robot elleni védelem (kb. 45 perc)

```
Feladat a TutorIA Flask appban (app.py, templates/register.html, templates/login.html, templates/forgot_password.html, translations.py): védelem robotok ellen a regisztrációnál, a belépésnél és az elfelejtett jelszónál. Külső szolgáltatás (reCAPTCHA, Cloudflare) NEM kell.

SZIGORÚ SZABÁLYOK
- Csak a felsorolt fájlokhoz nyúlhatsz. A hang-rendszerhez (hang.py, speakUrl, TTS) és a static/kartyak mappához tilos.
- A fájlok CRLF sorvégűek, így is maradjanak. Ne formázd át a meglévő kódot, ne nevezz át semmit.
- Minden felhasználónak látszó szöveg magyarul ÉS spanyolul legyen, a translations.py meglévő mintája szerint (i18n.t("kulcs", g.lang)).

MIT CSINÁLJ
1. Csapda-mező (honeypot) a regisztrációs és az elfelejtett jelszó űrlapon: egy "weboldal" nevű szövegmező, amely embernek láthatatlan (CSS-sel képernyőn kívülre téve, NEM display:none), tabindex="-1", autocomplete="off", aria-hidden="true". Ha a beküldött űrlapon ez nem üres → úgy teszünk, mintha sikerült volna (ugyanaz az átirányítás/üzenet, mint sikernél), de NEM hozunk létre fiókot, NEM küldünk e-mailt, és logger.warning-gal naplózzuk.
2. Időzár: az űrlap egy rejtett mezőben hordozza a megjelenítés idejét (szerveroldalon aláírva, pl. itsdangerous URLSafeTimedSerializer az app.secret_key-jel). Ha a beküldés 3 másodpercen belül jön, vagy az aláírás hibás/hiányzik → ugyanaz a csendes elutasítás, mint az 1. pontnál.
3. Gyakoriság-korlát IP-nként (memóriában, egy dict + threading.Lock elég; az IP: request.headers.get("X-Forwarded-For", request.remote_addr) első eleme, ahogy az app.py ~1581. sorában is van):
   - /login POST: legfeljebb 10 próbálkozás 10 percen belül,
   - /register POST: legfeljebb 5 / óra,
   - /forgot-password POST: legfeljebb 5 / óra.
   Túllépéskor flash üzenet (új fordítási kulcs: "flash_tul_sok_proba": HU "Túl sok próbálkozás. Várj egy kicsit, és próbáld újra!", ES "Demasiados intentos. Espera un poco y vuelve a intentarlo.") és az űrlap újra megjelenik, a kérés nem fut tovább. A régi bejegyzéseket a függvény takarítsa ki, hogy a memória ne nőjön.
4. A meglévő működés semmiben ne változzon egy rendes felhasználónak.

ELLENŐRZÉS (kötelező, írd ki az eredményt)
- python -m py_compile app.py translations.py → írd ki, hogy hibátlan.
- Sorold fel fájlonként, pontosan mely sorokat változtattad (diff-szerűen).
- Írd le, hogyan próbáltad ki: Flask test_client-tel írj egy rövid, ideiglenes szkriptet (NE a projektbe, hanem egy temp fájlba), amely: (a) kitöltött csapda-mezővel regisztrál → nem jön létre fiók; (b) 11-szer rossz jelszóval belép → a 11. már a "túl sok" üzenetet kapja. Írd ki a kimenetét. Ha adatbázis kell hozzá és nem megy, írd meg őszintén.
```

**Saját ellenőrzés:** a próbaoldalon regisztrálj egy új teszt-fiókkal (várj 5 mp-et a kitöltés előtt) – menjen át. Lépj be rendesen – menjen. Ha bármelyik nem megy: ne commitold.

---

## 2–4. PROMPT – A 3. csomag elemei (egyenként kb. 1 óra)

Ugyanaz a szöveg háromszor, csak az ELEMEK sor más. Másold be a közös részt, és cseréld ki benne az `ELEMEK:` sort:

- **2. prompt:** `ELEMEK: kor, maganh, jly, irasjel`
- **3. prompt:** `ELEMEK: elolj, rovar, foto, korszak`
- **4. prompt:** `ELEMEK: kresz, binaris, magnes, ph`

(Az „oltoz" – a maci – most kimarad, azt a képekkel együtt én csinálom.)

```
ELEMEK: kor, maganh, jly, irasjel

Feladat: a "Claude outputs/interaktiv_minta6.html" mintaoldal fenti elemeit (a <section id="..."> azonosítók) beépíteni a TutorIA chat-táblájára, magyarul és spanyolul. Ugyanúgy, ahogy az előző 40 elem be van építve – azokat kövesd PONTOSAN mintának.

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

**Saját ellenőrzés minden elem-prompt után:** a próbaoldalon egy órán kérd meg a tanárt, hogy adjon ilyen feladatot (pl. „Adj egy feladatot a kör részeiről!”), és nézd meg telefonon is: megjelenik-e, működik-e, és a Kész után válaszol-e a tanár. Ha nem jön elő, az még nem hiba (lehet, hogy a tanár mást választott) – ha viszont **megjelenik, de rossz**, ne commitold.

---

## Ami NEM megy Cursorra (ezek délután nálam)
- A kisfiú beépítése a képekkel (mozgással), és a maci egész képekkel.
- A 7. és 8. mintaoldal elemei.
- Az 1. és 2. csomag élesre vitele (`git push origin proba:main`) – ezt te is megcsinálhatod, ha a próbán minden jó.
