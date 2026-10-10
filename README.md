# ai-design

AI가 쓴 글과 AI가 만든 화면에 남는 흔적을 걸러 내는 도구 모음입니다. 어느 프로젝트에나 붙일 수 있습니다.
과장된 수식어, 번역투, 문체 혼용, 보라색 그라데이션, 똑같은 카드 세 장 같은 흔적이 대상입니다.

| 구성 | 하는 일 |
| --- | --- |
| `polish-writing` 스킬 | 한국어·영어 글을 다듬습니다. 문서는 합니다체 하나, 사실을 지어내지 않음, 내용 형식(설명은 문단, 실행할 것은 명령, 흐름은 도식, 비교는 표) |
| `polish-ui` 스킬 | 화면을 디자인 시스템에서 시작합니다. 프로젝트에 토큰이 없으면 기본 디자인 시스템 "Clear"를 씁니다. 접근성과 한글 타이포그래피 최소 기준 포함 |
| 디자인 시스템 Clear | 라이트(흰 바탕, 파란 강조색 하나)와 다크(그래파이트) 토큰, `ds-` 컴포넌트, 복사 버튼, 테마 전환 |
| 스타일 검사 | 규칙 약 55개(한국어·영어 글, UI 마크업). 표준 라이브러리만 쓰는 Python 스크립트 하나. 수정 직후 훅, 명령줄, pre-commit, CI에서 같은 규칙으로 동작 |

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
  rev: v1.0.0
  hooks:
    - id: ai-design-style
```

### 명령줄과 CI

레포를 받아 두고 검사기를 직접 실행합니다. `error`가 있으면 종료 코드 1을 돌려주므로 CI 단계로 그대로 쓸 수 있습니다.

```bash
git clone --depth 1 https://github.com/jungrok5/ai-design ~/.ai-design
python3 ~/.ai-design/plugins/ai-design/style/style_check.py README.md docs/*.md src/**/*.tsx
python3 ~/.ai-design/plugins/ai-design/style/style_check.py --list-rules
```

### Cursor, Copilot 등 다른 도구

규칙 파일을 프로젝트에 복사합니다. 세 파일 모두 같은 기준을 가리킵니다.

| 도구 | 복사할 파일 | 위치 |
| --- | --- | --- |
| AGENTS.md를 읽는 도구(Codex, Gemini CLI, Aider 등) | [adapters/AGENTS.snippet.md](adapters/AGENTS.snippet.md) | 프로젝트 `AGENTS.md`에 붙여 넣기 |
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

프로젝트 루트의 `.style/rules.toml`에 같은 형식으로 규칙을 추가하거나 끕니다. 예를 들어 해요체를 쓰기로 한 제품
화면은 다음처럼 `ko-haeyo`를 끕니다. 한 문서 안의 문체 혼용 검사는 그대로 유지됩니다.

```toml
[[rule]]
id = "ko-haeyo"
severity = "off"
```

나쁜 예시를 일부러 인용하는 줄에는 `style-ignore`를 표시하고, 여러 줄이면 `style-ignore-start`와 `style-ignore-end`
사이에 둡니다.

## 검증

| 대상 | 명령 |
| --- | --- |
| 검사기 동작 | `python3 -m unittest discover -s tests` |
| 이 레포의 글과 화면 | `python3 plugins/ai-design/style/style_check.py README.md docs/*.md examples/*.html` |
| 스킬이 필요할 때만 호출되는지 | `claude plugin eval plugins/ai-design --trust-plugin --no-publish` |

평가 케이스는 `plugins/ai-design/evals/`에 있습니다. 호출해야 하는 경우(랜딩 문구, 히어로 화면)와 호출하지 않아야
하는 경우(코드 버그 수정)를 함께 둡니다.

## 출처와 라이선스

MIT. 규칙과 스킬은 여러 공개 자료를 참고해 새로 작성했습니다. 출처와 각 라이선스는
[THIRD_PARTY_NOTICES.md](plugins/ai-design/THIRD_PARTY_NOTICES.md)에 있습니다.
