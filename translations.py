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
    # A "Vezérlőpult" gépies, és nem mondja meg, mi van mögötte. Ez az oldal
    # a gyerekek listája és a haladásuk, ezért "Áttekintés". (Ha inkább
    # "Kezdőlap" vagy "Gyerekek" kell, elég ezt az egy sort átírni.)
    "nav_dashboard": {"hu": "Áttekintés", "es": "Resumen"},
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
    "label_child_grade_hu": {"hu": "Osztály (magyar tanterv)", "es": "Curso (currículo húngaro)"},
    "label_child_grade_es": {"hu": "Osztály (spanyol tanterv)", "es": "Curso (currículo español)"},
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
    "btn_generate_tasks": {"hu": "Tanulás indítása", "es": "Empezar a aprender"},
    "select_tasks_title": {"hu": "Tanulás indítása", "es": "Empezar a aprender"},
    "select_tasks_subtitle": {
        "hu": "Válassz tantárgyat {name} számára, majd indítsd el a tanulást.",
        "es": "Elige una asignatura para {name} y empieza a aprender.",
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
    "btn_back_dashboard": {"hu": "Vissza", "es": "Volver"},
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
    "es_primary_only_notice": {
        "hu": "A spanyol tanterv (Educación Primaria) csak 1–6. osztályig érhető el. "
              "{name} {grade}. osztályos, ezért itt nincs elérhető spanyol tananyag.",
        "es": "El currículo español (Educación Primaria) solo llega hasta 6.º. "
              "{name} está en {grade}.º, así que no hay contenido disponible.",
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

    # --- chat oldal + teszt ablak ---
    "chat_topics_title": {"hu": "Témakörök", "es": "Temas"},
    "chat_topics_done_suffix": {"hu": "témakör kész", "es": "temas completados"},
    "chat_average_label": {"hu": "Átlagod", "es": "Tu media"},
    "chat_now_learning": {"hu": "🎯 Most ezt tanulod", "es": "🎯 Ahora estás aprendiendo"},
    "chat_minutes_suffix": {"hu": "perc", "es": "min"},
    "chat_level_fmt": {"hu": "{n}. szint", "es": "Nivel {n}"},
    "chat_streak_fmt": {"hu": "🔥 {n} napos sorozat!", "es": "🔥 {n} días seguidos!"},
    "chat_test_start": {"hu": "⭐ Szintfelmérő teszt", "es": "⭐ Test de nivel"},
    "chat_test_start_short": {"hu": "Teszt indítása ✏️", "es": "Empezar test ✏️"},
    "chat_test_generating": {"hu": "Generálás... ⏳", "es": "Generando... ⏳"},
    "chat_voice_switch_chat": {"hu": "← Inkább írok", "es": "← Prefiero escribir"},
    "chat_mode_voice": {"hu": "🎙️ Hangos mód", "es": "🎙️ Modo voz"},
    "chat_mode_chat": {"hu": "💬 Chat mód", "es": "💬 Modo chat"},
    "chat_vocab_title": {"hu": "Szójegyzék", "es": "Vocabulario"},
    "chat_vocab_empty": {
        "hu": "Még nincs szó – tanulás közben töltődik fel.",
        "es": "Aún no hay palabras: se irán añadiendo mientras aprendes.",
    },
    "chat_input_label": {"hu": "Üzenet", "es": "Mensaje"},
    "chat_input_placeholder": {"hu": "Írd ide az üzeneted…", "es": "Escribe tu mensaje…"},
    "chat_send": {"hu": "Küldés", "es": "Enviar"},
    "chat_voice_status_idle": {"hu": "Nyomd meg és beszélj! 🎙️", "es": "¡Pulsa y habla! 🎙️"},
    "chat_voice_listening": {
        "hu": "Figyelek... 👂 Ha befejezted, nyomd meg újra!",
        "es": "Te escucho... 👂 Cuando termines, ¡pulsa otra vez!",
    },
    "chat_voice_processing": {"hu": "Mindjárt mondom... 💭", "es": "Un momento... 💭"},
    "chat_voice_unsupported": {
        "hu": "A böngésződ nem támogatja a hangfelvételt.",
        "es": "Tu navegador no admite la grabación de voz.",
    },
    "chat_voice_try_text": {"hu": "Próbáld a szöveges chatet", "es": "Prueba el chat de texto"},
    "chat_voice_mic_permission": {
        "hu": "Kérjük engedélyezd a mikrofon használatát!",
        "es": "¡Permite el uso del micrófono, por favor!",
    },
    "chat_err_no_reply": {
        "hu": "Sajnos most nem tudok válaszolni. 😊",
        "es": "Lo siento, ahora no puedo responder. 😊",
    },
    "chat_err_network": {
        "hu": "Hálózati hiba – próbáld újra!",
        "es": "Error de red: ¡inténtalo de nuevo!",
    },
    # Nem "hiba" a gyerek felé: a lassú válasz nem az ő hibája, és nem is
    # zsákutca. Megmondjuk, mit tegyen.
    "chat_err_timeout": {
        "hu": "Ez most sokáig tartott, és félbeszakadt. Írd le még egyszer, kérlek! 🙂",
        "es": "Esto ha tardado demasiado y se ha cortado. ¿Puedes escribirlo otra vez? 🙂",
    },
    # Nem hiba, hanem használati tipp: a gomb KAPCSOLÓ – egy nyomás indít,
    # a következő leállít, nem kell nyomva tartani.
    # ── Kiejtés-gyakorlás ────────────────────────────────────────────────
    # A gyerek SOHA nem lát pontszámot, csak ezeket a mondatokat. Egy hatéves
    # számára a szám ítélet; a mondat feladat.
    "kiejtes_tokeletes": {
        "hu": "Nagyon szép volt! Minden szót jól mondtál. 🌟",
        "es": "¡Muy bien! Has dicho todas las palabras correctamente. 🌟",
    },
    "kiejtes_gyakorold": {
        "hu": "Szép volt! Ezt gyakoroljuk még egy kicsit: {szavak}",
        "es": "¡Bien hecho! Vamos a practicar un poco más: {szavak}",
    },
    "kiejtes_nem_hallottam": {
        "hu": "Ezt nem hallottam jól. Mondd el még egyszer, kérlek! 🎤",
        "es": "No te he oído bien. ¿Puedes decirlo otra vez? 🎤",
    },
    "kiejtes_nem_ment": {
        "hu": "Most nem tudtam meghallgatni – de menjünk tovább! 🙂",
        "es": "Ahora no he podido escucharte, ¡pero sigamos! 🙂",
    },
    "kiejtes_cim": {"hu": "Mondd utánam", "es": "Repite conmigo"},
    "kiejtes_sugo": {
        "hu": "Nyomd meg, mondd ki, aztán nyomd meg újra.",
        "es": "Pulsa, dilo y vuelve a pulsar.",
    },
    "kiejtes_hallgasd": {"hu": "🔊 Hallgasd meg", "es": "🔊 Escúchalo"},
    "kiejtes_ujra": {"hu": "Még egyszer", "es": "Otra vez"},
    "kiejtes_figyelek": {"hu": "Figyelek…", "es": "Te escucho…"},
    "kiejtes_nezem": {"hu": "Megnézem…", "es": "Un momento…"},

    "chat_voice_too_short": {
        "hu": "Ez túl rövid volt. Nyomd meg, beszélj, majd nyomd meg újra! 🎤",
        "es": "Ha sido muy corto. Pulsa, habla y vuelve a pulsar. 🎤",
    },
    "chat_err_not_understood": {
        "hu": "Nem értettem – próbáld újra! 🙂",
        "es": "No te he entendido: ¡inténtalo de nuevo! 🙂",
    },
    "chat_think_1": {"hu": "Gondolkodom... 🤔", "es": "Estoy pensando... 🤔"},
    "chat_think_2": {"hu": "Mindjárt kész... ✍️", "es": "Casi listo... ✍️"},
    "chat_think_3": {"hu": "Összeszedem a választ... 📚", "es": "Preparo la respuesta... 📚"},
    "chat_think_4": {"hu": "Még egy pillanat... ⭐", "es": "Un momento más... ⭐"},
    "chat_replay_title": {"hu": "Hallgasd meg újra", "es": "Escuchar de nuevo"},
    "chat_mic_label": {"hu": "Mikrofon", "es": "Micrófono"},
    # --- teszt ablak ---
    "test_title": {"hu": "Teszt", "es": "Test"},
    "test_title_fmt": {"hu": "Teszt: {topic}", "es": "Test: {topic}"},
    "test_close": {"hu": "Bezárás", "es": "Cerrar"},
    "quiz_submit": {"hu": "Beküldés", "es": "Enviar"},
    "quiz_answer_placeholder": {"hu": "Írd ide a válaszod...", "es": "Escribe tu respuesta..."},
    "quiz_create_failed": {
        "hu": "Nem sikerült a tesztet létrehozni.",
        "es": "No se pudo crear el test.",
    },
    "quiz_advance": {"hu": "Továbblépek", "es": "Continuar"},
    "quiz_practice_more": {"hu": "Még gyakorlok", "es": "Practicar más"},
    "quiz_retry": {"hu": "Újra", "es": "Reintentar"},
    "quiz_next_fmt": {"hu": "➡️ Tovább: {topic}", "es": "➡️ Siguiente: {topic}"},
    "quiz_next_hint": {
        "hu": "Kattints a gombra a következő témakörre lépéshez.",
        "es": "Pulsa el botón para pasar al siguiente tema.",
    },
    "quiz_all_done": {
        "hu": "Minden témakört teljesítettél ebben a tantárgyban! 🎉",
        "es": "¡Has completado todos los temas de esta asignatura! 🎉",
    },
    "quiz_review_current_hint": {
        "hu": "Kattints a gombra, ha újra át szeretnéd nézni a témát.",
        "es": "Pulsa el botón si quieres repasar el tema.",
    },
    "quiz_try_again_fmt": {"hu": "Próbáld újra! {score}%", "es": "¡Inténtalo de nuevo! {score}%"},
    "quiz_attempts_left_fmt": {
        "hu": "Még {n} próbálkozásod van. Tanulj még {time} és próbálhatsz újra!",
        "es": "Te quedan {n} intentos. ¡Estudia {time} más y vuelve a intentarlo!",
    },
    # A fejléc két buborékja: az érme a kinézet-boltba, a pont a tasakboltba visz.
    "voice_budget_spent": {
        "hu": "Mára elfogyott a felolvasás – de a tanulás megy tovább írásban!",
        "es": "Hoy se ha acabado la voz, ¡pero seguimos aprendiendo por escrito!",
    },
    "coin_hint": {
        "hu": "Az érméid – a boltban tasakra vagy kinézetre költheted",
        "es": "Tus monedas: gástalas en sobres o en el aspecto",
    },
    "album_title": {
        "hu": "Gyűjtőalbum – ragaszd be a lapjaidat",
        "es": "Álbum: pega tus cromos",
    },
    "looks_shop_title": {
        "hu": "Kinézet – az érméidből háttért választhatsz",
        "es": "Aspecto: elige un fondo con tus monedas",
    },
    "pack_shop_title": {
        "hu": "Tasakbolt – a pontjaidból lapot húzhatsz",
        "es": "Tienda de sobres: consigue cromos con tus puntos",
    },
    # Amíg van a három esélyből, NEM kell várni – ilyenkor ez a szöveg megy.
    "quiz_attempts_left_now_fmt": {
        "hu": "Még {n} próbálkozásod van. Nézd át a hibákat, és próbáld újra!",
        "es": "Te quedan {n} intentos. ¡Repasa los fallos y vuelve a intentarlo!",
    },
    "quiz_study_more_fmt": {
        "hu": "Tanulj még {time} és utána próbálhatsz újra!",
        "es": "¡Estudia {time} más y luego vuelve a intentarlo!",
    },
    "quiz_study_60_retry": {
        "hu": "Tanulj még 60 percet és újra próbálhatod!",
        "es": "¡Estudia 60 minutos más y vuelve a intentarlo!",
    },
    "time_about_hours_fmt": {"hu": "kb. {h} órát", "es": "unas {h} horas"},
    "time_hours_minutes_fmt": {"hu": "{h} órát {m} percet", "es": "{h} horas {m} minutos"},
    "time_minutes_fmt": {"hu": "{m} percet", "es": "{m} minutos"},
    # --- teszt generálás kapu (szerver-oldali kikényszerítés) ---
    "test_gate_attempts_exhausted": {
        "hu": "Már háromszor próbálkoztál ezzel a szintfelmérővel. "
             "Tanuld végig a leckét, és a végén jön a leckezáró — ott újra "
             "megmutathatod, mit tudsz!",
        "es": "Ya lo has intentado tres veces con esta evaluación inicial. "
             "Estudia la lección completa y al final tendrás la prueba de "
             "cierre, donde podrás demostrar lo que sabes!",
    },
    "test_gate_study_more": {
        "hu": "Mielőtt újra próbálod, tanulj még kb. {minutes} percet ebben "
             "a témakörben!",
        "es": "Antes de volver a intentarlo, estudia unos {minutes} minutos "
             "mas en este tema!",
    },
    "gate_retry_hint": {
        "hu": "Zárd be ezt az ablakot, tanulj, és térj vissza később!",
        "es": "Cierra esta ventana, estudia y vuelve mas tarde!",
    },
    # --- teszt eredmény: hibalista ---
    "review_title": {"hu": "Eredmények áttekintése", "es": "Resumen de resultados"},
    "review_your_answer": {"hu": "A te válaszod", "es": "Tu respuesta"},
    "review_correct_answer": {"hu": "Helyes válasz", "es": "Respuesta correcta"},
    "review_no_answer": {"hu": "(nincs válasz)", "es": "(sin respuesta)"},
    "review_explanation": {"hu": "Magyarázat", "es": "Explicación"},

    # --- tanár hangja / neve (profil szerkesztése) ---
    "label_teacher_voice": {"hu": "A tanár hangja", "es": "La voz del profe"},
    "help_teacher_voice": {
        "hu": "Válaszd ki, milyen hangon szólaljon meg a tanár. "
              "A tanár neve a hanghoz tartozik, és bármikor módosítható.",
        "es": "Elige con qué voz habla el profe. El nombre del profe va con la voz "
              "y puede cambiarse en cualquier momento.",
    },
    "label_teacher_voice_hu": {
        "hu": "Magyar tanterv", "es": "Currículo húngaro",
    },
    "label_teacher_voice_es": {
        "hu": "Spanyol tanterv", "es": "Currículo español",
    },
    "label_teacher_voice_current": {
        "hu": "Hang és tanár", "es": "Voz y profe",
    },
    "dashboard_teacher_fmt": {
        "hu": "Tanár: {teacher}", "es": "Profe: {teacher}",
    },
    "voice_female": {"hu": "Női hang", "es": "Voz femenina"},
    "voice_male": {"hu": "Férfi hang", "es": "Voz masculina"},

    # --- chat üdvözlő üzenetek ---
    "chat_welcome_placement": {
        "hu": "Szia {name}! 🌟 {teacher} vagyok, {article} {subject} tanárod. "
              "Kezdjük is el a tanulást!",
        "es": "¡Hola {name}! 🌟 Soy {teacher}, tu profe de {subject}. "
              "¡Empecemos a aprender!",
    },
    "chat_welcome_continue": {
        "hu": "Szia {name}! 👋 Folytatjuk {article} {subject} tanulást — "
              "most itt tartunk: {topic}.",
        "es": "¡Hola {name}! 👋 Seguimos con {subject} — "
              "ahora estamos aquí: {topic}.",
    },

    # --- select_tasks oldal ---
    "grade_label": {"hu": "osztály", "es": "curso"},
    "grade_display_fmt": {"hu": "{grade}. osztály", "es": "{grade}.º curso"},
    "learning_time_toggle": {"hu": "⏱️ Tanulási idő", "es": "⏱️ Tiempo de estudio"},
    "time_today": {"hu": "ma", "es": "hoy"},
    "time_this_week": {"hu": "e héten", "es": "esta semana"},
    "time_total": {"hu": "összesen", "es": "total"},
    "btn_practice_tasks": {"hu": "📝 Gyakorló feladatok", "es": "📝 Ejercicios de práctica"},
    "btn_ai_chat": {"hu": "💬 AI tanulás és beszélgetés (chat)", "es": "💬 Estudio y conversación con IA (chat)"},
    "btn_ai_voice": {"hu": "🎙️ AI tanulás és beszélgetés (hangos)", "es": "🎙️ Estudio y conversación con IA (voz)"},
    "link_writing_alt": {"hu": "vagy inkább írok ✍️", "es": "o mejor escribo ✍️"},
    "link_chat_alt": {"hu": "💬 Inkább chatelünk", "es": "💬 Mejor chateamos"},
    "language_spanyol": {"hu": "Spanyol", "es": "Español"},
    "language_francia": {"hu": "Francia", "es": "Francés"},

    # --- automatikus osztálylépés ---
    "grade_promotion": {
        "hu": "Gratulálok! Mostantól a {grade}. osztály anyagát tanulod! 🎉",
        "es": "¡Enhorabuena! ¡Ahora estudias el contenido de {grade}.º curso! 🎉",
    },
    "grade_all_done": {
        "hu": "Gratulálok! Minden tananyagot teljesítettél ebben a tantervben! 🏆",
        "es": "¡Enhorabuena! ¡Has completado todo el contenido de este currículo! 🏆",
    },

    # --- lábléc ---
    # ── Jogi oldalak, fiókkezelés ──────────────────────────────────────────
    "privacy_title": {
        "hu": "Adatkezelési tájékoztató",
        "es": "Política de privacidad",
    },
    "terms_title": {
        "hu": "Felhasználási feltételek",
        "es": "Condiciones de uso",
    },
    "nav_account": {"hu": "Fiókom", "es": "Mi cuenta"},
    "privacy_delete_box_title": {
        "hu": "Bármikor meggondolhatod magad",
        "es": "Puede cambiar de opinión cuando quiera",
    },
    "privacy_delete_box_text": {
        "hu": "Az adataidat egy kattintással letöltheted, a fiókodat pedig "
              "azonnal és véglegesen törölheted itt:",
        "es": "Puede descargar sus datos con un clic y borrar la cuenta de "
              "forma inmediata y definitiva aquí:",
    },
    "terms_privacy_box_title": {
        "hu": "Mit kezdünk az adataiddal",
        "es": "Qué hacemos con sus datos",
    },
    "terms_privacy_box_text": {
        "hu": "Külön leírtuk, milyen adatot tárolunk és kihez kerül:",
        "es": "Lo explicamos por separado: qué guardamos y a quién llega:",
    },
    "account_data_title": {"hu": "A fiókod", "es": "Su cuenta"},
    "account_registered": {"hu": "Regisztrált", "es": "Registrado"},
    "account_children_count": {"hu": "Gyerekek", "es": "Menores"},
    "account_export_title": {
        "hu": "Az adataid letöltése",
        "es": "Descargar sus datos",
    },
    "account_export_text": {
        "hu": "Egy fájlba gyűjtve megkapod mindazt, amit rólad és a "
              "gyerekeidről tárolunk – a beszélgetéseket is beleértve.",
        "es": "Recibirá en un solo archivo todo lo que guardamos sobre usted "
              "y sus hijos, incluidas las conversaciones.",
    },
    "account_export_btn": {"hu": "Letöltés", "es": "Descargar"},
    "account_delete_title": {"hu": "A fiók törlése", "es": "Borrar la cuenta"},
    "account_delete_warning": {
        "hu": "Ez végleges. A gyerekeid haladása, eredményei, érméi és "
              "kártyái is elvesznek, és nem állíthatók vissza.",
        "es": "Esto es definitivo. También se perderán el progreso, los "
              "resultados, las monedas y las cartas de sus hijos, sin "
              "posibilidad de recuperarlos.",
    },
    "account_delete_text": {
        "hu": "Ha biztos vagy benne, add meg a jelszavadat.",
        "es": "Si está seguro, introduzca su contraseña.",
    },
    "account_delete_password": {"hu": "Jelszó", "es": "Contraseña"},
    "account_delete_btn": {"hu": "A fiókom végleges törlése",
                           "es": "Borrar mi cuenta definitivamente"},
    "account_delete_confirm": {
        "hu": "Biztosan törlöd a fiókot? Ez nem vonható vissza.",
        "es": "¿Seguro que desea borrar la cuenta? No se puede deshacer.",
    },
    "account_delete_done": {
        "hu": "A fiókod és minden hozzá tartozó adat törölve.",
        "es": "Su cuenta y todos sus datos han sido eliminados.",
    },
    "account_delete_bad_password": {
        "hu": "A jelszó nem stimmel – a fiók nem lett törölve.",
        "es": "La contraseña no es correcta: la cuenta no se ha borrado.",
    },
    "notify_title": {
        "hu": "Haladás-jelentés e-mailben",
        "es": "Informe de progreso por correo",
    },
    "notify_text": {
        "hu": "Rendszeres levél arról, mit tanult a gyereked, mi ment jól és "
              "mivel küzd még. A jelszavad kell hozzá, hogy csak te tudd "
              "átállítani – így a gyerek nem kapcsolhatja ki.",
        "es": "Un correo periódico con lo que ha estudiado su hijo, lo que le "
              "ha salido bien y lo que aún le cuesta. Pedimos su contraseña "
              "para que solo usted pueda cambiarlo.",
    },
    "notify_daily": {"hu": "Naponta", "es": "A diario"},
    "notify_weekly": {"hu": "Hetente", "es": "Cada semana"},
    "notify_monthly": {"hu": "Havonta", "es": "Cada mes"},
    "notify_off": {"hu": "Ne küldjetek", "es": "No enviar"},
    "notify_daily_note": {
        "hu": "Naponta csak akkor megy levél, ha aznap volt tanulás.",
        "es": "El correo diario solo se envía si ese día hubo estudio.",
    },
    "notify_save": {"hu": "Mentés", "es": "Guardar"},
    "notify_saved": {
        "hu": "Beállítva.",
        "es": "Guardado.",
    },
    "notify_saved_error": {
        "hu": "Ismeretlen beállítás – nem változott semmi.",
        "es": "Opción desconocida: no se ha cambiado nada.",
    },
    "notify_unsub_title": {
        "hu": "Kikapcsoltuk a leveleket",
        "es": "Hemos desactivado los correos",
    },
    "notify_unsub_text": {
        "hu": "Több haladás-jelentést nem küldünk. Ha meggondolod magad, a "
              "Fiókom oldalon bármikor visszakapcsolhatod.",
        "es": "No enviaremos más informes. Si cambia de opinión, puede "
              "volver a activarlo en Mi cuenta.",
    },
    "account_delete_failed": {
        "hu": "A törlés nem sikerült. Írj nekünk, és kézzel elintézzük.",
        "es": "No se ha podido borrar. Escríbanos y lo haremos manualmente.",
    },
    "register_accept": {
        "hu": "Elolvastam és elfogadom a feltételeket és az adatkezelési "
              "tájékoztatót.",
        "es": "He leído y acepto las condiciones de uso y la política de "
              "privacidad.",
    },
    "register_accept_required": {
        "hu": "A regisztrációhoz el kell fogadnod a feltételeket.",
        "es": "Para registrarse debe aceptar las condiciones.",
    },
    "chat_fullscreen": {
        "hu": "Teljes képernyő",
        "es": "Pantalla completa",
    },
    "chat_fullscreen_exit": {
        "hu": "Kilépés a teljes képernyőből",
        "es": "Salir de pantalla completa",
    },
    "footer_text": {
        "hu": "TutorIA — Tanulás, személyre szabva.",
        "es": "TutorIA — Aprendizaje, personalizado.",
    },
    # ── BEMUTATÓ (főoldal) ────────────────────────────────────────────────
    # Rövid mondatok. Egy szülő nem olvas bekezdéseket egy főoldalon.
    "bem_cim_1": {"hu": "Egy tanár, aki", "es": "Un profesor que"},
    "bem_cim_kiemelt": {"hu": "megvárja", "es": "espera"},
    "bem_cim_2": {"hu": "a gyerekedet.", "es": "a tu hijo."},
    "bem_alcim": {
        "hu": "Lépésről lépésre halad az iskolai anyaggal. Ha a válasz nem jó, nem megy tovább.",
        "es": "Avanza paso a paso con el temario escolar. Si la respuesta no es correcta, no sigue adelante.",
    },
    "bem_cta": {"hu": "Kipróbálom", "es": "Quiero probarlo"},
    "bem_apro": {
        "hu": "Az első hónap ingyenes. Bankkártya nem kell.",
        "es": "El primer mes es gratis. No hace falta tarjeta.",
    },
    "bem_osztaly_kerdes": {
        "hu": "Hányadik osztályos a gyereked?",
        "es": "¿En qué curso está tu hijo?",
    },
    "bem_osztaly": {"hu": "osztály", "es": "curso"},

    "bem_mi_cim": {"hu": "Nem csevegő robot. Tanár.", "es": "No es un chatbot. Es un profesor."},
    "bem_mi_1_cim": {"hu": "Az iskolai anyagot tanítja", "es": "Enseña el temario del colegio"},
    "bem_mi_1": {
        "hu": "Ugyanazt, ugyanabban a sorrendben, mint a suliban.",
        "es": "Lo mismo y en el mismo orden que en clase.",
    },
    "bem_mi_2_cim": {"hu": "Akkor, amikor kell", "es": "Cuando hace falta"},
    "bem_mi_2": {
        "hu": "Délután, este, hétvégén. Annyiszor, ahányszor a gyerek kéri.",
        "es": "Por la tarde, por la noche, el fin de semana. Las veces que el niño quiera.",
    },
    "bem_mi_3_cim": {"hu": "Beszélni is lehet vele", "es": "También se le puede hablar"},
    "bem_mi_3": {
        "hu": "A gyerek hangosan válaszol, és a kiejtésére is kap visszajelzést.",
        "es": "El niño responde en voz alta y recibe también corrección de pronunciación.",
    },

    "bem_biz_cim": {"hu": "Nyugodtan otthagyhatod vele", "es": "Puedes dejarle a solas con él"},
    "bem_biz_alcim": {
        "hu": "Nem attól félsz, hogy rosszul tanít. Attól, hogy a gyereked mást csinál majd.",
        "es": "No te preocupa que enseñe mal. Te preocupa que tu hijo acabe haciendo otra cosa.",
    },
    "bem_biz_1_cim": {"hu": "Csak a tanulásról beszél", "es": "Solo habla de estudiar"},
    "bem_biz_1": {
        "hu": "Ha a gyerek elterelné, kedvesen visszavezeti az órához.",
        "es": "Si el niño cambia de tema, lo devuelve a la clase con amabilidad.",
    },
    "bem_biz_2_cim": {"hu": "Nincs benne idegen", "es": "No hay nada ajeno dentro"},
    "bem_biz_2": {
        "hu": "Se hirdetés, se videó, se csevegés más gyerekekkel.",
        "es": "Ni anuncios, ni vídeos, ni chat con otros niños.",
    },
    "bem_biz_3_cim": {"hu": "Te látod, mi történt", "es": "Tú ves lo que ha pasado"},
    "bem_biz_3": {
        "hu": "Bármikor elolvashatod, miről beszélgettek.",
        "es": "Puedes leer en cualquier momento de qué han hablado.",
    },
    "bem_pelda_1": {
        "hu": "Kb. mennyi 4210 + 1680, ha százasokra kerekítesz?",
        "es": "¿Cuánto es 4210 + 1680, más o menos, redondeando a centenas?",
    },
    "bem_pelda_2": {
        "hu": "inkább nézzünk valami vicceset",
        "es": "mejor vemos algo divertido",
    },
    "bem_pelda_3": {
        "hu": "Megértem 🙂 De előbb fejezzük be ezt az egyet. Szóval: kb. mennyi 4210 + 1680, ha százasokra kerekítesz?",
        "es": "Te entiendo 🙂 Pero antes terminamos esta. Entonces: ¿cuánto es 4210 + 1680, más o menos, redondeando a centenas?",
    },
    "bem_cimke_tanar": {"hu": "Tanár", "es": "Profesor"},
    "bem_cimke_gyerek": {"hu": "Gyerek", "es": "Niño"},

    "bem_hogyan_cim": {"hu": "Hogyan működik", "es": "Cómo funciona"},
    "bem_l1_cim": {"hu": "Felveszed a gyereket", "es": "Añades a tu hijo"},
    "bem_l1": {"hu": "Név, osztály, tanárhang. Egy perc.", "es": "Nombre, curso, voz del profesor. Un minuto."},
    "bem_l2_cim": {"hu": "Választ tantárgyat", "es": "Elige una asignatura"},
    "bem_l2": {"hu": "A témakörök sorban nyílnak.", "es": "Los temas se abren en orden."},
    "bem_l3_cim": {"hu": "Tanul és hibázik", "es": "Aprende y se equivoca"},
    "bem_l3": {"hu": "A rossz válasz nem baj. Abból tanul.", "es": "Equivocarse no pasa nada. Así aprende."},
    "bem_l4_cim": {"hu": "Kap érte kártyát", "es": "Gana cromos"},
    "bem_l4": {
        "hu": "A kész témakör érmét ér, az érme kártyát.",
        "es": "Cada tema terminado da monedas, y las monedas dan cromos.",
    },

    "bem_album_cim": {"hu": "A gyűjtőalbum", "es": "El álbum de cromos"},
    "bem_album_alcim": {"hu": "Ezért ül le holnap is.", "es": "Por esto se sienta también mañana."},

    "bem_lapok_cim": {"hu": "Néhány lap az albumból", "es": "Algunos cromos del álbum"},
    "bem_zaro_cim": {"hu": "Ülj le vele egy órára.", "es": "Siéntate con él una clase."},
    "bem_zaro_alcim": {"hu": "Utána mondd meg, mit gondolsz.", "es": "Después dime qué te parece."},
    "bem_zaro_cta": {"hu": "Elkezdem", "es": "Empezar"},

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
