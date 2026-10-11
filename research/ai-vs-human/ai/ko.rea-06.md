# 탈출구

<Intro>

어떤 컴포넌트는 React 바깥의 시스템을 제어하거나 그 시스템과 동기화해야 할 때가 있습니다. 브라우저 API로 input에 포커스를 주거나, React 없이 만들어진 비디오 플레이어를 재생하거나 멈추거나, 원격 서버에 연결해 메시지를 받는 경우가 그렇습니다. 이 장에서는 React의 "바깥으로 나가서" 외부 시스템과 연결하는 탈출구를 배웁니다. 애플리케이션 로직과 데이터 흐름은 대부분 이런 기능에 기대지 않아야 합니다.

</Intro>

<YouWillLearn isChapter={true}>

* 리렌더링 없이 정보를 "기억"하는 방법
* React가 관리하는 DOM 엘리먼트에 접근하는 방법
* 컴포넌트를 외부 시스템과 동기화하는 방법
* 컴포넌트에서 불필요한 Effect를 없애는 방법
* Effect의 생명주기가 컴포넌트의 생명주기와 다른 점
* 일부 값이 Effect를 다시 실행하지 않도록 하는 방법
* Effect가 덜 자주 다시 실행되게 하는 방법
* 컴포넌트 간에 로직을 공유하는 방법

</YouWillLearn>

## Ref로 값 참조하기 {/*referencing-values-with-refs*/}

컴포넌트가 정보를 "기억"해야 하지만 그 정보가 [새 렌더링을 일으키지 않아야](/learn/render-and-commit) 한다면 *ref*를 쓸 수 있습니다.

```js
const ref = useRef(0);
```

ref는 state처럼 React가 리렌더링 사이에도 값을 보존합니다. 다만 state를 바꾸면 컴포넌트가 다시 렌더링되고, ref를 바꾸면 다시 렌더링되지 않습니다. ref의 현재 값은 `ref.current` 프로퍼티로 읽고 쓸 수 있습니다.

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

ref는 React가 추적하지 않는 컴포넌트의 비밀 주머니라고 생각하면 됩니다. [타임아웃 ID](https://developer.mozilla.org/ko/docs/Web/API/setTimeout#return_value), [DOM 엘리먼트](https://developer.mozilla.org/ko/docs/Web/API/Element)처럼 렌더링 결과에 영향을 주지 않는 객체를 저장할 때 ref를 씁니다.

<LearnMore path="/learn/referencing-values-with-refs">

**[Ref로 값 참조하기](/learn/referencing-values-with-refs)** 에서 ref로 정보를 기억하는 방법을 알아보세요.

</LearnMore>

## Ref로 DOM 조작하기 {/*manipulating-the-dom-with-refs*/}

React는 렌더링 결과에 맞춰 DOM을 자동으로 갱신하므로 직접 DOM을 조작할 일은 많지 않습니다. 그래도 노드에 포커스를 주거나, 노드로 스크롤하거나, 크기와 위치를 재야 할 때는 React가 관리하는 DOM 엘리먼트에 접근해야 합니다. React에는 이런 작업을 하는 내장 기능이 없으므로 DOM 노드를 가리키는 ref가 필요합니다. 다음 예시에서는 버튼을 클릭하면 ref를 사용해 input에 포커스를 줍니다.

```js
import { useRef } from 'react';

export default function Form() {
  const inputRef = useRef(null);

  function handleClick() {
    inputRef.current.focus();
  }

  return (
    <>
      <input ref={inputRef} />
      <button onClick={handleClick}>
        Focus the input
      </button>
    </>
  );
}
```

<LearnMore path="/learn/manipulating-the-dom-with-refs">

**[Ref로 DOM 조작하기](/learn/manipulating-the-dom-with-refs)** 에서 React가 관리하는 DOM 엘리먼트에 접근하는 방법을 알아보세요.

</LearnMore>

## Effect로 동기화하기 {/*synchronizing-with-effects*/}

어떤 컴포넌트는 외부 시스템과 동기화해야 합니다. 예를 들어 React state에 따라 React가 아닌 컴포넌트를 제어하거나, 서버에 연결하거나, 컴포넌트가 화면에 나타났을 때 분석 로그를 보내야 할 수 있습니다. 특정 이벤트를 처리하는 이벤트 핸들러와 달리, *Effect*는 렌더링이 끝난 뒤에 코드를 실행합니다. Effect를 사용하면 컴포넌트를 React 바깥의 시스템과 동기화할 수 있습니다.

```js
import { useState, useRef, useEffect } from 'react';

function VideoPlayer({ src, isPlaying }) {
  const ref = useRef(null);

  useEffect(() => {
    if (isPlaying) {
      ref.current.play();
    } else {
      ref.current.pause();
    }
  }, [isPlaying]);

  return <video ref={ref} src={src} loop playsInline />;
}
```

많은 Effect는 스스로 "정리"도 합니다. 예를 들어 채팅 서버에 연결하는 Effect는 *클린업 함수*를 반환해 컴포넌트와 서버의 연결을 끊는 방법을 React에 알려야 합니다.

```js
useEffect(() => {
  const connection = createConnection();
  connection.connect();
  return () => connection.disconnect();
}, []);
```

개발 환경에서 React는 Effect를 한 번 실행하고 정리한 뒤 곧바로 다시 실행합니다. 그래서 `"✅ Connecting..."`이 두 번 출력됩니다. 클린업 함수를 빠뜨린 실수를 찾기 쉽게 하려는 동작입니다.

<LearnMore path="/learn/synchronizing-with-effects">

**[Effect로 동기화하기](/learn/synchronizing-with-effects)** 에서 컴포넌트를 외부 시스템과 동기화하는 방법을 알아보세요.

</LearnMore>

## Effect가 필요하지 않을 수도 있습니다 {/*you-might-not-need-an-effect*/}

Effect는 React 패러다임에서 벗어나는 탈출구입니다. Effect를 쓰면 React의 "바깥으로 나가서" 컴포넌트를 외부 시스템과 동기화할 수 있습니다. 외부 시스템이 관여하지 않는다면, 예를 들어 props나 state가 바뀔 때 컴포넌트의 state를 갱신하려는 것뿐이라면 Effect는 필요하지 않습니다. 불필요한 Effect를 없애면 코드를 따라가기 쉬워지고, 실행 속도가 빨라지고, 오류가 생길 여지도 줄어듭니다.

Effect가 필요하지 않은 대표적인 경우는 두 가지입니다.

* **렌더링을 위해 데이터를 변환할 때는 Effect가 필요하지 않습니다.**
* **사용자 이벤트를 처리할 때는 Effect가 필요하지 않습니다.**

다음 컴포넌트는 `firstName`과 `lastName` state 변수를 합쳐 `fullName`을 계산합니다. 이 계산에는 Effect가 필요하지 않습니다. **렌더링 중에 계산하면 됩니다.**

```js
function Form() {
  const [firstName, setFirstName] = useState('Taylor');
  const [lastName, setLastName] = useState('Swift');
  // ✅ 좋습니다: 렌더링 중에 계산됩니다
  const fullName = firstName + ' ' + lastName;
  // ...
}
```

같은 값을 Effect로 계산해 별도의 state에 저장하면, 오래된 값으로 한 번 렌더링한 다음 갱신된 값으로 다시 렌더링하게 되어 비효율적입니다.

<LearnMore path="/learn/you-might-not-need-an-effect">

**[Effect가 필요하지 않을 수도 있습니다](/learn/you-might-not-need-an-effect)** 에서 불필요한 Effect를 없애는 방법을 알아보세요.

</LearnMore>

## React Effect의 생명주기 {/*lifecycle-of-reactive-effects*/}

Effect의 생명주기는 컴포넌트와 다릅니다. 컴포넌트는 마운트되고, 업데이트되고, 언마운트됩니다. 반면 Effect가 하는 일은 두 가지뿐입니다. 동기화를 시작하는 것과, 나중에 동기화를 멈추는 것입니다. Effect가 시간에 따라 바뀌는 props나 state에 의존한다면 이 주기가 여러 번 반복될 수 있습니다.

다음 Effect는 `roomId` prop 값에 의존합니다. props는 *반응형 값*이므로 리렌더링될 때 바뀔 수 있습니다. `roomId`가 바뀌면 Effect가 *재동기화*되어 다른 서버에 다시 연결합니다.

```js
function ChatRoom({ roomId }) {
  useEffect(() => {
    const connection = createConnection(serverUrl, roomId);
    connection.connect();
    return () => connection.disconnect();
  }, [roomId]);

  return <h1>Welcome to the {roomId} room!</h1>;
}
```

React에는 Effect의 의존성을 올바르게 지정했는지 확인하는 린터 규칙이 있습니다. 위 예시에서 의존성 배열에 `roomId`를 빠뜨리면 린터가 이 버그를 자동으로 찾아줍니다.

<LearnMore path="/learn/lifecycle-of-reactive-effects">

**[React Effect의 생명주기](/learn/lifecycle-of-reactive-effects)** 에서 Effect의 생명주기가 컴포넌트와 어떻게 다른지 알아보세요.

</LearnMore>

## Effect에서 이벤트 분리하기 {/*separating-events-from-effects*/}

이벤트 핸들러는 같은 상호작용을 다시 할 때만 다시 실행됩니다. Effect는 이벤트 핸들러와 달리, 읽고 있는 props나 state 같은 값이 지난 렌더링 때와 다르면 다시 동기화됩니다. 때로는 두 동작을 섞어서, 일부 값에는 반응하고 다른 값에는 반응하지 않는 Effect가 필요할 수도 있습니다.

이럴 때는 반응하지 않아야 할 로직을 *Effect 이벤트*로 옮기면 됩니다.

```js
function ChatRoom({ roomId, theme }) {
  const onConnected = useEffectEvent(() => {
    showNotification('Connected!', theme);
  });

  useEffect(() => {
    const connection = createConnection(serverUrl, roomId);
    connection.on('connected', () => {
      onConnected();
    });
    connection.connect();
    return () => connection.disconnect();
  }, [roomId]); // ✅ 모든 의존성이 선언되었습니다
  // ...
}
```

Effect 이벤트 안의 코드는 반응형이 아니므로, `theme`을 바꿔도 Effect가 다시 연결되지 않습니다.

<LearnMore path="/learn/separating-events-from-effects">

**[Effect에서 이벤트 분리하기](/learn/separating-events-from-effects)** 에서 일부 값이 Effect를 다시 실행하지 않도록 하는 방법을 알아보세요.

</LearnMore>

## Effect의 의존성 제거하기 {/*removing-effect-dependencies*/}

Effect를 작성하면 린터는 Effect가 읽는 모든 반응형 값을 의존성 목록에 넣었는지 확인합니다. 그래서 불필요한 의존성 때문에 Effect가 너무 자주 실행되거나 무한 루프에 빠질 수 있습니다. 이때 린터 경고를 끄는 것은 해결책이 아닙니다. **필요하지 않은 의존성은 코드를 고쳐서 *그 값이 의존성일 필요가 없다는 것을 증명*해야 합니다.**

예를 들어 렌더링 중에 만든 객체를 의존성으로 쓰면 렌더링할 때마다 새 객체가 만들어지므로 Effect가 매번 다시 동기화됩니다. 객체를 Effect *안에서* 만들면 이 문제가 사라집니다.

```js
function ChatRoom({ roomId }) {
  useEffect(() => {
    const options = {
      serverUrl: serverUrl,
      roomId: roomId
    };
    const connection = createConnection(options);
    connection.connect();
    return () => connection.disconnect();
  }, [roomId]); // ✅ 모든 의존성이 선언되었습니다
  // ...
}
```

의존성 목록은 고르는 것이 아니라 코드가 정합니다. 의존성을 바꾸고 싶다면 먼저 코드를 바꾸세요.

<LearnMore path="/learn/removing-effect-dependencies">

**[Effect의 의존성 제거하기](/learn/removing-effect-dependencies)** 에서 Effect가 덜 자주 다시 실행되게 하는 방법을 알아보세요.

</LearnMore>

## 커스텀 Hook으로 로직 재사용하기 {/*reusing-logic-with-custom-hooks*/}

React에는 `useState`, `useContext`, `useEffect` 같은 내장 Hook이 있습니다. 그런데 데이터를 가져오거나, 사용자가 온라인인지 확인하거나, 채팅방에 연결하는 것처럼 더 구체적인 목적의 Hook이 필요할 때가 있습니다. 이럴 때는 애플리케이션에 맞는 Hook을 직접 만들 수 있습니다.

다음 예시에서는 `usePointerPosition` 커스텀 Hook이 커서 위치를 추적하고, `useDelayedValue` 커스텀 Hook이 전달받은 값보다 일정 시간 "뒤처진" 값을 반환합니다.

```js
export default function Canvas() {
  const pos1 = usePointerPosition();
  const pos2 = useDelayedValue(pos1, 100);
  const pos3 = useDelayedValue(pos2, 200);
  // ...
}
```

커스텀 Hook으로는 상태 *자체*가 아니라 상태를 다루는 *로직*을 공유합니다. 같은 Hook을 호출하더라도 각 호출의 state는 완전히 독립적입니다. 앱의 Effect가 대부분 커스텀 Hook 안에 들어가 있다면, 코드는 더 선언적이고 React 철학에 더 가까워집니다.

<LearnMore path="/learn/reusing-logic-with-custom-hooks">

**[커스텀 Hook으로 로직 재사용하기](/learn/reusing-logic-with-custom-hooks)** 에서 컴포넌트 간에 로직을 공유하는 방법을 알아보세요.

</LearnMore>

## 다음 단계 {/*whats-next*/}

이 장을 한 페이지씩 읽으려면 [Ref로 값 참조하기](/learn/referencing-values-with-refs)로 이동하세요.
