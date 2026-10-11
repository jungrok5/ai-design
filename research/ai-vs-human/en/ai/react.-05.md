I couldn't save the file because the Write tool is disabled in this session, so the page is below as Markdown you can copy into a `.md` file. It's about 650 words of body text, with code samples counted separately.

````markdown
# Incremental Adoption

React does not need to own your entire page. You can adopt it gradually, one component at a time, inside an application that is otherwise written with another framework or with plain HTML. This approach lets you add interactive features to an existing site without a rewrite, and it lets a team learn React on a small surface before committing to it everywhere.

This page describes the main techniques for doing so. Each one relies on the same idea: React manages the DOM inside the nodes you give it, and leaves everything else alone.

## Rendering React into an existing element

To show a React component inside a DOM node that already exists on the page, create a root for that node and call `render` on it:

```jsx
// main.jsx
import { createRoot } from 'react-dom/client';
import CommentWidget from './CommentWidget.jsx';

const domNode = document.getElementById('comments');
const root = createRoot(domNode);
root.render(<CommentWidget />);
```

The surrounding HTML is unchanged. Any markup outside `#comments` remains under the control of your existing code, which may be a server template, a jQuery script, or another framework entirely.

React treats the node as its own. Anything placed inside it by other code will be overwritten on the next render, so do not share a node between React and other scripts. Give React an empty container dedicated to its component, and let the component decide what goes inside it.

## Creating several roots

A page can contain any number of roots. Each one is independent: it has its own component tree, its own state, and its own update cycle. This is useful when a page has several unrelated widgets, such as a search box in the header, a cart counter in the navigation, and a chart in the sidebar.

```jsx
const widgets = [
  { id: 'search-box', component: SearchBox },
  { id: 'cart-count', component: CartCount },
  { id: 'price-chart', component: PriceChart },
];

for (const { id, component: Component } of widgets) {
  const node = document.getElementById(id);
  if (node !== null) {
    createRoot(node).render(<Component />);
  }
}
```

Creating a root for each widget is cheap, but it is not free. If several widgets need to share state or context, consider placing them in a single root instead, so that they can communicate through props and context rather than through the DOM. Separate roots are best for widgets that are truly independent of one another.

## Sharing data between roots

Roots do not share a React context. A value provided in one root is invisible to components rendered by another. To pass information between them, use one of these approaches:

- Pass plain data into each root as props when you call `render`.
- Use a small external store, such as a module-level object with a subscribe function, that both roots read through `useSyncExternalStore`.
- Dispatch browser events on `window` or on a shared element, and listen for them in the other root.

Choose the simplest option that fits. Props work well for data that is known at startup. An external store suits state that changes over time, because every root that subscribes will update when the store changes.

A minimal store might look like this:

```js
// cartStore.js
let items = [];
const listeners = new Set();

export function getItems() {
  return items;
}

export function addItem(item) {
  items = [...items, item];
  listeners.forEach((listener) => listener());
}

export function subscribe(listener) {
  listeners.add(listener);
  return () => listeners.delete(listener);
}
```

A component in another root can then read the store:

```jsx
import { useSyncExternalStore } from 'react';
import { getItems, subscribe } from './cartStore.js';

export default function CartCount() {
  const items = useSyncExternalStore(subscribe, getItems);
  return <span>{items.length}</span>;
}
```

## Rendering outside the root with portals

Sometimes a component needs to render its output in a different part of the document, such as a modal that must sit at the end of `body` to escape a container's `overflow: hidden`. A portal does this while keeping the component in its original React tree:

```jsx
import { createPortal } from 'react-dom';

export default function Modal({ children }) {
  return createPortal(
    <div className="modal">{children}</div>,
    document.body
  );
}
```

Events from portal content still bubble through the React tree, not the DOM tree. A click inside the modal reaches handlers on its React ancestors, even though the modal is physically elsewhere in the document.

## Unmounting a root

When a widget is no longer needed, for example because the user navigated to another view, call `unmount` on its root. This runs cleanup for every effect and releases the state held by the component:

```js
root.unmount();
```

After unmounting, the node is empty. You can create a new root on it later if needed, but you should not call `render` on a root that has been unmounted. Unmounting is also the right time to remove any event listeners or timers that your non-React code attached to the same node.

## Pitfalls

- Do not call `createRoot` on the same node twice. React will warn you, and the second root will fight the first for control of the DOM.
- Do not render into `document.body` or `<html>` directly. React expects to own its container, and the rest of the document is shared with other code.
- Keep server-rendered markup and client roots in agreement. If your server sends HTML for a widget, hydrate it with `hydrateRoot` rather than `createRoot`, or React will discard the markup and render it again.

## Summary

Incremental adoption works because React is willing to be small. Pick one node, give it a root, and let the component take over that area. As the team grows comfortable, the roots can merge into larger trees, and shared state can move from ad hoc events into well-defined stores. Each step is optional, and the rest of the page keeps working throughout.
````
