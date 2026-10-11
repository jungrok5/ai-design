I couldn't save a file because the Write tool is disabled in this session, so the page is below.

# Arrays

The **`Array`** object is a global object used to construct arrays, which are high-level, list-like objects. An array is an ordered collection of values, each identified by a numeric index. JavaScript arrays are zero-indexed, resizable, and can hold values of any type, including numbers, strings, objects, functions, and other arrays, all within the same collection.

## Description

Arrays are JavaScript objects whose elements are stored under integer-like property keys. They also have a special `length` property that updates automatically as elements are added or removed. Unlike arrays in many lower-level languages, JavaScript arrays do not require every element to share one type, and their elements are not guaranteed to occupy contiguous memory. Engines may optimize storage internally, for example by storing arrays that contain only small integers in a compact form.

Because arrays are objects, the `typeof` operator returns `"object"` for them. To check whether a value is an array, use `Array.isArray()`:

```js
Array.isArray([1, 2, 3]); // true
typeof [1, 2, 3]; // "object"
```

## Creating arrays

The most common way to create an array is with an array literal, a comma-separated list of values inside square brackets:

```js
const fruits = ["apple", "banana", "cherry"];
const empty = [];
```

The `Array()` constructor also works, but its behavior depends on the number of arguments. A single numeric argument sets the length of the new array instead of creating an element:

```js
const threeEmpty = new Array(3); // length 3, no values
const seven = Array.of(7); // [7]
```

For this reason, `Array.of()` is preferred when you want an array from numeric arguments. To create an array from an iterable or array-like object, use `Array.from()`, optionally with a mapping function:

```js
Array.from("abc"); // ["a", "b", "c"]
Array.from({ length: 4 }, (_, i) => i * 2); // [0, 2, 4, 6]
```

## Accessing and changing elements

Elements are read and written with bracket notation using their index, which starts at `0`. Reading an index that does not exist returns `undefined` rather than throwing an error:

```js
const colors = ["red", "green", "blue"];
colors[0]; // "red"
colors[5]; // undefined
colors[1] = "yellow"; // replaces "green"
```

The `at()` method accepts negative indexes, which count from the end. `colors.at(-1)` returns `"blue"`.

The `length` property is always one greater than the highest index. Setting it to a smaller value removes the elements beyond the new length:

```js
const numbers = [1, 2, 3, 4, 5];
numbers.length = 2; // numbers is now [1, 2]
```

## Iterating over arrays

The most direct way to visit every element is a `for...of` loop, which iterates over the values:

```js
for (const color of colors) {
  console.log(color);
}
```

When you also need the index, use a classic `for` loop or `forEach()`. Avoid `for...in` on arrays. It iterates over all enumerable property keys, including any added to the object, and it yields keys as strings.

## Common array methods

Some array methods **mutate** the array they are called on. Others return a new array and leave the original unchanged.

Mutating methods include:

- `push()` and `pop()`, which add and remove elements at the end.
- `unshift()` and `shift()`, which add and remove elements at the start.
- `splice()`, which inserts or removes elements at any position.
- `sort()`, `reverse()`, and `fill()`.

Non-mutating methods include:

- `map()`, which transforms each element.
- `filter()`, which keeps elements that pass a test.
- `slice()`, which extracts a portion of the array.
- `concat()`, which joins arrays together.
- `flat()` and `flatMap()`, which flatten nested arrays.
- `toSorted()`, `toReversed()`, and `toSpliced()`, which are non-mutating versions of `sort()`, `reverse()`, and `splice()`.

Searching and testing methods include `indexOf()`, `includes()`, `find()`, `findIndex()`, `some()`, and `every()`. To combine all elements into one value, use `reduce()`:

```js
const prices = [12, 7, 30];
const total = prices.reduce((sum, price) => sum + price, 0); // 49

const expensive = prices.filter((price) => price > 10); // [12, 30]
const doubled = prices.map((price) => price * 2); // [24, 14, 60]
```

## Sorting

By default, `sort()` converts elements to strings and compares them by UTF-16 code units, so numbers are not sorted numerically. Pass a comparison function to sort numbers correctly:

```js
const scores = [10, 9, 100];
scores.sort(); // [10, 100, 9]
scores.sort((a, b) => a - b); // [9, 10, 100]
```

## Copying arrays

Assigning an array to another variable copies only the reference, so both variables point to the same array. To create an independent shallow copy, use spread syntax, `slice()`, or `Array.from()`:

```js
const original = [1, 2, 3];
const alias = original; // same array
const copy = [...original]; // new array

alias.push(4); // original is now [1, 2, 3, 4]
copy; // [1, 2, 3]
```

A shallow copy duplicates only the top-level elements. If an element is an object or array, both copies refer to the same nested value.

## Sparse arrays

An array has empty slots when its length is larger than the number of values it holds. Empty slots appear with `new Array(n)`, when you assign to an index past the end, or when you delete an element with the `delete` operator. Methods such as `forEach()` and `map()` skip empty slots, while `for...of` and `Array.from()` treat them as `undefined`.

```js
const sparse = [1, , 3]; // length 3, index 1 is empty
sparse.forEach((value) => console.log(value)); // logs 1 and 3
```

Avoid creating sparse arrays on purpose. Their behavior is harder to predict, and engines may store them less efficiently.

## Specifications

- ECMAScript Language Specification, section on Array objects

## See also

- `Array` reference on MDN
- Indexed collections guide
- `Array.prototype.map()`
- `Array.prototype.filter()`
- `Array.prototype.reduce()`
- `Array.prototype.sort()`
