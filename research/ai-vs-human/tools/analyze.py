"""Find phrases far more common in AI-written docs than in human docs on the same topics.

Document frequency (does a doc contain it), not raw counts, so one repetitive doc cannot dominate.
Kept only if: in >= MIN_AI AI train docs, AI rate >= RATIO x human rate (+ smoothing), seen in >= 2 of 3 models
and >= 3 of 5 source topics. Output: candidates.tsv with examples for manual review.
"""
import collections, hashlib, json, math, pathlib, re, sys
G = pathlib.Path(sys.argv[1]).resolve(); H = G / "human"
MIN_AI, RATIO = int(sys.argv[2]) if len(sys.argv) > 2 else 10, float(sys.argv[3]) if len(sys.argv) > 3 else 4.0
pairs = json.load(open(G / "pairs.json"))

def prose(t):
    t = re.sub(r"^---\n.*?\n---\n", "", t, flags=re.S)
    t = re.sub(r"```.*?```", " ", t, flags=re.S); t = re.sub(r"`[^`\n]*`", " CODE ", t)
    t = re.sub(r"<[^>]+>", " ", t); t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t); t = re.sub(r"https?://\S+", " URL ", t)
    t = re.sub(r"^[#>*\-+|\s\d.]+", "", t, flags=re.M)          # markdown line markers
    return t
def sentences(t):
    for line in t.splitlines():
        for s in re.split(r"(?<=[.!?])\s+", line.strip()):
            if re.search(r"[가-힣]", s): yield s.strip()
def feats(t):
    f = set(); ws_all = []
    for s in sentences(prose(t)):
        ws = re.findall(r"[가-힣A-Za-z0-9]+", s)
        ws_all.append(ws)
        for n in (1, 2, 3):
            for i in range(len(ws) - n + 1):
                g = ws[i:i + n]
                if any(re.search(r"[가-힣]", w) for w in g) and not all(re.fullmatch(r"[A-Za-z0-9]+", w) for w in g):
                    f.add("W " + " ".join(g))
        if len(ws) >= 2: f.add("END " + " ".join(ws[-2:]))         # sentence-final phrase
        if ws: f.add("END1 " + ws[-1]); f.add("START " + ws[0])
    return f

def human_docs():
    out = []
    for repo in ["ko.react.dev", "es-toolkit", "fe-news", "tech-interview-for-developer", "translated-content"]:
        for p in sorted((H / repo).rglob("*.md")):
            if ".git" in p.parts: continue
            t = p.read_text(encoding="utf-8", errors="replace"); pr = prose(t)
            if len(re.findall(r"[가-힣]", pr)) < 400: continue
            split = "test" if int(hashlib.md5(str(p.relative_to(H)).encode()).hexdigest(), 16) % 5 == 0 else "train"   # relative: same split wherever the folder is
            out.append(dict(repo=repo, path=str(p), split=split, text=t))
    return out

hum = human_docs()
ai = [dict(repo=x["repo"], path=str(G / "ai" / f"{x['id']}.md"), split=x["split"], model=x["model"],
           text=(G / "ai" / f"{x['id']}.md").read_text(encoding="utf-8")) for x in pairs if (G / "ai" / f"{x['id']}.md").exists()]
json.dump({"human": [{k: v for k, v in d.items() if k != "text"} for d in hum],
           "ai": [{k: v for k, v in d.items() if k != "text"} for d in ai]}, open(G / "splits.json", "w"), ensure_ascii=False, indent=0)
htr = [d for d in hum if d["split"] == "train"]; atr = [d for d in ai if d["split"] == "train"]
hc, ac = collections.Counter(), collections.Counter(); amodel = collections.defaultdict(set); arepo = collections.defaultdict(set)
for d in htr: hc.update(feats(d["text"]))
for d in atr:
    fs = feats(d["text"]); ac.update(fs)
    for f in fs: amodel[f].add(d["model"]); arepo[f].add(d["repo"])
NA, NH = len(atr), len(htr)
rows = []
for f, a in ac.items():
    if a < MIN_AI: continue
    h = hc.get(f, 0); pa, ph = a / NA, (h + 0.5) / (NH + 1)
    if pa / ph < RATIO or len(amodel[f]) < 2 or len(arepo[f]) < 3: continue
    lo = math.log((a + 0.5) / (NA - a + 0.5)) - math.log((h + 0.5) / (NH - h + 0.5))
    rows.append((lo, f, a, h, pa, ph, ",".join(sorted(m.split("-")[1] for m in amodel[f])), len(arepo[f])))
rows.sort(reverse=True)
with open(G / "candidates.tsv", "w") as o:
    o.write("logodds\tfeature\tai_docs\thuman_docs\tai_rate\thuman_rate\tmodels\tsources\n")
    for r in rows: o.write("%.2f\t%s\t%d\t%d\t%.3f\t%.4f\t%s\t%d\n" % r)
print(f"AI train {NA} docs, human train {NH} docs -> {len(rows)} candidates (min_ai={MIN_AI}, ratio>={RATIO})")
for r in rows[:60]: print("%.2f  %-28s ai %3d/%d  human %3d/%d  %s" % (r[0], r[1], r[2], NA, r[3], NH, r[6]))
