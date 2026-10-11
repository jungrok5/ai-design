# debounce

연속으로 호출되는 함수를 마지막 호출 이후 일정 시간이 지난 뒤 **한 번만** 실행하도록 지연시키는 함수입니다. 검색창 자동완성, 창 크기 변경 처리, 폼 입력 검증처럼 짧은 시간에 이벤트가 반복되는 상황에서 불필요한 연산과 네트워크 요청을 줄이는 데 유용합니다.

## 시그니처

```ts
debounce<T extends (...args: any[]) => any>(
  func: T,
  wait?: number,
  options?: DebounceOptions
): DebouncedFunction<T>
```

## 매개변수

| 이름 | 타입 | 기본값 | 설명 |
| --- | --- | --- | --- |
| `func` | `Function` | - | 지연 실행할 함수 |
| `wait` | `number` | `0` | 마지막 호출 이후 대기할 시간(밀리초) |
| `options.leading` | `boolean` | `false` | `true`이면 대기 시작 시점에 먼저 실행 |
| `options.trailing` | `boolean` | `true` | `true`이면 대기 종료 시점에 실행 |
| `options.maxWait` | `number` | - | 실행이 미뤄질 수 있는 최대 시간(밀리초) |

## 반환값

디바운스된 함수를 반환합니다. 반환된 함수에는 다음 메서드가 있습니다.

- `cancel()`: 대기 중인 실행을 취소합니다.
- `flush()`: 대기 중인 실행을 즉시 수행하고 결과를 반환합니다.
- `pending()`: 실행 대기 중이면 `true`를 반환합니다.

## 사용 예시

```js
import { debounce } from 'my-utils';

const search = debounce((query) => {
  fetch(`/api/search?q=${query}`);
}, 300);

input.addEventListener('input', (e) => search(e.target.value));

// 컴포넌트 해제 시 정리
window.addEventListener('beforeunload', () => search.cancel());
```

`leading` 옵션을 사용하면 첫 호출은 즉시 처리하고 이후 연속 호출은 무시할 수 있습니다.

```js
const save = debounce(saveDraft, 1000, { leading: true, trailing: false });
```

## 주의 사항

- `wait`에 음수를 전달하면 `0`으로 처리됩니다.
- `leading`과 `trailing`이 모두 `false`이면 함수가 실행되지 않습니다.
- 원본 함수의 `this`와 인자는 마지막 호출 기준으로 전달됩니다.
- 지속적으로 호출되는 환경에서는 `maxWait`를 지정해 실행이 무한정 미뤄지는 것을 방지하세요.

## 관련 함수

- `throttle`: 일정 간격마다 최대 한 번 실행합니다.
- `once`: 함수를 단 한 번만 실행합니다.
