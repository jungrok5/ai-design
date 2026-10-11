# findLastIndex (Lodash 호환성)

배열을 **끝에서부터** 순회하며 조건을 만족하는 첫 번째 요소의 인덱스를 반환합니다. 일치하는 요소가 없으면 `-1`을 반환합니다. Lodash의 `_.findLastIndex`와 동일한 동작을 제공하며, 기존 코드를 거의 수정 없이 옮길 수 있습니다.

## 시그니처

```ts
findLastIndex<T>(
  array: ArrayLike<T> | null | undefined,
  predicate?: ListIterateeCustom<T, boolean>,
  fromIndex?: number
): number
```

## 매개변수

| 이름 | 타입 | 설명 |
| --- | --- | --- |
| `array` | `ArrayLike<T> \| null \| undefined` | 검색할 배열 또는 유사 배열 객체 |
| `predicate` | 함수, 객체, 배열, 문자열 | 각 요소에 적용할 조건. 생략 시 항등 함수(truthy 검사)를 사용합니다. |
| `fromIndex` | `number` | 검색을 시작할 인덱스. 기본값은 `array.length - 1`입니다. |

## 반환값

`number` — 조건을 만족하는 마지막 요소의 인덱스. 없으면 `-1`.

## predicate 단축 표기

Lodash와 마찬가지로 다음 형태를 지원합니다.

- **함수**: `(value, index, array) => boolean`
- **객체**: `{ active: true }` — 모든 속성이 일치하는 요소를 찾습니다.
- **배열**: `['active', true]` — 지정한 속성과 값이 일치하는 요소를 찾습니다.
- **문자열**: `'active'` — 해당 속성이 truthy인 요소를 찾습니다.

## 사용 예시

```js
import { findLastIndex } from 'your-library/compat';

const users = [
  { user: 'barney', active: true },
  { user: 'fred', active: false },
  { user: 'pebbles', active: false },
];

findLastIndex(users, (u) => u.user === 'pebbles'); // 2
findLastIndex(users, { user: 'barney', active: true }); // 0
findLastIndex(users, ['active', false]); // 2
findLastIndex(users, 'active'); // 0

// fromIndex 지정
findLastIndex(users, ['active', false], 1); // 1

// 음수 fromIndex는 끝에서부터 계산
findLastIndex(users, 'active', -3); // 0
```

## Lodash와의 차이 및 주의사항

- `array`가 `null` 또는 `undefined`이면 오류 없이 `-1`을 반환합니다.
- `fromIndex`가 음수이면 `array.length + fromIndex`로 계산하며, 결과가 0보다 작으면 `0`으로 보정합니다.
- `fromIndex`가 배열 길이 이상이면 마지막 인덱스부터 검색합니다.
- 희소 배열의 빈 슬롯도 `undefined`로 간주하여 순회합니다.

## 참고

- 앞에서부터 검색하려면 `findIndex`를 사용하세요.
- 인덱스가 아닌 요소 자체가 필요하면 `findLast`를 사용하세요.
- 네이티브 `Array.prototype.findLastIndex`(ES2023)는 객체·문자열 단축 표기를 지원하지 않으므로, 해당 기능이 필요하면 이 호환 함수를 사용하세요.
