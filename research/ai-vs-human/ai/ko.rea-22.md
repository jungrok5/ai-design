# 서버 함수

<Intro>

서버 함수(Server Functions)를 사용하면 클라이언트 컴포넌트에서 서버에서 실행되는 비동기 함수를 호출할 수 있습니다.

</Intro>

<Note>

#### 서버 함수는 어떤 기능을 위한 것인가요? {/*what-are-server-functions*/}

서버 함수는 `"use server"` 지시어로 정의하며, 클라이언트 코드에서 마치 일반 함수처럼 호출할 수 있습니다. 실제로는 React가 서버로 요청을 보내고 결과를 돌려받습니다. 이 기능을 사용하려면 React Server Components를 지원하는 프레임워크나 번들러 설정이 필요합니다.

</Note>

<InlineToc />

---

## 개요 {/*overview*/}

서버 함수는 데이터베이스 변경, 파일 처리, 비밀 키가 필요한 외부 API 호출처럼 서버에서만 안전하게 실행해야 하는 작업을 클라이언트에서 간편하게 트리거할 수 있게 해 줍니다. 별도의 API 엔드포인트를 만들고 `fetch`로 호출하는 과정을 React가 대신 처리합니다.

서버 함수를 정의하면 프레임워크는 해당 함수에 대한 참조를 만들어 클라이언트 컴포넌트에 전달합니다. 클라이언트에서 이 참조를 호출하면 React는 서버에 요청을 보내 함수를 실행하고, 반환값을 클라이언트로 돌려줍니다.

<Pitfall>

서버 함수는 공개적으로 접근 가능한 엔드포인트와 같다고 생각해야 합니다. 클라이언트가 보내는 모든 인자는 신뢰할 수 없는 입력이므로, 반드시 서버에서 인증, 권한 확인, 입력값 검증을 수행하세요.

</Pitfall>

---

## 서버 함수 만들기 {/*creating-server-functions*/}

서버 함수는 두 가지 방법으로 정의할 수 있습니다.

### 함수 단위로 정의하기 {/*function-level*/}

비동기 함수의 본문 첫 줄에 `"use server"` 지시어를 추가합니다.

```js {2}
async function requestUsername(formData) {
  'use server';
  const username = formData.get('username');
  // ...
}
```

이 방식은 서버 컴포넌트 안에서 함수를 정의하고, 이를 클라이언트 컴포넌트에 props로 전달할 때 유용합니다.

### 모듈 단위로 정의하기 {/*module-level*/}

파일의 맨 위에 `"use server"`를 작성하면 해당 파일이 내보내는 모든 함수가 서버 함수가 됩니다.

```js [[1, 1, "'use server'"]]
'use server';

export async function createNote() {
  await db.notes.create();
}

export async function deleteNote(id) {
  await db.notes.delete(id);
}
```

클라이언트 컴포넌트에서는 이 파일에서 함수를 가져와 사용하면 됩니다. 번들러는 클라이언트 번들에 함수 본문 대신 서버를 가리키는 참조만 포함합니다.

---

## 서버 함수 사용하기 {/*using-server-functions*/}

### 폼 액션과 함께 사용하기 {/*with-form-actions*/}

가장 흔한 사용법은 `<form>`의 `action`에 서버 함수를 전달하는 것입니다. 서버 함수는 `FormData`를 인자로 받습니다.

```js
import { updateName } from './actions';

function UpdateName() {
  return (
    <form action={updateName}>
      <input type="text" name="name" />
      <button type="submit">저장</button>
    </form>
  );
}
```

이 방식은 점진적 향상(progressive enhancement)을 지원합니다. 프레임워크에 따라 JavaScript가 로드되기 전에도 폼이 동작할 수 있습니다.

### 이벤트 핸들러에서 호출하기 {/*in-event-handlers*/}

폼이 아닌 곳에서도 서버 함수를 호출할 수 있습니다. 이때는 상태 업데이트와 함께 쓰기 위해 [트랜지션](/reference/react/useTransition) 안에서 호출하는 것이 좋습니다.

```js
import { incrementLike } from './actions';
import { useState, useTransition } from 'react';

function LikeButton() {
  const [likes, setLikes] = useState(0);
  const [isPending, startTransition] = useTransition();

  const onClick = () => {
    startTransition(async () => {
      const newLikes = await incrementLike();
      setLikes(newLikes);
    });
  };

  return (
    <button onClick={onClick} disabled={isPending}>
      좋아요 {likes}
    </button>
  );
}
```

### useActionState와 함께 사용하기 {/*with-use-action-state*/}

서버 함수의 결과나 오류를 UI에 보여 주려면 [`useActionState`](/reference/react/useActionState)를 사용합니다.

```js
import { useActionState } from 'react';
import { signup } from './actions';

function Signup() {
  const [state, formAction, isPending] = useActionState(signup, null);

  return (
    <form action={formAction}>
      <input name="email" type="email" />
      <button disabled={isPending}>가입</button>
      {state?.error && <p>{state.error}</p>}
    </form>
  );
}
```

---

## 인자와 반환값 {/*arguments-and-return-values*/}

클라이언트와 서버 사이에서 주고받는 값은 직렬화(serialize)할 수 있어야 합니다. 문자열, 숫자, 불리언, `Date`, `Map`, `Set`, 프로미스, `FormData` 등은 전달할 수 있지만, 함수(다른 서버 함수 제외), 클래스 인스턴스, 심볼 등은 전달할 수 없습니다.

추가 인자를 미리 묶어서 전달하려면 `bind`를 사용하세요.

```js
function DeleteButton({ id }) {
  const deleteWithId = deleteNote.bind(null, id);
  return (
    <form action={deleteWithId}>
      <button>삭제</button>
    </form>
  );
}
```

---

## 주의 사항 {/*caveats*/}

- **순차 실행**: 서버 함수 호출은 기본적으로 한 번에 하나씩 순서대로 처리됩니다. 병렬로 데이터를 가져와야 한다면 서버 컴포넌트에서 가져오는 방식을 고려하세요.
- **POST 요청**: 서버 함수는 항상 POST 요청으로 전달되므로 데이터 조회보다는 데이터 변경에 적합합니다.
- **보안**: 서버 함수 안에서 사용하는 비밀 값은 클라이언트에 노출되지 않지만, 반환값은 그대로 클라이언트에 전달됩니다. 민감한 정보를 반환하지 않도록 주의하세요.
- **클로저**: 서버 컴포넌트 안에서 정의한 서버 함수가 클로저로 값을 캡처하면, 해당 값은 암호화되어 클라이언트를 거쳐 전달됩니다. 그래도 가능한 한 명시적인 인자를 사용하는 편이 안전합니다.
- **프레임워크 지원**: 서버 함수의 세부 동작과 설정은 사용하는 프레임워크나 번들러에 따라 다를 수 있습니다.

<DeepDive>

#### 서버 액션과 서버 함수는 같은 것인가요? {/*server-actions-vs-functions*/}

이전에는 "서버 액션(Server Actions)"이라는 이름이 널리 쓰였습니다. 현재는 서버에서 실행되는 모든 함수를 가리키는 "서버 함수"가 올바른 용어이며, 그중 `action` prop에 전달되거나 트랜지션 안에서 호출되는 것을 "서버 액션"이라 부를 수 있습니다.

</DeepDive>

---

## 더 알아보기 {/*learn-more*/}

- [`"use server"` 지시어](/reference/rsc/use-server)
- [서버 컴포넌트](/reference/rsc/server-components)
- [`useActionState`](/reference/react/useActionState)
- [`useTransition`](/reference/react/useTransition)
