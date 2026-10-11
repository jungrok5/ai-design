---
title: Getting started with React
slug: Learn/Tools_and_testing/Client-side_JavaScript_frameworks/React_getting_started
page-type: learn-module-chapter
---

{{LearnSidebar}}

{{PreviousMenuNext("Learn/Tools_and_testing/Client-side_JavaScript_frameworks/Introduction", "Learn/Tools_and_testing/Client-side_JavaScript_frameworks/React_todo_list_beginning", "Learn/Tools_and_testing/Client-side_JavaScript_frameworks")}}

React is a JavaScript library for building user interfaces out of small, reusable pieces called components. In this article, you will set up a development environment, create a new project, and write your first component. You will also learn the core ideas behind the library.

<table>
  <tbody>
    <tr>
      <th scope="row">Prerequisites:</th>
      <td>
        Familiarity with HTML, CSS, and JavaScript fundamentals, and with
        using the command line. You also need Node.js installed.
      </td>
    </tr>
    <tr>
      <th scope="row">Objective:</th>
      <td>
        To set up a React project and understand components, JSX, props,
        and state.
      </td>
    </tr>
  </tbody>
</table>

## What is React?

React lets you describe what your interface should look like for a given state of your data. When the data changes, React works out the smallest set of changes needed and updates the {{Glossary("DOM")}} for you. This approach is called _declarative_ programming. You don't write step-by-step instructions to find elements and change them. You describe the result you want.

React applications are built from components. A component is a JavaScript function that returns a description of part of the user interface. Components can contain other components, so you can build complex pages from simple building blocks.

## Setting up your environment

React code needs a build step. Browsers don't understand {{Glossary("JSX")}}, the syntax most React projects use, so a tool must transform it into plain JavaScript. A build tool also bundles your files and provides a development server with live reloading.

### Prerequisites

You need [Node.js](https://nodejs.org/) and its package manager, npm. To check whether they are installed, open a terminal and run:

```bash
node --version
npm --version
```

If both commands print a version number, you are ready. Otherwise, install the current LTS release of Node.js and try again.

### Creating a new project

This guide uses [Vite](https://vite.dev/), a fast build tool that offers a React template. Run the following command:

```bash
npm create vite@latest moz-react -- --template react
```

Then move into the new folder, install the dependencies, and start the development server:

```bash
cd moz-react
npm install
npm run dev
```

The terminal prints a local address, usually `http://localhost:5173/`. Open it in your browser and you should see the starter page. Leave the server running. It reloads the page whenever you save a file.

> **Note:** Frameworks such as Next.js and React Router also build on React and add features like routing and server rendering. Starting with a plain Vite project helps you learn the core library first.

## Exploring the project

The generated project contains several files and folders. These are the most important:

- `index.html`: the single HTML page. It contains an empty `<div id="root">` element where React will render your application.
- `src/main.jsx`: the entry point. It finds the root element and tells React to render your top-level component into it.
- `src/App.jsx`: the top-level component, which you will edit first.
- `package.json`: lists your dependencies and the scripts you can run.

Open `src/main.jsx`. It looks something like this:

```jsx
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App.jsx";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
```

The `createRoot()` function connects React to the page. The `render()` method displays the `App` component inside the root element. `StrictMode` is an optional wrapper that runs extra checks during development to help you find problems.

## Writing your first component

Open `src/App.jsx` and replace its contents with the following:

```jsx
function App() {
  return (
    <main>
      <h1>Hello, React!</h1>
      <p>This is my first component.</p>
    </main>
  );
}

export default App;
```

Save the file and check your browser. The page updates immediately.

The `App` function looks like it returns HTML, but it returns JSX. JSX is a syntax extension that lets you write markup inside JavaScript. A build tool converts each tag into a function call. JSX has a few rules that differ from HTML:

- A component must return a single parent element. Wrap siblings in a `<div>`, or in an empty fragment (`<>…</>`) if you don't want an extra element in the DOM.
- Every tag must be closed. Write `<br />` and `<img />`, not `<br>` and `<img>`.
- Attribute names use camelCase. For example, `class` becomes `className`, and `tabindex` becomes `tabIndex`.
- You can insert JavaScript expressions with curly braces, such as `<p>{2 + 2}</p>`.

Component names must start with a capital letter. React uses this to tell your components apart from built-in HTML elements.

## Props: passing data to components

Components become reusable when you can customize them. You do this with _props_, short for properties. Props are passed to a component as attributes and arrive as an object in the first argument of the function.

Create a new file called `src/Greeting.jsx`:

```jsx
function Greeting({ name, mood = "happy" }) {
  return (
    <p>
      Hello, {name}! You seem {mood} today.
    </p>
  );
}

export default Greeting;
```

The function uses destructuring to pull `name` and `mood` out of the props object. The default value `"happy"` applies when no `mood` prop is given. Now use the component in `App.jsx`:

```jsx
import Greeting from "./Greeting.jsx";

function App() {
  return (
    <main>
      <h1>Hello, React!</h1>
      <Greeting name="Ada" />
      <Greeting name="Grace" mood="curious" />
    </main>
  );
}

export default App;
```

Each `Greeting` shows different text, even though the code is written once. Props are read-only. A component must never change its own props.

## State: making components interactive

Props pass data into a component. _State_ is data that a component manages itself and that changes over time. You create state with the `useState()` hook:

```jsx
import { useState } from "react";

function Counter() {
  const [count, setCount] = useState(0);

  return (
    <button type="button" onClick={() => setCount(count + 1)}>
      You clicked {count} times
    </button>
  );
}

export default Counter;
```

The `useState()` function takes an initial value and returns an array with two items: the current value and a function that updates it. When you call `setCount()`, React stores the new value and calls your component again to produce updated output. The button label changes without any manual DOM code.

Hooks are functions whose names start with `use`. Call them only at the top level of a component, never inside loops, conditions, or nested functions.

## Summary

In this article, you created a React project with Vite, explored its structure, and wrote components in JSX. You also learned how props configure a component and how state makes it interactive. These ideas underpin everything else in React.

In the next article, you will use them to begin building a to-do list application.

## See also

- [React documentation](https://react.dev/)
- [JSX in depth](https://react.dev/learn/writing-markup-with-jsx)
- [Vite guide](https://vite.dev/guide/)
- [Introduction to client-side frameworks](/en-US/docs/Learn/Tools_and_testing/Client-side_JavaScript_frameworks/Introduction)

{{PreviousMenuNext("Learn/Tools_and_testing/Client-side_JavaScript_frameworks/Introduction", "Learn/Tools_and_testing/Client-side_JavaScript_frameworks/React_todo_list_beginning", "Learn/Tools_and_testing/Client-side_JavaScript_frameworks")}}
