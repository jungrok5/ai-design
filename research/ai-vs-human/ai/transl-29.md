# 실력을 평가해 보세요: 함수

이 페이지에서는 함수에 관해 배운 내용을 얼마나 이해했는지 점검합니다. 각 문제의 코드를 직접 실행하기 전에 결과를 예측해 보세요. 예측이 틀렸다면 그 이유를 생각해 보는 것이 가장 좋은 학습 방법입니다. 정답과 해설은 마지막 절에 있습니다.

## 문제 1: 함수 선언과 함수 표현식

다음 코드를 살펴보세요.

```js
console.log(add(2, 3));
console.log(multiply(2, 3));

function add(a, b) {
  return a + b;
}

const multiply = function (a, b) {
  return a * b;
};
```

**질문:** 두 `console.log`는 각각 무엇을 출력할까요? 두 번째 줄에서 어떤 일이 일어나는지도 설명해 보세요.

## 문제 2: 매개변수 기본값

다음 함수의 호출 결과를 예측해 보세요.

```js
function greet(name = "손님", greeting = `안녕하세요, ${name}`) {
  return `${greeting}!`;
}

console.log(greet());
console.log(greet("민수"));
console.log(greet(undefined, "반가워요"));
console.log(greet(null));
```

**질문:** 네 번째 호출에서 기본값이 적용되지 않는 이유는 무엇일까요?

## 문제 3: 나머지 매개변수

```js
function sumAll(first, ...rest) {
  return rest.reduce((total, n) => total + n, first);
}

console.log(sumAll(1, 2, 3, 4));
console.log(sumAll(10));
console.log(sumAll.length);
```

**질문:** 세 줄의 출력값을 각각 적어 보세요. `sumAll.length`는 왜 그 값이 되는지도 설명해 보세요.

## 문제 4: 클로저

```js
function makeCounter() {
  let count = 0;
  return {
    increment() {
      count += 1;
      return count;
    },
    reset() {
      count = 0;
    },
  };
}

const c1 = makeCounter();
const c2 = makeCounter();

console.log(c1.increment());
console.log(c1.increment());
console.log(c2.increment());
c1.reset();
console.log(c1.increment());
```

**질문:** 다섯 번째 줄의 출력값은 무엇일까요? `c1`과 `c2`가 서로 영향을 주지 않는 이유도 설명해 보세요.

## 문제 5: 화살표 함수와 `this`

다음 코드는 브라우저의 일반 스크립트에서 실행하며, 전역 `window.name`은 빈 문자열이라고 가정합니다.

```js
const user = {
  name: "지수",
  sayArrow: () => `나는 ${this.name}`,
  sayMethod() {
    return `나는 ${this.name}`;
  },
};

console.log(user.sayArrow());
console.log(user.sayMethod());
```

**질문:** 두 출력값은 각각 무엇인가요? 화살표 함수가 메서드 정의에 적합하지 않은 이유를 설명해 보세요.

---

## 정답 및 해설

### 문제 1 해설

첫 번째 줄은 `5`를 출력합니다. 함수 선언인 `add`는 코드 실행 전에 호이스팅되어 호출할 수 있습니다.

두 번째 줄에서는 `ReferenceError`가 발생합니다. `multiply`는 함수 표현식을 `const`로 선언한 변수입니다. 변수는 호이스팅되지만 선언문에 도달하기 전까지는 일시적 사각지대(TDZ)에 있어 접근할 수 없습니다. 따라서 `multiply`는 아직 초기화되지 않았고, 호출하는 순간 오류가 발생합니다.

### 문제 2 해설

출력 결과는 다음과 같습니다.

```
안녕하세요, 손님!
안녕하세요, 민수!
반가워요, 손님!
안녕하세요, null!
```

기본값은 인수가 `undefined`일 때만 적용됩니다. `null`은 값이 있는 것으로 취급되므로 `name`에는 `null`이 그대로 들어갑니다. 그 결과 `greeting`의 기본값 템플릿 문자열도 `null`을 사용해 `안녕하세요, null`이 됩니다.

### 문제 3 해설

출력 결과는 `10`, `10`, `1`입니다.

`sumAll(1, 2, 3, 4)`에서 `first`는 `1`이고 `rest`는 `[2, 3, 4]`입니다. `reduce`의 초깃값으로 `first`를 주었으므로 합계는 10입니다. `sumAll(10)`에서는 `rest`가 빈 배열이므로 결과는 `10`입니다.

`length` 속성은 기본값이나 나머지 매개변수 이전에 선언된 매개변수의 개수를 반환합니다. 나머지 매개변수 `...rest`는 세지 않으므로 값은 `1`입니다.

### 문제 4 해설

출력 결과는 `1`, `2`, `1`, `1`입니다.

`count`는 `makeCounter` 함수의 지역 변수입니다. `increment`와 `reset` 메서드는 이 변수를 참조하는 클로저를 만듭니다. 함수를 호출할 때마다 새로운 실행 컨텍스트와 새로운 `count`가 생성되므로 `c1`과 `c2`는 각자의 상태를 가집니다. 따라서 `c1.reset()` 이후 `c1.increment()`는 `1`을 반환합니다.

### 문제 5 해설

출력 결과는 `나는 ` 과 `나는 지수`입니다.

화살표 함수는 자신만의 `this`를 가지지 않습니다. 대신 정의된 위치의 바깥 스코프에서 `this`를 가져옵니다. 이 예제에서 `sayArrow`는 최상위 스코프에서 정의되었으므로 `this`는 `window`를 가리키고, `window.name`은 빈 문자열이므로 `나는 `이 출력됩니다.

반면 `sayMethod`는 일반 메서드 문법으로 정의되었습니다. 메서드로 호출되면 `this`는 호출한 객체인 `user`를 가리키므로 `나는 지수`가 출력됩니다. 따라서 객체의 메서드를 정의할 때는 일반 함수 문법을 사용하는 것이 안전합니다.
