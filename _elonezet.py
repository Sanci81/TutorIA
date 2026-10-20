"""Ideiglenes előnézet: python _elonezet.py feladatok.json  →  _elonezet.html
A json: [[jelölő-json, es (true/false), osztály, tantárgy], ...]."""
import re, json, io, sys, contextlib
with contextlib.redirect_stderr(io.StringIO()), contextlib.redirect_stdout(io.StringIO()):
    import app
sys.stdout.reconfigure(encoding="utf-8")

src = open("templates/chat.html", encoding="utf-8").read()
css = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", src, re.S))
css = re.sub(r"\{\{.*?\}\}|\{%.*?%\}", "", css)
js = src[src.index("    var DM = {};"):src.index("    function feladatElem(f)")]

lista = json.load(open(sys.argv[1], encoding="utf-8"))
feladatok = []
for jel, es, grade in lista:
    r = app._feladat_parse("x <FELADAT>" + jel + "</FELADAT>", grade=grade, es_tanterv=es)
    print(("ES " if es else "HU ") + jel, "->", r)
    if r:
        feladatok.append(r)

kattint = open(sys.argv[2], encoding="utf-8").read() if len(sys.argv) > 2 else ""
html = """<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;800;900&display=swap" rel="stylesheet">
<style>""" + css + """
body{background:#EAF3EE;padding:12px;display:block!important;overflow:auto!important;height:auto!important;font-family:Nunito,sans-serif}
.racs{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.racs>div{background:#fff;border-radius:18px;padding:14px}
.feladat-kerdes{font-weight:900;font-size:19px;margin-bottom:6px}
</style></head><body><div class="racs" id="r"></div>
<script>
var L = {feladatKesz: 'Kész'};
function ieKever(t){ return t.slice(); }
function ieUnnep(){}
function ieSzoKimond(){}
function ieKerdes(k){ var d=document.createElement('div'); d.className='feladat-kerdes'; d.textContent=k; return d; }
function feladatKuld(d, v){ var p=document.createElement('div'); p.style.cssText='margin-top:8px;color:#888;font-size:13px'; p.textContent='→ tanárnak: '+v; d.appendChild(p); }
""" + js + """
var F = """ + json.dumps(feladatok, ensure_ascii=False) + """;
F.forEach(function (f) { var w = document.createElement('div'); w.appendChild(dmFeladat(f)); document.getElementById('r').appendChild(w); });
var W = document.querySelectorAll('#r>div'), kat = function (e) { e.dispatchEvent(new MouseEvent('click', {bubbles: true})); };
if (location.hash === '#kattint') { try {
""" + kattint + """
} catch (e) { document.body.insertAdjacentHTML('afterbegin', '<pre style="color:red">' + e + '</pre>'); } }
</script></body></html>"""
open("_elonezet.html", "w", encoding="utf-8").write(html)
