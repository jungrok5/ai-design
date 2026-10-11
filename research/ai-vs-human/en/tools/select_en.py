"""Pick human English docs and build paired prompts (same design as the Korean select.py)."""
import json, pathlib, random, re, sys
G = pathlib.Path(sys.argv[1]).resolve(); H = G / "human"
KIND = {"react.dev": "a page of the official React documentation", "es-toolkit": "a page of the API reference of a JavaScript utility library",
        "mdn-content": "a page of the MDN Web Docs"}
def prose(t):
    t = re.sub(r"^---\n.*?\n---\n", "", t, flags=re.S); t = re.sub(r"```.*?```", "", t, flags=re.S); t = re.sub(r"`[^`\n]*`", "", t)
    t = re.sub(r"<[^>]+>", "", t); t = re.sub(r"\{\{[^}]*\}\}", "", t); return re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
def title(t, p):
    m = re.search(r"^title:\s*['\"]?(.+?)['\"]?\s*$", t, re.M) or re.search(r"^#\s+(.+)$", t, re.M)
    return re.sub(r"<[^>]+>", "", (m.group(1).strip() if m else p.stem)).strip("# ").strip()
rng = random.Random(42); pairs = []; models = ["claude-opus-5-5", "claude-sonnet-5-5", "claude-haiku-5-5"]
for repo, kind in KIND.items():
    cands = []
    for p in sorted((H / repo).rglob("*.md")):
        if ".git" in p.parts: continue
        t = p.read_text(encoding="utf-8", errors="replace"); words = len(re.findall(r"[A-Za-z]{2,}", prose(t)))
        if words >= 250: cands.append((p, t, words))
    pick = rng.sample(cands, min(32, len(cands)))
    for i, (p, t, w) in enumerate(pick):
        pairs.append(dict(id=f"{repo[:6]}-{i:02d}", repo=repo, path=str(p.relative_to(H)), title=title(t, p), kind=kind,
                          words=max(250, min(900, w)), split="test" if i % 5 == 4 else "train", model=models[len(pairs) % 3]))
    print(repo, len(cands), "candidates ->", len(pick))
(G / "pairs.json").write_text(json.dumps(pairs, ensure_ascii=False, indent=1)); print("pairs", len(pairs))
