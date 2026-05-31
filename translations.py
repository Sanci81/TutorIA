"""Kétnyelvű (magyar / spanyol) szövegek a TutorIA alkalmazáshoz."""

LANGUAGES = {
    "hu": "Magyar",
    "es": "Español",
}

DEFAULT_LANG = "hu"

# A 17 spanyol autonóm közösség (kód -> nyelvfüggő név)
SPANISH_REGIONS = [
    {"code": "AN", "hu": "Andalúzia", "es": "Andalucía"},
    {"code": "AR", "hu": "Aragónia", "es": "Aragón"},
    {"code": "AS", "hu": "Asztúria", "es": "Principado de Asturias"},
    {"code": "IB", "hu": "Baleár-szigetek", "es": "Islas Baleares"},
    {"code": "CN", "hu": "Kanári-szigetek", "es": "Canarias"},
    {"code": "CB", "hu": "Kantábria", "es": "Cantabria"},
    {"code": "CM", "hu": "Kasztília-La Mancha", "es": "Castilla-La Mancha"},
    {"code": "CL", "hu": "Kasztília és León", "es": "Castilla y León"},
    {"code": "CT", "hu": "Katalónia", "es": "Cataluña"},
    {"code": "VC", "hu": "Valenciai Közösség", "es": "Comunidad Valenciana"},
    {"code": "EX", "hu": "Extremadura", "es": "Extremadura"},
    {"code": "GA", "hu": "Galícia", "es": "Galicia"},
    {"code": "RI", "hu": "La Rioja", "es": "La Rioja"},
    {"code": "MD", "hu": "Madridi Közösség", "es": "Comunidad de Madrid"},
    {"code": "MC", "hu": "Murciai Régió", "es": "Región de Murcia"},
    {"code": "NC", "hu": "Navarra", "es": "Comunidad Foral de Navarra"},
    {"code": "PV", "hu": "Baszkföld", "es": "País Vasco"},
]

TRANSLATIONS = {
    # --- általános / navigáció ---
    "app_name": {"hu": "TutorIA", "es": "TutorIA"},
    "nav_home": {"hu": "Főoldal", "es": "Inicio"},
    "nav_dashboard": {"hu": "Vezérlőpult", "es": "Panel"},
    "nav_register": {"hu": "Regisztráció", "es": "Registrarse"},
    "nav_login": {"hu": "Bejelentkezés", "es": "Iniciar sesión"},
    "nav_logout": {"hu": "Kijelentkezés", "es": "Cerrar sesión"},

    # --- landing / főoldal ---
    "landing_title": {
        "hu": "Személyre szabott tanulás a gyermekednek",
        "es": "Aprendizaje personalizado para tu hijo/a",
    },
    "landing_subtitle": {
        "hu": "A TutorIA segít követni és támogatni gyermeked iskolai fejlődését – egyszerűen, egy helyen.",
        "es": "TutorIA te ayuda a seguir y apoyar el progreso escolar de tu hijo/a, de forma sencilla y en un solo lugar.",
    },
    "landing_cta": {"hu": "Kezdjük el", "es": "Empezar"},
    "landing_login_prompt": {
        "hu": "Már van fiókod?",
        "es": "¿Ya tienes cuenta?",
    },
    "feature_1_title": {"hu": "Több gyerek profil", "es": "Varios perfiles"},
    "feature_1_text": {
        "hu": "Hozz létre profilt minden gyermekednek külön.",
        "es": "Crea un perfil para cada uno de tus hijos.",
    },
    "feature_2_title": {"hu": "Helyi tanterv", "es": "Currículo local"},
    "feature_2_text": {
        "hu": "Ország és régió szerinti testreszabás.",
        "es": "Personalización por país y región.",
    },
    "feature_3_title": {"hu": "Kétnyelvű", "es": "Bilingüe"},
    "feature_3_text": {
        "hu": "Magyar és spanyol nyelven is elérhető.",
        "es": "Disponible en húngaro y español.",
    },

    # --- regisztráció ---
    "register_title": {"hu": "Szülői regisztráció", "es": "Registro de padres"},
    "register_subtitle": {
        "hu": "Hozz létre egy fiókot a kezdéshez.",
        "es": "Crea una cuenta para empezar.",
    },
    "label_email": {"hu": "E-mail cím", "es": "Correo electrónico"},
    "label_password": {"hu": "Jelszó", "es": "Contraseña"},
    "label_password_confirm": {"hu": "Jelszó megerősítése", "es": "Confirmar contraseña"},
    "show_password": {"hu": "Jelszó megjelenítése", "es": "Mostrar contraseña"},
    "hide_password": {"hu": "Jelszó elrejtése", "es": "Ocultar contraseña"},
    "btn_register": {"hu": "Regisztráció", "es": "Registrarse"},
    "have_account": {"hu": "Van már fiókod?", "es": "¿Ya tienes cuenta?"},

    # --- bejelentkezés ---
    "login_title": {"hu": "Bejelentkezés", "es": "Iniciar sesión"},
    "btn_login": {"hu": "Bejelentkezés", "es": "Iniciar sesión"},
    "no_account": {"hu": "Nincs még fiókod?", "es": "¿No tienes cuenta?"},

    # --- gyerek hozzáadása ---
    "add_child_title": {"hu": "Gyerek hozzáadása", "es": "Añadir niño/a"},
    "add_child_subtitle": {
        "hu": "Add meg gyermeked adatait.",
        "es": "Introduce los datos de tu hijo/a.",
    },
    "label_child_name": {"hu": "Név", "es": "Nombre"},
    "label_child_age": {"hu": "Kor", "es": "Edad"},
    "label_child_grade": {"hu": "Osztály", "es": "Curso"},
    "label_country": {"hu": "Ország", "es": "País"},
    "label_region": {"hu": "Autonóm közösség", "es": "Comunidad autónoma"},
    "country_es": {"hu": "Spanyolország", "es": "España"},
    "country_hu": {"hu": "Magyarország", "es": "Hungría"},
    "select_placeholder": {"hu": "Válassz...", "es": "Selecciona..."},
    "btn_save_child": {"hu": "Profil mentése", "es": "Guardar perfil"},
    "btn_cancel": {"hu": "Mégse", "es": "Cancelar"},

    # --- dashboard ---
    "dashboard_title": {"hu": "Gyermekeid", "es": "Tus hijos"},
    "dashboard_welcome": {"hu": "Üdv újra", "es": "Bienvenido/a de nuevo"},
    "btn_add_child": {"hu": "+ Gyerek hozzáadása", "es": "+ Añadir niño/a"},
    "empty_children": {
        "hu": "Még nincs hozzáadott gyerek. Kezdd az első profil létrehozásával!",
        "es": "Aún no hay niños. ¡Empieza creando el primer perfil!",
    },
    "card_age": {"hu": "Kor", "es": "Edad"},
    "card_grade": {"hu": "Osztály", "es": "Curso"},
    "card_location": {"hu": "Helyszín", "es": "Ubicación"},
    "years_old": {"hu": "éves", "es": "años"},

    # --- flash üzenetek ---
    "flash_registered": {
        "hu": "Sikeres regisztráció! Üdv a TutorIA-ban.",
        "es": "¡Registro completado! Bienvenido/a a TutorIA.",
    },
    "flash_email_taken": {
        "hu": "Ez az e-mail cím már foglalt.",
        "es": "Este correo electrónico ya está registrado.",
    },
    "flash_password_mismatch": {
        "hu": "A két jelszó nem egyezik.",
        "es": "Las contraseñas no coinciden.",
    },
    "flash_password_short": {
        "hu": "A jelszónak legalább 6 karakter hosszúnak kell lennie.",
        "es": "La contraseña debe tener al menos 6 caracteres.",
    },
    "flash_invalid_login": {
        "hu": "Hibás e-mail cím vagy jelszó.",
        "es": "Correo o contraseña incorrectos.",
    },
    "flash_logged_out": {
        "hu": "Sikeresen kijelentkeztél.",
        "es": "Has cerrado sesión correctamente.",
    },
    "flash_child_added": {
        "hu": "Gyerek profil sikeresen létrehozva.",
        "es": "Perfil del niño/a creado correctamente.",
    },
    "flash_region_required": {
        "hu": "Spanyolország esetén válassz autonóm közösséget.",
        "es": "Para España, selecciona una comunidad autónoma.",
    },
    "flash_login_required": {
        "hu": "Kérlek, jelentkezz be a folytatáshoz.",
        "es": "Por favor, inicia sesión para continuar.",
    },

    # --- lábléc ---
    "footer_text": {
        "hu": "TutorIA — Tanulás, személyre szabva.",
        "es": "TutorIA — Aprendizaje, personalizado.",
    },
}


def t(key, lang):
    """Lekér egy fordítást. Ha nincs meg, magát a kulcsot adja vissza."""
    entry = TRANSLATIONS.get(key)
    if entry is None:
        return key
    return entry.get(lang, entry.get(DEFAULT_LANG, key))


def region_name(code, lang):
    """Autonóm közösség nevének lekérése kód alapján."""
    for region in SPANISH_REGIONS:
        if region["code"] == code:
            return region.get(lang, region["es"])
    return code
