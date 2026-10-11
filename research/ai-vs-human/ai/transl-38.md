# JavaScript 객체 기본

## 개요

객체(object)는 JavaScript에서 데이터를 **키(key)와 값(value)의 쌍**으로 묶어 저장하는 기본 자료 구조입니다. 키는 보통 문자열이나 심볼(Symbol)이며, 값에는 숫자, 문자열, 배열, 함수, 다른 객체 등 어떤 타입이든 들어갈 수 있습니다.

객체의 키-값 쌍은 **속성(property)**이라고 부릅니다. 값이 함수인 속성은 특별히 **메서드(method)**라고 부릅니다.

```js
const person = {
  name: "지수",
  age: 28,
  greet() {
    return `안녕하세요, ${this.name}입니다.`;
  },
};

console.log(person.name);    // "지수"
console.log(person.greet()); // "안녕하세요, 지수입니다."
```

## 객체 만들기

### 객체 리터럴

가장 흔한 방법은 중괄호 `{}`를 사용하는 **객체 리터럴**입니다.

```js
const car = { brand: "현대", year: 2024 };
```

### `new Object()`

빈 객체를 만드는 생성자 호출도 가능하지만, 일반적으로는 리터럴 표기법이 더 간결하고 읽기 좋아서 권장됩니다.

```js
const empty = new Object(); // 동작은 하지만 잘 쓰지 않음
const obj = {};             // 권장
```

### 생성자 함수와 `class`

같은 구조의 객체를 여러 개 만들 때는 생성자 함수나 `class` 문법을 사용합니다.

```js
class Point {
  constructor(x, y) {
    this.x = x;
    this.y = y;
  }
}

const p = new Point(3, 4);
```

## 속성 접근

속성에 접근하는 방법은 두 가지입니다.

- **점 표기법**: `obj.key`
- **대괄호 표기법**: `obj["key"]`

대괄호 표기법은 키가 공백이나 하이픈을 포함하거나, 변수에 담긴 키를 사용할 때 필요합니다.

```js
const user = { "user-name": "민수", age: 30 };

console.log(user["user-name"]); // "민수"

const key = "age";
console.log(user[key]);         // 30
// console.log(user.key);       // undefined: 'key'라는 이름의 속성을 찾음
```

존재하지 않는 속성에 접근하면 에러가 아니라 `undefined`가 반환됩니다.

## 속성 추가, 수정, 삭제

객체는 생성된 뒤에도 자유롭게 변경할 수 있습니다.

```js
const book = { title: "자바스크립트 입문" };

book.author = "홍길동";   // 추가
book.title = "JS 입문";   // 수정
delete book.author;       // 삭제

console.log(book); // { title: "JS 입문" }
```

`const`로 선언해도 **객체 내부의 속성은 변경할 수 있습니다.** `const`는 변수가 가리키는 참조를 바꾸지 못하게 할 뿐입니다.

## `this` 키워드

메서드 안에서 `this`는 보통 메서드를 호출한 객체를 가리킵니다.

```js
const counter = {
  count: 0,
  increment() {
    this.count++;
    return this.count;
  },
};

counter.increment(); // 1
counter.increment(); // 2
```

화살표 함수는 자신만의 `this`를 갖지 않고 바깥 스코프의 `this`를 물려받습니다. 따라서 객체의 메서드를 화살표 함수로 정의하면 의도와 다르게 동작할 수 있으니 주의해야 합니다.

## 편리한 문법

### 속성 단축 표기

변수 이름과 속성 이름이 같으면 줄여서 쓸 수 있습니다.

```js
const name = "수진";
const age = 25;

const profile = { name, age }; // { name: "수진", age: 25 }
```

### 계산된 속성 이름

대괄호로 감싸면 키를 표현식으로 계산할 수 있습니다.

```js
const field = "color";
const item = { [field]: "빨강" }; // { color: "빨강" }
```

### 구조 분해 할당

객체의 속성을 변수로 간편하게 꺼낼 수 있습니다.

```js
const { name, age, city = "서울" } = { name: "현우", age: 40 };
console.log(name, age, city); // "현우" 40 "서울"
```

### 나머지 속성과 전개 구문

```js
const base = { a: 1, b: 2 };
const extended = { ...base, b: 99, c: 3 };
console.log(extended); // { a: 1, b: 99, c: 3 }
```

전개 구문(`...`)은 얕은 복사(shallow copy)를 수행합니다. 중첩된 객체는 여전히 같은 참조를 공유합니다.

## 객체 순회

객체의 속성들을 순회하는 대표적인 방법은 다음과 같습니다.

```js
const score = { math: 90, english: 85, science: 92 };

// 키 목록
for (const key of Object.keys(score)) {
  console.log(key);
}

// 값 목록
console.log(Object.values(score)); // [90, 85, 92]

// 키-값 쌍
for (const [key, value] of Object.entries(score)) {
  console.log(`${key}: ${value}`);
}
```

`for...in` 문도 사용할 수 있지만, 상속된 열거 가능한 속성까지 포함될 수 있으므로 일반 객체를 순회할 때는 위의 `Object` 메서드들이 더 안전합니다.

## 참조 타입

객체는 **참조 타입**입니다. 변수에는 객체 자체가 아니라 객체가 저장된 메모리 위치에 대한 참조가 담깁니다. 따라서 객체를 다른 변수에 대입하면 같은 객체를 가리키게 됩니다.

```js
const a = { value: 1 };
const b = a;

b.value = 2;
console.log(a.value); // 2
```

독립된 복사본이 필요하다면 `structuredClone()`이나 전개 구문을 사용합니다.

```js
const copy = structuredClone(a); // 깊은 복사
```

## 객체 동결

객체의 변경을 막고 싶다면 `Object.freeze()`를 사용할 수 있습니다.

```js
const config = Object.freeze({ debug: false });
config.debug = true; // 엄격 모드가 아니면 무시되고, 엄격 모드에서는 에러
console.log(config.debug); // false
```

`freeze`는 얕게 동작하므로 중첩된 객체까지 막으려면 재귀적으로 적용해야 합니다.

## 요약

- 객체는 키-값 쌍의 모음이며, 값으로 함수를 넣으면 메서드가 됩니다.
- 속성 접근에는 점 표기법과 대괄호 표기법을 상황에 맞게 사용합니다.
- 객체는 참조 타입이므로 복사와 대입의 차이를 이해해야 합니다.
- 전개 구문, 구조 분해, 단축 표기 등을 활용하면 코드가 간결해집니다.
- 순회에는 `Object.keys()`, `Object.values()`, `Object.entries()`가 안전하게 쓰입니다.
