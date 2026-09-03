# -*- coding: utf-8 -*-
"""Az előre elkészített óratervek betöltése és beillesztése a tanári promptba.

MIÉRT VAN EZ A FÁJL
    A tanár eddig minden fordulóban a nulláról találta ki, mit tanítson és
    milyen sorrendben. Innen jött a "there is / there are" a létige ELŐTT, és
    innen jöttek a ténybeli tévedések is.

    Az oraterv_keszito.py témakörönként EGYSZER megírja a tanítás lépéseit,
    és egy okosabb modellel átnézeti a tényeit. Ez a fájl azt a kész tervet
    keresi elő, és teszi be a promptba.

HA NINCS TERV, MINDEN MEGY ÚGY, AHOGY EDDIG
    Ha a témakörhöz nincs kész terv, vagy a tanterv időközben megváltozott,
    ez a modul ÜRES SZÖVEGET ad vissza. Az oldal ilyenkor pontosan úgy
    működik, mint eddig. Ez szándékos: a bekötés nem vehet el semmit.
"""

from __future__ import annotations

import hashlib
import json
import logging
from pathlib import Path

log = logging.getLogger(__name__)

MAPPA = Path(__file__).parent / "oratervek"

# Betöltött fájlok. A tervek nem változnak futás közben, elég egyszer
# beolvasni őket. Kulcs: (tantargy_fajl, evfolyam, nyelv).
_GYORSITO: dict[tuple, dict] = {}


def ujjlenyomat(szoveg: str) -> str:
    """A tantervi szöveg lenyomata.

    Ha a kerettantervi JSON szövege megváltozik, ez a lenyomat is más lesz,
    és a régi terv MAGÁTÓL érvényét veszti. Így nem fordulhat elő, hogy egy
    elavult terv szerint tanítunk egy időközben átírt témakört.
    """
    return hashlib.sha256((szoveg or "").encode("utf-8")).hexdigest()[:16]


def fajlnev(tantargy_fajl: str, evfolyam, nyelv: str | None) -> Path:
    alap = (tantargy_fajl or "").replace(".json", "")
    nev = f"{alap}__{evfolyam}" + (f"__{nyelv}" if nyelv else "") + ".json"
    return MAPPA / nev


def _betolt(tantargy_fajl: str, evfolyam, nyelv: str | None) -> dict:
    kulcs = (tantargy_fajl, str(evfolyam), nyelv or "")
    if kulcs in _GYORSITO:
        return _GYORSITO[kulcs]
    adat: dict = {}
    ut = fajlnev(tantargy_fajl, evfolyam, nyelv)
    try:
        if ut.is_file():
            adat = json.loads(ut.read_text(encoding="utf-8")) or {}
    except Exception as hiba:                              # pragma: no cover
        log.warning("ORATERV: %s nem olvasható: %s", ut.name, hiba)
        adat = {}
    _GYORSITO[kulcs] = adat
    return adat


def lepesek(tantargy_fajl: str, evfolyam, nyelv: str | None,
            temakor: dict | None) -> list[dict]:
    """A témakörhöz tartozó tanítási lépések, vagy üres lista.

    Üres listát ad, ha nincs fájl, nincs benne ez a témakör, vagy a témakör
    tantervi szövege időközben megváltozott.
    """
    if not temakor:
        return []
    adat = _betolt(tantargy_fajl, evfolyam, nyelv)
    tervek = adat.get("temakorok") or []
    if not tervek:
        return []

    azonosito = temakor.get("id")
    nev = (temakor.get("name") or "").strip()
    talalat = None
    for t in tervek:
        if azonosito and t.get("temakor_id") == azonosito:
            talalat = t
            break
    if talalat is None:
        for t in tervek:
            if nev and (t.get("temakor") or "").strip() == nev:
                talalat = t
                break
    if talalat is None:
        return []

    regi = talalat.get("ujjlenyomat")
    mostani = ujjlenyomat(temakor.get("text") or "")
    if regi and regi != mostani:
        log.info("ORATERV: %r terve elavult (a tanterv szövege megváltozott), "
                 "nem használom.", nev)
        return []

    return [l for l in (talalat.get("lepesek") or []) if isinstance(l, dict)]


# ── A promptba kerülő szöveg ────────────────────────────────────────────────
_HASZNALAT_HU = """
HOGYAN HASZNÁLD A TERVET
· Nézd meg a beszélgetés előzményében, hol tartotok. Ha még nem kezdtétek el,
  az 1. lépéssel kezdj.
· EGYSZERRE EGY LÉPÉS. Elmagyarázod, mutatod a példát, felteszed az ellenőrző
  kérdést — és MEGVÁROD a választ. Ne told egymás után két lépést.

· HA A VÁLASZ ROSSZ, MARADSZ AZON A LÉPÉSEN. Nem lépsz tovább, nem hozol új
  kérdést, nem kezdesz új témát. Elmagyarázod MÁSKÉPP, MÁS példával, és
  UGYANARRA kérdezel vissza, amíg meg nem lesz.
  EZ EGY VALÓDI HIBA EMLÉKE. A gyerek ezt írta a 4210 + 1680-ra: 5210.
    ROSSZ:  "Jó, hogy próbálkoztál! A helyes 5900. Most jön: 3620 + 2790?"
            (megmondta a választ, és rögtön ugrott a következő kérdésre —
             a gyerek a másodikat is elrontotta, és mentek tovább)
    JÓ:     "Nézzük együtt. A 4210-hez melyik kerek százas van a legközelebb?"
            — és megvárod. Aztán: "És az 1680-hoz?" Csak ha megvan mind a
            kettő, akkor jön az összeadás, és csak utána a következő kérdés.
  Kivétel NINCS. Két rossz válasz után sem lépsz tovább; harmadszorra bontsd
  még kisebb darabokra.

· A JÓ VÁLASZ AZ JÓ — akkor is, ha nem az, amit vártál. Becslős kérdésnél a
  PONTOS eredmény IS helyes, sőt jobb. Ha a gyerek 4210 + 1680-ra 5890-et
  mond, az a pontos összeg: dicsérd meg, és annyit tegyél hozzá, hogy
  becsléssel 5900 jönne ki. NE mondd rá, hogy "elcsúszott".

· A "példa" és a "kérdés" MINTA, nem felolvasandó szöveg. Mondhatod a saját
  szavaiddal, de a TARTALMÁTÓL ne térj el: ezeket a tényeket ellenőriztük.
· Ha a gyerek egy későbbi lépésre kérdez rá, válaszolj röviden, aztán térj
  vissza oda, ahol tartotok.
· NE MONDD MEG a gyereknek, hogy terv szerint haladtok, és ne számozd neki a
  lépéseket. Ez a te jegyzeted, nem az övé.

· TE NEM ÍRSZ TESZTET A BESZÉLGETÉSBE. A felmérés külön gombon van, a képernyő
  jobb felső sarkában: "⭐ Szintfelmérő teszt". Amikor az utolsó lépés is
  megvan, EGY mondatban szólj, hogy erre a gombra kattintva jöhet a teszt.
  NE sorolj fel kérdéseket, és főleg NE azokat, amiket az óra alatt már
  feltettél — azokra a gyerek már hallotta tőled a választ, tehát semmit nem
  mérnek.
"""

_HASZNALAT_ES = """
CÓMO USAR EL PLAN
· Mira en el historial de la conversación por dónde vais. Si aún no habéis
  empezado, empieza por el paso 1.
· UN PASO CADA VEZ. Explicas, muestras el ejemplo, haces la pregunta de
  comprobación — y ESPERAS la respuesta. No juntes dos pasos.
· SI LA RESPUESTA ES INCORRECTA, TE QUEDAS EN ESE PASO. No avanzas, no traes
  una pregunta nueva, no empiezas otro tema. Lo explicas DE OTRA MANERA, con
  OTRO ejemplo, y vuelves a preguntar LO MISMO hasta que salga.
  ESTO RECUERDA UN FALLO REAL. El niño respondió 5210 a 4210 + 1680.
    MAL:  "¡Bien intentado! Lo correcto es 5900. Ahora: ¿3620 + 2790?"
          (dio la respuesta y saltó a la pregunta siguiente — el niño también
           falló esa, y siguieron adelante igualmente)
    BIEN: "Vamos juntos. ¿Qué centena redonda está más cerca de 4210?"
          — y esperas. Después: "¿Y de 1680?" Solo cuando estén las dos, se
          suman, y solo después viene la pregunta siguiente.
  NO hay excepción. Ni después de dos fallos avanzas; a la tercera, divídelo
  en trozos aún más pequeños.

· UNA RESPUESTA CORRECTA ES CORRECTA — aunque no sea la que esperabas. En una
  pregunta de estimación, el resultado EXACTO también vale, e incluso es
  mejor. Si el niño dice 5890 para 4210 + 1680, esa es la suma exacta:
  felicítale y añade que la estimación daría 5900. NO digas que "se ha
  desviado".

· El "ejemplo" y la "pregunta" son MODELOS, no un texto para leer en voz alta.
  Puedes decirlo con tus palabras, pero no cambies el CONTENIDO: estos datos
  están verificados.
· Si el niño pregunta por un paso posterior, respóndele brevemente y vuelve al
  punto en el que estáis.
· NO le digas al niño que seguís un plan, y no le numeres los pasos. Esto es
  tu guion, no el suyo.

· TÚ NO ESCRIBES UN TEST EN LA CONVERSACIÓN. La prueba está en un botón
  aparte, arriba a la derecha: "⭐ Test de nivel". Cuando termines el último
  paso, dilo en UNA frase: que puede pulsar ese botón para hacer el test.
  NO enumeres preguntas, y menos aún las que ya has hecho durante la clase —
  el niño ya te ha oído la respuesta, así que no miden nada.
"""


def prompt_blokk(lepes_lista: list[dict], *, spanyol: bool = False) -> str:
    """A tervből a promptba illeszthető szöveg. Üres lista → üres szöveg."""
    if not lepes_lista:
        return ""

    sorok: list[str] = []
    if spanyol:
        sorok.append("\n=== PLAN DE ENSEÑANZA DEL TEMA ===")
        sorok.append(
            "Este plan ya está hecho y un revisor ha comprobado sus datos. NO "
            "lo reinventes y no te desvíes de él. El orden es obligatorio: "
            "cada paso se apoya en el anterior.")
        cimke = ("qué aprende", "ejemplo", "pregunta")
    else:
        sorok.append("\n=== A TÉMAKÖR TANÍTÁSI TERVE ===")
        sorok.append(
            "Ez a terv előre elkészült, és egy ellenőrző átnézte a tényeit. NE "
            "TALÁLD KI ÚJRA, és ne térj el tőle. A sorrend kötelező: minden "
            "lépés az előzőre épül.")
        cimke = ("mit tanul", "példa", "kérdés")

    for i, lep in enumerate(lepes_lista, 1):
        sorok.append(f"\n  {i}. {(lep.get('cim') or '').strip()}")
        for kulcs, szo in zip(("mit", "pelda", "kerdes"), cimke):
            ertek = (lep.get(kulcs) or "").strip()
            if ertek:
                sorok.append(f"     {szo}: {ertek}")

    sorok.append(_HASZNALAT_ES if spanyol else _HASZNALAT_HU)
    return "\n".join(sorok)
