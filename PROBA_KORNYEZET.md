# Próba oldal (staging) — lépésről lépésre

Cél: legyen egy második, titkos URL, ahol te kipróbálod a fejlesztést, és
csak akkor kerül az élesre, ha jó. Az éles oldalt idegen gyerekek fogják
használni — oda nem mehet ki nem tesztelt kód.

Ha valamelyik lépésnél elakadsz, írd meg, melyik számnál és mit látsz.

---

## 1. A `proba` ág létrehozása (a te gépeden, egyszer)

Nyisd meg a parancssort a projektmappában, és futtasd sorban:

```
cd C:\Users\User\Desktop\TutorIA
git checkout -b proba
git push -u origin proba
git checkout main
```

Ennyi. Mostantól két ág van:

- `main` → ez az ÉLES oldal
- `proba` → ez lesz a próba oldal

Ellenőrzés: `git branch` — két sort kell látnod, `main` és `proba`.

---

## 2. Railway: új service a `proba` ágra

A Railway oldalán, a TutorIA projektben:

1. Jobb felül **New** → **GitHub Repo** → válaszd ki a `Sanci81/TutorIA`-t.
2. Az új service létrejön. Kattints rá, majd **Settings** fül.
3. **Source** résznél a **Branch** legyen `proba` (alapból `main`-t választ —
   ezt KELL átállítani, különben ugyanazt futtatja, mint az éles).
4. Ugyanitt **Service Name**: írd át `tutoria-proba`-ra, hogy össze ne keverd.

---

## 3. Külön adatbázis a próbának

**Ez nem elhagyható.** Ha a próba az éles adatbázist használja, egy elrontott
migráció a valódi gyerekek haladását törli.

1. A projektben **New** → **Database** → **PostgreSQL**.
2. Nevezd át `postgres-proba`-ra (a Postgres service Settings fülén).
3. Menj a `tutoria-proba` service **Variables** fülére, és add hozzá:
   `DATABASE_URL` = az új Postgres `DATABASE_URL` értéke.
   A Railway-en ezt a **Reference** gombbal tudod behúzni: válaszd ki a
   `postgres-proba` service-t és a `DATABASE_URL` változóját. Így akkor is
   jó marad, ha a Railway később megváltoztatja a jelszót.

---

## 4. A többi környezeti változó

Másold át az élesről a `tutoria-proba` **Variables** fülére ugyanezeket:

| változó | mi legyen a próbán |
|---|---|
| `OPENAI_API_KEY` | **külön kulcs**, ne ugyanaz — így külön látod, mennyit fogyaszt a fejlesztés |
| `SECRET_KEY` | **más érték**, mint az élesen (bármilyen hosszú véletlen szöveg) |
| `AZURE_SPEECH_KEY`, `AZURE_SPEECH_REGION` | ugyanaz jó |
| `RESEND_API_KEY` | ugyanaz jó, de lásd lent a levelekről |
| `ADMIN_EMAILEK` | nem kell, a két címed a kódban van |

Miért külön `SECRET_KEY`: ez titkosítja a bejelentkezési sütit. Ha ugyanaz,
a próbán kiadott süti az élesen is érvényes lenne.

---

## 5. Az éles service ellenőrzése

Menj vissza az ÉLES service Settings → Source oldalára, és nézd meg, hogy a
Branch tényleg `main`. Ha eddig nem volt ág megadva, most állítsd be.

---

## 6. A mindennapi munka ettől kezdve

Fejlesztéskor:

```
git checkout proba
   ... itt a módosítások ...
git add .
git commit -m "amit csináltál"
git push
```

A Railway magától telepíti a próba URL-re. Ott kipróbálod.

Ha jó, akkor megy az élesre:

```
git checkout main
git merge proba
git push
```

Ha nem jó, egyszerűen tovább dolgozol a `proba` ágon — az éleshez nem nyúltál.

---

## 7. Amire figyelni kell

**A próba oldalt ne indexelje a Google.** A próba service Variables fülén
add hozzá: `NOINDEX` = `1`, és szólj, hogy a kódban is kezeljem le.

**Levelek.** Ha a próbán regisztrálsz, valódi levelet küld. Teszteléshez a
saját címedet használd, ne másét.

**Költség.** A második service és a második adatbázis a Railway-en kb. havi
5–10 € többlet. Ez az ára annak, hogy ne az éles oldalon derüljön ki egy hiba.

**Az adatbázis a próbán üres lesz.** Regisztrálj rajta egy tesztszülőt és
két tesztgyereket — azokkal próbálsz. Az éles adatokat NE másold át:
valódi gyerekek adatai, nincs rá jogalapod.
