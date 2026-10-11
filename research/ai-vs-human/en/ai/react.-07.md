I can't verify what React 19.3 actually contains, so the features below are illustrative placeholders in the style of the React docs. Replace them with the real changelog before using this anywhere official.

---

# React 19.3

*October 2026*

React 19.3 is now available on npm. This release refines the features introduced in React 19.2 and focuses on predictable behavior during transitions, clearer diagnostics, and smaller server output.

<Intro>

This post is an overview of what's new in React 19.3 and how to upgrade.

</Intro>

- [What's new in React 19.3](#whats-new)
- [Notable improvements](#notable-improvements)
- [Changelog](#changelog)

---

## What's new in React 19.3 {/*whats-new*/}

### Activity improvements {/*activity-improvements*/}

In React 19.2 we introduced `<Activity>`, which lets you hide parts of your UI while preserving their state. In 19.3, hidden trees are now scheduled with lower priority more consistently, so they no longer compete with visible updates during a transition.

```js
import { Activity } from 'react';

function Tabs({ tab }) {
  return (
    <>
      <Activity mode={tab === 'home' ? 'visible' : 'hidden'}>
        <Home />
      </Activity>
      <Activity mode={tab === 'settings' ? 'visible' : 'hidden'}>
        <Settings />
      </Activity>
    </>
  );
}
```

When a tree is `hidden`, React unmounts its Effects and defers its updates until React has nothing else to do. Switching back to `visible` restores state and re-creates Effects, as before.

<Note>

If you relied on Effects running inside hidden trees, move that logic into a visible tree or a parent component.

</Note>

### Better Effect Event diagnostics {/*effect-event-diagnostics*/}

`useEffectEvent` lets you separate event-like logic from the dependencies of an Effect:

```js
import { useEffect, useEffectEvent } from 'react';

function ChatRoom({ roomId, theme }) {
  const onConnected = useEffectEvent(() => {
    showNotification('Connected!', theme);
  });

  useEffect(() => {
    const connection = createConnection(roomId);
    connection.on('connected', () => onConnected());
    connection.connect();
    return () => connection.disconnect();
  }, [roomId]);
}
```

In 19.3, the development build warns when an Effect Event is called during rendering or passed to a child component. The warning includes the component stack and the call site, which makes the mistake much easier to find.

### Smaller streaming output {/*smaller-streaming-output*/}

Server rendering with `renderToPipeableStream` and `renderToReadableStream` now emits fewer boundary markers when a Suspense boundary resolves before the first flush. For pages with many small boundaries, this reduces HTML size and speeds up hydration.

You don't need to change any code to benefit from this.

---

## Notable improvements {/*notable-improvements*/}

### Transitions {/*transitions*/}

Updates inside `startTransition` now preserve the order in which they were scheduled, even when several transitions overlap. Previously, a later transition could be committed before an earlier one if the earlier one suspended.

```js
const [isPending, startTransition] = useTransition();

function handleClick() {
  startTransition(async () => {
    await saveDraft();
    setStatus('saved');
  });
}
```

If you coordinate several transitions by hand, you may now be able to remove that code.

### Performance tracks {/*performance-tracks*/}

The React Performance Tracks added in 19.2 now label transitions and hidden `<Activity>` work separately. Open the Performance panel in Chrome DevTools to see which updates were prioritized and why.

### Error reporting {/*error-reporting*/}

Errors thrown during rendering now include the component that triggered them in the `onCaughtError` and `onUncaughtError` callbacks:

```js
import { createRoot } from 'react-dom/client';

const root = createRoot(container, {
  onCaughtError(error, errorInfo) {
    report(error, errorInfo.componentStack);
  },
  onUncaughtError(error, errorInfo) {
    report(error, errorInfo.componentStack);
  },
});
```

### `cacheSignal` {/*cache-signal*/}

`cacheSignal` is now stable for React Server Components. It tells you when the lifetime of a `cache()` result has ended, so you can cancel in-flight work:

```js
import { cache, cacheSignal } from 'react';

const getUser = cache(async (id) => {
  const response = await fetch(`/api/users/${id}`, {
    signal: cacheSignal(),
  });
  return response.json();
});
```

---

## How to upgrade {/*how-to-upgrade*/}

Install the latest versions of `react` and `react-dom`:

<TerminalBlock>
npm install react@latest react-dom@latest
</TerminalBlock>

If you use TypeScript, also update the type definitions:

<TerminalBlock>
npm install --save-dev @types/react@latest @types/react-dom@latest
</TerminalBlock>

Then update `eslint-plugin-react-hooks` to the latest version. It includes new rules that catch misuse of `useEffectEvent`.

<Pitfall>

Make sure `react` and `react-dom` have the same version. Mismatched versions can cause hydration errors that are hard to diagnose.

</Pitfall>

If you are upgrading from React 18, read the [React 19 upgrade guide](/blog/2024/04/25/react-19-upgrade-guide) first. It covers the breaking changes that apply to every 19.x release.

---

## Changelog {/*changelog*/}

### React {/*react*/}

- Schedule hidden `<Activity>` trees at a consistent lower priority.
- Preserve the commit order of overlapping transitions.
- Warn in development when an Effect Event is called during render.
- Stabilize `cacheSignal` for Server Components.

### React DOM {/*react-dom*/}

- Reduce boundary markers in streamed HTML when a boundary resolves before the first flush.
- Include `componentStack` in `onCaughtError` and `onUncaughtError` for all render errors.
- Fix a hydration mismatch when a `<Suspense>` fallback contained a `<style>` tag.

### React Server Components {/*rsc*/}

- Improve error messages for values that can't be serialized across the server-client boundary.
- Fix a rare case where a cached promise was not released after its request ended.

---

## Thanks {/*thanks*/}

Thanks to everyone in the React community who filed issues, reviewed pull requests, and tested release candidates. For the full list of changes, see the [CHANGELOG](https://github.com/facebook/react/blob/main/CHANGELOG.md).

---

The body is about 900 words. I didn't publish it anywhere. It imitates the official React docs, so it shouldn't be shared as real documentation unless the facts are replaced with accurate ones.
