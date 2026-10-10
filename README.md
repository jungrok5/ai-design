# ai-design

Claude Code가 쓰는 글과 화면에서 AI 티를 줄이는 플러그인입니다. Claude Code가 문서나 화면 작업을 시작할 때 글쓰기
지침과 화면 지침을 읽게 하고, 파일을 수정한 직후 과장 수식어, 번역투, 문체 혼용, 보라색 그라데이션 같은 표현을 줄
번호와 함께 Claude에게 돌려줍니다. 검사기는 pre-commit, GitHub Action, 명령줄에서도 씁니다. Python 3.11 이상이
필요하고, Markdown, HTML, CSS, JSX/TSX, Vue, Svelte, Astro 파일을 검사합니다.

| 구성 | 하는 일 |
| --- | --- |
| `polish-writing` 스킬 | 한국어·영어 글을 다듬습니다. 문서는 합니다체 하나, 사실을 지어내지 않음, 내용 형식(설명은 문단, 실행할 것은 명령, 흐름은 도식, 비교는 표) |
| `polish-ui` 스킬 | 화면을 디자인 시스템에서 시작합니다. 프로젝트에 토큰이 없으면 기본 디자인 시스템 "Clear"를 씁니다. 접근성과 한글 타이포그래피 최소 기준 포함 |
| 디자인 시스템 Clear | 라이트(흰 바탕, 파란 강조색 하나)와 다크(그래파이트) 토큰, `ds-` 컴포넌트, 복사 버튼, 테마 전환 |
| 스타일 검사 | 한국어·영어 글과 UI 마크업 규칙(목록: `--list-rules`). 표준 라이브러리만 쓰는 Python 스크립트. 수정 직후 훅(수정한 줄만 보고), 명령줄, pre-commit, GitHub Action에서 실행 |

**소개 페이지:** https://jungrok5.github.io/ai-design/ (Claude Code를 ai-design 없이, 그리고 켜고 실행한 결과 비교를
담았습니다. 원본은 [site/](site/), 실행 결과 파일은 [site/samples/claude/](site/samples/claude/))

사람이 쓴 공개 한국어 문서 4곳에서 측정한 규칙별 보고 수와 표본 판정은 [docs/measurement.md](docs/measurement.md),
버전별 변경과 고정할 커밋은 [CHANGELOG.md](CHANGELOG.md)에 있습니다.

기준 전문은 [docs/standard.md](docs/standard.md)에 있습니다. 컴포넌트 예시는 [examples/index.html](examples/index.html)을
브라우저로 열어 확인합니다.

## 설치

### Claude Code

마켓플레이스를 한 번 추가하고 플러그인을 설치합니다. 설치하면 두 스킬과 수정 직후 검사 훅이 함께 켜집니다.

```bash
claude plugin marketplace add jungrok5/ai-design
claude plugin install ai-design@ai-design
```

팀 프로젝트에서 모든 팀원에게 자동으로 켜려면 프로젝트의 `.claude/settings.json`에 등록합니다.

```json
{
  "extraKnownMarketplaces": {
    "ai-design": { "source": { "source": "github", "repo": "jungrok5/ai-design" } }
  },
  "enabledPlugins": { "ai-design@ai-design": true }
}
```

갱신은 `claude plugin update ai-design@ai-design`으로 받습니다.

### pre-commit

사람의 커밋과 다른 AI 도구가 만든 변경도 같은 규칙으로 검사합니다. 프로젝트의 `.pre-commit-config.yaml`에 추가합니다.
Python 3.11 이상이 필요합니다.

```yaml
- repo: https://github.com/jungrok5/ai-design
  rev: REV_PLACEHOLDER  # 1.3.0
  hooks:
    - id: ai-design-style
```

이 레포는 태그를 쓰지 않으므로 `rev`에는 [CHANGELOG.md](CHANGELOG.md)에 적힌 버전별 커밋을 씁니다.

### GitHub Action

PR이 바꾼 파일만 검사하고, 보고를 PR의 변경 줄 옆에 주석으로 표시합니다.

```yaml
on: pull_request
jobs:
  style:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: jungrok5/ai-design@REV_PLACEHOLDER  # 1.3.0
        with:
          warn-only: "true"   # 첫 도입 기간에는 실패 처리하지 않음
          # baseline: .style/baseline.txt
          # paths: README.md docs   (비우면 변경 파일)
```

### 명령줄과 CI

레포를 받아 두고 검사기를 직접 실행합니다. 파일이나 폴더를 넘기며, 폴더는 숨김 폴더와 `node_modules`, `vendor`,
`dist`, `build`를 빼고 하위 파일을 검사합니다.

```bash
git clone --depth 1 https://github.com/jungrok5/ai-design ~/.ai-design
python3 ~/.ai-design/plugins/ai-design/style/style_check.py README.md docs src
gh pr view --json body -q .body | python3 ~/.ai-design/plugins/ai-design/style/style_check.py - --stdin-name pr.md
```

| 옵션 | 동작 |
| --- | --- |
| `--format text\|github\|json` | 출력 형식. `github`는 워크플로 주석 |
| `--warn-only` | 보고만 하고 종료 코드 0 |
| `--write-baseline FILE`, `--baseline FILE` | 현재 보고를 기록, 기록된 보고는 제외 |
| `-`, `--stdin-name NAME` | 표준 입력을 NAME 형식의 파일로 검사 |
| `--list-rules`, `--help` | 규칙 목록, 사용법 |

| 종료 코드 | 뜻 |
| --- | --- |
| 0 | `error` 없음, 또는 `--warn-only` |
| 1 | `error`가 하나 이상 |
| 2 | 없는 경로, 지원하지 않는 파일, 검사한 파일 없음, Python 3.11 미만 |

### Cursor, Copilot 등 다른 도구

규칙 요약과 검사 명령을 담은 파일을 프로젝트에 복사합니다. 이 도구들에는 수정 직후 검사가 없으므로 pre-commit이나
GitHub Action을 함께 씁니다.

| 도구 | 복사할 파일 | 위치 |
| --- | --- | --- |
| AGENTS.md를 읽는 도구(Codex 등) | [adapters/AGENTS.snippet.md](adapters/AGENTS.snippet.md) | 프로젝트 `AGENTS.md`에 붙여 넣기 |
| Cursor | [adapters/cursor/ai-design.mdc](adapters/cursor/ai-design.mdc) | `.cursor/rules/` |
| GitHub Copilot | [adapters/copilot/ai-design.instructions.md](adapters/copilot/ai-design.instructions.md) | `.github/instructions/` |

### 디자인 시스템만 쓸 때

`plugins/ai-design/skills/polish-ui/design/`의 네 파일을 프로젝트로 복사합니다. 불러오는 순서와 컴포넌트 규칙은
[DESIGN.md](plugins/ai-design/skills/polish-ui/design/DESIGN.md)에 있습니다.

```html
<link rel="stylesheet" href="design/tokens.css">
<link rel="stylesheet" href="design/components.css">
<script src="design/theme.js"></script>   <!-- <head> 안에 -->
<script src="design/copy.js" defer></script>
```

## 프로젝트별 조정

프로젝트 루트의 `.style/rules.toml`에 같은 형식으로 규칙을 추가하거나 끕니다. 해요체로 통일한 문서나 제품 화면은
다음처럼 `ko-haeyo`를 끕니다. 한 문서 안의 문체 혼용 검사(`ko-register-mix`)는 그대로 유지됩니다. 문답집은
`ko-question-heading`, 입문 자습서는 `ko-reader-talk`을 같은 방법으로 끕니다.

```toml
[[rule]]
id = "ko-haeyo"
severity = "off"
```

나쁜 예시를 일부러 인용하는 줄에는 `style-ignore`를 표시하고, 여러 줄이면 `style-ignore-start`와 `style-ignore-end`
사이에 둡니다.

## 팀 도입

이미 문서가 많은 레포는 다음 순서로 넓힙니다.

1. GitHub Action을 `warn-only: "true"`로 추가하고 PR 주석을 한두 주 확인
2. 오탐이 잦은 규칙을 `.style/rules.toml`에서 끄거나 warning으로 낮춤
3. 기존 보고를 기준 파일로 기록: `style_check.py --write-baseline .style/baseline.txt README.md docs`
4. Action에서 `warn-only`를 지우고 `baseline: .style/baseline.txt`를 지정해 새 `error`만 실패 처리

기준 파일은 파일 경로, 규칙, 찾은 표현으로 보고를 구분하므로 줄이 옮겨져도 같은 보고로 봅니다.

## 검증

| 대상 | 명령 |
| --- | --- |
| 검사기 동작 | `python3 -m unittest discover -s tests` |
| 이 레포의 글과 화면 | `python3 plugins/ai-design/style/style_check.py README.md CHANGELOG.md docs examples site/index.html adapters` |
| 소개 페이지 빌드 | `python3 site/build.py` (`_site/`) |
| 스킬이 필요할 때만 호출되는지 | `claude plugin eval plugins/ai-design --trust-plugin --no-publish` |

평가 케이스는 `plugins/ai-design/evals/`에 있습니다. 호출해야 하는 경우(랜딩 문구, 히어로 화면)와 호출하지 않아야
하는 경우(코드 버그 수정)를 함께 둡니다.

## 출처와 라이선스

MIT. 규칙과 스킬은 여러 공개 자료를 참고해 새로 작성했습니다. 출처와 각 라이선스는
[THIRD_PARTY_NOTICES.md](plugins/ai-design/THIRD_PARTY_NOTICES.md)에 있습니다.
