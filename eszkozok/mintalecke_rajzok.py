# Mintalecke rajzok (fix131, 2026-11-11) – futtatás: python eszkozok/mintalecke_rajzok.py
# A béka (beka.svg) és a fazék (forras.svg) külön, kézzel készült; ezt a fájlt nem írja felül.
import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "static", "img", "minta"); os.makedirs(OUT, exist_ok=True)
RM = "@media (prefers-reduced-motion:reduce){*{animation:none !important}}"
def svg(name, body, css="", vb="0 0 200 150"):
    s = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">'
    if css: s += f"<style>{css}{RM}</style>"
    s += body + "</svg>"
    open(f"{OUT}/{name}.svg", "w").write(s)
def arnyek(cx=100, cy=138, rx=46, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<ellipse{c} cx="{cx}" cy="{cy}" rx="{rx}" ry="7" fill="#E3EEE8"/>'
def alma_rajz(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})">'
            '<path d="M0 -20 C-6 -26 -24 -26 -27 -6 C-30 14 -14 30 -6 28 C-3 27 3 27 6 28 C14 30 30 14 27 -6 C24 -26 6 -26 0 -20Z" fill="#E5484D"/>'
            '<path d="M6 28 C14 30 30 14 27 -6 C25 -18 16 -24 8 -23 C20 -14 22 10 6 28Z" fill="#C93439"/>'
            '<ellipse cx="-14" cy="-8" rx="5" ry="9" fill="#fff" opacity=".45" transform="rotate(20 -14 -8)"/>'
            '<path d="M0 -20 Q1 -30 5 -36" stroke="#7A4A23" stroke-width="4" fill="none" stroke-linecap="round"/>'
            '<path d="M4 -30 Q16 -40 26 -32 Q16 -24 4 -30Z" fill="#3DBE72"/></g>')

# 1. ALMA
svg("alma", arnyek(100,138,40,"a") + '<g class="b">' + alma_rajz(100, 82, 1.7) + '</g>',
    ".b{animation:b 2.4s ease-in-out infinite}.a{animation:a 2.4s ease-in-out infinite;transform-origin:100px 138px}"
    "@keyframes b{50%{transform:translateY(-6px)}}@keyframes a{50%{transform:scale(.85)}}")

# 2. HAL
svg("hal",
    '<path d="M10 128 q15 -8 30 0 t30 0 t30 0 t30 0 t30 0 t30 0" fill="none" stroke="#9AD0F2" stroke-width="4" stroke-linecap="round"/>'
    '<g fill="none" stroke="#9AD0F2" stroke-width="3"><circle class="bu" cx="150" cy="60" r="5"/><circle class="bu" style="animation-delay:.8s" cx="160" cy="70" r="3.5"/><circle class="bu" style="animation-delay:1.6s" cx="146" cy="76" r="3"/></g>'
    '<g class="h"><g class="f" ><path d="M58 72 L28 48 Q34 72 28 96Z" fill="#E07B39"/></g>'
    '<ellipse cx="96" cy="72" rx="46" ry="30" fill="#F59E0B"/>'
    '<path d="M80 44 q12 -16 30 -2 q-14 4 -30 2Z" fill="#E07B39"/><path d="M86 100 q10 12 24 2 q-12 -2 -24 -2Z" fill="#E07B39"/>'
    '<path d="M84 46 q-10 26 0 52 M100 43 q-10 29 0 58" stroke="#FCD34D" stroke-width="6" fill="none" opacity=".8"/>'
    '<circle cx="122" cy="64" r="8" fill="#fff"/><circle cx="124" cy="64" r="4.5" fill="#163A2E"/><circle cx="125.5" cy="62.5" r="1.5" fill="#fff"/>'
    '<path d="M134 80 q4 3 8 0" stroke="#163A2E" stroke-width="3" fill="none" stroke-linecap="round"/></g>',
    ".h{animation:h 3s ease-in-out infinite}.f{animation:f .5s ease-in-out infinite alternate;transform-origin:58px 72px}"
    ".bu{animation:bu 2.4s ease-in infinite}"
    "@keyframes h{50%{transform:translate(-6px,4px)}}@keyframes f{to{transform:scaleY(.7)}}"
    "@keyframes bu{0%{transform:translateY(0);opacity:0}20%{opacity:1}100%{transform:translateY(-40px);opacity:0}}")

# 3. SÜN
tuskek = "".join(f'<path d="M{x} {y} l{dx} {dy} l{ex} {ey}" fill="#6B4528"/>' for (x,y,dx,dy,ex,ey) in [])
svg("sun",
    arnyek(100,132,58) +
    '<g class="t">'
    '<path d="M44 118 Q40 70 80 54 L86 40 L94 54 L102 38 L110 54 L118 40 L124 56 L134 46 L136 62 L148 58 L146 74 L156 76 L148 88 L160 96 L148 104 L154 118Z" fill="#7A4E2D"/>'
    '<path d="M50 112 Q50 76 82 62 L88 50 L95 62 L103 48 L110 62 L118 52 L122 66 L132 60 L132 74 L142 72 L140 86 L150 92 L140 100 L146 112Z" fill="#94603A"/>'
    '<g class="o"><path d="M58 120 Q44 78 66 74 Q48 82 18 106 Q10 114 20 120Z" fill="#F2D3B0"/>'
    '<circle cx="16" cy="110" r="6" fill="#163A2E"/><circle cx="17.5" cy="108" r="1.8" fill="#fff"/>'
    '<circle cx="46" cy="96" r="4.5" fill="#163A2E"/><circle cx="47.5" cy="94.5" r="1.5" fill="#fff"/>'
    '<circle cx="50" cy="108" r="4.5" fill="#F7A6A6" opacity=".8"/><path d="M26 116 q6 3 12 0" stroke="#163A2E" stroke-width="2" fill="none" stroke-linecap="round"/></g>'
    '<ellipse cx="66" cy="124" rx="9" ry="5" fill="#5A3A22"/><ellipse cx="130" cy="124" rx="9" ry="5" fill="#5A3A22"/></g>',
    ".t{animation:t 2.6s ease-in-out infinite;transform-origin:100px 124px}.o{animation:o 1.3s ease-in-out infinite}"
    "@keyframes t{50%{transform:scale(1.02,.98)}}@keyframes o{50%{transform:translate(-2px,1px)}}")

# 4. TÍZES KERET (8 + 2 + 3)
cells = ""
for r in range(2):
    for c in range(5):
        cells += f'<rect x="{18+c*26}" y="{40+r*26}" width="24" height="24" rx="5" fill="#fff" stroke="#BFD8CC" stroke-width="2"/>'
for r in range(2):
    for c in range(5):
        cells += f'<rect x="{18+c*26}" y="{100+r*26}" width="24" height="24" rx="5" fill="#fff" stroke="#E2E8E5" stroke-width="2" opacity="{1 if r==0 else .0}"/>'
dots = ""
for i in range(8):
    r, c = divmod(i, 5); dots += f'<circle cx="{30+c*26}" cy="{52+r*26}" r="9" fill="#2F8FD8"/>'
for k,i in enumerate([8,9]):
    r, c = divmod(i, 5); dots += f'<circle class="u1" cx="{30+c*26}" cy="{52+r*26}" r="9" fill="#F59E0B"/>'
for c in range(3):
    dots += f'<circle class="u2" cx="{30+c*26}" cy="112" r="9" fill="#F59E0B"/>'
svg("tizes", '<g transform="translate(26 -14)">' + cells + dots + '</g>',
    ".u1{animation:u1 4s ease-out infinite}.u2{animation:u2 4s ease-out infinite}"
    "@keyframes u1{0%,15%{opacity:0;transform:translateY(-8px)}30%,90%{opacity:1;transform:none}100%{opacity:0}}"
    "@keyframes u2{0%,40%{opacity:0;transform:translateY(-8px)}55%,90%{opacity:1;transform:none}100%{opacity:0}}")

# 5. TÍZES RUDAK (30 + 40)
def rud(x, col, cls, d):
    s = f'<g class="{cls}" style="animation-delay:{d}s">'
    for k in range(10):
        s += f'<rect x="{x}" y="{24+k*10}" width="14" height="9" rx="2" fill="{col}"/>'
    return s + "</g>"
body = "".join(rud(22+i*20, "#2F8FD8", "r", i*.15) for i in range(3))
body += '<path d="M92 72 h14 M99 65 v14" stroke="#163A2E" stroke-width="4" stroke-linecap="round"/>'
body += "".join(rud(116+i*20, "#F59E0B", "r", .6+i*.15) for i in range(4))
svg("tizesek", body, ".r{animation:rud 4s ease-out infinite}@keyframes rud{0%{opacity:0;transform:translateY(-14px)}12%,88%{opacity:1;transform:none}100%{opacity:0}}")

# 6. MATRICÁK
def csillag(cx, cy, r, col):
    import math
    pts = []
    for k in range(10):
        a = -math.pi/2 + k*math.pi/5; rr = r if k%2==0 else r*.45
        pts.append(f"{cx+rr*math.cos(a):.1f},{cy+rr*math.sin(a):.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="{col}" stroke="#fff" stroke-width="1.5" stroke-linejoin="round"/>'
cols = ["#F59E0B","#D9467F","#2F8FD8","#22A06B","#8A5CD6","#0EA5B7"]
lap = '<rect x="18" y="18" width="104" height="120" rx="10" fill="#fff" stroke="#D6E2DC" stroke-width="3"/>'
k = 0
for r in range(6):
    for c in range(4):
        lap += csillag(36+c*23, 36+r*19, 8, cols[k%6]); k += 1
uj = "".join(f'<g class="s" style="animation-delay:{i*.25}s">' + csillag(150+(i%2)*24, 34+i*22, 11, cols[(i+2)%6]) + "</g>" for i in range(5))
svg("matrica", lap + uj, ".s{animation:s 2.2s ease-in-out infinite;transform-box:fill-box;transform-origin:center}"
    "@keyframes s{50%{transform:scale(1.18) rotate(12deg)}}")

# 7. ŐSZ – fa, hulló levelek
def level(x, y, col, cls="", d=0):
    c = f' class="{cls}" style="animation-delay:{d}s"' if cls else ""
    return f'<g{c}><path d="M{x} {y} q8 -10 16 0 q-8 10 -16 0Z" fill="{col}"/></g>'
fa = arnyek(100,138,60)
fa += '<path d="M92 138 L96 86 L104 86 L108 138Z" fill="#8B5E3C"/><path d="M100 104 L84 90 M100 98 L116 84" stroke="#8B5E3C" stroke-width="5" stroke-linecap="round"/>'
fa += '<circle cx="74" cy="64" r="26" fill="#E07B39"/><circle cx="126" cy="64" r="26" fill="#E5484D"/><circle cx="100" cy="42" r="30" fill="#F59E0B"/><circle cx="100" cy="70" r="26" fill="#F2A33A"/><circle cx="86" cy="40" r="8" fill="#FCD34D" opacity=".7"/><circle cx="118" cy="56" r="6" fill="#FCD34D" opacity=".6"/>'
fa += "".join(level(x, y, c, "lv", d) for x,y,c,d in [(60,90,"#E07B39",0),(128,88,"#E5484D",1.1),(92,96,"#F59E0B",2.2),(140,80,"#E07B39",.6)])
fa += level(46,134,"#E5484D") + level(140,132,"#F59E0B") + level(122,136,"#E07B39") + level(64,136,"#F59E0B")
svg("osz", fa, ".lv{animation:lv 3.4s ease-in infinite}"
    "@keyframes lv{0%{transform:translate(0,0) rotate(0);opacity:0}10%{opacity:1}100%{transform:translate(-14px,46px) rotate(140deg);opacity:0}}")

# 8. ÉVSZAKOK KÖRE
kor = '<g transform="translate(100 76)">'
kor += '<path d="M0 0 L0 -58 A58 58 0 0 1 58 0Z" fill="#BDEFC9"/><path d="M0 0 L58 0 A58 58 0 0 1 0 58Z" fill="#FDE68A"/>'
kor += '<path d="M0 0 L0 58 A58 58 0 0 1 -58 0Z" fill="#FBC99A"/><path d="M0 0 L-58 0 A58 58 0 0 1 0 -58Z" fill="#CFE8FA"/>'
kor += '<circle r="58" fill="none" stroke="#fff" stroke-width="4"/><path d="M0 -58 V58 M-58 0 H58" stroke="#fff" stroke-width="4"/>'
# tavasz virág
kor += '<g transform="translate(24 -26)">' + "".join(f'<circle cx="{dx}" cy="{dy}" r="5.5" fill="#F7A6C4"/>' for dx,dy in [(0,-7),(7,0),(0,7),(-7,0)]) + '<circle r="4" fill="#F59E0B"/></g>'
# nyár nap
kor += '<g transform="translate(26 26)"><circle r="9" fill="#F59E0B"/>' + "".join(f'<path d="M0 -13 v-5" stroke="#F59E0B" stroke-width="3" stroke-linecap="round" transform="rotate({a})"/>' for a in range(0,360,45)) + '</g>'
# ősz levél
kor += '<g transform="translate(-26 26) rotate(-30)"><path d="M-10 0 q10 -14 20 0 q-10 14 -20 0Z" fill="#E07B39"/><path d="M-12 0 h22" stroke="#B4541F" stroke-width="1.5"/></g>'
# tél hópehely
kor += '<g transform="translate(-26 -26)" stroke="#2F8FD8" stroke-width="3" stroke-linecap="round">' + "".join(f'<path d="M0 -11 V11" transform="rotate({a})"/>' for a in (0,60,120)) + '</g>'
kor += '<g class="m"><path d="M0 -6 L0 -46" stroke="#163A2E" stroke-width="5" stroke-linecap="round"/><path d="M-7 -38 L0 -50 L7 -38Z" fill="#163A2E"/></g><circle r="7" fill="#163A2E"/>'
kor += '</g>'
svg("evszakok", kor, ".m{animation:m 8s linear infinite}@keyframes m{to{transform:rotate(360deg)}}")

# 9. NAPTÁR – tél
nap = arnyek(100,140,50)
nap += '<rect x="52" y="26" width="96" height="106" rx="10" fill="#fff" stroke="#D6E2DC" stroke-width="3"/>'
nap += '<path d="M52 36 a10 10 0 0 1 10 -10 h76 a10 10 0 0 1 10 10 v14 h-96z" fill="#2F8FD8"/>'
nap += '<rect x="70" y="18" width="7" height="18" rx="3.5" fill="#5F6E78"/><rect x="123" y="18" width="7" height="18" rx="3.5" fill="#5F6E78"/>'
nap += '<g transform="translate(100 92)" stroke="#9AD0F2" stroke-width="5" stroke-linecap="round">' + "".join(f'<path d="M0 -26 V26 M0 -26 l-7 -7 M0 -26 l7 -7 M0 26 l-7 7 M0 26 l7 7" transform="rotate({a})"/>' for a in (0,60,120)) + '</g>'
nap += "".join(f'<circle class="h" style="animation-delay:{d}s" cx="{x}" cy="40" r="3" fill="#CFE8FA"/>' for x,d in [(36,0),(164,.9),(26,1.8),(176,2.6)])
svg("naptar", nap, ".h{animation:h 3.2s linear infinite}@keyframes h{0%{transform:translateY(0);opacity:0}15%{opacity:1}100%{transform:translateY(96px);opacity:0}}")

# 10. TÁNYÉROK ALMÁKKAL (3 × 4)
tany = ""
for i,cx in enumerate((34,100,166)):
    tany += f'<ellipse cx="{cx}" cy="108" rx="29" ry="11" fill="#E9DCC3"/><ellipse cx="{cx}" cy="104" rx="29" ry="11" fill="#FFF4E0" stroke="#F1DDBA" stroke-width="3"/>'
    for dx,dy in ((-10,-30),(10,-30),(-11,-9),(11,-9)):
        tany += alma_rajz(cx+dx, 104+dy, .32)
svg("tanyerok", tany)

# 11. 3×4 = 4×3 forgó pontrács
racs = '<g class="g">'
for r in range(3):
    for c in range(4):
        racs += f'<circle cx="{100-39+c*26}" cy="{76-26+r*26}" r="10" fill="{["#2F8FD8","#8A5CD6","#22A06B"][r]}"/>'
racs += "</g>"
svg("forgas", racs, ".g{animation:g 4s ease-in-out infinite;transform-origin:100px 76px}"
    "@keyframes g{0%,30%{transform:rotate(0)}50%,80%{transform:rotate(90deg)}100%{transform:rotate(0)}}")

# 12. CERUZÁK 4 DOBOZBAN
pc = ["#E5484D","#F59E0B","#FCD34D","#22A06B","#2F8FD8","#8A5CD6","#D9467F","#0EA5B7"]
cer = arnyek(100,136,90)
for b in range(4):
    x0 = 10 + b*47
    for k in range(8):
        px = x0 + 4 + k*4.6
        cer += f'<rect x="{px}" y="{58 - (k%2)*6}" width="4" height="40" fill="{pc[k]}"/><path d="M{px} {58-(k%2)*6} l2 -7 l2 7z" fill="#F2D3B0"/>'
    cer += f'<rect x="{x0}" y="84" width="42" height="46" rx="5" fill="#8A5CD6"/><rect x="{x0}" y="84" width="42" height="9" rx="3" fill="#6D3FC0"/>'
svg("ceruzak", cer)

# 13. ISKOLA
isk = arnyek(100,138,80)
isk += '<rect x="34" y="66" width="132" height="70" rx="4" fill="#FDE3C8"/><path d="M26 70 L100 30 L174 70Z" fill="#E5484D"/>'
isk += '<rect x="88" y="10" width="24" height="24" rx="3" fill="#FDE3C8"/><path d="M84 14 L100 0 L116 14Z" fill="#E5484D"/>'
isk += '<g class="cs"><path d="M94 30 q0 -12 6 -12 q6 0 6 12z" fill="#F59E0B"/><circle cx="100" cy="31" r="2.5" fill="#B45309"/></g>'
for x in (46,70,120,144):
    isk += f'<rect x="{x}" y="80" width="16" height="16" rx="2" fill="#9AD0F2" stroke="#fff" stroke-width="2"/><rect x="{x}" y="106" width="16" height="16" rx="2" fill="#9AD0F2" stroke="#fff" stroke-width="2"/>'
isk += '<path d="M90 136 v-26 a10 10 0 0 1 20 0 v26z" fill="#22A06B"/><circle cx="100" cy="54" r="8" fill="#fff" stroke="#163A2E" stroke-width="2"/><path d="M100 54 v-5 M100 54 h4" stroke="#163A2E" stroke-width="2"/>'
svg("iskola", isk, ".cs{animation:cs 1.6s ease-in-out infinite;transform-origin:100px 18px}@keyframes cs{25%{transform:rotate(14deg)}75%{transform:rotate(-14deg)}}")

# 15. GYORS NYÚL
ny = arnyek(104,136,50,"a")
ny += '<g class="v" stroke="#BFD8CC" stroke-width="4" stroke-linecap="round"><path d="M14 74 h26 M6 92 h34 M18 110 h22"/></g>'
ny += ('<g class="n">'
       '<path d="M60 112 q-20 6 -16 18 q18 2 30 -8z" fill="#D8CFC4"/>'
       '<ellipse cx="96" cy="98" rx="40" ry="26" fill="#ECE6DF"/>'
       '<circle cx="58" cy="90" r="10" fill="#fff"/>'
       '<path d="M124 112 q14 10 26 16 q-14 6 -30 -4z" fill="#D8CFC4"/>'
       '<path d="M126 60 q-14 -40 -4 -48 q14 6 16 46z" fill="#ECE6DF"/><path d="M128 56 q-9 -30 -3 -38 q8 6 9 36z" fill="#F7C6CF"/>'
       '<path d="M138 58 q0 -44 12 -48 q8 10 -2 50z" fill="#ECE6DF"/><path d="M141 54 q1 -32 8 -38 q3 8 -2 38z" fill="#F7C6CF"/>'
       '<ellipse cx="138" cy="80" rx="24" ry="21" fill="#ECE6DF"/>'
       '<circle cx="146" cy="74" r="4.5" fill="#163A2E"/><circle cx="147.5" cy="72.5" r="1.5" fill="#fff"/>'
       '<ellipse cx="160" cy="84" rx="3.5" ry="3" fill="#F49BAA"/><path d="M155 90 q3 3 7 0" stroke="#163A2E" stroke-width="2" fill="none" stroke-linecap="round"/>'
       '<circle cx="140" cy="88" r="5" fill="#F7A6A6" opacity=".5"/>'
       '</g>')
svg("nyul", ny, ".n{animation:n .45s ease-in-out infinite alternate}.v{animation:v .45s linear infinite}.a{animation:a .45s ease-in-out infinite alternate;transform-origin:104px 136px}"
    "@keyframes n{to{transform:translateY(-7px) rotate(-2deg)}}@keyframes v{0%{transform:translateX(0);opacity:1}100%{transform:translateX(-10px);opacity:.3}}@keyframes a{to{transform:scale(.86)}}")

# 16. PIZZA 8 szelet, 3 hiányzik
import math
piz = arnyek(100,138,60)
piz += '<circle cx="100" cy="76" r="60" fill="#F7EDE0" stroke="#E9DCC3" stroke-width="3"/>'  # tányér
for k in range(8):
    if k in (0,1,2): continue
    a0 = -math.pi/2 + k*math.pi/4; a1 = a0 + math.pi/4
    x0,y0 = 100+50*math.cos(a0), 76+50*math.sin(a0); x1,y1 = 100+50*math.cos(a1), 76+50*math.sin(a1)
    piz += f'<path d="M100 76 L{x0:.1f} {y0:.1f} A50 50 0 0 1 {x1:.1f} {y1:.1f}Z" fill="#F59E0B" stroke="#E9A74A" stroke-width="2"/>'
    xi,yi = 100+42*math.cos(a0), 76+42*math.sin(a0); xj,yj = 100+42*math.cos(a1), 76+42*math.sin(a1)
    piz += f'<path d="M100 76 L{xi:.1f} {yi:.1f} A42 42 0 0 1 {xj:.1f} {yj:.1f}Z" fill="#FCD34D"/>'
    am = (a0+a1)/2
    piz += f'<circle cx="{100+28*math.cos(am):.1f}" cy="{76+28*math.sin(am):.1f}" r="5" fill="#E5484D"/>'
    piz += f'<path d="M100 76 L{x0:.1f} {y0:.1f}" stroke="#FFF7E6" stroke-width="2"/>'
piz += '<circle cx="118" cy="38" r="1.8" fill="#E9A74A"/><circle cx="132" cy="56" r="1.5" fill="#E9A74A"/><circle cx="124" cy="68" r="1.6" fill="#E9A74A"/>'
svg("pizza", piz)

# 17. 1/5 + 2/5 = 3/5 csíkok
def csik(x, y, db, cls="", d=0, w=20):
    s = ""
    for k in range(5):
        fill = "#8A5CD6" if k < db else "#fff"
        c = f' class="{cls}" style="animation-delay:{d+k*.12}s"' if (cls and k < db) else ""
        s += f'<rect{c} x="{x+k*w}" y="{y}" width="{w-2}" height="22" rx="4" fill="{fill}" stroke="#C9B7EE" stroke-width="2"/>'
    return s
tt = csik(50,22,1,"p",0) + '<path d="M96 56 v10 M91 61 h10" stroke="#163A2E" stroke-width="3" stroke-linecap="round"/>'
tt += csik(50,72,2,"p",.6) + '<path d="M86 106 h20 M86 113 h20" stroke="#163A2E" stroke-width="3" stroke-linecap="round"/>'
tt += csik(50,122,3,"p",1.4)
svg("tortek", tt, ".p{animation:p 4s ease-out infinite}@keyframes p{0%{fill:#fff}12%,90%{fill:#8A5CD6}100%{fill:#fff}}", vb="0 0 200 150")

# 18. 1/2 = 2/4 = 3/6
fel = ""
for row,(n,y) in enumerate(((2,24),(4,64),(6,104))):
    w = 132/n
    for k in range(n):
        fill = ["#22A06B","#0EA5B7","#F59E0B"][row] if k < n/2 else "#fff"
        fel += f'<rect x="{34+k*w:.1f}" y="{y}" width="{w-3:.1f}" height="26" rx="5" fill="{fill}" stroke="#CFDDD6" stroke-width="2"/>'
fel += '<path class="v" d="M98.5 14 V140" stroke="#163A2E" stroke-width="2.5" stroke-dasharray="5 6"/>'
svg("fele", fel, ".v{animation:v 1.4s linear infinite}@keyframes v{to{stroke-dashoffset:-22}}")

# 19. JÉGKOCKA
def kocka(s=1.0):
    return (f'<g transform="translate(100 78) scale({s})">'
            '<path d="M-36 -18 L0 -36 L36 -18 L0 0Z" fill="#E4F4FD"/>'
            '<path d="M-36 -18 L0 0 L0 42 L-36 24Z" fill="#B7E0F7"/>'
            '<path d="M36 -18 L0 0 L0 42 L36 24Z" fill="#8CCBEF"/>'
            '<path d="M-26 -16 L-4 -27" stroke="#fff" stroke-width="4" stroke-linecap="round"/>'
            '<path d="M-28 -6 L-28 12" stroke="#fff" stroke-width="3" stroke-linecap="round" opacity=".8"/></g>')
jeg = arnyek(100,132,44) + kocka(1.3)
jeg += '<g class="cs" fill="#fff" stroke="#8CCBEF" stroke-width="1.5"><path d="M150 40 l3 8 l8 3 l-8 3 l-3 8 l-3 -8 l-8 -3 l8 -3z"/></g>'
jeg += '<g class="cs" style="animation-delay:.9s" fill="#fff" stroke="#8CCBEF" stroke-width="1.5"><path d="M50 30 l2 6 l6 2 l-6 2 l-2 6 l-2 -6 l-6 -2 l6 -2z"/></g>'
svg("jeg", jeg, ".cs{animation:cs 1.8s ease-in-out infinite;transform-box:fill-box;transform-origin:center}@keyframes cs{50%{transform:scale(.4);opacity:.3}}")

# 20. OLVADÁS
olv = '<ellipse class="t" cx="100" cy="132" rx="30" ry="8" fill="#9AD0F2"/>'
olv += '<g class="k">' + kocka(1.0).replace('translate(100 78)', 'translate(100 92)') + '</g>'
olv += '<path class="c" d="M128 104 q-4 8 0 12 q4 -4 0 -12z" fill="#6FB7E8"/><path class="c" style="animation-delay:.9s" d="M74 100 q-4 8 0 12 q4 -4 0 -12z" fill="#6FB7E8"/>'
svg("olvadas", olv,
    ".k{animation:k 5s ease-in infinite;transform-origin:100px 132px}.t{animation:t 5s ease-in infinite;transform-origin:100px 132px}.c{animation:c 1.8s ease-in infinite}"
    "@keyframes k{0%{transform:scale(1)}80%{transform:scale(.35,.25);opacity:.6}100%{transform:scale(.35,.25);opacity:0}}"
    "@keyframes t{0%{transform:scale(.6)}80%,100%{transform:scale(1.9,1.4)}}"
    "@keyframes c{0%{transform:translateY(0);opacity:0}20%{opacity:1}100%{transform:translateY(18px);opacity:0}}")

# 22-24 FÜGGVÉNYGÉP
def fogas(cx, cy, r, col, cls):
    s = f'<g class="{cls}" style="transform-origin:{cx}px {cy}px">'
    for a in range(0,360,45):
        s += f'<rect x="{cx-4}" y="{cy-r-6}" width="8" height="9" rx="2" fill="{col}" transform="rotate({a} {cx} {cy})"/>'
    return s + f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}"/><circle cx="{cx}" cy="{cy}" r="{r*.38:.1f}" fill="#fff"/></g>'
def gep(be, ki, vissza=False):
    s = arnyek(96,140,70)
    s += '<path d="M60 22 h40 l-10 22 h-20z" fill="#0EA5B7"/>'  # tölcsér
    s += '<rect x="40" y="44" width="112" height="78" rx="14" fill="#2F8FD8"/><rect x="48" y="52" width="96" height="62" rx="9" fill="#5BA7E6"/>'
    s += fogas(78, 84, 15, "#FCD34D", "g1") + fogas(112, 78, 11, "#F59E0B", "g2")
    s += '<circle cx="132" cy="104" r="4" fill="#E5484D"/><circle cx="120" cy="104" r="4" fill="#22A06B"/>'
    s += '<path d="M152 96 h22 l8 10 h-30z" fill="#0EA5B7"/>'  # kimenet csúszda
    s += f'<g class="be"><circle cx="80" cy="12" r="12" fill="#fff" stroke="#163A2E" stroke-width="2.5"/><text x="80" y="17" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-weight="700" font-size="{13 if len(be)<2 else 11}" fill="#163A2E">{be}</text></g>'
    s += f'<g class="ki"><circle cx="182" cy="124" r="12" fill="#FDE68A" stroke="#163A2E" stroke-width="2.5"/><text x="182" y="129" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-weight="700" font-size="{13 if len(ki)<2 else 11}" fill="#163A2E">{ki}</text></g>'
    if vissza:
        s += '<path class="ny" d="M178 108 Q186 40 104 8" fill="none" stroke="#D9467F" stroke-width="3.5" stroke-dasharray="6 6" stroke-linecap="round"/><path d="M110 2 L100 8 L110 15" fill="none" stroke="#D9467F" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>'
    return s
gcss_fw = (".g1{animation:f 3s linear infinite}.g2{animation:fr 2s linear infinite}"
           ".be{animation:be 3s ease-in infinite}.ki{animation:ki 3s ease-out infinite}"
           "@keyframes f{to{transform:rotate(360deg)}}@keyframes fr{to{transform:rotate(-360deg)}}"
           "@keyframes be{0%{transform:translateY(-6px);opacity:0}10%{opacity:1}35%{transform:translateY(34px);opacity:1}40%,100%{transform:translateY(34px);opacity:0}}"
           "@keyframes ki{0%,45%{transform:translate(-26px,-14px);opacity:0}60%{opacity:1}75%,92%{transform:none;opacity:1}100%{opacity:0}}")
svg("gep", gep("1","3"), gcss_fw)
svg("gep_be", gep("10","?"), gcss_fw)
svg("gep_vissza", gep("?","15", True),
    ".g1{animation:fr 3s linear infinite}.g2{animation:f 2s linear infinite}.ny{animation:ny 1.2s linear infinite}"
    "@keyframes f{to{transform:rotate(360deg)}}@keyframes fr{to{transform:rotate(-360deg)}}@keyframes ny{to{stroke-dashoffset:24}}")

# 25. MEDVE (oso)
med = arnyek(100,140,44)
med += '<circle cx="62" cy="40" r="18" fill="#8B5E3C"/><circle cx="62" cy="40" r="9" fill="#C99A6E"/><circle cx="138" cy="40" r="18" fill="#8B5E3C"/><circle cx="138" cy="40" r="9" fill="#C99A6E"/>'
med += '<ellipse cx="100" cy="80" rx="52" ry="48" fill="#A0704A"/><ellipse cx="100" cy="98" rx="26" ry="20" fill="#E6C49E"/>'
med += '<g class="sz"><ellipse cx="80" cy="72" rx="6" ry="7" fill="#163A2E"/><ellipse cx="120" cy="72" rx="6" ry="7" fill="#163A2E"/></g><circle cx="82" cy="70" r="2" fill="#fff"/><circle cx="122" cy="70" r="2" fill="#fff"/>'
med += '<ellipse cx="100" cy="90" rx="10" ry="7" fill="#3B2414"/><path d="M100 97 v6 M92 106 q8 6 16 0" stroke="#3B2414" stroke-width="3" fill="none" stroke-linecap="round"/>'
med += '<circle cx="66" cy="94" r="7" fill="#F7A6A6" opacity=".55"/><circle cx="134" cy="94" r="7" fill="#F7A6A6" opacity=".55"/>'
svg("medve", med, ".sz{animation:sz 4s infinite;transform-origin:100px 72px}@keyframes sz{0%,92%,100%{transform:scaleY(1)}95%{transform:scaleY(.1)}}")

# 26. ASZTAL (mesa)
asz = arnyek(100,140,70)
asz += '<rect x="34" y="66" width="132" height="12" rx="4" fill="#B97A45"/><rect x="28" y="60" width="144" height="10" rx="4" fill="#D4945A"/>'
asz += '<rect x="42" y="78" width="10" height="60" rx="3" fill="#A86B3A"/><rect x="148" y="78" width="10" height="60" rx="3" fill="#A86B3A"/>'
asz += '<rect x="58" y="78" width="8" height="48" rx="3" fill="#8F5A30"/><rect x="134" y="78" width="8" height="48" rx="3" fill="#8F5A30"/>'
asz += '<path d="M86 60 q-4 -18 6 -26 h16 q10 8 6 26z" fill="#0EA5B7"/><path d="M96 34 q-2 -10 -10 -14 M104 34 q2 -12 10 -16 M100 34 v-18" stroke="#22A06B" stroke-width="3" fill="none" stroke-linecap="round"/>'
asz += '<circle cx="86" cy="20" r="6" fill="#F7A6C4"/><circle cx="114" cy="18" r="6" fill="#FCD34D"/><circle cx="100" cy="13" r="6" fill="#E5484D"/>'
svg("asztal", asz)

# 27. LABDA (pelota) – pattogó strandlabda
lab = '<ellipse class="a" cx="100" cy="140" rx="34" ry="6" fill="#E3EEE8"/>'
lab += ('<g class="l"><circle cx="100" cy="100" r="40" fill="#fff"/>'
        '<path d="M100 60 A40 40 0 0 1 140 100 L100 100Z" fill="#E5484D"/><path d="M100 140 A40 40 0 0 1 60 100 L100 100Z" fill="#2F8FD8"/>'
        '<path d="M60 100 A40 40 0 0 1 100 60 L100 100Z" fill="#FCD34D"/><path d="M140 100 A40 40 0 0 1 100 140 L100 100Z" fill="#22A06B"/>'
        '<circle cx="100" cy="100" r="40" fill="none" stroke="#fff" stroke-width="3"/><circle cx="100" cy="100" r="6" fill="#fff"/>'
        '<ellipse cx="86" cy="82" rx="7" ry="4" fill="#fff" opacity=".6" transform="rotate(-35 86 82)"/></g>')
svg("labda", lab, ".l{animation:l 1.2s cubic-bezier(.5,0,.5,1) infinite}.a{animation:a 1.2s cubic-bezier(.5,0,.5,1) infinite;transform-origin:100px 140px}"
    "@keyframes l{0%,100%{transform:translateY(0) scale(1.06,.94)}50%{transform:translateY(-46px)}}@keyframes a{50%{transform:scale(.55);opacity:.5}}")
print(sorted(os.listdir(OUT)))
