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
                  "화면이 비슷해 보이는 이유는 기본값을 쓰기 때문입니다.\n").stdout
        self.assertIn("ko-universal-claim", out)
        self.assertIn("ko-reason-cleft", out)
        ok = run("ok.md", "# 원인\n\n실패한 이유를 로그에서 확인합니다. 어느 쪽을 고를지 표로 비교합니다.\n"
                 "읽기는 캐시에서, 쓰기는 DB에서 처리합니다.\n").stdout
        for rule in ("ko-universal-claim", "ko-reason-cleft", "ko-paired-contrast"):
            self.assertNotIn(rule, ok)

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


if __name__ == "__main__":
    unittest.main()
