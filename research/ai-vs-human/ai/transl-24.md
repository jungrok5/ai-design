```markdown
---
title: Array.prototype[Symbol.iterator]()
slug: Web/JavaScript/Reference/Global_Objects/Array/Symbol.iterator
page-type: javascript-instance-method
browser-compat: javascript.builtins.Array.@@iterator
---

{{JSRef}}

{{jsxref("Array")}} 인스턴스의 **`[Symbol.iterator]()`** 메서드는 [순회 가능 프로토콜](/ko/docs/Web/JavaScript/Reference/Iteration_protocols)을 구현하여 배열을 [`for...of`](/ko/docs/Web/JavaScript/Reference/Statements/for...of) 반복문 같은 대부분의 구문에서 사용할 수 있게 합니다. 이 메서드는 배열의 각 인덱스에 해당하는 값을 내놓는 [배열 반복자 객체](/ko/docs/Web/JavaScript/Reference/Global_Objects/Iterator)를 반환합니다.

이 속성의 초기값은 {{jsxref("Array.prototype.values")}} 속성의 초기값과 같은 함수 객체입니다.

{{InteractiveExample("JavaScript Demo: Array.prototype[Symbol.iterator]()")}}

```js interactive-example
const array1 = ["a", "b", "c"];
const iterator1 = array1[Symbol.iterator]();

for (const value of iterator1) {
  console.log(value);
}

// 예상 결과: "a"
// 예상 결과: "b"
// 예상 결과: "c"
```

## 구문

```js-nolint
array[Symbol.iterator]()
```

### 매개변수

없음.

### 반환 값

{{jsxref("Array.prototype.values()")}}와 같은 반환 값입니다. 배열의 각 인덱스에 해당하는 값을 내놓는 새로운 [순회 가능한 반복자 객체](/ko/docs/Web/JavaScript/Reference/Global_Objects/Iterator)입니다.

## 설명

배열에 `for...of`를 사용하거나, 전개 구문(`...`)이나 구조 분해 할당을 적용하면 JavaScript 엔진은 내부적으로 이 메서드를 호출합니다. 따라서 대부분의 경우 이 메서드를 직접 호출할 필요는 없습니다.

이 메서드는 [범용](/ko/docs/Web/JavaScript/Reference/Global_Objects/Array#범용_배열_메서드)입니다. `this` 값에 `length` 속성과 정수 키 속성만 있으면 동작합니다.

## 예제

### for...of 반복문을 사용한 순회

이 메서드를 직접 호출하는 일은 드뭅니다. 배열이 순회 가능하다는 사실만으로 `for...of` 반복문에서 바로 사용할 수 있습니다.

```js
const arr = ["a", "b", "c", "d", "e"];
for (const letter of arr) {
  console.log(letter);
}
// "a" "b" "c" "d" "e"
```

### 반복자를 직접 순회하기

반환된 반복자 객체의 `next()` 메서드를 직접 호출하면 순회 과정을 세밀하게 제어할 수 있습니다.

```js
const arr = ["a", "b", "c", "d", "e"];
const arrIter = arr[Symbol.iterator]();
console.log(arrIter.next().value); // a
console.log(arrIter.next().value); // b
console.log(arrIter.next().value); // c
console.log(arrIter.next().value); // d
console.log(arrIter.next().value); // e
console.log(arrIter.next()); // { value: undefined, done: true }
```

### 문자열과 문자열 배열을 같은 함수로 처리하기

문자열과 배열은 모두 반복자 프로토콜을 구현하므로, 두 입력을 같은 방식으로 다루는 범용 함수를 작성할 수 있습니다. 아래 예제에서는 `Symbol.iterator`가 함수인지 확인하여 입력이 순회 가능한지 판별합니다.

```js
function logIterable(it) {
  if (typeof it[Symbol.iterator] !== "function") {
    console.log(it, "은(는) 순회 가능하지 않습니다.");
    return;
  }
  for (const letter of it) {
    console.log(letter);
  }
}

// 배열
logIterable(["a", "b", "c"]);
// a
// b
// c

// 문자열
logIterable("abc");
// a
// b
// c

// 숫자
logIterable(123);
// 123 은(는) 순회 가능하지 않습니다.
```

## 명세서

{{Specifications}}

## 브라우저 호환성

{{Compat}}

## 같이 보기

- [`core-js`의 `Array.prototype[Symbol.iterator]` 폴리필](https://github.com/zloirock/core-js#ecmascript-array)
- [인덱스 기반 컬렉션](/ko/docs/Web/JavaScript/Guide/Indexed_collections) 안내서
- {{jsxref("Array")}}
- {{jsxref("Array.prototype.keys()")}}
- {{jsxref("Array.prototype.entries()")}}
- {{jsxref("Array.prototype.values()")}}
- {{jsxref("TypedArray.prototype.@@iterator", "TypedArray.prototype[Symbol.iterator]()")}}
- {{jsxref("String.prototype.@@iterator", "String.prototype[Symbol.iterator]()")}}
- {{jsxref("Symbol.iterator")}}
- [순회 프로토콜](/ko/docs/Web/JavaScript/Reference/Iteration_protocols)
```
