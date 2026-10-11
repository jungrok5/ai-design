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

    def test_rules_from_ai_vs_human_comparison(self):
        # Each rule: a sentence Claude wrote in the comparison corpus is flagged, a human-docs phrasing is not.
        cases = {"ko-advise": ("한 번 더 확인하시길 권합니다.\n", "업그레이드를 권장합니다. 이 방식을 추천합니다.\n"),
                 "ko-template-heading": ("## 이달의 실무 체크리스트\n\n본문입니다.\n", "각 장에는 체크리스트가 포함되어 있습니다.\n"),
                 "ko-count-runup": ("눈여겨볼 변경은 세 가지입니다.\n", "설정은 세 가지 방법으로 바꿉니다.\n"),
                 "ko-hedged-advice": ("CI에서 먼저 돌려 보고 올리는 편이 안전합니다.\n", "기본값을 그대로 씁니다.\n")}
        for rule, (bad, ok) in cases.items():
            self.assertIn(rule, run("b.md", bad).stdout, rule)
            self.assertNotIn(rule, run("o.md", ok).stdout, rule)

    def test_rules_absorbed_from_open_source_detectors(self):
        # 1.5.0: each rule catches the example its source lists and leaves a near-miss alone.
        cases = {
            "ko-meeting-gajida": ("어제 팀과 회의를 가졌다.\n", "회의를 열었다.\n"),
            "ko-ilueojida": ("합의가 이루어졌다. 논의가 이루어지고 있다. 투자가 이루어집니다.\n", "꿈이 이루어졌다. 합의했다.\n"),
            "ko-abstract-subject-verb": ("DeepSeek-V4의 등장은 오픈소스의 가능성을 보여줍니다.\n", "이 예제는 사용자 목록을 보여줍니다.\n"),
            "ko-evaluative-clear": ("AI 도입이 필요하다는 점은 명확하다.\n", "분명히 말하지만 사실이 아니다.\n"),
            "ko-foundation-formula": ("지능 강국으로 도약하는 발판을 마련할 수 있다.\n", "공항이 문을 열었다.\n"),
            "ko-english-buzzword-hada": ("사용자에게 seamless하고 robust한 경험을 제공한다\n", "robust 성능을 측정한다.\n"),
            "ko-first-second-third": ("첫째, AI 도구로 의사결정을 개선해야 합니다. 둘째, 클라우드로 확장성을 확보합니다. 셋째, 보안에 투자합니다.\n", "첫째 날은 설치를 합니다.\n"),
            "ko-inline-numbering": ("1) 표준화된 인프라가 일반화되면서 학습 데이터 확보가 용이해졌다. 2) 도메인 특화 LLM이 성숙하면서 활용 범위가 넓어졌다. 3) 클라우드 GPU 단가가 하락했다.\n", "1) 첫 항목\n2) 둘째 항목\n3) 셋째 항목\n"),
            "ko-colon-subtitle-heading": ("### **서론**: 제조업의 미래, AI에 달려있다\n", "## 설치: macOS\n"),
            "ko-opens-possibility": ("새로운 서비스의 가능성을 열어준다.\n", "가능성을 검토한다.\n"),
            "ko-more-than-ever": ("지금은 그 어느 때보다 중요한 시기다.\n", "어느 때나 가능하다.\n"),
            "ko-personified-subject": ("두 지능의 충돌이 질문을 던집니다.\n", "사용자가 질문을 던진다.\n"),
            "ko-leads-to-chain": ("이는 결국 지역 경제의 침체로 이어진다.\n", "오류로 이어지는 호출 경로를 추적한다.\n"),
            "ko-this-is-why": ("이중구조를 더 벌려놓을 수 있다는 우려가 나오는 이유다.\n", "이유를 설명한다.\n"),
            "ko-empty-caveat": ("그러나 과제도 남아 있다.\n", "남은 과제도 있습니다. 로그인 오류를 먼저 고친다.\n"),
            "ko-sensory-evaluation": ("1부의 진단은 서늘하다.\n", "방 안 공기는 서늘하다.\n"),
            "ko-synonym-pair": ("중요하고 핵심적인 역할\n", "작고 빠른 기능\n"),
            "ko-role-and-function": ("핵심 도구로서의 역할과 기능\n", "역할과 권한을 설정한다.\n"),
            "ko-hedge-double": ("오류가 생길 가능성이 있을 수 있다.\n", "가능성이 있다.\n"),
            "ko-unattributed-verdict": ("수요가 시장을 떠받치고 있다는 분석이다.\n", "분석이 끝났다.\n"),
            "en-its-not-x-its-y": ("It's not a framework, it's a toolkit.\n", "If it's not installed, it is skipped.\n"),
            "en-not-because": ("We moved it, not because it was slow, but because it was fragile.\n", "The build failed, not because of the tests.\n"),
            "en-question-isnt-reframe": ("The problem isn't the model. It's the data.\n", "The issue is not reproducible on Linux, per the report.\n"),
            "en-negative-listing": ("No setup. No config. No lock-in.\n", "No such file or directory. Check the path.\n"),
            "en-mic-drop-fragment": ("That's the whole point.\n", "That's the only place the token is stored.\n"),
            "en-rhetorical-self-answer": ("The result? Faster builds.\n", "What is the result? See the output below.\n"),
            "en-chatbot-signoff": ("Feel free to reach out if anything is unclear.\n", "Feel free to override this default in the config.\n"),
            "en-ai-disclosure": ("As an AI language model, I cannot browse the web.\n", "The AI model is loaded at startup.\n"),
            "en-assistant-opener": ("Absolutely! Here is the fix.\n", "Of course, this is optional.\n"),
            "en-uncomfortable-truth": ("The uncomfortable truth is that tests are slow.\n", "The truth value is stored as a boolean.\n"),
            "en-performed-candor": ("Let me be clear: this is breaking.\n", "The client is honest about its capacity.\n"),
            "en-to-be-clear": ("To be clear, this is a breaking change.\n", "The output must be clear before the next run.\n"),
            "en-heres-the-catch": ("Here's the catch: it needs a restart.\n", "Here's the full config.\n"),
            "en-nobody-talks-about": ("Nobody talks about the migration cost.\n", "No one talks to the database directly; use the API.\n"),
            "en-narrative-pivot": ("This is where things get interesting.\n", "The index shifted after the insert.\n"),
            "en-urgency-inflation": ("The importance of backups cannot be overstated.\n", "The value cannot be negative.\n"),
            "en-marks-a-turning-point": ("The release marks a pivotal moment for the project.\n", "The marker marks a boundary in the log.\n"),
            "en-landscape-noun": ("the evolving landscape of cloud security\n", "Use landscape orientation for the print layout.\n"),
            "en-navigate-complexities": ("navigate the complexities of modern tooling\n", "Navigate to Settings and click Save.\n"),
            "en-vague-attribution": ("Experts argue that caching is overused.\n", "The expert panel meets on Friday.\n"),
            "en-stark-reminder": ("It serves as a stark reminder of the risk.\n", "Send a reminder email on Friday.\n"),
            "en-plays-role": ("Caching plays a critical role.\n", "The role is assigned in IAM.\n"),
        }
        for rule, (bad, ok) in cases.items():
            self.assertIn(f"[{rule}]", run("b.md", "# t\n\n" + bad).stdout, rule)
            self.assertNotIn(f"[{rule}]", run("o.md", "# t\n\n" + ok).stdout, rule)

    def test_double_passive_past_tense(self):
        self.assertIn("ko-double-passive", run("p.md", "# t\n\n문서가 작성되어졌다.\n").stdout)

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
