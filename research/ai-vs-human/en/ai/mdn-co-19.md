# HTTP Client hints

**HTTP Client hints** are a set of request headers that a user agent (browser) sends to a server to describe the client's device, network, and user preferences. A server can ask for specific hints in a response, so it can adapt content such as image resolution, layout, or language to the client without relying on the `User-Agent` string.

## Overview

Client hints solve a problem with the `User-Agent` header. That string is a long, legacy mix of browser names and version numbers, and servers have often used it to guess device capabilities. This leads to fragile browser sniffing. Client hints replace that guesswork with structured, named headers that carry specific values.

Client hints fall into three groups:

- **Low-entropy hints** are sent by default on every request. They reveal little about the user, so browsers send them without asking.
- **High-entropy hints** reveal more identifying detail, such as the exact OS version. Browsers send them only when the server has requested them.
- **Device and network hints** describe the screen, memory, color scheme, or connection quality. They are also sent only when requested.

Client hints are available only in [secure contexts](/en-US/docs/Web/Security/Secure_Contexts), which means over HTTPS.

## Default (low-entropy) hints

Browsers send the following headers on every request by default:

| Header | Example value | Meaning |
| --- | --- | --- |
| `Sec-CH-UA` | `"Chromium";v="130", "Not?A_Brand";v="99"` | Brand and major version of each browser component |
| `Sec-CH-UA-Mobile` | `?0` | `?1` if the client is a mobile device |
| `Sec-CH-UA-Platform` | `"Windows"` | Operating system family |

These headers are useful for simple decisions, such as whether to send a mobile layout. They reveal enough to guide most rendering choices without exposing a fingerprint.

## Requesting high-entropy hints

A server requests additional hints by sending the `Accept-CH` response header. The value is a comma-separated list of hint names:

```http
Accept-CH: Sec-CH-UA-Full-Version-List, Sec-CH-UA-Platform-Version, Sec-CH-UA-Arch
```

The browser stores this preference for the origin. On later requests to the same origin, it sends the listed hints. The first response that asks for them cannot benefit from them, so the server must handle that first request without the hints.

Some hints are marked as **critical** using the `Critical-CH` header. If a browser receives a `Critical-CH` response, it knows the server cannot respond correctly without those hints. It then retries the request with the hints attached, so the first response is still correct:

```http
Accept-CH: Sec-CH-DPR, Sec-CH-Viewport-Width
Critical-CH: Sec-CH-DPR
```

Common high-entropy hints include `Sec-CH-UA-Full-Version-List`, `Sec-CH-UA-Platform-Version`, `Sec-CH-UA-Arch`, `Sec-CH-UA-Model`, and `Sec-CH-UA-Bitness`.

## Device and preference hints

These hints describe the user's environment and settings:

- `Sec-CH-Prefers-Color-Scheme` reports `light` or `dark`, so the server can send a matching theme.
- `Sec-CH-Prefers-Reduced-Motion` reports `reduce` when the user has asked for less animation.
- `Sec-CH-Prefers-Reduced-Transparency` and `Sec-CH-Prefers-Contrast` report comparable accessibility preferences.
- `Sec-CH-Prefers-Reduced-Data` reports a user preference to conserve bandwidth.
- `Device-Memory` reports approximate RAM in gigabytes, rounded down to a power of two.
- `Sec-CH-DPR` reports the device pixel ratio, and `Sec-CH-Viewport-Width` reports the layout viewport width in CSS pixels.

Some older network and image hints, such as `Save-Data`, `Downlink`, `ECT`, `RTT`, `DPR`, `Width`, and `Viewport-Width`, have been deprecated or removed in some browsers. Check current browser support before relying on them.

## Using hints in server code

A server can read hints to choose the right resource. The following Node.js example selects an image size based on the device pixel ratio and viewport width:

```js
import http from "node:http";

http.createServer((req, res) => {
  // Ask for hints on future requests.
  res.setHeader(
    "Accept-CH",
    "Sec-CH-DPR, Sec-CH-Viewport-Width, Sec-CH-Prefers-Color-Scheme",
  );

  const dpr = Number(req.headers["sec-ch-dpr"]) || 1;
  const width = Number(req.headers["sec-ch-viewport-width"]) || 1024;
  const scheme = req.headers["sec-ch-prefers-color-scheme"] === "dark"
    ? "dark"
    : "light";

  // Pick an image that is sharp on this screen without oversending bytes.
  const imageWidth = Math.min(Math.round(width * dpr), 2400);

  res.setHeader("Content-Type", "text/html");
  res.end(`<img src="/hero?w=${imageWidth}&theme=${scheme}" alt="">`);
}).listen(8080);
```

## Caching and the Vary header

Responses can change depending on client hints, so caches must know which headers affected the response. Servers should list those headers in `Vary`:

```http
Vary: Sec-CH-UA-Mobile, Sec-CH-DPR
```

Without `Vary`, a shared cache might serve a mobile layout to a desktop user, or a low-resolution image to a high-density screen. Each `Vary` entry adds a dimension to the cache key, so list only the hints that actually change the response.

## Third-party and cross-origin use

Client hints are sent to the origin that requested them. A request to a third-party origin, such as an embedded iframe or an image CDN, does not include hints unless that origin has requested them and the embedding page permits it.

To allow cross-origin delegation, the top-level page uses the [`Permissions-Policy`](/en-US/docs/Web/HTTP/Reference/Headers/Permissions-Policy) header to control which origins may receive each hint:

```http
Permissions-Policy: ch-prefers-color-scheme=(self "https://cdn.example")
```

An iframe can also receive hints through the `allow` attribute, which is the easiest way to pass hints to embedded content from a trusted origin.

## Privacy considerations

Client hints give servers more information than a default browser exposes, so browsers limit high-entropy values. Servers must request only the hints they need, and they should not use hints to build long-term identifiers of users. Browsers may reduce, round, or omit values, and users can disable hints in their settings. Code should always work when a hint is missing.

## Browser compatibility

Chromium-based browsers support most client hints. Firefox and Safari support a smaller set, so fallback behavior matters. Treat every hint as optional, and provide a sensible default when a header is absent.

## See also

- [`Accept-CH`](/en-US/docs/Web/HTTP/Reference/Headers/Accept-CH)
- [`Critical-CH`](/en-US/docs/Web/HTTP/Reference/Headers/Critical-CH)
- [`Permissions-Policy`](/en-US/docs/Web/HTTP/Reference/Headers/Permissions-Policy)
- [`NavigatorUAData`](/en-US/docs/Web/API/NavigatorUAData) API
- [`Vary`](/en-US/docs/Web/HTTP/Reference/Headers/Vary)
