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
    "forgot_password": {"hu": "Elfelejtett jelszó?", "es": "¿Olvidaste tu contraseña?"},
    "forgot_password_title": {"hu": "Elfelejtett jelszó", "es": "Contraseña olvidada"},
    "forgot_password_subtitle": {
        "hu": "Add meg az e-mail címedet, és küldünk egy visszaállító linket.",
        "es": "Introduce tu correo y te enviaremos un enlace para restablecerla.",
    },
    "reset_password_title": {"hu": "Új jelszó beállítása", "es": "Establecer nueva contraseña"},
    "reset_password_subtitle": {
        "hu": "Add meg az új jelszavadat.",
        "es": "Introduce tu nueva contraseña.",
    },
    "btn_send_reset_link": {"hu": "Link küldése", "es": "Enviar enlace"},
    "btn_reset_password": {"hu": "Jelszó mentése", "es": "Guardar contraseña"},
    "back_to_login": {"hu": "Vissza a bejelentkezéshez", "es": "Volver al inicio de sesión"},

    # --- gyerek hozzáadása ---
    "add_child_title": {"hu": "Gyerek hozzáadása", "es": "Añadir niño/a"},
    "add_child_subtitle": {
        "hu": "Add meg gyermeked adatait.",
        "es": "Introduce los datos de tu hijo/a.",
    },
    "label_child_name": {"hu": "Név", "es": "Nombre"},
    "label_child_birth_date": {
        "hu": "Születési dátum",
        "es": "Fecha de nacimiento",
    },
    "edit_child_title": {"hu": "Gyerek szerkesztése", "es": "Editar niño/a"},
    "edit_child_subtitle": {
        "hu": "Frissítsd gyermeked adatait.",
        "es": "Actualiza los datos de tu hijo/a.",
    },
    "btn_edit_child": {"hu": "Profil szerkesztése", "es": "Editar perfil"},
    "banner_birth_date_missing": {
        "hu": "Kérjük, add meg a születési dátumot minden gyerek profiljánál (szerkesztés).",
        "es": "Indica la fecha de nacimiento en el perfil de cada niño/a (editar).",
    },
    "flash_child_updated": {
        "hu": "A gyerek profil frissítve.",
        "es": "Perfil actualizado.",
    },
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

    # --- feladatgenerálás ---
    "btn_generate_tasks": {"hu": "Feladatok generálása", "es": "Generar ejercicios"},
    "select_tasks_title": {"hu": "Feladatok generálása", "es": "Generar ejercicios"},
    "select_tasks_subtitle": {
        "hu": "Válassz tantárgyat {name} számára, majd kattints a generálás gombra.",
        "es": "Elige una asignatura para {name} y pulsa generar.",
    },
    "label_subject": {"hu": "Tantárgy", "es": "Asignatura"},
    "btn_generate_now": {"hu": "Generálás ✨", "es": "Generar ✨"},
    "generating_tasks": {
        "hu": "Feladatok készülnek… egy pillanat!",
        "es": "Creando ejercicios… ¡un momento!",
    },
    "tasks_page_title": {"hu": "Gyakorló feladatok", "es": "Ejercicios de práctica"},
    "tasks_for": {"hu": "Feladatok neki:", "es": "Ejercicios para:"},
    "tasks_subject": {"hu": "Tantárgy", "es": "Asignatura"},
    "task_number": {"hu": "Feladat", "es": "Ejercicio"},
    "btn_show_hint": {"hu": "Segítség kell? 💡", "es": "¿Necesitas ayuda? 💡"},
    "btn_show_answer": {"hu": "Mutasd a választ! ✅", "es": "¡Muéstrame la respuesta! ✅"},
    "btn_check_answer": {"hu": "Ellenőrzés ✓", "es": "Comprobar ✓"},
    "btn_read_aloud": {"hu": "🔊 Felolvas", "es": "🔊 Leer en voz alta"},
    "btn_speak_answer": {"hu": "🎙️ Bemondja a választ", "es": "🎙️ Decir la respuesta"},
    "btn_mic_answer": {"hu": "🎙️", "es": "🎙️"},
    "task_voice_listening": {"hu": "Figyelek… 👂", "es": "Te escucho… 👂"},
    "task_voice_processing": {"hu": "Egy pillanat…", "es": "Un momento…"},
    "task_answer_placeholder": {
        "hu": "Írd ide a válaszod…",
        "es": "Escribe tu respuesta…",
    },
    "label_feedback": {"hu": "Visszajelzés", "es": "Comentario"},
    "label_hint": {"hu": "Tipp", "es": "Pista"},
    "label_answer": {"hu": "Válasz", "es": "Respuesta"},
    "btn_new_tasks": {"hu": "Új feladatok", "es": "Nuevos ejercicios"},
    "btn_regenerate_tasks": {"hu": "🔄 Új feladatok", "es": "🔄 Nuevos ejercicios"},
    "btn_other_subject": {"hu": "📚 Másik tantárgy", "es": "📚 Otra asignatura"},
    "btn_tasks_home": {"hu": "👈 Főoldal", "es": "👈 Inicio"},
    "btn_back_dashboard": {"hu": "← Vissza", "es": "← Volver"},
    "tasks_encouragement": {
        "hu": "Szuper vagy! Próbáld meg egyedül, aztán kérj segítséget! 🌟",
        "es": "¡Genial! Inténtalo tú solo/a, y pide ayuda si la necesitas! 🌟",
    },
    "flash_tasks_pending": {
        "hu": "A feladatgenerálás hamarosan elérhető.",
        "es": "La generación de ejercicios estará disponible pronto.",
    },
    "flash_tasks_failed": {
        "hu": "Feladatgenerálás sikertelen. Próbáld újra később.",
        "es": "No se pudieron generar los ejercicios. Inténtalo más tarde.",
    },
    "flash_subject_required": {
        "hu": "Kérlek, válassz tantárgyat.",
        "es": "Por favor, elige una asignatura.",
    },
    "flash_language_required": {
        "hu": "Kérlek, válassz nyelvet (angol, német vagy spanyol).",
        "es": "Por favor, elige un idioma (inglés o alemán).",
    },
    "label_language": {"hu": "Nyelv", "es": "Idioma"},
    "language_angol": {"hu": "Angol", "es": "Inglés"},
    "language_nemet": {"hu": "Német", "es": "Alemán"},

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
    "flash_reset_email_sent": {
        "hu": "Ha ez az e-mail cím regisztrálva van, hamarosan kapsz egy visszaállító linket.",
        "es": "Si este correo está registrado, recibirás un enlace para restablecer la contraseña.",
    },
    "flash_reset_email_failed": {
        "hu": "Az e-mail küldése sikertelen. Próbáld újra később.",
        "es": "No se pudo enviar el correo. Inténtalo más tarde.",
    },
    "flash_invalid_reset_token": {
        "hu": "Érvénytelen vagy lejárt visszaállító link. Kérj újat.",
        "es": "Enlace inválido o caducado. Solicita uno nuevo.",
    },
    "flash_password_reset_success": {
        "hu": "A jelszavad sikeresen megváltozott. Most már bejelentkezhetsz.",
        "es": "Contraseña cambiada correctamente. Ya puedes iniciar sesión.",
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
