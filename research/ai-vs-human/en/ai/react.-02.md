I can't write files in this session, so here's the page as Markdown you can copy and save as `upgrade-to-react-18.md`.

````markdown
# How to Upgrade to React 18

This page explains how to move an existing app from React 17 to React 18. Most apps need only a few changes. The largest is switching from `ReactDOM.render` to `createRoot`, which enables the concurrent features that React 18 introduces.

## Installing React 18

Install the React and ReactDOM packages at version 18:

```bash
npm install react@18 react-dom@18
```

If you use TypeScript, update the type definitions too:

```bash
npm install @types/react@18 @types/react-dom@18
```

## Step 1: Replace `ReactDOM.render` with `createRoot`

In React 17, you rendered an app like this:

```js
import { render } from 'react-dom';

const container = document.getElementById('app');
render(<App />, container);
```

In React 18, create a root first, then render into it:

```js
import { createRoot } from 'react-dom/client';

const container = document.getElementById('app');
const root = createRoot(container);
root.render(<App />);
```

The old API still works in React 18, but it runs your app in legacy mode and logs a warning in development. Legacy mode does not include automatic batching or other concurrent features, so moving to `createRoot` is what unlocks them.

Unmounting also changed. Replace `unmountComponentAtNode` with `root.unmount()`:

```js
root.unmount();
```

## Step 2: Replace `ReactDOM.hydrate` with `hydrateRoot`

If you server-render your app and hydrate it on the client, switch to `hydrateRoot`:

```js
import { hydrateRoot } from 'react-dom/client';

const container = document.getElementById('app');
const root = hydrateRoot(container, <App />);
```

Hydration is stricter in React 18. Mismatches between server and client markup are reported as errors, so fix any differences rather than relying on React to patch them silently.

## Step 3: Remove render callbacks

`ReactDOM.render` accepted a callback as its third argument. `root.render` does not. If your code depended on that callback running after the DOM updated, you have two options.

Move the logic into a component, using an effect that runs after the component renders:

```js
function App() {
  useEffect(() => {
    // Runs after the app has rendered into the DOM.
  }, []);

  return <Content />;
}
```

Or, if you need the DOM to be updated synchronously, wrap the render in `flushSync`:

```js
import { flushSync } from 'react-dom';

flushSync(() => {
  root.render(<App />);
});
// The DOM is updated here.
```

Use `flushSync` sparingly, because it opts out of batching and can hurt performance.

## Automatic batching

React 18 batches state updates in more places. Previously, React batched updates only inside its own event handlers. Now updates inside promises, `setTimeout`, native event listeners, and other callbacks are batched too.

Most apps benefit with no changes. If a component depended on each `setState` causing a separate render, though, its behavior may change. To opt out for a specific update, use `flushSync`:

```js
import { flushSync } from 'react-dom';

function handleClick() {
  flushSync(() => {
    setCount(c => c + 1);
  });
  flushSync(() => {
    setFlag(f => !f);
  });
}
```

## Strict Mode changes

In development, Strict Mode now mounts each component, unmounts it, and mounts it again, reusing the preserved state. This surfaces effects that lack cleanup. If your effect subscribes to something, starts a timer, or fetches data, make sure its cleanup function undoes that work:

```js
useEffect(() => {
  const id = setInterval(tick, 1000);
  return () => clearInterval(id);
}, []);
```

This double-run behavior happens only in development. Production builds are unaffected.

## Effect timing

Effects triggered by discrete user input, such as clicks and key presses, now flush synchronously. Most code works without changes, but if you rely on the exact timing of an effect after a click, test that interaction after upgrading.

## Server rendering

React 18 adds streaming server rendering with Suspense. Use `renderToPipeableStream` in Node environments or `renderToReadableStream` in environments that support Web Streams. The older `renderToString` still works, but it does not support streaming Suspense boundaries.

## Browser support

React 18 no longer supports Internet Explorer. Check your browserslist configuration and polyfills before upgrading, and make sure your target browsers support the features React now relies on.

## TypeScript changes

The React 18 type definitions include several breaking changes:

- `React.FC` and `React.FunctionComponent` no longer include `children` in props implicitly. Add `children` to your prop types where you need it.
- `useRef` requires an argument. Pass `null` explicitly if you have no initial value, for example `useRef<HTMLDivElement>(null)`.
- Some return types were tightened, so code that compiled against React 17 types may need small fixes.

Run your type checker after updating the packages and fix the errors it reports.

## Testing changes

If you test components with React Testing Library, upgrading the library to a version that supports React 18 is usually enough. If you call `act` yourself, import it from `react-dom/test-utils`, and wrap any code that triggers state updates in it:

```js
import { act } from 'react-dom/test-utils';

act(() => {
  root.render(<App />);
});
```

If you do not use a testing library, set the global flag that tells React it is running in a test environment:

```js
global.IS_REACT_ACT_ENVIRONMENT = true;
```

## Upgrade checklist

1. Install `react@18` and `react-dom@18`, plus the matching type packages.
2. Replace `render` with `createRoot` and `unmountComponentAtNode` with `root.unmount()`.
3. Replace `hydrate` with `hydrateRoot`, and fix any hydration mismatches.
4. Move render callback logic into effects, or use `flushSync` where needed.
5. Add cleanup functions to effects so they survive Strict Mode's double-run.
6. Review any code that depended on the number of renders caused by state updates.
7. Update server rendering to use the streaming APIs if you need Suspense on the server.
8. Fix TypeScript errors, and update your test setup to use `act`.
````
