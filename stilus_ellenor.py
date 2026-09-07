# -*- coding: utf-8 -*-
"""Megnézi, van-e olyan CSS-osztály, amit a felület használ, de a
stíluslap nem ismer.

MIÉRT VAN EZ A FÁJL
    Kétszer is előfordult, hogy egy CSS-blokk cseréjekor a szomszédos
    blokkok is kiestek. A hiba NÉMA: a program fut, az oldal betöltődik,
    csak a doboz néz ki csúnyán — és ez csak akkor derül ki, ha valaki
    ránéz. Ez a pár soros ellenőrzés két másodperc alatt megmondja.

HASZNÁLAT
    python stilus_ellenor.py
    Kilépési kód 1, ha talált hiányzót — így push előtt is futtatható.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

GYOKER = Path(__file__).parent
STILUS = GYOKER / "static" / "css" / "style.css"
SABLONOK = GYOKER / "templates"

# Amit nem mi adunk: böngésző, külső könyvtár, vagy szándékosan üres.
KIVETEL = {"active", "hidden", "show", "open", "selected", "disabled"}

# ÁTNÉZVE, RENDBEN VAN: ezeknek tényleg nincs saját szabályuk. Vagy csak
# szerkezeti keretek (a szülő rács pozicionálja őket), vagy a JavaScript
# tölti fel őket. Azért soroljuk fel, hogy a lista tiszta maradjon, és egy
# ÚJ hiányzó osztály rögtön kitűnjön.
RENDBEN = {
    "bem-hero-szoveg",      # a hero bal oszlopa, a rács pozicionálja
    "brand-name",           # a fejléc felirata, a szülő adja a stílust
    "footer-jogi",          # lábléc-sor, a szülő adja
    "feladat-hely",         # üres hely: a JavaScript cseréli feladatra
    "nyelvracs",            # a nyelvcsempék rácsa, .targyracs adja a formát
    "select-tasks-form",    # űrlapkeret, nincs saját megjelenése
    "select-tasks-notice",  # rejtett üzenetdoboz
    "topic-name",           # a témakör neve, a szülő stílusa érvényes
}

_OSZTALY = re.compile(r"\.([A-Za-z_][\w-]*)")
_CLASS_ATTR = re.compile(r'class="([^"{}]+)"')
_STYLE_BLOKK = re.compile(r"<style[^>]*>(.*?)</style>", re.DOTALL | re.IGNORECASE)


def _ismert_osztalyok(szoveg: str) -> set[str]:
    return set(_OSZTALY.findall(szoveg))


def _sablon_sajat_stilusa(szoveg: str) -> set[str]:
    """Amit a lap a saját <style> blokkjában definiál."""
    ismert: set[str] = set()
    for blokk in _STYLE_BLOKK.findall(szoveg):
        ismert |= _ismert_osztalyok(blokk)
    return ismert


def _hianyzok(kozos: set[str]) -> dict[str, set[str]]:
    """Osztálynév -> mely sablonok használják stílus nélkül."""
    talalat: dict[str, set[str]] = {}
    for f in sorted(SABLONOK.glob("*.html")):
        szoveg = f.read_text(encoding="utf-8")
        # A lap SAJÁT <style> blokkja is számít ismertnek.
        ismert = kozos | _sablon_sajat_stilusa(szoveg)
        # A <style> blokkon KÍVÜLI részben keresünk class="..." attribútumot;
        # a JavaScript sorai nem érdekelnek, ezért a szkripteket kihagyjuk.
        torzs = _STYLE_BLOKK.sub("", szoveg)
        torzs = re.sub(r"<script[^>]*>.*?</script>", "", torzs,
                       flags=re.DOTALL | re.IGNORECASE)
        for csoport in _CLASS_ATTR.findall(torzs):
            for nev in csoport.split():
                nev = nev.strip()
                if (not nev or "{" in nev or nev in KIVETEL
                        or nev in RENDBEN or nev in ismert):
                    continue
                talalat.setdefault(nev, set()).add(f.name)
    return talalat


def main() -> int:
    if not STILUS.is_file():
        print(f"Nincs meg a stíluslap: {STILUS}")
        return 1
    kozos = _ismert_osztalyok(STILUS.read_text(encoding="utf-8"))
    hianyzo = _hianyzok(kozos)
    if not hianyzo:
        print(f"Rendben: minden osztálynak van stílusa ({len(kozos)} ismert).")
        return 0
    print(f"HIÁNYZÓ STÍLUS ({len(hianyzo)} osztály):")
    for nev in sorted(hianyzo):
        print(f"  .{nev:<28} — {', '.join(sorted(hianyzo[nev]))}")
    print("\nEz nem feltétlenül hiba: lehet, hogy a JavaScript adja hozzá,")
    print("vagy szándékosan nincs stílusa. De ha valami csúnyán néz ki,")
    print("itt kezdd a keresést.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
