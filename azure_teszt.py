# -*- coding: utf-8 -*-
"""
Él-e az Azure Speech kulcs? – független teszt.

MIÉRT VAN EZ
    Az éles naplóban ez áll:  azure hiba: <HTTPError 401: 'Unauthorized'>
    A 401 azt jelenti, hogy az Azure ELUTASÍTJA A KULCSOT. Ez a hitelesítésnél
    dől el, MIELŐTT az Azure egyáltalán megnézné, mit küldtünk neki. Ha a
    kérésünk tartalmában lenne hiba (rossz SSML, ismeretlen hangnév), a válasz
    400 Bad Request lenne, nem 401.

    Ez a script NEM használja a TutorIA kódját. Egyetlen dolgot csinál:
    fogja a kulcsot és a régiót, és kér egy tokent az Azure-tól. Ha itt is
    401 jön, akkor a kulcs vagy a régió a hibás – a programhoz semmi köze.

HASZNÁLAT (PowerShell, a saját gépeden)
    $env:AZURE_SPEECH_KEY = "..."        # a Railway-en beállított érték
    $env:AZURE_SPEECH_REGION = "..."     # ugyanaz
    python azure_teszt.py

    A kulcsot és a régiót az Azure portálon találod:
    a Speech erőforrásod → Keys and Endpoint. A KULCSNAK ÉS A RÉGIÓNAK
    UGYANARRÓL AZ OLDALRÓL kell származnia.
"""

from __future__ import annotations

import os
import sys
import urllib.error
import urllib.request


def cim(sz: str) -> None:
    print("\n" + "=" * 60)
    print(sz)
    print("=" * 60)


kulcs = (os.environ.get("AZURE_SPEECH_KEY") or "").strip()
regio = (os.environ.get("AZURE_SPEECH_REGION") or "").strip().lower()
nyers_regio = os.environ.get("AZURE_SPEECH_REGION") or ""

cim("1. MIT LÁTOK A KÖRNYEZETI VÁLTOZÓKBAN?")
if not kulcs:
    print("AZURE_SPEECH_KEY: NINCS BEÁLLÍTVA ebben az ablakban")
else:
    print(f"AZURE_SPEECH_KEY: megvan, {len(kulcs)} karakter, "
          f"eleje: {kulcs[:4]}…, vége: …{kulcs[-4:]}")
    if len(kulcs) not in (32, 84):
        print(f"  FIGYELEM: a Speech kulcs általában 32 karakter "
              f"(vagy 84 az újabb formátumban). Ez {len(kulcs)}.")

if not regio:
    print("AZURE_SPEECH_REGION: NINCS BEÁLLÍTVA")
else:
    print(f"AZURE_SPEECH_REGION: {regio!r}")
    if nyers_regio != nyers_regio.strip():
        print("  FIGYELEM: szóköz vagy sortörés van a régió körül!")
    if " " in regio or regio != regio.lower():
        print("  FIGYELEM: a régió rövid, kisbetűs alak legyen —")
        print("  pl. 'westeurope', NEM 'West Europe'.")

if not kulcs or not regio:
    print("\nA teszt itt megáll: állítsd be mind a kettőt, és indítsd újra.")
    sys.exit(1)


cim("2. ELFOGADJA-E AZ AZURE A KULCSOT?")
print(f"Kérés ide: https://{regio}.api.cognitive.microsoft.com"
      f"/sts/v1.0/issueToken")

url = f"https://{regio}.api.cognitive.microsoft.com/sts/v1.0/issueToken"
keres = urllib.request.Request(
    url,
    data=b"",
    headers={"Ocp-Apim-Subscription-Key": kulcs,
             "Content-Length": "0",
             "User-Agent": "TutorIA-azure-teszt"},
    method="POST",
)

try:
    with urllib.request.urlopen(keres, timeout=20) as valasz:
        token = valasz.read().decode("utf-8", "replace")
    print(f"\n✅ RENDBEN – az Azure kiadott egy tokent ({len(token)} karakter).")
    print("A kulcs és a régió JÓ. Ha az éles oldalon mégis 401 jön, akkor")
    print("a Railway-en más érték van beállítva, mint amit itt megadtál.")
except urllib.error.HTTPError as exc:
    torzs = ""
    try:
        torzs = exc.read().decode("utf-8", "replace")[:300]
    except Exception:
        pass
    print(f"\n❌ HTTP {exc.code}: {exc.reason}")
    if torzs:
        print(f"a válasz: {torzs}")
    if exc.code == 401:
        print("""
401 = az Azure NEM FOGADJA EL A KULCSOT. Három oka lehet:

  1. A RÉGIÓ NEM EGYEZIK A KULCCSAL. Minden kulcs EGY régióhoz tartozik.
     Azure portál → a Speech erőforrásod → Keys and Endpoint: ott van
     kiírva a régió. Pontosan azt kell beírni, rövid kisbetűs alakban.

  2. A KULCS MÁR NEM ÉL. Ha valaha megnyomtad a Regenerate Key gombot,
     a régi azonnal érvénytelen lett. Másold ki újra a KEY 1-et.

  3. AZ ERŐFORRÁS LE VAN TILTVA. Lejárt ingyenes próbaidőszak, elfogyott
     a kredit, vagy törölt erőforrás esetén szintén 401 jön. Azure portál
     → az erőforrás → Overview: ott látszik, ha nem aktív.

FONTOS: ez a script a TutorIA kódjából SEMMIT nem használ. Ha itt 401 van,
akkor a hiba a kulcs/régió/előfizetés oldalán van, nem a programban.""")
    elif exc.code == 403:
        print("403 = a kulcs jó, de ehhez a művelethez nincs jogosultság.")
    else:
        print("Nem 401: ez már nem hitelesítési hiba.")
except Exception as exc:
    print(f"\n❌ Nem sikerült elérni az Azure-t: {type(exc).__name__}: {exc}")
    print("Ez hálózati hiba, nem a kulcs hibája.")

cim("VÉGE – küldd át az egész kimenetet")
