# Managing State

As your application grows, it helps to be intentional about how your state is organized and how data flows between your components. Redundant or duplicate state is a common source of bugs. In this chapter, you'll learn how to structure your state well, how to keep state update logic maintainable, and how to share state between distant components.

## In this chapter

- How to think about UI changes as state changes
- How to structure state well
- How to "lift state up" to share it between components
- How to control whether the state gets preserved or reset
- How to consolidate complex state logic in a function
- How to pass information without "prop drilling"
- How to scale state management as your app grows

## Reacting to input with state

With React, you won't modify the UI from code directly. For example, you won't write commands like "disable the button", "enable the button", "show the success message", and so on. Instead, you will describe the UI you want to see for the different visual states of your component ("initial state", "typing state", "success state"), and then trigger the state changes in response to user input. This is similar to how designers think about UI.

Here is a quiz form built using React. Note how it uses the `status` state variable to determine whether to enable or disable the submit button, and whether to show the success message instead.

```js
import { useState } from 'react';

export default function Form() {
  const [answer, setAnswer] = useState('');
  const [status, setStatus] = useState('typing');

  if (status === 'success') {
    return <h1>That's right!</h1>;
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setStatus('submitting');
    try {
      await submitForm(answer);
      setStatus('success');
    } catch (err) {
      setStatus('typing');
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <textarea
        value={answer}
        onChange={(e) => setAnswer(e.target.value)}
        disabled={status === 'submitting'}
      />
      <button disabled={answer.length === 0 || status === 'submitting'}>
        Submit
      </button>
    </form>
  );
}
```

> **Learn how to think about UI as state** to see how to approach an interaction with this mindset.

## Choosing the state structure

Structuring state well can make the difference between a component that is pleasant to modify and debug, and one that is a constant source of bugs. The most important principle is that state shouldn't contain redundant or duplicated information. If there's unnecessary state, it's easy to forget to update it, and introduce bugs.

For example, this form has a redundant `fullName` state variable:

```js
const [firstName, setFirstName] = useState('');
const [lastName, setLastName] = useState('');
const [fullName, setFullName] = useState('');
```

You can remove it and calculate `fullName` while rendering the component:

```js
const [firstName, setFirstName] = useState('');
const [lastName, setLastName] = useState('');
const fullName = firstName + ' ' + lastName;
```

This may seem like a small change, but many bugs in React apps are fixed this way. Other principles worth following include grouping related state, avoiding contradictions in state, avoiding deeply nested state, and avoiding duplication of objects between pieces of state.

> **Read Choosing the State Structure** to learn how to design state variables well.

## Sharing state between components

Sometimes, you want the state of two components to always change together. To do it, remove state from both of them, move it to their closest common parent, and then pass it down to them via props. This is known as *lifting state up*, and it's one of the most common things you will do writing React code.

In this example, only one panel should be active at a time. To achieve this, instead of keeping the active state inside each panel, the parent component holds the state and specifies the props for its children.

```js
import { useState } from 'react';

export default function Accordion() {
  const [activeIndex, setActiveIndex] = useState(0);
  return (
    <>
      <Panel
        title="About"
        isActive={activeIndex === 0}
        onShow={() => setActiveIndex(0)}
      >
        A short description of the project.
      </Panel>
      <Panel
        title="Etymology"
        isActive={activeIndex === 1}
        onShow={() => setActiveIndex(1)}
      >
        Where the name comes from.
      </Panel>
    </>
  );
}

function Panel({ title, children, isActive, onShow }) {
  return (
    <section className="panel">
      <h3>{title}</h3>
      {isActive ? <p>{children}</p> : <button onClick={onShow}>Show</button>}
    </section>
  );
}
```

> **Read Sharing State Between Components** to learn how to lift state up and keep components in sync.

## Preserving and resetting state

When you re-render a component, React needs to decide which parts of the tree to keep and update, and which parts to discard or recreate from scratch. In most cases, React's automatic behavior works well enough. By default, React preserves the parts of the tree that "match up" with the previously rendered component tree.

However, sometimes this is not what you want. You can force React to reset a component's state by passing it a different `key`:

```js
<Chat key={contact.id} contact={contact} />
```

Now, switching between recipients will always reset the draft message, because each contact gets its own `Chat` instance.

> **Read Preserving and Resetting State** to learn the lifetime of state and how to control it.

## Extracting state logic into a reducer

Components with many state updates spread across many event handlers can get overwhelming. For these cases, you can consolidate all the state update logic outside your component in a single function, called a *reducer*. Your event handlers become concise because they only specify the user "actions". At the bottom of the file, the reducer function specifies how the state should update in response to each action.

```js
function tasksReducer(tasks, action) {
  switch (action.type) {
    case 'added':
      return [...tasks, { id: action.id, text: action.text, done: false }];
    case 'deleted':
      return tasks.filter((t) => t.id !== action.id);
    default:
      throw Error('Unknown action: ' + action.type);
  }
}
```

Inside your component, you call it with `useReducer`:

```js
const [tasks, dispatch] = useReducer(tasksReducer, initialTasks);

function handleDeleteTask(taskId) {
  dispatch({ type: 'deleted', id: taskId });
}
```

> **Read Extracting State Logic into a Reducer** to learn how to consolidate logic in a reducer function.

## Passing data deeply with context

Usually, you will pass information from a parent component to a child component via props. But passing props can become inconvenient if you need to pass some prop through many components, or if many components need the same information. Context lets the parent component make some information available to any component in the tree below it, no matter how deep, without passing it explicitly through props.

```js
import { createContext, useContext } from 'react';

const LevelContext = createContext(1);

function Heading({ children }) {
  const level = useContext(LevelContext);
  return <h1 className={`h${level}`}>{children}</h1>;
}
```

Context works well for values such as the current theme, the signed-in user, or the active language. It's tempting to reach for it whenever props feel tedious, but try extracting components and passing `children` first.

> **Read Passing Data Deeply with Context** to learn about using context as an alternative to passing props.

## Scaling up with reducer and context

Reducers let you consolidate a component's state update logic. Context lets you pass information deep down to other components. You can combine reducers and context together to manage the state of a complex screen.

With this approach, a parent component with complex state manages it with a reducer. Other components anywhere deep in the tree can read its state via context. They can also dispatch actions to update that state.

> **Read Scaling Up with Reducer and Context** to learn how state management scales in a growing app.

## What's next?

Head over to **Reacting to Input with State** to start reading this chapter page by page.

Alternatively, if you're already familiar with these topics, you could read about **Escape Hatches**.
