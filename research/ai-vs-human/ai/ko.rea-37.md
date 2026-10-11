# captureOwnerStack

`captureOwnerStack`은 현재 **소유자 스택(Owner Stack)**을 문자열로 반환합니다. 소유자 스택이 없거나 사용할 수 없으면 `null`을 반환합니다.

> **참고**
> `captureOwnerStack`은 개발 환경에서만 동작합니다. 프로덕션 빌드에서는 항상 `null`을 반환합니다.

```js
const stack = captureOwnerStack();
```

- [레퍼런스](#reference)
  - [`captureOwnerStack()`](#captureownerstack)
- [사용법](#usage)
  - [커스텀 오류 오버레이 만들기](#enhancing-a-custom-error-overlay)
- [문제 해결](#troubleshooting)
  - [소유자 스택이 `null`입니다](#the-owner-stack-is-null)
  - [`captureOwnerStack`을 사용할 수 없습니다](#captureownerstack-is-not-available)

---

## 레퍼런스 {/*reference*/}

### `captureOwnerStack()` {/*captureownerstack*/}

현재 소유자 스택을 가져오려면 `captureOwnerStack`을 호출하세요.

```js {1,5,7}
import * as React from 'react';

function Component() {
  if (process.env.NODE_ENV !== 'production') {
    const ownerStack = React.captureOwnerStack();
    console.log(ownerStack);
  }
}
```

#### 매개변수 {/*parameters*/}

`captureOwnerStack`은 매개변수를 받지 않습니다.

#### 반환값 {/*returns*/}

`captureOwnerStack`은 `string | null`을 반환합니다.

소유자 스택은 다음 조건에서 사용할 수 있습니다.

- 컴포넌트 렌더링 중
- `useEffect`, `useLayoutEffect` 안에서
- React 이벤트 핸들러 안에서 (예: `<button onClick={...} />`)
- React 오류 핸들러 안에서 (예: `createRoot`의 `onCaughtError`, `onRecoverableError`, `onUncaughtError` 옵션)

사용할 수 없는 상황에서는 `null`을 반환합니다. 자세한 내용은 [문제 해결](#the-owner-stack-is-null)을 참고하세요.

#### 주의 사항 {/*caveats*/}

- 소유자 스택은 **개발 환경에서만** 제공됩니다. 프로덕션에서는 `captureOwnerStack`이 항상 `null`을 반환합니다.
- 소유자 스택 문자열은 JavaScript 엔진마다 형식이 다를 수 있습니다. 형식에 의존하는 파싱 코드는 피하세요.

<DeepDive>

#### 소유자 스택과 컴포넌트 스택의 차이 {/*owner-stack-vs-component-stack*/}

**소유자 스택**은 컴포넌트 스택과 다릅니다.

- **컴포넌트 스택**은 컴포넌트가 *트리 어디에 위치하는지*를 보여줍니다. 즉, 부모–자식 관계를 따라 올라갑니다.
- **소유자 스택**은 컴포넌트를 *누가 렌더링했는지*를 보여줍니다. 즉, 해당 엘리먼트를 만든(JSX를 작성한) 컴포넌트들의 사슬을 따라갑니다.

예를 들어 `App`이 `<Layout><Button /></Layout>`를 렌더링한다면, `Button`의 컴포넌트 스택에는 `Layout`이 포함되지만 소유자는 `App`입니다. 어떤 컴포넌트가 잘못된 props를 전달했는지 찾을 때는 소유자 스택이 훨씬 유용합니다.

</DeepDive>

---

## 사용법 {/*usage*/}

### 커스텀 오류 오버레이 만들기 {/*enhancing-a-custom-error-overlay*/}

개발 중 오류가 발생했을 때 직접 만든 오류 오버레이에 소유자 스택을 함께 보여주고 싶다면, [루트의 오류 핸들러](/reference/react-dom/client/createRoot#parameters)에서 `captureOwnerStack`을 호출하세요.

```js [[2, 8, "console.error"], [1, 5, "captureOwnerStack"]]
import { createRoot } from 'react-dom/client';
import { captureOwnerStack } from 'react';
import { reportOverlay } from './overlay';

createRoot(document.getElementById('root'), {
  onUncaughtError(error, errorInfo) {
    const ownerStack = captureOwnerStack();
    console.error(error);
    reportOverlay({
      message: error.message,
      componentStack: errorInfo.componentStack,
      ownerStack,
    });
  },
}).render(<App />);
```

이렇게 하면 오버레이에 *오류가 발생한 위치*(컴포넌트 스택)와 *그 컴포넌트를 렌더링한 주체*(소유자 스택)를 함께 표시할 수 있습니다.

`console.error`를 가로채서 경고에 소유자 스택을 덧붙이는 것도 가능합니다.

```js
if (process.env.NODE_ENV !== 'production') {
  const originalError = console.error;
  console.error = function patchedError(...args) {
    const owner = captureOwnerStack();
    originalError.apply(this, [...args, owner ?? '']);
  };
}
```

> **주의**
> 이런 패치는 개발 환경에서만 사용하세요. 프로덕션 번들에 포함되지 않도록 `process.env.NODE_ENV` 검사로 감싸야 합니다.

---

## 문제 해결 {/*troubleshooting*/}

### 소유자 스택이 `null`입니다 {/*the-owner-stack-is-null*/}

다음과 같은 경우 `captureOwnerStack`이 `null`을 반환할 수 있습니다.

- **React가 실행 중인 코드가 아닐 때.** `setTimeout`, `fetch().then(...)` 같은 비동기 콜백이나 React와 무관한 이벤트 리스너 안에서는 소유자 스택이 없습니다. 필요하다면 렌더링이나 이벤트 핸들러 안에서 미리 캡처해 두세요.
- **프로덕션 빌드일 때.** 소유자 스택은 개발 환경 전용입니다.
- **서버 컴포넌트가 아닌 곳에서 서버 전용 정보를 기대할 때.** 서버에서 렌더링된 소유자 정보는 클라이언트에서 같은 방식으로 보이지 않을 수 있습니다.

```js
function Component() {
  // 렌더링 중에 미리 캡처
  const ownerStack = captureOwnerStack();

  useEffect(() => {
    setTimeout(() => {
      // 여기서 captureOwnerStack()을 호출하면 null일 수 있습니다.
      console.log(ownerStack);
    }, 1000);
  }, []);
}
```

### `captureOwnerStack`을 사용할 수 없습니다 {/*captureownerstack-is-not-available*/}

`captureOwnerStack`은 `react` 패키지의 최신 안정 버전(19.1 이상)에서 export됩니다. 가져오기가 `undefined`라면 React 버전을 확인하세요.

```bash
npm install react@latest react-dom@latest
```

또한 `import { captureOwnerStack } from 'react'`처럼 올바른 패키지에서 가져오고 있는지 확인하세요. `react-dom`에서는 export되지 않습니다.
