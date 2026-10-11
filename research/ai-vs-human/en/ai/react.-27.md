```markdown
---
title: "<style>"
---

<Intro>

The [built-in browser `<style>` component](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/style) lets you add inline CSS stylesheets to your document.

```js
<style>{` p { color: red; } `}</style>
```

</Intro>

<InlineToc />

---

## Reference {/*reference*/}

### `<style>` {/*style*/}

To add inline styles to your document, render the [built-in browser `<style>` component](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/style). You can render `<style>` from any component. React will, in some cases, place the matching DOM element in the document head and remove duplicate styles.

```js
<style>{` p { color: red; } `}</style>
```

[See more examples below.](#usage)

#### Props {/*props*/}

`<style>` supports all [common element props.](/reference/react-dom/components/common#props)

* `children`: a string, required. The contents of the stylesheet.
* `precedence`: a string. Tells React where to place the `<style>` DOM node relative to other stylesheets in the document `<head>`. This decides which stylesheet can override another. React assumes that precedence values it finds first are lower and those it finds later are higher. Many style systems work well with a single precedence value because style rules are atomic. Stylesheets with the same precedence go together, whether they are `<link>` or inline `<style>` tags or loaded with the [`preinit`](/reference/react-dom/preinit) function.
* `href`: a string. Lets React [remove duplicate styles](#special-rendering-behavior) that have the same `href`.
* `media`: a string. Limits the stylesheet to a certain [media query](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_media_queries/Using_media_queries).
* `nonce`: a string. A cryptographic [nonce to allow the resource](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/nonce) when using a strict Content Security Policy.
* `title`: a string. Gives the name of an [alternative stylesheet](https://developer.mozilla.org/en-US/docs/Web/CSS/Alternative_style_sheets).

Props that are **not recommended** for use with React:

* `blocking`: a string. If set to `"render"`, tells the browser not to render the page until the stylesheet is loaded. React gives finer control using Suspense.

#### Special rendering behavior {/*special-rendering-behavior*/}

React can move `<style>` components to the document's `<head>`, remove duplicate stylesheets, and suspend while the stylesheet is loading.

To use this behavior, provide both the `href` and `precedence` props. React removes duplicate styles that have the same `href`. The `precedence` prop tells React where to place the `<style>` DOM node relative to others in the document `<head>`. This decides which stylesheet can override another.

This special treatment comes with three caveats:

* React ignores changes to props after the style has rendered. React will show a warning in development if this happens.
* React drops all extra props when you use the `precedence` prop. Only `href` and `precedence` are kept.
* React may leave the style in the DOM even after the component that rendered it has unmounted.

---

## Usage {/*usage*/}

### Rendering an inline CSS stylesheet {/*rendering-an-inline-css-stylesheet*/}

If a component depends on certain CSS styles to display correctly, you can render an inline stylesheet inside the component.

The `href` prop should uniquely identify the stylesheet, because React removes stylesheets that have the same `href`. If you give a `precedence` prop, React reorders inline stylesheets based on the order these values appear in the component tree.

Inline stylesheets don't trigger Suspense boundaries while they load. They load inline with the rest of the markup, so they're ready before the content that depends on them.

<Sandpack>

```js src/App.js active
import ShowRenderedHTML from './ShowRenderedHTML.js';
import { useId } from 'react';

function PieChart({data, colors}) {
  const id = useId();
  const stylesheet = colors.map((color, index) =>
    `#${id} .color-${index}: \{ color: "${color}"; \}`
  ).join();
  return (
    <>
      <style href={"PieChart-" + JSON.stringify(colors)} precedence="medium">
        {stylesheet}
      </style>
      <svg id={id}>
        …
      </svg>
    </>
  );
}

export default function App() {
  return (
    <ShowRenderedHTML>
      <PieChart data="..." colors={['red', 'green', 'blue']} />
    </ShowRenderedHTML>
  );
}
```

</Sandpack>
```

The page uses the same MDX conventions as react.dev: the `<Intro>`, `<InlineToc />` and `<Sandpack>` tags, and anchors like `{/*props*/}` on each heading. The body text is about 440 words, not counting the code. The `ShowRenderedHTML.js` helper in the Sandpack example isn't included here, because react.dev pages usually leave it out of the visible example.
