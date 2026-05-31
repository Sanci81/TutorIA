"""Tantárgy-listák betöltése hivatalos forrásokból (HU / ES).

Magyarország: kerettanterv.oh.gov.hu (tükör: oktatas.hu)
Spanyolország: educagob.educacionfpydeportes.gob.es + autonóm közösség oldalak

Az eredmény fájl-cache-be kerül; sikertelen lekérés esetén fallback lista.
"""

from __future__ import annotations

import json
import os
import re
import ssl
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
    "elo_idegen_nyelv_A_egyben": "Első élő idegen nyelv",
    "elo_idegen_nyelv_F_egyben": "Első élő idegen nyelv",
    "elo_idegen_nyelv": "Első élő idegen nyelv",
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
    "Első élő idegen nyelv": (4, 4),
}

_HU_GRADE_RULES_UPPER: dict[str, tuple[int, int]] = {
    "Természettudomány": (5, 6),
    "Technika és tervezés": (5, 7),
    "Kémia": (7, 8),
    "Fizika": (7, 8),
    "Biologia": (7, 8),
    "Földrajz": (7, 8),
    "Dráma és színház": (7, 8),
    "Állampolgári ismeretek": (8, 8),
}

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
        "Első élő idegen nyelv",
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
            cached["source"] = "cache"
            return cached

    try:
        if country == "HU":
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
