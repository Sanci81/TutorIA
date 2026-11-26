/* LUMI – az oldal arca (fix228, Sándor 11.20)
   Lumi a fejléc logójában lakik (a lámpa az ő feje). A nem-tanulós oldalakon (GYIK, regisztráció,
   csomagok, jogi oldalak…) lenéz, ledob egy kötelet, lemászik rajta, és ugrál az oldalon:
   mező kitöltése → örül, hibás/üres mező → gondolkodik, beküldés → nagy ugrás.
   Amíg kint van, a logó helye üres. Ha sokáig nem csinálsz semmit, visszamászik; ha közben
   megint csinálsz valamit, félúton meggondolja magát, és visszajön.
   Ha az egér (vagy az ujj) hozzáér, „megcsiklandozod”: odébb ugrik – sosem marad útban.
   Tanulós oldalon (lecke, mintalecke, gyerekoldalak) a logóban marad.
   Vektoros rajz, kóddal mozgatva: nincs képfájl, nincs költség. „Kevesebb mozgás” beállításnál
   csak a logó cserélődik, nem mászik ki. Visszaállítás: base.html-ből a lumi.js sor törlése
   (a régi logó rajza: static/img/logo_lampa_eredeti.svg). */
(function () {
    'use strict';
    if (window.__lumi) { return; }
    var D = document, NS = 'http://www.w3.org/2000/svg';
    /* fix286: HIBAKERESŐ NAPLÓ – csak ha a címben ott van: ?lumi=nez. Máskor nem csinál semmit.
       A napló: window.__lumiNaplo (Claude a böngészőből olvassa ki). */
    var NAPLO = /[?&]lumi=nez/.test(location.search);
    function nl() { if (NAPLO) { (window.__lumiNaplo = window.__lumiNaplo || []).push([Math.round(performance.now())].concat([].slice.call(arguments))); } }
    nl('betoltve', D.readyState);
    var kevesMozgas = false;
    try { kevesMozgas = window.matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) {}

    // ── KÖZÖS RAJZELEMEK (a referenciakép szerint: sötét izzó, vastag menta keret, sárga „T”) ──
    var DEFS =
        '<radialGradient id="lmBel" cx="50%" cy="48%" r="60%"><stop offset="0" stop-color="#3F7656"/><stop offset=".6" stop-color="#25503A"/><stop offset="1" stop-color="#173826"/></radialGradient>' +
        '<radialGradient id="lmIzz" cx="50%" cy="45%" r="60%"><stop offset="0" stop-color="#FFF6B0" stop-opacity=".95"/><stop offset=".6" stop-color="#FFE27A" stop-opacity=".55"/><stop offset="1" stop-color="#FFE27A" stop-opacity="0"/></radialGradient>' +
        '<radialGradient id="lmGlo" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#FFF0A0" stop-opacity=".9"/><stop offset=".5" stop-color="#FFE68A" stop-opacity=".35"/><stop offset="1" stop-color="#FFE68A" stop-opacity="0"/></radialGradient>';
    var IZZO_UT = 'M60 17c-15 0-26.5 11.3-26.5 25.4 0 8.8 4.2 15 8.4 19.9 2.9 3.4 4.6 6.4 5.1 10.3h26c.5-3.9 2.2-6.9 5.1-10.3 4.2-4.9 8.4-11.1 8.4-19.9C86.5 28.3 75 17 60 17Z';
    function fejRajz(id, talp) {    // a 120×120-as logó-koordinátákban; talp: a csíkos nyak is (a logóban)
        return '<path d="' + IZZO_UT + '" fill="url(#lmBel)" stroke="#3DDC97" stroke-width="5.6" stroke-linejoin="round"/>' +
            '<path id="' + id + 'Izz" d="' + IZZO_UT + '" fill="url(#lmIzz)" opacity="0"/>' +
            '<path d="M41 26 q-5 5 -5.5 12" fill="none" stroke="#A8F5D2" stroke-width="2.2" stroke-linecap="round" opacity=".7"/>' +
            '<g id="' + id + 'Sz"><path d="M45 37h30M60 37v25" stroke="#F5D565" stroke-width="4" stroke-linecap="round"/>' +
            '<g fill="#F5D565"><circle cx="45" cy="37" r="5.6"/><circle cx="60" cy="37" r="5.6"/><circle cx="75" cy="37" r="5.6"/><circle cx="60" cy="62" r="5.6"/></g></g>' +
            (talp === false ? '' : '<path d="M48 79h24M50 86h20M54 93h12" fill="none" stroke="#F6DE7E" stroke-width="5" stroke-linecap="round"/>');
    }

    // ── A LOGÓ: Lumi feje a sötét négyzetben (a régi lámpa helyett) ──────────
    var logo = D.querySelector('.brand-mark');
    var logoFej = null;
    if (logo) {
        var regi = logo.querySelector('svg');
        if (regi) { regi.style.display = 'none'; }
        logoFej = D.createElementNS(NS, 'svg');
        logoFej.setAttribute('viewBox', '0 0 120 120');
        logoFej.setAttribute('width', '100%'); logoFej.setAttribute('height', '100%');
        logoFej.innerHTML = '<defs>' + DEFS.replace(/id="lm/g, 'id="lgl') + '</defs><rect width="120" height="120" rx="30" fill="#0e2a1e"/>' +
            '<g id="lgFej" style="transition:transform .35s ease, opacity .25s">' + fejRajz('lgf').replace(/url\(#lm/g, 'url(#lgl') + '</g>';
        logo.appendChild(logoFej);
    }
    var logoG = logoFej && logoFej.querySelector('#lgFej');
    function logoAllapot(van, nez) {
        if (!logoG) { return; }
        logoG.style.opacity = van ? '1' : '0';
        logoG.style.transformOrigin = '60px 90px';
        logoG.style.transform = nez ? 'rotate(14deg) translateY(4px)' : '';
    }

    var tanulos = D.body.classList.contains('gyerek-hatter') || /\/(chat|minta|clase-de-prueba|admin|children\/\d+\/)/.test(location.pathname) ||
        D.querySelector('.chat-wrap, #mlChat, .gymenu');
    window.__lumi = {};
    if (tanulos || kevesMozgas || !logo) { return; }

    // ── A KINTI LUMI – fix231: a JÓVÁHAGYOTT KÉPEKBŐL (static/figurak/lumi/*.webp) ─────────
    // Sándor: „a rajzolt Lumi fabábu – az eredeti képből legyen”. A testtartás a kép, a mozgást
    // (ugrás, lapulás, billegés, mászás a kötélen) a program adja. A képek egyformán nagyok
    // (a lámpa szélessége szerint igazítva), a lámpa közepe mindig ugyanott marad, így a
    // testtartás-váltás nem „ugrik”.
    var KICSI = function () { return innerWidth < 700; };
    var MAGAS = function () { return KICSI() ? 86 : 116; };   // fix238: kicsit kisebb – így a mezők között is elfér          // a figura magassága px-ben
    var KEPUT = (D.currentScript && D.currentScript.src) ? D.currentScript.src.replace(/js\/lumi\.js.*$/, 'figurak/lumi/') : '/static/figurak/lumi/';
    // név: [szélesség, magasság, lámpa-szélesség, lámpa közepe (x arány), talp (y arány)]
    var META = {"alap": [334, 640, 286, 0.503, 0.991], "orul": [372, 640, 258, 0.5, 0.991], "gondolkodik": [334, 640, 287, 0.501, 0.989], "integet": [347, 640, 269, 0.546, 0.991], "biztat": [326, 640, 272, 0.5, 0.991], "tapsol": [368, 640, 274, 0.5, 0.991], "aha": [335, 640, 277, 0.512, 0.991], "maszik": [306, 640, 266, 0.5, 0.992], "ul": [311, 640, 269, 0.503, 0.992], "meglepodik": [340, 640, 272, 0.491, 0.992], "lenez": [378, 640, 299, 0.538, 0.991]};
    var ULES = .80;                                                    // fix234: a kezei a mező vonalán – a vonalon ül, nem alatta                                                    // az „ül” képen az ülés magassága (y arány)
    Object.keys(META).forEach(function (n) { var i = new Image(); i.src = KEPUT + n + '.webp'; });
    /* fix237: új testtartás (fejfogás) – ha a kép már megvan, magától használja; addig a „gondolkodik” megy helyette */
    ['fejfogas'].forEach(function (n) { if (META[n]) { return; } var i = new Image();
        i.onload = function () { META[n] = [i.naturalWidth * 640 / i.naturalHeight, 640, META.alap[2], .5, .99]; }; i.src = KEPUT + n + '.webp'; });
    var doboz = D.createElement('div');
    doboz.id = 'lumi';
    doboz.setAttribute('aria-hidden', 'true');
    doboz.style.cssText = 'position:absolute;left:0;top:0;width:0;height:0;z-index:45;pointer-events:none;';
    var kotel = D.createElementNS(NS, 'svg');
    kotel.style.cssText = 'position:absolute;left:0;top:0;width:1px;height:1px;overflow:visible;pointer-events:none;z-index:44';
    kotel.innerHTML = '<path d="" fill="none" stroke="#9A6A32" stroke-width="3.4" stroke-linecap="round"/><path d="" fill="none" stroke="#E0B47A" stroke-width="1.4" stroke-dasharray="3 5" stroke-linecap="round"/>';
    var arny = D.createElement('div');
    arny.style.cssText = 'position:absolute;border-radius:50%;background:radial-gradient(closest-side,rgba(14,42,30,.22),rgba(14,42,30,0));pointer-events:none;opacity:0';
    var kep = D.createElement('img');
    kep.alt = ''; kep.draggable = false;
    kep.style.cssText = 'position:absolute;left:0;top:0;transform-origin:50% 100%;pointer-events:auto;cursor:pointer;opacity:0;user-select:none;-webkit-user-drag:none;will-change:transform';
    var buborek = D.createElement('div');
    buborek.style.cssText = 'position:absolute;width:34px;height:34px;border-radius:50%;background:#fff;border:2.5px solid #2E9E6C;color:#1E7F4F;font:900 22px/29px Nunito,Arial,sans-serif;text-align:center;pointer-events:none;opacity:0;box-shadow:0 2px 6px rgba(0,0,0,.12)';
    doboz.appendChild(arny); doboz.appendChild(kep); doboz.appendChild(buborek);
    var R = {test: kep};

    // ── ÁLLAPOT ─────────────────────────────────────────────────────────
    // x, y: a talppont a lapon (px); kep: testtartás; tukor: tükrözve (mászásnál felváltva);
    // dol, fej: billenés fokban; ny: nyúlás/lapulás (1 = normál); emel: magasság a talp fölött;
    // meret: 0..1 (a logóból kibújva nő), lat: láthatóság, feny: ragyogás 0..1, jelA: a buborék
    var P = {x: 0, y: 0, kep: 'alap', tukor: 0, dol: 0, fej: 0, ny: 1, emel: 0, meret: 1, lat: 0, feny: 0, arnyek: 1, jelA: 0};
    var NYUGI = {dol: 0, fej: 0, ny: 1};
    function meretek() {
        var m = META[P.kep] || META.alap, ref = META.alap, h = MAGAS() * P.meret * (ref[2] / m[2]) * (ref[1] / ref[1]);
        var w = h * m[0] / m[1];
        return {w: w, h: h, cx: m[3], talp: m[4]};
    }
    var utolsoKep = '';
    function rajzol() {
        if (utolsoKep !== P.kep) { kep.src = KEPUT + P.kep + '.webp'; utolsoKep = P.kep; }
        var M = meretek(), ay = P.kep === 'ul' ? ULES : M.talp;
        var bal = P.x - M.w * (P.tukor ? 1 - M.cx : M.cx), fel = P.y - M.h * ay - P.emel;
        kep.style.width = M.w + 'px'; kep.style.height = M.h + 'px';
        kep.style.transformOrigin = (P.tukor ? (1 - M.cx) : M.cx) * 100 + '% ' + ay * 100 + '%';
        kep.style.transform = 'translate(' + bal + 'px,' + fel + 'px) rotate(' + (P.dol + P.fej) + 'deg) scale(' + ((P.tukor ? -1 : 1) * (2 - P.ny)) + ',' + P.ny + ')';
        kep.style.opacity = P.lat;
        var f = Math.max(0, Math.min(1, P.feny));
        kep.style.filter = f > .02 ? 'drop-shadow(0 0 ' + (4 + f * 14) + 'px rgba(255,226,110,' + (.35 + f * .55) + ')) brightness(' + (1 + f * .12) + ')' : '';
        var e = Math.max(0, Math.min(1, 1 - P.emel / 140)) * P.arnyek * (P.kep === 'ul' ? 0 : 1), aw = M.w * .62 * (.5 + .5 * e);
        arny.style.width = aw + 'px'; arny.style.height = aw * .22 + 'px';
        arny.style.left = (P.x - aw / 2) + 'px'; arny.style.top = (P.y - aw * .11) + 'px'; arny.style.opacity = P.lat * e;
        buborek.style.left = (P.x + M.w * .32) + 'px'; buborek.style.top = (P.y - M.h * 1.02 - P.emel) + 'px';
        buborek.style.opacity = P.jelA * P.lat;
    }

    // ── IDŐZÍTÉS ────────────────────────────────────────────────────────
    var EASE = {lin: function (t) { return t; }, be: function (t) { return t * t; }, ki: function (t) { return 1 - (1 - t) * (1 - t); },
        bk: function (t) { return t < .5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2; },
        rugo: function (t) { return 1 - Math.cos(t * Math.PI * 2.5) * Math.exp(-t * 5); }};
    var megszakit = 0;
    function anim(cel, ido, ease, path) {
        return new Promise(function (ok) {
            var t0 = performance.now(), kezd = {}, k, f = EASE[ease || 'bk'];
            for (k in cel) { kezd[k] = P[k]; }
            (function lep(t) {
                var u = Math.min(1, (t - t0) / ido), e = f(u);
                for (var k2 in cel) { P[k2] = kezd[k2] + (cel[k2] - kezd[k2]) * e; }
                if (path) { path(u, e); }
                rajzol();
                if (u < 1) { requestAnimationFrame(lep); } else { ok(); }
            })(t0);
        });
    }
    function var_(ms) { return new Promise(function (ok) { setTimeout(ok, ms); }); }
    var sor = Promise.resolve(), fut = 0;
    function tedd(fv) { fut++; sor = sor.then(fv).catch(function (e) { nl('HIBA', String(e && e.message || e)); if (window.console) { console.warn('lumi', e); } }).then(function () { fut--; }); return sor; }
    function legyen(k) { P.kep = k; P.tukor = 0; rajzol(); }

    // ── MOZDULATOK (a testtartás a kép, a mozgás a kódé) ──────────────────
    function alap(ido) { return anim(NYUGI, ido || 280).then(function () { legyen('alap'); }); }
    function ugras(x, y, magas, ido) {
        var x0 = P.x, y0 = P.y;
        if (P.kep === 'ul') { legyen('alap'); }
        return anim({ny: .86}, 140, 'ki')                                                  // nekiguggol
            .then(function () { legyen('meglepodik'); P.tukor = x < x0 ? 1 : 0;
                return anim({ny: 1.08}, ido, 'lin', function (u) {
                    P.x = x0 + (x - x0) * u; P.y = y0 + (y - y0) * u;
                    P.emel = 4 * magas * u * (1 - u);
                    P.dol = (x > x0 ? 1 : -1) * Math.sin(u * Math.PI) * 8;
                }); })
            .then(function () { P.emel = 0; legyen('alap'); return anim({ny: .82, dol: 0}, 100, 'ki'); })   // landol
            .then(function () { return anim(NYUGI, 380, 'rugo'); });
    }
    function jel(sz, be) { buborek.textContent = sz; return anim({jelA: be ? 1 : 0}, 220, 'ki'); }
    function orul(nagy) {
        var m = MAGAS() * (nagy ? .5 : .2);
        return anim({ny: .86}, 130, 'ki')
            .then(function () { legyen(nagy ? 'orul' : 'tapsol');
                return anim({ny: 1.06, feny: 1}, nagy ? 560 : 380, 'lin', function (u) {
                    P.emel = 4 * m * u * (1 - u); if (nagy) { P.dol = Math.sin(u * Math.PI * 2) * 7; } }); })
            .then(function () { P.emel = 0; return anim({ny: .84}, 100, 'ki'); })
            .then(function () { return anim({ny: 1, dol: 0, feny: 0}, 600, 'rugo'); })
            .then(function () { return var_(nagy ? 500 : 250); }).then(function () { legyen('alap'); });
    }
    function gondolkodik() {
        legyen('gondolkodik');
        return jel('?', true)
            .then(function () { return anim({fej: -4}, 520); }).then(function () { return anim({fej: 3}, 620); })
            .then(function () { return anim({fej: 0}, 400); }).then(function () { return jel('?', false); })
            .then(function () { legyen('biztat'); return var_(900); }).then(function () { legyen('alap'); });
    }
    function aha() {
        legyen('aha');
        return anim({feny: 1, ny: 1.06}, 240, 'ki')
            .then(function () { return jel('!', true); }).then(function () { return var_(800); })
            .then(function () { return jel('!', false); }).then(function () { return anim({feny: 0, ny: 1}, 420, 'rugo'); })
            .then(function () { legyen('alap'); });
    }
    function integet() {
        legyen('integet');
        return anim({}, 1300, 'lin', function (u) { P.dol = Math.sin(u * Math.PI * 4) * 4; })
            .then(function () { P.dol = 0; legyen('alap'); });
    }
    /* fix237 (Sándor: „ha nem jó valami, fogja a fejét – de csak ha végzett”) */
    function fejetFog() {
        var ult = P.kep === 'ul';
        if (ult) { legyen('alap'); }
        legyen(META.fejfogas ? 'fejfogas' : 'gondolkodik');
        return jel('!', true)
            .then(function () { return anim({}, 900, 'lin', function (u) { P.dol = Math.sin(u * Math.PI * 6) * 3; }); })
            .then(function () { P.dol = 0; return jel('!', false); }).then(function () { return var_(350); })
            .then(function () { legyen(ult ? 'ul' : 'alap'); });
    }
    function lenez() { legyen('lenez'); return var_(900).then(function () { legyen('alap'); }); }
    function ul() { if (P.kep !== 'alap') { return Promise.resolve(); } legyen('ul'); return anim({ny: .95}, 160, 'ki').then(function () { return anim({ny: 1}, 300, 'rugo'); }); }
    function maszik(u, gyors) {                                     // kézen-kézen: a kép felváltva tükröződik
        if (P.kep !== 'maszik') { P.kep = 'maszik'; }
        var f = Math.sin(u * Math.PI * (gyors || 7));
        P.tukor = f > 0 ? 1 : 0; P.dol = f * 2; P.emel = Math.abs(f) * 3;
    }

    // ── KÖTÉL ───────────────────────────────────────────────────────────
    function lap(el) { var r = el.getBoundingClientRect(); return {x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height}; }
    var kp = kotel.querySelectorAll('path');
    function kotelVonal(pt) { var d = pt.length > 1 ? 'M' + pt.map(function (p) { return p[0].toFixed(1) + ' ' + p[1].toFixed(1); }).join(' L') : '';
        kp.forEach(function (p) { p.setAttribute('d', d); }); }
    function kotelRajz(x, y1, y2) { kotelVonal(y2 > y1 ? [[x, y1], [x, y2]] : []); }
    /* fix242 (Sándor: „hol a kötél? a semmiben lóg”): a kötél a (ragadós) fejlécre van kötve, ezért a felső
       pontját a KÉPERNYŐHÖZ mérjük (av), nem a laphoz – ha közben görgetsz, a kötél a fejléccel megy, nem marad
       ott a semmiben. ay = scrollY + av, minden képkockán újraszámolva. */
    function kotelTest(ax, av) {                 // fix239: a kötél a fogóponttól Lumi kezén át, alatta kicsit lelóg
        var ay = scrollY + av, h = MAGAS() * P.meret, t = P.dol * Math.PI / 180, si = Math.sin(t), co = Math.cos(t), y = P.y - P.emel;
        kotelVonal([[ax, ay], [P.x + si * h * .62, y - co * h * .62], [P.x - si * 14, y + co * 14]]);
    }
    function tetoV() {                           // a kötél felső pontja a képernyőn: a fejléc alja (ha nem látszik, a képernyő teteje)
        var hd = D.querySelector('.navbar, header'), b = hd ? Math.max(0, hd.getBoundingClientRect().bottom) : 0;
        return Math.min(b, innerHeight * .3) - 4;
    }
    function tetoY() { return scrollY + tetoV(); }
    function horgonyX(x) {                       // fix242: a kötél csak ott lóghat, ahol fölötte tényleg fejléc van (széles képernyőn a sáv nem ér a széléig)
        var hd = D.querySelector('.navbar-inner') || D.querySelector('.navbar, header'); if (!hd) { return x; }
        var r = hd.getBoundingClientRect(); return Math.max(r.left + scrollX + 30, Math.min(r.right + scrollX - 30, x));
    }
    function logoV() { var r = logo.getBoundingClientRect(); return {x: r.left + scrollX + r.width / 2, y: r.top + r.height * .55, al: r.bottom - 2}; }   // a logó a képernyőn
    function kotelV(x, av, y2) { kotelRajz(x, scrollY + av, y2); }      // függőleges kötél a fejléctől y2-ig (lapkoordináta)
    function lengoSzint(y1) {                    // fix242: olyan magasan lóg, hogy a lendülés tetején se bújjon a fejléc alá
        var h = MAGAS(); return Math.max(fejlecAlja() + h * 1.3 + 14, Math.min(P.y, y1) - h * .55);
    }
    function kotelBe() { if (!kotel.parentNode) { D.body.insertBefore(kotel, doboz); } }
    function kotelKi() { kotelRajz(0, 0, 0); if (kotel.parentNode) { kotel.parentNode.removeChild(kotel); } }

    // ── KI A LOGÓBÓL / VISSZA ───────────────────────────────────────────
    var kint = false;
    function logoPont() { var l = lap(logo); return {x: l.x + l.w / 2, y: l.y + l.h * .55, al: l.y + l.h}; }
    /* fix239 (Sándor: „sose teleportáljon – sétáljon, másszon, kicsit ugorjon; messzire kötélen menjen”).
       Mozgásmódok: SÉTA ugyanazon a felületen · kis UGRÁS a szomszédos felületre · KÖTÉLÚT nagy távolságra
       (ledobja a kötelet, felmászik, átlendül, lemászik) · ha nem látszik: kötélen ERESZKEDIK le a látható részre. */
    function mozog(ido, path, stop) {            // képkockánként fut; ha stop() igaz, félbehagyja (true-val tér vissza)
        return new Promise(function (ok) {
            var t0 = performance.now();
            (function lep(t) {
                if (stop && stop()) { ok(true); return; }
                var u = Math.min(1, (t - t0) / ido); path(u); rajzol();
                if (u < 1) { requestAnimationFrame(lep); } else { ok(false); }
            })(t0);
        });
    }
    function seta(x) {                           // lépeget (billeg, kicsit emelkedik minden lépésnél)
        var x0 = P.x, d = Math.abs(x - x0); if (d < 3) { return Promise.resolve(); }
        legyen('alap'); P.tukor = x < x0 ? 1 : 0;
        var lepes = Math.max(2, Math.round(d / 20));
        return mozog(Math.min(2600, 280 + d * 6.5), function (u) {
            var p = .5 * u + .5 * EASE.bk(u), f = Math.sin(u * Math.PI * lepes);
            P.x = x0 + (x - x0) * p; P.emel = Math.abs(f) * 4; P.dol = f * 3;
        }).then(function () { P.x = x; P.emel = 0; P.dol = 0; P.tukor = 0; rajzol(); });
    }
    function kuszik(x, av, yc, stop, ax) {       // mászik a kötélen (fel vagy le), kézen-kézen; ax: a kötél felső pontja (ha nem éppen fölötte)
        var ycF = typeof yc === 'function' ? yc : function () { return yc; };   // fix243: a cél lehet a fejléchez mért magasság is (görgetéskor vele megy)
        var y0 = P.y, d = ycF() - y0; if (ax == null) { ax = x; } if (Math.abs(d) < 2) { return Promise.resolve(false); }
        P.kep = 'maszik'; P.arnyek = 0;
        var n = Math.max(2, Math.round(Math.abs(d) / 36));
        var s0 = scrollY;                        // fix242: a kötelet fogja – ha görgetsz, a kiindulópont a fejléccel (a kötéllel) megy, a cél a lappal
        return mozog(Math.min(2800, 380 + Math.abs(d) * 3.6), function (u) { P.x = x; P.y = (y0 + scrollY - s0) * (1 - u) + ycF() * u; maszik(u, n); kotelTest(ax, av); }, stop);
    }
    function lendul(ax0, ax1, av) {              // a fogópont a fejléc alján átcsúszik, Lumi ingaként lendül utána
        var Dx = ax1 - ax0, ay0 = scrollY + av, L0 = Math.max(70, Math.hypot(P.x - ax0, Math.max(0, P.y - ay0)));
        var phi = Math.max(-1, Math.min(1, Math.atan2(P.x - ax0, Math.max(40, P.y - ay0)))), hatar = Math.max(.5, Math.abs(phi));   // ha nem éppen a fogópont alatt van, onnan lendül
        if (Math.abs(Dx) < 8 && Math.abs(phi) < .02) { P.x = ax1; return Promise.resolve(); }
        var L = L0, g = 2600, om = 0, T = Math.min(1.7, .65 + Math.abs(Dx) * .0011), Ts = .8;
        P.kep = 'maszik'; P.tukor = Dx < 0 ? 1 : 0; P.emel = 0;
        return new Promise(function (ok) {
            var t0 = performance.now(), tl = t0;
            (function lep(now) {
                var t = (now - t0) / 1000, dt = Math.max(.008, Math.min(.033, (now - tl) / 1000)); tl = now;
                var u = Math.min(1, t / T), ax = ax0 + Dx * EASE.bk(u), a = t < T ? Dx * (u < .5 ? 4 : -4) / (T * T) : 0, ay = scrollY + av;
                om += (-(g / L) * Math.sin(phi) - (a / L) * Math.cos(phi) - (t < T ? 2.2 : 7) * om) * dt; phi += om * dt;
                hatar = Math.max(.5, hatar * .97);
                phi = Math.max(-hatar, Math.min(hatar, phi));                 // fix242: kisebb kilengés – nem emelkedik a fejléc alá
                if (t > T + Ts - .25) { phi *= .82; }
                P.x = ax + L * Math.sin(phi); P.y = ay + L * Math.cos(phi); P.dol = -phi * 180 / Math.PI;
                kotelTest(ax, av); rajzol();
                if (t < T + Ts) { requestAnimationFrame(lep); }
                else { P.x = ax1 + L * Math.sin(phi); P.y = scrollY + av + L * Math.cos(phi); P.dol = 0; P.tukor = 0; kotelTest(ax1, av); rajzol(); ok(); }
            })(t0);
        });
    }
    function leszall(xa, x1, y1, f, av) {        // fix242: a kötél xa-nál lóg; ha a cél (x1) máshol van: lemászik, és odasétál / odaugrik
        var h = MAGAS();
        if (Math.abs(x1 - xa) < 4) { return kuszik(xa, av, y1).then(function () { return lelep(xa, av); }); }
        var fr = f && felulet(f);
        var gx = talajKeres(xa, y1 - 1, 8, 8);
        if (gx && Math.abs(gx.y - y1) < 5 && takaras(dobozom(xa, gx.y, false), null) < 1) {
            return kuszik(xa, av, y1).then(function () { return lelep(xa, av); }).then(function () { return seta(x1); });     // ugyanarra a felületre ér le, onnan sétál
        }
        if (Math.abs(x1 - xa) < h * 2.2) {                                    // közel van: a kötélről ugrik át
            return kuszik(xa, av, y1 - h * .35).then(function () {
                P.arnyek = 1;
                return Promise.all([ugras(x1, y1, h * .4, Math.min(650, 340 + Math.abs(x1 - xa) * .5)),
                    var_(200).then(function () { return anim({}, 380, 'be', function (u) { var ay = scrollY + av; kotelRajz(xa, ay, ay + (y1 - h * .9 - ay) * (1 - u)); }); })]);
            }).then(kotelKi);
        }
        return kuszik(x1, av, y1, null, xa).then(function () { return lelep(xa, av); });      // végső eset: ferde kötélen
    }
    function lelep(ax, av) {                     // a felületre lép, a kötél felszalad
        P.arnyek = 1; P.emel = 0; P.dol = 0; legyen('alap');
        var hy = P.y - MAGAS() * .62;
        return Promise.all([
            anim({ny: .9}, 110, 'ki').then(function () { return anim(NYUGI, 380, 'rugo'); }),
            var_(140).then(function () { return anim({}, 420, 'be', function (u) { var ay = scrollY + av; kotelRajz(ax, ay, ay + (hy - ay) * (1 - u)); }); })
        ]).then(kotelKi);
    }
    function megfog(ax, av) {                    // ledobja a kötelet maga mellé, és megfogja
        if (P.kep === 'ul') { legyen('alap'); }
        kotelBe(); var y0 = P.y;
        var x0 = P.x;                          // fix242: a kötél a fejléc alól lóg (ax), ha ő máshol áll, ferdén ér hozzá
        return anim({}, 380, 'ki', function (u, e) { var ay = scrollY + av; kotelVonal([[ax, ay], [ax + (x0 - ax) * e, ay + (y0 + 12 - ay) * e]]); })
            .then(function () { return anim({ny: .9}, 110, 'ki'); })
            .then(function () { P.kep = 'maszik'; P.arnyek = 0; Object.assign(P, NYUGI); P.x = x0; kotelTest(ax, av); rajzol(); });
    }
    /* fix243: ha útközben görgetsz, és a cél kiesik a képből, nem mászik le a semmibe: új, látható helyet keres
       (ha nincs, a kötélen a logóba mászik). A lengés magassága a fejléchez mért – görgetéskor a kötéllel megy. */
    function ujHely() { var m = most(); if (m && lathato(m.y)) { return m; } var c = fodoboz(); return c ? (horgony = c, helyDoboz(c)) : null; }
    function logobaFel(xFrom, av) {
        var lv = logoV(), h = MAGAS();
        return lendul(xFrom, lv.x, av).then(function () {
            reteg(true);
            return kuszik(lv.x, av, function () { return scrollY + logoV().y + h * 1.05; });
        }).then(function () {
            var y1v = P.y - scrollY;
            return anim({meret: .4, lat: 0}, 380, 'be', function (u) { P.y = scrollY + y1v - u * 6; var ay = scrollY + av; kotelRajz(lv.x, ay, ay + (P.y - ay) * (1 - u)); });
        }).then(function () { kotelKi(); kint = false; alattam = null; reteg(false); logoAllapot(true); bentIdo = Date.now(); P.meret = 1; return 'haza'; });
    }
    function kotelut(x1, y1, o) {                // nagy távolság: felmászik, átlendül, lemászik
        o = o || {}; var av = o.av != null ? o.av : tetoV(), ax = o.ax0 != null ? o.ax0 : horgonyX(P.x), cel = {x: x1, y: y1, f: o.f, ul: o.ul};
        return (o.marKotelen ? Promise.resolve() : megfog(ax, av))
            .then(function () { var lv = lengoSzint(cel.y) - fejlecAlja(); return kuszik(P.x, av, function () { return fejlecAlja() + lv; }, null, ax); })
            .then(function () {
                if (!lathato(cel.y)) { var u = ujHely(); if (!u) { return logobaFel(ax, av); } cel = u; }
                var xa = horgonyX(cel.x);
                return lendul(ax, xa, av).then(function () {
                    if (!lathato(cel.y)) { var u2 = ujHely(); if (!u2) { return logobaFel(xa, av); } cel = u2; var xb = horgonyX(cel.x);
                        return lendul(xa, xb, av).then(function () { return leszall(xb, cel.x, cel.y, cel.f, av); }).then(function () { return cel; }); }
                    return leszall(xa, cel.x, cel.y, cel.f, av).then(function () { return cel; });
                });
            });
    }
    function leereszkedik(x1, y1, f) {           // nem látszott: felülről, kötélen ereszkedik le a látható részre
        var h = MAGAS(), av = tetoV(), xa = horgonyX(x1);
        kotelBe(); P.x = xa; P.y = scrollY + av + h * .9; P.kep = 'maszik'; Object.assign(P, NYUGI); P.arnyek = 0; P.lat = 0; P.meret = 1; P.emel = 0; P.feny = 0;
        return anim({}, 320, 'ki', function (u, e) { var ay = scrollY + av; kotelRajz(xa, ay, ay + (P.y + 14 - ay) * e); })
            .then(function () { return Promise.all([kuszik(xa, av, function () { return Math.min(y1, scrollY + av + h * 1.3); }), anim({lat: 1}, 260, 'ki')]); })
            .then(function () { return leszall(xa, x1, y1, f, av); });
    }
    var kint = false, alattam = null, kijott = false, bentIdo = 0;           // alattam: a felület (elem), amin épp áll
    function logoPont() { var l = lap(logo); return {x: l.x + l.w / 2, y: l.y + l.h * .55, al: l.y + l.h}; }
    function kijon(cel) {
        var lv = logoV(), x = lv.x, av = lv.al, h = MAGAS();
        var c = cel.hely2 || most() || {x: x + 80, y: cel.y};
        logoAllapot(true, true);                                   // lenéz
        kotelBe(); reteg(true);
        return var_(450)
            .then(function () { return anim({}, 380, 'ki', function (u, e) { kotelV(x, av, scrollY + av + h * 1.6 * e); }); })   // ledobja a kötelet
            .then(function () {
                logoAllapot(false); kint = true;
                P.x = x; P.y = scrollY + lv.y + h * .35; P.meret = .4; P.lat = 1; P.feny = 0; Object.assign(P, NYUGI); maszik(0); P.arnyek = 0;
                var y0 = lv.y;
                return anim({meret: 1}, 420, 'ki', function (u) { P.y = scrollY + y0 + h * (.35 + .9 * u); kotelTest(x, av); });       // kibújik
            })
            .then(function () { return kuszik(x, av, function () { return Math.min(c.y, fejlecAlja() + h * 1.3 + 14); }); })      // lejjebb mászik, amíg az egész teste a fejléc alá ér
            .then(function () { reteg(false); })
            .then(function () { return kotelut(c.x, c.y, {ax0: x, av: av, marKotelen: true, f: c.f}); })           // átlendül, lemászik, lelép
            .then(function (r) { if (r === 'haza' || !kint) { return 'haza'; } if (r && r.x != null) { c = r; } alattam = c.f || null; return integet(); })
            .then(function (r) { if (r !== 'haza' && kint && c.ul && P.kep === 'alap') { return ul(); } });
    }
    /* fix241 (Sándor: „a fejléc lefejezi Lumit”): Lumi a lap része – a fejléc ALATT halad el (a fejléc eltakarja,
       nem ő a fejlécet). Csak amíg a logóból kibújik / visszabújik, addig van a fejléc fölött. */
    function reteg(fent) { doboz.style.zIndex = fent ? 950 : 45; kotel.style.zIndex = fent ? 948 : 44; }
    function fejAlatt() { return P.y - MAGAS() * .9 < fejlecAlja() - 2; }      // a feje a fejléc alá csúszott
    function hazaCsendben() {                    // fix239: nem látszik, és a képernyőn sehol nincs neki szabad hely
        kotelKi(); kint = false; alattam = null; P.lat = 0; rajzol(); logoAllapot(true); bentIdo = Date.now();
        if (logoG) { logoG.style.transform = 'scale(.7)'; setTimeout(function () { logoAllapot(true); }, 60); }
        return Promise.resolve('bent');
    }
    function visszamaszik() {
        var lv = logoV(), av = lv.al, sajat = megszakit, h = MAGAS(), ax = P.x, y0 = P.y;
        if (!(lv.al > 0 && lv.al < innerHeight) || !latszik()) { return Promise.resolve(); }      // a logó (vagy ő) nem látszik: marad
        var stop = function () { return sajat !== megszakit; };
        function meggondol(x) {                                    // félúton „jé, megint csinál valamit!” – visszamászik
            var c = most() || {x: ax, y: y0, f: alattam}; reteg(false);
            return jel('!', true).then(function () { return var_(400); }).then(function () { return jel('!', false); })
                .then(function () { return kotelut(c.x, c.y, {ax0: x, av: av, marKotelen: true, f: c.f}); })
                .then(function (r) { if (r === 'haza' || !kint) { return; } if (r && r.x != null) { c = r; } alattam = c.f || null; if (c.ul && P.kep === 'alap') { return ul(); } })
                .then(function () { return kint ? 'meggondolta' : 'bent'; });
        }
        var axh = horgonyX(ax);
        return megfog(axh, av)
            .then(function () { return kuszik(P.x, av, function () { return fejlecAlja() + h * 1.3 + 14; }, stop, axh); })       // a fejléc alatt lóg (nem bújik alá)
            .then(function (s) { if (s) { return meggondol(axh); }
                return lendul(axh, lv.x, av).then(function () { if (stop()) { return meggondol(lv.x); }
                    reteg(true);                                                                     // innen a fejléc előtt mászik fel a logóba
                    return kuszik(lv.x, av, function () { return scrollY + logoV().y + h * 1.05; }, stop).then(function (s2) { if (s2) { reteg(false); return meggondol(lv.x); }
                        var y1v = P.y - scrollY;            // fix244: a logóhoz mérve – ha közben görgetsz, nem mászik a logó fölé
                        return anim({meret: .4, lat: 0}, 380, 'be', function (u) { P.y = scrollY + y1v - u * 6; var ay = scrollY + av; kotelRajz(lv.x, ay, ay + (P.y - ay) * (1 - u)); })   // be a logóba
                            .then(function () { kotelKi(); kint = false; alattam = null; reteg(false); logoAllapot(true); bentIdo = Date.now(); return 'bent'; });
                    });
                });
            });
    }

    // ── HOVA ÁLL? fix237 (Sándor: „sose lógjon bele a szövegbe, és a levegőben se lógjon”) ──────────
    // Lumi csak VALÓDI felületen áll vagy ül (mező, doboz, kártya FELSŐ SZÉLÉN), és csak ott, ahol a
    // teste nem takar szöveget, gombot, képet, ikont. Végigpróbálja a felületeket jobbról balra;
    // ha sehol nincs szabad hely, a doboz mellett, a margón KÖTÉLEN lóg (nem a levegőben áll).
    var akadalyIdo = 0, akadalyok = [];
    function akadalyGyujt() {
        if (performance.now() - akadalyIdo < 350) { return akadalyok; }
        akadalyIdo = performance.now(); akadalyok = [];
        var sx = scrollX, sy = scrollY, fel = sy - innerHeight * .5, le = sy + innerHeight * 1.5;
        function tesz(r, tip, el) { if (r.width > 1 && r.height > 1 && r.bottom + sy > fel && r.top + sy < le) {
            akadalyok.push({l: r.left + sx, t: r.top + sy, r: r.right + sx, b: r.bottom + sy, tip: tip, el: el}); } }
        var w = D.createTreeWalker(D.body, NodeFilter.SHOW_TEXT, {acceptNode: function (n) {
            if (!n.nodeValue || !n.nodeValue.trim()) { return NodeFilter.FILTER_REJECT; }
            var p = n.parentElement; if (!p || p.closest('#lumi, script, style, noscript')) { return NodeFilter.FILTER_REJECT; }
            if (p.closest('details:not([open]) > :not(summary)') || (p.checkVisibility && !p.checkVisibility({visibilityProperty: true}))) { return NodeFilter.FILTER_REJECT; }   // fix239: a becsukott GYIK-válasz szövege nem akadály
            return NodeFilter.FILTER_ACCEPT; }});
        var rg = D.createRange(), n;
        while ((n = w.nextNode())) { rg.selectNodeContents(n); [].forEach.call(rg.getClientRects(), function (r) { tesz(r, 'szoveg'); }); }
        D.querySelectorAll('button, img, video, canvas, select, textarea, input, svg, .fp-nyil, .password-toggle, a.fp-gomb, [role=button]').forEach(function (e) {
            if (e.closest('#lumi, details:not([open]) > :not(summary)') || e.type === 'hidden' || (e.checkVisibility && !e.checkVisibility())) { return; }
            var cs = getComputedStyle(e); if (cs.visibility === 'hidden' || cs.display === 'none' || +cs.opacity < .2) { return; }
            if (e.tagName.toLowerCase() === 'svg') { var rs = e.getBoundingClientRect(); if (e.parentElement && e.parentElement.closest('svg')) { return; } var nagy = Math.max(rs.width, rs.height), kis = Math.min(rs.width, rs.height); if (nagy > 90 && (kis < 26 || nagy / Math.max(1, kis) > 6 || e.getAttribute('aria-hidden') === 'true')) { return; } }   // fix239: a nagy díszítő vonal (pl. pöttyözött út) nem akadály, az ikon igen
            tesz(e.getBoundingClientRect(), e.matches('input, textarea, select') ? 'mezo' : 'elem', e);
        });
        return akadalyok;
    }
    function szovegSzeles(m) {                 // a mezőbe írt szöveg (vagy helykitöltő) mennyi helyet foglal balról
        try { var cs = getComputedStyle(m), c = szovegSzeles.c || (szovegSzeles.c = D.createElement('canvas').getContext('2d'));
            c.font = cs.fontWeight + ' ' + cs.fontSize + ' ' + cs.fontFamily;
            var t = m.type === 'password' ? (m.value ? new Array(m.value.length + 1).join('●') : '') : (m.value || m.placeholder || '');
            return parseFloat(cs.paddingLeft) + c.measureText(t).width + 14; } catch (e) { return 80; }
    }
    function dobozom(x, y, ules) {            // Lumi teste ezen a helyen (lapkoordináták)
        var h = MAGAS(), fel = ules ? .82 : .99, al = ules ? .22 : 0;
        return {l: x - h * .25, r: x + h * .25, t: y - h * fel, b: y + h * al};
    }
    function utkozik(d, sajatMezo) { return takaras(d, sajatMezo) > 0; }
    var fejAljaIdo = 0, fejAlja = 0;
    function fejlecAlja() {                     // fix239: a (ragadós) fejléc alja lapkoordinátában – Lumi teste ennél feljebb nem lóghat
        if (performance.now() - fejAljaIdo > 300) { fejAljaIdo = performance.now(); var hd = D.querySelector('.navbar, header'); fejAlja = hd ? hd.getBoundingClientRect().bottom : 0; }
        return scrollY + Math.max(0, fejAlja);
    }
    function takaras(d, sajatMezo) {          // fix238: MENNYI szöveget/elemet takarna (terület, px²)
        var a = akadalyGyujt(), ossz = 0, fa = fejlecAlja();
        if (d.t < fa + 2) { ossz += (fa + 2 - d.t) * (d.r - d.l) * 3; }       // belelógna a fejlécbe
        for (var i = 0; i < a.length; i++) {
            var o = a[i], l = o.l, r = o.r;
            if (o.tip === 'mezo') {                       // a mezőn ülhet/állhat – csak a beírt szövegre nem lóghat
                if (o.el === sajatMezo || (sajatMezo && o.el && o.el.closest && sajatMezo.closest && o.el === sajatMezo)) { r = l + szovegSzeles(o.el); }
                else if (d.b <= o.t + 3) { continue; }    // fölötte áll: nem ütközés
                else { r = l + szovegSzeles(o.el); }
            }
            var ww = Math.min(d.r, r + 4) - Math.max(d.l, l - 4), hh = Math.min(d.b, o.b + 3) - Math.max(d.t, o.t + 3);
            if (ww > 0 && hh > 0) { ossz += ww * hh * (o.tip === 'szoveg' ? 1 : 1.5); }
        }
        return ossz;
    }
    function felulet(el) { var p = lap(el); return {l: p.x, r: p.x + p.w, y: p.y, w: p.w, el: el}; }
    /* fix238 (Sándor: „ne oldalt a levegőben – találja meg a helyet, ahol nem takar”): mindig VALÓDI felületen
       marad. Sorrend: állva semmit nem takar → ülve (a lába a mező üres részén) semmit nem takar → ahol a
       legkevesebbet takarná. Kötélen oldalt már nem lóg. */
    /* fix239 (Sándor: „belelóg a szövegbe”, csomagok: a levegőben ült): csak LÁTHATÓ felületen áll – aminek
       háttere, kerete vagy árnyéka van (kártya, mező, sáv) –, és csak ott, ahol a talpa alatt tényleg az a
       felület van (nem takarja el más). Az átlátszó „láthatatlan dobozok” teteje nem felület. */
    function alfa(c) { if (!c || c === 'transparent') { return 0; } var m = c.match(/rgba?\(([^)]+)\)/); if (!m) { return 1; }
        var p = m[1].split(/[\s,\/]+/).filter(Boolean); return p.length > 3 ? parseFloat(p[3]) : 1; }
    function valodi(el) {
        if (!el || el.nodeType !== 1) { return false; }
        if (el.matches('input:not([type=checkbox]):not([type=radio]), textarea, select, button, img, video, canvas')) { return true; }
        var cs = getComputedStyle(el);
        if (cs.visibility === 'hidden' || +cs.opacity < .3) { return false; }
        return alfa(cs.backgroundColor) > .15 || cs.backgroundImage !== 'none' || cs.boxShadow !== 'none' ||
            (parseFloat(cs.borderTopWidth) > .5 && cs.borderTopStyle !== 'none' && alfa(cs.borderTopColor) > .15);
    }
    function alatta(x, y, el) {                 // a talpa alatt (pár px-szel lejjebb) tényleg ez a felület van-e
        var vx = x - scrollX, vy = y + 3 - scrollY;
        if (vx < 1 || vy < 1 || vx > innerWidth - 1 || vy > innerHeight - 1) { return true; }   // nem látszik – nem tudjuk ellenőrizni
        var t = D.elementsFromPoint(vx, vy);
        for (var i = 0; i < t.length; i++) { if (t[i].closest('#lumi')) { continue; } return el.contains(t[i]); }
        return false;
    }
    /* fix242 (Sándor: „hova ül le? a semmibe!”): a hullámos / tépett szélű sávok (svg) befoglaló doboza feljebb
       kezdődik, mint a látható széle – ott a doboz teteje még levegő. Ilyenkor lejjebb keresi, hol kezdődik
       ténylegesen a felület ezen az x-en (az svg átlátszó részén a böngésző magát az <svg>-t „találja el”, a
       festett részen a rajzot). */
    /* fix243 (Sándor: „a levegőben áll meg, pár másodperc múlva visszamászik”): a talajt a KÉPPONTOK alapján
       keresi, nem a dobozok méretéből. Egy oszlopban (x) ott kezdődik felület, ahol fölötte (6 px-szel) még
       más látszik, alatta pedig egy festett, ELŐRÉBB lévő dolog: kártya, mező, gomb, kép, a zöld hullám rajza…
       A doboz átlátszó része, a kártya alja (alatta a háttér) vagy a szöveg sora nem talaj. Ugyanezzel a
       szabállyal választ helyet ÉS ezzel ellenőrzi utána is magát – így nem mond ellent saját magának. */
    function festett(e) {
        if (!e || e === D.body || e === D.documentElement || !e.tagName) { return false; }
        if (e.tagName.toLowerCase() === 'svg') { return false; }            // az svg átlátszó része
        if (typeof SVGElement !== 'undefined' && e instanceof SVGElement) { return true; }   // a rajz festett része (path, rect…)
        return valodi(e);
    }
    function verem(x, y) {
        var vx = x - scrollX, vy = y - scrollY;
        if (vx < 1 || vy < 1 || vx > innerWidth - 1 || vy > innerHeight - 1) { return null; }
        return D.elementsFromPoint(vx, vy).filter(function (e) { return !e.closest('#lumi'); });
    }
    function elso(st) { if (!st) { return null; } for (var i = 0; i < st.length; i++) { if (festett(st[i])) { return st[i]; } } return null; }
    function szine(e) {                          // a festett elem színe (svg: kitöltés, egyébként háttér); null, ha nem egyszínű
        try { var cs = getComputedStyle(e), c = (typeof SVGElement !== 'undefined' && e instanceof SVGElement) ? cs.fill : cs.backgroundColor;
            if (!(typeof SVGElement !== 'undefined' && e instanceof SVGElement) && cs.backgroundImage !== 'none') { return null; }
            var m = c && c.match(/rgba?\(([^)]+)\)/); if (!m) { return null; }
            var p = m[1].split(/[\s,\/]+/).filter(Boolean).map(parseFloat); return p.length > 3 && p[3] < .5 ? null : p.slice(0, 3);
        } catch (er) { return null; }
    }
    function egyszinu(a, b) { var ca = szine(a), cb = szine(b); return ca && cb && Math.abs(ca[0] - cb[0]) + Math.abs(ca[1] - cb[1]) + Math.abs(ca[2] - cb[2]) < 36; }
    function talajE(x, y) {                     // y-nál (lapkoordináta) kezdődik-e látható felület ebben az oszlopban
        var s2 = verem(x, y + 2), s1 = verem(x, y - 6); if (!s2 || !s1) { return null; }
        var lent = elso(s2), fent = elso(s1);
        if (!lent || lent === fent) { return null; }
        if (fent && egyszinu(fent, lent)) { return null; }                 // ugyanaz a szín folytatódik (pl. a zöld hullám alatt a zöld sáv) – nem látszik határ
        if (fent) {
            var fi = s2.indexOf(fent);
            if (fi >= 0 && fi < s2.indexOf(lent)) { return null; }        // a fenti tart tovább, és előrébb van
            if (fi < 0 && lent.contains(fent)) { return null; }            // a kártya alja: alatta a saját háttere – nem talaj
        }
        return lent;
    }
    function talajKeres(x, y0, fel, le) {        // a y0-hoz legközelebbi talaj ebben az oszlopban (fel: ennyit felfelé, le: ennyit lefelé)
        fel = fel == null ? 140 : fel; le = le == null ? 40 : le;
        for (var d = 0; d <= Math.max(fel, le); d += 3) {
            if (d <= fel) { var e1 = talajE(x, y0 - d); if (e1) { return {y: y0 - d + 1, el: e1}; } }
            if (d && d <= le) { var e2 = talajE(x, y0 + d); if (e2) { return {y: y0 + d + 1, el: e2}; } }
        }
        return null;
    }
    function talajItt(x, y) {                    // áll-e valamin (ül vagy áll) – a figyelő és a csiklandozás ezt nézi
        if (!verem(x, y + 2)) { return true; }                                  // nem látszik – nem tudjuk ellenőrizni
        return !!talajKeres(x, y - 1, 6, 6) || !!talajKeres(x - 8, y - 1, 6, 6) || !!talajKeres(x + 8, y - 1, 6, 6);
    }
    function keres(feluletek, sajatMezo) {
        var h = MAGAS(), fel = h * .28, lx = scrollX + 6, rx = scrollX + innerWidth - 6, legjobb = null;
        feluletek = feluletek.filter(function (f) { return f && f.w >= h * .6 && f.y > scrollY + 20 && f.y < scrollY + innerHeight - 8 && valodi(f.el); });   // csak látható, valódi felület
        for (var mod = 0; mod < 2; mod++) {
            for (var i = 0; i < feluletek.length; i++) {
                var f = feluletek[i];
                var bal = Math.max(f.l + fel, lx + fel), jobb = Math.min(f.r - fel, rx - fel);
                for (var x = jobb; x >= bal; x -= 8) {
                    var t = takaras(dobozom(x, f.y + 1, mod === 1), sajatMezo) + (jobb - x) * .01 + i * 50;
                    if (t < 1 + (jobb - x) * .01 + i * 50) {
                        var g = talajKeres(x, f.y); if (!g) { continue; }
                        var yy = g.y;
                        if (Math.abs(yy - f.y - 1) > 1 && (yy < scrollY + 20 || takaras(dobozom(x, yy, mod === 1), sajatMezo) >= 1)) { continue; }
                        return {x: x, y: yy, ul: mod === 1, f: f.el};
                    }
                }
            }
        }
        return null;            // fix239 (Sándor: „belelóg a szövegbe”): ha mindenhol takarna, itt nincs helye – inkább máshová megy
    }
    function kartyaja(el) { return el.closest('.fp-kartya, .auth-card, .doboz, .card, details, form, main section') || el.parentElement; }
    function helyMezo(m) {
        var c = m.closest('.password-field, .input-group') || m;
        if (m.type === 'checkbox' || m.type === 'radio') { c = m.closest('label, .field') || m; }
        var mezo = m.matches('input, textarea, select') && m.type !== 'checkbox' ? m : null;
        // csak a mező közelében keres (a doboz tetejére nem ugrik el – ott messze lenne attól, amit csinálsz)
        return keres([felulet(c), c !== m && felulet(m), m.closest('.field') && felulet(m.closest('.field'))], mezo);
    }
    function helyDoboz(el) {
        var k = kartyaja(el), fl = [felulet(el), k && k !== el && felulet(k)], n = (k && k !== el ? k : el).nextElementSibling;
        // fix239: ha ott nincs szabad hely (pl. a doboz fölött szöveg van), a következő 1-3 dobozon keres – nem lóg bele a szövegbe
        for (var i = 0; i < 3 && n; i++, n = n.nextElementSibling) { var r = n.getBoundingClientRect(); if (r.width > 200 && r.height > 30) { fl.push(felulet(n)); } }
        return keres(fl, null);
    }
    function ulhet() {                           // leülhet-e ott, ahol áll (a lába se takarjon szöveget)
        return horgony && !utkozik(dobozom(P.x, P.y, true), horgony.matches && horgony.matches('input, textarea') ? horgony : null);
    }
    function fodoboz() {                          // fix239: a látható rész egyik VALÓDI doboza, ahol nem takar szöveget
        var jel_ = ['.fp-kartya', '.auth-card', '.doboz', 'details.fp-k', '.fp-k', '.cs-lap', '.card', 'details', 'main section', 'main form', 'main h2', '.content'];
        var fent = tetoY() - scrollY + MAGAS() * 1.1, legjobb = null, lt = 1e12, volt = [];
        function probal(e) {
            if (volt.indexOf(e) >= 0 || e.closest('#lumi, .navbar, header')) { return false; }
            volt.push(e);
            var r = e.getBoundingClientRect();
            if (!(r.width > 120 && r.height > 24 && r.top > fent && r.top < innerHeight - 30)) { return false; }
            var hh = helyDoboz(e); if (!hh) { return false; }
            legjobb = e; return true;
        }
        for (var i = 0; i < jel_.length; i++) {
            var t = D.querySelectorAll(jel_[i]);
            for (var j = 0; j < t.length; j++) { if (probal(t[j])) { return legjobb; } }
        }
        // bármilyen más látható felület (sáv, kép, gomb, táblázat…), a képernyő közepéhez legközelebb
        var mind = [].slice.call(D.querySelectorAll('body *')).filter(function (e) {
            if (e.closest('#lumi, .navbar, header, script, style')) { return false; }
            var r = e.getBoundingClientRect(); return r.width > 120 && r.height > 24 && r.top > fent && r.top < innerHeight - 30 && valodi(e); });
        mind.sort(function (a, b) { return Math.abs(a.getBoundingClientRect().top - innerHeight * .45) - Math.abs(b.getBoundingClientRect().top - innerHeight * .45); });
        var tetok = {};
        for (var k = 0, n = 0; k < mind.length && n < 90; k++) { var tk = Math.round(mind[k].getBoundingClientRect().top / 4); if (tetok[tk] > 2) { continue; } tetok[tk] = (tetok[tk] || 0) + 1; n++; if (probal(mind[k])) { return legjobb; } }
        return null;
    }
    var horgony = null;
    function most() {
        if (!horgony) { return null; }
        return horgony.matches && horgony.matches('input, select, textarea') ? helyMezo(horgony) : helyDoboz(horgony);
    }
    function lathato(y) { return y > scrollY + 50 && y < scrollY + innerHeight - 10; }
    function latszik() { return P.y > scrollY + 5 && P.y - MAGAS() * .9 < scrollY + innerHeight - 5; }   // Lumi bármely része látszik
    function rendben() { return P.y > scrollY + 5 && P.y < scrollY + innerHeight - 2 && !fejAlatt(); }   // fix241: EGÉSZEN látszik (a lába sem lóg ki alul, a feje sincs a fejléc alatt)
    function menj(hely) {                       // fix239: séta / kis ugrás / kötélút – sosem teleportál
        hely = hely || most();
        if (!hely || !lathato(hely.y)) { return Promise.resolve(); }      // a cél nem látszik: marad
        var h = MAGAS(), dx = Math.abs(hely.x - P.x), dy = Math.abs(hely.y - P.y), ut;
        if (!latszik()) { ut = leereszkedik(hely.x, hely.y, hely.f); }
        else if (dx < 3 && dy < 3) { ut = Promise.resolve(); }
        else if (dy < 3 && (hely.f === alattam || dx < h * .9)) { ut = seta(hely.x); }
        else if (dx < h * 2.2 && dy < h * 1.4) { ut = ugras(hely.x, hely.y, Math.max(h * .3, (P.y - hely.y) + h * .35), Math.min(650, 340 + Math.hypot(dx, dy) * .5)); }
        else { ut = kotelut(hely.x, hely.y, {f: hely.f}); }
        return ut.then(function (r) {
            if (r === 'haza' || !kint) { return; }                        // útközben hazament (nem volt látható hely)
            var hh = r && r.x != null ? r : hely;                         // fix243: ha útközben új helyet választott, az számít
            alattam = hh.f || null; P.arnyek = 1; if (hh.ul && P.kep === 'alap') { return ul(); } });
    }

    // ── EGYÜTT ÉL VELÜNK: ha hozzáérsz, odébb ugrik ───────────────────────
    var csikiIdo = -1e9;
    function csiki(ev) {
        if (!kint || fut > 1 || performance.now() - csikiIdo < 900) { return; }
        csikiIdo = performance.now();
        var ex = (ev && ev.pageX) || P.x, irany = ex < P.x ? 1 : -1, h = MAGAS();
        // fix239: ugyanazon a felületen ugrik odébb, és csak oda, ahol nem takar szöveget; ha nincs ilyen hely, csak összerezzen
        var f = alattam && felulet(alattam), sm = horgony && horgony.matches && horgony.matches('input, textarea') ? horgony : null, cel = null;
        [irany, -irany].some(function (ir) {
            if (!f) { return true; }
            for (var d = h * .6; d <= h * 1.6; d += 8) {
                var x = P.x + ir * d;
                if (x < f.l + h * .28 || x > f.r - h * .28 || x < scrollX + 20 || x > scrollX + innerWidth - 20) { break; }
                if (takaras(dobozom(x, P.y, false), sm) < 1 && talajItt(x, P.y)) { cel = x; irany = ir; return true; }
            }
            return false;
        });
        megszakit++; utolsoMozdulat = Date.now();
        tedd(function () {
            if (P.kep === 'ul') { legyen('alap'); }
            var mozdul = cel != null ? ugras(cel, P.y, h * .35, 330) : anim({ny: .9, dol: -irany * 6}, 160, 'ki').then(function () { return anim(NYUGI, 420, 'rugo'); });
            return jel('!', true).then(function () { return mozdul; })
                .then(function () { return jel('!', false); }).then(function () { return anim({fej: -irany * 10}, 300); })
                .then(function () { return var_(500); }).then(function () { return alap(300); });
        });
    }
    R.test.addEventListener('pointerenter', function (e) { if (e.pointerType === 'mouse') { csiki(e); } });
    R.test.addEventListener('pointerdown', function (e) { csiki(e); });

    // ── REAKCIÓK ────────────────────────────────────────────────────────
    var utolsoMozdulat = Date.now();
    function tevekeny(cel) {           // a felhasználó csinál valamit: ha bent van, kijön; ha mászik vissza, megáll
        utolsoMozdulat = Date.now(); megszakit++;
        if (cel) { horgony = cel; }
        if (!kint && fut === 0) { tedd(function () { var h = most(); return h ? kijon({y: h.y, hely2: h}) : null; }); return true; }
        return !kint;
    }
    var mezoAll = new WeakMap();
    function jo(m) {
        if (m.type === 'checkbox') { return m.checked; }
        var v = (m.value || '').trim(); if (!v) { return false; }
        if (m.id === 'password_confirm') { var p = D.getElementById('password'); if (p && p.value !== m.value) { return false; } }
        return m.checkValidity ? m.checkValidity() : true;
    }
    function urlap(f) {
        var mezok = [].slice.call(f.querySelectorAll('input, select, textarea')).filter(function (m) { return m.type !== 'hidden'; });
        var idoz = null;
        mezok.forEach(function (m) {
            m.addEventListener('focus', function () {
                akadalyIdo = 0;
                if (tevekeny(m)) { return; }
                if (fut > 1) { return; }
                tedd(function () { return menj(helyMezo(m)).then(function () { if (P.kep !== 'ul') { return lenez(); } }); });
            });
            var gepel = function () {
                utolsoMozdulat = Date.now();
                clearTimeout(idoz);
                idoz = setTimeout(function () {
                    var ok = jo(m), volt = mezoAll.get(m), v = (m.value || '').trim();
                    if (ok && volt !== 'jo') { mezoAll.set(m, 'jo'); if (kint && fut < 2) { tedd(function () { return orul(false); }); } }
                    else if (!ok && v && volt !== 'rossz') { mezoAll.set(m, 'rossz'); if (kint && fut < 2) { tedd(fejetFog); } }   // abbahagyta a gépelést, és nem jó
                    else if (!ok && !v) { mezoAll.set(m, ''); }
                }, 1400);
            };
            m.addEventListener('input', gepel); m.addEventListener('change', gepel);
            m.addEventListener('blur', function () {
                var v = (m.value || '').trim();
                if (!kint || fut >= 2) { return; }
                if (v && !jo(m) && mezoAll.get(m) !== 'rossz') { mezoAll.set(m, 'rossz'); tedd(fejetFog); }
                else if (!v && m.required && m.type !== 'checkbox') { tedd(gondolkodik); }
            });
        });
        f.addEventListener('submit', function () {
            var mind = mezok.every(function (m) { return !m.required || jo(m); });
            if (kint) { tedd(mind ? function () { return orul(true); } : gondolkodik); }
        });
    }

    // ── INDULÁS ─────────────────────────────────────────────────────────
    /* fix284 (a main GYIK-oldalán Lumi nem jött ki, a próbán igen – Sándor gépén, azonos ablakban
       nézve): induláskor még nem talált helyet, és többé nem is próbálta; pár másodperccel később
       ugyanott már talált volna. Most ha elsőre nincs hely, 0,7 mp-enként még 6-szor megpróbálja. */
    function kijonHaLehet(proba) {
        nl('kijonHaLehet', proba, 'kijott=' + kijott, 'kint=' + kint, 'scrollY=' + Math.round(scrollY));
        if (kijott) { return; }
        akadalyIdo = 0;
        var cel = fodoboz(), h = cel && helyDoboz(cel);
        horgony = cel;
        // ha van űrlap, egyenesen az első mezőre ugrik (a doboz tetején a fölötte lévő szöveget takarná)
        var elso = [].slice.call(D.querySelectorAll('main form input, .fp form input, .content form input')).filter(function (m) {
            var r = m.getBoundingClientRect(); return m.type !== 'hidden' && m.offsetParent && r.width > 120 && r.left >= 0 && r.right <= innerWidth && r.top > 80 && r.bottom < innerHeight - 20; })[0];
        var hm = elso && helyMezo(elso); if (hm) { horgony = elso; h = hm; }
        nl('hely', cel && cel.className, h ? Math.round(h.x) + ',' + Math.round(h.y) : null);
        if (h) {
            kijott = true;
            tedd(function () { return var_(400).then(function () { return kijon({y: h.y, hely2: h}); }); });
            /* fix286: ha a kijövés valamiért elakadt (hiba, vagy közben máshová ment), 4 mp múlva
               újra próbálja – eddig a „kijott” jelző ilyenkor örökre lezárta az utat. */
            setTimeout(function () { if (!kint && !fut && proba < 6) { nl('nem jott ki - ujra'); kijott = false; kijonHaLehet(proba + 1); } }, 4000);
        }
        else if (proba < 6) { setTimeout(function () { kijonHaLehet(proba + 1); }, 700); }
    }
    function indul() {
        nl('indul');
        D.body.appendChild(doboz);
        kijonHaLehet(0);
        D.querySelectorAll('main form, .content form, .fp form').forEach(function (f) { if (!f.closest('header, nav')) { urlap(f); } });
        D.querySelectorAll('details').forEach(function (d) {
            d.addEventListener('toggle', function () {
                akadalyIdo = 0;
                if (!d.open) { return; }
                var s = d.querySelector('summary') || d;
                if (tevekeny(s)) { return; }
                if (fut < 2) { tedd(function () { return menj(helyDoboz(s)).then(gondolkodik).then(aha); }); }
            });
        });
        var gIdo = null;
        addEventListener('scroll', function () {
            clearTimeout(gIdo);
            gIdo = setTimeout(function bejon() {                      // fix239: ha épp mást csinál, kicsit később jön le
                if (!kint && (fut || (kijott && Date.now() - bentIdo < 2500))) { gIdo = setTimeout(bejon, 600); return; }
                if (!kint) { var c0 = fodoboz(); if (c0) { kijott = true; horgony = c0; tedd(function () { var h1 = helyDoboz(c0); nl('gorgetes-kijon', h1 ? 'van hely' : 'NINCS hely'); if (!h1) { kijott = false; return; } return kijon({y: h1.y, hely2: h1}); }); } return; }   // fix286: ha nincs hely, ne zárja le az utat   // fix239: ha betöltéskor nem volt hova, görgetéskor jön ki
                if (!kint || rendben()) { return; }
                if (latszik()) {            // fix241: csak részben látszik (a fejléc alatt / alul kilóg) – kötélen átmegy egy egészen látható helyre (vagy hazamászik)
                    if (fut) { gIdo = setTimeout(bejon, 500); return; }
                    var c1 = fodoboz(); if (c1) { horgony = c1; tedd(function () { return menj(helyDoboz(c1)); }); } else { tedd(visszamaszik); }
                    return;
                }
                if (fut) { gIdo = setTimeout(bejon, 500); return; }
                var uj = fodoboz(); if (uj) { horgony = uj; tedd(function () { return menj(helyDoboz(uj)); }); } else { tedd(hazaCsendben); }
            }, 450);
        }, {passive: true});
        var rIdo = null;
        addEventListener('resize', function () {          // fix239: a felülete mozdult el – vele megy; ha máshová kell, odamegy
            akadalyIdo = 0; clearTimeout(rIdo);
            rIdo = setTimeout(function () {
                if (!kint || fut || !horgony) { return; }
                var m2 = most(); if (!m2) { return; }
                if (m2.f === alattam) { P.x = m2.x; P.y = m2.y; rajzol(); } else { tedd(function () { return menj(m2); }); }
            }, 250);
        });
        // ha sokáig nem csinálsz semmit, visszamászik a logóba
        setInterval(function () {
            if (!kint || fut || D.hidden) { return; }
            var tetlen = Date.now() - utolsoMozdulat;
            if (tetlen > 40000) { tedd(visszamaszik); return; }
            // fix231: ha egy mezőn áll, és egy ideje nem történik semmi, leül a mező szélére
            // fix239 (Sándor: „üljön le, ahogy a főoldalon”): ha egy ideje nem történik semmi, leül a felület szélére –
            // csak ha a lába sem takar szöveget, és nem egy rosszul kitöltött mezőn van
            if (tetlen > 5000 && P.kep === 'alap' && horgony && rendben() && ulhet()
                && !(horgony.matches && horgony.matches('input, select, textarea') && (horgony.value || '').trim() && !jo(horgony))) { tedd(ul); return; }
            if (tetlen > 9000 && Math.random() < .35 && lathato(P.y)) {
                tedd(Math.random() < .5 ? integet : function () { return anim({fej: 12}, 500).then(function () { return var_(600); }).then(function () { return anim({fej: -10}, 700); }).then(function () { return alap(500); }); });
            }
        }, 4000);
        /* fix242 (Sándor: „legyen okos, vegyen észre mindent, mint egy igazi kabala”): FIGYELŐ – fél másodpercenként
           megnézi magát: látszik-e egészen, valódi felületen áll-e (nem a levegőben), nem takar-e szöveget, nincs-e
           a fejléc alatt. Ha bármelyik nem stimmel, magától keres jó helyet, és oda megy (séta / ugrás / kötél);
           ha a képernyőn nincs ilyen hely, hazamászik a logóba. */
        function baj() {
            if (!latszik()) { return 'nem-latszik'; }
            if (!rendben()) { return 'reszben'; }
            var sm = horgony && horgony.matches && horgony.matches('input, textarea') ? horgony : null;
            if (takaras(dobozom(P.x, P.y, P.kep === 'ul'), sm) > 40) { return 'takar'; }
            if (!talajItt(P.x, P.y)) { return 'levego'; }
            return '';
        }
        function javit(ok) {
            var h2 = ok !== 'nem-latszik' && most(), c2 = null;
            if (h2 && !(Math.abs(h2.x - P.x) < 3 && Math.abs(h2.y - P.y) < 3)) { tedd(function () { return menj(h2); }); return; }
            c2 = fodoboz();
            var h3 = c2 && helyDoboz(c2);
            if (h3 && !(Math.abs(h3.x - P.x) < 3 && Math.abs(h3.y - P.y) < 3)) { horgony = c2; tedd(function () { return menj(h3); }); return; }
            tedd(latszik() ? visszamaszik : hazaCsendben);
        }
        var bajSzam = 0;
        setInterval(function () {
            if (!kint || fut || D.hidden || P.lat < .9 || (P.kep !== 'alap' && P.kep !== 'ul') || performance.now() - csikiIdo < 1500) { bajSzam = 0; return; }
            var b = baj();
            bajSzam = b ? bajSzam + 1 : 0;
            if (bajSzam >= 2) { bajSzam = 0; akadalyIdo = 0; javit(b); }     // kétszer egymás után (1 mp) – görgetés közben nem kapkod
        }, 500);
        ['pointerdown', 'keydown'].forEach(function (t) { addEventListener(t, function () { utolsoMozdulat = Date.now(); megszakit++; }, true); });
        /* fix243 (Sándor: „figyeljen mindenre, mint egy igazi kabala”): FIGYEL RÁD –
           · a fejét arra fordítja, amerre az egér / az ujjad van (ha közel vagy hozzá);
           · ha egy gomb vagy link fölé viszed az egeret, a lámpája felragyog (a fő gomboknál jobban);
           · ha rákattintasz valamire, odanéz és bólint egyet. */
        var mut = {x: -1e4, y: -1e4, t: 0}, ragyog = 0;
        addEventListener('pointermove', function (e) { mut.x = e.pageX; mut.y = e.pageY; mut.t = performance.now(); }, {passive: true});
        var GOMB = 'a, button, summary, [role=button], input[type=submit], .fp-gomb, .nav-cta';
        D.addEventListener('pointerover', function (e) {
            var g = e.target && e.target.closest && e.target.closest(GOMB);
            if (!g || g.closest('#lumi')) { return; }
            ragyog = g.matches('.fp-gomb, .nav-cta, button[type=submit], .fp-teli') ? .75 : .35;
        });
        D.addEventListener('pointerout', function (e) {
            var g = e.target && e.target.closest && e.target.closest(GOMB);
            if (g && !(e.relatedTarget && g.contains(e.relatedTarget))) { ragyog = 0; }
        });
        D.addEventListener('pointerdown', function (e) {
            mut.x = e.pageX; mut.y = e.pageY; mut.t = performance.now();
            var g = e.target && e.target.closest && e.target.closest(GOMB);
            if (!kint || fut || !g || g.closest('#lumi') || !rendben()) { return; }
            tedd(function () { return anim({ny: .9, fej: (e.pageX < P.x ? -1 : 1) * 9}, 130, 'ki').then(function () { return anim({ny: 1}, 380, 'rugo'); }); });
        }, true);
        // pihenés: lélegzik, a fény pislákol
        var t0 = performance.now();
        (function el(t) {
            if (kint && !fut && P.lat > .9) {
                var s = (t - t0) / 1000; P.ny = 1 + Math.sin(s * 2.2) * .012;
                if (P.kep === 'alap' || P.kep === 'ul') {      // fix243: odafordul, ahol az egér / az ujjad van; a lámpa ragyog, ha gombon vagy
                    var tav = Math.hypot(mut.x - P.x, mut.y - (P.y - MAGAS() * .6)), friss = t - mut.t < 4000;
                    var cel = friss && tav < 650 ? Math.max(-10, Math.min(10, (mut.x - P.x) / 25)) : 0;
                    P.fej += (cel - P.fej) * .08;
                    P.feny += (ragyog - P.feny) * .08;
                }
                /* fix234: ha az oldal elmozdul alatta (pl. megjelenik a jelszó-csík, és lejjebb csúsznak a mezők),
                   vele megy – mindig a mező vonalán marad */
                if (horgony && (P.kep === 'alap' || P.kep === 'ul') && t - (el.utolso || 0) > 400 && performance.now() - csikiIdo > 5000) {
                    el.utolso = t; var h0 = most();
                    if (h0) {
                        var sajat = h0.f === alattam, dx = Math.abs(h0.x - P.x), dy = Math.abs(h0.y - P.y);
                        if (sajat && dy > 1) { P.y = h0.y; dy = 0; }                                               // a felülete mozdult: vele megy
                        var itt = sajat && takaras(dobozom(P.x, P.y, P.kep === 'ul'), horgony.matches && horgony.matches('input, textarea') ? horgony : null) < 1;
                        if (!sajat || (dx > 8 && !itt)) { if (lathato(h0.y) && rendben()) { tedd(function () { return menj(most()); }); } }   // fix239: csak ha a mostani helyén takarna, vagy másik felületre kell
                        else if (itt) { /* jó helyen van: marad */ }
                        else if (h0.ul && P.kep === 'alap') { tedd(ul); }                                           // fix238: ott csak ülve fér el
                        else if (sajat && dx > 1) { P.x = h0.x; }
                    }
                }
                rajzol();
            }
            requestAnimationFrame(el);
        })(t0);
    }
    window.__lumi = {poz: function (o) { Object.assign(P, o); rajzol(); }, hely: function () { var h = most(); return h && {x: h.x, y: h.y, ul: h.ul, t: h.t, P: [P.x, P.y, P.kep]}; },
        doboz: function () { var e = fodoboz(); return e && (e.tagName + '.' + e.className); },
        allapot: function () { return {x: P.x, y: P.y, kep: P.kep, kint: kint, fut: fut, lat: P.lat, h: MAGAS()}; }, orul: function () { return tedd(function () { return orul(true); }); }, gondolkodik: function () { return tedd(gondolkodik); },
        integet: function () { return tedd(integet); }, aha: function () { return tedd(aha); }, vissza: function () { return tedd(visszamaszik); }};
    /* fix263: Lumi csak akkor indul, amikor az oldal MÁR BETÖLTÖTT (képek is),
       és a böngésző ráér – így az első másodpercekben nem lassítja az oldalt
       (PageSpeed/Geekflare: sok hosszú feladat a főoldalon). Ha a betöltés
       4 mp alatt sem fejeződik be, akkor is elindul. */
    var lumiIndult = false;
    function lumiIndit() {
        if (lumiIndult) { return; }
        lumiIndult = true;
        var ura = window.requestIdleCallback || function (f) { return setTimeout(f, 1); };
        ura(function () { setTimeout(indul, 400); }, {timeout: 2000});
    }
    if (D.readyState === 'complete') { lumiIndit(); }
    else {
        window.addEventListener('load', lumiIndit);
        setTimeout(lumiIndit, 4000);
    }
})();
