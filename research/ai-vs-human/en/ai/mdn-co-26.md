````markdown
---
title: Media query fundamentals
slug: Learn_web_development/Core/CSS_layout/Media_queries
page-type: learn-module-chapter
sidebar: learnsidebar
---

{{PreviousMenuNext("Learn_web_development/Core/CSS_layout/Responsive_Design", "Learn_web_development/Core/CSS_layout/Test_your_skills/Media_queries", "Learn_web_development/Core/CSS_layout")}}

The **CSS media query** lets you apply CSS only when the browser and device environment match a rule you set, for example "the viewport is wider than 480 pixels". Media queries are a key part of responsive web design. You can use them to create different layouts depending on the size of the viewport. You can also use them to find out other things about the environment your site is running in, such as whether the user has a touchscreen or a mouse. This lesson covers the syntax used in media queries, then shows how to use them in a simple design.

<table>
  <tbody>
    <tr>
      <th scope="row">Prerequisites:</th>
      <td>
        HTML basics (study
        <a href="/en-US/docs/Learn_web_development/Core/Structuring_content">Basic HTML syntax</a>), and an idea of how CSS works (study
        <a href="/en-US/docs/Learn_web_development/Core/Styling_basics">CSS Styling basics</a>).
      </td>
    </tr>
    <tr>
      <th scope="row">Learning outcomes:</th>
      <td>
        <ul>
          <li>The syntax of media queries.</li>
          <li>Media types, and the common media features such as <code>width</code> and <code>orientation</code>.</li>
          <li>Combining media queries with logical operators.</li>
          <li>Choosing breakpoints, and the mobile-first approach to responsive design.</li>
        </ul>
      </td>
    </tr>
  </tbody>
</table>

## Media query basics

The simplest media query syntax looks like this:

```css
@media media-type and (media-feature-rule) {
  /* CSS rules go here */
}
```

It has the following parts:

- The {{cssxref("@media")}} at-rule.
- A media type, which tells the browser what kind of media this code is for, such as print or screen.
- A media expression, which is a rule or test that must pass for the CSS inside to be applied.
- A set of CSS rules that are applied if the test passes and the media type is correct.

### Media types

The possible types of media you can specify are:

- `all`
- `print`
- `screen`

The following media query only sets the body to `12pt` when the page is printed. It doesn't apply when the page is shown in a browser.

```css
@media print {
  body {
    font-size: 12pt;
  }
}
```

> [!NOTE]
> The media type is optional. If you don't give a media type in your media query, it defaults to `all`.

### Media feature rules

After specifying the type, you can target a media feature with a rule.

#### Width and height

The feature most often tested to create responsive designs is the viewport width. You can apply CSS when the viewport is above or below a certain width, or exactly a certain width, using the {{cssxref("@media/width", "width")}} media feature.

Modern browsers support the _range syntax_, which uses comparison operators such as `<`, `>`, `<=`, and `>=`. The following example makes the body text red when the viewport is 600 pixels or narrower:

```css
@media screen and (width <= 600px) {
  body {
    color: red;
  }
}
```

You will often see older code that uses the `min-width` and `max-width` prefixes instead. The following query matches the same viewports as the previous one:

```css
@media screen and (max-width: 600px) {
  body {
    color: red;
  }
}
```

You can also test a range between two values in one expression:

```css
@media (30em <= width <= 50em) {
  body {
    color: blue;
  }
}
```

In practice, testing for an exact width is rarely useful, because the devices people use come in so many sizes.

#### Orientation

The {{cssxref("@media/orientation", "orientation")}} media feature tests for `portrait` or `landscape` mode. The following example changes the body text color when the device is in landscape orientation:

```css
@media (orientation: landscape) {
  body {
    color: rebeccapurple;
  }
}
```

A standard desktop view has a landscape orientation, and a design that works well in this orientation may not work as well on a phone or tablet held in portrait mode.

#### Use of pointing devices

The {{cssxref("@media/hover", "hover")}} media feature lets you test whether the user can hover over an element, which usually means they are using a mouse or a similar pointing device. Touchscreens and keyboard navigation can't hover. In the example below, the color only changes on hover if the user's primary input can hover:

```css
@media (hover: hover) {
  body {
    color: rebeccapurple;
  }
}
```

The related {{cssxref("@media/pointer", "pointer")}} feature tells you whether the pointer is `fine` (such as a mouse) or `coarse` (such as a finger). You could use it to make controls larger for users on a touchscreen.

#### User preferences

Some media features report the user's preferences rather than facts about the device. For example, {{cssxref("@media/prefers-color-scheme", "prefers-color-scheme")}} tells you whether the user has asked for a light or dark theme, and {{cssxref("@media/prefers-reduced-motion", "prefers-reduced-motion")}} tells you whether they want to minimize animation:

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation: none;
    transition: none;
  }
}
```

## More complex media queries

Sometimes you want to combine several tests. You can do this with the logical operators `and`, `or` (written as a comma), and `not`.

### "and" logic

To combine media features, use `and`. All the conditions must be true for the CSS to apply. The following example applies only when the viewport is at least 600 pixels wide _and_ the device is in landscape orientation:

```css
@media screen and (width >= 600px) and (orientation: landscape) {
  body {
    color: blue;
  }
}
```

### "or" logic

If you have a set of queries, any of which could match, separate them with commas. The CSS applies if _any_ of the queries is true:

```css
@media screen and (width >= 600px), screen and (orientation: landscape) {
  body {
    color: blue;
  }
}
```

### "not" logic

You can negate an entire media query using the `not` operator. The following example applies everywhere _except_ wide landscape screens:

```css
@media not screen and (width >= 600px) and (orientation: landscape) {
  body {
    color: blue;
  }
}
```

Note that `not` applies to the whole query, not just the first condition after it.

## How to choose breakpoints

The points where a media query changes the layout are known as **breakpoints**. In the early days of responsive design, many designers targeted very specific screen sizes, such as those of popular phones and tablets. There are now far too many devices with different sizes to make this practical, and new ones appear all the time.

Rather than targeting devices, a better approach is to change the design at the size where the content starts to break in some way. Perhaps the line lengths become far too long, or a boxed-out sidebar gets squashed and hard to read. That's the point where you want a media query to change the design.

To find these points, make your browser window smaller and larger, or use the [Responsive Design Mode](https://firefox-source-docs.mozilla.org/devtools-user/responsive_design_mode/index.html) in your browser's developer tools, and watch where the layout stops working.

> [!NOTE]
> Using `em` units for breakpoints, such as `(width >= 40em)`, means the layout responds to the user's chosen text size as well as to the viewport size.

## Mobile first responsive design

There are two broad approaches to responsive design. You can start with your desktop or widest view and then add breakpoints that adjust the layout as the viewport becomes smaller, or you can start with the smallest view and add layout as the viewport grows. This second approach is described as **mobile first** responsive design and is often the best one to follow.

The view for the very smallest devices is often a simple single column of content, much as it appears in normal flow. This means you often don't need to do much layout for small devices: order your source well and you will have a readable layout by default.

```css
/* Base styles: a single column for all viewports */
.wrapper {
  margin: 0 auto;
  max-width: 90em;
}

/* Add a two-column layout once there is room for it */
@media (width >= 40em) {
  .wrapper {
    display: grid;
    grid-template-columns: 3fr 1fr;
    gap: 1rem;
  }
}
```

Because the base styles come first and the media query only adds to them, browsers that are narrow, or that don't understand your query, still get a usable layout.

### The viewport meta tag

Mobile browsers often pretend to have a wide viewport and then scale the page down, which stops your media queries from matching as expected. To prevent this, include the following element in the {{htmlelement("head")}} of your document:

```html
<meta name="viewport" content="width=device-width,initial-scale=1" />
```

This tells mobile browsers to set the viewport width to the width of the device and not to scale the page.

## Do you really need a media query?

Flexbox, grid, and multi-column layout all give you ways to create flexible and even responsive components without a media query. For example, the following grid creates as many columns of at least 200 pixels as will fit, without any breakpoints:

```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
}
```

It's always worth checking whether a layout method can do the work before reaching for a media query. For components that need to respond to the size of their container rather than the viewport, see [container queries](/en-US/docs/Web/CSS/CSS_containment/Container_queries).

## Summary

In this lesson, you've learned about media queries and how to use them in practice to create a mobile first responsive design. You've seen how to target media types and features, how to combine queries with logical operators, and how to choose breakpoints based on your content rather than particular devices.

In the next article, you'll find some tests you can use to check how well you've understood and retained this information.

## See also

- [Using media queries](/en-US/docs/Web/CSS/CSS_media_queries/Using_media_queries)
- [Testing media queries programmatically](/en-US/docs/Web/CSS/CSS_media_queries/Testing_media_queries)
- {{cssxref("@media")}}

{{PreviousMenuNext("Learn_web_development/Core/CSS_layout/Responsive_Design", "Learn_web_development/Core/CSS_layout/Test_your_skills/Media_queries", "Learn_web_development/Core/CSS_layout")}}
````

The page follows MDN conventions: YAML front matter, a prerequisites and learning-outcomes table, KumaScript macros (`{{cssxref}}`, `{{PreviousMenuNext}}`) and GFM-style `> [!NOTE]` callouts. The prose, not counting the code blocks, comes to about 900 words. I made up the slug and the previous/next links to fit the CSS layout module in the Learn area. Check them against the current file tree before you use the page.
