# Server Functions

Server Functions let you define functions that run on the server and call them from components that run in the browser. When a Server Function is called, React sends the request to the server, runs the function there, and returns the result to the client. You don't need to write a separate API endpoint to perform this work.

Server Functions are used with React Server Components, and React frameworks provide the network layer that connects client and server. The details of how requests are routed can vary between frameworks.

## Defining a Server Function

To mark a function as a Server Function, add the `"use server"` directive at the top of the function body:

```js
async function createNote(formData) {
  'use server';
  const title = formData.get('title');
  await db.notes.insert({ title });
}
```

You can also place the directive at the top of a file. In that case, every exported function in the file becomes a Server Function:

```js
'use server';

export async function deleteNote(id) {
  await db.notes.delete(id);
}
```

Client Components can import functions from a file marked with `"use server"`. When the client calls an imported function, React makes a network request to the server.

## Using Server Functions in forms

The most common use of Server Functions is with forms. Pass a Server Function to the `action` prop of a `<form>` element. React calls the function with the form's data when the form is submitted:

```jsx
import { createNote } from './actions';

export default function NewNote() {
  return (
    <form action={createNote}>
      <input type="text" name="title" />
      <button type="submit">Save</button>
    </form>
  );
}
```

## Calling from Client Components

Client Components can also call Server Functions directly, for example in an event handler:

```jsx
'use client';

import { deleteNote } from './actions';

export default function DeleteButton({ id }) {
  return (
    <button onClick={() => deleteNote(id)}>
      Delete
    </button>
  );
}
```

When a call might take a while, track its pending state. Use a transition or a hook such as `useActionState` so the interface can show progress and handle errors.

## Arguments and return values

Arguments and return values cross the network boundary, so they must be serializable. Serializable values include primitives, plain objects, arrays, `Date`, and `FormData`. Functions and class instances can't be sent as arguments, with the exception of other Server Functions.

## Security

Server Functions are public endpoints. Anyone can send a request to them, so don't assume that only your own UI will call a given function. Check that the current user is allowed to perform the action, and validate every argument on the server, even if the client has already validated it:

```js
'use server';

export async function deleteNote(id) {
  const user = await getCurrentUser();
  if (!user) throw new Error('Not signed in');

  const note = await db.notes.find(id);
  if (note.ownerId !== user.id) throw new Error('Forbidden');

  await db.notes.delete(id);
}
```

Frameworks may hide error details from the client in production. For errors you expect, such as invalid input, return a result value that the component can display instead of relying on thrown error messages.

## Recap

- Server Functions run on the server and can be called from Client Components.
- Mark a function or a file with `"use server"`.
- Pass a Server Function to a `<form>` element's `action` prop to handle submissions.
- Arguments and return values must be serializable.
- Always authorize and validate input inside the Server Function.

---

*Note: This is an original page written in the style of the React docs, not the official text. The word count of the body is approximately 620 words.*
