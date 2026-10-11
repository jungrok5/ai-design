# Hook의 규칙

Hook은 `use`로 시작하는 JavaScript 함수지만, 일반 함수와 달리 호출 위치에 제약이 있습니다. Hook은 UI에 대한 재사용 가능한 로직을 표현하는 특별한 방식이며, 아래 규칙을 지켜야 React가 컴포넌트의 상태를 올바르게 추적할 수 있습니다.

<Note>

이 규칙을 자동으로 검사하려면 [`eslint-plugin-react-hooks`](https://www.npmjs.com/package/eslint-plugin-react-hooks)를 사용하세요.

</Note>

## 최상위에서만 Hook을 호출하세요 {/*only-call-hooks-at-the-top-level*/}

이름이 `use`로 시작하는 함수를 **Hook**이라고 합니다. 반복문, 조건문, 중첩 함수, `try`/`catch`/`finally` 블록 안에서는 Hook을 호출하지 마세요. 대신 항상 React 함수의 최상위에서, 얼리 리턴보다 앞서 Hook을 호출해야 합니다. 이렇게 하면 컴포넌트가 렌더링될 때마다 Hook이 항상 같은 순서로 호출됩니다. React는 이 순서에 의존해 여러 `useState`와 `useEffect` 호출 사이에서 상태를 올바르게 유지합니다.

```js
function Counter() {
  // ✅ 좋은 예: 컴포넌트의 최상위
  const [count, setCount] = useState(0);
  // ...
}

function Bad({ cond }) {
  if (cond) {
    // 🔴 나쁜 예: 조건문 안
    const theme = useContext(ThemeContext);
  }
  for (let i = 0; i < 10; i++) {
    // 🔴 나쁜 예: 반복문 안
    const theme = useContext(ThemeContext);
  }
  if (cond) {
    return;
  }
  // 🔴 나쁜 예: 얼리 리턴 이후
  const theme = useContext(ThemeContext);
  // ...
}
```

<Note>

[`use`](/reference/react/use)는 예외적인 Hook입니다. 조건문이나 반복문 안에서도 호출할 수 있지만, `try`/`catch`/`finally` 블록 안에서는 호출할 수 없습니다.

</Note>

## React 함수에서만 Hook을 호출하세요 {/*only-call-hooks-from-react-functions*/}

일반 JavaScript 함수에서는 Hook을 호출하지 마세요. 대신 다음 위치에서만 호출할 수 있습니다.

- ✅ React 함수 컴포넌트의 최상위
- ✅ 커스텀 Hook의 최상위

이 규칙을 따르면 컴포넌트의 모든 상태 관련 로직을 소스 코드에서 명확하게 확인할 수 있습니다.

```js
function FriendList() {
  // ✅ 좋은 예: 함수 컴포넌트 안
  const [onlineStatus, setOnlineStatus] = useState('offline');
}

function useOnlineStatus() {
  // ✅ 좋은 예: 커스텀 Hook 안
  const [onlineStatus, setOnlineStatus] = useState('offline');
  return onlineStatus;
}

function setupStatus() {
  // 🔴 나쁜 예: 컴포넌트도 Hook도 아닌 일반 함수
  const [status, setStatus] = useState('offline');
}
```

클래스 컴포넌트 안에서도 Hook을 사용할 수 없습니다.

## 함수를 일반 값처럼 전달하지 마세요 {/*dont-pass-hooks-as-regular-values*/}

Hook을 일반 값처럼 다른 곳에 전달하거나 동적으로 호출하지 마세요. Hook은 정적으로 분석할 수 있어야 하며, 항상 호출하는 자리에서 직접 사용해야 합니다.

```js
function ChatInput() {
  const useDataWithLogging = withLogging(useData); // 🔴 나쁜 예: 고차 Hook 금지
}
```

대신 Hook이 필요한 곳에서 직접 호출하고, 공통 로직은 `useDataWithLogging`처럼 별도의 커스텀 Hook으로 분리하세요.
