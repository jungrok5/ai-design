제목이 비어 있어서 React 공식 문서에서 자주 쓰이는 주제인 **"State: 컴포넌트의 메모리"**로 골라 썼습니다. 원하시던 제목이 따로 있으면 알려 주세요. 그 제목으로 다시 쓰겠습니다.

---

# State: 컴포넌트의 메모리

컴포넌트는 상호작용에 따라 화면에 보이는 내용을 바꿔야 할 때가 많습니다. 폼에 글자를 입력하면 입력 필드가 바뀌어야 하고, 이미지 캐러셀에서 "다음"을 누르면 다른 이미지가 보여야 합니다. "구매" 버튼을 누르면 상품이 장바구니에 담겨야 합니다. 이렇게 하려면 컴포넌트가 현재 입력값, 현재 이미지, 장바구니 같은 것을 "기억"해야 합니다. React에서는 이런 컴포넌트별 메모리를 **state**라고 부릅니다.

<YouWillLearn>

- [`useState`](/reference/react/useState) Hook으로 state 변수를 추가하는 방법
- `useState` Hook이 반환하는 두 값
- state 변수를 여러 개 추가하는 방법
- state가 지역적(local)이라고 하는 이유

</YouWillLearn>

## 일반 변수로는 충분하지 않은 경우 {/*when-a-regular-variable-isnt-enough*/}

조각상 이미지를 보여 주는 컴포넌트가 있다고 해 보겠습니다. "Next" 버튼을 누르면 `index`가 `1`, `2`로 늘어나면서 다음 조각상이 나와야 합니다. 하지만 아래 코드는 **동작하지 않습니다.**

```js
import { sculptureList } from './data.js';

export default function Gallery() {
  let index = 0;

  function handleClick() {
    index = index + 1;
  }

  let sculpture = sculptureList[index];
  return (
    <>
      <button onClick={handleClick}>Next</button>
      <h2>{sculpture.name}</h2>
      <img src={sculpture.url} alt={sculpture.alt} />
    </>
  );
}
```

`handleClick` 이벤트 핸들러가 지역 변수 `index`를 바꾸지만, 화면은 바뀌지 않습니다. 이유는 두 가지입니다.

1. **지역 변수는 렌더링 사이에 유지되지 않습니다.** React는 컴포넌트를 다시 렌더링할 때 처음부터 다시 실행합니다. 이때 이전에 지역 변수를 바꾼 내용은 고려하지 않습니다.
2. **지역 변수를 바꿔도 렌더링이 일어나지 않습니다.** React는 새 데이터로 컴포넌트를 다시 렌더링해야 한다는 것을 알지 못합니다.

컴포넌트를 새 데이터로 업데이트하려면 다음 두 가지가 필요합니다.

1. 렌더링 사이에 데이터를 **유지**해야 합니다.
2. 새 데이터로 컴포넌트를 렌더링하도록 React에 **알려야(trigger)** 합니다.

[`useState`](/reference/react/useState) Hook은 이 두 가지를 모두 제공합니다.

1. 렌더링 사이에 데이터를 유지하는 **state 변수**
2. 변수를 업데이트하고 React가 컴포넌트를 다시 렌더링하게 하는 **state setter 함수**

## state 변수 추가하기 {/*adding-a-state-variable*/}

state 변수를 추가하려면 파일 맨 위에서 React의 `useState`를 가져옵니다.

```js
import { useState } from 'react';
```

그다음 아래 줄을

```js
let index = 0;
```

이렇게 바꿉니다.

```js
const [index, setIndex] = useState(0);
```

`index`는 state 변수이고 `setIndex`는 setter 함수입니다. 이벤트 핸들러에서는 이렇게 씁니다.

```js
function handleClick() {
  setIndex(index + 1);
}
```

이제 "Next" 버튼을 누르면 조각상이 바뀝니다.

## 첫 번째 Hook 만나기 {/*meet-your-first-hook*/}

React에서 `useState`처럼 `use`로 시작하는 함수를 모두 **Hook**이라고 부릅니다. Hook은 React가 [렌더링](/learn/render-and-commit) 중일 때만 쓸 수 있는 특별한 함수입니다. Hook을 쓰면 컴포넌트가 여러 React 기능에 "연결(hook into)"될 수 있습니다. state는 그런 기능 중 하나이고, 다른 Hook은 뒤에서 다룹니다.

<Pitfall>

**Hook은 컴포넌트의 최상위 수준**이나 직접 만든 Hook 안에서만 호출할 수 있습니다. 조건문, 반복문, 중첩 함수 안에서는 Hook을 호출할 수 없습니다. Hook은 함수이긴 하지만, 컴포넌트에 필요한 것을 조건 없이 "선언"한다고 생각하면 이해하기 쉽습니다. 파일 맨 위에서 모듈을 `import`하는 것과 비슷합니다.

</Pitfall>

## `useState` 해부하기 {/*anatomy-of-usestate*/}

[`useState`](/reference/react/useState)를 호출하는 것은 React에 이 컴포넌트가 무언가를 기억해야 한다고 알리는 것입니다.

```js
const [index, setIndex] = useState(0);
```

위 코드에서는 React가 `index`를 기억합니다. `useState`에 넘기는 유일한 인자는 state 변수의 **초기값**입니다. 여기서는 `0`입니다.

컴포넌트가 렌더링될 때마다 `useState`는 다음 두 값이 든 배열을 반환합니다.

1. 저장해 둔 값이 담긴 **state 변수** (`index`)
2. state 변수를 업데이트하고 React가 컴포넌트를 다시 렌더링하게 하는 **setter 함수** (`setIndex`)

실제로는 다음 순서로 동작합니다.

1. **컴포넌트가 처음 렌더링됩니다.** `index`의 초기값으로 `0`을 넘겼으므로 `[0, setIndex]`가 반환됩니다. React는 `0`을 최신 state 값으로 기억합니다.
2. **state를 업데이트합니다.** 사용자가 버튼을 누르면 `setIndex(index + 1)`이 호출됩니다. `index`가 `0`이므로 `setIndex(1)`이 됩니다. React는 이제 `index`가 `1`이라는 것을 기억하고 다시 렌더링을 시작합니다.
3. **컴포넌트가 두 번째로 렌더링됩니다.** React는 여전히 `useState(0)`을 보지만, `index`를 `1`로 설정했다는 것을 기억하고 있으므로 `[1, setIndex]`를 반환합니다.
4. 이후에도 같은 과정이 반복됩니다.

<Note>

state 변수와 setter 함수의 이름은 `[something, setSomething]`처럼 짓는 것이 관례입니다. 다른 이름을 써도 동작하지만, 관례를 따르면 여러 프로젝트에서 코드를 읽기 쉬워집니다.

</Note>

## 여러 개의 state 변수 사용하기 {/*giving-a-component-multiple-state-variables*/}

한 컴포넌트 안에서 원하는 만큼 많은 종류의 state 변수를 쓸 수 있습니다. 아래 컴포넌트에는 숫자 `index`와 상세 설명 표시 여부를 담는 불리언 `showMore`가 있습니다.

```js
const [index, setIndex] = useState(0);
const [showMore, setShowMore] = useState(false);

function handleMoreClick() {
  setShowMore(!showMore);
}
```

이 예시의 `index`와 `showMore`처럼 서로 관련이 없는 state는 변수를 나누는 것이 좋습니다. 반대로 두 state 변수를 항상 함께 바꾼다면 하나로 합치는 편이 나을 수 있습니다. 예를 들어 필드가 많은 폼은 필드마다 state 변수를 두기보다 객체 하나를 state로 두는 것이 더 편할 수 있습니다. 자세한 내용은 [state 구조 선택하기](/learn/choosing-the-state-structure)를 참고하세요.

## State는 격리되어 있고 비공개입니다 {/*state-is-isolated-and-private*/}

state는 화면에 있는 컴포넌트 인스턴스마다 따로 존재합니다. 즉, **같은 컴포넌트를 두 번 렌더링하면 각 사본은 완전히 독립된 state를 갖습니다.** 한쪽을 바꿔도 다른 쪽에는 영향이 없습니다.

```js
export default function Page() {
  return (
    <div className="Page">
      <Gallery />
      <Gallery />
    </div>
  );
}
```

모듈 맨 위에 선언하는 일반 변수와 state가 다른 점이 바로 이것입니다. state는 특정 함수 호출이나 코드 위치에 묶여 있지 않고, 화면의 특정 위치에 "지역적"입니다. 위에서 `<Gallery />`를 두 번 렌더링했으므로 state도 따로따로 저장됩니다.

또한 `Page` 컴포넌트는 `Gallery`의 state가 무엇인지, 심지어 state가 있는지조차 알지 못합니다. props와 달리 **state는 그것을 선언한 컴포넌트만 접근할 수 있는 비공개 값**입니다. 부모 컴포넌트는 state를 바꿀 수 없습니다. 그래서 다른 컴포넌트에 영향을 주지 않고 언제든 state를 추가하거나 제거할 수 있습니다.

두 갤러리가 state를 동기화하게 하려면 React에서는 자식 컴포넌트의 state를 없애고 가장 가까운 공통 부모에 state를 둡니다. 이 방법은 [컴포넌트 간 state 공유하기](/learn/sharing-state-between-components)에서 자세히 다룹니다.

<Recap>

- 컴포넌트가 렌더링 사이에 정보를 "기억"해야 할 때는 state 변수를 사용합니다.
- state 변수는 `useState` Hook을 호출해서 선언합니다.
- Hook은 `use`로 시작하는 특별한 함수로, state 같은 React 기능에 "연결"할 수 있게 해 줍니다.
- Hook은 조건 없이 컴포넌트의 최상위 수준에서만 호출해야 합니다.
- `useState` Hook은 현재 state와 그것을 업데이트하는 함수, 두 값을 반환합니다.
- state 변수는 여러 개 둘 수 있습니다. React는 호출 순서로 각 state를 구분합니다.
- state는 컴포넌트에 비공개입니다. 같은 컴포넌트를 두 곳에서 렌더링하면 각 사본은 자기만의 state를 갖습니다.

</Recap>
