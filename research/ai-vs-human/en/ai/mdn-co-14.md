```md
---
title: Measuring performance
slug: Learn_web_development/Extensions/Performance/Measuring_performance
page-type: learn-module-chapter
sidebar: learnsidebar
---

{{PreviousMenuNext("Learn_web_development/Extensions/Performance/Perceived_performance", "Learn_web_development/Extensions/Performance/Multimedia", "Learn_web_development/Extensions/Performance")}}

Measuring performance gives you numbers you can track over time. With them, you can see whether your site is getting faster or slower and tell whether a change helped. This article covers the main performance metrics, the tools you can use to collect them, and the browser APIs that let you measure performance from your own code.

<table>
  <tbody>
    <tr>
      <th scope="row">Prerequisites:</th>
      <td>
        Basic familiarity with <a href="/en-US/docs/Learn_web_development/Core/Structuring_content">HTML</a>,
        <a href="/en-US/docs/Learn_web_development/Core/Styling_basics">CSS</a>, and
        <a href="/en-US/docs/Learn_web_development/Core/Scripting">JavaScript</a>, and a basic understanding of
        <a href="/en-US/docs/Learn_web_development/Extensions/Performance/why_web_performance">why web performance matters</a>.
      </td>
    </tr>
    <tr>
      <th scope="row">Learning outcomes:</th>
      <td>
        <ul>
          <li>Understand the main web performance metrics, including the Core Web Vitals.</li>
          <li>Understand the difference between lab data and field data.</li>
          <li>Use performance tools and browser developer tools to measure a site.</li>
          <li>Use performance APIs to measure performance in JavaScript.</li>
        </ul>
      </td>
    </tr>
  </tbody>
</table>

## Why measure?

You can't fix a performance problem until you can see it. A page might feel fast on your development machine, which has a fast processor and a wired connection. The same page can feel slow to someone on a budget phone with a weak mobile signal. Measuring helps you:

- Find out where the time goes: network requests, script execution, rendering, or something else.
- Set a **performance budget**, which is a limit on things like page weight or load time, and check that new work stays within it.
- Show that an optimization actually helped, instead of guessing.
- Catch regressions before your users notice them.

## Key metrics

There are many ways to describe how fast a page is. These are some of the most useful:

- [Time to First Byte (TTFB)](/en-US/docs/Glossary/Time_to_first_byte)
  - : The time between the browser requesting a page and receiving the first byte of the response. A high TTFB usually points to a slow server or network.
- [First Contentful Paint (FCP)](/en-US/docs/Glossary/First_contentful_paint)
  - : The time until the browser renders the first piece of content from the DOM, such as text or an image. This tells the user that something is happening.
- [Largest Contentful Paint (LCP)](/en-US/docs/Web/API/LargestContentfulPaint)
  - : The time until the largest image or text block in the viewport is rendered. This is a good stand-in for when the main content has loaded.
- [Interaction to Next Paint (INP)](/en-US/docs/Glossary/Interaction_to_next_paint)
  - : How quickly the page responds to user input. It covers clicks, taps, and key presses across the whole time the user spends on the page.
- [Cumulative Layout Shift (CLS)](/en-US/docs/Glossary/CLS)
  - : How much visible content moves around unexpectedly while the page loads, for example when an image without set dimensions pushes text down.

LCP, INP, and CLS make up Google's **Core Web Vitals**. They are widely used as a basic measure of user experience.

## Lab data and field data

Performance data comes in two kinds:

- **Lab data** is collected in a controlled setting, with a set device, network speed, and location. It is easy to repeat, so it works well for debugging and for comparing two versions of a page.
- **Field data**, also called real user monitoring (RUM), is collected from real visitors. It shows how your site actually performs across many different devices and networks. However, it is noisier and harder to trace back to a specific cause.

You need both. Lab tests help you find and fix problems. Field data tells you whether those problems affect real people.

## Performance tools

Several free tools can measure a page and suggest improvements:

- **[Lighthouse](https://developer.chrome.com/docs/lighthouse/overview/)** is built into Chrome's developer tools and is also available as a command-line tool. It loads your page under simulated conditions and gives a score, a list of metrics, and specific suggestions.
- **[PageSpeed Insights](https://pagespeed.web.dev/)** runs Lighthouse on any public URL. Where enough real-user data exists, it also shows field data from the Chrome User Experience Report.
- **[WebPageTest](https://www.webpagetest.org/)** tests your page from real browsers in different locations and on different connection speeds. It produces detailed waterfall charts and filmstrip views of the page loading.

## Browser developer tools

Every major browser includes developer tools for looking into performance in detail:

- The **Network** panel lists every request the page makes, with its size, timing, and priority. You can also throttle the connection to simulate a slower network. See the [Firefox Network Monitor](https://firefox-source-docs.mozilla.org/devtools-user/network_monitor/) as an example.
- The **Performance** panel records what the browser does while the page runs, including script execution, style calculation, layout, and painting. Long tasks that block the main thread show up clearly. See the [Firefox Profiler](https://profiler.firefox.com/docs/) for details.

When you test, use a private window or turn off browser extensions, because they can skew the results. Also run each test more than once, since timings vary from run to run.

## Measuring with performance APIs

The [Performance API](/en-US/docs/Web/API/Performance_API) lets you take measurements in JavaScript and send them to your own analytics. This is how most RUM is done.

For a high-precision timestamp, use {{domxref("Performance.now()", "performance.now()")}}:

```js
const start = performance.now();
doSomethingExpensive();
const duration = performance.now() - start;
console.log(`That took ${duration} milliseconds`);
```

To mark specific moments in your code and measure the time between them, use {{domxref("Performance.mark()", "performance.mark()")}} and {{domxref("Performance.measure()", "performance.measure()")}`. These entries also appear in the browser's Performance panel:

```js
performance.mark("search-start");
await runSearch();
performance.mark("search-end");

const measure = performance.measure(
  "search-duration",
  "search-start",
  "search-end",
);
console.log(measure.duration);
```

The browser also records its own performance entries, such as resource timings, paint timings, and LCP candidates. You can watch for these as they happen with a {{domxref("PerformanceObserver")}}:

```js
const observer = new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    console.log("LCP candidate:", entry.startTime, entry.element);
  }
});
observer.observe({ type: "largest-contentful-paint", buffered: true });
```

The `buffered: true` option includes entries that were recorded before the observer was created. This matters because your script may run after the page has already started painting.

## Summary

Measuring performance turns "it feels slow" into something you can act on. Decide which metrics matter for your site, set a budget for them, and use lab tools to investigate problems. Then use field data to confirm that your fixes help real users. In the next article, we'll look at how to optimize multimedia, which is often the biggest single factor in page weight.

## See also

- [Web performance](/en-US/docs/Web/Performance)
- [Performance API](/en-US/docs/Web/API/Performance_API)
- [Performance budget](/en-US/docs/Web/Performance/Guides/Performance_budgets)

{{PreviousMenuNext("Learn_web_development/Extensions/Performance/Perceived_performance", "Learn_web_development/Extensions/Performance/Multimedia", "Learn_web_development/Extensions/Performance")}}
```
