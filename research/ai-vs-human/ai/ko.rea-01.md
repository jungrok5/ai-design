# 상호작용 추가하기

화면의 일부 요소는 사용자 입력에 따라 실시간으로 바뀝니다. 이미지 갤러리에서 이미지를 클릭하면 선택한 이미지가 바뀌고, 장바구니에서 "구매" 버튼을 누르면 상품이 담깁니다. React에서는 시간에 따라 변하는 데이터를 **state**라고 부릅니다. 어떤 컴포넌트에든 state를 추가할 수 있고, 필요하면 언제든 수정할 수 있습니다. 이 장에서는 상호작용하는 컴포넌트를 작성하는 방법, state를 업데이트하는 방법, 그리고 시간에 따라 화면이 바뀌는 원리를 배웁니다.

<YouWillLearn isChapter={true}>

* [사용자가 일으킨 이벤트를 처리하는 방법](/learn/responding-to-events)
* [state를 사용해 컴포넌트가 정보를 "기억"하게 만드는 방법](/learn/state-a-components-memory)
* [React가 UI를 두 단계에 걸쳐 업데이트하는 방식](/learn/render-and-commit)
* [state를 변경한 직후에는 왜 값이 갱신되지 않는지](/learn/state-as-a-snapshot)
* [여러 state 업데이트를 큐에 담는 방법](/learn/queueing-a-series-of-state-updates)
* [state 안의 객체를 업데이트하는 방법](/learn/updating-objects-in-state)
* [state 안의 배열을 업데이트하는 방법](/learn/updating-arrays-in-state)

</YouWillLearn>

## 이벤트에 응답하기 {/*responding-to-events*/}

React에서는 JSX에 **이벤트 핸들러**를 추가할 수 있습니다. 이벤트 핸들러는 클릭, 마우스 호버, 폼 인풋 포커스 등 사용자의 상호작용에 반응해 실행되는 여러분의 함수입니다.

`<button>`처럼 내장된 컴포넌트는 `onClick`과 같은 내장 브라우저 이벤트만 지원합니다. 하지만 직접 만든 컴포넌트를 만들 때는 이벤트 핸들러 props에 애플리케이션에 맞는 원하는 이름을 붙일 수 있습니다.

<Sandpack>

```js
export default function App() {
  return (
    <Toolbar
      onPlayMovie={() => alert('재생 중!')}
      onUploadImage={() => alert('업로드 중!')}
    />
  );
}

function Toolbar({ onPlayMovie, onUploadImage }) {
  return (
    <div>
      <Button onClick={onPlayMovie}>
        영화 재생
      </Button>
      <Button onClick={onUploadImage}>
        이미지 업로드
      </Button>
    </div>
  );
}

function Button({ onClick, children }) {
  return (
    <button onClick={onClick}>
      {children}
    </button>
  );
}
```

```css
button { margin-right: 10px; }
```

</Sandpack>

<LearnMore path="/learn/responding-to-events">

**[이벤트에 응답하기](/learn/responding-to-events)** 에서 이벤트 핸들러를 추가하는 방법을 배워보세요.

</LearnMore>

## State: 컴포넌트의 기억 저장소 {/*state-a-components-memory*/}

컴포넌트는 상호작용의 결과로 화면의 내용을 바꾸어야 할 때가 많습니다. 폼에 입력하면 입력 필드가 갱신되어야 하고, 이미지 캐러셀에서 "다음"을 클릭하면 표시되는 이미지가 바뀌어야 하며, "구매"를 누르면 상품이 장바구니에 담겨야 합니다. 컴포넌트는 현재 입력값, 현재 이미지, 장바구니 같은 것들을 "기억"해야 합니다. React에서는 이러한 컴포넌트별 기억 저장소를 state라고 부릅니다.

[`useState`](/reference/react/useState) Hook으로 state를 추가할 수 있습니다. *Hook*은 컴포넌트가 React 기능을 사용할 수 있게 해주는 특별한 함수이며, `useState`도 그중 하나입니다. `useState`는 state 변수를 선언할 수 있게 해줍니다. 초깃값을 받아 현재 state 값과 이를 업데이트할 수 있는 state 설정 함수의 쌍을 반환합니다.

```js
const [index, setIndex] = useState(0);
const [showMore, setShowMore] = useState(false);
```

다음은 이미지 갤러리가 클릭에 따라 state를 사용하는 방법입니다.

<Sandpack>

```js
import { useState } from 'react';
import { sculptureList } from './data.js';

export default function Gallery() {
  const [index, setIndex] = useState(0);
  const [showMore, setShowMore] = useState(false);
  const hasNext = index < sculptureList.length - 1;

  function handleNextClick() {
    if (hasNext) {
      setIndex(index + 1);
    } else {
      setIndex(0);
    }
  }

  function handleMoreClick() {
    setShowMore(!showMore);
  }

  let sculpture = sculptureList[index];
  return (
    <>
      <button onClick={handleNextClick}>
        다음
      </button>
      <h2>
        <i>{sculpture.name} </i>
        by {sculpture.artist}
      </h2>
      <h3>
        ({index + 1} / {sculptureList.length})
      </h3>
      <button onClick={handleMoreClick}>
        {showMore ? '숨기기' : '보기'} 상세 정보
      </button>
      {showMore && <p>{sculpture.description}</p>}
      <img
        src={sculpture.url}
        alt={sculpture.alt}
      />
    </>
  );
}
```

```js src/data.js hidden
export const sculptureList = [{
  name: 'Homenaje a la Neurocirugía',
  artist: 'Marta Colvin Andrade',
  description: '콜빈은 주로 전 히스패닉 시대의 상징을 연상시키는 추상적인 주제로 알려져 있지만, 이 거대한 조각상은 그녀의 가장 잘 알려진 공공 예술 작품 중 하나입니다.',
  url: 'https://i.imgur.com/Mx7dA2Y.jpg',
  alt: '두 손이 정수리에서 만나 뻗어 있는 청동 조각상.'
}, {
  name: 'Floralis Genérica',
  artist: 'Eduardo Catalano',
  description: '이 거대한 은빛 꽃(높이 75피트)은 아르헨티나 부에노스아이레스에 있습니다. 해가 지면 꽃잎이 닫히고 해가 뜨면 열리도록 설계되었습니다.',
  url: 'https://i.imgur.com/ZF6s192m.jpg',
  alt: '반사되는 거울 같은 꽃잎과 단단한 수술을 가진 거대한 금속 꽃 조각상.'
}];
```

```css
h2 { margin-top: 10px; margin-bottom: 0; }
h3 { margin-top: 5px; font-weight: normal; font-size: 100%; }
img { width: 120px; height: 120px; }
button { display: block; margin-top: 10px; margin-bottom: 10px; }
```

</Sandpack>

<LearnMore path="/learn/state-a-components-memory">

**[State: 컴포넌트의 기억 저장소](/learn/state-a-components-memory)** 에서 값을 기억하고 상호작용에 따라 업데이트하는 방법을 배워보세요.

</LearnMore>

## 렌더링 그리고 커밋 {/*render-and-commit*/}

컴포넌트가 화면에 표시되기 전에 React가 먼저 렌더링해야 합니다. 이 과정을 이해하면 코드가 어떻게 실행되는지 파악하고 그 동작을 설명하는 데 도움이 됩니다.

컴포넌트를 주방의 요리사, React를 손님의 주문을 받아 음식을 내오는 웨이터라고 상상해 보세요. UI를 요청하고 제공받는 과정은 세 단계로 이루어집니다.

1. **렌더링 트리거** (손님의 주문을 주방에 전달)
2. **컴포넌트 렌더링** (주방에서 주문 준비)
3. **DOM에 커밋** (손님의 테이블에 주문 내용 전달)

<Illustration src="/images/docs/illustrations/i_render-and-commit.png" alt="React가 레스토랑에서 서버 역할을 하여 사용자의 요청을 받아 컴포넌트 주방에 전달하는 모습." />

<LearnMore path="/learn/render-and-commit">

**[렌더링 그리고 커밋](/learn/render-and-commit)** 에서 UI 업데이트의 생명 주기를 알아보세요.

</LearnMore>

## 스냅샷으로서의 state {/*state-as-a-snapshot*/}

일반 JavaScript 변수와 달리 React의 state는 스냅샷처럼 동작합니다. state 변수를 설정해도 이미 가지고 있는 state 변수는 바뀌지 않고, 대신 리렌더링을 일으킵니다. 처음에는 놀라울 수 있습니다.

```js
console.log(count);  // 0
setCount(count + 1); // 1로 리렌더링 요청
console.log(count);  // 여전히 0!
```

이 동작은 미묘한 버그를 피하는 데 도움이 됩니다. 다음은 채팅 앱 예시입니다. "보내기"를 누른 뒤 5초 안에 수신자를 Bob으로 바꾸면 어떻게 될까요? 추측해 보세요.

<Sandpack>

```js
import { useState } from 'react';

export default function Form() {
  const [to, setTo] = useState('Alice');
  const [message, setMessage] = useState('안녕');

  function handleSubmit(e) {
    e.preventDefault();
    setTimeout(() => {
      alert(`${to}에게 ${message}를 보냈습니다`);
    }, 5000);
  }

  return (
    <form onSubmit={handleSubmit}>
      <label>
        받는 사람:{' '}
        <select
          value={to}
          onChange={e => setTo(e.target.value)}>
          <option value="Alice">Alice</option>
          <option value="Bob">Bob</option>
        </select>
      </label>
      <textarea
        placeholder="메시지"
        value={message}
        onChange={e => setMessage(e.target.value)}
      />
      <button type="submit">보내기</button>
    </form>
  );
}
```

```css
label, textarea { margin-bottom: 10px; display: block; }
```

</Sandpack>

<LearnMore path="/learn/state-as-a-snapshot">

**[스냅샷으로서의 state](/learn/state-as-a-snapshot)** 에서 이벤트 핸들러 안에서 state가 "고정된" 값으로 보이는 이유를 배워보세요.

</LearnMore>

## 일련의 state 업데이트를 큐에 담기 {/*queueing-a-series-of-state-updates*/}

이 컴포넌트에는 버그가 있습니다. "+3"을 클릭해도 점수가 한 번만 증가합니다.

<Sandpack>

```js
import { useState } from 'react';

export default function Counter() {
  const [score, setScore] = useState(0);

  function increment() {
    setScore(score + 1);
  }

  return (
    <>
      <button onClick={() => increment()}>+1</button>
      <button onClick={() => {
        increment();
        increment();
        increment();
      }}>+3</button>
      <h1>점수: {score}</h1>
    </>
  );
}
```

```css
button { display: inline-block; margin: 10px; font-size: 20px; }
```

</Sandpack>

[스냅샷으로서의 state](/learn/state-as-a-snapshot)가 이유를 설명해 줍니다. state를 설정하면 새로운 리렌더링을 요청하지만 이미 실행 중인 코드의 값은 바꾸지 않습니다. 따라서 `setScore(score + 1)`을 세 번 호출해도 `score`는 계속 `0`입니다. 이는 *다음 state 값*을 기준으로 하는 **업데이터 함수**를 전달해 해결할 수 있습니다. `setScore(s => s + 1)`처럼 쓰면 큐에 담긴 업데이트가 차례로 적용됩니다.

<LearnMore path="/learn/queueing-a-series-of-state-updates">

**[일련의 state 업데이트를 큐에 담기](/learn/queueing-a-series-of-state-updates)** 에서 state 업데이트 큐의 동작을 배워보세요.

</LearnMore>

## state 안의 객체 업데이트하기 {/*updating-objects-in-state*/}

state에는 객체를 포함한 모든 종류의 JavaScript 값을 넣을 수 있습니다. 하지만 React state에 있는 객체를 직접 변경해서는 안 됩니다. 객체를 업데이트하고 싶다면 새 객체를 만들고(또는 기존 객체를 복사한 뒤), state가 그 복사본을 사용하도록 설정해야 합니다.

보통은 `...` 전개 구문을 사용해 변경하려는 부분만 바꾸어 복사합니다.

<Sandpack>

```js
import { useState } from 'react';

export default function Form() {
  const [person, setPerson] = useState({
    name: 'Niki de Saint Phalle',
    artwork: {
      title: 'Blue Nana',
      city: 'Hamburg',
    }
  });

  function handleNameChange(e) {
    setPerson({
      ...person,
      name: e.target.value
    });
  }

  function handleTitleChange(e) {
    setPerson({
      ...person,
      artwork: {
        ...person.artwork,
        title: e.target.value
      }
    });
  }

  return (
    <>
      <label>
        이름:
        <input value={person.name} onChange={handleNameChange} />
      </label>
      <label>
        제목:
        <input value={person.artwork.title} onChange={handleTitleChange} />
      </label>
      <p>
        <i>{person.artwork.title}</i>
        {' by '}
        {person.name}
      </p>
    </>
  );
}
```

```css
label { display: block; }
input { margin-left: 5px; margin-bottom: 5px; }
```

</Sandpack>

중첩된 객체를 복사하는 일이 번거롭다면 [Immer](https://github.com/immerjs/use-immer) 같은 라이브러리로 반복 코드를 줄일 수 있습니다.

<LearnMore path="/learn/updating-objects-in-state">

**[state 안의 객체 업데이트하기](/learn/updating-objects-in-state)** 에서 객체를 올바르게 업데이트하는 방법을 배워보세요.

</LearnMore>

## state 안의 배열 업데이트하기 {/*updating-arrays-in-state*/}

배열 또한 state에 저장할 수 있는 변경 가능한 JavaScript 객체입니다. 객체와 마찬가지로, state에 저장된 배열을 업데이트하려면 새 배열을 만들거나 기존 배열의 복사본을 만든 뒤 state를 새 배열로 설정해야 합니다.

| | 피해야 할 방법 (배열을 변경) | 선호하는 방법 (새로운 배열을 반환) |
|---|---|---|
| 추가 | `push`, `unshift`, `arr[i] = ...` | `concat`, `[...arr]` 전개 구문 |
| 제거 | `pop`, `shift`, `splice` | `filter`, `slice` |
| 교체 | `splice`, `arr[i] = ...` | `map` |
| 정렬 | `reverse`, `sort` | 배열을 먼저 복사 |

<LearnMore path="/learn/updating-arrays-in-state">

**[state 안의 배열 업데이트하기](/learn/updating-arrays-in-state)** 에서 배열을 올바르게 업데이트하는 방법을 배워보세요.

</LearnMore>

## 다음 단계는 무엇인가요? {/*whats-next*/}

[이벤트에 응답하기](/learn/responding-to-events)를 읽고 이 장을 한 페이지씩 차근차근 학습해 보세요!

또는 이미 위 주제들에 익숙하다면 [state 관리하기](/learn/managing-state)에 대해 읽어보는 것은 어떨까요?
