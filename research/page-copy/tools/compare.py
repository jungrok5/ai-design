"""Docs with at least one writing finding (register rules and ui-* excluded) under two checkers.
usage: compare.py OLD_STYLE_CHECK NEW_STYLE_CHECK
Needs research/ai-vs-human/fetch-human.sh and en/fetch-human.sh to have been run."""
import collections, glob, json, pathlib, subprocess, sys
HERE = pathlib.Path(__file__).resolve().parents[1]; G = HERE.parent / "ai-vs-human"
pages = lambda d: sorted(glob.glob(str(HERE / d / "*/*.html")) + glob.glob(str(HERE / d / "*/*.md")))
sets = {"human-ko": glob.glob(str(G / "human/**/*.md"), recursive=True), "human-en": glob.glob(str(G / "en/human/**/*.md"), recursive=True),
        "ai-tech-ko": glob.glob(str(G / "ai/*.md")), "pages-no-plugin": pages("out"),
        "pages-1.6.1-plugin": pages("gen-1.6.1"), "pages-1.7.0-plugin": pages("gen-1.7.0")}
REG = {"ko-haeyo", "ko-register-mix"}
def run(check, files):
    hits = collections.defaultdict(set)
    for i in range(0, len(files), 200):
        r = subprocess.run([sys.executable, str(pathlib.Path(check).resolve()), "--format", "json", *files[i:i + 200]],
                           capture_output=True, text=True, cwd="/")
        for f in json.loads(r.stdout or "[]"):
            if f["rule"] not in REG and not f["rule"].startswith("ui-"):
                hits[f["file"]].add(f["rule"])
    return hits
for name, files in sets.items():
    if not files:
        continue
    o, n = run(sys.argv[1], files), run(sys.argv[2], files)
    added = collections.Counter(r for f in n for r in n[f] - o.get(f, set()))
    print(f"{name:20} docs {len(files):5}  old {len(o):4}  new {len(n):4}  rules newly reporting a doc: {dict(added.most_common(10))}")
