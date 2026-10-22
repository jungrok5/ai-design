#!/usr/bin/env python3
"""ai-design style check: flags the AI tone in prose and the AI look in UI code. Deterministic, stdlib only.

  style_check.py PATH...                 check files; a directory is searched for supported files
  style_check.py - --stdin-name pr.md    check text from stdin (e.g. a PR body), typed by the given name
  style_check.py --hook                  PostToolUse hook mode: read the hook JSON on stdin, check the edited file and
                                         hand findings on the edited lines back to the agent (never blocks the edit)
  style_check.py --list-rules            print the rule table

Options:
  --format text|github|json   text (default); github = workflow annotations for pull requests; json
  --warn-only                 always exit 0 (for a first rollout in CI)
  --baseline FILE             ignore findings recorded in FILE; --write-baseline FILE records the current ones

Exit codes: 0 no error-level findings (or --warn-only), 1 at least one error, 2 usage problem (missing path,
unsupported file, nothing checked, Python older than 3.11).

Rules live next to this file in rules.toml. A repository can add or override rules in `.style/rules.toml`
(same format; a rule with an existing id replaces it, `severity = "off"` disables it).

Prose rules run on human-readable text only: Markdown outside code, HTML text outside <script>/<style>/<pre>/<code>.
Markup rules run on raw HTML/CSS/JSX/TSX/Vue/Svelte source.
Skip a line with `style-ignore` anywhere on it (e.g. `<!-- style-ignore -->`), or a block between
`style-ignore-start` and `style-ignore-end` — for quoting bad examples on purpose.
"""
from __future__ import annotations

import bisect
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # Python < 3.11
    tomllib = None

HERE = Path(__file__).resolve().parent
PROSE_EXT = {".md", ".mdx", ".markdown", ".txt", ".html", ".htm"}
MARKUP_EXT = {".html", ".htm", ".css", ".scss", ".jsx", ".tsx", ".vue", ".svelte", ".astro"}
HANGUL = re.compile(r"[가-힣]")
WORD = re.compile(r"[A-Za-z]+|[가-힣]+")  # English words and Korean eojeol-ish runs, for max_per_1k


@dataclass
class Rule:
    id: str
    kind: str          # prose | markup
    lang: str          # ko | en | any
    severity: str      # error | warning | off
    pattern: re.Pattern
    message: str
    suggest: str = ""
    max_per_file: int = 0  # >0: only report when the pattern occurs more than this many times in the file
    max_per_1k: float = 0  # >0: and more than this many times per 1,000 words, so long files are not flagged for length


def load_rules() -> list[Rule]:
    if tomllib is None:
        print("style_check: Python 3.11+ is needed to read rules.toml", file=sys.stderr)
        return []
    raw: dict[str, dict] = {}
    sources = [HERE / "rules.toml"]
    root = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    sources.append(Path(root) / ".style" / "rules.toml")
    for src in sources:
        if src.is_file():
            for r in tomllib.loads(src.read_text(encoding="utf-8")).get("rule", []):
                raw[r["id"]] = {**raw.get(r["id"], {}), **r}
    rules = []
    for r in raw.values():
        if r.get("severity", "warning") == "off":
            continue
        flags = re.IGNORECASE if r.get("ignore_case", r.get("lang") == "en") else 0
        rules.append(Rule(id=r["id"], kind=r.get("kind", "prose"), lang=r.get("lang", "any"),
                          severity=r.get("severity", "warning"), pattern=re.compile(r["pattern"], flags),
                          message=r["message"], suggest=r.get("suggest", ""), max_per_file=int(r.get("max_per_file", 0)),
                          max_per_1k=float(r.get("max_per_1k", 0))))
    return rules


def _blank(m: re.Match) -> str:
    """Replace a match with spaces/newlines so line and column numbers stay put."""
    return re.sub(r"[^\n]", " ", m.group(0))


def prose_of(path: Path, text: str) -> str:
    ext = path.suffix.lower()
    if ext in (".html", ".htm"):
        text = re.sub(r"<(script|style|pre|code)\b.*?</\1>", _blank, text, flags=re.S | re.I)
        text = re.sub(r"<!--.*?-->", _blank, text, flags=re.S)
        text = re.sub(r"<[^>]+>", _blank, text)
        text = re.sub(r"&[a-z]+;|&#\d+;", _blank, text)
        return text
    text = re.sub(r"\A---\n.*?\n---\n", _blank, text, flags=re.S)           # front matter
    text = re.sub(r"^(```|~~~).*?^\1[^\n]*$", _blank, text, flags=re.S | re.M)  # fenced code
    text = re.sub(r"`[^`\n]+`", _blank, text)                                 # inline code
    text = re.sub(r"<!--.*?-->", _blank, text, flags=re.S)
    text = re.sub(r"https?://\S+", _blank, text)
    text = re.sub(r"\]\([^)]*\)", _blank, text)                               # link targets
    return text


def ignored_lines(text: str) -> set[int]:
    out, inside = set(), False
    for n, line in enumerate(text.splitlines(), 1):
        if "style-ignore-start" in line:
            inside = True
        if inside or "style-ignore" in line:
            out.add(n)
        if "style-ignore-end" in line:
            inside = False
    return out


def supported(path: Path) -> bool:
    return path.suffix.lower() in PROSE_EXT | MARKUP_EXT


def check_file(path: Path, rules: list[Rule]) -> list[dict]:
    if not supported(path) or not path.is_file():
        return []
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return []
    return check_text(path, text, rules)


def check_text(path: Path, text: str, rules: list[Rule]) -> list[dict]:
    ext = path.suffix.lower()
    skip = ignored_lines(text)
    if "style-ignore-file" in text[:500]:
        return []
    views = {"markup": text if ext in MARKUP_EXT else None, "prose": prose_of(path, text) if ext in PROSE_EXT else None}
    has_ko = bool(HANGUL.search(views["prose"] or ""))
    findings, starts = [], {}
    for rule in rules:
        if rule.kind == "register":
            findings += register_mix(path, views["prose"], rule, skip) if has_ko else []
            continue
        body = views.get(rule.kind)
        if body is None or (rule.lang == "ko" and not has_ko):
            continue
        if body not in starts:  # offsets of each line start, so a match position maps to its line in O(log n)
            starts[body] = [0] + [i + 1 for i, c in enumerate(body) if c == "\n"]
        line_starts = starts[body]
        hits, seen_lines, total = [], set(), 0
        has_hit = "hit" in rule.pattern.groupindex  # a (?P<hit>…) group narrows what is reported
        for m in rule.pattern.finditer(body):
            start = m.start("hit") if has_hit and m.group("hit") is not None else m.start()
            line = bisect.bisect_right(line_starts, start)
            if line in skip:
                continue
            total += 1  # max_per_file counts every occurrence outside style-ignore lines
            if line in seen_lines:  # but each rule is reported once per line
                continue
            seen_lines.add(line)
            col = start - line_starts[line - 1] + 1
            text = m.group("hit") if has_hit and m.group("hit") is not None else m.group(0)
            hits.append({"file": str(path), "line": line, "col": col, "rule": rule.id, "severity": rule.severity,
                         "match": text.strip()[:60], "message": rule.message, "suggest": rule.suggest})
        limit = rule.max_per_file
        if rule.max_per_1k:
            words = len(WORD.findall(body))
            limit = max(limit, int(rule.max_per_1k * words / 1000))
        if limit and total <= limit:
            continue
        if limit:
            hits = hits[:1]
            per = f", 1,000단어당 {rule.max_per_1k:g}회" if rule.max_per_1k else ""
            hits[0]["message"] += f" ({total}회, 기준 {limit}회{per})"
        findings += hits
    return sorted(findings, key=lambda f: (f["file"], f["line"], f["col"]))


FORMAL = re.compile(r"(니다|니까)[.?!]")
# "~하세요." / "~주세요." is the usual way to give an instruction inside 합니다체 docs, so it does not count as 해요체.
POLITE = re.compile(r"[가-힣](?<!니)(?<!세)요[.?!]|세요\?")
PLAIN = re.compile(r"[가-힣](?<!니)다[.!]")
REGISTERS = {"합니다체": FORMAL, "해요체": POLITE, "한다체": PLAIN}


def register_mix(path: Path, prose: str | None, rule: Rule, skip: set[int]) -> list[dict]:
    """Flag a file that mixes speech levels (합니다체 / 해요체 / 한다체) in running sentences.

    Table cells and list items written as noun phrases (개조식) have no sentence ending and are not counted.
    A level counts as mixed in when it has 3+ endings and at least 10% of all endings.
    """
    if not prose:
        return []
    lines = prose.splitlines()
    hits = {k: [(n, m) for n, l in enumerate(lines, 1) if n not in skip for m in rx.finditer(l)] for k, rx in REGISTERS.items()}
    total = sum(map(len, hits.values()))
    used = sorted(((k, v) for k, v in hits.items() if len(v) >= 3 and len(v) >= 0.1 * total), key=lambda kv: len(kv[1]))
    if len(used) < 2:
        return []
    kind, occ = used[0]
    n, m = occ[0]
    counts = ", ".join(f"{k} {len(v)}곳" for k, v in hits.items() if v)
    return [{"file": str(path), "line": n, "col": m.start() + 1, "rule": rule.id, "severity": rule.severity,
             "match": m.group(0), "suggest": rule.suggest,
             "message": f"{rule.message} ({counts}; 소수인 {kind}의 첫 위치)"}]


def fmt(f: dict) -> str:
    s = f"{f['file']}:{f['line']}:{f['col']} {f['severity']} [{f['rule']}] \"{f['match']}\" — {f['message']}"
    return s + (f" → {f['suggest']}" if f["suggest"] else "")


def edited_lines(path: Path, tool_input: dict) -> set[int] | None:
    """Line numbers the edit touched, or None for a whole-file write (then every line counts)."""
    news = [e.get("new_string", "") for e in tool_input.get("edits", [])] or [tool_input.get("new_string")]
    news = [n for n in news if n]
    if not news:
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None
    lines: set[int] = set()
    for new in news:
        at = text.find(new)
        if at < 0:
            continue
        first = text.count("\n", 0, at) + 1
        lines.update(range(first - 1, first + new.count("\n") + 2))  # the edit plus one line of context each side
    return lines or None


def hook_mode(rules: list[Rule]) -> int:
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        return 0
    tool_input = payload.get("tool_input") or {}
    path = Path(tool_input.get("file_path") or "")
    if not str(path) or not supported(path):
        return 0
    findings = check_file(path, rules)
    touched = edited_lines(path, tool_input)
    if touched is not None:
        findings = [f for f in findings if f["line"] in touched]
    if not findings:
        return 0  # nothing is sent to the agent, so a clean edit costs no tokens
    shown = findings[:15]
    lines = [fmt(f) for f in shown] + ([f"… and {len(findings) - len(shown)} more"] if len(findings) > len(shown) else [])
    context = ("ai-design style check (github.com/jungrok5/ai-design, docs/standard.md) found AI-tone/AI-look patterns in the "
               "lines you just wrote. Fix the ones that are real in this context, only in those lines (keep facts, names and "
               "code unchanged; do not rewrite text you were not asked to touch); leave deliberate quotes with a "
               "`style-ignore` marker. For a metaphor or slogan, rewrite the sentence as a plain statement of who does what "
               "(with the number or condition if you have it) instead of swapping in another image.\n" + "\n".join(lines))
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": context}}, ensure_ascii=False))
    return 0


def expand(paths: list[str]) -> tuple[list[Path], list[str]]:
    """Files to check and usage problems. Directories are searched; hidden and vendored folders are skipped."""
    files, problems = [], []
    for a in paths:
        p = Path(a)
        if p.is_dir():
            found = sorted(f for f in p.rglob("*") if f.is_file() and supported(f)
                           and not any(part.startswith(".") or part in ("node_modules", "vendor", "dist", "build")
                                       for part in f.relative_to(p).parts[:-1]))
            files += found
        elif not p.exists():
            problems.append(f"{a}: no such file (an unexpanded glob? quote-free shells need globstar for **)")
        elif not supported(p):
            problems.append(f"{a}: not a supported file type ({', '.join(sorted(PROSE_EXT | MARKUP_EXT))})")
        else:
            files.append(p)
    return files, problems


def fingerprint(f: dict) -> str:
    return f"{f['file']}\t{f['rule']}\t{f['match']}"


def report(findings: list[dict], form: str) -> None:
    if form == "json":
        print(json.dumps(findings, ensure_ascii=False, indent=1))
        return
    for f in findings:
        if form == "github":
            level = "error" if f["severity"] == "error" else "warning"
            msg = f"[{f['rule']}] {f['match']}: {f['message']}" + (f" → {f['suggest']}" if f["suggest"] else "")
            msg = msg.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
            print(f"::{level} file={f['file']},line={f['line']},col={f['col']}::{msg}")
        else:
            print(fmt(f))


def take(argv: list[str], flag: str) -> str | None:
    if flag in argv:
        i = argv.index(flag)
        if i + 1 >= len(argv):
            sys.exit(f"style_check: {flag} needs a value")
        value = argv[i + 1]
        del argv[i:i + 2]
        return value
    return None


def main(argv: list[str]) -> int:
    argv = list(argv)
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0 if argv else 2
    if tomllib is None:
        print("style_check: Python 3.11 or newer is required (tomllib); nothing was checked", file=sys.stderr)
        return 0 if argv[:1] == ["--hook"] else 2
    rules = load_rules()
    if argv[:1] == ["--hook"]:
        return hook_mode(rules)
    if argv[:1] == ["--list-rules"]:
        for r in sorted(rules, key=lambda r: (r.kind, r.lang, r.id)):
            print(f"{r.severity:7} {r.kind:6} {r.lang:3} {r.id:28} {r.message}")
        return 0
    form = take(argv, "--format") or "text"
    if form not in ("text", "github", "json"):
        print(f"style_check: unknown --format {form}", file=sys.stderr)
        return 2
    stdin_name = take(argv, "--stdin-name") or "stdin.md"
    baseline, write_baseline = take(argv, "--baseline"), take(argv, "--write-baseline")
    warn_only = "--warn-only" in argv
    argv = [a for a in argv if a != "--warn-only"]
    unknown = [a for a in argv if a.startswith("--")]
    if unknown:
        print(f"style_check: unknown option {unknown[0]} (see --help)", file=sys.stderr)
        return 2

    findings, checked = [], 0
    if "-" in argv:
        argv.remove("-")
        if not supported(Path(stdin_name)):
            print(f"style_check: --stdin-name {stdin_name} is not a supported file type", file=sys.stderr)
            return 2
        findings += check_text(Path(stdin_name), sys.stdin.read(), rules)
        checked += 1
    files, problems = expand(argv)
    for msg in problems:
        print(f"style_check: {msg}", file=sys.stderr)
    for f in files:
        findings += check_file(f, rules)
    checked += len(files)
    if not checked:
        print("style_check: nothing was checked", file=sys.stderr)
        return 2

    if write_baseline:
        Path(write_baseline).write_text("\n".join(sorted(fingerprint(f) for f in findings)) + "\n", encoding="utf-8")
        print(f"style: wrote {len(findings)} finding(s) to {write_baseline}", file=sys.stderr)
        return 0
    known = 0
    if baseline:
        base = Path(baseline).read_text(encoding="utf-8").splitlines() if Path(baseline).is_file() else []
        remaining = {}
        for b in base:
            remaining[b] = remaining.get(b, 0) + 1
        kept = []
        for f in findings:
            k = fingerprint(f)
            if remaining.get(k):
                remaining[k] -= 1
                known += 1
            else:
                kept.append(f)
        findings = kept

    report(findings, form)
    errors = sum(f["severity"] == "error" for f in findings)
    warnings = len(findings) - errors
    extra = f", {known} known (baseline)" if baseline else ""
    print(f"style: {errors} error(s), {warnings} warning(s) in {checked} file(s){extra}", file=sys.stderr)
    if problems:
        return 2  # a path that was asked for but not checked must not pass silently, even with --warn-only
    return 0 if warn_only else (1 if errors else 0)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
