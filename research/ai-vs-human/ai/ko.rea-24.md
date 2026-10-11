# Effect의 의존성 제거하기

Effect를 작성하면 린터는 Effect가 읽는 반응형 값(props, state 등)이 의존성 목록에 모두 들어 있는지 확인합니다. 이 검사 덕분에 Effect가 컴포넌트의 최신 props, state와 맞춰 동작합니다. 하지만 불필요한 의존성이 있으면 Effect가 너무 자주 실행되거나 무한 루프가 생길 수 있습니다. 이 페이지에서는 불필요한 의존성을 찾아 제거하는 방법을 설명합니다.

> **이 페이지에서 배울 내용**
> - Effect 의존성 무한 루프를 고치는 방법
> - 의존성을 제거하고 싶을 때 해야 할 일
> - Effect가 값에 "반응"하지 않고 값을 읽기만 하게 하는 방법
> - 객체와 함수를 의존성으로 쓰지 말아야 하는 이유
> - 의존성 린터를 억제하면 위험한 이유

## 의존성은 코드와 일치해야 합니다

Effect를 작성할 때는 먼저 Effect가 무엇을 시작하고 어떻게 정리할지를 정합니다.

```js
const serverUrl = 'https://localhost:1234';

function ChatRoom({ roomId }) {
  useEffect(() => {
    const connection = createConnection(serverUrl, roomId);
    connection.connect();
    return () => connection.disconnect();
  }, [roomId]); // ✅ 모든 의존성이 선언됨
  // ...
}
```

`roomId`는 컴포넌트 본문에서 선언된 prop이므로 **반응형 값**입니다. 리렌더링 때 값이 바뀔 수 있으니 의존성으로 선언해야 합니다. 반대로 `serverUrl`은 컴포넌트 밖에서 선언된 상수라서 절대 바뀌지 않으므로 의존성이 될 필요가 없습니다.

의존성 목록은 여러분이 "고르는" 것이 아닙니다. **Effect의 코드가 의존성을 결정합니다.** 린터가 제대로 설정되어 있다면 코드에 맞는 의존성 목록을 제안해 줍니다.

## 의존성을 제거하려면 의존성이 아님을 증명하세요

`roomId`를 의존성 목록에서 빼면 린터는 오류를 냅니다. 이 오류가 맞습니다. `roomId`가 바뀌면 Effect는 새 채팅방에 다시 연결해야 하기 때문입니다.

의존성을 제거하려면 그 값이 반응형 값이 아니라는 것을 린터에 **증명**해야 합니다. 예를 들어 `roomId`를 컴포넌트 밖으로 옮기면 더 이상 바뀔 수 없으므로 의존성 목록에서 빼도 됩니다.

```js
const roomId = 'music'; // 반응형 값이 아님

function ChatRoom() {
  useEffect(() => {
    const connection = createConnection(serverUrl, roomId);
    connection.connect();
    return () => connection.disconnect();
  }, []); // ✅ 모든 의존성이 선언됨
}
```

정리하면 이렇습니다. **의존성을 바꾸고 싶다면 먼저 코드를 바꾸세요.**

> ⚠️ **주의**
> `// eslint-disable-next-line react-hooks/exhaustive-deps`로 린터를 억제하지 마세요. 린터를 억제하면 React는 Effect가 의존하는 값을 알 수 없습니다. 그러면 Effect가 오래된 값을 읽는 버그가 생기는데, 이런 버그는 찾기도 고치기도 어렵습니다.

## 불필요한 의존성 제거하기

의존성 목록을 볼 때마다 이렇게 질문해 보세요. "이 값이 바뀔 때마다 Effect를 다시 실행하는 게 맞을까?" 답이 "아니오"라면 아래 방법 중 하나를 적용해 보세요.

### 이 코드를 이벤트 핸들러로 옮겨야 하나요?

특정 상호작용에 대한 응답으로 실행되어야 하는 코드라면 Effect가 아니라 이벤트 핸들러에 넣으세요. 예를 들어 폼을 제출할 때 알림을 띄우는 코드를 `submitted` state와 Effect로 처리하면 `theme` 같은 값이 의존성에 끼어들게 됩니다. 이 로직을 `handleSubmit` 안으로 옮기면 Effect와 그 의존성이 모두 사라집니다.

### Effect가 관련 없는 여러 일을 하고 있나요?

하나의 Effect가 서로 관련 없는 두 가지 작업(예: 도시 목록을 가져오는 일과 지역 목록을 가져오는 일)을 동기화하고 있다면 Effect를 둘로 나누세요. 각 Effect는 **하나의 독립적인 동기화 과정**만 맡아야 합니다. 이렇게 나누면 한 의존성이 바뀌어도 관련 없는 Effect가 다시 실행되지 않습니다.

### 다음 state를 계산하려고 state를 읽고 있나요?

```js
useEffect(() => {
  connection.on('message', (msg) => {
    setMessages([...messages, msg]);
  });
  // ...
}, [roomId, messages]); // 🔴 메시지가 올 때마다 다시 연결됨
```

`messages`를 읽기 때문에 `messages`가 의존성이 되고, 새 메시지가 올 때마다 채팅방에 다시 연결됩니다. **업데이터 함수**를 쓰면 이 문제가 사라집니다.

```js
setMessages(msgs => [...msgs, msg]); // ✅ messages를 읽지 않음
```

### 값에 "반응"하지 않고 읽기만 하고 싶나요?

새 메시지가 오면 소리를 재생하되, `isMuted` 값이 바뀌었다는 이유로 다시 연결되지는 않게 하고 싶다고 해 봅시다. 이럴 때는 비반응형 로직을 **Effect 이벤트**로 분리하세요.

```js
import { useEffect, useEffectEvent } from 'react';

function ChatRoom({ roomId }) {
  const [isMuted, setIsMuted] = useState(false);

  const onMessage = useEffectEvent(receivedMessage => {
    if (!isMuted) playSound();
  });

  useEffect(() => {
    const connection = createConnection(serverUrl, roomId);
    connection.on('message', onMessage);
    connection.connect();
    return () => connection.disconnect();
  }, [roomId]); // ✅ 모든 의존성이 선언됨
}
```

Effect 이벤트 안에서는 항상 최신 props와 state를 읽을 수 있습니다. 그리고 Effect 이벤트 자체는 의존성 목록에 넣지 않습니다. props로 받은 이벤트 핸들러(`onReceiveMessage` 등)를 감쌀 때도 같은 방법을 쓸 수 있습니다.

### 반응형 값이 의도치 않게 바뀌고 있나요?

컴포넌트 본문에서 만든 객체나 함수는 **렌더링할 때마다 새로 만들어집니다.** 내용이 같아도 매번 다른 값이므로, 이런 값을 의존성으로 쓰면 Effect가 렌더링마다 다시 실행됩니다.

```js
function ChatRoom({ roomId }) {
  const options = { serverUrl, roomId }; // 🔴 매번 새 객체

  useEffect(() => {
    const connection = createConnection(options);
    connection.connect();
    return () => connection.disconnect();
  }, [options]);
}
```

해결 방법은 다음과 같습니다.

1. **정적인 객체와 함수는 컴포넌트 밖으로 옮기세요.** props나 state에 의존하지 않는다면 컴포넌트 밖에 선언해도 됩니다.
2. **동적인 객체와 함수는 Effect 안으로 옮기세요.** 객체를 Effect 안에서 만들면 의존성은 원시 값인 `roomId`만 남습니다.

   ```js
   useEffect(() => {
     const options = { serverUrl, roomId };
     const connection = createConnection(options);
     connection.connect();
     return () => connection.disconnect();
   }, [roomId]); // ✅
   ```

3. **객체에서 원시 값을 읽으세요.** props로 객체를 받는다면 Effect 밖에서 구조 분해한 다음 원시 값만 의존성으로 쓰세요.

   ```js
   const { roomId, serverUrl } = options;
   useEffect(() => { /* ... */ }, [roomId, serverUrl]);
   ```

4. **함수에서 원시 값을 계산하세요.** 부모가 함수를 넘긴다면 Effect 밖에서 함수를 호출해 결과값만 의존성으로 쓰면 됩니다. 단, 이 방법은 **순수 함수**에만 써야 합니다.

## 요약

- 의존성은 항상 코드와 일치해야 합니다.
- 의존성이 마음에 들지 않으면 의존성 목록이 아니라 코드를 고치세요.
- 린터를 억제하면 찾기 어려운 버그가 생깁니다.
- 특정 상호작용에 대한 응답으로 실행할 코드는 이벤트 핸들러로 옮기세요.
- Effect의 각 부분이 서로 다른 이유로 다시 실행되어야 한다면 Effect를 여러 개로 나누세요.
- 이전 state를 바탕으로 state를 업데이트할 때는 업데이터 함수를 쓰세요.
- 값에 반응하지 않고 최신 값을 읽기만 하려면 Effect 이벤트를 쓰세요.
- 객체와 함수는 렌더링마다 새로 만들어지므로 의존성으로 쓰지 마세요. 컴포넌트 밖이나 Effect 안으로 옮기거나 원시 값을 꺼내 쓰세요.
