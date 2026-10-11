---
title: 함수 반환 값
slug: Learn/JavaScript/Building_blocks/Return_values
---

{{LearnSidebar}}

이 과정에서 함수에 대해 마지막으로 다룰 개념은 **반환 값**입니다. 함수 중에는 실행이 끝난 뒤 의미 있는 값을 돌려주지 않는 것도 있고, 값을 돌려주는 것도 있습니다. 반환 값이 무엇인지, 어떻게 활용하는지, 직접 만든 함수가 값을 반환하게 하려면 어떻게 하는지 알아 두어야 합니다.

| 선수 지식 | HTML과 CSS 기초, [JavaScript 첫걸음](/ko/docs/Learn/JavaScript/First_steps), [함수 — 재사용 가능한 코드 블록](/ko/docs/Learn/JavaScript/Building_blocks/Functions) |
| --- | --- |
| 학습 목표 | 함수 반환 값을 이해하고 활용하는 방법 익히기 |

## 반환 값이란?

**반환 값**은 함수가 실행을 마친 뒤 돌려주는 값입니다. 사실 여러분은 이미 반환 값을 여러 번 사용했습니다. 다음 코드를 살펴봅시다.

```js
const myText = "The weather is cold";
const newString = myText.replace("cold", "warm");
console.log(newString); // "The weather is warm"
```

[`replace()`](/ko/docs/Web/JavaScript/Reference/Global_Objects/String/replace) 메서드는 문자열에서 일부 문자열을 찾아 다른 문자열로 바꿉니다. 이때 원래 문자열 `myText`는 바뀌지 않습니다. 대신 치환이 적용된 **새 문자열을 반환**하며, 우리는 이 값을 `newString` 변수에 저장해 사용합니다.

반면 어떤 함수는 의미 있는 값을 반환하지 않습니다. 예를 들어 [`Array.prototype.forEach()`](/ko/docs/Web/JavaScript/Reference/Global_Objects/Array/forEach)는 각 요소에 대해 콜백을 실행할 뿐 결과로 [`undefined`](/ko/docs/Web/JavaScript/Reference/Global_Objects/undefined)를 반환합니다. 이런 함수는 값을 계산해 돌려주기보다 화면을 갱신하거나 콘솔에 출력하는 등 **부수 효과**를 위해 호출합니다.

> [!NOTE]
> JavaScript에서 `return` 문이 없는 함수는 항상 `undefined`를 반환합니다. 함수 이름만 보고 반환 값이 있는지 알 수 없을 때는 MDN 참고서의 각 함수 문서에 있는 "반환 값" 항목을 확인하세요.

## 직접 만든 함수에서 반환 값 사용하기

직접 만든 함수가 값을 반환하게 하려면 [`return`](/ko/docs/Web/JavaScript/Reference/Statements/return) 키워드를 사용합니다. 다음은 0 이상 `number` 미만의 정수 하나를 무작위로 반환하는 함수입니다.

```js
function random(number) {
  return Math.floor(Math.random() * number);
}
```

`return` 문은 두 가지 일을 합니다.

1. 뒤에 오는 표현식을 평가해 그 결과를 함수를 호출한 곳으로 돌려줍니다.
2. 그 즉시 함수 실행을 끝냅니다. `return` 뒤에 있는 코드는 실행되지 않습니다.

그래서 함수 호출식은 반환된 값으로 대체된다고 생각할 수 있습니다. 예를 들어 다음 코드에서

```js
ctx.arc(random(WIDTH), random(HEIGHT), random(50), 0, 2 * Math.PI);
```

`random()`을 세 번 호출하고 각 반환 값이 해당 자리에 들어갑니다. 첫 번째 호출이 `500`, 두 번째가 `200`, 세 번째가 `35`를 반환했다면 실제로는 다음과 같이 실행됩니다.

```js
ctx.arc(500, 200, 35, 0, 2 * Math.PI);
```

이렇게 함수 호출은 바깥쪽 코드가 실행되기 전에 먼저 평가됩니다.

### 조기 반환

`return`은 함수를 즉시 끝내므로, 조건에 맞지 않을 때 일찍 빠져나오는 용도로도 자주 쓰입니다.

```js
function divide(a, b) {
  if (b === 0) {
    return null; // 0으로 나눌 수 없으므로 여기서 끝냅니다.
  }
  return a / b;
}

console.log(divide(10, 2)); // 5
console.log(divide(10, 0)); // null
```

함수 끝까지 중첩된 `if...else`를 쓰는 대신 예외 상황을 먼저 처리하고 반환하면 코드를 읽기 쉬워집니다.

## 실습: 반환 값을 돌려주는 함수 만들기

숫자를 입력받아 여러 계산 결과를 보여 주는 간단한 페이지를 만들어 봅시다.

```html
<input class="numberInput" type="text" />
<p></p>
```

```js
const input = document.querySelector(".numberInput");
const para = document.querySelector("p");

function squared(num) {
  return num * num;
}

function cubed(num) {
  return num * num * num;
}

function factorial(num) {
  if (num < 0) return undefined;
  if (num === 0) return 1;
  let x = num - 1;
  while (x > 1) {
    num *= x;
    x--;
  }
  return num;
}

input.addEventListener("change", () => {
  const num = parseFloat(input.value);
  if (isNaN(num)) {
    para.textContent = "숫자를 입력해 주세요!";
  } else {
    para.textContent = `${num}의 제곱은 ${squared(num)}입니다. `;
    para.textContent += `${num}의 세제곱은 ${cubed(num)}입니다. `;
    para.textContent += `${num}의 팩토리얼은 ${factorial(num)}입니다.`;
  }
});
```

`squared()`, `cubed()`, `factorial()`은 모두 계산 결과를 반환할 뿐 화면에는 아무것도 직접 출력하지 않습니다. 출력은 이벤트 처리기가 맡습니다. 이처럼 **값을 계산하는 함수와 그 값을 사용하는 코드를 분리**하면 각 함수를 다른 곳에서도 재사용할 수 있고 테스트하기도 쉬워집니다.

> [!NOTE]
> [`isNaN()`](/ko/docs/Web/JavaScript/Reference/Global_Objects/isNaN) 역시 반환 값을 사용하는 함수입니다. 인수가 숫자가 아니면 `true`, 숫자면 `false`를 반환하므로 조건문에 바로 쓸 수 있습니다.

### 직접 해 보기

- 숫자가 음수일 때 `factorial()`이 `undefined`를 반환합니다. 이 경우 다른 안내 문구를 표시하도록 이벤트 처리기를 수정해 보세요.
- 원의 반지름을 받아 넓이를 반환하는 `circleArea()` 함수를 추가해 보세요. ([`Math.PI`](/ko/docs/Web/JavaScript/Reference/Global_Objects/Math/PI)를 사용하세요.)
- 숫자가 짝수인지 판별해 `true` 또는 `false`를 반환하는 `isEven()` 함수를 만들어 보세요.

## 여러 값 반환하기

`return` 문은 값 하나만 반환할 수 있습니다. 여러 값을 돌려주려면 배열이나 객체로 묶은 뒤 [구조 분해 할당](/ko/docs/Web/JavaScript/Reference/Operators/Destructuring_assignment)으로 꺼내 쓰면 됩니다.

```js
function minMax(numbers) {
  return { min: Math.min(...numbers), max: Math.max(...numbers) };
}

const { min, max } = minMax([3, 9, 1, 7]);
console.log(min, max); // 1 9
```

## 실력 점검

이 글을 다 읽었다면 핵심 내용을 기억하는지 [실력 점검: 함수](/ko/docs/Learn/JavaScript/Building_blocks/Test_your_skills:_Functions)에서 확인해 보세요.

## 결론

반환 값은 함수가 계산한 결과를 바깥으로 전달하는 통로입니다. `return`으로 값을 돌려주고 함수를 끝내며, `return`이 없으면 `undefined`가 반환된다는 점을 기억하세요. 반환 값을 잘 활용하면 작고 재사용 가능한 함수를 조합해 복잡한 프로그램을 만들 수 있습니다.

## 같이 보기

- [함수 심층 탐구](/ko/docs/Web/JavaScript/Reference/Functions)
- [`return` 문](/ko/docs/Web/JavaScript/Reference/Statements/return)
- [콜백 함수](/ko/docs/Glossary/Callback_function)

{{PreviousMenuNext("Learn/JavaScript/Building_blocks/Build_your_own_function", "Learn/JavaScript/Building_blocks/Events", "Learn/JavaScript/Building_blocks")}}
