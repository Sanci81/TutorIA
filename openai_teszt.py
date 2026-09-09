# -*- coding: utf-8 -*-
"""
Miért nem éri el a gépem az OpenAI-t? – rövid diagnosztika.

Az "APIConnectionError: Connection error." semmit nem mond meg: elrejti a
VALÓDI okot (DNS, tanúsítvány, tűzfal, proxy, rossz kulcs). Ez a script
lépésenként végigpróbálja, és minden lépésnél kiírja a pontos hibát.

    python openai_teszt.py

Küldd át nekem a teljes kimenetet, és megmondom, mit kell csinálni.
"""

from __future__ import annotations

import os
import socket
import ssl
import sys
import traceback


def cim(szoveg: str) -> None:
    print("\n" + "=" * 60)
    print(szoveg)
    print("=" * 60)


def okok(exc: BaseException) -> None:
    """Az egymásba csomagolt hibák kibontása – ITT van a valódi ok."""
    szint = 0
    e: BaseException | None = exc
    while e is not None:
        print(f"  {'  ' * szint}→ {type(e).__name__}: {e}")
        e = e.__cause__ or e.__context__
        szint += 1
        if szint > 6:
            break


# ── 1. Alapok ───────────────────────────────────────────────────────────────
cim("1. VERZIÓK")
print(f"Python: {sys.version.split()[0]}")
try:
    import openai
    print(f"openai csomag: {openai.__version__}")
except Exception as exc:
    print("openai csomag: NINCS TELEPÍTVE")
    okok(exc)
    sys.exit(1)

try:
    import httpx
    print(f"httpx: {httpx.__version__}")
except Exception:
    print("httpx: nincs")

kulcs = os.environ.get("OPENAI_API_KEY") or ""
if not kulcs:
    print("OPENAI_API_KEY: NINCS BEÁLLÍTVA ebben az ablakban")
else:
    print(f"OPENAI_API_KEY: megvan, {len(kulcs)} karakter, "
          f"így kezdődik: {kulcs[:7]}…, így végződik: …{kulcs[-4:]}")
    if kulcs != kulcs.strip():
        print("  FIGYELEM: szóköz vagy sortörés van a kulcs elején/végén!")

# Proxy-beállítások – ezek csendben elronthatják a kapcsolatot
for v in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy",
          "ALL_PROXY", "REQUESTS_CA_BUNDLE", "SSL_CERT_FILE"):
    if os.environ.get(v):
        print(f"proxy/tanúsítvány beállítás: {v} = {os.environ[v]}")


# ── 2. Névfeloldás ──────────────────────────────────────────────────────────
cim("2. MEGTALÁLJA-E A GÉPED AZ api.openai.com-ot? (DNS)")
try:
    ip = socket.gethostbyname("api.openai.com")
    print(f"OK – api.openai.com = {ip}")
except Exception as exc:
    print("NEM SIKERÜLT")
    okok(exc)


# ── 3. Titkosított kapcsolat ────────────────────────────────────────────────
cim("3. LÉTREJÖN-E A BIZTONSÁGOS KAPCSOLAT? (SSL)")
try:
    ctx = ssl.create_default_context()
    with socket.create_connection(("api.openai.com", 443), timeout=15) as s:
        with ctx.wrap_socket(s, server_hostname="api.openai.com") as ss:
            print(f"OK – {ss.version()}")
            tan = ss.getpeercert()
            kiado = dict(x[0] for x in tan.get("issuer", ()))
            print(f"a tanúsítványt kiállította: "
                  f"{kiado.get('organizationName', '?')}")
            if "openai" not in str(tan).lower() and \
               kiado.get("organizationName", "").lower() not in ("", "?"):
                pass
except Exception as exc:
    print("NEM SIKERÜLT – ez a leggyakoribb ok: vírusirtó vagy tűzfal")
    print("(ESET, Kaspersky, Avast: a HTTPS-vizsgálat saját tanúsítványt tesz")
    print(" a kapcsolatba, és a Python ezt nem fogadja el)")
    okok(exc)


# ── 4. Egy egyszerű HTTPS kérés ─────────────────────────────────────────────
cim("4. VÁLASZOL-E AZ OPENAI EGY EGYSZERŰ KÉRÉSRE?")
try:
    import httpx
    r = httpx.get("https://api.openai.com/v1/models",
                  headers={"Authorization": f"Bearer {kulcs}"}, timeout=30)
    print(f"HTTP {r.status_code}")
    if r.status_code == 200:
        print("OK – a kulcs jó, a hálózat jó.")
    else:
        print(f"a válasz eleje: {r.text[:300]}")
except Exception as exc:
    print("NEM SIKERÜLT")
    okok(exc)


# ── 5. Szöveges hívás ───────────────────────────────────────────────────────
cim("5. MŰKÖDIK-E EGY SZÖVEGES HÍVÁS?")
try:
    from openai import OpenAI
    kliens = OpenAI(api_key=kulcs, timeout=60.0, max_retries=0)
    v = kliens.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Mondd: rendben"}],
    )
    print("OK –", (v.choices[0].message.content or "").strip()[:60])
except Exception as exc:
    print("NEM SIKERÜLT")
    okok(exc)
    traceback.print_exc()


# ── 6. Képgenerálás ─────────────────────────────────────────────────────────
cim("6. MŰKÖDIK-E A KÉPGENERÁLÁS? (ez tarthat 1-2 percet)")
try:
    from openai import OpenAI
    kliens = OpenAI(api_key=kulcs, timeout=180.0, max_retries=0)
    v = kliens.images.generate(
        model="gpt-image-1",
        prompt="A simple red circle on a white background.",
        size="1024x1024",
        quality="low",
    )
    import base64
    from pathlib import Path
    adat = base64.b64decode(v.data[0].b64_json)
    Path("teszt_kep.png").write_bytes(adat)
    print(f"OK – kimentve: teszt_kep.png ({len(adat)} bájt)")
except Exception as exc:
    print("NEM SIKERÜLT")
    okok(exc)
    print("\nHa itt 403 vagy 'must be verified' szerepel: a gpt-image-1")
    print("modellhez az OpenAI szervezet-ellenőrzés kell.")
    print("platform.openai.com → Settings → Organization → General → Verify")

cim("VÉGE – küldd át az EGÉSZ kimenetet")
