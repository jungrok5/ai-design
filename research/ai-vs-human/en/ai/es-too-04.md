I couldn't check this against es-toolkit's real release history, so the version numbers, dates and entries below are examples, not the project's actual changelog. Function names like `chunk`, `debounce`, `windowed` and the `es-toolkit/compat` entry point are real. Before you publish, replace the entries with ones from the project's own `CHANGELOG.md`.

---

```markdown
# es-toolkit Changelog

This page lists notable changes to es-toolkit by release, newest first. Each release follows
[Semantic Versioning](https://semver.org/): patch releases fix bugs, minor releases add
functions or options without breaking existing code, and major releases may change behavior.

Changes are grouped under these headings:

- **Added**: new functions, options or entry points.
- **Changed**: behavior changes that stay compatible with earlier releases.
- **Fixed**: bug fixes.
- **Performance**: speed or bundle-size improvements that don't change behavior.
- **Compat**: changes to the `es-toolkit/compat` layer, which matches Lodash behavior.

To find out which version you have installed, run:

    npm ls es-toolkit

---

## 1.42.0

### Added

- `windowed(arr, size, step?, options?)` returns sliding windows over an array. Set
  `{ partialWindows: true }` to keep the trailing windows that have fewer than `size`
  elements.

      windowed([1, 2, 3, 4, 5], 3);
      // => [[1, 2, 3], [2, 3, 4], [3, 4, 5]]

- `attemptAsync(fn)` runs an async function and returns `[error, result]` instead of
  throwing, which makes error handling easier with top-level `await`.
- `Semaphore` accepts an optional `AbortSignal` in `acquire()`. If the signal fires while
  the call is waiting, the call rejects.

### Fixed

- `debounce` no longer calls a pending trailing invocation after `cancel()` when
  `maxWait` was set.
- `isEqual` now treats two `Date` objects that both hold invalid dates as equal, as
  documented.

### Compat

- `compat/get` and `compat/set` handle path strings with quoted bracket keys, such as
  `a["b.c"]`, the same way Lodash does.

---

## 1.41.0

### Added

- `mapAsync`, `filterAsync` and `reduceAsync` take an optional `concurrency` option that
  limits how many callbacks run at the same time.
- `toCamelCaseKeys` and `toSnakeCaseKeys` convert object keys recursively and preserve the
  types of nested arrays.

### Changed

- `retry` now takes a `shouldRetry(error, attempt)` predicate. If the predicate returns
  `false`, the original error is thrown right away instead of the function being retried
  again.
- `throttle` checks that its `wait` argument is a non-negative finite number and throws a
  `RangeError` otherwise.

### Performance

- `groupBy` and `keyBy` are about 15% faster on large arrays because they no longer copy
  arrays inside the loop.

---

## 1.40.0

### Added

- `Mutex`, a lock for a single holder built on top of `Semaphore`. Use
  `await mutex.acquire()` and `mutex.release()`, or run a callback with
  `mutex.runExclusive(fn)`.
- `isJSON(value)` reports whether a string parses as JSON.
- `partition` accepts a type-guard predicate and narrows both output arrays.

      const [strings, others] = partition(values, (v): v is string => typeof v === 'string');

### Fixed

- `cloneDeep` copies `Map` and `Set` instances that are nested inside class instances,
  and keeps their prototypes.
- `merge` no longer replaces typed arrays in the target with plain objects.

### Compat

- `compat/sortBy` sorts `undefined` and `NaN` values in the same order as Lodash 4.17.

---

## 1.39.0

### Added

- `es-toolkit/server` is a new entry point for utilities that need Node.js built-ins. It
  is separate so that the main bundle stays free of platform-specific code.
- `timeout(ms)` and `withTimeout(fn, ms)` reject with a `TimeoutError` when the time limit
  is exceeded.

### Changed

- All functions in `es-toolkit/string` now split words with the same Unicode-aware word
  segmentation, so `camelCase`, `kebabCase` and `snakeCase` return consistent results for
  accented and non-Latin text.

### Fixed

- `pick` and `omit` now copy symbol keys correctly.

---

## 1.0.0

This is the first stable release. Starting with this version, the public API follows
Semantic Versioning strictly.

### Highlights

- **Tree-shakable modules.** You can import every function on its own, for example
  `import { chunk } from 'es-toolkit/array'`, and bundlers remove the code you don't use.
- **TypeScript first.** Type declarations ship with the package, and functions use
  generics and type guards wherever they help.
- **Compatibility layer.** `es-toolkit/compat` gives you Lodash-compatible signatures,
  including argument coercion and edge-case behavior, so you can migrate gradually.
- **Modern runtime targets.** The package supports Node.js 18 and later, Deno, Bun and
  all evergreen browsers.

### Breaking changes from 0.x

- Functions that used to accept `null` or `undefined` as a collection now throw a
  `TypeError` in the main entry point. Use `es-toolkit/compat` to keep the lenient
  behavior.
- `debounce` and `throttle` return objects whose `cancel` and `flush` methods are
  non-enumerable.
- The deprecated `isNil` alias `isNullish` was removed.

---

## Migrating between versions

Minor and patch releases never require changes to your code. When a function is marked
deprecated, it keeps working until the next major release, and its JSDoc comment names the
function to use instead. Turn on your editor's deprecation warnings so you can find these
calls early.

If you are moving from Lodash, start with `es-toolkit/compat`. Then switch imports to the
main entry point one module at a time. The main entry point is smaller and faster, but it
doesn't do the implicit type coercion that Lodash does.

## Reporting issues

If you find a regression, open an issue on the project's GitHub repository. Include:

1. The es-toolkit version and your runtime (Node.js, Deno, Bun or the browser and its
   version).
2. A small reproduction.
3. The output you expected and the output you got.

A regression that breaks documented behavior is usually fixed in the next patch release.
```
