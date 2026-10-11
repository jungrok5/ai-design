# React DOM APIs

`react-dom` 패키지에는 웹 애플리케이션(브라우저 DOM 환경)에서만 지원되는 메서드가 들어 있습니다. 이 메서드들은 React 컴포넌트를 DOM 에 연결하거나, 컴포넌트 트리 바깥으로 렌더링하거나, 렌더링 동작을 세밀하게 제어해야 할 때 사용합니다. 대부분의 컴포넌트에서는 이 API 를 직접 가져올 필요가 없습니다.

```js
import { createPortal, flushSync } from 'react-dom';
```

---

## 리소스 미리 로딩 API

이 API 들은 앱의 성능을 높이기 위해 스크립트, 스타일시트, 폰트 같은 리소스를 미리 불러올 때 사용합니다. 다음 화면에서 필요한 리소스를 브라우저가 미리 준비하도록 알려 줍니다.

- [`prefetchDNS`](https://react.dev/reference/react-dom/prefetchDNS) 는 연결하려는 서버의 IP 주소를 미리 조회합니다.
- [`preconnect`](https://react.dev/reference/react-dom/preconnect) 는 리소스를 아직 사용하지 않더라도 서버에 미리 연결합니다.
- [`preload`](https://react.dev/reference/react-dom/preload) 는 스타일시트, 폰트, 이미지, 외부 스크립트를 가져옵니다.
- [`preloadModule`](https://react.dev/reference/react-dom/preloadModule) 은 ESM 모듈을 가져옵니다.
- [`preinit`](https://react.dev/reference/react-dom/preinit) 은 외부 스크립트를 가져와 실행하거나 스타일시트를 가져와 적용합니다.
- [`preinitModule`](https://react.dev/reference/react-dom/preinitModule) 은 ESM 모듈을 가져와 실행합니다.

```js
import { preconnect, preload } from 'react-dom';

function App() {
  preconnect('https://example.com');
  preload('https://example.com/font.woff2', { as: 'font' });
  return <Page />;
}
```

---

## 일반 API

`react-dom` 에서 제공하는 일반 API 는 다음과 같습니다.

- [`createPortal`](https://react.dev/reference/react-dom/createPortal) 은 자식 요소를 DOM 트리의 다른 위치에 렌더링할 수 있게 해 줍니다. 모달이나 툴팁처럼 부모의 스타일 영향을 받지 않아야 하는 UI 에 유용합니다.
- [`flushSync`](https://react.dev/reference/react-dom/flushSync) 는 전달한 콜백 안의 state 업데이트를 동기적으로 처리하도록 강제하여 DOM 이 즉시 갱신되게 합니다.

```js
import { flushSync } from 'react-dom';

flushSync(() => {
  setCount(count + 1);
});
// 이 시점에는 DOM 이 이미 갱신되어 있습니다.
```

`flushSync` 는 성능에 부담을 줄 수 있으므로 꼭 필요한 경우에만 사용하세요.

---

## 클라이언트 API

`react-dom/client` 패키지는 클라이언트(브라우저)에서 React 컴포넌트를 렌더링하기 위한 API 를 제공합니다. 일반적으로 앱의 최상단에서 한 번 호출합니다.

- [`createRoot`](https://react.dev/reference/react-dom/client/createRoot) 는 브라우저 DOM 노드 안에 React 컴포넌트를 표시할 루트를 만듭니다.
- [`hydrateRoot`](https://react.dev/reference/react-dom/client/hydrateRoot) 는 `react-dom/server` 로 미리 생성된 HTML 에 React 를 연결해 상호작용이 가능하게 합니다.

```js
import { createRoot } from 'react-dom/client';

const root = createRoot(document.getElementById('root'));
root.render(<App />);
```

---

## 서버 API

`react-dom/server` 패키지는 React 컴포넌트를 HTML 로 렌더링하기 위한 API 를 제공합니다. 이 API 들은 서버 환경에서만 사용하며, 초기 HTML 을 빠르게 내려 주거나 정적 페이지를 만들 때 쓰입니다.

- [`renderToPipeableStream`](https://react.dev/reference/react-dom/server/renderToPipeableStream) 은 Node.js 스트림으로 HTML 을 렌더링합니다.
- [`renderToReadableStream`](https://react.dev/reference/react-dom/server/renderToReadableStream) 은 Web Stream 으로 HTML 을 렌더링합니다.
- [`renderToStaticMarkup`](https://react.dev/reference/react-dom/server/renderToStaticMarkup) 은 상호작용이 없는 정적 HTML 문자열을 만듭니다.
- [`renderToString`](https://react.dev/reference/react-dom/server/renderToString) 은 HTML 문자열로 렌더링합니다.

스트리밍 방식은 `Suspense` 와 함께 동작하므로, 가능하면 `renderToString` 보다 스트리밍 API 를 사용하는 것이 좋습니다.

---

## 정적 API

`react-dom/static` 패키지는 React 컴포넌트를 정적 HTML 로 생성하는 API 를 제공합니다. 데이터가 모두 준비될 때까지 기다린 뒤 결과를 반환합니다.

- [`prerender`](https://react.dev/reference/react-dom/static/prerender) 는 Web Stream 환경에서 정적 HTML 을 생성합니다.
- [`prerenderToNodeStream`](https://react.dev/reference/react-dom/static/prerenderToNodeStream) 은 Node.js 스트림 환경에서 정적 HTML 을 생성합니다.

---

## 참고

- 컴포넌트 안에서 DOM 요소를 직접 다뤄야 한다면 `ref` 를 먼저 고려하세요.
- 레거시 API 인 `render`, `hydrate`, `findDOMNode` 는 최신 React 에서 제거되었거나 더 이상 권장되지 않습니다. 새 코드에서는 `createRoot` 와 `hydrateRoot` 를 사용하세요.
