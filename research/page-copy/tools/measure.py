"""Count the docs a candidate regex reports, the way style_check.py applies a rule: human Korean (or English) Markdown,
Claude-written tech docs, and the generated pages in out/.
usage: measure.py CANDIDATES.py [--en] [--show N]   (CANDIDATES.py defines C = {id: pattern or (pattern, {max_per_file: n})})"""
import glob, importlib.util, pathlib, re, sys
HERE = pathlib.Path(__file__).resolve().parents[1]; REPO = HERE.parents[1]; G = HERE.parent / "ai-vs-human"
spec = importlib.util.spec_from_file_location("sc", REPO / "plugins/ai-design/style/style_check.py")
sc = importlib.util.module_from_spec(spec); sys.modules["sc"] = sc; spec.loader.exec_module(sc)
load = lambda paths: [(p, pathlib.Path(p).read_text(encoding="utf-8", errors="replace")) for p in paths]
LANG = "en" if "--en" in sys.argv else "ko"
if LANG == "en":
    human, ai = load(glob.glob(str(G / "en/human/**/*.md"), recursive=True)), load(glob.glob(str(G / "en/ai/*.md")))
else:
    human = [d for d in load(glob.glob(str(G / "human/**/*.md"), recursive=True)) if re.search("[가-힣]", d[1][:4000])]
    ai = load(glob.glob(str(G / "ai/*.md")))
pages = load(glob.glob(str(HERE / "out/*/*.html")) + glob.glob(str(HERE / "out/*/*.md")))
ns = {}; exec(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"), ns)
show = int(sys.argv[sys.argv.index("--show") + 1]) if "--show" in sys.argv else 3
print(f"human {len(human)} docs, AI tech {len(ai)}, pages {len(pages)}")
for cid, spec_ in ns["C"].items():
    pat, kw = (spec_, {}) if isinstance(spec_, str) else spec_
    rule = sc.Rule(id=cid, kind="prose", lang=LANG, severity="warning", pattern=re.compile(pat, re.I if LANG == "en" else 0), message="", **kw)
    hit = lambda docs: [(p, f[0]) for p, t in docs for f in [sc.check_text(pathlib.Path(p), t, [rule])] if f]
    h, a, s = hit(human), hit(ai), hit(pages)
    print(f"{cid:<26} human {len(h):4d}  ai-tech {len(a):3d}  pages {len(s):2d}")
    for p, f in h[:show]:
        print(f"   human {p.split('/human/')[-1]}:{f['line']} {f['match']!r}")
