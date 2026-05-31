# TutorIA

Személyre szabott tanulást támogató web alkalmazás szülőknek (Flask + SQLite).
Kétnyelvű: **magyar** és **spanyol**.

> *Aplicación web de aprendizaje personalizado para padres. Bilingüe: húngaro y español.*

## Funkciók (1. fázis)

- Szülői regisztráció és bejelentkezés (email + jelszó, hashelve)
- Gyerek profil létrehozása: név, kor, osztály, ország (ES/HU)
  - Spanyolország esetén a 17 autonóm közösség közül választható régió
- Vezérlőpult a gyerek kártyák megjelenítésével
- Nyelvváltó (HU / ES) a fejlécben
- Modern, mobilbarát, zöld-fehér design

## Struktúra

```
TutorIA/
├── app.py             # Flask alkalmazás és útvonalak
├── database.py        # SQLite adatbázis kezelés
├── translations.py    # Magyar / spanyol fordítások
├── requirements.txt
├── templates/         # HTML sablonok
│   ├── base.html
│   ├── index.html
│   ├── register.html
│   ├── login.html
│   ├── add_child.html
│   └── dashboard.html
└── static/
    ├── css/style.css
    └── js/main.js
```

## Telepítés és futtatás

```bash
# (ajánlott) virtuális környezet
python -m venv venv
venv\Scripts\activate        # Windows PowerShell
# source venv/bin/activate   # macOS / Linux

pip install -r requirements.txt
python app.py
```

Ezután nyisd meg a böngészőben: http://127.0.0.1:5000

Az adatbázis (`tutoria.db`) az első indításkor automatikusan létrejön.
