"""TutorIA – Flask alkalmazás.

Funkciók (1. fázis):
  - Szülői regisztráció és bejelentkezés
  - Gyerek profil létrehozása (ország ES/HU, ES esetén autonóm közösség)
  - Vezérlőpult a gyerek kártyákkal
  - Kétnyelvű felület (magyar / spanyol) nyelvváltóval
"""

import json
import logging
import os
import re
import traceback
from datetime import date, datetime, timezone, timedelta
from functools import wraps
from typing import Any

from flask import (
    Flask,
    Response,
    abort,
    flash,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
import resend
from werkzeug.security import check_password_hash, generate_password_hash

import database
import translations as i18n
from curriculum_loader import (
    ELO_IDEGEN_NYELV_1_4_FILE,
    ELO_IDEGEN_NYELV_5_8_FILE,
    foreign_language_prompt_block,
    get_curriculum_for_chat,
    get_curriculum_for_child,
    get_hu_subjects_for_grade,
    get_subject_options_for_ui,
    get_subjects_for_profile,
    get_topic_from_catalog,
    hu_1_4_label_from_value,
    is_elo_idegen_subject,
    is_hu_1_4_grade,
    parse_grade,
    subject_ui_label,
)
from database import RESET_TOKEN_HOURS

logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-insecure-key")

# Railway HTTPS linkekhez (elfelejtett jelszó e-mail)
app.config["PREFERRED_URL_SCHEME"] = os.environ.get("PREFERRED_URL_SCHEME", "https")

try:
    database.init_db()
except Exception:
    logger.exception("Adatbázis inicializálás sikertelen induláskor")


# ---------------------------------------------------------------------------
# Nyelv kezelés
# ---------------------------------------------------------------------------

@app.before_request
def load_language():
    """Beállítja az aktuális nyelvet (session alapján)."""
    lang = session.get("lang", i18n.DEFAULT_LANG)
    if lang not in i18n.LANGUAGES:
        lang = i18n.DEFAULT_LANG
    g.lang = lang


@app.context_processor
def inject_helpers():
    """Sablonokban elérhetővé teszi a fordítót és a nyelvi adatokat."""
    return {
        "t": lambda key: i18n.t(key, g.lang),
        "lang": g.lang,
        "languages": i18n.LANGUAGES,
        "region_name": lambda code: i18n.region_name(code, g.lang),
        "spanish_regions": i18n.SPANISH_REGIONS,
    }


@app.route("/lang/<lang_code>")
def set_language(lang_code):
    if lang_code in i18n.LANGUAGES:
        session["lang"] = lang_code
    # Visszairányítás az előző oldalra, vagy a főoldalra
    return redirect(request.referrer or url_for("index"))


# ---------------------------------------------------------------------------
# Segédek
# ---------------------------------------------------------------------------

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "parent_id" not in session:
            flash(i18n.t("flash_login_required", g.lang), "info")
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped


def _mail_is_configured() -> bool:
    return bool(os.environ.get("RESEND_API_KEY"))


def _resend_from_address() -> str:
    return os.environ.get("RESEND_FROM", "TutorIA <onboarding@resend.dev>")


def _reset_password_url(token: str) -> str:
    """Visszaállító link – Railway-en APP_URL env ajánlott."""
    app_url = (os.environ.get("APP_URL") or os.environ.get("RAILWAY_PUBLIC_DOMAIN") or "").rstrip(
        "/"
    )
    path = url_for("reset_password", token=token, _external=False)
    if app_url:
        if not app_url.startswith("http"):
            app_url = f"https://{app_url}"
        return f"{app_url}{path}"
    return url_for("reset_password", token=token, _external=True)


def _send_password_reset_email(recipient: str, token: str, lang: str) -> None:
    api_key = os.environ.get("RESEND_API_KEY")
    if not api_key:
        raise RuntimeError("RESEND_API_KEY nincs beállítva")

    reset_url = _reset_password_url(token)
    subjects = {
        "hu": "TutorIA – Jelszó visszaállítása",
        "es": "TutorIA – Restablecer contraseña",
    }
    bodies = {
        "hu": (
            "Kérted a TutorIA jelszavad visszaállítását.\n\n"
            f"Kattints az alábbi linkre ({RESET_TOKEN_HOURS} órán belül érvényes):\n{reset_url}\n\n"
            "Ha nem te kérted, hagyd figyelmen kívül ezt az e-mailt."
        ),
        "es": (
            "Has solicitado restablecer tu contraseña de TutorIA.\n\n"
            f"Haz clic en el siguiente enlace (válido durante {RESET_TOKEN_HOURS} horas):\n{reset_url}\n\n"
            "Si no lo solicitaste, ignora este correo."
        ),
    }

    resend.api_key = api_key
    resend.Emails.send(
        {
            "from": _resend_from_address(),
            "to": [recipient],
            "subject": subjects.get(lang, subjects["hu"]),
            "text": bodies.get(lang, bodies["hu"]),
        }
    )


def _curriculum_for_child(child: dict, *, subject: str | None = None) -> dict:
    """Tanterv a gyerek profiljához; HU esetén JSON témakörökkel."""
    region = child["region"] if child["country"] == "ES" else None
    if child["country"] == "HU" and subject:
        return get_curriculum_for_child(
            child["country"], child["grade"], region, subject=subject
        )
    return get_subjects_for_profile(child["country"], child["grade"], region)


def _build_task_generation_prompt(
    child: dict,
    curriculum: dict,
    *,
    subject: str | None = None,
    subject_display: str | None = None,
    lang: str,
    foreign_language: str | None = None,
) -> str:
    """AI prompt – hivatalos tantervi tantárgyak és (HU) JSON témakörök."""
    subjects = curriculum["subjects"]
    subject_line = subject_display or subject or (subjects[0] if subjects else "általános")
    location = child["country"]
    if child.get("region"):
        location = f"{location} ({child['region']})"

    topic_block = ""
    ctx = curriculum.get("subject_context") or {}
    summary = ctx.get("summary") or ""
    if summary:
        if len(summary) > 2500:
            summary = summary[:2500] + "\n..."
        topic_block = (
            f"\nHivatalos tantervi témakörök ({ctx.get('subject', subject_line)}, "
            f"{curriculum.get('grade', child['grade'])}. évfolyam):\n{summary}\n"
        )

    child_age = _child_effective_age(child)
    if lang == "es":
        prompt = (
            f"Genera 3 ejercicios de práctica para un/a niño/a de {child_age} años, "
            f"curso {child['grade']}, ubicación {location}.\n"
            f"Tema / asignatura: {subject_line}\n"
            f"Asignaturas del currículo oficial: {', '.join(subjects)}\n"
        )
        if topic_block:
            prompt += topic_block.replace("Hivatalos", "Contenido oficial")
        prompt += (
            "Los ejercicios deben alinearse con el currículo anterior, "
            "ser apropiados para la edad y el curso, y tener dificultad moderada."
        )
        return prompt

    prompt = (
        f"Készíts 3 gyakorló feladatot egy {child_age} éves gyereknek, "
        f"{child['grade']}. osztály, helyszín: {location}.\n"
        f"Tantárgy: {subject_line}\n"
        f"Hivatalos tantervi tantárgyak: {', '.join(subjects)}\n"
    )
    if topic_block:
        prompt += topic_block
    if foreign_language:
        prompt += foreign_language_prompt_block(foreign_language)
    prompt += (
        "A feladatok illeszkedjenek a fenti hivatalos tantervi témakörökhöz, "
        "legyenek életkornak és osztály szintnek megfelelőek, közepes nehézségűek."
    )
    return prompt


def _openai_api_key() -> str | None:
    """OpenAI kulcs – OPENAI_API_KEY vagy OPENAI_KEY env-ből."""
    return os.environ.get("OPENAI_API_KEY") or os.environ.get("OPENAI_KEY")


def _openai_client(api_key: str, *, request_timeout: float = 90.0):
    """OpenAI kliens httpx timeout-tal (Railway connection error ellen)."""
    import httpx
    from openai import OpenAI

    return OpenAI(
        api_key=api_key,
        timeout=httpx.Timeout(request_timeout, connect=10.0),
        max_retries=2,
    )


def _call_ai_for_tasks(
    prompt: str,
    *,
    lang: str,
    foreign_language: str | None = None,
    curriculum_text: str = "",
    grade_num: int = 1,
    subject_label: str = "",
) -> list[dict]:
    """OpenAI (gpt-4o-mini) hívás – 3 gyakorló feladat JSON formában."""
    api_key = _openai_api_key()
    if not api_key:
        logger.error("Task generation: OPENAI_API_KEY / OPENAI_KEY nincs beállítva")
        raise NotImplementedError("OPENAI_API_KEY nincs beállítva")

    logger.info(
        "curriculum_text length=%d grade=%d subject=%s",
        len(curriculum_text), grade_num, subject_label,
    )

    # Kerettanterv blokk – minden system prompt ELEJÉN
    curriculum_block = f"""
KIZÁRÓLAG a következő hivatalos kerettanterv alapján generálj feladatokat.
Tilos kitalálni bármit ami nincs a tantervben.

TILOS:
- Rajzolásra utasítani (nincs papír a képernyőn)
- Képekre, ábrákra hivatkozni
- Magyar nyelv tantárgynál matematikai feladatot adni
- Matematikánál irodalmi feladatot adni
- Olyan feladatot adni ami nem szerepel a kerettantervben

KÖTELEZŐ:
- A feladat egyértelműen megoldható szóban/írásban
- Az adott tantárgy és osztály szintjének PONTOSAN megfeleljen
- Minden szükséges adat benne legyen a kérdésben (ne hivatkozzon külső dologra)

KERETTANTERV ({grade_num}. osztály, {subject_label}):
{curriculum_text}
""" if curriculum_text and len(curriculum_text) > 200 else ""

    logger.info(
        "curriculum_block length=%d used=%s",
        len(curriculum_block), "yes" if curriculum_block else "no",
    )

    if foreign_language == "angol":
        system_hu = curriculum_block + (
            "Te egy tapasztalt angol nyelvtanár vagy magyar általános iskolásoknak. "
            "A feladatok tartalma kizárólag angol nyelven legyen. "
            "Válaszolj kizárólag érvényes JSON-nal; a task mezők angolul legyenek."
        )
    elif foreign_language == "nemet":
        system_hu = curriculum_block + (
            "Te egy tapasztalt német nyelvtanár vagy magyar általános iskolásoknak. "
            "A feladatok tartalma kizárólag német nyelven legyen. "
            "Válaszolj kizárólag érvényes JSON-nal; a task mezők németül legyenek."
        )
    elif foreign_language == "spanyol":
        system_hu = curriculum_block + (
            "Te egy tapasztalt spanyol nyelvtanár vagy magyar általános iskolásoknak. "
            "A feladatok tartalma kizárólag spanyol nyelven legyen. "
            "Válaszolj kizárólag érvényes JSON-nal; a task mezők spanyolul legyenek."
        )
    else:
        system_hu = curriculum_block + (
            "Te egy tapasztalt magyar tanár vagy. A megadott hivatalos NAT 2020 "
            "kerettantervi témakörök alapján készíts gyakorló feladatokat. "
            "Válaszolj kizárólag érvényes JSON-nal, magyar nyelven.\n\n"
            "A feladatok legyenek nyelvtanilag helyesek magyarul.\n"
            "Összehasonlító kérdéseknél használj '-ból/-ből' ragot: "
            "'Melyikből van több?' nem 'Melyik van több?'\n"
            "A feladatok legyenek pontosan az adott osztály szintjének megfelelők."
        )
    system_es = curriculum_block + (
        "Eres un/a profesor/a experimentado/a. Crea ejercicios según el currículo "
        "oficial indicado. Responde solo con JSON válido en español."
    )
    user_suffix_hu = (
        'Add vissza JSON objektumként: {"tasks": [{"title": "...", "question": "...", '
        '"hint": "...", "answer": "..."}, ...]} – pontosan 3 feladat.'
    )
    user_suffix_es = (
        'Devuelve un objeto JSON: {"tasks": [{"title": "...", "question": "...", '
        '"hint": "...", "answer": "..."}, ...]} – exactamente 3 ejercicios.'
    )

    user_content = prompt + (user_suffix_es if lang == "es" else user_suffix_hu)
    logger.info(
        "OpenAI task request: model=gpt-4o-mini lang=%s prompt_chars=%d",
        lang,
        len(user_content),
    )

    raw = ""
    try:
        client = _openai_client(api_key, request_timeout=90.0)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": system_es if lang == "es" else system_hu,
                },
                {"role": "user", "content": user_content},
            ],
            temperature=0.7,
        )
        raw = response.choices[0].message.content or "{}"
        logger.info("OpenAI response received: chars=%d", len(raw))
    except ImportError as exc:
        logger.exception("OpenAI csomag nincs telepítve – pip install openai")
        raise RuntimeError(
            "OpenAI csomag hiányzik a szerverről. Telepítsd: pip install openai"
        ) from exc
    except Exception as exc:
        logger.exception(
            "OpenAI API hívás sikertelen (%s): %s",
            type(exc).__name__,
            exc,
        )
        raise RuntimeError(f"OpenAI API hiba: {type(exc).__name__}: {exc}") from exc

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        logger.error(
            "OpenAI JSON feldolgozás sikertelen: %s | raw_preview=%r",
            exc,
            raw[:800],
        )
        raise RuntimeError(f"AI válasz nem érvényes JSON: {exc}") from exc

    tasks = payload.get("tasks", payload if isinstance(payload, list) else [])
    if not isinstance(tasks, list) or not tasks:
        logger.error(
            "OpenAI válasz üres vagy hibás tasks mező: keys=%s preview=%r",
            list(payload.keys()) if isinstance(payload, dict) else type(payload),
            raw[:800],
        )
        raise RuntimeError("Az AI nem adott vissza feladatlistát")

    normalized: list[dict] = []
    for idx, task in enumerate(tasks[:3], start=1):
        if not isinstance(task, dict):
            logger.warning("Task #%d nem dict: %r", idx, task)
            continue
        normalized.append(
            {
                "title": task.get("title") or f"Feladat {idx}",
                "question": task.get("question") or task.get("text") or "",
                "hint": task.get("hint") or "",
                "answer": task.get("answer") or "",
            }
        )

    if not normalized:
        raise RuntimeError("Az AI válaszából nem sikerült feladatot kinyerni")

    return normalized


def _tasks_session_key(child_id: int) -> str:
    return f"practice_tasks_{child_id}"


def _generate_practice_tasks_bundle(
    child_id: int,
    child: dict,
    subject: str,
    language: str | None,
) -> tuple[list[dict], dict, str, str | None] | None:
    """
    Feladatgenerálás – tanterv + OpenAI.
    Vissza: (tasks, curriculum, subject_label, foreign_language) vagy None hiba esetén.
    """
    subject = (subject or "").strip()
    language = (language or "").strip().lower() or None

    if not subject:
        flash(i18n.t("flash_subject_required", g.lang), "error")
        return None

    grade_num = parse_grade(child["grade"])
    if g.lang == "hu":
        allowed_files = {o["value"] for o in get_hu_subjects_for_grade(grade_num)}
        if subject not in allowed_files:
            flash(i18n.t("flash_subject_required", g.lang), "error")
            return None
        idegen_files = (ELO_IDEGEN_NYELV_1_4_FILE, ELO_IDEGEN_NYELV_5_8_FILE)
        if subject in idegen_files and language not in ("angol", "nemet", "spanyol"):
            flash(i18n.t("flash_language_required", g.lang), "error")
            return None
        if subject not in idegen_files:
            language = None
    else:
        region = child["region"] if child["country"] == "ES" else None
        try:
            available = get_subjects_for_profile(
                child["country"], child["grade"], region
            ).get("subjects", [])
        except Exception:
            available = []
        if available and subject not in available:
            flash(i18n.t("flash_subject_required", g.lang), "error")
            return None
        language = None

    subject_display = hu_1_4_label_from_value(subject)
    curriculum = _curriculum_for_child(child, subject=subject)
    subject_ctx = curriculum.get("subject_context") or {}
    if child["country"] == "HU":
        if subject_ctx.get("found"):
            logger.info(
                "Tanterv JSON betöltve: subject=%s file=%s child_id=%s",
                subject,
                subject_ctx.get("file"),
                child_id,
            )
        else:
            logger.warning(
                "Tanterv JSON nem található (generálás JSON nélkül folytatódik): "
                "subject=%s grade=%s child_id=%s",
                subject,
                child["grade"],
                child_id,
            )

    # Teljes kerettanterv szöveg a feladat promptba (get_curriculum_for_chat).
    curriculum_chat = (
        get_curriculum_for_chat(subject, child["grade"], language=language)
        if child["country"] == "HU"
        else None
    )
    curriculum_text = curriculum_chat.get("content", "") if curriculum_chat else ""

    if not curriculum_text or len(curriculum_text) < 100:
        if curriculum_chat and curriculum_chat.get("data"):
            from curriculum_loader import _hu_evfolyam_blokk_for_grade

            data = curriculum_chat["data"]
            blokk = _hu_evfolyam_blokk_for_grade(data, grade_num)
            if blokk:
                curriculum_text = blokk.get("teljes_szoveg", "")
        if not curriculum_text:
            if curriculum_chat and curriculum_chat.get("data"):
                data = curriculum_chat["data"]
                curriculum_text = data.get("teljes_szoveg", "")

    logger.warning(
        "CURRICULUM DEBUG: subject=%s grade=%s len=%d content_preview=%s",
        subject_display,
        grade_num,
        len(curriculum_text),
        curriculum_text[:200],
    )

    curriculum["content"] = curriculum_text
    logger.info(
        "FINAL curriculum_text len=%d grade=%s subject=%s language=%s",
        len(curriculum_text), child["grade"], subject, language,
    )

    if is_elo_idegen_subject(subject):
        if language == "spanyol":
            foreign_language = "spanyol"
        elif language in ("angol", "nemet"):
            foreign_language = language
        else:
            foreign_language = None
    else:
        foreign_language = None

    prompt = _build_task_generation_prompt(
        child,
        curriculum,
        subject=subject,
        subject_display=subject_display,
        lang=g.lang,
        foreign_language=foreign_language,
    )

    api_key = _openai_api_key()
    if not api_key:
        logger.error("OPENAI_API_KEY hiányzik (child_id=%s)", child_id)
        flash(i18n.t("flash_tasks_failed", g.lang), "error")
        return None

    try:
        tasks = _call_ai_for_tasks(
            prompt,
            lang=g.lang,
            foreign_language=foreign_language,
            curriculum_text=curriculum.get("content", ""),
            grade_num=grade_num,
            subject_label=subject_display,
        )
    except NotImplementedError:
        flash(i18n.t("flash_tasks_pending", g.lang), "info")
        return None
    except Exception as exc:
        tb = traceback.format_exc()
        logger.error(
            "Feladatgenerálás sikertelen (child_id=%s): %s\n%s",
            child_id,
            exc,
            tb,
        )
        print(tb, flush=True)
        flash(i18n.t("flash_tasks_failed", g.lang), "error")
        return None

    subject_label = (
        subject_display
        if g.lang == "hu"
        else subject_ui_label(subject, g.lang, child["country"])
    )
    return tasks, curriculum, subject_label, foreign_language


def _render_practice_tasks_page(
    child_id: int,
    child: dict,
    *,
    tasks: list[dict],
    curriculum: dict,
    subject: str,
    subject_label: str,
    language: str | None,
) -> str:
    session[_tasks_session_key(child_id)] = {
        "tasks": tasks,
        "subject": subject,
        "language": language or "",
        "lang": g.lang,
    }
    session.modified = True
    effective_age = _child_effective_age(child)
    return render_template(
        "tasks.html",
        child=child,
        tasks=tasks,
        curriculum=curriculum,
        subject=subject,
        subject_label=subject_label,
        effective_age=effective_age,
        tasks_voice_young=effective_age <= 7,
    )


def _call_ai_check_task_answer(
    child: dict,
    task: dict,
    user_answer: str,
    *,
    lang: str,
) -> dict[str, Any]:
    """Tanuló válaszának ellenőrzése – helyes / visszajelzés."""
    api_key = _openai_api_key()
    if not api_key:
        raise NotImplementedError("OPENAI_API_KEY nincs beállítva")

    age = _child_effective_age(child)
    question = task.get("question") or ""
    reference = task.get("answer") or ""
    if lang == "es":
        system = (
            "Eres un/a profesor/a paciente de primaria. Evalúas la respuesta del alumno. "
            "Responde SOLO con JSON válido."
        )
        user_msg = (
            f"Alumno: {child['name']}, {age} años, curso {child['grade']}.\n"
            f"Ejercicio: {question}\n"
            f"Solución de referencia (profesor): {reference}\n"
            f"Respuesta del alumno: {user_answer}\n\n"
            'JSON: {"correct": true o false, "feedback": "mensaje corto y amable"}\n'
            "Si es correcta: felicita brevemente.\n"
            "Si no: explica por qué no encaja y cómo pensar el problema, "
            "SIN dar la solución completa."
        )
    else:
        system = (
            "Te egy türelmes magyar általános iskolai tanár vagy. "
            "A tanuló válaszát értékeled. Válaszolj KIZÁRÓLAG érvényes JSON-nal."
        )
        user_msg = (
            f"Tanuló: {child['name']}, {age} éves, {child['grade']}. osztály.\n"
            f"Feladat: {question}\n"
            f"Helyes megoldás (tanári referencia): {reference}\n"
            f"Tanuló válasza: {user_answer}\n\n"
            'JSON: {"correct": true vagy false, "feedback": "rövid, barátságos üzenet"}\n'
            "Ha helyes: rövid dicséret.\n"
            "Ha nem helyes: mondd el miért nem jó, és hogyan gondolkodjon tovább – "
            "NE add meg a teljes helyes választ."
        )

    client = _openai_client(api_key, request_timeout=45.0)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user_msg},
        ],
        temperature=0.4,
    )
    raw = response.choices[0].message.content or "{}"
    payload = json.loads(raw)
    correct = bool(payload.get("correct"))
    feedback = (payload.get("feedback") or "").strip()
    if not feedback:
        feedback = (
            "Szép munka, ez így helyes! 🌟"
            if correct
            else "Még nem teljesen jó – gondolkodj tovább! 💪"
        )
    return {"correct": correct, "feedback": feedback}


# ---------------------------------------------------------------------------
# Útvonalak
# ---------------------------------------------------------------------------

@app.route("/test-openai")
def test_openai():
    """Egyszerű OpenAI diagnosztika – plain text válasz."""
    try:
        api_key = _openai_api_key()
        if not api_key:
            return "ERROR: OpenAI API key missing", 500

        client = _openai_client(api_key, request_timeout=30.0)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Say hello in one word."}],
            max_tokens=10,
        )
        return f"OK: {response.choices[0].message.content}"
    except Exception as e:
        logger.exception("test-openai sikertelen")
        return f"ERROR: {str(e)}", 500


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip()
        password = request.form.get("password") or ""
        confirm = request.form.get("password_confirm") or ""

        if len(password) < 6:
            flash(i18n.t("flash_password_short", g.lang), "error")
            return render_template("register.html", email=email)

        if password != confirm:
            flash(i18n.t("flash_password_mismatch", g.lang), "error")
            return render_template("register.html", email=email)

        parent_id = database.create_parent(email, generate_password_hash(password))
        if parent_id is None:
            flash(i18n.t("flash_email_taken", g.lang), "error")
            return render_template("register.html", email=email)

        session["parent_id"] = parent_id
        flash(i18n.t("flash_registered", g.lang), "success")
        return redirect(url_for("dashboard"))

    return render_template("register.html", email="")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip()
        password = request.form.get("password") or ""

        parent = database.get_parent_by_email(email)
        if parent and check_password_hash(parent["password_hash"], password):
            session["parent_id"] = parent["id"]
            return redirect(url_for("dashboard"))

        flash(i18n.t("flash_invalid_login", g.lang), "error")
        return render_template("login.html", email=email)

    return render_template("login.html", email="")


@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip()
        lang = g.lang

        try:
            parent = database.get_parent_by_email(email)
            if parent:
                if not _mail_is_configured():
                    logger.error("E-mail küldés: RESEND_API_KEY hiányzik")
                    flash(i18n.t("flash_reset_email_failed", lang), "error")
                    return render_template("forgot_password.html", email=email)

                token = database.create_password_reset_token(parent["id"])
                _send_password_reset_email(parent["email"], token, lang)
        except Exception:
            logger.exception("Elfelejtett jelszó feldolgozás sikertelen")
            flash(i18n.t("flash_reset_email_failed", lang), "error")
            return render_template("forgot_password.html", email=email)

        flash(i18n.t("flash_reset_email_sent", lang), "success")
        return redirect(url_for("login"))

    return render_template("forgot_password.html", email="")


@app.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    try:
        reset_row = database.get_password_reset_by_token(token)
    except Exception:
        logger.exception("Token ellenőrzés sikertelen")
        flash(i18n.t("flash_invalid_reset_token", g.lang), "error")
        return redirect(url_for("forgot_password"))

    if not reset_row:
        flash(i18n.t("flash_invalid_reset_token", g.lang), "error")
        return redirect(url_for("forgot_password"))

    if request.method == "POST":
        password = request.form.get("password") or ""
        confirm = request.form.get("password_confirm") or ""

        if len(password) < 6:
            flash(i18n.t("flash_password_short", g.lang), "error")
            return render_template("reset_password.html", token=token)

        if password != confirm:
            flash(i18n.t("flash_password_mismatch", g.lang), "error")
            return render_template("reset_password.html", token=token)

        database.update_parent_password(
            reset_row["parent_id"], generate_password_hash(password)
        )
        database.mark_reset_token_used(reset_row["id"])
        flash(i18n.t("flash_password_reset_success", g.lang), "success")
        return redirect(url_for("login"))

    return render_template("reset_password.html", token=token)


@app.route("/logout")
def logout():
    session.pop("parent_id", None)
    flash(i18n.t("flash_logged_out", g.lang), "info")
    return redirect(url_for("index"))


@app.route("/dashboard")
@login_required
def dashboard():
    parent = database.get_parent_by_id(session["parent_id"])
    children = database.get_children_for_parent(session["parent_id"])
    today = date.today()
    for child in children:
        bd_str = child.get("birth_date")
        if bd_str:
            try:
                bd = date.fromisoformat(bd_str)
                child["is_birthday"] = bd.month == today.month and bd.day == today.day
            except (ValueError, TypeError):
                child["is_birthday"] = False
        else:
            child["is_birthday"] = False
    return render_template("dashboard.html", parent=parent, children=children)


def _parse_birth_date_form(raw: str) -> date | None:
    """YYYY-MM-DD űrlapmező."""
    text = (raw or "").strip()[:10]
    if not text:
        return None
    try:
        born = date.fromisoformat(text)
    except ValueError:
        return None
    if born > date.today():
        return None
    return born


@app.route("/children/add", methods=["GET", "POST"])
@login_required
def add_child():
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        birth_date_raw = request.form.get("birth_date") or ""
        grade = (request.form.get("grade") or "").strip()
        country = request.form.get("country") or ""
        region = request.form.get("region") or None

        errors = False
        birth_date = _parse_birth_date_form(birth_date_raw)
        if not birth_date:
            errors = True

        if not name or country not in ("ES", "HU") or not grade:
            errors = True

        if country == "ES" and not region:
            flash(i18n.t("flash_region_required", g.lang), "error")
            errors = True

        if errors:
            return render_template(
                "add_child.html",
                form={
                    "name": name,
                    "birth_date": birth_date_raw,
                    "grade": grade,
                    "country": country,
                    "region": region,
                },
            )

        if country != "ES":
            region = None

        database.create_child(
            session["parent_id"], name, birth_date, grade, country, region
        )
        flash(i18n.t("flash_child_added", g.lang), "success")
        return redirect(url_for("dashboard"))

    return render_template("add_child.html", form={})


@app.route("/children/<int:child_id>/edit", methods=["GET", "POST"])
@login_required
def edit_child(child_id: int):
    child = database.get_child_by_id(child_id, session["parent_id"])
    if not child:
        abort(404)

    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        birth_date_raw = request.form.get("birth_date") or ""
        grade = (request.form.get("grade") or "").strip()
        country = request.form.get("country") or ""
        region = request.form.get("region") or None

        errors = False
        birth_date = _parse_birth_date_form(birth_date_raw)
        if not birth_date:
            errors = True

        if not name or country not in ("ES", "HU") or not grade:
            errors = True

        if country == "ES" and not region:
            flash(i18n.t("flash_region_required", g.lang), "error")
            errors = True

        if errors:
            return render_template(
                "edit_child.html",
                child=child,
                form={
                    "name": name,
                    "birth_date": birth_date_raw,
                    "grade": grade,
                    "country": country,
                    "region": region,
                },
            )

        if country != "ES":
            region = None

        database.update_child(
            child_id,
            session["parent_id"],
            name=name,
            birth_date=birth_date,
            grade=grade,
            country=country,
            region=region,
        )
        flash(i18n.t("flash_child_updated", g.lang), "success")
        return redirect(url_for("dashboard"))

    form = {
        "name": child["name"],
        "birth_date": child.get("birth_date") or "",
        "grade": child["grade"],
        "country": child["country"],
        "region": child.get("region") or "",
    }
    return render_template("edit_child.html", child=child, form=form)


@app.route("/children/<int:child_id>/tasks", methods=["GET"])
@login_required
def select_tasks(child_id: int):
    """Tantárgy választása feladatgeneráláshoz."""
    child = database.get_child_by_id(child_id, session["parent_id"])
    if not child:
        abort(404)

    grade_num = parse_grade(child["grade"])

    # Mindig g.lang alapján dönt, nem country alapján
    if g.lang == "hu":
        subject_options = get_hu_subjects_for_grade(grade_num)
        curriculum = {
            "subjects": [o["label"] for o in subject_options],
            "source": "json",
            "grade": grade_num,
        }
    else:
        region = child["region"] if child["country"] == "ES" else None
        try:
            curriculum, subject_options = get_subject_options_for_ui(
                child["country"], child["grade"], region, g.lang
            )
        except Exception:
            curriculum = {"subjects": []}
            subject_options = []

    effective_age = _child_effective_age(child)
    chat_profile = _chat_interaction_profile(effective_age)

    return render_template(
        "select_tasks.html",
        child=child,
        subject_options=subject_options,
        curriculum=curriculum,
        effective_age=effective_age,
        chat_profile=chat_profile,
        elo_idegen_file=(
            ELO_IDEGEN_NYELV_1_4_FILE
            if is_hu_1_4_grade(grade_num)
            else ELO_IDEGEN_NYELV_5_8_FILE
        ),
        learning_summary=database.get_learning_time_summary(child_id),
    )


@app.route("/children/<int:child_id>/tasks/generate", methods=["POST"])
@login_required
def generate_tasks(child_id: int):
    """Feladatgenerálás – tanterv JSON + OpenAI."""
    child = database.get_child_by_id(child_id, session["parent_id"])
    if not child:
        abort(404)

    payload = request.get_json(silent=True) if request.is_json else None
    form_data = payload or request.form
    subject = form_data.get("subject")
    subject = subject.strip() if subject else None
    language = (form_data.get("language") or "").strip().lower()

    if not subject:
        if request.is_json:
            return jsonify({"error": "subject_required"}), 400
        flash(i18n.t("flash_subject_required", g.lang), "error")
        return redirect(url_for("select_tasks", child_id=child_id))

    bundle = _generate_practice_tasks_bundle(child_id, child, subject, language)
    if bundle is None:
        if request.is_json:
            return jsonify({"error": "task_generation_failed"}), 500
        return redirect(url_for("select_tasks", child_id=child_id))

    tasks, curriculum, subject_label, _foreign = bundle

    if request.is_json:
        return jsonify({"tasks": tasks, "curriculum": curriculum})

    return _render_practice_tasks_page(
        child_id,
        child,
        tasks=tasks,
        curriculum=curriculum,
        subject=subject,
        subject_label=subject_label,
        language=language,
    )


@app.route("/children/<int:child_id>/tasks/regenerate", methods=["POST"])
@login_required
def regenerate_tasks(child_id: int):
    """Új feladatok ugyanazzal a tantárggyal – azonnal, session paraméterekből."""
    child = database.get_child_by_id(child_id, session["parent_id"])
    if not child:
        abort(404)

    stored = session.get(_tasks_session_key(child_id)) or {}
    subject = (stored.get("subject") or "").strip()
    language = (stored.get("language") or "").strip().lower() or None

    if not subject:
        flash(i18n.t("flash_subject_required", g.lang), "error")
        return redirect(url_for("select_tasks", child_id=child_id))

    bundle = _generate_practice_tasks_bundle(child_id, child, subject, language)
    if bundle is None:
        return redirect(url_for("select_tasks", child_id=child_id))

    tasks, curriculum, subject_label, _foreign = bundle
    return _render_practice_tasks_page(
        child_id,
        child,
        tasks=tasks,
        curriculum=curriculum,
        subject=subject,
        subject_label=subject_label,
        language=language,
    )


@app.route("/children/<int:child_id>/tasks/check", methods=["POST"])
@login_required
def check_task_answer(child_id: int):
    """Tanuló válasz ellenőrzése OpenAI-val."""
    child = database.get_child_by_id(child_id, session["parent_id"])
    if not child:
        abort(404)

    data = request.get_json(silent=True) or {}
    try:
        task_index = int(data.get("task_index"))
    except (TypeError, ValueError):
        return jsonify({"error": "invalid_task_index"}), 400

    user_answer = (data.get("answer") or "").strip()
    if not user_answer:
        return jsonify({"error": "answer_required"}), 400

    stored = session.get(_tasks_session_key(child_id)) or {}
    tasks = stored.get("tasks") or []
    if task_index < 0 or task_index >= len(tasks):
        return jsonify({"error": "task_not_found"}), 404

    task = tasks[task_index]
    lang = stored.get("lang") or g.lang

    try:
        result = _call_ai_check_task_answer(
            child, task, user_answer, lang=lang
        )
    except NotImplementedError:
        return jsonify({"error": "openai_not_configured"}), 501
    except Exception as exc:
        logger.exception("Feladat ellenőrzés hiba (child_id=%s): %s", child_id, exc)
        return jsonify({"error": "check_failed", "detail": str(exc)}), 500

    return jsonify(result)


# ---------------------------------------------------------------------------
# AI tanár chat
# ---------------------------------------------------------------------------

TOPIC_PASS_THRESHOLD = 70

_CHAT_PROFILE_VOICE_ONLY = "voice_only"
_CHAT_PROFILE_VOICE_DEFAULT = "voice_default"
_CHAT_PROFILE_BOTH = "both"


def _child_effective_age(child: dict) -> int:
    """Életkor a birth_date-ből, különben age mező, különben osztály + 5."""
    bd_str = child.get("birth_date")
    if bd_str:
        try:
            bd = date.fromisoformat(str(bd_str)[:10])
            today = date.today()
            age = today.year - bd.year - (
                (today.month, today.day) < (bd.month, bd.day)
            )
            return max(1, age)
        except Exception:
            pass
    return child.get("age") or (parse_grade(child.get("grade", 1)) + 5)


def _chat_interaction_profile(effective_age: int) -> str:
    if effective_age <= 6:
        return _CHAT_PROFILE_VOICE_ONLY
    if effective_age == 7:
        return _CHAT_PROFILE_VOICE_DEFAULT
    return _CHAT_PROFILE_BOTH


def _normalize_chat_mode(mode: str | None, profile: str) -> str:
    requested = (mode or "").strip().lower()
    if profile == _CHAT_PROFILE_VOICE_ONLY:
        return "voice"
    if profile == _CHAT_PROFILE_VOICE_DEFAULT:
        return "chat" if requested == "chat" else "voice"
    if requested == "voice":
        return "voice"
    return "chat"

_CHAT_MARKER_TOPIC = re.compile(r"<TOPIC_COMPLETE>", re.IGNORECASE)
_CHAT_MARKER_LEVEL = re.compile(r"<LEVEL:\s*([1-5])>", re.IGNORECASE)
_CHAT_MARKER_VOCAB = re.compile(
    r"<VOCAB>\s*([^=]+?)\s*=\s*([^<]+?)\s*</VOCAB>", re.IGNORECASE
)


def _parse_chat_markers(text: str) -> tuple[str, bool, int | None, list[tuple[str, str]]]:
    """Belső jelölők eltávolítása; topic, level, szójegyzék párok."""
    level_val: int | None = None
    level_match = _CHAT_MARKER_LEVEL.search(text)
    if level_match:
        level_val = int(level_match.group(1))

    vocab_pairs: list[tuple[str, str]] = []
    for native, foreign in _CHAT_MARKER_VOCAB.findall(text):
        n, f = native.strip(), foreign.strip()
        if n and f:
            vocab_pairs.append((n, f))

    clean = _CHAT_MARKER_TOPIC.sub("", text)
    clean = _CHAT_MARKER_LEVEL.sub("", clean)
    clean = _CHAT_MARKER_VOCAB.sub("", clean).strip()
    topic_done = bool(_CHAT_MARKER_TOPIC.search(text))
    return clean, topic_done, level_val, vocab_pairs


def _chat_load_curriculum(
    subject_file: str, grade: str | int, *, language: str | None = None
) -> dict:
    """Kerettanterv kizárólag helyi JSON-ból (sidebar topic_catalog is innen)."""
    return get_curriculum_for_chat(subject_file, grade, language=language)


_CHAT_LANGUAGES = frozenset({"angol", "nemet", "spanyol"})
_CHAT_LANGUAGE_DISPLAY = {
    "angol": "Angol",
    "nemet": "Német",
    "spanyol": "Spanyol",
}


def _normalize_chat_language(language: str | None) -> str:
    lang = (language or "").strip().lower()
    return lang if lang in _CHAT_LANGUAGES else ""


def _display_language_name(language: str | None) -> str:
    """nemet → Német, angol → Angol, spanyol → Spanyol (Jinja2 filter)."""
    return _CHAT_LANGUAGE_DISPLAY.get(
        (language or "").strip().lower(), (language or "").capitalize()
    )


@app.template_filter("display_language")
def display_language_filter(value: str) -> str:
    return _display_language_name(value)


def _chat_progress_subject(subject: str, language: str | None) -> str:
    """Haladás / teszt pontok: tantárgy + nyelv külön scope."""
    subj = (subject or "").strip()
    lang = _normalize_chat_language(language)
    return f"{subj}::{lang}" if lang else subj


def _chat_bind_flask_session(
    child_id: int, subject: str, language: str | None
) -> str:
    """Flask session: aktív chat kontextus (child + tantárgy + nyelv).
    A hívó felelős a helyes language átadásáért – a függvény NEM
    esik vissza a régi session értékre (lásd child_chat logika)."""
    lang = _normalize_chat_language(language)
    session["language"] = lang
    session["chat_subject"] = (subject or "").strip()
    session["chat_child_id"] = child_id
    session[f"chat_{child_id}_{subject}_{lang}"] = True
    return lang


def _chat_grade_num(child: dict) -> int:
    return parse_grade(child["grade"])


def _build_topic_sidebar(
    catalog: list[dict],
    scores: dict[str, dict],
    current_topic_id: str | None,
    *,
    level: int = 1,
) -> dict[str, Any]:
    """Sidebar állapot: témakörök zárolás / aktív / teljesített."""
    items: list[dict[str, Any]] = []
    passed_count = 0
    score_sum = 0
    score_n = 0

    for i, topic in enumerate(catalog):
        tid = topic["id"]
        rec = scores.get(tid) or {}
        passed = bool(rec.get("passed"))
        score = rec.get("score")

        if passed:
            passed_count += 1
            if score is not None:
                score_sum += int(score)
                score_n += 1

        prev_passed = (
            i == 0
            or bool((scores.get(catalog[i - 1]["id"]) or {}).get("passed"))
        )
        if level == 0:
            unlocked = i == 0
        else:
            unlocked = prev_passed

        if not unlocked:
            state = "locked"
        elif passed:
            state = "completed"
        elif tid == current_topic_id:
            state = "active"
        else:
            state = "available"

        items.append(
            {
                "id": tid,
                "name": topic["name"],
                "index": i + 1,
                "state": state,
                "score": score if passed else None,
                "unlocked": unlocked,
            }
        )

    total = len(catalog)
    avg = round(score_sum / score_n) if score_n else 0

    return {
        "topics": items,
        "completed_count": passed_count,
        "total_count": total,
        "average_score": avg,
        "current_topic_id": current_topic_id,
    }


def _resolve_current_topic_id(
    catalog: list[dict], progress: dict, scores: dict[str, dict]
) -> str | None:
    if not catalog:
        return None
    last = progress.get("last_position")
    if last:
        for t in catalog:
            if t["name"] == last:
                return t["id"]
    for t in catalog:
        tid = t["id"]
        if not (scores.get(tid) or {}).get("passed"):
            return tid
    return catalog[0]["id"]


def _topic_teaching_prompt_block(topic: dict | None) -> str:
    if not topic:
        return ""
    text = (topic.get("text") or "")[:12000]
    return (
        f"\n\nMost a következő témán vagytok: {topic.get('name', '')}.\n"
        f"Témakör tananyaga (kerettanterv):\n{text}\n"
        "Ebből tanítsd a gyereket lépésről lépésre, majd kínáld fel a tesztet, "
        "ha úgy érzed, készen áll (vagy ha a gyerek kéri).\n"
    )


def _voice_mode_prompt_block(effective_age: int) -> str:
    return f"""

HANGOS MÓD: A tanuló {effective_age} éves és hangon kommunikál veled.
Válaszaidat RÖVIDEN fogalmazd (max 2-3 mondat).
Csak egyszerű szavakat használj, amit egy {effective_age} éves megért.
Ne tegyél fel egyszerre több kérdést.
"""


def _whisper_transcribe(audio_bytes: bytes, filename: str = "audio.webm") -> str:
    api_key = _openai_api_key()
    if not api_key:
        raise NotImplementedError("OPENAI_API_KEY nincs beállítva")
    import io

    client = _openai_client(api_key, request_timeout=60.0)
    buf = io.BytesIO(audio_bytes)
    buf.name = filename if "." in filename else f"{filename}.webm"
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=buf,
        language="hu",
        prompt="Magyar gyerek beszél. Matematika, olvasás, számok, "
               "állatok, színek, betűk. Lehetséges szavak: igen, nem, "
               "kettő, három, alma, kutya, piros, kék, szia.",
    )
    return (transcription.text or "").strip()


def _openai_tts_speak(text: str) -> bytes:
    api_key = _openai_api_key()
    if not api_key:
        raise NotImplementedError("OPENAI_API_KEY nincs beállítva")
    client = _openai_client(api_key, request_timeout=60.0)
    text = text.replace("**", "").replace("##", "").replace("- ", "")
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=text[:4096],
    )
    return response.content


def _chat_progress_percent(progress: dict, all_topics: list[str]) -> int:
    if not all_topics:
        return 0
    done = len(progress.get("topics_completed") or [])
    return min(100, int(100 * done / len(all_topics)))


def _chat_current_topic(progress: dict, all_topics: list[str]) -> str:
    if progress.get("last_position"):
        return progress["last_position"]
    completed = set(progress.get("topics_completed") or [])
    for topic in all_topics:
        if topic not in completed:
            return topic
    return all_topics[-1] if all_topics else "Általános"


def _chat_advance_topic(
    progress: dict, all_topics: list[str], completed_now: str
) -> tuple[list[str], str | None]:
    completed = list(progress.get("topics_completed") or [])
    if completed_now and completed_now not in completed:
        completed.append(completed_now)
    completed_set = set(completed)
    next_topic = None
    for topic in all_topics:
        if topic not in completed_set:
            next_topic = topic
            break
    return completed, next_topic


def _age_specific_rules(age: int) -> str:
    """Egyszerű TILOS/KÖTELEZŐ szabályblokk: a curriculum a mérvadó."""
    lines = []
    lines.append("TILOS:")
    lines.append("- Markdown formázás (###, **, *, {{ }})")
    lines.append("- Törtek, tizedestörtek, százalékok, kivéve ha a kerettanterv kifejezetten tartalmazza")
    lines.append("- A kerettantervben NEM szereplő témák tanítása")
    lines.append("- Hosszú, bonyolult magyarázatok")
    lines.append("")
    lines.append("KÖTELEZŐ:")
    lines.append("- SZIGORÚAN csak a megadott kerettantervi szöveget tanítsd és kérdezd")
    lines.append("- A nehézséget a kerettanterv határozza meg, nem manuális korlátozások")
    lines.append("- Mindig a kerettantervi szövegből vett konkrét példákat használj")
    lines.append("- Az aktuális témakör ELSŐ leckéjétől kezdve")
    return "\n".join(lines)


def _build_chat_system_prompt(
    child: dict,
    *,
    subject_label: str,
    current_topic: str,
    curriculum_json_content: str,
    completed_topics: list[str],
    level: int,
    is_foreign_language: bool,
    teaching_language: str | None = None,
) -> str:
    age = _child_effective_age(child)
    curriculum_body = curriculum_json_content or (
        "NINCS BETÖLTÖTT KERETTANTERV – kérd a szülőtől a tananyag betöltését."
    )
    lang = _normalize_chat_language(teaching_language)
    lang_line = f"language={lang}" if lang else "language= (magyar tantárgy – magyarul taníts)"

    prompt = f"""Te egy kedves, türelmes, lelkesítő AI tanár vagy, aki {subject_label}-t tanít
{child["name"]} nevű, {age} éves, {child["grade"]}. osztályos gyereknek.

KRITIKUS: Ez a gyerek profilja amit MINDEN válasznál figyelembe kell venni:
- Neve: {child["name"]}
- Kora: {age} éves
- Osztálya: {child["grade"]}. osztály
- Szintje: {age} éves gyereknek megfelelő feladatok kellenek

{_age_specific_rules(age)}

FONTOS SZABÁLYOK:
1. MINDIG a kerettanterv szerint taníts - csak azt amit a lenti tananyag tartalmaz
2. Ha a gyerek először nyitja meg a témát, kezdd az alapoktól (ne ugorj bele a közepébe)
3. Légy NAGYON barátságos, bátorító, használj emojit
4. Rövid mondatok, egyszerű szavak
5. Ha a gyerek jól válaszol: dicsérj lelkesen ('Szuper!', 'Brávó!', 'Fantasztikus!')
6. Ha rosszul válaszol: bátorítsd ('Majdnem!', 'Próbáld újra!', 'Segítek egy kicsit!')
7. SOHA ne ismételd szó szerint ugyanazt a mondatot ha visszautasítasz valamit
8. Ha idegen nyelvet tanítasz, akkor a MEGADOTT nyelven taníts, ne keverj más nyelvet
9. SOHA ne írj ### fejléceket, ## alcímeket a válaszaidban
9b. SOHA ne írj ** vagy * csillag jelöléseket (pl. **szó** helyett csak: szó)
9c. Csak egyszerű mondatokat írj, semmi formázás
10. SOHA ne írj {{{{ }}}} kapcsos zárójeleket - ha példákat adsz,
    sorold fel őket így: alma, körte, szőlő - nem így: {{alma, körte}}
11. Folyamatos mondatokban írj, nem markdown formátumban

12. SZIGORÚAN kövesd a témakörök sorrendjét. Az aktuális témakör az
    egyetlen amit most tanítasz: {current_topic}
    NE ugorj előre más témakörre, NE tanítsd a később következő témákat.
    Ha a gyerek más témáról kérdez, barátságosan mondd:
    "Azt majd később tanuljuk! Most a(z) [aktuális téma]-val foglalkozunk."

13. Az aktuális témakört a LEGELEJÉTŐL kezdd tanítani, még ha a gyerek
    már tudni látszik is valamit. Az alapoktól haladj fokozatosan.

Idegen nyelveknél: {lang_line}. Ha language=angol, CSAK angolul taníts.
Ha language=spanyol, CSAK spanyolul taníts. Ha language=nemet, CSAK németül taníts.

AKTUÁLIS TANANYAG (ezt tanítsd, ebből ne lépj ki):
{curriculum_body}"""

    if current_topic:
        prompt += f"\n\nJelenlegi témakör: {current_topic}"
    if completed_topics:
        prompt += f"\nMár elvégzett témakörök: {', '.join(completed_topics)}"

    if level == 0:
        prompt += """
\nSZINTFELMÉRŐ: Tegyél fel 5 játékos kérdést a kerettanterv fő részeiből, majd add meg: <LEVEL:X> (X=1-5).
"""

    if is_foreign_language and lang:
        prompt += """
\nÚj idegen szó tanításakor (rejtett, a gyerek ne lássa): <VOCAB>magyar=idegen_szó</VOCAB>
"""

    prompt += """
\nHa egy témakör biztosan megvan (rejtett tag): <TOPIC_COMPLETE>
Csak tanításról beszélj; más témánál finoman terelj vissza a tananyaghoz (mindig más szavakkal).
"""
    return prompt


def _call_ai_for_quiz(
    *, grade: int, topic_name: str, topic_text: str, age: int, ora_szam: int, all_ora_szamok: list[int]
) -> list[dict[str, Any]]:
    api_key = _openai_api_key()
    if not api_key:
        raise NotImplementedError("OPENAI_API_KEY nincs beállítva")

    max_ora = max(all_ora_szamok) if all_ora_szamok else 1
    q_count = max(8, min(15, round(8 + (ora_szam / max_ora) * 7)))
    material = (topic_text or topic_name)[:10000]

    system = (
        "You are a strict curriculum-based quiz generator. "
        "You must ONLY create questions based on the exact curriculum text provided below. "
        "NEVER invent questions from outside this text.\n"
        f"Child profile: {age} years old, grade {grade}. "
        "Difficulty must match exactly what is written in the curriculum text - not easier, not harder.\n"
        "STRICTLY FORBIDDEN: generating questions about topics not present in the curriculum text below, "
        "using your own knowledge instead of the curriculum, "
        "creating generic math or animal questions unrelated to the curriculum topic.\n"
        "If the curriculum text is short or unclear, still create practical problems "
        "using the specific mathematical concepts, numbers, and operations mentioned in the curriculum text. "
        "Never create questions about how to solve problems theoretically - always create actual problems to solve.\n"
        "REQUIRED: every single question must directly reference concepts, terms, or examples "
        "from the curriculum text below. If the curriculum mentions halmazok, ask about halmazok. "
        "If it mentions mérés, ask about mérés.\n"
        "IMPORTANT: Do NOT ask theoretical or definition questions like what is X or how do we define Y. "
        "Instead create PRACTICAL problems where the child must calculate or solve something "
        "using the concepts from the curriculum. For example if the curriculum is about word problems, "
        "create actual word problems with numbers that need to be solved, not questions about what word problems are. "
        "Every question must require the child to actually DO something, not just recall a definition.\n"
        f"CURRICULUM TEXT (use ONLY this as your source):\n{material}\n"
        f"Generate exactly {q_count} multiple choice questions with 3 options each, "
        "1 correct answer (correct: 0, 1 or 2).\n"
        'Return ONLY a JSON object in this exact format, no other text: '
        '{"questions": [{"q": "question text here", "options": ["option a", "option b", "option c"], "correct": 0}]}. '
        "The q field must be named exactly q, not question or text. "
        "correct must be 0, 1, or 2.\n"
    )
    client = _openai_client(api_key, request_timeout=60.0)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": system,
            },
            {"role": "user", "content": f"Generate {q_count} questions based on the curriculum text above."},
        ],
        temperature=0.5,
    )
    raw = response.choices[0].message.content or "{}"
    payload = json.loads(raw)
    questions = payload.get("questions", payload if isinstance(payload, list) else [])
    if not isinstance(questions, list) or len(questions) < 1:
        raise ValueError("Érvénytelen kvíz JSON")
    return questions[:q_count]


def _call_ai_for_chat(
    system_prompt: str, history: list[dict[str, str]], user_message: str
) -> str:
    api_key = _openai_api_key()
    if not api_key:
        raise NotImplementedError("OPENAI_API_KEY nincs beállítva")

    messages: list[dict[str, str]] = [{"role": "system", "content": system_prompt}]
    for msg in history:
        if msg["role"] in ("user", "assistant"):
            messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": user_message})

    client = _openai_client(api_key, request_timeout=60.0)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.7,
    )
    return (response.choices[0].message.content or "").strip()


def _chat_initial_assistant_message(
    child_name: str, subject_label: str, *, placement: bool
) -> str:
    if placement:
        return (
            f"Szia {child_name}! 🌟 Én vagyok a {subject_label} AI tanárod. "
            "Először egy rövid játékos felmérést csinálunk, hogy tudjam, "
            "honnan induljunk. Kész vagy az első kérdésre?"
        )
    return (
        f"Szia {child_name}! 👋 Folytatjuk a {subject_label} tanulást. "
        "Írd meg, miben segíthetek, vagy válaszolj az utolsó kérdésemre!"
    )


def _chat_subject_label(
    child: dict,
    subject_file: str,
    chat_curriculum: dict,
    *,
    language: str | None = None,
) -> str:
    if g.lang == "hu":
        subject_label = hu_1_4_label_from_value(subject_file)
    else:
        subject_label = subject_ui_label(subject_file, g.lang, child["country"])
    subject_label = chat_curriculum.get("subject_name", subject_label)
    lang = _normalize_chat_language(language)
    if lang == "angol":
        return "Angol"
    if lang == "nemet":
        return "Német"
    if lang == "spanyol":
        return "Spanyol"
    return subject_label


def _chat_save_vocabulary(
    child_id: int,
    subject: str,
    language: str,
    vocab_pairs: list[tuple[str, str]],
) -> list[dict]:
    added: list[dict] = []
    for native, foreign in vocab_pairs:
        row = database.add_vocabulary_word(
            child_id,
            subject,
            language=language,
            word_native=native,
            word_foreign=foreign,
        )
        if row:
            added.append(row)
    return added


@app.route("/children/<int:child_id>/vocabulary")
@login_required
def child_vocabulary(child_id: int):
    """Szójegyzék JSON – ABC sorrend."""
    child = database.get_child_by_id(child_id, session["parent_id"])
    if not child:
        abort(404)

    subject = (request.args.get("subject") or "").strip()
    language = (request.args.get("language") or "").strip().lower()
    if not subject:
        return jsonify({"words": []})

    words = database.get_vocabulary(
        child_id, subject, language=language or None
    )
    return jsonify({"words": words})


@app.route("/children/<int:child_id>/chat")
@login_required
def child_chat(child_id: int):
    """AI tanár chat – kizárólag kerettanterv JSON alapján."""
    child = database.get_child_by_id(child_id, session["parent_id"])
    if not child:
        abort(404)

    logger.warning(
        "CHILD_CHAT DEBUG: request.args=%s request.form=%s session_subject=%s session_language=%s",
        dict(request.args),
        dict(request.form),
        session.get("subject"),
        session.get("language"),
    )

    # Language session törlése – LEGELEJÉN, mielőtt bármi más történne
    subject_raw = (
        request.args.get("subject") or request.form.get("subject") or ""
    ).strip()
    is_foreign = (
        is_elo_idegen_subject(subject_raw)
        or subject_raw.lower() in ("angol", "nemet", "spanyol", "idegen nyelv", "élő idegen nyelv")
    )
    if not is_foreign:
        session.pop("language", None)
        session["language"] = ""
    explicit_lang = (request.args.get("language") or "").strip().lower()
    if explicit_lang and is_foreign:
        session["language"] = explicit_lang

    subject = subject_raw
    if not subject:
        flash(i18n.t("flash_subject_required", g.lang), "error")
        return redirect(url_for("select_tasks", child_id=child_id))

    # Language: explicit request.args → session fallback (csak idegen nyelvnél)
    explicit_language = (request.args.get("language") or "").strip().lower()
    is_foreign_subj = is_elo_idegen_subject(subject)
    if not explicit_language:
        if is_foreign_subj:
            language = session.get("language", "")
        else:
            language = ""  # nem idegen nyelv → régi session["language"] törlődik
    else:
        language = explicit_language

    language = _chat_bind_flask_session(child_id, subject, language)
    session["subject"] = subject

    effective_age = _child_effective_age(child)
    chat_profile = _chat_interaction_profile(effective_age)
    chat_mode = _normalize_chat_mode(request.args.get("mode"), chat_profile)

    chat_curriculum = _chat_load_curriculum(
        subject, child["grade"], language=language or None
    )
    if not chat_curriculum.get("found") or not chat_curriculum.get("content"):
        flash(
            "Ehhez a tantárgyhoz nem található kerettanterv JSON. Válassz másik tantárgyat.",
            "error",
        )
        return redirect(url_for("select_tasks", child_id=child_id))

    catalog = chat_curriculum.get("topic_catalog") or []
    grade_num = _chat_grade_num(child)
    subject_label = _chat_subject_label(
        child, subject, chat_curriculum, language=language
    )
    logger.warning(
        "SUBJECT_DEBUG: subject=%s subject_label=%s session_subject=%s language=%s",
        subject,
        subject_label,
        session.get("subject"),
        session.get("language"),
    )
    is_foreign = is_elo_idegen_subject(subject) or bool(language)
    progress_subject = _chat_progress_subject(subject, language)

    progress = database.get_or_create_child_progress(
        child_id,
        progress_subject,
        last_position=catalog[0]["name"] if catalog else None,
    )
    scores = database.get_topic_scores(child_id, progress_subject, grade_num)
    current_topic_id = _resolve_current_topic_id(catalog, progress, scores)
    current_topic = next(
        (t["name"] for t in catalog if t["id"] == current_topic_id), ""
    )
    sidebar = _build_topic_sidebar(
        catalog, scores, current_topic_id, level=progress.get("level", 0)
    )
    progress_pct = (
        int(100 * sidebar["completed_count"] / sidebar["total_count"])
        if sidebar["total_count"]
        else 0
    )

    chat_session = database.get_or_create_chat_session(
        child_id,
        subject,
        language=language,
        curriculum_position={
            "current_topic": current_topic,
            "current_topic_id": current_topic_id,
        },
    )

    messages = database.get_chat_messages(chat_session["id"], limit=20)
    placement_mode = progress.get("level", 0) == 0

    if not messages:
        welcome = _chat_initial_assistant_message(
            child["name"], subject_label, placement=placement_mode
        )
        database.add_chat_message(chat_session["id"], "assistant", welcome)
        messages = database.get_chat_messages(chat_session["id"], limit=20)

    vocabulary = []
    if is_foreign and language:
        vocabulary = database.get_vocabulary(child_id, subject, language=language)

    chat_switch_params = {"child_id": child_id, "subject": subject, "mode": "chat"}
    if language:
        chat_switch_params["language"] = language
    chat_switch_url = url_for("child_chat", **chat_switch_params)

    learning_today = database.get_learning_time_today(child_id, subject)
    attempts = progress.get("early_placement_attempts", 0)
    if attempts < 3:
        show_early_test = True
    else:
        learning_total = database.get_learning_time_total(child_id, subject)
        show_early_test = learning_total >= 60

    return render_template(
        "chat.html",
        child=child,
        subject=subject,
        subject_label=subject_label,
        messages=messages,
        session_id=chat_session["id"],
        progress_pct=progress_pct,
        current_topic=current_topic,
        current_topic_id=current_topic_id,
        placement_mode=placement_mode,
        level=progress.get("level", 0),
        grade_num=grade_num,
        sidebar=sidebar,
        is_foreign_language=is_foreign,
        language=language,
        vocabulary=vocabulary,
        pass_threshold=TOPIC_PASS_THRESHOLD,
        chat_mode=chat_mode,
        chat_profile=chat_profile,
        effective_age=effective_age,
        chat_switch_url=chat_switch_url,
        show_chat_switch=chat_profile != _CHAT_PROFILE_VOICE_ONLY,
        learning_today=learning_today,
        show_early_test=show_early_test,
    )


@app.route("/children/<int:child_id>/chat/send", methods=["POST"])
@login_required
def child_chat_send(child_id: int):
    """Chat üzenet küldése – OpenAI válasz + haladás mentés."""
    child = database.get_child_by_id(child_id, session["parent_id"])
    if not child:
        abort(404)

    data = request.get_json(silent=True) or {}
    user_text = (data.get("message") or request.form.get("message") or "").strip()
    subject = (data.get("subject") or request.form.get("subject") or "").strip()
    session_id = data.get("session_id") or request.form.get("session_id")
    language = _normalize_chat_language(
        data.get("language") or request.form.get("language") or session.get("language")
    )
    focus_topic = (data.get("focus_topic") or "").strip()
    topic_id = (data.get("topic_id") or "").strip()
    req_mode = (data.get("mode") or request.form.get("mode") or "").strip().lower()
    chat_profile = _chat_interaction_profile(_child_effective_age(child))
    chat_mode = _normalize_chat_mode(req_mode or None, chat_profile)

    if not user_text or not subject:
        return jsonify({"error": "message_and_subject_required"}), 400

    try:
        session_id = int(session_id)
    except (TypeError, ValueError):
        return jsonify({"error": "invalid_session"}), 400

    if not database.get_chat_session_for_child(
        session_id, child_id, subject, language=language
    ):
        return jsonify({"error": "invalid_session"}), 403

    chat_curriculum = _chat_load_curriculum(
        subject, child["grade"], language=language or None
    )
    if not chat_curriculum.get("found") or not chat_curriculum.get("content"):
        return jsonify({"error": "curriculum_not_found"}), 400

    catalog = chat_curriculum.get("topic_catalog") or []
    grade_num = _chat_grade_num(child)
    subject_label = _chat_subject_label(
        child, subject, chat_curriculum, language=language
    )
    is_foreign = is_elo_idegen_subject(subject) or bool(language)
    progress_subject = _chat_progress_subject(subject, language)
    teaching_language = chat_curriculum.get("language") or language

    progress = database.get_or_create_child_progress(
        child_id,
        progress_subject,
        last_position=catalog[0]["name"] if catalog else None,
    )
    scores = database.get_topic_scores(child_id, progress_subject, grade_num)

    if topic_id:
        topic_item = get_topic_from_catalog(catalog, topic_id)
        if topic_item:
            progress = database.update_child_progress(
                child_id, progress_subject, last_position=topic_item["name"]
            )
    elif focus_topic:
        for t in catalog:
            if t["name"] == focus_topic:
                progress = database.update_child_progress(
                    child_id, progress_subject, last_position=focus_topic
                )
                topic_id = t["id"]
                break

    current_topic_id = _resolve_current_topic_id(catalog, progress, scores)
    current_topic_item = get_topic_from_catalog(catalog, current_topic_id)
    current_topic = current_topic_item["name"] if current_topic_item else ""

    system_prompt = _build_chat_system_prompt(
        child,
        subject_label=subject_label,
        current_topic=current_topic,
        curriculum_json_content=chat_curriculum["content"],
        completed_topics=[
            t["name"]
            for t in catalog
            if (scores.get(t["id"]) or {}).get("passed")
        ],
        level=progress.get("level", 0),
        is_foreign_language=is_foreign,
        teaching_language=teaching_language,
    )
    system_prompt += _topic_teaching_prompt_block(current_topic_item)
    if chat_mode == "voice":
        system_prompt += _voice_mode_prompt_block(_child_effective_age(child))

    history = database.get_chat_messages(session_id, limit=20)
    database.add_chat_message(session_id, "user", user_text)

    try:
        raw_reply = _call_ai_for_chat(system_prompt, history, user_text)
    except NotImplementedError:
        return jsonify({"error": "openai_not_configured"}), 501
    except Exception as exc:
        logger.exception("Chat AI hiba (child_id=%s): %s", child_id, exc)
        return jsonify({"error": "chat_failed", "detail": str(exc)}), 500

    reply, topic_done, level_set, vocab_pairs = _parse_chat_markers(raw_reply)
    database.add_chat_message(session_id, "assistant", reply)

    if is_foreign and language and vocab_pairs:
        _chat_save_vocabulary(child_id, subject, language, vocab_pairs)

    completed = list(progress.get("topics_completed") or [])
    last_pos = progress.get("last_position")
    level = progress.get("level", 0)

    if level_set is not None:
        level = level_set

    topic_names = [t["name"] for t in catalog]
    if topic_done and current_topic and current_topic in topic_names:
        completed, last_pos = _chat_advance_topic(progress, topic_names, current_topic)
        if last_pos is None and completed:
            last_pos = topic_names[-1] if topic_names else current_topic

    progress = database.update_child_progress(
        child_id,
        progress_subject,
        topics_completed=completed,
        last_position=last_pos or current_topic,
        level=level,
    )

    database.update_chat_session_position(
        session_id,
        {
            "current_topic": last_pos or current_topic,
            "current_topic_id": current_topic_id,
        },
    )

    scores = database.get_topic_scores(child_id, progress_subject, grade_num)
    sidebar = _build_topic_sidebar(
        catalog, scores, current_topic_id, level=progress.get("level", 0)
    )
    progress_pct = (
        int(100 * sidebar["completed_count"] / sidebar["total_count"])
        if sidebar["total_count"]
        else 0
    )
    vocabulary = []
    if is_foreign and language:
        vocabulary = database.get_vocabulary(child_id, subject, language=language)

    return jsonify(
        {
            "reply": reply,
            "progress_pct": progress_pct,
            "current_topic": current_topic,
            "current_topic_id": current_topic_id,
            "level": progress.get("level", 0),
            "placement_mode": progress.get("level", 0) == 0,
            "sidebar": sidebar,
            "vocabulary": vocabulary,
            "show_test_offer": "teszt" in reply.lower()
            or "tesztet" in reply.lower(),
        }
    )


@app.route("/children/<int:child_id>/chat/progress")
@login_required
def child_chat_progress(child_id: int):
    child = database.get_child_by_id(child_id, session["parent_id"])
    if not child:
        abort(404)
    subject = (request.args.get("subject") or "").strip()
    language = _normalize_chat_language(
        request.args.get("language") or session.get("language")
    )
    if not subject:
        return jsonify({"error": "subject_required"}), 400
    grade_num = _chat_grade_num(child)
    chat_curriculum = _chat_load_curriculum(
        subject, child["grade"], language=language or None
    )
    catalog = chat_curriculum.get("topic_catalog") or []
    progress_subject = _chat_progress_subject(subject, language)
    progress = database.get_or_create_child_progress(child_id, progress_subject)
    scores = database.get_topic_scores(child_id, progress_subject, grade_num)
    current_topic_id = _resolve_current_topic_id(catalog, progress, scores)
    sidebar = _build_topic_sidebar(
        catalog, scores, current_topic_id, level=progress.get("level", 0)
    )
    return jsonify(sidebar)


@app.route("/children/<int:child_id>/chat/test/generate", methods=["POST"])
@login_required
def child_chat_test_generate(child_id: int):
    child = database.get_child_by_id(child_id, session["parent_id"])
    if not child:
        abort(404)
    data = request.get_json(silent=True) or {}
    subject = (data.get("subject") or "").strip()
    topic_id = (data.get("topic_id") or "").strip()
    language = _normalize_chat_language(
        data.get("language") or session.get("language")
    )
    if not subject or not topic_id:
        return jsonify({"error": "subject_and_topic_required"}), 400

    chat_curriculum = _chat_load_curriculum(
        subject, child["grade"], language=language or None
    )
    catalog = chat_curriculum.get("topic_catalog") or []
    topic = get_topic_from_catalog(catalog, topic_id)
    if not topic:
        return jsonify({"error": "topic_not_found"}), 404

    try:
        all_ora_szamok = [t.get("ora_szam", 0) for t in catalog]
        questions = _call_ai_for_quiz(
            grade=_chat_grade_num(child),
            topic_name=topic["name"],
            topic_text=topic.get("text", ""),
            age=_child_effective_age(child),
            ora_szam=topic.get("ora_szam", 0),
            all_ora_szamok=all_ora_szamok,
        )
    except NotImplementedError:
        return jsonify({"error": "openai_not_configured"}), 501
    except Exception as exc:
        logger.exception("Kvíz generálás hiba: %s", exc)
        return jsonify({"error": "quiz_failed", "detail": str(exc)}), 500

    return jsonify({"questions": questions, "topic_id": topic_id, "topic_name": topic["name"]})


@app.route("/children/<int:child_id>/chat/test/submit", methods=["POST"])
@login_required
def child_chat_test_submit(child_id: int):
    child = database.get_child_by_id(child_id, session["parent_id"])
    if not child:
        abort(404)
    data = request.get_json(silent=True) or {}
    subject = (data.get("subject") or "").strip()
    topic_id = (data.get("topic_id") or "").strip()
    language = _normalize_chat_language(
        data.get("language") or session.get("language")
    )
    answers = data.get("answers") or []
    questions = data.get("questions") or []

    if not subject or not topic_id or not questions:
        return jsonify({"error": "invalid_payload"}), 400
    progress_subject = _chat_progress_subject(subject, language)

    correct = 0
    total = len(questions)
    for i, q in enumerate(questions):
        try:
            if int(answers[i]) == int(q.get("correct", -1)):
                correct += 1
        except (IndexError, TypeError, ValueError):
            pass
    score = int(round(100 * correct / total)) if total else 0
    passed = score >= TOPIC_PASS_THRESHOLD

    chat_curriculum = _chat_load_curriculum(
        subject, child["grade"], language=language or None
    )
    catalog = chat_curriculum.get("topic_catalog") or []
    topic = get_topic_from_catalog(catalog, topic_id)
    topic_name = topic["name"] if topic else topic_id
    grade_num = _chat_grade_num(child)

    database.save_topic_test_result(
        child_id,
        progress_subject,
        grade_num,
        topic_id,
        topic_name,
        score,
        pass_threshold=TOPIC_PASS_THRESHOLD,
    )

    congrats_message = None

    if passed:
        completed_names = [
            t["name"]
            for t in catalog
            if (
                database.get_topic_scores(child_id, progress_subject, grade_num)
                .get(t["id"])
                or {}
            ).get("passed")
        ]
        database.update_child_progress(
            child_id,
            progress_subject,
            topics_completed=completed_names,
            last_position=topic_name,
        )
        next_topic = None
        for t in catalog:
            if t["id"] == topic_id:
                continue
            if not (
                database.get_topic_scores(child_id, progress_subject, grade_num).get(
                    t["id"]
                )
                or {}
            ).get("passed"):
                next_topic = t
                break
        if next_topic:
            database.update_child_progress(
                child_id, progress_subject, last_position=next_topic["name"]
            )

        # 100% → AI gratuláció
        congrats_message = None
        if score == 100:
            try:
                age = _child_effective_age(child)
                congrats_prompt = (
                    f"Te egy kedves, lelkesítő AI tanár vagy. A gyerek ({child['name']}, "
                    f"{age} éves, {child['grade']}. osztályos) épp 100%-os eredményt ért el "
                    f"a(z) „{topic_name}” témakör tesztjén.\n\n"
                    f"GRATULÁLJ neki nagyon lelkesen, korának megfelelő stílusban!\n"
                    f"{age} éves gyereknek:\n"
                    f"- Rövid, lelkes mondatok\n"
                    f"- Emojik használata\n"
                    f"- Jelezd, hogy továbbléptek a következő témakörre\n"
                    f"- A következő témakör: {next_topic['name'] if next_topic else 'nincs'}\n"
                    f"Ne használj ###, **, {{ }} formázást."
                )
                chat_session = database.get_or_create_chat_session(
                    child_id, subject, language=language
                )
                reply = _call_ai_for_chat(congrats_prompt, [], "")
                database.add_chat_message(chat_session["id"], "assistant", reply)
                congrats_message = reply
            except Exception:
                logger.exception("Gratuláció generálás hiba")
                congrats_message = None

    scores = database.get_topic_scores(child_id, progress_subject, grade_num)
    progress = database.get_or_create_child_progress(child_id, progress_subject)
    current_topic_id = _resolve_current_topic_id(catalog, progress, scores)
    sidebar = _build_topic_sidebar(
        catalog, scores, current_topic_id, level=progress.get("level", 0)
    )

    return jsonify(
        {
            "score": score,
            "passed": passed,
            "pass_threshold": TOPIC_PASS_THRESHOLD,
            "topic_id": topic_id,
            "topic_name": topic_name,
            "congrats_message": congrats_message,
            "sidebar": sidebar,
        }
    )


@app.route("/api/voice/transcribe", methods=["POST"])
@login_required
def api_voice_transcribe():
    """Whisper: audio/webm → magyar szöveg."""
    upload = request.files.get("file") or request.files.get("audio")
    if not upload or not upload.filename:
        return jsonify({"error": "no_audio"}), 400
    audio_bytes = upload.read()
    if len(audio_bytes) < 200:
        return jsonify({"error": "audio_too_short"}), 400
    try:
        text = _whisper_transcribe(audio_bytes, upload.filename)
    except NotImplementedError:
        return jsonify({"error": "openai_not_configured"}), 501
    except Exception as exc:
        logger.exception("Whisper átírás hiba: %s", exc)
        return jsonify({"error": "transcribe_failed", "detail": str(exc)}), 500
    if not text:
        return jsonify({"error": "empty_transcript"}), 400
    return jsonify({"text": text})


@app.route("/api/voice/speak", methods=["POST"])
@login_required
def api_voice_speak():
    """TTS: AI szöveg → audio/mpeg."""
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    if not text:
        return jsonify({"error": "no_text"}), 400
    try:
        audio_bytes = _openai_tts_speak(text)
    except NotImplementedError:
        return jsonify({"error": "openai_not_configured"}), 501
    except Exception as exc:
        logger.exception("TTS hiba: %s", exc)
        return jsonify({"error": "speak_failed", "detail": str(exc)}), 500
    return Response(audio_bytes, mimetype="audio/mpeg")


# ---------------------------------------------------------------------------
# Tanulási idő követés
# ---------------------------------------------------------------------------


@app.route("/api/learning/start", methods=["POST"])
@login_required
def api_learning_start():
    """Tanulási session indítása."""
    data = request.get_json(silent=True) or {}
    child_id = data.get("child_id")
    subject = (data.get("subject") or "").strip()
    topic_id = (data.get("topic_id") or "").strip() or None
    if not child_id or not subject:
        return jsonify({"error": "child_id and subject required"}), 400
    child = database.get_child_by_id(child_id, session["parent_id"])
    if not child:
        return jsonify({"error": "child not found"}), 404
    result = database.start_learning_session(child_id, subject, topic_id)
    if not result:
        return jsonify({"error": "failed"}), 500
    return jsonify(result)


@app.route("/api/learning/heartbeat", methods=["POST"])
@login_required
def api_learning_heartbeat():
    """Heartbeat – session_id alapján frissíti a session_end-et."""
    data = request.get_json(silent=True) or {}
    session_id = data.get("session_id")
    minutes = float(data.get("minutes", 0))
    if not session_id or minutes < 0:
        return jsonify({"error": "invalid"}), 400
    database.end_learning_session(session_id, minutes)
    return jsonify({"ok": True})


@app.route("/api/learning/end", methods=["POST"])
@login_required
def api_learning_end():
    """Tanulási session zárása."""
    data = request.get_json(silent=True) or {}
    session_id = data.get("session_id")
    minutes = float(data.get("minutes", 0))
    if session_id:
        database.end_learning_session(session_id, minutes)
    return jsonify({"ok": True})


@app.route("/api/learning/today", methods=["GET"])
@login_required
def api_learning_today():
    """Mai tanulási percek (opcionálisan: ?subject=X)."""
    child_id = request.args.get("child_id")
    subject = request.args.get("subject")
    if not child_id:
        return jsonify({"error": "child_id required"}), 400
    minutes = database.get_learning_time_today(int(child_id), subject)
    return jsonify({"minutes": minutes})


@app.route("/api/learning/weekly", methods=["GET"])
@login_required
def api_learning_weekly():
    """Heti bontás: ?child_id=X&subject=Y."""
    child_id = request.args.get("child_id")
    subject = request.args.get("subject")
    if not child_id or not subject:
        return jsonify({"error": "child_id and subject required"}), 400
    weekly = database.get_learning_time_weekly(int(child_id), subject)
    return jsonify({"weekly": weekly})


@app.route("/api/learning/early-placement", methods=["POST"])
@login_required
def api_learning_early_placement():
    """Korai szintfelmérő indítása / státusz lekérése."""
    data = request.get_json(silent=True) or {}
    child_id = data.get("child_id")
    subject = (data.get("subject") or "").strip()
    if not child_id or not subject:
        return jsonify({"error": "child_id and subject required"}), 400
    child = database.get_child_by_id(child_id, session["parent_id"])
    if not child:
        return jsonify({"error": "child not found"}), 404

    progress = database.get_or_create_child_progress(child_id, subject)
    attempts = progress.get("early_placement_attempts", 0)
    total_minutes = database.get_learning_time_today(child_id, subject)

    # 3 próbálkozás után eltűnik a gomb
    if attempts >= 3:
        return jsonify({
            "available": False,
            "reason": "max_attempts",
            "early_placement_attempts": attempts,
        })

    # Minimum 1 óra tanulás kell
    if total_minutes < 60:
        return jsonify({
            "available": False,
            "reason": "too_soon",
            "remaining_minutes": round(60 - total_minutes, 1),
            "early_placement_attempts": attempts,
        })

    return jsonify({
        "available": True,
        "reason": "ready",
        "early_placement_attempts": attempts,
    })


@app.route("/api/learning/early-placement/start", methods=["POST"])
@login_required
def api_learning_early_placement_start():
    """Korai szintfelmérő indítása – növeli a próbálkozások számát."""
    data = request.get_json(silent=True) or {}
    child_id = data.get("child_id")
    subject = (data.get("subject") or "").strip()
    if not child_id or not subject:
        return jsonify({"error": "child_id and subject required"}), 400

    progress = database.get_or_create_child_progress(child_id, subject)
    attempts = progress.get("early_placement_attempts", 0) + 1

    database.update_child_progress(
        child_id, subject, level=0,  # level=0 → placement mode
    )
    database.increment_early_placement_attempts(child_id, subject)

    return jsonify({"ok": True, "early_placement_attempts": attempts})


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
