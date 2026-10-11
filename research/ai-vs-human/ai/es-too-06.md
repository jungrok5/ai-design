# serialize

값을 문자열로 변환하는 직렬화 함수입니다. 일반 `JSON.stringify`가 처리하지 못하는 `Date`, `Map`, `Set`, `RegExp`, `BigInt`, `undefined`, 순환 참조까지 안전하게 다루며, 짝을 이루는 `deserialize`로 원래 값을 복원할 수 있습니다.

```js
import { serialize } from 'utilkit';
```

## 시그니처

```ts
function serialize(value: unknown, options?: SerializeOptions): string;
```

## 매개변수

### `value`

- 타입: `unknown`
- 필수

직렬화할 값입니다. 원시값, 객체, 배열, 내장 컬렉션 타입을 모두 받을 수 있습니다.

### `options`

- 타입: `SerializeOptions`
- 선택

| 옵션 | 타입 | 기본값 | 설명 |
| --- | --- | --- | --- |
| `space` | `number \| string` | `0` | 들여쓰기 칸 수 또는 문자열. 최대 10칸까지 적용됩니다. |
| `sortKeys` | `boolean` | `false` | `true`이면 객체 키를 사전순으로 정렬해 항상 같은 결과를 보장합니다. |
| `circular` | `'throw' \| 'ref' \| 'drop'` | `'ref'` | 순환 참조 처리 방식. `'throw'`는 오류, `'ref'`는 경로 참조로 대체, `'drop'`은 해당 속성 제거. |
| `maxDepth` | `number` | `Infinity` | 직렬화할 최대 깊이. 초과한 하위 값은 `"[MaxDepth]"`로 대체됩니다. |
| `replacer` | `(key, value) => unknown` | `undefined` | 각 값을 변환하기 전에 호출되는 사용자 정의 함수. |
| `exclude` | `string[]` | `[]` | 결과에서 제외할 속성 이름 목록. |
| `tagTypes` | `boolean` | `true` | 특수 타입에 `__type` 태그를 붙여 복원이 가능하도록 합니다. |

## 반환값

- 타입: `string`

직렬화된 문자열을 반환합니다. `tagTypes`가 `true`(기본값)이면 결과는 `deserialize`로 복원할 수 있는 형식이며, `false`이면 표준 JSON과 호환되는 단순 문자열이 됩니다.

## 지원하는 타입

| 입력 타입 | 직렬화 결과 |
| --- | --- |
| `Date` | `{"__type":"Date","value":"2026-01-01T00:00:00.000Z"}` |
| `Map` | `{"__type":"Map","value":[[k, v], ...]}` |
| `Set` | `{"__type":"Set","value":[v, ...]}` |
| `RegExp` | `{"__type":"RegExp","source":"a+","flags":"gi"}` |
| `BigInt` | `{"__type":"BigInt","value":"9007199254740993"}` |
| `undefined` | `{"__type":"undefined"}` |
| `NaN`, `Infinity` | `{"__type":"Number","value":"NaN"}` |
| `Error` | `name`, `message`, `stack`을 보존한 객체 |
| 함수, `Symbol` | 무시됩니다(배열 내부에서는 `null`). |

## 사용 예제

### 기본 사용

```js
serialize({ a: 1, b: 'text', c: [1, 2, 3] });
// '{"a":1,"b":"text","c":[1,2,3]}'
```

### 특수 타입 다루기

```js
const data = {
  createdAt: new Date('2026-01-01T00:00:00Z'),
  tags: new Set(['js', 'util']),
  big: 12345678901234567890n,
};

const text = serialize(data);
const restored = deserialize(text);

restored.createdAt instanceof Date; // true
restored.tags instanceof Set;       // true
restored.big === data.big;          // true
```

### 순환 참조

```js
const node = { name: 'root' };
node.self = node;

serialize(node);
// '{"name":"root","self":{"__ref":"$"}}'

serialize(node, { circular: 'drop' });
// '{"name":"root"}'

serialize(node, { circular: 'throw' });
// TypeError: Circular reference detected at "$.self"
```

### 키 정렬과 들여쓰기

```js
serialize({ b: 2, a: 1 }, { sortKeys: true, space: 2 });
// {
//   "a": 1,
//   "b": 2
// }
```

`sortKeys`는 해시 계산, 캐시 키 생성, 스냅샷 테스트처럼 같은 입력이 항상 같은 문자열이어야 하는 상황에서 유용합니다.

### 민감 정보 제외

```js
const user = { id: 1, name: 'Kim', password: 'secret', token: 'abc' };

serialize(user, { exclude: ['password', 'token'] });
// '{"id":1,"name":"Kim"}'
```

### 사용자 정의 replacer

```js
serialize(
  { price: 1200, name: 'item' },
  { replacer: (key, value) => (key === 'price' ? value / 100 : value) },
);
// '{"price":12,"name":"item"}'
```

`replacer`는 태그 처리보다 먼저 호출되므로, 변환 결과가 다시 특수 타입이면 정상적으로 태그가 붙습니다.

### 표준 JSON 출력

```js
serialize({ d: new Date(0), s: new Set([1]) }, { tagTypes: false });
// '{"d":"1970-01-01T00:00:00.000Z","s":[1]}'
```

이 모드는 외부 시스템으로 데이터를 보낼 때 적합하지만, 원래 타입으로는 복원할 수 없습니다.

## 동작 규칙

1. 객체의 `toJSON` 메서드가 있으면 먼저 호출한 뒤 그 결과를 직렬화합니다.
2. 열거 가능한 자체 속성만 포함하며, 프로토타입 속성은 무시합니다.
3. 클래스 인스턴스는 일반 객체로 직렬화되므로 복원 후 프로토타입은 유지되지 않습니다.
4. 키 순서는 `sortKeys`가 `false`이면 삽입 순서를 따릅니다.
5. `maxDepth`는 루트를 깊이 `0`으로 계산합니다.

## 오류

| 오류 | 발생 조건 |
| --- | --- |
| `TypeError` | `circular: 'throw'`에서 순환 참조를 발견했을 때 |
| `RangeError` | `maxDepth` 또는 `space`가 음수일 때 |
| `TypeError` | `replacer`가 함수가 아닌 값일 때 |

## 주의 사항

- 매우 큰 객체를 직렬화하면 메모리를 많이 사용할 수 있습니다. 대용량 데이터는 `maxDepth`나 `exclude`로 범위를 줄이세요.
- `__type`이라는 이름의 속성을 가진 사용자 객체는 복원 시 오해될 수 있으므로, 해당 속성은 `__type$`처럼 이스케이프되어 저장됩니다.
- 신뢰할 수 없는 입력을 `deserialize`로 복원할 때는 먼저 출처를 검증하세요. 직렬화 결과는 코드를 실행하지 않지만, 예상치 못한 크기의 데이터가 포함될 수 있습니다.

## 관련 함수

- [`deserialize`](./deserialize.md): 직렬화된 문자열을 원래 값으로 복원합니다.
- [`cloneDeep`](./cloneDeep.md): 문자열을 거치지 않고 값을 깊은 복사합니다.
- [`stableStringify`](./stableStringify.md): 키 정렬이 적용된 표준 JSON 문자열을 만듭니다.
