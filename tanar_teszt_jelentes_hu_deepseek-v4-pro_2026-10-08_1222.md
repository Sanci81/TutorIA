# TutorIA – tanári minőség, 2026-10-08 12:16

Tanár modellje: **deepseek-v4-pro** (https://api.deepseek.com/v1)  
Tanári hívások: **12**, ebből elszállt: **0**  
Átlagos válaszidő: **24.0 mp**  
Tokenek: be **189,449**, ki **16,967**  
Oldal: **magyar**  
Lejátszott órák: **3**  
Gépi találat (számtan, felolvasás, szivárgás, jelölőhiba, hiányzó kérdés — ez NEM vélemény): **2**  
Az ellenőrző szerint biztos hiba: **6**  
Az ellenőrző szerint gyanús: **2**

> Az ellenőrző maga is egy AI. Nem talál meg mindent, és néha
> olyat is megjelöl, ami rendben van. A lista nem ítélet — nézd át.
> A GÉPI találatok viszont tények, azokat nem kell mérlegelni.


## Gépi találatok fajtánként

- [üres]: **2**

## Gépi találatok

- **Digitális kultúra** (6. o.): [üres] a válaszból a gyerek semmit nem lát
- **Földrajz** (7. o.): [üres] a válaszból a gyerek semmit nem lát

## Amit az ellenőrző talált


### 3. TÉNYBELI HIBA. Bármely tantárgyban: rossz évszám, rossz képlet, rossz

- **BIZTOS** — Digitális kultúra 6. o., „Szöveg bevitele, javítása, mentése”
  - A tanár ezt mondta: „Például van egy mondatod: "A macska a széken ül." Ki szeretnéd cserélni a "macska" szót "kutyá"-ra.”
  - Miért baj: A „kutyá” alak hibás, helyesen „kutyá”-ra helyett „kutyára” vagy egyszerűen „kutyá”-tól függően más szerkezet kellene, de így biztosan nem jó szóalak.
- **BIZTOS** — Digitális kultúra 6. o., „Szöveg bevitele, javítása, mentése”
  - A tanár ezt mondta: „Képzeld el, hogy ezt írod egy fogalmazásban: "A fiu a parkba megy." A program két szót is aláhúz, mert a "fiu" helyesen "fiú", a "parkba" pedig "parkba" — várj, az utóbbi jó.”
  - Miért baj: A tanár előbb tévesen azt állítja, hogy a „parkba” hibás, majd javítja magát; ez tényszerű hibás magyarázat a tananyagban.
- **BIZTOS** — Földrajz 7. o., „Tájékozódás a térképen – fokhálózat és méretarány”
  - A tanár ezt mondta: „A szélességi körök tényleg észak-déli irányba adják meg a helyzetünket, a hosszúsági körök pedig kelet-nyugati irányba.”
  - Miért baj: Ténybeli hiba, mert a szélességi körök kelet–nyugati irányú körök, a hosszúsági körök pedig észak–déli irányú félkörök; legfeljebb azt lehet mondani, hogy a szélesség északra vagy délre, a hosszúság keletre vagy nyugatra mutat.
- gyanús — Digitális kultúra 5. o., „Mi az algoritmus? Lépések és sorrend”
  - A tanár ezt mondta: „A tea készítése. 🍵 A bemenet: víz, teafilter, csésze, cukor.”
  - Miért baj: Ténybelileg hiányos vagy pontatlan, mert a csésze és a cukor nem szükségszerű bemenete minden teakészítésnek, a tea pedig cukor nélkül is tea.

### 4. ÍGÉRT, DE HIÁNYZÓ DOLOG. "Nézd meg az ábrát", "itt egy kép", "lent

- gyanús — Digitális kultúra 5. o., „Mi az algoritmus? Lépések és sorrend”
  - A tanár ezt mondta: „Nézd meg jól: a bemenet az, amit beleteszel a folyamatba, a kimenet pedig az, amit kapsz belőle.”
  - Miért baj: A tanár azt mondja, hogy „nézd meg”, de itt nem hivatkozik valódi ábrára vagy látható elemre, csak szövegre.

### 8. MAGYARTALAN VAGY IDEGENSZERŰ MONDAT. Rossz ragozás, tükörfordítás,

- **BIZTOS** — Digitális kultúra 5. o., „Mi az algoritmus? Lépések és sorrend”
  - A tanár ezt mondta: „A bemenet hozzá: liszt, tojás, tej, cukor, egy kis só.”
  - Miért baj: A „hozzá” itt magyartalanul hat; természetesebben az lenne, hogy „a bemenete” vagy „a hozzávalók”.
- **BIZTOS** — Digitális kultúra 5. o., „Mi az algoritmus? Lépések és sorrend”
  - A tanár ezt mondta: „A kimenet pedig: egy forró, finom csésze tea.”
  - Miért baj: Magyartalan a szerkezet, mert nem a csésze forró és finom, hanem a tea; természetesebben: „egy csésze forró, finom tea”.

### 12. TECHNIKAI SZEMÉT A KÉPERNYŐN. Olyasmi látszik, ami a programnak szólt,

- **BIZTOS** — Földrajz 7. o., „Tájékozódás a térképen – fokhálózat és méretarány”
  - A tanár ezt mondta: „[A szöveg alatt ez a feladat jelenik meg – választható gombok: délnyugat / délkelet / északnyugat / északkkelet]”
  - Miért baj: Technikai vagy tartalmi hiba a feladatrészben, mert az egyik válaszlehetőség el van írva: „északkkelet”.

---

A teljes beszélgetések: `tanar_teszt_beszelgetesek_hu_2026-10-08_1216.txt`
