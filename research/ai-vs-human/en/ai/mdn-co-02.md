```markdown
---
title: "Multimedia: Images"
slug: Learn_web_development/Extensions/Performance/Multimedia
page-type: learn-module-chapter
sidebar: learnsidebar
---

{{PreviousMenuNext("Learn_web_development/Extensions/Performance/Perceived_performance", "Learn_web_development/Extensions/Performance/video", "Learn_web_development/Extensions/Performance")}}

Media, especially images, often make up most of the bytes a typical website downloads. A little work on your images can noticeably improve your site's performance. This article shows how to choose image formats, serve images at the right size, and control when and how the browser loads them.

<table>
  <tbody>
    <tr>
      <th scope="row">Prerequisites:</th>
      <td>
        <a href="/en-US/docs/Learn_web_development/Getting_started/Environment_setup/Installing_software">Basic software installed</a>, and basic knowledge of
        <a href="/en-US/docs/Learn_web_development/Getting_started/Your_first_website">client-side web technologies</a>.
      </td>
    </tr>
    <tr>
      <th scope="row">Objective:</th>
      <td>
        To learn about the various image formats, their impact on performance, and how to reduce the impact of images on overall page load time.
      </td>
    </tr>
  </tbody>
</table>

> [!NOTE]
> This is a high-level introduction to optimizing multimedia delivery on the web, covering general principles and techniques. For a more in-depth guide, see <https://web.dev/learn/images>.

## Why optimize your multimedia?

For the average website, a large share of the bandwidth comes from images. Some sites also serve video. Bytes spent on media are bytes the user has to download before the page is complete. On slow or metered connections, this costs your users time and money.

Images also affect user-centric performance metrics. The largest element on screen is often an image, so the time it takes to load affects [Largest Contentful Paint](/en-US/docs/Glossary/Largest_contentful_paint) (LCP). Images that load without reserved space push content around as they arrive, and this hurts [Cumulative Layout Shift](/en-US/docs/Glossary/CLS) (CLS). Optimizing media is often the easiest way to improve these numbers.

## Optimizing image delivery

Image optimization comes down to four questions:

1. Does this image need to be loaded at all, or at least right now?
2. Which format should it use?
3. What size should it be?
4. How should the browser prioritize it?

### Loading strategy

The biggest gain often comes from not loading images until they are needed. Many images sit below the fold, where the user may never scroll. Use the [`loading`](/en-US/docs/Web/HTML/Reference/Elements/img#loading) attribute to defer these images until the user scrolls close to them:

```html
<img src="photo.jpg" loading="lazy" alt="A field of sunflowers at dusk" />
```

Don't lazy-load images that are visible when the page first renders, particularly the LCP image. Lazy loading delays the request until layout is known, which slows down the content the user sees first.

You can also stop the browser from blocking on image decoding with the [`decoding`](/en-US/docs/Web/HTML/Reference/Elements/img#decoding) attribute. `decoding="async"` lets the browser render other content while it decodes the image.

### Choosing a format

Each image format suits different content:

- **Photographs**: [AVIF](/en-US/docs/Web/Media/Guides/Formats/Image_types#avif_image) and [WebP](/en-US/docs/Web/Media/Guides/Formats/Image_types#webp_image) usually produce much smaller files than JPEG at similar visual quality. JPEG remains a safe fallback.
- **Simple graphics, icons, and logos**: [SVG](/en-US/docs/Web/SVG) is a vector format. It scales to any size without losing sharpness and is often tiny. Run SVG files through a tool such as [SVGO](https://github.com/svg/svgo) to remove editor metadata.
- **Images that need transparency or exact pixels**: PNG is lossless. WebP and AVIF also support lossless compression and transparency, often with smaller files.
- **Animations**: Avoid animated GIFs, which are very large. Use a short muted, looping {{htmlelement("video")}} or an animated WebP or AVIF instead.

Use the {{htmlelement("picture")}} element to offer modern formats while keeping a fallback. The browser picks the first {{htmlelement("source")}} whose `type` it supports, and falls back to the {{htmlelement("img")}} element otherwise:

```html
<picture>
  <source type="image/avif" srcset="hero.avif" />
  <source type="image/webp" srcset="hero.webp" />
  <img src="hero.jpg" alt="Mountains reflected in a still lake" />
</picture>
```

Whatever the format, compression matters. Tools such as [Squoosh](https://squoosh.app/), or build-time plugins for your bundler, let you trade a small amount of quality for a large reduction in file size. A quality setting around 75–85 is usually indistinguishable from the original for photos.

### Serving the right size

A 4000-pixel-wide photo shown in a 400-pixel-wide column wastes most of its bytes. Use [responsive images](/en-US/docs/Web/HTML/Guides/Responsive_images) so that each device downloads a suitable size.

The [`srcset`](/en-US/docs/Web/HTML/Reference/Elements/img#srcset) attribute lists available image files and their intrinsic widths. The [`sizes`](/en-US/docs/Web/HTML/Reference/Elements/img#sizes) attribute tells the browser how wide the image will be shown at different viewport sizes. The browser combines this with the screen's pixel density to choose a file:

```html
<img
  src="garden-800.jpg"
  srcset="garden-400.jpg 400w, garden-800.jpg 800w, garden-1600.jpg 1600w"
  sizes="(width <= 600px) 100vw, 50vw"
  alt="A vegetable garden with raised beds" />
```

If you want different crops of an image at different breakpoints, a technique called _art direction_, use `<source>` elements with a `media` attribute inside `<picture>`.

### Avoiding layout shifts

Always include `width` and `height` attributes on your images:

```html
<img src="garden-800.jpg" width="800" height="533" alt="…" />
```

Browsers use these values to calculate the image's [aspect ratio](/en-US/docs/Web/CSS/Reference/Properties/aspect-ratio) and reserve space before the image downloads. This works even when CSS resizes the image, as long as you set `height: auto` along with a flexible width:

```css
img {
  max-width: 100%;
  height: auto;
}
```

### Prioritizing important images

By default, browsers don't know which image matters most until layout happens. You can give them a hint with the [`fetchpriority`](/en-US/docs/Web/HTML/Reference/Elements/img#fetchpriority) attribute. Set `fetchpriority="high"` on your LCP image so it starts downloading early:

```html
<img src="hero.jpg" fetchpriority="high" alt="…" />
```

Use this sparingly. If everything is high priority, nothing is.

Images set with CSS, such as [`background-image`](/en-US/docs/Web/CSS/Reference/Properties/background-image), are discovered only after the stylesheet has downloaded and been parsed. If such an image is important, consider using an `<img>` element instead, or [preload](/en-US/docs/Web/HTML/Reference/Attributes/rel/preload) it:

```html
<link rel="preload" as="image" href="hero.avif" type="image/avif" />
```

For responsive CSS backgrounds, the {{cssxref("image/image-set", "image-set()")}} function lets you offer several resolutions or formats.

### Delivery and caching

Images rarely change, so serve them with long-lived [`Cache-Control`](/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control) headers and include a version or hash in the filename. Then returning visitors won't download them again. An image CDN can also convert formats and resize images on the fly, based on the requesting browser.

## Conclusion

In this article, you learned how to cut image weight by choosing a suitable format, compressing it, and serving the right size with `srcset` and `sizes`. You also learned how to control loading with `loading`, `decoding`, and `fetchpriority`, and how to prevent layout shifts with `width` and `height`. In the next article, we'll cover how to optimize video to improve performance.

## See also

- [Responsive images](/en-US/docs/Web/HTML/Guides/Responsive_images)
- [Image file type and format guide](/en-US/docs/Web/Media/Guides/Formats/Image_types)
- [Lazy loading](/en-US/docs/Web/Performance/Guides/Lazy_loading)
- {{htmlelement("img")}} and {{htmlelement("picture")}} reference

{{PreviousMenuNext("Learn_web_development/Extensions/Performance/Perceived_performance", "Learn_web_development/Extensions/Performance/video", "Learn_web_development/Extensions/Performance")}}
```
