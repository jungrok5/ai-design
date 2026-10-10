# 변경 기록

버전은 `plugins/ai-design/.claude-plugin/plugin.json`과 `.claude-plugin/marketplace.json`에 같은 값으로 기록합니다.
태그 대신 커밋 SHA를 적어 두므로 pre-commit과 GitHub Action에서는 이 SHA를 `rev`나 `uses`에 고정해 씁니다.

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
