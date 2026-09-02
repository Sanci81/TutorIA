"""Tantárgy-listák betöltése hivatalos forrásokból (HU / ES).

Magyarország: kerettanterv.oh.gov.hu (tükör: oktatas.hu)
Spanyolország: educagob.educacionfpydeportes.gob.es + autonóm közösség oldalak

Az eredmény fájl-cache-be kerül; sikertelen lekérés esetén fallback lista.
"""

from __future__ import annotations

import json
import logging
import os
import re
import ssl
import unicodedata
import urllib.error
import urllib.request
from datetime import datetime, timezone
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

# ---------------------------------------------------------------------------
# Konfiguráció
# ---------------------------------------------------------------------------

CACHE_DIR = Path(os.environ.get("CURRICULUM_CACHE_DIR", Path(__file__).parent / "cache" / "curriculum"))
CACHE_TTL_HOURS = int(os.environ.get("CURRICULUM_CACHE_TTL_HOURS", "168"))  # 7 nap

HU_BASE_URLS = (
    "https://kerettanterv.oh.gov.hu",
    "https://www.oktatas.hu",
)

ES_BASE_URL = "https://educagob.educacionfpydeportes.gob.es"
ES_AREAS_PATH = (
    "/curriculo/curriculo-lomloe/menu-curriculos-basicos/ed-primaria/areas/desarrollo-areas.html"
)
ES_COMMUNITIES_PATH = (
    "/curriculo/curriculo-lomloe/menu-curriculos-basicos/ed-primaria/curriculo-comunidades-autonomas.html"
)

USER_AGENT = "TutorIA/1.0 (education curriculum loader)"

logger = logging.getLogger(__name__)

_SSL_CTX = ssl.create_default_context()
_SSL_CTX.check_hostname = False
_SSL_CTX.verify_mode = ssl.CERT_NONE

# ---------------------------------------------------------------------------
# Magyar tantárgy-nevek (docx fájlnév -> megjelenített név)
# ---------------------------------------------------------------------------

_HU_DOCX_SUBJECTS: dict[str, str] = {
    "Magyar_nyelv_es_irodalom": "Magyar nyelv és irodalom",
    "Matematika": "Matematika",
    "Etika": "Etika",
    "Kornyezetismeret": "Környezetismeret",
    "elo_idegen_nyelv_A_egyben": "Idegen nyelv",
    "elo_idegen_nyelv_F_egyben": "Idegen nyelv",
    "elo_idegen_nyelv": "Idegen nyelv",
    "Enek-zene": "Ének-zene",
    "Vizualis_kultura": "Vizuális kultúra",
    "Technika_es_tervezes": "Technika és tervezés",
    "Digitalis_kultura": "Digitális kultúra",
    "Testneveles": "Testnevelés",
    "Tortenelem": "Történelem",
    "Allampolgari_ismeretek": "Állampolgári ismeretek",
    "Hon_es_nepismeret": "Hon- és népismeret",
    "Termeszettudomany_5_6": "Természettudomány",
    "Kemia": "Kémia",
    "Fizika": "Fizika",
    "Biologia": "Biológia",
    "Foldrajz": "Földrajz",
    "Drama_es_szinhaz": "Dráma és színház",
}

# Évfolyamonkénti szűrés a kerettanterv-sávokon belül (min, max)
_HU_GRADE_RULES_LOWER: dict[str, tuple[int, int]] = {
    "Környezetismeret": (3, 4),
    "Digitális kultúra": (3, 4),
    "Idegen nyelv": (1, 4),
    "Első élő idegen nyelv": (1, 4),
}

_HU_GRADE_RULES_UPPER: dict[str, tuple[int, int]] = {
    "Természettudomány": (5, 6),
    "Technika és tervezés": (5, 7),
    "Kémia": (7, 8),
    "Fizika": (7, 8),
    "Biológia": (7, 8),
    "Földrajz": (7, 8),
    "Dráma és színház": (5, 8),
    "Állampolgári ismeretek": (8, 8),
}

# Spirális tantárgyak — ezeknél a témakörök minden évben visszatérnek,
# NEM szabad szétosztani a sáv-blokkok témaköreit évfolyamok között.
_SPIRAL_SUBJECT_DISPLAY_NAMES: frozenset[str] = frozenset(
    {
        "Testnevelés",
        "Ének-zene",
        "Vizuális kultúra",
        "Etika",
        "Dráma és színház",
        "Közösségi nevelés",
        "Hon- és népismeret",
    }
)

_LOE_SPIRAL_SUBJECT_NAMES: frozenset[str] = frozenset(
    {
        "Educación Física",
        "Educación Artística",
        "Educación en Valores Cívicos y Éticos",
    }
)

# UI nyelv szerinti tantárgy-feliratok (value = tantervi név, label = UI nyelv)
_HU_SUBJECT_UI_ES: dict[str, str] = {
    "Magyar nyelv és irodalom": "Lengua y literatura húngaras",
    "Matematika": "Matemáticas",
    "Etika": "Ética",
    "Környezetismeret": "Conocimiento del medio",
    "Digitális kultúra": "Cultura digital",
    "Idegen nyelv": "Lengua extranjera",
    "Első élő idegen nyelv": "Lengua extranjera",
    "Ének-zene": "Educación musical",
    "Vizuális kultúra": "Educación plástica y visual",
    "Technika és tervezés": "Tecnología",
    "Testnevelés": "Educación física",
    "Történelem": "Historia",
    "Hon- és népismeret": "Patria y folklore",
    "Természettudomány": "Ciencias naturales",
    "Kémia": "Química",
    "Fizika": "Física",
    "Biológia": "Biología",
    "Földrajz": "Geografía",
    "Dráma és színház": "Teatro y drama",
    "Állampolgári ismeretek": "Educación cívica",
}

_ES_SUBJECT_UI_HU: dict[str, str] = {
    "Conocimiento del Medio Natural, Social y Cultural": "Környezetismeret",
    "Ciencias de la Naturaleza": "Természetismeret",
    "Ciencias Sociales": "Társadalomismeret",
    "Educación Artística": "Művészetek",
    "Educación Física": "Testnevelés",
    "Lengua Castellana y Literatura": "Spanyol nyelv és irodalom",
    "Lengua Extranjera": "Idegen nyelv",
    "Matemáticas": "Matematika",
    "Educación en Valores Cívicos y Éticos": "Polgári értékek",
    "Enseñanzas de religión": "Vallásoktatás",
    "Lengua Cooficial y Literatura (Catalán)": "Katalán nyelv és irodalom",
    "Lengua Cooficial y Literatura (Euskera)": "Baszk nyelv és irodalom",
    "Lengua Cooficial y Literatura (Galego)": "Galíciai nyelv és irodalom",
    "Lengua Cooficial y Literatura (Valenciano)": "Valenciai nyelv és irodalom",
}

# Spanyol tantárgynevek – HU profilban soha nem jelenhetnek meg
_SPANISH_SUBJECT_KEYS = frozenset(
    {
        "cienciasdelanaturaleza",
        "cienciassociales",
        "cienciasnaturales",
        "conocimientodelmedionaturalsocialycultural",
        "lenguacastellanayliteratura",
        "ensenanzasdereligion",
        "educacionartistica",
        "educacionfisica",
        "lenguaextranjera",
        "matematicas",
        "educacionenvalorescivicosyetico",
    }
)

# ES profil + HU UI: ezek a magyar fordítások csak spanyol UI-ban
_ES_ONLY_HU_UI_LABELS = frozenset(
    {
        "Spanyol nyelv és irodalom",
        "Vallásoktatás",
    }
)

_HU_CORE_SUBJECT = "Magyar nyelv és irodalom"

_HU_EXCLUDED_SUBJECT_KEYS = frozenset(
    {
        "kozossegieneveles",
        "kozossegineveles",
        "elsoeloidegennyelv",   # régi fájlnév, nem valódi tantárgy (→ Idegen nyelv)
    }
)

# Feladatgeneráláshoz: megjelenített név → JSON fájl tantárgy
_HU_SUBJECT_JSON_ALIASES: dict[str, tuple[str, ...]] = {
    "idegennyelv": ("eloidegennyelv",),
    "angol": ("eloidegennyelv", "angol"),
    "nemet": ("eloidegennyelv", "nemet"),
    "spanyol": ("spanyol",),
    "magyarnyelvesirodalom": ("magyarnyelvesirodalom",),
}

# HU 1–4: kizárólag hardcoded lista (NE fájlrendszer-ből építsd!)
_HU_1_4_SUBJECT_MAP: dict[str, str] = {
    "Magyar nyelv és irodalom": "Magyar_nyelv_es_irodalom_1_4.json",
    "Matematika": "Matematika_1_4.json",
    "Környezetismeret": "Kornyezetismeret_1_4.json",
    "Etika": "Etika_1_4.json",
    "Idegen nyelv": "Elo_idegen_nyelv_1_4.json",
    "Ének-zene": "Enek_zene_1_4.json",
    "Vizuális kultúra": "Vizualis_kultura_1_4.json",
    "Technika és tervezés": "Technika_es_tervezes_1_4.json",
    "Digitális kultúra": "Digitalis_kultura_1_4.json",
    "Testnevelés": "Testneveles_1_4.json",
}

ELO_IDEGEN_NYELV_1_4_FILE = "Elo_idegen_nyelv_1_4.json"
ELO_IDEGEN_NYELV_5_8_FILE = "elo_idegen_nyelv_5-8.json"
ELO_IDEGEN_NYELV_5_8_ALT = "elo_idegen_nyelv_5-8.json"
SPANYOL_1_4_FILE = "spanyol_1-4.json"
SPANYOL_5_8_FILE = "spanyol_5-8.json"
ANGOL_1_4_FILE = "angol_1-4.json"
ANGOL_5_8_FILE = "angol_5-8.json"
NEMET_1_4_FILE = "nemet_1-4.json"
NEMET_5_8_FILE = "nemet_5-8.json"

# Nyelvspecifikus fájlok — NEM önálló tantárgyak, kizárandók a tantárgylistából
_LANGUAGE_SPECIFIC_FILES: frozenset[str] = frozenset(
    {ANGOL_1_4_FILE, ANGOL_5_8_FILE, SPANYOL_1_4_FILE, SPANYOL_5_8_FILE,
     NEMET_1_4_FILE, NEMET_5_8_FILE}
)

# ── LOMLOE spanyol nemzeti tanterv (BOE-A-2022-3296) ──────────────────────
ES_LOE_DIR: Path = Path(__file__).parent / "es_kerettanterv"
ES_LOE_FILES: dict[str, str] = {
    "conocimiento": "es_LOMLOE_Conocimiento_1-6.json",
    "artistica": "es_LOMLOE_Artistica_1-6.json",
    "fisica": "es_LOMLOE_Fisica_1-6.json",
    "lengua": "es_LOMLOE_Lengua_1-6.json",
    "extranjera": "es_LOMLOE_Extranjera_1-6.json",
    "matematicas": "es_LOMLOE_Matematicas_1-6.json",
    "valores": "es_LOMLOE_Valores_5-6.json",
}

# Startup check: log whether LOE files are available
try:
    _LOE_MISSING = []
    if ES_LOE_DIR.is_dir():
        for fname in ES_LOE_FILES.values():
            if not (ES_LOE_DIR / fname).is_file():
                _LOE_MISSING.append(fname)
    else:
        _LOE_MISSING = list(ES_LOE_FILES.values())
    _LOE_AVAILABLE = len(_LOE_MISSING) == 0
    logger.warning(
        "LOMLOE startup: ES_LOE_DIR=%s EXISTS=%s ALL_PRESENT=%s MISSING=%s",
        str(ES_LOE_DIR),
        ES_LOE_DIR.is_dir(),
        _LOE_AVAILABLE,
        _LOE_MISSING,
    )
except Exception:
    _LOE_AVAILABLE = False
    logger.warning("LOMLOE startup: error checking ES_LOE_DIR", exc_info=True)

# LOMLOE spanyol tantárgynevek – UI megjelenítéshez
_ES_LOE_SUBJECT_LABELS: dict[str, str] = {
    "conocimiento": "Conocimiento del Medio",
    "artistica": "Educación Artística",
    "fisica": "Educación Física",
    "lengua": "Lengua Castellana y Literatura",
    "extranjera": "Lengua Extranjera",
    "matematicas": "Matemáticas",
    "valores": "Educación en Valores Cívicos y Éticos",
}

# Sablonokhoz: megengedett fájlnevek és címkék
HU_1_4_SUBJECT_NAMES: list[str] = list(_HU_1_4_SUBJECT_MAP.keys())
HU_1_4_SUBJECT_FILES: frozenset[str] = frozenset(_HU_1_4_SUBJECT_MAP.values())

# ── LOMLOE tanterv betöltése ────────────────────────────────────────────────

_loe_cache: dict[str, dict[str, Any]] = {}


def _load_loe_json(subject_key: str) -> dict[str, Any] | None:
    """Betölt egy LOMLOE JSON fájlt az es_kerettanterv könyvtárból."""
    if subject_key in _loe_cache:
        logger.warning("_load_loe_json CACHE HIT: key=%r", subject_key)
        return _loe_cache[subject_key]
    filename = ES_LOE_FILES.get(subject_key)
    if not filename:
        logger.warning("_load_loe_json FAIL: no filename for key=%r in ES_LOE_FILES=%r", subject_key, list(ES_LOE_FILES.keys()))
        return None
    path = ES_LOE_DIR / filename
    if not path.is_file():
        logger.warning(
            "_load_loe_json FAIL: file not found key=%r expected_path=%r ES_LOE_DIR=%r cwd=%r",
            subject_key, str(path), str(ES_LOE_DIR), str(Path.cwd()),
        )
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        _loe_cache[subject_key] = data
        logger.warning(
            "_load_loe_json SUCCESS: key=%r path=%s size=%s",
            subject_key, path, len(json.dumps(data)),
        )
        return data
    except Exception as exc:
        logger.warning(
            "_load_loe_json FAIL: json.load error key=%r path=%s error=%r",
            subject_key, path, exc,
            exc_info=True,
        )
        return None


def get_loe_subject_keys() -> list[str]:
    """Visszaadja az elérhető LOMLOE tantárgy-kulcsokat."""
    return [k for k in ES_LOE_FILES if (ES_LOE_DIR / ES_LOE_FILES[k]).is_file()]


def get_loe_subjects_for_grade(grade: int) -> list[dict[str, str]]:
    """Visszaadja az elérhető LOMLOE tantárgyakat adott évfolyamhoz."""
    result = []
    for k in get_loe_subject_keys():
        data = _load_loe_json(k)
        if data is None:
            continue
        evfolyamok = data.get("meta", {}).get("evfolyamok", [1, 2, 3, 4, 5, 6])
        if grade in evfolyamok:
            result.append({
                "label": _ES_LOE_SUBJECT_LABELS.get(k, k),
                "value": k,
            })
    return result


def get_loe_subject_label(subject_key: str) -> str:
    """LOMLOE tantárgy emberi neve."""
    return _ES_LOE_SUBJECT_LABELS.get(subject_key, subject_key)


def loe_cycle_for_grade(grade: int) -> str | None:
    """Visszaadja a LOMLOE ciklus nevét adott évfolyamhoz."""
    if 1 <= grade <= 2:
        return "1_ciclo"
    elif 3 <= grade <= 4:
        return "2_ciclo"
    elif 5 <= grade <= 6:
        return "3_ciclo"
    return None


def get_loe_curriculum_text(subject_key: str, grade: int) -> str | None:
    """Visszaadja a LOMLOE tantervi szöveget adott tantárgyhoz és évfolyamhoz."""
    data = _load_loe_json(subject_key)
    if not data:
        logger.warning(
            "get_loe_curriculum_text FAIL: _load_loe_json returned None for key=%r grade=%s",
            subject_key, grade,
        )
        return None
    cycle = loe_cycle_for_grade(grade)
    if not cycle:
        logger.warning(
            "get_loe_curriculum_text FAIL: no cycle for grade=%s (loe_cycle_for_grade returned None)",
            grade,
        )
        return None
    # Ellenőrizzük, hogy a ciklus létezik-e az adatokban
    ciklusok = data.get("ciklusok", {})
    if cycle not in ciklusok:
        logger.warning(
            "get_loe_curriculum_text FAIL: cycle=%r not in ciklusok keys=%r for key=%r",
            cycle, list(ciklusok.keys()), subject_key,
        )
        return None

    bevezeto = data.get("bevezeto", "")
    cycle_data = ciklusok.get(cycle, {})
    cycle_text = cycle_data.get("teljes_szoveg", "")

    # Összeállítjuk a teljes szöveget: bevezető + ciklus-specifikus rész
    parts = [bevezeto] if bevezeto else []
    if cycle_text:
        parts.append(cycle_text)
    result = "\n\n".join(parts)
    logger.warning(
        "get_loe_curriculum_text SUCCESS: key=%r grade=%s cycle=%s text_len=%s",
        subject_key, grade, cycle, len(result),
    )
    return result


def get_loe_curriculum_for_chat(subject_key: str, grade: int) -> dict[str, Any]:
    """Chat-hez használható LOMLOE tantervi kontextus."""
    text = get_loe_curriculum_text(subject_key, grade)
    if not text:
        logger.warning(
            "get_loe_curriculum_for_chat FAIL: no text for key=%r grade=%s",
            subject_key, grade,
        )
        return {
            "curriculum_body": "",
            "topics": {},
            "catalog": [],
            "data": {},
        }

    # A LOMLOE tantervet nyers szövegként adjuk vissza,
    # a magyar struktúra (topics, catalog) itt nem értelmezhető közvetlenül.
    data = _load_loe_json(subject_key) or {}
    meta = data.get("meta", {})

    result = {
        "curriculum_body": text,
        "topics": {"Általános tanterv": [meta.get("tantargy", subject_key)]},
        "catalog": [],
        "data": data,
        "subject_name": _ES_LOE_SUBJECT_LABELS.get(subject_key, subject_key),
        "language": "spanyol",
    }
    logger.warning(
        "get_loe_curriculum_for_chat SUCCESS: key=%r grade=%s body_len=%s",
        subject_key, grade, len(text),
    )
    return result


def get_hu_1_4_subjects() -> list[dict[str, str]]:
    """HU 1–4 tantárgyválasztó – fix lista, label + JSON fájlnév."""
    return [
        {"label": label, "value": filename}
        for label, filename in _HU_1_4_SUBJECT_MAP.items()
    ]


def _hu_1_4_subject_dicts_filtered(allowed_labels: set[str]) -> list[dict[str, str]]:
    """1-4 tantárgyválasztó szűrése engedélyezett címkékre, eredeti sorrendben."""
    result: list[dict[str, str]] = []
    for label, filename in _HU_1_4_SUBJECT_MAP.items():
        if label in allowed_labels:
            result.append({"label": label, "value": filename})
    return result


def get_hu_5_8_subjects(grade: int) -> list[dict[str, str]]:
    """HU 5–8 tantárgyválasztó – helyi JSON fájlokból (grade szerint szűrve)."""
    grade_num = parse_grade(grade)
    if not 5 <= grade_num <= 8:
        return []

    entries = _build_hu_json_index().get((5, 8, grade_num), [])
    options: list[dict[str, str]] = []
    seen_files: set[str] = set()
    for path, _slug, display in entries:
        if path.name in seen_files:
            continue
        seen_files.add(path.name)
        data = _load_hu_json(path)
        label = _display_subject_name(data.get("meta", {}).get("tantargy", display))
        options.append({"label": label, "value": path.name})

    options.sort(key=lambda o: o["label"].casefold())
    # Kizárt tantárgyak szűrése (pl. "Első élő idegen nyelv" → régi fájlnév)
    options = [o for o in options if _normalize_key(o["label"]) not in _HU_EXCLUDED_SUBJECT_KEYS]
    has_idegen = any(
        o["value"] == ELO_IDEGEN_NYELV_5_8_FILE
        or "idegen" in o["label"].casefold()
        for o in options
    )
    if not has_idegen:
        idegen_path = _PROJECT_ROOT / "hu_kerettanterv_5_8_TELJES" / ELO_IDEGEN_NYELV_5_8_FILE
        if idegen_path.is_file():
            options.append({"label": "Idegen nyelv", "value": ELO_IDEGEN_NYELV_5_8_FILE})
            options.sort(key=lambda o: o["label"].casefold())

    # Évfolyam-kapuzás a hivatalos kerettanterv szerint
    options = [o for o in options if _hu_json_applies_to_grade(o["label"], grade_num, "5-8")]
    return options


def is_elo_idegen_subject(subject_file: str) -> bool:
    return (subject_file or "").strip() in (
        ELO_IDEGEN_NYELV_1_4_FILE,
        ELO_IDEGEN_NYELV_5_8_FILE,
        ELO_IDEGEN_NYELV_5_8_ALT,
    )


def _elo_idegen_filename_for_grade(grade: int) -> str:
    grade_num = parse_grade(grade)
    if is_hu_1_4_grade(grade_num):
        return ELO_IDEGEN_NYELV_1_4_FILE
    return ELO_IDEGEN_NYELV_5_8_ALT


def _hu_1_4_path_candidates(filename: str) -> list[Path]:
    """1–4 JSON: lehetséges elérési utak (sorrendben), Railway / helyi mappa."""
    root = Path(__file__).parent
    seen: set[Path] = set()
    ordered: list[Path] = []
    for dir_name in _HU_JSON_DIR_CANDIDATES["1-4"]:
        base = root / dir_name
        for candidate in (
            base / filename,
            base / "hu_kerettanterv_1_4_TELJES" / filename,
        ):
            if candidate not in seen:
                seen.add(candidate)
                ordered.append(candidate)
    return ordered


def _log_resolve_hu_subject_file(
    subject: str, grade_num: int, result: dict[str, Any] | None
) -> None:
    """Diagnosztika: mit old fel a resolver, mely útvonalakat próbálja megnyitni."""
    root = Path(__file__).parent
    if result is None:
        logger.info(
            "_resolve_hu_subject_file: subject=%r grade=%s -> None (project_root=%s)",
            subject,
            grade_num,
            root,
        )
        return

    filename = result.get("file", "")
    if is_hu_1_4_grade(grade_num):
        candidates = _hu_1_4_path_candidates(filename)
        chosen = _hu_1_4_path_from_filename(filename)
        tried = "; ".join(
            f"{p} (exists={p.is_file()})" for p in candidates
        )
        logger.info(
            "_resolve_hu_subject_file: subject=%r grade=%s -> %s; "
            "project_root=%s; tried=[%s]; chosen=%s",
            subject,
            grade_num,
            result,
            root,
            tried,
            chosen,
        )
    else:
        path_58 = root / "hu_kerettanterv_5_8_TELJES" / filename
        logger.info(
            "_resolve_hu_subject_file: subject=%r grade=%s -> %s; "
            "5-8 path=%s (exists=%s)",
            subject,
            grade_num,
            result,
            path_58,
            path_58.is_file(),
        )


def _resolve_hu_subject_file(
    subject: str, grade: int | str
) -> dict[str, Any] | None:
    """Tantárgy név / fájlnév → JSON fájl + opcionális nyelvi ág (angol, nemet)."""
    raw = (subject or "").strip()
    if not raw:
        return None
    key = _normalize_key(raw)
    grade_num = parse_grade(grade)
    band_1_4 = is_hu_1_4_grade(grade_num)

    result: dict[str, Any] | None = None
    if key in ("angol",):
        result = {
            "file": _elo_idegen_filename_for_grade(grade_num),
            "language": "angol",
            "label": "Angol",
        }
    elif key in ("nemet",):
        result = {
            "file": _elo_idegen_filename_for_grade(grade_num),
            "language": "nemet",
            "label": "Német",
        }
    elif key in ("francia",):
        result = {
            "file": _elo_idegen_filename_for_grade(grade_num),
            "language": "francia",
            "label": "Francia",
        }
    elif key in ("spanyol",):
        result = {
            "file": SPANYOL_1_4_FILE if band_1_4 else SPANYOL_5_8_FILE,
            "language": None,
            "label": "Spanyol",
        }
    elif key == "idegennyelv":
        result = {
            "file": _elo_idegen_filename_for_grade(grade_num),
            "language": None,
            "label": "Idegen nyelv",
        }
    elif is_elo_idegen_subject(raw):
        result = {"file": raw, "language": None, "label": raw}
    elif raw in HU_1_4_SUBJECT_FILES and band_1_4:
        result = {"file": raw, "language": None, "label": hu_1_4_label_from_value(raw)}
    elif raw in _HU_1_4_SUBJECT_MAP and band_1_4:
        filename = _HU_1_4_SUBJECT_MAP[raw]
        result = {"file": filename, "language": None, "label": raw}
    else:
        for label, filename in _HU_1_4_SUBJECT_MAP.items():
            if band_1_4 and (raw == label or raw == filename):
                result = {"file": filename, "language": None, "label": label}
                break

    _log_resolve_hu_subject_file(raw, grade_num, result)
    return result


def _curriculum_data_for_language(
    data: dict[str, Any], language: str | None
) -> dict[str, Any]:
    """Élő idegen nyelv JSON: angol / német ág kiválasztása a nyelvek blokkból."""
    if not language:
        # Nincs nyelv megadva (pl. "Idegen nyelv" → nincs konkrét nyelv).
        # Próbáljuk az "angol" ágat, ha nincs, az első elérhető nyelvet.
        nyelvek = data.get("nyelvek")
        if isinstance(nyelvek, dict) and nyelvek:
            for default in ("angol",):
                if default in nyelvek and isinstance(nyelvek[default], dict):
                    return nyelvek[default]
            # Első elérhető nyelv
            first = next(iter(nyelvek))
            branch = nyelvek[first]
            if isinstance(branch, dict):
                return branch
        return data
    lang = (language or "").strip().lower()
    nyelvek = data.get("nyelvek")
    if isinstance(nyelvek, dict) and lang in nyelvek:
        branch = nyelvek[lang]
        if isinstance(branch, dict):
            return branch
    # A kért nyelvhez nincs ág (pl. "francia") → visszaesés "angol"-ra,
    # vagy az első elérhető nyelvre, hogy a lista ne legyen üres.
    if isinstance(nyelvek, dict) and nyelvek:
        for default in ("angol",):
            if default in nyelvek and isinstance(nyelvek[default], dict):
                return nyelvek[default]
        first = next(iter(nyelvek))
        branch = nyelvek[first]
        if isinstance(branch, dict):
            return branch
    return data


def get_hu_subjects_for_grade(grade: int) -> list[dict[str, str]]:
    """HU tantárgylista évfolyam szerint (1–4 és 5–8 kapuzással)."""
    grade_num = parse_grade(grade)
    if is_hu_1_4_grade(grade_num):
        allowed = set(list_hu_subjects_1_4(grade_num))
        return _hu_1_4_subject_dicts_filtered(allowed)
    if 5 <= grade_num <= 8:
        return get_hu_5_8_subjects(grade_num)
    return []


def is_hu_1_4_grade(grade: str | int) -> bool:
    try:
        grade_num = parse_grade(grade)
    except ValueError:
        return False
    return 1 <= grade_num <= 4


def uses_hu_1_4_curriculum(curriculum: str, grade: str | int) -> bool:
    """HU 1–4: fájlnév-alapú tantárgylista + helyi JSON tanterv."""
    return (curriculum or "").upper() == "HU" and is_hu_1_4_grade(grade)


def hu_1_4_label_from_value(value: str) -> str:
    """JSON fájlnév vagy régi megjelenítési név → magyar tantárgy név."""
    if value in _HU_1_4_SUBJECT_MAP:
        return value
    for label, filename in _HU_1_4_SUBJECT_MAP.items():
        if value == filename:
            return label
    return value


def foreign_language_prompt_block(language: str | None) -> str:
    """Idegen nyelv tantárgyhoz: angol/német feladat utasítás."""
    if language == "angol":
        return (
            "\nFONTOS: A feladatok KIZÁRÓLAG ANGOL nyelvűek legyenek. "
            "A gyerek angolul tanulja ezt a nyelvet; a feladatok, szavak, "
            "mondatok és fordítások is angolul legyenek.\n"
        )
    if language == "nemet":
        return (
            "\nFONTOS: A feladatok KIZÁRÓLAG NÉMET nyelvűek legyenek. "
            "A gyerek németül tanulja ezt a nyelvet; a feladatok, szavak, "
            "mondatok és fordítások is németül legyenek.\n"
        )
    if language == "spanyol":
        return (
            "\nFONTOS: A feladatok KIZÁRÓLAG spanyol nyelvűek legyenek. "
            "A gyerek spanyolul tanulja ezt a nyelvet; a feladatok, szavak, "
            "mondatok és fordítások is spanyolul legyenek.\n"
        )
    return ""


# Régi katalógus – csak 5–8 indexhez (1–4 NE használja dinamikus listát)
_HU_1_4_JSON_CATALOG: tuple[tuple[str, str, int, int], ...] = tuple(
    (label, filename.replace("_1_4.json", ""), 1, 4)
    for label, filename in _HU_1_4_SUBJECT_MAP.items()
)

# ---------------------------------------------------------------------------
# Spanyol ár-nevek (slug -> megjelenített név)
# ---------------------------------------------------------------------------

_ES_AREA_SLUGS: dict[str, str] = {
    "conocimiento-medio": "Conocimiento del Medio Natural, Social y Cultural",
    "educacion-artistica": "Educación Artística",
    "educacion-fisica": "Educación Física",
    "lengua-castellana": "Lengua Castellana y Literatura",
    "lengua-extranjera": "Lengua Extranjera",
    "matematicas": "Matemáticas",
    "educacion-valores": "Educación en Valores Cívicos y Éticos",
    "ensenanzas-religion": "Enseñanzas de religión",
}

# Autonóm közösség -> educagob térkép title attribútum
_ES_REGION_TITLES: dict[str, str] = {
    "AN": "Andalucía",
    "AR": "Aragón",
    "AS": "Asturias (P. de)",
    "IB": "Balears (Illes)",
    "CN": "Canarias",
    "CB": "Cantabria",
    "CM": "Castilla-La Mancha",
    "CL": "Castilla y León",
    "CT": "Cataluña",
    "VC": "Valenciana (C.)",
    "EX": "Extremadura",
    "GA": "Galicia",
    "RI": "Rioja (La)",
    "MD": "Madrid (C. de)",
    "MC": "Murcia (Región de)",
    "NC": "Navarra (C.F. de)",
    "PV": "País Vasco",
}

# HTML szövegből kinyerhető tantárgy-minták (autonóm dokumentumok)
_ES_SUBJECT_PATTERNS: tuple[str, ...] = (
    r"Lengua Castellana y Literatura",
    r"Lengua Cooficial y Literatura",
    r"Lengua propia y literatura",
    r"Lengua Extranjera",
    r"Segunda Lengua Extranjera",
    r"Matemáticas",
    r"Conocimiento del Medio Natural, Social y Cultural",
    r"Ciencias de la Naturaleza",
    r"Ciencias Sociales",
    r"Educación Artística",
    r"Educación Plástica y Visual",
    r"Música y Danza",
    r"Educación Física",
    r"Educación en Valores Cívicos y Éticos",
    r"Enseñanzas de religión",
)

# ---------------------------------------------------------------------------
# Fallback listák
# ---------------------------------------------------------------------------

FALLBACK_HU: dict[str, list[str]] = {
    "1-4": [
        "Magyar nyelv és irodalom",
        "Matematika",
        "Etika",
        "Ének-zene",
        "Vizuális kultúra",
        "Technika és tervezés",
        "Testnevelés",
    ],
    "1-4_g3": [
        "Magyar nyelv és irodalom",
        "Matematika",
        "Etika",
        "Környezetismeret",
        "Digitális kultúra",
        "Ének-zene",
        "Vizuális kultúra",
        "Technika és tervezés",
        "Testnevelés",
    ],
    "1-4_g4": [
        "Magyar nyelv és irodalom",
        "Matematika",
        "Etika",
        "Környezetismeret",
        "Idegen nyelv",
        "Digitális kultúra",
        "Ének-zene",
        "Vizuális kultúra",
        "Technika és tervezés",
        "Testnevelés",
    ],
    "5-8": [
        "Magyar nyelv és irodalom",
        "Matematika",
        "Történelem",
        "Hon- és népismeret",
        "Etika",
        "Első élő idegen nyelv",
        "Ének-zene",
        "Vizuális kultúra",
        "Digitális kultúra",
        "Testnevelés",
    ],
    "5-8_g56": [
        "Magyar nyelv és irodalom",
        "Matematika",
        "Történelem",
        "Hon- és népismeret",
        "Etika",
        "Természettudomány",
        "Technika és tervezés",
        "Első élő idegen nyelv",
        "Ének-zene",
        "Vizuális kultúra",
        "Digitális kultúra",
        "Testnevelés",
    ],
    "5-8_g78": [
        "Magyar nyelv és irodalom",
        "Matematika",
        "Történelem",
        "Hon- és népismeret",
        "Etika",
        "Kémia",
        "Fizika",
        "Biológia",
        "Földrajz",
        "Dráma és színház",
        "Első élő idegen nyelv",
        "Ének-zene",
        "Vizuális kultúra",
        "Digitális kultúra",
        "Testnevelés",
    ],
    "5-8_g8": [
        "Magyar nyelv és irodalom",
        "Matematika",
        "Történelem",
        "Hon- és népismeret",
        "Etika",
        "Állampolgári ismeretek",
        "Kémia",
        "Fizika",
        "Biológia",
        "Földrajz",
        "Dráma és színház",
        "Első élő idegen nyelv",
        "Ének-zene",
        "Vizuális kultúra",
        "Digitális kultúra",
        "Testnevelés",
    ],
    "9-12": [
        "Magyar nyelv és irodalom",
        "Matematika",
        "Történelem",
        "Földrajz",
        "Biológia",
        "Kémia",
        "Fizika",
        "Digitális kultúra",
        "Testnevelés",
        "Első élő idegen nyelv",
    ],
}

FALLBACK_ES_BASE: list[str] = [
    "Conocimiento del Medio Natural, Social y Cultural",
    "Educación Artística",
    "Educación Física",
    "Lengua Castellana y Literatura",
    "Lengua Extranjera",
    "Matemáticas",
]

FALLBACK_ES_REGION_EXTRAS: dict[str, list[str]] = {
    "CT": ["Lengua Cooficial y Literatura (Catalán)"],
    "PV": ["Lengua Cooficial y Literatura (Euskera)"],
    "GA": ["Lengua Cooficial y Literatura (Galego)"],
    "NC": ["Lengua Cooficial y Literatura (Euskera)"],
    "IB": ["Lengua Cooficial y Literatura (Catalán)"],
    "VC": ["Lengua Cooficial y Literatura (Valenciano)"],
}

# ---------------------------------------------------------------------------
# Magyar hivatalos kerettanterv JSON (hu_kerettanterv_*_TELJES mappák)
# ---------------------------------------------------------------------------

_PROJECT_ROOT = Path(__file__).parent
_HU_JSON_DIR_CANDIDATES: dict[str, tuple[str, ...]] = {
    "1-4": ("hu_kerettanterv_1_4_TELJES", "hu_kerettanterv_1_4"),
    "5-8": ("hu_kerettanterv_5_8_TELJES",),
}
_HU_FILENAME_RE = re.compile(r"^(.+)[_-](\d+)[_-](\d+)\.json$", re.IGNORECASE)
_HU_AGGREGATE_PREFIX = "hu_kerettanterv_"

# Csak ezek jelenhetnek meg HU 1–4 feladatválasztóban (JSON fájlokkal párosítva)
_HU_1_4_ALLOWED: frozenset[str] = frozenset(
    {
        "Magyar nyelv és irodalom",
        "Matematika",
        "Környezetismeret",
        "Etika",
        "Idegen nyelv",
        "Ének-zene",
        "Vizuális kultúra",
        "Technika és tervezés",
        "Digitális kultúra",
        "Testnevelés",
    }
)

# Spanyol tantárgyak – kizárólag ES ország + spanyol UI
_ES_CIENCIAS_CANONICAL = frozenset(
    {
        "Ciencias de la Naturaleza",
        "Ciencias Sociales",
    }
)

# HU profilban tiltott feliratok / téves mappingek
_FORBIDDEN_HU_LABELS = frozenset(
    {
        "Spanyol nyelv és irodalom",
        "Vallásoktatás",
    }
)

_json_file_cache: dict[str, dict[str, Any]] = {}
_hu_json_index: dict[tuple[int, int, int], list[tuple[Path, str, str]]] | None = None


def _normalize_key(value: str) -> str:
    text = unicodedata.normalize("NFKD", value)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]", "", text.casefold())


def _display_subject_name(raw: str) -> str:
    # Strip grade range suffix from filenames (e.g., "Tortenelem_5_8.json" -> "Tortenelem")
    raw = re.sub(r'[-_]\d+[-_]\d+\.json$', '', raw, flags=re.IGNORECASE)
    key = _normalize_key(raw)
    for slug, display in _HU_DOCX_SUBJECTS.items():
        if key in (_normalize_key(slug), _normalize_key(display)):
            return display
    aliases = {
        "digitaliskultura": "Digitális kultúra",
        "enekzene": "Ének-zene",
        "vizualiskultura": "Vizuális kultúra",
        "kornyezetismeret": "Környezetismeret",
        "idegennyelv": "Idegen nyelv",
        "eloidegennyelv": "Idegen nyelv",
        "technikaestervezes": "Technika és tervezés",
        "testneveles": "Testnevelés",
        "tortenelem": "Történelem",
        "allampolgariismeretek": "Állampolgári ismeretek",
        "honesnepismeret": "Hon- és népismeret",
        "termeszettudomany": "Természettudomány",
        "dramaesszinhaz": "Dráma és színház",
        "kozossegineveles": "Közösségi nevelés",
    }
    return aliases.get(key, raw)


def _subjects_match(requested: str, slug: str, meta_name: str) -> bool:
    req = _normalize_key(requested)
    file_keys = {
        _normalize_key(slug),
        _normalize_key(meta_name),
        _normalize_key(_display_subject_name(meta_name)),
    }
    if req in file_keys:
        return True
    for alias_key in _HU_SUBJECT_JSON_ALIASES.get(req, ()):
        if alias_key in file_keys:
            return True
    return False


def _hu_band_for_grade(grade: int) -> str:
    if 1 <= grade <= 4:
        return "1-4"
    if 5 <= grade <= 8:
        return "5-8"
    raise ValueError(f"Magyar JSON tanterv csak 1–8. évfolyamhoz érhető el: {grade}")


def _hu_json_directories(grade: int) -> list[Path]:
    band = _hu_band_for_grade(grade)
    dirs: list[Path] = []
    for name in _HU_JSON_DIR_CANDIDATES[band]:
        path = _PROJECT_ROOT / name
        if path.is_dir():
            dirs.append(path)
    return dirs


def _load_hu_json(path: Path) -> dict[str, Any]:
    key = str(path.resolve())
    if key not in _json_file_cache:
        _json_file_cache[key] = json.loads(path.read_text(encoding="utf-8"))
    return _json_file_cache[key]


def _hu_sort_key(path: Path) -> tuple[int, str]:
    """Rendezési kulcs: kötőjeles fájlok előbb (új, ékezetes), majd ABC."""
    name = path.name.casefold()
    prefers_hyphen = 0 if "-" in Path(name).stem.split("_")[-1] else 1
    return (prefers_hyphen, name)


def _build_hu_json_index() -> dict[tuple[int, int, int], list[tuple[Path, str, str]]]:
    """Index: (grade_lo, grade_hi, grade) -> [(path, slug, display_name), ...]."""
    global _hu_json_index
    if _hu_json_index is not None:
        return _hu_json_index

    index: dict[tuple[int, int, int], list[tuple[Path, str, str]]] = {}
    seen: set[tuple[str, int, int]] = set()

    for band, dir_names in _HU_JSON_DIR_CANDIDATES.items():
        grade_lo, grade_hi = (1, 4) if band == "1-4" else (5, 8)
        for dir_name in dir_names:
            directory = _PROJECT_ROOT / dir_name
            if not directory.is_dir():
                continue
            for path in sorted(directory.glob("*.json"), key=_hu_sort_key):
                if _is_hu_aggregate_json(path):
                    continue
                if path.name in _LANGUAGE_SPECIFIC_FILES:
                    continue
                match = _HU_FILENAME_RE.match(path.name)
                if not match:
                    continue
                slug, file_lo, file_hi = match.group(1), int(match.group(2)), int(match.group(3))
                slug = _normalize_filename_slug(slug)
                dedupe_key = (slug.casefold(), grade_lo, grade_hi)
                if dedupe_key in seen:
                    continue
                seen.add(dedupe_key)
                data = _load_hu_json(path)
                meta_name = data.get("meta", {}).get("tantargy", slug.replace("_", " "))
                display = _display_subject_name(meta_name)
                lo = max(grade_lo, file_lo)
                hi = min(grade_hi, file_hi)
                for grade in range(lo, hi + 1):
                    index.setdefault((grade_lo, grade_hi, grade), []).append((path, slug, display))

    _hu_json_index = index
    return index


def _normalize_filename_slug(slug: str) -> str:
    """Fájlnév slug tisztítása (mojibake / ékezetek kezelése)."""
    text = unicodedata.normalize("NFKD", slug)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = re.sub(r"[^a-zA-Z0-9_]", "", text)
    if _normalize_key(text).startswith("testnevel"):
        return "Testneveles"
    return text


def _is_hu_aggregate_json(path: Path) -> bool:
    """Összesítő / master JSON – nem tantárgy (pl. hu_kerettanterv_1_4_HIVATALOS.json)."""
    name = path.name.casefold()
    return name.startswith(_HU_AGGREGATE_PREFIX) or "hivatalos" in name


def _is_aggregate_subject_name(name: str) -> bool:
    """Tantárgy-név, ami valójában összesítő fájlra utal – kiszűrendő."""
    key = _normalize_key(name)
    return (
        "hivatalos" in key
        or key.startswith("hukerettanterv")
        or ("kerettanterv" in key and "magyar" not in key)
    )


def _hu_1_4_json_path(slug: str) -> Path | None:
    """JSON fájl elérési útja slug alapján (relatív a curriculum_loader.py-hoz)."""
    filename = f"{slug}_1_4.json"
    return _hu_1_4_path_from_filename(filename)


def _hu_1_4_path_from_filename(filename: str) -> Path | None:
    """Hardcoded JSON fájlnév → teljes elérési út (hu_kerettanterv_1_4_TELJES)."""
    if filename not in HU_1_4_SUBJECT_FILES and filename not in (SPANYOL_1_4_FILE, ANGOL_1_4_FILE, NEMET_1_4_FILE):
        return None
    for candidate in _hu_1_4_path_candidates(filename):
        if candidate.is_file() and not _is_hu_aggregate_json(candidate):
            return candidate
    return None


def _hu_json_search_paths(filename: str, grade: int) -> list[Path]:
    """Keresési útvonalak egy tantárgy-JSON-hoz (1–4 és 5–8 mappák)."""
    paths: list[Path] = []
    root = Path(__file__).parent
    grade_num = parse_grade(grade)
    if is_hu_1_4_grade(grade_num):
        p = _hu_1_4_path_from_filename(filename)
        if p:
            paths.append(p)
    for dir_name in _HU_JSON_DIR_CANDIDATES.get("5-8", ()):
        candidate = root / dir_name / filename
        if candidate.is_file() and candidate not in paths:
            paths.append(candidate)
    if is_hu_1_4_grade(grade_num):
        for dir_name in _HU_JSON_DIR_CANDIDATES["1-4"]:
            candidate = root / dir_name / filename
            if candidate.is_file() and candidate not in paths:
                paths.append(candidate)
    return paths


def list_hu_subjects_1_4(grade: int) -> list[str]:
    """1–4. évfolyam: tantárgyak évfolyam-kapuzással."""
    if not 1 <= grade <= 4:
        return []
    result: list[str] = []
    for entry in get_hu_1_4_subjects():
        label = entry["label"]
        if _hu_json_applies_to_grade(label, grade, "1-4"):
            result.append(label)
    return result


def _is_spanish_subject_name(name: str) -> bool:
    return _normalize_key(name) in _SPANISH_SUBJECT_KEYS


def _ciencias_visible_in_ui(curriculum: str, ui_lang: str) -> bool:
    """Ciencias de la Naturaleza / Sociales – csak ES tanterv + spanyol UI."""
    return curriculum.upper() == "ES" and ui_lang == "es"


def _sanitize_hu_subjects(subjects: list[str], grade: int) -> list[str]:
    """HU tantárgy-lista: 1–4 JSON katalógus; 5+ spanyol nevek kiszűrése."""
    if 1 <= grade <= 4:
        catalog = list_hu_subjects_1_4(grade)
        if catalog:
            return catalog
        return [s for s in _hu_fallback(grade) if s in _HU_1_4_ALLOWED]

    if grade < 1 or grade > 12:
        return _dedupe(subjects)

    band = _hu_band_for_grade(grade)
    cleaned: list[str] = []
    seen: set[str] = set()

    for raw in subjects:
        raw_name = (raw or "").strip()
        if not raw_name or _is_spanish_subject_name(raw_name):
            continue
        canonical = _display_subject_name(raw_name)
        key = _normalize_key(canonical)
        if key in _HU_EXCLUDED_SUBJECT_KEYS or key in seen:
            continue
        if not _hu_json_applies_to_grade(canonical, grade, band):
            continue
        seen.add(key)
        cleaned.append(canonical)

    magyar_key = _normalize_key(_HU_CORE_SUBJECT)
    if magyar_key not in seen:
        cleaned.insert(0, _HU_CORE_SUBJECT)

    if not cleaned:
        return _hu_fallback(grade)

    ordered: list[str] = []
    for subj in _hu_fallback(grade):
        if _normalize_key(subj) in _HU_EXCLUDED_SUBJECT_KEYS:
            continue
        if subj not in ordered:
            ordered.append(subj)
    for subj in cleaned:
        if subj not in ordered:
            ordered.append(subj)
    return ordered


def subject_ui_label(canonical: str, ui_lang: str, curriculum: str) -> str:
    """Tantárgy megjelenítési neve a UI nyelve szerint (HU / ES)."""
    curriculum = curriculum.upper()
    if ui_lang == "es":
        if curriculum == "HU":
            return _HU_SUBJECT_UI_ES.get(canonical, canonical)
        return canonical
    if curriculum == "HU":
        return canonical
    label = _ES_SUBJECT_UI_HU.get(canonical, canonical)
    if label in _ES_ONLY_HU_UI_LABELS:
        return canonical
    return label


def get_subject_options_for_ui(
    curriculum: str,
    grade: str | int,
    region: str | None,
    ui_lang: str,
) -> tuple[dict[str, Any], list[dict[str, str]]]:
    """Tanterv + legördülő opciók: value=tantervi név, label=UI nyelv."""
    curriculum = curriculum.upper()
    grade_num = parse_grade(grade)

    # HU 1–4: kizárólag hardcoded lista – semmi más logika nem írhatja felül
    if curriculum == "HU" and 1 <= grade_num <= 4:
        options = get_hu_1_4_subjects()
        profile: dict[str, Any] = {
            "subjects": [o["label"] for o in options],
            "source": "hardcoded",
            "fetched_at": _now_iso(),
            "curriculum": curriculum,
            "grade": grade_num,
            "region": None,
        }
        return profile, options

    profile = get_subjects_for_profile(curriculum, grade, region)
    options: list[dict[str, str]] = []
    for canonical in profile["subjects"]:
        if curriculum == "HU":
            if _is_spanish_subject_name(canonical) or _is_aggregate_subject_name(
                canonical
            ):
                continue
        if canonical in _ES_CIENCIAS_CANONICAL and not _ciencias_visible_in_ui(
            curriculum, ui_lang
        ):
            continue
        label = subject_ui_label(canonical, ui_lang, curriculum)
        if curriculum == "HU" and (
            label in _FORBIDDEN_HU_LABELS
            or label == "Spanyol nyelv és irodalom"
        ):
            continue
        # LOMLOE tantárgyak: használjuk a LOE labelt
        if canonical in _ES_LOE_SUBJECT_LABELS:
            label = _ES_LOE_SUBJECT_LABELS[canonical]
        options.append({"value": canonical, "label": label})
    return profile, options


def _hu_json_applies_to_grade(display_name: str, grade: int, band: str) -> bool:
    rules = _HU_GRADE_RULES_LOWER if band == "1-4" else _HU_GRADE_RULES_UPPER
    canonical = _display_subject_name(display_name)
    if canonical in rules:
        lo, hi = rules[canonical]
        return lo <= grade <= hi
    if display_name in rules:
        lo, hi = rules[display_name]
        return lo <= grade <= hi
    return True


def list_hu_subjects_from_json(grade: int) -> list[str]:
    """Tantárgy-lista a helyi JSON fájlokból (1–8. évfolyam)."""
    band = _hu_band_for_grade(grade)
    if band == "1-4":
        return list_hu_subjects_1_4(grade)

    grade_lo, grade_hi = (5, 8)
    entries = _build_hu_json_index().get((grade_lo, grade_hi, grade), [])
    from_json: list[str] = []
    for _, _, display in entries:
        canonical = _display_subject_name(display)
        if _hu_json_applies_to_grade(canonical, grade, band) and canonical not in from_json:
            from_json.append(canonical)
    fallback = _hu_fallback(grade)
    ordered: list[str] = []
    for subj in fallback:
        if _hu_json_applies_to_grade(subj, grade, band) and subj not in ordered:
            ordered.append(subj)
    for subj in from_json:
        if subj not in ordered:
            ordered.append(subj)
    return _sanitize_hu_subjects(ordered, grade)


def find_hu_json_file(grade: int, subject: str) -> Path | None:
    """Megfelelő tantárgy-JSON fájl keresése évfolyam és tantárgy alapján."""
    resolved = _resolve_hu_subject_file(subject, grade)
    if resolved:
        for path in _hu_json_search_paths(resolved["file"], grade):
            return path

    band = _hu_band_for_grade(grade)
    if band == "1-4":
        if subject in HU_1_4_SUBJECT_FILES or subject == SPANYOL_1_4_FILE:
            path = _hu_1_4_path_from_filename(subject)
            if path:
                return path
        for label, filename in _HU_1_4_SUBJECT_MAP.items():
            slug = filename.replace("_1_4.json", "")
            if _subjects_match(subject, slug, label):
                path = _hu_1_4_path_from_filename(filename)
                if path:
                    return path
        return None

    grade_lo, grade_hi = (5, 8)
    entries = _build_hu_json_index().get((grade_lo, grade_hi, grade), [])
    for path, slug, display in entries:
        data = _load_hu_json(path)
        meta_name = data.get("meta", {}).get("tantargy", slug)
        if _subjects_match(subject, slug, meta_name) or _subjects_match(subject, slug, display):
            if _hu_json_applies_to_grade(display, grade, band):
                return path
    return None


def _hu_evfolyam_blokk_for_grade(
    data: dict[str, Any], grade: int | str
) -> dict[str, Any] | None:
    """Új JSON: evfolyam_blokkok – melyik blokk tartozik az osztályhoz."""
    grade_num = parse_grade(grade)
    blocks = data.get("evfolyam_blokkok", {})
    if not isinstance(blocks, dict):
        return None
    best_with_topics: dict[str, Any] | None = None
    best_span = 999
    for _key, blokk in blocks.items():
        if not isinstance(blokk, dict):
            continue
        evs = blokk.get("evfolyamok") or []
        if grade_num not in evs:
            continue
        if blokk.get("temakorok"):
            span = (max(evs) - min(evs)) if evs else 999
            if span < best_span:
                best_span = span
                best_with_topics = blokk
    if best_with_topics:
        return best_with_topics
    for _key, blokk in blocks.items():
        if not isinstance(blokk, dict):
            continue
        if grade_num in blokk.get("evfolyamok", []):
            return blokk
    # Pl. 1–4. évfolyam egyetlen „4” blokkban – legközelebbi blokk temakorokkal
    best: dict[str, Any] | None = None
    best_hi = -1
    for blokk in blocks.values():
        if not isinstance(blokk, dict) or not blokk.get("temakorok"):
            continue
        evs = blokk.get("evfolyamok") or []
        if evs and max(evs) <= grade_num and max(evs) > best_hi:
            best_hi = max(evs)
            best = blokk
    if best:
        return best
    for blokk in blocks.values():
        if isinstance(blokk, dict) and blokk.get("temakorok"):
            return blokk
    return None


def _is_spiral_subject(data: dict[str, Any], raw_data: dict[str, Any] | None = None) -> bool:
    """Ellenőrzi, hogy a tantárgy spirális-e (a témakörök minden évben visszatérnek).

    Két forrásból dolgozik:
      1. a tantárgy neve szerepel a _SPIRAL_SUBJECT_DISPLAY_NAMES halmazban, VAGY
      2. a fájl `meta.spiralis` mezője igaz.
    A második azért kell, mert egy tantárgy lehet spirális az egyik évfolyam-
    sávban és sorrendi a másikban (pl. Technika és tervezés 1-4 vs. 5-8),
    ezért a névalapú lista önmagában nem elég pontos.
    """
    meta = (raw_data or data).get("meta", {}) or {}
    if meta.get("spiralis") is True:
        return True
    tantargy = meta.get("tantargy", "")
    if not tantargy:
        return False
    return tantargy in _SPIRAL_SUBJECT_DISPLAY_NAMES


def _is_loe_spiral_subject(data: dict[str, Any]) -> bool:
    """Ellenőrzi, hogy a LOMLOE tantárgy spirális-e."""
    tantargy = data.get("meta", {}).get("tantargy", "")
    return tantargy in _LOE_SPIRAL_SUBJECT_NAMES


def _loe_cycle_grade_range(cycle: str) -> tuple[int, int] | None:
    """Visszaadja a LOMLOE ciklus első és utolsó évfolyamát."""
    _CYCLES = {"1_ciclo": (1, 2), "2_ciclo": (3, 4), "3_ciclo": (5, 6)}
    return _CYCLES.get(cycle)


def _exclusive_split_ranges(
    ora_list: list[int], num_grades: int
) -> list[tuple[int, int]]:
    """KIZÁRÓ (átfedésmentes) [start, end) index-tartományok évfolyamonként.

    SZIGORÚAN INDEX-ALAPÚ szétosztás: minden témakör indexe alapján PONTOSAN
    egy évfolyamhoz kerül. NEM óraszám-határ metszés alapján, hanem a témakörök
    sorszáma (pozíciója) dönti el, melyik évfolyamé.

    Algoritmus (egyenletes, darabszám szerinti, kizáró felosztás):
      - per_grade = n // num_grades, remainder = n % num_grades
      - az első `remainder` évfolyam 1-gyel több témakört kap
      - a tartományok egymást KIZÁRJÁK: [0,s1), [s1,s2), ..., [s_{k-1}, n)

    Garantálja: a tartományok uniója PONTOSAN [0, n), átfedés és kihagyás
    nélkül — így minden témakör pontosan egy évfolyamhoz tartozik.
    (Az ora_list paramétert az aláíráskompatibilitás miatt megtartjuk.)
    """
    n = len(ora_list)
    if num_grades <= 1:
        return [(0, n)]
    # Egyenletes, darabszám szerinti, SZIGORÚAN kizáró felosztás index alapján
    per_grade = n // num_grades
    remainder = n % num_grades
    ranges: list[tuple[int, int]] = []
    start = 0
    for gi in range(num_grades):
        size = per_grade + (1 if gi < remainder else 0)
        ranges.append((start, start + size))
        start += size
    return ranges


def _split_loe_topics_for_grade(
    temakorok: list[dict[str, Any]],
    grade_num: int,
    *,
    first_grade: int,
    last_grade: int,
) -> list[dict[str, Any]]:
    """LOMLOE ciklus témaköreinek KIZÁRÓ szétosztása évfolyamok között.

    Ugyanaz a logika, mint a magyar _split_band_topics_for_grade, de közvetlenül
    témakör-listával dolgozik (a ciklus első és utolsó évfolyama paraméter).
    Minden témakör PONTOSAN egy évfolyamhoz kerül: a szétosztott listák uniója
    az eredeti lista, ismétlődés nélkül.
    """
    if not temakorok:
        return temakorok
    evfolyamok = list(range(first_grade, last_grade + 1))
    if len(evfolyamok) <= 1 or grade_num not in evfolyamok:
        return temakorok

    ora_list: list[int] = []
    for item in temakorok:
        if isinstance(item, dict) and item.get("nev"):
            raw = str(item.get("javasolt_oraszam", "0"))
            m = re.search(r"\d+", raw)
            ora_list.append(int(m.group()) if m else 0)
        else:
            ora_list.append(0)

    grade_idx = evfolyamok.index(grade_num)
    ranges = _exclusive_split_ranges(ora_list, len(evfolyamok))
    start, end = ranges[grade_idx]
    return temakorok[start:end]


def _split_band_topics_for_grade(
    blokk: dict[str, Any], grade_num: int
) -> list[dict[str, Any]]:
    """Sáv-blokk témaköreinek KIZÁRÓ szétosztása évfolyamok között.

    Ha a blokk evfolyamok listája EGY évfolyamot tartalmaz, a teljes listát adja
    vissza. Több évfolyam esetén a javasolt_oraszam szerint halmozva osztja szét
    úgy, hogy minden témakör PONTOSAN egy évfolyamhoz kerüljön (a szétosztott
    listák uniója az eredeti lista, ismétlődés nélkül). Óraszám híján
    egyenletesen, darabszám szerint oszt.
    """
    evfolyamok: list[int] = blokk.get("evfolyamok") or []
    temakorok: list[dict[str, Any]] = blokk.get("temakorok") or []

    if not temakorok:
        return temakorok
    if len(evfolyamok) <= 1 or grade_num not in evfolyamok:
        return temakorok

    # Óraszámok kigyűjtése témakörönként
    ora_list: list[int] = []
    for item in temakorok:
        if isinstance(item, dict) and item.get("nev"):
            raw = str(item.get("javasolt_oraszam", "0"))
            m = re.search(r"\d+", raw)
            ora_list.append(int(m.group()) if m else 0)
        else:
            ora_list.append(0)

    grade_idx = evfolyamok.index(grade_num)
    ranges = _exclusive_split_ranges(ora_list, len(evfolyamok))
    start, end = ranges[grade_idx]
    return temakorok[start:end]


def extract_hu_grade_topics(data: dict[str, Any], grade: int) -> dict[str, list[str]]:
    """Évfolyam-specifikus témakörök kinyerése egy tantárgy JSON-ból."""
    blokk = _hu_evfolyam_blokk_for_grade(data, grade)
    if blokk:
        topics: dict[str, list[str]] = {}
        temakorok = blokk.get("temakorok") or []
        if isinstance(temakorok, list):
            for item in temakorok:
                if isinstance(item, dict) and item.get("nev"):
                    topics[str(item["nev"])] = []
                elif isinstance(item, str) and item.strip():
                    topics[item.strip()] = []
        return topics

    evfolyamok = data.get("evfolyamok", {})
    grade_node = evfolyamok.get(str(parse_grade(grade)))
    if not isinstance(grade_node, dict):
        return {}
    topics = {}
    for category, items in grade_node.items():
        if isinstance(items, list):
            cleaned = [str(item).strip() for item in items if str(item).strip()]
            if cleaned:
                topics[str(category)] = cleaned
    return topics


def curriculum_topic_names(topics: dict[str, list[str]]) -> list[str]:
    """Tananyag-fejlécek listája haladáskövetéshez."""
    if not topics:
        return ["Általános"]
    return list(topics.keys())


# ── A TANTERV SZERKEZETE ────────────────────────────────────────────────────
# A tantervi fájlokban a nyelvi témaköröknél KÜLÖN, SORRENDBE RAKOTT listák
# állnak — például az angol 5. osztály első témakörénél:
#     nyelvtan: ["létige: to be teljes ragozása", "kérdőszavak: who, when...",
#                "igenlő és nemleges rövid válasz"]
# Ez a sorrend nem véletlen: a létige ELŐBB jön, mert a többi arra épül.
#
# A katalógus korábban CSAK a nevet és a prózát (teljes_szoveg) tartotta meg,
# ezeket a listákat eldobta. Így a tanár modellnek a prózából kellett
# kitalálnia a sorrendet, minden fordulóban újra — és nem mindig találta el.
# Innen jött, hogy a "there is / there are" a létige előtt került elő.
#
# Ezek a mezők NEM MINDEN témakörnél vannak meg: a matematika és a többi
# nem-nyelvi tantárgy csak nevet, óraszámot és prózát ad. Ezért a hiányuk
# normális, nem hiba — a hívónak üres listával kell számolnia.
_SZERKEZET_MEZOK = (
    "szokincs",                 # a témakör szavai
    "nyelvtan",                 # NYELVTANI SORRENDBEN – ez a legfontosabb
    "kommunikacios_szandekok",  # mire használja a nyelvet
    "javasolt_tevekenysegek",   # milyen feladatokon keresztül
    "cefr_cel",                 # mit tudjon a végén (szöveg, nem lista)
    "kerettantervi_temakor",    # a hivatalos témakör neve (szöveg)
)


def _szerkezet(item: dict[str, Any]) -> dict[str, Any]:
    """A témakör szerkezetes mezői, ha a tanterv megadta őket.

    Csak azt adja vissza, ami TÉNYLEG ott van: a hiányzó mező nem kerül be
    üresen, hogy a hívó meg tudja különböztetni a "nincs megadva" esetet a
    "meg van adva, de üres"-től.
    """
    ki: dict[str, Any] = {}
    for mezo in _SZERKEZET_MEZOK:
        ertek = item.get(mezo)
        if isinstance(ertek, list):
            tisztitott = [str(x).strip() for x in ertek if str(x).strip()]
            if tisztitott:
                ki[mezo] = tisztitott
        elif isinstance(ertek, str) and ertek.strip():
            ki[mezo] = ertek.strip()
    return ki


def extract_topic_catalog(
    data: dict[str, Any], grade: int | str, *, raw_data: dict[str, Any] | None = None
) -> list[dict[str, Any]]:
    """Témakör lista chat sidebarhoz: id, name, text, index, ora_szam."""
    grade_num = parse_grade(grade)
    blokk = _hu_evfolyam_blokk_for_grade(data, grade_num)
    if blokk:
        catalog: list[dict[str, Any]] = []
        temakorok = blokk.get("temakorok") or []
        # Spirális tantárgyak: minden téma minden évben visszatér → ne osszuk szét
        if not _is_spiral_subject(data, raw_data):
            temakorok = _split_band_topics_for_grade(blokk, grade_num)
        if isinstance(temakorok, list):
            for idx, item in enumerate(temakorok):
                if isinstance(item, dict) and item.get("nev"):
                    raw = str(item.get("javasolt_oraszam", "0"))
                    m = re.search(r"\d+", raw)
                    ora_szam = int(m.group()) if m else 0
                    catalog.append(
                        {
                            "id": f"t{idx}",
                            "name": str(item["nev"]),
                            "text": str(item.get("teljes_szoveg", "")),
                            "index": idx,
                            "ora_szam": ora_szam,
                            # A tanterv saját sorrendje – lásd _szerkezet().
                            **_szerkezet(item),
                        }
                    )
        return catalog

    topics = extract_hu_grade_topics(data, grade_num)
    return [
        {"id": f"t{idx}", "name": name, "text": "", "index": idx, "ora_szam": 0}
        for idx, name in enumerate(topics.keys())
    ]


def _loe_catalog_from_list(items: list) -> list[dict[str, Any]]:
    """Témakör-lista → katalógus (id, name, text, index, ora_szam)."""
    catalog: list[dict[str, Any]] = []
    for idx, item in enumerate(items):
        if isinstance(item, dict) and item.get("nev"):
            raw = str(item.get("javasolt_oraszam", "0"))
            m = re.search(r"\d+", raw)
            catalog.append({
                "id": f"t{idx}",
                "name": str(item["nev"]),
                "text": str(item.get("teljes_szoveg") or ""),
                "index": idx,
                "ora_szam": int(m.group()) if m else 0,
                **_szerkezet(item),
            })
    return catalog


def extract_loe_topic_catalog(
    data: dict[str, Any], grade: int | str, *, language: str | None = None,
) -> list[dict[str, Any]]:
    """Spanyol (LOMLOE) témakör-katalógus a ciklus temakorok tömbjéből.

    Ugyanaz a szerkezet, mint az extract_topic_catalog (magyar) kimenete:
    id, name, text, index, ora_szam.

    Ha a language paraméter meg van adva (pl. "angol") és a ciklusban
    létezik temakorok_by_lang[language] nem üres lista, akkor azt
    használja a közös temakorok helyett (nyelvspecifikus leckék).
    """
    grade_num = parse_grade(grade)
    cycle = loe_cycle_for_grade(grade_num)
    if not cycle:
        return []
    ciklusok = data.get("ciklusok", {})
    if not isinstance(ciklusok, dict):
        return []
    cval = ciklusok.get(cycle)
    if not isinstance(cval, dict):
        return []

    # Nyelvspecifikus leckék (pl. extranjera + angol):
    lang_specific: list[dict[str, Any]] | None = None
    if language:
        by_lang = cval.get("temakorok_by_lang", {})
        if isinstance(by_lang, dict):
            candidates = by_lang.get(language)
            if isinstance(candidates, list) and len(candidates) > 0:
                lang_specific = candidates

    # ÉVFOLYAMONKÉNTI leckék, ha vannak (temakorok_by_grade["3"] stb.).
    # Ez a magyar oldal évfolyam-blokkjainak a spanyol megfelelője: a LOMLOE
    # „saberes básicos” blokkjai kompetenciaterületek, nem leckék, ezért a nagy
    # blokkokat konkrét, évfolyamhoz kötött leckékre bontjuk. Ha van ilyen
    # lista, azt használjuk, és NEM osztjuk szét a ciklus témaköreit.
    by_grade = cval.get("temakorok_by_grade")
    if lang_specific is None and isinstance(by_grade, dict):
        per_grade = by_grade.get(str(grade_num)) or by_grade.get(grade_num)
        if isinstance(per_grade, list) and per_grade:
            catalog_src = per_grade
            return _loe_catalog_from_list(catalog_src)

    temakorok = lang_specific if lang_specific is not None else (cval.get("temakorok") or [])
    if not isinstance(temakorok, list):
        return []

    # Ciklus témaköreinek szétosztása évfolyamok között
    # (kivéve spirális tantárgyak: Educación Física, Artística, Valores)
    if not _is_loe_spiral_subject(data):
        cycle_range = _loe_cycle_grade_range(cycle)
        if cycle_range:
            temakorok = _split_loe_topics_for_grade(
                temakorok, grade_num,
                first_grade=cycle_range[0], last_grade=cycle_range[1],
            )

    catalog: list[dict[str, Any]] = []
    for idx, item in enumerate(temakorok):
        if isinstance(item, dict) and item.get("nev"):
            raw = str(item.get("javasolt_oraszam", "0"))
            m = re.search(r"\d+", raw)
            ora_szam = int(m.group()) if m else 0
            catalog.append(
                {
                    "id": f"t{idx}",
                    "name": str(item["nev"]),
                    "text": str(item.get("teljes_szoveg", "")),
                    "index": idx,
                    "ora_szam": ora_szam,
                }
            )
    return catalog


def get_topic_from_catalog(
    catalog: list[dict[str, Any]], topic_id: str
) -> dict[str, Any] | None:
    for item in catalog:
        if item.get("id") == topic_id:
            return item
    return None


def format_curriculum_for_grade(data: dict[str, Any], grade: int | str) -> str:
    """Új struktúra: evfolyam_blokkok -> teljes_szoveg + temakorok."""
    grade_num = int(parse_grade(grade))

    blokk = _hu_evfolyam_blokk_for_grade(data, grade_num)
    if blokk:
        subject_name = data.get("meta", {}).get("tantargy", "Tantárgy")
        output = [
            f"=== {subject_name} – {grade_num}. évfolyam ===",
            "",
            "HIVATALOS KERETTANTERV TELJES SZÖVEGE:",
            "",
            str(blokk.get("teljes_szoveg", "")),
        ]
        return "\n".join(output)

    evfolyamok = data.get("evfolyamok", {})
    grade_node = evfolyamok.get(str(grade_num))
    if not isinstance(grade_node, dict) or not grade_node:
        return ""

    subject_name = data.get("meta", {}).get("tantargy", "Tantárgy")
    lines = [
        f"=== {subject_name} – {grade_num}. évfolyam (hivatalos kerettanterv) ===",
        "",
    ]
    for category, items in grade_node.items():
        lines.append(f"## {category}")
        if isinstance(items, list):
            for idx, item in enumerate(items, 1):
                text = str(item).strip()
                if text:
                    lines.append(f"  {idx}. {text}")
        lines.append("")
    return "\n".join(lines).strip()


def _elo_json_language_branch_score(
    path: Path, effective_language: str | None
) -> int:
    """0 = megfelelő nyelvi ág; magasabb = rosszabb (pl. német-only 1–4 JSON)."""
    if not effective_language:
        return 0
    lang = effective_language.strip().lower()
    if lang not in ("angol", "nemet", "spanyol"):
        return 0
    try:
        raw = _load_hu_json(path)
        if lang == "spanyol":
            name = path.name.casefold()
            meta = str((raw.get("meta") or {}).get("tantargy", "")).casefold()
            if "spanyol" in name or "spanyol" in meta:
                return 0
            if is_elo_idegen_subject(path.name):
                return 3
            return 1
        nyelvek = raw.get("nyelvek")
        if isinstance(nyelvek, dict) and lang in nyelvek:
            return 0
        if is_elo_idegen_subject(path.name) and not nyelvek:
            return 3
        return 1
    except Exception:
        return 5


# ── A NYELV NEVE ÉKEZET NÉLKÜL ──────────────────────────────────────────────
# ÉLES HIBA, 2026-09-02: a német tananyag (nemet_5-8.json) SOHA nem került
# használatba. A program a nyelvet a felületről "német" alakban kapta, a
# fájlválasztó viszont mindenhol az ékezet nélküli "nemet"-hez hasonlított.
# A kettő soha nem egyezett, ezért a német óra a közös, angol nyelvű
# Elo_idegen_nyelv_*.json-ból ment — nyelvtani sorrend és szókincs nélkül,
# angol témakörnevekkel. Az angolnál és a spanyolnál nincs ékezet a névben,
# ezért azoknál fel sem tűnt.
#
# EZÉRT NEM SPECIÁLIS ESET: minden nyelvnevet ékezet nélküli alakra hozunk,
# hogy a következő ékezetes nyelv (pl. "francia" rendben, de "cseh"/"görög"
# később) ne akadjon el ugyanezen.
_NYELV_EKEZET = str.maketrans({
    "á": "a", "é": "e", "í": "i", "ó": "o", "ö": "o", "ő": "o",
    "ú": "u", "ü": "u", "ű": "u",
})


def _nyelv_kulcs(nyelv: str | None) -> str | None:
    """'német' → 'nemet'. A fájlválasztó ezt az alakot ismeri."""
    kulcs = (nyelv or "").strip().lower()
    return kulcs.translate(_NYELV_EKEZET) or None


def get_curriculum_for_chat(
    subject_file: str,
    grade: int | str,
    *,
    language: str | None = None,
) -> dict[str, Any]:
    """JSON betöltés + évfolyam szerinti teljes tananyag (chat AI-hoz)."""
    grade_num = parse_grade(grade)
    subject_file = (subject_file or "").strip()
    explicit_language = _nyelv_kulcs(language)
    effective_language = explicit_language

    logger.warning(
        "get_curriculum_for_chat START: subject_file=%r grade=%s language=%s "
        "in_ES_LOE_FILES=%s loe_cycle=%s ES_LOE_DIR=%r ES_LOE_FILES_keys=%s",
        subject_file,
        grade_num,
        effective_language,
        subject_file in ES_LOE_FILES,
        loe_cycle_for_grade(grade_num),
        str(ES_LOE_DIR),
        list(ES_LOE_FILES.keys()),
    )

    # ── LOMLOE spanyol nemzeti tanterv ──────────────────────────────────────
    if subject_file in ES_LOE_FILES and loe_cycle_for_grade(grade_num):
        loe = get_loe_curriculum_for_chat(subject_file, grade_num)
        logger.warning(
            "get_curriculum_for_chat LOE branch: curriculum_body_len=%s subject_name=%s",
            len(loe.get("curriculum_body") or ""),
            loe.get("subject_name", "?"),
        )
        if loe.get("curriculum_body"):
            loe_catalog = extract_loe_topic_catalog(
                loe.get("data", {}), grade_num, language=effective_language,
            )
            logger.warning(
                "get_curriculum_for_chat LOE branch: topic_catalog_len=%s",
                len(loe_catalog),
            )
            # A 'extranjera' (idegen nyelv) tantárgynál a tanított nyelv a
            # kiválasztott célnyelv (angol/német/francia), nem a spanyol.
            loe_language = "spanyol"
            if subject_file == "extranjera" and effective_language in (
                "angol", "nemet", "francia"
            ):
                loe_language = effective_language
            return {
                "found": True,
                "content": loe["curriculum_body"],
                "topics": ["LOMLOE tananyag"],
                "topics_detail": {},
                "topic_catalog": loe_catalog,
                "file": ES_LOE_FILES[subject_file],
                "subject_name": loe.get("subject_name", subject_file),
                "data": loe.get("data", {}),
                "language": loe_language,
            }
        logger.warning("get_curriculum_for_chat LOE branch: curriculum_body was EMPTY, falling through to HU path")

    resolved = _resolve_hu_subject_file(subject_file, grade_num)
    logger.warning(
        "get_curriculum_for_chat HU path: resolved=%r",
        resolved,
    )
    if resolved:
        subject_file = resolved["file"]
        if not effective_language and resolved.get("language"):
            effective_language = resolved["language"]
        display_label = resolved.get("label") or subject_file
    else:
        display_label = subject_file

    candidates: list[Path] = []
    root = Path(__file__).parent
    logger.warning(
        "get_curriculum_for_chat SEARCH: root=%r cwd=%r",
        str(root), str(Path.cwd()),
    )
    if subject_file:
        for path in _hu_json_search_paths(subject_file, grade_num):
            if path not in candidates:
                candidates.append(path)

        found = find_hu_json_file(grade_num, subject_file)
        if found and found not in candidates:
            candidates.append(found)

    if effective_language in ("angol", "nemet"):
        # 1-4 and 5-8 grade: prefer file with nyelvek structure for language separation
        for alt_name in (ELO_IDEGEN_NYELV_5_8_ALT, ELO_IDEGEN_NYELV_5_8_FILE):
            alt = root / "hu_kerettanterv_5_8_TELJES" / alt_name
            if alt.is_file() and alt not in candidates:
                candidates.insert(0, alt)

    # ── Nyelvspecifikus fájlok (spanyol_*/angol_*) kényszerítése ──
    # A pontozás (_score_path) a nyelvek-struktúrás általános fájlt
    # (elo_idegen_nyelv_*-*.json) preferálná, mert abban van nyelvek.angol ág,
    # a nyelvspecifikus fájlban nincs nyelvek kulcs. Ezt felül kell írni:
    # a nyelvspecifikus fájlnak mindig elsőnek KELL maradnia.
    _forced_paths: set[Path] = set()
    if effective_language == "spanyol" and is_hu_1_4_grade(grade_num):
        sp_path = _hu_1_4_path_from_filename(SPANYOL_1_4_FILE)
        if sp_path and sp_path not in candidates:
            _forced_paths.add(sp_path)
            candidates.insert(0, sp_path)
    elif effective_language == "spanyol" and grade_num >= 5:
        sp_path = root / "hu_kerettanterv_5_8_TELJES" / SPANYOL_5_8_FILE
        if sp_path.is_file() and sp_path not in candidates:
            _forced_paths.add(sp_path)
            candidates.insert(0, sp_path)

    if effective_language == "angol" and is_hu_1_4_grade(grade_num):
        en_path = _hu_1_4_path_from_filename(ANGOL_1_4_FILE)
        if en_path and en_path not in candidates:
            _forced_paths.add(en_path)
            candidates.insert(0, en_path)
    elif effective_language == "angol" and 5 <= grade_num <= 8:
        en_path = root / "hu_kerettanterv_5_8_TELJES" / ANGOL_5_8_FILE
        if en_path.is_file() and en_path not in candidates:
            _forced_paths.add(en_path)
            candidates.insert(0, en_path)

    if effective_language == "nemet" and is_hu_1_4_grade(grade_num):
        de_path = _hu_1_4_path_from_filename(NEMET_1_4_FILE)
        if de_path and de_path not in candidates:
            _forced_paths.add(de_path)
            candidates.insert(0, de_path)
    elif effective_language == "nemet" and 5 <= grade_num <= 8:
        de_path = root / "hu_kerettanterv_5_8_TELJES" / NEMET_5_8_FILE
        if de_path.is_file() and de_path not in candidates:
            _forced_paths.add(de_path)
            candidates.insert(0, de_path)

    def _has_new_structure(path: Path) -> bool:
        try:
            raw = _load_hu_json(path)
            view = _curriculum_data_for_language(raw, effective_language)
            return bool(view.get("evfolyam_blokkok"))
        except Exception:
            return False

    def _score_path(path: Path) -> tuple:
        lang_score = _elo_json_language_branch_score(path, effective_language)
        name = path.name.casefold()
        prefer_nyelvek = 0
        if effective_language in ("angol", "nemet"):
            prefer_nyelvek = 0 if ELO_IDEGEN_NYELV_5_8_ALT in name else 1
        return (
            lang_score,
            not _has_new_structure(path),
            prefer_nyelvek,
            len(str(path)),
        )

    candidates.sort(key=_score_path)

    # A kényszerített nyelvspecifikus fájlok vissza a lista elejére
    # (a _score_path alacsonyabbra pontozhatta őket, de elsőbbséget kell élvezzenek)
    for fp in sorted(_forced_paths, key=str):
        if fp in candidates:
            candidates.remove(fp)
            candidates.insert(0, fp)

    logger.warning(
        "get_curriculum_for_chat CANDIDATES: count=%s paths=%s",
        len(candidates),
        [str(p) for p in candidates],
    )

    # ── Évfolyam-szűrés a fájlnévben lévő tartomány alapján ──────────────
    grade_candidates: list[Path] = []
    for path in candidates:
        m = _HU_FILENAME_RE.match(path.name)
        if m:
            try:
                lo = int(m.group(2))
                hi = int(m.group(3))
                if lo <= grade_num <= hi:
                    grade_candidates.append(path)
            except (ValueError, IndexError):
                grade_candidates.append(path)  # parse error → keep
        else:
            grade_candidates.append(path)  # no grade range in name → keep

    logger.warning(
        "get_curriculum_for_chat CANDIDATES grade-filtered: count=%s paths=%s",
        len(grade_candidates),
        [str(p) for p in grade_candidates],
    )

    if grade_candidates:
        usable_in_grade = False
        for path in grade_candidates:
            try:
                raw = _load_hu_json(path)
                data = _curriculum_data_for_language(raw, effective_language)
                content = format_curriculum_for_grade(data, grade_num)
                catalog = extract_topic_catalog(data, grade_num, raw_data=raw)
                if content or catalog:
                    usable_in_grade = True
                    break
            except Exception:
                pass

        if usable_in_grade:
            candidates = grade_candidates
        else:
            logger.warning(
                "GRADE_FALLBACK: nincs %s. évfolyamhoz való fájl, marad: %s",
                grade_num, [str(p) for p in candidates],
            )
    else:
        logger.warning(
            "GRADE_FALLBACK: nincs %s. évfolyamhoz való fájl, marad: %s",
            grade_num, [str(p) for p in candidates],
        )

    for path in candidates:
        raw = _load_hu_json(path)
        # angol/német/spanyol: nyelvek.* ág (pl. 5–8 JSON), nem a nyers raw
        data = _curriculum_data_for_language(raw, effective_language)
        topics = extract_hu_grade_topics(data, grade_num)
        catalog = extract_topic_catalog(data, grade_num, raw_data=raw)
        content = format_curriculum_for_grade(data, grade_num)
        subject_name = (
            data.get("nyelv")
            or _display_subject_name(data.get("meta", {}).get("tantargy", ""))
            or _display_subject_name(raw.get("meta", {}).get("tantargy", ""))
            or display_label
        )
        if effective_language == "angol":
            subject_name = "Angol"
        elif effective_language == "nemet":
            subject_name = "Német"
        elif effective_language == "francia":
            subject_name = "Francia"
        elif effective_language == "spanyol":
            subject_name = "Spanyol"
        logger.warning(
            "get_curriculum_for_chat CANDIDATE: path=%s content_len=%s catalog_len=%s "
            "content_or_catalog=%s subject_name=%s",
            str(path),
            len(content or ""),
            len(catalog),
            bool(content or catalog),
            subject_name,
        )
        # Évfolyam-kapuzás: ha a tantárgy nem engedélyezett ezen az évfolyamon
        # (pl. Állampolgári ismeretek csak 8.-ban), ugorjuk át a jelöltet.
        if grade_num >= 5 and not _hu_json_applies_to_grade(subject_name, grade_num, "5-8"):
            logger.warning(
                "get_curriculum_for_chat CANDIDATE SKIP: %s not allowed for grade %s",
                subject_name, grade_num,
            )
            continue
        if content or catalog:
            return {
                "found": True,
                "content": content,
                "topics": [t["name"] for t in catalog]
                or curriculum_topic_names(topics),
                "topics_detail": topics,
                "topic_catalog": catalog,
                "file": path.name,
                "subject_name": subject_name,
                "data": data,
                "language": effective_language,
                # Spirális tantárgynál a leckenevek évről évre visszatérnek,
                # ezért nem több lecke kell, hanem évfolyamonként mélyebb
                # tartalom — az app ebből tudja, hogy ilyenkor a promptba
                # évfolyam-specifikus mélységet kell tennie.
                "spiralis": _is_spiral_subject(data, raw_data=raw),
            }

    logger.warning(
        "get_curriculum_for_chat FALLBACK: no matching candidate found, returning found=False "
        "subject_file=%r grade=%s candidates_checked=%s",
        subject_file, grade_num, len(candidates),
    )
    return {
        "found": False,
        "content": "",
        "topics": [],
        "topics_detail": {},
        "topic_catalog": [],
        "file": subject_file,
        "subject_name": display_label,
        "data": {},
        "language": effective_language,
    }


def format_hu_topics_for_prompt(
    topics: dict[str, list[str]],
    *,
    max_categories: int = 12,
    max_items_per_category: int = 6,
) -> str:
    """Tantervi témakörök tömör szöveges összefoglalója AI prompthoz."""
    if not topics:
        return ""
    lines: list[str] = []
    for idx, (category, items) in enumerate(topics.items()):
        if idx >= max_categories:
            lines.append(f"... és még {len(topics) - max_categories} témakör")
            break
        sample = items[:max_items_per_category]
        joined = "; ".join(sample)
        if len(items) > max_items_per_category:
            joined += f" (... összesen {len(items)} követelmény)"
        lines.append(f"- {category}: {joined}")
    return "\n".join(lines)


def get_hu_curriculum_context(
    grade: int, subject: str, *, language: str | None = None
) -> dict[str, Any]:
    """Egy tantárgy teljes tantervi kontextusa feladatgeneráláshoz."""
    grade_num = parse_grade(grade)
    effective_language = (language or "").strip().lower() or None
    resolved = _resolve_hu_subject_file(subject, grade_num)
    if resolved:
        if resolved.get("language"):
            effective_language = resolved["language"]
        subject_lookup = resolved["file"]
    else:
        subject_lookup = subject

    path = find_hu_json_file(grade_num, subject_lookup)
    if not path:
        logger.warning(
            "HU JSON tanterv nem található: subject=%r grade=%s (path keresés: %s)",
            subject,
            grade_num,
            Path(__file__).parent,
        )
        return {
            "found": False,
            "subject": subject,
            "grade": grade_num,
            "topics": {},
            "summary": "",
            "source": "json",
        }

    raw = _load_hu_json(path)
    data = _curriculum_data_for_language(raw, effective_language)
    meta = data.get("meta", {}) or raw.get("meta", {})
    display = _display_subject_name(
        data.get("nyelv") or meta.get("tantargy", subject)
    )
    topics = extract_hu_grade_topics(data, grade_num)
    return {
        "found": True,
        "subject": display,
        "grade": grade_num,
        "file": path.name,
        "topics": topics,
        "summary": format_hu_topics_for_prompt(topics),
        "meta": meta,
        "source": "json",
    }


def get_curriculum_for_child(
    curriculum: str,
    grade: str | int,
    region: str | None = None,
    *,
    subject: str | None = None,
) -> dict[str, Any]:
    """Tantervi kontextus gyerekprofilhoz – tantárgy-lista + (HU) JSON témakörök."""
    base = get_subjects_for_profile(curriculum, grade, region)
    grade_num = base["grade"]
    result: dict[str, Any] = dict(base)

    if curriculum.upper() != "HU" or not subject:
        # LOMLOE spanyol tanterv kontextus
        if curriculum.upper() == "ES" and subject and subject in ES_LOE_FILES:
            loe = get_loe_curriculum_for_chat(subject, grade_num)
            result["subject_context"] = {
                "found": True,
                "subject": loe["subject_name"],
                "grade": grade_num,
                "file": ES_LOE_FILES[subject],
                "topics": loe.get("topics", {}),
                "summary": loe.get("curriculum_body", "")[:500],
                "meta": loe.get("data", {}).get("meta", {}),
                "source": "loe_json",
            }
            result["curriculum_summary"] = result["subject_context"]["summary"]
        return result

    ctx = get_hu_curriculum_context(grade_num, subject)
    result["subject_context"] = ctx
    if ctx.get("summary"):
        result["curriculum_summary"] = ctx["summary"]
    return result


def get_subject_label_for_loe(subject_key: str) -> str:
    """LOMLOE tantárgy emberi neve, magyar címkével."""
    labels = {
        "conocimiento": "Conocimiento del Medio (LOMLOE)",
        "artistica": "Educación Artística (LOMLOE)",
        "fisica": "Educación Física (LOMLOE)",
        "lengua": "Lengua Castellana (LOMLOE)",
        "extranjera": "Lengua Extranjera (LOMLOE)",
        "matematicas": "Matemáticas (LOMLOE)",
        "valores": "Educación en Valores Cívicos y Éticos (LOMLOE)",
    }
    return labels.get(subject_key, subject_key)


def _is_spanish_subject_list(subjects: list[str]) -> bool:
    """Felismeri, ha a lista spanyol tantervi neveket vagy LOMLOE kulcsokat tartalmaz."""
    markers = (
        "matemáticas",
        "lengua castellana",
        "educación artística",
        "conocimiento del medio",
        "lengua extranjera",
        "ciencias de la naturaleza",
        "ciencias sociales",
        "educación física",
        "enseñanzas de religión",
    )
    joined = " ".join(s.casefold() for s in subjects)
    if any(marker in joined for marker in markers):
        return True
    # LOMLOE kulcsok
    loe_keys = frozenset(ES_LOE_FILES.keys())
    return bool(loe_keys.intersection(subjects))


def get_subjects_for_profile(
    curriculum: str,
    grade: str | int,
    region: str | None = None,
) -> dict[str, Any]:
    """Tanterv-specifikus tantárgy-lista – HU: magyar, ES: spanyol (nem UI nyelv!)."""
    curriculum = curriculum.upper()
    grade_num = parse_grade(grade)

    if curriculum == "HU":
        subjects: list[str] = []
        source = "fallback"
        if 1 <= grade_num <= 8:
            try:
                json_subjects = list_hu_subjects_from_json(grade_num)
                if json_subjects and not _is_spanish_subject_list(json_subjects):
                    subjects = json_subjects
                    source = "json"
            except Exception:
                pass
        if not subjects:
            subjects = _hu_fallback(grade_num)
            source = "fallback"
        subjects = _sanitize_hu_subjects(subjects, grade_num)
        return {
            "subjects": subjects,
            "source": source,
            "fetched_at": _now_iso() if source == "json" else None,
            "curriculum": curriculum,
            "grade": grade_num,
            "region": None,
        }

    if curriculum == "ES":
        # LOMLOE tantárgyak spanyol gyerekeknek – évfolyamra szűrve
        # (pl. 'valores' csak 5-6. osztályban / 3_ciclo létezik a BOE szerint).
        subjects = [s["value"] for s in get_loe_subjects_for_grade(grade_num)]
        if subjects:
            return {
                "subjects": subjects,
                "source": "loe_json",
                "fetched_at": _now_iso(),
                "curriculum": curriculum,
                "grade": grade_num,
                "region": region,
            }
        # LOMLOE fájlok nem találhatók – logolás és üres lista visszaadása
        logger.warning(
            "get_subjects_for_profile: LOE files not found at %r (ES_LOE_DIR), "
            "trying fallback with region=%r",
            str(ES_LOE_DIR), region,
        )
        if region:
            return get_subjects(curriculum, grade_num, region)
        # Nincs region → nincs tantárgy lista (hibaüzenet helyett üres lista)
        return {
            "subjects": [],
            "source": "loe_missing",
            "fetched_at": _now_iso(),
            "curriculum": curriculum,
            "grade": grade_num,
            "region": None,
        }

    raise ValueError(f"Ismeretlen tanterv: {curriculum}")


# ---------------------------------------------------------------------------
# HTTP / cache segédek
# ---------------------------------------------------------------------------


def _fetch_url(url: str, *, use_ssl_relax: bool = False) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    ctx = _SSL_CTX if use_ssl_relax else None
    with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
        raw = resp.read()
    for encoding in ("utf-8", "latin-1", "cp1252"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def _cache_path(country: str, grade: int, region: str | None) -> Path:
    region_part = (region or "none").upper()
    return CACHE_DIR / f"{country.upper()}_g{grade}_{region_part}.json"


def _cache_valid(path: Path) -> bool:
    if not path.exists():
        return False
    age_hours = (datetime.now(timezone.utc).timestamp() - path.stat().st_mtime) / 3600
    return age_hours < CACHE_TTL_HOURS


def _read_cache(path: Path) -> dict[str, Any] | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _write_cache(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def parse_grade(grade: str | int) -> int:
    """Osztály / évfolyam szám kinyerése szövegből (pl. '3/a' -> 3)."""
    if isinstance(grade, int):
        return grade
    match = re.search(r"\d+", str(grade))
    if not match:
        raise ValueError(f"Érvénytelen évfolyam: {grade!r}")
    return int(match.group())


def _hu_grade_band(grade: int) -> tuple[str, str]:
    if 1 <= grade <= 4:
        return "lower", "/kozneveles/kerettantervek/2020_nat/kerettanterv_alt_isk_1_4_evf/"
    if 5 <= grade <= 8:
        return "upper", "/kozneveles/kerettantervek/2020_nat/kerettanterv_alt_isk_5_8/"
    if 9 <= grade <= 12:
        return "gimn", "/kozneveles/kerettantervek/2020_nat/kerettanterv_gimn_9_12_evf/"
    raise ValueError(f"Magyar évfolyam tartományon kívül: {grade}")


def _hu_fallback_key(grade: int) -> str:
    if 1 <= grade <= 2:
        return "1-4"
    if grade == 3:
        return "1-4_g3"
    if grade == 4:
        return "1-4_g4"
    if grade in (5, 6):
        return "5-8_g56"
    if grade == 7:
        return "5-8_g78"
    if grade == 8:
        return "5-8_g8"
    return "9-12"


def _hu_fallback(grade: int) -> list[str]:
    return list(FALLBACK_HU[_hu_fallback_key(grade)])


def _es_fallback(grade: int, region: str | None) -> list[str]:
    subjects = list(FALLBACK_ES_BASE)
    if grade >= 5:
        subjects.append("Educación en Valores Cívicos y Éticos")
    subjects.append("Enseñanzas de religión")
    if region and region.upper() in FALLBACK_ES_REGION_EXTRAS:
        subjects.extend(FALLBACK_ES_REGION_EXTRAS[region.upper()])
    return _dedupe(subjects)


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        key = item.casefold()
        if key not in seen:
            seen.add(key)
            out.append(item)
    return out


# ---------------------------------------------------------------------------
# Magyar scraper
# ---------------------------------------------------------------------------

_HU_DOCX_RE = re.compile(
    r"/pub_bin/dload/kozoktatas/kerettanterv/([^\"'?#]+)\.docx",
    re.IGNORECASE,
)


def _docx_to_subject(filename: str) -> str | None:
    if "kozossegi_neveles" in filename.lower():
        return None
    candidates = [
        filename,
        re.sub(r"_jav_\d+$", "", filename),
        re.sub(r"_(A|F)_egyben$", "", filename),
        re.sub(r"_(A|F)$", "", filename),
        re.sub(r"_5_6$", "", filename),
    ]
    for stem in candidates:
        if stem in _HU_DOCX_SUBJECTS:
            return _HU_DOCX_SUBJECTS[stem]
        for key, name in _HU_DOCX_SUBJECTS.items():
            if stem == key or stem.startswith(key + "_"):
                return name
    return None


def _parse_hu_subjects(html: str) -> list[str]:
    subjects: list[str] = []
    for match in _HU_DOCX_RE.finditer(html):
        name = _docx_to_subject(match.group(1))
        if name:
            subjects.append(name)
    return _dedupe(subjects)


def _filter_hu_subjects(subjects: list[str], grade: int, band: str) -> list[str]:
    rules = _HU_GRADE_RULES_LOWER if band == "lower" else _HU_GRADE_RULES_UPPER
    filtered: list[str] = []
    for subject in subjects:
        if subject in rules:
            lo, hi = rules[subject]
            if lo <= grade <= hi:
                filtered.append(subject)
        else:
            filtered.append(subject)
    return filtered


def _fetch_hu_curriculum_page(path: str) -> str:
    last_error: Exception | None = None
    for base in HU_BASE_URLS:
        url = urljoin(base, path)
        try:
            return _fetch_url(url)
        except (urllib.error.URLError, urllib.error.HTTPError) as exc:
            last_error = exc
    raise RuntimeError(f"Magyar kerettanterv oldal nem érhető el: {path}") from last_error


def fetch_hu_subjects(grade: int) -> list[str]:
    band, path = _hu_grade_band(grade)
    html = _fetch_hu_curriculum_page(path)
    subjects = _parse_hu_subjects(html)
    if not subjects:
        raise RuntimeError("Nem található tantárgy a magyar kerettanterv oldalon")
    return _filter_hu_subjects(subjects, grade, band)


# ---------------------------------------------------------------------------
# Spanyol scraper
# ---------------------------------------------------------------------------


class _LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str | None]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        attr_map = dict(attrs)
        href = attr_map.get("href")
        title = attr_map.get("title")
        if href:
            self.links.append((href, title))


def _parse_es_national_areas(html: str) -> list[str]:
    slugs: set[str] = set()
    for match in re.finditer(r"/ed-primaria/areas/([a-z-]+)\.html", html):
        slug = match.group(1)
        if slug.startswith("criterios") or slug == "desarrollo-areas":
            continue
        slugs.add(slug)
    subjects = [_ES_AREA_SLUGS[s] for s in slugs if s in _ES_AREA_SLUGS]
    return _dedupe(subjects)


def _filter_es_subjects(subjects: list[str], grade: int) -> list[str]:
    filtered: list[str] = []
    for subject in subjects:
        if subject == "Educación en Valores Cívicos y Éticos" and grade < 5:
            continue
        filtered.append(subject)
    return filtered


def _fetch_es_community_url(region: str) -> str | None:
    region = region.upper()
    title = _ES_REGION_TITLES.get(region)
    if not title:
        return None
    html = _fetch_url(ES_BASE_URL + ES_COMMUNITIES_PATH, use_ssl_relax=True)
    parser = _LinkParser()
    parser.feed(html)
    for href, link_title in parser.links:
        if link_title == title and href.startswith("http"):
            return href
    # Lista elemek span title alapján
    for href, link_title in parser.links:
        if link_title and title.split(" (")[0] in link_title and href.startswith("http"):
            return href
    return None


def _parse_es_community_html(html: str) -> list[str]:
    text = unescape(re.sub(r"<[^>]+>", " ", html))
    text = re.sub(r"\s+", " ", text)
    found: list[str] = []
    for pattern in _ES_SUBJECT_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            found.append(pattern if pattern[0].isupper() else pattern.capitalize())
    # Normalizálás ismert nevekre
    normalized: list[str] = []
    for item in found:
        for canonical in _ES_AREA_SLUGS.values():
            if canonical.lower() in item.lower() or item.lower() in canonical.lower():
                normalized.append(canonical)
                break
        else:
            normalized.append(item)
    return _dedupe(normalized)


def _is_pdf_url(url: str) -> bool:
    return url.lower().split("?")[0].endswith(".pdf")


def fetch_es_subjects(grade: int, region: str) -> list[str]:
    areas_html = _fetch_url(ES_BASE_URL + ES_AREAS_PATH, use_ssl_relax=True)
    subjects = _parse_es_national_areas(areas_html)
    if not subjects:
        raise RuntimeError("Nem található área a spanyol currículum oldalon")

    community_url = _fetch_es_community_url(region)
    community_extra: list[str] = []
    if community_url:
        if _is_pdf_url(community_url):
            community_extra = FALLBACK_ES_REGION_EXTRAS.get(region.upper(), [])
        else:
            try:
                community_html = _fetch_url(community_url, use_ssl_relax=True)
                community_extra = _parse_es_community_html(community_html)
            except (urllib.error.URLError, urllib.error.HTTPError):
                community_extra = FALLBACK_ES_REGION_EXTRAS.get(region.upper(), [])

    if not community_extra:
        community_extra = FALLBACK_ES_REGION_EXTRAS.get(region.upper(), [])

    subjects = _dedupe(subjects + community_extra)

    return _filter_es_subjects(subjects, grade)


# ---------------------------------------------------------------------------
# Publikus API
# ---------------------------------------------------------------------------


def get_subjects(
    country: str,
    grade: str | int,
    region: str | None = None,
    *,
    force_refresh: bool = False,
) -> dict[str, Any]:
    """Tantárgy-lista lekérése cache-sel és fallbackkel.

    Args:
        country: 'HU' vagy 'ES'
        grade: évfolyam / osztály (szám vagy szöveg)
        region: spanyol autonóm közösség kódja (ES esetén kötelező)
        force_refresh: True esetén újra letölti, cache figyelmen kívül hagyása

    Returns:
        dict: subjects, source ('live'|'cache'|'fallback'), fetched_at, meta
    """
    country = country.upper()
    grade_num = parse_grade(grade)
    cache_file = _cache_path(country, grade_num, region)

    if not force_refresh and _cache_valid(cache_file):
        cached = _read_cache(cache_file)
        if cached and cached.get("subjects"):
            cached_country = (cached.get("country") or country).upper()
            subjects = cached.get("subjects", [])
            if cached_country == country and not (
                country == "HU" and _is_spanish_subject_list(subjects)
            ):
                if country == "HU":
                    cached["subjects"] = _sanitize_hu_subjects(subjects, grade_num)
                cached["source"] = "cache"
                return cached

    try:
        if country == "HU":
            json_subjects = list_hu_subjects_from_json(grade_num)
            if json_subjects:
                json_subjects = _sanitize_hu_subjects(json_subjects, grade_num)
                payload = {
                    "subjects": json_subjects,
                    "source": "json",
                    "fetched_at": _now_iso(),
                    "country": country,
                    "grade": grade_num,
                    "region": None,
                }
                _write_cache(cache_file, payload)
                return payload
            subjects = fetch_hu_subjects(grade_num)
        elif country == "ES":
            if not region:
                raise ValueError("Spanyolország esetén kötelező a region paraméter")
            subjects = fetch_es_subjects(grade_num, region)
        else:
            raise ValueError(f"Ismeretlen ország: {country}")

        payload = {
            "subjects": subjects,
            "source": "live",
            "fetched_at": _now_iso(),
            "country": country,
            "grade": grade_num,
            "region": region.upper() if region else None,
        }
        _write_cache(cache_file, payload)
        return payload

    except Exception:
        if country == "HU":
            subjects = _hu_fallback(grade_num)
        elif country == "ES":
            subjects = _es_fallback(grade_num, region)
        else:
            raise

        payload = {
            "subjects": subjects,
            "source": "fallback",
            "fetched_at": None,
            "country": country,
            "grade": grade_num,
            "region": region.upper() if region else None,
        }
        _write_cache(cache_file, payload)
        return payload


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Használat: python curriculum_loader.py HU 3")
        print("           python curriculum_loader.py ES 4 CT")
        raise SystemExit(1)

    c = sys.argv[1]
    g = sys.argv[2]
    r = sys.argv[3] if len(sys.argv) > 3 else None
    result = get_subjects(c, g, r, force_refresh=True)
    print(json.dumps(result, ensure_ascii=False, indent=2))
