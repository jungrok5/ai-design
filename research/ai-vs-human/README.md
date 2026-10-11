# AI 글과 사람 글 비교 데이터

[docs/measurement.md](../../docs/measurement.md)의 "AI 글과 사람 글 비교"에 쓴 데이터와 스크립트입니다. 같은 제목으로
사람이 쓴 한국어 문서와 Claude가 쓴 문서를 비교해 AI 글에 특히 많은 표현을 찾고, 규칙이 두 글을 얼마나 구분하는지
측정합니다.

| 파일 | 내용 |
| --- | --- |
| `pairs.json` | 비교한 178개 주제: 사람 문서 경로, 제목, 문서 종류, 분량, 작성 모델, 학습용·시험용 구분 |
| `ai/` | Claude Opus 5.5, Sonnet 5.5, Haiku 5.5가 쓴 문서 178개. 생성 결과를 고치지 않고 그대로 둠 |
| `human-manifest.json` | 사람 문서 664개의 출처와 학습용·시험용 구분. 원문은 레포에 넣지 않고 `fetch-human.sh`로 받음 |
| `candidates.tsv` | 학습용에서 찾은 후보 표현 132개와 AI·사람 문서 수 |
| `results-*.txt` | 후보 추출, 학습용·시험용 측정, 새 규칙 4개 합계의 출력 |
| `tools/` | `select.py`(주제 선정), `gen_one.sh`(문서 생성), `analyze.py`(후보 추출), `evaluate.py`(규칙 측정), `summarize.py`, `ctx.py`(후보 문맥 보기) |

사람 문서의 저작권은 각 출처에 있습니다. 이 폴더에는 경로와 커밋만 기록합니다. 재현 명령은
[docs/measurement.md](../../docs/measurement.md#재현)에 있습니다.
