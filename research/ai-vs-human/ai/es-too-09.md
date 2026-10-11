# retry

실패할 수 있는 비동기 함수를 지정한 횟수만큼 자동으로 다시 실행합니다. 네트워크 요청이나 외부 API 호출처럼 일시적인 오류가 잦은 작업에 적합합니다.

## 시그니처

```js
retry(fn, options?) => Promise<T>
```

## 매개변수

| 이름 | 타입 | 기본값 | 설명 |
|---|---|---|---|
| `fn` | `(attempt: number) => Promise<T>` | 필수 | 실행할 비동기 함수. 현재 시도 횟수(1부터 시작)를 인자로 받습니다. |
| `options.retries` | `number` | `3` | 최초 시도 이후 허용할 재시도 횟수 |
| `options.delay` | `number` | `1000` | 재시도 사이의 기본 대기 시간(ms) |
| `options.factor` | `number` | `2` | 대기 시간에 곱하는 지수 배수. `1`이면 고정 간격 |
| `options.maxDelay` | `number` | `30000` | 대기 시간의 상한(ms) |
| `options.shouldRetry` | `(error, attempt) => boolean` | `() => true` | `false`를 반환하면 즉시 중단하고 오류를 던집니다. |
| `options.signal` | `AbortSignal` | `undefined` | 신호가 발생하면 대기를 멈추고 `AbortError`를 던집니다. |

## 반환값

`fn`이 성공하면 그 결과로 이행되는 `Promise`를 반환합니다. 모든 시도가 실패하면 마지막으로 발생한 오류로 거부됩니다.

## 사용 예시

기본 사용:

```js
import { retry } from 'js-utils';

const data = await retry(() => fetch('/api/users').then(r => r.json()));
```

옵션 지정:

```js
const result = await retry(
  async (attempt) => {
    console.log(`${attempt}번째 시도`);
    const res = await fetch('/api/orders');
    if (!res.ok) throw new HttpError(res.status);
    return res.json();
  },
  {
    retries: 5,
    delay: 500,
    factor: 2,
    // 4xx 오류는 재시도해도 소용없으므로 즉시 중단
    shouldRetry: (err) => err.status >= 500,
  }
);
```

취소 가능한 재시도:

```js
const controller = new AbortController();
setTimeout(() => controller.abort(), 5000);

await retry(() => connect(), { retries: 10, signal: controller.signal });
```

## 동작 방식

- 대기 시간은 `delay * factor^(시도 횟수 - 1)`로 계산하며 `maxDelay`를 넘지 않습니다.
- `retries: 3`이면 최대 4번(최초 1회 + 재시도 3회) 실행됩니다.
- 마지막 시도가 실패하면 대기 없이 바로 오류를 던집니다.

## 주의사항

- 멱등하지 않은 작업(결제, 주문 생성 등)에는 중복 실행 위험이 있으므로 주의하세요.
- 여러 클라이언트가 동시에 재시도하면 서버에 부하가 몰릴 수 있습니다. 이런 경우 무작위 지연(jitter)을 함께 사용하세요.

## 관련 함수

- `timeout` — 작업에 제한 시간을 설정합니다.
- `sleep` — 지정한 시간만큼 대기합니다.
