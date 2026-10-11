"""Combine evaluate.py outputs: how many AI vs human docs the four comparison rules flag, per split and per model."""
import json, pathlib, sys
G = pathlib.Path(sys.argv[1]).resolve(); tag = sys.argv[2] if len(sys.argv) > 2 else "rules-repo"
sp = json.load(open(G / "splits.json")); new = ["ko-advise", "ko-template-heading", "ko-count-runup", "ko-hedged-advice"]
for split in ("train", "test"):
    e = json.load(open(G / f"eval-{tag}-{split}.json"))
    na = sum(d["split"] == split for d in sp["ai"]); nh = sum(d["split"] == split for d in sp["human"])
    for label, rules in (("4 new rules", new), ("4 new + ko-emoji-marker", new + ["ko-emoji-marker"])):
        a = set().union(*[set(e["ai"].get(r, [])) for r in rules]); h = set().union(*[set(e["human"].get(r, [])) for r in rules])
        print(f"{split:5} {label:<26} AI {len(a)}/{na} = {100*len(a)/na:.0f}%   human {len(h)}/{nh} = {100*len(h)/nh:.1f}%")
    by = {}
    for d in sp["ai"]:
        if d["split"] != split: continue
        m = d["model"].split("-")[1]; by.setdefault(m, [0, 0]); by[m][1] += 1
        by[m][0] += any(d["path"] in e["ai"].get(r, []) for r in new)
    print(f"{split:5} per model (4 new rules): " + ", ".join(f"{k} {v[0]}/{v[1]}" for k, v in sorted(by.items())))
