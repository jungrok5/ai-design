# useContext

`useContext`는 컴포넌트에서 [context](/learn/passing-data-deeply-with-context)를 읽고 구독할 수 있게 해 주는 React Hook입니다.

```js
const value = useContext(SomeContext)
```

<Note>

## 목차

- [레퍼런스](#reference)
  - [`useContext(SomeContext)`](#usecontext)
- [사용법](#usage)
  - [트리 깊숙이 데이터 전달하기](#passing-data-deeply-into-the-tree)
  - [context를 통해 전달된 데이터 업데이트하기](#updating-data-passed-via-context)
  - [폴백 기본값 지정하기](#specifying-a-fallback-default-value)
  - [트리 일부의 context 덮어쓰기](#overriding-context-for-a-part-of-the-tree)
  - [객체와 함수를 전달할 때 리렌더링 최적화하기](#optimizing-re-renders-when-passing-objects-and-functions)
- [문제 해결](#troubleshooting)

</Note>

---

## 레퍼런스

### `useContext(SomeContext)`

컴포넌트의 최상위 레벨에서 `useContext`를 호출하여 context 값을 읽고 구독합니다.

```js
import { useContext } from 'react';

function MyComponent() {
  const theme = useContext(ThemeContext);
  // ...
```

[아래에서 더 많은 예시를 확인하세요.](#usage)

#### 매개변수

- `SomeContext`: [`createContext`](/reference/react/createContext)로 만든 context입니다. context 자체는 정보를 담고 있지 않으며, 컴포넌트에서 제공하거나 읽을 수 있는 정보의 _종류_ 를 나타냅니다.

#### 반환값

`useContext`는 호출한 컴포넌트에 대한 context 값을 반환합니다. 이 값은 트리에서 호출한 컴포넌트보다 위에 있는 가장 가까운 `SomeContext.Provider`에 전달된 `value`로 결정됩니다. 해당 Provider가 없다면 반환값은 그 context를 만들 때 `createContext`에 전달한 `defaultValue`입니다. 반환된 값은 항상 최신 상태입니다. context가 변경되면 React는 그 context를 읽는 컴포넌트를 자동으로 리렌더링합니다.

#### 주의 사항

- 컴포넌트의 `useContext()` 호출은 **같은 컴포넌트**가 반환하는 Provider의 영향을 받지 않습니다. 해당 `<Context.Provider>`는 `useContext()`를 호출하는 컴포넌트보다 **위에** 있어야 합니다.
- React는 다른 `value`를 받는 Provider부터 시작하여 특정 context를 사용하는 모든 자식을 **자동으로 리렌더링**합니다. 이전 값과 다음 값은 [`Object.is`](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Object/is) 비교로 판단합니다. [`memo`](/reference/react/memo)로 리렌더링을 건너뛰더라도 자식이 새로운 context 값을 받는 것을 막지는 못합니다.
- 빌드 시스템이 결과물에 중복된 모듈을 생성한다면(심볼릭 링크에서 발생할 수 있습니다) context가 깨질 수 있습니다. context를 통해 무언가를 전달할 때는 `===` 비교로 판단하는 `SomeContext`와 `SomeContext.Provider`가 정확히 같은 객체여야 합니다.

---

## 사용법

### 트리 깊숙이 데이터 전달하기

컴포넌트의 최상위 레벨에서 `useContext`를 호출하여 context를 읽고 구독합니다.

```js [[2, 4, "theme"], [1, 4, "ThemeContext"]]
import { useContext } from 'react';

function Button() {
  const theme = useContext(ThemeContext);
  // ...
```

`useContext`는 전달한 context에 대한 <CodeStep step={2}>context 값</CodeStep>을 반환합니다. context 값을 결정하기 위해 React는 컴포넌트 트리를 탐색하며, 해당 context에 대해 **위쪽으로 가장 가까운 Provider**를 찾습니다.

context를 `Button`에 전달하려면, 해당 버튼 또는 그 부모 컴포넌트 중 하나를 대응하는 context Provider로 감쌉니다.

```js [[1, 3, "ThemeContext"], [2, 3, "\\"dark\\""], [1, 5, "ThemeContext"]]
function MyPage() {
  return (
    <ThemeContext.Provider value="dark">
      <Form />
    </ThemeContext.Provider>
  );
}

function Form() {
  // ... 이 안에서 버튼을 렌더링합니다 ...
}
```

Provider와 `Button` 사이에 몇 겹의 컴포넌트가 있든 상관없습니다. `Form` 내부 어디에서든 `Button`이 `useContext(ThemeContext)`를 호출하면 `"dark"`를 값으로 받습니다.

<Pitfall>

`useContext()`는 항상 호출하는 컴포넌트에서 **위쪽으로 가장 가까운** Provider를 찾습니다. 위쪽으로 탐색하므로, `useContext()`를 호출하는 컴포넌트 자신이 렌더링한 Provider는 **고려하지 않습니다.**

</Pitfall>

---

### context를 통해 전달된 데이터 업데이트하기

시간이 지나면서 context가 변경되기를 원하는 경우가 많습니다. context를 업데이트하려면 [state](/reference/react/useState)와 함께 사용하세요. 부모 컴포넌트에서 state 변수를 선언하고, 현재 state를 <CodeStep step={2}>context 값</CodeStep>으로 Provider에 전달합니다.

```js {2,11}
function MyPage() {
  const [theme, setTheme] = useState('dark');
  return (
    <ThemeContext.Provider value={theme}>
      <Form />
      <Button onClick={() => {
        setTheme('light');
      }}>
        라이트 테마로 전환
      </Button>
    </ThemeContext.Provider>
  );
}
```

이제 Provider 내부의 모든 `Button`은 현재 `theme` 값을 받습니다. Provider에 전달한 `theme` 값을 갱신하려고 `setTheme`을 호출하면, 모든 `Button` 컴포넌트가 새로운 `'light'` 값으로 리렌더링됩니다.

#### 예시: context 업데이트하기

아래 예시에서 `MyApp` 컴포넌트는 state 변수를 가지고 있고, 이 값이 `ThemeContext` Provider로 전달됩니다. "다크 모드" 체크박스를 선택하면 Provider의 값이 바뀌고, 그 context를 사용하는 모든 컴포넌트가 다시 렌더링됩니다.

```js
import { createContext, useContext, useState } from 'react';

const ThemeContext = createContext(null);

export default function MyApp() {
  const [theme, setTheme] = useState('light');
  return (
    <ThemeContext.Provider value={theme}>
      <Form />
      <label>
        <input
          type="checkbox"
          checked={theme === 'dark'}
          onChange={(e) => {
            setTheme(e.target.checked ? 'dark' : 'light');
          }}
        />
        다크 모드 사용
      </label>
    </ThemeContext.Provider>
  )
}

function Form({ children }) {
  return (
    <Panel title="환영합니다">
      <Button>회원 가입</Button>
      <Button>로그인</Button>
    </Panel>
  );
}

function Panel({ title, children }) {
  const theme = useContext(ThemeContext);
  const className = 'panel-' + theme;
  return (
    <section className={className}>
      <h1>{title}</h1>
      {children}
    </section>
  )
}

function Button({ children }) {
  const theme = useContext(ThemeContext);
  const className = 'button-' + theme;
  return (
    <button className={className}>
      {children}
    </button>
  );
}
```

`value="dark"`처럼 문자열 리터럴을 전달하든 `value={theme}`처럼 JavaScript 변수를 전달하든, 어느 쪽이든 동작합니다. 다만 `value`가 바뀔 때에만 소비하는 컴포넌트들이 다시 렌더링된다는 점을 기억하세요.

---

### 폴백 기본값 지정하기

React가 부모 트리에서 해당 <CodeStep step={1}>context</CodeStep>의 Provider를 찾지 못하면, `useContext()`가 반환하는 값은 [context를 만들 때](/reference/react/createContext) 지정한 <CodeStep step={3}>기본값</CodeStep>과 같아집니다.

```js [[1, 1, "ThemeContext"], [3, 1, "null"]]
const ThemeContext = createContext(null);
```

기본값은 **절대 바뀌지 않습니다.** context를 업데이트하고 싶다면 위에서 설명한 것처럼 state와 함께 사용하세요.

보통은 `null` 대신 더 의미 있는 값을 기본값으로 사용할 수 있습니다.

```js [[1, 1, "ThemeContext"], [3, 1, "light"]]
const ThemeContext = createContext('light');
```

이렇게 하면 실수로 Provider 없이 일부 컴포넌트를 렌더링하더라도 깨지지 않습니다. 또한 테스트 환경에서 많은 Provider를 설정하지 않고도 컴포넌트가 잘 동작하게 해 줍니다.

---

### 트리 일부의 context 덮어쓰기

트리의 일부를 다른 값의 Provider로 감싸서 해당 부분의 context를 덮어쓸 수 있습니다.

```js {3,5}
<ThemeContext.Provider value="dark">
  ...
  <ThemeContext.Provider value="light">
    <Footer />
  </ThemeContext.Provider>
  ...
</ThemeContext.Provider>
```

필요한 만큼 Provider를 중첩하고 덮어쓸 수 있습니다.

#### 예시: 중첩된 context로 테마 바꾸기

```js
import { createContext, useContext } from 'react';

const ThemeContext = createContext(null);

export default function MyApp() {
  return (
    <ThemeContext.Provider value="dark">
      <Form />
    </ThemeContext.Provider>
  )
}

function Form() {
  return (
    <Panel title="환영합니다">
      <Button>회원 가입</Button>
      <Button>로그인</Button>
      <ThemeContext.Provider value="light">
        <Footer />
      </ThemeContext.Provider>
    </Panel>
  );
}

function Footer() {
  return (
    <footer>
      <Button>설정</Button>
    </footer>
  );
}
```

위 예시에서 `Footer` 안의 `Button`은 `"light"`를, 그 밖의 `Button`은 `"dark"`를 받습니다.

---

### 객체와 함수를 전달할 때 리렌더링 최적화하기

context를 통해 객체와 함수를 포함한 어떤 값이든 전달할 수 있습니다.

```js [[2, 10, "{ currentUser, login }"]]
function MyApp() {
  const [currentUser, setCurrentUser] = useState(null);

  function login(response) {
    storeCredentials(response.credentials);
    setCurrentUser(response.user);
  }

  return (
    <AuthContext.Provider value={{ currentUser, login }}>
      <Page />
    </AuthContext.Provider>
  );
}
```

여기서 context 값은 `currentUser`와 `login` 두 속성을 가진 JavaScript 객체입니다. `MyApp`이 리렌더링될 때마다 _다른_ 객체가 _다른_ 함수를 가리키게 되므로, React는 `useContext(AuthContext)`를 호출하는 트리 깊은 곳의 모든 컴포넌트도 리렌더링해야 합니다.

규모가 작은 앱에서는 문제가 되지 않지만, `currentUser` 같은 근본적인 데이터가 바뀌지 않았다면 리렌더링할 필요가 없습니다. React가 이 사실을 활용할 수 있도록 `login` 함수를 [`useCallback`](/reference/react/useCallback)으로 감싸고, 객체 생성은 [`useMemo`](/reference/react/useMemo)로 감쌀 수 있습니다. 이는 성능 최적화입니다.

```js {1,6,9,11}
import { useCallback, useMemo } from 'react';

function MyApp() {
  const [currentUser, setCurrentUser] = useState(null);

  const login = useCallback((response) => {
    storeCredentials(response.credentials);
    setCurrentUser(response.user);
  }, []);

  const contextValue = useMemo(() => ({
    currentUser,
    login
  }), [currentUser, login]);

  return (
    <AuthContext.Provider value={contextValue}>
      <Page />
    </AuthContext.Provider>
  );
}
```

이렇게 하면 `currentUser`가 바뀌어야 하는 경우가 아니라면 `MyApp`이 리렌더링되어도 `useContext(AuthContext)`를 호출하는 컴포넌트는 리렌더링되지 않습니다.

[`useMemo`](/reference/react/useMemo#skipping-re-rendering-of-components)와 [`useCallback`](/reference/react/useCallback#preventing-an-effect-from-firing-too-often)에 대해 더 읽어 보세요.

---

## 문제 해결

### 컴포넌트가 Provider의 값을 받지 못합니다

이런 일이 발생하는 몇 가지 흔한 경우가 있습니다.

1. `useContext()`를 호출하는 컴포넌트와 같은 컴포넌트(또는 그 아래)에서 `<SomeContext.Provider>`를 렌더링하고 있습니다. `<SomeContext.Provider>`를 `useContext()`를 호출하는 컴포넌트의 _위쪽과 바깥_ 으로 옮기세요.
2. 컴포넌트를 `<SomeContext.Provider>`로 감싸는 것을 잊었거나, 생각한 것과 다른 위치에 두었을 수 있습니다. [React DevTools](/learn/react-developer-tools)로 계층 구조가 올바른지 확인하세요.
3. 제공하는 쪽과 사용하는 쪽에서 보는 `SomeContext`가 서로 다른 두 객체일 수 있습니다. 빌드 도구 문제로 발생할 수 있습니다. 예를 들어 context를 별도 파일에서 export/import 하는 경우, 두 파일이 서로 다른 객체를 만들어 낼 수 있습니다. 전역 변수에 할당해 확인해 볼 수 있습니다. 예를 들어 `window.SomeContext1`과 `window.SomeContext2`를 콘솔에서 `window.SomeContext1 === window.SomeContext2`로 비교해 보세요.

### context의 값이 항상 `undefined`입니다

Provider에 `value`가 없는 경우일 수 있습니다.

```js {1,2}
<ThemeContext.Provider>
   <Page />
</ThemeContext.Provider>
```

`value`를 지정하는 것을 잊었다면 `value={undefined}`를 전달한 것과 같습니다.

또한 실수로 다른 prop 이름을 사용했을 수도 있습니다.

```js {1}
<ThemeContext.Provider theme={theme}>
   <Page />
</ThemeContext.Provider>
```

두 경우 모두 콘솔에 React의 경고가 표시됩니다. 이를 고치려면 prop 이름을 `value`로 바꾸세요.

```js {1}
<ThemeContext.Provider value={theme}>
   <Page />
</ThemeContext.Provider>
```

[기본값](#specifying-a-fallback-default-value)이 `createContext(defaultValue)`로 지정된 경우, 상위에 Provider가 없을 때에만 그 값이 사용된다는 점에 유의하세요. 부모 트리 어딘가에 `<SomeContext.Provider value={undefined}>`가 있다면, 이를 사용하는 컴포넌트는 기본값이 아니라 `undefined`를 받습니다.
