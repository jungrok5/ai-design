# findIndex (Lodash 호환성)

## 개요

`findIndex`는 배열을 앞에서부터 순회하며 `predicate` 함수가 `true`를 반환하는 첫 번째 요소의 인덱스를 반환합니다. 조건을 만족하는 요소가 없으면 `-1`을 반환합니다. 이 함수는 Lodash의 `_.findIndex`와 동일한 인자 규칙과 반환값을 따르므로, Lodash에서 이 라이브러리로 옮겨 올 때 코드를 거의 수정하지 않아도 됩니다.

## 시그니처

```js
findIndex(array, [predicate=identity], [fromIndex=0])
```

## 매개변수

| 이름 | 타입 | 기본값 | 설명 |
|------|------|--------|------|
| `array` | `Array` | - | 검색할 배열입니다. `null`이나 `undefined`이면 `-1`을 반환합니다. |
| `predicate` | `Function`, `Object`, `Array`, `string` | `identity` | 요소를 검사하는 조건입니다. 아래 단축 표현을 지원합니다. |
| `fromIndex` | `number` | `0` | 검색을 시작할 인덱스입니다. 음수이면 배열 끝에서부터 계산합니다. |

`predicate`는 `(value, index, array)` 인자를 받습니다.

## 단축 표현

- **객체**: `{ user: 'fred', active: true }`는 `_.matches`와 같이 속성 값이 모두 일치하는지 검사합니다.
- **배열**: `['active', true]`는 `_.matchesProperty`와 같이 속성 값이 일치하는지 검사합니다.
- **문자열**: `'active'`는 `_.property`와 같이 참조하는 속성의 truthy 여부를 검사합니다.

## 예제

```js
const users = [
  { user: 'barney',  active: false },
  { user: 'fred',    active: false },
  { user: 'pebbles', active: true }
];

findIndex(users, u => u.user === 'fred');   // 1
findIndex(users, { user: 'barney' });       // 0
findIndex(users, ['active', false]);        // 0
findIndex(users, 'active');                 // 2
findIndex(users, u => !u.active, 1);        // 1
findIndex(users, u => !u.active, -1);       // -1
findIndex(null, u => u);                    // -1
```

## Lodash 호환성

| 항목 | Lodash | 본 함수 |
|------|--------|---------|
| 반환값 (미발견) | `-1` | `-1` |
| 음수 `fromIndex` | 끝에서부터 계산 | 동일 |
| 단축 표현 | 객체, 배열, 문자열 지원 | 동일 |
| `null` 또는 `undefined` 배열 | `-1` | 동일 |

## 주의사항

- 이 함수는 조건을 만족하는 **첫 번째** 인덱스만 반환합니다. 모든 인덱스가 필요하면 `filter`와 `map`을 조합하세요.
- 희소 배열(sparse array)의 빈 칸도 `undefined` 값으로 순회됩니다.
- 배열의 값을 변경하지 않습니다.
