# 'use client'

`'use client'`는 React Server Components(RSC) 환경에서 클라이언트 경계를 선언하는 디렉티브입니다. 파일 맨 위에 이 문자열을 적으면 해당 파일과, 그 파일이 import하는 모듈들이 브라우저에서 실행되는 클라이언트 코드로 취급됩니다.

## 개요

React 컴포넌트는 서버에서 실행될 수도 있고 브라우저에서 실행될 수도 있습니다. 서버 컴포넌트는 서버에서만 실행되고 클라이언트 번들에 포함되지 않습니다. 반면 `useState`, `useEffect`, `onClick` 같은 상태와 인터랙션이 필요한 코드는 브라우저에서 실행되어야 합니다. `'use client'`는 이 경계가 어디인지 번들러에게 알려 줍니다.

```jsx
'use client';

import { useState } from 'react';

export default function Counter() {
  const [count, setCount] = useState(0);
  return (
    <button onClick={() => setCount(count + 1)}>
      클릭 횟수: {count}
    </button>
  );
}
```

## 사용 위치와 문법

- 디렉티브는 파일의 가장 윗부분에 와야 합니다. 주석은 앞에 올 수 있지만 `import`문보다 먼저 나와야 합니다.
- 작은따옴표와 큰따옴표 모두 사용할 수 있습니다.
- 모든 파일에 붙일 필요는 없습니다. 인터랙션이 필요한 컴포넌트 트리의 진입점 파일에만 붙이면 됩니다. 그 파일이 가져오는 하위 모듈은 자동으로 클라이언트 코드가 됩니다.

## 클라이언트 경계의 동작 규칙

`'use client'` 파일은 서버 컴포넌트와 클라이언트 컴포넌트 사이의 관계를 정합니다.

- 서버 컴포넌트는 클라이언트 컴포넌트를 import해서 일반 JSX처럼 렌더링할 수 있습니다.
- 클라이언트 컴포넌트는 서버 컴포넌트를 직접 import할 수 없습니다. 클라이언트 모듈 그래프에 들어가면 서버 전용 코드가 섞이기 때문입니다.
- 서버 컴포넌트를 클라이언트 컴포넌트의 `children`이나 다른 props로 넘기면 렌더링할 수 있습니다. 이 방식은 서버 컴포넌트가 클라이언트 번들에 포함되지 않게 해 줍니다.

```jsx
// app/page.jsx (서버 컴포넌트)
import ClientLayout from './ClientLayout';
import ServerContent from './ServerContent';

export default function Page() {
  return (
    <ClientLayout>
      <ServerContent />
    </ClientLayout>
  );
}
```

```jsx
// ClientLayout.jsx
'use client';

import { useState } from 'react';

export default function ClientLayout({ children }) {
  const [open, setOpen] = useState(false);
  return (
    <div>
      <button onClick={() => setOpen(!open)}>메뉴 열기</button>
      {open && children}
    </div>
  );
}
```

`ServerContent`는 서버에서 미리 렌더링되어 `children`으로 전달되고, 클라이언트 컴포넌트는 그 결과를 보여 주기만 합니다.

## props 직렬화 제약

서버 컴포넌트에서 클라이언트 컴포넌트로 전달하는 props는 직렬화할 수 있어야 합니다. 네트워크를 통해 전달되어야 하기 때문입니다.

전달할 수 있는 값은 다음과 같습니다.

- 문자열, 숫자, 불리언, `null`, `undefined`, `BigInt`
- 배열과 일반 객체
- `Date`, `Map`, `Set`, `TypedArray`
- `'use server'`로 표시된 서버 함수(서버 액션)
- 이들로 구성된 JSX 요소

일반 함수, 클래스 인스턴스, 심볼은 전달할 수 없습니다.

```jsx
// 서버 컴포넌트 안에서 작성하면 오류가 발생합니다
<ClientButton onSelect={(id) => console.log(id)} />
```

이 경우에는 클라이언트 컴포넌트 안에서 핸들러를 정의하거나, 서버에서 실행해야 하는 로직이라면 `'use server'` 함수를 전달합니다.

## export 시 주의할 점

`'use client'` 파일에서 export한 모든 값은 서버에서 보면 클라이언트 참조가 됩니다. 따라서 다음과 같은 문제가 생길 수 있습니다.

- 서버 컴포넌트에서 이 파일의 함수를 직접 호출하면 실패합니다. 컴포넌트로만 렌더링할 수 있습니다.
- 상수나 유틸 함수를 export하면 서버에서 실제 값으로 읽을 수 없습니다.

그래서 서버와 클라이언트가 함께 쓰는 상수나 순수 함수는 디렉티브가 없는 별도 파일로 분리하는 것이 좋습니다.

## 'use client'와 'use server'의 차이

두 디렉티브는 방향이 반대입니다.

| 디렉티브 | 표시 대상 | 의미 |
|---|---|---|
| `'use client'` | 파일 | 이 파일과 하위 모듈을 브라우저 쪽에 둡니다 |
| `'use server'` | 파일 또는 함수 | 이 함수를 서버에서 실행되는 함수로 만듭니다 |

클라이언트 컴포넌트에서 `'use server'` 함수를 호출하면 서버에서 실행되고 결과만 돌아옵니다. 폼 제출이나 데이터 변경에 자주 쓰입니다.

## SSR과 하이드레이션

`'use client'`가 "클라이언트에서만 렌더링한다"는 뜻은 아닙니다. 클라이언트 컴포넌트도 초기 HTML을 만들기 위해 서버에서 한 번 렌더링됩니다. 이후 브라우저가 JavaScript를 불러와 같은 트리에 이벤트 핸들러와 상태를 붙이는 과정이 하이드레이션입니다.

따라서 서버와 클라이언트에서 결과가 달라지면 하이드레이션 불일치 경고가 발생합니다. `window`, `localStorage`, `Date.now()`처럼 환경마다 다른 값은 렌더링 중에 직접 읽지 않고, `useEffect` 안에서 읽는 것이 안전합니다.

## 서드파티 라이브러리 사용법

많은 라이브러리는 내부적으로 훅을 쓰면서도 `'use client'`를 붙이지 않은 채 배포됩니다. 이런 컴포넌트를 서버 컴포넌트에서 바로 가져오면 오류가 발생할 수 있습니다. 이때는 직접 래퍼 파일을 만듭니다.

```jsx
// components/Carousel.jsx
'use client';

export { Carousel } from 'some-carousel-library';
```

서버 컴포넌트는 이 래퍼를 import하면 됩니다. 라이브러리가 이미 `'use client'`를 가지고 있다면 래퍼는 필요하지 않습니다.

## 컨텍스트 제공자 패턴

`createContext`로 만든 Provider는 `useState`를 사용하는 경우가 많으므로 클라이언트 컴포넌트여야 합니다. 보통 Provider를 `'use client'` 파일에 정의하고, 서버 컴포넌트인 레이아웃에서 `children`을 감싸서 사용합니다.

```jsx
// ThemeProvider.jsx
'use client';

import { createContext, useState } from 'react';

export const ThemeContext = createContext('light');

export default function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light');
  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}
```

Context 객체 자체를 export하면 위의 export 주의 사항이 적용되므로, Context를 읽는 훅과 Provider는 클라이언트 파일 안에 두는 편이 안전합니다.

## 적용되지 않는 환경

- RSC를 지원하는 프레임워크나 번들러(예: Next.js App Router)에서 의미가 있습니다.
- 서버 렌더링 없이 클라이언트만으로 동작하는 React 앱(예: Vite SPA, Create React App)에서는 보통 무시됩니다.
- Pages Router처럼 RSC를 쓰지 않는 구조에서도 실행에 영향을 주지 않습니다.

## 정리

- 인터랙션이 필요한 컴포넌트의 진입점 파일에만 `'use client'`를 붙입니다.
- 의존 방향은 서버 컴포넌트에서 클라이언트 컴포넌트로 향하도록 설계합니다.
- 클라이언트로 넘기는 props는 직렬화 가능한 값으로 제한합니다.
- 디렉티브가 붙은 파일의 export는 값으로 쓰이지 않는다고 보고 구조를 나눕니다.
- `'use client'`는 보안 경계가 아닙니다. 클라이언트 번들은 누구나 볼 수 있으므로 비밀 키나 DB 접근 코드는 서버 전용 모듈에 두어야 합니다.

*이 글은 React 공식 문서(react.dev)의 'use client' 항목 내용을 바탕으로 한국어로 정리·재구성한 것입니다.*
