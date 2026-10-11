---
title: Advanced JavaScript objects
slug: Learn/JavaScript/Objects/Advanced_objects
page-type: learn-module-chapter
---

{{LearnSidebar}}

This article looks at features that give you finer control over objects: property descriptors, getters and setters, and the prototype chain. Once you understand them, you can design objects that protect their data and share behavior efficiently.

## Prerequisites

You should already know how to create objects with literals and how to access their properties using dot and bracket notation.

## Property descriptors

Every property has a set of attributes that describe how it behaves. You can read them with {{jsxref("Object.getOwnPropertyDescriptor()")}} and set them with {{jsxref("Object.defineProperty()")}}.

```js
const book = { title: "Dune" };

Object.defineProperty(book, "isbn", {
  value: "978-0441013593",
  writable: false,
  enumerable: true,
  configurable: false,
});

book.isbn = "000"; // silently ignored (throws in strict mode)
console.log(book.isbn); // "978-0441013593"
```

The three main attributes are:

- `writable`: whether the value can be changed.
- `enumerable`: whether the property appears in `for...in` loops and {{jsxref("Object.keys()")}}.
- `configurable`: whether the property can be deleted or its attributes changed.

Properties you create with assignment have all three set to `true`. Properties you create with `defineProperty()` default to `false`.

## Getters and setters

Accessor properties run a function when you read or write them. They look like ordinary properties to the code that uses them.

```js
const user = {
  first: "Ada",
  last: "Lovelace",
  get fullName() {
    return `${this.first} ${this.last}`;
  },
  set fullName(value) {
    [this.first, this.last] = value.split(" ");
  },
};

console.log(user.fullName); // "Ada Lovelace"
user.fullName = "Grace Hopper";
console.log(user.first); // "Grace"
```

Use accessors to validate input, compute values on demand, or keep related properties in sync.

## The prototype chain

When you access a property, JavaScript looks for it on the object first. If it isn't found, the engine follows the object's internal prototype and keeps going until it finds the property or reaches `null`. This sequence of objects is the **prototype chain**.

```js
const animal = {
  speak() {
    return `${this.name} makes a sound.`;
  },
};

const dog = Object.create(animal);
dog.name = "Rex";

console.log(dog.speak()); // "Rex makes a sound."
console.log(Object.getPrototypeOf(dog) === animal); // true
```

Here `dog` has no `speak()` method of its own, so JavaScript finds it on `animal`. Methods defined on a prototype are shared by every object that inherits from it, which saves memory.

Use {{jsxref("Object.hasOwn()")}} to check whether a property belongs to the object itself rather than to its prototype chain.

## Preventing changes to an object

JavaScript provides three levels of protection:

| Method | Add properties | Delete properties | Change values |
| ------ | :------------: | :---------------: | :-----------: |
| {{jsxref("Object.preventExtensions()")}} | No | Yes | Yes |
| {{jsxref("Object.seal()")}} | No | No | Yes |
| {{jsxref("Object.freeze()")}} | No | No | No |

Note that `freeze()` is shallow. Nested objects remain mutable unless you freeze them too.

## See also

- {{jsxref("Object.defineProperties()")}}
- [Inheritance and the prototype chain](/en-US/docs/Web/JavaScript/Inheritance_and_the_prototype_chain)
- [Working with objects](/en-US/docs/Web/JavaScript/Guide/Working_with_objects)
