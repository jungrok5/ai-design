"""Write splits.json for the English corpus: all qualifying human docs (hash split on repo-relative path) + generated AI docs."""
import hashlib, json, pathlib, re, sys
G = pathlib.Path(sys.argv[1]).resolve(); H = G / "human"
def prose(t):
    t = re.sub(r"^---\n.*?\n---\n", "", t, flags=re.S); t = re.sub(r"```.*?```", "", t, flags=re.S); return re.sub(r"<[^>]+>|\{\{[^}]*\}\}", "", t)
hum = []
for repo in ("react.dev", "es-toolkit", "mdn-content"):
    for p in sorted((H / repo).rglob("*.md")):
        if ".git" in p.parts: continue
        if len(re.findall(r"[A-Za-z]{2,}", prose(p.read_text(encoding="utf-8", errors="replace")))) < 250: continue
        rel = str(p.relative_to(H)); split = "test" if int(hashlib.md5(rel.encode()).hexdigest(), 16) % 5 == 0 else "train"
        hum.append(dict(repo=repo, path=str(p), split=split))
pairs = json.load(open(G / "pairs.json"))
ai = [dict(repo=x["repo"], path=str(G / "ai" / f"{x['id']}.md"), split=x["split"], model=x["model"]) for x in pairs if (G / "ai" / f"{x['id']}.md").exists()]
json.dump({"human": hum, "ai": ai}, open(G / "splits.json", "w"), indent=0)
print("human", len(hum), sum(d["split"] == "test" for d in hum), "test; ai", len(ai), sum(d["split"] == "test" for d in ai), "test")
