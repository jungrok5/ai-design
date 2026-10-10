# CLAUDE.md

This repo is a Claude Code plugin marketplace with one plugin, `plugins/ai-design` (skills `polish-writing`,
`polish-ui`, the design system "Clear", and `style/style_check.py`). The standard is `docs/standard.md`.

- Keep `version` in `.claude-plugin/marketplace.json` and `plugins/ai-design/.claude-plugin/plugin.json` equal; bump both
  for any change users should receive. Pre-commit users pin a commit SHA or a `vX.Y.Z` tag.
- A rule that misfires gets fixed in `style/rules.toml` with a test in `tests/`, not silenced with `style-ignore`.
- Check before committing: `python3 -m unittest discover -s tests` and the style check on changed files.
- Prose for people (README, docs) is Korean 합니다체; code, comments and commit messages are English.
