# 변경 기록

버전은 `plugins/ai-design/.claude-plugin/plugin.json`과 `.claude-plugin/marketplace.json`에 같은 값으로 기록합니다.
태그 대신 커밋 SHA를 적어 두므로 pre-commit과 GitHub Action에서는 이 SHA를 `rev`나 `uses`에 고정해 씁니다.

## 1.6.1

- `ui-raw-font`: `@font-face` 블록 안의 `font-family`는 보고하지 않음. 이 값은 불러올 글꼴의 이름을 정하는 선언이라 토큰
  밖의 글꼴 스택이 아님. 일반 CSS 규칙과 `style` 속성의 글꼴 스택은 그대로 보고. 사이트 3곳에서 비교한 결과 줄어든 보고
  12건은 모두 `@font-face` 선언이었고, 남은 4건은 실제 규칙의 글꼴 스택

## 1.6.0 (`c64fa89`)

<!-- style-ignore-start -->
- AI 문체 검출 도구 13곳(모두 MIT)의 패턴을 1.5.0과 같은 방법으로 측정해서 사람 글을 잘못 보고하지 않는 것만 경고 규칙으로
  추가([docs/measurement.md](docs/measurement.md#160-출처-13곳-추가)):
  - 한국어 20개: 굵은 머리말 목록(`ko-bold-label-list`), "~로 자리잡고 있다", "한 획을 그었다", "전문가들은", "앞으로의
    행보가 기대된다", "~해 드릴까요?", "하나씩 짚어 보겠습니다", "~하고 있는 중이다", "미리 예측" 등
  - 영어 13개: "The best part: …", "the data tells us", "north star", "reflects broader trends", "at the end of
    the day", "Contrary to popular belief", "Whether you're a … or …", "What makes this work is" 등
  - `ko-personified-subject`가 "시장이 원한다", "결과가 증명한다"도 보고
  - 시험용에서 새 규칙이 보고한 문서는 한국어 AI 8/35(23%), 사람 1/139, 영어 AI 0/13, 사람 2/150
- 경고 규칙 `ko-metaphor-noun`: 연결이나 과정을 비유 명사로 쓴 표현("샘플 페이지로 가는 길이 있습니다", "패킷을 받는
  길", "~의 여정", "전체 지도", "문을 열어 줍니다", "첫걸음을 내딛", "디딤돌", "나침반")
- 사람 문서를 보고하지 않도록 패턴을 좁힘: `길이`(length), `길찾기`, `지름길`, "집에 가는 길에", "React 여정을 시작",
  "JavaScript 첫걸음", "~하는 열쇠입니다"는 보고하지 않음. 비교 묶음에서 사람 문서 보고는 학습용 0/525, 시험용 0/139,
  표본 밖 Markdown 0/836 ([docs/measurement.md](docs/measurement.md#비유-명사-160))
<!-- style-ignore-end -->
- `polish-writing` 스킬: 문단 순서 점검, 따라 할 일은 동사로, 군더더기를 지운 뒤 빠진 성분 점검, 여러 신호가 겹친
  곳만 고치기, 마지막 자기 점검, 원문의 추측 표현 유지. [docs/standard.md](docs/standard.md)에도 같은 기준 추가
- 후보 목록과 채택 이유, 출처 커밋: [research/oss-patterns/](research/oss-patterns/). 후보를 검사기와 같은 방식으로
  세는 `research/oss-patterns/measure.py` 추가
- 스킬과 `docs/standard.md`, Cursor, Copilot, AGENTS.md 어댑터의 규칙 요약에 위 표현 추가

## 1.5.1 (`ece33e4`)

- 규칙 옵션 `max_per_1k`: 1,000단어당 이 횟수를 넘을 때만 보고. 긴 파일이 길다는 이유로 보고되지 않음
- `en-filler-words`(1,000단어당 4회)와 `dash-overuse`(8회)에 적용. 시험용 사람 영어 문서에서 보고 비율이 각각
  26.0%에서 3.3%, 27.3%에서 4.0%로 줄었고 AI가 쓴 칼럼에서의 보고는 그대로
  ([docs/measurement.md](docs/measurement.md#오픈소스-검출기의-패턴))

## 1.5.0 (`dd0ea88`)

<!-- style-ignore-start -->
- 다른 AI 문체 검출 도구 11곳(MIT, Apache-2.0)의 패턴을 측정해서 사람 글을 잘못 보고하지 않는 것만 경고 규칙으로 추가
  ([docs/measurement.md](docs/measurement.md#오픈소스-검출기의-패턴)):
  - 한국어 20개: 칼럼·보도자료 상투구("그 어느 때보다", "가능성을 열어준다", "과제도 남아 있다", "~다는 분석이다",
    "회의를 가졌다", "## 결론: …" 헤딩 등)
  - 영어 22개: "It's not X, it's Y", "The question isn't X", "Here's the catch", "The result?", "Feel free to reach
    out", "Absolutely!", "To be honest", "marks a pivotal moment", "the evolving landscape" 등
  - 기술 문서 시험용에서 사람 문서 보고는 한국어 0/139, 영어 2/150. 칼럼 형식 AI 글에서는 영어 5/8, 한국어 2/8편을 보고
- `ko-double-passive`가 "되어졌다"도 보고
<!-- style-ignore-end -->
- 넣지 않은 후보와 이유, 영어 비교 묶음(react.dev, es-toolkit, MDN), 칼럼 형식 AI 글:
  [research/oss-patterns/](research/oss-patterns/), [research/ai-vs-human/en/](research/ai-vs-human/en/)
- 기존 영어 규칙이 영어 기술 문서에서 AI 글보다 사람 글을 더 많이 보고한다는 측정 결과 기록(시험용 AI 0/13, 사람 65/150)
- `polish-writing` 스킬과 어댑터의 규칙 요약에 위 표현 추가

## 1.4.0 (`6c5ce60`)

<!-- style-ignore-start -->
- AI 글과 사람 글 비교에서 찾은 경고 규칙 4개([docs/measurement.md](docs/measurement.md#ai-글과-사람-글-비교)):
  `ko-advise`("~하시길 권합니다"), `ko-template-heading`(체크리스트·핵심 포인트 같은 절 제목),
  `ko-count-runup`("변경은 세 가지입니다"), `ko-hedged-advice`("~하는 편이 안전합니다"). 같은 주제로 쓴 시험용
  문서에서 AI 문서 26%, 사람 문서 1.4%에서 보고됨
<!-- style-ignore-end -->
- `polish-writing` 스킬과 Cursor, Copilot, AGENTS.md 어댑터의 규칙 요약에 위 표현 추가
- 비교 데이터와 스크립트: [research/ai-vs-human/](research/ai-vs-human/)

## 1.3.0 (`c1e0dc9`)

- 검사기 명령줄:
  - 없는 경로, 지원하지 않는 파일, 검사한 파일이 없는 경우를 종료 코드 2로 처리. 따옴표 없이 넘긴 `**` glob이
    조용히 통과하던 문제 수정
  - 디렉터리를 넘기면 하위 파일을 찾아 검사. 숨김 폴더, `node_modules`, `vendor`, `dist`, `build`는 제외
  - Python 3.11 미만은 종료 코드 2. 수정 직후 훅에서는 편집을 막지 않도록 0
  - 요약 줄이 실제로 검사한 파일 수를 표시
  - 새 옵션: `--help`, `--warn-only`, `--format github|json`, `--baseline`과 `--write-baseline`,
    표준 입력(`-`, `--stdin-name`)
- 수정 직후 훅이 파일 전체가 아니라 이번에 수정한 줄(앞뒤 한 줄 포함)의 결과만 Claude에게 전달
- GitHub Action(`action.yml`): PR이 바꾼 파일만 검사하고 결과를 PR 화면에 주석으로 표시
- 영어 규칙: `en-filler-preface`(`it is important to note`), `en-buzzword`(`robust`, `comprehensive` 등, 경고),
  `en-ai-vocabulary`에 `leverage`, `synergy` 추가, `en-hype`에 `state-of-the-art`, `empower` 추가
- Claude Code 실행 비교에서 본 표현을 잡는 경고 규칙: `ko-question-heading`(질문형 제목), `ko-slogan`("~면 끝"),
  `ko-cta-now`("지금 ~해 보세요"), `ui-default-accent`(Tailwind 남색·보라 강조색)
- 공개 한국어 문서 4곳 측정([docs/measurement.md](docs/measurement.md))에서 드러난 오탐과 성능 문제 수정:
  - `ko-register-mix`가 합니다체 문서의 지시문 `~하세요.`를 해요체로 세지 않음
  - `ko-ni-isseoseo`("위치에 있어"), `ko-personify`("데이터가 흘러가는"), `ko-universal-claim`(시스템 안의 범위),
    `ko-question-heading`(영어 링크 제목)의 패턴을 좁힘
  - `ko-reason-cleft`는 한 파일에서 3회 이상일 때만 보고
  - 큰 파일에서 `ko-emoji-marker`의 반복 탐색으로 7.7초 걸리던 문제를 0.3초로 수정. 줄 번호 계산도 이진 탐색으로 변경
- Cursor, Copilot, AGENTS.md용 어댑터에 규칙 요약과 실행 명령을 직접 포함
- 마켓플레이스 최상위 버전을 플러그인 버전과 일치시키고 CI에서 확인

## 1.2.0 (`41a545e`)

- 검사기 자체의 한국어 제안을 명사형으로 통일하고 테스트 추가
- 같은 규칙은 한 줄에 한 번만 보고. 빈도 규칙은 모든 등장 횟수를 셈
- 스킬: 히어로와 본문의 반복, 짧은 문장 연속, 한 단어로 두 주체 지칭, 부분 합과 전체 수 불일치 점검 추가

## 1.1.0 (`bffa187`)

- 경고 규칙 7개: `ko-metaphor-verb`, `ko-universal-claim`, `ko-reason-cleft`, `ko-paired-contrast`,
  `ko-just-one`, `ui-section-number`, `ui-table-min-width`
- 스킬에 페이지 단위 점검 추가(실제 출력 제시, 조건이 붙은 숫자, 같은 틀의 반복 금지 등)
- 디자인 시스템: 실행 결과를 보여 주는 `.ds-output`, 조용한 복사 버튼, 휴대폰에서 줄바꿈되는 명령 블록

## 1.0.0 (`d8c880f`)

- 첫 공개: `polish-writing`, `polish-ui` 스킬, 디자인 시스템 Clear, 스타일 검사기, pre-commit 훅
