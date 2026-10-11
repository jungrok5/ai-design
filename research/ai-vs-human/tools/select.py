"""Pick human Korean docs and build paired prompts. Output: pairs.json [{id, repo, path, title, kind, chars, split, model}]."""
import json, pathlib, random, re, sys
G = pathlib.Path(sys.argv[1]).resolve(); H = G / "human"
KIND = {"ko.react.dev": "React 공식 문서의 한 페이지", "es-toolkit": "JavaScript 유틸리티 라이브러리의 API 문서 한 페이지",
        "fe-news": "프론트엔드 개발 소식을 모아 소개하는 월간 뉴스레터 한 호", "tech-interview-for-developer": "개발자 기술 면접 대비 정리 노트",
        "translated-content": "MDN 웹 문서의 한 페이지"}
def prose(t):
    t = re.sub(r"^---\n.*?\n---\n", "", t, flags=re.S)
    t = re.sub(r"```.*?```", "", t, flags=re.S); t = re.sub(r"`[^`\n]*`", "", t)
    t = re.sub(r"<[^>]+>", "", t); t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
    return t
def title(t, p):
    m = re.search(r"^title:\s*['\"]?(.+?)['\"]?\s*$", t, re.M) or re.search(r"^#\s+(.+)$", t, re.M)
    return re.sub(r"<[^>]+>", "", (m.group(1).strip() if m else p.stem)).strip("# ").strip()
rng = random.Random(42); pairs = []; models = ["claude-opus-5-5", "claude-sonnet-5-5", "claude-haiku-5-5"]
for repo, kind in KIND.items():
    cands = []
    for p in sorted((H / repo).rglob("*.md")):
        if ".git" in p.parts: continue
        t = p.read_text(encoding="utf-8", errors="replace"); pr = prose(t)
        han = len(re.findall(r"[가-힣]", pr))
        if han < 400 or han / max(1, len(re.sub(r"\s", "", pr))) < 0.3: continue
        cands.append((p, t, len(pr)))
    pick = rng.sample(cands, min(40, len(cands)))
    for i, (p, t, n) in enumerate(pick):
        pairs.append(dict(id=f"{repo[:6]}-{i:02d}", repo=repo, path=str(p.relative_to(H)), title=title(t, p), kind=kind,
                          chars=max(800, min(3000, n)), split="test" if i % 5 == 4 else "train", model=models[len(pairs) % 3]))
    print(repo, len(cands), "candidates ->", len(pick))
(G / "pairs.json").write_text(json.dumps(pairs, ensure_ascii=False, indent=1))
print("pairs", len(pairs)); [print(" ", x["id"], x["model"], x["title"][:50]) for x in pairs[::23]]
