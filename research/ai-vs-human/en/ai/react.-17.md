# Introduction

React is a JavaScript library for building user interfaces. It lets you split a screen into small, reusable pieces called components, describe what each piece should show for its current data, and keep the page in sync when that data changes. This page introduces the core ideas you will use throughout the rest of the documentation.

## Why React?

Most interfaces are built from repeated patterns. A social feed has many posts with the same layout. A shopping cart has many line items with the same controls. Building each one by hand, then updating the page manually whenever the data changes, becomes error-prone very quickly. React addresses this in two ways.

First, it encourages composition. You write a function that returns the markup for one piece of UI, then reuse it wherever you need it. Larger screens are assembled from smaller pieces, and each piece can be understood on its own.

Second, it is declarative. Instead of writing step-by-step instructions for changing the page ("find this element, remove that class, append a new node"), you describe what the UI should look like for the current data. React works out how to move from the previous screen to the next one.

## Components

A component is a JavaScript function that returns JSX. Component names start with a capital letter so React can tell them apart from ordinary HTML tags.

```jsx
function Greeting({ name }) {
  return <h1>Hello, {name}!</h1>;
}

export default function App() {
  return (
    <main>
      <Greeting name="Ada" />
      <Greeting name="Grace" />
    </main>
  );
}
```

Here `Greeting` is defined once and used twice. Each use receives different props, which are the inputs a parent passes to a child. Components nest inside one another to form a tree, with the root component at the top. Props flow down that tree from parent to child. Props behave like function arguments: a child reads them but should not modify them.

## JSX

JSX is a syntax extension that looks like HTML inside JavaScript. You do not have to use it to write React, but most React code uses it because it keeps markup close to the logic that produces it. A few differences from HTML matter from the start:

- Use `className` instead of `class`, because `class` is a reserved word in JavaScript.
- Every tag must be closed, including self-closing tags such as `<img />`.
- Curly braces embed any JavaScript expression, such as `{user.name}` or `{items.length > 0 && <List />}`.
- A component must return a single root element. Wrap several elements in a `<div>` or in a fragment written as `<>...</>`.

Build tools compile JSX into ordinary function calls before the code runs in the browser, so the final output is plain JavaScript.

## State: data that changes over time

Props let a parent configure a child, but many interfaces also need to remember things that change while someone uses them. A menu may be open or closed, a search box holds whatever the user typed, and a tab bar has a selected tab. React calls this kind of information state. You declare it with the `useState` Hook:

```jsx
import { useState } from 'react';

export default function Counter() {
  const [count, setCount] = useState(0);

  return (
    <button onClick={() => setCount(count + 1)}>
      You clicked {count} times
    </button>
  );
}
```

When you call the setter function, React re-renders the component with the new value. You never update the button's text yourself. You change the state, and the output follows from it.

Hooks are functions whose names begin with `use`. They connect a component to React features such as state, context, and side effects. Call Hooks only at the top level of a component or of another Hook, never inside loops, conditions, or nested functions. This rule lets React match each Hook call to the same piece of state across renders.

## Thinking about rendering

A helpful mental model is to treat rendering as a calculation. Given the current props and state, a component returns the UI it should show. While doing so, it should not change anything outside itself. Keeping rendering free of side effects makes components predictable and easier to test, and it lets React call them more than once when it needs to.

Actions that do affect the outside world, such as fetching data, subscribing to events, or changing the document title, belong in event handlers or in Effects. You will meet both later in this documentation.

## What you will learn next

The rest of the documentation builds on these ideas in order:

1. **Describing the UI**, covering JSX, components, and props.
2. **Adding interactivity**, covering event handlers and state that responds to user input.
3. **Managing state**, covering how to organize state and share it across several components.
4. **Sharing data deeply**, covering context and reducers for larger applications.
5. **Synchronizing with external systems**, covering Effects for network requests, subscriptions, and browser APIs.

Each section includes small examples you can run in a sandbox or in your own project. You do not need to master everything before you start. Build a small app, experiment with the examples, and the concepts will become familiar quickly.

---

*Note: This is an original page written in the style of the React documentation, not the official text. For the current official content, see react.dev.*
