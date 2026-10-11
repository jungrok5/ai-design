# 중괄호가 있는 JSX 안에서 자바스크립트 사용하기

JSX를 사용하면 자바스크립트 파일 안에 HTML과 비슷한 마크업을 작성할 수 있어서, 렌더링 로직과 콘텐츠를 한곳에 둘 수 있습니다. 가끔은 마크업 안에 자바스크립트 로직을 조금 추가하거나 동적인 프로퍼티를 참조하고 싶을 때가 있습니다. 이럴 때 JSX 안에서 중괄호를 사용하면 자바스크립트로 통하는 창을 열 수 있습니다.

<YouWillLearn>

* 따옴표로 문자열을 전달하는 방법
* 중괄호로 JSX 안에서 자바스크립트 변수를 참조하는 방법
* 중괄호로 JSX 안에서 자바스크립트 함수를 호출하는 방법
* 중괄호로 JSX 안에서 자바스크립트 객체를 사용하는 방법

</YouWillLearn>

## 따옴표로 문자열 전달하기

JSX에 문자열 어트리뷰트를 전달하려면 작은따옴표나 큰따옴표로 묶습니다.

```js
export default function Avatar() {
  return (
    <img
      className="avatar"
      src="https://i.imgur.com/7vQD0fPs.jpg"
      alt="Gregorio Y. Zara"
    />
  );
}
```

여기서 `"https://i.imgur.com/7vQD0fPs.jpg"`와 `"Gregorio Y. Zara"`는 문자열로 전달됩니다.

그렇다면 `src`나 `alt` 텍스트를 동적으로 지정하려면 어떻게 해야 할까요? `"`와 `"`를 `{`와 `}`로 바꾸면 **자바스크립트의 값을 사용**할 수 있습니다.

```js
export default function Avatar() {
  const avatar = 'https://i.imgur.com/7vQD0fPs.jpg';
  const description = 'Gregorio Y. Zara';
  return (
    <img
      className="avatar"
      src={avatar}
      alt={description}
    />
  );
}
```

`className="avatar"`처럼 따옴표로 지정한 부분과 `src={avatar}`처럼 중괄호로 지정한 부분의 차이를 확인해 보세요. 중괄호를 쓰면 `avatar` 변수의 값을 읽어서 `src` 어트리뷰트에 전달합니다.

## 중괄호 사용하기: 자바스크립트 세상으로 통하는 창

JSX는 자바스크립트를 작성하는 특별한 방법입니다. 그래서 중괄호 `{ }`를 사용해 그 안에서 다시 자바스크립트를 사용할 수 있습니다. 다음 예시는 먼저 `name`이라는 변수를 선언한 뒤, `<h1>` 태그 안에서 중괄호로 감싸 사용합니다.

```js
export default function TodoList() {
  const name = 'Gregorio Y. Zara';
  return (
    <h1>{name}의 할 일 목록</h1>
  );
}
```

`name`의 값을 `'Hedy Lamarr'`나 `'Hedy Lamarr 2'`처럼 다른 값으로 바꿔 보세요. 목록의 제목이 어떻게 바뀌는지 확인할 수 있습니다.

변수뿐만 아니라 `formatDate()` 같은 함수 호출을 포함해, 어떤 자바스크립트 **표현식**이든 중괄호 사이에서 동작합니다.

```js
const today = new Date();

function formatDate(date) {
  return new Intl.DateTimeFormat(
    'ko-KR',
    { weekday: 'long' }
  ).format(date);
}

export default function TodoList() {
  return (
    <h1>{formatDate(today)}의 할 일 목록</h1>
  );
}
```

## 중괄호를 사용할 수 있는 곳

JSX 안에서는 중괄호를 두 가지 방법으로 사용할 수 있습니다.

1. **JSX 태그 안의 텍스트로 사용하기**: `<h1>{name}의 할 일 목록</h1>`은 동작하지만, `<{tag}>Gregorio Y. Zara의 할 일 목록</{tag}>`은 동작하지 않습니다.
2. **`=` 바로 뒤에 오는 어트리뷰트로 사용하기**: `src={avatar}`는 `avatar` 변수를 읽지만, `src="{avatar}"`는 `"{avatar}"`라는 문자열 자체를 그대로 전달합니다.

즉, 태그의 이름 자리에는 쓸 수 없고, 태그 사이의 콘텐츠 자리와 어트리뷰트의 값 자리에서만 쓸 수 있습니다.

## "이중 중괄호" 사용하기: JSX 안의 CSS와 다른 객체

문자열, 숫자 및 기타 자바스크립트 표현식뿐만 아니라 JSX에서 객체를 전달할 수도 있습니다. 객체도 `{ name: "Hedy Lamarr", inventions: 5 }`처럼 중괄호로 표현합니다. 따라서 JSX에서 자바스크립트 객체를 전달하려면 객체를 또 다른 중괄호 쌍으로 감싸야 합니다. `person={{ name: "Hedy Lamarr", inventions: 5 }}`처럼요.

인라인 CSS 스타일에서 이런 표기를 본 적이 있을 것입니다. React에서는 인라인 `style`을 꼭 사용해야 하는 것은 아닙니다. CSS 클래스가 대부분의 경우에 잘 동작하기 때문입니다. 하지만 인라인 `style` 어트리뷰트는 동적인 스타일이 필요할 때 유용합니다.

```js
export default function TodoList() {
  return (
    <ul style={{
      backgroundColor: 'black',
      color: 'pink'
    }}>
      <li>Improve the videophone</li>
      <li>Prepare aeronautics lectures</li>
      <li>Work on the alcohol-fuelled engine</li>
    </ul>
  );
}
```

다음 코드에서 `{{`와 `}}`를 보면 JSX의 특별한 문법이 있다고 생각할 수 있지만, 사실은 JSX 중괄호 안에 객체가 들어 있는 것일 뿐입니다.

```js
<ul style={
  {
    backgroundColor: 'black',
    color: 'pink'
  }
}>
```

인라인 `style` 프로퍼티는 카멜 케이스(camelCase)로 작성합니다. 예를 들어 HTML에서 `<ul style="background-color: black">`으로 쓰는 것을 컴포넌트에서는 `<ul style={{ backgroundColor: 'black' }}>`로 작성해야 합니다.

## 자바스크립트 객체와 중괄호에 대해 더 알아보기

여러 표현식을 하나의 객체에 담아서 JSX 중괄호 안에서 참조할 수도 있습니다.

```js
const person = {
  name: 'Gregorio Y. Zara',
  theme: {
    backgroundColor: 'black',
    color: 'pink'
  }
};

export default function TodoList() {
  return (
    <div style={person.theme}>
      <h1>{person.name}의 할 일 목록</h1>
      <img
        className="avatar"
        src="https://i.imgur.com/7vQD0fPs.jpg"
        alt="Gregorio Y. Zara"
      />
      <ul>
        <li>Improve the videophone</li>
        <li>Prepare aeronautics lectures</li>
        <li>Work on the alcohol-fuelled engine</li>
      </ul>
    </div>
  );
}
```

이 예시에서 `person` 객체는 `name` 문자열과 `theme` 객체를 포함합니다. 컴포넌트는 `person.name`처럼 점 표기법으로 값을 읽고, `person.theme`을 통째로 `style`에 전달합니다.

JSX는 템플릿 언어보다는 자바스크립트에 가깝게 설계되었기 때문에, 데이터와 로직을 자바스크립트로 정리한 다음 마크업에서 간결하게 참조할 수 있습니다.

<Recap>

이제 JSX에 대해 거의 모든 것을 알게 되었습니다.

* 따옴표로 묶인 JSX 어트리뷰트는 문자열로 전달됩니다.
* 중괄호를 사용하면 자바스크립트 로직과 변수를 마크업 안으로 가져올 수 있습니다.
* 중괄호는 JSX 태그 콘텐츠의 내부 또는 어트리뷰트의 `=` 바로 뒤에서 동작합니다.
* `{{`와 `}}`는 특별한 문법이 아니라 JSX 중괄호 안에 들어 있는 자바스크립트 객체입니다.

</Recap>

<Challenges>

#### 실수 고치기

다음 코드는 `Objects are not valid as a React child`라는 오류와 함께 충돌합니다.

```js
const person = {
  name: 'Gregorio Y. Zara',
  theme: {
    backgroundColor: 'black',
    color: 'pink'
  }
};

export default function TodoList() {
  return (
    <div style={person.theme}>
      <h1>{person}의 할 일 목록</h1>
    </div>
  );
}
```

<Solution>

`{person}`은 객체 전체를 렌더링하려고 하기 때문에 오류가 발생합니다. 문자열을 렌더링하려면 `{person.name}`으로 바꿔야 합니다. React는 객체를 자식으로 렌더링하는 방법을 알지 못합니다.

</Solution>

</Challenges>
