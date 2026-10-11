# flushSync

`flushSync` lets you force React to flush any updates inside the provided callback synchronously. This ensures that the DOM is updated immediately.

```js
flushSync(callback)
```

- [Reference](#reference)
  - [`flushSync(callback)`](#flushsync)
- [Usage](#usage)
  - [Flushing updates for third-party integrations](#flushing-updates-for-third-party-integrations)
- [Troubleshooting](#troubleshooting)

---

## Reference

### `flushSync(callback)`

Call `flushSync` to force React to flush any pending work and update the DOM synchronously.

```js
import { flushSync } from 'react-dom';

flushSync(() => {
  setSomething(123);
});
```

Most of the time, `flushSync` can be avoided. Use it as a last resort.

[See more examples below.](#usage)

#### Parameters

- `callback`: A function. React will immediately call this callback and flush any updates it contains synchronously. It may also flush any pending updates, Effects, or updates inside Effects. If an update suspends as a result of this `flushSync` call, the fallbacks may be re-shown.

#### Returns

`flushSync` returns `undefined`.

#### Caveats

- `flushSync` can significantly hurt performance. Use it sparingly.
- `flushSync` may force pending Suspense boundaries to show their `fallback` state.
- `flushSync` may run pending Effects and synchronously apply any updates they contain before returning.
- `flushSync` may flush updates outside the callback when necessary to flush the updates inside the callback. For example, if there are pending updates from a click, React may flush those before flushing the updates inside the callback.
- Calling `flushSync` during rendering or inside an Effect is not supported. React will warn, and the call will not flush synchronously.

---

## Usage

### Flushing updates for third-party integrations

When integrating with third-party code such as browser APIs or UI libraries, it may be necessary to force React to flush updates. Use `flushSync` to flush any state updates inside the callback synchronously:

```js
flushSync(() => {
  setSomething(123);
});
// By this line, the DOM is updated.
```

This ensures that, by the time the next line of code runs, React has already updated the DOM.

**Using `flushSync` is uncommon, and using it often can significantly hurt the performance of your app.** If your app only uses React APIs, and does not integrate with third-party libraries, `flushSync` should be unnecessary.

However, it can be helpful for integrating with third-party code like browser APIs.

Some browser APIs expect results inside of callbacks to be written to the DOM synchronously, by the end of the callback, so the browser can do something with the rendered DOM. In most cases, React handles this for you automatically. But in some cases it may be necessary to force a synchronous update.

For example, the browser `onbeforeprint` API allows you to change the page immediately before the print dialog opens. This is useful for applying custom print styles that allow the document to display better for printing. In the example below, you use `flushSync` inside of the `onbeforeprint` callback to immediately "flush" the React state to the DOM. Then, by the time the print dialog opens, the page displays `isPrinting` as "yes":

```js
import { useEffect, useState } from 'react';
import { flushSync } from 'react-dom';

export default function PrintApp() {
  const [isPrinting, setIsPrinting] = useState(false);

  useEffect(() => {
    function handleBeforePrint() {
      flushSync(() => {
        setIsPrinting(true);
      });
    }

    function handleAfterPrint() {
      setIsPrinting(false);
    }

    window.addEventListener('beforeprint', handleBeforePrint);
    window.addEventListener('afterprint', handleAfterPrint);
    return () => {
      window.removeEventListener('beforeprint', handleBeforePrint);
      window.removeEventListener('afterprint', handleAfterPrint);
    };
  }, []);

  return (
    <>
      <h1>isPrinting: {isPrinting ? 'yes' : 'no'}</h1>
      <button onClick={() => window.print()}>Print</button>
    </>
  );
}
```

Without `flushSync`, the print dialog would display `isPrinting` as "no". This is because React batches the updates asynchronously, and the print dialog is displayed before the state is updated.

<Pitfall>

`flushSync` can significantly hurt performance, and may unexpectedly force pending Suspense boundaries to show their fallback state.

Most of the time, `flushSync` can be avoided, so use `flushSync` as a last resort.

</Pitfall>

---

## Troubleshooting

### I'm getting an error: "flushSync was called from inside a lifecycle method"

React cannot `flushSync` in the middle of rendering. If you do, it will warn and the update will be scheduled normally instead.

This includes calling `flushSync` directly in a component body, inside an updater function, or inside a `useLayoutEffect` callback.

```js
function MyComponent() {
  // 🔴 Wrong: calling flushSync during rendering
  flushSync(() => {
    setCount(1);
  });
}
```

Instead, move the call into an event handler, or into a browser callback that you subscribe to in an Effect, as shown in the example above:

```js
function MyComponent() {
  function handleClick() {
    // ✅ Correct: calling flushSync in an event handler
    flushSync(() => {
      setCount(1);
    });
  }
  // ...
}
```

If you only need to read the latest DOM after an update, consider using a [ref](/reference/react/useRef) together with [`useLayoutEffect`](/reference/react/useLayoutEffect) rather than forcing a synchronous flush.
