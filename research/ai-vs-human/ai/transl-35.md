# Array.prototype.findLastIndex()

**`findLastIndex()`** 메서드는 배열을 뒤에서부터 순회하면서 주어진 판별 함수를 만족하는 **마지막 요소의 인덱스**를 반환합니다. 조건을 만족하는 요소가 하나도 없으면 `-1`을 반환합니다.

이 메서드는 ECMAScript 2023(ES2023)에서 추가되었으며, `Array.prototype.findIndex()`와 같은 방식으로 동작하지만 탐색 방향이 반대입니다.

## 구문

```js
findLastIndex(callbackFn)
findLastIndex(callbackFn, thisArg)
```

## 매개변수

- `callbackFn`
  - 각 요소에 대해 실행할 함수입니다. 다음 세 인자를 받습니다.
    - `element`: 현재 처리 중인 요소입니다.
    - `index`: 현재 요소의 인덱스입니다.
    - `array`: `findLastIndex()`가 호출된 배열입니다.
  - 조건을 만족하면 `true`(또는 truthy 값)를 반환합니다.
- `thisArg` (선택 사항)
  - `callbackFn`을 실행할 때 `this`로 사용할 값입니다. 화살표 함수에서는 무시됩니다.

## 반환 값

판별 함수가 truthy 값을 반환한 마지막 요소의 인덱스입니다. 그런 요소가 없으면 `-1`을 반환합니다.

## 설명

`findLastIndex()`는 배열의 마지막 인덱스(`length - 1`)에서 시작해 0번 인덱스까지 역방향으로 콜백을 호출합니다. 콜백이 truthy 값을 반환하는 순간 탐색을 멈추고 그 인덱스를 반환합니다. 따라서 조건을 만족하는 요소를 찾기 전까지만 콜백이 호출됩니다.

- 원본 배열을 변경하지 않습니다.
- 탐색 범위는 호출 시점의 `length`로 고정됩니다. 콜백 실행 중에 추가된 요소는 방문하지 않습니다.
- 희소 배열의 빈 슬롯도 방문하며, 이때 `element`는 `undefined`입니다.
- 배열이 비어 있으면 콜백을 한 번도 호출하지 않고 `-1`을 반환합니다.
- `callbackFn`이 함수가 아니면 `TypeError`가 발생합니다.
- 제네릭 메서드이므로 `length` 속성을 가진 array-like 객체에도 `Array.prototype.findLastIndex.call()`로 사용할 수 있습니다.

### findIndex()와의 차이

| 메서드 | 탐색 방향 | 반환 값 |
| --- | --- | --- |
| `findIndex()` | 앞에서 뒤로 | 처음 일치하는 인덱스 |
| `findLastIndex()` | 뒤에서 앞으로 | 마지막으로 일치하는 인덱스 |

두 메서드 모두 일치하는 요소가 없으면 `-1`을 반환합니다.

## 예제

### 마지막으로 짝수인 요소의 인덱스 찾기

```js
const numbers = [1, 3, 4, 7, 8, 9];

const index = numbers.findLastIndex((n) => n % 2 === 0);
console.log(index); // 4 (값은 8)
```

### 조건을 만족하는 요소가 없는 경우

```js
const fruits = ["apple", "banana", "cherry"];

console.log(fruits.findLastIndex((f) => f.startsWith("z"))); // -1
```

### 객체 배열에서 마지막 항목 찾기

```js
const inventory = [
  { name: "apples", quantity: 2 },
  { name: "bananas", quantity: 0 },
  { name: "cherries", quantity: 5 },
  { name: "oranges", quantity: 0 },
];

const lastEmptyIndex = inventory.findLastIndex((item) => item.quantity === 0);
console.log(lastEmptyIndex); // 3
```

### thisArg 사용하기

```js
const range = { min: 5 };
const values = [3, 7, 10, 2, 6];

const index = values.findLastIndex(function (v) {
  return v >= this.min;
}, range);
console.log(index); // 4 (값은 6)
```

## 명세

- [ECMAScript® 2023 Language Specification: Array.prototype.findLastIndex ( predicate [ , thisArg ] )](https://tc39.es/ecma262/multipage/indexed-collections.html#sec-array.prototype.findlastindex)

## 브라우저 호환성

`findLastIndex()`는 주요 브라우저에서 2023년부터 지원되는 기능입니다(Baseline 2023).

- Chrome 97 이상
- Edge 97 이상
- Firefox 104 이상
- Safari 15.4 이상

오래된 환경을 지원해야 한다면 최신 호환성 정보를 MDN의 브라우저 호환성 표에서 확인하세요.

## 관련 문서

- `Array.prototype.findLast()`
- `Array.prototype.findIndex()`
- `Array.prototype.find()`
- `Array.prototype.lastIndexOf()`
