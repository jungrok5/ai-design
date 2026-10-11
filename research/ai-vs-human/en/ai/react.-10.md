---
title: React Conf 2025 Recap
---

<Intro>

Last week we hosted React Conf 2025 in Henderson, Nevada. This post summarizes the talks and announcements from both days, with links to the recordings and to the documentation for everything that shipped.

</Intro>

<YouTubeEmbed title="React Conf 2025 Day 1" src="https://www.youtube.com/embed/zyVRg2QR6LA?si=z-uxsFkq1AxUHSZ1" />

<YouTubeEmbed title="React Conf 2025 Day 2" src="https://www.youtube.com/embed/p9OcztRyDl0?si=v1mn3R5rUwDlmZ6F" />

<Note>

Recordings of both days are available on the React YouTube channel. Slides and speaker notes are linked from each talk's description.

</Note>

## Day 1 keynote {/*day-1-keynote*/}

The first keynote focused on how the pieces of React fit together: a stable compiler, a faster runtime, and better tools for understanding what your app is doing. The team framed these as one effort. Each piece makes the others more useful.

### React 19.2 {/*react-192*/}

React 19.2 is the third release in the past year, following React 19 in December and React 19.1 in June. It adds several features that came out of real production feedback.

**`<Activity />`** lets you split your app into "activities" that you can control and prioritize. You can use it as an alternative to conditionally rendering parts of your UI. When an activity is hidden, React preserves its state and DOM, unmounts its Effects, and defers its updates until React has nothing else to do.

```js
import { Activity } from 'react';

function App({ tab }) {
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

This means you can pre-render the tab a user is likely to visit next, and restore a screen exactly as they left it when they navigate back.

**`useEffectEvent`** extracts non-reactive logic out of Effects into a reusable function. It solves a common problem: reading the latest props or state inside an Effect without making the Effect re-run whenever they change.

```js
import { useEffect, useEffectEvent } from 'react';

function ChatRoom({ roomId, theme }) {
  const onConnected = useEffectEvent(() => {
    showNotification('Connected!', theme);
  });

  useEffect(() => {
    const connection = createConnection(roomId);
    connection.on('connected', onConnected);
    connection.connect();
    return () => connection.disconnect();
  }, [roomId]);
}
```

React 19.2 also adds new **Performance Tracks** to the Chrome DevTools profiler, which show what React is scheduling and when. There are also improvements to server rendering, including partial pre-rendering, which lets you pre-render the static shell of an app and resume the dynamic parts later.

For the full list of changes, see the [React 19.2 release post](/blog/2025/10/01/react-19-2).

### React Compiler 1.0 {/*react-compiler-10*/}

The React team announced the first stable release of React Compiler. The compiler automatically memoizes your components and hooks at build time, so you can write idiomatic React and still get fine-grained updates without sprinkling `useMemo`, `useCallback`, and `memo` throughout your code.

Teams that adopted the compiler during the beta reported measurable improvements in interaction latency with no code changes. The compiler can also memoize in places that manual memoization can't reach, such as after an early return.

The 1.0 release includes:

- Support for Vite, Next.js, and Expo through their standard build plugins.
- A lint rule set, shipped in `eslint-plugin-react-hooks`, that reports code the compiler can't safely optimize.
- Incremental adoption, so you can enable the compiler for one directory or one component at a time.

To get started, read the [installation guide](/learn/react-compiler/installation) and the [incremental adoption guide](/learn/react-compiler/incremental-adoption).

### Canary features {/*canary-features*/}

The keynote also previewed two features that are available in the Canary channel and are close to stable:

- **View Transitions** animate elements that update as a result of a Transition, using the browser's native View Transition API. You describe what should animate and React coordinates the timing.
- **Fragment Refs** let you attach a ref to a `<Fragment>` and interact with all of its top-level DOM nodes, which is useful for observers and for focus management.

<Note>

Canary features are ready for frameworks and libraries to adopt and for you to try in your own apps, but their APIs may still change before a stable release.

</Note>

## The React Foundation {/*the-react-foundation*/}

Meta announced that React, React Native, and JSX will move to a new independent React Foundation, hosted by the Linux Foundation. The foundation's goals are to support the open source community around React and to give companies that depend on React a neutral place to collaborate on its future.

Day-to-day development of React isn't changing. The core team continues to work in the open, and RFCs and the release process stay the same. The foundation will take on responsibilities such as owning trademarks and funding community programs.

## React Native {/*react-native*/}

The React Native sessions covered the New Architecture, which is now the default and the only supported architecture going forward. Speakers shared migration strategies from large apps and showed how concurrent features like Transitions and Suspense now work the same way on native as they do on the web.

Other highlights included:

- Performance work on the Hermes engine, including faster startup.
- Improved debugging, with DevTools that connect directly to your running app.
- New ways to share code between web and native using the same components and hooks.

## Day 2 {/*day-2*/}

The second day went deeper on specific topics through talks from the community and the team.

### Server Components and frameworks {/*server-components-and-frameworks*/}

Several talks showed how teams are using Server Components and Server Functions in production. Common themes were moving data fetching closer to the components that need it, shipping less JavaScript to the client, and using Suspense boundaries to stream content as soon as it's ready. Framework authors discussed how routers, bundlers, and caching layers integrate with these primitives.

### Performance and tooling {/*performance-and-tooling*/}

Speakers walked through profiling real apps with the new Performance Tracks, finding unnecessary re-renders, and deciding when the compiler is enough and when to restructure state. There were also sessions on testing concurrent UIs and on writing Effects that are easier to reason about.

### Accessibility and design {/*accessibility-and-design*/}

Talks on accessibility covered building keyboard-friendly components, announcing asynchronous updates, and respecting user motion preferences when adopting View Transitions.

## Thank you {/*thank-you*/}

Thank you to our speakers, sponsors, volunteers, and everyone who joined us in Henderson or watched online. We'll share details about future events on the [React blog](/blog) and on our social channels.

## Try these features {/*try-these-features*/}

- Upgrade to React 19.2 and try [`<Activity />`](/reference/react/Activity) and [`useEffectEvent`](/reference/react/useEffectEvent).
- Enable [React Compiler](/learn/react-compiler) in your project.
- Try [View Transitions](/reference/react/ViewTransition) in the Canary channel.
- Watch the recordings and share them with your team.
