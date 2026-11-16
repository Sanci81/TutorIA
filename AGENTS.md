# TutorIA – térkép az AI-asszisztensnek (Claude, Cursor, bármelyik modell)

Olvasd el ELŐSZÖR. Ez csak térkép: a részletek a kódban és a `TEENDOK.md`-ben
vannak. Magyarul válaszolj, röviden. Frissítve: 2026-11-16.

## MI EZ

Kétnyelvű AI-tanár gyerekeknek. Magyar oldal: 1–8. osztály (NAT kerettanterv).
Spanyol oldal: 1.º–6.º Primaria (LOMLOE). Flask + SQLAlchemy, Railway-en fut,
élesben **PostgreSQL** (a helyi teszt SQLite-on megy – eltérhet!).
Tulajdonos: Sándor, NEM programozó, magánszemélyként fizet mindent.

- `proba` ág → próba oldal (web-production-fb5a05.up.railway.app), saját adatbázis
- `main` ág → éles: tutoriacademia.com
- Mindig: először `git push origin proba`, ellenőrzés, csak utána `proba:main`.

## SZABÁLYOK (nem szeghetők meg)

1. **Külalak előtt MUTASD MEG** (kép/HTML minta), csak utána módosíts.
2. **Csak azt változtasd, amit kértek.** Ha más útban van: szólj, ne javítsd.
3. **A tanítás minősége nem romolhat.** Minden új viselkedés env flaggel
   kikapcsolható legyen, és először a próba oldalra menjen.
4. **Push előtt:** `python -m py_compile app.py` és `python hang_teszt.py`
   (ingyenes, mind "ok" kell). Minden javított hiba kerüljön be a tesztbe.
5. **`static/kartyak/` mappába NEM írunk** (átnevezés = duplikátum). Mondd meg
   Sándornak, mit nevezzen át / másoljon.
6. **Kulcsot soha** ne írj ki; példában: `ide-a-sajat-kulcsod`.
7. **Gyerekek mentett beszélgetéseit (`mentes_*.json`) nem olvassuk.**
8. **Hang/TTS viselkedéshez** csak Sándor engedélyével nyúlunk.
9. **Pénzbe kerülő futtatás** (AI, képgenerálás) csak kérdés után. A kártyakép-
   generálás SZÜNETEL, amíg nincs regisztráció.
10. **Git:** `git add <konkrét fájlok>`, soha `-A`.
11. Ami nincs kész, vagy fontos később: **automatikusan a `TEENDOK.md`-be.**
12. Jog: nincs kamu vélemény, nincs követő süti / Facebook Pixel.

## FŐ FÁJLOK

| fájl | mit csinál |
|---|---|
| `app.py` (~1 MB, ~100 útvonal) | minden útvonal, tanári prompt, chat, admin |
| `database.py` | táblák, lekérdezések (DATABASE_URL) |
| `translations.py` / `i18n` | HU/ES felületi szövegek |
| `curriculum_loader.py` | kerettantervi JSON-ok (`hu_kerettanterv_*`, `es_kerettanterv/`) |
| `oraterv.py`, `oratervek/` | előre kész óratervek a promptba |
| `hang.py`, `kiejtes.py` | AMIT A GYEREK HALL (számok, ragok kiejtése) |
| `szamellenor.py` | AMIT A GYEREK LÁT: rossz kérdésformák javítása |
| `hang_teszt.py` | ingyenes regressziós teszt (fenti kettő) |
| `tanar_teszt.py` | órákat játszik le – PÉNZBE KERÜL |
| `mintalecke.py` + `templates/mintalecke.html` | ingyenes mintalecke (regisztráció nélkül), képek: `static/img/minta/*.svg` |
| `kartyak.py`, `kartyak_es.py`, `tasak.py`, `pontok.py` | tudáskártyák, pontok, album |
| `csomagok.py` | csomagok/bérletek (fizetés MÉG NINCS, nincs Stripe) |
| `level.py` | e-mailek (Resend) |
| `jogi/` | DPIA, adatkezelési nyilvántartás, LIA |
| `templates/` | Jinja oldalak (index, chat, album, feltetelek, adatvedelem…) |
| `static/css/style.css` | közös stílus (asztali fejléc a végén) |
| `TEENDOK.md` | nyitott feladatok, fix-számokkal (fixNNN) |

## FONTOS HELYEK AZ `app.py`-BAN (keress a névre, ne sorszámra)

- `child_chat_send` – a gyerek chatje, ide fűződnek a prompt-blokkok
  (`_TANITO_PONTOS_HU/_ES`, FELADAT_TIPP stb.)
- `_DM_FELULETEK` – interaktív feladattípusok listája. Tuple:
  `(tipus, cimkek, min_evf, max_evf, HU leírás, ES leírás, "HU név → tipus", "ES név → tipus")`.
  A Feladat-próba neve: a HU sor `→` előtti része.
- `_feladat_parse_belso` – a feladatok ellenőrzője (típusonként egy `if tipus ==` ág)
- `_dm_cimkek` – tantárgy → címke
- Frontend párja: `templates/chat.html` → `DM.<tipus> = function(f, D)`
- `_szulo_csomag`, `_ajandek_cimek` – csomag, ajándék percek
- `fiok`, `fiok_torles`, `csomagok_oldal`, `register`, `mintalecke*`, `admin_*`

Minden új feladattípusnál írd meg: Feladat-próba név, melyik évfolyam,
működik-e a spanyol oldalon.

## ENV FLAGEK (Railway; a próba és az éles KÜLÖN állítandó)

Funkciók: `MINTALECKE`, `TANITO_PONTOS`, `FELADAT_TIPP`, `NYITO_FELADAT`,
`POTLAS_JO`, `KERDES_LEKTOR`, `EMAIL_MEGEROSITES`, `EMLEKEZTETO`,
`FIZETES_ELERHETO`, `PROBA_OLDAL`. Admin: `ADMIN_EMAILEK`, `ADMIN_KOD`,
`AJANDEK_CIMEK` (vesszővel elválasztott e-mailek → TESZT csomag).
Modellek: `MODELL_*`, `TANAR_API_*`. A `0` érték kikapcsol.

## TECHNIKAI CSAPDÁK

- Python 3.12 kell a fordításhoz.
- A felület a nyelvet ékezet nélkül küldi (`nemet`); fogadd el mindkét alakot.
- OpenAI JSON-válaszhoz a kérésben legyen benne a "json" szó.
- Sortörést tartalmazó API-kulcs → félrevezető `Connection error`.
- Böngésző kb. 6 AudioContextet enged – ne hozz létre újat hívásonként.
- Spanyol chat: `chat-frame` rejtett mező kell szöveges módban is (különben
  magyar bevezető jön).
- Kártyák: `kartyak.mappa(oldal)` – lapos `static/kartyak/<oldal>/`; spanyol
  `kep` nevekben nincs évfolyamszám.

## MÉRÉS ÉS JAVÍTÁS NEM EGYSZERRE

Az ellenőrző listát rögzítsd → mérj → csak a programot javítsd → mérj újra
ugyanazzal. Ha közben az ellenőrzőt is módosítod, a két szám értéktelen.

## FIZETÉS ELŐTT KÖTELEZŐ (részletek: TEENDOK fix155–157)

Pipák + „Fizetési kötelezettséggel járó megrendelés” gomb, visszaigazoló
e-mail, „Elállás a szerződéstől itt” gomb (14 napig), arányos visszatérítés
jóváhagyással, lemondás ≠ fióktörlés, számlák megőrzése törlés után is,
áfával/IVA incluido kiírás, automata teszt a pénzes utakra (Stripe tesztmód).
