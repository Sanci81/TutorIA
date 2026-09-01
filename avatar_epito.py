# -*- coding: utf-8 -*-
"""A szétvágott részekből összerakja a mozgó avatart (bemutató oldal).

A képeket base64-ként ágyazza be, hogy egyetlen fájl legyen, amit
kattintásra meg lehet nyitni — nincs útvonal-gond.
"""

from __future__ import annotations

import base64
import json
from pathlib import Path

MAPPA = Path(__file__).parent / "avatar"
ADAT = json.loads((MAPPA / "adatok.json").read_text())


def _b64(nev: str) -> str:
    return "data:image/png;base64," + base64.b64encode((MAPPA / nev).read_bytes()).decode()


def figura(n: str, azon: str) -> str:
    a = ADAT[n]
    W, H = a["kep"]

    def kep(r: str) -> str:
        d = a[r]
        return (f'<img data-r="{r}" src="{_b64(f"{n}_{r}.png")}" '
                f'style="left:{d[0]}px;top:{d[1]}px">')

    sz, fd = a["szaj_kp"], a["fej"]
    fw, fh = fd[2] - fd[0], fd[3] - fd[1]
    szx, szy, szw = fd[0] + fw * sz[0], fd[1] + fh * sz[1], fw * sz[2]

    r = [f'<div class="fejcsop" style="transform-origin:{(fd[0]+fd[2])/2}px {fd[3]}px">',
         kep("fej"),
         f'<div class="szaj" style="left:{szx-szw/2:.0f}px;top:{szy-szw*.10:.0f}px;'
         f'width:{szw:.0f}px;height:{szw*.44:.0f}px"></div></div>',
         kep("torzs")]
    for o in ("bal", "jobb"):
        v, k = a[f"vall_{o}"], a[f"konyok_{o}"]
        r.append(
            f'<div class="kar {o}" style="transform-origin:{v[0]}px {v[1]}px">'
            f'{kep(f"felkar_{o}")}'
            f'<div class="alkar {o}" style="transform-origin:{k[0]}px {k[1]}px">'
            f'{kep(f"alkar_{o}")}</div></div>')
    return (f'<div class="figura" id="{azon}" style="width:{W}px;height:{H}px">'
            + "".join(r) + '</div>')


SABLON = """<!doctype html><html lang="hu"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>TutorIA – avatar</title><style>
:root{--kek:#1f3a63;--zold:#16a34a;--papir:#f6f8fb;--keret:#d9dee7;--szurke:#5b6474}
*{box-sizing:border-box}
body{margin:0;background:var(--papir);color:#1a1f2b;font:16px/1.6 system-ui,-apple-system,sans-serif}
header{background:#fff;border-bottom:1px solid var(--keret);padding:16px 20px}
h1{margin:0 0 3px;font-size:1.3rem} header p{margin:0;color:var(--szurke);font-size:.93rem}
.vez{position:sticky;top:0;z-index:9;background:#fff;border-bottom:1px solid var(--keret);
     padding:11px 20px;display:flex;gap:7px;flex-wrap:wrap;align-items:center}
.vez b{font-size:.88rem;color:var(--szurke)}
button{font:inherit;font-size:.9rem;padding:6px 13px;border-radius:999px;border:1px solid var(--keret);
       background:#fff;cursor:pointer}
button:hover{border-color:#9aa4b5} button.aktiv{background:var(--kek);border-color:var(--kek);color:#fff}
.racs{display:flex;gap:20px;justify-content:center;flex-wrap:wrap;padding:22px 20px 6px}
.doboz{background:#fff;border:1px solid var(--keret);border-radius:16px;padding:14px;text-align:center}
.doboz h2{margin:0 0 8px;font-size:1rem}
.szinpad{background:linear-gradient(#eef4ff,#e8f6ed);border-radius:12px;position:relative;
         overflow:hidden}
.figura{position:relative;transform-origin:top left}
.figura img{position:absolute;display:block}
.figura div{position:absolute}
.figura>.fejcsop,.figura>.kar,.kar>.alkar{left:0;top:0;width:100%;height:100%}
.kar,.alkar,.fejcsop{transition:transform .40s cubic-bezier(.34,.9,.4,1)}
.fejcsop{animation:fejmozog 7s ease-in-out infinite}
@keyframes fejmozog{0%,100%{transform:rotate(-1deg)}50%{transform:rotate(1deg)}}
.szaj{border-radius:50% 50% 46% 46%;background:#6d2f33;
      box-shadow:inset 0 -22% 0 rgba(255,255,255,.14);
      transform-origin:center top;transform:scaleY(var(--nyit,0));
      opacity:var(--szajlat,0);transition:transform .07s,opacity .18s}
.eles{max-width:980px;margin:0 auto;padding:8px 20px 40px}
.eles h3{font-size:1rem;margin:0 0 10px}
.chatdoboz{background:#fff;border:1px solid var(--keret);border-radius:16px;padding:14px;
           display:flex;gap:12px;align-items:flex-end}
.bub{background:var(--zold);color:#fff;border-radius:16px;padding:11px 15px;font-size:.93rem;max-width:520px}
.megj{max-width:980px;margin:0 auto;padding:0 20px 60px;color:var(--szurke);font-size:.92rem}
</style></head><body>
<header><h1>TutorIA – avatar a te Leonardo-figuráidból</h1>
<p>Ugyanaz a mozgásváz, csak most a generált rajz van rajta, darabokra vágva.</p></header>
<div class="vez"><b>Mit csinál:</b>
<button id="beszel">▶ Magyaráz (beszél)</button>
<button class="moz aktiv" data-m="pihen">Áll</button>
<button class="moz" data-m="mutat">Rámutat</button>
<button class="moz" data-m="tapsol">Tapsol</button>
<button class="moz" data-m="gondolkodik">Gondolkodik</button>
<button class="moz" data-m="integet">Integet</button></div>
<div class="racs">
  <div class="doboz"><h2>Nő</h2><div class="szinpad" id="sz1"></div></div>
  <div class="doboz"><h2>Férfi</h2><div class="szinpad" id="sz2"></div></div>
</div>
<div class="eles"><h3>Így néz ki a chat mellett</h3>
<div class="chatdoboz"><div class="szinpad" id="sz3" style="background:none"></div>
<div class="bub">A téglatest térfogata a hossz, a szélesség és a magasság szorzata.
Nézd meg az ábrán: az <b>a</b> a hosszúság, a <b>b</b> a szélesség, az <b>m</b> a magasság.</div>
</div></div>
<div class="megj"><p>A száj most szabályos ütemben mozog, mert nincs valódi hang.
Élesben a felolvasott hang tényleges hangerejéhez igazodik. A nyugalmi mosolyt a rajz
adja; beszéd közben úszik rá az animált száj.</p></div>
<script>
const FIG = { no: NOFIG, ferfi: FERFIFIG };
/* A kinyújtott kar kilóg a kép eredeti szélességéből, ezért a színpad
   SZÉLESEBB, mint a figura, és középre tesszük. Enélkül levágná a kezet. */
function beilleszt(hova, nev, magassag, kereszt=1.7){
  const d = document.getElementById(hova);
  d.innerHTML = FIG[nev];
  const f = d.querySelector('.figura');
  const fw = parseFloat(f.style.width), fh = parseFloat(f.style.height);
  const s = magassag / fh;
  const szelesseg = fw * s * kereszt;
  f.style.transform = `translateX(${(szelesseg - fw*s)/2}px) scale(${s})`;
  d.style.width = szelesseg + 'px';
  d.style.height = magassag + 'px';
}
beilleszt('sz1','no',430); beilleszt('sz2','ferfi',430); beilleszt('sz3','no',150,1.25);

const MOZ = {
  pihen:      {bal:[0,0],    jobb:[0,0]},
  magyarazA:  {bal:[18,-40], jobb:[-22,44]},
  magyarazB:  {bal:[30,-22], jobb:[-12,58]},
  magyarazC:  {bal:[12,-52], jobb:[-32,26]},
  mutat:      {bal:[4,-8],   jobb:[-58,-16]},
  tapsol:     {bal:[26,-62], jobb:[-26,62]},
  gondolkodik:{bal:[12,-46], jobb:[-34,-70]},
  integet:    {bal:[2,-6],   jobb:[-104,26]},
};
const mind = s => Array.from(document.querySelectorAll(s));
function allit(p){
  mind('.figura').forEach(f=>{
    for (const o of ['bal','jobb']){
      const kar=f.querySelector('.kar.'+o), al=f.querySelector('.alkar.'+o);
      if(kar) kar.style.transform=`rotate(${p[o][0]}deg)`;
      if(al)  al.style.transform =`rotate(${p[o][1]}deg)`;
    }
  });
}
let besz=false, t=0, tSzaj=null, tGeszt=null, gi=0;
const SOR=['magyarazA','magyarazB','magyarazC','magyarazB'];
document.getElementById('beszel').onclick=function(){
  besz=!besz; this.classList.toggle('aktiv',besz);
  this.textContent = besz? '■ Elhallgat' : '▶ Magyaráz (beszél)';
  mind('.figura').forEach(f=>f.style.setProperty('--szajlat', besz?1:0));
  if(besz){
    mind('.moz').forEach(x=>x.classList.remove('aktiv'));
    tSzaj=setInterval(()=>{ t+=.13;
      const n=.10+Math.abs(Math.sin(t*3.1))*.62+Math.abs(Math.sin(t*7.7))*.26;
      mind('.figura').forEach(f=>f.style.setProperty('--nyit',n.toFixed(2)));},70);
    const lep=()=>allit(MOZ[SOR[gi++%SOR.length]]); lep();
    tGeszt=setInterval(lep,950);
  } else {
    clearInterval(tSzaj); clearInterval(tGeszt);
    mind('.figura').forEach(f=>f.style.setProperty('--nyit',0));
    allit(MOZ.pihen);
    document.querySelector('.moz[data-m="pihen"]').classList.add('aktiv');
  }
};
mind('.moz').forEach(b=>b.onclick=function(){
  if(besz) document.getElementById('beszel').click();
  mind('.moz').forEach(x=>x.classList.remove('aktiv')); this.classList.add('aktiv');
  allit(MOZ[this.dataset.m]);
});
</script></body></html>"""


if __name__ == "__main__":
    lap = (SABLON.replace("NOFIG", json.dumps(figura("no", "f-no")))
                 .replace("FERFIFIG", json.dumps(figura("ferfi", "f-ferfi"))))
    ki = Path(__file__).parent / "avatar_kesz.html"
    ki.write_text(lap, encoding="utf-8")
    print(f"kesz: {len(lap)//1024} KB -> {ki}")
