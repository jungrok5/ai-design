# Array.prototype.indexOf()

**`indexOf()`** 메서드는 배열에서 주어진 요소가 처음 나타나는 인덱스를 반환합니다. 해당 요소가 없으면 `-1`을 반환합니다.

## 구문

```js
indexOf(searchElement)
indexOf(searchElement, fromIndex)
```

## 매개변수

- `searchElement`: 배열에서 찾으려는 요소입니다.
- `fromIndex` (선택): 검색을 시작할 인덱스입니다. 기본값은 `0`입니다.
  - 값이 음수이면 배열 끝에서부터의 오프셋으로 취급합니다. 이때도 검색은 배열의 앞쪽 방향으로 진행합니다.
  - 값이 배열 길이보다 크거나 같으면 검색하지 않고 `-1`을 반환합니다.

## 반환 값

`searchElement`가 처음 발견된 인덱스를 반환합니다. 일치하는 요소가 없으면 `-1`을 반환합니다.

## 설명

`indexOf()`는 `fromIndex`부터 배열 끝까지 순서대로 각 요소를 검사합니다. 비교에는 엄격한 동등 연산자(`===`)를 사용하므로 타입이 다르면 같은 값으로 보지 않습니다. 예를 들어 숫자 `1`과 문자열 `'1'`은 서로 다른 값입니다.

객체는 내용이 같아도 참조가 다르면 일치하지 않습니다. 같은 객체를 가리키는 참조를 넘겨야 찾을 수 있습니다.

`NaN`은 `===`로 비교할 수 없으므로 `indexOf()`로 찾을 수 없습니다. `NaN`을 찾으려면 `includes()`나 `findIndex()`를 사용하세요.

희소 배열(sparse array)에서는 비어 있는 슬롯을 건너뜁니다. 이 메서드는 원본 배열을 변경하지 않습니다.

## 예제

### 기본 사용

```js
const beasts = ['ant', 'bison', 'camel', 'duck', 'bison'];

console.log(beasts.indexOf('bison'));     // 1
console.log(beasts.indexOf('bison', 2));  // 4
console.log(beasts.indexOf('giraffe'));   // -1
```

### 음수 fromIndex

```js
const arr = [2, 5, 9, 2];

console.log(arr.indexOf(2, -1));  // 3  (인덱스 3부터 검색)
console.log(arr.indexOf(2, -3));  // 3  (인덱스 1부터 검색)
```

### 엄격 비교와 NaN

```js
console.log([1, 2, 3].indexOf('1'));  // -1 (타입이 달라 불일치)
console.log([NaN].indexOf(NaN));      // -1 (NaN은 자기 자신과 같지 않음)
```

### 요소 존재 여부 확인

```js
const fruits = ['apple', 'banana'];

if (fruits.indexOf('banana') !== -1) {
  console.log('바나나가 있습니다.');
}
```

ES2016 이후에는 `includes()`를 사용하면 `NaN`도 올바르게 찾을 수 있으므로, 단순히 존재 여부만 확인할 때는 `includes()`가 더 적합할 수 있습니다.

## 명세

- ECMAScript® 2026 Language Specification: Array.prototype.indexOf

## 브라우저 호환성

`indexOf()`는 ES5부터 정의된 메서드로, 현재 사용되는 모든 주요 브라우저와 Node.js에서 지원됩니다.
