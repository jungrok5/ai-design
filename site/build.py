"""Build _site/ for GitHub Pages: the page, the design system files it loads, and the real checker output.

The page source (site/index.html) has placeholders that are filled here, so nothing on the page is typed by hand:
  <!--SAMPLE:path-->  a file under site/samples/ (escaped), e.g. <!--SAMPLE:claude/notice-with.md-->
  <!--RAW:path-->     the sample as live markup (only for samples built from Clear components)
  <!--OUTPUT:path-->  what style_check.py printed for that sample, run now, plus its exit code (path without suffix)
  <!--COUNT:all|ko|en|any|ui-->  number of rules from --list-rules
  <!--VERSION-->      the plugin version
  <!--REV-->          the commit recorded for the newest version in CHANGELOG.md (the same rev the README pins),
                      or the commit being built when that version has no commit yet
  <!--JSONLD-->       WebSite, SoftwareSourceCode and author markup, plus FAQPage built from the visible #faq list
  <!--OGV-->          short hash of site/img/og.png, so chat apps refetch the share image when it changes
site/img/ is copied as is; sitemap.xml is written next to the page.
og.png is rendered from site/og/card.html (see site/og/render.mjs) and committed.
"""
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECK = ROOT / "plugins/ai-design/style/style_check.py"
DESIGN = ROOT / "plugins/ai-design/skills/polish-ui/design"
SAMPLES = ROOT / "site/samples"
OUT = ROOT / "_site"


def run_sample(name: str) -> str:
    r = subprocess.run([sys.executable, str(CHECK), name], cwd=SAMPLES, capture_output=True, text=True)
    lines = []
    for line in (r.stdout + r.stderr).splitlines():
        cls = "ds-err" if " error [" in line else "ds-warn" if " warning [" in line else "ds-prompt"
        loc = re.match(r"^(\S+:\d+:\d+) (.*)$", line)  # gray file:line:col, colored finding
        body = f'<span class="ds-prompt">{html.escape(loc.group(1))}</span> {html.escape(loc.group(2))}' if loc else html.escape(line)
        lines.append(f'<span class="{cls}">{body}</span>')
    lines.append(f'<span class="ds-prompt">exit {r.returncode}</span>')
    return "\n".join(lines)


def rule_counts() -> dict:
    rows = subprocess.run([sys.executable, str(CHECK), "--list-rules"], capture_output=True, text=True).stdout.splitlines()
    rows = [r.split() for r in rows if r.strip()]
    kinds = [(r[1], r[2]) for r in rows]
    return {"all": len(rows), "ko": sum(lang == "ko" for _, lang in kinds), "en": sum(lang == "en" for _, lang in kinds),
            "any": sum(kind == "prose" and lang == "any" for kind, lang in kinds), "ui": sum(kind == "markup" for kind, _ in kinds)}


def released_rev() -> str:
    """Full SHA of the newest CHANGELOG entry, so the page, README and CHANGELOG pin the same rev (needs full history)."""
    top = re.search(r"^## \d+\.\d+\.\d+.*$", (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"), re.M).group(0)
    m = re.search(r"\(`([0-9a-f]{7,40})`\)", top)
    ref = m.group(1) if m else (os.environ.get("GITHUB_SHA") or "HEAD")
    return subprocess.run(["git", "rev-parse", ref], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()


URL = "https://jungrok5.github.io/ai-design/"


def json_ld(page: str, version: str) -> str:
    """Structured data that only restates what the page shows. The FAQ answers are read from the rendered #faq list."""
    faq = re.search(r'<section[^>]*id="faq".*?</section>', page, re.S).group(0)
    text = lambda h: re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", h))).strip()
    qa = [{"@type": "Question", "name": text(q), "acceptedAnswer": {"@type": "Answer", "text": text(a)}}
          for q, a in re.findall(r"<dt>(.*?)</dt>\s*<dd>(.*?)</dd>", faq, re.S)]
    title = text(re.search(r"<title>(.*?)</title>", page, re.S).group(1))
    desc = html.unescape(re.search(r'<meta name="description" content="([^"]*)"', page).group(1))
    person = {"@type": "Person", "@id": "https://jungrok5.github.io/resume/#person", "name": "오정록 (Jeongrok Oh)",
              "url": "https://jungrok5.github.io/resume/", "sameAs": ["https://github.com/jungrok5", "https://www.linkedin.com/in/jungrok5"]}
    graph = [{"@type": "WebSite", "@id": URL + "#website", "name": "ai-design", "url": URL, "inLanguage": "ko", "author": {"@id": person["@id"]}},
             {"@type": "SoftwareSourceCode", "name": "ai-design", "headline": title, "description": desc, "url": URL,
              "codeRepository": "https://github.com/jungrok5/ai-design", "version": version, "license": "https://opensource.org/licenses/MIT",
              "programmingLanguage": ["Python", "CSS", "JavaScript"], "runtimePlatform": "Claude Code", "inLanguage": "ko",
              "author": {"@id": person["@id"]}, "isPartOf": {"@id": URL + "#website"}},
             {"@type": "FAQPage", "inLanguage": "ko", "mainEntity": qa}, person]
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False) + "</script>"


def main() -> None:
    page = (ROOT / "site/index.html").read_text(encoding="utf-8")
    page = re.sub(r"<!--SAMPLE:([\w./-]+)-->", lambda m: html.escape((SAMPLES / m.group(1)).read_text(encoding="utf-8").rstrip("\n")), page)
    page = re.sub(r"<!--RAW:([\w./-]+)-->", lambda m: (SAMPLES / m.group(1)).read_text(encoding="utf-8"), page)
    names = {str(p.relative_to(SAMPLES).with_suffix("")): str(p.relative_to(SAMPLES)) for p in SAMPLES.rglob("*") if p.is_file()}
    page = re.sub(r"<!--OUTPUT:([\w/-]+)-->", lambda m: run_sample(names[m.group(1)]), page)
    counts = rule_counts()
    page = re.sub(r"<!--COUNT:(\w+)-->", lambda m: str(counts[m.group(1)]), page)
    version = json.loads((ROOT / "plugins/ai-design/.claude-plugin/plugin.json").read_text(encoding="utf-8"))["version"]
    page = page.replace("<!--VERSION-->", version)
    page = page.replace("<!--REV-->", released_rev())
    page = page.replace("<!--OGV-->", hashlib.sha1((ROOT / "site/img/og.png").read_bytes()).hexdigest()[:8])
    page = page.replace("<!--JSONLD-->", json_ld(page, version))
    left = re.findall(r"<!--(SAMPLE|OUTPUT|COUNT|REV|RAW|VERSION|OGV|JSONLD)[^>]*-->", page)
    if left:
        sys.exit(f"build.py: unfilled placeholders {left}")
    shutil.rmtree(OUT, ignore_errors=True)
    (OUT / "design").mkdir(parents=True)
    (OUT / "index.html").write_text(page, encoding="utf-8")
    for f in ("tokens.css", "components.css", "theme.js", "copy.js"):
        shutil.copy(DESIGN / f, OUT / "design" / f)
    shutil.copytree(ROOT / "site/img", OUT / "img")
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n'
                                     '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                     f"  <url><loc>{URL}</loc></url>\n</urlset>\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}/ (rules: {counts})")


if __name__ == "__main__":
    main()
