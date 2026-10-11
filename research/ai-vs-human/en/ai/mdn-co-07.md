# Test your skills: Values and units

This page tests what you learned about CSS values and units. Answer each question before you check the solution at the end. If you get stuck, go back to the earlier lessons and try again.

## Question 1: Valid declarations

Which of the following declarations is valid?

- `margin: 1 em;`
- `width: 50px;`
- `font-size: 16 px;`
- `padding: 10PX;`

## Question 2: Relative font sizes

The root element has `font-size: 16px`. A `<p>` inside a `<div>` with `font-size: 20px` contains a `<span>` with `font-size: 1.5em`. What is the computed font size of the `<span>`?

## Question 3: Rem and em

Consider this rule:

```css
h2 {
  font-size: 2rem;
}
```

If the `<h2>` is nested inside a parent with `font-size: 10px`, what is the computed font size of the `<h2>`? Explain your answer.

## Question 4: Percentages

A `<div>` has `width: 50%` and sits inside a container that is 800px wide. What is the width of the `<div>` in pixels? Which property would a percentage `font-size` be relative to?

## Question 5: Mixed units

Write a declaration that makes an element's width equal to the full width of its container, minus 2rem.

## Solutions

**Question 1:** Only `width: 50px;` is valid. `margin: 1 em;` is invalid because a number and unit must not be separated by a space. `font-size: 16 px;` is invalid for the same reason. Units are case-insensitive, so `10PX` is valid, and `padding: 10PX;` is also correct.

**Question 2:** The `<span>` computes to 30px. Its `em` value is relative to its parent's font size, which is 20px, so 1.5 × 20px = 30px.

**Question 3:** The `<h2>` computes to 32px. `rem` is relative to the root font size, not the parent, so the nested parent does not affect the result.

**Question 4:** The `<div>` is 400px wide, because 50% of 800px is 400px. A percentage `font-size` is relative to the parent element's font size.

**Question 5:** `width: calc(100% - 2rem);`
