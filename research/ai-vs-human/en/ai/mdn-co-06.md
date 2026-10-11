---
title: Grid lanes layout
slug: Web/CSS/CSS_grid_layout/Grid_lanes_layout
page-type: css-guide
status:
  - experimental
---

**Grid lanes layout** is a CSS layout model that arranges items in columns (or rows) of uneven length, packing each item into the lane with the most available space. It is often called a "masonry" or "waterfall" layout, and it's commonly used for image galleries and card feeds.

## Overview

Unlike standard [grid layout](/en-US/docs/Web/CSS/CSS_grid_layout), where items align to shared row tracks, grid lanes layout defines tracks in only one axis. Items flow along the other axis without row alignment. Each item is placed in the lane that lets it sit closest to the start edge, which removes the gaps that appear when items have different heights.

## Creating a grid lanes container

Set the [`display`](/en-US/docs/Web/CSS/display) property to `grid-lanes`, then define the lanes with [`grid-template-columns`](/en-US/docs/Web/CSS/grid-template-columns).

```css
.gallery {
  display: grid-lanes;
  grid-template-columns: repeat(auto-fill, minmax(14rem, 1fr));
  gap: 1rem;
}
```

```html
<div class="gallery">
  <img src="photo-1.jpg" alt="A lighthouse at dusk" />
  <img src="photo-2.jpg" alt="A mountain trail" />
  <img src="photo-3.jpg" alt="A city street" />
</div>
```

Here the browser creates as many 14rem-minimum lanes as fit, and each image is placed in the shortest one.

## Item placement

Items are placed in source order, so the visual order may differ from the DOM order. Keep this in mind for keyboard navigation and screen readers, as it can cause accessibility problems.

An item can span several lanes with [`grid-column`](/en-US/docs/Web/CSS/grid-column), for example `grid-column: span 2`. Authors can also pin an item to a specific lane.

## Controlling lane choice

Items normally go to the shortest lane, but small height differences can make the layout jump around unpredictably. The `flow-tolerance` property sets how much shorter a lane must be before an item moves to it. A larger tolerance keeps the order closer to the source.

## Browser support

Grid lanes layout is experimental, and its syntax may change. Check the compatibility table before using it in production, and provide a fallback such as multi-column or standard grid layout.

## See also

- [CSS grid layout](/en-US/docs/Web/CSS/CSS_grid_layout)
- [`display`](/en-US/docs/Web/CSS/display)
- [`gap`](/en-US/docs/Web/CSS/gap)
