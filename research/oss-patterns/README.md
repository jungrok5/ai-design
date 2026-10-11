# 오픈소스 검출기에서 가져온 패턴

1.5.0에서 다른 AI 문체 검출 도구가 잡는 패턴을 모아 측정하고, 사람 글을 잘못 보고하지 않는 것만 규칙으로 넣었습니다.
결과 요약은 [docs/measurement.md](../../docs/measurement.md#오픈소스-검출기의-패턴)에 있습니다.

## 출처

라이선스가 MIT나 Apache-2.0인 레포만 썼습니다. 패턴 목록과 예문을 읽고 정규식은 새로 작성했습니다. 라이선스가 없는
레포(`halans/ai-pattern-detection`, `shannhk/avoid-slop`)는 읽기만 하고 쓰지 않았습니다.

| 레포 | 커밋 | 라이선스 | 언어 |
| --- | --- | --- | --- |
| [epoko77-ai/im-not-ai](https://github.com/epoko77-ai/im-not-ai) | `2f3d943` | MIT | 한국어 |
| [DaleSeo/korean-skills](https://github.com/DaleSeo/korean-skills) | 1.0.0부터 출처 | MIT | 한국어 |
| [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop) | `8da1f03` | MIT | 영어 |
| [JMill/deslop](https://github.com/JMill/deslop) | `1ccad56` | MIT | 영어 |
| [jdkato/voices](https://github.com/jdkato/voices) | `5409079` | MIT | 영어 |
| [tbhb/vale-ai-tells](https://github.com/tbhb/vale-ai-tells) | `4c7abc9` | MIT | 영어 |
| [krishnasunkam/vale-ai-tells](https://github.com/krishnasunkam/vale-ai-tells) | `d4a2f64` | MIT | 영어 |
| [sam-paech/slop-score](https://github.com/sam-paech/slop-score) | `289264a` | MIT | 영어 |
| [tnguyen21/slop-guard-rs](https://github.com/tnguyen21/slop-guard-rs) | `a64d405` | MIT | 영어 |
| [aaazzam/dslop](https://github.com/aaazzam/dslop) | `bade119` | Apache-2.0 | 영어 |
| [blader/humanizer](https://github.com/blader/humanizer) | 1.0.0부터 출처 | MIT | 영어 |

korean-skills의 번역투·어휘 패턴은 대부분 1.0.0 규칙이나 im-not-ai 후보와 겹쳤습니다.

## 파일

- `candidates-ko.json`, `candidates-en.json`: 기존 규칙이 잡지 않는 후보(한국어 72개, 영어 59개). 후보마다 출처 파일과
  줄, 정규식, 잡아야 할 예문과 잡으면 안 되는 예문, 학습용 문서에서 보고된 AI·사람 문서 수(`train_ai_docs`,
  `train_human_docs`), 채택 여부와 이유(`decision`)가 있습니다.
- `essay/`: 칼럼 형식의 AI 글 16편(한국어 8, 영어 8)과 생성에 쓴 프롬프트, 스크립트입니다.

## 채택 기준

1. 한국어 비교 묶음([../ai-vs-human/](../ai-vs-human/))과 영어 비교 묶음([../ai-vs-human/en/](../ai-vs-human/en/))의
   학습용 문서에서 후보마다 보고된 문서 수를 셉니다.
2. 사람 문서에서 1건 이하로 보고되고, 1건이면 그 문장을 읽어 AI 문체로 볼 수 있는 경우만 남깁니다.
3. 영어 후보는 서로 다른 레포 3곳 이상이 같은 패턴을 다루는 경우만 남깁니다. 한국어 후보는 출처가 하나뿐이어서 이
   조건을 적용하지 않았습니다.
4. AI 문서에서 보고되더라도 기존 규칙이 이미 같은 문서를 보고하면 넣지 않습니다(`ko-emoji-inline`).
5. 남은 규칙을 시험용 문서에서 한 번 측정합니다.

## 재현

```bash
cd research/ai-vs-human/en
./fetch-human.sh && python3 tools/splits_en.py .
python3 ../tools/evaluate.py . /tmp test     # 시험용 영어 문서에서 규칙별 AI·사람 문서 수

cd ../../oss-patterns/essay
for id in $(python3 -c "import json;print(' '.join(p['id'] for p in json.load(open('prompts.json'))))"); do ./gen.sh "$PWD" "$id"; done
python3 ../../../plugins/ai-design/style/style_check.py ai/*.md
```
