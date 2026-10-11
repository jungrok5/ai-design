# 이벤트에 응답하기

React에서는 JSX에 **이벤트 핸들러(event handler)** 를 추가해 사용자의 동작에 반응할 수 있습니다. 이벤트 핸들러는 클릭, 마우스 호버, 폼 입력창 포커스 등 사용자 상호작용에 따라 실행되는 여러분의 함수입니다.

<YouWillLearn>

* 이벤트 핸들러를 작성하는 여러 가지 방법
* 부모 컴포넌트에서 이벤트 처리 로직을 전달하는 방법
* 이벤트가 전파되는 방식과 이를 멈추는 방법

</YouWillLearn>

## 이벤트 핸들러 추가하기

이벤트 핸들러를 추가하려면 먼저 함수를 정의한 다음, 그 함수를 적절한 JSX 태그에 prop으로 전달합니다. 예를 들어, 아직 아무 동작도 하지 않는 버튼은 다음과 같습니다.

```js
export default function Button() {
  return (
    <button>
      나를 클릭하세요
    </button>
  );
}
```

사용자가 버튼을 클릭할 때 메시지를 보여주려면 다음 세 단계를 따르세요.

1. `Button` 컴포넌트 *안에* `handleClick`이라는 함수를 선언합니다.
2. 함수 내부 로직을 구현합니다. (`alert`를 사용해 메시지를 보여줍니다.)
3. `<button>` JSX에 `onClick={handleClick}`을 추가합니다.

```js
export default function Button() {
  function handleClick() {
    alert('클릭하셨습니다!');
  }

  return (
    <button onClick={handleClick}>
      나를 클릭하세요
    </button>
  );
}
```

`handleClick` 함수를 정의한 뒤 `<button>`에 [prop으로 전달](/learn/passing-props-to-a-component)했습니다. 여기서 `handleClick`이 바로 **이벤트 핸들러**입니다. 이벤트 핸들러 함수는 다음과 같은 특징이 있습니다.

* 대개 컴포넌트 *안에* 정의됩니다.
* `handle`로 시작하고 그 뒤에 이벤트 이름을 붙인 이름을 가집니다.

관례상 이벤트 핸들러의 이름은 `handle`에 이벤트 이름을 붙여 짓습니다. `onClick={handleClick}`, `onMouseEnter={handleMouseEnter}` 같은 형태를 자주 보게 될 것입니다.

또는 JSX 안에서 인라인으로 이벤트 핸들러를 정의할 수도 있습니다.

```jsx
<button onClick={function handleClick() {
  alert('클릭하셨습니다!');
}}>
```

혹은 화살표 함수를 사용해 더 간결하게 작성할 수도 있습니다.

```jsx
<button onClick={() => {
  alert('클릭하셨습니다!');
}}>
```

이 방식들은 모두 동일하게 동작합니다. 인라인 이벤트 핸들러는 함수가 짧을 때 편리합니다.

<Pitfall>

이벤트 핸들러에 전달하는 함수는 호출하는 것이 아니라 *전달*되어야 합니다. 예를 들어 다음 표를 보세요.

| 함수를 전달하기 (올바름) | 함수를 호출하기 (잘못됨) |
| --- | --- |
| `<button onClick={handleClick}>` | `<button onClick={handleClick()}>` |

차이는 미묘합니다. 첫 번째 예시에서는 `handleClick` 함수가 `onClick` 이벤트 핸들러로 전달됩니다. 이는 React가 이 함수를 기억해 두었다가 사용자가 버튼을 클릭했을 때만 호출하도록 합니다.

두 번째 예시에서는 `handleClick()` 끝의 `()`가 [렌더링](/learn/render-and-commit) 도중, 클릭이 일어나지 않았는데도 *즉시* 함수를 실행합니다. [JSX의 `{`와 `}`](/learn/javascript-in-jsx-with-curly-braces) 사이에 있는 JavaScript는 바로 실행되기 때문입니다.

인라인 코드를 작성할 때도 같은 함정이 있습니다. 다음 두 코드는 서로 다르게 동작합니다.

| 함수를 전달하기 (올바름) | 함수를 호출하기 (잘못됨) |
| --- | --- |
| `<button onClick={() => alert('...')}>` | `<button onClick={alert('...')}>` |

인라인 함수를 전달하면 클릭할 때마다 실행되지만, 그렇지 않으면 클릭과 상관없이 컴포넌트가 렌더링될 때마다 코드가 실행됩니다.

핸들러를 직접 호출하는 대신 `onClick={() => handleClick()}`처럼 감싸 주세요.

</Pitfall>

## 이벤트 핸들러에서 props 읽기

이벤트 핸들러는 컴포넌트 내부에 선언되므로 컴포넌트의 props에 접근할 수 있습니다. 다음 버튼은 클릭하면 `message` prop을 담은 알림을 보여줍니다.

```js
function AlertButton({ message, children }) {
  return (
    <button onClick={() => alert(message)}>
      {children}
    </button>
  );
}

export default function Toolbar() {
  return (
    <div>
      <AlertButton message="재생 중!">
        영화 재생
      </AlertButton>
      <AlertButton message="업로드 중!">
        이미지 업로드
      </AlertButton>
    </div>
  );
}
```

이렇게 하면 두 버튼이 서로 다른 메시지를 보여줄 수 있습니다. 전달되는 메시지를 바꿔 보세요.

## 이벤트 핸들러를 prop으로 전달하기

부모 컴포넌트가 자식의 이벤트 핸들러를 지정하고 싶을 때가 있습니다. 예를 들어 버튼을 어디에서 사용하느냐에 따라 어떤 곳에서는 영화를 재생하고, 다른 곳에서는 이미지를 업로드해야 할 수 있습니다.

이럴 때는 컴포넌트가 부모로부터 받은 prop을 이벤트 핸들러로 전달하면 됩니다.

```js
function Button({ onClick, children }) {
  return (
    <button onClick={onClick}>
      {children}
    </button>
  );
}

function PlayButton({ movieName }) {
  function handlePlayClick() {
    alert(`${movieName} 재생 중!`);
  }

  return (
    <Button onClick={handlePlayClick}>
      "{movieName}" 재생
    </Button>
  );
}

function UploadButton() {
  return (
    <Button onClick={() => alert('업로드 중!')}>
      이미지 업로드
    </Button>
  );
}

export default function Toolbar() {
  return (
    <div>
      <PlayButton movieName="카키의 마법 배달" />
      <UploadButton />
    </div>
  );
}
```

여기서 `Toolbar` 컴포넌트는 `PlayButton`과 `UploadButton`을 렌더링합니다.

* `PlayButton`은 `handlePlayClick`을 `Button` 내부의 `onClick` prop으로 전달합니다.
* `UploadButton`은 `() => alert('업로드 중!')`을 `Button` 내부의 `onClick` prop으로 전달합니다.

마지막으로 `Button` 컴포넌트는 `onClick`이라는 prop을 받아 브라우저 내장 `<button>`에 `onClick={onClick}`으로 직접 전달합니다. 이렇게 하면 React는 클릭 시 전달받은 함수를 호출합니다.

[디자인 시스템](https://www.smashingmagazine.com/2020/03/setting-up-design-system-react/)을 사용한다면 버튼과 같은 컴포넌트는 스타일링만 담당하고 동작은 지정하지 않는 경우가 많습니다. 그 대신 `PlayButton`과 `UploadButton`처럼 이벤트 핸들러를 아래로 전달합니다.

## 이벤트 핸들러 prop 이름 정하기

`<button>`이나 `<div>` 같은 내장 컴포넌트는 `onClick`과 같은 [브라우저 이벤트 이름](/reference/react-dom/components/common#common-props)만 지원합니다. 하지만 직접 만드는 컴포넌트에서는 이벤트 핸들러 prop의 이름을 원하는 대로 정할 수 있습니다.

관례상 이벤트 핸들러 prop은 `on`으로 시작하고 그 뒤에 대문자로 시작하는 이름을 붙입니다.

예를 들어 `Button` 컴포넌트의 `onClick` prop은 `onSmash`라고 불러도 됩니다.

```js
function Button({ onSmash, children }) {
  return (
    <button onClick={onSmash}>
      {children}
    </button>
  );
}

export default function App() {
  return (
    <div>
      <Button onSmash={() => alert('재생 중!')}>
        영화 재생
      </Button>
      <Button onSmash={() => alert('업로드 중!')}>
        이미지 업로드
      </Button>
    </div>
  );
}
```

이 예시에서 `<button onClick={onSmash}>`는 브라우저의 `<button>`(소문자)이 여전히 `onClick`이라는 prop을 필요로 한다는 것을 보여줍니다. 하지만 사용자 정의 `Button` 컴포넌트가 받는 prop 이름은 여러분이 정할 수 있습니다.

컴포넌트가 여러 상호작용을 지원할 때는 앱에 특화된 이름으로 이벤트 핸들러 prop을 만들 수 있습니다. 예를 들어 `Toolbar` 컴포넌트는 `onPlayMovie`와 `onUploadImage`를 받을 수 있습니다.

```js
export default function App() {
  return (
    <Toolbar
      onPlayMovie={() => alert('재생 중!')}
      onUploadImage={() => alert('업로드 중!')}
    />
  );
}

function Toolbar({ onPlayMovie, onUploadImage }) {
  return (
    <div>
      <Button onClick={onPlayMovie}>
        영화 재생
      </Button>
      <Button onClick={onUploadImage}>
        이미지 업로드
      </Button>
    </div>
  );
}

function Button({ onClick, children }) {
  return (
    <button onClick={onClick}>
      {children}
    </button>
  );
}
```

`App` 컴포넌트는 `Toolbar`가 `onPlayMovie`나 `onUploadImage`로 *무엇을 할지* 알 필요가 없습니다. 그것은 `Toolbar`의 구현 세부 사항입니다. `Toolbar`는 이 핸들러를 `Button`의 `onClick`으로 전달할 뿐입니다. 이처럼 prop 이름을 용도에 맞게 지으면 나중에 사용 방식을 바꾸기 쉬워집니다.

<Note>

이벤트 핸들러에는 적절한 HTML 태그를 사용해야 합니다. 예를 들어 클릭을 처리하려면 `<div onClick={handleClick}>` 대신 [`<button onClick={handleClick}>`](https://developer.mozilla.org/docs/Web/HTML/Element/button)을 사용하세요. 실제 브라우저의 `<button>`은 키보드 내비게이션 같은 내장 브라우저 동작을 지원합니다. 버튼의 기본 브라우저 스타일이 마음에 들지 않아 링크나 다른 UI 요소처럼 보이게 하고 싶다면 CSS로 원하는 모양을 만들 수 있습니다. [접근성을 위한 마크업 작성법에 대해 더 알아보세요.](https://developer.mozilla.org/docs/Learn/Accessibility/HTML)

</Note>

## 이벤트 전파

이벤트 핸들러는 해당 컴포넌트가 가진 자식 컴포넌트에서 발생한 이벤트도 감지합니다. 이를 이벤트가 트리를 따라 "버블링" 또는 "전파"된다고 표현합니다. 이벤트는 발생한 곳에서 시작해 트리를 따라 위로 올라갑니다.

다음 `<div>`는 두 개의 버튼을 포함합니다. `<div>`와 각 버튼에는 모두 자신만의 `onClick` 핸들러가 있습니다. 버튼을 클릭하면 어떤 핸들러가 실행될까요?

```js
export default function Toolbar() {
  return (
    <div className="Toolbar" onClick={() => {
      alert('툴바를 클릭하셨습니다!');
    }}>
      <button onClick={() => alert('재생 중!')}>
        영화 재생
      </button>
      <button onClick={() => alert('업로드 중!')}>
        이미지 업로드
      </button>
    </div>
  );
}
```

버튼 중 하나를 클릭하면 해당 버튼의 `onClick`이 먼저 실행되고, 이어서 부모 `<div>`의 `onClick`이 실행됩니다. 따라서 메시지가 두 개 나타납니다. 툴바 자체를 클릭하면 부모 `<div>`의 `onClick`만 실행됩니다.

<Pitfall>

`onScroll`을 제외한 모든 이벤트는 React에서 전파됩니다. `onScroll`은 이를 붙인 JSX 태그에서만 동작합니다.

</Pitfall>

### 전파 멈추기

이벤트 핸들러는 **이벤트 객체**를 유일한 인수로 받습니다. 관례상 "event"를 뜻하는 `e`라고 부르는 경우가 많습니다. 이 객체로 이벤트에 대한 정보를 읽을 수 있습니다.

이벤트 객체를 통해 전파를 멈출 수도 있습니다. 이벤트가 상위 컴포넌트에 도달하지 못하게 하려면 다음 `Button` 컴포넌트처럼 `e.stopPropagation()`을 호출해야 합니다.

```js
function Button({ onClick, children }) {
  return (
    <button onClick={e => {
      e.stopPropagation();
      onClick();
    }}>
      {children}
    </button>
  );
}

export default function Toolbar() {
  return (
    <div className="Toolbar" onClick={() => {
      alert('툴바를 클릭하셨습니다!');
    }}>
      <Button onClick={() => alert('재생 중!')}>
        영화 재생
      </Button>
      <Button onClick={() => alert('업로드 중!')}>
        이미지 업로드
      </Button>
    </div>
  );
}
```

버튼을 클릭하면 다음과 같은 일이 일어납니다.

1. React가 `<button>`에 전달된 `onClick` 핸들러를 호출합니다.
2. `Button`에 정의된 이 핸들러는 다음을 수행합니다.
   * `e.stopPropagation()`을 호출해 이벤트가 더 위로 전파되는 것을 막습니다.
   * `Toolbar` 컴포넌트가 전달한 `onClick` 함수를 호출합니다.
3. `Toolbar` 컴포넌트에 정의된 이 함수가 버튼의 알림을 보여줍니다.
4. 전파가 멈췄으므로 부모 `<div>`의 `onClick` 핸들러는 실행되지 않습니다.

`e.stopPropagation()` 덕분에 이제 버튼을 클릭해도 `<div>` 툴바의 알림은 나타나지 않고 버튼의 알림만 나타납니다. 버튼 클릭과 주변 툴바 클릭은 다르므로, 이 UI에서는 전파를 막는 것이 적절합니다.

<DeepDive>

#### 캡처 단계 이벤트

드물지만 자식 요소가 전파를 멈추더라도 *모든* 이벤트를 잡아야 할 때가 있습니다. 예를 들어 전파 로직과 상관없이 분석을 위해 모든 클릭을 기록하고 싶을 수 있습니다. 이벤트 이름 끝에 `Capture`를 붙이면 됩니다.

```js
<div onClickCapture={() => { /* 이 코드가 먼저 실행됩니다 */ }}>
  <button onClick={e => e.stopPropagation()} />
  <button onClick={e => e.stopPropagation()} />
</div>
```

각 이벤트는 세 단계로 전파됩니다.

1. 아래로 내려가면서 모든 `onClickCapture` 핸들러를 호출합니다.
2. 클릭된 요소의 `onClick` 핸들러를 실행합니다.
3. 위로 올라가면서 모든 `onClick` 핸들러를 호출합니다.

캡처 이벤트는 라우터나 분석 라이브러리 같은 코드에는 유용하지만, 일반 앱 코드에서는 사용할 일이 거의 없을 것입니다.

</DeepDive>

### 전파의 대안으로 핸들러 전달하기

이 클릭 핸들러가 어떻게 한 줄의 코드를 실행한 *다음* 부모가 전달한 `onClick` prop을 호출하는지 살펴보세요.

```js
function Button({ onClick, children }) {
  return (
    <button onClick={e => {
      e.stopPropagation();
      onClick();
    }}>
      {children}
    </button>
  );
}
```

이 핸들러에 `onClick`을 호출하기 전에 코드를 더 추가할 수도 있습니다. 이 패턴은 전파의 *대안*이 됩니다. 자식 컴포넌트가 이벤트를 처리하면서도 부모 컴포넌트가 추가 동작을 지정할 수 있게 해 줍니다. 전파와 달리 자동으로 일어나지 않습니다. 하지만 이 패턴의 장점은 어떤 이벤트의 결과로 실행되는 코드 연쇄를 명확하게 따라갈 수 있다는 점입니다.

전파에 의존하고 있어서 어떤 핸들러가 왜 실행되는지 추적하기 어렵다면 이 방식을 대신 시도해 보세요.

### 기본 동작 방지하기

일부 브라우저 이벤트에는 기본 동작이 연결되어 있습니다. 예를 들어 `<form>`의 제출 이벤트는 내부 버튼을 클릭하면 발생하며, 기본적으로 페이지 전체를 새로고침합니다.

```js
export default function Signup() {
  return (
    <form onSubmit={() => alert('제출 중!')}>
      <input />
      <button>보내기</button>
    </form>
  );
}
```

이벤트 객체의 `e.preventDefault()`를 호출하면 이를 막을 수 있습니다.

```js
export default function Signup() {
  return (
    <form onSubmit={e => {
      e.preventDefault();
      alert('제출 중!');
    }}>
      <input />
      <button>보내기</button>
    </form>
  );
}
```

`e.stopPropagation()`과 `e.preventDefault()`를 혼동하지 마세요. 둘 다 유용하지만 서로 관련이 없습니다.

* [`e.stopPropagation()`](https://developer.mozilla.org/docs/Web/API/Event/stopPropagation)은 위쪽 태그에 연결된 이벤트 핸들러가 실행되지 않도록 막습니다.
* [`e.preventDefault()`](https://developer.mozilla.org/docs/Web/API/Event/preventDefault)는 기본 브라우저 동작이 있는 몇몇 이벤트에서 그 기본 동작을 막습니다.

## 이벤트 핸들러에 부수 효과가 있어도 될까요?

물론입니다! 이벤트 핸들러는 부수 효과를 일으키기에 가장 좋은 장소입니다.

렌더링 함수와 달리 이벤트 핸들러는 [순수](/learn/keeping-components-pure)할 필요가 없습니다. 따라서 입력값을 바꾸거나, 사용자의 입력에 따라 무언가를 변경하는 등 *무언가를 바꾸기에* 좋은 장소입니다. 다만 어떤 정보를 바꾸려면 먼저 그 정보를 저장할 방법이 필요합니다. React에서는 컴포넌트의 기억 장치인 [state](/learn/state-a-components-memory)를 사용합니다. 다음 페이지에서 이에 대해 자세히 배우게 됩니다.

<Recap>

* `<button>` 같은 요소에 함수를 prop으로 전달하여 이벤트를 처리할 수 있습니다.
* 이벤트 핸들러는 호출이 아니라 **전달**해야 합니다. `onClick={handleClick()}`이 아니라 `onClick={handleClick}`입니다.
* 이벤트 핸들러 함수는 따로 정의하거나 인라인으로 정의할 수 있습니다.
* 이벤트 핸들러는 컴포넌트 내부에 정의되므로 props에 접근할 수 있습니다.
* 부모에서 이벤트 핸들러를 선언하고 자식에게 prop으로 전달할 수 있습니다.
* 앱에 특화된 이름으로 이벤트 핸들러 prop을 직접 정의할 수 있습니다.
* 이벤트는 위로 전파됩니다. 이를 막으려면 첫 번째 인수로 `e.stopPropagation()`을 호출하세요.
* 이벤트는 원치 않는 기본 브라우저 동작을 일으킬 수 있습니다. 이를 막으려면 `e.preventDefault()`를 호출하세요.
* 자식 핸들러에서 이벤트 핸들러 prop을 명시적으로 호출하는 것은 전파의 좋은 대안입니다.

</Recap>
