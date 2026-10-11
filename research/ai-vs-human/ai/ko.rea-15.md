# Ref로 값 참조하기

컴포넌트가 어떤 정보를 "기억"하게 하고 싶지만 그 정보 때문에 [새로운 렌더링](/learn/render-and-commit)이 일어나지 않기를 바란다면 **ref**를 사용할 수 있습니다.

<YouWillLearn>

- 컴포넌트에 ref를 추가하는 방법
- ref의 값을 업데이트하는 방법
- ref와 state의 차이점
- ref를 안전하게 사용하는 방법

</YouWillLearn>

## 컴포넌트에 ref 추가하기 {/*adding-a-ref-to-your-component*/}

React에서 `useRef` Hook을 가져와 컴포넌트에 ref를 추가할 수 있습니다.

```js
import { useRef } from 'react';
```

컴포넌트 안에서 `useRef` Hook을 호출하고, 참조하려는 초기값을 유일한 인수로 넘깁니다. 예를 들어 다음은 값 `0`을 담은 ref입니다.

```js
const ref = useRef(0);
```

`useRef`는 다음과 같은 객체를 반환합니다.

```js
{
  current: 0 // useRef에 전달한 값
}
```

`ref.current` 프로퍼티로 해당 ref의 현재 값에 접근할 수 있습니다. 이 값은 의도적으로 변경할 수 있게 만들어졌으므로 읽기와 쓰기가 모두 가능합니다. React가 추적하지 않는 컴포넌트의 비밀 주머니라고 생각하면 됩니다. (이 점 때문에 ref는 React의 단방향 데이터 흐름에서 벗어나는 "탈출구"가 됩니다.)

다음 예시에서는 버튼을 클릭할 때마다 `ref.current`가 증가합니다.

```js
import { useRef } from 'react';

export default function Counter() {
  let ref = useRef(0);

  function handleClick() {
    ref.current = ref.current + 1;
    alert('You clicked ' + ref.current + ' times!');
  }

  return (
    <button onClick={handleClick}>
      Click me!
    </button>
  );
}
```

ref는 숫자를 가리키고 있지만, [state](/learn/state-a-components-memory)처럼 문자열, 객체, 함수 등 무엇이든 가리킬 수 있습니다. state와 달리 ref는 `current` 프로퍼티를 읽고 수정할 수 있는 일반 자바스크립트 객체입니다.

**컴포넌트는 증가할 때마다 다시 렌더링되지 않는다는** 점에 주목하세요. ref도 state처럼 React가 리렌더링 사이에 값을 유지합니다. 하지만 state를 변경하면 컴포넌트가 다시 렌더링되고, ref를 변경하면 다시 렌더링되지 않습니다.

## 예시: 스톱워치 만들기 {/*example-building-a-stopwatch*/}

ref와 state를 하나의 컴포넌트에서 함께 사용할 수 있습니다. 사용자가 버튼을 눌러 시작하거나 멈출 수 있는 스톱워치를 만들어 보겠습니다.

"Start"를 누른 뒤 얼마나 시간이 지났는지 표시하려면 시작 버튼을 누른 시점과 현재 시각을 추적해야 합니다. **이 정보는 렌더링에 사용되므로 state로 관리합니다.**

```js
const [startTime, setStartTime] = useState(null);
const [now, setNow] = useState(null);
```

사용자가 "Start"를 누르면 [`setInterval`](https://developer.mozilla.org/docs/Web/API/setInterval)을 사용해 10밀리초마다 시간을 업데이트합니다. "Stop" 버튼을 누르면 `now` state 변수의 업데이트를 멈추도록 기존 interval을 취소해야 합니다. 이를 위해 [`clearInterval`](https://developer.mozilla.org/docs/Web/API/clearInterval)을 호출하는데, 사용자가 Start를 눌렀을 때 `setInterval`이 반환한 interval ID를 넘겨줘야 합니다. interval ID는 어딘가에 보관해야 합니다. **interval ID는 렌더링에 사용되지 않으므로 ref에 보관할 수 있습니다.**

```js
import { useState, useRef } from 'react';

export default function Stopwatch() {
  const [startTime, setStartTime] = useState(null);
  const [now, setNow] = useState(null);
  const intervalRef = useRef(null);

  function handleStart() {
    setStartTime(Date.now());
    setNow(Date.now());

    clearInterval(intervalRef.current);
    intervalRef.current = setInterval(() => {
      setNow(Date.now());
    }, 10);
  }

  function handleStop() {
    clearInterval(intervalRef.current);
  }

  let secondsPassed = 0;
  if (startTime != null && now != null) {
    secondsPassed = (now - startTime) / 1000;
  }

  return (
    <>
      <h1>Time passed: {secondsPassed.toFixed(3)}</h1>
      <button onClick={handleStart}>
        Start
      </button>
      <button onClick={handleStop}>
        Stop
      </button>
    </>
  );
}
```

렌더링에 쓰이는 정보는 state에 두세요. 이벤트 핸들러에서만 필요하고 변경되어도 리렌더링할 필요가 없는 정보라면 ref를 사용하는 편이 더 효율적일 수 있습니다.

## ref와 state의 차이 {/*differences-between-refs-and-state*/}

ref가 state보다 덜 엄격해 보여서, 예를 들어 state 설정 함수를 쓰지 않고도 값을 바꿀 수 있으니 항상 ref를 쓰고 싶을 수도 있습니다. 하지만 대부분은 state를 사용하게 됩니다. ref는 자주 필요하지 않은 "탈출구"입니다. state와 ref를 비교하면 다음과 같습니다.

| ref | state |
| --- | --- |
| `useRef(initialValue)`는 `{ current: initialValue }`를 반환합니다. | `useState(initialValue)`는 state 변수의 현재 값과 state 설정 함수(`[value, setValue]`)를 반환합니다. |
| 변경해도 리렌더링되지 않습니다. | 변경하면 리렌더링됩니다. |
| 변경 가능: 렌더링 과정 밖에서 `current` 값을 수정하고 업데이트할 수 있습니다. | "불변성": state를 수정하려면 state 설정 함수를 사용해 리렌더링을 대기열에 넣어야 합니다. |
| 렌더링 중에는 `current` 값을 읽거나 쓰면 안 됩니다. | 언제든지 state를 읽을 수 있습니다. 다만 각 렌더링에는 변하지 않는 자체 state [스냅샷](/learn/state-as-a-snapshot)이 있습니다. |

다음은 ref로 구현하면 동작하지 않는 카운터 버튼입니다.

```js
import { useRef } from 'react';

export default function Counter() {
  let countRef = useRef(0);

  function handleClick() {
    // 이 코드는 컴포넌트를 리렌더링하지 않습니다!
    countRef.current = countRef.current + 1;
  }

  return (
    <button onClick={handleClick}>
      You clicked {countRef.current} times
    </button>
  );
}
```

화면에 count 값을 표시하므로 이 경우에는 state가 맞습니다. `setCount()`로 값을 설정하면 React가 컴포넌트를 다시 렌더링해 새 count를 반영합니다. 반대로 ref는 `ref.current`가 바뀌어도 리렌더링을 일으키지 않아서 화면이 그대로 남아 있습니다.

<DeepDive>

#### useRef는 내부에서 어떻게 동작하나요? {/*how-does-use-ref-work-inside*/}

`useState`와 `useRef` 모두 React가 제공하지만, 원칙적으로는 `useRef`를 `useState` 위에 구현할 수도 있습니다. React 내부에서 `useRef`가 다음과 같이 구현되어 있다고 상상해 볼 수 있습니다.

```js
// React 내부
function useRef(initialValue) {
  const [ref, unused] = useState({ current: initialValue });
  return ref;
}
```

첫 번째 렌더링에서 `useRef`는 `{ current: initialValue }`를 반환합니다. React는 이 객체를 저장해 두므로 다음 렌더링에서도 같은 객체가 반환됩니다. 이 예시에서 state 설정 함수가 쓰이지 않는다는 점에 주목하세요. `useRef`는 항상 같은 객체를 반환해야 하므로 설정 함수가 필요 없습니다.

</DeepDive>

## ref를 사용해야 하는 경우 {/*when-to-use-refs*/}

일반적으로 컴포넌트가 React 바깥으로 나가 외부 API, 주로 컴포넌트의 모습에 영향을 주지 않는 브라우저 API와 통신해야 할 때 ref를 사용합니다. 다음은 이런 경우의 예입니다.

- [timeout ID](https://developer.mozilla.org/docs/Web/API/setTimeout) 저장
- [DOM 엘리먼트](https://developer.mozilla.org/docs/Web/API/Element) 저장과 조작 ([다음 페이지](/learn/manipulating-the-dom-with-refs)에서 다룹니다.)
- JSX를 계산하는 데 필요하지 않은 다른 객체 저장

컴포넌트가 어떤 값을 저장해야 하지만 그 값이 렌더링 로직에 영향을 주지 않는다면 ref를 선택하세요.

## ref 사용 모범 사례 {/*best-practices-for-refs*/}

다음 원칙을 따르면 컴포넌트를 더 예측 가능하게 만들 수 있습니다.

- **ref를 탈출구로 취급하세요.** ref는 외부 시스템이나 브라우저 API와 작업할 때 유용합니다. 애플리케이션 로직과 데이터 흐름의 상당 부분이 ref에 의존한다면 접근 방식을 다시 검토해 보는 것이 좋습니다.
- **렌더링 중에는 `ref.current`를 읽거나 쓰지 마세요.** 렌더링에 어떤 정보가 필요하다면 state를 사용하세요. React는 `ref.current`가 언제 바뀌는지 알 수 없으므로, 렌더링 중에 읽기만 해도 컴포넌트의 동작을 예측하기 어려워집니다. (단, `if (!ref.current) ref.current = new Thing()`처럼 첫 렌더링 때 한 번만 ref를 설정하는 코드는 예외입니다.)

React state의 제약은 ref에 적용되지 않습니다. 예를 들어 state는 [모든 렌더링에서 스냅샷처럼](/learn/state-as-a-snapshot) 동작하며 [동기적으로 업데이트되지 않습니다.](/learn/queueing-a-series-of-state-updates) 하지만 ref의 현재 값을 변경하면 즉시 바뀝니다.

```js
ref.current = 5;
console.log(ref.current); // 5
```

**ref 자체가 일반 자바스크립트 객체이기 때문에** 이렇게 동작합니다.

ref를 변경할 때 [변경 금지 규칙](/learn/updating-objects-in-state)을 신경 쓸 필요도 없습니다. 변경하는 객체가 렌더링에 쓰이지 않는다면 React는 ref로 무엇을 하든 상관하지 않습니다.

## ref와 DOM {/*refs-and-the-dom*/}

ref는 어떤 값이든 가리킬 수 있습니다. 하지만 가장 흔한 용도는 DOM 엘리먼트에 접근하는 것입니다. 예를 들어 프로그래밍 방식으로 input에 포커스를 줄 때 유용합니다. JSX에서 `<div ref={myRef}>`처럼 `ref` 어트리뷰트에 ref를 전달하면 React는 해당 DOM 엘리먼트를 `myRef.current`에 넣어 줍니다. 엘리먼트가 DOM에서 제거되면 React는 `myRef.current`를 `null`로 업데이트합니다. 자세한 내용은 [Ref로 DOM 조작하기](/learn/manipulating-the-dom-with-refs)에서 확인할 수 있습니다.

<Recap>

- ref는 렌더링에 쓰이지 않는 값을 보관하는 탈출구이며, 자주 필요하지는 않습니다.
- ref는 `current`라는 프로퍼티 하나를 가진 일반 자바스크립트 객체로, 값을 읽거나 설정할 수 있습니다.
- `useRef` Hook을 호출하면 React가 ref를 제공합니다.
- state처럼 ref도 컴포넌트가 리렌더링되는 사이에 정보를 유지합니다.
- state와 달리 ref의 `current` 값을 설정해도 리렌더링되지 않습니다.
- 렌더링 중에는 `ref.current`를 읽거나 쓰지 마세요. 컴포넌트를 예측하기 어려워집니다.

</Recap>
