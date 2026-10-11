```markdown
---
title: The HTML5 input types
slug: Learn_web_development/Extensions/Forms/HTML5_input_types
page-type: learn-module-chapter
sidebar: learnsidebar
---

{{PreviousMenuNext("Learn_web_development/Extensions/Forms/Basic_native_form_controls", "Learn_web_development/Extensions/Forms/Other_form_controls", "Learn_web_development/Extensions/Forms")}}

In the [previous article](/en-US/docs/Learn_web_development/Extensions/Forms/Basic_native_form_controls), we looked at the {{htmlelement("input")}} element and the values of its `type` attribute that have been around since the early days of HTML. Now we'll look at the newer form controls in detail. HTML5 added several new input types to collect specific kinds of data, along with new attributes to control them.

<table>
  <tbody>
    <tr>
      <th scope="row">Prerequisites:</th>
      <td>
        A basic understanding of <a href="/en-US/docs/Learn_web_development/Core/Structuring_content">HTML</a>.
      </td>
    </tr>
    <tr>
      <th scope="row">Learning outcomes:</th>
      <td>
        <ul>
          <li>Knowing which input types are available for collecting specific kinds of data.</li>
          <li>Understanding the validation and user interface benefits that these types provide.</li>
          <li>Knowing how browsers support these types and what happens when one isn't supported.</li>
        </ul>
      </td>
    </tr>
  </tbody>
</table>

> [!NOTE]
> Most of the features discussed in this article are well supported across browsers. Where support differs, we note it. If you want more detail, look at the reference pages for each input type, which include browser compatibility tables.

Because the look of HTML form controls can be very different from what a designer specifies, web developers sometimes build their own custom form controls. We cover this in an advanced tutorial: [How to build custom form widgets](/en-US/docs/Learn_web_development/Extensions/Forms/How_to_build_custom_form_controls).

## Email address field

You can create this type of field by setting the [`type`](/en-US/docs/Web/HTML/Reference/Elements/input#type) attribute to `email`:

```html
<input type="email" id="email" name="email" />
```

When this `type` is used, the user must type a valid email address into the field. Any other content causes the browser to display an error when the form is submitted.

You can also use the [`multiple`](/en-US/docs/Web/HTML/Reference/Attributes/multiple) attribute with the `email` input type. This allows the user to enter several email addresses in the same input, separated by commas:

```html
<input type="email" id="email" name="email" multiple />
```

On some devices, especially touch devices with on-screen keyboards such as smartphones, a different virtual keypad might appear for typing email addresses. It typically includes the `@` key by default.

> [!NOTE]
> You can find examples of the basic text input types at [basic input examples](https://mdn.github.io/learning-area/html/forms/basic-input-examples/) (see the [source code](https://github.com/mdn/learning-area/blob/main/html/forms/basic-input-examples/index.html) also).

This is another good reason to use these newer input types, improving the user experience for users of these devices.

### Client-side validation

As you can see above, `email` — along with other newer `input` types — provides built-in _client-side_ error validation, performed by the browser before the data gets sent to the server. It _is_ a helpful aid to guide users to fill out a form accurately, and it can save time: it is useful to know that your data is not correct immediately, rather than having to wait for a round trip to the server.

But it _should not be considered_ an exhaustive security measure! Your apps should always perform security checks on any form-submitted data on the _server-side_ as well as the client-side, because client-side validation is too easy to turn off, so malicious users can still easily send bad data through to your server. Read [Website security](/en-US/docs/Learn_web_development/Extensions/Server-side/First_steps/Website_security) for an idea of what _could_ happen.

Note also that `a@b` is a valid email address according to the default provided constraints. This is because the `email` input type allows intranet email addresses by default. To implement different validation behavior, you can use the [`pattern`](/en-US/docs/Web/HTML/Reference/Attributes/pattern) attribute.

## Search field

Search fields are intended to be used to create search boxes on pages and apps. This type of field is set by using the value `search` for the [`type`](/en-US/docs/Web/HTML/Reference/Elements/input#type) attribute:

```html
<input type="search" id="search" name="search" />
```

The main difference between a `text` field and a `search` field is how the browser styles its appearance. Often, `search` fields are rendered with rounded corners; they also sometimes display an "Ⓧ", which clears the field of any value when clicked. Additionally, on devices with dynamic keyboards, the keyboard's enter key may read "**search**", or display a magnifying glass icon.

It's also worth noting that the values of a `search` field can be automatically saved and reused to offer auto-completion across multiple pages of the same website.

## Phone number field

A special field for filling in phone numbers can be created using `tel` as the value of the [`type`](/en-US/docs/Web/HTML/Reference/Elements/input#type) attribute:

```html
<input type="tel" id="tel" name="tel" />
```

When accessed via a touch device with a dynamic keyboard, most devices will display a numeric keypad when `type="tel"` is encountered, meaning this type is useful whenever a numeric keypad is useful, and doesn't just have to be used for telephone numbers.

Due to the wide variety of phone number formats around the world, this type of field does not enforce any constraints on the value entered by a user. This is why it can include letters and other characters. You can use the [`pattern`](/en-US/docs/Web/HTML/Reference/Attributes/pattern) attribute to enforce a particular format.

## URL field

A special type of field for entering URLs can be created using the value `url` for the [`type`](/en-US/docs/Web/HTML/Reference/Elements/input#type) attribute:

```html
<input type="url" id="url" name="url" />
```

It adds special validation constraints to the field. The browser will report an error if no protocol (such as `http:`) is entered, or if the URL is otherwise malformed. On devices with dynamic keyboards, the default keyboard will often display some or all of the colon, period, and forward slash as default keys.

> [!NOTE]
> Just because the URL is well-formed doesn't necessarily mean that it refers to a location that actually exists!

## Numeric field

Controls for entering numbers can be created with an {{HTMLElement("input")}} [`type`](/en-US/docs/Web/HTML/Reference/Elements/input#type) of `number`. This control looks like a text field but allows only floating-point numbers, and usually provides buttons in the form of a spinner to increase and decrease the value. On devices with dynamic keyboards, the numeric keyboard is generally displayed.

With the `number` input type, you can constrain the minimum and maximum values allowed by setting the [`min`](/en-US/docs/Web/HTML/Reference/Elements/input#min) and [`max`](/en-US/docs/Web/HTML/Reference/Elements/input#max) attributes. You can also use the `step` attribute to set the increment of the spinner buttons:

```html
<input type="number" name="age" id="age" min="1" max="10" step="2" />
```

By default, `step` is `1`, so only integers are valid. To allow decimal numbers, set `step="any"` or a fractional value such as `step="0.01"`.

## Slider controls

Another way to pick a number is to use a **slider**. You see these quite often on sites like house-buying sites where you want to set a maximum property price to filter by:

```html
<label for="price">Choose a maximum house price: </label>
<input
  type="range"
  name="price"
  id="price"
  min="50000"
  max="500000"
  step="1000"
  value="250000" />
<output class="price-output" for="price"></output>
```

One problem with sliders is that they don't offer any kind of visual feedback as to what the current value is. This is why we've included an {{htmlelement("output")}} element to contain the current value, which you can update with JavaScript whenever the slider's [`input`](/en-US/docs/Web/API/Element/input_event) event fires:

```js
const price = document.querySelector("#price");
const output = document.querySelector(".price-output");

output.textContent = price.value;

price.addEventListener("input", () => {
  output.textContent = price.value;
});
```

Sliders are best used when the exact value is less important than an approximate one, because precise selection can be hard.

## Date and time pickers

Gathering date and time values has traditionally been a nightmare for web developers. For good user experience, it is important to provide a calendar selection UI, enabling users to select dates without needing to switch context to a native calendar application. HTML provides several types for this:

- [`date`](/en-US/docs/Web/HTML/Reference/Elements/input/date) — a year, month, and day, with no time.
- [`time`](/en-US/docs/Web/HTML/Reference/Elements/input/time) — a time of day, with no date.
- [`datetime-local`](/en-US/docs/Web/HTML/Reference/Elements/input/datetime-local) — a date and time, with no time zone information.
- [`month`](/en-US/docs/Web/HTML/Reference/Elements/input/month) — a year and month.
- [`week`](/en-US/docs/Web/HTML/Reference/Elements/input/week) — a year and a week number.

```html
<input type="date" name="date" id="date" min="2025-01-01" max="2025-12-31" />
```

All date and time controls can be constrained using the `min` and `max` attributes. The value is always submitted in a standard format (for example, `2025-06-15` for a date), regardless of how the browser displays it to the user.

> [!WARNING]
> Support for `month` and `week` is still incomplete in some browsers. Where a type isn't supported, the control falls back to a plain `text` input, so make sure your form still makes sense in that case.

## Color picker control

Colors are always a bit difficult to handle. There are many ways to express them: RGB values (decimal or hexadecimal), HSL values, keywords, and so on. A `color` control can be created using the {{HTMLElement("input")}} element with its [`type`](/en-US/docs/Web/HTML/Reference/Elements/input#type) attribute set to `color`:

```html
<input type="color" name="color" id="color" />
```

When supported, clicking a color control shows the operating system's default color-picking functionality. The value returned is always a lowercase 6-digit hexadecimal color, such as `#ff8800`.

## Test your skills!

You've reached the end of this article, but can you remember the most important information? You can find some further tests to verify that you've retained this information before you move on — see [Test your skills: HTML5 controls](/en-US/docs/Learn_web_development/Extensions/Forms/Test_your_skills/HTML5_controls).

## Summary

That brings us to the end of our tour of the HTML5 form input types. There are a few other control types that cannot be easily grouped together due to their very specific behaviors, but which are still essential to know about. We cover those in the next article.

{{PreviousMenuNext("Learn_web_development/Extensions/Forms/Basic_native_form_controls", "Learn_web_development/Extensions/Forms/Other_form_controls", "Learn_web_development/Extensions/Forms")}}
```
