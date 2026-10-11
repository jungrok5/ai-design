# Array.prototype.flatMap()

**`flatMap()`** 메서드는 배열의 각 요소에 주어진 콜백 함수를 적용한 뒤, 그 결과를 깊이 1까지 평탄화(flatten)한 새로운 배열을 반환합니다. `map()` 다음에 깊이 1의 `flat()`을 호출하는 것과 같지만, 두 작업을 하나로 합쳐 조금 더 효율적으로 동작합니다.

## 구문

```js
flatMap(callbackFn)
flatMap(callbackFn, thisArg)
```

### 매개변수

- `callbackFn`
  - 배열의 각 요소에 대해 실행할 함수입니다. 새 배열에 들어갈 요소를 포함하는 배열이나 단일 값을 반환해야 합니다. 함수는 다음 인수와 함께 호출됩니다.
    - `element`: 배열에서 처리 중인 현재 요소.
    - `index`: 배열에서 처리 중인 현재 요소의 인덱스.
    - `array`: `flatMap()`을 호출한 배열.
- `thisArg` (선택)
  - `callbackFn`을 실행할 때 `this`로 사용할 값입니다. [반복 메서드](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Array#반복_메서드)를 참고하세요.

### 반환 값

각 요소에 `callbackFn`을 적용하고 깊이 1로 평탄화한 결과를 담은 새로운 배열입니다.

## 설명

`flatMap()` 메서드는 [반복 메서드](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Array#반복_메서드)입니다. 콜백 함수의 동작 방식에 대한 자세한 내용은 [`Array.prototype.map()`](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Array/map)을 참고하세요. `flatMap()`은 `map()` 뒤에 `flat(1)`을 호출한 것과 동일합니다. 즉, 콜백이 반환한 값이 배열이면 그 배열의 요소가 결과 배열에 하나씩 펼쳐져 들어가고, 배열이 아니면 값 그대로 하나의 요소로 추가됩니다.

`flatMap()`은 단일 요소를 0개 또는 여러 개의 요소로 바꿔야 할 때 매우 유용합니다. 콜백이 빈 배열을 반환하면 해당 요소는 결과에서 사라지고, 길이가 2 이상인 배열을 반환하면 요소가 여러 개로 늘어납니다. 따라서 하나의 메서드로 `filter()`와 `map()`의 역할을 동시에 수행할 수 있습니다.

`flatMap()` 메서드는 호출한 배열을 변경하지 않습니다. 다만 `callbackFn`이 배열을 변경할 수는 있습니다. 또한 평탄화는 한 단계만 이루어지므로, 콜백이 중첩된 배열을 반환하면 안쪽 배열은 그대로 남습니다. 더 깊은 평탄화가 필요하다면 `flat()`에 깊이를 지정해 사용하세요.

`flatMap()`은 희소 배열의 빈 슬롯을 건너뜁니다. 한편 콜백이 반환한 값이 배열 형태의 객체(array-like)라 하더라도 펼쳐지지 않고 그대로 추가됩니다. 오직 실제 배열(`Array.isArray()`가 `true`인 값)만 평탄화됩니다.

### 대안

#### 요소 추가와 제거

`flatMap()`은 `map()` 도중에 항목을 추가하거나 제거하여 항목 수를 바꿀 수 있습니다. 항목이 하나씩 대응되어야 하는 `map()`과 달리, 입력 항목마다 출력 개수가 다를 수 있습니다. 빈 배열을 반환하면 항목이 제거되고, 요소가 여러 개인 배열을 반환하면 항목이 추가됩니다.

```js
// 음수는 제거하고, 홀수는 1과 나머지 짝수로 나누고, 짝수는 그대로 둡니다.
const a = [5, 4, -3, 20, 17, -33, -4, 18];
//         |\  \  x   |  | \   x   x   |
//        [4,1, 4,   20, 16, 1,       18]

const result = a.flatMap((n) => {
  if (n < 0) {
    return [];
  }
  return n % 2 === 0 ? [n] : [n - 1, 1];
});
console.log(result); // [4, 1, 4, 20, 16, 1, 18]
```

## 예제

### map()과 flatMap() 비교

```js
const arr1 = [1, 2, 1];

const result = arr1.flatMap((num) => (num === 2 ? [2, 2] : 1));

console.log(result);
// [1, 2, 2, 1]
```

`map()`만 사용하면 `[1, [2, 2], 1]`처럼 중첩 배열이 만들어지지만, `flatMap()`은 이를 한 단계 펼쳐 `[1, 2, 2, 1]`을 반환합니다.

```js
const arr1 = ["it's Sunny in", "", "California"];

console.log(arr1.map((x) => x.split(" ")));
// [["it's","Sunny","in"],[""],["California"]]

console.log(arr1.flatMap((x) => x.split(" ")));
// ["it's","Sunny","in", "", "California"]
```

### 한 단계만 평탄화됨

```js
const arr = [1, 2, 3, 4];

console.log(arr.flatMap((x) => [[x * 2]]));
// [[2], [4], [6], [8]]
```

콜백이 `[[x * 2]]`를 반환하므로 바깥 배열만 펼쳐지고 안쪽 배열은 유지됩니다.

### 배열 형태의 객체는 평탄화되지 않음

```js
const arrayLike = { length: 1, 0: "a" };

console.log([1, 2].flatMap(() => arrayLike));
// [{ length: 1, 0: "a" }, { length: 1, 0: "a" }]
```

### 희소 배열에서의 사용

```js
console.log([1, 2, , 4, 5].flatMap((x) => [x, x * 2]));
// [1, 2, 2, 4, 4, 8, 5, 10]

console.log([1, 2, 3].flatMap((x) => [, x * 2]));
// [4, 6, 8]
```

첫 번째 예에서는 빈 슬롯이 건너뛰어지고, 두 번째 예에서는 콜백이 반환한 희소 배열의 빈 슬롯이 무시됩니다.

### 배열이 아닌 값 반환하기

```js
console.log([1, 2, 3].flatMap((x) => x * 2));
// [2, 4, 6]
```

콜백이 배열이 아닌 값을 반환하면 `map()`과 동일하게 동작합니다.

### 문자열 처리와 단어 분리

```js
const sentences = ["안녕 하세요", "자바스크립트 배열"];

const words = sentences.flatMap((s) => s.split(" "));
console.log(words);
// ["안녕", "하세요", "자바스크립트", "배열"]
```

### 세 번째 인수 활용

```js
const items = ["a", "b", "c"];

const pairs = items.flatMap((item, index, array) => [
  item,
  `${index + 1}/${array.length}`,
]);
console.log(pairs);
// ["a", "1/3", "b", "2/3", "c", "3/3"]
```

## 명세서

| 명세서 |
| --- |
| [ECMAScript Language Specification](https://tc39.es/ecma262/multipage/indexed-collections.html#sec-array.prototype.flatmap) |

## 브라우저 호환성

`flatMap()`은 Chrome 69, Edge 79, Firefox 62, Safari 12 이상과 Node.js 11 이상에서 지원되며, 최신 브라우저에서는 별도 폴리필 없이 사용할 수 있습니다.

## 같이 보기

- [`Array.prototype.flat()`](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Array/flat)
- [`Array.prototype.map()`](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Array/map)
- [`Array.prototype.filter()`](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Array/filter)
- [`Array.prototype.reduce()`](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Array/reduce)
- [`Array.from()`](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Array/from)
