# pipe

여러 함수를 **왼쪽에서 오른쪽 순서로** 이어 붙여 하나의 함수로 합성합니다. 앞 함수의 반환값이 다음 함수의 인자로 전달됩니다.

## 시그니처

```ts
pipe<A extends unknown[], R>(
  fn1: (...args: A) => any,
  ...fns: Array<(arg: any) => any>
): (...args: A) => R
```

## 매개변수

| 이름 | 타입 | 설명 |
|------|------|------|
| `fn1` | `Function` | 처음 실행할 함수입니다. 인자를 여러 개 받을 수 있습니다. |
| `...fns` | `Function[]` | 이어서 실행할 함수들입니다. 각 함수는 인자를 하나만 받습니다. |

## 반환값

`(...args) => R`: 합성된 새 함수입니다. 호출하면 `fn1`부터 마지막 함수까지 차례로 실행하고, 마지막 함수의 결과를 돌려줍니다.

## 예제

### 기본 사용

```js
import { pipe } from 'my-utils';

const add = (a, b) => a + b;
const double = (x) => x * 2;
const toString = (x) => `결과: ${x}`;

const calc = pipe(add, double, toString);

calc(2, 3); // '결과: 10'
```

### 데이터 가공 파이프라인

```js
const getActiveUserNames = pipe(
  (users) => users.filter((u) => u.active),
  (users) => users.map((u) => u.name),
  (names) => names.sort()
);

getActiveUserNames([
  { name: '민수', active: true },
  { name: '지은', active: false },
  { name: '가람', active: true },
]); // ['가람', '민수']
```

## 주의 사항

- **실행 순서**: `pipe(f, g, h)(x)`는 `h(g(f(x)))`와 같습니다. 오른쪽에서 왼쪽으로 실행하려면 `compose`를 사용하세요.
- **단항 함수**: 첫 번째 함수를 뺀 나머지 함수는 인자를 하나만 받습니다. 인자가 여러 개 필요한 함수는 `curry`나 `partial`로 미리 인자를 채워 두세요.
- **비동기 미지원**: `Promise`를 반환하는 함수를 넣으면 다음 함수가 `Promise` 객체를 그대로 받습니다. 비동기 처리가 필요하면 `pipeAsync`를 사용하세요.
- **빈 호출**: 함수를 하나도 넘기지 않으면 `TypeError`가 발생합니다.

## 관련 항목

`compose`, `curry`, `partial`, `pipeAsync`
