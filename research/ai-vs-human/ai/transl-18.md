# 함수 만들기

이전 글에서 함수의 기본 개념을 살펴보았습니다. 이번 글에서는 직접 함수를 만들어 봅니다. 함수의 기본 문법, 함수를 호출하는 방법, 매개변수를 정의하고 사용하는 방법을 하나씩 알아보겠습니다.

| | |
|---|---|
| **사전 지식:** | [HTML](/ko/docs/Learn/HTML)과 [CSS 기초](/ko/docs/Learn/CSS/First_steps), [JavaScript 첫걸음](/ko/docs/Learn/JavaScript/First_steps), [함수 — 재사용 가능한 코드 블록](/ko/docs/Learn/JavaScript/Building_blocks/Functions)에 대한 이해 |
| **목표:** | 사용자 정의 함수를 만들어 보고, 함수를 유용하게 만드는 세부 사항을 이해합니다. |

## 실습: 함수 만들기

이번에 만들 함수의 이름은 `displayMessage()`입니다. 웹 페이지에 사용자 정의 메시지 상자를 띄우는 함수로, 브라우저에 내장된 [`alert()`](/ko/docs/Web/API/Window/alert) 함수를 직접 만들어 보는 셈입니다. 브라우저 개발자 도구의 콘솔에 다음 코드를 입력해 보세요.

```js
alert("이것은 메시지입니다");
```

`alert()` 함수는 인수 하나를 받고, 그 문자열을 경고 상자에 표시합니다. 이제 이와 비슷하게 동작하는 함수를 만들어 보겠습니다.

> **참고:** 이 예제는 최신 브라우저에서 잘 동작하지만, 아주 오래된 브라우저에서는 스타일이 이상하게 보일 수 있습니다.

## 기본 함수

먼저 기본 함수를 작성해 봅시다.

1. [function-start.html](https://github.com/mdn/learning-area/blob/main/javascript/building-blocks/functions/function-start.html) 파일을 내려받아 로컬 컴퓨터에 저장합니다. HTML 구조는 간단합니다. `<body>`에는 버튼 하나가 있고, `<style>` 요소에는 메시지 상자를 꾸밀 CSS가 들어 있으며, 비어 있는 `<script>` 요소에 JavaScript 코드를 작성하게 됩니다.

2. 이제 `<script>` 요소 안에 다음 코드를 추가합니다.

   ```js
   function displayMessage() {
     const body = document.body;

     const panel = document.createElement("div");
     panel.setAttribute("class", "msgBox");
     body.appendChild(panel);

     const msg = document.createElement("p");
     msg.textContent = "이것은 메시지 상자입니다";
     panel.appendChild(msg);

     const closeBtn = document.createElement("button");
     closeBtn.textContent = "x";
     panel.appendChild(closeBtn);

     closeBtn.addEventListener("click", () =>
       panel.parentNode.removeChild(panel),
     );
   }
   ```

코드가 길어 보이지만 한 줄씩 살펴보면 어렵지 않습니다.

함수는 `function` 키워드로 시작합니다. 그 뒤에 함수 이름, 괄호 한 쌍, 중괄호 한 쌍이 차례로 옵니다. 함수에 넘길 매개변수는 괄호 안에 쓰고, 함수를 호출했을 때 실행할 코드는 중괄호 안에 씁니다.

- 첫 번째 줄은 [DOM API](/ko/docs/Web/API/Document_Object_Model)로 `<body>` 요소를 가져와 `body` 상수에 저장합니다.
- 다음 부분은 `document.createElement()`로 `<div>` 요소를 만들어 `panel` 상수에 저장합니다. 이 `<div>`가 메시지 상자의 바깥 틀이 됩니다. `setAttribute()`로 `class` 속성에 `msgBox` 값을 지정해 스타일을 적용하고, `appendChild()`로 `<body>` 안에 추가합니다.
- 그다음 두 부분에서는 `<p>`와 `<button>` 요소를 만들어 패널 안에 넣습니다. `<p>`의 [`textContent`](/ko/docs/Web/API/Node/textContent)에는 메시지를, 버튼에는 `x`를 넣습니다. 이 버튼은 사용자가 메시지 상자를 닫을 때 사용합니다.
- 마지막 부분은 [`addEventListener()`](/ko/docs/Web/API/EventTarget/addEventListener)로 버튼을 클릭했을 때 실행할 함수를 등록합니다. 이 함수는 패널을 부모 요소에서 제거해 메시지 상자를 닫습니다.

정리하면, `function` 키워드가 붙은 이 코드 블록 전체가 메시지 상자를 만들고 표시하는 함수의 본문입니다.

## 함수 호출하기

이제 함수를 정의했지만 아직 아무 일도 일어나지 않습니다. 정의만 했을 뿐 호출하지 않았기 때문입니다. 함수 아래에 다음 줄을 추가해 보세요.

```js
displayMessage();
```

이 줄은 함수를 호출해 즉시 실행합니다. 페이지를 새로 고치면 메시지 상자가 바로 나타납니다. 함수는 원할 때 언제든 다시 호출할 수 있습니다.

하지만 페이지를 열자마자 메시지가 뜨는 것은 그리 유용하지 않습니다. 실제 애플리케이션에서는 사용자의 동작이나 특정 상황에 반응해 메시지를 띄우는 경우가 대부분입니다. 방금 추가한 `displayMessage();` 줄을 지우고, 대신 다음 코드를 추가하세요.

```js
const btn = document.querySelector("button");
btn.addEventListener("click", displayMessage);
```

이제 버튼을 클릭할 때만 메시지 상자가 나타납니다.

여기서 `displayMessage` 뒤에 괄호를 붙이지 않았다는 점에 주의하세요. 괄호를 붙여 `displayMessage()`라고 쓰면 함수가 그 자리에서 바로 실행되고, 그 반환값이 이벤트 처리기로 등록됩니다. 괄호 없이 함수 이름만 넘겨야 "버튼을 클릭했을 때 이 함수를 실행해 달라"는 뜻이 됩니다. 직접 괄호를 붙여서 페이지를 새로 고쳐 보면 버튼을 누르지 않아도 메시지 상자가 나타나는 것을 확인할 수 있습니다.

## 매개변수로 함수 개선하기

지금의 함수는 항상 같은 메시지만 표시하므로 활용도가 낮습니다. 매개변수를 추가해 서로 다른 메시지와 아이콘을 표시할 수 있도록 개선해 보겠습니다.

1. 먼저 함수의 첫 줄을 다음과 같이 바꿉니다.

   ```js
   function displayMessage(msgText, msgType) {
   ```

   이제 함수를 호출할 때 괄호 안에 두 값을 넘길 수 있습니다. 첫 번째는 표시할 메시지, 두 번째는 메시지의 종류입니다.

2. 메시지 내용을 지정하는 줄을 다음과 같이 바꿔 첫 번째 매개변수를 사용합니다.

   ```js
   msg.textContent = msgText;
   ```

3. 마지막으로 이벤트 처리기를 수정합니다. 인수를 넘겨야 하므로 함수 이름만 넘길 수 없습니다. 대신 익명 함수 안에서 호출합니다.

   ```js
   btn.addEventListener("click", () =>
     displayMessage("안녕하세요. 반갑습니다!"),
   );
   ```

페이지를 새로 고치고 버튼을 클릭하면 인수로 넘긴 메시지가 표시됩니다.

### 조건문으로 메시지 종류 구분하기

두 번째 매개변수 `msgType`은 메시지 종류에 따라 아이콘과 배경색을 바꾸는 데 사용합니다. 함수 안의 적절한 위치에 다음 코드를 추가하세요.

```js
if (msgType === "warning") {
  msg.style.backgroundImage = "url(icons/warning.png)";
  panel.style.backgroundColor = "red";
} else if (msgType === "chat") {
  msg.style.backgroundImage = "url(icons/chat.png)";
  panel.style.backgroundColor = "aqua";
} else {
  msg.style.paddingLeft = "20px";
}
```

`msgType`이 `"warning"`이면 경고 아이콘과 빨간 배경이, `"chat"`이면 채팅 아이콘과 하늘색 배경이 표시됩니다. 값을 넘기지 않으면 아이콘 없이 기본 스타일을 사용합니다. 다음과 같이 호출해 확인해 보세요.

```js
displayMessage("인터넷 연결을 확인하세요.", "warning");
displayMessage("새 메시지가 도착했습니다.", "chat");
```

> **참고:** 예제가 제대로 동작하지 않는다면 GitHub에 있는 [완성된 버전](https://github.com/mdn/learning-area/blob/main/javascript/building-blocks/functions/function-stage-4.html)과 코드를 비교해 보세요.

## 마무리

지금까지 사용자 정의 함수를 직접 만들어 보았습니다. 조금만 더 다듬으면 실제 웹사이트에서도 충분히 쓸 수 있습니다. 다음 글에서는 함수가 값을 반환하는 방법을 알아봅니다.

## 같이 보기

- [함수 상세 가이드](/ko/docs/Web/JavaScript/Guide/Functions)
- [함수 참고서](/ko/docs/Web/JavaScript/Reference/Functions)
- [기본 매개변수](/ko/docs/Web/JavaScript/Reference/Functions/Default_parameters)
- [화살표 함수](/ko/docs/Web/JavaScript/Reference/Functions/Arrow_functions)

{{PreviousMenuNext("Learn/JavaScript/Building_blocks/Functions","Learn/JavaScript/Building_blocks/Return_values", "Learn/JavaScript/Building_blocks")}}
