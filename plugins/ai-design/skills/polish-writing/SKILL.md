---
name: polish-writing
description: Remove the AI tone from Korean or English prose — product and developer-site copy, API docs, README, docs/, design docs, PR and issue text — and make it concrete, consistent and human. Use whenever you write or revise text people will read (pages, headlines, buttons, error messages, documentation), or when asked to 다듬어, 윤문, AI 티 빼기, polish, rewrite or edit copy.
paths:
  - "**/*.md"
  - "**/*.mdx"
  - "**/*.html"
  - "**/locales/**"
  - "**/i18n/**"
---

# Polish writing

The standard is `docs/standard.md` in [jungrok5/ai-design](https://github.com/jungrok5/ai-design/blob/main/docs/standard.md). A deterministic check runs after every edit
(`style_check.py`, rules in `style/rules.toml`); its findings come back to you as context. This skill covers what a
regex cannot judge.

## Hard limits (never break these while polishing)

- Do not add facts, numbers, names, quotes, customers or claims that are not in the source. If copy needs a number
  you do not have, leave `[숫자 필요]` / `[TODO: metric]` and say so.
- Leave code, commands, paths, identifiers, link targets, API names, units and quoted text exactly as they are.
- Keep the author's meaning and technical precision; cut words, not content. Keep the strength of each claim too: a
  hedge the source chose (`~로 보인다`, `may`) stays a hedge.

## Order of work

1. **Reader and job.** Who reads this and what must they do or decide after? Product page: what the product does
   for them. API docs: how to call it and what can go wrong. Internal doc: what to do and why.
2. **One speech level: 합니다체.** Docs, README, sites and design docs use 합니다체 in a written, documentary
   register: subject and verb explicit, no conversational endings (`~거예요`, `~잖아요`), no talking to the reader
   (`걱정하지 마세요`, `살펴볼까요`), no personifying work or tools (`일이 흘러가요`, `알아서 챙겨요` → name who does
   what). Lists and table cells are noun phrases (개조식). A product UI that decides on 해요체 turns `ko-haeyo` off in
   the project's `.style/rules.toml`. English: plain, sentence-case headings.
3. **Concrete over impressive.** Replace every adjective of praise with what it means: a number with a unit
   (`1 ms`, `64 KB`, `50,000원`), a condition, or an action. If you cannot, delete the adjective.
4. **Headlines say the user outcome; buttons say what happens next** (`API 키 발급`, `결제하기`, `Save changes`),
   never `시작하기`/`Submit` for everything. Errors say what happened and what to do, without apologizing.
5. **Cut the scaffolding:** run-ups (`이제 ~을 알아보겠습니다`, `변경은 세 가지입니다`, `Let's dive in`), advice voice
   (`~하시길 권합니다`, `~하는 편이 안전합니다`: state the condition and result instead), stock section headings
   (`체크리스트`, `핵심 포인트`: name what the section holds), summaries of what was just said
   (`결론적으로`, `In summary`), significance inflation (`시사하는 바가 크다`, `pivotal`), contrast theater
   (`단순한 X를 넘어`, `It's not X, it's Y`, `The question isn't X`), staged reveals (`Here's the catch`, `The result?`,
   `The best part:`), column clichés (`그 어느 때보다`, `가능성을 열어준다`, `과제도 남아 있다`, `~다는 분석이다`,
   `한 획을 그었다`, `앞으로의 행보가 기대된다`), unsourced authority (`전문가들은`, `일각에서는`), assistant residue
   (`Absolutely!`, `Feel free to reach out`, `~해 드릴까요?`), forced triplets, rhetorical questions, emoji markers,
   decorative bold and bold-label lists (`- **성능:** …`).
6. **Natural Korean.** Prefer verbs to nominalizations (`삭제 작업을 수행합니다` → `삭제합니다`), active voice with a real
   subject, and Korean particles over translationese (`~을 통해` → `~로`, `~에 있어서` → `~에서`, `~을 가지고 있다` →
   `~이 있다`). One term per concept; expand an abbreviation once on first use, e.g. `SSR(Server-Side Rendering)`.
7. **Read it aloud.** If a sentence carries two ideas, split it. If a paragraph's first sentence repeats the heading,
   delete it.

## Content form

Match the form to the content: explanation (why/what) as short paragraphs; actions as copyable command blocks or
numbered steps (with a copy button on pages); structure, flow or relations with three or more steps or two or more
actors as a diagram first, prose only for conditions and exceptions; comparisons and criteria as tables; numeric trends
as charts. Never write an action as an explanation, an explanation as a list of commands, or repeat one fact in prose,
table and diagram.

## Page-level tells (the style check sees sentences, not pages)

A page can pass every rule and still read as generated. Before you finish, read the whole page once for these:

- **Show, then describe.** When the text introduces a tool, paste its real output from an actual run (a command and
  what it printed). An example the reader can copy must be one you ran; if the result depends on a condition (a
  threshold, a flag), say so next to it.
- **Numbers carry their source.** Give a measurement its condition (`5 KB 파일 하나에 약 0.1초`, measured how). A count
  that changes with the code (rules, tests, files) appears once, and every document in the repo states the same value.
  When parts and a total appear together, the parts add up to the total. Do not call a made-up sample "real" or "typical".
- **Scope is the real precondition.** Replace `어느 프로젝트에나`, `모든`, `항상` with what is actually required. A tool
  page also says when not to use it and what it gets wrong.
- **Headings and endings state facts.** A section heading names what the section says (`배포 시간`, `배포 한 건당 21분
  단축`), not a question the reader did not ask (`얼마나 빨라졌나요?`, `왜 X인가`) unless the page is an FAQ. No slogan
  fragments (`명령 하나면 끝.`) and no closing nudge (`지금 설치해 보세요`); a page ends on its last fact or the one
  command to run. These came from comparing real Claude Code runs with and without this skill.
- **Say each point once.** A section does not open by restating its heading, and a later section repeats an earlier
  fact only to add something new. If a steps list or diagram shows a flow, the hero lead and the section text do not
  narrate the same flow again.
- **Break the stamp.** If three sections share one frame (number, heading, lead, body) or three sentences share one
  shape (`X는 A로, Y는 B로`), change the form of at least one; let the content set the number of items. Splitting a
  paired sentence into two matching short sentences is the same stamp. Do not run three or more short sentences in a
  row; join a cause and its result in one sentence. Lists of exactly three examples need a reason to be three.
- **Literal verbs, one subject.** Name what the thing does (`검사합니다`, `알립니다`, `막습니다`), not a metaphor
  (`걸러 냅니다`, `덜어 줍니다`). Name the real object, not a metaphor noun for a link or a flow
  (`샘플 페이지로 가는 길이 있습니다` → `샘플 페이지 링크가 있습니다`; `패킷을 받는 길`, `~의 여정`, `전체 지도`,
  `문을 열어 줍니다`, `열쇠`, `첫걸음`, `발판`, `디딤돌`, `나침반`, `청사진`). Keep one subject per sentence; do not
  start with the product and end with something else.

## Page copy: plain, not mannered

<!-- style-ignore-start -->
Asked for a site, a landing page or an About page, models switch into a brand-copy voice they do not use in chat:
metaphor and flourish stand in for the statement (Anthropic's guide calls this mannered prose: "When a literal phrase
is available, use it"). In 42 pages Claude Code wrote with no plugin, almost every promotional page had it; the docs
pages (API quick start, README) had little. Write page copy the way you would answer the same question in chat.

- **Say the mechanism.** `작은 쇼핑몰과 고객 사이를 가장 짧은 길로 잇습니다` → `오후 1시까지 들어온 주문을 그날 밤
  10시 전에 배송합니다`. `흘러가는 로그에서 필요한 것만` → `tail 중인 로그에서 조건에 맞는 줄만 골라 셉니다`.
  `밀이 숨 쉬는 시간만큼 결이 생깁니다` → `반죽을 4℃에서 14시간 발효한 뒤 굽습니다`. If the metaphor hid that you
  have no fact, leave `[숫자 필요]` instead of a softer metaphor.
- **Do not trade one image for another.** `흐름`, `결`, `온도`, `숨`, `닿다`, `잇다`, `스며들다`, `빚다`, `축`, `벽`,
  `문턱`, `출발선`, `연료`, `한 판`, `단단하게`, `흔들리지 않는`, `가르다`(원인을 가르는 로그 → 판별할 수 있는
  로그), `자리`(렉이 생기는 자리 → 렉이 발생할 수 있는 위치), English `journey`, `lens`, `load-bearing`,
  `earns its keep`: replacing one with another of the list is the same tell. Keep a word when it is the literal term
  (`빵의 결` as the crumb, `작업 흐름` for a workflow, `오시는 길` for directions, `x축`).
- **No aphorism, reframe or reveal.** Lines that sound like a motto carry no information: `기다리는 시간이 맛을
  만듭니다`, `루틴이 실력을 만듭니다`, `X는 목적이 아니라 수단입니다`, `리뷰는 코드를 평가하는 자리이지 사람을
  평가하는 자리가 아닙니다`, `정답보다 과정에 집중합니다`, `~하는 것. 그게 우리가 하는 일입니다`,
  `성장은 함께 하는 것이니까요`. State the rule or the fact behind it (`리뷰 댓글은 코드 줄에만 답니다`), or delete it.
- **Headlines are sentences.** No slogan fragments that end on a particle or adverb (`돈 관리는 더 쉽게.`,
  `5분 안에 첫 집계까지.`, `원하는 방법으로.`), no mirrored pairs (`속도만큼 신뢰를, 규모만큼 책임을`,
  `적는 수고는 줄이고, 재미는 더하고`), no division-of-labor slogans (`녹음만 하세요. 정리는 노트메이트가 합니다`),
  no counted promises in headings (`세 가지 약속`, `새로워진 세 가지`, `세 단계면 충분합니다`). Headline = what the
  reader gets, as a plain sentence (`회의 녹음을 올리면 회의록과 할 일 목록이 나옵니다`).
- **Do not overcorrect.** Plain is not stiff. Keep the page's register: an FAQ in 합니다체 still asks
  `참여할 수 있나요?`, not `참여할 수 있습니까?`; a neighborhood bakery can say `다 팔리면 일찍 닫습니다`.
  Remove the decoration, keep the warmth that comes from facts (hours, prices, names).
<!-- style-ignore-end -->
- **One name per concept, one concept per name.** Do not rotate synonyms (흔적 / AI 티, 결과 / 출력) to avoid
  repetition, and do not use one word for two actors (the AI that wrote the text and the AI that fixes it). An internal
  name (a theme or code name) gets a plain noun the first time.
- **Say who made it and why**, when the reader will ask: one honest paragraph from facts you have, never invented.
- **Paragraphs build on each other.** If two body paragraphs could swap places without breaking anything, the page is
  a list of points: connect them, or make it an honest list. Ask of each paragraph what it adds that the last one did not.
- **Steps are verbs.** Write what the reader does (`기호를 먼저 구한 뒤 문제를 하나씩 풉니다`), not a classification of it
  (`~부터 깨는 순서입니다`, `~는 구조라`, `~하는 쪽이 빠릅니다`).
- **Cutting must not starve a sentence.** After removing filler, check that no subject, object, particle or degree word
  went with it; a short sentence the reader cannot parse is worse than the padded one. Restore only what the text itself
  supports. These last three come from Aparnabuilds/humanizer, Aboudjem/humanizer-skill, teo713ko-gif/hangul-humanizer
  and amondnet/yoonmoon; the cluster rule and the self-check below from IsaacEryn/humanizer-ko and
  giudegio-ai/claude-skill-humanizer (all MIT).

## Output

When asked to polish existing text, judge by clusters: one dash, one `다양한` or one bold label is not a tell, and a
passage with no cluster stays as written (say so). Rewrite the rest, then ask once: what in this still reads as
generated, and did any fact, number or name enter that the source does not have? Fix those, then return the revised
text and at most 5 bullets naming the biggest changes. When writing new text, just write it to this standard. Fix
every `error` from the style check; for a `warning`, fix it or keep it on purpose. To quote a bad example on purpose, mark the line with `style-ignore`.

Sources and licenses: `THIRD_PARTY_NOTICES.md` in this plugin.
