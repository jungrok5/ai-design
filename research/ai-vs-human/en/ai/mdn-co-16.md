---
title: CSS FAQ
slug: Web/CSS/FAQ
page-type: guide
---

# CSS FAQ

This page answers common questions about Cascading Style Sheets (CSS). It covers how to attach styles to a document, how the cascade decides which rule wins, how to size and position elements, and how to troubleshoot styles that don't appear as expected. For a complete list of properties, see the CSS reference.

## General questions

### What is CSS?

CSS describes the presentation of HTML and other markup documents. HTML defines the structure and meaning of content, while CSS controls colors, fonts, spacing, layout, and how content responds to different screen sizes.

A CSS file consists of rules. Each rule has a selector, which picks the elements to style, and a declaration block, which sets property-value pairs:

```css
/* Selector */
h1 {
  /* Declarations */
  color: rebeccapurple;
  font-size: 2rem;
}
```

### How do I add CSS to a page?

The most common method is an external stylesheet linked from the `<head>`:

```html
<link rel="stylesheet" href="styles.css" />
```

You can also place rules in a `<style>` element in the document head, or add declarations directly to an element with the `style` attribute. External stylesheets are preferred for most projects because browsers can cache them and multiple pages can share them. Reserve inline styles for values that change at runtime.

### Which CSS features can I rely on?

CSS is no longer a single specification. It is a collection of modules, and each module evolves at its own pace. Check browser compatibility data before you rely on a feature. You can also use feature queries to provide fallbacks:

```css
@supports (display: grid) {
  .gallery {
    display: grid;
  }
}
```

## The cascade and specificity

### Why isn't my style applied?

Most missing styles have one of three causes. The selector doesn't match the element, another rule with higher precedence overrides it, or the stylesheet fails to load. Open your browser's developer tools and inspect the element. The Styles panel shows which rules apply, which are overridden (usually with a strikethrough), and which file each rule comes from. Also check the Console for 404 errors on the stylesheet URL.

### How does the cascade decide which rule wins?

When several declarations target the same property on the same element, the browser resolves the conflict in roughly this order:

1. **Origin and importance:** user-agent, user, and author styles, with `!important` declarations reversing the normal order.
2. **Context:** cascade layers (`@layer`) and tree scope, such as Shadow DOM.
3. **Specificity:** the more specific selector wins.
4. **Source order:** when specificity is equal, the rule that appears later wins.

### How is specificity calculated?

Specificity is a three-part value, often written as (a, b, c):

- **a** counts ID selectors.
- **b** counts class selectors, attribute selectors, and pseudo-classes.
- **c** counts type selectors and pseudo-elements.

The universal selector (`*`), combinators, and `:where()` add nothing. Inline styles outrank all selectors. For example, `#nav .item a` has a specificity of (1, 1, 1), and `li.item` has (0, 1, 1).

Avoid raising specificity repeatedly with IDs or `!important`, because later overrides become difficult. Single class selectors are usually the easiest to maintain.

### When should I use !important?

Rarely. It is useful for utility classes that must override other styles, and for accessibility overrides. In most other cases, `!important` signals a specificity problem that is better fixed by simplifying your selectors.

## Layout and sizing

### Why doesn't my width include padding?

By default, `box-sizing` is `content-box`, so `width` sets only the content area. Padding and border are added outside it. Many projects change this globally:

```css
*,
*::before,
*::after {
  box-sizing: border-box;
}
```

With `border-box`, the declared width includes padding and border.

### How do I center an element?

To center a block element that has a set width, use automatic inline margins:

```css
.card {
  width: 600px;
  margin-inline: auto;
}
```

To center content both horizontally and vertically, use grid:

```css
.container {
  display: grid;
  place-items: center;
  min-height: 100vh;
}
```

### Should I use flexbox or grid?

Use flexbox for one-dimensional layouts, such as a row of buttons or a navigation bar. Use grid for two-dimensional layouts where rows and columns both matter. The two work well together: grid for the page skeleton, and flexbox for components inside it.

### Why doesn't z-index work?

`z-index` applies only to positioned elements (those with a `position` value other than `static`) and to flex and grid items. Also, some properties create a new stacking context, including `opacity` less than 1, `transform`, and `filter`. Descendants are then ordered only within that context.

### Why do my margins collapse?

Vertical margins between adjacent block siblings collapse into the larger of the two. A parent's margin can also collapse with its first or last child's margin when no border, padding, or content separates them. To prevent this, add padding or a border to the parent, or use `display: flow-root`, or make the parent a flex or grid container.

## Units and responsive design

### Should I use px, em, or rem?

Pixels are absolute and predictable, but they ignore users' font-size preferences. `rem` scales with the root font size and is a good default for typography and spacing. `em` scales with the current element's font size, which suits components that should scale together. For fluid layouts, use percentages or viewport units.

### How do I make a page responsive?

Use relative units, flexible layouts, and media queries. Write mobile styles first, then add rules for wider screens:

```css
.layout {
  display: grid;
  grid-template-columns: 1fr;
}

@media (min-width: 48em) {
  .layout {
    grid-template-columns: 2fr 1fr;
  }
}
```

Also include a viewport meta tag in the HTML:

```html
<meta name="viewport" content="width=device-width, initial-scale=1" />
```

### How do I support dark mode?

Define colors as custom properties, then change their values with the `prefers-color-scheme` media feature:

```css
:root {
  --bg: #ffffff;
  --fg: #1a1a1a;
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg: #121212;
    --fg: #f0f0f0;
  }
}

body {
  background: var(--bg);
  color: var(--fg);
}
```

## See also

- [CSS reference](/en-US/docs/Web/CSS/Reference)
- [CSS layout guide](/en-US/docs/Web/CSS/CSS_layout)
- [Specificity](/en-US/docs/Web/CSS/Specificity)
- [The box model](/en-US/docs/Web/CSS/CSS_box_model)
