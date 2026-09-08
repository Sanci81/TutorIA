"""Az adatkivonat OLVASHATÓ változata.

MIÉRT VAN EZ: a GDPR 20. cikke (adathordozhatóság) géppel olvasható formát
kér – az a JSON. A 15. cikk (hozzáférés) viszont azt mondja, hogy a
másolatot „tömör, átlátható, érthető" alakban kell megadni – annak a JSON
nem felel meg: a legtöbb szülő meg sem tudja nyitni. Ezért mind a kettő
letölthető, és a PDF-ben ugyanaz van, mint a JSON-ban.

A betűtípus a repóban van (static/fonts/pdf), nem a szerver rendszeréből
jön: konténerben nincs garantálva, hogy van bármilyen betűtípus, és
ékezetek nélkül a kivonat használhatatlan lenne.
"""

from __future__ import annotations

import os
import re
from datetime import date, datetime

from fpdf import FPDF

BETU_MAPPA = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "static", "fonts", "pdf")
BETU = "DejaVu"

# A PDF betűtípusában nincs színes emoji. Ha benne hagynánk, üres négyzetek
# lennének a szövegben. A JSON-ból természetesen nem vesszük ki semmit.
_EMOJI = re.compile(
    "[\U0001F000-\U0001FAFF\U00002190-\U000021FF\U00002300-\U000027BF"
    "\U0000FE00-\U0000FE0F\U00002B00-\U00002BFF]+")

SZOVEG = {
    "hu": {
        "cim": "Adatkivonat",
        "alcim": "Ez a kivonat mindent tartalmaz, amit a TutorIA a fiókodról tárol.",
        "keszult": "Készült",
        "szulo": "A fiók adatai",
        "email": "E-mail cím",
        "regisztralt": "Regisztráció",
        "gyerek": "Tanuló",
        "osztaly": "Osztály",
        "tanterv": "Tanterv",
        "letrehozva": "Létrehozva",
        "ido": "Tanulással töltött idő",
        "ido_fej": ("Dátum", "Tantárgy", "Perc"),
        "ido_ossz": "Összesen",
        "perc": "perc",
        "eredmeny": "Eredmények",
        "eredmeny_fej": ("Tantárgy", "Témakör", "Eredmény"),
        "beszelgetes": "Beszélgetések",
        "tanar": "Tanár",
        "tanulo": "Tanuló",
        "nincs_adat": "Nincs rögzített adat.",
        "nincs_gyerek": "Ehhez a fiókhoz nincs tanuló rögzítve.",
        "oldal": "oldal",
        "labjegyzet": "TutorIA · adatkivonat",
    },
    "es": {
        "cim": "Copia de tus datos",
        "alcim": "Esta copia contiene todo lo que TutorIA guarda sobre tu cuenta.",
        "keszult": "Fecha",
        "szulo": "Datos de la cuenta",
        "email": "Correo electrónico",
        "regisztralt": "Registro",
        "gyerek": "Alumno/a",
        "osztaly": "Curso",
        "tanterv": "Currículo",
        "letrehozva": "Creado",
        "ido": "Tiempo de estudio",
        "ido_fej": ("Fecha", "Asignatura", "Minutos"),
        "ido_ossz": "Total",
        "perc": "minutos",
        "eredmeny": "Resultados",
        "eredmeny_fej": ("Asignatura", "Tema", "Resultado"),
        "beszelgetes": "Conversaciones",
        "tanar": "Profesor",
        "tanulo": "Alumno/a",
        "nincs_adat": "No hay datos registrados.",
        "nincs_gyerek": "Esta cuenta no tiene ningún alumno.",
        "oldal": "página",
        "labjegyzet": "TutorIA · copia de datos",
    },
}

FEKETE = (26, 26, 26)
SZURKE = (110, 118, 130)
ZOLD = (30, 122, 77)
HALVANY = (238, 243, 239)
KEK = (31, 58, 99)


def _tiszta(szoveg) -> str:
    """A PDF-be író szöveg. Az emojit kivesszük, mert nincs hozzá betűkép."""
    if szoveg is None:
        return "—"
    sz = _EMOJI.sub("", str(szoveg)).replace("\r", "")
    # Az emoji helyén maradt dupla szóközt is összehúzzuk, különben a
    # mondatok közepén lyukak látszanak.
    sz = re.sub(r"[ \t]{2,}", " ", sz)
    sz = re.sub(r"[ \t]+\n", "\n", sz)
    return sz.strip() or "—"


def _datum(ertek) -> str:
    """ISO időbélyegből olvasható dátum. Ami nem az, azt békén hagyjuk."""
    if not ertek:
        return "—"
    sz = str(ertek)
    for alak in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(sz[:len(alak) + 2].rstrip("."),
                                     alak).strftime("%Y. %m. %d.")
        except ValueError:
            continue
    return sz[:10]


class _Lap(FPDF):
    """Csak a lábjegyzet miatt van saját osztály: oldalszám kell rá."""

    def __init__(self, sz: dict):
        super().__init__(orientation="P", unit="mm", format="A4")
        self._sz = sz

    def footer(self):
        self.set_y(-14)
        self.set_font(BETU, size=8)
        self.set_text_color(*SZURKE)
        self.cell(0, 6, f"{self._sz['labjegyzet']} · "
                        f"{self._sz['oldal']} {self.page_no()}",
                  align="C")


def _betuk(pdf: FPDF) -> None:
    pdf.add_font(BETU, "", os.path.join(BETU_MAPPA, "DejaVuSans.ttf"))
    pdf.add_font(BETU, "B", os.path.join(BETU_MAPPA, "DejaVuSans-Bold.ttf"))


def _fejezet(pdf: FPDF, cim: str) -> None:
    """Szakaszcím. Új oldalt kezd, ha a cím alá már nem férne semmi –
    különben árván maradna egy cím a lap alján."""
    if pdf.get_y() > 250:
        pdf.add_page()
    pdf.ln(4)
    pdf.set_font(BETU, "B", 13)
    pdf.set_text_color(*ZOLD)
    pdf.cell(0, 8, _tiszta(cim), new_x="LMARGIN", new_y="NEXT")
    pdf.set_draw_color(*ZOLD)
    pdf.set_line_width(0.4)
    y = pdf.get_y()
    pdf.line(pdf.l_margin, y, pdf.w - pdf.r_margin, y)
    pdf.ln(3)
    pdf.set_text_color(*FEKETE)


def _adatsor(pdf: FPDF, cimke: str, ertek: str) -> None:
    pdf.set_font(BETU, size=10)
    pdf.set_text_color(*SZURKE)
    pdf.cell(45, 6, _tiszta(cimke))
    pdf.set_text_color(*FEKETE)
    pdf.multi_cell(0, 6, _tiszta(ertek), new_x="LMARGIN", new_y="NEXT")


def _tablazat(pdf: FPDF, fejlec, sorok, szelesseg) -> None:
    """Egyszerű táblázat. Lapdobásnál megismétli a fejlécet, különben a
    következő oldalon nem lehetne tudni, melyik oszlop mi."""
    def fej():
        pdf.set_font(BETU, "B", 9)
        pdf.set_fill_color(*HALVANY)
        pdf.set_text_color(*FEKETE)
        for cim, sz in zip(fejlec, szelesseg):
            pdf.cell(sz, 7, _tiszta(cim), border=0, fill=True)
        pdf.ln()

    fej()
    pdf.set_font(BETU, size=9)
    for sor in sorok:
        if pdf.get_y() > 262:
            pdf.add_page()
            fej()
            pdf.set_font(BETU, size=9)
        for ertek, sz in zip(sor, szelesseg):
            pdf.cell(sz, 6, _tiszta(ertek)[:60], border="B")
        pdf.ln()
    pdf.ln(2)


def _uzenet(pdf: FPDF, ki: str, szoveg: str, tanare: bool) -> None:
    """Egy chat-üzenet. Nem buborék, hanem beszélgetés-átirat: a PDF-nek
    olvashatónak kell lennie, nem a képernyőt kell utánoznia."""
    if pdf.get_y() > 258:
        pdf.add_page()
    pdf.set_font(BETU, "B", 9)
    pdf.set_text_color(*(ZOLD if tanare else KEK))
    pdf.cell(0, 5, _tiszta(ki) + ":", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font(BETU, size=9.5)
    pdf.set_text_color(*FEKETE)
    pdf.set_x(pdf.l_margin + 4)
    pdf.multi_cell(pdf.w - pdf.l_margin - pdf.r_margin - 4, 5,
                   _tiszta(szoveg), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1.5)


def keszit(adat: dict, nyelv: str = "hu") -> bytes:
    """Az export_parent_data() eredményéből olvasható PDF."""
    sz = SZOVEG.get(nyelv) or SZOVEG["hu"]
    pdf = _Lap(sz)
    pdf.set_auto_page_break(auto=True, margin=18)
    _betuk(pdf)
    pdf.add_page()

    pdf.set_font(BETU, "B", 20)
    pdf.set_text_color(*ZOLD)
    pdf.cell(0, 11, "TutorIA — " + sz["cim"], new_x="LMARGIN", new_y="NEXT")
    pdf.set_font(BETU, size=10)
    pdf.set_text_color(*SZURKE)
    pdf.multi_cell(0, 5.5, _tiszta(sz["alcim"]), new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, f"{sz['keszult']}: {date.today().strftime('%Y. %m. %d.')}",
             new_x="LMARGIN", new_y="NEXT")

    szulo = adat.get("szulo") or {}
    _fejezet(pdf, sz["szulo"])
    _adatsor(pdf, sz["email"], szulo.get("email"))
    _adatsor(pdf, sz["regisztralt"], _datum(szulo.get("regisztralt")))

    gyerekek = adat.get("gyerekek") or []
    if not gyerekek:
        pdf.ln(4)
        pdf.set_font(BETU, size=10)
        pdf.cell(0, 6, _tiszta(sz["nincs_gyerek"]), new_x="LMARGIN", new_y="NEXT")

    for gy in gyerekek:
        pdf.add_page()
        _fejezet(pdf, f"{sz['gyerek']}: {_tiszta(gy.get('nev'))}")
        _adatsor(pdf, sz["osztaly"], gy.get("osztaly"))
        _adatsor(pdf, sz["tanterv"], gy.get("tanterv"))
        _adatsor(pdf, sz["letrehozva"], _datum(gy.get("letrehozva")))

        idok = gy.get("tanulasi_ido") or []
        _fejezet(pdf, sz["ido"])
        if idok:
            _tablazat(pdf, sz["ido_fej"],
                      [(t.get("datum"), t.get("tantargy"), t.get("perc"))
                       for t in idok], (40, 100, 30))
            ossz = sum(int(t.get("perc") or 0) for t in idok)
            pdf.set_font(BETU, "B", 10)
            pdf.cell(0, 6, f"{sz['ido_ossz']}: {ossz} {sz['perc']}",
                     new_x="LMARGIN", new_y="NEXT")
        else:
            pdf.set_font(BETU, size=10)
            pdf.cell(0, 6, _tiszta(sz["nincs_adat"]), new_x="LMARGIN", new_y="NEXT")

        eredmenyek = gy.get("eredmenyek") or []
        _fejezet(pdf, sz["eredmeny"])
        if eredmenyek:
            _tablazat(pdf, sz["eredmeny_fej"],
                      [(e.get("tantargy"), e.get("temakor"),
                        f"{e.get('szazalek')}%" if e.get("szazalek") is not None
                        else "—") for e in eredmenyek], (45, 95, 30))
        else:
            pdf.set_font(BETU, size=10)
            pdf.cell(0, 6, _tiszta(sz["nincs_adat"]), new_x="LMARGIN", new_y="NEXT")

        beszelgetesek = gy.get("beszelgetesek") or []
        _fejezet(pdf, sz["beszelgetes"])
        if not beszelgetesek:
            pdf.set_font(BETU, size=10)
            pdf.cell(0, 6, _tiszta(sz["nincs_adat"]), new_x="LMARGIN", new_y="NEXT")
        for b in beszelgetesek:
            uzenetek = b.get("uzenetek") or []
            if not uzenetek:
                continue
            if pdf.get_y() > 250:
                pdf.add_page()
            pdf.ln(2)
            pdf.set_font(BETU, "B", 10)
            pdf.set_text_color(*KEK)
            pdf.multi_cell(0, 6, _tiszta(f"{b.get('tantargy')} · "
                                         f"{b.get('temakor')}"),
                           new_x="LMARGIN", new_y="NEXT")
            pdf.set_text_color(*FEKETE)
            for u in uzenetek:
                tanare = (u.get("ki") or "") == "assistant"
                _uzenet(pdf, sz["tanar"] if tanare else sz["tanulo"],
                        u.get("szoveg"), tanare)

    ki = pdf.output()
    return bytes(ki)
