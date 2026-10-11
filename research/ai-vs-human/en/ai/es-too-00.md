# AI Integration

The `ai` module provides helpers for calling language model providers from JavaScript. It normalizes request options, retries transient failures, and streams responses as async iterables. Unless noted otherwise, every function returns a promise.

## `createClient(options)`

Creates a reusable client bound to one provider and API key.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `provider` | `string` | None | Provider identifier, such as `"anthropic"` or `"openai"`. |
| `apiKey` | `string` | None | Secret key. Read from the environment when omitted. |
| `timeout` | `number` | `30000` | Request timeout in milliseconds. |
| `maxRetries` | `number` | `2` | Retries for network errors and HTTP 429 or 5xx responses. |

Returns a `Client` object. Create one client per application and share it across requests.

## `client.complete(prompt, options?)`

Sends a single prompt and resolves with the full response text.

Options include `model` (string, required), `temperature` (number from 0 to 1, default `1`), and `maxTokens` (number, default `1024`).

## `client.stream(prompt, options?)`

Returns an async iterable of text chunks. Consume it with `for await`. To cancel, break out of the loop or pass an `AbortSignal` through the `signal` option.

## `estimateTokens(text)`

Synchronous. Returns an approximate token count for `text`. Results are estimates and may differ from provider billing.

## Errors

Failed requests reject with an `AIError` that includes `status`, `code`, and `retryable` fields. Check `retryable` before writing your own retry logic, because the client has already retried those errors up to `maxRetries`.

```js
import { createClient } from "fluxkit/ai";

const client = createClient({ provider: "anthropic" });
const text = await client.complete("Summarize this release.", {
  model: "claude-haiku-5-5",
});
```
