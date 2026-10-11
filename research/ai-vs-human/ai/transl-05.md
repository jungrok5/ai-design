# Array[Symbol.species]

`Array[Symbol.species]`는 배열 메서드가 파생 배열을 만들 때 사용할 생성자 함수를 반환하는 정적 접근자(getter) 속성입니다. 기본적으로 `this`를 반환하므로, `Array`를 상속한 클래스에서는 그 하위 클래스가 반환됩니다.

## 구문

```js
Array[Symbol.species]
```

## 반환 값

배열을 생성할 때 사용되는 생성자입니다. 기본값은 호출된 생성자 자신(`this`)입니다.

## 설명

`Symbol.species`는 파생 객체를 만들 때 사용할 생성자를 지정하는 잘 알려진 심볼(well-known symbol)입니다. `Array[Symbol.species]`는 다음 메서드가 결과 배열을 만들 때 참조합니다.

- `concat()`
- `filter()`
- `flat()`
- `flatMap()`
- `map()`
- `slice()`
- `splice()`

`Array.from()`과 `Array.of()`는 species를 참조하지 않고 `this` 값을 직접 사용하므로 이 속성의 영향을 받지 않습니다.

이 속성에는 setter가 없어 값을 직접 바꿀 수 없지만, 하위 클래스에서 getter를 재정의하여 동작을 바꿀 수 있습니다. 재정의한 값이 `undefined`나 `null`이면 기본값인 `Array`가 사용됩니다.

## 예제

### 기본 동작

```js
class MyArray extends Array {}

const a = new MyArray(1, 2, 3);
const b = a.map((x) => x * 2);

console.log(b instanceof MyArray); // true
console.log(b instanceof Array);   // true
```

### 파생 배열을 일반 Array로 만들기

```js
class MyArray extends Array {
  static get [Symbol.species]() {
    return Array;
  }
}

const a = new MyArray(1, 2, 3);
const b = a.filter((x) => x > 1);

console.log(b instanceof MyArray); // false
console.log(b instanceof Array);   // true
```

---

*MDN 웹 문서의 내용을 바탕으로 한국어로 정리한 글이며, 원문을 그대로 번역한 것은 아닙니다.*
