## Writing and UI

Text people read and UI people use follow the ai-design standard
(https://github.com/jungrok5/ai-design/blob/main/docs/standard.md):

- Docs and README in 합니다체, one speech level per document; lists and table cells as noun phrases.
- No hype, translationese, personification or talking to the reader. Never add facts or numbers while polishing.
- Content form: explanation as short paragraphs, actions as copyable commands, flows with 3+ steps or 2+ actors as a
  diagram, comparisons as tables.
- UI uses the project's design tokens; if there are none, the default "Clear" tokens and components from ai-design.
  No raw colors or font stacks outside the tokens file.
- After editing, run the style check and fix every error:
  `python3 <path-to-ai-design>/plugins/ai-design/style/style_check.py <changed files>`
