# React v18.0

React 18은 동시성 렌더링(Concurrent Rendering)을 기반으로 한 메이저 릴리스입니다. 이번 버전은 주로 **렌더링 방식의 변화**를 다루며, 기존 코드의 동작을 크게 바꾸지 않고도 새 기능을 점진적으로 도입할 수 있도록 설계되었습니다.

## 주요 변경 사항 요약

React 18의 핵심은 다음과 같습니다.

- **자동 배칭(Automatic Batching)**: 이벤트 핸들러 바깥의 상태 업데이트도 자동으로 묶어 처리합니다.
- **트랜지션(Transitions)**: 긴급하지 않은 업데이트를 표시해 입력 반응성을 유지합니다.
- **새로운 루트 API**: `createRoot`와 `hydrateRoot`를 도입했습니다.
- **Suspense 개선**: 서버 렌더링에서 스트리밍과 선택적 하이드레이션을 지원합니다.
- **새로운 훅**: `useId`, `useTransition`, `useDeferredValue`, `useSyncExternalStore`, `useInsertionEffect`가 추가되었습니다.
- **Strict Mode 강화**: 개발 환경에서 Effect를 마운트, 언마운트, 재마운트하여 부작용 문제를 찾아냅니다.

## 새로운 루트 API: createRoot

React 18부터 앱을 렌더링할 때 `ReactDOM.render` 대신 `createRoot`를 사용하는 것을 권장합니다. `ReactDOM.render`를 계속 사용하면 React 17처럼 동작하며 동시성 기능을 사용할 수 없고, 콘솔에 경고가 표시됩니다.

```jsx
// React 17 방식 (React 18에서는 동시성 기능 사용 불가)
import ReactDOM from 'react-dom';
ReactDOM.render(<App />, document.getElementById('root'));

// React 18 방식
import { createRoot } from 'react-dom/client';
const container = document.getElementById('root');
const root = createRoot(container);
root.render(<App />);
```

언마운트할 때도 `unmountComponentAtNode` 대신 `root.unmount()`를 사용합니다.

```jsx
root.unmount();
```

## 자동 배칭

React 17까지는 이벤트 핸들러 안에서의 상태 업데이트만 배칭되었습니다. `setTimeout`, Promise 콜백, 네이티브 이벤트 핸들러 안의 업데이트는 각각 리렌더링을 일으켰습니다. React 18에서는 모든 업데이트가 자동으로 배칭됩니다.

```jsx
function handleClick() {
  fetchData().then(() => {
    setCount(c => c + 1);   // React 17: 리렌더링 발생
    setFlag(f => !f);       // React 17: 또 리렌더링 발생
    // React 18: 두 업데이트가 한 번의 렌더링으로 묶임
  });
}
```

대부분의 앱에서는 별도의 수정 없이 렌더링 횟수가 줄어듭니다. 업데이트 직후 DOM 값을 읽어야 하는 특수한 경우에는 `flushSync`로 동기 처리를 강제할 수 있습니다.

## 트랜지션: startTransition과 useTransition

트랜지션은 화면 전환처럼 즉각적인 반응이 꼭 필요하지 않은 업데이트를 표시하는 방법입니다. 긴급한 업데이트(입력 값 반영 등)가 들어오면 React는 진행 중이던 트랜지션 렌더링을 중단하고 긴급한 작업을 먼저 처리합니다.

```jsx
import { startTransition } from 'react';

function handleChange(e) {
  // 긴급: 입력창에 바로 반영
  setQuery(e.target.value);

  // 비긴급: 무거운 목록 갱신은 트랜지션으로 처리
  startTransition(() => {
    setFilteredItems(filterItems(e.target.value));
  });
}
```

로딩 상태를 함께 관리하고 싶다면 `useTransition`을 사용합니다.

```jsx
import { useTransition } from 'react';

function TabContainer() {
  const [isPending, startTransition] = useTransition();
  const [tab, setTab] = useState('about');

  function selectTab(nextTab) {
    startTransition(() => setTab(nextTab));
  }

  return (
    <>
      <button onClick={() => selectTab('posts')}>글 목록</button>
      {isPending && <span>불러오는 중...</span>}
      <TabContent tab={tab} />
    </>
  );
}
```

## useDeferredValue

`useDeferredValue`는 값의 변경을 지연시켜 무거운 렌더링이 입력 반응성을 해치지 않도록 합니다. `startTransition`이 상태 설정 함수를 감싸는 방식이라면, `useDeferredValue`는 값 자체를 감쌉니다.

```jsx
import { useDeferredValue } from 'react';

function SearchResults({ query }) {
  const deferredQuery = useDeferredValue(query);
  // 무거운 목록은 지연된 값으로 렌더링
  return <HeavyList keyword={deferredQuery} />;
}
```

## useId

`useId`는 서버와 클라이언트에서 일관되게 유일한 ID를 생성하는 훅입니다. 하이드레이션 불일치를 막고, `label`과 `input`을 연결하는 등 접근성 속성에 사용하기 좋습니다.

```jsx
import { useId } from 'react';

function NameField() {
  const id = useId();
  return (
    <>
      <label htmlFor={id}>이름</label>
      <input id={id} type="text" />
    </>
  );
}
```

`useId`는 리스트의 `key`를 만드는 용도로 쓰면 안 됩니다. 키는 데이터에서 가져와야 합니다.

## useSyncExternalStore

외부 상태 저장소(Redux, 브라우저 API 등)를 구독할 때 사용합니다. 동시성 렌더링 중에도 여러 컴포넌트가 같은 값을 보도록 보장합니다. 일반적으로 라이브러리 작성자가 사용하는 훅입니다.

```jsx
import { useSyncExternalStore } from 'react';

function useOnlineStatus() {
  return useSyncExternalStore(
    subscribe,                         // 변경 구독 함수
    () => navigator.onLine,            // 클라이언트 현재 값
    () => true                         // 서버 렌더링 시 기본값
  );
}
```

## Suspense와 서버 렌더링

React 18에서는 Suspense가 서버 렌더링에서도 동작합니다. `renderToPipeableStream`은 HTML을 조각 단위로 스트리밍하며, 데이터가 준비되지 않은 Suspense 경계는 폴백을 먼저 보내고 나중에 실제 콘텐츠를 채웁니다.

```jsx
import { renderToPipeableStream } from 'react-dom/server';

const { pipe } = renderToPipeableStream(<App />, {
  onShellReady() {
    res.setHeader('Content-Type', 'text/html');
    pipe(res);
  },
});
```

하이드레이션도 Suspense 단위로 나뉩니다. 특정 영역의 JavaScript가 아직 로드되지 않았더라도 나머지 부분은 먼저 상호작용할 수 있고, 사용자가 해당 영역을 클릭하면 React가 그 부분을 우선 하이드레이션합니다.

```jsx
import { hydrateRoot } from 'react-dom/client';

hydrateRoot(document.getElementById('root'), <App />);
```

## 새로운 훅: useInsertionEffect

`useInsertionEffect`는 CSS-in-JS 라이브러리가 DOM을 변경하기 직전에 `<style>` 태그를 삽입할 수 있도록 만든 훅입니다. 일반 애플리케이션 코드에서는 거의 사용하지 않습니다.

## Strict Mode 변화

React 18의 Strict Mode는 개발 환경에서 컴포넌트가 처음 마운트될 때 Effect를 한 번 실행하고, 즉시 정리(cleanup)한 뒤 다시 실행합니다. 이 과정은 Effect가 재마운트를 안전하게 처리하는지 확인하기 위한 것입니다.

```jsx
useEffect(() => {
  const connection = createConnection();
  connection.connect();
  return () => connection.disconnect(); // 정리 함수가 반드시 필요
}, []);
```

이 동작은 개발 환경에서만 발생하며, 프로덕션 빌드에는 영향을 주지 않습니다. 정리 함수가 없거나 불완전하면 개발 중에 바로 드러나므로 버그를 조기에 발견할 수 있습니다.

## 업그레이드 시 주의할 점

React 18로 업그레이드할 때 다음 사항을 확인하세요.

1. **의존성 업데이트**: `react`와 `react-dom`을 18 버전으로 올리고, TypeScript를 사용한다면 `@types/react`, `@types/react-dom`도 함께 올립니다.
2. **진입점 변경**: `ReactDOM.render`를 `createRoot`로, `hydrate`를 `hydrateRoot`로 바꿉니다.
3. **Effect 타이밍**: `useEffect`가 이전보다 늦게 실행되거나 배칭으로 인해 실행 순서가 달라질 수 있습니다. 타이밍에 의존하던 코드를 점검하세요.
4. **하이드레이션 불일치**: 서버와 클라이언트의 렌더링 결과가 다르면 React 18은 더 엄격하게 경고하며, 불일치 부분을 클라이언트에서 다시 렌더링할 수 있습니다. `Date.now()`, `Math.random()`처럼 실행마다 달라지는 값은 `useEffect` 이후에 설정하도록 옮기세요.
5. **브라우저 지원**: React 18은 Internet Explorer를 더 이상 지원하지 않습니다. Promise, Symbol, Object.assign 같은 기능을 폴리필로 보완해야 하는 환경이라면 확인이 필요합니다.
6. **컴포넌트 반환값**: 컴포넌트가 `undefined`를 반환해도 오류가 나지 않도록 개선되었습니다.
7. **타입 변경**: `React.FC`는 더 이상 `children`을 암묵적으로 포함하지 않습니다. `children`이 필요한 컴포넌트는 props 타입에 직접 명시해야 합니다.

```tsx
// React 18 타입에서는 children을 직접 선언
type CardProps = { title: string; children: React.ReactNode };

function Card({ title, children }: CardProps) {
  return <section><h2>{title}</h2>{children}</section>;
}
```

## 마무리

React 18은 대부분의 기존 앱이 큰 수정 없이 실행되는 것을 목표로 했습니다. 다만 `createRoot` 전환과 Effect 정리 함수 점검은 거의 모든 프로젝트에서 필요한 작업입니다. 업그레이드 후에는 개발 환경에서 Strict Mode 경고를 먼저 해결하고, 이후 트랜지션이나 `useDeferredValue` 같은 동시성 기능을 점진적으로 도입하는 것을 권장합니다.

---

*참고: 이 문서는 React 공식 릴리스 노트(React v18.0)의 내용을 바탕으로 한국어로 재구성한 것입니다. 원문 그대로의 번역이 아니며, 세부 사항이나 최신 API는 react.dev의 공식 문서에서 확인하시기 바랍니다.*
