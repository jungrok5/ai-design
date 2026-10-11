# IFrame credentialless

**Experimental:** This is an experimental technology. Check the browser compatibility table before relying on it in production.

The **`credentialless`** attribute of the `<iframe>` element loads the embedded document in a new, ephemeral context. The document gets no access to the embedding site's existing credentials and storage. This lets a page that uses [cross-origin isolation](/en-US/docs/Web/API/Window/crossOriginIsolated) embed third-party documents that don't opt in to the required headers.

## Syntax

```html
<iframe src="https://example.com/widget" credentialless></iframe>
```

`credentialless` is a boolean attribute. If it's present, the iframe is credentialless. If it's absent, the iframe behaves normally.

## Description

Features such as [`SharedArrayBuffer`](/en-US/docs/Web/JavaScript/Reference/Global_Objects/SharedArrayBuffer) require the page to be cross-origin isolated. To achieve this, the page sends the [`Cross-Origin-Embedder-Policy`](/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Embedder-Policy) (COEP) header with the value `require-corp` or `credentialless`. With `require-corp`, every embedded cross-origin resource must explicitly opt in using [`Cross-Origin-Resource-Policy`](/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Resource-Policy) (CORP) or CORS. Third-party iframes often don't send these headers, so they are blocked.

The `credentialless` attribute removes that obstacle. A credentialless iframe is loaded from a fresh, empty state, so it can't expose the user's private data to the embedding page. The browser therefore doesn't require the embedded document to opt in.

### Differences from a normal iframe

A credentialless iframe differs from a normal iframe in these ways:

- **Ephemeral storage.** The document uses a new storage partition. Cookies, [`localStorage`](/en-US/docs/Web/API/Window/localStorage), [`sessionStorage`](/en-US/docs/Web/API/Window/sessionStorage), [IndexedDB](/en-US/docs/Web/API/IndexedDB_API), the [Cache API](/en-US/docs/Web/API/Cache) and service workers are all separate from the ones the same origin would normally use. The browser discards this data when the iframe is destroyed or navigated away.
- **No inherited credentials.** Requests made by the document don't carry existing cookies, client certificates or HTTP authentication. The user appears signed out.
- **Isolated from the embedder's origin.** The document is loaded in a different context even if it is same-origin with the embedding page, so it doesn't share the embedder's storage.
- **Inherited COEP behavior.** The document is treated as if it had `Cross-Origin-Embedder-Policy: credentialless`. Its own no-cors subresource requests are sent without credentials.

### Detecting credentialless contexts

The read-only [`window.credentialless`](/en-US/docs/Web/API/Window/credentialless) property returns `true` inside a credentialless iframe. The reflected [`HTMLIFrameElement.credentialless`](/en-US/docs/Web/API/HTMLIFrameElement/credentialless) property lets scripts in the embedding page read or set the attribute.

> **Note:** Changing the `credentialless` attribute after the iframe has loaded has no effect until the iframe navigates.

## Examples

### Embedding a third-party widget

The page below is cross-origin isolated. The server sends these headers:

```http
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: credentialless
```

The page can then embed a widget that sends no CORP header:

```html
<iframe
  src="https://widget.example.net/chat"
  credentialless
  title="Support chat"></iframe>
```

The widget loads, but it can't read the visitor's cookies for `widget.example.net`. A "sign in to continue" prompt may therefore appear even when the user is signed in elsewhere.

### Feature detection

```js
const frame = document.createElement("iframe");

if ("credentialless" in frame) {
  frame.credentialless = true;
  frame.src = "https://widget.example.net/chat";
} else {
  // Fall back to a link, or to a server-side integration
}

document.body.append(frame);
```

### Checking from inside the frame

```js
if (window.credentialless) {
  console.log("Running in an ephemeral, credentialless context.");
}
```

## Security considerations

Credentialless iframes protect the user's data from the embedding page. They don't protect the embedding page from a malicious document. Continue to use the [`sandbox`](/en-US/docs/Web/HTML/Reference/Elements/iframe#sandbox) attribute and a [Content Security Policy](/en-US/docs/Web/HTTP/Guides/CSP) where appropriate. The two can be combined.

## Specifications

Not currently part of a standard. The feature is described in the WICG [Anonymous iframe explainer](https://wicg.github.io/anonymous-iframe/).

## Browser compatibility

Support is currently limited to Chromium-based browsers, starting with Chrome 110. Check an up-to-date compatibility table before use.

## See also

- [`<iframe>` element](/en-US/docs/Web/HTML/Reference/Elements/iframe)
- [`Cross-Origin-Embedder-Policy`](/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Embedder-Policy) header
- [`Window.credentialless`](/en-US/docs/Web/API/Window/credentialless)
- [`Window.crossOriginIsolated`](/en-US/docs/Web/API/Window/crossOriginIsolated)
- [Cross-Origin Resource Policy (CORP)](/en-US/docs/Web/HTTP/Guides/Cross-Origin_Resource_Policy)
