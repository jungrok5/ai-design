# compilationMode

`compilationMode`는 React Compiler가 소스 코드의 어떤 함수를 컴파일(최적화)할지 결정하는 옵션입니다. React Compiler의 Babel 플러그인(`babel-plugin-react-compiler`)에 전달하며, 기본값은 `'infer'`입니다.

## 값

| 값 | 설명 |
|---|---|
| `'infer'` (기본값) | 이름 규칙으로 컴포넌트와 훅을 추론해 컴파일합니다. 컴포넌트는 PascalCase 이름을, 훅은 `use`로 시작하는 이름을 가진 함수입니다. |
| `'annotation'` | 함수 본문 첫 줄에 `"use memo"` 지시어가 있는 함수만 컴파일합니다. |
| `'all'` | 최상위 함수를 모두 컴파일합니다. React와 무관한 함수도 대상이 되므로 권장하지 않습니다. |
| `'syntax'` | Flow의 `component`, `hook` 문법으로 선언된 것만 컴파일합니다. 실험적 기능입니다. |

## 설정 예시

Babel 설정:

```js
// babel.config.js
module.exports = {
  plugins: [
    ['babel-plugin-react-compiler', { compilationMode: 'annotation' }],
  ],
};
```

Vite에서 `@vitejs/plugin-react`를 사용하는 경우:

```js
// vite.config.js
import react from '@vitejs/plugin-react';

export default {
  plugins: [
    react({
      babel: {
        plugins: [
          ['babel-plugin-react-compiler', { compilationMode: 'annotation' }],
        ],
      },
    }),
  ],
};
```

## annotation 모드 예시

```jsx
function TodoList({ todos }) {
  'use memo';
  return (
    <ul>
      {todos.map(todo => (
        <li key={todo.id}>{todo.text}</li>
      ))}
    </ul>
  );
}
```

`annotation` 모드에서는 `'use memo'`가 없는 함수는 컴파일되지 않으므로, 최적화를 적용할 컴포넌트만 골라 점진적으로 도입할 수 있습니다.

## 주의 사항

- `'infer'` 모드에서는 이름이 소문자로 시작하는 컴포넌트가 컴파일 대상에서 제외됩니다.
- `'annotation'` 모드는 파일 단위가 아니라 함수 단위로 적용하므로 기존 코드베이스에 점진적으로 도입하기 좋습니다.
- `'all'` 모드는 일반 유틸리티 함수까지 컴파일해 예상치 못한 동작 변화를 일으킬 수 있습니다.
- 옵션을 변경하면 빌드 결과가 달라지므로 변경 후 테스트를 함께 실행하세요.

> 참고: 위 내용은 제가 알고 있는 지식을 바탕으로 정리한 것이므로, 최신 공식 문서와 세부 내용이 다를 수 있습니다. 정확한 옵션 값과 지원 범위는 react.dev의 React Compiler 문서에서 확인하시는 것을 권장합니다.
