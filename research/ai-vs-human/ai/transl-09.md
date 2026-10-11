```markdown
---
title: 판단 내리기 — 조건문
slug: Learn/JavaScript/Building_blocks/conditionals
---

{{LearnSidebar}}

프로그래밍 언어에서도 코드는 사용자의 입력처럼 상황에 따라 판단을 내리고 그에 맞는 동작을 해야 합니다. 이 글에서는 JavaScript에서 **조건문**이 어떻게 작동하는지 알아봅니다.

| 사전 지식 | [HTML](/ko/docs/Learn/HTML), [CSS](/ko/docs/Learn/CSS), [JavaScript 첫걸음](/ko/docs/Learn/JavaScript/First_steps)에 대한 기본 이해 |
| --- | --- |
| 목표 | JavaScript에서 조건문을 사용하는 방법 이해하기 |

## 조건이 있는 삶

사람은 하루에도 수없이 많은 판단을 내립니다. "쿠키를 하나 먹을까, 두 개 먹을까?" 같은 사소한 결정부터 진로처럼 중요한 결정까지요. 이처럼 조건을 따져 보고 그 결과에 따라 행동을 선택하는 것을 코드로 표현한 것이 조건문입니다. 예를 들어 "쿠키가 남아 있다면 하나 먹고, 없다면 가게에 간다"는 판단을 코드로 그대로 옮길 수 있습니다.

## if...else 문

JavaScript에서 가장 흔히 쓰는 조건문은 [`if...else`](/ko/docs/Web/JavaScript/Reference/Statements/if...else)입니다.

### 기본 문법

```js
if (조건) {
  /* 조건이 참일 때 실행할 코드 */
} else {
  /* 조건이 거짓일 때 실행할 코드 */
}
```

1. 키워드 `if` 뒤에 괄호를 씁니다.
2. 괄호 안에는 검사할 조건을 넣습니다. 보통 비교 연산자를 사용하며, 결과는 `true` 또는 `false`가 됩니다.
3. 첫 번째 중괄호 안의 코드는 조건이 `true`일 때만 실행됩니다.
4. `else` 뒤 중괄호 안의 코드는 조건이 `false`일 때 실행됩니다.

`else` 부분은 꼭 쓰지 않아도 됩니다. 조건이 거짓일 때 할 일이 없다면 `if`만 써도 괜찮습니다.

### 실제 예제

```js
let shoppingDone = false;
let childsAllowance;

if (shoppingDone) {
  childsAllowance = 10;
} else {
  childsAllowance = 5;
}
```

위 코드에서 `shoppingDone`이 `false`이므로 아이는 용돈을 5만 받습니다. 장보기를 마친 뒤 이 변수를 `true`로 바꾸면 10을 받게 됩니다.

### else if

선택지가 두 개보다 많을 때는 `else if`를 이어서 붙이면 됩니다.

```js
const select = document.querySelector("select");
const para = document.querySelector("p");

select.addEventListener("change", setWeather);

function setWeather() {
  const choice = select.value;

  if (choice === "sunny") {
    para.textContent = "오늘은 화창해요. 반바지를 입고 바다에 가 보세요!";
  } else if (choice === "rainy") {
    para.textContent = "비가 오고 있어요. 우산을 챙기세요.";
  } else if (choice === "snowing") {
    para.textContent = "눈이 내려요! 눈사람을 만들어 볼까요?";
  } else {
    para.textContent = "";
  }
}
```

조건은 위에서부터 차례대로 검사되며, 처음으로 참이 되는 블록 하나만 실행됩니다.

### 비교 연산자

조건을 검사할 때는 다음과 같은 [비교 연산자](/ko/docs/Learn/JavaScript/First_steps/Math#비교_연산자)를 자주 씁니다.

- `===`, `!==` — 두 값이 같은지, 다른지 검사합니다.
- `<`, `>` — 한 값이 다른 값보다 작은지, 큰지 검사합니다.
- `<=`, `>=` — 작거나 같은지, 크거나 같은지 검사합니다.

> **참고:** 값을 비교하지 않고 변수만 넣어도 됩니다. `false`, `undefined`, `null`, `0`, `NaN`, 빈 문자열(`""`)은 거짓으로 취급되고(falsy), 나머지 값은 모두 참으로 취급됩니다(truthy).

### 논리 연산자: AND, OR, NOT

여러 조건을 한꺼번에 검사하려면 [논리 연산자](/ko/docs/Web/JavaScript/Reference/Operators#이진_논리_연산자)를 사용합니다.

- `&&` (AND) — 모든 조건이 참일 때만 참입니다.
- `||` (OR) — 조건 중 하나라도 참이면 참입니다.
- `!` (NOT) — 결과를 반대로 뒤집습니다.

```js
if (choice === "sunny" && temperature < 86) {
  para.textContent = "날씨가 맑고 기분 좋게 따뜻해요.";
} else if (choice === "sunny" && temperature >= 86) {
  para.textContent = "정말 더워요! 자외선 차단제를 꼭 바르세요.";
}

if (!(iceCreamVanOutside || houseStatus === "on fire")) {
  console.log("집에 그대로 있어도 괜찮아요.");
}
```

흔히 하는 실수는 `if (x === 5 || 7 || 10)`처럼 쓰는 것입니다. `7`은 항상 참이므로 이 조건은 언제나 참이 됩니다. 각각의 비교를 `x === 5 || x === 7 || x === 10`처럼 따로 써야 합니다.

## switch 문

하나의 값을 여러 선택지와 비교해야 한다면 `else if`를 길게 늘어놓는 대신 [`switch`](/ko/docs/Web/JavaScript/Reference/Statements/switch) 문을 쓰는 편이 읽기 쉽습니다.

```js
switch (choice) {
  case "sunny":
    para.textContent = "오늘은 화창해요.";
    break;
  case "rainy":
    para.textContent = "비가 오고 있어요.";
    break;
  default:
    para.textContent = "";
}
```

- `switch` 괄호 안의 값을 각 `case` 뒤의 값과 차례로 비교합니다.
- 일치하는 `case`를 찾으면 그 아래 코드를 실행합니다.
- `break`를 만나면 `switch` 문을 빠져나옵니다. `break`를 빠뜨리면 다음 `case`의 코드까지 이어서 실행되니 주의하세요.
- 일치하는 값이 없으면 `default`의 코드가 실행됩니다. `default`는 생략할 수 있습니다.

## 삼항 연산자

간단한 조건으로 둘 중 하나의 값을 고를 때는 [삼항 연산자](/ko/docs/Web/JavaScript/Reference/Operators/Conditional_operator)가 편리합니다.

```js
조건 ? 참일_때_실행할_코드 : 거짓일_때_실행할_코드;
```

```js
const greeting = isBirthday
  ? "생일 축하해요, 좋은 하루 보내세요!"
  : "좋은 아침이에요.";
```

코드가 짧아지지만, 너무 복잡한 조건에 쓰면 오히려 읽기 어려워집니다. 그럴 때는 `if...else`를 사용하세요.

## 직접 해 보기: 간단한 달력

`<select>`에서 달을 고르면 그 달의 일수를 정하는 코드를 직접 작성해 보세요.

```js
let days = 31;

if (choice === "2월") {
  days = 28;
} else if (
  choice === "4월" ||
  choice === "6월" ||
  choice === "9월" ||
  choice === "11월"
) {
  days = 30;
}
```

## 실력 점검하기

이 글의 끝에 도달했지만 중요한 내용을 기억하고 있나요? 다음 단계로 넘어가기 전에 [실력 점검: 조건문](/ko/docs/Learn/JavaScript/Building_blocks/Test_your_skills:_Conditionals)에서 확인해 보세요.

## 결론

지금까지 JavaScript에서 조건문을 사용하는 방법을 알아보았습니다. `if...else`, 비교·논리 연산자, `switch`, 삼항 연산자를 상황에 맞게 골라 쓰면 코드가 스스로 판단을 내리게 만들 수 있습니다. 이해되지 않는 부분이 있다면 글을 다시 읽어 보거나 [커뮤니티](/ko/docs/MDN/Community)에 도움을 요청하세요.

## 같이 보기

- [비교 연산자](/ko/docs/Learn/JavaScript/First_steps/Math#비교_연산자)
- [JavaScript 가이드: 제어 흐름과 에러 처리](/ko/docs/Web/JavaScript/Guide/Control_flow_and_error_handling)
- [`if...else`](/ko/docs/Web/JavaScript/Reference/Statements/if...else)
- [`switch`](/ko/docs/Web/JavaScript/Reference/Statements/switch)

{{NextMenu("Learn/JavaScript/Building_blocks/Looping_code", "Learn/JavaScript/Building_blocks")}}
```
