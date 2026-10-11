I couldn't save this as a `.md` file: the file-writing tool is disabled in this session, so the text is below instead.

# use

`use` is a React API that lets you read the value of a resource, such as a Promise or a context.

```js
const value = use(resource);
```

When you pass a Promise to `use`, it integrates with Suspense and Error Boundaries. When you pass a context, it works like `useContext`, with one important difference: it can be called inside conditionals and loops.

---

## Reference

### `use(resource)`

Call `use` inside your component to read the value of a resource.

```js
import { use } from 'react';

function Comments({ commentsPromise }) {
  const comments = use(commentsPromise);
  return comments.map(comment => <p key={comment.id}>{comment.text}</p>);
}
```

Unlike Hooks such as `useState` or `useContext`, `use` can be called inside loops and conditional statements like `if`. Even so, it is best to call `use` at the top level of your component when you can, because this keeps the component's reads easy to follow.

#### Parameters

* `resource`: The source of the value you want to read. A resource is either a Promise or a context, such as the object returned by `createContext`.

#### Returns

The value read from the resource. For a Promise, this is the resolved value. For a context, this is the current context value from the nearest matching provider.

#### Caveats

* `use` must be called inside a component or a custom Hook.
* When you pass a Promise, React suspends the component that called `use` until the Promise settles. If the Promise rejects, the error is thrown to the nearest Error Boundary.
* `use` cannot be called inside a `try-catch` block. To handle errors, wrap the component in an Error Boundary instead.
* Promises passed to `use` should come from a Server Component, a framework, or a cache. If a Client Component creates a new Promise during render, that Promise is recreated on every render, and the component may suspend repeatedly.
* Unlike `useContext`, `use` can be called after an early return, such as `if (!children) return null;`.

---

## Usage

### Reading context conditionally

Because `use` can run after an early return, you can read context only when you need it:

```js
import { use } from 'react';
import { ThemeContext } from './ThemeContext';

function Heading({ children }) {
  if (children == null) {
    return null;
  }
  const theme = use(ThemeContext);
  return <h1 style={{ color: theme.primary }}>{children}</h1>;
}
```

If `children` is empty, the component returns early and never reads the context.

### Streaming data from the server to the client

You can start a request on the server and pass the Promise to a Client Component. The Client Component reads it with `use`, and a Suspense boundary shows a fallback until the data arrives.

On the server:

```js
import { Suspense } from 'react';
import { fetchMessage } from './lib';
import { Message } from './Message';

export default function App() {
  const messagePromise = fetchMessage();
  return (
    <Suspense fallback={<p>Waiting for message...</p>}>
      <Message messagePromise={messagePromise} />
    </Suspense>
  );
}
```

On the client:

```js
'use client';
import { use } from 'react';

export function Message({ messagePromise }) {
  const message = use(messagePromise);
  return <p>Here is the message: {message}</p>;
}
```

The Promise is created once on the server, so the Client Component does not recreate it on each render.

### Handling rejected Promises

If the Promise rejects, `use` throws the error. Wrap the component in an Error Boundary to show a fallback:

```js
import { Suspense } from 'react';
import { ErrorBoundary } from 'react-error-boundary';
import { Message } from './Message';

function MessageContainer({ messagePromise }) {
  return (
    <ErrorBoundary fallback={<p>Could not load the message.</p>}>
      <Suspense fallback={<p>Waiting for message...</p>}>
        <Message messagePromise={messagePromise} />
      </Suspense>
    </ErrorBoundary>
  );
}
```

The `Message` component is the same as in the previous example. It calls `use` and does not need its own error handling.

---

## Troubleshooting

### My component keeps suspending

This usually happens when a Client Component creates a new Promise on every render:

```js
// Avoid: a new Promise is created on every render
function Notes({ id }) {
  const notes = use(fetchNotes(id));
  return <NoteList notes={notes} />;
}
```

Create the Promise outside the component, in a parent or a Server Component, or store it in a cache keyed by `id`. Then pass the same Promise to the component.

### I get an error when I wrap `use` in try-catch

`use` cannot be called inside a `try-catch` block. Move the call out of the block and handle the failure with an Error Boundary, as shown above.

### `use` is not defined

Import it from React: `import { use } from 'react';`. The `use` API is available in React 19 and later.
