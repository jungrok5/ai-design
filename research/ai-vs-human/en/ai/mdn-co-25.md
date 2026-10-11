# JavaScript frameworks and libraries

> **Summary:** JavaScript libraries and frameworks are reusable collections of code that help developers build web applications more quickly. A *library* provides functions that your code calls when it needs them. A *framework* provides the overall structure of an application and calls your code at defined points. This article explains the difference, outlines the main categories, and offers guidance on choosing one.

## Overview

JavaScript was originally designed to add small amounts of interactivity to documents. As web applications grew into full-featured software, developers needed shared solutions for common problems: updating the page when data changes, routing between views, managing state, making network requests, and working consistently across browsers. Libraries and frameworks emerged to address these needs.

Both are third-party code that you add to a project, but they differ in how they shape your code.

## Libraries and frameworks

### Libraries

A library is a collection of functions and utilities that your code calls. You stay in control of the program's flow. For example, you might use a date-formatting library in one part of an application and leave the rest of the architecture unchanged.

jQuery was once one of the most widely used libraries. It simplified DOM selection, event handling, and AJAX requests across browsers that implemented these features inconsistently. Many modern browser APIs now provide equivalent functionality natively, so the need for jQuery has declined, although it still appears on many existing sites.

### Frameworks

A framework supplies the structure of an application. It defines how code is organized and calls your code through mechanisms such as components, lifecycle hooks, or route handlers. This is often described as *inversion of control*: instead of your code calling the framework, the framework calls your code.

Frameworks typically include conventions about:

- How user interface components are defined and composed.
- How data flows through the application and how state is updated.
- How pages or views are routed.
- How the project is built, tested, and deployed.

The line between the two is not always sharp. Many projects called "frameworks" are really libraries with optional extensions, and developers often combine several libraries to build something that behaves like a framework.

## Categories

Most client-side tools fall into a few broad categories:

| Category | Purpose | Examples |
| --- | --- | --- |
| UI libraries | Build reusable interface components and keep the DOM in sync with data | React, Preact, Solid |
| Full frameworks | Provide routing, state management, build tooling, and conventions | Angular, Vue, Svelte |
| Meta-frameworks | Add server rendering, file-based routing, and deployment on top of a UI library | Next.js, Nuxt, SvelteKit |
| Web component libraries | Create standards-based custom elements | Lit, Stencil |
| Utility libraries | Provide helpers for data, dates, or animation | Lodash, date-fns, GSAP |

Category boundaries shift over time, and many tools span more than one row.

## Reactive rendering

Most modern UI tools share a central idea: the interface is a function of application state. When state changes, the library or framework updates only the parts of the page that depend on that state. The following example, written with React, shows the pattern:

```jsx
import { useState } from "react";

export function Counter() {
  const [count, setCount] = useState(0);

  return (
    <button onClick={() => setCount(count + 1)}>
      Clicked {count} times
    </button>
  );
}
```

Other tools express the same idea differently. Vue uses reactive proxies, Svelte compiles components into efficient imperative code at build time, and Solid tracks fine-grained dependencies. The goal is the same: keep the displayed page consistent with the underlying data while minimizing manual DOM work.

## Choosing a tool

No single tool is best for every project. When evaluating options, consider:

- **The size and lifespan of the project.** Long-lived applications benefit from stable APIs, clear conventions, and a large ecosystem.
- **Team experience.** Familiarity often matters more than marginal performance differences.
- **Bundle size and performance requirements.** A small widget may not justify a large framework.
- **Rendering needs.** Content-heavy sites may benefit from server-side rendering or static generation, which meta-frameworks provide.
- **Ecosystem and hiring.** Mature tools have more documentation, plugins, and community answers.
- **Standards alignment.** Relying more on native platform features reduces long-term dependence on any single project.

For a small enhancement to an existing page, plain JavaScript and native browser APIs are often sufficient. Adding a library is worthwhile when it solves a problem you would otherwise have to solve yourself. A framework is worthwhile when the application is large enough to benefit from its structure.

## Dependencies and trade-offs

Every dependency carries costs. It adds download size, requires updates, may introduce security vulnerabilities, and ties your project to its maintainers' decisions. Before adopting a tool, check its release history, license, open issues, and browser support. Lock files and regular dependency audits help manage these risks over time.

## See also

- [Learn web development](https://developer.mozilla.org/en-US/docs/Learn_web_development)
- [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
- [Web components](https://developer.mozilla.org/en-US/docs/Web/API/Web_components)
- [Document Object Model (DOM)](https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model)
