---
applyTo: "**/*.md,**/*.mdx,**/*.html,**/*.css,**/*.scss,**/*.tsx,**/*.jsx,**/*.vue,**/*.svelte,**/*.astro"
---

Text people read (README, docs, UI copy) and UI people use follow the ai-design standard:
https://github.com/jungrok5/ai-design/blob/main/docs/standard.md

Writing
- One speech level per document. Korean docs use 합니다체; list items and table cells are noun phrases.
  A product UI uses the one register the product chose (해요체 is fine there).
<!-- style-ignore-start -->
- No hype adjectives, superlatives without a source, translationese (`~을 통해`, `~에 있어서`, `수행합니다`),
  personification, or sentences that talk to the reader. In English: no delve, leverage, seamless, cutting-edge,
  "it is important to note", "In conclusion,".
<!-- style-ignore-end -->
- Start with the fact and end on the last fact: no run-up, no recap, no forced groups of three.
- Never add facts, numbers, names or quotes while polishing. Leave `[number needed]` where a number is missing.
- Form follows content: explanation as short paragraphs, actions as copyable commands, flows with 3+ steps or
  2+ actors as a diagram, comparisons as tables.

UI
- Use the project's design tokens. With none, use the "Clear" tokens and components from
  ai-design (`plugins/ai-design/skills/polish-ui/design/`).
- No purple/indigo gradients, gradient text, emoji icons, colored side stripes on cards, or the same three cards.
- No raw colors or font stacks outside the tokens file. Contrast 4.5:1 for body text, visible `:focus-visible`.

Check
After editing any of these files, run the style check on the files you changed and fix every `error`
(judge each `warning` in context). A clean run prints nothing but the summary line.

    git clone --depth 1 https://github.com/jungrok5/ai-design ~/.ai-design   # once
    python3 ~/.ai-design/plugins/ai-design/style/style_check.py <changed files>

Mark a line you quote on purpose with `style-ignore`. Project overrides live in `.style/rules.toml`.
