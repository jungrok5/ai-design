---
title: Making decisions in your code — conditionals
slug: Learn/JavaScript/Building_blocks/conditionals
---

In any programming language, code needs to make decisions and carry out actions accordingly, depending on different inputs. For example, in a game, if the player's number of lives reaches 0, the game is over. In a weather app, if it is being looked at in the morning, it shows a sunrise graphic; if it is nighttime, it shows stars and a moon. In this article, we'll explore how so-called conditional statements work in JavaScript.

| | |
|---|---|
| **Prerequisites** | Basic computer literacy, a basic understanding of HTML and CSS, and familiarity with JavaScript basics. |
| **Learning outcomes** | Understand how to use conditional structures in JavaScript. |

## You can have it on one condition..!

Human beings (and other animals) make decisions all the time that affect their lives, from small ("should I eat one cookie or two?") to large ("should I stay in my home country and work on my father's farm, or move to America and study astrophysics?").

Conditional statements allow us to represent such decision-making in JavaScript, from the choice that must be made (for example, "one cookie or two") to the resulting outcome of those choices (perhaps the outcome of "ate one cookie" might be "still felt hungry", and the outcome of "ate two cookies" might be "felt full, but mom scolded me for eating all the cookies").

## if...else statements

Let's look at by far the most common type of conditional statement you'll use in JavaScript: the humble [`if...else` statement](/en-US/docs/Web/JavaScript/Reference/Statements/if...else).

### Basic if...else syntax

The basic syntax looks like this in {{glossary("pseudocode")}}:

```js-nolint
if (condition) {
  code to run if condition is true
} else {
  run some other code instead
}
```

Here we've got:

1. The keyword `if` followed by some parentheses.
2. A condition to test, placed inside the parentheses (typically "is this value bigger than this other value?" or "does this value exist?"). The condition makes use of the [comparison operators](#comparison-operators) we discussed in the last module and returns `true` or `false`.
3. A set of curly braces, inside which we have some code. This can be any code we like, and it only runs if the condition returns `true`.
4. The keyword `else`.
5. Another set of curly braces, inside which we have some more code. This code only runs if the condition is `false`.

This code is pretty human-readable. It says "**if** the **condition** returns `true`, run code A, **else** run code B".

You should note that you don't have to include the `else` and the second curly brace block. The following is also perfectly legal code:

```js-nolint
if (condition) {
  code to run if condition is true
}

run some other code
```

However, you need to be careful here: in this case, the second block of code is not controlled by the conditional statement, so it **always** runs, regardless of whether the condition returns `true` or `false`. This is not necessarily a bad thing, but it might not be what you want.

### A real example

To understand this syntax better, let's consider a real example. Imagine a child being asked for help with a chore by their mother or father. The parent might say, "Hey sweetheart, if you help me by going and doing the shopping, I'll give you some extra allowance so you can afford that toy you wanted."

In JavaScript, we could represent this like so:

```js
let shoppingDone = false;
let childsAllowance;

if (shoppingDone === true) {
  childsAllowance = 10;
} else {
  childsAllowance = 5;
}
```

This code as shown always results in the `shoppingDone` variable returning `false`, meaning disappointment for our poor child. It'd be up to us to provide a mechanism for the parent to set the `shoppingDone` variable to `true` if the child did the shopping.

> [!NOTE]
> You can see a more complete version of this example on GitHub.

## else if

The last example provided us with two choices, or outcomes, but what if we want more than two?

There is a way to chain extra choices onto your `if...else` — using `else if`. Each extra choice requires an additional block to put in between `if () { }` and `else { }`.

```js
let weather = "rainy";

if (weather === "sunny") {
  console.log("Wear shorts and a t-shirt.");
} else if (weather === "rainy") {
  console.log("Take a raincoat and an umbrella.");
} else if (weather === "snowing") {
  console.log("Wrap up warm and wear boots.");
} else {
  console.log("Check the forecast again.");
}
```

Here the code checks each condition in turn, from top to bottom. As soon as one condition is `true`, its block runs and the remaining checks are skipped. The final `else` block acts as a safety net, running only when nothing else matched.

> [!NOTE]
> It is good practice to include a final `else` block, even if it only logs a message. It makes unexpected input far easier to notice and debug.

## A note on comparison operators

Conditions are built using comparison operators:

- `===` and `!==` test whether one value is strictly equal to, or not equal to, another.
- `<` and `>` test whether one value is less than or greater than another.
- `<=` and `>=` test whether one value is less than or equal to, or greater than or equal to, another.

> [!NOTE]
> Prefer `===` over `==`. The loose equality operator converts types before comparing, so `"5" == 5` is `true`, which often leads to surprising bugs.

## Nesting if...else

It is perfectly OK to put one `if...else` statement inside another one — to nest them. For example, we could update our weather app to show a further set of choices depending on what the temperature is:

```js
if (weather === "sunny") {
  if (temperature < 86) {
    console.log(`It is ${temperature} degrees — nice and sunny.`);
  } else {
    console.log(`It is ${temperature} degrees — hot! Seek shade.`);
  }
}
```

Even though all the code works together, each `if...else` statement works completely independently of the other one. Deeply nested code quickly becomes hard to read, so consider whether logical operators could simplify it.

## Logical operators: AND, OR and NOT

If you want to test multiple conditions without writing nested `if...else` statements, logical operators can help you:

- `&&` — AND; allows you to chain together two or more expressions so that all of them have to individually evaluate to `true` for the whole expression to return `true`.
- `||` — OR; allows you to chain together two or more expressions so that one or more of them have to individually evaluate to `true` for the whole expression to return `true`.
- `!` — NOT; can be used to negate an expression.

```js
if (choice === "sunny" && temperature >= 86) {
  console.log("Hot and sunny — head to the beach!");
}

if (day === "Saturday" || day === "Sunday") {
  console.log("It's the weekend.");
}
```

## switch statements

`if...else` statements do the job of enabling conditional code well, but they are not without their downsides. They are mainly good for cases where you've got a couple of choices, and each one requires a reasonable amount of code to be run. When you have many options of a single value, they can become unwieldy.

In such cases, a [`switch` statement](/en-US/docs/Web/JavaScript/Reference/Statements/switch) is your friend:

```js-nolint
switch (expression) {
  case choice1:
    run this code
    break;

  case choice2:
    run this code instead
    break;

  default:
    actually, just run this code
}
```

The `break` statement ends the `switch`. Without it, execution "falls through" and runs the code of the following cases too.

```js
const day = "Tuesday";

switch (day) {
  case "Saturday":
  case "Sunday":
    console.log("Enjoy the weekend!");
    break;
  default:
    console.log("Back to work.");
}
```

## Ternary operator

There is one final bit of syntax we want to introduce before you get your hands dirty. The [ternary or conditional operator](/en-US/docs/Web/JavaScript/Reference/Operators/Conditional_operator) tests a condition and returns one value if it is `true` and another if it is `false`:

```js-nolint
condition ? run this code : run this code instead
```

```js
const greeting = isBirthday
  ? "Happy birthday!"
  : "Good morning!";
```

This is useful for simple choices, but avoid chaining several ternaries together, as the result is difficult to read.

## Test your skills!

You've reached the end of this article, but can you remember the most important information? Try rewriting the weather example using a `switch` statement, then rewrite the birthday greeting as a full `if...else`. Compare the two versions: which is easier to read, and why?

## Summary

This article covered the conditional structures you'll use most often in JavaScript: `if...else`, `else if`, nesting, logical operators, `switch`, and the ternary operator. Choose the simplest structure that clearly expresses your intent, and your code will be easier to read and maintain.

## See also

- [Comparison operators](/en-US/docs/Learn/JavaScript/First_steps/Math#comparison_operators)
- [Control flow and error handling](/en-US/docs/Web/JavaScript/Guide/Control_flow_and_error_handling)
- [`if...else` reference](/en-US/docs/Web/JavaScript/Reference/Statements/if...else)
- [`switch` reference](/en-US/docs/Web/JavaScript/Reference/Statements/switch)
