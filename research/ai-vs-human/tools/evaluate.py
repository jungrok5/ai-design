"""Run the real style_check.py on held-out docs. usage: evaluate.py G RULESDIR [split]
RULESDIR may hold .style/rules.toml with extra rules (the checker's project override). Prints, per rule,
how many AI and human docs it fires in, and the share of docs with any finding."""
import collections, json, pathlib, subprocess, sys
G, RD = pathlib.Path(sys.argv[1]).resolve(), pathlib.Path(sys.argv[2]).resolve(); split = sys.argv[3] if len(sys.argv) > 3 else "test"
CHECK = str(pathlib.Path(__file__).resolve().parents[3] / "plugins/ai-design/style/style_check.py")
sp = json.load(open(G / "splits.json"))
def run(paths):
    hits = collections.defaultdict(set)
    for i in range(0, len(paths), 100):
        r = subprocess.run([sys.executable, CHECK, "--format", "json", *paths[i:i + 100]], cwd=RD, capture_output=True, text=True)
        try: data = json.loads(r.stdout or "[]")
        except json.JSONDecodeError: sys.exit("bad json: " + r.stdout[:300] + r.stderr[:300])
        for f in (data if isinstance(data, list) else data.get("findings", [])):
            hits[f["rule"]].add(f["file"])
    return hits
ai = [d["path"] for d in sp["ai"] if d["split"] == split]; hu = [d["path"] for d in sp["human"] if d["split"] == split]
ha, hh = run(ai), run(hu)
print(f"{split}: AI {len(ai)} docs, human {len(hu)} docs   (rule: AI docs hit / human docs hit)")
for rule in sorted(set(ha) | set(hh), key=lambda r: -len(ha.get(r, ()))):
    a, h = len(ha.get(rule, ())), len(hh.get(rule, ()))
    print(f"  {rule:<26} AI {a:3d} ({100*a/len(ai):4.0f}%)   human {h:3d} ({100*h/len(hu):4.1f}%)")
REG = {"ko-haeyo", "ko-register-mix"}
anyA = set().union(*[v for k, v in ha.items() if k not in REG]) if ha else set()
anyH = set().union(*[v for k, v in hh.items() if k not in REG]) if hh else set()
print(f"  any finding (excl. register rules): AI {len(anyA)}/{len(ai)} = {100*len(anyA)/len(ai):.0f}%   human {len(anyH)}/{len(hu)} = {100*len(anyH)/len(hu):.0f}%")
json.dump({"ai": {k: sorted(v) for k, v in ha.items()}, "human": {k: sorted(v) for k, v in hh.items()}},
          open(G / f"eval-{RD.name}-{split}.json", "w"), ensure_ascii=False)
