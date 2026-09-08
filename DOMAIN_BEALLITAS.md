# A domain rákötése — tutoriacademia.com

Cél: a `web-production-d406e.up.railway.app` helyett a saját címed nyíljon
meg. A Railway-es cím ettől még működni fog, nem veszik el semmi.

Két helyen kell csinálni valamit: a **Railway-en** megmondod, hogy ez a
domain hozzád tartozik, a **Cloudflare-en** pedig megmondod, hogy ez a
domain a Railway-re mutasson. A sorrend számít: előbb a Railway.

---

## 1. Railway: a domain bejelentése

1. Railway → a **TutorIA projekt** → kattints a webes service-re (az, amit
   most a `web-production-d406e` cím szolgál ki, NEM a Postgres).
2. **Settings** fül → görgess a **Networking** részhez.
3. **Custom Domain** → **+ Add Domain**.
4. Írd be: `tutoriacademia.com` → **Add**.
5. Kattints megint a **+ Add Domain**-re, és írd be: `www.tutoriacademia.com`
   → **Add**.

A Railway most kiír egy **CNAME célt** — valami ilyet:
`abc123.up.railway.app`. **Ezt a szöveget másold ki**, ez kell a következő
lépéshez. Mindkét domainhez ugyanazt adja.

Amíg nincs kész a DNS, a Railway sárgán jelzi, hogy „Waiting for DNS" —
ez normális.

---

## 2. Cloudflare: a domain a Railway-re mutasson

1. Cloudflare → **Account home** → kattints a `tutoriacademia.com`-ra.
2. Bal oldalon **DNS** → **Records** → **Add record**.

**Első rekord (a fő cím):**

| mező | mit írj be |
|---|---|
| Type | `CNAME` |
| Name | `@` |
| Target | a Railway-től kimásolt cím |
| Proxy status | **DNS only** (a felhő legyen SZÜRKE, ne narancs) |
| TTL | Auto |

Mentés: **Save**.

**Második rekord (a www):**

| mező | mit írj be |
|---|---|
| Type | `CNAME` |
| Name | `www` |
| Target | ugyanaz a Railway-cím |
| Proxy status | **DNS only** (szürke felhő) |
| TTL | Auto |

Mentés: **Save**.

> **Miért szürke a felhő?** A narancs (proxy) módban a Cloudflare a saját
> tanúsítványát tenné a Railway elé, és a kettő könnyen összeakad —
> „túl sok átirányítás" hibát okoz. DNS-only módban a Railway intézi a
> tanúsítványt, és minden magától működik. Később, ha akarod, be lehet
> kapcsolni a proxyt, de akkor a Cloudflare SSL módját „Full (strict)"-re
> kell állítani.

---

## 3. Várakozás

A Railway Networking oldalán a sárga „Waiting for DNS" pár perc múlva
zöldre vált, és kiírja, hogy a tanúsítvány kész. Ez általában 2–10 perc,
de akár egy órát is várhat. Nem kell csinálni közben semmit.

Amikor zöld, nyisd meg: **https://tutoriacademia.com** — a főoldalnak kell
jönnie, lakat ikonnal a címsorban.

---

## 4. Amit még be kell állítani UTÁNA

**A levelekben lévő linkek.** A jelszó-visszaállító és az értesítő levelek
a program szerint építik a linkeket. Railway → a service **Variables**
fülén vedd fel:

`APP_URL` = `https://tutoriacademia.com`

Enélkül a levelekben a régi railway.app-os cím maradna.

**Az admin oldal.** Semmit nem kell tenni: ugyanaz a program szolgálja ki,
tehát a saját címeden is ott lesz — `https://tutoriacademia.com/admin`.
Ugyanúgy csak a te két e-mail-címed jut be. Ugyanez igaz a többi
üzemeltetői oldalra is (`/abra-naplo`, `/kiejtes-proba`).

**A régi cím.** A `web-production-d406e.up.railway.app` tovább él és
működik. Nem baj: te ismered, más nem. Ha zavar, később a Railway-en el
lehet rejteni.

---

## Ha valami nem stimmel

- **„Waiting for DNS" fél óra után is:** nézd meg a Cloudflare DNS
  rekordokat — a Target pontosan az, amit a Railway adott? A felhő
  szürke?
- **„Too many redirects":** a felhő narancs. Állítsd DNS-only-ra.
- **Nem biztonságos a kapcsolat:** a tanúsítvány még készül, várj pár
  percet, és frissíts.

Ha elakadsz, írd meg, melyik lépésnél és mit látsz.
