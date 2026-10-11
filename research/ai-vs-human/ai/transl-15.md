# 반복기 및 생성기

반복기(iterator)와 생성기(generator)는 반복 개념을 JavaScript 언어의 핵심 기능으로 가져와 {{jsxref("Statements/for...of", "for...of")}} 루프의 동작을 직접 정의할 수 있게 해 줍니다.

자세한 내용은 다음 문서도 함께 참고하세요.

- [반복 프로토콜](/ko/docs/Web/JavaScript/Reference/Iteration_protocols)
- {{jsxref("Statements/for...of", "for...of")}}
- {{jsxref("Statements/function*", "function*")}} 및 {{jsxref("Generator")}}
- {{jsxref("Operators/yield", "yield")}} 및 {{jsxref("Operators/yield*", "yield*")}}

## 반복기

JavaScript에서 **반복기**는 시퀀스를 정의하고, 끝에 도달했을 때 반환값을 함께 돌려줄 수 있는 객체입니다.

정확히 말하면, 반복기는 [반복기 프로토콜](/ko/docs/Web/JavaScript/Reference/Iteration_protocols#반복기_프로토콜)을 구현한 객체입니다. 이 객체에는 `next()` 메서드가 있어야 하며, 이 메서드는 두 개의 속성을 가진 객체를 반환합니다.

- `value`
  - : 반복 시퀀스의 다음 값입니다.
- `done`
  - : 시퀀스의 마지막 값을 이미 소비했다면 `true`입니다. `done`과 함께 `value`가 있으면 그 값은 반복기의 반환값입니다.

반복기 객체를 만든 뒤에는 `next()`를 반복해서 호출해 명시적으로 순회할 수 있습니다. 이처럼 반복기를 순회하는 것을 반복기를 *소비한다*고 하는데, 보통 한 번만 할 수 있기 때문입니다. 종료값이 나온 뒤에 `next()`를 더 호출하면 계속 `{ done: true }`를 반환해야 합니다.

가장 흔한 반복기는 배열 반복기로, 배열의 각 값을 차례대로 반환합니다. 모든 반복기를 배열로 표현할 수 있을 것 같지만 그렇지 않습니다. 배열은 전체 메모리를 할당해야 하지만, 반복기는 필요할 때만 값을 만들어 냅니다. 그래서 `0`부터 {{jsxref("Infinity")}}까지의 정수처럼 크기 제한이 없는 시퀀스도 나타낼 수 있습니다.

다음은 그런 반복기의 예시입니다. `start`(포함)부터 `end`(미포함)까지 `step` 간격으로 정수를 만드는 범위 반복기를 생성하며, 최종 반환값은 생성한 시퀀스의 크기입니다. 이 값은 `iterationCount` 변수에 저장됩니다.

```js
function makeRangeIterator(start = 0, end = Infinity, step = 1) {
  let nextIndex = start;
  let iterationCount = 0;

  const rangeIterator = {
    next() {
      let result;
      if (nextIndex < end) {
        result = { value: nextIndex, done: false };
        nextIndex += step;
        iterationCount++;
        return result;
      }
      return { value: iterationCount, done: true };
    },
  };
  return rangeIterator;
}
```

이 반복기는 다음과 같이 사용합니다.

```js
const iter = makeRangeIterator(1, 10, 2);

let result = iter.next();
while (!result.done) {
  console.log(result.value); // 1 3 5 7 9
  result = iter.next();
}

console.log("Iterated over sequence of size:", result.value); // [5 numbers returned, that took interval in between: 0 to 10]
```

> [!NOTE]
> 어떤 객체가 반복기인지 리플렉션으로 확인하는 방법은 없습니다. 꼭 확인해야 한다면 [반복 가능 객체](#반복_가능_객체)를 사용하세요.

## 생성기 함수

직접 만든 반복기는 유용하지만, 내부 상태를 직접 관리해야 하므로 신중하게 작성해야 합니다. **생성기 함수**는 강력한 대안입니다. 실행이 연속적이지 않은 하나의 함수만 작성하면 반복 알고리즘을 정의할 수 있습니다. 생성기 함수는 {{jsxref("Statements/function*", "function*")}} 문법으로 작성합니다.

생성기 함수를 호출해도 처음에는 코드가 실행되지 않습니다. 대신 **생성기**라는 특별한 종류의 반복기를 반환합니다. 생성기의 `next()` 메서드를 호출해 값을 소비하면, 생성기 함수는 `yield` 키워드를 만날 때까지 실행됩니다.

생성기 함수는 필요한 만큼 몇 번이든 호출할 수 있으며, 호출할 때마다 새로운 생성기를 반환합니다. 다만 각 생성기는 한 번만 순회할 수 있습니다.

위의 예시를 생성기로 바꾸면 다음과 같습니다. 두 코드의 동작은 같지만, 생성기 쪽이 훨씬 쓰기 쉽고 읽기도 쉽습니다.

```js
function* makeRangeIterator(start = 0, end = Infinity, step = 1) {
  let iterationCount = 0;
  for (let i = start; i < end; i += step) {
    iterationCount++;
    yield i;
  }
  return iterationCount;
}
```

## 반복 가능 객체

[반복 가능 프로토콜](/ko/docs/Web/JavaScript/Reference/Iteration_protocols#반복_가능_프로토콜)을 구현한 객체는 **반복 가능**합니다. 즉 `for...of` 구문에서 어떤 값을 순회할지와 같은 반복 동작을 정의합니다. {{jsxref("Array")}}와 {{jsxref("Map")}} 같은 내장 타입에는 기본 반복 동작이 있지만, {{jsxref("Object")}} 같은 타입에는 없습니다.

**반복 가능**하려면 객체에 {{jsxref("Symbol.iterator")}} 키를 가진 메서드가 있어야 합니다. 이 메서드는 반복기를 반환합니다.

반복 가능 객체는 한 번만 순회할 수도 있고(예: 생성기), 여러 번 순회할 수도 있습니다(예: 배열). 이는 프로그래머가 정하기 나름입니다.

### 사용자 정의 반복 가능 객체

다음과 같이 직접 반복 가능 객체를 만들 수 있습니다.

```js
const myIterable = {
  *[Symbol.iterator]() {
    yield 1;
    yield 2;
    yield 3;
  },
};
```

사용자 정의 반복 가능 객체는 일반 반복 가능 객체처럼 `for...of` 루프나 전개 구문에서 사용할 수 있습니다.

```js
for (const value of myIterable) {
  console.log(value);
}
// 1
// 2
// 3

[...myIterable]; // [1, 2, 3]
```

### 내장 반복 가능 객체

{{jsxref("String")}}, {{jsxref("Array")}}, {{jsxref("TypedArray")}}, {{jsxref("Map")}}, {{jsxref("Set")}}은 모두 내장 반복 가능 객체입니다. 각각의 프로토타입 객체에 `Symbol.iterator` 메서드가 있기 때문입니다.

### 반복 가능 객체를 받는 구문

`for...of` 루프, [전개 구문](/ko/docs/Web/JavaScript/Reference/Operators/Spread_syntax), `yield*`, [구조 분해](/ko/docs/Web/JavaScript/Reference/Operators/Destructuring) 같은 일부 구문과 표현식은 반복 가능 객체를 받습니다.

```js
for (const value of ["a", "b", "c"]) {
  console.log(value);
}
// "a"
// "b"
// "c"

[..."abc"]; // ["a", "b", "c"]

function* gen() {
  yield* ["a", "b", "c"];
}

gen().next(); // { value: "a", done: false }

const [a, b, c] = new Set(["a", "b", "c"]);
a; // "a"
```

## 고급 생성기

생성기는 필요할 때만 값을 계산하므로 계산 비용이 큰 시퀀스나 위에서 본 것과 같은 무한 시퀀스도 효율적으로 표현할 수 있습니다.

{{jsxref("Generator/next", "next()")}} 메서드는 인수를 받을 수도 있으며, 이 값으로 생성기의 내부 상태를 바꿀 수 있습니다. `next()`에 전달한 값은 `yield` 표현식의 결과가 됩니다. 단, 첫 번째 `next()` 호출에 전달한 값은 항상 무시됩니다.

> [!NOTE]
> 첫 번째 `next()` 호출에 전달한 값은 항상 무시됩니다.

다음 피보나치 생성기는 `next(x)`를 사용해 시퀀스를 다시 시작합니다.

```js
function* fibonacci() {
  let current = 0;
  let next = 1;
  while (true) {
    const reset = yield current;
    [current, next] = [next, next + current];
    if (reset) {
      current = 0;
      next = 1;
    }
  }
}

const sequence = fibonacci();
console.log(sequence.next().value); // 0
console.log(sequence.next().value); // 1
console.log(sequence.next().value); // 1
console.log(sequence.next().value); // 2
console.log(sequence.next().value); // 3
console.log(sequence.next().value); // 5
console.log(sequence.next().value); // 8
console.log(sequence.next(true).value); // 0
console.log(sequence.next().value); // 1
console.log(sequence.next().value); // 1
console.log(sequence.next().value); // 2
```

생성기의 {{jsxref("Generator/throw", "throw()")}} 메서드를 호출하면서 던질 예외 값을 전달하면 생성기 안에서 강제로 예외를 발생시킬 수 있습니다. 이 예외는 현재 일시 정지된 생성기 컨텍스트에서, 마치 일시 정지된 `yield`가 `throw value` 문인 것처럼 발생합니다.

생성기 내부에서 예외를 잡지 않으면 예외는 `throw()` 호출을 통해 바깥으로 전파되며, 이후 `next()`를 호출하면 `done` 속성이 `true`가 됩니다.

생성기에는 {{jsxref("Generator/return", "return()")}} 메서드도 있습니다. 이 메서드는 주어진 값을 반환하고 생성기 자체를 종료합니다.

{{PreviousNext("Web/JavaScript/Guide/Typed_arrays", "Web/JavaScript/Guide/Meta_programming")}}

---

중간에 있는 `console.log("Iterated over sequence of size:", result.value);` 줄의 주석에 실수가 있습니다. 바르게 고친 줄은 다음과 같습니다.

```js
console.log("Iterated over sequence of size:", result.value); // 5
```

"고급 생성기" 절에서는 `next()`의 첫 번째 인수가 무시된다는 설명이 본문과 `[!NOTE]` 상자에 두 번 들어가 있습니다. 둘 중 하나는 지우는 것이 좋습니다.

`{{jsxref}}`, `{{PreviousNext}}` 같은 매크로와 `[!NOTE]` 문법은 MDN 콘텐츠 저장소(Yari) 형식에 맞춘 것입니다. 이 페이지를 다른 곳에서 쓰려면 이 부분을 일반 링크로 바꿔야 합니다.
