I couldn't save the file. Writing files is disabled in this session, and I have no other way to create one. Here is the page as Markdown so you can save it yourself.

```markdown
# 'use client'

`'use client'` is a directive. Place it at the very top of a file, before any imports, and it tells a React framework that the file and the modules it imports belong to the client side of the application.

```js
'use client';

import { useState } from 'react';

export default function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(count + 1)}>Clicked {count} times</button>;
}
```

The directive is a plain string literal, so either quote style works and the semicolon is optional. It only takes effect as the first statement in the file. A directive that appears after an import is ignored.

## Overview

React components can run in two environments. Server Components render on the server ahead of time, and their output is sent to the browser. Client Components are rendered on the server for the initial HTML and then hydrated, which means their JavaScript is downloaded and run in the browser so they can respond to user input.

By default, every component is a Server Component in a framework that supports them. Adding `'use client'` marks a boundary: the file it appears in, and everything that file imports, is included in the JavaScript bundle sent to the browser.

You only need the directive in the files where interactivity begins. You do not need it in every component.

## When to use it

Add `'use client'` when a component needs something that only exists in the browser or that depends on React's client-side state. Common cases include:

- Hooks such as `useState`, `useReducer`, `useEffect`, and `useLayoutEffect`
- Event handlers such as `onClick`, `onChange`, or `onSubmit`
- Browser APIs such as `window`, `localStorage`, `IntersectionObserver`, or `navigator`
- Custom hooks that wrap any of the above

If a component only renders props and markup, leave the directive out. That keeps less JavaScript in the browser.

## How the boundary works

Once a file is marked, any component it imports is also treated as a client component, even if the imported file has no directive of its own. The boundary spreads downward through the import graph, so place it as high as needed but no higher.

The reverse direction has a rule. A client component cannot import a Server Component directly. Server Components can, however, be passed into a client component as `children` or as another prop. The server renders them first, and the client component receives the finished output.

```js
// layout.js (Server Component, no directive)
import ClientPanel from './ClientPanel';
import ServerDetails from './ServerDetails';

export default function Layout() {
  return (
    <ClientPanel>
      <ServerDetails />
    </ClientPanel>
  );
}
```

```js
// ClientPanel.js
'use client';

import { useState } from 'react';

export default function ClientPanel({ children }) {
  const [open, setOpen] = useState(true);
  return (
    <section>
      <button onClick={() => setOpen(!open)}>Toggle</button>
      {open && children}
    </section>
  );
}
```

This pattern keeps the data-fetching parts of the tree on the server while the interactive shell stays on the client.

## Passing props across the boundary

Props that move from a Server Component to a Client Component must be serializable. That includes strings, numbers, booleans, plain objects and arrays, `Date` values, and Server Actions marked with `'use server'`. Ordinary functions, class instances, and objects with methods cannot cross the boundary.

If you need to run server logic in response to a click, define it as a Server Action and pass the action itself. Do not pass an ordinary function.

## Common mistakes

**Adding the directive everywhere.** Each marked file grows the client bundle. Start with the smallest component that needs interactivity and mark that one.

**Placing it below an import.** The directive must be the first statement. Placed afterward, it is an unused string.

**Expecting `window` on the server.** Code in a client component still runs on the server during the initial render. Guard browser-only access inside `useEffect`, which runs only in the browser, or check `typeof window !== 'undefined'`.

**Importing server-only code into a client file.** Database clients, secrets, and file system access should stay out of any module reachable from a `'use client'` file, because that code would end up in the browser bundle.

**Assuming it works in every React setup.** In a plain React app with no framework, the directive does nothing. It is read by the bundler or framework that supports React Server Components, such as Next.js.

## Summary

- `'use client'` goes at the top of a file, before any imports.
- It marks the file and its imports as client code included in the browser bundle.
- Use it where state, effects, event handlers, or browser APIs are needed, and keep it as low in the tree as possible.
- Client components can receive Server Components as children and props, but cannot import them directly.
- Props crossing the boundary must be serializable, and functions should be passed only as Server Actions.
```

The body is about 900 words. It's an original explanation written in the style of the React docs, not a copy of the official page. To get a file, save this as `use-client.md`, or enable file writing and I'll create it and send it to you.
