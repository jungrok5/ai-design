---
title: Functions
slug: Web/JavaScript/Guide/Functions
page-type: guide
---

{{jsSidebar("JavaScript Guide")}}

Functions are one of the fundamental building blocks in JavaScript. A function is a reusable set of statements that performs a task or calculates a value. To use a function, you must define it somewhere in the scope from which you wish to call it.

This guide covers how to define functions, call them, and pass data in and out of them.

## Defining functions

### Function declarations

A **function declaration** (also called a function statement) consists of the `function` keyword, followed by:

- The name of the function.
- A list of parameters, enclosed in parentheses and separated by commas.
- The statements that make up the function, enclosed in curly braces.

```js
function square(number) {
  return number * number;
}
```

The function `square` takes one parameter, called `number`. The `return` statement specifies the value the function gives back to its caller.

Function declarations are _hoisted_. You can call a declared function before the line where it appears in your code:

```js
console.log(square(5)); // 25

function square(number) {
  return number * number;
}
```

### Function expressions

A function can also be created by a **function expression**. The function may be anonymous, which means it has no name:

```js
const square = function (number) {
  return number * number;
};

console.log(square(4)); // 16
```

A function expression can also have a name. The name is local to the function body and is useful for recursion and for stack traces:

```js
const factorial = function fac(n) {
  return n < 2 ? 1 : n * fac(n - 1);
};

console.log(factorial(3)); // 6
```

Unlike declarations, function expressions are not hoisted. Calling `square` before its assignment throws a {{jsxref("ReferenceError")}}.

### Arrow functions

An **arrow function expression** has a shorter syntax than a regular function expression. It does not have its own bindings to `this`, `arguments`, or `super`.

```js
const square = (number) => number * number;

const add = (a, b) => {
  const sum = a + b;
  return sum;
};
```

When the body is a single expression, the braces and the `return` keyword can be omitted, and the value of the expression is returned implicitly. Arrow functions are well suited to short callbacks:

```js
const numbers = [1, 2, 3];
const doubled = numbers.map((n) => n * 2);
console.log(doubled); // [2, 4, 6]
```

## Calling functions

Defining a function does not run it. You _call_ the function by using its name followed by parentheses that contain the arguments:

```js
square(5);
```

The values you pass are called **arguments**. The names listed in the definition are called **parameters**. Arguments are matched to parameters by position.

A function is also run when it is used as an event handler, passed to a method such as {{domxref("Window.setTimeout", "setTimeout()")}}, or invoked through methods like `call()` and `apply()`.

## Parameters

### Default parameters

If an argument is omitted or `undefined`, the parameter takes its default value:

```js
function greet(name = "stranger") {
  return `Hello, ${name}!`;
}

console.log(greet()); // "Hello, stranger!"
console.log(greet("Ada")); // "Hello, Ada!"
```

Default values are evaluated each time the function is called, so they may use earlier parameters or call other functions.

### Rest parameters

The **rest parameter** syntax collects any number of remaining arguments into a real array:

```js
function sum(...values) {
  return values.reduce((total, value) => total + value, 0);
}

console.log(sum(1, 2, 3, 4)); // 10
```

The rest parameter must be the last one in the list.

### Passing values

Primitive values (such as numbers and strings) are passed by value. Changing the parameter inside the function has no effect outside it. Objects are passed as a reference to the same object. If the function changes a property of that object, the change is visible to the caller:

```js
function rename(person) {
  person.name = "Grace";
}

const user = { name: "Ada" };
rename(user);
console.log(user.name); // "Grace"
```

Reassigning the parameter itself, as in `person = {}`, does not affect the caller's variable.

## Return values

A function returns `undefined` unless a `return` statement specifies another value. A `return` ends the function immediately, so code after it does not run.

To return several values, return an array or an object and use destructuring:

```js
function minMax(list) {
  return { min: Math.min(...list), max: Math.max(...list) };
}

const { min, max } = minMax([3, 1, 4]);
```

## Function scope and closures

Variables declared inside a function are not accessible from outside it. A function can, however, access the variables of the scope in which it was defined. When an inner function keeps access to those variables after the outer function has finished, it forms a **closure**:

```js
function makeCounter() {
  let count = 0;
  return function () {
    count += 1;
    return count;
  };
}

const counter = makeCounter();
console.log(counter()); // 1
console.log(counter()); // 2
```

Each call to `makeCounter()` creates a new, private `count` variable. Closures are the basis for data privacy, callbacks, and many patterns in modern JavaScript. See [Closures](/en-US/docs/Web/JavaScript/Closures) for more detail.

## Functions are values

In JavaScript, functions are _first-class_: they are objects that can be assigned to variables, stored in data structures, passed as arguments, and returned from other functions. A function that accepts or returns another function is called a **higher-order function**.

```js
function applyTwice(fn, value) {
  return fn(fn(value));
}

console.log(applyTwice((n) => n + 3, 10)); // 16
```

Because functions are objects, they have properties and methods. For example, the `name` property holds the function's name, and `length` holds the number of declared parameters.

## Immediately invoked function expressions

An **immediately invoked function expression** (IIFE) is defined and called in one step. It was commonly used to create a private scope before modules existed:

```js
(function () {
  const secret = "hidden";
  console.log(secret);
})();
```

## The `this` keyword

Inside a regular function, the value of `this` depends on how the function is called. For a method call such as `obj.method()`, `this` is `obj`. Arrow functions instead inherit `this` from the surrounding scope, which makes them convenient inside methods that use callbacks. You can set `this` explicitly with {{jsxref("Function.prototype.call()", "call()")}}, {{jsxref("Function.prototype.apply()", "apply()")}}, or {{jsxref("Function.prototype.bind()", "bind()")}}.

## See also

- [Functions](/en-US/docs/Web/JavaScript/Reference/Functions) reference
- {{jsxref("Function")}}
- [Arrow function expressions](/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions)
- [Default parameters](/en-US/docs/Web/JavaScript/Reference/Functions/Default_parameters)
- [Rest parameters](/en-US/docs/Web/JavaScript/Reference/Functions/rest_parameters)
- [Closures](/en-US/docs/Web/JavaScript/Closures)
