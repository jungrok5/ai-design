# Debugging and Troubleshooting

<Intro>

Every React app runs into bugs eventually. This page covers the tools and habits that help you find the cause of a problem quickly, so you can get back to building.

</Intro>

<YouWillLearn>

* How to read React's error messages and warnings
* How to use React Developer Tools to inspect components
* How to find the cause of unexpected re-renders
* How to fix the most common mistakes

</YouWillLearn>

## Read the error message {/*read-the-error-message*/}

Most problems announce themselves. In development, React prints warnings and errors to the browser console, and many include a link to a longer explanation. Read the whole message before changing any code. It often names the component, the prop, or the rule you broke.

Two details are worth noting:

* **Component stacks** show which components were rendering when the error occurred. Start with the topmost component in your own code, not in a library.
* **Warnings only appear in development.** If something works locally but fails in production, check that you aren't relying on behavior that only exists in development builds.

## Use React Developer Tools {/*use-react-developer-tools*/}

[React Developer Tools](/learn/react-developer-tools) is a browser extension that adds two tabs to your browser's developer tools: **Components** and **Profiler**.

The **Components** tab shows your component tree. Select any component to see its current props, state, and context. You can edit these values directly, which lets you test how a component behaves without changing your code.

The **Profiler** tab records a session of interaction and shows which components rendered and how long each took. Use it when your app feels slow, but measure before you optimize.

## Check your assumptions with logging {/*check-your-assumptions-with-logging*/}

When the cause isn't obvious, print values and compare them to what you expected:

```js
function Cart({ items }) {
  console.log('Cart rendered with', items);
  // ...
}
```

If a log appears twice during development, that is usually [Strict Mode](/reference/react/StrictMode) at work. Strict Mode renders components an extra time to help you find impure code. It doesn't happen in production.

You can also use the `debugger` statement or your browser's breakpoints to pause execution and inspect the call stack.

## Common problems {/*common-problems*/}

### State doesn't update immediately {/*state-doesnt-update-immediately*/}

Calling a state setter doesn't change the variable in the current render. It schedules a new render with the new value.

```js
function handleClick() {
  setCount(count + 1);
  console.log(count); // Still the old value
}
```

To use the next value right away, store it in a variable first. To update based on the previous value, pass an updater function such as `setCount(c => c + 1)`.

### Mutating state directly {/*mutating-state-directly*/}

React compares old and new state to decide whether to re-render. If you modify an object or array in place, React sees the same reference and skips the update. Always create a new object or array instead:

```js
setItems([...items, newItem]); // Correct
items.push(newItem);           // Wrong
```

### Infinite loops {/*infinite-loops*/}

A component that sets state during rendering will render again, set state again, and never stop. React throws a "Too many re-renders" error to protect you. Check for event handlers that are *called* instead of *passed*:

```js
<button onClick={handleClick()}>  // Wrong: runs during render
<button onClick={handleClick}>    // Correct
```

The same problem occurs with an Effect that updates state it also depends on. Review its dependency list and ask whether the Effect is necessary at all.

### Stale values in Effects {/*stale-values-in-effects*/}

If an Effect or event handler seems to use an outdated value, its dependency array is probably missing something. Install the React ESLint plugin, which flags missing dependencies as you type.

## Catch errors with Error Boundaries {/*catch-errors-with-error-boundaries*/}

An error thrown during rendering would otherwise unmount your whole app. An [Error Boundary](/reference/react/Component#catching-rendering-errors-with-an-error-boundary) catches the error in part of the tree and shows a fallback UI instead. Place them around sections that can fail independently, such as a widget that loads third-party data.

Error Boundaries don't catch errors in event handlers or asynchronous code. Use `try`/`catch` for those.

## Isolate the problem {/*isolate-the-problem*/}

If you're still stuck, shrink the problem. Remove components until the bug disappears, then add them back one at a time. Recreating the issue in a small sandbox often reveals the cause, and gives you something to share if you need to ask for help.

<Recap>

* Read error messages fully; they usually point to the cause.
* Use React Developer Tools to inspect props, state, and renders.
* Remember that state updates apply on the next render, and never mutate state.
* Use Error Boundaries to contain rendering errors.
* Reduce your code to a minimal example when you can't find the bug.

</Recap>
