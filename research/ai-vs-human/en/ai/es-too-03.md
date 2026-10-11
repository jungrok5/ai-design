Write is disabled in this session, so I couldn't save a `.md` file. Here is the page as Markdown, ready to copy into a file:

````markdown
# Browser Support

This page lists the browsers that Utilkit officially supports, explains how the library detects missing features, and describes the polyfills it can load. For minimum requirements of individual functions, see each function's reference page.

## Supported browsers

Utilkit 4.x is tested against the browsers below. Older versions may work, but they are not covered by the test suite and may fail silently.

| Browser | Minimum version |
|---|---|
| Chrome | 102 |
| Firefox | 101 |
| Safari | 15.4 |
| Edge | 102 |
| Samsung Internet | 18 |

Node.js 18 and later is supported for server-side rendering and tests.

## Feature detection

Utilkit does not sniff user agents. Each module checks for the features it needs when it loads and records the results in `support`, a read-only object exported by the package.

```js
import { support } from "utilkit";

if (!support.intersectionObserver) {
  console.warn("IntersectionObserver is unavailable; lazy loading is disabled.");
}
```

### `support`

Each key is a boolean. A value of `true` means the feature is available in the current environment.

| Key | Type | Description |
|---|---|---|
| `structuredClone` | `boolean` | Native `structuredClone()` is available. |
| `intersectionObserver` | `boolean` | `IntersectionObserver` is available. |
| `resizeObserver` | `boolean` | `ResizeObserver` is available. |
| `fetchStreams` | `boolean` | Response bodies can be read as streams. |

The object is frozen after the first read and does not change during a session.

## Polyfills

### `loadPolyfills(features)`

Loads polyfill modules for the listed features. Polyfills are never loaded automatically, so call this function before using any feature that depends on a missing flag.

- **Parameters:** `features` (`string[]`): feature keys from `support`.
- **Returns:** `Promise<void>`, resolved when all requested polyfills are ready.

```js
await loadPolyfills(["resizeObserver"]);
```

## Known limitations

- Internet Explorer 11 is not supported, and no polyfill set is provided for it.
- Safari 15.3 and earlier lack `structuredClone()`. `clone()` then falls back to JSON serialization, which drops `Date` and `Map` values.
- Functions that need `IntersectionObserver` throw `UnsupportedError` when the flag is `false` and no polyfill has been loaded.

Report any other inconsistencies in the issue tracker.
````

The page is about 355 words of body text, not counting the code blocks. Utilkit is a placeholder library name, so swap in your real one and adjust the browser versions to match what you actually test.
