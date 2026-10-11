# Challenge: Styling a home color scheme search app

**Prerequisites:** Basic knowledge of [HTML](/en-US/docs/Learn_web_development/Core/Structuring_content), [CSS](/en-US/docs/Learn_web_development/Core/Styling_basics), and [JavaScript](/en-US/docs/Learn_web_development/Core/Scripting). You should also be comfortable with [CSS custom properties](/en-US/docs/Web/CSS/Guides/Cascading_variables), [Flexbox](/en-US/docs/Web/CSS/Guides/Flexbox), and [media queries](/en-US/docs/Web/CSS/Guides/Media_queries).

## Scenario

A paint company wants a small web app that helps customers choose colors for their homes. Visitors type a room name or a mood, such as "calm bedroom" or "warm kitchen," and the app displays a list of matching palettes. Each palette has a name, a short description, and a row of five color swatches.

The developers have already written the HTML structure and the JavaScript that filters the results. Your job is to style the page so that it looks polished, respects the visitor's color preferences, and works well on both phones and desktop screens.

## Getting started

Copy the following starter markup into an `index.html` file. Link your stylesheet in the `<head>` and save your CSS in a `styles.css` file.

```html
<header>
  <h1>Home Palette Finder</h1>
  <p>Find a color scheme for every room.</p>
</header>
<main>
  <form id="search-form" role="search">
    <label for="query">Room or mood</label>
    <input type="search" id="query" name="query" placeholder="e.g. calm bedroom">
    <button type="submit">Search</button>
  </form>
  <section id="results" aria-live="polite">
    <article class="palette">
      <h2>Coastal Morning</h2>
      <p>Soft blues and sandy neutrals for bright, airy spaces.</p>
      <ul class="swatches">
        <li style="--swatch: #a8d5e2">#a8d5e2</li>
        <li style="--swatch: #f4e4c1">#f4e4c1</li>
        <li style="--swatch: #e8c39e">#e8c39e</li>
        <li style="--swatch: #6fa8bc">#6fa8bc</li>
        <li style="--swatch: #2f4858">#2f4858</li>
      </ul>
    </article>
  </section>
</main>
```

Note that each swatch uses an inline `--swatch` custom property to set its background color. You can read this value in your CSS with `var(--swatch)`.

## Your task

Style the page so that it meets the following requirements:

1. Define at least five colors as custom properties on `:root`, and use them throughout your stylesheet rather than repeating hexadecimal values.
2. Provide a light color scheme by default, and a dark color scheme when the visitor's system prefers dark mode. Use the `prefers-color-scheme` media feature to switch between them.
3. Lay out the search form so that the input and button sit on one line on wide screens and stack vertically on narrow screens.
4. Display the palette cards in a responsive grid. Use as many columns as fit, with a minimum card width of about 16rem.
5. Show the five swatches in each palette as equal-width blocks that fill the card's width. Give the swatches rounded corners and a thin border so that very light colors remain visible against the background.
6. Print each hex value on its swatch, and choose a text color that remains readable against the swatch's background.
7. Give the input and button a clearly visible focus style for keyboard users. Avoid removing focus outlines without providing a replacement.
8. Make sure the layout works at a width of 320 pixels, with a 16-pixel gutter on each side and no horizontal scrolling.

## Hints

- Use `flex-wrap: wrap` on the form so that the input and button wrap when space runs out.
- For the card grid, try `grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr))`.
- To size the swatches, apply `display: flex` to the `.swatches` list and `flex: 1` to each item.
- Use `clamp()` to create fluid font sizes for headings.
- The `:focus-visible` pseudo-class lets you show focus rings only for keyboard interaction.
- To check text contrast, use your browser's developer tools or an online contrast checker. Aim for a ratio of at least 4.5:1 for body text.

## Success criteria

Your finished page should look balanced at every width you test. Switch your operating system between light and dark mode and confirm that both schemes are readable. Tab through the form to verify that the focus style is visible. When you finish, compare your solution with the design goals above rather than with a single "correct" layout, because many different stylesheets can satisfy these requirements.

## See also

- [CSS custom properties (variables)](/en-US/docs/Web/CSS/Guides/Cascading_variables)
- [`prefers-color-scheme`](/en-US/docs/Web/CSS/@media/prefers-color-scheme)
- [CSS grid layout](/en-US/docs/Web/CSS/Guides/Grid_layout)
- [Flexbox](/en-US/docs/Web/CSS/Guides/Flexbox)
- [`:focus-visible`](/en-US/docs/Web/CSS/:focus-visible)
- [`clamp()`](/en-US/docs/Web/CSS/clamp)
