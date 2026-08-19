# -*- coding: utf-8 -*-
"""Apró jelek a felülethez – album, tasak, kinézet.

MIÉRT NEM EMODZSI
    A 📕 és társai minden rendszeren máshogy néznek ki, és a Windows-változatuk
    egy elmosott kis piros kocka. Ez a három rajz mindenhol ugyanaz, a felület
    színét veszi fel, és apró méretben is felismerhető.
"""

from __future__ import annotations


def _svg(belso: str, meret: int = 20, szin: str = "currentColor") -> str:
    return (f'<svg viewBox="0 0 24 24" width="{meret}" height="{meret}" '
            f'fill="none" stroke="{szin}" stroke-width="1.9" '
            f'stroke-linecap="round" stroke-linejoin="round" '
            f'style="vertical-align:-4px">{belso}</svg>')


# Album: nyitott könyv, benne egy lap helye – nem sima könyv, hanem GYŰJTŐ.
ALBUM = ('<path d="M3 5.5c2.6-1 5.4-1 7.5.8v13c-2.1-1.8-4.9-1.8-7.5-.8z"/>'
         '<path d="M21 5.5c-2.6-1-5.4-1-7.5.8v13c2.1-1.8 4.9-1.8 7.5-.8z"/>'
         '<rect x="14.6" y="8.4" width="4.6" height="6.4" rx="0.8"/>')

# Tasak: fogazott tetejű zacskó – ugyanaz a forma, mint a bontásnál.
TASAK = ('<path d="M6.5 6.5h11v12a2 2 0 0 1-2 2h-7a2 2 0 0 1-2-2z"/>'
         '<path d="M6.5 6.5 8 4.6l1.5 1.9L11 4.6l1.5 1.9L14 4.6l1.5 1.9L17 4.6"/>'
         '<path d="M10 11.5h4"/>')

# Kinézet: ecset – az érme külalakra megy el.
KINEZET = ('<path d="M15.5 4.5 19.5 8.5 11 17a3.5 3.5 0 0 1-2 1l-3.5.5.5-3.5a3.5 3.5 0 0 1 1-2z"/>'
           '<path d="M13.6 6.4 17.6 10.4"/>')


def album(meret: int = 20, szin: str = "currentColor") -> str:
    return _svg(ALBUM, meret, szin)


def tasak(meret: int = 20, szin: str = "currentColor") -> str:
    return _svg(TASAK, meret, szin)


def kinezet(meret: int = 20, szin: str = "currentColor") -> str:
    return _svg(KINEZET, meret, szin)
