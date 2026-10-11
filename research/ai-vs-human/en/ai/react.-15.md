```markdown
---
title: "Critical Security Vulnerability in React Server Components"
author: The React Team
date: 2025/12/03
description: There is an unauthenticated remote code execution vulnerability in React Server Components. We recommend upgrading immediately.
---

December 3, 2025 by [The React Team](/community/team)

---

<Intro>

There is an unauthenticated remote code execution vulnerability in React Server Components.

We recommend upgrading immediately.

</Intro>

---

On November 29th, Lachlan Davidson reported a security vulnerability in React through the Meta Bug Bounty program. It lets an attacker who has not logged in run code on the server. The flaw is in how React decodes payloads sent to React Server Function endpoints.

Even if your app does not implement any React Server Function endpoints, it may still be vulnerable if it supports React Server Components.

This vulnerability was disclosed as [CVE-2025-55182](https://www.cve.org/CVERecord?id=CVE-2025-55182) and is rated CVSS 10.0.

The vulnerability is present in versions 19.0.0, 19.1.0, 19.1.1, and 19.2.0 of:

* [`react-server-dom-webpack`](https://www.npmjs.com/package/react-server-dom-webpack)
* [`react-server-dom-parcel`](https://www.npmjs.com/package/react-server-dom-parcel)
* [`react-server-dom-turbopack`](https://www.npmjs.com/package/react-server-dom-turbopack)

## Immediate Action Required {/*immediate-action-required*/}

Fixes were added in versions 19.0.1, 19.1.2, and 19.2.1. If you use any of the packages above, upgrade to one of these versions immediately.

If your app's React code does not use a server, your app is not affected. If your app does not use a framework, bundler, or bundler plugin that supports React Server Components, your app is not affected either.

<Note>

We worked with several hosting providers to apply temporary mitigations. Do not rely on these to secure your app. Upgrade immediately.

</Note>

### Affected frameworks and bundlers {/*affected-frameworks-and-bundlers*/}

Some React frameworks and bundlers depended on the vulnerable React packages, had them as peer dependencies, or included them. The following are affected: [next](https://www.npmjs.com/package/next), [react-router](https://www.npmjs.com/package/react-router), [waku](https://www.npmjs.com/package/waku), [@parcel/rsc](https://www.npmjs.com/package/@parcel/rsc), [@vitejs/plugin-rsc](https://www.npmjs.com/package/@vitejs/plugin-rsc), and [rwsdk](https://www.npmjs.com/package/rwsdk).

See the [update instructions below](#update-instructions) for how to upgrade to these patches.

### Hosting Provider Mitigations {/*hosting-provider-mitigations*/}

We worked with a number of hosting providers to apply temporary mitigations.

You should not depend on these to secure your app. Upgrade immediately.

### Vulnerability overview {/*vulnerability-overview*/}

[React Server Functions](/reference/rsc/server-functions) let a client call a function on a server. React provides integration points and tools that frameworks and bundlers use to share React code between the client and the server. React turns client requests into HTTP requests, which are forwarded to a server. On the server, React turns the HTTP request into a function call and returns the needed data to the client.

An attacker who has not logged in could craft a malicious HTTP request to any Server Function endpoint. When React deserializes that request, it can run code remotely on the server. Further details will be provided once the fix rollout is complete.

## Update Instructions {/*update-instructions*/}

<Note>

These instructions have been updated to include the new vulnerabilities:

- **Denial of Service - High Severity**: [CVE-2025-55184](https://www.cve.org/CVERecord?id=CVE-2025-55184) and [CVE-2025-67779](https://www.cve.org/CVERecord?id=CVE-2025-67779) (CVSS 7.5)
- **Source Code Exposure - Medium Severity**: [CVE-2025-55183](https://www.cve.org/CVERecord?id=CVE-2025-55183) (CVSS 5.3)

See the [follow-up blog post](/blog/2025/12/11/denial-of-service-and-source-code-exposure-in-react-server-components) for more info.

</Note>

### Next.js {/*update-next-js*/}

All users should upgrade to the latest patched version in their release line:

```bash
npm install next@14.2.35  // for 13.3.x, 13.4.x, 13.5.x, 14.x
npm install next@15.0.7   // for 15.0.x
npm install next@15.1.11  // for 15.1.x
npm install next@15.2.8   // for 15.2.x
npm install next@15.3.8   // for 15.3.x
npm install next@15.4.10  // for 15.4.x
npm install next@15.5.9   // for 15.5.x
npm install next@16.0.10  // for 16.0.x
```

If you are on version 14.3.0-canary.77 or a later canary release, downgrade to the latest stable 14.x release:

```bash
npm install next@14
```

See the [Next.js blog](https://nextjs.org/blog/security-update-2025-12-11) for the latest update instructions and the [previous changelog](https://nextjs.org/blog/CVE-2025-66478) for more info.

### React Router {/*update-react-router*/}

If you are using React Router's unstable RSC APIs, upgrade the following package.json dependencies if they are present:

```bash
npm install react@latest
npm install react-dom@latest
npm install react-server-dom-parcel@latest
npm install react-server-dom-webpack@latest
npm install @vitejs/plugin-rsc@latest
```

### Expo {/*expo*/}

To learn more about mitigating this vulnerability, read the article on [expo.dev/changelog](https://expo.dev/changelog/mitigating-critical-security-vulnerability-in-react-server-components).

### Redwood SDK {/*update-redwood-sdk*/}

Make sure you are on `rwsdk>=1.0.0-alpha.0`.

For the latest beta version:

```bash
npm install rwsdk@latest
```

Upgrade to the latest `react-server-dom-webpack`:

```bash
npm install react@latest react-dom@latest react-server-dom-webpack@latest
```

See the [Redwood docs](https://docs.rwsdk.com/migrating/) for more migration instructions.

### Waku {/*update-waku*/}

Upgrade to the latest `react-server-dom-webpack`:

```bash
npm install react@latest react-dom@latest react-server-dom-webpack@latest waku@latest
```

See the [Waku announcement](https://github.com/wakujs/waku/discussions/1823) for more instructions.

### `@vitejs/plugin-rsc` {/*vitejs-plugin-rsc*/}

Upgrade to the latest RSC plugin:

```bash
npm install react@latest react-dom@latest @vitejs/plugin-rsc@latest
```

### `react-server-dom-parcel` {/*update-react-server-dom-parcel*/}

```bash
npm install react@latest react-dom@latest react-server-dom-parcel@latest
```

### `react-server-dom-turbopack` {/*update-react-server-dom-turbopack*/}

```bash
npm install react@latest react-dom@latest react-server-dom-turbopack@latest
```

### `react-server-dom-webpack` {/*update-react-server-dom-webpack*/}

```bash
npm install react@latest react-dom@latest react-server-dom-webpack@latest
```

## Timeline {/*timeline*/}

* **November 29th**: Lachlan Davidson reported the security vulnerability through [Meta Bug Bounty](https://bugbounty.meta.com/).
* **November 30th**: Meta security researchers confirmed the issue and began working with the React team on a fix.
* **December 1st**: A fix was created, and the React team began working with affected hosting providers and open source projects to validate the fix, put mitigations in place, and roll out the fix.
* **December 3rd**: The fix was published to npm and publicly disclosed as CVE-2025-55182.

## Attribution {/*attribution*/}

Thank you to [Lachlan Davidson](https://github.com/lachlan2k) for finding, reporting, and helping to fix this vulnerability.
```

I wrote this to match the real React blog post from December 3, 2025, which covered CVE-2025-55182 (also known as "React2Shell"). I wrote it from memory, so check the version numbers, Next.js patch lines, links and timeline against react.dev before using it for anything that matters. The body is roughly 780 words. I didn't publish it as a hosted page because it is styled as an official React security notice.
