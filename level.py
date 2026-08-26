# -*- coding: utf-8 -*-
"""TutorIA – a szülőnek küldött haladás-jelentés szövege.

MIÉRT KÜLÖN FÁJL
    Az app.py már így is több ezer soros. A levél szövegét viszont sokat
    fogjuk csiszolni, és jó, ha külön tesztelhető: elég egy szótárat átadni,
    nem kell hozzá adatbázis, se Flask.

MIT KELL TUDNI A LEVÉLRŐL
    A szülő nem fog belépni az oldalra. Ez a levél az EGYETLEN rendszeres
    visszajelzés arról, hogy amiért fizet, az működik-e. Ezért:
      - a legfontosabb szám (mennyit tanult) legyen az első sorban,
      - legyen benne valami KONKRÉT (melyik témakör ment jól, mi nem),
      - és ha a gyerek nem tanult, azt is meg kell írni. Az elhallgatott
        rossz hír később mondja fel az előfizetést, nem a rossz hír maga.
"""

from __future__ import annotations

from html import escape

SZOVEG = {
    "hu": {
        "targy_van": "TutorIA – {nev} haladása",
        "targy_tobb": "TutorIA – a gyerekek haladása",
        "targy_ures": "TutorIA – ezen a héten nem volt tanulás",
        "koszones": "Kedves Szülő!",
        "bevezeto_van": "Itt van, mi történt {idoszak}.",
        "bevezeto_ures": (
            "{idoszak} nem volt tanulás. Nem baj — de gondoltuk, jobb, "
            "ha tudod, mint ha nem szólnánk."
        ),
        "napi": "az elmúlt napban", "heti": "az elmúlt héten",
        "havi": "az elmúlt hónapban",
        "perc": "{perc} perc", "napon": "{napok} napon",
        "nem_tanult": "Ezen az időszakon nem tanult.",
        "tantargyak": "Mivel foglalkozott",
        "teljesitett": "Ami sikerült",
        "gyenge": "Amivel még küzd",
        "gyenge_alcim": "Ezeket érdemes vele átnézni.",
        "gyujtemeny": "{szavak} szó a szójegyzékben · {kartyak} kártya a gyűjteményben",
        "gomb": "Megnézem az oldalon",
        "labjegyzet": (
            "Ezt a levelet azért kapod, mert TutorIA-fiókod van. "
            "A gyakoriságot a Fiókom oldalon állíthatod, vagy "
            '<a href="{le}" style="color:#5b6474">itt kapcsolhatod ki</a>.'
        ),
    },
    "es": {
        "targy_van": "TutorIA – el progreso de {nev}",
        "targy_tobb": "TutorIA – el progreso de tus hijos",
        "targy_ures": "TutorIA – esta semana no ha habido estudio",
        "koszones": "Hola:",
        "bevezeto_van": "Esto es lo que ha pasado {idoszak}.",
        "bevezeto_ures": (
            "{idoszak} no ha habido estudio. No pasa nada — pero hemos "
            "pensado que es mejor que lo sepas."
        ),
        "napi": "en el último día", "heti": "en la última semana",
        "havi": "en el último mes",
        "perc": "{perc} minutos", "napon": "en {napok} días",
        "nem_tanult": "No ha estudiado en este período.",
        "tantargyak": "Qué ha trabajado",
        "teljesitett": "Lo que ha conseguido",
        "gyenge": "Lo que aún le cuesta",
        "gyenge_alcim": "Merece la pena repasarlo con él o ella.",
        "gyujtemeny": "{szavak} palabras en el vocabulario · {kartyak} cartas",
        "gomb": "Verlo en la página",
        "labjegyzet": (
            "Recibes este correo porque tienes una cuenta en TutorIA. "
            "Puedes cambiar la frecuencia en Mi cuenta o "
            '<a href="{le}" style="color:#5b6474">desactivarlo aquí</a>.'
        ),
    },
}

_KERET = """<!doctype html><html><body style="margin:0;padding:0;background:#f6f8fb">
<div style="max-width:560px;margin:0 auto;padding:26px 18px 40px;
     font:16px/1.6 -apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;color:#1a1f2b">
  <div style="font-size:1.25rem;font-weight:700;color:#1f3a63;margin-bottom:18px">TutorIA</div>
  {torzs}
  <div style="margin-top:26px;text-align:center">
    <a href="{app}" style="display:inline-block;background:#16a34a;color:#fff;
       text-decoration:none;padding:11px 24px;border-radius:999px;font-weight:600">{gomb}</a>
  </div>
  <p style="margin-top:26px;color:#8a93a3;font-size:.8rem;line-height:1.55">{lab}</p>
</div></body></html>"""


def _gyerek_blokk(gy: dict, sz: dict) -> str:
    if gy["perc"] <= 0:
        belso = (f'<p style="margin:0;color:#6b7280">{escape(sz["nem_tanult"])}</p>')
    else:
        sorok = [
            f'<p style="margin:0 0 10px">'
            f'<span style="font-size:1.5rem;font-weight:700;color:#16a34a">'
            f'{escape(sz["perc"].format(perc=gy["perc"]))}</span> '
            f'<span style="color:#6b7280">'
            f'{escape(sz["napon"].format(napok=gy["napok"]))}</span></p>'
        ]
        if gy["tantargyak"]:
            lista = " · ".join(
                f'{escape(str(n))} <b>{int(p)}p</b>' for n, p in gy["tantargyak"][:5])
            sorok.append(f'<p style="margin:0 0 10px;color:#4b5563">'
                         f'<b>{escape(sz["tantargyak"])}:</b> {lista}</p>')
        if gy["teljesitett"]:
            t = ", ".join(f'{escape(str(x["nev"]))} ({x["pont"]}%)'
                          for x in gy["teljesitett"])
            sorok.append(
                f'<p style="margin:0 0 10px;padding:9px 12px;background:#f0fdf4;'
                f'border-left:3px solid #16a34a;border-radius:0 8px 8px 0">'
                f'<b>{escape(sz["teljesitett"])}:</b> {t}</p>')
        if gy["gyenge"]:
            t = ", ".join(f'{escape(str(x["nev"]))} ({x["pont"]}%)'
                          for x in gy["gyenge"])
            sorok.append(
                f'<p style="margin:0 0 10px;padding:9px 12px;background:#fff8e6;'
                f'border-left:3px solid #e8a33d;border-radius:0 8px 8px 0">'
                f'<b>{escape(sz["gyenge"])}:</b> {t}<br>'
                f'<span style="color:#6b7280;font-size:.9rem">'
                f'{escape(sz["gyenge_alcim"])}</span></p>')
        if gy["szavak"] or gy["kartyak"]:
            sorok.append(
                f'<p style="margin:0;color:#8a93a3;font-size:.86rem">'
                + escape(sz["gyujtemeny"].format(szavak=gy["szavak"],
                                                 kartyak=gy["kartyak"])) + '</p>')
        belso = "".join(sorok)
    return (f'<div style="background:#fff;border:1px solid #e2e8f0;border-radius:14px;'
            f'padding:16px 18px;margin-bottom:14px">'
            f'<div style="font-weight:700;font-size:1.05rem;margin-bottom:8px">'
            f'{escape(gy["nev"])}</div>{belso}</div>')


def keszit(jelentes: dict, *, nyelv: str = "hu",
           app_url: str = "", leiratkozo_url: str = "") -> tuple[str, str, str]:
    """(tárgy, HTML, egyszerű szöveg). A sima szöveg azoknak kell, akiknek a
    levelezője nem mutat HTML-t – enélkül üres levelet kapnának."""
    sz = SZOVEG.get(nyelv) or SZOVEG["hu"]
    gyerekek = jelentes.get("gyerekek") or []
    idoszak = sz.get(jelentes.get("mod", "heti"), sz["heti"])

    if not jelentes.get("van_tanulas"):
        targy = sz["targy_ures"]
        bevezeto = sz["bevezeto_ures"].format(idoszak=idoszak.capitalize())
    else:
        tanulok = [g for g in gyerekek if g["perc"] > 0]
        targy = (sz["targy_van"].format(nev=tanulok[0]["nev"])
                 if len(tanulok) == 1 else sz["targy_tobb"])
        bevezeto = sz["bevezeto_van"].format(idoszak=idoszak)

    torzs = (f'<p style="margin:0 0 4px">{escape(sz["koszones"])}</p>'
             f'<p style="margin:0 0 18px;color:#4b5563">{escape(bevezeto)}</p>'
             + "".join(_gyerek_blokk(g, sz) for g in gyerekek))

    html = _KERET.format(torzs=torzs, app=escape(app_url),
                         gomb=escape(sz["gomb"]),
                         lab=sz["labjegyzet"].format(le=escape(leiratkozo_url)))

    sorok = [sz["koszones"], "", bevezeto, ""]
    for g in gyerekek:
        sorok.append(f'{g["nev"]}:')
        if g["perc"] <= 0:
            sorok.append(f'  {sz["nem_tanult"]}')
        else:
            sorok.append(f'  {sz["perc"].format(perc=g["perc"])}, '
                         f'{sz["napon"].format(napok=g["napok"])}')
            if g["tantargyak"]:
                sorok.append("  " + sz["tantargyak"] + ": " + ", ".join(
                    f'{n} {int(p)}p' for n, p in g["tantargyak"][:5]))
            if g["teljesitett"]:
                sorok.append("  " + sz["teljesitett"] + ": " + ", ".join(
                    f'{x["nev"]} ({x["pont"]}%)' for x in g["teljesitett"]))
            if g["gyenge"]:
                sorok.append("  " + sz["gyenge"] + ": " + ", ".join(
                    f'{x["nev"]} ({x["pont"]}%)' for x in g["gyenge"]))
        sorok.append("")
    sorok += [app_url, "", leiratkozo_url]
    return targy, html, "\n".join(sorok)
