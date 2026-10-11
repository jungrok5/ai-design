```md
---
title: Your first form
slug: Learn_web_development/Core/Structuring_content/Your_first_form
page-type: learn-module-chapter
sidebar: learnsidebar
---

{{PreviousMenuNext("Learn_web_development/Core/Structuring_content/Basic_HTML_syntax", "Learn_web_development/Core/Structuring_content/Forms_overview", "Learn_web_development/Core/Structuring_content")}}

The first article in our series gives you a first experience of creating a web form, including designing a simple form, implementing it using the right HTML form controls and other HTML elements, adding some very simple styling via CSS, and describing how data is sent to a server. We'll expand on each of these subtopics in more detail later in the module.

<table>
  <tbody>
    <tr>
      <th scope="row">Prerequisites:</th>
      <td>
        A basic understanding of
        <a href="/en-US/docs/Learn_web_development/Core/Structuring_content/Basic_HTML_syntax">HTML syntax</a>
        and how to use a text editor.
      </td>
    </tr>
    <tr>
      <th scope="row">Learning outcomes:</th>
      <td>
        <ul>
          <li>What a web form is and what it is used for.</li>
          <li>How to build a simple form with labels, text inputs and a submit button.</li>
          <li>How form data travels from the browser to a server.</li>
        </ul>
      </td>
    </tr>
  </tbody>
</table>

## What are web forms?

Web forms are one of the main points of interaction between a user and a website or application. They allow users to enter data, which is generally sent to a web server for processing and storage, or used on the client side to immediately update the interface in some way. For example, a form might let you sign in, search a catalog, post a comment, or check out of an online store.

A web form consists of one or more **form controls** (sometimes called **widgets**), plus some additional elements to help structure the overall form. The controls can be single or multi-line text fields, dropdown boxes, buttons, checkboxes, or radio buttons, and are mostly created using the {{htmlelement("input")}} element, although there are some other elements to learn about too.

Form controls can also be programmed to enforce specific formats or values to be entered ({{glossary("Form validation", "form validation")}}), and are paired with text labels that describe their purpose to both sighted and visually impaired users.

## Designing your form

Before you start coding, it's always better to step back and take the time to think about your form. Designing a quick mockup will help you to define the right set of data you want to ask your user to enter. From a user experience (UX) point of view, it's important to remember that the bigger your form, the more you risk frustrating people and losing users. Keep it simple and stay focused: ask only for the data you absolutely need.

In this article, we'll build a simple contact form. Let's make a rough sketch.

Our form will contain three text fields and one button. We are asking the user for their name, their email address and the message they want to send. Hitting the button will send their data to a web server.

## Active learning: Implementing our form HTML

Okay, let's have a go at building the HTML for our form. We will use the following HTML elements: {{htmlelement("form")}}, {{htmlelement("label")}}, {{htmlelement("input")}}, {{htmlelement("textarea")}}, and {{htmlelement("button")}}.

### The `<form>` element

All forms start with a {{htmlelement("form")}} element, like this:

```html
<form action="/my-handling-form-page" method="post">
  …
</form>
```

This element formally defines a form. It's a container element like a {{htmlelement("section")}} or {{htmlelement("footer")}} element, but specifically for containing forms; it also supports some specific attributes to configure the way the form behaves. All of its attributes are optional, but it's standard practice to always set at least the `action` and `method` attributes:

- The `action` attribute defines the location (URL) where the form's collected data should be sent when it is submitted.
- The `method` attribute defines which HTTP method to send the data with (usually `get` or `post`).

> [!NOTE]
> We'll look at how those attributes work in the [Sending form data](#sending-form-data) section later on.

### The `<label>`, `<input>`, and `<textarea>` elements

Our contact form is not complex. The data entry portion contains three text fields, each with a corresponding {{htmlelement("label")}}:

- The input field for the name is a basic single-line text field.
- The input field for the email is an input of type email: a single-line text field that accepts only email addresses.
- The input field for the message is a {{htmlelement("textarea")}}: a multiline text field.

In terms of HTML code, we need something like the following to implement these form widgets:

```html
<form action="/my-handling-form-page" method="post">
  <ul>
    <li>
      <label for="name">Name:</label>
      <input type="text" id="name" name="user_name" />
    </li>
    <li>
      <label for="mail">Email:</label>
      <input type="email" id="mail" name="user_email" />
    </li>
    <li>
      <label for="msg">Message:</label>
      <textarea id="msg" name="user_message"></textarea>
    </li>
  </ul>
</form>
```

The list items are there to structure our code conveniently and make styling easier, but they aren't required. Pay attention to the use of the `for` attribute on all {{htmlelement("label")}} elements; it is a special attribute that binds a label to a form control by referencing the control's `id`. This has some benefits: a user can click the label to activate the matching control, and assistive technology such as screen readers announces the label when the control receives focus.

On the {{htmlelement("input")}} elements, the most important attribute is `type`. It defines the way the element appears and behaves. We'll cover this in detail in a later article. Also note the `name` attribute, which holds the name of the data item. When the form is sent, the name is sent along with the value the user entered.

### The `<button>` element

The markup for our form is almost complete; we just need to add a button to allow the user to send, or "submit", their data once they have filled out the form. This is done by using the {{htmlelement("button")}} element; add the following just above the closing `</form>` tag:

```html
<li class="button">
  <button type="submit">Send your message</button>
</li>
```

The {{htmlelement("button")}} element also accepts a `type` attribute, which accepts one of three values: `submit`, `reset`, or `button`.

- A click on a `submit` button (the default value) sends the form's data to the web page defined by the `action` attribute of the {{htmlelement("form")}} element.
- A click on a `reset` button resets all the form widgets to their default value immediately. From a UX point of view, this is considered bad practice, so you should avoid using this type of button unless you really have a good reason to include one.
- A click on a `button` button does _nothing_ by default. That sounds silly, but it's amazingly useful for building custom buttons: you can define their chosen functionality with JavaScript.

## Basic styling for our form

Now that you have finished writing the HTML code of the form, try saving it and looking at it in a browser. At the moment, you'll see that it looks rather ugly.

Forms are notoriously tricky to style, but a little CSS goes a long way. Add the following inside a {{htmlelement("style")}} element in your page's {{htmlelement("head")}}:

```css
ul {
  list-style: none;
  padding: 0;
  margin: 0;
  max-width: 400px;
}

li + li {
  margin-top: 1rem;
}

label {
  display: inline-block;
  width: 90px;
  text-align: right;
}

input,
textarea {
  font: 1em sans-serif;
  width: 300px;
  box-sizing: border-box;
  border: 1px solid #999;
}

input:focus,
textarea:focus {
  border-color: #000;
}

textarea {
  vertical-align: top;
  height: 5em;
}

.button {
  padding-left: 90px;
}
```

Our form looks a lot less ugly now. You can see that the labels line up with their controls, the fields share a consistent width and font, and the focused control is highlighted.

## Sending form data

The last part, and perhaps the trickiest, is to handle form data on the server side. The {{htmlelement("form")}} element defines where and how to send the data thanks to the `action` and `method` attributes.

We provide a `name` attribute for each form control. The names are important on both the client and server side; they tell the browser which name to give each piece of data and, on the server side, they let the server handle each piece of data by name. The form data is sent to the server as name/value pairs.

To name the data in a form, you need to use the `name` attribute on each form widget that will collect a specific piece of data. Let's look at some of our form code again:

```html
<form action="/my-handling-form-page" method="post">
  <ul>
    <li>
      <label for="name">Name:</label>
      <input type="text" id="name" name="user_name" />
    </li>
    <li>
      <label for="mail">Email:</label>
      <input type="email" id="mail" name="user_email" />
    </li>
    <li>
      <label for="msg">Message:</label>
      <textarea id="msg" name="user_message"></textarea>
    </li>
    …
  </ul>
</form>
```

In our example, the form will send three pieces of data named `user_name`, `user_email`, and `user_message`. That data will be sent to the URL `/my-handling-form-page` using the HTTP [`POST`](/en-US/docs/Web/HTTP/Reference/Methods/POST) method.

On the server side, the script at the URL `/my-handling-form-page` receives the data as a list of three key/value items contained in the HTTP request. The way this script will handle that data is up to you. Each server-side language (PHP, Python, Ruby, Java, C#, and so on) has its own mechanism for handling form data. It's beyond the scope of this guide to go deeper into that subject, but if you want to know more, we have provided some examples in our later article [Sending form data](/en-US/docs/Learn_web_development/Extensions/Forms/Sending_and_retrieving_form_data).

## Test your skills!

You've reached the end of this article, but can you remember the most important information? Try to rewrite the contact form from memory, then compare your version against the code above. Pay particular attention to the `for`/`id` pairing on labels and inputs, and to the `name` attributes.

## Summary

You now have a working contact form: HTML to structure it, a little CSS to make it readable, and an understanding of how its data reaches a server. The following articles go much deeper into each of the pieces introduced here.

## See also

- {{htmlelement("form")}}
- {{htmlelement("input")}}
- {{htmlelement("label")}}
- {{htmlelement("button")}}
- [HTML forms guide](/en-US/docs/Learn_web_development/Extensions/Forms)

{{PreviousMenuNext("Learn_web_development/Core/Structuring_content/Basic_HTML_syntax", "Learn_web_development/Core/Structuring_content/Forms_overview", "Learn_web_development/Core/Structuring_content")}}
```
