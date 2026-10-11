# Sharing State Between Components

<Intro>

Sometimes you want the state of two components to always change together. To do that, remove the state from both of them, move it to their closest common parent, and pass it down to them through props. This is called *lifting state up*, and it's one of the most common things you'll do when writing React code.

</Intro>

<YouWillLearn>

- How to share state between components by lifting it up
- What controlled and uncontrolled components are
- Why each piece of state should have a single "source of truth"

</YouWillLearn>

## Lifting state up by example {/*lifting-state-up-by-example*/}

In this example, a parent `FAQ` component renders two separate `Question` components:

- `FAQ`
  - `Question`
  - `Question`

Each `Question` has a heading and an answer. A "Show answer" button lets the user expand it:

```js
import { useState } from 'react';

function Question({ title, children }) {
  const [isOpen, setIsOpen] = useState(false);
  return (
    <section className="question">
      <h3>{title}</h3>
      {isOpen ? (
        <p>{children}</p>
      ) : (
        <button onClick={() => setIsOpen(true)}>
          Show answer
        </button>
      )}
    </section>
  );
}

export default function FAQ() {
  return (
    <>
      <h2>Frequently asked questions</h2>
      <Question title="How long does shipping take?">
        Most orders arrive within three to five business days.
      </Question>
      <Question title="Can I return an item?">
        Yes, you can return any unused item within 30 days.
      </Question>
    </>
  );
}
```

Pressing the button on one question doesn't affect the other. Each one is independent.

Now suppose the design changes, and only one answer should be visible at a time. When you expand the second answer, the first one should collapse. How would you do that?

To coordinate these two questions, you need to "lift their state up" to a parent component in three steps:

1. **Remove** the state from the child components.
2. **Pass** hardcoded data from the common parent.
3. **Add** state to the common parent and pass it down together with the event handlers.

This lets the `FAQ` component coordinate both `Question`s and expand only one at a time.

### Step 1: Remove state from the child components {/*step-1-remove-state-from-the-child-components*/}

You'll give control of the `Question`'s `isOpen` to its parent component. That means the parent will pass `isOpen` to the `Question` as a prop. Start by **removing this line** from the `Question` component:

```js
const [isOpen, setIsOpen] = useState(false);
```

Then add `isOpen` to the `Question`'s list of props instead:

```js
function Question({ title, children, isOpen }) {
  // ...
```

Now the `Question`'s parent can *control* `isOpen` by passing it down as a prop. On the other hand, the `Question` component no longer controls the value of `isOpen` itself. It's up to the parent.

### Step 2: Pass hardcoded data from the common parent {/*step-2-pass-hardcoded-data-from-the-common-parent*/}

To lift state up, you need to find the closest common parent of *both* child components you want to coordinate. Here, that's the `FAQ` component. It sits above both questions and can control their props, so it becomes the "source of truth" for which answer is currently visible.

Make the `FAQ` component pass hardcoded values of `isOpen` (for example, `true`) to both questions:

```js
export default function FAQ() {
  return (
    <>
      <h2>Frequently asked questions</h2>
      <Question title="How long does shipping take?" isOpen={true}>
        Most orders arrive within three to five business days.
      </Question>
      <Question title="Can I return an item?" isOpen={true}>
        Yes, you can return any unused item within 30 days.
      </Question>
    </>
  );
}
```

Try changing the hardcoded `isOpen` values in the `FAQ` component and see what happens on the screen.

### Step 3: Add state to the common parent {/*step-3-add-state-to-the-common-parent*/}

Lifting state up often changes what you're storing as state.

In this case, only one question should be open at a time. So instead of storing a boolean for each question, the `FAQ` component should keep track of *which* question is open. You can use a number for the index of the open question:

```js
const [openIndex, setOpenIndex] = useState(0);
```

When `openIndex` is `0`, the first question is open. When it's `1`, the second one is.

Pressing the "Show answer" button in either `Question` needs to change the index in `FAQ`. A `Question` can't set `openIndex` directly because that state is defined inside `FAQ`. The `FAQ` component needs to *explicitly allow* the `Question` to change its state by **passing an event handler down as a prop**:

```js
import { useState } from 'react';

function Question({ title, children, isOpen, onShow }) {
  return (
    <section className="question">
      <h3>{title}</h3>
      {isOpen ? (
        <p>{children}</p>
      ) : (
        <button onClick={onShow}>
          Show answer
        </button>
      )}
    </section>
  );
}

export default function FAQ() {
  const [openIndex, setOpenIndex] = useState(0);
  return (
    <>
      <h2>Frequently asked questions</h2>
      <Question
        title="How long does shipping take?"
        isOpen={openIndex === 0}
        onShow={() => setOpenIndex(0)}
      >
        Most orders arrive within three to five business days.
      </Question>
      <Question
        title="Can I return an item?"
        isOpen={openIndex === 1}
        onShow={() => setOpenIndex(1)}
      >
        Yes, you can return any unused item within 30 days.
      </Question>
    </>
  );
}
```

That's it! Lifting state up is complete. Moving state into the common parent let you coordinate the two questions. Using the open index instead of two separate "is open" flags guarantees that only one answer is visible at any time. And passing the event handler down let each child change the parent's state.

Here's what happens when you press the second question's button:

1. The `Question` calls its `onShow` prop.
2. The `FAQ` component's handler calls `setOpenIndex(1)`.
3. React re-renders `FAQ` with `openIndex` set to `1`.
4. The first `Question` gets `isOpen={false}`, and the second gets `isOpen={true}`.

<DeepDive>

#### Controlled and uncontrolled components {/*controlled-and-uncontrolled-components*/}

It's common to call a component with some local state "uncontrolled". For example, the first version of `Question` with its own `isOpen` state variable was uncontrolled because its parent couldn't change whether it was open.

On the other hand, you might say a component is "controlled" when the important information in it is driven by props instead of its own local state. This lets the parent component fully decide how it behaves. The final `Question` component with the `isOpen` prop is controlled by the `FAQ` component.

Uncontrolled components are easier to use inside their parents because they need less configuration. But they're less flexible when you want to coordinate them. Controlled components are as flexible as possible, but the parent has to configure them fully with props.

In practice, "controlled" and "uncontrolled" aren't strict technical terms. Each component usually has a mix of local state and props. Still, they're a useful way to talk about how components are designed and what they can do.

When you write a component, think about which information in it should be controlled through props, and which should be uncontrolled through state. You can always change your mind and refactor later.

</DeepDive>

## A single source of truth for each state {/*a-single-source-of-truth-for-each-state*/}

In a React application, many components will have their own state. Some state may "live" close to the leaf components (the components at the bottom of the tree), like inputs. Other state may "live" closer to the top of the app. For example, even client-side routing libraries are usually built by storing the current route in React state and passing it down through props.

**For each unique piece of state, you choose the component that "owns" it.** This principle is also known as having a ["single source of truth".](https://en.wikipedia.org/wiki/Single_source_of_truth) It doesn't mean that all state lives in one place. It means that for _each_ piece of state, there is a _specific_ component that holds that piece of information. Instead of copying shared state between components, *lift it up* to their common shared parent, and *pass it down* to the children that need it.

Your app will change as you work on it. It's common to move state down, or back up, while you're still figuring out where each piece of state "lives". This is all part of the process.

To see what this feels like in practice with a few more components, read [Thinking in React.](/learn/thinking-in-react)

<Recap>

- When you want to coordinate two components, move their state to their common parent.
- Then pass the information down through props from their common parent.
- Finally, pass the event handlers down so that the children can change the parent's state.
- It's useful to think of components as "controlled" (driven by props) or "uncontrolled" (driven by state).

</Recap>

---

**Notes:**
- **Format:** The page uses the conventions of the react.dev source files: `<Intro>`, `<YouWillLearn>`, `<DeepDive>` and `<Recap>` blocks, plus `{/*anchor*/}` heading IDs. If you're using plain Markdown, delete those tags and anchor IDs.
- **Content:** The text and the shipping/returns FAQ example are new writing in the React docs style, not a copy of the real react.dev page. The body runs to about 900 words, not counting code.
