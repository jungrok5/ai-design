# resumeToPipeableStream

<Intro>

`resumeToPipeableStream`은 [사전 렌더링(prerender)](/reference/react-dom/static/prerenderToNodeStream)으로 미리 만들어 둔 React 트리의 렌더링을 이어서 진행하고, 그 결과를 [Node.js 스트림](https://nodejs.org/api/stream.html)으로 내보냅니다.

```js
const { pipe, abort } = resumeToPipeableStream(reactNode, postponedState, options?)
```

</Intro>

<Note>

이 API는 Node.js 전용입니다. Deno나 최신 엣지 런타임처럼 [Web Streams](https://developer.mozilla.org/ko/docs/Web/API/Streams_API)를 지원하는 환경에서는 [`resume`](/reference/react-dom/server/resume)을 사용하세요.

</Note>

---

## 레퍼런스 {/*reference*/}

### `resumeToPipeableStream(reactNode, postponedState, options?)` {/*resume-to-pipeable-stream*/}

`resumeToPipeableStream`을 호출하면 사전 렌더링된 React 트리를 HTML로 이어서 렌더링하고, 그 결과를 Node.js 스트림으로 보냅니다.

```js
import { resumeToPipeableStream } from 'react-dom/server';
import { getPostponedState } from './storage';

function handler(request, response) {
  const postponed = getPostponedState(request);
  const { pipe } = resumeToPipeableStream(<App />, postponed, {
    onShellReady() {
      pipe(response);
    }
  });
}
```

[아래에서 더 많은 예시를 확인하세요.](#usage)

#### 매개변수 {/*parameters*/}

* `reactNode`: `prerender`를 호출할 때 사용한 것과 같은 React 노드입니다. 예를 들어 `<App />` 같은 JSX 엘리먼트입니다. 사전 렌더링할 때와 같은 트리를 넘겨야 합니다.
* `postponedState`: 사전 렌더링 API가 반환한 불투명(opaque)한 `postponed` 객체입니다. 이 객체를 저장해 둔 곳에서 불러와 그대로 전달하세요.
* **선택 사항** `options`: 스트리밍 옵션을 담은 객체입니다.
  * **선택 사항** `nonce`: [`script-src` 콘텐츠 보안 정책(CSP)](https://developer.mozilla.org/ko/docs/Web/HTTP/Headers/Content-Security-Policy/script-src)을 위해 인라인 스크립트에 붙일 [`nonce`](http://developer.mozilla.org/ko/docs/Web/HTML/Element/script#nonce) 문자열입니다.
  * **선택 사항** `signal`: [abort signal](https://developer.mozilla.org/ko/docs/Web/API/AbortSignal)입니다. 이 신호로 서버 렌더링을 중단하면 나머지 부분은 클라이언트에서 렌더링됩니다.
  * **선택 사항** `onError`: 서버에서 오류가 날 때마다 호출되는 콜백입니다. [복구할 수 있는 오류](/reference/react-dom/server/renderToPipeableStream#recovering-from-errors-outside-the-shell)든 [그렇지 않은 오류](/reference/react-dom/server/renderToPipeableStream#recovering-from-errors-inside-the-shell)든 모두 이 콜백을 거칩니다. 기본값은 `console.error`만 호출합니다. [충돌 보고를 기록하도록](/reference/react-dom/server/renderToPipeableStream#logging-crashes-on-the-server) 덮어쓴다면 `console.error`도 계속 호출해 주세요.
  * **선택 사항** `onShellReady`: 셸(shell)이 준비되면 호출되는 콜백입니다. 여기에서 `pipe`를 호출해 스트리밍을 시작할 수 있습니다.
  * **선택 사항** `onShellError`: 셸을 렌더링하다 오류가 나면 호출되는 콜백입니다. 오류 객체를 인수로 받습니다.
  * **선택 사항** `onAllReady`: 셸과 모든 추가 [콘텐츠](/reference/react/Suspense)를 포함해 렌더링이 전부 끝나면 호출되는 콜백입니다.

#### 반환값 {/*returns*/}

`resumeToPipeableStream`은 메서드 두 개를 가진 객체를 반환합니다.

* `pipe`: HTML을 지정한 [쓰기 가능한 Node.js 스트림](https://nodejs.org/api/stream.html#writable-streams)으로 출력합니다. 스트리밍을 켜려면 `onShellReady`에서, 크롤러나 정적 생성에 쓰려면 `onAllReady`에서 `pipe`를 호출하세요.
* `abort`: [서버 렌더링을 중단](/reference/react-dom/server/renderToPipeableStream#aborting-server-rendering)하고 나머지는 클라이언트에서 렌더링하도록 합니다.

#### 주의 사항 {/*caveats*/}

- `resumeToPipeableStream`은 `bootstrapScripts`, `bootstrapScriptContent`, `bootstrapModules` 옵션을 받지 않습니다. 이 옵션들은 `postponedState`를 만드는 `prerender` 호출에 넘겨야 합니다. 부트스트랩 콘텐츠를 프리렌더 결과에 직접 넣어도 됩니다.
- `resumeToPipeableStream`은 `identifierPrefix`도 받지 않습니다. prerender와 resume에서 접두사가 똑같아야 하기 때문입니다.
- `nonce`는 prerender에 넘길 수 없으므로 prerender에 스크립트를 넘기지 않을 때만 resume에 `nonce`를 넘기세요.
- `resumeToPipeableStream`은 완전히 사전 렌더링되지 않은 컴포넌트를 찾을 때까지 루트부터 다시 렌더링합니다. 완전히 사전 렌더링된 컴포넌트(그 컴포넌트와 자식들이 모두 사전 렌더링을 끝낸 경우)만 통째로 건너뜁니다.

---

## 사용법 {/*usage*/}

### 사전 렌더링 이어서 하기 {/*resuming-a-prerender*/}

먼저 빌드 시점이나 캐시 단계에서 `prerender` API로 정적인 셸을 만들고, 반환된 `postponed` 상태를 저장합니다.

```js
import { prerenderToNodeStream } from 'react-dom/static';

const controller = new AbortController();
const { prelude, postponed } = await prerenderToNodeStream(<App />, {
  signal: controller.signal,
});

await savePrelude(prelude);
await savePostponedState(postponed);
```

요청이 들어오면 먼저 저장해 둔 프렐류드(prelude)를 보냅니다. 그다음 `resumeToPipeableStream`으로 미뤄 두었던 동적인 부분을 이어서 스트리밍합니다.

```js {8-14}
import { resumeToPipeableStream } from 'react-dom/server';

async function handler(request, response) {
  const prelude = await getPrelude();
  const postponed = await getPostponedState();

  response.write(prelude);
  const { pipe } = resumeToPipeableStream(<App />, postponed, {
    onShellReady() {
      pipe(response);
    },
    onError(error) {
      console.error(error);
    },
  });
}
```

이렇게 하면 정적인 셸을 캐시나 CDN에서 바로 보내 첫 화면을 빠르게 띄울 수 있습니다. 요청마다 달라지는 데이터가 필요한 부분만 서버에서 렌더링합니다.

<Note>

`resumeToPipeableStream`에 넘기는 `reactNode`는 사전 렌더링할 때 사용한 트리와 같아야 합니다. 트리 구조가 다르면 React가 미뤄 둔 지점을 제대로 찾지 못할 수 있습니다.

</Note>

---

### 추가 자료 {/*further-reading*/}

이어서 렌더링하는 동작은 `renderToPipeableStream`과 비슷합니다. 더 많은 예시는 [`renderToPipeableStream`의 사용법](/reference/react-dom/server/renderToPipeableStream#usage)을 참고하세요. 사전 렌더링에 대해서는 [`prerenderToNodeStream`의 사용법](/reference/react-dom/static/prerenderToNodeStream#usage)을 참고하세요.
