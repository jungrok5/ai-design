---
title: What are browser developer tools?
slug: Learn_web_development/Getting_started/Tools/Browser_developer_tools
page-type: guide
---

# What are browser developer tools?

**Browser developer tools** are a set of built-in utilities that let you inspect, debug, and measure a web page while it runs in the browser. They show the page's HTML, CSS, and JavaScript, the network requests it makes, the performance of its rendering, and the data it stores. Every major browser ships with them: Chrome and Edge use DevTools, Firefox has its Developer Tools, and Safari provides the Web Inspector.

This guide explains what the tools are, how to open them, and what the most useful panels do.

## Opening the developer tools

You can open the developer tools in several ways:

- Press <kbd>F12</kbd> on Windows and Linux, or <kbd>Cmd</kbd>+<kbd>Option</kbd>+<kbd>I</kbd> on macOS.
- Right-click an element on the page and choose **Inspect**. This opens the tools with that element already selected in the DOM tree.
- Open the browser menu and choose the developer tools option, usually under **More tools** or **Web Developer**.

Safari hides its Web Inspector until you enable it. Open **Settings** > **Advanced** and select **Show features for web developers**, then use the **Develop** menu.

The tools can appear docked to the side or bottom of the window, or in a separate window. Most browsers let you change this in the settings panel.

## The main panels

Developer tools are organized into panels, each focused on one part of the web platform. The exact names vary between browsers, but the core set is similar.

### Elements (Inspector)

The **Elements** panel shows the live DOM, which is the structure of the page after the browser has parsed the HTML and run any scripts that changed it. This is important because the DOM may differ from the source file. You can:

- Edit element attributes and text, and see the change immediately.
- View and modify CSS rules that apply to the selected element, including the cascade and inherited properties.
- Toggle individual declarations on or off to test layout ideas.
- Check the box model, which shows an element's margin, border, padding, and content size.

The inspector is often the fastest way to find out why an element looks the way it does.

### Console

The **Console** shows messages that the page logs with `console.log()`, warnings, and errors, including uncaught exceptions and failed resource loads. It also provides a command line where you can run JavaScript in the context of the current page. You can query the DOM, call functions, or test a snippet before adding it to your code.

### Sources (Debugger)

The **Sources** panel lets you read the JavaScript and other files the page has loaded. You can set **breakpoints** that pause execution on a particular line, then step through the code one statement at a time. While paused, you can inspect the values of variables in the current scope and the call stack. Breakpoints are more useful than scattered `console.log()` calls when you need to understand the order in which code runs.

Source maps, when a site provides them, let you debug minified or transpiled code as if you were reading the original source.

### Network

The **Network** panel records every request the page makes, such as HTML, stylesheets, scripts, images, fonts, and API calls. For each request, it shows the status code, the size, the time taken, and the headers and response body. You can filter requests by type, throttle the connection to simulate a slow mobile network, and disable the cache to see what a first-time visitor downloads.

This panel is essential for diagnosing slow page loads, failed API calls, and CORS errors.

### Performance

The **Performance** panel records a profile of the page over a period of time. It shows CPU activity, scripting, style recalculation, layout, painting, and compositing, all aligned on a timeline. Long tasks and layout thrashing appear clearly in the recording, which helps you find the code responsible for dropped frames or sluggish interactions.

### Memory

The **Memory** panel takes heap snapshots and tracks allocations. You can use it to find memory leaks, such as event listeners or detached DOM nodes that are never released.

### Application (Storage)

The **Application** panel, called **Storage** in some browsers, shows data the site keeps on the client. This includes cookies, `localStorage` and `sessionStorage`, IndexedDB databases, Cache Storage used by service workers, and registered service workers and manifests. You can edit or clear this data to test how your site behaves for new and returning users.

### Accessibility and audits

Most browsers include an accessibility tree view, which shows what assistive technologies receive from the page. Chrome also includes **Lighthouse**, an audit tool that scores performance, accessibility, best practices, and search readiness, and suggests fixes.

## Device and responsive testing

Browsers include a device toolbar, often called responsive design mode, that resizes the viewport to a chosen phone or tablet size. It can simulate touch events, device pixel ratios, and user-agent strings. This is a quick way to check media queries, but it does not replace testing on real hardware, because engines, fonts, and input methods still differ.

## Debugging remote and mobile pages

When a problem appears only on a phone, you can connect the device to your computer and inspect it remotely. Chrome supports this on Android through USB debugging, and Safari can inspect pages on iOS and iPadOS devices when the Web Inspector is enabled on the device. Remote inspection gives you the same panels you use on the desktop, so you can read the DOM and console output from the real device.

## Good habits

Developer tools are most effective when you use them as part of a repeatable process:

1. Reproduce the problem first, and note the browser and viewport size.
2. Use the Console to read errors before changing code.
3. Use the Network panel to confirm that requests succeed and return the expected data.
4. Use the Elements panel to test CSS changes live before editing your stylesheet.
5. Use breakpoints for logic bugs, and the Performance panel for slowness.
6. Copy the verified change back into your source files, because edits made in the tools are not saved to disk.

The last point matters. Changes made in the Elements and Sources panels exist only in the current page session. They disappear on reload unless you save them to your project, or use a workspace feature that maps the browser's files to your local folder.

## See also

- [Debugging JavaScript](/en-US/docs/Learn_web_development/Getting_started/Tools/Debugging_JavaScript)
- [Source maps](/en-US/docs/Glossary/Source_map)
- [Web Console](/en-US/docs/Web/API/console)
- [Document Object Model (DOM)](/en-US/docs/Web/API/Document_Object_Model)
