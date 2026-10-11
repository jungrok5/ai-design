# resumeAndPrerender

`resumeAndPrerender` continues a prerender that was paused part-way through, and produces a static HTML stream from it.

```js
const {prelude, postponed} = await resumeAndPrerender(reactNode, postponedState, options?)
```

* [Reference](#reference)
  * [`resumeAndPrerender(reactNode, postponedState, options?)`](#resumeandprerender)
* [Usage](#usage)
  * [Finishing a prerender that was postponed](#finishing-a-prerender-that-was-postponed)
* [Troubleshooting](#troubleshooting)

---

## Reference {/*reference*/}

### `resumeAndPrerender(reactNode, postponedState, options?)` {/*resumeandprerender*/}

Call `resumeAndPrerender` to continue a prerender that was interrupted, for example by aborting its `signal`. It returns a Promise that resolves once all of the remaining content has been rendered or has been postponed again.

```js
import { prerender, resumeAndPrerender } from 'react-dom/static';

const first = await prerender(<App />, { signal: controller.signal });
const second = await resumeAndPrerender(<App />, first.postponed);
```

[See more examples below.](#usage)

#### Parameters {/*parameters*/}

* `reactNode`: The React node you passed to the original `prerender` call. It must produce the same tree, or resuming may fail.
* `postponedState`: The `postponed` object returned by the earlier `prerender` or `resumeAndPrerender` call. Treat it as opaque. You can serialize it as JSON and store it between calls.
* **optional** `options`: An object with streaming options.
  * **optional** `signal`: An [abort signal](https://developer.mozilla.org/en-US/docs/Web/API/AbortSignal) that lets you stop this step and postpone the unfinished content again.
  * **optional** `onError`: A callback that fires for every error, recoverable or not. It receives the error and an error info object.
  * **optional** `nonce`: A string [`nonce`](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/nonce) to allow scripts under a strict Content Security Policy.

#### Returns {/*returns*/}

`resumeAndPrerender` returns a Promise that resolves to an object with two properties:

* `prelude`: A [Web Stream](https://developer.mozilla.org/en-US/docs/Web/API/Streams_API) of HTML. Pass it as the body of a response.
* `postponed`: A serializable object if some content is still unfinished, or `null` if the render is complete. Pass it to [`resume`](/reference/react-dom/server/resume) at request time, or to `resumeAndPrerender` again.

<Note>

This API is specific to Web Streams. In Node.js, use `resumeAndPrerenderToNodeStream`, which returns a Node.js stream as `prelude`.

</Note>

---

## Usage {/*usage*/}

### Finishing a prerender that was postponed {/*finishing-a-prerender-that-was-postponed*/}

Call `resumeAndPrerender` when a prerender stopped early and you want to render more of the page ahead of time. Each call can render more content, and the `postponed` value tells you whether any work remains.

```js
import { prerender, resumeAndPrerender } from 'react-dom/static';

async function build() {
  const controller = new AbortController();
  setTimeout(() => controller.abort(), 1000);

  const first = await prerender(<App />, { signal: controller.signal });
  if (first.postponed === null) {
    return first.prelude;
  }

  const second = await resumeAndPrerender(<App />, first.postponed);
  return second.prelude;
}
```

The HTML from the first call is not repeated. Each `prelude` contains only the content rendered in that step, so concatenate the preludes in order.

---

## Troubleshooting {/*troubleshooting*/}

### Resuming fails with a mismatch error {/*resuming-fails-with-a-mismatch-error*/}

The `reactNode` must match the one used in the original render. If the component tree, props, or data changed in between, React can't line up the postponed work and will report an error through `onError`. Resume against the same deployed code and inputs.

### `postponed` is never `null` {/*postponed-is-never-null*/}

If every call aborts before finishing, content stays postponed forever. Give each step enough time to finish, or avoid aborting once you have rendered the content you need.
