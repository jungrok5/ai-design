```markdown
---
title: Array.prototype.reverse()
slug: Web/JavaScript/Reference/Global_Objects/Array/reverse
page-type: javascript-instance-method
browser-compat: javascript.builtins.Array.reverse
---

{{JSRef}}

The **`reverse()`** method of {{jsxref("Array")}} instances reverses an array _[in place](https://en.wikipedia.org/wiki/In-place_algorithm)_ and returns a reference to the same array. The first array element becomes the last, and the last array element becomes the first. In other words, the array's elements are now in the opposite order.

To reverse the elements of an array without changing the original array, use {{jsxref("Array/toReversed", "toReversed()")}}.

{{InteractiveExample("JavaScript Demo: Array.prototype.reverse()")}}

```js interactive-example
const array1 = ["one", "two", "three"];
console.log("array1:", array1);
// Expected output: "array1:" Array ["one", "two", "three"]

const reversed = array1.reverse();
console.log("reversed:", reversed);
// Expected output: "reversed:" Array ["three", "two", "one"]

// Careful: reverse is destructive -- it changes the original array.
console.log("array1:", array1);
// Expected output: "array1:" Array ["three", "two", "one"]
```

## Syntax

```js-nolint
reverse()
```

### Parameters

None.

### Return value

A reference to the original array, now reversed. The return value is the same object as the original array, so changing one also changes the other.

## Description

The `reverse()` method moves elements in the calling array object so that their order is reversed. It changes the array and returns a reference to it.

The `reverse()` method keeps empty slots. If the source array is [sparse](/en-US/docs/Web/JavaScript/Guide/Indexed_collections#sparse_arrays), the indices that empty slots move to are deleted, so they also become empty slots.

The `reverse()` method is [generic](/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array#generic_array_methods). It only expects the `this` value to have a `length` property and integer-keyed properties. Strings are also array-like, but this method can't be used on them, because strings are immutable.

## Examples

### Reversing the elements in an array

The following example creates an array `items` containing three elements, then reverses it. The call to `reverse()` returns a reference to the reversed array `items`.

```js
const items = [1, 2, 3];
console.log(items); // [1, 2, 3]

items.reverse();
console.log(items); // [3, 2, 1]
```

### The reverse() method returns the reference to the same array

The `reverse()` method returns a reference to the original array, so changing the returned array also changes the original array.

```js
const numbers = [3, 2, 4, 1, 5];
const reversed = numbers.reverse();
// numbers and reversed are both in reversed order [5, 1, 4, 2, 3]
reversed[0] = 5;
console.log(numbers[0]); // 5
```

If you want `reverse()` to leave the original array unchanged but still return a shallow-copied array, as other array methods do (for example, [`map()`](/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/map)), use {{jsxref("Array/toReversed", "toReversed()")}}. Or you can make a shallow copy before you call `reverse()`, using the [spread syntax](/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax) or [`Array.from()`](/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/from).

```js
const numbers = [3, 2, 4, 1, 5];
// [...numbers] creates a shallow copy, so reverse() does not mutate the original
const reverted = [...numbers].reverse();
reverted[0] = 5;
console.log(numbers[0]); // 3
```

### Using reverse() on sparse arrays

Sparse arrays stay sparse after you call `reverse()`.

```js
console.log([1, , 3].reverse()); // [3, empty, 1]
console.log([1, , 3, 4].reverse()); // [4, 3, empty, 1]
```

### Calling reverse() on non-array objects

The `reverse()` method reads the `length` property of `this`. It then visits each property that has an integer key between `0` and `length / 2`, and swaps the two matching indices at both ends. It [deletes](/en-US/docs/Web/JavaScript/Reference/Operators/delete) any destination property for which the source property did not exist.

```js
const arrayLike = {
  length: 3,
  unrelated: "foo",
  2: 4,
  3: 33, // ignored by reverse() since length is 3
};
console.log(Array.prototype.reverse.call(arrayLike));
// { 0: 4, 3: 33, length: 3, unrelated: 'foo' }
// The index 2 is deleted because there was no index 0 present originally
// The index 3 is unchanged since the length is 3
```

## Specifications

{{Specifications}}

## Browser compatibility

{{Compat}}

## See also

- [Polyfill of `Array.prototype.reverse` in `core-js`](https://github.com/zloirock/core-js#ecmascript-array) with fixes of this method
- [Indexed collections](/en-US/docs/Web/JavaScript/Guide/Indexed_collections) guide
- {{jsxref("Array")}}
- {{jsxref("Array.prototype.join()")}}
- {{jsxref("Array.prototype.sort()")}}
- {{jsxref("Array.prototype.toReversed()")}}
- {{jsxref("TypedArray.prototype.reverse()")}}
```
