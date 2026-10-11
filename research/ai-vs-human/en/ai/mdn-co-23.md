```markdown
---
title: "Challenge: Structuring a page of content"
short-title: "Challenge: Structuring a page"
slug: Learn_web_development/Core/Structuring_content/Structuring_a_page_of_content
page-type: learn-module-assessment
sidebar: learnsidebar
---

{{PreviousMenuNext("Learn_web_development/Core/Structuring_content/Structuring_documents", "Learn_web_development/Core/Structuring_content/HTML_images", "Learn_web_development/Core/Structuring_content")}}

In this challenge, you'll use the semantic structural elements you've learned about to mark up a simple web page. The aim is to check that you can organize content into logical regions, such as a header, navigation, main content, sidebar, and footer, and that you know which element fits each region.

## Starting point

To start, download the [starting files](https://github.com/mdn/learning-area/tree/main/html/introduction-to-html/structuring-a-page-of-content-start). Save them in a new folder on your computer. The folder contains:

- An `index.html` file with the page content but little structure.
- A `style.css` file that styles the page once the correct structure is in place.
- Some images used on the page.

You can also use an online editor such as [CodePen](https://codepen.io/) or [JSFiddle](https://jsfiddle.net/). Paste the HTML into the HTML panel and the CSS into the CSS panel. If your editor doesn't have a separate CSS panel, put the CSS inside a {{htmlelement("style")}} element in the document's `<head>`.

## Project brief

The page is a small website for birdwatchers in a fictional town. The text and images are already there. Your job is to wrap the content in suitable structural elements so that the page has a clear, meaningful outline. When the structure is right, the stylesheet will lay the page out correctly.

Follow these steps:

1. Wrap the site title and the main heading of the page in a {{htmlelement("header")}} element.
2. Wrap the list of navigation links in a {{htmlelement("nav")}} element. In this design, the navigation sits inside the header.
3. Wrap the page's main content in a {{htmlelement("main")}} element. Remember that a document should only have one visible `<main>` element.
4. Inside `<main>`, wrap the welcome text and its heading in an {{htmlelement("article")}} element. This content makes sense on its own, so an `<article>` is a good fit.
5. Wrap the "Favorite photos" block in an {{htmlelement("aside")}} element. It is related to the main content but not essential to it, so it belongs in a sidebar.
6. Wrap the copyright notice at the bottom in a {{htmlelement("footer")}} element.
7. Link the provided stylesheet to the page by adding a {{htmlelement("link")}} element to the `<head>`, if it isn't already there.

When you've finished, the page should show a heading banner across the top, the navigation bar below it, the main article and the photo sidebar next to each other, and the footer at the bottom.

## Hints and tips

- Use the [W3C Nu HTML Checker](https://validator.w3.org/nu/) to validate your HTML. Fix any errors it reports before you finish.
- You don't need to know any CSS to complete this challenge. Leave the CSS file as it is. If the layout looks broken, the problem is almost always in the HTML structure, not the stylesheet.
- Don't use {{htmlelement("div")}} elements for the regions listed above. A `<div>` has no meaning. Only use one if no semantic element fits, for example as a wrapper that exists only for styling.
- Check that your headings form a logical hierarchy. There should be one {{htmlelement("Heading_Elements", "&lt;h1&gt;")}} for the page, with {{htmlelement("Heading_Elements", "&lt;h2&gt;")}} elements for the main sections below it. Don't skip heading levels.
- Your browser's developer tools can help. Open the Inspector or Elements panel to see how your elements are nested and to find tags that weren't closed.

## Example

Your finished structure should look something like this outline. The content of each element has been left out to keep it short:

```html
<body>
  <header>
    <h1>…</h1>
    <nav>
      <ul>
        …
      </ul>
    </nav>
  </header>

  <main>
    <article>
      <h2>…</h2>
      …
    </article>

    <aside>
      <h2>Favorite photos</h2>
      …
    </aside>
  </main>

  <footer>
    <p>…</p>
  </footer>
</body>
```

Your solution doesn't need to match this outline exactly. It's fine to put the `<nav>` outside the `<header>`, for example. What matters is that each part of the page is wrapped in the element that best describes its purpose, and that the page validates and looks correct with the stylesheet applied.

## Getting help

If you get stuck, see the [finished example](https://github.com/mdn/learning-area/tree/main/html/introduction-to-html/structuring-a-page-of-content-finished). Try to solve the problem yourself first, and compare your code with the example afterwards. If you still have questions, ask on the [MDN community forums](/en-US/about/community).

{{PreviousMenuNext("Learn_web_development/Core/Structuring_content/Structuring_documents", "Learn_web_development/Core/Structuring_content/HTML_images", "Learn_web_development/Core/Structuring_content")}}
```
