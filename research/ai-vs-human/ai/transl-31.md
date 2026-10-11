# 배열(Arrays)

**배열**은 여러 값을 하나의 변수에 순서대로 담을 수 있는 JavaScript의 전역 객체입니다. 리스트와 비슷한 고수준 객체이며, 순회와 변경에 쓰는 메서드를 내장하고 있습니다. JavaScript 배열은 길이와 요소의 자료형이 고정되어 있지 않습니다. 따라서 배열은 언제든 크기가 변할 수 있고, 서로 다른 자료형의 값을 함께 담을 수 있습니다.

## 설명

JavaScript 배열은 **0부터 시작하는 인덱스**를 사용합니다. 첫 번째 요소의 인덱스는 `0`이고, 마지막 요소의 인덱스는 `length - 1`입니다. 배열 요소는 일반 객체의 속성처럼 저장되지만, 숫자 인덱스로 접근하는 데 최적화되어 있습니다.

배열은 연속된 메모리 공간에 값을 나열하는 구조와 달리, JavaScript 엔진이 내부적으로 다양한 방식으로 최적화합니다. 그래서 동작 방식은 객체에 가깝지만, 숫자 키를 쓰는 일반적인 경우에는 매우 빠르게 동작합니다.

### 배열 만들기

가장 흔한 방법은 대괄호를 사용하는 **배열 리터럴**입니다.

```js
const fruits = ["사과", "바나나", "체리"];
console.log(fruits.length); // 3
```

`Array` 생성자나 `Array.of()`, `Array.from()`으로도 만들 수 있습니다.

```js
const a = new Array(3);        // 길이가 3인 빈 배열 (빈 슬롯 3개)
const b = Array.of(3);         // [3]
const c = Array.from("가나다"); // ["가", "나", "다"]
const d = Array.from({ length: 3 }, (_, i) => i * 2); // [0, 2, 4]
```

> **참고:** `new Array(3)`처럼 숫자 하나만 넘기면 요소가 3개인 배열이 아니라 **길이가 3인 빈 배열**이 만들어집니다. 의도치 않은 동작을 피하려면 리터럴이나 `Array.of()`를 사용하세요.

### 요소 접근하기

대괄호 표기법으로 인덱스를 지정해 요소에 접근합니다.

```js
const fruits = ["사과", "바나나", "체리"];

console.log(fruits[0]); // "사과"
console.log(fruits[2]); // "체리"
console.log(fruits[5]); // undefined

fruits[1] = "블루베리";
console.log(fruits); // ["사과", "블루베리", "체리"]
```

음수 인덱스로 끝에서부터 접근하려면 `at()` 메서드를 사용합니다.

```js
console.log(fruits.at(-1)); // "체리"
```

### length 속성

`length` 속성은 배열에 담긴 요소의 수를 나타내며, 가장 큰 인덱스보다 항상 1 큽니다. `length`에 값을 대입하면 배열을 줄이거나 늘릴 수 있습니다.

```js
const arr = [1, 2, 3, 4, 5];
arr.length = 3;
console.log(arr); // [1, 2, 3]
arr.length = 0;   // 배열 비우기
```

## 주요 메서드

### 요소 추가와 제거

| 메서드 | 설명 | 원본 변경 |
| --- | --- | --- |
| `push()` | 배열 끝에 요소를 추가하고 새 길이를 반환 | 예 |
| `pop()` | 배열 끝 요소를 제거하고 반환 | 예 |
| `unshift()` | 배열 앞에 요소를 추가하고 새 길이를 반환 | 예 |
| `shift()` | 배열 앞 요소를 제거하고 반환 | 예 |
| `splice()` | 지정한 위치의 요소를 제거하거나 교체·삽입 | 예 |
| `slice()` | 일부를 복사하여 새 배열로 반환 | 아니요 |
| `concat()` | 배열을 합쳐 새 배열을 반환 | 아니요 |

```js
const nums = [1, 2, 3];
nums.push(4);       // [1, 2, 3, 4]
nums.shift();       // [2, 3, 4]
nums.splice(1, 1);  // [2, 4]
```

### 순회와 변환

배열의 각 요소에 함수를 적용하는 고차 함수들이 있습니다.

```js
const nums = [1, 2, 3, 4, 5];

nums.forEach((n) => console.log(n));

const doubled = nums.map((n) => n * 2);          // [2, 4, 6, 8, 10]
const evens   = nums.filter((n) => n % 2 === 0); // [2, 4]
const sum     = nums.reduce((acc, n) => acc + n, 0); // 15
```

- `forEach()`: 각 요소에 대해 함수를 실행합니다. 반환값은 없습니다.
- `map()`: 각 요소를 변환한 새 배열을 반환합니다.
- `filter()`: 조건을 만족하는 요소만 모아 새 배열을 반환합니다.
- `reduce()`: 요소를 하나의 값으로 누적합니다.

`for...of` 반복문도 배열을 순회할 때 유용합니다.

```js
for (const [index, value] of ["a", "b"].entries()) {
  console.log(index, value); // 0 "a", 1 "b"
}
```

### 검색

```js
const nums = [10, 20, 30, 20];

nums.indexOf(20);          // 1
nums.lastIndexOf(20);      // 3
nums.includes(30);         // true
nums.find((n) => n > 15);  // 20
nums.findIndex((n) => n > 15); // 1
nums.some((n) => n > 25);  // true
nums.every((n) => n > 5);  // true
```

### 정렬과 뒤집기

`sort()`는 기본적으로 요소를 **문자열로 변환한 뒤 유니코드 순서**로 정렬합니다. 숫자를 정렬할 때는 반드시 비교 함수를 넘겨야 합니다.

```js
[10, 9, 1].sort();              // [1, 10, 9]  (의도와 다름)
[10, 9, 1].sort((a, b) => a - b); // [1, 9, 10]
```

`sort()`와 `reverse()`는 원본을 변경합니다. 원본을 유지하려면 `toSorted()`, `toReversed()`, `toSpliced()`, `with()` 같은 복사본 반환 메서드를 사용하세요.

```js
const original = [3, 1, 2];
const sorted = original.toSorted((a, b) => a - b);
console.log(original); // [3, 1, 2]
console.log(sorted);   // [1, 2, 3]
```

## 배열 복사와 전개

배열을 대입하면 값이 아니라 **참조**가 복사됩니다.

```js
const a = [1, 2, 3];
const b = a;
b.push(4);
console.log(a); // [1, 2, 3, 4]
```

독립된 복사본이 필요하면 전개 구문이나 `slice()`를 사용합니다. 다만 이 방법들은 **얕은 복사**이므로 중첩된 객체는 여전히 같은 참조를 공유합니다. 깊은 복사가 필요하면 `structuredClone()`을 사용하세요.

```js
const copy1 = [...a];
const copy2 = a.slice();
const deep  = structuredClone([{ x: 1 }]);
```

## 다차원 배열

배열은 다른 배열을 요소로 가질 수 있으므로 행렬 같은 다차원 구조를 표현할 수 있습니다. `flat()`으로 중첩을 평탄화할 수 있습니다.

```js
const matrix = [
  [1, 2, 3],
  [4, 5, 6],
];
console.log(matrix[1][2]); // 6
console.log(matrix.flat()); // [1, 2, 3, 4, 5, 6]
```

## 배열인지 확인하기

`typeof`는 배열에도 `"object"`를 반환하므로 `Array.isArray()`를 사용합니다.

```js
Array.isArray([1, 2]); // true
Array.isArray({});     // false
```

## 유사 배열 객체

`arguments`나 `NodeList`처럼 `length`와 인덱스를 가졌지만 배열 메서드가 없는 객체를 **유사 배열 객체**라고 합니다. `Array.from()`이나 전개 구문으로 진짜 배열로 바꿔 사용할 수 있습니다.

```js
const items = document.querySelectorAll("li");
const list = Array.from(items);
list.map((li) => li.textContent);
```

## 정리

- 배열은 순서가 있는 가변 길이 컬렉션이며 인덱스는 0부터 시작합니다.
- 원본을 변경하는 메서드(`push`, `splice`, `sort` 등)와 새 배열을 반환하는 메서드(`map`, `filter`, `slice`, `toSorted` 등)를 구분해서 사용하세요.
- 배열 대입은 참조 복사이므로, 복사본이 필요하면 전개 구문이나 `structuredClone()`을 사용하세요.
- 배열 여부는 `Array.isArray()`로 확인합니다.

## 같이 보기

- `Array` 생성자
- `TypedArray`
- `Map`과 `Set`
- 반복 프로토콜(Iteration protocols)
