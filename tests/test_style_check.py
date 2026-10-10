"""Smoke tests for the style check: bad text and markup are flagged, clean text and token-based CSS are not."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

CHECK = Path(__file__).resolve().parents[1] / "plugins/ai-design/style/style_check.py"


def run(name: str, body: str, *args: str) -> subprocess.CompletedProcess:
    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / name
        f.write_text(body, encoding="utf-8")
        return subprocess.run([sys.executable, str(CHECK), *args, str(f)], capture_output=True, text=True, cwd=d)


class StyleCheck(unittest.TestCase):
    def test_flags_korean_ai_tone(self):
        r = run("bad.md", "# 소개\n\n혁신적인 AI 기반 분석으로 경쟁력을 강화하세요.\n결론적으로, 지금이야말로 시작할 때입니다.\n")
        self.assertEqual(r.returncode, 1)
        self.assertIn("ko-hype", r.stdout)
        self.assertIn("ko-closing-formula", r.stdout)

    def test_clean_formal_korean_passes(self):
        r = run("ok.md", "# 설치\n\n`make setup`을 실행합니다. 설치에는 약 2분이 걸립니다.\n")
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_flags_ai_look_markup(self):
        html = '<h1 class="bg-clip-text text-transparent bg-gradient-to-r from-indigo-500 to-purple-500">🚀 Hi</h1>\n'
        r = run("bad.html", html)
        self.assertEqual(r.returncode, 1)
        self.assertIn("ui-gradient-text", r.stdout)
        self.assertIn("ui-purple-gradient", r.stdout)

    def test_raw_color_is_a_warning_and_tokens_are_fine(self):
        self.assertIn("ui-raw-color", run("a.css", "a{color:#1d4ed8}\n").stdout)
        self.assertNotIn("ui-raw-color", run("b.css", ":root{--accent:#1d4ed8}\na{color:var(--accent)}\n").stdout)

    def test_style_ignore(self):
        r = run("q.md", "인용: 혁신적인 제품 <!-- style-ignore -->\n")
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_hook_mode_returns_context_and_never_blocks(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "x.md"
            f.write_text("혁신적인 솔루션입니다.\n", encoding="utf-8")
            r = subprocess.run([sys.executable, str(CHECK), "--hook"], input=json.dumps({"tool_input": {"file_path": str(f)}}),
                               capture_output=True, text=True, cwd=d)
        self.assertEqual(r.returncode, 0)
        self.assertIn("additionalContext", json.loads(r.stdout)["hookSpecificOutput"])

    def test_structure_level_korean_tells(self):
        out = run("t.md", "# 소개\n\n이 도구는 어느 프로젝트에나 붙일 수 있습니다.\n"
                  "화면이 비슷해 보이는 이유는 기본값을 쓰기 때문입니다.\n"
                  "글이 길어지는 이유는 요약을 반복하기 때문입니다.\n"
                  "신뢰가 떨어지는 이유는 숫자가 없기 때문입니다.\n").stdout
        self.assertIn("ko-universal-claim", out)
        self.assertIn("ko-reason-cleft", out)
        ok = run("ok.md", "# 원인\n\n실패한 이유를 로그에서 확인합니다. 어느 쪽을 고를지 표로 비교합니다.\n"
                 "읽기는 캐시에서, 쓰기는 DB에서 처리합니다.\n").stdout
        for rule in ("ko-universal-claim", "ko-reason-cleft", "ko-paired-contrast"):
            self.assertNotIn(rule, ok)

    def test_false_positives_found_in_public_korean_docs(self):
        """Lines from ko.react.dev and naver/fe-news that the 1.3.0 measurement showed were flagged wrongly."""
        human = ("# 구조\n\n에이전트의 모든 기능이 예측 가능한 위치에 있어 검사와 확장이 쉽다.\n"
                 "컴포넌트들을 연결하여 데이터가 그 사이를 흘러가게 합니다.\n"
                 "트리의 어느 위치에서나 Suspense를 추가할 수 있습니다.\n"
                 "그 이유는 Ref가 일반 객체처럼 동작하기 때문입니다.\n\n"
                 "## [Should I use e.code or e.key?](https://example.com)\n")
        out = run("h.md", human).stdout
        for rule in ("ko-ni-isseoseo", "ko-personify", "ko-universal-claim", "ko-reason-cleft", "ko-question-heading"):
            self.assertNotIn(rule, out)
        bad = run("b.md", "# 소개\n\n개발 과정에 있어서 중요합니다.\n라벨만 붙이면 일이 알아서 흘러갑니다.\n").stdout
        self.assertIn("ko-ni-isseoseo", bad)
        self.assertIn("ko-personify", bad)

    def test_frequency_rules_need_repeats(self):
        once = run("a.md", "# 메일\n\n필터가 스팸 메일을 걸러 냅니다.\n").stdout
        self.assertNotIn("ko-metaphor-verb", once)
        twice = run("b.md", "# 소개\n\nAI 티를 걸러 냅니다.\n흔적을 걸러 내는 도구입니다.\n").stdout
        self.assertIn("ko-metaphor-verb", twice)

    def test_decorative_section_numbers(self):
        html = "".join(f'<section><span class="num">0{i}</span><h2>t</h2></section>' for i in range(1, 5))
        self.assertIn("ui-section-number", run("s.html", html).stdout)
        self.assertNotIn("ui-section-number", run("t.html", "<td>01</td><span>09:00</span>").stdout)

    def test_ignored_lines_are_not_counted(self):
        body = "# 예\n\n" + "".join(f"<!-- style-ignore --> 이 API를 통해 {i}\n" for i in range(5)) + "이 API를 통해 조회합니다.\n"
        self.assertNotIn("ko-tonghae", run("i.md", body).stdout)

    def test_korean_messages_use_one_register(self):
        """The checker's own Korean messages and suggestions are noun phrases, never 해요체 or imperatives."""
        import re
        import tomllib
        rules = tomllib.loads(CHECK.with_name("rules.toml").read_text(encoding="utf-8"))["rule"]
        bad = [r["id"] for r in rules for key in ("message", "suggest")
               if re.search(r"(세요|십시오|[가-힣]요)[ .)]*$|(세요|십시오)[ .,)]", r.get(key, ""))]
        self.assertEqual(bad, [])

    def test_english_filler_and_buzzwords(self):
        out = run("e.md", "It is important to note that we leverage a robust engine.\n").stdout
        for rule in ("en-filler-preface", "en-ai-vocabulary"):
            self.assertIn(rule, out)
        self.assertIn("en-buzzword", run("f.md", "A robust parser.\n").stdout)
        self.assertEqual(run("g.md", "Retries survive a dropped connection.\n").returncode, 0)

    def test_tells_seen_in_real_claude_runs(self):
        out = run("n.md", "## 얼마나 빨라졌나요?\n\n스테이징 배포, 명령 하나면 끝.\n\n지금 설치해 보세요.\n").stdout
        for rule in ("ko-question-heading", "ko-slogan", "ko-cta-now"):
            self.assertIn(rule, out)
        ok = run("o.md", "## 배포 시간\n\n조건이 맞으면 충분히 빠릅니다. 지금 사용하는 버전을 확인합니다.\n").stdout
        for rule in ("ko-question-heading", "ko-slogan", "ko-cta-now"):
            self.assertNotIn(rule, ok)
        self.assertIn("ui-default-accent", run("a.html", '<p class="text-indigo-600">x</p>\n').stdout)
        self.assertNotIn("ui-default-accent", run("b.html", '<p class="text-slate-600">x</p>\n').stdout)

    def test_instruction_seyo_is_not_a_register_mix(self):
        """'~하세요.' gives instructions inside 합니다체 docs (seen in ko.react.dev); it is not 해요체."""
        body = "# 사용\n\n" + "".join(f"설정 {i}을 적용합니다.\n" for i in range(8)) + "".join(f"[예시 {i}를 참고하세요.](#a)\n" for i in range(4))
        self.assertNotIn("ko-register-mix", run("r.md", body).stdout)
        mixed = "# 사용\n\n" + "".join(f"설정 {i}을 적용합니다.\n" for i in range(8)) + "".join(f"값 {i}이 바뀌어요.\n" for i in range(4))
        self.assertIn("ko-register-mix", run("m.md", mixed).stdout)

    def test_large_file_with_blank_runs_is_fast(self):
        """A 348 KB ko.react.dev post took 7.7 s before: '^\\s*' spanned blank lines left by stripped code blocks."""
        import time
        body = "# 글\n\n" + ("설명합니다.\n" + "\n" * 200 + "- 항목\n") * 300
        t = time.monotonic()
        run("big.md", body)
        self.assertLess(time.monotonic() - t, 3.0)


def cli(*args: str, stdin: str = "", cwd: str | None = None) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(CHECK), *args], input=stdin, capture_output=True, text=True, cwd=cwd)


class Cli(unittest.TestCase):
    """Paths that were asked for never pass silently, and the rollout options behave as documented."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.d = Path(self.tmp.name)
        (self.d / "docs" / "node_modules").mkdir(parents=True)
        (self.d / "docs" / "bad.md").write_text("혁신적인 솔루션입니다.\n", encoding="utf-8")
        (self.d / "docs" / "ok.md").write_text("설치에 2분이 걸립니다.\n", encoding="utf-8")
        (self.d / "docs" / "node_modules" / "x.md").write_text("혁신적인 도구입니다.\n", encoding="utf-8")
        (self.d / "LICENSE").write_text("MIT\n", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_missing_path_is_a_usage_error(self):
        r = cli("nope/*.md", cwd=self.tmp.name)
        self.assertEqual(r.returncode, 2)
        self.assertIn("no such file", r.stderr)
        self.assertEqual(cli("--warn-only", "docs/ok.md", "nope.md", cwd=self.tmp.name).returncode, 2)

    def test_unsupported_file_and_empty_call(self):
        self.assertEqual(cli("LICENSE", cwd=self.tmp.name).returncode, 2)
        self.assertEqual(cli(cwd=self.tmp.name).returncode, 2)
        self.assertEqual(cli("--bogus", "docs", cwd=self.tmp.name).returncode, 2)

    def test_directory_recurses_and_skips_vendored(self):
        r = cli("docs", cwd=self.tmp.name)
        self.assertEqual(r.returncode, 1)
        self.assertIn("in 2 file(s)", r.stderr)
        self.assertNotIn("node_modules", r.stdout)

    def test_help(self):
        r = cli("--help")
        self.assertEqual(r.returncode, 0)
        self.assertIn("--warn-only", r.stdout)

    def test_warn_only(self):
        r = cli("--warn-only", "docs", cwd=self.tmp.name)
        self.assertEqual(r.returncode, 0)
        self.assertIn("ko-hype", r.stdout)

    def test_stdin(self):
        r = cli("-", "--stdin-name", "pr.md", stdin="혁신적인 변경입니다.\n")
        self.assertEqual(r.returncode, 1)
        self.assertIn("pr.md:1:", r.stdout)

    def test_github_and_json_formats(self):
        gh = cli("--format", "github", "docs/bad.md", cwd=self.tmp.name).stdout
        self.assertRegex(gh, r"^::error file=docs/bad.md,line=1,col=1::\[ko-hype\]")
        data = json.loads(cli("--format", "json", "docs/bad.md", cwd=self.tmp.name).stdout)
        self.assertEqual(data[0]["rule"], "ko-hype")

    def test_baseline_hides_known_findings_only(self):
        self.assertEqual(cli("--write-baseline", "base.txt", "docs", cwd=self.tmp.name).returncode, 0)
        self.assertEqual(cli("--baseline", "base.txt", "docs", cwd=self.tmp.name).returncode, 0)
        (self.d / "docs" / "new.md").write_text("결론적으로, 지금이 시작할 때입니다.\n", encoding="utf-8")
        r = cli("--baseline", "base.txt", "docs", cwd=self.tmp.name)
        self.assertEqual(r.returncode, 1)
        self.assertIn("new.md", r.stdout)
        self.assertNotIn("bad.md", r.stdout)

    def test_hook_reports_only_edited_lines(self):
        f = self.d / "page.md"
        f.write_text("혁신적인 옛 문장입니다.\n\n\n\n설치에 2분이 걸립니다.\n", encoding="utf-8")
        payload = {"tool_input": {"file_path": str(f), "old_string": "x", "new_string": "설치에 2분이 걸립니다."}}
        self.assertEqual(cli("--hook", stdin=json.dumps(payload)).stdout, "")
        payload["tool_input"]["new_string"] = "혁신적인 옛 문장입니다."
        self.assertIn("ko-hype", cli("--hook", stdin=json.dumps(payload)).stdout)


if __name__ == "__main__":
    unittest.main()
