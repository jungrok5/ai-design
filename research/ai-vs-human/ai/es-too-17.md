# flowAsync

`flowAsync`는 여러 함수를 왼쪽에서 오른쪽 순서로 이어 붙여 **비동기 함수 하나**로 만들어 줍니다. 각 함수의 반환값은 `await`로 처리된 뒤 다음 함수의 인자로 넘어갑니다. 그래서 동기 함수와 `Promise`를 반환하는 함수를 한 파이프라인에 함께 넣을 수 있습니다.

## 시그니처

```typescript
function flowAsync<A extends unknown[], R>(
  ...funcs: Array<(...args: any[]) => unknown>
): (...args: A) => Promise<Awaited<R>>;
```

## 매개변수

| 이름 | 타입 | 설명 |
| --- | --- | --- |
| `...funcs` | `Function[]` | 순서대로 실행할 함수 목록입니다. 첫 번째 함수만 인자를 여러 개 받을 수 있고, 나머지 함수는 직전 결과 하나만 받습니다. |

## 반환값

`(...args) => Promise<R>`: 합성된 비동기 함수를 반환합니다. 이 함수를 호출하면 마지막 함수의 결과로 이행(resolve)되는 `Promise`가 나옵니다.

## 예제

```javascript
import { flowAsync } from 'your-utils';

const fetchUser = async (id) => {
  const res = await fetch(`/api/users/${id}`);
  return res.json();
};
const getName = (user) => user.name;
const greet = (name) => `안녕하세요, ${name}님!`;

const greetUser = flowAsync(fetchUser, getName, greet);

await greetUser(42); // '안녕하세요, 홍길동님!'
```

첫 번째 함수에는 인자를 여러 개 넘길 수 있습니다.

```javascript
const sumThenDouble = flowAsync(
  async (a, b) => a + b,
  (n) => n * 2
);

await sumThenDouble(1, 2); // 6
```

## 동작 방식

- **순차 실행**: 앞 함수의 `Promise`가 이행된 뒤에야 다음 함수가 실행됩니다. 함수들을 병렬로 실행하지 않습니다.
- **에러 전파**: 중간 함수가 예외를 던지거나 `Promise`가 거부(reject)되면 남은 함수는 실행되지 않습니다. 반환된 `Promise`도 같은 에러로 거부됩니다.
- **`this` 바인딩**: 합성된 함수를 호출할 때의 `this`가 모든 함수에 그대로 전달됩니다.
- **빈 인자**: 함수를 하나도 넘기지 않으면 첫 번째 인자를 그대로 이행하는 함수를 반환합니다.

## 주의 사항

- 모든 함수가 동기 함수여도 결과는 항상 `Promise`입니다. 동기 결과만 필요하다면 `flow`를 쓰세요.
- 오른쪽에서 왼쪽 순서로 합성하려면 `flowRightAsync`를 쓰세요.

## 함께 보기

- [`flow`](./flow.md): 동기 함수를 합성합니다.
- [`flowRightAsync`](./flowRightAsync.md): 오른쪽에서 왼쪽 순서로 비동기 함수를 합성합니다.
- [`pipeAsync`](./pipeAsync.md): 값을 바로 넣어 비동기 파이프라인을 실행합니다.
