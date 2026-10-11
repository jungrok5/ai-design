# Removing Effect Dependencies

When you write an Effect, the linter checks that you've included every reactive value the Effect reads in its dependency list. This keeps your Effect in sync with your component's props and state. Unnecessary dependencies may cause your Effect to run too often, or even create an infinite loop. This page shows you how to review and remove unnecessary dependencies from your Effects.

<YouWillLearn>

* How to fix infinite Effect dependency loops
* What to do when you want to remove a dependency
* How to read a value from your Effect without "reacting" to it
* How and why to avoid object and function dependencies
* Why suppressing the dependency linter is dangerous, and what to do instead

</YouWillLearn>

## Dependencies should match the code {/*dependencies-should-match-the-code*/}

When you write an Effect, you first specify how to start and stop whatever you want your Effect to do:

```js {5-7}
const serverUrl = 'https://localhost:1234';

function ChatRoom({ roomId }) {
  useEffect(() => {
    const connection = createConnection(serverUrl, roomId);
    connection.connect();
    return () => connection.disconnect();
    // ...
```

Then, if you leave the Effect dependencies empty (`[]`), the linter will suggest the correct dependencies:

```js {8}
function ChatRoom({ roomId }) {
  useEffect(() => {
    const connection = createConnection(serverUrl, roomId);
    connection.connect();
    return () => connection.disconnect();
  }, [roomId]); // <-- Fix the mistake here!
  return <h1>Welcome to the {roomId} room!</h1>;
}
```

Fill them in according to what the linter says. Effects "react" to reactive values. Since `roomId` is a reactive value (it can change due to a re-render), the linter verifies that you've specified it as a dependency. If `roomId` receives a different value, React will re-synchronize your Effect. This ensures that the chat stays connected to the selected room and "reacts" to the dropdown.

### To remove a dependency, prove that it's not a dependency {/*to-remove-a-dependency-prove-that-its-not-a-dependency*/}

Notice that you can't "choose" the dependencies of your Effect. Every reactive value used by your Effect's code must be declared in your dependency list. The dependency list is determined by the surrounding code:

```js [[2, 3, "roomId"], [2, 5, "roomId"], [2, 8, "roomId"]]
const serverUrl = 'https://localhost:1234';

function ChatRoom({ roomId }) { // This is a reactive value
  useEffect(() => {
    const connection = createConnection(serverUrl, roomId); // This Effect reads that reactive value
    connection.connect();
    return () => connection.disconnect();
  }, [roomId]); // ✅ So you must specify that reactive value as a dependency of your Effect
  // ...
}
```

[Reactive values](/learn/lifecycle-of-reactive-effects#all-variables-declared-in-the-component-body-are-reactive) include props and all variables and functions declared directly inside of your component. Since `roomId` is a reactive value, you can't remove it from the dependency list. The linter wouldn't allow it:

```js {8}
const serverUrl = 'https://localhost:1234';

function ChatRoom({ roomId }) {
  useEffect(() => {
    const connection = createConnection(serverUrl, roomId);
    connection.connect();
    return () => connection.disconnect();
  }, []); // 🔴 React Hook useEffect has a missing dependency: 'roomId'
  // ...
}
```

And the linter would be right! Since `roomId` may change over time, this would introduce a bug in your code.

**To remove a dependency, "prove" to the linter that it *doesn't need* to be a dependency.** For example, you can move `roomId` out of your component to prove that it's not reactive and won't change on re-renders:

```js {2,9}
const serverUrl = 'https://localhost:1234';
const roomId = 'music'; // Not a reactive value anymore

function ChatRoom() {
  useEffect(() => {
    const connection = createConnection(serverUrl, roomId);
    connection.connect();
    return () => connection.disconnect();
  }, []); // ✅ All dependencies declared
  // ...
}
```

Now that `roomId` is not a reactive value (and can't change on a re-render), it doesn't need to be a dependency. **If your Effect's code doesn't use any reactive values, its dependency list should be empty (`[]`).** An Effect with empty dependencies doesn't re-run when any of your component's props or state change.

### To change the dependencies, change the code {/*to-change-the-dependencies-change-the-code*/}

You might have noticed a pattern in your workflow:

1. First, you **change the code** of your Effect or how your reactive values are declared.
2. Then, you follow the linter and adjust the dependencies to **match the code you have changed.**
3. If you're not happy with the list of dependencies, you **go back to the first step** (and change the code again).

The last part is important. **If you want to change the dependencies, change the surrounding code first.** You can think of the dependency list as [a list of all the reactive values used by your Effect's code.](/learn/lifecycle-of-reactive-effects#react-verifies-that-you-specified-every-reactive-value-as-a-dependency) You don't *choose* what to put on that list. The list *describes* your code. To change the dependency list, change the code.

<Pitfall>

#### Suppressing the linter is dangerous {/*suppressing-the-linter-is-dangerous*/}

If you have an existing codebase, you might have some Effects that suppress the linter like this:

```js {3-4}
useEffect(() => {
  // ...
  // 🔴 Avoid suppressing the linter like this:
  // eslint-ignore-next-line react-hooks/exhaustive-deps
}, []);
```

When dependencies don't match the code, there is a very high risk of introducing bugs. By suppressing the linter, you "lie" to React about the values your Effect depends on.

</Pitfall>

## Removing unnecessary dependencies {/*removing-unnecessary-dependencies*/}

Every time you adjust the Effect's dependencies to reflect the code, look at the dependency list. Does it make sense for the Effect to re-run when any of these dependencies change? Sometimes, the answer is "no":

* You might want to re-execute *different parts* of your Effect under different conditions.
* You might want to only read the *latest value* of some dependency instead of "reacting" to its changes.
* A dependency may change too often *unintentionally* because it's an object or a function.

To find the right solution, you'll need to answer a few questions about your Effect. Let's walk through them.

### Should this code move to an event handler? {/*should-this-code-move-to-an-event-handler*/}

The first thing you should think about is whether this code should be an Effect at all.

Imagine a form. On submit, you set the `submitted` state variable to `true`. You need to send a POST request and show a notification. You've put this logic inside an Effect that "reacts" to `submitted` being `true`:

```js {6-8}
function Form() {
  const [submitted, setSubmitted] = useState(false);

  useEffect(() => {
    if (submitted) {
      // 🔴 Avoid: Event-specific logic inside an Effect
      post('/api/register');
      showNotification('Successfully registered!');
    }
  }, [submitted]);

  function handleSubmit() {
    setSubmitted(true);
  }
  // ...
}
```

Later, you want to style the notification message according to the current theme, so you read the current theme. Since `theme` is declared in the component body, it is a reactive value, so you add it as a dependency. But now, changing the theme would re-send the registration request, which is not what you want.

**Code inside event handlers isn't reactive, so it will only run when the user performs the same interaction again.** Move the logic into the handler:

```js {3-5}
function Form() {
  const theme = useContext(ThemeContext);

  function handleSubmit() {
    // ✅ Good: Event-specific logic is called from event handlers
    post('/api/register');
    showNotification('Successfully registered!', theme);
  }
  // ...
}
```

Now the code lives in an event handler, and the dependency problem disappears.

### Is your Effect doing several unrelated things? {/*is-your-effect-doing-several-unrelated-things*/}

The next question to ask is whether your Effect is doing several unrelated things. Split it into separate Effects, each with its own synchronization process and its own dependencies.

<Recap>

* Dependencies should always match the code.
* When you're not happy with your dependencies, what you need to edit is the code.
* Suppressing the linter leads to confusing bugs, and you should always avoid it.
* To remove a dependency, "prove" to the linter that it's not needed.
* If some code should run in response to a specific interaction, move that code to an event handler.
* If different parts of your Effect should re-run for different reasons, split it into several Effects.

</Recap>
