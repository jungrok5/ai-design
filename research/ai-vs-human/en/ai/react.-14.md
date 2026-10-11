I couldn't save this as a `.md` file because file writing is disabled in this session. Here is the page in full:

# React v18.0

*Released March 29, 2022*

React 18 is a major release focused on concurrent rendering. It changes how React prepares and commits updates to the screen, so that React can pause, resume, and prioritize rendering work. Most applications will run without code changes, but the new root API and a few behavior changes are worth understanding before you upgrade.

This page covers the headline features, the steps needed to upgrade, and the breaking changes you should check.

## Upgrading to React 18

Install the new packages:

```bash
npm install react@18 react-dom@18
```

If you use TypeScript, also update the type definitions:

```bash
npm install @types/react@18 @types/react-dom@18
```

Then switch your entry point from `ReactDOM.render` to `createRoot`, described below. React 18 still runs the legacy API, but it does so in React 17 mode and logs a warning, so you do not get the new features until you migrate.

## New Root API

React 18 introduces `createRoot` from `react-dom/client`. It replaces `ReactDOM.render`:

```js
import { createRoot } from 'react-dom/client';

const container = document.getElementById('app');
const root = createRoot(container);
root.render(<App />);
```

To unmount a tree, call `root.unmount()` instead of `ReactDOM.unmountComponentAtNode`. For server-rendered pages, `hydrateRoot` replaces `ReactDOM.hydrate`:

```js
import { hydrateRoot } from 'react-dom/client';

hydrateRoot(document.getElementById('app'), <App />);
```

The new root API is what enables concurrent features. Apps that stay on the legacy root will not see automatic batching, transitions, or the new Suspense behavior.

## Automatic Batching

React has always batched state updates inside React event handlers. React 18 extends batching to every update, including those inside promises, `setTimeout`, and native event listeners. Fewer renders means better performance:

```js
function handleClick() {
  setCount(c => c + 1);
  setFlag(f => !f);
  // One re-render, not two.
}
```

If you need an update to apply immediately, wrap it in `flushSync`:

```js
import { flushSync } from 'react-dom';

flushSync(() => {
  setCount(c => c + 1);
});
// The DOM has already been updated here.
```

## Transitions

Some updates are urgent, such as typing into an input. Others can wait, such as filtering a large list. React 18 lets you mark the second kind as a *transition* with `startTransition`:

```js
import { startTransition } from 'react';

startTransition(() => {
  setSearchResults(filterItems(query));
});
```

Transition updates can be interrupted by urgent ones, so the interface stays responsive. The `useTransition` hook gives you an `isPending` flag for showing a loading indicator while the transition is in progress.

`useDeferredValue` offers a related tool. It returns a deferred copy of a value that updates after more urgent work finishes, which is useful when you cannot change the code that sets the value.

## Suspense Improvements

Suspense now works on the server. React 18 can stream HTML to the browser as components finish rendering, instead of waiting for the entire page. On Node, use `renderToPipeableStream`. On edge runtimes, use `renderToReadableStream`.

Suspense boundaries also enable *selective hydration*. React hydrates the parts of the page that are ready first, and it prioritizes the part the user interacts with. A slow component no longer blocks hydration of the rest of the page.

## New Hooks

React 18 adds several hooks:

- **`useId`** generates unique IDs that are stable across the server and the client. It is intended for accessibility attributes, not for list keys.
- **`useSyncExternalStore`** lets libraries subscribe to external data stores safely during concurrent rendering. Most application code should not need it directly.
- **`useInsertionEffect`** runs before layout effects and is designed for CSS-in-JS libraries that inject styles.

## Strict Mode Changes

In development, `StrictMode` now mounts each component, unmounts it, and mounts it again, preserving its state. This surfaces effects that do not clean up properly. If your effects subscribe to something, make sure the cleanup function removes the subscription. Production builds are not affected.

## Breaking Changes

Review these items before upgrading:

- **Legacy root API.** `ReactDOM.render` and `ReactDOM.hydrate` still work but are deprecated and run in React 17 mode.
- **Browser support.** React 18 no longer supports Internet Explorer.
- **Components can return `undefined`.** Earlier versions threw an error when a component returned `undefined`. React 18 allows it.
- **TypeScript children.** `React.FC` no longer includes an implicit `children` prop. Add it explicitly if you need it.
- **Hydration mismatches.** When server and client markup differ, React 18 now attempts to recover by client rendering the nearest Suspense boundary and logs an error. Fix the underlying mismatch, since it can cause visible flicker.
- **Warnings removed.** React no longer warns when you call `setState` on an unmounted component, because the warning was mostly noise.

## Summary

React 18 gives you concurrent rendering, automatic batching, transitions, and streaming server rendering. The migration is mostly a matter of switching to `createRoot` and `hydrateRoot`, then checking your effects for proper cleanup. Once that is done, you can adopt transitions and Suspense where they help the most.

---

If you want it saved as a file, you can copy the text above into `react-v18-0.md`. Also, this is written from memory of the React 18 release, so check the details against react.dev before you publish it.
