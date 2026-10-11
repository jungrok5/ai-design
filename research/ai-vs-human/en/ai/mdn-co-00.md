```md
---
title: Event bubbling
slug: Learn_web_development/Core/Scripting/Event_bubbling
page-type: guide
---

{{PreviousMenuNext("Learn_web_development/Core/Scripting/Events", "Learn_web_development/Core/Scripting/Event_delegation", "Learn_web_development/Core/Scripting")}}

**Event bubbling** is the way events propagate through the DOM tree. After an event fires on a target element, it triggers handlers on that element. It then triggers handlers on the element's parent, then on the parent's parent, and so on, up to the root of the document. Understanding this behavior is essential for writing predictable event-driven code and for using patterns such as event delegation.

## The three phases of event propagation

When an event is dispatched on an element, it moves through the DOM in three phases:

1. **Capturing phase**: the event travels down from the {{domxref("Window")}} through each ancestor toward the target.
2. **Target phase**: the event reaches the element on which it occurred.
3. **Bubbling phase**: the event travels back up through the ancestors, in the reverse order, to the `window`.

By default, event listeners are registered for the bubbling phase. This is why, in most code, a listener on a parent element fires _after_ listeners on its children.

> [!NOTE]
> Not every event bubbles. For example, {{domxref("Element/focus_event", "focus")}}, {{domxref("Element/blur_event", "blur")}}, and {{domxref("HTMLElement/load_event", "load")}} do not bubble. You can check the {{domxref("Event.bubbles")}} property of an event object to find out whether it does.

## A simple example

Consider the following nested structure:

```html
<div id="outer">
  <div id="middle">
    <button id="inner">Click me</button>
  </div>
</div>
```

Now add a click listener to each element:

```js
const outer = document.querySelector("#outer");
const middle = document.querySelector("#middle");
const inner = document.querySelector("#inner");

outer.addEventListener("click", () => console.log("outer"));
middle.addEventListener("click", () => console.log("middle"));
inner.addEventListener("click", () => console.log("inner"));
```

When you click the button, the console logs the following:

```plain
inner
middle
outer
```

The event fires first on the button, the element that was actually clicked. It then bubbles up to `#middle` and finally to `#outer`. A single user action therefore results in three handler calls.

## Target and currentTarget

Inside a handler, two properties of the {{domxref("Event")}} object help you tell which element is which:

- {{domxref("Event.target")}} is the innermost element on which the event originated. It stays the same as the event bubbles.
- {{domxref("Event.currentTarget")}} is the element whose listener is currently running. It changes as the event moves up the tree.

```js
outer.addEventListener("click", (event) => {
  console.log(`target: ${event.target.id}`);
  console.log(`currentTarget: ${event.currentTarget.id}`);
});
```

If you click the button, the `#outer` listener logs `target: inner` and `currentTarget: outer`. This distinction is the foundation of event delegation, described below.

## Stopping propagation

Sometimes you don't want an event to reach ancestor elements. You can stop it by calling {{domxref("Event.stopPropagation()")}}:

```js
inner.addEventListener("click", (event) => {
  event.stopPropagation();
  console.log("inner");
});
```

With this change, clicking the button logs only `inner`. The listeners on `#middle` and `#outer` are never called.

A related method, {{domxref("Event.stopImmediatePropagation()")}}, does the same thing but also prevents any other listeners attached to the _same_ element from running.

Use these methods sparingly. Stopping propagation makes code harder to reason about, because other parts of your application, such as analytics scripts or components that close menus when you click outside them, may rely on seeing the event. In many cases there is a better solution, such as checking `event.target` inside the ancestor's handler.

> [!NOTE]
> Stopping propagation is not the same as preventing the default action. {{domxref("Event.preventDefault()")}} stops the browser's built-in behavior, such as following a link or submitting a form, but the event still bubbles.

## Listening during the capturing phase

You can listen during the capturing phase instead by passing the `capture` option to {{domxref("EventTarget.addEventListener()")}}:

```js
outer.addEventListener("click", () => console.log("outer (capture)"), {
  capture: true,
});
```

With this listener added, the capturing listener on `#outer` runs before any bubbling listener. The click on the button would now log `outer (capture)`, `inner`, `middle`, `outer`. Capturing is useful when an ancestor must react to an event before the target handles it, but it is needed far less often than bubbling.

## Event delegation

Bubbling makes a powerful pattern possible: **event delegation**. Instead of attaching a listener to every child element, you attach a single listener to a common ancestor and use `event.target` to work out which child triggered the event.

```html
<ul id="todo-list">
  <li>Buy milk</li>
  <li>Write documentation</li>
  <li>Review pull request</li>
</ul>
```

```js
const list = document.querySelector("#todo-list");

list.addEventListener("click", (event) => {
  const item = event.target.closest("li");
  if (item && list.contains(item)) {
    item.classList.toggle("done");
  }
});
```

This approach has several advantages:

- It uses less memory, because there is one listener rather than many.
- It works for elements added later. If your script appends a new `<li>` to the list, clicking it works immediately, with no additional setup.
- It keeps setup and cleanup code simple.

The call to {{domxref("Element.closest()")}} handles the case where the user clicks an element nested inside the `<li>`, such as a `<strong>` tag. Without it, `event.target` would be that inner element rather than the list item.

## Events that don't bubble

Some events are dispatched only on their target. If you need to delegate such events, you can often use a bubbling alternative. For example, {{domxref("Element/focusin_event", "focusin")}} and {{domxref("Element/focusout_event", "focusout")}} behave like `focus` and `blur` but bubble. Alternatively, you can listen during the capturing phase, because capturing occurs even for events that don't bubble.

## Summary

- Events travel down the DOM in the capturing phase, reach the target, and then bubble back up.
- Listeners run during the bubbling phase by default.
- `event.target` identifies the origin of the event, while `event.currentTarget` identifies the element handling it.
- `stopPropagation()` halts propagation, but it should be used carefully.
- Event delegation relies on bubbling to handle many elements with a single listener.

## See also

- {{domxref("EventTarget.addEventListener()")}}
- {{domxref("Event.bubbles")}}
- {{domxref("Event.eventPhase")}}
- [Introduction to events](/en-US/docs/Learn_web_development/Core/Scripting/Events)
- [Event reference](/en-US/docs/Web/Events)

{{PreviousMenuNext("Learn_web_development/Core/Scripting/Events", "Learn_web_development/Core/Scripting/Event_delegation", "Learn_web_development/Core/Scripting")}}
```
