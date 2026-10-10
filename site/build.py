"""Build _site/ for GitHub Pages: the page, the design system files it loads, and the real checker output.

The page source (site/index.html) has placeholders that are filled here, so nothing on the page is typed by hand:
  <!--SAMPLE:name-->  the sample input from site/samples/name (escaped)
  <!--RAW:name-->     the sample as live markup (only for samples built from Clear components)
  <!--OUTPUT:stem-->  what style_check.py printed for that sample, run now, plus its exit code
  <!--COUNT:all|ko|en|any|ui-->  number of rules from --list-rules
  <!--REV-->          the commit being built (a valid pre-commit rev)
"""
import html
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


def main() -> None:
    page = (ROOT / "site/index.html").read_text(encoding="utf-8")
    page = re.sub(r"<!--SAMPLE:([\w.-]+)-->", lambda m: html.escape((SAMPLES / m.group(1)).read_text(encoding="utf-8").rstrip("\n")), page)
    page = re.sub(r"<!--RAW:([\w.-]+)-->", lambda m: (SAMPLES / m.group(1)).read_text(encoding="utf-8"), page)
    names = {p.stem: p.name for p in SAMPLES.iterdir()}
    page = re.sub(r"<!--OUTPUT:([\w-]+)-->", lambda m: run_sample(names[m.group(1)]), page)
    counts = rule_counts()
    page = re.sub(r"<!--COUNT:(\w+)-->", lambda m: str(counts[m.group(1)]), page)
    rev = os.environ.get("GITHUB_SHA") or subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    page = page.replace("<!--REV-->", rev)
    left = re.findall(r"<!--(SAMPLE|OUTPUT|COUNT|REV|RAW)[^>]*-->", page)
    if left:
        sys.exit(f"build.py: unfilled placeholders {left}")
    shutil.rmtree(OUT, ignore_errors=True)
    (OUT / "design").mkdir(parents=True)
    (OUT / "index.html").write_text(page, encoding="utf-8")
    for f in ("tokens.css", "components.css", "theme.js", "copy.js"):
        shutil.copy(DESIGN / f, OUT / "design" / f)
    print(f"wrote {OUT.relative_to(ROOT)}/ (rules: {counts})")


if __name__ == "__main__":
    main()
