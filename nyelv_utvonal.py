"""A NYELV A CÍMBEN — /es/ előtag a spanyol oldalnak.

MIÉRT KELL. Ma a nyelv a munkamenetben él: ugyanaz a cím (`/csomagok`)
szolgálja ki a magyart és a spanyolt is, attól függően, mire kattintott a
látogató. Egy keresőnek ez azt jelenti, hogy CSAK EGY változat létezik —
a spanyol oldalt soha nem fogja megtalálni, és hreflanget sem lehet
kiírni, mert nincs mire hivatkozni.

MIT CSINÁL. Leszedi a cím elejéről az `/es` előtagot, mielőtt a Flask
egyáltalán megnézné, melyik útvonalról van szó. Így `/es/csomagok` és
`/csomagok` UGYANAZT a programrészt hívja — nem kell minden útvonalat
megduplázni, és a leckeoldalakhoz nem kell hozzányúlni.

A SCRIPT_NAME A LÉNYEG, és könnyű elnézni. Nem elég az előtagot leszedni:
ha csak azt tennénk, a lapon lévő összes hivatkozás előtag NÉLKÜL
képződne, és a spanyol látogató az első kattintással visszaesne a magyar
oldalra. A SCRIPT_NAME beállításával a Flask `url_for` MAGÁTÓL kiírja az
`/es` előtagot minden belső hivatkozásnál. Egy sor, de ezen áll az egész.

AMIT SZÁNDÉKOSAN NEM CSINÁL. Nem dönt a nyelvről — csak megjelöli a
kérést. A döntés marad ott, ahol eddig volt (`load_language` az app.py-ban),
hogy egy helyen legyen. A munkamenetes váltó (`/lang/es`) is működik
tovább: ez a réteg csak akkor szól közbe, ha a címben ott az előtag.
"""

# Melyik előtag melyik nyelvet jelenti. Bővíteni itt kell, ha egyszer
# harmadik nyelv jön – a program többi részéhez nem kell hozzányúlni.
ELOTAGOK: dict[str, str] = {
    "/es": "es",
}

# A kérés megjelölése ezen a kulcson megy át a Flask felé.
KULCS = "tutoria.nyelv"

# ── SPANYOL CÍMEK (fix163, SEO) ──────────────────────────────────────────
# A spanyol oldal eddig magyar szavakkal élt (/es/csomagok). A spanyol
# kereső a címben lévő szavakat is nézi, ezért spanyol cím kell. A program
# BELÜL továbbra is a magyar útvonalat használja – ez a réteg fordít oda-
# vissza: bejövő /es/precios → /csomagok, kimenő url_for /es/csomagok →
# /es/precios. A régi /es/csomagok címek 301-gyel átirányítanak (a Google
# így átviszi az eddigi értékelést). Kikapcsolás: SPANYOL_CIMEK = {}.
# Bővíteni csak ide kell. Az alcímek is fordulnak (/minta/3 → /clase-de-prueba/3).
SPANYOL_CIMEK: dict[str, str] = {
    "/csomagok": "/precios",
    "/register": "/registro",
    "/login": "/iniciar-sesion",
    "/gyik": "/preguntas-frecuentes",
    "/adatvedelem": "/privacidad",
    "/feltetelek": "/condiciones",
    "/impresszum": "/aviso-legal",
    "/hogy-megy": "/como-funciona",
    "/minta": "/clase-de-prueba",
    "/forgot-password": "/recuperar-contrasena",
    "/blog/hogyan-segit-az-ai-a-gyerekek-tanulasaban":
        "/blog/como-ayuda-la-ia-al-aprendizaje-de-los-ninos",
}
_SPANYOLBOL = {v: k for k, v in SPANYOL_CIMEK.items()}


def _csere(ut: str, szotar: dict[str, str]) -> str | None:
    """A leghosszabb illeszkedő elejét cseréli (pontos egyezés vagy alcím)."""
    for kulcs in sorted(szotar, key=len, reverse=True):
        if ut == kulcs or ut.startswith(kulcs + "/"):
            return szotar[kulcs] + ut[len(kulcs):]
    return None


def spanyolra(ut: str) -> str:
    """Belső (magyar) útvonal → spanyol cím. Ha nincs fordítása, marad."""
    return _csere(ut, SPANYOL_CIMEK) or ut


def spanyolbol(ut: str) -> str:
    """Spanyol cím → belső útvonal. Ha nem spanyol cím, marad."""
    return _csere(ut, _SPANYOLBOL) or ut


def kimeno_cim(cim: str) -> str:
    """url_for eredménye: ha /es/ alatti lap, a spanyol szót teszi bele.
    Sima (/es/...) és teljes (https://…/es/...) címmel is működik."""
    if not SPANYOL_CIMEK:
        return cim
    for elo, ny in ELOTAGOK.items():
        if ny != "es":
            continue
        if "://" in cim:
            eleje, _, maradek = cim.partition("://")
            gep, per, ut = maradek.partition("/")
            if not per:
                return cim
            uj = kimeno_cim("/" + ut)
            return f"{eleje}://{gep}{uj}"
        ut, kerdo, query = cim.partition("?")
        ut, hash_, horgony = ut.partition("#")
        if ut.startswith(elo + "/") and not ut.startswith(elo + "/static/"):
            ut = elo + spanyolra(ut[len(elo):])
        return ut + hash_ + horgony + kerdo + query
    return cim


class NyelvElotag:
    """WSGI köztes réteg: a nyelvi előtagot leszedi a címről."""

    def __init__(self, wsgi_app):
        self._wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        utvonal = environ.get("PATH_INFO", "") or "/"
        for elotag, nyelv in ELOTAGOK.items():
            # CSAK a pontos előtag vagy az alatta lévő címek. A feltétel
            # második fele nélkül egy „/estebanjaimes" nevű útvonal is
            # beleesne – ilyen ma nincs, de egyszer lehet.
            if utvonal == elotag or utvonal.startswith(elotag + "/"):
                belso = utvonal[len(elotag):] or "/"
                if nyelv == "es" and SPANYOL_CIMEK:
                    spanyol = spanyolra(belso)
                    # Régi, magyar szavas cím a spanyol oldalon → 301 az újra.
                    if (spanyol != belso
                            and environ.get("REQUEST_METHOD", "GET") in ("GET", "HEAD")):
                        cel = environ.get("SCRIPT_NAME", "") + elotag + spanyol
                        if environ.get("QUERY_STRING"):
                            cel += "?" + environ["QUERY_STRING"]
                        start_response("301 Moved Permanently",
                                       [("Location", cel), ("Content-Length", "0")])
                        return [b""]
                    belso = spanyolbol(belso)
                environ["SCRIPT_NAME"] = (
                    environ.get("SCRIPT_NAME", "") + elotag)
                environ["PATH_INFO"] = belso
                environ[KULCS] = nyelv
                break
        return self._wsgi_app(environ, start_response)


def nyelv_a_cimbol(environ) -> str | None:
    """A kéréshez tartozó nyelv, ha a címben volt előtag. Különben None."""
    return environ.get(KULCS)


def alap_utvonal(utvonal: str) -> str:
    """A cím nyelvi előtag NÉLKÜL – ez kell a hreflang tagekhez.

    A hreflangnak minden nyelvi változatot fel kell sorolnia, és
    mindegyiknek UGYANARRA a tartalomra kell mutatnia. Ezért a kiírás
    előtt le kell csupaszítani a címet, akármelyik nyelven vagyunk épp.
    """
    for elotag in ELOTAGOK:
        if utvonal == elotag or utvonal.startswith(elotag + "/"):
            return spanyolbol(utvonal[len(elotag):] or "/")   # fix163
    return utvonal or "/"


def elotag(nyelv: str) -> str:
    """Az adott nyelv előtagja. A magyar a gyökéren van, annak üres."""
    for elo, ny in ELOTAGOK.items():
        if ny == nyelv:
            return elo
    return ""


def nyelvi_cim(utvonal: str, nyelv: str) -> str:
    """Ugyanaz a tartalom a kért nyelv címén. A hreflang és a nyelvváltó
    gomb is ezt használja, hogy a kettő soha ne mondjon mást."""
    alap = alap_utvonal(utvonal)
    if nyelv == "es":
        alap = spanyolra(alap)                                  # fix163
    return (elotag(nyelv) + alap) or "/"


def statikus_elotag_nelkul(cim: str) -> str:
    """A CSS, a betűtípus és a képek EGYETLEN címen éljenek.

    A SCRIPT_NAME minden hivatkozásra ráteszi az előtagot – a lapok
    esetében pont ez a cél, a fájloknál viszont nem: ugyanaz a CSS így két
    címen lenne elérhető, és aki mindkét nyelvet megnézi, kétszer töltené
    le. A böngésző gyorstára címre emlékszik, nem tartalomra.

    Sima (`/es/static/...`) és teljes (`https://…/es/static/...`) címmel is
    számolunk, mert az előnézeti képnél teljes cím képződik.
    """
    for elo in ELOTAGOK:
        if cim.startswith(elo + "/static/"):
            return cim[len(elo):]
        jeloles = elo + "/static/"
        if "://" in cim and jeloles in cim:
            return cim.replace(jeloles, "/static/", 1)
    return cim
