# prerender

`prerender`는 `react-dom/static`이 제공하는 API로, React 트리를 빌드 시점에 정적 HTML로 렌더링합니다. 모든 Suspense 경계의 데이터가 준비될 때까지 기다린 뒤 완성된 HTML 스트림을 반환하므로, 정적 사이트 생성(SSG)이나 미리 만들어 둘 페이지를 준비할 때 사용합니다.

> `prerender`는 React 19.2부터 사용할 수 있습니다. 이전 버전에서는 `react-dom/server`의 `renderToReadableStream`이나 `renderToPipeableStream`을 사용해야 합니다.

---

## 레퍼런스

### `prerender(reactNode, options?)`

`prerender(reactNode, options?)`를 호출하여 React 노드를 정적 HTML 스트림으로 변환합니다.

```js
import { prerender } from 'react-dom/static';

const { prelude } = await prerender(<App />, {
  bootstrapScripts: ['/main.js'],
});
```

`prerender`는 Promise를 반환합니다. 렌더링이 끝나면 `prelude`라는 속성을 가진 객체로 해결(resolve)됩니다.

#### 매개변수

* `reactNode`: 렌더링할 React 노드입니다. 예를 들어 `<App />`처럼 JSX로 작성한 요소가 여기에 해당합니다. 문자열, 숫자, 배열 같은 다른 React 노드도 사용할 수 있습니다.
* `options`(선택): 렌더링 동작을 조절하는 객체입니다. 자세한 내용은 아래 **옵션** 절을 참고하세요.

#### 반환값

`prerender`는 다음 속성을 가진 객체로 해결되는 Promise를 반환합니다.

* `prelude`: 완성된 HTML을 담은 웹 표준 `ReadableStream`입니다. 이 스트림을 문자열로 바꾸거나 파일에 쓸 수 있습니다.

Promise는 다음과 같은 경우에 거부(reject)됩니다.

* 렌더링 중 복구할 수 없는 오류가 발생한 경우
* `signal`로 중단 요청을 받은 경우

#### 옵션

| 옵션 | 타입 | 설명 |
| --- | --- | --- |
| `signal` | `AbortSignal` | 렌더링을 중단하기 위한 신호입니다. 중단되면 Promise가 거부됩니다. |
| `onError` | `(error) => string \| void` | 렌더링 중 오류가 발생했을 때 호출됩니다. 반환한 문자열은 서버 오류 다이제스트로 사용됩니다. |
| `bootstrapScripts` | `string[]` | 페이지에 `<script>` 태그로 추가할 스크립트 경로 목록입니다. |
| `bootstrapModules` | `string[]` | 페이지에 `<script type="module">` 태그로 추가할 모듈 경로 목록입니다. |
| `identifierPrefix` | `string` | `useId`로 생성되는 ID의 접두사입니다. 한 페이지에 여러 React 루트가 있을 때 ID 충돌을 막는 데 사용합니다. |
| `namespaceURI` | `string` | 루트 요소의 네임스페이스 URI입니다. SVG나 MathML을 렌더링할 때 사용합니다. |
| `nonce` | `string` | 인라인 스크립트와 스타일에 적용할 `nonce` 값입니다. Content Security Policy와 함께 사용합니다. |
| `progressiveChunkSize` | `number` | 스트림을 나눌 청크 크기의 기준값(바이트)입니다. 기본값을 쓰는 것이 대부분의 경우 적절합니다. |

---

## 사용법

### 정적 HTML 파일 생성하기

빌드 스크립트에서 `prerender`를 호출하고, 반환된 스트림을 문자열로 읽어 파일에 씁니다.

```js
import { prerender } from 'react-dom/static';
import { writeFile } from 'node:fs/promises';
import App from './App.js';

async function build() {
  const { prelude } = await prerender(<App />, {
    bootstrapModules: ['/assets/main.js'],
  });

  const html = await new Response(prelude).text();
  await writeFile('dist/index.html', html);
}

build();
```

`prelude`는 웹 표준 스트림이므로 `Response` 객체로 감싸면 간단하게 텍스트로 바꿀 수 있습니다.

### Suspense로 데이터 기다리기

`prerender`는 Suspense 경계 안에서 아직 끝나지 않은 데이터가 있으면, 그 데이터가 준비될 때까지 기다린 후 HTML을 완성합니다. 따라서 빌드 결과에는 로딩 상태가 아니라 데이터가 채워진 실제 콘텐츠가 들어갑니다.

```jsx
import { Suspense } from 'react';

async function getPosts() {
  const response = await fetch('https://api.example.com/posts');
  return response.json();
}

async function Posts() {
  const posts = await getPosts();
  return (
    <ul>
      {posts.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  );
}

export default function App() {
  return (
    <main>
      <h1>블로그</h1>
      <Suspense fallback={<p>불러오는 중...</p>}>
        <Posts />
      </Suspense>
    </main>
  );
}
```

위 코드를 `prerender`로 렌더링하면 `fallback`이 아니라 게시글 목록이 포함된 HTML이 생성됩니다.

### 렌더링 중단하기

오래 걸리는 렌더링은 `AbortController`로 중단할 수 있습니다. 시간 제한을 두고 싶을 때 유용합니다.

```js
const controller = new AbortController();
const timeout = setTimeout(() => controller.abort(), 10_000);

try {
  const { prelude } = await prerender(<App />, {
    signal: controller.signal,
  });
  // prelude 사용
} finally {
  clearTimeout(timeout);
}
```

중단되면 Promise가 거부되므로 `try`/`catch`로 처리해야 합니다.

### 오류 처리하기

`onError` 옵션으로 렌더링 중 발생한 오류를 기록할 수 있습니다. 반환한 문자열은 서버에서 발생한 오류를 식별하는 다이제스트로 HTML에 포함됩니다.

```js
const { prelude } = await prerender(<App />, {
  onError(error) {
    console.error('prerender 오류:', error);
    return error.digest;
  },
});
```

클라이언트에서 같은 오류를 식별하려면 다이제스트 값을 로그와 함께 남겨 두세요.

---

## 주의 사항

* **`prerender`는 빌드 환경에서 사용하는 API입니다.** 요청마다 실행되는 서버 렌더링에는 `react-dom/server`를 사용하는 것이 적절합니다. 두 API의 차이는 `prerender`가 모든 데이터가 준비될 때까지 기다린다는 점입니다.
* **모든 Suspense 경계가 완료되어야 결과가 반환됩니다.** 중간에 영원히 끝나지 않는 Promise가 있으면 `prerender`도 끝나지 않으므로, 외부 요청에는 시간 제한을 두는 것이 좋습니다.
* **클라이언트 전용 코드는 HTML에 포함되지 않습니다.** `window`, `localStorage`처럼 브라우저에만 있는 값을 렌더링 중에 직접 사용하면 오류가 발생합니다. 이런 코드는 `useEffect` 안이나 클라이언트 전용 컴포넌트로 옮기세요.
* **상호작용은 하이드레이션 후에 동작합니다.** `prerender`가 만든 HTML은 정적 콘텐츠이므로, 버튼 클릭 같은 이벤트는 클라이언트에서 같은 트리를 `hydrateRoot`로 연결한 뒤에야 동작합니다.
* **`bootstrapScripts`나 `bootstrapModules`를 지정하지 않으면** 생성된 HTML에 클라이언트 번들이 포함되지 않습니다. 하이드레이션이 필요하다면 빌드된 번들 경로를 반드시 전달하세요.

---

## 문제 해결

### 생성된 HTML에 로딩 중 문구만 보입니다

`prerender`가 Suspense 경계의 데이터를 기다리지 않았을 가능성이 있습니다. 데이터를 가져오는 컴포넌트가 실제로 `await`되고 있는지, 그리고 `fetch`가 오류 없이 끝나는지 확인하세요.

### 하이드레이션 불일치 경고가 나옵니다

빌드 시점과 클라이언트의 렌더링 결과가 다를 때 발생합니다. 날짜, 난수, `window` 값처럼 실행 환경에 따라 달라지는 값을 렌더링에 직접 사용하지 않았는지 확인하세요.

### 빌드가 멈춘 것처럼 보입니다

완료되지 않는 Promise가 있는지 확인하고, `signal` 옵션으로 시간 제한을 설정해 보세요. 어떤 컴포넌트가 원인인지 파악하려면 `onError`와 로그를 함께 확인하는 것이 도움이 됩니다.
