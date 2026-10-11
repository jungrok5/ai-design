# Standard built-in objects

This chapter documents all of JavaScript's standard, built-in objects, including their methods and properties.

The term "global objects" (or standard built-in objects) here is not to be confused with the **global object**. Here, "global objects" refers to _objects in the global scope_. The **global object** itself can be accessed using the {{jsxref("globalThis")}} property.

## Standard objects by category

### Value properties

These global properties return a simple value. They have no properties or methods.

- {{jsxref("globalThis")}}
- {{jsxref("Infinity")}}
- {{jsxref("NaN")}}
- {{jsxref("undefined")}}

### Function properties

These global functions return a result directly to the caller.

- {{jsxref("eval()")}}
- {{jsxref("isFinite()")}}
- {{jsxref("isNaN()")}}
- {{jsxref("parseFloat()")}}
- {{jsxref("parseInt()")}}
- {{jsxref("decodeURI()")}}
- {{jsxref("decodeURIComponent()")}}
- {{jsxref("encodeURI()")}}
- {{jsxref("encodeURIComponent()")}}

### Fundamental objects

These are the fundamental objects on which all other objects are based. This includes objects that represent general objects, functions, and errors.

- {{jsxref("Object")}}
- {{jsxref("Function")}}
- {{jsxref("Boolean")}}
- {{jsxref("Symbol")}}
- {{jsxref("Error")}}
  - {{jsxref("EvalError")}}
  - {{jsxref("RangeError")}}
  - {{jsxref("ReferenceError")}}
  - {{jsxref("SyntaxError")}}
  - {{jsxref("TypeError")}}
  - {{jsxref("URIError")}}

### Numbers and dates

These are the base objects representing numbers, dates, and mathematical calculations.

- {{jsxref("Number")}}
- {{jsxref("BigInt")}}
- {{jsxref("Math")}}
- {{jsxref("Date")}}

### Text processing

These objects represent strings and support manipulating them.

- {{jsxref("String")}}
- {{jsxref("RegExp")}}

### Indexed collections

These objects represent collections of data which are ordered by an index value. This includes (typed) arrays and array-like constructs.

- {{jsxref("Array")}}
- {{jsxref("Int8Array")}}
- {{jsxref("Uint8Array")}}
- {{jsxref("Uint8ClampedArray")}}
- {{jsxref("Int16Array")}}
- {{jsxref("Uint16Array")}}
- {{jsxref("Int32Array")}}
- {{jsxref("Uint32Array")}}
- {{jsxref("Float32Array")}}
- {{jsxref("Float64Array")}}
- {{jsxref("BigInt64Array")}}
- {{jsxref("BigUint64Array")}}

### Keyed collections

These objects represent collections which use keys. The iterable collections ({{jsxref("Map")}} and {{jsxref("Set")}}) contain elements which are easily iterated in the order of insertion.

- {{jsxref("Map")}}
- {{jsxref("Set")}}
- {{jsxref("WeakMap")}}
- {{jsxref("WeakSet")}}

### Structured data

These objects represent and interact with structured data buffers and data coded using JavaScript Object Notation (JSON).

- {{jsxref("ArrayBuffer")}}
- {{jsxref("SharedArrayBuffer")}}
- {{jsxref("DataView")}}
- {{jsxref("Atomics")}}
- {{jsxref("JSON")}}

### Managing memory

These objects interact with the garbage collection mechanism.

- {{jsxref("WeakRef")}}
- {{jsxref("FinalizationRegistry")}}

### Control abstraction objects

Control abstractions can help to structure code, especially async code without using deeply nested callbacks, for example.

- {{jsxref("Iterator")}}
- {{jsxref("Promise")}}
- {{jsxref("GeneratorFunction")}}
- {{jsxref("AsyncGeneratorFunction")}}
- {{jsxref("Generator")}}
- {{jsxref("AsyncGenerator")}}
- {{jsxref("AsyncFunction")}}

### Reflection

- {{jsxref("Reflect")}}
- {{jsxref("Proxy")}}

### Internationalization

Additions to the ECMAScript core for language-sensitive functionalities.

- {{jsxref("Intl")}}
- {{jsxref("Intl.Collator")}}
- {{jsxref("Intl.DateTimeFormat")}}
- {{jsxref("Intl.NumberFormat")}}
- {{jsxref("Intl.PluralRules")}}

## Specifications

| Specification                                                    |
| ---------------------------------------------------------------- |
| [ECMAScript® Language Specification](https://tc39.es/ecma262/)   |

## See also

- [JavaScript reference](/en-US/docs/Web/JavaScript/Reference)
- [Standard built-in objects overview](/en-US/docs/Web/JavaScript/Reference/Global_Objects)
