# 페이지 문구의 비유와 슬로건 (1.7.0)

<!-- style-ignore-start -->
Claude Code에게 웹페이지나 문서를 만들게 하면 채팅에서는 쓰지 않는 광고 문구 말투가 나옵니다. "가장 짧은 길로
잇습니다", "흘러가는 로그", "밀이 숨 쉬는 시간만큼 결이 생깁니다" 같은 표현입니다. 1.7.0의 규칙과 스킬은 이 폴더의
조사와 측정으로 정했습니다.
<!-- style-ignore-end -->
결과 요약은 [docs/measurement.md](../../docs/measurement.md)에 있습니다.

| 파일 | 내용 |
| --- | --- |
| `prompts.tsv` | 페이지·문서 주제 14개와 요청 문장. 사용자가 실제로 보낼 만한 짧은 요청 |
| `tells.tsv` | 플러그인 없이 만든 42개에서 직접 읽고 표시한 AI 티 표현 105개와 종류 |
| `candidates-ko.py`, `candidates-en.py` | 측정한 정규식 후보 |
| `community-ko.md`, `community-en.md` | 커뮤니티·기사·검출기 레포에서 AI 문체로 지적한 표현 조사(2026-10-22, 출처 URL 포함) |
| `tools/gen.sh` | 플러그인 없이 빈 폴더에서 `claude -p`로 페이지 한 개 생성 |
| `tools/genp.sh` | 플러그인(`--plugin-dir`)을 켜고 같은 요청으로 생성 |
| `tools/polish.sh` | 만든 페이지를 플러그인을 켠 Claude Code(Opus)에게 다듬게 함 |
| `tools/totext.py`, `tools/survive.py` | 페이지에서 사람이 읽는 글을 뽑고, `tells.tsv`의 표현이 다듬은 뒤에 남았는지 셈 |
| `tools/measure.py` | 후보 정규식이 사람 문서, AI 기술 문서, 생성한 페이지를 몇 개 보고하는지 셈 |
| `tools/compare.py` | 두 버전의 검사기가 보고하는 문서 수 비교 |
| `out/` | 플러그인 없이 만든 페이지와 문서 42개(주제 14개 × Opus, Sonnet, Haiku). 생성 결과를 고치지 않음(예시 API 키 문자열만 `sk_test_EXAMPLE`로 가림) |
| `gen-1.6.1/`, `gen-1.7.0/` | 같은 요청을 플러그인을 켜고 Opus로 만든 결과 각 14개 |
| `blind/` | 세 묶음의 Opus 결과를 라벨을 가려 섞은 글, 집계 결과(`blind-counts.tsv`)와 정답(`blind-key.json`) |

## 채택 기준

1. 사람이 쓴 한국어 Markdown 1,472개([../ai-vs-human/](../ai-vs-human/)의 `fetch-human.sh`로 받는 5곳 전체)에서
   보고가 0–1건이고, 1건이면 그 문장을 읽어 AI 문체로 볼 수 있는 경우만 넣습니다.
2. 영어는 사람 문서 985개에서 0건이고 커뮤니티 조사에서 출처가 여러 곳인 것만 넣습니다.
3. 감성어 단어 하나(`결`, `흐름`, `잇다`, `닿다`, `온도`)는 사람 문구에도 흔해서 넣지 않습니다. 페이지에서 꾸밈으로만
   쓰는 짝말만 넣습니다.
