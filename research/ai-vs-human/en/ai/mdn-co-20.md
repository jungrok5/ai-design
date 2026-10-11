```md
---
title: Subgrid
slug: Web/CSS/CSS_grid_layout/Subgrid
page-type: guide
sidebar: cssref
---

The **`subgrid`** value is part of the [CSS grid layout](/en-US/docs/Web/CSS/CSS_grid_layout) module. It lets a nested grid use the tracks of its parent grid instead of defining its own. This guide explains what subgrid does, shows some common uses, and describes how it works with line names, gaps, and the implicit grid.

## Introduction to subgrid

When you add `display: grid` to a grid container, only its direct children become grid items. You can then place those items on the grid you have created. The children of those items are laid out in normal flow.

You can nest grids by making a grid item into a grid container. However, these grids are independent of the parent grid and of each other. They do not take their track sizing from the parent grid, so it is hard to line up items in a nested grid with items in the main grid.

If you set the value `subgrid` on {{cssxref("grid-template-columns")}}, {{cssxref("grid-template-rows")}}, or both, the nested grid uses the tracks defined on the parent instead of creating new ones. The nested grid's items are then sized and placed on the parent grid's tracks. Because the tracks are shared, the content of the subgrid can change the size of the parent's tracks, and items in different subgrids stay lined up with each other.

## Subgrid for columns

In the example below, the grid container has nine `1fr` column tracks and four rows that are at least `100px` tall.

The `.item` element is placed from column line 2 to column line 7, and from row line 2 to row line 4. It is a grid container itself, with `grid-template-columns: subgrid`. Its rows are defined normally with `grid-template-rows`. The child elements of `.item` use the five column tracks that the item spans on the parent, and they are laid out in rows defined on `.item`.

### HTML

```html
<div class="grid">
  <div class="item">
    <div class="subitem"></div>
  </div>
</div>
```

### CSS

```css
.grid {
  display: grid;
  grid-template-columns: repeat(9, 1fr);
  grid-template-rows: repeat(4, minmax(100px, auto));
}

.item {
  display: grid;
  grid-column: 2 / 7;
  grid-row: 2 / 4;
  grid-template-columns: subgrid;
  grid-template-rows: repeat(3, 80px);
}

.subitem {
  grid-column: 3 / 6;
  grid-row: 1 / 3;
}
```

### Result

{{EmbedLiveSample("Subgrid for columns", "", "450px")}}

Line numbering restarts inside a subgrid. Column line 1 of the subgrid is the first line that `.item` covers, which is column line 2 of the parent. This means you can create a component that is placed on a subgrid and it will behave the same way wherever the subgrid is placed in the parent.

## Subgrid for rows

The same approach works for rows. The following example uses `subgrid` for `grid-template-rows` and defines the column tracks normally on the nested grid. The nested grid's items use the rows that `.item` spans on the parent.

```css
.item {
  display: grid;
  grid-column: 2 / 7;
  grid-row: 2 / 4;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: subgrid;
}
```

## Subgrid in both dimensions

If you set `subgrid` on both `grid-template-columns` and `grid-template-rows`, the nested grid uses the parent's tracks in both dimensions.

```css
.item {
  display: grid;
  grid-column: 2 / 7;
  grid-row: 2 / 4;
  grid-template-columns: subgrid;
  grid-template-rows: subgrid;
}
```

## No implicit grid in a subgridded dimension

If you want to auto-place items and don't know how many there will be, be careful with subgrid. A subgrid can't create implicit tracks in the dimension that uses `subgrid`.

In the example below, the subgrid spans two column tracks and two row tracks of the parent, in both dimensions. That is enough room for four items. If you add a fifth or sixth item, no new rows are created. Any auto-placed items that don't fit go into the last track of the subgrid and overlap the items already there.

```css
.grid {
  display: grid;
  grid-template-columns: repeat(9, 1fr);
  grid-template-rows: repeat(4, minmax(100px, auto));
}

.item {
  display: grid;
  grid-column: 2 / 4;
  grid-row: 2 / 4;
  grid-template-columns: subgrid;
  grid-template-rows: subgrid;
}
```

If you use `subgrid` in only one dimension, the other dimension behaves like any other grid. In that dimension, the subgrid creates implicit tracks as needed, and you can size them with {{cssxref("grid-auto-rows")}} or {{cssxref("grid-auto-columns")}}. This is the most common pattern: use `subgrid` for the columns and let rows be created as content needs them.

## Gaps and subgrids

A subgrid inherits the gap sizes set on the parent with {{cssxref("gap")}}, {{cssxref("column-gap")}}, or {{cssxref("row-gap")}}. Any gap on the parent applies to the tracks that the subgrid uses.

You can override this by setting a different gap on the subgrid. Track sizes still come from the parent, but the space between the subgrid's own items changes to the new value. This is useful if you want the outer layout to have wide gutters and the content inside a component to sit closer together.

```css
.grid {
  display: grid;
  grid-template-columns: repeat(9, 1fr);
  gap: 20px;
}

.item {
  display: grid;
  grid-column: 2 / 7;
  grid-template-columns: subgrid;
  column-gap: 0;
}
```

## Named grid lines

If you use named lines on the parent grid, the subgrid inherits those names. In the example below, the parent defines lines named `col-start` and `col-end`. Items inside the subgrid can be placed with these names.

```css
.grid {
  display: grid;
  grid-template-columns:
    1fr 1fr 1fr [col-start] 1fr 1fr 1fr [col-end] 1fr 1fr 1fr;
}

.item {
  display: grid;
  grid-column: 1 / -1;
  grid-template-columns: subgrid;
}

.subitem {
  grid-column: col-start / col-end;
}
```

You can also add line names on the subgrid itself. To do this, write a list of line names after the `subgrid` keyword. Each set of brackets names the next line of the subgrid, in order. The names are added to any names inherited from the parent.

```css
.item {
  display: grid;
  grid-column: 1 / -1;
  grid-template-columns: subgrid [line1] [line2] [line3] [line4];
}
```

## Using subgrid to align components

A common use of subgrid is a set of cards in which each card has a title, body text, and footer. If each card is its own grid, a card with a longer title pushes its body text down, and the parts of the cards don't line up with each other.

With subgrid, each card spans three rows of the parent and uses `grid-template-rows: subgrid`. Because all the cards in a row share the same row tracks, every title, body, and footer lines up with those of the other cards. The tallest content in each row decides the size of that track.

```css
.cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  grid-auto-rows: auto auto 1fr;
  gap: 1em;
}

.card {
  display: grid;
  grid-row: span 3;
  grid-template-rows: subgrid;
  row-gap: 0.5em;
}
```

The `.card` sets its own `row-gap`, so the space between the parts of a card is smaller than the `gap` between cards.

## Specifications

{{Specifications("css.properties.grid-template-columns.subgrid")}}

## Browser compatibility

{{Compat("css.properties.grid-template-columns.subgrid")}}

## See also

- {{cssxref("grid-template-columns")}}
- {{cssxref("grid-template-rows")}}
- [Basic concepts of grid layout](/en-US/docs/Web/CSS/CSS_grid_layout/Basic_concepts_of_grid_layout)
- [Grid layout using named grid lines](/en-US/docs/Web/CSS/CSS_grid_layout/Grid_layout_using_named_grid_lines)
- [Auto-placement in grid layout](/en-US/docs/Web/CSS/CSS_grid_layout/Auto-placement_in_grid_layout)
```

The `slug` is a guess based on where MDN keeps its grid guides. Check it against the content repo before you commit the page.
