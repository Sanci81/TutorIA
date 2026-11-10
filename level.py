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
        "targy_van": "{nev} haladása – TutorIAcademia",
        "targy_tobb": "A gyerekek haladása – TutorIAcademia",
        # A tárgy a BEÁLLÍTOTT gyakorisághoz igazodik. Korábban akkor is
        # "ezen a héten" állt benne, ha a szülő napi vagy havi jelentést
        # kért — és a levél így mást állított, mint amit ő beállított.
        "targy_ures_napi": "Ma nem volt tanulás – TutorIAcademia",
        "targy_ures_heti": "Ezen a héten nem volt tanulás – TutorIAcademia",
        "targy_ures_havi": "Ebben a hónapban nem volt tanulás – TutorIAcademia",
        "koszones": "Kedves Szülő!",
        "bevezeto_van": "Itt van, mi történt {idoszak}.",
        "bevezeto_ures": (
            "{idoszak} nem volt tanulás. Nem baj — de gondoltuk, jobb, "
            "ha tudod, mint ha nem szólnánk."
        ),
        "napi": "az elmúlt napban", "heti": "az elmúlt héten",
        "havi": "az elmúlt hónapban",
        "perc": "{perc} perc", "napon": "{napok} napon",
        "nem_tanult": "Ebben az időszakban nem tanult.",
        "tantargyak": "Mivel foglalkozott",
        "teljesitett": "Ami sikerült",
        "gyenge": "Amivel még küzd",
        "gyenge_alcim": "Ezeket érdemes vele átnézni.",
        "gyujtemeny": "{szavak} szó a szójegyzékben · {kartyak} kártya a gyűjteményben",
        "gomb": "Megnézem az oldalon",
        "cim": "Haladás-jelentés", "c_perc": "perc", "c_nap": "nap", "c_kartya": "kártya összesen",
        "c_szo": "szó",
        "labjegyzet": (
            "Ezt a levelet azért kapod, mert TutorIAcademia-fiókod van. "
            "A gyakoriságot a Fiókom oldalon állíthatod, vagy "
            '<a href="{le}" style="color:#5b6474">itt kapcsolhatod ki</a>.'
        ),
    },
    "es": {
        "targy_van": "El progreso de {nev} – TutorIAcademia",
        "targy_tobb": "El progreso de tus hijos – TutorIAcademia",
        "targy_ures_napi": "Hoy no ha habido estudio – TutorIAcademia",
        "targy_ures_heti": "Esta semana no ha habido estudio – TutorIAcademia",
        "targy_ures_havi": "Este mes no ha habido estudio – TutorIAcademia",
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
        "cim": "Informe de progreso", "c_perc": "minutos", "c_nap": "días", "c_kartya": "cartas en total",
        "c_szo": "palabras",
        "labjegyzet": (
            "Recibes este correo porque tienes una cuenta en TutorIAcademia. "
            "Puedes cambiar la frecuencia en Mi cuenta o "
            '<a href="{le}" style="color:#5b6474">desactivarlo aquí</a>.'
        ),
    },
}

# 2026-11-10 (Sándor: „kicsit meg lehetne formázni, de ne a zsiráfos képpel”):
# a TutorIAcademia színei – zöld fejléc, krémszínű háttér, kártyák, számdobozok,
# tantárgyanként csík. Csak táblázat és beágyazott stílus: így minden levelezőben
# (Gmail, Outlook, telefon) ugyanúgy néz ki.
_KERET = """<!doctype html><html><body style="margin:0;padding:0;background:#FBF5EA">
<table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background:#FBF5EA">
<tr><td align="center" style="padding:22px 10px 34px">
<table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="max-width:580px">
  <tr><td style="background:#17604A;border-radius:22px 22px 0 0;padding:22px 26px 20px">
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0"><tr>
      <td style="font:800 22px Arial,Helvetica,sans-serif;color:#ffffff">Tutor<span style="color:#F5A01E">IA</span>cademia</td>
      <td align="right" style="font:700 13px Arial,Helvetica,sans-serif;color:#BFE6D3;letter-spacing:.5px;text-transform:uppercase">{cim}</td>
    </tr></table>
  </td></tr>
  <tr><td style="background:#ffffff;border-radius:0 0 22px 22px;padding:24px 22px 26px;
                 font:16px/1.55 Arial,Helvetica,sans-serif;color:#1F2D28;box-shadow:0 6px 18px rgba(23,96,74,.10)">
  {torzs}
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="margin-top:22px"><tr><td align="center">
    <a href="{app}" style="display:inline-block;background:#F5A01E;color:#ffffff;text-decoration:none;
       font:800 16px Arial,Helvetica,sans-serif;padding:14px 32px;border-radius:14px;border-bottom:4px solid #C97F0E">{gomb}</a>
  </td></tr></table>
  </td></tr>
  <tr><td style="padding:18px 24px 0;color:#8A8F87;font:12px/1.6 Arial,Helvetica,sans-serif;text-align:center">{lab}</td></tr>
</table></td></tr></table></body></html>"""


def _perc(p) -> str:
    """Perc a jelentésbe. A fél percből eddig „0p" lett – az úgy néz ki,
    mintha a gyerek nem csinált volna semmit, pedig tanult."""
    try:
        ertek = float(p or 0)
    except Exception:
        return "0p"
    if ertek > 0 and ertek < 1:
        return "<1p"
    return "%dp" % int(ertek)

_SZINEK = ("#22A06B", "#2F8FD8", "#8A5CD6", "#F59E0B", "#0EA5B7", "#D9467F")


def _doboz(szam: str, cimke: str, szin: str) -> str:
    return (f'<td width="33%" style="padding:0 4px"><table role="presentation" width="100%" cellspacing="0" '
            f'cellpadding="0" style="background:{szin}14;border-radius:14px"><tr><td align="center" '
            f'style="padding:12px 4px 10px;font:800 26px Arial,Helvetica,sans-serif;color:{szin}">{escape(szam)}'
            f'<div style="font:700 12px Arial,Helvetica,sans-serif;color:#5E6B66;text-transform:uppercase;'
            f'letter-spacing:.4px;margin-top:2px">{escape(cimke)}</div></td></tr></table></td>')


def _gyerek_blokk(gy: dict, sz: dict) -> str:
    nev = str(gy["nev"])
    kezdo = escape(nev.strip()[:1].upper() or "?")
    fej = (f'<table role="presentation" cellspacing="0" cellpadding="0" style="margin-bottom:14px"><tr>'
           f'<td style="width:40px;height:40px;border-radius:50%;background:#E3F3EA;color:#17604A;text-align:center;'
           f'font:800 18px/40px Arial,Helvetica,sans-serif">{kezdo}</td>'
           f'<td style="padding-left:12px;font:800 19px Arial,Helvetica,sans-serif;color:#17342C">{escape(nev)}</td>'
           f'</tr></table>')
    if gy["perc"] <= 0:
        belso = (f'<p style="margin:0;padding:12px 14px;background:#F6F4EE;border-radius:12px;color:#5E6B66">'
                 f'{escape(sz["nem_tanult"])}</p>')
    else:
        sorok = ['<table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="margin:0 0 16px"><tr>'
                 + _doboz(str(gy["perc"]), sz["c_perc"], "#22A06B")
                 + _doboz(str(gy["napok"]), sz["c_nap"], "#2F8FD8")
                 + _doboz(str(gy.get("kartyak") or 0), sz["c_kartya"], "#F59E0B")
                 + '</tr></table>']
        if gy["tantargyak"]:
            lista = gy["tantargyak"][:5]
            try:
                legtobb = max(float(p or 0) for _, p in lista) or 1.0
            except Exception:
                legtobb = 1.0
            sorok.append(f'<div style="font:800 13px Arial,Helvetica,sans-serif;color:#5E6B66;text-transform:uppercase;'
                         f'letter-spacing:.4px;margin:0 0 8px">{escape(sz["tantargyak"])}</div>')
            for k, (n, p) in enumerate(lista):
                try:
                    szel = max(4, min(100, int(round(float(p or 0) / legtobb * 100))))
                except Exception:
                    szel = 4
                szin = _SZINEK[k % len(_SZINEK)]
                sorok.append(
                    f'<table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="margin:0 0 8px"><tr>'
                    f'<td style="font:15px Arial,Helvetica,sans-serif;color:#1F2D28">{escape(str(n))}</td>'
                    f'<td align="right" style="font:800 15px Arial,Helvetica,sans-serif;color:{szin};white-space:nowrap">{_perc(p)}</td></tr>'
                    f'<tr><td colspan="2" style="padding-top:4px"><table role="presentation" width="100%" cellspacing="0" cellpadding="0" '
                    f'style="background:#EEF2EF;border-radius:6px"><tr><td width="{szel}%" style="background:{szin};height:8px;'
                    f'border-radius:6px;font-size:0;line-height:0">&nbsp;</td><td style="font-size:0;line-height:0">&nbsp;</td>'
                    f'</tr></table></td></tr></table>')
        if gy["teljesitett"]:
            t = ", ".join(f'{escape(str(x["nev"]))} ({x["pont"]}%)' for x in gy["teljesitett"])
            sorok.append(f'<p style="margin:14px 0 0;padding:11px 14px;background:#EAF7F0;border-radius:12px">'
                         f'✅ <b>{escape(sz["teljesitett"])}:</b> {t}</p>')
        if gy["gyenge"]:
            t = ", ".join(f'{escape(str(x["nev"]))} ({x["pont"]}%)' for x in gy["gyenge"])
            sorok.append(f'<p style="margin:10px 0 0;padding:11px 14px;background:#FFF4E0;border-radius:12px">'
                         f'💡 <b>{escape(sz["gyenge"])}:</b> {t}<br>'
                         f'<span style="color:#7A6A4F;font-size:14px">{escape(sz["gyenge_alcim"])}</span></p>')
        if gy["szavak"]:
            sorok.append(f'<p style="margin:12px 0 0;color:#8A8F87;font-size:13px">📖 '
                         f'{escape(str(gy["szavak"]))} {escape(sz["c_szo"])}</p>')
        belso = "".join(sorok)
    return (f'<table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="border:1px solid #EFE6D4;'
            f'border-radius:18px;margin:0 0 16px"><tr><td style="padding:18px 16px">{fej}{belso}</td></tr></table>')


def keszit(jelentes: dict, *, nyelv: str = "hu",
           app_url: str = "", leiratkozo_url: str = "") -> tuple[str, str, str]:
    """(tárgy, HTML, egyszerű szöveg). A sima szöveg azoknak kell, akiknek a
    levelezője nem mutat HTML-t – enélkül üres levelet kapnának."""
    sz = SZOVEG.get(nyelv) or SZOVEG["hu"]
    gyerekek = jelentes.get("gyerekek") or []
    idoszak = sz.get(jelentes.get("mod", "heti"), sz["heti"])

    if not jelentes.get("van_tanulas"):
        targy = sz.get("targy_ures_" + jelentes.get("mod", "heti"),
                       sz["targy_ures_heti"])
        bevezeto = sz["bevezeto_ures"].format(idoszak=idoszak.capitalize())
    else:
        tanulok = [g for g in gyerekek if g["perc"] > 0]
        targy = (sz["targy_van"].format(nev=tanulok[0]["nev"])
                 if len(tanulok) == 1 else sz["targy_tobb"])
        bevezeto = sz["bevezeto_van"].format(idoszak=idoszak)

    torzs = (f'<p style="margin:0 0 4px;font-weight:800;font-size:18px;color:#17342C">{escape(sz["koszones"])}</p>'
             f'<p style="margin:0 0 20px;color:#4D665D">{escape(bevezeto)}</p>'
             + "".join(_gyerek_blokk(g, sz) for g in gyerekek))

    html = _KERET.format(torzs=torzs, app=escape(app_url), cim=escape(sz["cim"]),
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
                    f'{n} {_perc(p)}' for n, p in g["tantargyak"][:5]))
            if g["teljesitett"]:
                sorok.append("  " + sz["teljesitett"] + ": " + ", ".join(
                    f'{x["nev"]} ({x["pont"]}%)' for x in g["teljesitett"]))
            if g["gyenge"]:
                sorok.append("  " + sz["gyenge"] + ": " + ", ".join(
                    f'{x["nev"]} ({x["pont"]}%)' for x in g["gyenge"]))
        sorok.append("")
    sorok += [app_url, "", leiratkozo_url]
    return targy, html, "\n".join(sorok)
