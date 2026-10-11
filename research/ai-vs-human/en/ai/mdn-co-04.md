# UI pseudo-classes

**UI pseudo-classes** are CSS [pseudo-classes](https://developer.mozilla.org/en-US/docs/Web/CSS/Pseudo-classes) that select elements based on their user interface state. That state can come from user interaction, from form validation, or from the element's attributes. For example, `:checked` matches a checkbox that is ticked, and `:invalid` matches a form field whose value fails its constraints. Because these selectors respond to state, you can style controls without adding JavaScript or extra class names.

## Syntax

```css
element:pseudo-class {
  /* declarations */
}
```

A pseudo-class is written after a selector, with no spaces. It matches only when the element is in the stated state.

## Description

UI pseudo-classes fall into a few groups:

- **Availability:** `:enabled` and `:disabled` match form controls that can or cannot receive input.
- **Selection and defaults:** `:checked`, `:indeterminate`, and `:default` describe the current or initial selection state of checkboxes, radio buttons, and options.
- **Constraint validation:** `:valid`, `:invalid`, `:required`, `:optional`, `:in-range`, and `:out-of-range` reflect the rules set by attributes such as `required`, `min`, `max`, `pattern`, and `type`.
- **Editing permission:** `:read-only` and `:read-write` describe whether the user can edit a field.
- **Input state:** `:placeholder-shown` matches an input that is currently displaying its placeholder, and `:blank` matches an input with no value.
- **Browser-managed state:** `:autofill` matches fields that the browser has filled automatically.
- **Focus and interaction:** `:focus`, `:focus-visible`, `:focus-within`, and `:hover` describe how the user is interacting with an element.

### Validation pseudo-classes

`:valid` and `:invalid` are the most commonly used. They are computed from the element's constraints, so an empty required field is `:invalid` as soon as the page loads, before the user has typed anything. This can show error styling too early. Selectors Level 4 defines `:user-invalid` and `:user-valid` to address this. They match only after the user has interacted with the field. Browser support for these newer selectors varies, so check the compatibility table before relying on them.

A form element is also `:invalid` when any of its descendants is invalid. A form with a required empty field therefore matches `form:invalid`.

### Selection pseudo-classes

`:checked` matches checkboxes and radio buttons that are selected, and `<option>` elements that are selected. `:indeterminate` matches a checkbox whose indeterminate state has been set, which is often used for "select all" controls where only some children are chosen. It also matches a `<progress>` element that has no `value`, and a radio group in which no button is checked.

`:default` matches the control that is selected by default, such as the default submit button in a form or a checkbox that has the `checked` attribute in its markup.

### Focus pseudo-classes

`:focus` matches the element that currently has focus. It applies to mouse clicks as well as keyboard navigation, which can produce outlines that look unexpected after a click. `:focus-visible` matches only when the browser decides that a focus indicator should be shown, which is usually during keyboard navigation. `:focus-within` matches an element that contains a focused descendant, which is useful for highlighting a whole form row or card.

`:hover` matches while a pointer is over an element. It has no equivalent on touch devices, so do not depend on it for information that users need.

## Examples

### Styling required and optional fields

This example adds a marker to required fields and highlights invalid input:

```css
input:required {
  border-left: 4px solid #c00;
}

input:optional {
  border-left: 4px solid transparent;
}

input:invalid {
  border-color: #c00;
  outline-color: #c00;
}

input:valid {
  border-color: #080;
}
```

### Styling disabled controls

```css
button:disabled,
input:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
```

### Styling a checkbox label

Pair `:checked` with the sibling combinator to style the label of a checked box:

```css
input[type="checkbox"] + label {
  color: #333;
}

input[type="checkbox"]:checked + label {
  color: #080;
  text-decoration: line-through;
}
```

### Highlighting a form row

```css
.field:focus-within {
  background-color: #fff8dc;
}
```

Here `.field` is a wrapper around a label and its input. The row is highlighted whenever the input inside it has focus.

### Keyboard-only focus rings

```css
button:focus {
  outline: none;
}

button:focus-visible {
  outline: 3px solid #36f;
  outline-offset: 2px;
}
```

Removing the outline with `:focus` while keeping a visible indicator with `:focus-visible` preserves keyboard accessibility without showing rings after mouse clicks.

## Accessibility considerations

- **Do not rely on color alone.** A red border for `:invalid` helps sighted users, but screen reader users need text messages and the `aria-invalid` attribute. CSS cannot announce a state to assistive technology.
- **Keep focus indicators visible.** Removing outlines entirely makes keyboard navigation difficult. Use `:focus-visible` to limit the indicator to keyboard use, and make sure it has enough contrast.
- **Avoid hiding state behind hover.** Touch users and keyboard users cannot trigger `:hover`, so any information shown only on hover is unavailable to them.
- **Check placeholder contrast.** `:placeholder-shown` makes it easy to style placeholder text, but placeholders are not a replacement for a `<label>`, and their contrast must still meet WCAG guidelines.

## Browser compatibility

Most UI pseudo-classes, including `:checked`, `:disabled`, `:required`, `:valid`, `:invalid`, `:focus`, and `:focus-within`, have been supported in all major browsers for years. `:focus-visible` is also widely supported. `:autofill` was historically available only with the `-webkit-` prefix in some browsers. Newer selectors such as `:user-invalid` and `:blank` have more limited support. Check the compatibility data on MDN before using them without a fallback.

## See also

- [Pseudo-classes](https://developer.mozilla.org/en-US/docs/Web/CSS/Pseudo-classes)
- [Constraint validation](https://developer.mozilla.org/en-US/docs/Web/HTML/Constraint_validation)
- [`:focus-visible`](https://developer.mozilla.org/en-US/docs/Web/CSS/:focus-visible)
- [Forms](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Forms)
