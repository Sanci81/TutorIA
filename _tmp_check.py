import sys, io, json, pathlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, '.')
import curriculum_loader as cl

ok_all = True

def check_union_no_dup(per_grade: dict, original_names: list[str], label: str):
    global ok_all
    # flatten in grade order
    flat = []
    for g in sorted(per_grade):
        flat.extend(per_grade[g])
    # overlap check
    seen = {}
    overlaps = []
    for g in sorted(per_grade):
        for n in per_grade[g]:
            if n in seen:
                overlaps.append((n, seen[n], g))
            seen[n] = g
    union_ok = flat == original_names
    dup_ok = len(overlaps) == 0
    count_ok = len(flat) == len(original_names)
    print(f"[{label}] union==original: {union_ok} | no duplicates: {dup_ok} | counts: {len(flat)}/{len(original_names)}")
    if overlaps:
        print("   OVERLAPS:", overlaps)
    if not union_ok:
        print("   ORDER/SET MISMATCH")
    if not (union_ok and dup_ok and count_ok):
        ok_all = False

# ── HU Matematika 5-8 (chat path, as the app uses it) ──
hu_path = pathlib.Path('hu_kerettanterv_5_8_TELJES/matematika_5-8.json')
hu_data = json.loads(hu_path.read_text(encoding='utf-8'))
hu_blocks = hu_data['evfolyam_blokkok']

print("=== HU Matematika (via get_curriculum_for_chat) ===")
hu_per_grade = {}
for g in (5, 6, 7, 8):
    res = cl.get_curriculum_for_chat("Matematika", g)
    cat = res.get("topic_catalog") or []
    hu_per_grade[g] = [c['name'] for c in cat]
    print(f"  grade {g}: file={res.get('file')} count={len(cat)} first={cat[0]['name'] if cat else '-'}")

# union per block: 5-6 block and 7-8 block separately
b56 = [t['nev'] for t in hu_blocks['5-6']['temakorok']]
b78 = [t['nev'] for t in hu_blocks['7-8']['temakorok']]
check_union_no_dup({5: hu_per_grade[5], 6: hu_per_grade[6]}, b56, "HU blokk 5-6")
check_union_no_dup({7: hu_per_grade[7], 8: hu_per_grade[8]}, b78, "HU blokk 7-8")

print()
print("=== ES Matemáticas (via get_curriculum_for_chat) ===")
es_path = pathlib.Path('es_kerettanterv/es_LOMLOE_Matematicas_1-6.json')
es_data = json.loads(es_path.read_text(encoding='utf-8'))
es_per_grade = {}
for g in (1, 2, 3, 4, 5, 6):
    res = cl.get_curriculum_for_chat("matematicas", g)
    cat = res.get("topic_catalog") or []
    es_per_grade[g] = [c['name'] for c in cat]
    print(f"  grade {g}: file={res.get('file')} count={len(cat)} first={cat[0]['name'] if cat else '-'}")

for cyc, grades in (("1_ciclo", (1, 2)), ("2_ciclo", (3, 4)), ("3_ciclo", (5, 6))):
    orig = [t['nev'] for t in es_data['ciklusok'][cyc]['temakorok']]
    check_union_no_dup({g: es_per_grade[g] for g in grades}, orig, f"ES {cyc}")

print()
print("ALL CHECKS PASSED" if ok_all else "!!! SOME CHECKS FAILED")
