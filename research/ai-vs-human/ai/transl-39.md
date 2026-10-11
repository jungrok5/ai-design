# 객체 프로토타입

프로토타입은 JavaScript 객체가 서로 기능을 상속받는 메커니즘입니다. 이 문서에서는 프로토타입이 무엇인지, 프로토타입 체인이 어떻게 동작하는지, 그리고 객체의 프로토타입을 설정하는 방법을 설명합니다.

| | |
|---|---|
| **사전 지식:** | JavaScript 함수에 대한 이해, JavaScript 기초([JavaScript 첫걸음](/ko/docs/Learn/JavaScript/First_steps), [JavaScript 구성 요소](/ko/docs/Learn/JavaScript/Building_blocks) 참고), 객체 기초([JavaScript 객체 기본](/ko/docs/Learn/JavaScript/Objects/Basics) 참고) |
| **목표:** | JavaScript 객체 프로토타입과 프로토타입 체인의 동작 방식, 객체의 프로토타입을 설정하는 방법을 이해합니다. |

## 프로토타입 체인

브라우저 콘솔에서 다음과 같이 객체 리터럴을 만들어 봅시다.

```js
const myObject = {
  city: "Madrid",
  greet() {
    console.log(`Greetings from ${this.city}`);
  },
};

myObject.greet(); // Greetings from Madrid
```

이 객체에는 데이터 속성 `city`와 메서드 `greet()`가 있습니다. 콘솔에 `myObject.`까지 입력하면 자동 완성 목록이 나타나는데, 여기에는 `city`와 `greet` 외에도 다음과 같은 속성이 많이 보입니다.

```plain
__defineGetter__
__defineSetter__
__lookupGetter__
__lookupSetter__
__proto__
city
constructor
greet
hasOwnProperty
isPrototypeOf
propertyIsEnumerable
toLocaleString
toString
valueOf
```

이 중 하나를 호출해 보세요.

```js
myObject.toString(); // "[object Object]"
```

정의한 적 없는 `toString()`이 동작합니다. 그렇다면 이 속성들은 어디서 온 것일까요?

JavaScript의 모든 객체에는 **프로토타입(prototype)** 이라고 부르는 내장 속성이 있습니다. 프로토타입도 객체이므로 그 자체로 프로토타입을 가지며, 이렇게 이어진 연결을 **프로토타입 체인(prototype chain)** 이라고 합니다. 체인은 자신의 프로토타입이 `null`인 객체에 이르러 끝납니다.

> [!NOTE]
> 객체의 프로토타입을 가리키는 속성은 `prototype`이 **아닙니다**. 명세에서는 이를 `[[Prototype]]`이라고 표기하며, 이름은 표준이 아니지만 대부분의 브라우저는 `__proto__`라는 이름으로 노출합니다. 객체의 프로토타입에 접근하는 표준 방법은 {{jsxref("Object.getPrototypeOf()")}} 메서드입니다.

객체의 속성에 접근하면 먼저 객체 자신에서 그 속성을 찾습니다. 찾지 못하면 프로토타입에서 찾고, 그래도 없으면 프로토타입의 프로토타입에서 찾는 식으로 체인 끝에 이를 때까지 검색합니다. 끝까지 찾지 못하면 `undefined`를 반환합니다.

따라서 `myObject.toString()`을 호출하면 브라우저는 다음 순서로 동작합니다.

1. `myObject`에서 `toString`을 찾습니다.
2. 찾지 못했으므로 `myObject`의 프로토타입 객체에서 `toString`을 찾습니다.
3. 그곳에서 찾았으므로 호출합니다.

`myObject`의 프로토타입은 다음과 같이 확인할 수 있습니다.

```js
Object.getPrototypeOf(myObject); // Object { }
```

이 객체는 `Object.prototype`이라고 하며, 모든 객체가 기본으로 갖는 가장 기본적인 프로토타입입니다. `Object.prototype`의 프로토타입은 `null`이므로 이곳이 프로토타입 체인의 끝입니다.

다만 객체의 프로토타입이 항상 `Object.prototype`인 것은 아닙니다. 다음 예제를 보세요.

```js
const myDate = new Date();
let object = myDate;

do {
  object = Object.getPrototypeOf(object);
  console.log(object);
} while (object);

// Date.prototype
// Object { }
// null
```

`Date` 객체를 만들고 프로토타입 체인을 따라가며 각 프로토타입을 출력했습니다. `myDate`의 프로토타입은 `Date.prototype`이고, 그 프로토타입이 `Object.prototype`입니다. 그래서 `myDate.getTime()`처럼 `Date.prototype`에 정의된 메서드를 사용할 수 있습니다.

## 속성 섀도잉

객체에 정의한 속성과 같은 이름의 속성이 프로토타입에도 있으면 어떻게 될까요?

```js
const myDate = new Date(1995, 11, 17);

console.log(myDate.getTime()); // 819129600000

myDate.getTime = function () {
  console.log("something else!");
};

myDate.getTime(); // 'something else!'
```

프로토타입 체인의 동작 방식을 생각하면 결과를 예측할 수 있습니다. `getTime`을 찾을 때 브라우저는 먼저 `myDate` 자신에서 그 이름의 속성을 찾고, 거기서 찾으면 프로토타입은 확인하지 않습니다. 이처럼 객체 자신의 속성이 프로토타입의 속성을 가리는 것을 속성 **섀도잉(shadowing)** 이라고 합니다.

## 프로토타입 설정하기

JavaScript에서 객체의 프로토타입을 설정하는 방법은 여러 가지가 있습니다. 여기서는 `Object.create()`와 생성자, 두 가지를 살펴봅니다.

### Object.create 사용하기

{{jsxref("Object.create()")}} 메서드는 새 객체를 만들면서 그 객체의 프로토타입으로 사용할 객체를 지정할 수 있게 해 줍니다.

```js
const personPrototype = {
  greet() {
    console.log("hello!");
  },
};

const carl = Object.create(personPrototype);
carl.greet(); // hello!
```

`personPrototype`을 프로토타입으로 하는 `carl` 객체를 만들었기 때문에 `carl`에서 `greet()`을 호출할 수 있습니다.

### 생성자 사용하기

JavaScript에서 모든 함수에는 `prototype`이라는 속성이 있습니다. 함수를 생성자로 호출하면, 이 속성에 지정된 객체가 새로 만들어진 객체의 프로토타입이 됩니다(관례상 이 속성은 `__proto__`라는 이름으로 노출됩니다).

따라서 생성자의 `prototype`을 설정하면, 그 생성자로 만드는 모든 객체에 같은 프로토타입을 지정할 수 있습니다.

```js
const personPrototype = {
  greet() {
    console.log(`hello, my name is ${this.name}!`);
  },
};

function Person(name) {
  this.name = name;
}

Object.assign(Person.prototype, personPrototype);
// 또는
// Person.prototype.greet = personPrototype.greet;
```

위 코드는 다음과 같이 동작합니다.

- `greet()` 메서드를 가진 `personPrototype` 객체를 정의합니다.
- 생성할 사람의 이름을 초기화하는 `Person()` 생성자 함수를 정의합니다.
- {{jsxref("Object.assign()")}}을 사용해 `personPrototype`의 메서드를 `Person` 함수의 `prototype` 속성에 복사합니다.

이제 `Person()`으로 만든 객체는 `Person.prototype`을 프로토타입으로 갖게 되고, 그 안에 `greet` 메서드가 자동으로 포함됩니다.

```js
const reuben = new Person("Reuben");
reuben.greet(); // hello, my name is Reuben!
```

이 방식은 `Object.create()`로 프로토타입을 지정했을 때 `constructor` 속성이 사라지는 문제도 해결해 줍니다. `Person.prototype`에는 원래 `Person` 함수를 가리키는 `constructor` 속성이 있는데, `Object.assign()`은 이 속성을 덮어쓰지 않고 메서드만 추가하기 때문입니다.

### 자체 속성

위 `Person()` 생성자로 만든 객체에는 두 가지 속성이 있습니다.

- 생성자 안에서 설정한 `name` 속성은 `Person` 객체 자신에 있습니다.
- `greet()` 메서드는 프로토타입에 있습니다.

메서드는 프로토타입에 한 번만 정의하고 데이터 속성은 생성자 안에서 정의하는 패턴은 흔히 사용됩니다. 메서드는 보통 모든 객체에서 같지만, 데이터 속성은 객체마다 서로 다른 값을 갖기 때문입니다.

`name`처럼 객체에 직접 정의된 속성을 **자체 속성(own property)** 이라고 하며, 정적 메서드 {{jsxref("Object.hasOwn()")}}으로 자체 속성인지 확인할 수 있습니다.

```js
const irma = new Person("Irma");

console.log(Object.hasOwn(irma, "name")); // true
console.log(Object.hasOwn(irma, "greet")); // false
```

> [!NOTE]
> 정적이 아닌 메서드인 {{jsxref("Object.prototype.hasOwnProperty()")}}도 사용할 수 있지만, 가능하면 `Object.hasOwn()`을 사용할 것을 권장합니다.

## 프로토타입과 상속

프로토타입은 JavaScript의 강력하고 유연한 기능으로, 코드를 재사용하고 객체를 조합할 수 있게 해 줍니다. 특히 일종의 **상속(inheritance)** 을 지원합니다. 상속은 객체 지향 프로그래밍 언어의 기능으로, 프로그래머가 "시스템의 어떤 객체는 다른 객체를 더 특수화한 버전이다"라는 개념을 표현할 수 있게 해 줍니다.

예를 들어 학교를 모델링한다면 *교수*와 *학생*이 있을 수 있습니다. 둘 다 *사람*이므로 이름이 있고 인사를 할 수 있다는 공통점이 있지만, 각자 고유한 기능도 추가로 가질 수 있습니다. 이때 공통 기능은 `Person`의 프로토타입에 두고, `Professor`와 `Student` 객체는 `Person`을 프로토타입으로 삼아 필요한 기능만 추가하면 됩니다.

다음 글에서는 상속을 비롯한 객체 지향 프로그래밍의 핵심 개념을 소개하고, JavaScript가 이를 어떻게 지원하는지 살펴봅니다.

## 요약

이 문서에서는 프로토타입 체인으로 객체가 다른 객체의 기능을 상속받는 방식과 속성 섀도잉, `Object.create()`와 생성자의 `prototype` 속성으로 프로토타입을 설정하는 방법, 자체 속성을 확인하는 방법을 살펴보았습니다.

{{PreviousMenuNext("Learn/JavaScript/Objects/Basics", "Learn/JavaScript/Objects/Object-oriented_programming", "Learn/JavaScript/Objects")}}
