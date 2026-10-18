"""Count the AI and human docs each candidate regex reports, the way style_check.py applies a rule.

usage: python3 measure.py candidates-ko.json [train|test] [--since 1.6.0]

Needs the comparison corpora (research/ai-vs-human/fetch-human.sh and en/fetch-human.sh) and their splits.json.
A candidate is run as a warning rule on its own (with its max_per_file / max_per_1k), so code blocks, inline code,
link targets and style-ignore lines are skipped exactly as in the checker. Prints, per candidate, the AI and human
docs it reports and the first human lines, so each hit can be read.
"""
import importlib.util, json, pathlib, re, sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
spec = importlib.util.spec_from_file_location("style_check", REPO / "plugins/ai-design/style/style_check.py")
sc = importlib.util.module_from_spec(spec); sys.modules["style_check"] = sc; spec.loader.exec_module(sc)

args = [a for a in sys.argv[1:] if not a.startswith("--")]
since = sys.argv[sys.argv.index("--since") + 1] if "--since" in sys.argv else None
path = pathlib.Path(args[0]); split = args[1] if len(args) > 1 and args[1] in ("train", "test") else "train"
lang = "en" if path.stem.endswith("-en") else "ko"
G = REPO / ("research/ai-vs-human/en" if lang == "en" else "research/ai-vs-human")
sp = json.load(open(G / "splits.json"))
docs = {k: [(d["path"], pathlib.Path(d["path"]).read_text(encoding="utf-8", errors="replace")) for d in sp[k] if d["split"] == split]
        for k in ("ai", "human")}
print(f"{split}: AI {len(docs['ai'])} docs, human {len(docs['human'])} docs")
for c in json.load(open(path)):
    if since and c.get("added_in") != since and not (since == "1.6.0" and "re_measured_1_6_0" in c):
        continue
    pat = c.get("re_measured_1_6_0", {}).get("pattern") if since == "1.6.0" and "re_measured_1_6_0" in c else c.get("pattern")
    if not pat:
        continue
    flags = re.IGNORECASE if lang == "en" and not c.get("case_sensitive") else 0
    rule = sc.Rule(id=c["suggest_id"], kind="prose", lang=lang, severity="warning", pattern=re.compile(pat, flags), message="",
                   max_per_file=int(c.get("max_per_file", 0)), max_per_1k=float(c.get("max_per_1k", 0)))
    found = {k: [(p, f) for p, t in docs[k] for f in sc.check_text(pathlib.Path("x.md"), t, [rule])[:1]] for k in docs}
    print(f"{c['suggest_id']:<28} AI {len(found['ai']):3d}  human {len(found['human']):3d}")
    for p, f in found["human"][:3]:
        print(f"      {p.split('/human/')[-1]}:{f['line']} [{f['match']}]")
