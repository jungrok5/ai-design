# Effect에서 이벤트 분리하기

이벤트 핸들러는 같은 상호작용을 다시 수행할 때만 다시 실행됩니다. Effect는 이벤트 핸들러와 달리, 읽은 props나 state 같은 값이 지난 렌더링 때와 다르면 다시 동기화합니다. 때로는 두 동작의 특성을 섞고 싶을 수 있습니다. 어떤 값에는 반응해서 다시 실행되지만, 다른 값에는 반응하지 않는 Effect가 필요한 경우입니다. 이 페이지에서는 그 방법을 알아봅니다.

<YouWillLearn>

- 이벤트 핸들러와 Effect 중 무엇을 선택해야 하는지
- Effect가 반응형인 이유와 이벤트 핸들러가 그렇지 않은 이유
- Effect 코드의 일부가 반응하지 않기를 원할 때 해야 할 일
- Effect Event가 무엇이고 Effect에서 어떻게 분리하는지
- Effect Event로 Effect에서 최신 props와 state를 읽는 방법

</YouWillLearn>

## 이벤트 핸들러와 Effect 중에서 선택하기

먼저 이벤트 핸들러와 Effect의 차이를 다시 짚어 보겠습니다.

채팅방 컴포넌트를 구현한다고 가정해 봅시다. 요구 사항은 다음과 같습니다.

1. 컴포넌트는 선택된 채팅방에 자동으로 연결해야 합니다.
2. "전송" 버튼을 클릭하면 채팅에 메시지를 보내야 합니다.

코드는 이미 작성했지만, 어디에 넣어야 할지 확신이 없다고 해 봅시다. 이벤트 핸들러에 넣을까요, Effect에 넣을까요? 이 질문에 답해야 할 때마다 [_왜_ 그 코드가 실행되어야 하는지](/learn/lifecycle-of-reactive-effects#effects-aren-t-reactive-values-and-event-handlers)를 생각해 보세요.

### 이벤트 핸들러는 특정 상호작용에 대한 응답으로 실행됩니다

사용자 입장에서 메시지 전송은 특정 "전송" 버튼을 클릭했기 *때문에* 일어나야 합니다. 다른 시점이나 다른 이유로 메시지가 전송되면 사용자는 몹시 당황할 것입니다. 그래서 메시지 전송은 이벤트 핸들러에 있어야 합니다. 이벤트 핸들러는 특정 상호작용을 처리할 수 있게 해 줍니다.

```js {4-6}
function ChatRoom({ roomId }) {
  const [message, setMessage] = useState('');
  // ...
  function handleSendClick() {
    sendMessage(message);
  }
  // ...
  return (
    <>
      <input value={message} onChange={e => setMessage(e.target.value)} />
      <button onClick={handleSendClick}>전송</button>
    </>
  );
}
```

이벤트 핸들러를 사용하면 `sendMessage(message)`가 사용자가 버튼을 클릭할 때*만* 실행됩니다.

### Effect는 동기화가 필요할 때마다 실행됩니다

컴포넌트가 채팅방에 연결된 상태를 유지해야 한다는 점도 기억하세요. 그 코드는 어디에 넣어야 할까요?

이 코드를 실행하는 이유는 특정 상호작용이 아닙니다. 사용자가 채팅방 화면으로 어떻게 이동했는지는 중요하지 않습니다. 이제 사용자가 그 화면을 보고 있고 상호작용할 수 있으므로, 컴포넌트는 선택된 채팅 서버에 계속 연결되어 있어야 합니다. 채팅방 컴포넌트가 앱의 초기 화면이든, 다른 화면이든, 사용자가 입력 한 번 하지 않았더라도 마찬가지입니다. 그래서 이 코드는 Effect에 들어갑니다.

```js {3-9}
function ChatRoom({ roomId }) {
  // ...
  useEffect(() => {
    const connection = createConnection(serverUrl, roomId);
    connection.connect();
    return () => {
      connection.disconnect();
    };
  }, [roomId]);
  // ...
}
```

이 코드를 사용하면 사용자가 *현재 선택된* 채팅방에 항상 활성 연결을 유지할 수 있습니다. 사용자가 앱을 열었든, 다른 방을 선택했든, 다른 화면에 갔다가 돌아왔든 상관없습니다. Effect는 컴포넌트가 현재 선택된 방과 동기화된 상태를 유지하도록 보장합니다.

## 반응형 값과 반응형 로직

직관적으로, 이벤트 핸들러는 버튼을 클릭하는 것과 같이 항상 "수동"으로 트리거된다고 말할 수 있습니다. 반면 Effect는 "자동"입니다. 동기화를 유지하는 데 필요할 때마다 실행되고 다시 실행됩니다.

더 정확한 방법이 있습니다. 컴포넌트 본문에서 선언된 props, state, 변수를 <CodeStep>반응형 값</CodeStep>이라고 합니다. 이 예시에서 `serverUrl`은 반응형 값이 아니지만, `roomId`와 `message`는 반응형 값입니다. 이들은 렌더링 데이터 흐름에 참여합니다.

### 이벤트 핸들러 안의 로직은 반응형이 아닙니다

`handleSendClick` 같은 이벤트 핸들러 안의 로직은 반응형 값을 읽더라도 *반응하지* 않습니다. 사용자가 클릭할 때마다 한 번 실행되는 "일회성" 코드이기 때문입니다. `message`나 `roomId`가 바뀌어도 이벤트 핸들러는 다시 실행되지 않습니다. 이벤트 핸들러는 항상 클릭 시점의 최신 값을 읽을 뿐입니다.

### Effect 안의 로직은 반응형입니다

Effect 안에서 반응형 값을 읽으면, 그 값을 의존성으로 지정해야 합니다. 그러면 값이 바뀔 때마다 React가 Effect를 다시 실행합니다. 위 예시처럼 `roomId`가 바뀌면 이전 방의 연결을 해제하고 새 방에 연결하는 것이 올바른 동작입니다.

## Effect 안의 비반응형 로직 추출하기

반응형 로직과 비반응형 로직이 섞이면 문제가 더 까다로워집니다. 예를 들어 사용자가 채팅방에 연결되면 알림을 보여 주되, 알림 테마(밝게/어둡게)는 현재 `theme` props에 따라 정하고 싶다고 합시다.

```js {1,4-6,11}
function ChatRoom({ roomId, theme }) {
  useEffect(() => {
    const connection = createConnection(serverUrl, roomId);
    connection.on('connected', () => {
      showNotification('연결되었습니다!', theme);
    });
    connection.connect();
    return () => {
      connection.disconnect();
    };
  }, [roomId, theme]); // ✅ 모든 의존성이 선언되었습니다.
  // ...
}
```

`theme`은 반응형 값이므로 의존성에 포함해야 합니다. 그런데 이렇게 하면 사용자가 테마를 바꿀 때마다 채팅방 연결이 끊어졌다 다시 연결됩니다. 테마 변경은 연결과 무관한데도 말입니다. 우리가 원하는 것은 `showNotification` 호출만 `theme`의 최신 값을 읽되, 그 변화에는 반응하지 않는 것입니다.

### Effect Event 선언하기

<Canary>

이 절에서 설명하는 API는 아직 React의 안정 버전에 포함되지 않은 **실험적 API**입니다.

</Canary>

[`useEffectEvent`](/reference/react/experimental_useEffectEvent)라는 특별한 Hook을 사용해 이 비반응형 로직을 Effect에서 분리할 수 있습니다.

```js {1,4-6}
import { useEffect, useEffectEvent } from 'react';

function ChatRoom({ roomId, theme }) {
  const onConnected = useEffectEvent(() => {
    showNotification('연결되었습니다!', theme);
  });
  // ...
}
```

여기서 `onConnected`를 *Effect Event*라고 합니다. Effect 로직의 일부이지만, 동작은 이벤트 핸들러에 더 가깝습니다. 내부 로직이 반응형이 아니며, 항상 props와 state의 최신 값을 "볼" 수 있습니다.

이제 Effect 안에서 `onConnected`를 호출할 수 있습니다.

```js {2-4,9,13}
function ChatRoom({ roomId, theme }) {
  const onConnected = useEffectEvent(() => {
    showNotification('연결되었습니다!', theme);
  });

  useEffect(() => {
    const connection = createConnection(serverUrl, roomId);
    connection.on('connected', () => {
      onConnected();
    });
    connection.connect();
    return () => connection.disconnect();
  }, [roomId]); // ✅ 모든 의존성이 선언되었습니다.
  // ...
}
```

이렇게 하면 `onConnected`는 Effect Event이므로 의존성 배열에 넣을 필요가 없습니다. 그 결과 `theme`이 바뀌어도 채팅방 연결은 유지되고, 알림은 항상 최신 테마로 표시됩니다.

### Effect Event로 최신 props와 state 읽기

Effect Event는 흔히 사용하는 다음과 같은 경우를 해결해 줍니다. 페이지를 방문할 때마다 로그를 남기는 Effect가 있다고 해 봅시다.

```js
function Page({ url }) {
  useEffect(() => {
    logVisit(url);
  }, [url]);
  // ...
}
```

이제 사이트에 여러 경로가 생겼고, 로그에 장바구니 상품 수 `numberOfItems`도 함께 기록하고 싶습니다. 하지만 `numberOfItems`를 의존성에 넣으면 상품 수가 바뀔 때마다 방문 로그가 다시 남게 됩니다. 이때 로그 호출을 Effect Event로 감싸면 `url`이 바뀔 때만 로그를 남기면서 최신 `numberOfItems`를 읽을 수 있습니다.

```js {2-4,7,9}
function Page({ url }) {
  const { items } = useContext(ShoppingCartContext);
  const numberOfItems = items.length;

  const onVisit = useEffectEvent(visitedUrl => {
    logVisit(visitedUrl, numberOfItems);
  });

  useEffect(() => {
    onVisit(url);
  }, [url]); // ✅ 모든 의존성이 선언되었습니다.
  // ...
}
```

## Effect Event의 한계

Effect Event는 매우 제한적인 방식으로만 사용해야 합니다.

- **Effect 내부에서만 호출하세요.**
- **다른 컴포넌트나 Hook에 전달하지 마세요.**

예를 들어 Effect Event를 다음처럼 선언하고 전달하면 안 됩니다.

```js {4-6,8}
function Timer() {
  const [count, setCount] = useState(0);

  const onTick = useEffectEvent(() => {
    setCount(count + 1);
  });

  useTimer(onTick, 1000); // 🔴 피하세요: Effect Event를 전달하고 있습니다.
}

function useTimer(callback, delay) {
  useEffect(() => {
    const id = setInterval(() => {
      callback();
    }, delay);
    return () => clearInterval(id);
  }, [delay, callback]); // 의존성에 'callback'을 지정해야 합니다.
}
```

대신 Effect Event는 사용하는 Effect 바로 옆에 선언하세요.

```js {4-6,10}
function Timer() {
  const [count, setCount] = useState(0);
  useTimer(() => {
    setCount(count + 1);
  }, 1000);
}

function useTimer(callback, delay) {
  const onTick = useEffectEvent(() => {
    callback();
  });

  useEffect(() => {
    const id = setInterval(() => {
      onTick(); // ✅ 좋습니다: Effect 내부에서만 호출합니다.
    }, delay);
    return () => clearInterval(id);
  }, [delay]); // 'onTick'을 의존성으로 지정할 필요가 없습니다.
}
```

Effect Event는 Effect 코드의 비반응형 "조각"입니다. 이를 사용하는 Effect 옆에 두세요.

<Recap>

- 이벤트 핸들러는 특정 상호작용에 대한 응답으로 실행됩니다.
- Effect는 동기화가 필요할 때마다 실행됩니다.
- 이벤트 핸들러 안의 로직은 반응형이 아니며, Effect 안의 로직은 반응형입니다.
- Effect의 비반응형 로직은 Effect Event로 옮길 수 있습니다.
- Effect Event는 Effect 안에서만 호출하세요.
- Effect Event를 다른 컴포넌트나 Hook에 전달하지 마세요.

</Recap>
