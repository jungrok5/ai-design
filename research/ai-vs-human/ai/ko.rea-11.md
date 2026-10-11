# isValidElement

`isValidElement`는 어떤 값이 React 요소(React element)인지 확인하는 함수입니다. 값이 React 요소이면 `true`를 반환하고, 그렇지 않으면 `false`를 반환합니다.

```js
const isElement = isValidElement(value);
```

## 레퍼런스

### `isValidElement(value)`

`value`가 React 요소인지 확인하려면 `isValidElement(value)`를 호출합니다.

#### 매개변수

- `value`: 확인하고 싶은 값입니다. 어떤 타입의 값이든 전달할 수 있습니다.

#### 반환 값

`value`가 React 요소이면 `true`, 그렇지 않으면 `false`를 반환합니다.

#### 주의 사항

- JSX 표현식(`<div />`)이나 `createElement`로 만든 결과는 React 요소이므로 `true`를 반환합니다.
- 문자열, 숫자, `boolean`, `null`, `undefined`, 배열은 React 요소가 아니므로 `false`를 반환합니다.
- 컴포넌트 자체(함수나 클래스)는 React 요소가 아닙니다. 요소는 컴포넌트를 렌더링하기 위해 만들어진 객체입니다. 따라서 `isValidElement(MyComponent)`는 `false`이고, `isValidElement(<MyComponent />)`는 `true`입니다.
- React 요소의 내부 구조(예: `$$typeof` 속성)는 React의 내부 구현입니다. 이에 의존하는 코드를 작성하지 마세요. 요소 여부는 반드시 `isValidElement`로 확인하세요.

## 사용법

### React 요소인지 확인하기

```jsx
import { isValidElement } from 'react';

console.log(isValidElement(<p>안녕하세요</p>)); // true
console.log(isValidElement('안녕하세요'));       // false
console.log(isValidElement(null));              // false
console.log(isValidElement([<p key="a" />]));   // false
```

### `children` 값 처리하기

부모 컴포넌트가 받은 `children`이 요소인지 확인한 뒤, 요소일 때만 속성을 추가할 수 있습니다. 문자열처럼 요소가 아닌 값에 `cloneElement`를 호출하면 오류가 발생하므로, 이 검사가 필요합니다.

```jsx
import { isValidElement, cloneElement } from 'react';

function Highlight({ children }) {
  if (isValidElement(children)) {
    return <section>{cloneElement(children, { className: 'highlight' })}</section>;
  }
  return <section>{children}</section>;
}
```

## 참고

대부분의 경우 `isValidElement`를 직접 호출할 필요는 없습니다. 자식 요소를 순회하거나 변환해야 한다면 `Children` API를 먼저 검토하세요. `isValidElement`는 값의 종류를 명확히 구분해야 하는 라이브러리나 고급 컴포넌트를 만들 때 특히 유용합니다.
