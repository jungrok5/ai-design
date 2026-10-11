# AI 활용

`@example/utils`에는 LLM(대규모 언어 모델) 기반 애플리케이션을 만들 때 자주 쓰는 함수가 모여 있습니다. 텍스트 분할, 토큰 수 추정, 응답 파싱, 재시도 처리를 한곳에서 해결할 수 있습니다. 모든 함수는 특정 AI 제공자에 묶여 있지 않아 어떤 SDK와도 함께 쓸 수 있습니다.

```js
import { chunkText, estimateTokens, parseJSONSafe, retry } from '@example/utils/ai';
```

---

## chunkText(text, options)

긴 텍스트를 모델의 컨텍스트 한도에 맞게 여러 조각으로 나눕니다. 문장 경계를 우선 지키므로 의미가 중간에 끊기는 일이 줄어듭니다.

| 매개변수 | 타입 | 기본값 | 설명 |
|---|---|---|---|
| `text` | `string` | — | 나눌 원문 |
| `options.maxTokens` | `number` | `500` | 조각 하나의 최대 토큰 수 |
| `options.overlap` | `number` | `50` | 이웃한 조각끼리 겹치는 토큰 수 |

**반환값:** `string[]`

```js
const chunks = chunkText(document, { maxTokens: 800, overlap: 100 });
// 임베딩 생성이나 RAG 검색 색인에 활용
```

> **참고:** `overlap`을 적절히 주면 조각 경계에 걸친 문맥을 잃지 않습니다. 보통 `maxTokens`의 10~15%가 알맞습니다.

---

## estimateTokens(text)

텍스트의 토큰 수를 대략 계산합니다. 별도 토크나이저 없이 문자 종류(영문, 한글, 숫자, 기호)에 따라 근삿값을 냅니다.

**반환값:** `number`

```js
estimateTokens('안녕하세요, 반갑습니다.'); // 약 9
```

> **주의:** 추정치이므로 모델마다 실제 값과 10~20% 정도 차이가 날 수 있습니다. 과금이나 한도처럼 정확한 값이 필요하면 제공자의 공식 토큰 계산 API를 쓰세요.

---

## parseJSONSafe(raw, fallback)

모델 응답에서 JSON을 꺼내 파싱합니다. 코드 블록(```` ```json ````)이나 앞뒤 설명 문장이 섞여 있어도 JSON 부분만 찾아냅니다. 파싱에 실패하면 예외를 던지지 않고 `fallback`을 돌려줍니다.

| 매개변수 | 타입 | 설명 |
|---|---|---|
| `raw` | `string` | 모델의 원본 응답 |
| `fallback` | `any` | 실패할 때 돌려줄 값 (기본값 `null`) |

```js
const data = parseJSONSafe(response.text, { items: [] });
```

---

## retry(fn, options)

비동기 함수를 지수 백오프 방식으로 다시 실행합니다. 요청 한도 초과(429)나 일시적인 서버 오류에 대응할 때 유용합니다.

| 옵션 | 타입 | 기본값 | 설명 |
|---|---|---|---|
| `retries` | `number` | `3` | 최대 재시도 횟수 |
| `baseDelay` | `number` | `1000` | 첫 대기 시간(ms) |
| `shouldRetry` | `(err) => boolean` | 모든 오류 | 재시도할지 정하는 함수 |

```js
const result = await retry(() => client.generate(prompt), {
  retries: 5,
  shouldRetry: (err) => err.status === 429 || err.status >= 500,
});
```

---

## 모범 사례

- **API 키 보호:** 키는 서버 환경 변수에만 두고, 브라우저 코드에 넣지 마세요.
- **입력 검증:** 사용자 입력을 프롬프트에 넣기 전에 길이를 제한하고 `estimateTokens`로 한도를 넘지 않는지 확인하세요.
- **출력 검증:** 모델 응답은 항상 신뢰할 수 없는 데이터로 다루세요. `parseJSONSafe`로 파싱한 뒤 스키마 검증을 한 번 더 하는 것이 안전합니다.
