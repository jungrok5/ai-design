# renderToString

<Pitfall>

`renderToString`은 스트리밍이나 데이터 로딩 대기를 지원하지 않습니다. [대안 보기](#alternatives)

</Pitfall>

`renderToString`은 React 트리를 HTML 문자열로 렌더링합니다.

```js
const html = renderToString(reactNode, options?)
```

---

## 레퍼런스 {/*reference*/}

### `renderToString(reactNode, options?)` {/*rendertostring*/}

서버에서 `renderToString`을 호출하면 앱이 HTML로 렌더링됩니다.

```js
import { renderToString } from 'react-dom/server';

const html = renderToString(<App />);
```

클라이언트에서는 [`hydrateRoot`](/reference/react-dom/client/hydrateRoot)를 호출해 서버에서 생성된 HTML을 상호작용할 수 있게 만듭니다.

#### 매개변수 {/*parameters*/}

* `reactNode`: HTML로 렌더링할 React 노드입니다. 예를 들어 `<App />`과 같은 JSX 노드입니다.

* **선택 사항** `options`: 서버 렌더링 옵션을 담은 객체입니다.
  * **선택 사항** `identifierPrefix`: React가 [`useId`](/reference/react/useId)로 생성하는 ID에 붙일 문자열 접두사입니다. 같은 페이지에서 여러 개의 루트를 사용할 때 충돌을 피하는 데 유용합니다. [`hydrateRoot`](/reference/react-dom/client/hydrateRoot#parameters)에 전달하는 접두사와 같아야 합니다.

#### 반환값 {/*returns*/}

HTML 문자열을 반환합니다.

#### 주의 사항 {/*caveats*/}

* `renderToString`은 Suspense 지원이 제한적입니다. 컴포넌트가 일시 중단되면 `renderToString`은 즉시 해당 폴백을 HTML로 보냅니다.

* `renderToString`은 브라우저에서도 동작하지만, 클라이언트 코드에서 사용하는 것은 [권장하지 않습니다.](#removing-rendertostring-from-the-client-code)

---

## 사용법 {/*usage*/}

### React 트리를 HTML 문자열로 렌더링하기 {/*rendering-a-react-tree-as-html-to-a-string*/}

`renderToString`을 호출하면 앱을 HTML 문자열로 렌더링해 서버 응답으로 보낼 수 있습니다.

```js {5-6}
import { renderToString } from 'react-dom/server';

// 라우트 핸들러 문법은 백엔드 프레임워크에 따라 다릅니다
app.use('/', (request, response) => {
  const html = renderToString(<App />);
  response.send(html);
});
```

이렇게 하면 React 컴포넌트의 상호작용이 없는 초기 HTML 출력이 만들어집니다. 클라이언트에서는 서버에서 생성된 HTML을 *하이드레이션*하고 상호작용할 수 있도록 [`hydrateRoot`](/reference/react-dom/client/hydrateRoot)를 호출해야 합니다.

<Pitfall>

`renderToString`은 스트리밍이나 데이터 로딩 대기를 지원하지 않습니다. [대안 보기](#alternatives)

</Pitfall>

---

## 대안 {/*alternatives*/}

### 서버에서 `renderToString`을 스트리밍 렌더링으로 전환하기 {/*migrating-from-rendertostring-to-a-streaming-render-on-the-server*/}

`renderToString`은 문자열을 즉시 반환하므로 스트리밍이나 데이터 로딩 대기를 지원하지 않습니다.

가능하다면 다음과 같이 완전한 기능을 갖춘 대안을 사용하는 것을 권장합니다.

* Node.js를 사용한다면 [`renderToPipeableStream`](/reference/react-dom/server/renderToPipeableStream)을 사용하세요.
* Deno나 Web Stream을 지원하는 최신 엣지 런타임을 사용한다면 [`renderToReadableStream`](/reference/react-dom/server/renderToReadableStream)을 사용하세요.

서버 환경이 스트림을 지원하지 않는다면 `renderToString`을 계속 사용해도 됩니다.

---

### 정적 사이트 생성을 위해 `renderToString`을 정적 사전 렌더링으로 전환하기 {/*migrating-from-rendertostring-to-a-static-prerender-on-the-server*/}

`renderToString`은 문자열을 즉시 반환하므로 정적 HTML을 생성할 때 데이터 로딩이 끝나기를 기다릴 수 없습니다.

다음과 같이 완전한 기능을 갖춘 대안을 사용하는 것을 권장합니다.

* Node.js를 사용한다면 [`prerenderToNodeStream`](/reference/react-dom/static/prerenderToNodeStream)을 사용하세요.
* Deno나 Web Stream을 지원하는 최신 엣지 런타임을 사용한다면 [`prerender`](/reference/react-dom/static/prerender)를 사용하세요.

정적 사이트 생성 환경이 스트림을 지원하지 않는다면 `renderToString`을 계속 사용해도 됩니다.

---

### 클라이언트 코드에서 `renderToString` 제거하기 {/*removing-rendertostring-from-the-client-code*/}

컴포넌트를 HTML로 변환하려고 클라이언트에서 `renderToString`을 사용하는 경우가 있습니다.

```js {1-2}
// 🚩 불필요: 클라이언트에서 renderToString 사용
import { renderToString } from 'react-dom/server';

const html = renderToString(<MyIcon />);
console.log(html); // 예: "<svg>...</svg>"
```

**클라이언트에서** `react-dom/server`를 import하면 번들 크기가 불필요하게 커지므로 피해야 합니다. 브라우저에서 컴포넌트를 HTML로 렌더링해야 한다면 [`createRoot`](/reference/react-dom/client/createRoot)를 사용하고 DOM에서 HTML을 읽으세요.

```js
import { createRoot } from 'react-dom/client';
import { flushSync } from 'react-dom';

const div = document.createElement('div');
const root = createRoot(div);
flushSync(() => {
  root.render(<MyIcon />);
});
console.log(div.innerHTML); // 예: "<svg>...</svg>"
```

[`flushSync`](/reference/react-dom/flushSync) 호출은 [`innerHTML`](https://developer.mozilla.org/ko/docs/Web/API/Element/innerHTML) 속성을 읽기 전에 DOM을 업데이트하기 위해 필요합니다.

---

## 문제 해결 {/*troubleshooting*/}

### 컴포넌트가 일시 중단되면 HTML에 항상 폴백이 포함됩니다 {/*when-a-component-suspends-the-html-always-contains-a-fallback*/}

`renderToString`은 Suspense를 완전히 지원하지 않습니다.

컴포넌트가 일시 중단되면(예를 들어 [`lazy`](/reference/react/lazy)로 정의되었거나 데이터를 가져오는 경우), `renderToString`은 해당 콘텐츠가 준비될 때까지 기다리지 않습니다. 대신 그 위에서 가장 가까운 [`<Suspense>`](/reference/react/Suspense) 경계를 찾아 `fallback` prop을 HTML로 렌더링합니다. 실제 콘텐츠는 클라이언트 코드가 로드된 뒤에야 나타납니다.

이 문제를 해결하려면 [권장 스트리밍 방식](#migrating-from-rendertostring-to-a-streaming-render-on-the-server) 중 하나를 사용하세요. 서버 렌더링에서는 서버에서 콘텐츠가 준비되는 대로 청크 단위로 스트리밍할 수 있습니다. 그러면 클라이언트 코드가 로드되기 전에도 사용자가 페이지가 점진적으로 채워지는 모습을 볼 수 있습니다. 정적 사이트 생성에서는 [권장 정적 사전 렌더링 방식](#migrating-from-rendertostring-to-a-static-prerender-on-the-server) 중 하나를 사용하면, 정적 HTML을 생성하기 전에 모든 콘텐츠가 준비될 때까지 기다릴 수 있습니다.
