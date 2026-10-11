# Component

`Component`는 React에서 클래스 형태로 컴포넌트를 정의할 때 사용하는 기반 클래스입니다.

> **참고:** 새로 작성하는 코드에서는 클래스 대신 함수로 컴포넌트를 정의하는 방식을 권장합니다. [마이그레이션 방법](#함수-컴포넌트로-마이그레이션하기)을 참고하세요.

---

## 개요

- [`Component`](#component-1)
- [`context`](#context)
- [`props`](#props)
- [`state`](#state)
- [`constructor(props)`](#constructorprops)
- [`componentDidCatch(error, info)`](#componentdidcatcherror-info)
- [`componentDidMount()`](#componentdidmount)
- [`componentDidUpdate(prevProps, prevState, snapshot?)`](#componentdidupdateprevprops-prevstate-snapshot)
- [`componentWillUnmount()`](#componentwillunmount)
- [`forceUpdate(callback?)`](#forceupdatecallback)
- [`getSnapshotBeforeUpdate(prevProps, prevState)`](#getsnapshotbeforeupdateprevprops-prevstate)
- [`render()`](#render)
- [`setState(nextState, callback?)`](#setstatenextstate-callback)
- [`shouldComponentUpdate(nextProps, nextState, nextContext)`](#shouldcomponentupdatenextprops-nextstate-nextcontext)
- [`static contextType`](#static-contexttype)
- [`static defaultProps`](#static-defaultprops)
- [`static getDerivedStateFromError(error)`](#static-getderivedstatefromerrorerror)
- [`static getDerivedStateFromProps(props, state)`](#static-getderivedstatefromprops-props-state)

---

## 레퍼런스

### `Component`

클래스 컴포넌트를 정의하려면 내장된 `Component` 클래스를 확장(`extends`)하고 [`render` 메서드](#render)를 작성합니다.

```js
import { Component } from 'react';

class Greeting extends Component {
  render() {
    return <h1>안녕하세요, {this.props.name}님!</h1>;
  }
}
```

`render` 메서드만 필수이며, 나머지 메서드는 선택 사항입니다.

#### 주의 사항

- 클래스 컴포넌트에는 상속 계층을 두지 않는 것이 좋습니다. 코드를 재사용하고 싶다면 상속 대신 [합성(composition)](https://ko.react.dev/learn/passing-props-to-a-component)을 사용하세요.
- `React.Component`를 직접 상속한 클래스만 지원하며, 중간에 다른 기반 클래스를 두는 방식은 권장하지 않습니다.

---

### `context`

클래스 컴포넌트에서는 `this.context`로 [컨텍스트](https://ko.react.dev/learn/passing-data-deeply-with-context)를 읽을 수 있습니다. 단, [`static contextType`](#static-contexttype)을 지정해야 값이 채워집니다.

```js
class Button extends Component {
  static contextType = ThemeContext;

  render() {
    const theme = this.context;
    const className = 'button-' + theme;
    return <button className={className}>{this.props.children}</button>;
  }
}
```

---

### `props`

`this.props`에는 부모가 전달한 props가 담깁니다. props는 읽기 전용이므로 직접 수정해서는 안 됩니다.

```js
class Greeting extends Component {
  render() {
    return <h1>안녕하세요, {this.props.name}님!</h1>;
  }
}

<Greeting name="태영" />
```

---

### `state`

`this.state`는 컴포넌트의 state를 나타냅니다. 초기값은 직접 정의해야 하며, 클래스 필드 문법을 사용하면 간단합니다. state를 직접 변경(`this.state.name = '...'`)하면 안 되고, 반드시 [`setState`](#setstatenextstate-callback)를 사용해야 합니다.

```js
class Counter extends Component {
  state = { age: 42 };

  handleAgeChange = () => {
    this.setState({ age: this.state.age + 1 });
  };

  render() {
    return (
      <>
        <button onClick={this.handleAgeChange}>나이 증가</button>
        <p>당신은 {this.state.age}살입니다.</p>
      </>
    );
  }
}
```

---

### `constructor(props)`

컴포넌트가 *마운트*되기 전에 생성자가 실행됩니다. 일반적으로 React에서 생성자는 두 가지 목적으로만 사용됩니다: state 선언, 그리고 클래스 메서드를 인스턴스에 [바인딩](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Operators/this#bound_methods)하는 것입니다.

```js
class Counter extends Component {
  constructor(props) {
    super(props);
    this.state = { counter: 0 };
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick() {
    // ...
  }
}
```

현대적인 문법에서는 생성자가 거의 필요하지 않습니다. 위 코드는 클래스 필드와 화살표 함수로 간단하게 바꿀 수 있습니다.

```js
class Counter extends Component {
  state = { counter: 0 };

  handleClick = () => {
    // ...
  };
}
```

#### 주의 사항

- 생성자 안에서 부수 효과(side effect)나 구독을 실행하지 마세요. 그 용도로는 `componentDidMount`를 사용합니다.
- 생성자 안에서는 `super(props)`를 가장 먼저 호출해야 합니다. 그렇지 않으면 생성자 실행 중 `this.props`가 `undefined`가 됩니다.

---

### `componentDidCatch(error, info)`

`componentDidCatch`를 정의하면, 자식 컴포넌트가 렌더링 중에 오류를 던졌을 때 React가 이 메서드를 호출합니다. 오류 정보를 외부 서비스에 기록하는 용도로 쓸 수 있습니다.

```js
class ErrorBoundary extends Component {
  state = { hasError: false };

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, info) {
    logErrorToMyService(error, info.componentStack);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback;
    }
    return this.props.children;
  }
}
```

> 현재 에러 바운더리를 함수 컴포넌트로 작성하는 방법은 없습니다. 에러 바운더리가 필요하면 클래스 컴포넌트를 쓰거나 [`react-error-boundary`](https://github.com/bvaughn/react-error-boundary) 같은 라이브러리를 사용하세요.

---

### `componentDidMount()`

컴포넌트가 화면에 추가(마운트)된 직후 호출됩니다. 데이터 불러오기, 구독 설정, DOM 노드 조작 등 부수 효과를 시작하기에 적합한 위치입니다.

```js
class ChatRoom extends Component {
  state = { serverUrl: 'https://localhost:1234' };

  componentDidMount() {
    this.setupConnection();
  }

  componentDidUpdate(prevProps, prevState) {
    if (
      this.props.roomId !== prevProps.roomId ||
      this.state.serverUrl !== prevState.serverUrl
    ) {
      this.destroyConnection();
      this.setupConnection();
    }
  }

  componentWillUnmount() {
    this.destroyConnection();
  }
  // ...
}
```

개발 모드에서 [Strict Mode](https://ko.react.dev/reference/react/StrictMode)를 켜면 React가 `componentDidMount`를 호출한 뒤 곧바로 `componentWillUnmount`와 `componentDidMount`를 한 번 더 호출합니다. 정리(cleanup) 로직이 빠져 있는 버그를 일찍 발견하기 위한 동작입니다.

---

### `componentDidUpdate(prevProps, prevState, snapshot?)`

props나 state가 바뀌어 컴포넌트가 다시 렌더링된 직후 호출됩니다. 최초 렌더링에서는 호출되지 않습니다. 이전 값과 현재 값을 비교하는 조건문 안에서만 부수 효과를 실행해야 무한 루프를 피할 수 있습니다.

```js
componentDidUpdate(prevProps) {
  if (this.props.userId !== prevProps.userId) {
    this.fetchUser(this.props.userId);
  }
}
```

`shouldComponentUpdate`가 `false`를 반환하면 이 메서드는 호출되지 않습니다.

---

### `componentWillUnmount()`

컴포넌트가 화면에서 제거(언마운트)되기 직전에 호출됩니다. 구독 해제, 타이머 정리, 네트워크 연결 종료처럼 `componentDidMount`에서 시작한 작업을 정리하세요. 이 메서드 안에서는 `setState`를 호출하면 안 됩니다.

---

### `forceUpdate(callback?)`

컴포넌트를 강제로 다시 렌더링합니다. 보통 필요하지 않으며, 외부 데이터를 `this.props`나 `this.state`가 아닌 곳에서 읽고 있을 때만 쓰게 됩니다. 가능하면 `forceUpdate`의 사용을 피하고 `render`에서는 `props`와 `state`만 읽으세요.

---

### `getSnapshotBeforeUpdate(prevProps, prevState)`

React가 DOM을 갱신하기 직전에 호출됩니다. 반환값은 `componentDidUpdate`의 세 번째 인자(`snapshot`)로 전달됩니다. 예를 들어 업데이트 전의 스크롤 위치를 저장해 두었다가 복원할 때 사용합니다.

```js
class ScrollingList extends Component {
  listRef = createRef(null);

  getSnapshotBeforeUpdate(prevProps) {
    if (prevProps.list.length < this.props.list.length) {
      const list = this.listRef.current;
      return list.scrollHeight - list.scrollTop;
    }
    return null;
  }

  componentDidUpdate(prevProps, prevState, snapshot) {
    if (snapshot !== null) {
      const list = this.listRef.current;
      list.scrollTop = list.scrollHeight - snapshot;
    }
  }

  render() {
    return <ul ref={this.listRef}>{/* ... */}</ul>;
  }
}
```

---

### `render()`

클래스 컴포넌트에서 유일하게 필수인 메서드입니다. 화면에 표시할 JSX를 반환합니다.

```js
class Greeting extends Component {
  render() {
    return <h1>안녕하세요, {this.props.name}님!</h1>;
  }
}
```

`render`는 [순수 함수](https://ko.react.dev/learn/keeping-components-pure)여야 합니다. 같은 props, state, context에 대해 항상 같은 JSX를 반환해야 하며, 렌더링 중에 state를 바꾸거나 네트워크 요청을 보내서는 안 됩니다.

---

### `setState(nextState, callback?)`

컴포넌트의 state를 갱신하고 다시 렌더링을 요청합니다.

```js
handleClick = () => {
  this.setState({ name: '로빈' });
};
```

이전 state를 기반으로 다음 값을 계산할 때는 업데이터 함수를 전달하세요.

```js
this.setState((state, props) => ({
  age: state.age + 1
}));
```

`setState`는 현재 렌더링 중인 `this.state`를 즉시 바꾸지 않고, 다음 렌더링을 위한 변경을 예약합니다. 따라서 호출 직후 `this.state`를 읽으면 이전 값이 나옵니다. 또한 여러 번 호출하면 React가 하나로 묶어(batching) 처리합니다.

---

### `shouldComponentUpdate(nextProps, nextState, nextContext)`

이 메서드가 `false`를 반환하면 React는 다시 렌더링을 건너뜁니다. 성능 최적화를 위한 수단이며, 일반적으로는 직접 구현하기보다 [`PureComponent`](https://ko.react.dev/reference/react/PureComponent)를 상속하는 편이 낫습니다.

```js
shouldComponentUpdate(nextProps, nextState) {
  return nextProps.value !== this.props.value;
}
```

---

### `static contextType`

클래스 컴포넌트에서 [`this.context`](#context)로 컨텍스트를 읽으려면 어떤 컨텍스트를 읽을지 지정해야 합니다. `createContext`로 만든 컨텍스트 객체를 할당하세요. 클래스 컴포넌트는 한 번에 하나의 컨텍스트만 읽을 수 있습니다.

---

### `static defaultProps`

props의 기본값을 지정합니다. `undefined`인 props에만 적용되며, `null`에는 적용되지 않습니다.

```js
class Button extends Component {
  static defaultProps = {
    color: 'blue'
  };

  render() {
    return <button className={this.props.color}>클릭</button>;
  }
}
```

---

### `static getDerivedStateFromError(error)`

자식 컴포넌트가 렌더링 중 오류를 던지면 호출됩니다. 오류를 받아 대체 UI를 보여 주기 위한 state를 반환하세요. 이 단계(렌더 단계)에서는 부수 효과를 실행하면 안 되며, 오류 기록 같은 작업은 `componentDidCatch`에서 합니다.

---

### `static getDerivedStateFromProps(props, state)`

초기 마운트와 이후 모든 업데이트 시 `render` 직전에 호출됩니다. state를 갱신하려면 객체를, 갱신하지 않으려면 `null`을 반환합니다. 다만 이 메서드는 코드를 장황하게 만들고 버그를 유발하기 쉬워, 대부분의 경우 [state를 파생시키는 다른 방법](https://ko.react.dev/blog/2018/06/07/you-probably-dont-need-derived-state)이 더 낫습니다.

---

## 사용법

### 클래스 컴포넌트 정의하기

`Component`를 확장하고 `render`를 구현합니다. 필요에 따라 state, 이벤트 핸들러, 생명주기 메서드를 추가합니다.

```js
import { Component } from 'react';

class Greeting extends Component {
  state = { name: '태영' };

  handleNameChange = (e) => {
    this.setState({ name: e.target.value });
  };

  render() {
    return (
      <>
        <input value={this.state.name} onChange={this.handleNameChange} />
        <p>안녕하세요, {this.state.name}님!</p>
      </>
    );
  }
}
```

### 생명주기 메서드 추가하기

클래스 컴포넌트는 *마운트*(화면에 추가), *업데이트*(props/state 변경 후 재렌더링), *언마운트*(화면에서 제거)의 세 단계를 거치며, 각 시점에 맞는 메서드를 정의해 동작을 끼워 넣을 수 있습니다.

### 에러 바운더리 만들기

렌더링 중 발생한 오류로 앱 전체가 깨지는 것을 막으려면 `getDerivedStateFromError`와 `componentDidCatch`를 구현한 에러 바운더리를 만들고, 보호할 영역을 감싸세요.

---

## 대안

### 함수 컴포넌트로 마이그레이션하기

새로운 코드에서는 클래스 대신 함수 컴포넌트를 사용하는 것을 권장합니다. 앞의 `Greeting` 예시는 다음과 같이 바꿀 수 있습니다.

```js
import { useState } from 'react';

function Greeting() {
  const [name, setName] = useState('태영');

  return (
    <>
      <input value={name} onChange={(e) => setName(e.target.value)} />
      <p>안녕하세요, {name}님!</p>
    </>
  );
}
```

생명주기 메서드는 다음과 같이 대응됩니다.

| 클래스 컴포넌트 | 함수 컴포넌트 |
| --- | --- |
| `state`, `setState` | `useState`, `useReducer` |
| `componentDidMount`, `componentDidUpdate`, `componentWillUnmount` | `useEffect` |
| `static contextType` | `useContext` |
| `shouldComponentUpdate` | `memo` |
| `getSnapshotBeforeUpdate` | (대응하는 Hook 없음, 클래스 유지) |
| `componentDidCatch`, `getDerivedStateFromError` | (대응하는 Hook 없음, 클래스 유지) |

> `getSnapshotBeforeUpdate`와 에러 바운더리 관련 메서드는 아직 Hook으로 대체할 수 없습니다.
