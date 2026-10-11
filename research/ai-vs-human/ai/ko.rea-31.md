# flushSync

`flushSync`를 사용하면 React가 제공된 콜백 안에서 발생한 state 업데이트를 동기적으로 처리하도록 강제할 수 있습니다. 이를 통해 DOM이 즉시 업데이트되도록 보장합니다.

```js
flushSync(callback)
```

- [레퍼런스](#reference)
  - [`flushSync(callback)`](#flushsync)
- [사용법](#usage)
  - [서드파티 통합을 위해 동기적으로 DOM 갱신하기](#flushing-updates-for-third-party-integrations)
- [문제 해결](#troubleshooting)
  - ["flushSync was called from inside a lifecycle method" 경고가 나타나요](#im-getting-an-error-flushsync-was-called-from-inside-a-lifecycle-method)

---

## 레퍼런스 {/*reference*/}

### `flushSync(callback)` {/*flushsync*/}

`flushSync`를 호출하면 대기 중인 모든 작업을 React가 즉시 처리하고 DOM을 동기적으로 갱신하도록 강제할 수 있습니다.

```js
import { flushSync } from 'react-dom';

flushSync(() => {
  setSomething(123);
});
```

대부분의 경우 `flushSync`는 필요하지 않습니다. 꼭 필요할 때만 최후의 수단으로 사용하세요.

[아래에서 더 많은 예시를 확인하세요.](#usage)

#### 매개변수 {/*parameters*/}

* `callback`: 함수입니다. React는 이 콜백을 즉시 호출하고, 그 안에 포함된 모든 업데이트를 동기적으로 처리합니다. 대기 중인 Effect, 콜백, 또는 업데이트도 함께 처리될 수 있습니다. `flushSync` 호출로 인해 업데이트가 일어나면 Suspense 폴백이 다시 표시될 수 있습니다.

#### 반환값 {/*returns*/}

`flushSync`는 `undefined`를 반환합니다.

#### 주의 사항 {/*caveats*/}

* `flushSync`는 성능을 크게 저하시킬 수 있습니다. 가능한 한 적게 사용하세요.
* `flushSync`는 대기 중인 Suspense 바운더리가 `fallback` 상태를 표시하도록 강제할 수 있습니다.
* `flushSync`는 대기 중인 Effect를 실행하고, 반환하기 전에 그 안에 포함된 업데이트를 동기적으로 적용할 수 있습니다.
* `flushSync`는 콜백 안의 업데이트를 처리하기 위해 필요한 경우 콜백 바깥의 업데이트도 함께 처리할 수 있습니다. 예를 들어 클릭 이벤트에서 대기 중인 업데이트가 있다면, React는 콜백 안의 업데이트를 처리하기 전에 해당 업데이트를 먼저 반영할 수 있습니다.

---

## 사용법 {/*usage*/}

### 서드파티 통합을 위해 동기적으로 DOM 갱신하기 {/*flushing-updates-for-third-party-integrations*/}

브라우저 API나 UI 라이브러리 같은 서드파티 코드와 연동할 때, React가 업데이트를 즉시 반영하도록 강제해야 할 수 있습니다. `flushSync`를 사용하면 콜백 안의 [state 업데이트](/reference/react/useState#setstate)가 실행된 직후 DOM에 반영되도록 만들 수 있습니다.

```js [[1, 2, "flushSync"], [1, 5, "flushSync"]]
import { flushSync } from 'react-dom';

flushSync(() => {
  setSomething(123);
});
// 이 줄에 도달하면 DOM은 이미 갱신되어 있습니다.
```

이렇게 하면 React가 다음 코드를 실행하기 전에 DOM을 갱신합니다.

기본적으로 React는 이벤트 핸들러가 끝난 뒤 여러 state 업데이트를 모아서 한 번에 처리합니다(배치). 이 방식은 불필요한 리렌더링을 막아 주기 때문에 대부분의 경우 바람직합니다. 그러나 업데이트 직후 DOM의 상태를 읽어야 하는 코드가 있다면, 배치 때문에 원하는 시점에 DOM이 준비되지 않을 수 있습니다.

대표적인 예로 브라우저의 인쇄 API를 들 수 있습니다. `window.print()`는 호출된 시점의 DOM을 기준으로 인쇄 미리보기를 만듭니다. 이때 state를 바꾼 직후 바로 `window.print()`를 호출하면, 아직 DOM이 갱신되지 않아 이전 화면이 인쇄됩니다.

<Sandpack>

```js src/App.js
import { useState, useEffect } from 'react';
import { flushSync } from 'react-dom';

export default function PrintApp() {
  const [isPrinting, setIsPrinting] = useState(false);

  useEffect(() => {
    function handleBeforePrint() {
      flushSync(() => {
        setIsPrinting(true);
      });
    }

    function handleAfterPrint() {
      setIsPrinting(false);
    }

    window.addEventListener('beforeprint', handleBeforePrint);
    window.addEventListener('afterprint', handleAfterPrint);
    return () => {
      window.removeEventListener('beforeprint', handleBeforePrint);
      window.removeEventListener('afterprint', handleAfterPrint);
    };
  }, []);

  return (
    <>
      <h1>isPrinting: {isPrinting ? 'yes' : 'no'}</h1>
      <button onClick={() => window.print()}>
        인쇄하기
      </button>
    </>
  );
}
```

</Sandpack>

위 예시에서 `beforeprint` 이벤트 핸들러는 `flushSync`로 `isPrinting` state를 동기적으로 반영합니다. 덕분에 브라우저가 인쇄 화면을 만들기 전에 DOM이 이미 `isPrinting: yes` 상태로 갱신됩니다.

또 다른 예시는 목록의 맨 아래로 스크롤하는 경우입니다. 새 항목을 추가한 직후 스크롤하려면, 새 항목이 DOM에 존재해야 합니다.

```js
import { useState, useRef } from 'react';
import { flushSync } from 'react-dom';

export default function TodoList() {
  const listRef = useRef(null);
  const [text, setText] = useState('');
  const [todos, setTodos] = useState([]);

  function handleAdd() {
    const newTodo = { id: nextId++, text: text };
    flushSync(() => {
      setText('');
      setTodos([...todos, newTodo]);
    });
    listRef.current.lastChild.scrollIntoView({
      behavior: 'smooth',
      block: 'nearest'
    });
  }

  return (
    <>
      <button onClick={handleAdd}>추가</button>
      <input
        value={text}
        onChange={e => setText(e.target.value)}
      />
      <ul ref={listRef}>
        {todos.map(todo => (
          <li key={todo.id}>{todo.text}</li>
        ))}
      </ul>
    </>
  );
}

let nextId = 0;
```

`flushSync` 없이 `scrollIntoView`를 호출하면 `listRef.current.lastChild`가 아직 이전 마지막 항목을 가리키므로, 새로 추가된 항목이 아니라 그 이전 항목으로 스크롤됩니다.

<Pitfall>

`flushSync`는 성능에 매우 불리합니다. 또한 대기 중인 Suspense 바운더리가 예기치 않게 폴백 상태를 표시하도록 만들 수 있습니다.

대부분의 경우 `flushSync`를 피할 수 있습니다. 가능하다면 다음과 같은 대안을 먼저 고려하세요.

* Effect나 이벤트 핸들러에서 state를 읽을 때는 업데이트된 값을 다음 렌더링에서 사용하도록 설계하세요.
* DOM 노드를 직접 다뤄야 한다면 [ref](/learn/manipulating-the-dom-with-refs)와 `useEffect`, `useLayoutEffect`를 사용하는 것이 더 자연스러운 경우가 많습니다.
* 여러 업데이트를 한 번에 반영하는 것이 더 효율적이라면, 기본 배치 동작을 그대로 활용하세요.

</Pitfall>

---

## 문제 해결 {/*troubleshooting*/}

### "flushSync was called from inside a lifecycle method" 경고가 나타나요 {/*im-getting-an-error-flushsync-was-called-from-inside-a-lifecycle-method*/}

React는 렌더링 도중이나 Effect, 라이프사이클 메서드가 실행되는 중에 `flushSync`를 호출하는 것을 허용하지 않습니다. 다음과 같은 경고가 표시됩니다.

<ConsoleBlock level="error">

flushSync was called from inside a lifecycle method. React cannot flush when React is already rendering. Consider moving this call to a scheduler task or micro task.

</ConsoleBlock>

React가 이미 렌더링을 진행하고 있는 상태에서 또 다른 렌더링을 동기적으로 시작하면 안전하게 처리할 수 없기 때문입니다. 이 경고가 나타나면 `flushSync` 호출을 렌더링이나 Effect 바깥으로 옮겨야 합니다.

예를 들어 Effect 안에서 꼭 호출해야 한다면, 마이크로태스크나 스케줄러 태스크로 호출을 미룰 수 있습니다.

```js {2-4}
useEffect(() => {
  queueMicrotask(() => {
    flushSync(() => {
      setSomething(123);
    });
  });
}, []);
```

다만 이 방법도 임시방편에 가깝습니다. 먼저 정말로 동기적인 DOM 갱신이 필요한지 다시 한번 검토해 보세요. 이벤트 핸들러에서 호출하거나, 업데이트 이후의 작업을 `useEffect`나 `useLayoutEffect`로 옮기면 `flushSync` 자체가 필요 없는 경우가 많습니다.

또한 `flushSync`는 `react-dom`에서 가져와야 한다는 점에 유의하세요. `react`가 아니라 `react-dom`에서 import합니다.

```js
// ✅ 올바른 import
import { flushSync } from 'react-dom';
```

React Native처럼 `react-dom`을 사용하지 않는 환경에서는 `flushSync`를 쓸 수 없습니다. 해당 환경에서는 각 렌더러가 제공하는 별도의 API를 확인하세요.
