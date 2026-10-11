---
title: "CSS: Styling the content"
slug: Learn/CSS/Styling_content
page-type: learn-module
---

{{CSSRef}}

**Cascading Style Sheets (CSS)** is the language that describes how HTML elements are presented on screen, on paper, or in other media. Where HTML gives a document its structure and meaning, CSS controls how that content looks: its colors, fonts, spacing, and layout. This page introduces the core ideas you need to start styling content with confidence.

## What CSS does

A web page without CSS still works. The browser applies a default style sheet, which is why headings are large and bold and links are blue and underlined. CSS lets you override those defaults and replace them with your own design.

CSS is a **declarative** language. You don't write step-by-step instructions. You describe the result you want, and the browser works out how to produce it. A rule might say "all paragraphs should have dark gray text", and the browser applies that to every paragraph in the document.

## Anatomy of a CSS rule

A CSS **rule** (or _ruleset_) has two main parts: a selector and a declaration block.

```css
p {
  color: darkslategray;
  font-size: 1.125rem;
}
```

- The **selector** (`p`) chooses which elements the rule applies to.
- The **declaration block** (the part in curly braces) holds one or more **declarations**.
- Each declaration pairs a **property** (`color`) with a **value** (`darkslategray`), separated by a colon and ended with a semicolon.

Properties are the aspects of an element you want to change. Values are the settings you choose for them.

## Adding CSS to a page

There are three ways to apply CSS to an HTML document.

### External style sheets

The most common and maintainable approach is to put your rules in a separate `.css` file and link to it from the document's `<head>`:

```html
<link rel="stylesheet" href="styles.css" />
```

One style sheet can style many pages, so a change in one place updates your whole site.

### Internal style sheets

You can place rules inside a {{HTMLElement("style")}} element in the document head. This suits small, single-page examples, but it doesn't scale well.

### Inline styles

The `style` attribute applies declarations to a single element:

```html
<p style="color: crimson;">Important notice</p>
```

Inline styles are hard to override and mix presentation with content, so use them sparingly.

## Selecting elements

Selectors are the heart of CSS. The most common types are:

| Selector type | Example         | Matches                                   |
| ------------- | --------------- | ----------------------------------------- |
| Type          | `h1`            | Every `<h1>` element                      |
| Class         | `.note`         | Elements with `class="note"`              |
| ID            | `#header`       | The element with `id="header"`            |
| Attribute     | `a[target]`     | Links that have a `target` attribute      |
| Pseudo-class  | `a:hover`       | Links while the pointer is over them      |
| Pseudo-element | `p::first-line` | The first formatted line of each paragraph |

You can combine selectors to be more precise. A **descendant combinator** (a space) matches elements nested inside others, so `article p` selects only paragraphs inside an `<article>`. A **child combinator** (`>`) matches only direct children.

## Styling text

Text is the main content of most pages, so typography properties are often the first ones you learn:

```css
body {
  font-family: system-ui, sans-serif;
  font-size: 1rem;
  line-height: 1.6;
  color: #222;
}

h1 {
  font-weight: 700;
  text-align: center;
  letter-spacing: 0.02em;
}

a {
  text-decoration: underline;
  text-underline-offset: 0.2em;
}
```

Some points to keep in mind:

- Give {{CSSxRef("font-family")}} a list of fallbacks, ending with a generic family such as `sans-serif`.
- A unitless {{CSSxRef("line-height")}} such as `1.6` scales with the font size and is usually the best choice.
- Prefer relative units such as `rem` and `em` for font sizes, so text respects the user's browser settings.

## Colors and backgrounds

CSS offers several ways to write a color: named keywords (`tomato`), hexadecimal values (`#ff6347`), and functional notations such as `rgb()`, `hsl()`, and `oklch()`.

```css
.card {
  background-color: hsl(210 40% 96%);
  color: hsl(215 25% 20%);
  border: 1px solid hsl(210 20% 80%);
}
```

Make sure text and background colors have enough **contrast**. Low contrast makes content hard to read for many people, especially those with low vision.

Backgrounds can also be images or gradients, set with {{CSSxRef("background-image")}}.

## The box model

Every element is treated as a rectangular box made up of four layers, from the inside out:

1. **Content**: the text or other material in the element.
2. **Padding**: space between the content and the border.
3. **Border**: a line that surrounds the padding.
4. **Margin**: space between this box and its neighbors.

```css
.card {
  padding: 1rem;
  border: 2px solid steelblue;
  margin: 1.5rem 0;
}
```

By default, `width` and `height` set the size of the content box only, so padding and borders make the element larger than you might expect. Setting {{CSSxRef("box-sizing")}} to `border-box` makes the declared width include padding and border, which most developers find more intuitive:

```css
*,
*::before,
*::after {
  box-sizing: border-box;
}
```

## The cascade, specificity, and inheritance

When several rules target the same element and set the same property, the browser must decide which one wins. This process is the **cascade**. It considers, in order:

1. **Origin and importance**: browser defaults, author styles, and `!important` declarations.
2. **Specificity**: more specific selectors beat less specific ones. An ID selector outranks a class selector, which outranks a type selector.
3. **Source order**: if everything else is equal, the rule that appears last wins.

Some properties, such as `color` and `font-family`, are also **inherited**: if you don't set them on an element, it takes the value from its parent. Others, such as `border` and `margin`, are not inherited by default. You can control this with the keywords `inherit`, `initial`, and `unset`.

## Making content responsive

People view your content on screens of many sizes. A few habits help it adapt:

- Use flexible units like percentages, `rem`, and `ch` instead of fixed pixel widths.
- Set `max-width: 100%` on images so they never overflow their container.
- Use **media queries** to adjust styles at particular viewport sizes:

```css
.layout {
  padding: 1rem;
}

@media (min-width: 48rem) {
  .layout {
    padding: 2rem;
    max-width: 60rem;
    margin-inline: auto;
  }
}
```

## Next steps

Once you are comfortable with these fundamentals, move on to CSS layout techniques such as [Flexbox](/en-US/docs/Learn/CSS/CSS_layout/Flexbox) and [Grid](/en-US/docs/Learn/CSS/CSS_layout/Grids), which let you arrange content in rows, columns, and complex page designs.

## See also

- [CSS reference](/en-US/docs/Web/CSS/Reference)
- [CSS selectors](/en-US/docs/Web/CSS/CSS_selectors)
- [The box model](/en-US/docs/Learn/CSS/Building_blocks/The_box_model)
- [Cascade and inheritance](/en-US/docs/Learn/CSS/Building_blocks/Cascade_and_inheritance)
