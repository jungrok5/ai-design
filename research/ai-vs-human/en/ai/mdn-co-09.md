---
title: Legacy layout methods
slug: Learn_web_development/Core/CSS_layout/Legacy_layout_methods
page-type: learn-module-chapter
---

{{LearnSidebar}}

Grid and flexbox are now the standard tools for building page layouts, but they are relatively recent additions to CSS. Before they arrived, developers used a collection of techniques that were never designed for layout. This article describes those legacy methods, so you can recognize them in older codebases, understand why they behave the way they do, and decide how to modernize them.

**Prerequisites:** Familiarity with HTML and CSS basics, including the box model, the {{cssxref("display")}} property, and normal flow.

**Learning outcomes:**

- How floats, tables, and positioning were used to build layouts
- Why these techniques were fragile
- How to replace each of them with modern CSS

## Why legacy methods exist

CSS was originally designed to style documents, not to build application interfaces. Its early layout model had block elements stacking vertically and inline elements flowing horizontally. There was no built-in way to say "put these three columns side by side" or "make these boxes the same height".

Developers worked around this by repurposing properties that were designed for something else. The results worked, but they came with side effects and a lot of extra markup.

> [!NOTE]
> You should not use these techniques for new layouts. They remain in this guide because you will meet them in existing sites, frameworks, and tutorials.

## Floated layouts

The {{cssxref("float")}} property was designed to let text wrap around an image, as in a magazine. Because a floated element is taken out of normal flow and pushed to the left or right, developers realized that floating several block elements would place them side by side.

```html
<div class="wrapper">
  <main>Main content</main>
  <aside>Sidebar</aside>
</div>
```

```css
main {
  float: left;
  width: 70%;
}

aside {
  float: right;
  width: 25%;
}
```

This produces a two-column layout, but it introduces several problems.

### Collapsing containers

A floated element no longer contributes to the height of its parent. In the example above, the `.wrapper` would collapse to zero height, because both children are out of flow. Content that follows the wrapper would then slide up and wrap around the floats.

### Clearing floats

To fix this, developers used the {{cssxref("clear")}} property. A cleared element moves below any earlier floats. Because this needed an element to apply it to, many sites included empty elements purely for presentation. A neater approach was the "clearfix" hack, which adds a cleared pseudo-element to the container:

```css
.wrapper::after {
  content: "";
  display: block;
  clear: both;
}
```

A modern alternative that does the same job without a hack is to create a new block formatting context on the container:

```css
.wrapper {
  display: flow-root;
}
```

### Fragile widths and equal heights

Floated columns need widths that add up to no more than 100%, and the result changes if you add padding or borders unless you also set `box-sizing: border-box`. Floats also cannot make columns the same height. A sidebar with less content simply ends early, which led to tricks such as faux columns, where a repeating background image on the container imitated a full-height column.

## Table layouts

In the 1990s, before CSS was widely supported, designers laid out entire pages using HTML `<table>` elements with invisible borders. Cells provided columns, and nested tables provided more complex arrangements.

This approach mixed presentation with content, produced deeply nested and hard-to-maintain markup, and was a poor experience for assistive technology users, who heard a page announced as tabular data when it was not.

CSS later offered a cleaner variation: the table display values. Setting `display: table`, `display: table-row`, and `display: table-cell` on ordinary elements gives table behavior without table semantics.

```css
.row {
  display: table;
  width: 100%;
}

.column {
  display: table-cell;
}
```

Table cells have one genuine advantage: they stretch to equal heights automatically, which floats could not do. However, the technique is inflexible. Cells cannot wrap onto a new line when space runs out, and the gaps between them are awkward to control. Flexbox and grid do both jobs better.

## Positioning

The {{cssxref("position")}} property, with the values `relative`, `absolute`, `fixed`, and `sticky`, is not obsolete. It is still the right tool for overlays, tooltips, badges, and sticky headers. What is legacy is using it for the main page structure.

An absolutely positioned element is removed from flow, and its location is set with {{cssxref("top")}}, {{cssxref("right")}}, {{cssxref("bottom")}}, and {{cssxref("left")}}. Developers built whole layouts this way, placing a sidebar at a fixed offset and giving the main content a matching margin.

```css
.sidebar {
  position: absolute;
  top: 0;
  left: 0;
  width: 200px;
}

.content {
  margin-left: 220px;
}
```

The drawback is that absolutely positioned elements know nothing about their siblings. If the sidebar grows taller than the content, nothing adjusts, and the parent does not grow to contain it. Every dimension must be managed by hand.

## Inline-block layouts

Setting `display: inline-block` allows elements to sit on one line while keeping width, height, and vertical margins. It was popular for navigation bars and grids of cards.

It has an infamous quirk: the whitespace between elements in the HTML source is rendered as a gap of a few pixels. Workarounds included removing the whitespace, commenting it out, or setting the parent's `font-size` to zero. Vertical alignment also depends on the text baseline, which often gives surprising results.

## Multiple-column and framework grids

Many CSS frameworks built 12-column grid systems out of floats or inline-blocks, using percentage widths such as `width: 8.333%` and classes like `col-4`. If you work in an older codebase, you may find the same pattern in your own stylesheets. These systems worked, but they put layout decisions in the HTML class names and needed careful clearing at each row.

## Modern replacements

The table below summarizes what to use today.

| Legacy technique                   | Problem                                      | Modern replacement                                              |
| ---------------------------------- | -------------------------------------------- | --------------------------------------------------------------- |
| Floated columns                    | Collapsing parent, clearing, unequal heights | [Grid](/en-US/docs/Web/CSS/CSS_grid_layout) or [flexbox](/en-US/docs/Web/CSS/CSS_flexible_box_layout) |
| Clearfix                           | Extra rules, or extra elements               | `display: flow-root`                                            |
| Table layout                       | Semantics, rigid cells                       | Grid or flexbox                                                 |
| Absolute-positioned page structure | No awareness of siblings                     | Grid                                                            |
| Inline-block rows                  | Whitespace gaps, baseline alignment          | Flexbox with `gap`                                              |
| Framework 12-column systems        | Class-based layout, hard-coded percentages   | `grid-template-columns` with `fr` units                         |

Here is the earlier two-column float example rewritten with grid:

```css
.wrapper {
  display: grid;
  grid-template-columns: 7fr 3fr;
  gap: 1rem;
}
```

The container contains its children without any clearing, the columns are the same height by default, and the spacing is handled by `gap` rather than by margin arithmetic.

## When floats are still appropriate

Floats are not entirely obsolete. The original use case, wrapping text around an image or pull quote, is still what they do best. Newer features such as {{cssxref("shape-outside")}} build on floats to wrap text around non-rectangular shapes.

```css
img.portrait {
  float: left;
  margin: 0 1rem 1rem 0;
  shape-outside: circle(50%);
}
```

## Summary

Floats, table layouts, positioning, and inline-block arrangements all solved layout problems that CSS had not yet addressed directly. Each carried hidden costs: collapsing containers, clearing hacks, whitespace gaps, and manual size calculations. Grid and flexbox remove those costs, so prefer them for new work, and when you maintain older code, replace legacy layouts gradually, one component at a time.

## See also

- [CSS grid layout](/en-US/docs/Web/CSS/CSS_grid_layout)
- [CSS flexible box layout](/en-US/docs/Web/CSS/CSS_flexible_box_layout)
- [Block formatting context](/en-US/docs/Web/CSS/CSS_display/Block_formatting_context)
- [Positioning](/en-US/docs/Learn_web_development/Core/CSS_layout/Position)
- {{cssxref("float")}} and {{cssxref("clear")}}
