No docs connector is available in this session. The ToolSearch returned only unrelated tools (connector suggestions, cron, worktrees, artifact comments), so I can't use the docs skill's workflow. I also can't write a file here, so the Markdown is below.

```markdown
# Keeping Components Pure

Purity is what makes React predictable. A pure component, given the same inputs, always returns the same JSX. It does not change anything that existed before it rendered, and it does not depend on values that might change between renders. When your components follow these rules, React can safely render them again, skip work it doesn't need to repeat, and keep the interface consistent.

## What is purity?

A pure function has two properties:

- **It minds its own business.** It does not modify objects or variables that existed before the call.
- **Same inputs, same output.** Given the same arguments, it always returns the same result.

React components are functions that take props, state, and context as input and return JSX. Written as pure functions, they look like this:

```jsx
function Recipe({ drinkers }) {
  return (
    <ol>
      <li>Boil {drinkers} cups of water.</li>
      <li>Add {drinkers} spoons of tea and {0.5 * drinkers} spoons of spice.</li>
      <li>Add {0.5 * drinkers} cups of milk and sugar to taste.</li>
    </ol>
  );
}
```

Render `<Recipe drinkers={4} />` twice and you get the same output both times. That predictability is the goal.

## Rendering is a calculation

Rendering should only calculate what the screen will show. Anything that changes the outside world is a **side effect**: updating the document title, starting a timer, writing to a database, sending a network request. Side effects belong in event handlers or in Effects, never in the body of a component.

Consider a component that mutates a module-level variable:

```jsx
let guestCount = 0;

function Guest() {
  guestCount = guestCount + 1; // Side effect during render
  return <p>Guest #{guestCount}</p>;
}
```

Rendering `<Guest />` three times produces "Guest #1", "Guest #2", and "Guest #3". The output depends on how many times the component has already run, so it cannot be predicted from its props. Strict Mode intentionally renders components twice in development to expose this kind of bug, and concurrent rendering may pause and retry work, so the problem gets worse over time.

A pure version receives the number from its parent:

```jsx
function Guest({ number }) {
  return <p>Guest #{number}</p>;
}

function GuestList() {
  return (
    <>
      <Guest number={1} />
      <Guest number={2} />
      <Guest number={3} />
    </>
  );
}
```

Now each guest's output depends only on what it was given.

## Local mutation is fine

Not every mutation is a problem. A component may change objects it created during the same render, because nothing outside the component can observe the change. For example, this list builder is pure even though it calls `push` and `sort`:

```jsx
function SortedList({ items }) {
  const sorted = [];
  for (const item of items) {
    sorted.push(item.toUpperCase());
  }
  sorted.sort();
  return (
    <ul>
      {sorted.map((s) => <li key={s}>{s}</li>)}
    </ul>
  );
}
```

The array `sorted` is brand new on every render, so changing it is safe. The rule is about ownership: if an object existed before rendering, do not modify it. Props in particular should be treated as read-only, as if they were frozen.

## Props and state are snapshots

Each render receives its own snapshot of props and state. Do not mutate them. If a child needs to change something its parent provided, it should call a callback the parent passed down:

```jsx
function Counter({ count, onIncrement }) {
  return <button onClick={onIncrement}>Count: {count}</button>;
}
```

State follows the same rule. Calling a state setter with a new value tells React to schedule a render with that value. Mutating an existing state object changes what the current snapshot shows without telling React anything happened, so the screen can fall out of sync. Replace the object instead of editing it in place.

## Where changes belong

Some changes must happen. The two correct places for them are:

- **Event handlers**, which run in response to a user action such as a click or a keystroke. Handlers are never called during rendering, so they have no purity requirement.
- **Effects**, which synchronize a component with something outside React after the screen has updated. Use them to subscribe to a connection, set up a timer, or update the document title.

If clicking a button should increase a counter, put the update in the click handler. If the document title should match the counter, put that in an Effect.

> **Pitfall:** Do not read or write `ref.current` during rendering. Refs are an escape hatch for values that are not part of the calculation. Touch them only in event handlers or Effects, because reading a ref during render makes the output depend on something React does not track.

## Summary

- A component should be a calculation from its props, state, and context.
- Do not modify objects or variables that existed before the render started.
- Create new objects during rendering freely, since you own them.
- Put side effects in event handlers or Effects.
- Replace state instead of mutating it, so React knows a change happened.
```
