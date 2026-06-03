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
from functools import wraps

from flask import (
    Flask,
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
    curriculum_topic_names,
    foreign_language_prompt_block,
    get_curriculum_for_child,
    get_hu_1_4_subjects,
    get_subject_options_for_ui,
    get_subjects_for_profile,
    hu_1_4_label_from_value,
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

    if lang == "es":
        prompt = (
            f"Genera 3 ejercicios de práctica para un/a niño/a de {child['age']} años, "
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
        f"Készíts 3 gyakorló feladatot egy {child['age']} éves gyereknek, "
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
    prompt: str, *, lang: str, foreign_language: str | None = None
) -> list[dict]:
    """OpenAI (gpt-4o-mini) hívás – 3 gyakorló feladat JSON formában."""
    api_key = _openai_api_key()
    if not api_key:
        logger.error("Task generation: OPENAI_API_KEY / OPENAI_KEY nincs beállítva")
        raise NotImplementedError("OPENAI_API_KEY nincs beállítva")

    if foreign_language == "angol":
        system_hu = (
            "Te egy tapasztalt angol nyelvtanár vagy magyar általános iskolásoknak. "
            "A feladatok tartalma kizárólag angol nyelven legyen. "
            "Válaszolj kizárólag érvényes JSON-nal; a task mezők angolul legyenek."
        )
    elif foreign_language == "nemet":
        system_hu = (
            "Te egy tapasztalt német nyelvtanár vagy magyar általános iskolásoknak. "
            "A feladatok tartalma kizárólag német nyelven legyen. "
            "Válaszolj kizárólag érvényes JSON-nal; a task mezők németül legyenek."
        )
    elif foreign_language == "spanyol":
        system_hu = (
            "Te egy tapasztalt spanyol nyelvtanár vagy magyar általános iskolásoknak. "
            "A feladatok tartalma kizárólag spanyol nyelven legyen. "
            "Válaszolj kizárólag érvényes JSON-nal; a task mezők spanyolul legyenek."
        )
    else:
        system_hu = (
            "Te egy tapasztalt magyar tanár vagy. A megadott hivatalos NAT 2020 "
            "kerettantervi témakörök alapján készíts gyakorló feladatokat. "
            "Válaszolj kizárólag érvényes JSON-nal, magyar nyelven."
        )
    system_es = (
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
    return render_template("dashboard.html", parent=parent, children=children)


@app.route("/children/add", methods=["GET", "POST"])
@login_required
def add_child():
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        age_raw = request.form.get("age") or ""
        grade = (request.form.get("grade") or "").strip()
        country = request.form.get("country") or ""
        region = request.form.get("region") or None

        errors = False

        try:
            age = int(age_raw)
            if age < 1 or age > 25:
                raise ValueError
        except ValueError:
            age = None
            errors = True

        if not name or country not in ("ES", "HU") or not grade or age is None:
            errors = True

        if country == "ES" and not region:
            flash(i18n.t("flash_region_required", g.lang), "error")
            errors = True

        if errors:
            return render_template(
                "add_child.html",
                form={
                    "name": name,
                    "age": age_raw,
                    "grade": grade,
                    "country": country,
                    "region": region,
                },
            )

        if country != "ES":
            region = None

        database.create_child(
            session["parent_id"], name, age, grade, country, region
        )
        flash(i18n.t("flash_child_added", g.lang), "success")
        return redirect(url_for("dashboard"))

    return render_template("add_child.html", form={})


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
        subject_options = get_hu_1_4_subjects()
        curriculum = {
            "subjects": [o["label"] for o in subject_options],
            "source": "hardcoded",
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

    return render_template(
        "select_tasks.html",
        child=child,
        subject_options=subject_options,
        curriculum=curriculum,
        elo_idegen_file=ELO_IDEGEN_NYELV_1_4_FILE,
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

    grade_num = parse_grade(child["grade"])
    if g.lang == "hu":
        allowed_files = {o["value"] for o in get_hu_1_4_subjects()}
        if subject not in allowed_files:
            if request.is_json:
                return jsonify({"error": "invalid_subject"}), 400
            flash(i18n.t("flash_subject_required", g.lang), "error")
            return redirect(url_for("select_tasks", child_id=child_id))
        if subject == ELO_IDEGEN_NYELV_1_4_FILE and language not in (
            "angol",
            "nemet",
            "spanyol",
        ):
            if request.is_json:
                return jsonify({"error": "language_required"}), 400
            flash(i18n.t("flash_language_required", g.lang), "error")
            return redirect(url_for("select_tasks", child_id=child_id))
        if subject != ELO_IDEGEN_NYELV_1_4_FILE:
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
            if request.is_json:
                return jsonify({"error": "invalid_subject"}), 400
            flash(i18n.t("flash_subject_required", g.lang), "error")
            return redirect(url_for("select_tasks", child_id=child_id))
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

    if subject == ELO_IDEGEN_NYELV_1_4_FILE:
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
        if request.is_json:
            return jsonify({"error": "OpenAI API key missing"}), 500
        flash(i18n.t("flash_tasks_failed", g.lang), "error")
        return redirect(url_for("select_tasks", child_id=child_id))

    try:
        tasks = _call_ai_for_tasks(
            prompt, lang=g.lang, foreign_language=foreign_language
        )
    except NotImplementedError:
        if request.is_json or request.headers.get("Accept") == "application/json":
            return jsonify(
                {
                    "status": "pending",
                    "message": "OPENAI_API_KEY not configured",
                    "curriculum": curriculum,
                    "prompt_preview": prompt,
                }
            ), 501
        flash(i18n.t("flash_tasks_pending", g.lang), "info")
        return redirect(url_for("select_tasks", child_id=child_id))
    except Exception as exc:
        tb = traceback.format_exc()
        logger.error(
            "Feladatgenerálás sikertelen (child_id=%s): %s\n%s",
            child_id,
            exc,
            tb,
        )
        print(tb, flush=True)
        if request.is_json:
            return jsonify({"error": "task_generation_failed", "detail": str(exc)}), 500
        flash(i18n.t("flash_tasks_failed", g.lang), "error")
        return redirect(url_for("select_tasks", child_id=child_id))

    if request.is_json:
        return jsonify({"tasks": tasks, "curriculum": curriculum})
    return render_template(
        "tasks.html",
        child=child,
        tasks=tasks,
        curriculum=curriculum,
        subject=subject,
        subject_label=(
            subject_display
            if g.lang == "hu"
            else subject_ui_label(subject, g.lang, child["country"])
        ),
    )


# ---------------------------------------------------------------------------
# AI tanár chat
# ---------------------------------------------------------------------------

_CHAT_MARKER_TOPIC = re.compile(r"<TOPIC_COMPLETE>", re.IGNORECASE)
_CHAT_MARKER_LEVEL = re.compile(r"<LEVEL:\s*([1-5])>", re.IGNORECASE)


def _parse_chat_markers(text: str) -> tuple[str, bool, int | None]:
    """Eltávolítja a belső jelölőket; topic_complete és level érték."""
    level_val: int | None = None
    level_match = _CHAT_MARKER_LEVEL.search(text)
    if level_match:
        level_val = int(level_match.group(1))
    clean = _CHAT_MARKER_TOPIC.sub("", text)
    clean = _CHAT_MARKER_LEVEL.sub("", clean).strip()
    topic_done = bool(_CHAT_MARKER_TOPIC.search(text))
    return clean, topic_done, level_val


def _chat_topic_list(curriculum: dict) -> list[str]:
    ctx = curriculum.get("subject_context") or {}
    return curriculum_topic_names(ctx.get("topics") or {})


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


def _build_chat_system_prompt(
    child: dict,
    *,
    subject_label: str,
    current_topic: str,
    curriculum_context: str,
    completed_topics: list[str],
    level: int,
) -> str:
    age = child["age"]
    if age <= 8:
        age_style = (
            "6-8 éves kornak megfelelő: rövid mondatok, sok emoji, egyszerű szavak."
        )
    else:
        age_style = "9+ éves kornak megfelelő: részletesebb, de közérthető magyarázatok."

    placement_block = ""
    if level == 0:
        placement_block = f"""
SZINTFELMÉRŐ MÓD (level == 0):
- Tegyél fel 5 kérdést a {subject_label} alapjairól, egyenként, a gyerek válaszai alapján.
- Az eredmény alapján határozd meg a szintet 1-5 skálán.
- Ha kész a felmérés, a válasz végén add meg: <LEVEL:X> ahol X a megállapított szint (1-5).
"""

    return f"""Te {child["name"]} AI tanára vagy.
{child["name"]} {child["grade"]}. osztályos, {age} éves.
Most {subject_label} tantárgyból tanulsz.
Jelenlegi fejezet: {current_topic}
Kerettanterv kontextus:
{curriculum_context or "(nincs részletes tanterv – általános iskolai szint)"}

SZEMÉLYISÉG:
- Kedves, türelmes, lelkesítő tanár
- {age_style}

HALADÁS:
- Már elvégzett témák: {", ".join(completed_topics) if completed_topics else "(még nincs)"}
- Mindig ott folytasd, ahol abbahagyta
- Ha egy témát megértett (kb. 3 helyes válasz vagy magabiztos megértés): jelezd a válasz végén <TOPIC_COMPLETE> és lépj a következő témára
- NE ismételd már elvégzett anyagot
{placement_block}
Belső jelölők (a gyerek NE lássa a szögletes zárójeleket – csak a szöveget írd ki nekik):
- Téma kész: <TOPIC_COMPLETE>
- Szintfelmérés kész: <LEVEL:X> (X = 1-5)
"""


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


@app.route("/children/<int:child_id>/chat")
@login_required
def child_chat(child_id: int):
    """AI tanár chat – tantárgy és haladás alapján."""
    child = database.get_child_by_id(child_id, session["parent_id"])
    if not child:
        abort(404)

    subject = (request.args.get("subject") or "").strip()
    if not subject:
        flash(i18n.t("flash_subject_required", g.lang), "error")
        return redirect(url_for("select_tasks", child_id=child_id))

    curriculum = _curriculum_for_child(child, subject=subject)
    all_topics = _chat_topic_list(curriculum)
    subject_label = (
        hu_1_4_label_from_value(subject)
        if g.lang == "hu"
        else subject_ui_label(subject, g.lang, child["country"])
    )

    progress = database.get_or_create_child_progress(
        child_id, subject, last_position=all_topics[0] if all_topics else None
    )
    current_topic = _chat_current_topic(progress, all_topics)
    progress_pct = _chat_progress_percent(progress, all_topics)

    ctx = curriculum.get("subject_context") or {}
    curriculum_summary = ctx.get("summary") or curriculum.get("curriculum_summary") or ""

    chat_session = database.get_or_create_chat_session(
        child_id,
        subject,
        curriculum_position={
            "current_topic": current_topic,
            "topic_index": all_topics.index(current_topic)
            if current_topic in all_topics
            else 0,
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

    return render_template(
        "chat.html",
        child=child,
        subject=subject,
        subject_label=subject_label,
        messages=messages,
        session_id=chat_session["id"],
        progress_pct=progress_pct,
        current_topic=current_topic,
        placement_mode=placement_mode,
        level=progress.get("level", 0),
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

    if not user_text or not subject:
        return jsonify({"error": "message_and_subject_required"}), 400

    try:
        session_id = int(session_id)
    except (TypeError, ValueError):
        return jsonify({"error": "invalid_session"}), 400

    curriculum = _curriculum_for_child(child, subject=subject)
    all_topics = _chat_topic_list(curriculum)
    ctx = curriculum.get("subject_context") or {}
    curriculum_summary = ctx.get("summary") or ""

    progress = database.get_or_create_child_progress(
        child_id, subject, last_position=all_topics[0] if all_topics else None
    )
    current_topic = _chat_current_topic(progress, all_topics)
    subject_label = (
        hu_1_4_label_from_value(subject)
        if g.lang == "hu"
        else subject_ui_label(subject, g.lang, child["country"])
    )

    system_prompt = _build_chat_system_prompt(
        child,
        subject_label=subject_label,
        current_topic=current_topic,
        curriculum_context=curriculum_summary,
        completed_topics=progress.get("topics_completed") or [],
        level=progress.get("level", 0),
    )

    history = database.get_chat_messages(session_id, limit=20)
    database.add_chat_message(session_id, "user", user_text)

    try:
        raw_reply = _call_ai_for_chat(system_prompt, history, user_text)
    except NotImplementedError:
        return jsonify({"error": "openai_not_configured"}), 501
    except Exception as exc:
        logger.exception("Chat AI hiba (child_id=%s): %s", child_id, exc)
        return jsonify({"error": "chat_failed", "detail": str(exc)}), 500

    reply, topic_done, level_set = _parse_chat_markers(raw_reply)
    database.add_chat_message(session_id, "assistant", reply)

    completed = list(progress.get("topics_completed") or [])
    last_pos = progress.get("last_position")
    level = progress.get("level", 0)

    if level_set is not None:
        level = level_set

    if topic_done and current_topic:
        completed, last_pos = _chat_advance_topic(progress, all_topics, current_topic)
        if last_pos is None and completed:
            last_pos = all_topics[-1] if all_topics else current_topic

    progress = database.update_child_progress(
        child_id,
        subject,
        topics_completed=completed,
        last_position=last_pos or current_topic,
        level=level,
    )

    database.update_chat_session_position(
        session_id,
        {
            "current_topic": last_pos or current_topic,
            "topic_index": all_topics.index(last_pos)
            if last_pos and last_pos in all_topics
            else 0,
        },
    )

    progress_pct = _chat_progress_percent(progress, all_topics)

    return jsonify(
        {
            "reply": reply,
            "progress_pct": progress_pct,
            "current_topic": last_pos or current_topic,
            "level": progress.get("level", 0),
            "placement_mode": progress.get("level", 0) == 0,
        }
    )


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
