import re, sys
fajl, *kulcsok = sys.argv[1:]
t = open(fajl, encoding="utf-8").read()
ki = []
for k in kulcsok:
    s = re.search(r'<section class="lap" id="%s">.*?</section>' % k, t, re.S)
    ki.append(f"===== {k} HTML =====\n" + (s.group(0) if s else "NINCS"))
    # a hozzá tartozó (function () { ... })(); blokk: amelyikben $("k-...") szerepel
    for b in re.finditer(r'/\*[^\n]*\*/\s*\(function \(\) \{.*?\n  \}\)\(\);', t, re.S):
        if f'"{k}-' in b.group(0) or f"'{k}-" in b.group(0):
            ki.append(f"===== {k} JS =====\n" + b.group(0))
            break
open("_kivonat.txt", "w", encoding="utf-8").write("\n".join(ki))
print(len("\n".join(ki)))
