# JavaScript modules

**JavaScript modules** let you split code into separate files, each with its own scope, and state explicitly which values it shares with other files. Modules were introduced in ECMAScript 2015 (ES6) and are supported natively by all modern browsers and by Node.js.

Before modules, developers relied on global variables, carefully ordered `<script>` tags, and patterns such as immediately invoked function expressions (IIFEs) to avoid naming collisions. Modules replace these techniques with the declarative `import` and `export` statements.

A file is treated as a module when it is loaded as one (for example, with `<script type="module">`) or when it is used by an `import` statement. Module code runs in strict mode, and its top-level declarations do not become properties of the global object.

## Syntax

```js
// Named imports
import { name1, name2 as alias } from "module-name";

// Default import
import defaultExport from "module-name";

// Namespace import
import * as name from "module-name";

// Side-effect import (runs the module, imports nothing)
import "module-name";

// Named exports
export const name1 = 1;
export { name2, name3 };

// Default export
export default expression;

// Re-export everything from another module
export * from "module-name";
```

## Description

### Named and default exports

A module can have any number of named exports and at most one default export. Named exports must be imported using their exact names, enclosed in braces. The default export can be imported under any name.

```js
// math.js
export const PI = 3.14159;

export function square(x) {
  return x * x;
}

export default function add(a, b) {
  return a + b;
}
```

```js
// main.js
import add, { PI, square } from "./math.js";

console.log(add(2, 3)); // 5
console.log(square(PI)); // 9.8696...
```

### Live bindings

Imports are live views of the exported values, not copies. If the exporting module changes an exported variable, importing modules see the new value the next time they read it. Importers cannot assign to an imported binding; doing so throws a `TypeError`.

### Module scripts in HTML

To load a module in a web page, add `type="module"` to a `<script>` element:

```html
<script type="module" src="main.js"></script>
```

Module scripts differ from classic scripts in several ways:

- **They are deferred by default.** They execute after the document has been parsed, in document order, just like a `defer` script.
- **They always run in strict mode.**
- **Their top-level `this` is `undefined`** rather than the global object.
- **They have their own scope.** Top-level variables are not shared through the global scope.
- **Cross-origin modules require CORS.** The server must send appropriate `Access-Control-Allow-Origin` headers.
- **Specifiers must be URLs or start with `/`, `./`, or `../`.** A bare specifier such as `"lodash"` fails unless an import map resolves it.

The `nomodule` attribute can be used on a classic script to provide a fallback for browsers that do not support modules. Those browsers ignore module scripts and run the `nomodule` script instead, while modern browsers ignore the `nomodule` script.

### Dynamic imports

The `import()` expression loads a module at runtime and returns a promise that resolves to the module's namespace object. Unlike static imports, it can be called from anywhere, including classic scripts and conditional code. This makes it useful for code splitting and lazy loading.

```js
button.addEventListener("click", async () => {
  const { renderChart } = await import("./chart.js");
  renderChart(data);
});
```

### Top-level await

In a module, you can use `await` outside of any function. Evaluation of the module, and of any module that imports it, waits until the awaited promise settles.

```js
const response = await fetch("/api/config.json");
export const config = await response.json();
```

### The `import.meta` object

`import.meta` exposes metadata about the current module. Its most common property is `import.meta.url`, which gives the URL the module was loaded from.

### Import maps

An import map is a JSON object, placed in a `<script type="importmap">` element, that maps bare module specifiers to URLs:

```html
<script type="importmap">
{
  "imports": {
    "lodash": "/node_modules/lodash-es/lodash.js"
  }
}
</script>
```

After this map is defined, `import _ from "lodash";` resolves to the given URL.

### Evaluation and caching

Each module is evaluated at most once per document. Every later import of the same module receives the same instance. Before evaluation begins, the browser fetches and parses the entire dependency graph. Circular dependencies are allowed, but a binding accessed before its module has initialized throws a `ReferenceError`.

## Examples

### A small application

The following files show a typical split between a utility module and an entry point:

```js
// utils/format.js
export function formatPrice(amount, currency = "USD") {
  return new Intl.NumberFormat("en-US", { style: "currency", currency }).format(amount);
}
```

```js
// app.js
import { formatPrice } from "./utils/format.js";

const total = 42.5;
document.querySelector("#total").textContent = formatPrice(total);
```

```html
<!-- index.html -->
<p>Total: <span id="total"></span></p>
<script type="module" src="app.js"></script>
```

## Specifications

- [ECMAScript Language Specification: Modules](https://tc39.es/ecma262/#sec-modules)
- [HTML Standard: The script element](https://html.spec.whatwg.org/multipage/scripting.html#the-script-element)

## See also

- [`import`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/import) and [`export`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/export) statement references
- [`import()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/import) operator
- [`import.meta`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/import.meta)
- [Import maps](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/script/type/importmap)

---

I couldn't save this as a `.md` file because the file-writing tool is disabled in this session, so the page is above in full. Copy it into a `.md` file as-is. The body is about 900 words, excluding code samples.
