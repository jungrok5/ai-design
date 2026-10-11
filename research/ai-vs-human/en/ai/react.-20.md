I couldn't save the file because the Write tool is disabled in this session, so here is the page as Markdown you can paste into a file:

```markdown
# React Versions

React uses semantic versioning (semver) for its releases. Each version number has three parts, MAJOR.MINOR.PATCH, and each part signals how much a release might change.

## Semantic versioning

- **Major** releases, such as 18.0.0 to 19.0.0, can contain breaking changes. They may remove deprecated APIs, change default behavior, or require updates to your code before your app works again.
- **Minor** releases, such as 18.2.0 to 18.3.0, add new features and improvements. They are designed to be backward compatible, so existing code should keep working without changes.
- **Patch** releases, such as 18.2.0 to 18.2.1, fix bugs and security issues. They do not add new features and should be safe to install.

## Release channels

React publishes releases through several channels. Most applications should use the Latest channel.

### Latest

The Latest channel contains the most recent stable release. This is the version that `npm install react` installs by default. Stable releases are tested thoroughly and are recommended for all production applications.

### Canary

Canary releases include features that are ready for testing but have not yet shipped in a stable version. They are published frequently and may change before the next stable release. Canary builds are useful for framework authors and teams that want to try upcoming features early. Install them with the `canary` tag.

### Experimental

Experimental releases include features that are still being developed and may never ship in their current form. They exist for experimentation and feedback only. Do not use experimental builds in production.

## Choosing a version

When choosing a version, keep the following guidelines in mind:

1. Use the latest stable version for new projects.
2. Upgrade to a new major version only after reading its upgrade guide.
3. Commit your lockfile so that every developer and every build installs the same versions.
4. Avoid mixing channels. A stable React DOM with a canary React package will cause errors.

## Upgrading

Before upgrading to a new major version, run your test suite and check the browser console. React logs warnings in development mode for deprecated APIs, so resolve these warnings before you upgrade. When possible, upgrade one major version at a time rather than skipping several.

To upgrade React and React DOM together, run the following command:

```bash
npm install react@latest react-dom@latest
```

## Deprecations

Deprecated features continue to work in the current major version but produce warnings in development. They are removed in a later major version. Deprecations are announced in release notes before removal, so reviewing those notes is the best way to find out what needs updating.

## Keeping packages in sync

React and React DOM must use matching versions. Libraries that depend on React should declare it as a peer dependency rather than bundling their own copy. Mismatched copies can cause errors such as "Invalid hook call." Your `package.json` should list both packages with the same major version:

```json
{
  "dependencies": {
    "react": "^19.0.0",
    "react-dom": "^19.0.0"
  }
}
```

## Version history

The following table lists selected major releases and their most notable changes.

| Version | Released | Notable change |
| --- | --- | --- |
| 16.8 | February 2019 | Introduced Hooks |
| 17.0 | October 2020 | Eased gradual upgrades; no new features |
| 18.0 | March 2022 | Introduced concurrent rendering |
| 19.0 | December 2024 | Introduced Actions and the `use` API |

This page describes the release history known when it was written. For the latest version, check the release notes or the npm registry.
```

This is written in the style of the React docs but is not the official text, so check it against react.dev before publishing it anywhere. The body text is about 600 words, excluding code and the table.
