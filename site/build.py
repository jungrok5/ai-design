"""Build _site/ for GitHub Pages: the page, the design system files it loads, and the real checker output.

The page source (site/index.html) has placeholders that are filled here, so nothing on the page is typed by hand:
  <!--SAMPLE:path-->  a file under site/samples/ (escaped), e.g. <!--SAMPLE:claude/notice-with.md-->
  <!--RAW:path-->     the sample as live markup (only for samples built from Clear components)
  <!--OUTPUT:path-->  what style_check.py printed for that sample, run now, plus its exit code (path without suffix)
  <!--COUNT:all|ko|en|any|ui-->  number of rules from --list-rules
  <!--VERSION-->      the plugin version
  <!--REV-->          the commit recorded for the newest version in CHANGELOG.md (the same rev the README pins),
                      or the commit being built when that version has no commit yet
site/img/ is copied as is.
"""
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
    left = re.findall(r"<!--(SAMPLE|OUTPUT|COUNT|REV|RAW|VERSION)[^>]*-->", page)
    if left:
        sys.exit(f"build.py: unfilled placeholders {left}")
    shutil.rmtree(OUT, ignore_errors=True)
    (OUT / "design").mkdir(parents=True)
    (OUT / "index.html").write_text(page, encoding="utf-8")
    for f in ("tokens.css", "components.css", "theme.js", "copy.js"):
        shutil.copy(DESIGN / f, OUT / "design" / f)
    shutil.copytree(ROOT / "site/img", OUT / "img")
    print(f"wrote {OUT.relative_to(ROOT)}/ (rules: {counts})")


if __name__ == "__main__":
    main()
