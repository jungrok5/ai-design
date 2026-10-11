I can't save a `.md` file in this session because the shell and file-writing tools aren't available, so here is the page in full:

---

# Contributing

Thanks for your interest in contributing to React! This page explains how to report problems, propose changes, and submit code. Whether you are fixing a typo or building a new feature, your help makes React better for everyone who uses it.

## Ways to contribute

There are many ways to help beyond writing code:

- **Answer questions** from other developers in community forums and chat channels.
- **Review pull requests** and leave constructive feedback on proposed changes.
- **Improve the documentation** by fixing unclear explanations, adding examples, or translating pages.
- **Report bugs** with a clear, reproducible example.
- **Write libraries and tools** that extend React and share them with the community.

If you are new to open source, documentation and issue triage are excellent places to start.

## Before you start

Please read the Code of Conduct first. We expect everyone in the project to treat others with respect, patience, and good faith. Harassment and dismissive behavior are not acceptable in issues, pull requests, or discussions.

Next, search existing issues and pull requests. Someone may already be working on the same problem, and the discussion there may answer your question.

## Reporting bugs

A good bug report makes it easy to reproduce the problem. Include:

1. The version of React and any related packages you are using.
2. The environment, such as the browser, operating system, or Node.js version.
3. A minimal reproducible example, ideally in a sandbox such as CodeSandbox or a small repository.
4. What you expected to happen, and what actually happened.

Keep the example as small as possible. Removing unrelated code often reveals the real cause of the bug, and it helps maintainers respond faster.

## Proposing changes

Large changes are easier to review when they start as a discussion. If you want to add a new API or change existing behavior, open an issue first and describe the problem you want to solve. This gives maintainers a chance to share context, suggest alternatives, and confirm that the work fits the project's direction before you invest significant time.

Small fixes, such as correcting a typo or a clear bug with an obvious solution, can go directly to a pull request.

## Submitting a pull request

Follow these steps when you submit code:

1. Fork the repository and create a branch from the main branch. Use a descriptive name, such as `fix-effect-cleanup`.
2. Make your changes in small, focused commits.
3. Add or update tests that cover the change.
4. Run the test suite and linters locally, and fix any failures.
5. Open a pull request and describe what the change does and why. Link to any related issue.

Keep each pull request focused on one concern. A pull request that fixes a bug and also reformats unrelated files is harder to review and may be asked to be split.

## Development workflow

The React repository is a monorepo containing several packages. Install the dependencies at the root of the repository, then use the scripts defined in the project's configuration to build, test, and lint. Most packages can be tested in isolation, which makes it faster to iterate on one area.

When you write tests, prefer testing observable behavior over implementation details. Tests that describe what a user or a developer would see tend to survive refactoring and catch real regressions.

Code style is enforced by automated tools. Run the formatter before you commit so that reviewers can focus on the substance of your change.

## Review process

Maintainers review pull requests as their time allows. You may receive requests for changes, and that is a normal part of the process. Respond to feedback by pushing new commits; avoid force-pushing during review, because it makes it harder for reviewers to see what changed since their last comment.

If a pull request has been quiet for a while, a polite follow-up comment is welcome. Please be patient, since maintainers handle many contributions at once.

## Licensing

React is released under the MIT License. By submitting a contribution, you agree that your work may be distributed under the same license.

## Thank you

Every contribution, large or small, helps the React community. We look forward to working with you.

---

Notes:
- This is an original page written in the style of the React docs, not a copy of the official text. I can't reproduce the official page word for word from memory.
- The body is roughly 680 words by my estimate. I didn't run a word count because I had no way to execute commands here.
- If you want it as a file, copy the text above into a `contributing.md` file, or ask me in a session where file writing is available.
