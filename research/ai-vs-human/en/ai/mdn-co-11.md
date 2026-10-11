```markdown
---
title: "Express Tutorial Part 6: Working with forms"
short-title: "6: Working with forms"
slug: Learn_web_development/Extensions/Server-side/Express_Nodejs/forms
page-type: learn-module-chapter
sidebar: learnsidebar
---

{{PreviousMenuNext("Learn_web_development/Extensions/Server-side/Express_Nodejs/Displaying_data", "Learn_web_development/Extensions/Server-side/Express_Nodejs/deployment", "Learn_web_development/Extensions/Server-side/Express_Nodejs")}}

In this tutorial we'll show you how to work with HTML forms in Express using Pug. In particular, we'll discuss how to write forms to create, update, and delete documents from the site's database.

<table>
  <tbody>
    <tr>
      <th scope="row">Prerequisites:</th>
      <td>
        Complete all previous tutorial topics, including
        <a href="/en-US/docs/Learn_web_development/Extensions/Server-side/Express_Nodejs/Displaying_data">Express Tutorial Part 5: Displaying library data</a>.
      </td>
    </tr>
    <tr>
      <th scope="row">Objective:</th>
      <td>
        To understand how to write forms to get data from users, and update the database with this data.
      </td>
    </tr>
  </tbody>
</table>

## Overview

An [HTML Form](/en-US/docs/Learn_web_development/Extensions/Forms) is a group of one or more fields/widgets on a web page that can be used to collect information from users for submission to a server. Forms are a flexible mechanism for collecting user input because there are suitable form inputs available for entering many different types of data: text boxes, checkboxes, radio buttons, date pickers, and so on. Forms are also a relatively secure way of sharing data with the server, as they allow us to send data in `POST` requests with cross-site request forgery protection.

Working with forms can be complicated! Developers need to write HTML for the form, validate and properly sanitize entered data on the server (and possibly also in the browser), repost the form with error messages to inform users of any invalid fields, handle the data when it has successfully been submitted, and finally respond to the user in some way to indicate success.

In this tutorial, we're going to show you how the above operations may be performed in _Express_. Along the way, we'll extend the _LocalLibrary_ website to allow users to create, edit and delete items from the library.

> [!NOTE]
> We haven't looked at how to restrict particular routes to authenticated or authorized users, so at this point, any user will be able to make changes to the database.

### HTML Forms

First a brief overview of [HTML Forms](/en-US/docs/Learn_web_development/Extensions/Forms). Consider a simple HTML form, with a single text field for entering the name of some "team", and its associated label:

```html
<form action="/team_name_url/" method="post">
  <label for="team_name">Enter name: </label>
  <input
    id="team_name"
    type="text"
    name="name_field"
    value="Default name for team." />
  <input type="submit" value="OK" />
</form>
```

The form is defined in HTML as a collection of elements inside `<form>…</form>` tags, containing at least one `input` element of `type="submit"`.

- The `type` attribute of the input defines what sort of widget will be displayed.
- The `name` and `id` of the field are used to identify the field in JavaScript/CSS/HTML, while `value` defines the initial value for the field when it is first displayed.
- The `submit` input will be displayed as a button by default. Pressing it uploads the data in the other input elements to the server.

The `action` attribute defines the URL to which data is sent when the form is submitted, and the `method` attribute defines the HTTP method used. The **HTTP `POST`** method should always be used if the data is going to result in a change to the server's database, because this can be made more resistant to cross-site forgery request attacks.

### Form handling process

Form handling uses all of the same techniques that we learned for displaying information about our models: the route sends our request to a controller function, which performs any database actions required, including reading data from the models, then generates and returns an HTML page. What makes things more complicated is that the server also needs to process the data provided by the user, and redisplay the form with error information if there are any problems.

The main things the form handling code needs to do are:

1. Display the default form the first time it is requested by the user.
2. Receive data submitted by the user, usually in an HTTP `POST` request.
3. Validate and sanitize the data.
4. If any data is invalid, re-display the form — this time with any user populated values and error messages for the problem fields.
5. If all data is valid, perform required actions (for example, save the data in the database).
6. Once all actions are complete, redirect the user to another page.

Often form handling code is implemented using a `GET` route for the initial display of the form and a `POST` route to the same path for handling validation and processing of form data. This is the approach that will be used in this tutorial.

Express itself doesn't provide any specific support for form handling operations, but it can use middleware to process `POST` and `GET` parameters from the form, and to validate/sanitize their values.

### Validation and sanitization

Before the data from a form is stored it must be validated and sanitized:

- Validation checks that entered values are appropriate for each field (are in the right range, format, and so on) and that values have been supplied for all required fields.
- Sanitization removes or replaces characters in the data that might potentially be used to send malicious content to the server.

For this tutorial, we'll be using the popular [express-validator](https://www.npmjs.com/package/express-validator) module to perform both validation and sanitization of our form data. Install it by running the following command in the root of the project:

```bash
npm install express-validator
```

To use the validator in our controllers, we specify the particular functions we want to import from the module:

```js
const { body, validationResult } = require("express-validator");
```

The [`body()`](https://express-validator.github.io/docs/api/check#body) function creates a validation chain for a named field in the request body. Validators and sanitizers can be daisy-chained:

```js
[
  body("name", "Genre name must contain at least 3 characters")
    .trim()
    .isLength({ min: 3 })
    .escape(),
];
```

- `trim()` removes leading and trailing whitespace.
- `isLength()` checks that the resulting string is at least three characters long.
- `escape()` replaces HTML characters that might be used in JavaScript cross-site scripting attacks.

The [`validationResult(req)`](https://express-validator.github.io/docs/api/validation-result/) function runs the validation, making errors available in the form of a `Result` object:

```js
asyncHandler(async (req, res, next) => {
  const errors = validationResult(req);

  if (!errors.isEmpty()) {
    // There are errors. Render form again with sanitized values and error messages.
  } else {
    // Data from form is valid.
  }
});
```

We use the `isEmpty()` method to check if there were errors, and its `array()` method to get the set of error messages.

## Routes

In order to implement our form handling code, we will need two routes that have the same URL pattern. The first (`GET`) route is used to display a new empty form for creating the object. The second route (`POST`) is used for validating data entered by the user, and then saving the information and redirecting to the detail page (if the data is valid) or redisplaying the form with errors (if the data is invalid).

We have already created the routes for all our model's create pages in **/routes/catalog.js**. For example, the genre routes are shown below:

```js
// GET request for creating a Genre. NOTE This must come before route that displays Genre (uses id).
router.get("/genre/create", genre_controller.genre_create_get);

// POST request for creating Genre.
router.post("/genre/create", genre_controller.genre_create_post);
```

## Express forms subarticles

The following subarticles will take us through the process of adding the required forms to our example application. You need to read and work through each one in turn, before moving on to the next one.

1. [Create Genre form](/en-US/docs/Learn_web_development/Extensions/Server-side/Express_Nodejs/forms/Create_genre_form) — defining a page to create `Genre` objects.
2. [Create Author form](/en-US/docs/Learn_web_development/Extensions/Server-side/Express_Nodejs/forms/Create_author_form) — defining a page to create `Author` objects.
3. [Create Book form](/en-US/docs/Learn_web_development/Extensions/Server-side/Express_Nodejs/forms/Create_book_form) — defining a page/form to create `Book` objects.
4. [Create BookInstance form](/en-US/docs/Learn_web_development/Extensions/Server-side/Express_Nodejs/forms/Create_BookInstance_form) — defining a page/form to create `BookInstance` objects.
5. [Delete Author form](/en-US/docs/Learn_web_development/Extensions/Server-side/Express_Nodejs/forms/Delete_author_form) — defining a page to delete `Author` objects.
6. [Update Book form](/en-US/docs/Learn_web_development/Extensions/Server-side/Express_Nodejs/forms/Update_Book_form) — defining a page to update `Book` objects.

## Challenge yourself

Implement the delete pages for the `Book`, `BookInstance`, and `Genre` models, linking them from the associated detail pages in the same way as our _Author delete_ page. The pages should follow the same design approach:

- If there are references to the object from other objects, then these other objects should be displayed along with a note that this record can't be deleted until the listed objects have been deleted.
- If there are no other references to the object then the view should prompt to delete it. If the user presses the **Delete** button, the record should then be deleted.

Then implement the update pages for the `Author`, `BookInstance`, and `Genre` models, linking them from the associated detail pages in the same way as our _Book update_ page.

## Summary

_Express_, node, and third-party packages on npm provide everything you need to add forms to your website. In this article, you've learned how to create forms using _Pug_, validate and sanitize input using _express-validator_, and add, delete, and modify records in the database.

You should now understand how to add basic forms and form-handling code to your own node websites!

## See also

- [express-validator](https://www.npmjs.com/package/express-validator) (npm docs).

{{PreviousMenuNext("Learn_web_development/Extensions/Server-side/Express_Nodejs/Displaying_data", "Learn_web_development/Extensions/Server-side/Express_Nodejs/deployment", "Learn_web_development/Extensions/Server-side/Express_Nodejs")}}
```

The page body is about 900 words. It uses MDN's front matter, the `{{PreviousMenuNext}}` navigation macro and the `> [!NOTE]` callout format.

The code examples continue the existing LocalLibrary project from the series. That includes the `asyncHandler` wrapper and the genre routes in **/routes/catalog.js**. The links to other pages and to the express-validator docs are written in MDN's usual style, but I haven't checked that they work, so please test them before you publish.
