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
    doboz.style.cssText = 'position:absolute;left:0;top:0;width:0;height:0;z-index:950;pointer-events:none;';
    var kotel = D.createElementNS(NS, 'svg');
    kotel.style.cssText = 'position:absolute;left:0;top:0;width:1px;height:1px;overflow:visible;pointer-events:none;z-index:948';
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
    function tedd(fv) { fut++; sor = sor.then(fv).catch(function (e) { if (window.console) { console.warn('lumi', e); } }).then(function () { fut--; }); return sor; }
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
    function kotelRajz(x, y1, y2) { kp.forEach(function (p) { p.setAttribute('d', y2 > y1 ? 'M' + x + ' ' + y1 + ' L' + x + ' ' + y2 : ''); }); }
    function kotelBe() { if (!kotel.parentNode) { D.body.insertBefore(kotel, doboz); } }
    function kotelKi() { kotelRajz(0, 0, 0); if (kotel.parentNode) { kotel.parentNode.removeChild(kotel); } }

    // ── KI A LOGÓBÓL / VISSZA ───────────────────────────────────────────
    var kint = false;
    function logoPont() { var l = lap(logo); return {x: l.x + l.w / 2, y: l.y + l.h * .55, al: l.y + l.h}; }
    function kijon(cel) {
        var lp = logoPont(), x = lp.x;
        logoAllapot(true, true);                                   // lenéz
        kotelBe();
        var cY = cel.y, fent = lp.al - 2;
        return var_(450)
            .then(function () { return anim({}, 380, 'ki', function (u, e) { kotelRajz(x, fent, fent + (Math.min(cY, fent + innerHeight * .8) - fent) * e); }); })   // ledobja a kötelet
            .then(function () {
                logoAllapot(false); kint = true;
                P.x = x; P.y = lp.y + MAGAS() * .35; P.meret = .4; P.lat = 1; P.feny = 0; Object.assign(P, NYUGI); maszik(0); P.arnyek = 0;
                return anim({meret: 1}, 420, 'ki', function (u) { P.y = lp.y + MAGAS() * (.35 + .9 * u); });       // kibújik
            })
            .then(function () {
                var y0 = P.y, ut = Math.max(0, cY - y0);
                return anim({feny: 0}, Math.min(2600, 500 + ut * 4), 'lin', function (u) {
                    P.y = y0 + ut * u; maszik(u, 2 + ut / 40);
                    kotelRajz(x, fent, Math.max(P.y + 8, cY));
                });
            })
            .then(function () {                                        // a kötélről átugrik a dobozra / mezőre
                var h2 = cel.hely2 || most() || {x: x + 80, y: cY};
                P.arnyek = 1;
                return Promise.all([
                    ugras(h2.x, h2.y, MAGAS() * .45, Math.min(720, 380 + Math.abs(h2.x - x) * .5)),
                    var_(250).then(function () { return anim({}, 420, 'be', function (u) { kotelRajz(x, fent, cY - (cY - fent) * u); }); })
                ]);
            })
            .then(function () { kotelKi(); return integet(); });
    }
    function visszamaszik() {
        var lp = logoPont(), fent = lp.al - 2, sajat = megszakit;
        if (!lathato(lp.al + 40)) { return Promise.resolve(); }                       // a logó nem látszik: marad
        kotelBe();
        var y0r = P.y;
        return anim({}, 360, 'ki', function (u, e) { kotelRajz(lp.x, fent, fent + (y0r - fent) * e); })      // ledobja a kötelet
            .then(function () { if (sajat !== megszakit) { return 'meggondolta'; }
                P.arnyek = 0; return ugras(lp.x, y0r, MAGAS() * .3, 420); })                                     // ráugrik
            .then(function (m) {
                if (m === 'meggondolta' || sajat !== megszakit) { kotelKi(); return 'meggondolta'; }
                return Promise.resolve()
                    .then(function () {
                        var y0 = P.y, ut = y0 - (lp.y + MAGAS() * 1.1), meggondolta = false;
                        P.arnyek = 0;
                        return anim({feny: .5}, Math.min(2800, 600 + ut * 5), 'lin', function (u) {
                            if (meggondolta) { return; }
                            if (sajat !== megszakit && u < .85) { meggondolta = true; return; }
                            P.y = y0 - ut * u; maszik(u, 2 + ut / 40); kotelRajz(lp.x, fent, P.y + 8);
                        }).then(function () {
                            if (meggondolta) {                                       // félúton „jé, megint csinál valamit!”
                                return jel('!', true).then(function () { return var_(400); })
                                    .then(function () { return jel('!', false); })
                                    .then(function () { var cel = most(); var y1 = P.y, ut2 = (cel ? cel.y : y0) - y1;
                                        return anim({}, Math.min(2000, 400 + Math.abs(ut2) * 3), 'lin', function (u) { P.y = y1 + ut2 * u; maszik(u, 4); kotelRajz(lp.x, fent, P.y + 8); }); })
                                    .then(function () { P.arnyek = 1; P.emel = 0; legyen('alap'); return anim(Object.assign({}, NYUGI), 300, 'rugo'); })
                                    .then(function () { return anim({}, 350, 'be', function (u) { kotelRajz(lp.x, fent, P.y - (P.y - fent) * u); }); })
                                    .then(function () { kotelKi(); return menj(null); })
                                    .then(function () { return 'meggondolta'; });
                            }
                            return anim({meret: .4, lat: 0}, 380, 'be', function (u) { P.y = P.y - u * 4; })      // be a logóba
                                .then(function () { kotelKi(); kint = false; logoAllapot(true); return 'bent'; });
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
            var p = n.parentElement; if (!p || p.closest('#lumi, script, style, noscript, .navbar, header')) { return NodeFilter.FILTER_REJECT; }
            return NodeFilter.FILTER_ACCEPT; }});
        var rg = D.createRange(), n;
        while ((n = w.nextNode())) { rg.selectNodeContents(n); [].forEach.call(rg.getClientRects(), function (r) { tesz(r, 'szoveg'); }); }
        D.querySelectorAll('button, img, video, canvas, select, textarea, input, .password-toggle, a.fp-gomb, [role=button]').forEach(function (e) {
            if (e.closest('#lumi, .navbar, header') || e.type === 'hidden') { return; }
            var cs = getComputedStyle(e); if (cs.visibility === 'hidden' || cs.display === 'none' || +cs.opacity < .2) { return; }
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
    function takaras(d, sajatMezo) {          // fix238: MENNYI szöveget/elemet takarna (terület, px²)
        var a = akadalyGyujt(), ossz = 0;
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
    function felulet(el) { var p = lap(el); return {l: p.x, r: p.x + p.w, y: p.y, w: p.w}; }
    /* fix238 (Sándor: „ne oldalt a levegőben – találja meg a helyet, ahol nem takar”): mindig VALÓDI felületen
       marad. Sorrend: állva semmit nem takar → ülve (a lába a mező üres részén) semmit nem takar → ahol a
       legkevesebbet takarná. Kötélen oldalt már nem lóg. */
    function keres(feluletek, sajatMezo) {
        var h = MAGAS(), fel = h * .28, lx = scrollX + 6, rx = scrollX + innerWidth - 6, legjobb = null;
        for (var mod = 0; mod < 2; mod++) {
            for (var i = 0; i < feluletek.length; i++) {
                var f = feluletek[i]; if (!f || f.w < h * .6) { continue; }
                var bal = Math.max(f.l + fel, lx + fel), jobb = Math.min(f.r - fel, rx - fel);
                for (var x = jobb; x >= bal; x -= 8) {
                    var t = takaras(dobozom(x, f.y + 1, mod === 1), sajatMezo) + (jobb - x) * .01 + i * 50;
                    if (t < 1 + (jobb - x) * .01 + i * 50) { return {x: x, y: f.y + 1, ul: mod === 1}; }
                    if (!legjobb || t < legjobb.t) { legjobb = {x: x, y: f.y + 1, ul: mod === 1, t: t}; }
                }
            }
        }
        return legjobb;
    }
    function kartyaja(el) { return el.closest('.fp-kartya, .auth-card, .doboz, .card, details, form, main section') || el.parentElement; }
    function kotelHely(el) {                     // nincs szabad felület: a doboz mellett, a margón lóg a kötélen
        var k = lap(kartyaja(el) || el), m = lap(el), h = MAGAS(), y = m.y + m.h * .5 + h * .55;
        if (k.x + k.w + h * .45 < scrollX + innerWidth - 4) { return {x: k.x + k.w + h * .3, y: y, kotel: true}; }
        if (k.x - h * .45 > scrollX + 4) { return {x: k.x - h * .3, y: y, kotel: true}; }
        return {x: scrollX + innerWidth - h * .2, y: y, kotel: true};  // keskeny telefonon: a képernyő jobb szélén kukucskál be, a margón lóg
    }
    function helyMezo(m) {
        var c = m.closest('.password-field, .input-group') || m;
        if (m.type === 'checkbox' || m.type === 'radio') { c = m.closest('label, .field') || m; }
        var mezo = m.matches('input, textarea, select') && m.type !== 'checkbox' ? m : null;
        // csak a mező közelében keres (a doboz tetejére nem ugrik el – ott messze lenne attól, amit csinálsz)
        return keres([felulet(c), m.closest('.field') && felulet(m.closest('.field'))], mezo) || {x: lap(c).x + lap(c).w - MAGAS() * .4, y: lap(c).y + 1};
    }
    function helyDoboz(el) { return keres([felulet(el), kartyaja(el) && kartyaja(el) !== el && felulet(kartyaja(el))], null) || {x: lap(el).x + lap(el).w * .62, y: lap(el).y + 2}; }
    function ulhet() {                           // leülhet-e ott, ahol áll (a lába se takarjon szöveget)
        return horgony && !utkozik(dobozom(P.x, P.y, true), horgony.matches && horgony.matches('input, textarea') ? horgony : null);
    }
    function fodoboz() {
        var jel_ = ['.fp-kartya', '.auth-card', '.doboz', 'details.fp-k', '.fp-k', '.cs-lap', '.card', 'main section', 'main', '.content'];
        for (var i = 0; i < jel_.length; i++) {
            var t = D.querySelectorAll(jel_[i]);
            for (var j = 0; j < t.length; j++) {
                var r = t[j].getBoundingClientRect();
                if (r.width > 220 && r.height > 60 && r.top > 70 && r.top < innerHeight - 100) { return t[j]; }
            }
        }
        return null;
    }
    var horgony = null;
    function most() {
        if (!horgony) { return null; }
        return horgony.matches && horgony.matches('input, select, textarea') ? helyMezo(horgony) : helyDoboz(horgony);
    }
    function lathato(y) { return y > scrollY + 50 && y < scrollY + innerHeight - 10; }
    var lognak = null;                          // {x, ky}: épp kötélen lóg (nincs szabad felület)
    function menj(hely, csak) {
        hely = hely || most();
        if (!hely) { return Promise.resolve(); }
        var volt = lognak, h = MAGAS();
        if (volt && hely.kotel && Math.abs(hely.x - volt.x) < 4) {      // ugyanazon a kötélen csúszik
            var y0 = P.y;
            return anim({}, 450, 'bk', function (u, e) { P.y = y0 + (hely.y - y0) * e; maszik(u, 3); lognak.ky = P.y - h * .62; kotelRajz(volt.x, 0, lognak.ky); });
        }
        lognak = null;
        var elotte = Promise.resolve();
        if (hely.kotel) {                                               // előbb leengedi a kötelet, aztán ráugrik
            kotelBe(); elotte = anim({}, 320, 'ki', function (u, e) { kotelRajz(hely.x, 0, (hely.y - h * .62) * e); });
        }
        return elotte.then(function () {
            var ut;
            if (!csak && (!lathato(P.y) || !lathato(hely.y))) {
                ut = anim({lat: 0}, 160).then(function () { P.x = hely.x; P.y = hely.y; Object.assign(P, NYUGI); return anim({lat: 1}, 260); });
            } else {
                var tav = Math.hypot(hely.x - P.x, hely.y - P.y);
                ut = tav < 6 ? Promise.resolve() : ugras(hely.x, hely.y, Math.max(h * .3, (P.y - hely.y) + h * .35), Math.min(700, 340 + tav * .5));
            }
            if (volt && !hely.kotel) {                                   // a régi kötél felszalad
                var ky = volt.ky;
                ut = Promise.all([ut, var_(150).then(function () { return anim({}, 380, 'be', function (u) { kotelRajz(volt.x, 0, ky * (1 - u)); }); })])
                    .then(function () { kotelKi(); });
            }
            return ut;
        }).then(function () {
            if (hely.kotel) { legyen('maszik'); P.arnyek = 0; lognak = {x: hely.x, ky: P.y - h * .62}; kotelRajz(hely.x, 0, lognak.ky); rajzol(); }
            else { P.arnyek = 1; if (hely.ul && P.kep === 'alap') { return ul(); } }
        });
    }

    // ── EGYÜTT ÉL VELÜNK: ha hozzáérsz, odébb ugrik ───────────────────────
    var csikiIdo = 0;
    function csiki(ev) {
        if (!kint || performance.now() - csikiIdo < 900) { return; }
        csikiIdo = performance.now();
        var ex = (ev && ev.pageX) || P.x, irany = ex < P.x ? 1 : -1, tav = MAGAS() * .75;
        // fix231: a helyén marad – mezőn a mező szélén belül ugrik odébb, nem a levegőbe
        var hat = horgony ? lap(horgony.closest && horgony.closest('.password-field, .field, details, .fp-kartya') || horgony) : {x: scrollX + 30, w: innerWidth - 60};
        var balSz = Math.max(scrollX + 30, hat.x + 34), jobbSz = Math.min(scrollX + innerWidth - 30, hat.x + hat.w - 34);
        if (P.x + irany * tav > jobbSz || P.x + irany * tav < balSz) { irany = -irany; }
        tav = Math.max(20, Math.min(tav, irany > 0 ? jobbSz - P.x : P.x - balSz));
        megszakit++; utolsoMozdulat = Date.now();
        tedd(function () {
            return jel('!', true).then(function () { return ugras(P.x + irany * tav, P.y, MAGAS() * .35, 330); })
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
    function indul() {
        D.body.appendChild(doboz);
        var cel = fodoboz();
        if (!cel) { return; }
        horgony = cel;
        var h = helyDoboz(cel);
        // ha van űrlap, egyenesen az első mezőre ugrik (a doboz tetején a fölötte lévő szöveget takarná)
        var elso = [].slice.call(D.querySelectorAll('main form input, .fp form input, .content form input')).filter(function (m) {
            var r = m.getBoundingClientRect(); return m.type !== 'hidden' && m.offsetParent && r.width > 120 && r.left >= 0 && r.right <= innerWidth && r.top > 80 && r.bottom < innerHeight - 20; })[0];
        if (elso) { horgony = elso; h = helyMezo(elso); }
        tedd(function () { return var_(400).then(function () { return kijon({y: h.y, hely2: h}); }); });
        D.querySelectorAll('main form, .content form, .fp form').forEach(function (f) { if (!f.closest('header, nav')) { urlap(f); } });
        D.querySelectorAll('details').forEach(function (d) {
            d.addEventListener('toggle', function () {
                if (!d.open) { return; }
                var s = d.querySelector('summary') || d;
                if (tevekeny(s)) { return; }
                if (fut < 2) { tedd(function () { return menj(helyDoboz(s)).then(gondolkodik).then(aha); }); }
            });
        });
        var gIdo = null;
        addEventListener('scroll', function () {
            clearTimeout(gIdo);
            gIdo = setTimeout(function () {
                if (!kint || fut || lathato(P.y)) { return; }
                var uj = fodoboz(); if (uj) { horgony = uj; tedd(function () { return menj(helyDoboz(uj)); }); }
            }, 450);
        }, {passive: true});
        addEventListener('resize', function () { if (kint && !fut && horgony) { var m2 = most(); P.x = m2.x; P.y = m2.y; rajzol(); } });
        // ha sokáig nem csinálsz semmit, visszamászik a logóba
        setInterval(function () {
            if (!kint || fut || D.hidden) { return; }
            var tetlen = Date.now() - utolsoMozdulat;
            if (tetlen > 40000) { tedd(visszamaszik); return; }
            // fix231: ha egy mezőn áll, és egy ideje nem történik semmi, leül a mező szélére
            if (tetlen > 5000 && P.kep === 'alap' && !lognak && horgony && horgony.matches && horgony.matches('input, select, textarea')
                && jo(horgony) && ulhet()) { tedd(ul); return; }                   // fix237: csak ha a mező jó, és a lába se takar szöveget
            if (tetlen > 9000 && Math.random() < .35 && lathato(P.y)) {
                tedd(Math.random() < .5 ? integet : function () { return anim({fej: 12}, 500).then(function () { return var_(600); }).then(function () { return anim({fej: -10}, 700); }).then(function () { return alap(500); }); });
            }
        }, 4000);
        ['pointerdown', 'keydown'].forEach(function (t) { addEventListener(t, function () { utolsoMozdulat = Date.now(); megszakit++; }, true); });
        // pihenés: lélegzik, a fény pislákol
        var t0 = performance.now();
        (function el(t) {
            if (kint && !fut && P.lat > .9) {
                var s = (t - t0) / 1000; P.ny = 1 + Math.sin(s * 2.2) * .012;
                /* fix234: ha az oldal elmozdul alatta (pl. megjelenik a jelszó-csík, és lejjebb csúsznak a mezők),
                   vele megy – mindig a mező vonalán marad */
                if (horgony && (P.kep === 'alap' || P.kep === 'ul' || lognak) && t - (el.utolso || 0) > 400) {
                    el.utolso = t; var h0 = most();
                    if (h0) {
                        var dx = Math.abs(h0.x - P.x), dy = Math.abs(h0.y - P.y);
                        if (!!h0.kotel !== !!lognak || dx > 30) { tedd(function () { return menj(most()); }); }      // fix237: új szabad hely → odaugrik
                        else if (h0.ul && P.kep === 'alap') { tedd(ul); }                                                 // fix238: ott csak ülve fér el
                        else if (!h0.ul && P.kep === 'ul' && takaras(dobozom(P.x, P.y, false), null) < 1) { legyen('alap'); }
                        else if (dx > 1 || dy > 1) { P.x = h0.x; P.y = h0.y; if (lognak) { lognak.ky = P.y - MAGAS() * .62; kotelRajz(lognak.x, 0, lognak.ky); } }
                    }
                }
                rajzol();
            }
            requestAnimationFrame(el);
        })(t0);
    }
    window.__lumi = {poz: function (o) { Object.assign(P, o); rajzol(); }, orul: function () { return tedd(function () { return orul(true); }); }, gondolkodik: function () { return tedd(gondolkodik); },
        integet: function () { return tedd(integet); }, aha: function () { return tedd(aha); }, vissza: function () { return tedd(visszamaszik); }};
    if (D.readyState === 'loading') { D.addEventListener('DOMContentLoaded', function () { setTimeout(indul, 600); }); } else { setTimeout(indul, 600); }
})();
