# -*- coding: utf-8 -*-
"""Lejátszik órákat a gyerek helyett, és megnézi, hibázik-e a tanár.

MIÉRT VAN EZ A FÁJL
    Eddig a hibákat a fiad találta meg, tanulás közben. Ez rossz sorrend:
    mire kiderül, hogy a tanár rosszat mondott, a gyerek már megtanulta.
    Ez a program leül a gyerek helyére, végigcsinál több órát több
    tantárgyból, és utána valaki más átnézi, mit mondott a tanár.

MIT NEM TUD
    Az ellenőrző MAGA IS EGY AI. Nem fog mindent észrevenni, és néha olyat
    is megjelöl, ami valójában rendben van. EZ SZÁNDÉKOS: inkább jelezzen
    tízet, amiből három valódi, mint hogy egyet se. A jelentés nem ítélet,
    hanem egy lista, amit ÁT KELL NÉZNED. Te döntesz, mi hiba.

    Amit viszont GÉPPEL ellenőrzünk (számtan, felolvasás), az nem vélemény:
    azt a szamellenor és a hang modul mondja meg, nem egy modell.

MENNYIBE KERÜL
    Minden lejátszott forduló két AI-hívás (gyerek + tanár), a végén még egy
    az átnézésre. Egy teljes kör nagyjából 1-2 euró. A --gyors kapcsolóval
    ennek a töredéke.

HASZNÁLAT
    python tanar_teszt.py                    minden tantárgy, 6 forduló
    python tanar_teszt.py --gyors            csak 3 óra, 4 forduló
    python tanar_teszt.py --tantargy Matematika --evfolyam 4
    python tanar_teszt.py --fordulo 10       hosszabb órák

    A végén készül egy tanar_teszt_jelentes.md — azt olvasd el.

MI KELL HOZZÁ
    Az OpenAI kulcs a környezetben. PowerShellben, egyszer, indítás előtt:
        $env:OPENAI_API_KEY = "sk-..."
    Adatbázis NEM kell: ez a program nem nyúl a gyerekek adataihoz.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import sys
import traceback
from datetime import datetime

# Az app importálásakor az adatbázis-kapcsolat elbukik, és ezt ki is írja a
# naplóba. Ez ITT NEM BAJ: a promptépítéshez nem kell adatbázis. Elnyomjuk,
# hogy ne tűnjön hibának.
import logging
logging.getLogger().setLevel(logging.CRITICAL)
os.environ.setdefault("SECRET_KEY", "tanar-teszt")

try:
    import app                                    # a VALÓDI tanári prompt
    import curriculum_loader as cl
    import szamellenor
    import hang
except Exception as hiba:                          # pragma: no cover
    print("Nem sikerült betölteni a programot:", hiba)
    print("A tanar_teszt.py-t a TutorIA mappából futtasd.")
    sys.exit(1)


TANAR_MODELL = "gpt-5.4-mini"      # amit a gyerek is kap élesben
GYEREK_MODELL = "gpt-5.4-mini"     # aki a gyereket játssza
ELLENOR_MODELL = "gpt-5.4"         # aki átnézi – ő legyen az okosabb


# ── KIKET JÁTSZUNK ──────────────────────────────────────────────────────────
# Nem egyforma gyerekeket: a hibák nagy része akkor jön elő, amikor a gyerek
# NEM az elvárt módon viselkedik – rosszul válaszol, elkalandozik, visszakérdez.
# A NÉV és a JELLEM állandó, az ÉVFOLYAM a tesztelt tantárgytól függ – így
# ugyanaz a "nehéz gyerek" viselkedés minden évfolyamon előjön.
GYEREKEK = [
    ("Bence", "Rövid válaszokat ad, néha csak egy szót. Gyakran rosszul "
              "válaszol, és olyankor elbizonytalanodik. Néha elkalandozik, "
              "és a kutyájáról kezd beszélni."),
    ("Anna", "Igyekvő, de siet, ezért elszámolja magát. Ha nem érti, "
             "rákérdez: 'ezt nem értem'."),
    ("Viki", "Okos, gyors. Néha SZÁNDÉKOSAN rosszat mond, hogy lássa, mit "
             "szól a tanár. Előreszaladna a nehezebb részre."),
    ("Máté", "Egyszavas válaszok, néha unott. Ha unja, azt mondja, hogy 'ez "
             "uncsi'. Néha HELYESEN válaszol, de másképp fogalmazva, mint "
             "ahogy a tanár várná — ilyenkor NEM szabad kijavítani."),
]

# ── MIT TANÍTSON ────────────────────────────────────────────────────────────
# NEM kézzel felsorolva. A tantárgyakat MAGÁTÓL a tantervből olvassa ki, hogy
# ne csak azt teszteljük, amire épp gondoltunk. Ha holnap új tantárgy kerül a
# tantervbe, ez a program magától tesztelni fogja.
# ÉKEZET NÉLKÜL, mert a felület is így küldi (a select value="nemet").
# Amikor ezt először ékezettel írtam, a teszt német órája nem is tudta
# magáról, hogy német — és én a programot hibáztattam érte.
NYELVEK = ("angol", "nemet", "spanyol")


def _tantargy_matrix(evfolyamok) -> list[tuple]:
    """(fájl, címke, évfolyam, nyelv) az ÖSSZES létező tantárgyra."""
    parok: list[tuple] = []
    for evf in evfolyamok:
        try:
            tantargyak = cl.get_hu_subjects_for_grade(evf) or []
        except Exception:
            continue
        for t in tantargyak:
            fajl, cimke = t.get("value"), t.get("label")
            if not fajl:
                continue
            try:
                idegen = cl.is_elo_idegen_subject(fajl)
            except Exception:
                idegen = False
            if idegen:
                parok.extend((fajl, cimke, evf, ny) for ny in NYELVEK)
            else:
                parok.append((fajl, cimke, evf, None))
    return parok


# ── AMIT AZ ELLENŐRZŐNEK KERESNIE KELL ──────────────────────────────────────
# Minden pont egy VALÓDI hiba emléke, amit egyszer már meg kellett találni.
# Ha új fajta hibát találsz, írd ide hozzá egy sorral.
ELLENORZO_LISTA = """
1. JÓ VÁLASZT KIJAVÍTOTT. A gyerek helyeset mondott, a tanár mégis
   "majdnem jó"-nak vagy hibásnak minősítette. Az összevont és a teljes alak
   EGYFORMÁN HELYES (isn't = is not, don't = do not). Chatben a kisbetű és a
   hiányzó vessző NEM hiba.
2. ROSSZ SORREND — CSAK NYELVTAN ÉS FOGALOM. Olyan NYELVTANI SZERKEZETET vagy
   FOGALMAT használt vagy tanított, aminek az előfeltételét még nem vették.
   Például "there is / there are" a létige előtt, vagy Perfekt akkor, amikor
   még csak a sein/haben múlt ideje van soron.
   FIGYELEM: ÚJ SZÓ TANÍTÁSA NEM HIBA. A tantervi lista a nyelvtan sorrendjét
   adja, nem a megengedett szavak teljes listáját. Ha a tanár a témához illő
   új szót tanít, az RENDBEN VAN — ne jelezd.
3. TÉNYBELI HIBA. Bármely tantárgyban: rossz évszám, rossz képlet, rossz
   fogalom, rossz tudós, rossz mértékegység, rossz fordítás. Ezt KÜLÖN
   figyeld: a történelem, fizika, kémia, biológia hibáit senki más nem szűri.
4. ÍGÉRT, DE HIÁNYZÓ DOLOG. "Nézd meg az ábrát", "itt egy kép", "lent
   látod" — de semmi nincs ott.
5. MEGVÁLASZOLHATATLAN KÉRDÉS. Választós kérdést tesz fel, de nincs mihez
   választani, VAGY egyik felkínált válasz sem helyes.
6. LERAGADT. Ugyanazt kérdezi újra, vagy csak dicsér és nem halad tovább.
   Egy frissen tanult szó VISSZAKÉRDEZÉSE NEM leragadás — az gyakorlás.
   Csak akkor jelezd, ha HÁROMSZOR is ugyanoda tér vissza előrelépés nélkül.
7. A KÉRDÉSBEN OTT A VÁLASZ. A gyerek a kérdés szövegéből kimásolhatja a
   megoldást. FIGYELEM: az alábbi szöveg már úgy szerepel, AHOGY A GYEREK
   LÁTJA. Ha egy választós kérdésnél csak az idegen szavak látszanak, a
   magyar megfelelőjük nem — az RENDBEN VAN, az egy rendes feladat.
8. MAGYARTALAN VAGY IDEGENSZERŰ MONDAT. Rossz ragozás, tükörfordítás,
   idegen szórend, hibás toldalék.
9. ÉLETKORHOZ NEM ILLŐ. Egy hatévesnek túl hosszú, túl elvont, vagy olyan
   szót használ, amit nem érthet.
10. NYELVET VÁLTOTT. Magyar órán idegen nyelvre váltott, vagy fordítva
    (idegennyelv-órán a célnyelvi rész kivételével).
11. NEM ANNYI, AMENNYIT MONDOTT. "Most két új szót tanulunk", aztán hármat
    sorol fel. Vagy "három feladat jön", és kettő jön.
12. TECHNIKAI SZEMÉT A KÉPERNYŐN. Olyasmi látszik, ami a programnak szólt,
    nem a gyereknek: <VOCAB>, <FL>, </FL>, <ABRA>, félbehagyott tag,
    kapcsos zárójel, JSON-részlet. Ez MINDIG hiba, akármilyen apró.
"""


def _kliens(idokorlat: float = 90.0):
    # A kulcsot MEGTISZTÍTJUK: a másolás gyakran hoz magával sortörést vagy
    # szóközt, és attól a kérés fejléce hibás lesz — a könyvtár pedig ezt
    # félrevezetően "Connection error" néven jelenti.
    kulcs = (os.environ.get("OPENAI_API_KEY")
             or os.environ.get("OPENAI_KEY") or "").strip().strip("'\"")
    if not kulcs:
        print("Nincs OPENAI_API_KEY a környezetben.")
        print('PowerShellben:  $env:OPENAI_API_KEY = "sk-..."')
        sys.exit(1)
    from openai import OpenAI
    return OpenAI(api_key=kulcs, timeout=idokorlat, max_retries=2)


def _valaszol(kliens, modell: str, uzenetek: list[dict], **extra) -> str:
    valasz = kliens.chat.completions.create(
        model=modell, messages=uzenetek, **extra)
    return (valasz.choices[0].message.content or "").strip()


def _json_kibont(szoveg: str) -> dict:
    """A modell néha ```json blokkba csomagolja. Onnan is kiszedjük."""
    szoveg = (szoveg or "").strip()
    if szoveg.startswith("```"):
        szoveg = szoveg.split("```")[1]
        if szoveg.lstrip().lower().startswith("json"):
            szoveg = szoveg.lstrip()[4:]
    eleje, vege = szoveg.find("{"), szoveg.rfind("}")
    if eleje >= 0 and vege > eleje:
        szoveg = szoveg[eleje:vege + 1]
    return json.loads(szoveg)


def _temakor(tantargy_fajl: str, evfolyam: int, nyelv: str | None):
    """Egy VALÓDI témakör a tantervből, a katalógus első eleme."""
    try:
        # UGYANAZ az út, amit a chat használ – nem külön betöltő, hogy ne
        # egy másik tananyagot teszteljünk, mint amit a gyerek kap.
        adat = app._chat_load_curriculum(
            tantargy_fajl, evfolyam, language=nyelv)
    except Exception:
        adat = None
    if not adat:
        return None, None
    katalogus = adat.get("topic_catalog") or []
    if not katalogus:
        return None, None
    return adat, katalogus[0]


def _tanari_prompt(gyerek: dict, tantargy: str, nyelv: str | None,
                   adat: dict, temakor: dict) -> str:
    """A VALÓDI rendszerprompt – ugyanaz, amit a gyerek kap élesben.

    A promptépítő a Flask kéréskörnyezetéből olvassa ki, MELYIK TANTERV aktív
    (g.lang). Kérés nélkül futtatva elszállna, ezért itt nyitunk neki egyet, és
    magyarra állítjuk. A spanyol oldalt külön kellene így tesztelni.
    """
    from flask import g as _g
    with app.app.test_request_context():
        _g.lang = "hu"
        return _tanari_prompt_belul(gyerek, tantargy, nyelv, adat, temakor)


def _tanari_prompt_belul(gyerek: dict, tantargy: str, nyelv: str | None,
                         adat: dict, temakor: dict) -> str:
    prompt = app._build_chat_system_prompt(
        gyerek,
        subject_label=tantargy,
        current_topic=temakor["name"],
        curriculum_json_content=adat.get("content", ""),
        completed_topics=[],
        level=1,
        is_foreign_language=bool(nyelv),
        teaching_language=nyelv,
        szokincs=temakor.get("szokincs"),
        spiralis=bool(adat.get("spiralis")),
    )
    prompt += app._topic_teaching_prompt_block(temakor, es_curriculum=False)
    return prompt


def _gepi_ellenorzes(szoveg: str) -> list[str]:
    """Amit GÉPPEL tudunk – ez nem vélemény, hanem tény."""
    talalatok: list[str] = []
    try:
        _, naplo = szamellenor.chat_ellenoriz(szoveg)
        talalatok.extend(f"[számtan] {sor}" for sor in naplo)
    except Exception as hiba:
        talalatok.append(f"[számtan] a vizsgálat elszállt: {hiba}")
    try:
        kimondva = hang.kiejtes(szoveg, "hu")
        # Ami SZÁMJEGY maradt a felolvasandó szövegben, azt a hangmotor
        # találgatja. A hang.py-nak mindent szóvá kellene írnia.
        import re
        maradek = re.findall(r"(?<![\w:/,.-])\d{1,6}(?![\w:/,.-])", kimondva)
        if maradek:
            talalatok.append(
                f"[felolvasás] számjegy maradt a kimondandó szövegben: "
                f"{maradek[:5]} — a hangmotor ezt találgatja")
    except Exception as hiba:
        talalatok.append(f"[felolvasás] a vizsgálat elszállt: {hiba}")
    return talalatok


def _ora(kliens, gyerek_adat, tantargy_fajl, cimke, evfolyam, nyelv,
         fordulok, naplo_ki):
    nev, kor, jellem = gyerek_adat
    adat, temakor = _temakor(tantargy_fajl, evfolyam, nyelv)
    if not temakor:
        return None

    # A gyerek-adatlap ugyanolyan alakú, mint az adatbázisban: az évfolyamot a
    # promptépítő a grade_hu mezőből olvassa, nem a "grade"-ből. Enélkül minden
    # órát elsősnek hitt volna, és a teszt hamis képet adott volna.
    gyerek = {"name": nev, "age": kor, "grade": evfolyam,
              "grade_hu": evfolyam, "grade_es": evfolyam}
    rendszer = _tanari_prompt(gyerek, cimke, nyelv, adat, temakor)

    gyerek_rendszer = (
        f"Egy {kor} éves magyar gyereket játszol, akit {nev}-nek hívnak. "
        f"{jellem}\n"
        f"Épp {cimke} órád van"
        + (f" ({nyelv})" if nyelv else "")
        + f", a téma: {temakor['name']}.\n"
        "Úgy válaszolj, ahogy EGY GYEREK válaszolna: rövid mondat, néha hiba, "
        "néha kérdés vissza. SOHA ne lépj ki a szerepből, ne magyarázd, hogy "
        "mit csinálsz, csak mondd, amit a gyerek mondana. Legfeljebb két mondat."
    )

    tortenet: list[dict] = []
    latott: list[str] = []          # amit a gyerek TÉNYLEG lát
    gyerek_tortenet: list[dict] = []
    gepi: list[str] = []

    # Az első lépést a tanár teszi, ahogy élesben is.
    gyerek_uzenet = "Szia! Kezdhetjük?"
    for _ in range(fordulok):
        uzenetek = ([{"role": "system", "content": rendszer}] + tortenet
                    + [{"role": "user", "content": gyerek_uzenet}])
        try:
            tanar_valasz = _valaszol(kliens, TANAR_MODELL, uzenetek,
                                     reasoning_effort="low")
        except Exception as hiba:
            tanar_valasz = f"[A TANÁR VÁLASZA ELSZÁLLT: {hiba}]"
            print(f"      ! a TANÁR válasza sem ment: "
                  f"{type(hiba).__name__}: {str(hiba)[:120]}", flush=True)
        tortenet.append({"role": "user", "content": gyerek_uzenet})
        tortenet.append({"role": "assistant", "content": tanar_valasz})
        gepi.extend(_gepi_ellenorzes(tanar_valasz))
        # AMIT A GYEREK LÁT — a jelölők feldolgozása után. Az ellenőrző EZT
        # kapja, nem a nyerset: az első futásnál a nyers <VOCAB>magyar=idegen</VOCAB>
        # párokat látva azt hitte, a válasz másolható a kérdésből, holott a
        # gyerek a magyar megfelelőt sosem látja.
        try:
            latott.append(app._parse_chat_markers(tanar_valasz)[0].strip())
        except Exception:
            latott.append(tanar_valasz)

        gyerek_tortenet.append({"role": "user", "content": tanar_valasz})
        try:
            gyerek_uzenet = _valaszol(
                kliens, GYEREK_MODELL,
                [{"role": "system", "content": gyerek_rendszer}] + gyerek_tortenet,
                reasoning_effort="low")
        except Exception:
            break
        gyerek_tortenet.append({"role": "assistant", "content": gyerek_uzenet})

    # A NAPLÓBA a nyers megy (hogy lásd a jelölőket is), az ELLENŐRZŐNEK a
    # megtisztított – az a valóság, amivel a gyerek szembesül.
    beszelgetes = "\n\n".join(
        ("GYEREK: " if m["role"] == "user" else "TANÁR: ") + m["content"]
        for m in tortenet)
    gyerek_uzenetek = [m["content"] for m in tortenet if m["role"] == "user"]
    sorok: list[str] = []
    for i_forduló, gy in enumerate(gyerek_uzenetek):
        sorok.append("GYEREK: " + gy)
        if i_forduló < len(latott):
            sorok.append("TANÁR: " + latott[i_forduló])
    beszelgetes_latott = "\n\n".join(sorok)

    sorrend = temakor.get("nyelvtan") or []
    sorrend_szoveg = ("\nA TANTERV SORRENDJE ehhez a témakörhöz:\n"
                      + "\n".join(f"  {i}. {p}" for i, p in enumerate(sorrend, 1))
                      ) if sorrend else ""

    ellenor_keres = (
        f"Egy {kor} éves gyerek {cimke} óráját olvasod"
        + (f" ({nyelv} nyelv)" if nyelv else "")
        + f". Témakör: {temakor['name']}.{sorrend_szoveg}\n\n"
        f"Keresd meg a TANÁR hibáit ez alapján:\n{ELLENORZO_LISTA}\n"
        "Adj vissza egy json választ ebben az alakban: "
        "{\"talalatok\": [{\"pont\": <1-12>, "
        "\"idezet\": \"<a tanár szó szerinti mondata>\", "
        "\"miert\": \"<egy mondat magyarul>\", "
        "\"biztos\": \"biztos\"|\"gyanus\"}]}\n"
        "INKÁBB JELEZZ, MINT HOGY KIHAGYJ: ha bizonytalan vagy, a "
        "\"biztos\" mező legyen \"gyanus\", de akkor is add vissza. "
        "Ha tényleg nincs semmi, üres listát adj.\n"
        "Az IDÉZET legyen SZÓ SZERINTI, hogy meg lehessen keresni.\n\n"
        f"AZ ÓRA (pontosan úgy, AHOGY A GYEREK LÁTTA):\n{beszelgetes_latott}"
    )
    # AZ ÁTNÉZÉS. Ha ez elbukik, azt HANGOSAN kell mondani: az első futásnál
    # mindhárom óra "0 hiba"-t mutatott, holott az ellenőrző el sem indult.
    # A néma nulla rosszabb, mint a hibaüzenet: azt hiszed, rendben van.
    talalatok: list = []
    ellenor_hiba = ""
    # HÁROM PRÓBÁLKOZÁS, egyre egyszerűbb. A "json_object" formátumot nem
    # minden modell fogadja el, ezért van a formátum nélküli tartalék: ott a
    # kérésben kérjük a JSON-t. A hiba TÍPUSÁT is kiírjuk – a "Connection
    # error" és a "model_not_found" teljesen mást jelent.
    probak = [(ELLENOR_MODELL, True), (ELLENOR_MODELL, False),
              (TANAR_MODELL, False)]
    for modell, json_mod in probak:
        extra = {"response_format": {"type": "json_object"}} if json_mod else {}
        keres = ellenor_keres if json_mod else (
            ellenor_keres + "\n\nCSAK a JSON-t add vissza, semmi mást.")
        try:
            nyers = _valaszol(kliens, modell,
                              [{"role": "user", "content": keres}], **extra)
            talalatok = _json_kibont(nyers).get("talalatok", [])
            ellenor_hiba = ""
            break
        except Exception as hiba:
            ellenor_hiba = (f"{modell}"
                            + (" +json" if json_mod else " (json nélkül)")
                            + f" → {type(hiba).__name__}: {str(hiba)[:160]}")
            print(f"      ! {ellenor_hiba}", flush=True)

    naplo_ki.write(f"\n\n{'=' * 70}\n{cimke}"
                   + (f" – {nyelv}" if nyelv else "")
                   + f" · {evfolyam}. osztály · {nev} ({kor} éves)\n"
                   + f"Témakör: {temakor['name']}\n{'=' * 70}\n{beszelgetes}\n")

    return {"tantargy": cimke, "nyelv": nyelv, "evfolyam": evfolyam,
            "gyerek": nev, "temakor": temakor["name"],
            "talalatok": talalatok, "gepi": gepi,
            "ellenor_hiba": ellenor_hiba}


def _kulcs_vizsgalat() -> None:
    """A kulcs ALAKJA. Nem írjuk ki, csak azt, hogy jól néz-e ki.

    MIÉRT: ha a kulcsban benne maradt egy sortörés, egy szóköz vagy egy
    „okos” idézőjel (a Word és a böngésző szeret ilyet beszúrni), akkor a
    kérés fejléce hibás lesz, és a könyvtár ezt CONNECTION ERROR néven
    jelenti — pedig valójában a kulcs karaktereivel van baj.
    """
    k = os.environ.get("OPENAI_API_KEY") or os.environ.get("OPENAI_KEY") or ""
    print("── A kulcs alakja ──")
    print(f"  hossz: {len(k)} karakter")
    print(f"  eleje: {k[:7]}…   vége: …{k[-4:] if len(k) > 4 else ''}")
    bajok = []
    if k != k.strip():
        bajok.append("szóköz vagy sortörés van az elején/végén")
    if any(c in k for c in "\r\n\t"):
        bajok.append("SORTÖRÉS vagy tabulátor van BENNE")
    if any(ord(c) > 127 for c in k):
        rossz = [c for c in k if ord(c) > 127][:3]
        bajok.append(f"nem angol karakter van benne: {rossz}")
    if k.startswith(("'", '"', "\u201c", "\u201e")):
        bajok.append("idézőjellel kezdődik – az idézőjel nem tartozik a kulcshoz")
    if not k.startswith("sk-"):
        bajok.append("nem 'sk-'-val kezdődik")
    if bajok:
        for b in bajok:
            print(f"  BAJ: {b}")
        print("  (Ez a program magától megtisztítja, tehát a teszt működni fog.")
        print("   DE ha valaha helyben indítod a Flask appot, az NEM tisztítja")
        print("   meg — ott ugyanígy 'Connection error' lenne. Érdemes újra")
        print("   beállítani a kulcsot egyetlen sorban, sortörés nélkül.)")
    else:
        print("  Alakra rendben.")
    print()


def _halozat_proba() -> None:
    """Elérhető-e egyáltalán az OpenAI – kulcs NÉLKÜL.

    Ha ez is elbukik, akkor nem a kulcs a baj, hanem a gép nem jut ki:
    tűzfal, vírusirtó TLS-vizsgálata, VPN vagy szolgáltatói hiba.
    """
    print("── Kijut-e egyáltalán a gép az OpenAI-hoz? ──")
    try:
        try:
            import httpx
            allapot = httpx.get("https://api.openai.com/v1/models",
                                timeout=20).status_code
        except ImportError:
            # httpx nélkül is meg tudjuk nézni – a lényeg, hogy KIJUT-E.
            import urllib.error
            import urllib.request
            try:
                with urllib.request.urlopen(
                        "https://api.openai.com/v1/models", timeout=20) as v:
                    allapot = v.status
            except urllib.error.HTTPError as v:
                allapot = v.code
        print(f"  A szerver válaszolt. HTTP {allapot} "
              "(a 401 itt JÓ jel: elértük, csak nincs kulcs a kérésben.)")
    except Exception as hiba:
        print(f"  NEM JUT KI: {type(hiba).__name__}: {str(hiba)[:200]}")
        okok = []
        h = hiba
        while getattr(h, "__cause__", None):
            h = h.__cause__
            okok.append(f"{type(h).__name__}: {str(h)[:160]}")
        for o in okok:
            print(f"     ↳ {o}")
    print()


def _onproba() -> int:
    """Megmondja, PONTOSAN hol akad el a dolog."""
    _kulcs_vizsgalat()
    _halozat_proba()

    kliens = _kliens(idokorlat=60.0)
    hosszu = "Ismételd meg ezt a szót: alma.\n" + ("x" * 30000)
    probak = [
        ("a tanár modellje", TANAR_MODELL,
         [{"role": "user", "content": "Mondd azt: szia"}], {}),
        ("az ellenőrző modellje", ELLENOR_MODELL,
         [{"role": "user", "content": "Mondd azt: szia"}], {}),
        # A KÉRÉSBEN SZEREPELNIE KELL a "json" szónak, különben az API
        # visszautasítja a json_object formátumot. Ez a próba korábban
        # emiatt bukott el – nem a modellel volt baj, hanem a kérdésemmel.
        ("az ellenőrző + JSON formátum", ELLENOR_MODELL,
         [{"role": "user",
           "content": 'Adj vissza egy json választ: {"ok": true}'}],
         {"response_format": {"type": "json_object"}}),
        ("hosszú kérés (30 ezer karakter)", ELLENOR_MODELL,
         [{"role": "user", "content": hosszu}], {}),
    ]
    print("── Hívások ──")
    baj = 0
    for cimke, modell, uzenet, extra in probak:
        print(f"  {cimke} ({modell}) …", end=" ", flush=True)
        try:
            v = _valaszol(kliens, modell, uzenet, **extra)
            print(f"OK — „{v[:40]}”")
        except Exception as hiba:
            baj += 1
            print(f"HIBA — {type(hiba).__name__}: {str(hiba)[:150]}")
            # A VALÓDI ok szinte mindig itt van elrejtve.
            h = hiba
            while getattr(h, "__cause__", None):
                h = h.__cause__
                print(f"     ↳ a valódi ok: {type(h).__name__}: {str(h)[:200]}")
    print()
    if baj:
        print("Másold be nekem a TELJES kimenetet, a kulcs alakjától kezdve.")
    else:
        print("Minden hívás átment. Indíthatod a tesztet.")
    return 1 if baj else 0


def main() -> int:
    p = argparse.ArgumentParser(
        description="Lejátszik órákat, és megnézi, hibázik-e a tanár.")
    p.add_argument("--gyors", action="store_true",
                   help="3 óra, 4 forduló – olcsó próba")
    p.add_argument("--fordulo", type=int, default=6,
                   help="hány oda-vissza egy órában")
    p.add_argument("--ora", type=int, default=8,
                   help="hány órát játsszon le")
    p.add_argument("--evfolyam", type=int, action="append",
                   help="csak ezt az évfolyamot (többször is megadható)")
    p.add_argument("--tantargy",
                   help="szűrés a tantárgy nevére, részlet is elég")
    p.add_argument("--proba", action="store_true",
                   help="csak négy apró hívás: hol akad el? (majdnem ingyen)")
    p.add_argument("--mind", action="store_true",
                   help="MINDEN tantárgy és évfolyam – drága, de teljes")
    a = p.parse_args()

    if a.proba:
        return _onproba()
    if a.gyors:
        a.ora, a.fordulo = 3, 4

    evfolyamok = a.evfolyam or [1, 2, 3, 4, 5, 6, 7, 8]
    matrix = _tantargy_matrix(evfolyamok)
    if a.tantargy:
        keres = a.tantargy.lower()
        matrix = [m for m in matrix if keres in (m[1] or "").lower()]
    if not matrix:
        print("Nincs ilyen tantárgy a tantervben. Amik vannak:")
        for _, cimke, evf, ny in _tantargy_matrix(evfolyamok)[:40]:
            print(f"  {evf}. o.  {cimke}" + (f" ({ny})" if ny else ""))
        return 1

    random.seed(12345)          # ugyanaz a keverés minden futásnál
    random.shuffle(matrix)
    if not a.mind:
        matrix = matrix[: a.ora]

    ido = datetime.now().strftime("%Y-%m-%d %H:%M")
    kliens = _kliens()
    eredmenyek: list[dict] = []
    print(f"{len(matrix)} óra lejátszása, óránként {a.fordulo} forduló.\n")

    with open("tanar_teszt_beszelgetesek.txt", "w", encoding="utf-8") as naplo:
        naplo.write(f"TutorIA – lejátszott órák, {ido}\n")
        for i, (fajl, cimke, evf, nyelv) in enumerate(matrix, 1):
            gyerek = GYEREKEK[i % len(GYEREKEK)]
            nev, jellem = gyerek
            kor = evf + 5
            jel = f"{cimke}" + (f" ({nyelv})" if nyelv else "")
            print(f"[{i}/{len(matrix)}] {evf}. o. {jel} …", flush=True)
            try:
                e = _ora(kliens, (nev, kor, jellem), fajl, cimke, evf, nyelv,
                         a.fordulo, naplo)
            except KeyboardInterrupt:
                print("\nMegszakítva – az eddigiekről készül jelentés.")
                break
            except Exception:
                traceback.print_exc()
                e = None
            if e is None:
                print("      (nincs tananyag ehhez, kihagyva)")
                continue
            eredmenyek.append(e)
            biztos = sum(1 for t in e["talalatok"]
                         if t.get("biztos") == "biztos")
            if e.get("ellenor_hiba"):
                print("      NEM NÉZTE ÁT SENKI – a nulla itt nem jelent jót")
            else:
                print(f"      {biztos} biztos, "
                      f"{len(e['talalatok']) - biztos} gyanús, "
                      f"{len(e['gepi'])} gépi")

    if not eredmenyek:
        print("\nEgy órát sem sikerült lejátszani.")
        return 1
    _jelentes(eredmenyek, ido)
    print("\nKész. Olvasd el: tanar_teszt_jelentes.md")
    print("A teljes beszélgetések: tanar_teszt_beszelgetesek.txt")
    return 0


def _jelentes(eredmenyek: list[dict], ido: str) -> None:
    biztos = sum(1 for e in eredmenyek for t in e["talalatok"]
                 if t.get("biztos") == "biztos")
    gyanus = sum(1 for e in eredmenyek for t in e["talalatok"]
                 if t.get("biztos") != "biztos")
    gepi_db = sum(len(e["gepi"]) for e in eredmenyek)

    atnezetlen = [e for e in eredmenyek if e.get("ellenor_hiba")]
    s = [f"# TutorIA – tanári minőség, {ido}\n"]
    if atnezetlen:
        s.append(f"> **FIGYELEM: {len(atnezetlen)} órát NEM NÉZETT ÁT senki** — "
                 "az átnézés elszállt. Az alábbi nullák NEM azt jelentik, hogy "
                 "hibátlan.\n>\n"
                 f"> A hiba: `{atnezetlen[0]['ellenor_hiba']}`\n>\n"
                 "> Ha a modell neve a baj, írd át az ELLENOR_MODELL sort a "
                 "tanar_teszt.py tetején.\n")
    s += [
         f"Lejátszott órák: **{len(eredmenyek)}**  ",
         f"Gépi találat (számtan, felolvasás — ez NEM vélemény): **{gepi_db}**  ",
         f"Az ellenőrző szerint biztos hiba: **{biztos}**  ",
         f"Az ellenőrző szerint gyanús: **{gyanus}**\n",
         "> Az ellenőrző maga is egy AI. Nem talál meg mindent, és néha",
         "> olyat is megjelöl, ami rendben van. A lista nem ítélet — nézd át.",
         "> A GÉPI találatok viszont tények, azokat nem kell mérlegelni.\n"]

    if gepi_db:
        s.append("\n## Gépi találatok\n")
        for e in eredmenyek:
            for g in e["gepi"]:
                s.append(f"- **{e['tantargy']}** ({e['evfolyam']}. o.): {g}")

    s.append("\n## Amit az ellenőrző talált\n")
    ures = True
    for pont in range(1, 13):
        sorok = [(e, t) for e in eredmenyek for t in e["talalatok"]
                 if t.get("pont") == pont]
        if not sorok:
            continue
        ures = False
        cim = ELLENORZO_LISTA.strip().split("\n")
        fejlec = next((c for c in cim if c.strip().startswith(f"{pont}.")),
                      f"{pont}.")
        s.append(f"\n### {fejlec.strip()}\n")
        for e, t in sorok:
            jel = "**BIZTOS**" if t.get("biztos") == "biztos" else "gyanús"
            s.append(f"- {jel} — {e['tantargy']} "
                     + (f"({e['nyelv']}) " if e["nyelv"] else "")
                     + f"{e['evfolyam']}. o., „{e['temakor']}”")
            s.append(f"  - A tanár ezt mondta: „{t.get('idezet','')}”")
            s.append(f"  - Miért baj: {t.get('miert','')}")
    if ures:
        s.append("Semmit. Ez jó jel, de nem bizonyíték — futtasd több órával.\n")

    s.append("\n---\n\nA teljes beszélgetések: `tanar_teszt_beszelgetesek.txt`\n")
    with open("tanar_teszt_jelentes.md", "w", encoding="utf-8") as f:
        f.write("\n".join(s))


if __name__ == "__main__":
    sys.exit(main())
