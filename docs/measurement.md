# 공개 한국어 문서에서 측정한 결과

사람이 쓴 공개 한국어 문서 4곳에 검사기를 실행하고, 규칙별 보고 수와 표본 판정을 기록합니다. 목적은 검사기가
사람의 글에서 무엇을 얼마나 보고하는지, 그중 무엇이 오탐인지 확인하는 것입니다. AI가 쓴 글을 얼마나 잡아내는지는
이 측정으로 알 수 없습니다.

## 조건

- 측정일: 2026-10-10. 검사기: ai-design 1.3.0. Python 3.13, 4코어 컨테이너
- 대상: Markdown 파일만. 코드 블록과 인라인 코드는 검사하지 않음
- 각 레포를 측정일의 기본 브랜치에서 `git clone --depth 1`로 받음

| 레포 | 커밋 | 범위 | 파일 | 줄 | 문체 |
| --- | --- | --- | --- | --- | --- |
| reactjs/ko.react.dev | `89f79e9` | `src/content` | 229 | 125,104 | 합니다체, 지시는 `~하세요` |
| toss/es-toolkit | `19bd2cb` | `docs/ko` | 680 | 42,785 | 해요체 |
| naver/fe-news | `82bad15` | 전체 | 82 | 17,211 | 한다체 |
| gyoogle/tech-interview-for-developer | `41a7e91` | 전체 | 196 | 23,787 | 한다체와 합니다체 혼용 |

## 결과

| 레포 | error | warning | 실행 시간 |
| --- | --- | --- | --- |
| ko.react.dev | 54 | 315 | 3.9초 |
| es-toolkit | 685 | 26 | 1.3초 |
| fe-news | 107 | 101 | 1.3초 |
| tech-interview-for-developer | 41 | 224 | 0.8초 |
| 합계 | 887 | 666 | 7.3초 |

es-toolkit의 error 685건 중 663건은 `ko-haeyo`입니다. 이 문서는 해요체로 통일되어 있으므로 문체 혼용이 아니라
프로젝트가 고른 문체입니다. 해요체를 쓰는 프로젝트는 `ko-haeyo`를 끄고 씁니다([README](../README.md#프로젝트별-조정)).
끄면 es-toolkit의 보고는 48건이 남습니다.

규칙별 보고 수는 다음과 같습니다(5건 이상인 규칙).

| 규칙 | 수준 | 합계 | ko.react.dev | es-toolkit | fe-news | tech-interview |
| --- | --- | --- | --- | --- | --- | --- |
| `ko-haeyo` | error | 665 | 2 | 663 | 0 | 0 |
| `ko-connective-comma` | warning | 126 | 64 | 1 | 29 | 32 |
| `ko-emoji-marker` | error | 113 | 26 | 2 | 85 | 0 |
| `ko-uihae` | warning | 108 | 77 | 6 | 1 | 24 |
| `ko-tonghae` | warning | 94 | 33 | 0 | 32 | 29 |
| `ko-question-heading` | warning | 72 | 0 | 0 | 0 | 72 |
| `ko-noun-verb` | warning | 63 | 32 | 5 | 7 | 19 |
| `ko-gajigo-itda` | warning | 59 | 27 | 10 | 1 | 21 |
| `ko-colloquial` | error | 43 | 6 | 19 | 3 | 15 |
| `ko-metadiscourse` | warning | 35 | 34 | 0 | 0 | 1 |
| `ko-vague-praise` | warning | 33 | 5 | 1 | 20 | 7 |
| `ko-must-important` | warning | 21 | 12 | 0 | 2 | 7 |
| `ko-daehae` | warning | 20 | 15 | 2 | 0 | 3 |
| `ko-ni-isseoseo` | error | 17 | 2 | 0 | 1 | 14 |
| `ko-cleft` | warning | 15 | 4 | 0 | 7 | 4 |
| `ko-hype` | error | 12 | 0 | 0 | 10 | 2 |
| `ko-double-passive` | error | 10 | 6 | 0 | 0 | 4 |
| `ko-hedge-stack` | warning | 9 | 7 | 0 | 2 | 0 |
| `ko-register-mix` | error | 7 | 1 | 1 | 0 | 5 |
| `ko-reader-talk` | error | 5 | 5 | 0 | 0 | 0 |

나머지 13개 규칙이 1–4건씩 모두 26건을 보고해, 전체 합계는 1,553건입니다.

## 표본 판정

보고가 5건 이상인 규칙 23개에서 4건씩, 모두 92건을 무작위로 골라 Claude가 문맥을 읽고 판정했습니다. 원문 작성자의
판정이 아니고, 규칙마다 같은 수를 뽑았으므로 전체 정확도로 읽지 않습니다. 판정 당시의 규칙은 아래 "측정 후 수정"
이전 상태입니다.

| 판정 | 뜻 | 건수 |
| --- | --- | --- |
| 고칠 만함 | 고치면 문장이 짧아지거나 정확해짐 | 41 |
| 의도된 선택 | 규칙이 겨냥한 표현은 맞지만 문서의 장르나 문체로 보아 그대로 둘 만함 | 44 |
| 오탐 | 규칙이 겨냥하지 않은 표현을 보고함 | 7 |

<!-- style-ignore-start -->
| 규칙 | 고칠 만함 | 의도된 선택 | 오탐 | 예 |
| --- | --- | --- | --- | --- |
| `ko-tonghae` | 4 | 0 | 0 | "props를 통한 전달" → "props로 전달" |
| `ko-double-passive` | 4 | 0 | 0 | "입력란이 비워지게 됩니다" → "비워집니다" |
| `ko-register-mix` | 4 | 0 | 0 | 한 파일 안의 한다체와 합니다체 |
| `ko-uihae` | 3 | 1 | 0 | "useId에 의해 생성된" → "useId가 생성한" |
| `ko-noun-verb` | 3 | 1 | 0 | "설치를 진행한다" → "설치한다" |
| `ko-gajigo-itda` | 3 | 1 | 0 | "HTML을 가지고 있지 않을" → "HTML이 없을" |
| `ko-must-important` | 3 | 1 | 0 | "수정하지 않는 것이 중요합니다" → "수정하지 않습니다" |
| `ko-daehae` | 3 | 1 | 0 | "React에 대해 깊게 이해" → "React를 깊게 이해" |
| `ko-ni-isseoseo` | 3 | 0 | 1 | 오탐: "예측 가능한 위치에 있어"(위치를 뜻함) |
| `ko-colloquial` | 2 | 2 | 0 | 합니다체 문서 속 "거예요" |
| `ko-hedge-stack` | 2 | 1 | 1 | 오탐: 퀴즈의 "1, 2, 3을 출력할 것으로 예상됩니다" |
| `ko-personify` | 2 | 0 | 2 | 오탐: "데이터가 흘러가는"(데이터 흐름은 기술 용어) |
| `ko-question-heading` | 1 | 2 | 1 | 의도된 선택: 면접 문답집의 "Commit과 Rollback이란?" |
| `ko-metadiscourse` | 1 | 3 | 0 | 의도된 선택: 자습서의 "다음 코드를 살펴보겠습니다" |
| `ko-vague-praise` | 1 | 3 | 0 | 고칠 만함: "더 빠르고 효율적인 테스트 환경" |
| `ko-cleft` | 1 | 3 | 0 | 의도된 선택: "새 아키텍처의 핵심은 ~이다" |
| `ko-hype` | 1 | 3 | 0 | 의도된 선택: 99%라는 수치가 붙은 "압도적인 점유율" |
| `ko-haeyo` | 0 | 4 | 0 | 해요체로 통일한 es-toolkit |
| `ko-emoji-marker` | 0 | 4 | 0 | 뉴스레터 제목의 이모지 |
| `ko-connective-comma` | 0 | 4 | 0 | 긴 문장에서 읽기를 돕는 쉼표 |
| `ko-reader-talk` | 0 | 4 | 0 | 입문 자습서의 "걱정하지 마세요" |
| `ko-reason-cleft` | 0 | 4 | 0 | "그 이유는 ~ 때문입니다" 한 번 |
| `ko-universal-claim` | 0 | 2 | 2 | 오탐: "트리의 어느 위치에서나 Suspense를 추가" |
<!-- style-ignore-end -->

## 측정 후 수정

측정에서 드러난 문제는 1.3.0에서 고쳤고, 각 사례를 테스트로 남겼습니다. 위 결과 표와 규칙별 보고 수는 수정 후
다시 실행한 값입니다.

| 문제 | 수정 |
| --- | --- |
| ko.react.dev 229개 파일 중 105개가 `ko-register-mix`로 보고됨. 합니다체 문서의 지시문 "참고하세요."를 해요체로 셈 | `~세요.`를 해요체로 세지 않음. 105건 → 1건 |
| 위 표의 오탐 7건 중 6건(`ko-ni-isseoseo`, `ko-personify`, `ko-universal-claim`, 영어 링크 제목의 `ko-question-heading`) | 패턴을 좁힘 |
| `ko-reason-cleft`가 사람 글에서 한 번 쓴 경우도 보고 | 파일 안에서 3회 이상일 때만 보고 |
| 348 KB 파일 하나에 7.7초. `ko-emoji-marker`의 `^\s*`가 코드 블록을 지운 빈 줄을 넘어 반복 탐색 | `^[ \t]*`로 수정. 0.3초 |

남은 오탐 1건(퀴즈 문장의 "것으로 예상됩니다")은 패턴으로 구분하기 어려워 그대로 둡니다. `ko-hedge-stack`은 <!-- style-ignore -->
warning이므로 실패 처리하지 않습니다.

## 읽는 법

- 검사기는 AI 판별기가 아니라 문체 검사기입니다. 사람이 쓴 문서에서도 번역투(`ko-tonghae`, `ko-uihae`)와 군더더기
  표현이 많이 보고되고, 표본에서 이런 보고는 대부분 고칠 만했습니다.
- 문서 장르에 따라 끌 규칙이 있습니다. 해요체 문서는 `ko-haeyo`, 문답집은 `ko-question-heading`, 입문 자습서는
  `ko-reader-talk`, `ko-metadiscourse`를 `.style/rules.toml`에서 끄거나 warning으로 낮춥니다.
- 이미 쓴 문서에 처음 적용할 때는 `--write-baseline`으로 현재 보고를 기록하고, 새로 생기는 보고만 확인합니다.

## 재현

```bash
git clone --depth 1 https://github.com/reactjs/ko.react.dev
python3 plugins/ai-design/style/style_check.py --format json ko.react.dev/src/content > react.json
```
