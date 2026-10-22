"""Count the tells listed in tells.tsv that are still in a polished set.
usage: survive.py ORIGINAL_TEXT_DIR POLISHED_TEXT_DIR   (both made by totext.py; a tell counts as left if its exact
words, ignoring spaces, are still on the polished page)"""
import collections, pathlib, re, sys
root = pathlib.Path(__file__).resolve().parents[1]; orig, done = map(pathlib.Path, sys.argv[1:3])
norm = lambda s: re.sub(r"\s+", "", s)
total, left, rows = collections.Counter(), collections.Counter(), []
for line in open(root / "tells.tsv", encoding="utf-8"):
    sid, phrase, cat = line.rstrip("\n").split("\t")
    assert norm(phrase) in norm((orig / f"{sid}.txt").read_text(encoding="utf-8")), (sid, phrase)
    p = done / f"{sid}.txt"
    if not p.exists():
        continue
    total[cat] += 1
    if norm(phrase) in norm(p.read_text(encoding="utf-8")):
        left[cat] += 1; rows.append(f"{sid}\t{phrase}")
print(f"left {sum(left.values())}/{sum(total.values())}")
for c in total:
    print(f"  {c:10} {left[c]}/{total[c]}")
print("\n".join(rows))
