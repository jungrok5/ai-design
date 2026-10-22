# English AI-writing tells, 2025–2026: website copy, docs, and Claude-specific patterns

Research date: 2026-10-22. Scope: what English-speaking communities currently call out as tells of AI-written text,
weighted toward landing pages, product pages, docs, READMEs and Claude-era (Opus 4.6 → 5.x, Fable) patterns.

## 0. Method and caveats

- Read directly: Wikipedia:Signs of AI writing (raw wikitext, current revision), Graphite's "AI Tells" corpus study,
  Anthropic docs (Fable 5.1 and Sonnet 5 prompting guides, frontend-design skill), GitHub repos (stop-slop,
  humanizer, tropes.fyi, claudeisms, slop-detect), Hacker News threads, and practitioner blogs.
- **Not reachable:** reddit.com is blocked for both WebSearch and WebFetch in this environment, so there are no
  first-hand Reddit quotes below. X/LinkedIn posts appear only as search-result snippets, marked *(snippet)*.
  The Economist, NYT, Washington Post and Fast Company returned 403. They are cited through the secondary pages named.
- "#src" = rough count of independent sources that name the pattern. Vendor "AI words to avoid" lists are counted
  only once as a group because they copy from each other.
- Coverage was checked against `plugins/ai-design/style/rules.toml` by running `style_check.py` on 130+ probe
  sentences (one per paragraph). Results are in §4.

### Source keys

| Key | Source |
|---|---|
| WP | https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing (raw wikitext, Oct 2026) |
| GRAPH | Graphite, "AI Tells" (2026-09-16), 90k AI vs 10k pre-2022 human articles, incl. Claude Opus 4/4.6/5 — https://graphite.io/five-percent/research/ai-tells |
| ANT-M | Anthropic, Prompting Claude Fable 5.1, "Writing density" — https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1 |
| ANT-FD | Anthropic frontend-design skill — https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md |
| ANT-S5 | Anthropic, Prompting Claude Sonnet 5 — https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5 |
| ECON | The Economist, "How to spot AI writing" (2026-07-30), via WP and https://daringfireball.net/linked/2026/08/11/ |
| CI | archiewood/claudeisms: word-frequency study of Opus 4.7/4.8 Claude Code output vs Stack Overflow — https://github.com/archiewood/claudeisms |
| I77136 | anthropics/claude-code #77136, "repetitive rhetorical tics" (Jul–Oct 2026) — https://github.com/anthropics/claude-code/issues/77136 |
| I53454 | anthropics/claude-code #53454, "can not stop using load-bearing" — https://github.com/anthropics/claude-code/issues/53454 |
| HN-LB | HN, "How to stop Claude from saying load-bearing" — https://news.ycombinator.com/item?id=48905248 |
| SLHCK | "Claudish" (2026-06-22) — https://slhck.info/software/2026/06/22/claudish.html |
| WB | "The AI Idiolect" (2026-07-16) — https://workbravely.substack.com/p/the-ai-idiolect-a-professional-writers |
| DAD | Daily AI Digest, "How To Combat Claude-Slop" (2026-09-03) — https://buttondown.com/dailyaidigest/archive/dad-how-to-combat-claude-slop-93/ |
| SS | hardikpandya/stop-slop, references/phrases.md + structures.md — https://github.com/hardikpandya/stop-slop |
| HUM | blader/humanizer SKILL.md v3.1.0 — https://github.com/blader/humanizer |
| TROPES | tropes.fyi gist — https://gist.github.com/ossa-ma/f3baa9d25154c33095e22272c631f5a1 |
| SD | ravidsrk/slop-detect, spec/copy-axis.md + packages/core/src/copyPatterns.ts — https://github.com/ravidsrk/slop-detect |
| SD279 | slop-detect issue #279, "context_leak_copy" (2026-10-20) — https://github.com/ravidsrk/slop-detect/issues/279 |
| GOD | "10 tells of a slop UI" (2026-09-27) — https://godobject.dev/blog/10-tells-of-slop |
| HN-UI | HN thread on GOD (386 pts) — https://news.ycombinator.com/item?id=49867038 |
| HN-LP | HN, "Are we in the era of AI slop landing pages?" — https://news.ycombinator.com/item?id=49024805 |
| HN-IMP | HN, "Impeccable Style" — https://news.ycombinator.com/item?id=46587284 |
| HN-NXY | HN comment, "No x, no y, just Z is a pattern so often used by chatGPT…" — https://news.ycombinator.com/item?id=46339333 *(snippet)* |
| KREBS | Adrian Krebs, "AI design slop" study of ~1,590 Show HN pages (2026-04-20) — https://www.adriankrebs.ch/blog/design-slop/ |
| CC | Capital & Compute, "How to Fix AI Slop in Web Design, Tell by Tell" (2026-09-25) — https://capitalandcompute.net/blog/fix-ai-slop-design/ |
| 925 | 925 Studios, "AI Slop Web Design" (2026) — https://www.925studios.co/blog/ai-slop-web-design-guide |
| OC | Olivia Cal Copywriting, "How to Spot AI Writing Tells" (2026, upd. May) — https://www.oliviacal.com/post/ai-writing-tells |
| CARLY | "Spotting machine-made prose" (2024-12-05) — https://carly.substack.com/p/spotting-machine-made-prose |
| RAS | "The LLM-ism Dictionary" (2026-08-15) — https://roughatsea.com/notes/the-llm-ism-dictionary/ |
| VOLL | "I Asked the Machine to Tell on Itself" (2026-04-24) — https://matthewvollmer.substack.com/p/i-asked-the-machine-to-tell-on-itself |
| AIW | aiwriter.ai slogan generator page (vendor) — https://aiwriter.ai/tools/ai-slogan-generator |
| JEN | Jenova, AI tagline generator (2026-04-09, vendor) — https://www.jenova.ai/en/resources/ai-tagline-generator |
| SG | Single Grain, "How LLMs interpret positioning statements and taglines" — https://www.singlegrain.com/intermediate-marketers/how-llms-interpret-positioning-statements-and-taglines/ *(search excerpt; full fetch timed out)* |
| BRICK | Dave Bricker, "Why AI-Generated Marketing Copy Misses the Mark" (2023/2024) — https://speakipedia.com/ai-generated-marketing/ |
| KRISS | Sam Kriss, NYT Magazine (2025-12-03), via https://maxread.substack.com/p/will-ai-writing-ever-be-good |
| WAPO | Washington Post ChatGPT style analysis (2025-11-13), via https://www.bostonglobe.com/2025/11/13/business/chatgpt-writing-style-clues/ |

---

## 1. Lexical and phrasal tells

### 1a. Landing-page hero and tagline formulas

The hypothesised hero formulas you listed are only partly documented. Several have **no** independent call-out
in 2025–26 sources (marked "none found"). Treat those as plausible but unverified.

| Pattern | Real examples (quoted from source) | Sources | #src |
|---|---|---|---|
| **No X. No Y. Just Z.** / "No X, no Y, just Z" / "Not X. Not Y. Z." | "No hardware. No fees. Just growth." (OC: "appears in every section of a landing page"); "The most obvious tell is the "No this. No that." copy which you find everywhere." (HN-UI, user 65); "Not a bug. Not a feature. A fundamental design flaw." (TROPES) | OC, HN-UI, HN-NXY, TROPES, WP §Not X but Y, SS "Negative Listing", SD `bare_antithesis` + SD279, I77136 | 8 |
| **X, reimagined** | "X, reimagined" named as one of "the same five cliché structures everyone has seen" (AIW); "Work, reimagined" vs "Async collaboration platform for remote engineering teams" (SG) | AIW, SG | 2 (both marketing vendors) |
| **The future of X** / "Build the future" | "The future of X" (AIW); "Build the future of work." (925); "Welcome to the Future of Work" cited as the classic too-clever headline in a 2026 headline guide (search result only) | AIW, 925 | 2 |
| **Where X meets Y** | "Where Excellence Meets Innovation", listed with "Empowering Your Success" and "Innovative Solutions for a Better Tomorrow" as what everyone gets from the same chatbot (JEN) | JEN (+ generator sample outputs) | 1 |
| **Experience the difference / Experience the power of X** | "Experience the difference" (AIW); "Experience the power of task management with our cutting-edge intuitive interface." (GOD) | AIW, GOD | 2 |
| **Generic scope or abstraction headline** | "Scale without limits." / "Your all-in-one platform." / "Empowering teams to build better products" (925); "innovative platform for modern teams" (SG) | 925, SG | 2 |
| **Elevate your X** | "Elevate your workflow" (CC); "Ready to elevate your brand…" (BRICK); "Elevate" (GOD) | CC, BRICK, GOD, OC, RAS, SD lexicon, WB | 6+ |
| **Supercharge / Unleash / Revolutionise your X** | "Supercharge," "Unleash," "Revolutionise your workflow" (GOD) | GOD, SD lexicon, vendor lists | 3 |
| **Unlock X** | "unlock new possibilities", "unlock the potential of…" (RAS); "unlocking the potential of AI-Enhanced Copywriting" (BRICK); "unlock" in Graphite's marketing-language class | RAS, BRICK, GRAPH, OC, WB ("metaphors as verbs"), SD | 6 |
| **Say goodbye to X** | "Say goodbye to endless hours spent crafting captivating marketing copy." (BRICK, 2023 sample of AI copy) | BRICK | 1 (and pre-2025) |
| **From A to B** ("false range") | "From innovation to implementation to cultural transformation." (TROPES: "what's in between???? Nothing!") | TROPES | 1 (prose, not hero-specific) |
| **Explore the limitless possibilities / game-changing opportunity** | both from BRICK's AI sample | BRICK | 1 |
| **Lowercase "one X. one Y." tagline** | "one campus. one app." (GOD); `one [a-z]+\. one [a-z]+\.` proposed (SD279) | GOD, HN-UI, SD279 | 2 |
| **Slogan pairs on sign-in or empty states** | "Find your words. Then make them yours." and "Sign in to pick up where you left off." (HN-UI, charles_f: "seven slogans and catch-phrases") | HN-UI | 1 |
| **"X, without the Y"** taglines | "React, without the nonsense", "your UI, simple, uncluttered" (HN-UI, slopinthebag) | HN-UI | 1 |
| **Context leak into copy** | "Your files never leave your browser" ("an INCESSANT need to inform you of this fact"); "Built with Hugo. Written from Neovim" (HN-UI, GOD, SD279) | HN-UI, GOD, SD279, SD `context_leak_copy` | 3 |
| **Generic CTA** | "Get Started" → "Name the action the button performs" (CC); "Get started for free" called "structurally sound and completely generic" for Claude Design output (magier.com via search) | CC, ANT-FD ("Save changes," not "Submit") | 2–3 |
| Built for teams who… / Ship faster / Your X, your way / Everything you need to… / Designed with care / Beautifully simple | **none found.** "Ship your startup in days, not weeks" exists as human (ShipFast) copy, not as a cited AI tell | — | 0 |
| crafted / thoughtfully crafted | one copywriter's complaint about "meticulously crafted" (Substack comment, search only); "crafting captivating" in BRICK sample | weak | ≤1 |
| effortless / frictionless / reimagine / future-proof / bespoke | listed in slop-detect's `marketing_2024_2026` buzzword lexicon (SD) | SD | 1 (curated lexicon) |

### 1b. Marketing adjectives and verbs (product pages, feature cards)

| Word family | Examples | Sources | #src |
|---|---|---|---|
| seamless(ly) | "the single most diluted word in the dictionary" (OC); "Particularly common in product copy" (RAS); "Seamless" (GOD) | OC, RAS, GOD, SD, WB, VOLL, vendor lists | 6+ |
| empower / transformative / revolutionary / game-changing / cutting-edge / next-gen | GOD's list; RAS #153 "marketing gloss": mundane capabilities become "powerful," "seamless," "transformative," or "game-changing" | GOD, RAS, OC, SD, VOLL, 925 | 5+ |
| payoff / amplify / boost / wins / tangible / streamline / leverage | Graphite's "marketing language" class; Astra uses it 73% less than GPT-4.1 | GRAPH | 1 (but corpus-measured) |
| showcase | "The marketing cousin of highlight" (RAS) | RAS, WP, HUM | 3 |
| journey | "LLMs convert processes into journeys with remarkable enthusiasm" (RAS); "Journey" in OC's flowery-metaphor list; "continue their journey toward excellence" (HUM example) | RAS, OC, CARLY, HUM | 4 |
| powerful / intuitive | "cutting-edge intuitive interface" (GOD) | GOD, RAS | 2 |
| Hype words now *declining* in Claude | "groundbreaking," "paramount," "unprecedented," "revolutionary," "invaluable," "profound," "exceptional" (GRAPH, falling across Claude versions) | GRAPH | 1 |

Note from GRAPH: generic hype is fading in newer models. The 2026 Claude signal is mostly **mannered/metaphorical
phrasing and contrast frames** (§1c, §2), not "revolutionary".

### 1c. Claude-era (2025–2026) lexical tells

Most of these came from Claude Code and agent output, then show up in docs, READMEs and commit messages written by
the same sessions (HN-LB: "load-bearing" in coworkers' "vibed docs"; I53454: "chat output, documents it writes,
commit messages").

| Pattern | Examples (quoted) | Sources | #src |
|---|---|---|---|
| **load-bearing** (figurative) | ">7,500x" vs Stack Overflow (CI); "Claude Code very frequently uses the word "load-bearing" in chat output, documents it writes, commit messages" (I53454); "13 load bearing em dashes" (HN-LB) | CI, I53454, I77136, HN-LB, WB, DAD, Marek Šuppa TIL (https://mareksuppa.com/til/load-bearing/), X (Nate Emerson, *snippet*) | 7 |
| **honest / honestly / "honest caveat" / "the honest take"** | "Honest caveat: X." (SLHCK); "The honest take: I was wrong" (HN-LB); "honest" still seen on Sonnet 5.5 (I77136, Oct 3) | SLHCK, HN-LB, I77136, CI (22x), X *(snippet: "Honest take.")* | 4 |
| **genuine / genuinely** | "genuinely" 224x vs SO (CI); listed as intensifier (WB) and adverb to kill (SS) | CI, WB, SS, HN-LB | 4 |
| **quietly / quiet** | "quietly orchestrating workflows, decisions, and interactions", "a quiet intelligence behind it" (TROPES); "I have been quietly building the product that's going to change everything" (WB); Kriss: models "love quietness", "softly humming" (KRISS); on WP's mid-2026 word list | TROPES, WB, KRISS, WP, HUM | 5 |
| **earns its keep / earned its place** | Anthropic: "Instead of "this point still matters," they write "this point earns its keep."" (ANT-M); "What do you mean that an agenda item has 'earned its place,' Claude?!?!?" (WB) | ANT-M, WB | 2 |
| **a dial worth turning** (type: X worth Y-ing metaphor) | "Instead of "a parameter worth varying," the mannered writer produces "a dial worth turning."" (ANT-M, quoted by GRAPH and DAD) | ANT-M, GRAPH, DAD | 3 |
| **less like a _ and more like** / "less X, more Y" | 105x human rate in Opus 5 (125 vs 1 occurrences); Claude does less-X-more-Y comparisons 82x as often as humans (GRAPH) | GRAPH | 1 (corpus) |
| **rather than merely / rather than simply** | 160x / 43x in Opus 5 (GRAPH); "Y rather than X … particularly common in recent LLM output" (WP) | GRAPH, WP | 2 |
| **matters because / matters more than / "This matters because"** | 132x / 93x Opus 5 (GRAPH); "This matters because" is an emphasis crutch (SS) | GRAPH, SS, WP (GPT-6 "matters") | 3 |
| **single most / arguably the most / every single / enormously** | Opus 5 superlative framing (GRAPH); "the single most important correction" (SLHCK) | GRAPH, SLHCK | 2 |
| **deliberate / steady / measured** | 26x / 6x / 4.2x Opus 5 (GRAPH); "steady" also on WP's GPT-6 list | GRAPH, WP | 2 |
| **without losing / sacrificing / compromising** | 6.1x / 4.3x / 2.6x Opus 5 (GRAPH) | GRAPH | 1 |
| **what comes next / looking ahead** | 28x / 33x Opus 5 (GRAPH) | GRAPH | 1 |
| Dev-jargon carried into prose: gating/gated, seam, surface(d), wired/wiring, landed, settles, verdict, scaffold, drift, canonical, cleanly, parity, mirrors, harness, floor | ratios 20x–762x vs SO (CI); "seam, substrate, load-bearing" (X *snippet*); "land" as a verb (HN-LB); "gate/gated/gating (figurative)" on HUM's word list | CI, HN-LB, HUM, WB ("surface", "land", "anchor", "earn"), X | 4 |
| **Invented concept labels** | "the supervision paradox", "the acceleration trap", "workload creep" (TROPES); "instrumentation is the unlock" (I77136); "Claude invents a noun for a concept and then reuses it" (DAD) | TROPES, I77136, DAD, SLHCK ("fleet-storm collapse") | 4 |
| **"prose", "push back", "hand-waving", "here's where I'd hold the line"** | from I77136 issue body and comments | I77136, HN-LB ("push back", "key insight") | 2 |
| **Aphorism template "X is the language/currency/architecture of Y"** | "Symmetry is the language of trust." (HUM before-example) | HUM | 1 |
| **"stops being X and starts being Y"** | (SS table); "workflows stop being collections of manual steps and start becoming orchestrations" (TROPES) | SS, TROPES | 2 |
| **"Two things worth flagging"**, "It's worth stating precisely", "Here's the argument, in plain terms" | quoted as leaked phrasing (HN-UI: trencedamp, unholiness) | HN-UI | 1 |
| **"Think of it as…" / "It's like a…"** | "Think of it as a Swiss Army knife for your workflow." (TROPES) | TROPES | 1 |
| **"Imagine a world where…"** | (TROPES, OC blacklist "Imagine a world") | TROPES, OC | 2 |
| GPT-6/mid-2026 list on WP: challenge, clearer, dependable, echoed, foster, leverage, matters, multifaceted, practical, prioritize, quietly, steady, universally | (WP, sourced to a 2026 review) | WP | 1 |
| Mid-2026 "corrective framing": "should be treated as … rather than as …", "the available information does not establish…", "should not be confused with" | Nemgiri example "disclosed as either ChatGPT or Claude" (WP, citing GRAPH) | WP, GRAPH | 2 |

### 1d. Older GPT-era list (still cited, mostly covered by our rules)

delve, tapestry, testament, intricate, meticulous, pivotal, vibrant, showcase, underscore, foster, realm, beacon,
embark, plethora, myriad, landscape, navigate, "in today's fast-paced world", "it's worth noting", "at its core",
"let's dive in", "in conclusion". Sources: WP (era table), SD `gpt4_2023_2024` lexicon, OC, RAS, CARLY, SS.
WP notes "delve" faded after 2024. WAPO: "delve" in only 1 in 1,000 ChatGPT chats by July 2025. Low value for new rules.

---

## 2. Ornamental metaphor: what is actually called out

**Primary source.** Anthropic's own Fable 5.1 guide names the problem and gives a suppression prompt: "Mannered
prose substitutes metaphor and flourish for direct statement. … The phrases exist to display the writer, not to
convey the idea … Metaphors drag in connotations the writer did not choose and cannot control. The fix is to say
what you mean. When a literal phrase is available, use it." Short form: "Please remove all mannered prose." (ANT-M)

**Measured.** GRAPH scored "mannered prose" (Anthropic's definition, model-judged index): Claude Opus 5 ≈ 2.5× the
human score, Gemini 3.1 Pro ≈ 2.5×, GPT-6 Astra ≈ 1.2×. This is the most direct evidence that ornamental phrasing
is a *current Claude* signal, not just an old ChatGPT one.

**Community.** I77136 (Jul–Oct 2026): "Forced, on-the-spot metaphors that must be decoded". A commenter quotes
Claude's reply to its own preferences: "a metaphor can illustrate a point but can't carry it". The issue was
closed on 2026-10-03 with the author saying it was addressed in the 5.5 models, yet a commenter still saw
"load-bearing" and "honest" on Sonnet 5.5 the same day. TROPES "The Dead Metaphor": "AI will repeat the same
metaphor 5-10 times" ("Walls and doors used 30+ times in the same article").

| Metaphor family | Called out? | Evidence |
|---|---|---|
| tapestry / weave / woven | **Yes, strongly** (classic) | WP, OC, CARLY ("symphonies," "tapestries," or "complex dances"), RAS #7 "canonical synthetic-profundity noun", TROPES, VOLL. "weave" itself is weak: only one vendor list |
| landscape / realm / ecosystem / terrain (domain-as-geography) | **Yes, strongly** | RAS #5 "LLMs love turning domains into geography", OC "spatial metaphors", TROPES, WB, WP |
| journey / path / roadmap / embark | **Yes** | RAS #25, OC ("Journey," "Roadmap"), CARLY, HUM example; SD lexicon "embark" |
| symphony / dance / orchestrate | **Yes** (moderate) | OC ("Symphony"), CARLY ("complex dances"), VOLL; TROPES "quietly orchestrating" |
| beacon / cornerstone / bedrock / mosaic / labyrinth | **Yes** (moderate) | OC, VOLL, SD lexicon, search-cited lists |
| lens ("through the lens of") | **Yes** | RAS #45; WP example "Through this lens…" |
| unlock / anchor / surface / land / earn / carry / hold / frame (metaphor-as-verb) | **Yes, newer** | WB §4 "Metaphors as Verbs" (16 verbs, with a Claude example); CI ("surfaced", "landed", "wired"); ANT-M ("earns its keep") |
| dial / lever / knob ("a dial worth turning", "the cause and the lever") | **Yes, Claude-specific** | ANT-M, GRAPH, SLHCK title "the Cause and the Lever Were Misstated" |
| load-bearing / seam / scaffold / gate / harness (engineering metaphors in prose) | **Yes, Claude-specific** | CI, I53454, I77136, HN-LB, HUM ("gate/gated/gating (figurative)") |
| ghosts / whispers / quiet / hum (atmospheric) | **Yes**, mainly fiction and creative copy | KRISS (via Max Read), TROPES ("quietly"), WB |
| north star / flywheel / moat | Yes (strategy-deck jargon) | already in our `en-buzz-metaphor` |
| "Think of it as a…" analogies | Yes | TROPES |
| X is the language/currency/architecture of Y | Yes | HUM §3 |
| flows / streams ("your work flows…") | **Not found** as a named tell (only "seamless flow" in generic lists) | — |
| canvas / heartbeat / compass / bridge / "home for…" / "second brain" / superpowers / magic | **Not found** in any 2025–26 source checked. A targeted search for north star/bridge/canvas/heartbeat/compass found nothing beyond "lens" and "tapestry" | — |

Inference (not from a source): the page-level prompts Anthropic itself publishes for frontend work are written in
metaphor ("so the page breathes", "feel sharp and controlled", "surprise and delight") (ANT-S5; best-practices
`<frontend_aesthetics>` snippet https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices).
A model that matches a "creative, distinctive" register for visuals may carry it into the copy. Anthropic's
frontend-design skill pushes back on this explicitly: "Words … are design content, not decoration … Describe what
something is or does in plain terms rather than selling it. Being specific and legible to new users is always better
than being clever." (ANT-FD). That sentence fits polish-writing's website section almost word for word.

---

## 3. Structural and page-level tells

| Tell | Evidence (quoted) | Sources | #src |
|---|---|---|---|
| **Template hero**: centered H1, one-line muted subhead, filled + ghost button, gradient/dot-grid, tilted screenshot | (UXS, paraphrased: https://uxskill.laithjunaidy.com/blog/ai-landing-page-hero-generic.html); "Centered hero set in a generic sans" (KREBS) | UXS, KREBS, DD | 3 |
| **Badge/pill above H1** | "Badge positioned right above the hero H1" (KREBS); "Now in Beta" pill (SD) | KREBS, SD `hero_eyebrow_pill`, DD | 3 |
| **Eyebrow labels, all caps or small caps** | "a tracked-out ALL-CAPS eyebrow label above every heading" (ANT-FD); "You forgot the small caps headings or tags added randomly everywhere" (HN-UI); "header, 'eyebrow', h1, description, footer all saying the same thing" (HN-UI) | ANT-FD, HN-UI, CC, KREBS, SD | 5 |
| **Labels "WORD — fragment"** with spaced em dash; **meta strings "A · B · C"** | (ANT-FD, verbatim); "Center-dots as dividers are the new tell tale" (HN-UI); "Meta string 'A · B · C'" (CC) | ANT-FD, HN-UI, CC | 3 |
| **Accent one word in the headline** (italic/serif/colour) | "Accenting just a single word or phrase in a headline" (ANT-FD); "Serif italic used as the accent font for one hero word" (KREBS) | ANT-FD, KREBS, CC, SD `hero_accent_word` | 4 |
| **"01 / 02 / 03" markers on non-sequences** | "only appropriate if the content actually is a sequence" (ANT-FD); "numbering that never goes beyond 01" (HN-UI) | ANT-FD, HN-UI, CC, KREBS | 4 |
| **Identical icon-topped feature cards** (usually 3 or 4) | "Identical feature cards with an icon on top" (KREBS); "the SaaS-card kit" (ANT-FD); Sonnet 5 sample brief asks for "a benefit grid with three or four blocks" (ANT-S5) | KREBS, ANT-FD, GOD, SD `icon_card_grid` | 4 |
| **Stat banner / big-number hero with invented stats** | "a big number with a small label, supporting stats, and a gradient accent is the default treatment" (ANT-FD); "10,000% ROI", "500,000 founders": "delete numbers you cannot source" (CC); "Trusted by 10,000+ professionals" with 0 traffic (HN-LP) | ANT-FD, CC, HN-LP, KREBS, SD `stat_banner` | 5 |
| **Fake or placeholder testimonials** | slop-detect flags pravatar/dicebear avatars, duplicate avatars, and ≥2 testimonials with no role/company/link (SD `structural_fake_social_proof`, "gradient-letter avatars"); "Popular" $100 tier invented by Claude Code to look "SaaS-y" (HN-IMP, author) | SD, HN-IMP, HN-LP | 3 |
| **Text volume: header + subheader + bullets per section** | "Just sections and sections of header + subheader + bullet list … I'm reading max 2 sentences on any landing page." (HN-UI); "SO MUCH TEXT." | HN-UI | 1 |
| **Redundant label above content** | "unnecessary labels above content" (CC); "Adding unnecessary typographic labels above content" (ANT-FD) | CC, ANT-FD | 2 |
| **"→" on every link and button** | "a '→' appended to link and button text" (ANT-FD); "Claude in particular loves the -> arrow" (TROPES) | ANT-FD, TROPES, CC | 3 |
| **Rule of three / tricolons** | "LLMs overuse the rule of three" (WP, citing ECON and KRISS); SD `rule_of_three`; SS "Three-item lists" | WP, SD, SS, HUM, TROPES, KRISS | 5+ |
| **Contrast frames** "not X but Y", "not just X, it's Y", "X rather than Y", "less X, more Y" | WP §Negative parallelisms; WAPO: "not just X, but Y" in 6% of ChatGPT chats (Jul 2025); GRAPH: corrective framing rises across GPT versions while other tells fall | WP, WAPO, GRAPH, SS, HUM, TROPES, SD, I77136, HN-UI | 9 |
| **Em dash** | **Now model-dependent.** WP renamed the section "Overuse of em dashes (2022–September 2026)", and says the latest models are "hard coded to not use em dashes at all". ECON (Jul 2026): "only Claude used em dashes more than professional writers". GRAPH (Sep 2026): Opus 5 ≈ human rate. One blog cites Arena: Opus 5.5 at 0.8 per 1,000 words vs 15.2 for Opus 5 (https://medium.com/@brentcsutoras/the-em-dash-dilemma-how-a-punctuation-mark-became-ais-stubborn-signature-684fbcc9f559, *single source*) | WP, ECON, GRAPH, HN-UI, HN-LB | 5 |
| **Punctuation monotony** (post-em-dash) | WP: models that suppress dashes use commas and periods more than humans, "now that has become its own sign" ({{cn}}). ECON via Daring Fireball: fewer commas and semicolons than humans, "hardly any parentheses". GRAPH: humans use more "!" and parenthetical asides | WP, ECON, GRAPH | 3 |
| **Title Case headings** | "AI chatbots strongly tend to capitalize all main words" (WP); HUM §20; CARLY | WP, HUM, CARLY | 3 |
| **Headings written for effect** | "A heading written for effect ("The decision, on one screen") should name what the section holds" (HUM §20); titles that narrate revisions, e.g. "Thing Y is real, but the Cause and the Lever Were Misstated" (SLHCK) | HUM, SLHCK | 2 |
| **Emoji headings / bullets** (README "🚀 Getting Started") | WP: emoji before headings, "more rare now"; SD `emoji_bullet_headers`; readme-ai ships emoji themes (https://eli64s.github.io/readme-ai/concepts/customize/emojis/). Weak and template-driven, not model-specific | WP, SD, GOD ("Welcome to your Dashboard, [Name] ✨") | 3 |
| **Bold inline-header lists** ("**Label**: text") | WP §Inline-header vertical lists; OC #14; HUM §19 | WP, OC, HUM | 3 |
| **Announced structure / restated-thesis closer** | "In this section, we'll explore", "Here's what makes X different:" (SD `announced_structure`) | SD, SS meta-commentary | 2 |
| **Chat residue in UI copy** | "Needs You" instead of "Requires Attention" (HN-UI); "Two things worth flagging..." (HN-UI) | HN-UI | 1 |
| **Docs/READMEs** | Little dedicated 2025–26 material. What exists: Claude puts "load-bearing" and jargon into docs and commit messages (I53454, HN-LB, CI). WP's Markdown-misuse sections. Wikipedia notes Claude "typically do[es] not use curly quotes" | I53454, HN-LB, WP | thin |

---

## 4. Coverage against current English rules

Method: 130+ probe sentences run through `style_check.py` (en rules use IGNORECASE). "Covered" means a probe fired.

### 4a. Already covered (rule ids)

| Pattern | Rule |
|---|---|
| seamless(ly), supercharge, empower(ing), game-changing, cutting-edge, revolutionize (US spelling), unlock the power/potential, next-gen, best-in-class | `en-hype` |
| elevate your, streamline, robust, comprehensive, holistic | `en-buzzword` |
| tapestry, meticulous, showcase, underscore, pivotal, vibrant, leverage, delve | `en-ai-vocabulary` |
| No X. No Y. / No X, no Y, just Z / Not a X. Not a Y. | `en-negative-listing` |
| It's not (just) X, it's Y | `en-its-not-x-its-y` |
| north star, flywheel, moat, harness the power, resonates with, poised to | `en-buzz-metaphor` |
| landscape of / evolving landscape | `en-landscape-noun` |
| navigate the complexities | `en-navigate-complexities` |
| The result? X. | `en-rhetorical-self-answer` |
| Here's the kicker | `en-heres-the-catch` |
| Whether you're X or Y | `en-whether-youre` |
| In today's fast-paced… / in the realm of | `en-era-opener` |
| at its core, at the end of the day | `en-hollow-phrase` |
| serves as / boasts | `en-is-avoidance` |
| ", highlighting/ensuring/fostering…" | `en-ing-rider` |
| honestly, / let me be honest / to be honest | `en-performed-candor` (only these forms; not "honest caveat") |
| The implications/stakes are high | `en-meaning-telling` |
| Em/en dash as punctuation | `dash-overuse` (density-gated) |
| "Trusted by N+", ★★★★★, John Doe/Acme | `ui-fake-social-proof` (markup files only) |
| All-caps eyebrow, hero pill, gradient text, emoji in headings, "01" section numbers, → on links | `ui-eyebrow-caps`, `ui-hero-pill`, `ui-gradient-text`, `ui-emoji-heading`, `ui-section-number`, `ui-arrow-chrome` |

### 4b. NOT covered (probes that did not fire), with source strength

Ordered by evidence strength and fit for the user's complaint (ornamental website and doc copy).

| # | Pattern | Example probe that passed | Evidence | Regex idea (sketch, needs FP tests) |
|---|---|---|---|---|
| 1 | **Mannered prose / Claude metaphors**: earns its keep, earned its place, a dial worth turning, X worth Y-ing (figurative) | "This point earns its keep." / "A dial worth turning" | ANT-M (primary), GRAPH (2.5×), WB, DAD | `\bearn(?:s|ed|ing)? (?:its|their) (?:keep|place)\b`, `\b(?:dial|lever|knob)s? worth (?:turning|pulling)\b` |
| 2 | **load-bearing** (figurative), plus figurative gating/seam/scaffold | "the load-bearing piece of the design" | CI, I53454, I77136, HN-LB, DAD, WB (7) | `\bload[- ]bearing\b` outside code (add to `en-ai-vocabulary` or a new `en-claude-jargon`) |
| 3 | **less (like) X, more (like) Y** | "It feels less like a tool and more like a teammate." | GRAPH (105×) | `\bless (?:like )?(?:a |an )?[\w-]+(?: [\w-]+){0,3},? (?:and )?more (?:like )?` |
| 4 | **rather than merely/simply**, "not just X, but (also) Y", "not only … but also", "more than just" | "Not only fast but also private." / "It is not just a tool, but a partner." / "More than just a notes app." | GRAPH (160×), WP, WAPO (6% of chats), SS, SD `antithesis_construction` | `\brather than (?:merely|simply|just)\b`, `\bnot only\b[^.]{1,60}\bbut(?: also)?\b`, `\bnot just (?:a |an )?[^,.]{1,40},? but\b`, `\bmore than just (?:a|an)\b` |
| 5 | **quietly / quiet intelligence** as an importance adverb | "It works quietly in the background." | TROPES, WB, KRISS, WP (GPT-6), HUM (5) | `\bquietly\b` with a max_per_file cap (literal uses exist) |
| 6 | **honest caveat / honest take / genuinely** | "Honest caveat: the sync is slow." | SLHCK, HN-LB, I77136, CI, WB, SS | extend `en-performed-candor`: `\bhonest (?:caveat|take|answer|assessment|framing)\b`; `genuinely` into `en-filler-words` |
| 7 | **Hero formulas**: ", reimagined", "The future of X", "Where X meets Y", "Experience the difference/power of", "Scale without limits", "all-in-one platform" | "Project management, reimagined." | AIW, SG, 925, JEN, GOD (each 1–2) | `,\s*reimagined\b`, `\bthe future of (?:work|\w+ing)\b`, `\bwhere [\w ]{2,20} meets [\w ]{2,20}`, `\bexperience the (?:difference|power of)\b`, `\ball-in-one (?:platform|solution|workspace)\b` |
| 8 | **unlock** beyond "the power/potential" (unlock new possibilities, unlock growth) | "Unlock new possibilities for your team." | RAS, BRICK, GRAPH, OC, WB, SD (6) | `\bunlock(?:s|ing)? (?:new |your |the )?(?:possibilit|growth|insight|value|productivity)` |
| 9 | **Marketing adjectives** missing from `en-hype`: effortless(ly), frictionless, transformative, innovative, unparalleled, bespoke, future-proof, limitless possibilities, take X to the next level, revolutionise (UK) | "Effortless invoicing for freelancers." | SD lexicon, RAS #153, BRICK, GOD, OC | add to `en-hype`: `effortless(?:ly)?|frictionless|transformative|unparalleled|future-proof|limitless possibilities|to the next level|revolutionis\w*` |
| 10 | **journey / embark / roadmap** (non-literal) | "Begin your journey with us." | RAS, OC, CARLY, HUM | `\b(?:your|the|our|this) journey\b`, `\bembark(?:s|ed|ing)? on\b` |
| 11 | **Other ornamental nouns**: symphony of, a dance of, beacon, cornerstone, mosaic, through the lens of, weave/woven (figurative) | "A symphony of tools in one window." | OC, CARLY, VOLL, RAS #45 | `\ba symphony of\b`, `\bthrough (?:the|a|this) (?:new )?lens of\b`, `\b(?:beacon|cornerstone|bedrock|mosaic) of\b`, `\bweav(?:e|es|ing) (?:\w+ )?(?:into|together)\b` |
| 12 | **Analogy and futurism set-ups**: "Think of it as", "It's like a", "Imagine a world where" | "Imagine a world where your inbox sorts itself." | TROPES, OC | `\bthink of (?:it|this) (?:as|like)\b`, `\bimagine a world (?:where|in which)\b` |
| 13 | **"stops being X and starts being Y"** transformation arc | "It stops being a chore and starts being a habit." | SS, TROPES | `\bstops? being\b[^.]{1,40}\bstarts? being\b` |
| 14 | **Context leak into copy**: "never leave(s) your browser/device", "Built with X. Written from Y." | "Your files never leave your browser." | HN-UI, GOD, SD279 | `\bnever leaves? your (?:browser|device|machine)\b` (warn; legit for real local-only tools) |
| 15 | **Lowercase "one X. one Y." tagline** | "one campus. one app." | GOD, SD279 | `(?m)^\s*one [a-z]{3,15}\.\s+one [a-z]{3,15}\.` (case-sensitive) |
| 16 | **Social-proof in prose** (md/copy files): "Join 10,000+ teams", "Loved by developers everywhere", "Join thousands of happy customers" | "Join thousands of happy customers." | HN-LP, CC, SD | prose twin of `ui-fake-social-proof`: `\b(?:join|trusted by|loved by|used by) (?:over )?(?:[\d,.]+k?\+?|thousands|millions) of\b` |
| 17 | **Superlative/importance framing**: "matters because", "the single most", "every single" | "This matters because the queue grows daily." | GRAPH (132×, 112×), SS, SLHCK | `\bthe single most\b`, `\bthis matters because\b` (start of sentence only) |
| 18 | **Tradeoff-free claims**: without sacrificing/compromising/losing | "Ship without sacrificing quality." | GRAPH | `\bwithout (?:sacrificing|compromising)\b` |
| 19 | **Invented concept labels** (X paradox/trap/creep/divide) | "The supervision paradox shows up again." | TROPES, I77136, DAD | `\bthe [\w-]+ (?:paradox|trap|creep|divide|vacuum|inversion|tax)\b` (noisy; warn with cap) |
| 20 | **Aphorism "X is the language/currency of Y"** | "Speed is the language of trust." | HUM | `\bis the (?:language|currency|architecture|grammar) of\b` |
| 21 | **Generic CTA** "Get started", "Learn more" in UI copy | "Get started for free today." | CC, ANT-FD, magier.com via search | markup rule on `<a|button>` text = Get started/Learn more/Submit (warn) |
| 22 | **Middle-dot meta strings** in prose (`A · B · C`) | "Fast · Private · Open source" | ANT-FD, HN-UI, CC | ko has `ko-spaced-middot-list`; en/any version: `\S \· \S+ \· \S` |
| 23 | **"WORD — fragment" labels** | "FEATURES — what you get" | ANT-FD | `(?m)^[A-Z]{3,}\s+—\s+\w` |
| 24 | **Unicode → chains in prose** | "Input → Processing → Output" | TROPES ("Claude in particular loves the -> arrow") | `\w+ → \w+ → \w+` in prose |
| 25 | Stop-slop/humanizer leftovers not in our rules: "It turns out", "Make no mistake", "When it comes to", "In a world where", "Let's unpack", "lean into", "deep dive", "Think about it:", "And that's okay.", "Not always. Not perfectly.", "Two things worth flagging" | (all passed) | SS, HUM, HN-UI | add to `en-run-up` / `en-hollow-phrase` |
| 26 | **"from X to Y" false range** | "From idea to production in minutes." | TROPES only (1) | too noisy for regex; mention in SKILL.md |
| 27 | **Triplets**: "Fast, secure, and reliable" / "Built to scale, built to last, built for you" | (passed) | WP, SD, SS, HUM, KRISS | anaphora: `\bbuilt (?:to|for) [^,.]+, built (?:to|for) [^,.]+, (?:and )?built\b`; adjective tricolons need density gating (as SD does: ≥3 per page and ≥5/1000 words) |
| 28 | **Title Case headings** | — | WP, HUM, CARLY | markdown heading check: ≥4 capitalised content words in `^#{1,6} ` |

Not covered and **not recommended** as regex (weak or unsourced): "Built for teams who…", "Ship faster",
"Your X, your way", "Everything you need to…", "Say goodbye to" (one 2023 source), "Designed with care",
"crafted", "beautifully simple", "canvas", "heartbeat", "compass", "bridge between", "home for…", "flows/streams".
None turned up as a named tell in 2025–26 sources. If the maintainer wants them anyway, they fit better as
SKILL.md guidance ("a headline that could sit on any product's page") than as rules.

### 4c. Small rule observations from the probes

- `en-hype` misses British spellings ("Revolutionise", which GOD quotes verbatim) and bare "unlock".
- `ui-fake-social-proof` only runs on markup. Copy drafted in `.md` first (common for landing-page drafts) never
  sees it. Gap #16 above.
- `en-performed-candor` covers "honestly," but not the Claude forms "honest caveat" / "the honest take" (SLHCK, HN-LB).
- The em-dash signal is now model-dependent. WP calls the em dash historical after Sept 2026 and points to comma and
  period monotony as the replacement sign. ECON and GRAPH still show Claude at or above the human rate, so keeping
  `dash-overuse` density-gated is still justified for Claude output.
