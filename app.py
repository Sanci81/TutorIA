"""TutorIA – Flask alkalmazás.

Funkciók (1. fázis):
  - Szülői regisztráció és bejelentkezés
  - Gyerek profil létrehozása (ország ES/HU, ES esetén autonóm közösség)
  - Vezérlőpult a gyerek kártyákkal
  - Kétnyelvű felület (magyar / spanyol) nyelvváltóval
"""

import os
from functools import wraps

from flask import (
    Flask,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_mail import Mail, Message
from werkzeug.security import check_password_hash, generate_password_hash

import database
import translations as i18n

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-insecure-key")

app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
app.config["MAIL_PORT"] = int(os.environ.get("MAIL_PORT", "587"))
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS", "true").lower() == "true"
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get(
    "MAIL_DEFAULT_SENDER", app.config["MAIL_USERNAME"]
)

mail = Mail(app)

# Az adatbázis biztosan létezik induláskor
database.init_db()


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


def _send_password_reset_email(recipient: str, token: str, lang: str) -> None:
    reset_url = url_for("reset_password", token=token, _external=True)
    subjects = {
        "hu": "TutorIA – Jelszó visszaállítása",
        "es": "TutorIA – Restablecer contraseña",
    }
    bodies = {
        "hu": (
            "Kérted a TutorIA jelszavad visszaállítását.\n\n"
            f"Kattints az alábbi linkre (1 órán belül érvényes):\n{reset_url}\n\n"
            "Ha nem te kérted, hagyd figyelmen kívül ezt az e-mailt."
        ),
        "es": (
            "Has solicitado restablecer tu contraseña de TutorIA.\n\n"
            f"Haz clic en el siguiente enlace (válido durante 1 hora):\n{reset_url}\n\n"
            "Si no lo solicitaste, ignora este correo."
        ),
    }
    msg = Message(
        subject=subjects.get(lang, subjects["hu"]),
        recipients=[recipient],
        body=bodies.get(lang, bodies["hu"]),
    )
    mail.send(msg)


# ---------------------------------------------------------------------------
# Útvonalak
# ---------------------------------------------------------------------------

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
        parent = database.get_parent_by_email(email)

        if parent:
            token = database.create_password_reset_token(parent["id"])
            try:
                _send_password_reset_email(parent["email"], token, g.lang)
            except Exception:
                flash(i18n.t("flash_reset_email_failed", g.lang), "error")
                return render_template("forgot_password.html", email=email)

        flash(i18n.t("flash_reset_email_sent", g.lang), "success")
        return redirect(url_for("login"))

    return render_template("forgot_password.html", email="")


@app.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    reset_row = database.get_password_reset_by_token(token)
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


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
