/* korszak HU: kártyák sorrendben a jó helyre (koppintással: kártya, aztán hely) */
function tegyel(w, nev, hely) {
  var c = Array.prototype.filter.call(w.querySelectorAll('.kartyak .kartya'), function (k) { return k.dataset.nev === nev; })[0];
  var r = c.getBoundingClientRect(), h = hely.getBoundingClientRect();
  c.dispatchEvent(new PointerEvent('pointerdown', {bubbles: true, clientX: r.left + 5, clientY: r.top + 5}));
  document.dispatchEvent(new PointerEvent('pointerup', {bubbles: true, clientX: r.left + 5, clientY: r.top + 5}));
  var t = document.elementFromPoint(h.left + h.width / 2, h.top + h.height / 2) || hely;
  t.dispatchEvent(new PointerEvent('pointerup', {bubbles: true, clientX: h.left + h.width / 2, clientY: h.top + h.height / 2}));
}
var hk = W[0].querySelectorAll('.korszakok .hely'); [0, 1, 2, 4, 3].forEach(function (n, i) { tegyel(W[0], String(n), hk[i]); });
kat(W[0].querySelector('.dm-kesz-sor button'));
/* bináris 13 = 8 + 4 + 1 */
var bk = W[3].querySelectorAll('.bk'); kat(bk[1]); kat(W[3].querySelectorAll('.bk')[2]); kat(W[3].querySelectorAll('.bk')[4]); kat(W[3].querySelector('.dm-kesz-sor button'));
