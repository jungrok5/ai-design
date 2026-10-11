import json, re, sys, random
G = str(__import__("pathlib").Path(sys.argv[1]).resolve()); sp = json.load(open(G + "/splits.json")); pats = sys.argv[2:]
def show(docs, label, pat, k=5):
    rx = re.compile(pat); out = []
    for d in docs:
        t = open(d["path"], encoding="utf-8", errors="replace").read(); t = re.sub(r"```.*?```", "", t, flags=re.S)
        for line in t.splitlines():
            if rx.search(line): out.append((d.get("model", d["repo"])[:14], line.strip()[:150])); break
    random.Random(1).shuffle(out)
    print(f"  [{label}] {len(out)} docs")
    for m, l in out[:k]: print(f"     {m:<14} {l}")
for p in pats:
    print("==", p)
    show([d for d in sp["ai"] if d["split"] == "train"], "AI", p); show([d for d in sp["human"] if d["split"] == "train"], "human", p, 3)
