I couldn't save the file: the Write tool is disabled in this session, and I have no shell to create it. The Markdown is below so you can copy it into a `.md` file.

````markdown
# Getting started with CSS

**Cascading Style Sheets (CSS)** is the language used to describe the presentation of a document written in HTML or XML. CSS controls colors, fonts, spacing, layout, and how content responds to different screen sizes. Where HTML defines the structure and meaning of a page, CSS defines how that structure looks.

This article introduces the core ideas you need to start styling web pages: what a CSS rule looks like, how to connect a stylesheet to a document, how selectors choose elements, and how the cascade decides which declaration wins when several apply to the same element.

## What CSS does

Every web page is built from elements such as headings, paragraphs, links, and images. By default, browsers apply a basic set of styles to these elements, which is why an unstyled page uses a plain white background, a default font, and blue underlined links. CSS lets you replace those defaults with your own choices.

The separation between content and presentation is one of the main advantages of CSS. You can keep your HTML focused on meaning and move all visual decisions into one or more stylesheets. This makes pages easier to maintain, and it allows the same content to be presented differently on screens, in print, or on other devices.

## Anatomy of a CSS rule

A CSS stylesheet is made of rules. Each rule has two parts: a selector and a declaration block. The selector identifies which elements the rule applies to. The declaration block contains one or more declarations, each made of a property and a value, separated by a colon and ended with a semicolon.

```css
h1 {
  color: navy;
  font-size: 2rem;
  margin-bottom: 0.5em;
}
```

In this example, `h1` is the selector, and the rule sets three properties: `color`, `font-size`, and `margin-bottom`. Every `<h1>` element in the document receives these styles.

Property names are not case-sensitive, but it is conventional to write them in lowercase. Values depend on the property. Some accept keywords such as `navy` or `bold`, some accept lengths such as `2rem` or `12px`, and others accept colors, percentages, or functions such as `rgb()`.

## Adding CSS to a document

There are three ways to include CSS in an HTML page.

The most common and recommended method is an **external stylesheet**, linked from the `<head>` of the document:

```html
<head>
  <link rel="stylesheet" href="styles.css" />
</head>
```

An external stylesheet can be shared by many pages, and browsers can cache it, which makes your site faster to load on later visits.

The second method is an **internal stylesheet**, placed inside a `<style>` element in the `<head>`. This is useful for small experiments or single-page documents, but it cannot be shared across pages.

The third method is an **inline style**, written directly in an element's `style` attribute. Inline styles have the highest precedence among author styles, so they are hard to override and hard to maintain. Use them sparingly, for example when a script generates a value at runtime.

## Selectors

Selectors determine which elements a rule targets. The simplest kinds are:

- **Type selectors**, which match elements by name, such as `p` or `section`.
- **Class selectors**, which match elements with a given `class` attribute, written with a leading dot, such as `.warning`.
- **ID selectors**, which match the element with a given `id` attribute, written with a leading hash, such as `#main-nav`. IDs must be unique within a page, so reserve them for unique landmarks rather than general styling.
- **Universal selector**, written as `*`, which matches every element.

You can combine selectors to make them more specific. A descendant selector such as `article p` matches paragraphs inside an `<article>` element at any depth. A child combinator such as `ul > li` matches only direct children. You can also group selectors with commas, so `h1, h2, h3` applies one rule to all three headings.

Pseudo-classes select elements based on their state or position. For example, `a:hover` matches a link while the pointer is over it, and `li:first-child` matches the first item in a list. Pseudo-elements, such as `p::first-line`, select a part of an element.

Class selectors are generally the best default for styling. They are specific enough to target what you need, reusable across many elements, and easy to read.

## The cascade and specificity

The word "cascading" refers to the way the browser resolves conflicts when more than one declaration applies to the same element. The browser considers three factors, in order.

First, **origin and importance**. Declarations marked with `!important` take priority over normal ones, and author styles generally override the browser's default styles. Use `!important` rarely, because it makes later overrides difficult.

Second, **specificity**. Each selector has a weight. Type selectors and pseudo-elements have the lowest weight, class selectors, attribute selectors, and pseudo-classes have a higher weight, and ID selectors have the highest. Inline styles outrank selectors. When two rules set the same property on the same element, the rule with the higher specificity wins, regardless of where it appears in the file.

Third, **source order**. If two rules have equal specificity, the one that appears later in the stylesheet wins.

Consider this example:

```css
p { color: black; }
.intro { color: darkslategray; }
p.intro { color: teal; }
```

A paragraph with the class `intro` is teal, because `p.intro` has a higher specificity than either of the other rules. Keeping selectors simple and avoiding unnecessary specificity makes stylesheets easier to extend later.

## A first complete example

The following example combines these ideas in a small page. The HTML provides the structure, and the stylesheet provides the appearance.

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>My first styled page</title>
    <link rel="stylesheet" href="styles.css" />
  </head>
  <body>
    <h1>Welcome</h1>
    <p class="intro">This paragraph uses the introduction style.</p>
    <p>This paragraph uses the default paragraph style.</p>
  </body>
</html>
```

```css
body {
  font-family: system-ui, sans-serif;
  line-height: 1.5;
  max-width: 40rem;
  margin: 2rem auto;
  padding: 0 1rem;
}

h1 {
  color: navy;
}

.intro {
  font-size: 1.2rem;
  color: darkslategray;
}
```

Open the page in a browser, and you see a centered column of text with a navy heading and a slightly larger, differently colored introduction. Changing a value in `styles.css` and reloading the page is the fastest way to learn how CSS behaves, so experiment freely.

## Tips for beginners

Use your browser's developer tools to inspect elements and see which rules apply to them. The Styles panel shows each declaration and marks the ones that are overridden. This is the most effective way to debug unexpected results.

Prefer relative units such as `rem` and `em` for font sizes and spacing, because they scale with the user's preferred text size. Avoid fixed heights where content may grow, and let elements size themselves according to their content whenever possible.

Organize your stylesheet from general to specific, and group related rules together. Comments, written between `/*` and `*/`, can explain why a rule exists.

## Next steps

Once you are comfortable with rules, selectors, and the cascade, you can move on to the layout systems that CSS provides. Flexbox arranges items along one axis and handles alignment and distribution of space. CSS Grid arranges items in two dimensions using rows and columns. Both are supported in all modern browsers and form the foundation of most contemporary page layouts.

You can also learn about responsive design with media queries, which apply rules only when a condition such as viewport width is met, and about custom properties, which let you store reusable values such as colors and spacing in one place.

## See also

- HTML basics
- Selectors reference
- The cascade and specificity
- Flexbox and Grid layout guides
````

To save it, copy the block into a file named `getting-started-with-css.md`. The body text is about 900 words, excluding the code examples.
