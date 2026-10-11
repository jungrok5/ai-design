```markdown
---
title: Object building practice
slug: Learn_web_development/Extensions/Advanced_JavaScript_objects/Object_building_practice
page-type: learn-module-chapter
sidebar: learnsidebar
---

{{PreviousMenuNext("Learn_web_development/Extensions/Advanced_JavaScript_objects/Classes_in_JavaScript", "Learn_web_development/Extensions/Advanced_JavaScript_objects/Adding_bouncing_balls_features", "Learn_web_development/Extensions/Advanced_JavaScript_objects")}}

In previous articles we looked at the theory and syntax of JavaScript objects, which gives you a solid place to start. In this article we'll do a practical exercise: you'll build your own JavaScript objects and use them to make something fun and colorful.

<table>
  <tbody>
    <tr>
      <th scope="row">Prerequisites:</th>
      <td>
        Familiarity with the basics of
        <a href="/en-US/docs/Learn_web_development/Core/Structuring_content">HTML</a>,
        <a href="/en-US/docs/Learn_web_development/Core/Styling_basics">CSS</a>, and
        <a href="/en-US/docs/Learn_web_development/Core/Scripting">JavaScript</a>,
        including <a href="/en-US/docs/Learn_web_development/Core/Scripting/Object_basics">object basics</a>
        and <a href="/en-US/docs/Learn_web_development/Extensions/Advanced_JavaScript_objects/Classes_in_JavaScript">classes</a>.
      </td>
    </tr>
    <tr>
      <th scope="row">Learning outcomes:</th>
      <td>
        <ul>
          <li>Practice using objects and object-oriented techniques in a real-world context.</li>
          <li>Use the Canvas API to draw shapes.</li>
          <li>Build a basic animation loop.</li>
        </ul>
      </td>
    </tr>
  </tbody>
</table>

## Let's bounce some balls

In this article we will write a classic "bouncing balls" demo, to show you how useful objects can be in JavaScript. Our little balls will bounce around on the screen, and change color when they touch each other. The finished example will look a little something like this:

![Screenshot of a webpage titled "Bouncing balls". 23 balls of various pastel colors and sizes are visible across a black screen with long trails behind them indicating motion.](bouncing-balls.png)

This example will make use of the [Canvas API](/en-US/docs/Learn_web_development/Extensions/Client-side_APIs/Drawing_graphics) for drawing the balls to the screen, and the {{domxref("Window.requestAnimationFrame", "requestAnimationFrame")}} API for animating the whole display. You don't need to have any previous knowledge of these APIs, and we hope that by the time you've finished this article you'll be interested in exploring them more. Along the way, we'll make use of some nifty objects, and show you a couple of nice techniques like bouncing balls off walls, and checking whether they have hit each other (otherwise known as _collision detection_).

## Getting started

To begin with, make local copies of our [`index.html`](https://github.com/mdn/learning-area/blob/main/javascript/oojs/bouncing-balls/index.html), [`style.css`](https://github.com/mdn/learning-area/blob/main/javascript/oojs/bouncing-balls/style.css), and [`main.js`](https://github.com/mdn/learning-area/blob/main/javascript/oojs/bouncing-balls/main.js) files. These contain the following, respectively:

1. A very simple HTML document featuring an {{htmlelement("Heading_Elements", "h1")}} element, a {{htmlelement("canvas")}} element to draw our balls on, and elements to apply our CSS and JavaScript to our HTML.
2. Some very simple styles, which mainly serve to style and position the `<h1>`, and get rid of any scrollbars or margin around the edge of the page (so that it looks nice and neat).
3. Some JavaScript that serves to set up the `<canvas>` element and provide a general function that we're going to use.

The first part of the script looks like this:

```js
const canvas = document.querySelector("canvas");
const ctx = canvas.getContext("2d");

const width = (canvas.width = window.innerWidth);
const height = (canvas.height = window.innerHeight);
```

This script gets a reference to the `<canvas>` element, then calls the {{domxref("HTMLCanvasElement.getContext()", "getContext()")}} method on it to give us a context on which we can start to draw. The resulting constant (`ctx`) is the object that directly represents the drawing area of the canvas and allows us to draw 2D shapes on it.

Next, we set constants called `width` and `height`, and the width and height of the canvas element (represented by the `canvas.width` and `canvas.height` properties) to equal the width and height of the browser viewport (the area that the webpage appears on — this can be retrieved from the {{domxref("Window.innerWidth")}} and {{domxref("Window.innerHeight")}} properties).

Note that we are chaining multiple assignments together, to get the variables all set quicker — this is perfectly OK.

Then we have two helper functions:

```js
function random(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function randomRGB() {
  return `rgb(${random(0, 255)} ${random(0, 255)} ${random(0, 255)})`;
}
```

The `random()` function takes two numbers as arguments, and returns a random number in the range between the two. The `randomRGB()` function generates a random color represented as an [`rgb()`](/en-US/docs/Web/CSS/color_value/rgb) string.

## Modeling a ball in our program

Our program will feature lots of balls bouncing around the screen. Since these balls will all behave in the same way, it makes sense to represent them with an object. Let's start by adding the following class definition to the bottom of our code.

```js
class Ball {
  constructor(x, y, velX, velY, color, size) {
    this.x = x;
    this.y = y;
    this.velX = velX;
    this.velY = velY;
    this.color = color;
    this.size = size;
  }
}
```

So far this class only contains a constructor, in which we can initialize the properties each ball needs in order to function in our program:

- `x` and `y` coordinates — the horizontal and vertical coordinates where the ball starts on the screen. This can range between 0 (top left hand corner) to the width and height of the browser viewport (bottom right-hand corner).
- horizontal and vertical velocity (`velX` and `velY`) — each ball is given a horizontal and vertical velocity; in real terms these values are regularly added to the `x`/`y` coordinate values when we animate the balls, to move them by this much on each frame.
- `color` — each ball gets a color.
- `size` — each ball gets a size — this is its radius, in pixels.

This handles the properties, but what about the methods? We want to get our balls to actually do something in our program.

### Drawing the ball

First add the following `draw()` method to the `Ball` class:

```js
draw() {
  ctx.beginPath();
  ctx.fillStyle = this.color;
  ctx.arc(this.x, this.y, this.size, 0, 2 * Math.PI);
  ctx.fill();
}
```

Using this function, we can tell the ball to draw itself onto the screen, by calling a series of members of the 2D canvas context we defined earlier (`ctx`):

- First, we use {{domxref("CanvasRenderingContext2D.beginPath", "beginPath()")}} to state that we want to draw a shape on the paper.
- Next, we use {{domxref("CanvasRenderingContext2D.fillStyle", "fillStyle")}} to define what color we want the shape to be — we set it to our ball's `color` property.
- Next, we use the {{domxref("CanvasRenderingContext2D.arc", "arc()")}} method to trace an arc shape on the paper. Its parameters are the `x` and `y` position of the arc's center, the radius of the arc, and the start and end angles in radians. Here we specify 0 and `2 * PI`, which is the equivalent of 360 degrees — a full circle.
- Last of all, we use the {{domxref("CanvasRenderingContext2D.fill", "fill()")}} method, which basically states "finish drawing the path we started with `beginPath()`, and fill the area it takes up with the color we specified earlier in `fillStyle`."

You can start testing your object out already. Save the code, load the HTML file in a browser, open the browser's [JavaScript console](/en-US/docs/Learn_web_development/Howto/Tools_and_setup/What_are_browser_developer_tools), and then try the following:

```js
const testBall = new Ball(50, 100, 4, 4, "blue", 10);
testBall.draw();
```

You should see a ball drawn on your canvas.

### Updating the ball's data

We can draw the ball in position, but to actually move it, we need an update function of some kind. Add the following code inside the class definition:

```js
update() {
  if (this.x + this.size >= width || this.x - this.size <= 0) {
    this.velX = -this.velX;
  }

  if (this.y + this.size >= height || this.y - this.size <= 0) {
    this.velY = -this.velY;
  }

  this.x += this.velX;
  this.y += this.velY;
}
```

The four checks look at whether the ball has reached the edge of the canvas. If it has, we reverse the polarity of the relevant velocity to make the ball travel in the opposite direction. We include `size` in the calculation because `x` and `y` are at the center of the ball, and we want its edge to bounce off the wall rather than letting it go halfway off the screen. The last two lines add the velocity values to the coordinates, effectively moving the ball each time this method is called.

## Animating the ball

Now let's make this fun. First, we need to create somewhere to store all our balls and then populate it:

```js
const balls = [];

while (balls.length < 25) {
  const size = random(10, 20);
  const ball = new Ball(
    // ball position always drawn at least one ball width
    // away from the edge of the canvas, to avoid drawing errors
    random(0 + size, width - size),
    random(0 + size, height - size),
    random(-7, 7),
    random(-7, 7),
    randomRGB(),
    size,
  );

  balls.push(ball);
}
```

The `while` loop creates a new instance of `Ball` using random values and pushes it onto the end of the array, until there are 25 balls.

Next, add the following to the bottom of your code:

```js
function loop() {
  ctx.fillStyle = "rgb(0 0 0 / 25%)";
  ctx.fillRect(0, 0, width, height);

  for (const ball of balls) {
    ball.draw();
    ball.update();
  }

  requestAnimationFrame(loop);
}

loop();
```

Every animation program generally involves an animation loop like this. Our `loop()` function first covers the whole canvas with a semi-transparent black rectangle, so the previous frame is cleared but faintly visible, creating the little trails behind the balls. It then loops through every ball and draws and updates it. Finally, it calls itself again using {{domxref("Window.requestAnimationFrame", "requestAnimationFrame()")}}, which runs the function a set number of times per second to create a smooth animation.

## Adding collision detection

Now for a bit of fun: let's add collision detection, so the balls know when they have hit another ball. Add the following method to your `Ball` class:

```js
collisionDetect() {
  for (const ball of balls) {
    if (this !== ball) {
      const dx = this.x - ball.x;
      const dy = this.y - ball.y;
      const distance = Math.sqrt(dx * dx + dy * dy);

      if (distance < this.size + ball.size) {
        ball.color = this.color = randomRGB();
      }
    }
  }
}
```

For each ball, we check every other ball to see whether it has collided with the current one. The `this !== ball` test makes sure we don't compare a ball with itself. We then use a common algorithm to check whether two circles overlap — the distance between their centers is less than the sum of their radii. If they collide, both balls get the same new random color. You could do something more complex, such as making the balls bounce off each other realistically, but that would be harder to implement.

Finally, call the method in each frame by updating the loop:

```js
for (const ball of balls) {
  ball.draw();
  ball.update();
  ball.collisionDetect();
}
```

Save and refresh the demo again, and you'll see your balls change color when they collide!

> [!NOTE]
> If you have trouble getting this example to work, try comparing your JavaScript code against our [finished version](https://github.com/mdn/learning-area/blob/main/javascript/oojs/bouncing-balls/main-finished.js) (also [see it running live](https://mdn.github.io/learning-area/javascript/oojs/bouncing-balls/index-finished.html)).

## Summary

We hope you had fun writing your own real-world random bouncing balls example, using various object and object-oriented techniques from throughout the module! This should have given you some useful practice in using objects, and good real-world context.

That's it for object articles — all that remains now is for you to test your skills in the next article.

## See also

- [Canvas tutorial](/en-US/docs/Web/API/Canvas_API/Tutorial) — a beginner's guide to using 2D canvas.
- {{domxref("Window.requestAnimationFrame", "requestAnimationFrame()")}}
- [2D collision detection](/en-US/docs/Games/Techniques/2D_collision_detection)
- [3D collision detection](/en-US/docs/Games/Techniques/3D_collision_detection)
- [2D breakout game using pure JavaScript](/en-US/docs/Games/Tutorials/2D_Breakout_game_pure_JavaScript) — a great beginner's tutorial showing how to build a 2D game.

{{PreviousMenuNext("Learn_web_development/Extensions/Advanced_JavaScript_objects/Classes_in_JavaScript", "Learn_web_development/Extensions/Advanced_JavaScript_objects/Adding_bouncing_balls_features", "Learn_web_development/Extensions/Advanced_JavaScript_objects")}}
```
