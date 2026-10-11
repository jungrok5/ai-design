The title was left blank, so I picked **Responding to Events**. Tell me if you meant a different topic and I'll rewrite it.

---

```markdown
---
title: Responding to Events
---

<Intro>

React lets you add *event handlers* to your JSX. Event handlers are your own functions that run in response to interactions such as clicking, hovering, or focusing a form input.

</Intro>

<YouWillLearn>

* Different ways to write an event handler
* How to pass event handling logic from a parent component
* How events propagate and how to stop them

</YouWillLearn>

## Adding event handlers {/*adding-event-handlers*/}

To add an event handler, first define a function. Then [pass it as a prop](/learn/passing-props-to-a-component) to the right JSX tag. Here is a button that doesn't do anything yet:

```js
export default function Button() {
  return (
    <button>
      I don't do anything
    </button>
  );
}
```

You can make it show a message when a user clicks by following three steps:

1. Declare a function called `handleClick` *inside* your `Button` component.
2. Write the logic inside that function. In this case, use `alert` to show the message.
3. Add `onClick={handleClick}` to the `<button>` JSX.

```js {2-4,7}
export default function Button() {
  function handleClick() {
    alert('You clicked me!');
  }

  return (
    <button onClick={handleClick}>
      Click me
    </button>
  );
}
```

You defined the `handleClick` function and then passed it as a prop to `<button>`. `handleClick` is an **event handler.** Event handler functions:

* Are usually defined *inside* your components.
* Have names that start with `handle`, followed by the name of the event.

By convention, event handlers are named `handle` followed by the event name, so you will often see `onClick={handleClick}`, `onMouseEnter={handleMouseEnter}`, and so on.

You can also define an event handler inline in the JSX:

```jsx
<button onClick={() => {
  alert('You clicked me!');
}}>
```

Inline handlers are convenient for short functions. Both styles do the same thing.

<Pitfall>

Functions passed to event handlers must be passed, not called. For example:

| passing a function (correct)     | calling a function (incorrect)     |
| -------------------------------- | ---------------------------------- |
| `<button onClick={handleClick}>` | `<button onClick={handleClick()}>` |

The difference is small. In the first example, the `handleClick` function is passed as an `onClick` event handler, and React calls it only when the user clicks the button.

In the second example, the `()` at the end of `handleClick()` runs the function *immediately* during [rendering](/learn/render-and-commit), before any click happens. That's because JavaScript inside the [JSX `{` and `}`](/learn/javascript-in-jsx-with-curly-braces) runs right away.

If you want to define an event handler inline, wrap it in an anonymous function, like `onClick={() => alert('...')}`.

</Pitfall>

### Reading props in event handlers {/*reading-props-in-event-handlers*/}

Because event handlers are declared inside a component, they have access to the component's props. Here is a button that shows an alert with its `message` prop when clicked:

```js
function AlertButton({ message, children }) {
  return (
    <button onClick={() => alert(message)}>
      {children}
    </button>
  );
}
```

This lets two buttons show two different messages. Try changing the messages passed to them.

### Passing event handlers as props {/*passing-event-handlers-as-props*/}

Often the parent component should decide what a child's event handler does. Think of buttons: depending on where you use a `Button` component, you might want it to run a different function. Perhaps one plays a movie and another uploads an image.

To do this, pass a prop the component receives from its parent as the event handler:

```js
function Button({ onClick, children }) {
  return (
    <button onClick={onClick}>
      {children}
    </button>
  );
}

function PlayButton({ movieName }) {
  function handlePlayClick() {
    alert(`Playing ${movieName}!`);
  }

  return (
    <Button onClick={handlePlayClick}>
      Play "{movieName}"
    </Button>
  );
}
```

Here, the `PlayButton` component passes `handlePlayClick` as the `onClick` prop to the `Button` inside. Then `Button` passes it straight to the built-in browser `<button>`.

When you build your own components, you can name the event handler props anything you like. By convention, they should start with `on` followed by a capital letter, such as `onPlayMovie` or `onUploadImage`. This lets you name props after what happens in your app instead of after low-level browser interactions.

## Event propagation {/*event-propagation*/}

Event handlers also catch events from any children your component has. We say an event "bubbles" or "propagates" up the tree: it starts where the event happened and then goes up the tree.

If a `<div>` with its own `onClick` contains two buttons, clicking either button runs the button's `onClick` first and then the parent `<div>`'s `onClick`.

<Note>

All events propagate in React except `onScroll`, which only works on the JSX tag you attach it to.

</Note>

### Stopping propagation {/*stopping-propagation*/}

Event handlers receive an **event object** as their only argument. By convention it's usually called `e`, which stands for "event". You can use this object to read information about the event.

The event object also lets you stop propagation. If you want to keep an event from reaching parent components, call `e.stopPropagation()`:

```js {3}
function Button({ onClick, children }) {
  return (
    <button onClick={e => {
      e.stopPropagation();
      onClick();
    }}>
      {children}
    </button>
  );
}
```

Now when you click a button, only that button's handler runs. The parent `<div>`'s handler doesn't run.

### Preventing default behavior {/*preventing-default-behavior*/}

Some browser events have default behavior attached to them. For example, a `<form>` submit event reloads the whole page by default. To prevent that, call `e.preventDefault()` on the event object:

```jsx
<form onSubmit={e => {
  e.preventDefault();
  alert('Submitting!');
}}>
```

Don't mix up `e.stopPropagation()` and `e.preventDefault()`. `stopPropagation` keeps the event from reaching handlers on parent tags. `preventDefault` stops the browser's default behavior for the events that have it.

## Can event handlers have side effects? {/*can-event-handlers-have-side-effects*/}

Yes. Event handlers are the best place for side effects. Unlike rendering functions, event handlers don't need to be [pure](/learn/keeping-components-pure), so they are a good place to *change* something. For example, you can change an input's value when the user types or change a list when the user clicks a button. To change information, you first need a way to store it. In React, you do this with [state, a component's memory.](/learn/state-a-components-memory)

<Recap>

* You handle events by passing a function as a prop to an element like `<button>`.
* Event handlers must be passed, **not called!** Write `onClick={handleClick}`, not `onClick={handleClick()}`.
* Event handlers are defined inside a component, so they can read props.
* You can pass event handlers from the parent to the child as props.
* Events propagate upwards. Call `e.stopPropagation()` on the event object to stop that.
* Call `e.preventDefault()` to stop the browser's default behavior.

</Recap>
```
