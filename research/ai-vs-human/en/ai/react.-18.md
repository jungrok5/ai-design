```markdown
---
title: useRef
---

`useRef` is a React Hook that lets you reference a value that's not needed for rendering.

```js
const ref = useRef(initialValue)
```

---

## Reference {/*reference*/}

### `useRef(initialValue)` {/*useref*/}

Call `useRef` at the top level of your component to declare a ref.

```js
import { useRef } from 'react';

function MyComponent() {
  const intervalRef = useRef(0);
  const inputRef = useRef(null);
  // ...
```

#### Parameters {/*parameters*/}

* `initialValue`: The value the ref object's `current` property should have at first. It can be a value of any type. React ignores this argument after the initial render.

#### Returns {/*returns*/}

`useRef` returns an object with a single property:

* `current`: At first, it's set to the `initialValue` you passed. You can later set it to something else. If you pass the ref object to React as a `ref` attribute on a JSX node, React sets its `current` property.

On later renders, `useRef` returns the same object.

#### Caveats {/*caveats*/}

* You can mutate the `ref.current` property. Unlike state, it is mutable. However, if it holds an object that is used for rendering (for example, a piece of your state), you shouldn't mutate that object.
* When you change the `ref.current` property, React does not re-render your component. React doesn't know when you change it because a ref is a plain JavaScript object.
* Do not write _or read_ `ref.current` during rendering, except for [initialization.](#avoiding-recreating-the-ref-contents) This makes your component's behavior unpredictable.
* In Strict Mode, React will **call your component function twice** to help you find accidental impurities. This is development-only behavior and does not affect production. Each ref object is created twice, but one of the versions is discarded. If your component function is pure (as it should be), this should not affect the behavior.

---

## Usage {/*usage*/}

### Referencing a value with a ref {/*referencing-a-value-with-a-ref*/}

Call `useRef` at the top level of your component to declare one or more refs.

```js [[1, 4, "intervalRef"], [3, 4, "0"]]
import { useRef } from 'react';

function Stopwatch() {
  const intervalRef = useRef(0);
  // ...
```

`useRef` returns a ref object with a single `current` property initially set to the initial value you provided.

On subsequent renders, `useRef` returns the same object. You can change its `current` property to store information and read it later. This might remind you of [state](/reference/react/useState), but there is an important difference.

**Changing a ref does not trigger a re-render.** This means refs are perfect for storing information that doesn't affect the visual output of your component. For example, if you need to store an [interval ID](https://developer.mozilla.org/en-US/docs/Web/API/setInterval) and retrieve it later, you can put it in a ref. To update the value inside the ref, manually change its `current` property:

```js
function handleStartClick() {
  const intervalId = setInterval(() => {
    // ...
  }, 1000);
  intervalRef.current = intervalId;
}
```

Later, you can read that interval ID from the ref so that you can [clear that interval](https://developer.mozilla.org/en-US/docs/Web/API/clearInterval):

```js
function handleStopClick() {
  const intervalId = intervalRef.current;
  clearInterval(intervalId);
}
```

By using a ref, you ensure that:

- You can **store information** between re-renders (unlike regular variables, which reset on every render).
- Changing it **does not trigger a re-render** (unlike state variables, which trigger a re-render).
- The **information is local** to each copy of your component (unlike the variables outside, which are shared).

Changing a ref does not trigger a re-render, so refs are not appropriate for storing information you want to display on the screen. Use state for that instead. Read more about [choosing between `useRef` and `useState`.](/learn/referencing-values-with-refs#differences-between-refs-and-state)

<Pitfall>

**Do not write _or read_ `ref.current` during rendering.**

React expects that the body of your component [behaves like a pure function](/learn/keeping-components-pure):

- If the inputs ([props](/learn/passing-props-to-a-component), [state](/learn/state-a-components-memory), and [context](/learn/passing-data-deeply-with-context)) are the same, it should return exactly the same JSX.
- Calling it in a different order or with different arguments should not affect the results of other calls.

Reading or writing a ref **during rendering** breaks these expectations.

```js {3-4,6-7}
function MyComponent() {
  // ...
  // 🚩 Don't write a ref during rendering
  myRef.current = 123;
  // ...
  // 🚩 Don't read a ref during rendering
  return <h1>{myOtherRef.current}</h1>;
}
```

You can read or write refs **from event handlers or Effects instead**.

```js {4-5,9-10}
function MyComponent() {
  // ...
  useEffect(() => {
    // ✅ You can read or write refs in effects
    myRef.current = 123;
  });
  // ...
  function handleClick() {
    // ✅ You can read or write refs in event handlers
    doSomething(myOtherRef.current);
  }
  // ...
}
```

If you *have to* read [or write](/reference/react/useState#storing-information-from-previous-renders) something during rendering, [use state](/reference/react/useState) instead.

When you break these rules, your component might still work, but most of the newer features we're adding to React will rely on these expectations.

</Pitfall>

---

### Manipulating the DOM with a ref {/*manipulating-the-dom-with-a-ref*/}

It's particularly common to use a ref to manipulate the [DOM.](https://developer.mozilla.org/en-US/docs/Web/API/HTML_DOM_API) React has built-in support for this.

First, declare a ref object with an initial value of `null`:

```js
import { useRef } from 'react';

function MyComponent() {
  const inputRef = useRef(null);
  // ...
```

Then pass your ref object as the `ref` attribute to the JSX of the DOM node you want to manipulate:

```js
  // ...
  return <input ref={inputRef} />;
```

After React creates the DOM node and puts it on the screen, React will set the `current` property of your ref object to that DOM node. Now you can access the `<input>`'s DOM node and call methods like [`focus()`](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/focus):

```js
  function handleClick() {
    inputRef.current.focus();
  }
```

React will set the `current` property back to `null` when the node is removed from the screen.

<Sandpack>

```js
import { useRef } from 'react';

export default function Form() {
  const inputRef = useRef(null);

  function handleClick() {
    inputRef.current.focus();
  }

  return (
    <>
      <input ref={inputRef} />
      <button onClick={handleClick}>
        Focus the input
      </button>
    </>
  );
}
```

</Sandpack>

Read more about [manipulating the DOM with refs.](/learn/manipulating-the-dom-with-refs)

---

### Avoiding recreating the ref contents {/*avoiding-recreating-the-ref-contents*/}

React saves the initial ref value once and ignores it on the next renders.

```js
function Video() {
  const playerRef = useRef(new VideoPlayer());
  // ...
```

Although the result of `new VideoPlayer()` is only used for the initial render, you're still calling this function on every render. This can be wasteful if it's creating expensive objects.

To solve it, you may initialize the ref like this instead:

```js
function Video() {
  const playerRef = useRef(null);
  if (playerRef.current === null) {
    playerRef.current = new VideoPlayer();
  }
  // ...
```

Normally, writing or reading `ref.current` during render is not allowed. However, it's fine in this case because the result is always the same, and the condition only executes during initialization so it's fully predictable.

---

## Troubleshooting {/*troubleshooting*/}

### I can't get a ref to a custom component {/*i-cant-get-a-ref-to-a-custom-component*/}

If you try to pass a `ref` to your own component like this:

```js
const inputRef = useRef(null);

return <MyInput ref={inputRef} />;
```

the ref will stay `null` unless `MyInput` does something with it. By default, your own components don't expose the DOM nodes inside them.

To fix this, find the component that should receive the ref and read `ref` from its props, then pass it down to the DOM node you want to expose:

```js {1-2}
function MyInput({ value, onChange, ref }) {
  return (
    <input
      value={value}
      onChange={onChange}
      ref={ref}
    />
  );
}
```

Now the parent component can get a ref to the `<input>` inside `MyInput`.

<Note>

In React 19 and later, `ref` is available as a regular prop for function components. In earlier versions, you needed to wrap the component in [`forwardRef`](/reference/react/forwardRef) to receive it.

</Note>

To expose a limited set of methods instead of the whole DOM node, use [`useImperativeHandle`](/reference/react/useImperativeHandle). Read more about [accessing another component's DOM nodes.](/learn/manipulating-the-dom-with-refs#accessing-another-components-dom-nodes)
```
