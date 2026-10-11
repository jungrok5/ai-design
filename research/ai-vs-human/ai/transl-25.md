# Array.prototype.includes()

**`includes()`** 메서드는 배열이 특정 요소를 포함하고 있는지 판별하여 `true` 또는 `false`를 반환합니다.

## 구문

```js
includes(searchElement)
includes(searchElement, fromIndex)
```

### 매개변수

- `searchElement`
  - 배열에서 찾을 값입니다.
- `fromIndex` {{optional_inline}}
  - 검색을 시작할 위치(0부터 시작)입니다. [정수로 변환](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Number#정수_변환)되며, 기본값은 `0`입니다.
  - 음수이면 `array.length + fromIndex` 위치부터 검색합니다. 계산된 값이 `0`보다 작으면 배열 전체를 검색합니다.
  - `fromIndex >= array.length`이면 배열을 검색하지 않고 `false`를 반환합니다.

### 반환 값

배열(또는 `fromIndex`가 지정된 경우 그 위치부터의 부분)에 `searchElement`가 있으면 `true`, 없으면 `false`를 반환합니다.

## 설명

`includes()` 메서드는 [SameValueZero](https://developer.mozilla.org/ko/docs/Web/JavaScript/Equality_comparisons_and_sameness#same-value-zero_equality) 알고리즘을 사용해 `searchElement`와 배열의 각 요소를 비교합니다. 이 알고리즘에서는 `0`, `-0`, `+0`을 모두 같은 값으로 취급하며, `false`와는 같지 않습니다. 또한 `NaN`은 `NaN`과 같다고 간주합니다.

> **참고:** `indexOf()`는 엄격한 동등 비교(`===`)를 사용하므로 `NaN`을 찾지 못합니다. 따라서 `NaN`을 검색해야 한다면 `includes()`를 사용해야 합니다.

`includes()`는 [희소 배열](https://developer.mozilla.org/ko/docs/Web/JavaScript/Guide/Indexed_collections#희소_배열)의 빈 슬롯을 `undefined`로 취급하여 방문합니다.

`includes()`는 범용(generic) 메서드입니다. `this` 값에 `length` 속성과 정수 키 속성만 있으면 되므로, 배열과 유사한 객체에도 사용할 수 있습니다.

## 예제

### includes() 사용하기

```js
[1, 2, 3].includes(2); // true
[1, 2, 3].includes(4); // false
[1, 2, 3].includes(3, 3); // false
[1, 2, 3].includes(3, -1); // true
[1, 2, NaN].includes(NaN); // true
["1", "2", "3"].includes(3); // false
```

### fromIndex가 배열 길이 이상인 경우

```js
const arr = ["a", "b", "c"];

arr.includes("c", 3); // false
arr.includes("c", 100); // false
```

### 계산된 인덱스가 0보다 작은 경우

```js
const arr = ["a", "b"];

arr.includes("a", -100); // true
arr.includes("b", -100); // true
arr.includes("a", -2); // true
```

### 희소 배열에서 includes() 사용하기

```js
console.log([1, , 3].includes(undefined)); // true
```

### 배열이 아닌 객체에 includes() 호출하기

```js
const arrayLike = {
  length: 3,
  0: 1,
  1: 2,
  2: 3,
  3: 4, // length가 3이므로 includes()는 무시합니다.
};
console.log(Array.prototype.includes.call(arrayLike, 1)); // true
console.log(Array.prototype.includes.call(arrayLike, 4)); // false
```

## 명세서

| 명세서 |
| ------ |
| [ECMAScript Language Specification: Array.prototype.includes](https://tc39.es/ecma262/multipage/indexed-collections.html#sec-array.prototype.includes) |

## 브라우저 호환성

`Array.prototype.includes()`는 Chrome 47, Edge 14, Firefox 43, Safari 9, Node.js 6 이상에서 지원됩니다. Internet Explorer에서는 지원하지 않습니다.

## 같이 보기

- [`Array.prototype.indexOf()`](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Array/indexOf)
- [`Array.prototype.find()`](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Array/find)
- [`Array.prototype.findIndex()`](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Array/findIndex)
- [`Array.prototype.some()`](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Array/some)
- [`TypedArray.prototype.includes()`](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/includes)
- [`String.prototype.includes()`](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/String/includes)
