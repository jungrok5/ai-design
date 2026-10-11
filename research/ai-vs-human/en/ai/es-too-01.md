# dedent

Removes the common leading whitespace from every line of a string. This lets you indent multi-line strings to match the surrounding code without the indentation ending up in the output.

```js
import { dedent } from 'utilkit';
```

## Signature

```ts
dedent(input: string | TemplateStringsArray, ...values: unknown[]): string
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `input` | `string \| TemplateStringsArray` | The text to dedent. You can pass a plain string or use `dedent` as a template tag. |
| `...values` | `unknown[]` | Values to interpolate. These are only used when `dedent` is called as a template tag. |

## Returns

`string`: A new string with the shared indentation removed. The original input is never modified.

## Description

`dedent` scans every non-blank line and finds the smallest number of leading whitespace characters. It then removes that many characters from the start of each line. Lines that contain only whitespace are ignored when measuring the indentation, and they become empty in the output.

`dedent` also removes a single leading newline and a single trailing newline, along with any whitespace on that last line. Because of this, a template literal can start and end on its own line without adding blank lines to the result.

When `dedent` is used as a tag, interpolation happens **after** the indentation is removed. Multi-line values are inserted exactly as they are and do not change how the indentation is measured.

## Examples

```js
const message = dedent`
  Hello, ${name}!
    Your order has shipped.
  Thanks for shopping with us.
`;
// "Hello, Ada!\n  Your order has shipped.\nThanks for shopping with us."
```

You can also call it as a regular function:

```js
dedent('    a\n      b\n    c');
// "a\n  b\nc"
```

## Notes

- Tabs and spaces are counted as one character each. If a string mixes the two, the result may not line up as expected.
- Escape sequences such as `\n` inside the template are processed normally.

## See also

- [`indent`](./indent.md)
- [`trimLines`](./trimLines.md)
