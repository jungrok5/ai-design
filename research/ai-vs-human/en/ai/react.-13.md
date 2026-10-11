# React Labs: What We've Been Working On – June 2022

*June 15, 2022 by Andrew Clark, Dan Abramov, Jan Kassens, Joseph Savona, Josh Story, Lauren Tan, Luna Ruan, Mengdi Chen, Rick Hanlon, Robert Zhang, Sathya Gunasekaran, Sebastian Markbåge, and Xuan Huang*

---

React 18 was years in the making, and it gave the React team important lessons about how to ship a major feature. Concurrent rendering reached users through a gradual adoption strategy, and that approach shaped how we plan the work ahead.

In this post, we'll give an update on the projects we're researching and building. These are early explorations, not commitments, and some may change direction or never ship. We share them because we want to work in the open and hear from the community.

## New React Docs {/*new-react-docs*/}

Earlier this year we released a beta of the new React documentation at [beta.reactjs.org](https://beta.reactjs.org). The new site teaches modern React with function components and Hooks, and every example is interactive. Instead of treating Hooks as an add-on, it makes them the foundation of how you learn React.

The beta also shows a different way of teaching. Each page builds a mental model first, then moves to API details. We've also added many diagrams and challenges so you can check your understanding as you read.

We're still filling in the remaining sections, including the full API reference. If you find a confusing explanation or a bug in an example, please open an issue on the docs repository.

## React Server Components {/*react-server-components*/}

Server Components are a new kind of component that renders ahead of time, before bundling, in an environment separate from your client app or SSR server. They can run once at build time, or on a web server for each request.

Server Components let you write components that read from your data layer directly, without sending that code to the browser. A component can query a database or the filesystem, and only its rendered output reaches the client. This keeps your bundle small and removes many client-server waterfalls.

Since our [introductory talk](/blog/2020/12/21/data-fetching-with-react-server-components), we've been working through the details of the design. Some of what we've learned:

- **The boundary between server and client must be explicit.** We're moving toward file-level markers so that tools and humans can both tell where code runs.
- **Server and client components should compose freely.** A Server Component can render a Client Component, and pass Server Components to it as children.
- **Frameworks need to own the integration.** Server Components require a bundler and server that understand the split, so we're working with framework authors on the integration points.

We don't expect most developers to wire this up by hand. We expect a framework or router to provide it, and we're collaborating with the Next.js team on the first implementation.

## Asset Loading {/*asset-loading*/}

Today, scripts, stylesheets, and fonts are often loaded in ways that hurt the user experience. Resources are discovered late, load in the wrong order, or cause layout shift when they arrive.

We want React to know about the assets a component needs, so it can load them at the right time and keep them consistent with Suspense. Imagine that a component declares its stylesheet, and React guarantees the styles are loaded before the content is revealed. This would prevent unstyled content from flashing on the screen.

We're exploring integration at several levels. For server rendering, React could emit preload hints early in the stream. For client transitions, it could wait for a stylesheet before committing a new screen. We're also working on a way to deduplicate resources, so that rendering the same component twice doesn't fetch the same file twice.

## Static Server Rendering Optimizations {/*static-server-rendering-optimizations*/}

Static Site Generation (SSG) and Incremental Static Regeneration (ISR) are great for performance, but they have limits. The page is either entirely static or entirely dynamic, and the middle ground is hard to reach.

We're designing optimizations that let a single React tree contain both kinds of content. Frameworks could serve the static shell immediately and fill in the dynamic parts as they become ready. Suspense already gives us the building blocks, since a boundary can mark the dynamic region while the rest of the page is sent right away.

The same technique could also improve how pages are cached. If most of a page is static, a CDN can store that portion and the server only needs to compute what changes.

## React Optimizing Compiler {/*react-optimizing-compiler*/}

In our [previous update](/blog/2021/12/17/react-conf-2021-recap), we shared an early look at an experimental compiler, nicknamed "React Forget." It automatically memoizes your components so you don't have to write `useMemo` and `useCallback` by hand.

Today, avoiding unnecessary re-renders often means wrapping values and functions in memoization Hooks. That's easy to forget and easy to get wrong. The compiler aims to deliver the performance benefits of fine-grained updates while you keep writing plain JavaScript.

The compiler's work depends on the Rules of React. It analyzes your code and assumes components are pure and follow the Rules of Hooks. In our experiments, most code already follows these rules. Where it doesn't, we plan to provide a linter and clear diagnostics.

We've been testing the compiler internally at Meta. It's still early, and we aren't ready to publish an API yet. We'll share more once we're confident in its behavior.

## Offscreen {/*offscreen*/}

Today, if you want to hide part of a UI and later show it again, you have two choices. You can keep it mounted and hidden, which wastes work, or unmount it and lose its state.

Offscreen is a proposed solution: a component that can be hidden while still preserving its state. When content is offscreen, React deprioritizes its updates and can unmount its effects. When it becomes visible again, React restores everything as it was.

This could enable features such as instant back navigation, tab switching without losing form input, and virtualized lists that keep their scroll position. It would also let React prepare a screen in the background before the user navigates to it.

## Transition Tracing {/*transition-tracing*/}

The Transition Tracing API lets you detect when React [Transitions](/reference/react/useTransition) are slow and investigate why. After using the new `startTransition` APIs in React 18, we found that teams needed a way to measure how long a transition takes from start to finish.

The API would let you name a transition and then report when it completes, including any Suspense boundaries it waited on. With that data, you can find the slowest parts of a navigation and fix them.

## Thank You {/*thank-you*/}

Thanks to everyone who tried the new docs, filed issues, and shared feedback on React 18. We'll keep sharing updates as these projects mature. If you want to follow along, watch the [React blog](/blog) and the [RFCs repository](https://github.com/reactjs/rfcs).
