I've written the page below and kept it in this reply instead of publishing it as a hosted page, since a page styled as React's official docs could pass for the real thing if shared. It uses the MDX components that react.dev pages use (`<Intro>`, `<YouWillLearn>`, `<Sandpack>`, `<LearnMore>`). The body text is about 900 words, not counting code.

```markdown
---
title: Describing the UI
---

<Intro>

React is a JavaScript library for rendering user interfaces (UI). UI is built from small units like buttons, text, and images. React lets you combine them into reusable, nestable *components*. From web sites to phone apps, everything on the screen can be broken down into components. In this chapter, you'll learn to create, customize, and conditionally display React components.

</Intro>

<YouWillLearn isChapter={true}>

* [How to write your first React component](/learn/your-first-component)
* [When and how to create multi-component files](/learn/importing-and-exporting-components)
* [How to add markup to JavaScript with JSX](/learn/writing-markup-with-jsx)
* [How to use curly braces with JSX to access JavaScript functionality from your components](/learn/javascript-in-jsx-with-curly-braces)
* [How to configure components with props](/learn/passing-props-to-a-component)
* [How to conditionally render components](/learn/conditional-rendering)
* [How to render multiple components at a time](/learn/rendering-lists)
* [How to avoid confusing bugs by keeping components pure](/learn/keeping-components-pure)
* [Why understanding your UI as trees is useful](/learn/understanding-your-ui-as-a-tree)

</YouWillLearn>

## Your first component {/*your-first-component*/}

React applications are built from isolated pieces of UI called *components*. A React component is a JavaScript function that you can sprinkle with markup. Components can be as small as a button or as large as an entire page. Here is a `Gallery` component rendering three `Profile` components:

<Sandpack>

```js
function Profile() {
  return (
    <img
      src="https://i.imgur.com/MK3eW3As.jpg"
      alt="Katherine Johnson"
    />
  );
}

export default function Gallery() {
  return (
    <section>
      <h1>Amazing scientists</h1>
      <Profile />
      <Profile />
      <Profile />
    </section>
  );
}
```

</Sandpack>

<LearnMore path="/learn/your-first-component">

Read **[Your First Component](/learn/your-first-component)** to learn how to declare and use React components.

</LearnMore>

## Importing and exporting components {/*importing-and-exporting-components*/}

You can declare many components in one file, but large files can get difficult to navigate. To solve this, you can *export* a component into its own file, and then *import* that component from another file:

<Sandpack>

```js src/App.js hidden
import Gallery from './Gallery.js';

export default function App() {
  return <Gallery />;
}
```

```js src/Gallery.js active
import Profile from './Profile.js';

export default function Gallery() {
  return (
    <section>
      <h1>Amazing scientists</h1>
      <Profile />
      <Profile />
      <Profile />
    </section>
  );
}
```

```js src/Profile.js
export default function Profile() {
  return (
    <img
      src="https://i.imgur.com/QIrZWGIs.jpg"
      alt="Alan L. Hart"
    />
  );
}
```

</Sandpack>

<LearnMore path="/learn/importing-and-exporting-components">

Read **[Importing and Exporting Components](/learn/importing-and-exporting-components)** to learn how to split components into their own files.

</LearnMore>

## Writing markup with JSX {/*writing-markup-with-jsx*/}

Each React component is a JavaScript function that may contain some markup that React renders into the browser. React components use a syntax extension called JSX to represent that markup. JSX looks a lot like HTML, but it is a bit stricter and can display dynamic information.

If you paste existing HTML markup into a React component, it won't always work. That's because JSX requires you to close every tag, to return a single root element, and to write most attributes in camelCase:

```js
export default function TodoList() {
  return (
    <>
      <h1>Hedy Lamarr's Todos</h1>
      <img
        src="https://i.imgur.com/yXOvdOSs.jpg"
        alt="Hedy Lamarr"
        className="photo"
      />
      <ul>
        <li>Invent new traffic lights</li>
        <li>Rehearse a movie scene</li>
        <li>Improve spectrum technology</li>
      </ul>
    </>
  );
}
```

<LearnMore path="/learn/writing-markup-with-jsx">

Read **[Writing Markup with JSX](/learn/writing-markup-with-jsx)** to learn how to write valid JSX.

</LearnMore>

## JavaScript in JSX with curly braces {/*javascript-in-jsx-with-curly-braces*/}

JSX lets you write HTML-like markup inside a JavaScript file, keeping rendering logic and content in the same place. Sometimes you will want to add a little JavaScript logic or reference a dynamic property inside that markup. In this situation, you can use curly braces in your JSX to "open a window" to JavaScript:

```js
const person = {
  name: 'Gregorio Y. Zara',
  theme: {
    backgroundColor: 'black',
    color: 'pink'
  }
};

export default function TodoList() {
  return (
    <div style={person.theme}>
      <h1>{person.name}'s Todos</h1>
      <ul>
        <li>Improve the videophone</li>
        <li>Prepare aeronautics lectures</li>
      </ul>
    </div>
  );
}
```

Notice the double curly braces in `style={person.theme}`. The outer pair switches into JavaScript; the value inside is just an ordinary object.

<LearnMore path="/learn/javascript-in-jsx-with-curly-braces">

Read **[JavaScript in JSX with Curly Braces](/learn/javascript-in-jsx-with-curly-braces)** to learn how to access JavaScript data from JSX.

</LearnMore>

## Passing props to a component {/*passing-props-to-a-component*/}

React components use *props* to communicate with each other. Every parent component can pass some information to its child components by giving them props. Props might remind you of HTML attributes, but you can pass any JavaScript value through them, including objects, arrays, functions, and even JSX!

```js
function Avatar({ person, size }) {
  return (
    <img
      className="avatar"
      src={getImageUrl(person)}
      alt={person.name}
      width={size}
      height={size}
    />
  );
}

export default function Profile() {
  return (
    <Avatar
      size={100}
      person={{ name: 'Katsuko Saruhashi', imageId: 'YfeOqp2' }}
    />
  );
}
```

Props are read-only snapshots: a component receives new props when its parent re-renders, but it should never change the props it was given.

<LearnMore path="/learn/passing-props-to-a-component">

Read **[Passing Props to a Component](/learn/passing-props-to-a-component)** to learn how to pass and read props.

</LearnMore>

## Conditional rendering {/*conditional-rendering*/}

Your components will often need to display different things depending on different conditions. In React, you can conditionally render JSX using JavaScript syntax like `if` statements, `&&`, and the `? :` ternary operator.

In this example, the `&&` operator is used to render a checkmark only when an item is packed:

```js
function Item({ name, isPacked }) {
  return (
    <li className="item">
      {name} {isPacked && '✅'}
    </li>
  );
}

export default function PackingList() {
  return (
    <section>
      <h1>Sally Ride's Packing List</h1>
      <ul>
        <Item isPacked={true} name="Space suit" />
        <Item isPacked={true} name="Helmet with a golden leaf" />
        <Item isPacked={false} name="Photo of Tam" />
      </ul>
    </section>
  );
}
```

<LearnMore path="/learn/conditional-rendering">

Read **[Conditional Rendering](/learn/conditional-rendering)** to learn the different ways to render content conditionally.

</LearnMore>

## Rendering lists {/*rendering-lists*/}

You will often want to display multiple similar components from a collection of data. You can use JavaScript's `filter()` and `map()` with React to filter and transform your array of data into an array of components.

For each array item, you will need to specify a `key`. Usually, you will want to use an ID from the database as a `key`. Keys let React keep track of each item's place in the list even if the list changes.

```js
import { people } from './data.js';

export default function List() {
  const listItems = people.map(person =>
    <li key={person.id}>
      <b>{person.name}:</b> {person.profession}
    </li>
  );
  return (
    <article>
      <h1>Scientists</h1>
      <ul>{listItems}</ul>
    </article>
  );
}
```

<LearnMore path="/learn/rendering-lists">

Read **[Rendering Lists](/learn/rendering-lists)** to learn how to render a list of components, and how to choose a key.

</LearnMore>

## Keeping components pure {/*keeping-components-pure*/}

Some JavaScript functions are *pure.* A pure function:

* **Minds its own business.** It does not change any objects or variables that existed before it was called.
* **Same inputs, same output.** Given the same inputs, a pure function should always return the same result.

By strictly only writing your components as pure functions, you can avoid an entire class of baffling bugs and unpredictable behavior as your codebase grows. Here is an example of an impure component:

```js
let guest = 0;

function Cup() {
  // Bad: changing a preexisting variable!
  guest = guest + 1;
  return <h2>Tea cup for guest #{guest}</h2>;
}
```

You can make this component pure by passing a prop instead of modifying a variable declared outside of it:

```js
function Cup({ guest }) {
  return <h2>Tea cup for guest #{guest}</h2>;
}
```

<LearnMore path="/learn/keeping-components-pure">

Read **[Keeping Components Pure](/learn/keeping-components-pure)** to learn how to write components as pure, predictable functions.

</LearnMore>

## Your UI as a tree {/*your-ui-as-a-tree*/}

React uses trees to model the relationships between components and modules.

A React *render tree* is a representation of the parent and child relationship between components. Components near the top of the tree, near the root component, are considered top-level components. Components with no child components are leaf components. This categorization is useful for understanding data flow and rendering performance.

Modeling the relationship between JavaScript modules is another useful way to understand your app. We refer to it as a *module dependency tree*. Build tools often use a dependency tree to bundle all the relevant JavaScript code for the client to download and render. A large bundle size regresses user experience, so understanding the module dependency tree helps you debug such issues.

<LearnMore path="/learn/understanding-your-ui-as-a-tree">

Read **[Your UI as a Tree](/learn/understanding-your-ui-as-a-tree)** to learn how to create render and module dependency trees for a React app, and how they're useful mental models for improving user experience and performance.

</LearnMore>

## What's next? {/*whats-next*/}

Head over to [Your First Component](/learn/your-first-component) to start reading this chapter page by page!

Or, if you're already familiar with these topics, why not read about [Adding Interactivity](/learn/adding-interactivity)?
```
