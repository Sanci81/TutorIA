# -*- coding: utf-8 -*-
"""TutorIA – kiejtés-értékelés az Azure Speech szolgáltatással.

MIT CSINÁL
    Elküldi a gyerek felvételét és azt a mondatot, aminek hangzania kellett
    volna. Az Azure visszaadja, hogy szavanként mennyire pontos a kiejtés,
    mennyire folyamatos a beszéd, és hogy a gyerek kihagyott-e szavakat.

MIÉRT KELL
    Ma a program dicséri a gyereket, de senki nem mondja meg, hogy a kiejtése
    tényleg jó-e. Ettől lesz a nyelvóra nyelvtanulás, és nem beszélgetés.

AMI MÉG NEM BIZTOS
    Az Azure kiejtés-értékelése 33 nyelven érhető el. A dokumentációból nem
    tudtam megbízhatóan kiolvasni, hogy a MAGYAR köztük van-e — a spanyol és
    az angol biztosan igen. Ezért van a `probal()` függvény: egyetlen valódi
    hívással eldönti, mielőtt bármit ráépítenénk.

HANGFORMÁTUM
    Az Azure rövid-hang végpontja 16 kHz-es, mono, PCM WAV-ot vár. A böngésző
    webm/opus-t vesz fel, ezért az ÁTALAKÍTÁS A BÖNGÉSZŐBEN történik (lásd a
    kiejtes_proba.html-t). Így nincs szükség ffmpegre a szerveren, és a
    Railway-telepítés érintetlen marad.
"""

from __future__ import annotations

import base64
import json
import os
import urllib.error
import urllib.request

# Az Azure legfeljebb 30 másodpercnyi hangot értékel kiejtésre.
MAX_MASODPERC = 30

# Egy gyereknél a 100-as skála a beszédesebb: "82 pont" érthető, a "4,1 / 5"
# kevésbé. A szó szintű bontás kell, hogy megmondhassuk, MELYIK szó nem ment.
_BEALLITAS = {
    "GradingSystem": "HundredMark",
    "Granularity": "Word",
    "Dimension": "Comprehensive",
    # Igaz esetén jelzi, ha a gyerek kihagyott vagy betoldott egy szót –
    # nem csak azt, hogy a kimondottak hogy szóltak.
    "EnableMiscue": "True",
    # Hangsúly, hanglejtés, tempó. Ez az, amitől egy mondat "magyarosan"
    # vagy "idegenül" hangzik, még ha minden hang jó is.
    "EnableProsodyAssessment": "True",
}


class NincsBeallitva(RuntimeError):
    """Nincs Azure kulcs vagy régió a környezeti változókban."""


def _kulcs_es_regio() -> tuple[str, str]:
    kulcs = (os.environ.get("AZURE_SPEECH_KEY") or "").strip()
    regio = (os.environ.get("AZURE_SPEECH_REGION") or "").strip().lower()
    if not kulcs or not regio:
        raise NincsBeallitva(
            "AZURE_SPEECH_KEY vagy AZURE_SPEECH_REGION hiányzik")
    return kulcs, regio


def ertekel(wav_bytes: bytes, mondat: str, *, nyelv: str = "hu-HU",
            idokorlat: float = 25.0) -> dict:
    """A felvétel kiejtésének értékelése. Nyers Azure-válasz szótárként.

    wav_bytes  – 16 kHz, mono, PCM WAV
    mondat     – amit a gyereknek mondania kellett
    nyelv      – "hu-HU", "es-ES", "en-US" …
    """
    if not wav_bytes:
        raise ValueError("üres hangfelvétel")
    if not (mondat or "").strip():
        raise ValueError("nincs viszonyítási mondat")

    kulcs, regio = _kulcs_es_regio()

    fejlec_json = json.dumps({"ReferenceText": mondat.strip(), **_BEALLITAS},
                             ensure_ascii=False)
    fejlec = base64.b64encode(fejlec_json.encode("utf-8")).decode("ascii")

    url = (f"https://{regio}.stt.speech.microsoft.com"
           f"/speech/recognition/conversation/cognitiveservices/v1"
           f"?language={nyelv}")
    keres = urllib.request.Request(
        url,
        data=wav_bytes,
        headers={
            "Ocp-Apim-Subscription-Key": kulcs,
            "Content-Type": "audio/wav; codecs=audio/pcm; samplerate=16000",
            "Pronunciation-Assessment": fejlec,
            "Accept": "application/json",
            "User-Agent": "TutorIA",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(keres, timeout=idokorlat) as valasz:
            nyers = valasz.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as hiba:
        reszlet = hiba.read().decode("utf-8", "replace")[:400]
        raise RuntimeError(f"Azure {hiba.code}: {reszlet}") from hiba
    return json.loads(nyers)


def egyszerusit(valasz: dict) -> dict:
    """Az Azure válaszából az, amit egy gyereknek meg lehet mutatni.

    Visszaad: {"felismert", "pontszamok": {...}, "szavak": [{szo, pont, hiba}]}
    Ha a válaszban nincs értékelés (nem támogatott nyelv, néma felvétel),
    a "pontszamok" üres marad – a hívó ebből tudja, hogy nincs mit mutatni.
    """
    ki: dict = {"felismert": "", "pontszamok": {}, "szavak": [],
                "allapot": valasz.get("RecognitionStatus", "")}
    nbest = valasz.get("NBest") or []
    if not nbest:
        return ki
    elso = nbest[0]
    ki["felismert"] = elso.get("Display") or elso.get("Lexical") or ""

    # Az Azure kétféleképpen adhatja vissza: külön "PronunciationAssessment"
    # blokkban, vagy a régebbi elrendezésben magukban a mezőkben.
    ertek = elso.get("PronunciationAssessment") or {}
    for kulcs, nev in (("AccuracyScore", "pontossag"),
                       ("FluencyScore", "folyamatossag"),
                       ("CompletenessScore", "teljesseg"),
                       ("ProsodyScore", "hanglejtes"),
                       ("PronScore", "osszesitett")):
        v = ertek.get(kulcs, elso.get(kulcs))
        if isinstance(v, (int, float)):
            ki["pontszamok"][nev] = round(float(v))

    for szo in elso.get("Words") or []:
        w = szo.get("PronunciationAssessment") or {}
        ki["szavak"].append({
            "szo": szo.get("Word", ""),
            "pont": round(float(w.get("AccuracyScore", 0) or 0)),
            # None / "None" / "Mispronunciation" / "Omission" / "Insertion"
            "hiba": (w.get("ErrorType") or "None"),
        })
    return ki


def probal(wav_bytes: bytes, mondat: str, nyelv: str) -> dict:
    """Egyetlen próbahívás: MŰKÖDIK-E ez a nyelv egyáltalán.

    Sosem dob kivételt – a hibát is adatként adja vissza, hogy a
    diagnosztikai oldal meg tudja mutatni.
    """
    try:
        nyers = ertekel(wav_bytes, mondat, nyelv=nyelv)
    except NincsBeallitva as hiba:
        return {"ok": False, "ok_szoveg": "nincs_beallitva", "uzenet": str(hiba)}
    except Exception as hiba:                      # hálózat, HTTP, JSON
        return {"ok": False, "ok_szoveg": "hiba", "uzenet": str(hiba)[:400]}

    egyszeru = egyszerusit(nyers)
    tamogatott = bool(egyszeru["pontszamok"])
    return {
        "ok": tamogatott,
        "ok_szoveg": "mukodik" if tamogatott else "nincs_ertekeles",
        "uzenet": ("" if tamogatott else
                   "Az Azure válaszolt, de kiejtés-pontszám nélkül – ezt a "
                   "nyelvet valószínűleg nem támogatja."),
        "eredmeny": egyszeru,
        "nyers": nyers,
    }
