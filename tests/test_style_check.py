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

    def test_spaced_middot_in_ui_metadata_is_not_a_prose_list(self):
        # One middot per <li>, and a caption row, are UI separators; a list inside a sentence is still reported.
        ui = '<ul class="tags"><li>2D · 3D</li><li>16:9 · 9:16</li><li>MP4</li></ul>\n<span class="no">장면 02 · 창조 · 35초</span><b>렌즈가 본 빛의 탄생입니다.</b>\n'
        self.assertNotIn("ko-spaced-middot-list", run("ui.html", ui).stdout)
        prose = '<p>파이프라인 · 프로토콜 · 서버 루프 같은 기술 과정을 영상으로 그립니다.</p>\n'
        self.assertIn("ko-spaced-middot-list", run("p.html", prose).stdout)

    def test_raw_font_skips_font_face_declarations(self):
        # font-family inside @font-face names the face being loaded; a stack in a rule or a style attribute is reported.
        face = '@font-face{font-family:"JetBrains Mono";src:url(a.woff2)}\n@font-face {\n  font-family: Pretendard;\n}\n:root{--font-mono:"JetBrains Mono",monospace}\np{font-family:var(--font-mono)}\n'
        self.assertNotIn("ui-raw-font", run("face.css", face).stdout)
        self.assertIn("ui-raw-font", run("rule.css", "p{color:var(--ink);\n  font-family: Arial, sans-serif}\n").stdout)
        self.assertIn("ui-raw-font", run("attr.html", '<p style="font-family: Arial">x</p>\n').stdout)
        r = run("mix.css", '@font-face{font-family:X;src:url(x.woff2)}\nh1{font-family:Georgia,serif}\n')
        self.assertEqual(r.stdout.count("ui-raw-font"), 1, r.stdout)
        self.assertIn(":2:", r.stdout)

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

    def test_rules_absorbed_in_1_6_0(self):
        # 1.6.0: every example a source lists is caught one by one; near-misses stay clean, including human-doc
        # sentences from the train split that a wider draft of the pattern flagged (research/oss-patterns/).
        cases = {
            "ko-legacy-inflation": (
                ["지역 문화 발전의 중요한 전환점을 마련했다.", "이 앨범은 대중음악사에 한 획을 그었다.", "업계 지형을 바꾸는 제품이다.", "국내외 언론의 주목을 받았다.", "테스트의 중요성은 아무리 강조해도 지나치지 않다."],
                ["교차로의 전환점에서 좌회전합니다.", "데이터 흐름을 바꿨습니다.", "언론 보도 자료를 첨부합니다."]),
            "ko-promo-vocab": (
                ["풍부한 문화유산과 빼어난 자연경관을 자랑하는 마을이다.", "명실상부한 업계 1위다.", "설악산 자락에 자리한 마을이다."],
                ["자랑할 만한 결과는 아니다.", "손꼽아 기다렸다."]),
            "ko-vague-attribution": (
                ["전문가들은 이 하천이 핵심적인 역할을 한다고 본다.", "일각에서는 성공 사례로 평가한다.", "여러 연구에 따르면 효과가 있다.", "업계에서는 이를 표준으로 본다."],
                ["Kim 등(2023)의 연구에 따르면 지연이 줄었다.", "전문가 모드에서 실행합니다.", "업계 표준을 따른다."]),
            "ko-closing-cliche": (
                ["여러 과제에 직면해 있다.", "앞으로의 행보가 기대된다.", "회사의 미래는 밝다.", "기후 위기는 우리 모두의 과제다.", "앞으로 배우는 사람이 되겠습니다."],
                ["다음 버전에서 기능이 추가됩니다.", "업계의 귀추가 주목된다.", "사람이 직접 확인한다.", "이러한 장애물에도 불구하고, 향상된 최적화 기술을 구현할 수 있습니다."]),
            "ko-ai-buzzword": (
                ["전통 식단과 시너지를 만들어냈다.", "새 강자로 급부상했다.", "이 책은 도시 문제를 조명한다."],
                ["조명을 켠다.", "무대 조명이 밝다.", "가장 널리 사용되는 도구 중 하나로 자리매김했었습니다."]),
            "ko-copula-avoidance": (
                ["협회의 전시 공간으로 자리잡고 있다.", "거점 역할을 수행하고 있다.", "대안으로 기능하고 있다."],
                ["서버가 요청을 수행한다.", "함수로 기능을 나눈다.", "배열을 보유하고 있다."]),
            "ko-interpretive-rider": (
                ["지역의 산과 바다를 상징하며, 주민들의 마음을 보여준다.", "규칙을 정비함으로써 생태계 발전에 기여한다."],
                ["캐시를 비움으로써 메모리를 확보한다.", "상태를 반영해 화면을 다시 그린다."]),
            "ko-chatbot-offer": (
                ["예시를 들어 드릴까요?", "더 자세한 설명이 필요하시면 말씀해 주세요.", "원하시면 표로 정리해 드리겠습니다.", "정확한 지적이시네요.", "정말 탁월한 관점입니다."],
                ["자세한 설명은 문서를 참고하세요.", "지적 재산권을 보호합니다.", "좋은 질문입니다."]),
            "ko-knowledge-gap": (
                ["설립 연도에 대한 구체적인 정보는 공개되어 있지 않으나 1990년대로 추정된다.", "알려진 바가 많지 않다."],
                ["2025년 기준 사용자는 3만 명이다."]),
            "ko-staged-opening": (
                ["알아야 할 내용을 하나씩 짚어드릴게요.", "본격적으로 들어가기 전에 용어를 정리합니다.", "그럼 시작해 볼까요?", "본 보고서에서는 원인을 다룬다.", "이상으로 세 가지 방법을 살펴보았다.", "사전적 의미로 협업은 함께 일하는 것이다."],
                ["다음 단계로 넘어갑니다.", "사전 데이터를 불러온다.", "웹 이벤트에 대해 알아야 할 모든 것을 알게 되었을 것입니다.", "어떤 일이 일어나는지 자세히 알아보고자 합니다."]),
            "ko-performed-candor": (
                ["솔직히 말해서, 그건 자주 쓰느냐에 달렸습니다."],
                ["솔직한 후기"]),
            "ko-aphorism": (
                ["대칭은 신뢰의 언어다.", "AI는 도구가 아니라 거울이다."],
                ["Python은 범용 언어다."]),
            "ko-staccato-negation": (
                ["대칭에 대한 선호도 없었다. 미적 편향도 없었다."],
                ["반환 값은 없다. 대신 이벤트를 보낸다.", "모든 질문에 대답할 필요는 없다. 그리고 리스트에 모든 것을 할 필요는 없다."]),
            "ko-calque": (
                ["검토하고 있는 중이다.", "반드시 확인하지 않으면 안 된다.", "결정을 만든다.", "전년 대비 구성이 상이하다.", "매출의 증가를 보였다.", "이러한 맥락에서 개선안을 마련했다."],
                ["검토 중이다.", "확인하지 않으면 오류가 난다.", "전년 대비 10% 늘었다.", "같은 맥락에서 보면 이해된다.", "HTML 이미지는 여기서 빛을 발합니다.", "약 30%의 이익 감소가 발생했다."]),
            "ko-pleonasm": (
                ["결과를 미리 예측한다.", "두 팀이 함께 협력한다.", "매주마다 회의를 한다."],
                ["미리 설정한다.", "다시 시작한다.", "공간을 미리 예약한다.", "스레드가 서로 협력관계일 경우 대기시킨다."]),
            "ko-brings-about": (
                ["이러한 변화는 효율성의 향상을 가져올 수 있습니다.", "새 정책은 큰 변화를 가져왔다."],
                ["서버에서 데이터를 가져온다.", "검색 결과를 가져오는 동안", "비즈니스적인 성과를 가져왔다고 소개했다."]),
            "ko-balance-pair": (
                ["장점과 단점이 모두 존재한다.", "단순한 도구에서 필수 파트너로 진화했다."],
                ["장점은 속도다.", "작은 함수에서 시작한다."]),
            "ko-spaced-middot-list": (
                ["속도 · 품질 · 비용을 본다.", "`--check`는 빠진 필드 · 없는 파일 · 동기화 여부를 검사합니다."],
                ["속도·품질·비용을 본다.", "`<!--$?-->`·`<!--/$-->` 주석과 `B:0`·`S:0` 템플릿",
                 "장면 01 · 창조 · 35초", "| 명령줄 · pre-commit · CI | 지원 |"]),
            "ko-personified-subject": (
                ["결과가 증명한다.", "시장이 원한다.", "기술이 질문을 던진다."],
                ["사용자가 원한다."]),
            "en-colon-reveal": (
                ["The catch: it only works offline.", "Fine. The best part: it learns.", "The answer is simple: use a queue.", "It all comes down to one thing: latency."],
                ["The takeaway is in the next section.", "Note: the cache is cleared on restart.", "The reason is this configuration key."]),
            "en-false-agency": (
                ["The data tells us that users churn early.", "The market rewards speed.", "The decision emerges from the review."],
                ["The data show a clear trend.", "The metrics show up in the dashboard."]),
            "en-buzz-metaphor": (
                ["This creates a virtuous cycle.", "Retention is our north star.", "Harness the power of streams.", "The message resonates with developers.", "The team is poised for growth.", "She is a thought leader in AI."],
                ["The flywheel arm is machined steel.", "Point the telescope at the North Star.", "Wire the harness to the board.", "The circuit resonates at 50 Hz."]),
            "en-meaning-telling": (
                ["This reflects broader trends in the industry.", "It represents a fundamental shift.", "The implications are significant.", "The stakes are high."],
                ["The value reflects the current state.", "The risks are listed below."]),
            "en-hollow-phrase": (
                ["At the end of the day, users want speed.", "At its core, the tool is a parser.", "Only time will tell.", "It remains to be seen whether teams adopt it."],
                ["The job runs at the end of each day.", "The core module loads first."]),
            "en-misconception-frame": (
                ["Contrary to popular belief, caching is cheap.", "Most people think this is a hiring problem."],
                ["The belief propagation step runs first."]),
            "en-false-concession": (
                ["While the model is impressive, cost remains a challenge.", "The approach is not without its challenges."],
                ["While the job is running, the lock remains held."]),
            "en-speculative-gap": (
                ["While specific details are limited, the firm grew.", "Based on available information, it launched in 2019."],
                ["Details are in the appendix."]),
            "en-whether-youre": (
                ["Whether you're a beginner or a seasoned pro, this guide helps.", "Whether you're a startup or an enterprise, it scales."],
                ["Check whether you're logged in."]),
            "en-promo-phrases": (
                ["The village is nestled in the hills.", "It is renowned for its stunning views."],
                ["Nested routes are supported."]),
            "en-wh-cleft-opener": (
                ["What makes this work is the cache.", "What makes it special is the API."],
                ["What makes the build slow? Profile it."]),
            "en-what-if-i-told-you": (
                ["What if I told you the cache is slower?"],
                ["What if the file is missing?"]),
            "en-in-an-era": (
                ["In an era of microservices, deploys multiply."],
                ["The era field stores the epoch."]),
        }
        for rule, (bad, ok) in cases.items():
            for text in bad:
                self.assertIn(f"[{rule}]", run("b.md", "# t\n\n" + text + "\n").stdout, f"{rule}: {text}")
            for text in ok:
                self.assertNotIn(f"[{rule}]", run("o.md", "# t\n\n" + text + "\n").stdout, f"{rule}: {text}")

    def test_bold_label_lists_and_repeated_opinion(self):
        labels = "".join(f"- **항목{i}:** 설정을 바꿉니다.\n" for i in range(5))
        self.assertIn("ko-bold-label-list", run("l.md", "# 설정\n\n" + labels).stdout)
        long_doc = "# 설정\n\n" + labels + "\n" + "이 함수는 입력 배열을 정렬한 뒤 새 배열을 반환합니다. " * 80 + "\n"
        self.assertNotIn("ko-bold-label-list", run("m.md", long_doc).stdout)
        self.assertNotIn("ko-bold-label-list", run("n.md", "# 설정\n\n" + labels.replace("**", "")).stdout)
        self.assertIn("ko-think-repeat", run("t.md", "# 의견\n\n좋다고 생각한다. 맞다고 생각한다. 옳다고 본다.\n").stdout)
        self.assertNotIn("ko-think-repeat", run("u.md", "# 의견\n\n좋다고 생각한다. 맞다고 본다.\n").stdout)
        self.assertIn("ko-personified-subject", run("p.md", "# 시장\n\n결과가 증명한다.\n").stdout)
        self.assertNotIn("ko-chatbot-offer", run("q.md", "# 답\n\n좋은 질문입니다.\n").stdout)  # ko-chatbot-residue reports it


    def test_density_threshold_spares_long_files(self):
        # 1.5.1: en-filler-words and dash-overuse count per 1,000 words, so a long doc is not flagged for its length.
        filler = "We just need the cache. " * 5
        self.assertIn("en-filler-words", run("s.md", "# t\n\n" + filler + "\n").stdout)
        long_text = "# t\n\n" + filler + "\n\n" + "The worker reads each record from the queue and writes it. " * 200 + "\n"
        self.assertNotIn("en-filler-words", run("l.md", long_text).stdout)
        dashes = "Cache it \u2014 then ship it. " * 6
        self.assertIn("dash-overuse", run("d.md", "# t\n\n" + dashes + "\n").stdout)
        self.assertNotIn("dash-overuse", run("e.md", "# t\n\n" + dashes + "\n\n" + "The worker writes each record. " * 200 + "\n").stdout)

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

    def test_metaphor_nouns_for_a_process_or_link(self):
        """1.6.0: '가는 길', '여정', '전체 지도' for a link or a flow; length (길이) and literal routes stay quiet."""
        bad = ["카드마다 그 스킬이 만드는 것과 샘플 페이지로 가는 길이 있습니다.", "패킷을 받는 길을 따라갑니다.",
               "서버로 가는 여정.", "요청의 여정을 살펴봅니다.", "## 패킷을 받는 길", "이 표가 전체 지도입니다.",
               "새 API가 확장의 문을 열어 줍니다.", "첫걸음을 내딛습니다.", "이 문서가 나침반이 됩니다.",
               "학습의 디딤돌입니다.", "성공의 열쇠는 테스트입니다.", "로드맵의 청사진을 제시합니다."]
        for line in bad:
            self.assertIn("ko-metaphor-noun", run("b.md", f"# 소개\n\n{line}\n").stdout, line)
        # Lines like these appear in ko.react.dev, MDN ko, es-toolkit and tech-interview (research/ai-vs-human).
        ok = ("# 길이\n\n문자열 길이를 구합니다. 배열의 길이가 3인 경우를 봅니다.\n"
              "문자열이 원하는 길이보다 짧을 때 패딩 문자를 추가합니다.\n"
              "두 헤더로 정의하는 길이가 알려진 본문입니다. 마지막 항목을 나타내는 길이 속성을 씁니다.\n"
              "운전기사는 당신이 몰랐던 지름길을 알고 있습니다. 길찾기 API와 갈림길을 표시합니다.\n"
              "집에 가는 길에 메일을 확인합니다. 정밀한 분석을 가능하게 하는 길을 열었습니다.\n"
              "React 여정을 시작하기에 좋은 곳입니다. JavaScript 첫걸음 모듈을 먼저 읽습니다.\n"
              "Refresh Token이 새 토큰을 발급하는 열쇠가 됩니다. 이것은 청사진처럼 간단한 설명입니다.\n"
              "안정화까지의 로드맵을 공유합니다. 지도 위젯을 불러옵니다. 도어록을 확인하려고 문을 열었다가 닫습니다.\n")
        self.assertNotIn("ko-metaphor-noun", run("ok.md", ok).stdout)

    def test_naya_question_is_not_a_register_mix(self):
        """1.7.0: an FAQ in 합니다체 asks '~나요?' (ko.react.dev, MDN ko); only other 해요체 endings count."""
        body = "# FAQ\n\n설치합니다. 설정합니다. 배포합니다. 확인합니다.\n\n참여할 수 있나요? 네, 참여할 수 있습니다.\n" \
               "비용이 있나요? 없습니다.\n혼자 와도 되나요? 됩니다.\n"
        self.assertNotIn("ko-register-mix", run("faq.md", body).stdout)
        mixed = body + "값이 바뀌어요. 다시 해 봐요. 그럼 끝나요.\n"
        self.assertIn("ko-register-mix", run("mix.md", mixed).stdout)

    def test_directions_heading_is_not_a_metaphor(self):
        """1.7.0: '오시는 길' and '찾아오는 길' are the standard directions label on a page, not a metaphor."""
        page = "<nav><a>오시는 길</a></nav><h2>오시는 길</h2><h2>찾아오는 길</h2><p>성수역에서 걸어서 5분입니다.</p>\n"
        self.assertNotIn("ko-metaphor-noun", run("p.html", page).stdout)
        self.assertIn("ko-metaphor-noun", run("q.md", "# 소개\n\n결제로 가는 길\n").stdout)

    def test_ornamental_page_copy(self):
        """1.7.0: lines Claude Code wrote for Korean landing pages with no plugin (docs/measurement.md)."""
        cases = {
            "ko-ornamental-verb": ["판매자, 배송 파트너, 고객을 하나의 흐름으로 잇습니다.", "흘러가는 로그를 바로 거르고 셉니다.",
                                   "토요일 오전은 이렇게 흘러갑니다.", "하루의 온도를 살피며 반죽을 기다리고, 그 시간만큼 빵의 결이 깊어집니다.",
                                   "중소 쇼핑몰의 주문을 오늘 안에 닿게 합니다.", "작은 쇼핑몰과 고객 사이를 가장 짧은 길로 잇습니다.",
                                   "로그는 흘러가게 두고, 필요한 것만 건져 올리세요.", "결제 버튼까지 가는 길을 짧고 단단하게 만듭니다."],
            "ko-axis-metaphor": ["Suspense라는 두 축을 중심으로 동작합니다.", "속도와 비용, 두 축으로 비교합니다.",
                                 "Actions를 축으로 데이터를 다룹니다."],
            "ko-metaphor-noun": ["최소 물량, 장기 계약이라는 벽에 막혀 있었습니다.", "같은 출발선에 서게 합니다.",
                                 "입양 문턱을 낮추었습니다.", "질문은 스터디의 연료입니다."],
            "ko-reframe": ["모노레포는 목적이 아니라 수단입니다.", "필요한 건 동기가 아니라 규율입니다.",
                           "재능도 아닙니다. 운도 아닙니다. 꾸준함입니다.",
                           "리뷰는 코드를 보는 일이지 사람을 평가하는 일이 아닙니다."],
            "ko-aphorism": ["기다리는 시간이 맛을 만듭니다.", "매주 같은 시간에 모입니다. 루틴이 실력을 만듭니다.", "지표로 말하기"],
            "ko-reveal": ["작은 쇼핑몰이 같은 속도로 배송하는 것. 그게 이음이 하는 일입니다.",
                          "문서가 틀리면 고쳐 주세요. 그게 첫 기여입니다."],
            "ko-paired-slogan": ["속도만큼 신뢰를, 규모만큼 책임을 생각합니다.", "기록은 더 적게, 돈 관리는 더 쉽게.",
                                 "구매 대신 입양을, 짧은 인연 대신 끝까지 함께하는 약속을.",
                                 "회의는 녹음만 하세요. 정리는 노트메이트가 합니다."],
            "ko-fragment-slogan": ["5분 안에 첫 집계까지.", "회의록 작성은 이제 그만", "세 단계면 회의록이 완성됩니다."],
            "ko-count-runup": ["## 우리가 일하는 세 가지 원칙", "## 2.0에서 새로워진 세 가지"],
            "ko-era-opener": ["급변하는 시장에서 살아남으려면 속도가 필요합니다."],
            "ko-hook-formula": ["결론부터 말씀드리면 배포는 다음 주입니다.", "이유는 단순합니다."],
        }
        for rule, lines in cases.items():
            for line in lines:
                self.assertIn(rule, run("c.md", f"# 소개\n\n{line}\n").stdout, line)
        # Literal uses from human docs and plain pages stay quiet.
        ok = ("# 데이터 흐름\n\n컴포넌트를 연결해 데이터가 그 사이를 흘러가게 합니다. 작업 흐름에 맞게 묶습니다.\n"
              "가로축에 시간, 세로축에 값을 둡니다. 실행 시간을 단축하고 이미지를 축소합니다.\n"
              "Effect가 아니라 이벤트 핸들러에 넣으세요. 인수 객체는 배열과 닮은 것이지 배열이 아닙니다.\n"
              "쌀가루를 섞어 결이 부드럽습니다. 요청이 서버에 닿으면 응답합니다.\n"
              "설치부터 첫 집계까지 약 5분이 걸립니다. 변경은 PR 하나로 끝납니다.\n")
        out = run("ok.md", ok).stdout
        for rule in cases:
            self.assertNotIn(rule, out)

    def test_garuda_and_jari_metaphors(self):
        """1.7.2: '가르는 로그 5줄' (판별할 수 있는 로그) and '렉이 생기는 자리' (위치), seen on a work page."""
        for line in ["원인을 가르는 로그 5줄을 봅니다.", "## 구조와 렉이 생기는 자리", "성패를 가르는 지표입니다.",
                     "병목이 막히는 자리를 표시합니다."]:
            self.assertIn("ko-ornamental-verb", run("g.md", f"# 소개\n\n{line}\n").stdout, line)
        ok = ("# 배열\n\n짧은 배열의 빈 자리는 `undefined`로 채워져요. 그 이터러블의 요소를 그 자리에서 내보냅니다.\n"
              "첫 번째 자리에 `Counter`가 있습니다. CVC는 아무 숫자 3자리를 입력합니다. 판별할 수 있는 로그 5줄을 봅니다.\n"
              "렉이 발생할 수 있는 위치를 정리합니다. 머리카락을 가르는 빗입니다.\n")
        self.assertNotIn("ko-ornamental-verb", run("ok.md", ok).stdout)

    def test_quoted_contrast_and_slogan(self):
        """1.7.1: a quoted 'X'가 아닌 'Y' pair and a quoted 'A 대신 B' motto, seen in a résumé reviewed with the plugin."""
        for line in ["서버 부하가 'NPC 총수'가 아닌 '유저 주변 활성 NPC 수'로 수렴합니다.",
                     "재진입 시 재전송 없음, '총량 대신 활성량만 처리'", "“총량 대신 활성량만 처리” 철학으로 설계했습니다."]:
            self.assertIn("ko-reframe", run("q.md", f"# 소개\n\n{line}\n").stdout, line)
        ok = ("# 테스트\n\nform의 필드명은 **'renewal_date'** 대신 **'due_back'**으로 나타납니다.\n"
              "전송 계층에서 TCP 대신 QUIC을 사용합니다. 'id'가 아닌 값은 무시합니다.\n")
        self.assertNotIn("ko-reframe", run("ok.md", ok).stdout)

    def test_game_terms_and_year_ranges_are_not_hype_or_dashes(self):
        """1.7.1: 'seamless field' is a game term; 2007 – 2015 is a range, not dash punctuation."""
        self.assertNotIn("en-hype", run("g.md", "# Work\n\nR&D on large-scale NPC processing and seamless fields.\n").stdout)
        self.assertIn("en-hype", run("h.md", "# Work\n\nA seamless experience for every team.\n").stdout)
        years = "# 경력\n\n" + "".join(f"- 회사 {i} · 20{i:02d} – 20{i + 1:02d} · 2024 – 현재\n" for i in range(10))
        self.assertNotIn("dash-overuse", run("y.md", years).stdout)
        prose = "# 글\n\n" + "이 값은 — 기본값과 달리 — 바뀝니다. " * 6 + "\n"
        self.assertIn("dash-overuse", run("p.md", prose).stdout)

    def test_english_mannered_copy(self):
        """1.7.0: Claude-era mannered prose and landing-page formulas; no hit in 985 human English docs."""
        cases = {"en-mannered": ["This check earns its keep.", "A dial worth turning.", "The load-bearing piece of the design."],
                 "en-hero-formula": ["Project management, reimagined.", "Where design meets code.", "Unlock new possibilities.",
                                     "Effortless invoicing for freelancers."],
                 "en-social-proof": ["Join thousands of happy customers.", "Trusted by 10,000+ of the best teams."],
                 "en-buzz-metaphor": ["We look at it through the lens of cost."],
                 "en-performed-candor": ["Honest caveat: the sync is slow."],
                 "en-what-if-i-told-you": ["Imagine a world where your inbox sorts itself."]}
        for rule, lines in cases.items():
            for line in lines:
                self.assertIn(rule, run("e.md", f"# Intro\n\n{line}\n").stdout, line)
        ok = "# Intro\n\nThink of it as a regular state variable. Ask before embarking on large tasks.\n"
        self.assertEqual(run("ok.md", ok).stdout.count("warning"), 0, run("ok.md", ok).stdout)

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
