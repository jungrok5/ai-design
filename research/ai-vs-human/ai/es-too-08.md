# hash

전달받은 값으로 결정적(deterministic) 해시 값을 만듭니다. 문자열, 숫자, 배열, 일반 객체를 모두 받을 수 있으며, 같은 입력에는 항상 같은 결과를 돌려줍니다. 캐시 키 생성, 변경 감지, 중복 제거처럼 값을 빠르게 비교해야 할 때 쓰기 좋습니다.

> ⚠️ 이 함수는 **암호학적 해시가 아닙니다**. 비밀번호 저장, 서명, 무결성 검증에는 `crypto.subtle.digest` 같은 보안 API를 사용하세요.

## 문법

```js
hash(value[, options])
```

## 매개변수

| 이름 | 타입 | 기본값 | 설명 |
| --- | --- | --- | --- |
| `value` | `any` | — | 해시할 값입니다. 객체는 키를 정렬한 뒤 직렬화합니다. |
| `options.seed` | `number` | `0` | 해시 계산의 초기값입니다. 시드가 다르면 결과도 달라집니다. |
| `options.output` | `'number' \| 'hex'` | `'hex'` | 반환 형식입니다. |

## 반환 값

32비트 해시 값입니다. `output`이 `'hex'`이면 8자리 16진수 문자열을, `'number'`이면 부호 없는 정수를 반환합니다.

## 예외

- `value`에 순환 참조가 있으면 `TypeError`가 발생합니다.
- `seed`가 정수가 아니면 `RangeError`가 발생합니다.

## 예제

### 기본 사용

```js
import { hash } from 'utils';

hash('hello');          // 예: '4f9f2cab'
hash('hello');          // 항상 같은 값
hash('hello', { output: 'number' }); // 예: 1335831723
```

### 객체의 키 순서는 무시됩니다

```js
hash({ a: 1, b: 2 }) === hash({ b: 2, a: 1 }); // true
```

### 시드로 해시 공간 나누기

```js
const userKey = hash(id, { seed: 1 });
const postKey = hash(id, { seed: 2 });
```

## 참고 사항

- 결과가 32비트이므로 입력이 아주 많으면 서로 다른 값의 해시가 같아질(충돌) 수 있습니다. 정확히 같은지 확인해야 한다면 해시가 일치한 뒤에 원본 값을 한 번 더 비교하세요.
- `undefined`, 함수, `Symbol` 속성은 직렬화할 때 빠집니다.
- `Map`과 `Set`은 항목을 배열로 바꾼 뒤 해시합니다.

## 함께 보기

- [`isEqual`](./isEqual.md): 두 값이 깊은 수준까지 같은지 비교합니다.
- [`memoize`](./memoize.md): 결과를 캐시하는 함수를 만듭니다.
