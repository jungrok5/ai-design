# Adding Interactivity

Some things on the screen change in response to what the user does. For example, clicking an image gallery switches the active image. In React, data that changes over time is called *state*. You can add state to any component and update it when you need to. In this chapter, you'll learn how to write components that handle interactions, update their state, and show different output over time.

> **In this chapter**
>
> - How to handle user-initiated events
> - How to make components "remember" information with state
> - How React updates the UI in two phases
> - Why state doesn't update right after you change it
> - How to queue multiple state updates
> - How to update an object in state
> - How to update an array in state

## Responding to events

React lets you add *event handlers* to your JSX. Event handlers are your own functions. React calls them when the user clicks, hovers, focuses form inputs, and so on.

Built-in components like `<button>` only support built-in browser events like `onClick`. You can also create your own components and give their event handler props any names that fit your app.

```jsx
export default function App() {
  return (
    <Toolbar
      onPlayMovie={() => alert('Playing!')}
      onUploadImage={() => alert('Uploading!')}
    />
  );
}

function Toolbar({ onPlayMovie, onUploadImage }) {
  return (
    <div>
      <Button onClick={onPlayMovie}>Play Movie</Button>
      <Button onClick={onUploadImage}>Upload Image</Button>
    </div>
  );
}

function Button({ onClick, children }) {
  return <button onClick={onClick}>{children}</button>;
}
```

Notice that you *pass* the function, `onClick={onPlayMovie}`, instead of *calling* it, `onClick={onPlayMovie()}`. React calls your handler only when the event happens.

## State: a component's memory

Components often need to change what's on the screen as a result of an interaction. Typing into a form should update the input field. Clicking "next" in an image carousel should change which image is shown. Clicking "buy" should put a product in the shopping cart. Components need to "remember" things: the current input value, the current image, the shopping cart. In React, this kind of component-specific memory is called *state*.

You add state to a component with the `useState` Hook. *Hooks* are special functions that let your components use React features. `useState` declares a state variable. It takes the initial state and returns a pair of values: the current state and a setter function to update it.

```jsx
import { useState } from 'react';

export default function Gallery() {
  const [index, setIndex] = useState(0);
  const [showMore, setShowMore] = useState(false);

  function handleNextClick() {
    setIndex(index + 1);
  }

  function handleMoreClick() {
    setShowMore(!showMore);
  }

  return (
    <>
      <button onClick={handleNextClick}>Next</button>
      <h3>Image {index + 1}</h3>
      <button onClick={handleMoreClick}>
        {showMore ? 'Hide' : 'Show'} details
      </button>
      {showMore && <p>Details about this image.</p>}
    </>
  );
}
```

State is local to a component instance. If you render the same component twice, each copy has its own fully isolated state. Changing one does not affect the other.

## Render and commit

Before your components appear on the screen, React has to render them. Knowing the steps in this process helps you think about how your code runs and explain its behavior.

Think of your components as cooks in a kitchen putting together tasty dishes from ingredients. React is the waiter who takes requests from customers and brings them their orders. Requesting and serving UI has three steps:

1. **Triggering** a render (delivering the diner's order to the kitchen)
2. **Rendering** the component (preparing the order in the kitchen)
3. **Committing** to the DOM (placing the order on the table)

A render happens for two reasons: the component's initial render, or an update to its state (or an ancestor's state). After rendering, React changes the DOM only where the output actually differs from the previous render.

## State as a snapshot

Unlike regular JavaScript variables, React state behaves more like a snapshot. Setting it does not change the state variable you already have. Instead, it triggers a re-render.

```jsx
console.log(count);  // 0
setCount(count + 1); // Request a re-render with 1
console.log(count);  // Still 0!
```

This behavior helps you avoid subtle bugs. During a single render, the value of a state variable never changes, even if the code in an event handler is asynchronous. Every event handler "sees" the state from the render that created it.

## Queueing a series of state updates

Because of this, the following component may surprise you. Clicking the button only increments the score once:

```jsx
function increment() {
  setScore(score + 1);
  setScore(score + 1);
  setScore(score + 1);
}
```

Each call uses the `score` from the current render, so all three calls amount to `setScore(0 + 1)`. React waits until all the code in the event handler has run before processing your state updates. This is called *batching*.

To update the same state variable several times before the next render, pass an *updater function* that computes the next state from the previous one:

```jsx
function increment() {
  setScore(s => s + 1);
  setScore(s => s + 1);
  setScore(s => s + 1);
}
```

React queues these functions and runs them in order during the next render, so the score goes up by three.

## Updating objects in state

State can hold any kind of JavaScript value, including objects. But you shouldn't change objects that you hold in React state directly. Instead, when you want to update an object, create a new one (or make a copy of an existing one), and then set the state to use that copy.

Usually, you will use the `...` spread syntax to copy the objects and arrays you want to change:

```jsx
const [person, setPerson] = useState({
  name: 'Niki de Saint Phalle',
  artwork: { title: 'Blue Nana', city: 'Hamburg' }
});

function handleCityChange(e) {
  setPerson({
    ...person,
    artwork: {
      ...person.artwork,
      city: e.target.value
    }
  });
}
```

If copying objects in code gets tedious, you can use a library like Immer to reduce the repetitive code.

## Updating arrays in state

Arrays are another kind of mutable JavaScript object you can store in state, and you should treat them as read-only. Just like with objects, when you want to update an array stored in state, you need to create a new one (or make a copy of an existing one), and then set state to use the new array.

| | Avoid (mutates the array) | Prefer (returns a new array) |
|---|---|---|
| Adding | `push`, `unshift` | `concat`, `[...arr]` spread |
| Removing | `pop`, `shift`, `splice` | `filter`, `slice` |
| Replacing | `splice`, `arr[i] = ...` | `map` |
| Sorting | `reverse`, `sort` | copy the array first |

```jsx
setArtists([...artists, { id: nextId++, name }]);           // add
setArtists(artists.filter(a => a.id !== artist.id));         // remove
setArtists(artists.map(a => a.id === id ? { ...a, done } : a)); // update
```

## What's next?

Head over to **Responding to Events** to start reading this chapter page by page.

Or, if you're already familiar with these topics, why not read about **Managing State**?
