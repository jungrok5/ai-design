# 오픈소스 검출기에서 가져온 패턴

1.5.0과 1.6.0에서 다른 AI 문체 검출 도구가 잡는 패턴을 모아 측정하고, 사람 글을 잘못 보고하지 않는 것만 규칙으로
넣었습니다. 결과 요약은 [docs/measurement.md](../../docs/measurement.md#오픈소스-검출기의-패턴)에 있습니다.

## 출처

라이선스가 MIT나 Apache-2.0인 레포만 썼습니다. 패턴 목록과 예문을 읽고 정규식은 새로 작성했습니다. 라이선스가 없는
레포(`halans/ai-pattern-detection`, `shannhk/avoid-slop`)는 읽기만 하고 쓰지 않았습니다.

| 레포 | 커밋 | 라이선스 | 언어 | 추가 |
| --- | --- | --- | --- | --- |
| [epoko77-ai/im-not-ai](https://github.com/epoko77-ai/im-not-ai) | `2f3d943` (1.6.0에서 `b37e020`까지 확인) | MIT | 한국어 | 1.5.0 |
| [DaleSeo/korean-skills](https://github.com/DaleSeo/korean-skills) | 1.0.0부터 출처 | MIT | 한국어 | 1.5.0 |
| [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop) | `8da1f03` | MIT | 영어 | 1.5.0 |
| [JMill/deslop](https://github.com/JMill/deslop) | `1ccad56` | MIT | 영어 | 1.5.0 |
| [jdkato/voices](https://github.com/jdkato/voices) | `5409079` | MIT | 영어 | 1.5.0 |
| [tbhb/vale-ai-tells](https://github.com/tbhb/vale-ai-tells) | `4c7abc9` | MIT | 영어 | 1.5.0 |
| [krishnasunkam/vale-ai-tells](https://github.com/krishnasunkam/vale-ai-tells) | `d4a2f64` | MIT | 영어 | 1.5.0 |
| [sam-paech/slop-score](https://github.com/sam-paech/slop-score) | `289264a` | MIT | 영어 | 1.5.0 |
| [tnguyen21/slop-guard-rs](https://github.com/tnguyen21/slop-guard-rs) | `a64d405` | MIT | 영어 | 1.5.0 |
| [aaazzam/dslop](https://github.com/aaazzam/dslop) | `bade119` | Apache-2.0 | 영어 | 1.5.0 |
| [blader/humanizer](https://github.com/blader/humanizer) | 1.0.0부터 출처 | MIT | 영어 | 1.5.0 |
| [IsaacEryn/humanizer-ko](https://github.com/IsaacEryn/humanizer-ko) | `d939ac7` | MIT | 한국어 | 1.6.0 |
| [amondnet/yoonmoon](https://github.com/amondnet/yoonmoon) | `c888531` | MIT | 한국어 | 1.6.0 (작업 흐름은 1.0.0부터 출처) |
| [leeandev/stop-slop-ko](https://github.com/leeandev/stop-slop-ko) | `837e38e` | MIT | 한국어 | 1.6.0 |
| [dongsukjang26/natural-korean-skills-for-research](https://github.com/dongsukjang26/natural-korean-skills-for-research) | `45962c0` | MIT | 한국어 | 1.6.0 |
| [nerdkim/im-a-korean-ai-in-seoul](https://github.com/nerdkim/im-a-korean-ai-in-seoul) | `bb2fa28` | MIT | 한국어 | 1.6.0 |
| [teo713ko-gif/hangul-humanizer](https://github.com/teo713ko-gif/hangul-humanizer) | `29867a8` | MIT | 한국어 | 1.6.0 |
| [giudegio-ai/claude-skill-humanizer](https://github.com/giudegio-ai/claude-skill-humanizer) | `5366553` | MIT | 영어, 이탈리아어 | 1.6.0 |
| [Aparnabuilds/humanizer](https://github.com/Aparnabuilds/humanizer) | `fd9728f` | MIT | 영어 | 1.6.0 |
| [Kevjade/humanizer-pro](https://github.com/Kevjade/humanizer-pro) | `d35c324` | MIT | 영어 | 1.6.0 |
| [jpeggdev/humanize-writing](https://github.com/jpeggdev/humanize-writing) | `da03340` | MIT | 영어 | 1.6.0 |
| [Aboudjem/humanizer-skill](https://github.com/Aboudjem/humanizer-skill) | `a58df06` | MIT | 영어 | 1.6.0 |
| [lguz/humanize-writing-skill](https://github.com/lguz/humanize-writing-skill) | `4b7c37f` | MIT | 영어 | 1.6.0 |
| [Hainrixz/humanizalo](https://github.com/Hainrixz/humanizalo) | `357a1e9` | MIT | 영어, 스페인어 | 1.6.0 |

korean-skills의 번역투·어휘 패턴은 대부분 1.0.0 규칙이나 im-not-ai 후보와 겹쳤습니다.

1.6.0에서 확인한 내용은 다음과 같습니다.

- 새 레포 13곳은 모두 MIT여서 읽기만 한 레포는 없습니다. IsaacEryn/humanizer-ko의 LICENSE는 원본인 blader/humanizer의
  저작권 표시(© 2025 Siqi Chen)를 그대로 둔 MIT입니다.
- im-not-ai는 `2f3d943` 뒤 `b37e020`까지 새 패턴이 없습니다. 바뀐 것은 기존 항목 3개를 보수적으로 고친 것입니다.
  A-11 `~을 위해`는 기본 보존, G-3 균형 어휘는 실증 부족으로 보류, H-1 문두 접속사는 한 문단에 3회 이상일 때만
  봅니다. 1.5.0에서 사람 문서 보고로 넣지 않은 `ko-wihae`, `ko-balance-lexicon`, `ko-additive-opener`와 같은
  방향입니다.
- 포크 justicehugo-ctrl/im-not-ai와 cryptaliac/im-not-ai는 `2f3d943` 그대로입니다. teo713ko-gif/hangul-humanizer는
  예전 버전을 이름만 바꾼 포크입니다. 새 항목은 I-8(행동 지시를 `~는 순서예요`처럼 명사 술어로 압축) 하나입니다.
- 비유 명사(`여정`, `문제의 뿌리`, `기준 개선의 한 바퀴`)는 다른 브랜치에서 `ko-metaphor-noun`으로 다루므로 후보 목록에
  기록만 하고 측정하지 않았습니다.
- 영어 레포 7곳은 대부분 blader/humanizer의 24개 패턴을 바탕으로 항목을 늘린 것이라 서로 많이 겹칩니다. 영어 후보의
  출처 수는 이 7곳과 1.5.0 영어 레포 9곳을 모두 검색한 뒤 실제로 그 패턴을 설명하는 레포만 셌습니다.

## 파일

- `candidates-ko.json`, `candidates-en.json`: 기존 규칙이 잡지 않는 후보. 1.5.0에서 한국어 72개, 영어 59개를 넣었고
  1.6.0에서 한국어 58개(측정한 57개와 측정하지 않은 비유 명사 1개), 영어 29개를 더했습니다(`added_in`). 후보마다 출처
  파일과 줄, 정규식, 잡아야 할 예문과 잡으면 안 되는 예문, 학습용 문서에서 보고된 AI·사람 문서 수(`train_ai_docs`,
  `train_human_docs`), 채택 여부와 이유(`decision`)가 있습니다. 1.6.0 항목에는 사람 문서에서 보고된 문장
  (`train_human_examples`), 채택한 규칙의 학습용·시험용 수(`rule_train`, `rule_test`), 사람 문서 때문에 뺀 대안
  (`narrowed`)도 있습니다.
- 1.5.0에서 출처가 3곳 미만이라 넣지 않은 영어 후보 8개는 새 출처를 더해 다시 측정했습니다(`re_measured_1_6_0`,
  `sources_added_1_6_0`). 새 출처가 다시 다루는 1.5.0 한국어 후보 21개에는 그 위치를 `also_in_1_6_0`에 적었습니다.
- `measure.py`: 후보 정규식을 검사기와 같은 방식(코드 블록·인라인 코드·링크 주소 제외, `max_per_file`)으로 실행해
  학습용·시험용 문서 수를 셉니다.
- `essay/`: 칼럼 형식의 AI 글 16편(한국어 8, 영어 8)과 생성에 쓴 프롬프트, 스크립트입니다.

## 채택 기준

1. 한국어 비교 묶음([../ai-vs-human/](../ai-vs-human/))과 영어 비교 묶음([../ai-vs-human/en/](../ai-vs-human/en/))의
   학습용 문서에서 후보마다 보고된 문서 수를 셉니다.
2. 사람 문서에서 1건 이하로 보고되고, 1건이면 그 문장을 읽어 AI 문체로 볼 수 있는 경우만 남깁니다.
3. 영어 후보는 서로 다른 레포 3곳 이상이 같은 패턴을 다루는 경우만 남깁니다. 한국어 후보는 1.5.0에서 출처가 하나뿐이어서
   이 조건을 적용하지 않았습니다. 1.6.0도 같은 기준을 썼습니다.
4. 대안 여러 개를 묶은 후보에서 사람 문서를 보고한 대안이 하나라면, 그 대안을 빼고 나머지를 다시 셉니다(1.6.0, `narrowed`).
   예를 들어 `ko-closing-cliche`에서 `귀추가 주목된다`는 fe-news 등 사람 문서 4건에서 나와 뺐습니다.
5. AI 문서에서 보고되더라도 기존 규칙이 이미 같은 문서를 보고하면 넣지 않습니다(`ko-emoji-inline`).
6. 남은 규칙을 시험용 문서에서 한 번 측정합니다.

## 재현

```bash
cd research/ai-vs-human
./fetch-human.sh && python3 tools/analyze.py . 10 3   # 한국어 사람 문서와 splits.json
cd ../oss-patterns
python3 measure.py candidates-ko.json train --since 1.6.0   # 1.6.0 한국어 후보의 학습용 AI·사람 문서 수

cd ../ai-vs-human/en
./fetch-human.sh && python3 tools/splits_en.py .
python3 ../tools/evaluate.py . /tmp test     # 시험용 영어 문서에서 규칙별 AI·사람 문서 수

cd ../../oss-patterns/essay
for id in $(python3 -c "import json;print(' '.join(p['id'] for p in json.load(open('prompts.json'))))"); do ./gen.sh "$PWD" "$id"; done
python3 ../../../plugins/ai-design/style/style_check.py ai/*.md
```
