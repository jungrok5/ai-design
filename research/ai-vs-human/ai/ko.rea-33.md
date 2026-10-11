# renderToStaticMarkup

`renderToStaticMarkup`은 상호작용하지 않는 React 트리를 HTML 문자열로 렌더링합니다.

```js
const html = renderToStaticMarkup(reactNode, options?)
```

---

## 레퍼런스

### `renderToStaticMarkup(reactNode, options?)`

서버에서 `renderToStaticMarkup`을 호출하면 앱을 HTML로 렌더링할 수 있습니다.

```js
import { renderToStaticMarkup } from 'react-dom/server';

const html = renderToStaticMarkup(<Page />);
```

이 함수는 React 컴포넌트를 상호작용하지 않는 HTML로 출력합니다.

#### 매개변수

- `reactNode`: HTML로 렌더링할 React 노드입니다. 예를 들면 `<Page />` 같은 JSX 노드입니다.
- **선택 사항** `options`: 서버 렌더링에 쓰이는 객체입니다.
  - **선택 사항** `identifierPrefix`: [`useId`](/reference/react/useId)가 생성하는 ID 앞에 붙는 문자열 접두사입니다. 같은 페이지에 여러 루트가 있을 때 ID 충돌을 막는 데 쓸 수 있습니다.

#### 반환값

HTML 문자열입니다.

#### 주의 사항

- `renderToStaticMarkup`으로 만든 결과물은 하이드레이션할 수 없습니다.
- `renderToStaticMarkup`은 Suspense를 제한적으로만 지원합니다. 컴포넌트가 일시 중단되면 `renderToStaticMarkup`은 곧바로 폴백을 HTML로 보냅니다.
- `renderToStaticMarkup`은 브라우저에서도 동작하지만 클라이언트 코드에서 사용하는 것은 권장하지 않습니다. 브라우저에서 컴포넌트를 HTML로 렌더링해야 한다면 [DOM 노드에 렌더링한 뒤 HTML을 읽어 오는 방식](/reference/react-dom/server/renderToString#removing-rendertostring-from-the-client-code)을 사용하세요.

---

## 사용법

### 상호작용하지 않는 HTML을 문자열로 렌더링하기

`renderToStaticMarkup`을 호출하면 앱을 HTML 문자열로 렌더링할 수 있고, 이 문자열을 서버 응답으로 보낼 수 있습니다.

```js {5-6}
import { renderToStaticMarkup } from 'react-dom/server';

// 라우트 핸들러 문법은 백엔드 프레임워크에 따라 다릅니다
app.use('/', (request, response) => {
  const html = renderToStaticMarkup(<Page />);
  response.send(html);
});
```

이 코드는 React 컴포넌트를 상호작용하지 않는 HTML로 출력합니다.

> **주의**
>
> 이 메서드로 렌더링한 HTML은 하이드레이션할 수 없으므로 **상호작용하지 않습니다.** 정적 페이지 생성기를 만들 때처럼 React를 단순한 정적 페이지 생성 도구로 쓰려는 경우나, 이메일처럼 완전히 정적인 콘텐츠를 렌더링할 때 유용합니다.
>
> 상호작용하는 앱이라면 서버에서는 [`renderToString`](/reference/react-dom/server/renderToString)을, 클라이언트에서는 [`hydrateRoot`](/reference/react-dom/client/hydrateRoot)를 사용하세요.
