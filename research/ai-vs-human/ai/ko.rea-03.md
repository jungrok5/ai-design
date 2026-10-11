# TypeScript 사용하기

TypeScript는 JavaScript 코드에 타입 정의를 더할 때 많이 쓰는 방법입니다. TypeScript는 기본적으로 JSX를 지원합니다. 여기에 `@types/react`와 `@types/react-dom`을 설치하면 React Web을 완전하게 지원받을 수 있습니다.

> **이 페이지에서 배울 내용**
>
> - React 컴포넌트에서 TypeScript를 쓰는 방법
> - Hook 사용 예시
> - `@types/react`의 주요 타입
> - 더 공부할 수 있는 곳

## 설치

[프로덕션 수준의 React 프레임워크](https://react.dev/learn/creating-a-react-app)는 대부분 TypeScript를 지원합니다. 프레임워크별 설치 안내를 따르세요.

- Next.js
- Remix
- Gatsby
- Expo

### 기존 React 프로젝트에 TypeScript 추가하기

최신 React 타입 정의를 설치하려면 다음 명령어를 실행하세요.

```bash
npm install --save-dev @types/react @types/react-dom
```

`tsconfig.json`에는 아래 컴파일러 옵션을 설정해야 합니다.

1. `lib`에 `dom`이 들어가야 합니다. (참고: `lib`을 지정하지 않으면 `dom`이 기본으로 포함됩니다.)
2. `jsx`를 유효한 값 중 하나로 설정해야 합니다. 대부분의 애플리케이션은 `preserve`면 충분합니다. 라이브러리를 배포한다면 [`jsx` 문서](https://www.typescriptlang.org/tsconfig/#jsx)를 참고해 값을 고르세요.

## React 컴포넌트와 TypeScript

> **중요**
>
> JSX가 들어간 파일은 반드시 `.tsx` 확장자를 써야 합니다. 이 확장자는 해당 파일에 JSX가 있다고 TypeScript에 알려 주는 역할을 합니다.

React에서 TypeScript를 쓰는 방식은 JavaScript와 아주 비슷합니다. 가장 큰 차이는 컴포넌트의 props에 타입을 줄 수 있다는 점입니다. 이 타입으로 코드가 맞는지 검사할 수 있고, 에디터에서 인라인 문서도 볼 수 있습니다.

[빠르게 시작하기](https://react.dev/learn) 가이드의 `MyButton` 컴포넌트에 버튼의 `title`을 설명하는 타입을 추가해 보겠습니다.

```tsx
function MyButton({ title }: { title: string }) {
  return <button>{title}</button>;
}

export default function MyApp() {
  return (
    <div>
      <h1>Welcome to my app</h1>
      <MyButton title="I'm a button" />
    </div>
  );
}
```

이렇게 인라인으로 적는 방식은 타입을 붙이는 가장 간단한 방법입니다. 설명할 필드가 많아지면 `interface`나 `type`으로 따로 정의하는 편이 읽기 좋습니다.

```tsx
interface MyButtonProps {
  /** 버튼 안에 표시할 텍스트 */
  title: string;
  /** 버튼과 상호작용할 수 있는지 여부 */
  disabled: boolean;
}

function MyButton({ title, disabled }: MyButtonProps) {
  return <button disabled={disabled}>{title}</button>;
}
```

props 타입은 객체 타입이므로 필요한 만큼 단순하게도, 복잡하게도 만들 수 있습니다. 다만 객체 타입이어야 한다는 점은 지켜야 합니다. 유니온 타입이나 제네릭 같은 고급 기능은 [TypeScript 핸드북](https://www.typescriptlang.org/docs/handbook/)에서 자세히 다룹니다.

## Hook 예시

`@types/react`의 타입 정의에는 내장 Hook의 타입도 들어 있습니다. 그래서 별도 설정 없이 컴포넌트에서 바로 Hook을 쓸 수 있습니다. 이 타입들은 작성한 코드를 바탕으로 동작하도록 만들어져 있어서, 대부분 [추론된 타입](https://www.typescriptlang.org/docs/handbook/type-inference.html)을 그대로 쓰면 됩니다. 그래도 타입을 직접 지정해야 하는 경우가 있으니 몇 가지 예를 살펴보겠습니다.

### `useState`

`useState`는 초기값을 보고 상태의 타입을 추론합니다.

```tsx
// 타입이 "boolean"으로 추론됩니다
const [enabled, setEnabled] = useState(false);
```

`setEnabled`에는 `boolean`만 넘길 수 있습니다. 상태에 직접 타입을 지정하고 싶다면 제네릭 인수를 사용하세요.

```tsx
// 타입을 명시적으로 "boolean"으로 지정합니다
const [enabled, setEnabled] = useState<boolean>(false);
```

여러 값 중 하나를 갖는 상태라면 유니온 타입이 유용합니다.

```tsx
type Status = "idle" | "loading" | "success" | "error";

const [status, setStatus] = useState<Status>("idle");
```

[상태 구조화 원칙](https://react.dev/learn/choosing-the-state-structure)에 따라, 관련 있는 상태는 객체 하나로 묶고 객체 타입의 유니온으로 각 경우를 표현할 수도 있습니다.

```tsx
type RequestState =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: any }
  | { status: "error"; error: Error };

const [requestState, setRequestState] = useState<RequestState>({ status: "idle" });
```

### `useReducer`

`useReducer`는 리듀서 함수와 초기 상태를 받습니다. 리듀서 함수의 타입은 초기 상태에서 추론됩니다. 상태 타입을 제네릭 인수로 줄 수도 있지만, 보통은 초기 상태에 타입을 붙이는 쪽을 권장합니다.

```tsx
import { useReducer } from "react";

interface State {
  count: number;
}

type CounterAction =
  | { type: "reset" }
  | { type: "setCount"; value: State["count"] };

const initialState: State = { count: 0 };

function stateReducer(state: State, action: CounterAction): State {
  switch (action.type) {
    case "reset":
      return initialState;
    case "setCount":
      return { ...state, count: action.value };
    default:
      throw new Error("Unknown action");
  }
}

export default function App() {
  const [state, dispatch] = useReducer(stateReducer, initialState);
  // ...
}
```

### `useContext`

`useContext`는 props를 넘기지 않고도 컴포넌트 트리 아래로 데이터를 전달하는 방법입니다. 컨텍스트 값의 타입은 `createContext`에 넘긴 값에서 추론됩니다.

```tsx
type Theme = "light" | "dark" | "system";
const ThemeContext = createContext<Theme>("system");

const useGetTheme = () => useContext(ThemeContext);
```

알맞은 기본값이 없다면 `null`을 쓸 수 있습니다. 이때는 `ContextShape | null` 형태로 타입을 지정하고, 컨텍스트를 사용하는 쪽에서 `null`을 걸러 주는 것이 좋습니다.

```tsx
const Context = createContext<ComplexObject | null>(null);

const useGetComplexObject = () => {
  const object = useContext(Context);
  if (!object) {
    throw new Error("useGetComplexObject must be used within a Provider");
  }
  return object;
};
```

### `useMemo`와 `useCallback`

`useMemo`의 타입은 함수의 반환값에서, `useCallback`의 타입은 함수 자체에서 추론됩니다. `useCallback`을 쓸 때는 매개변수에 타입을 붙여야 합니다. 그렇지 않으면 TypeScript의 strict 모드에서 오류가 납니다.

```tsx
const handleChange = useCallback(
  (event: React.ChangeEvent<HTMLInputElement>) => {
    setValue(event.currentTarget.value);
  },
  [setValue]
);
```

## 유용한 타입

`@types/react`에는 타입이 아주 많습니다. 그중 자주 쓰는 것만 소개합니다.

### DOM 이벤트

React에서 DOM 이벤트를 다룰 때는 대개 이벤트 핸들러에서 이벤트 타입이 추론됩니다. 다만 핸들러 함수를 따로 빼서 정의할 때는 이벤트 타입을 직접 지정해야 합니다.

```tsx
function handleChange(event: React.ChangeEvent<HTMLInputElement>) {
  setValue(event.currentTarget.value);
}
```

어떤 타입을 써야 할지 모르겠다면 에디터에서 핸들러 위에 마우스를 올려 보세요. 해당 이벤트의 타입이 표시됩니다.

### 자식 요소(children)

컴포넌트의 자식을 표현하는 방법은 크게 두 가지입니다.

```tsx
interface ModalRendererProps {
  title: string;
  children: React.ReactNode;
}
```

`React.ReactNode`는 JSX에서 자식으로 넘길 수 있는 모든 타입을 아우르는 유니온입니다.

```tsx
interface ModalRendererProps {
  title: string;
  children: React.ReactElement;
}
```

`React.ReactElement`는 JSX 요소만 받고, 문자열이나 숫자 같은 원시 값은 받지 않습니다. 참고로 TypeScript로는 자식이 *특정* JSX 요소인지까지 검사할 수 없습니다.

### 스타일 props

React에서 인라인 스타일을 쓸 때는 `React.CSSProperties`로 `style` prop에 넘길 객체의 타입을 지정할 수 있습니다. 이 타입은 사용할 수 있는 CSS 속성을 모두 포함하고 있어서, 올바른 속성을 넘기는지 확인하고 에디터 자동완성도 받을 수 있습니다.

```tsx
interface MyComponentProps {
  style: React.CSSProperties;
}
```

## 더 알아보기

이 페이지에서는 React와 함께 TypeScript를 쓰는 기본만 다뤘지만, 배울 내용은 훨씬 더 많습니다. API 레퍼런스의 각 페이지에서도 TypeScript 사용법을 더 자세히 다룹니다.

- [TypeScript 핸드북](https://www.typescriptlang.org/docs/handbook/): TypeScript 공식 문서이며, 언어의 핵심 기능을 대부분 설명합니다.
- [TypeScript 릴리스 노트](https://devblogs.microsoft.com/typescript/): 새로 추가된 기능을 자세히 소개합니다.
- [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/): 커뮤니티가 관리하는 React + TypeScript 치트시트로, 유용한 예외 상황이 많이 정리되어 있고 이 문서보다 다루는 범위가 넓습니다.
- [TypeScript 커뮤니티 Discord](https://discord.com/invite/typescript): React와 TypeScript를 쓰다 생긴 문제를 질문하고 도움을 받을 수 있는 곳입니다.
