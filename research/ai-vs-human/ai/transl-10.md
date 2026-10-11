# Array.prototype.toLocaleString()

**`Array.prototype.toLocaleString()`** 메서드는 배열의 요소를 나타내는 문자열을 반환합니다. 배열의 요소는 각각 자신의 `toLocaleString` 메서드를 사용해 문자열로 변환되며, 이 문자열은 로케일별 구분자(예: 쉼표 ",")로 이어 붙여집니다.

## 구문

```js
toLocaleString()
toLocaleString(locales)
toLocaleString(locales, options)
```

### 매개변수

- `locales` (선택)
  - BCP 47 언어 태그를 나타내는 문자열 또는 그러한 문자열의 배열입니다. `locales` 인수의 형식과 해석에 대해서는 `Intl` 페이지의 "매개변수" 부분을 참고하세요.
- `options` (선택)
  - 구성 속성을 가진 객체입니다. 숫자의 경우 `Number.prototype.toLocaleString()`을, 날짜의 경우 `Date.prototype.toLocaleString()`을 참고하세요.

### 반환 값

배열 요소를 로케일에 맞게 표현한 문자열입니다.

## 설명

`Array.prototype.toLocaleString` 메서드는 배열의 각 요소를 순회하며 `toLocaleString` 메서드를 호출하고, 그 결과를 구현체에서 정의한 구분자 문자열(예: 쉼표 ",")로 연결합니다. 이때 `locales`와 `options` 인수는 각 요소의 `toLocaleString` 호출에 그대로 전달됩니다.

배열 요소가 `undefined` 또는 `null`이면 `toLocaleString()`을 호출하지 않고 빈 문자열로 변환합니다.

구분자는 사용자 에이전트(브라우저)가 결정하므로, 구분자 문자열이 항상 쉼표라고 가정해서는 안 됩니다. 결과를 파싱해야 하는 용도라면 `Array.prototype.join()`을 사용하는 편이 안전합니다.

이 메서드는 범용(generic)입니다. 즉, `this` 값에 `length` 속성과 정수 키 속성만 있으면 배열이 아니어도 동작합니다.

순환 참조가 있는 배열에서는 순환되는 요소를 빈 문자열로 처리하여 무한 재귀를 방지합니다.

## 예제

### 로케일과 옵션 사용하기

배열의 요소는 `toLocaleString()` 메서드를 사용해 문자열로 변환됩니다.

- `Object`: `Object.prototype.toLocaleString()`
- `Number`: `Number.prototype.toLocaleString()`
- `Date`: `Date.prototype.toLocaleString()`

```js
const prices = ["¥7", 500, 8123, 12];

// 일본 엔화로 표시
console.log(
  prices.toLocaleString("ja-JP", { style: "currency", currency: "JPY" }),
);
// "¥7,¥500,¥8,123,¥12"

// 한국 원화로 표시
console.log(
  [1000, 25000].toLocaleString("ko-KR", { style: "currency", currency: "KRW" }),
);
// "₩1,000,₩25,000"
```

### 날짜가 포함된 배열

```js
const items = [1234.5, new Date(Date.UTC(2024, 0, 15, 12))];

console.log(items.toLocaleString("en-US", { timeZone: "UTC" }));
// "1,234.5,1/15/2024, 12:00:00 PM"

console.log(items.toLocaleString("ko-KR", { timeZone: "UTC" }));
// "1,234.5,2024. 1. 15. 오후 12:00:00"
```

### null과 undefined 처리

```js
const arr = [1, null, 2, undefined, 3];
console.log(arr.toLocaleString());
// "1,,2,,3"
```

### 희소 배열에서 toLocaleString() 사용하기

`toLocaleString()`은 빈 슬롯을 `undefined`와 동일하게 취급하여 빈 문자열을 생성합니다.

```js
console.log([1, , 3].toLocaleString()); // "1,,3"
```

### 배열이 아닌 객체에서 호출하기

```js
const arrayLike = {
  length: 3,
  0: 1000,
  1: 2000,
  2: 3000,
};

console.log(
  Array.prototype.toLocaleString.call(arrayLike, "en-US"),
);
// "1,000,2,000,3,000"
```

## 명세서

| 명세서 |
| --- |
| ECMAScript® Language Specification (`Array.prototype.toLocaleString`) |
| ECMAScript® 2026 Internationalization API Specification (`Array.prototype.toLocaleString`) |

## 브라우저 호환성

이 메서드는 모든 최신 브라우저(Chrome, Edge, Firefox, Safari, Opera)와 Node.js에서 지원됩니다. `locales`와 `options` 인수는 `Intl` API를 지원하는 환경에서 사용할 수 있습니다.

## 같이 보기

- [`Intl`](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Intl)
- [`Intl.ListFormat`](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Intl/ListFormat)
- [`Array.prototype.toString()`](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Array/toString)
- [`Array.prototype.join()`](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Array/join)
- [`TypedArray.prototype.toLocaleString()`](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/toLocaleString)
- [`Number.prototype.toLocaleString()`](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Number/toLocaleString)
- [`Date.prototype.toLocaleString()`](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Date/toLocaleString)
