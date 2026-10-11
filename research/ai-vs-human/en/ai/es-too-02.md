# es-toolkit LLM coding agent instructions

This page tells LLM coding agents how to use **es-toolkit**, a modern JavaScript utility library, when generating or editing code. Follow these rules unless the user's project says otherwise.

## When to use es-toolkit

Prefer es-toolkit over hand-written helpers when the task involves arrays, objects, strings, promises, or function wrappers. Don't add it for one-line operations that native JavaScript already handles well, such as `array.map` or `Object.keys`.

Check `package.json` first. If `es-toolkit` is already a dependency, use it. If the project uses `lodash`, don't migrate it unless asked. If the user wants a drop-in replacement, use `es-toolkit/compat`.

## Installation

```bash
npm install es-toolkit
```

The package ships ESM and CommonJS builds with bundled TypeScript types. It also works in Deno and Bun, and in browsers through a bundler.

## Import rules

Always use named imports from the package root:

```ts
import { chunk, debounce, pick } from 'es-toolkit';
```

Never import from internal paths such as `es-toolkit/dist/...`. They are unstable. Supported entry points are:

| Entry point | Purpose |
| --- | --- |
| `es-toolkit` | Main, fully typed API |
| `es-toolkit/array` | Array functions only |
| `es-toolkit/object` | Object functions only |
| `es-toolkit/string` | String functions only |
| `es-toolkit/promise` | Async helpers |
| `es-toolkit/function` | Function wrappers |
| `es-toolkit/predicate` | Type guards and checks |
| `es-toolkit/compat` | Lodash-compatible behavior |

## Choosing between main and compat

The main entry point favors strict types and predictable behavior. It does **not** reproduce every Lodash quirk. For example, it won't accept `null` where the type signature forbids it, and it doesn't support deep-path strings on every function.

Use `es-toolkit/compat` only when you are migrating existing Lodash code and need identical edge-case behavior. Don't mix both entry points for the same function in one file.

## Commonly used functions

### Arrays

- `chunk(arr, size)` splits an array into groups of `size`.
- `uniq(arr)` removes duplicate primitives.
- `uniqBy(arr, mapper)` removes duplicates by a computed key.
- `groupBy(arr, getKey)` returns a record of arrays keyed by `getKey`.
- `difference(a, b)` returns items of `a` absent from `b`.
- `compact(arr)` removes falsy values.
- `zip(...arrays)` combines arrays element by element.

```ts
import { chunk, groupBy } from 'es-toolkit';

chunk([1, 2, 3, 4, 5], 2); // [[1, 2], [3, 4], [5]]
groupBy(users, (u) => u.role); // { admin: [...], member: [...] }
```

### Objects

- `pick(obj, keys)` and `omit(obj, keys)` select or exclude keys.
- `cloneDeep(value)` deep-copies plain data.
- `merge(target, source)` merges recursively and mutates `target`.
- `mapValues(obj, fn)` and `mapKeys(obj, fn)` transform values or keys.
- `invert(obj)` swaps keys and values.

### Strings

- `camelCase`, `snakeCase`, `kebabCase`, and `pascalCase` convert case styles.
- `capitalize(str)` uppercases the first letter and lowercases the rest.
- `trim`, `trimStart`, and `trimEnd` accept custom characters.
- `escape` and `unescape` handle HTML entities.

### Functions and async

- `debounce(fn, ms, { signal })` delays calls and supports `AbortSignal`.
- `throttle(fn, ms)` limits call frequency.
- `memoize(fn)` caches results by the first argument.
- `once(fn)` runs only on the first call.
- `retry(fn, { retries, delay })` retries a failing promise.
- `delay(ms)` returns a promise that resolves after `ms`.
- `timeout(ms)` returns a promise that rejects after `ms`.
- `Mutex` and `Semaphore` coordinate concurrent async work.

## Conventions for generated code

1. **Keep types intact.** Don't cast results to `any`. Let inference work, and add explicit generics only when it fails.
2. **Avoid mutation.** Most array and object functions return new values. `merge` and `assign` are the exceptions, so copy first if the input is shared.
3. **Pass iteratee functions, not property strings.** The main API doesn't support Lodash shorthand like `groupBy(users, 'role')`. Write `groupBy(users, (u) => u.role)`.
4. **Use `AbortSignal` for cancellation.** Pass `signal` to `debounce`, `throttle`, and `retry` instead of storing timer IDs.
5. **Don't wrap in try/catch needlessly.** `retry` already rethrows the last error after all attempts fail.

## Migration from Lodash

When asked to replace Lodash:

1. Replace `import _ from 'lodash'` with named imports from `es-toolkit/compat`.
2. Run the existing test suite.
3. Switch individual calls to the main entry point only when tests still pass and the types are stricter.
4. Remove `lodash` from `package.json` once nothing imports it.

Functions with no equivalent in the main API, such as some collection helpers that accept strings or objects as iteratees, should stay on `compat`.

## Common mistakes

- Using `cloneDeep` on class instances, functions, or DOM nodes. It targets plain data.
- Expecting `memoize` to key on all arguments. Supply a `getCacheKey` option for multi-argument functions.
- Calling `debounce` inside a render function. Create it once, outside the render path or inside a stable memoized hook.
- Importing from `es-toolkit/compat` and the root for the same name, which causes inconsistent behavior.

## Verification checklist

Before finishing a change, confirm that:

- every import resolves to a documented entry point,
- no Lodash-style string shorthands remain in main-API calls,
- TypeScript compiles without new errors,
- tests covering the changed code pass.

When unsure about a function's signature, read its type definition in `node_modules/es-toolkit` instead of guessing.
