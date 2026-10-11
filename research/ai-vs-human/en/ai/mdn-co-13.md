# Function return values

**Summary:** The `return` statement ends the execution of a function and specifies the value the function passes back to its caller. This guide explains how return values work in JavaScript, including the default `undefined` value, common pitfalls, and patterns for returning more than one value.

## Syntax

```js
return;
return expression;
```

- `return;` ends the function and returns `undefined`.
- `return expression;` evaluates `expression`, ends the function, and returns the resulting value.

## Description

When a function is called, its body runs from top to bottom until it reaches a `return` statement or the end of the body. The value of the call expression is whatever the function returns. If the function does not reach a `return` statement, the call evaluates to `undefined`.

```js
function add(a, b) {
  return a + b;
}

const sum = add(2, 3); // 5
```

A `return` statement stops the function immediately. Any code after it in the same block does not run:

```js
function firstNegative(numbers) {
  for (const n of numbers) {
    if (n < 0) {
      return n; // Exits the function and the loop here
    }
  }
  return null; // Reached only if no negative number was found
}

firstNegative([3, -1, -7]); // -1
firstNegative([1, 2]); // null
```

### Functions without a return value

A function that has no `return` statement, or has a bare `return;`, returns `undefined`. This is common for functions that perform side effects, such as updating the DOM or writing to a log:

```js
function logMessage(message) {
  console.log(message);
}

const result = logMessage("Hello"); // Logs "Hello"
console.log(result); // undefined
```

### Any value can be returned

The `return` statement can pass back any JavaScript value: a primitive, an object, an array, a function, or a promise.

```js
function makeUser(name) {
  return { name, createdAt: Date.now() };
}

function makeCounter() {
  let count = 0;
  return () => ++count;
}
```

### Automatic semicolon insertion

JavaScript inserts a semicolon after a `return` keyword that is followed by a line break. The function then returns `undefined`, and the expression on the next line is never evaluated. This is one of the most common sources of bugs with return values:

```js
function getConfig() {
  return
  {
    debug: true,
  };
}

getConfig(); // undefined, not the object
```

To avoid this, start the returned expression on the same line as `return`, or wrap a multi-line value in parentheses:

```js
function getConfig() {
  return {
    debug: true,
  };
}
```

### Returning from arrow functions

An arrow function with an expression body returns that expression implicitly. To return an object literal this way, wrap it in parentheses. Otherwise the braces are parsed as a function body:

```js
const makePoint = (x, y) => ({ x, y });

const broken = (x, y) => { x, y }; // Syntax error: a block with labels, not an object
```

### Return values in special contexts

- **`finally` blocks:** A `return` inside a `finally` block overrides any value returned from the `try` or `catch` blocks.

  ```js
  function test() {
    try {
      return "try";
    } finally {
      return "finally";
    }
  }

  test(); // "finally"
  ```

- **Async functions:** An `async` function always returns a promise. A `return` value is used to resolve that promise, and a thrown error rejects it:

  ```js
  async function fetchUserName(id) {
    const response = await fetch(`/api/users/${id}`);
    const data = await response.json();
    return data.name; // The promise resolves with this string
  }
  ```

- **Generator functions:** A `return` statement in a generator sets the `value` of the final `{ done: true }` result. It does not appear in iteration with `for...of`.

- **Constructors:** When a function is called with `new`, it returns the newly created object by default. If the constructor returns an object, that object replaces the new instance. If it returns a primitive, the primitive is ignored.

## Returning multiple values

JavaScript functions return a single value, but that value can be an array or an object. Destructuring assignment makes it easy to unpack the result:

```js
function getMinMax(numbers) {
  return [Math.min(...numbers), Math.max(...numbers)];
}

const [min, max] = getMinMax([4, 9, 1, 7]);
console.log(min, max); // 1 9
```

Use an object when the values have names. This keeps the call site readable and lets callers pick only the properties they need:

```js
function parseDate(text) {
  const [year, month, day] = text.split("-").map(Number);
  return { year, month, day };
}

const { year, month } = parseDate("2026-10-11");
```

## Examples

### Returning early to handle invalid input

Guard clauses that return early keep the main logic at the top level of the function:

```js
function divide(a, b) {
  if (b === 0) {
    return NaN;
  }
  return a / b;
}
```

### Returning a function

Returning a function lets you create configured behavior:

```js
function multiplyBy(factor) {
  return (value) => value * factor;
}

const double = multiplyBy(2);
double(21); // 42
```

## Best practices

- Return a value of a consistent type. A function that sometimes returns a number and sometimes `null` or `undefined` is harder to use correctly.
- Use `return;` only when you intend to stop early. If a function never returns a meaningful value, do not add `return` statements that return `undefined` without reason.
- Name functions that return values after what they return or compute, such as `getUser` or `calculateTotal`, and name functions that only perform actions after the action, such as `saveUser` or `logError`.
- Avoid relying on `undefined` as a signal for failure when `null` or an error would be clearer.

## See also

- [`return`](/en-US/docs/Web/JavaScript/Reference/Statements/return) statement reference
- [Functions](/en-US/docs/Web/JavaScript/Guide/Functions) guide
- [Arrow functions](/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions)
- [Destructuring assignment](/en-US/docs/Web/JavaScript/Reference/Operators/Destructuring_assignment)
- [Async functions](/en-US/docs/Web/JavaScript/Reference/Statements/async_function)
