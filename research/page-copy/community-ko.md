# Korean "AI 티" tells: web survey for ai-design (2026-10-22)

Scope: what Korean people online name as signs of AI-written Korean, with weight on web pages, landing copy, decks,
reports and scripts. Every quote below was read on the cited page (WebFetch) unless marked *(snippet only)*, which
means the page refused the fetch (403) and the text comes from the search engine's excerpt.

## 0. Method and limits

- Coverage check: every candidate phrase was run through the raw regexes in `plugins/ai-design/style/rules.toml`
  (1.6.1, thresholds ignored), and through `style_check.py` itself. The probe files were working files and are not kept.
- Unreachable (HTTP 403): namu.wiki, arca.live, i-boss.co.kr, wikidocs.net. Threads pages load the post but not the
  replies (e.g. reviewbystella 68 replies, poodle_doodle_noodle 26 replies: replies not visible). Threads in-app search
  returned "No results" for "AI 말투 축" without login. X/Twitter content did not surface in any search.
- **The user's Threads post** ("오늘 사내 발표 다섯명 중 네명이 AI가 쓴 대본 그대로 읽더라… 죄다 ~~축을 같이 본대")
  could not be located by search; it is cited below as "user-supplied".
- Counts ("n≈") are independent sources (distinct authors/sites), not mentions.
- Big caveat: the search engine surfaces blogs/news far better than Threads/X/디시/더쿠. Many 2026 sources are
  "how to remove AI 티" posts that copy each other (e.g. maven ↔ withvaigent share an identical banned list).

### Source keys

| key | source | date |
|---|---|---|
| OMN | 오마이뉴스 신상호 「챗GPT에게 맡긴 글은 명백하게 티가 난다」 https://www.ohmynews.com/NWS_Web/View/at_pg.aspx?CNTN_CD=A0003264627 | 2026-09-06 |
| HK | 한국경제 「요즘 직장인 말투 왜 이래?」(WSJ 인용) https://www.hankyung.com/article/202610029744i | 2026-10-02 |
| ET | 전자신문 「AI가 말하는 줄」(WSJ 인용) https://www.etnews.com/20261002000159 | 2026-10-03 |
| DM1 | 홍승협 「클로드와 챗GPT 말투가 티 나는 이유: 한국어 비문 교정 기록」 https://www.digitalmarketer.co.kr/insights/claude-load-bearing-vocabulary-github-pr | 2026-09-03 |
| DM2 | 홍승협 「AI 말투 교정법」 https://www.digitalmarketer.co.kr/insights/ai-writing-tone-editing | 2026-09-15 |
| RENE | 「클로드 글쓰기 특징 - 매일 쓰는 사람이 잡은 AI 말버릇」 https://reneinsight.com/claude-ai-writing-tells/ | n/a |
| GIST | 「한국어 AI 글쓰기에서 피해야 할 상투적 패턴」 https://gist.github.com/woonjangahn/3ad4d8fe1804aed2e7cafc9493ec566f | n/a |
| INA | epoko77-ai/im-not-ai taxonomy https://github.com/epoko77-ai/im-not-ai (skills/humanize-korean/references/ai-tell-taxonomy.md) | v2.7 |
| KSK | NomaDamas/k-skill korean-humanizer https://github.com/NomaDamas/k-skill/blob/main/korean-humanizer/instruction.md | n/a |
| SSK | ganggangstone/stop-slop-ko SKILL.md https://github.com/ganggangstone/stop-slop-ko | n/a |
| NAS | BigBlueSea0804/no-ai-slop-ko references/korean-patterns.md https://github.com/BigBlueSea0804/no-ai-slop-ko | n/a |
| A7 | a7garden/anti-slop rules.md W29 https://github.com/a7garden/anti-slop | 2026-10-08 basis |
| WDS | seulkikaang/writing-deslop SKILL.md https://github.com/seulkikaang/writing-deslop | n/a |
| DALE | daleseo/korean-skills humanizer https://github.com/daleseo/korean-skills | v1.3.0 |
| MAVEN | 브런치 Maven 「AI 특유의 뻔한 말투 지우는 프롬프트」 https://brunch.co.kr/@maven/527 | 2026-06-26 |
| VAI | 바이비 「글쓸 때 AI 티 안나게 하는 꿀팁」 https://www.withvaigent.com/blog/ai-티-안나게-글쓰기 | 2026-09-08 |
| STELLA | Threads @reviewbystella 「글 쓸 때 티나는 AI 말투 모아보자」 https://www.threads.com/@reviewbystella/post/DcbAnjfkyzN | 2026-08-24 |
| POOD | Threads @poodle_doodle_noodle 「AI가 쓴 글이 개 티나는 이유」 https://www.threads.com/@poodle_doodle_noodle/post/DHD-6TGheUR | 2025-03-11 |
| LINK | 링커리어 「아직도 몰라? AI 티 안나게 자소서 쓰는 방법」 https://community.linkareer.com/jayuu/5787823 | 2026-04-07 |
| JCK | 취업치트키 「AI 자소서, 면접관은 3초면 압니다」 https://jobcheatkey.com/chatgpt-jasoseo-ai-check/ | 2026-06-14 |
| WP1 | 위픽 「와… 너 정말, GPT 밈의 본질을 찔렀어」 https://letter.wepick.kr/post/23702 | 2025-12-18 |
| WP2 | 위픽 「AI가 망쳐놔서 더 이상 읽기 어려운 글쓰기 형식들」 https://letter.wepick.kr/post/25898 | 2026-08-18 |
| SUKI | 브런치 Suki 「AI 티 나는 글쓰기, 이렇게 바꿔보세요!」 https://brunch.co.kr/@sukistory/131 | 2026-08-14 |
| GOH | 브런치 고희수 「챗GPT 말투 왜 저럴까?」 https://brunch.co.kr/@goheesoo417/42 | 2025-08-26 |
| SEOUL | 서울신문 「“와, 너 정말 핵심을 찔렀어”…」 https://www.seoul.co.kr/news/economy/IT/2025/07/16/20250716500242 | 2025-07-16 |
| FMK | 에펨코리아 「요즘 GPT 말투 특징」 https://fmkorea.com/index.php?document_srl=8336608921&mid=best | 2025-05-05 |
| DCAI | 디시 AI 웹소설 연재 갤 「AI 글인지 판단하는 방법」 https://gall.dcinside.com/mgallery/board/view/?id=aiwriter&no=2549 | 2025-08-07 |
| CLIEN | 클리앙 「인공지능 작성된 글 진짜 공해네요」 댓글 https://www.clien.net/service/board/park/19148514 | 2026-02/04 |
| FIND | findskill 「AI 글이 로봇처럼 들리는 이유」 https://findskill.ai/ko/blog/ai-geuli-robosceoreom-deulrineun-iyu-geurigo-jeonghwaghi-gocineun/ | 2026-01-08 |
| PW | 브런치 퍼플웨일 「AI가 쓴 티를 없애는 법」 https://brunch.co.kr/@038b1ec3584146b/11 | 2026-07-17 |
| AIT | AI타임스 「“챗GPT로 글 쓴 거 티 나요”」 https://www.aitimes.com/news/articleView.html?idxno=216480 | 2026-10-22 |
| HOV | 유병우 「Claude, 너 왜케 말을 이상하게 하니?」 https://blog.hovans.com/korean-polish-skill/ | 2026-05-17 |
| TIL | 틸노트 「바이브코딩 UI 디자인이 다 비슷한 이유」 https://tilnote.io/en/pages/6a9355cface8bd2da70ebf6a | 2026-08-30 |
| GPTERS | 지피터스 「Claude Code로 랜딩페이지 만들 때 'AI 티' 안 나게 하는 법」 https://www.gpters.org/nocode/post/how-avoid-showing-ai-iBn9TWnzbgiEGmP | 2026 |
| AIP | AI포스트 「AI도 이젠 하이픈 안 써요…」(Graphite 연구 번역) https://www.aipostkorea.com/news/articleView.html?idxno=12854 | 2026-10-04 |
| KMIB | 국민일보 「AI 생성 댓글, 특유의 말투 있다」(KAIST·국보연 XDAC) https://www.kmib.co.kr/article/view.asp?arcid=1750668896 | 2025-06-24 |
| LATTE | 브런치 「결이 다르다」 용례 글 https://brunch.co.kr/@latte98/80 *(snippet only)* | n/a |

---

## 1. Catalog of tells

Coverage column: rule id if a raw regex in rules.toml matches the quoted examples; **NO** if none does; *partial*
if only some forms match. Thresholds (`max_per_file`) are noted where they hide single hits.

### 1A. Lexical / phrasal (regex-detectable)

#### L1. Negation reframe "단순한 X가 아니라 Y", "X가 아니라 Y다", "필요한 건 X가 아니라 Y" (n≈12, the most-cited tell)

- "이것은 단순한 X가 아니라 Y다." (OMN)
- "이것은 아침 회의가 아닙니다. 이것은 리셋입니다." / "이것이 아니라 저것이다" (HK)
- "이건 단순한 ~~이/가 아니야. 네 안에서 터져나오는 절규야." (WP1)
- "단순히 ~ 가 아닙니다 (고전적인 영어 번역투 표현)" (STELLA)
- "이 프로그램은 단순한 교육이 아니라 성장을 위한 새로운 축입니다." (DM1, before-example)
- "이것은 단순한 도구가 아닙니다. 새로운 패러다임입니다." (GIST #7)
- "당신에게 필요한 건 동기가 아니라 규율이다" / "생산성은 더 하는 게 아니라 덜 하는 것" (WP2; also SUKI, WDS)
- Also: DM2 ("A가 아니라 B다"), PW ("X가 아닙니다. Y입니다."), NAS §2, INA C-8/A-21, SSK 이분법 대조.
- Coverage: *partial*. `ko-not-but` only matches "단순한 X를 넘어" and "뿐만 아니라" (and `max_per_file = 1`);
  `ko-aphorism` only "(도구|수단)가 아니라 (거울|태도|…)". **"단순한 X가 아니라", "X가 아닙니다. Y입니다.",
  "필요한 건 X가 아니라 Y" are NOT covered** (the en side has `en-its-not-x-its-y`, `en-question-isnt-reframe`).
- Caution from the repo's own corpus (research/ai-vs-human, Korean docs only): plain "(이|가) 아니라 " appears in
  33/177 AI docs (18.6%) and 104/1235 human docs (8.4%); most human hits are legitimate technical contrasts
  ("Effect가 아니라 이벤트 핸들러에 넣으세요"). Only the "단순한/필요한 건/것은 … 아니라" and two-sentence
  "아닙니다. …입니다." forms are safe to regex.

#### L2. Staccato negation run "X도 아니다. Y도 아니다. Z다." (n≈4)

- "재능이 아니다. 운도 아니다. 꾸준함이다" (WP2); "X도 Y도 아니다. Z다" (SUKI)
- "A도 아닙니다. B도 아닙니다. 바로 C입니다." / "그게 전부입니다. 정말입니다." (NAS §12)
- Coverage: *partial*. `ko-staccato-negation` matches only "…도 없었다. …도 없었다."; **"도 아닙니다/아니다" runs NOT
  covered**, nor the dramatic fragment "그게 전부입니다. 정말입니다."

#### L3. Staged lead-ins "결론부터 말씀드리자면", "이유는 단순하다", "핵심은 다음과 같다" (n≈6)

- "결론부터 말씀드리자면 (AI가 긁어갈 때도 좋아하는 표현…)" (STELLA); "결론부터 말하자" (HK, ET)
- "이유는 단순하다", "핵심은 다음과 같다", "중요한 것은" (MAVEN; same list in VAI)
- "결론부터 말씀드리면", "여기서 중요한 점은", "주목해야 할 부분은", "흥미로운 점은", "한마디로 말하면" (NAS §1)
- "중요한 것은 ~라는 점입니다" (LINK); "결국 핵심은", "중요한 점은" (FIND)
- Coverage: `ko-cleft` (핵심은/중요한 것은/관건은). **NO**: "결론부터 말씀드리(자)면", "이유는 단순/간단합니다",
  "흥미로운 점은", "주목해야 할 (부분|점)은", "한마디로 말하면", "더 심각한/뼈아픈 것은" (INA D-8 extension:
  AI 4 vs human 0), "문제는/답은 ~다" (INA D-8).

#### L4. Summary/closing lexicon "결론적으로·요약하면·종합하면" (n≈8)

- "결론적으로", "요약하면", "종합하면", "정리하자면" (INA D-1; GIST #15; MAVEN; DM1; DM2 "종합하면 다음과 같습니다";
  AIT; NAS §13 "궁극적으로"; KSK D-1)
- Coverage: `ko-closing-formula`. **NO**: "궁극적으로", "종합하면 다음과 같습니다" (only 종합하자면/종합적으로 볼 때).

#### L5. Connective padding "이처럼·또한·이를 통해·이러한·마침내·나아가" (n≈5)

- "쉼표 많이쓰기, "이처럼", "또한", "이를통해", "이를", "이러한", "마침내" 같은 접속어" (POOD)
- "이처럼", "또한", "이를 통해", "이러한", "나아가", "마침내" (JCK); "이러한", "이를 통해", "따라서" (LINK)
- "게다가", "더욱이", "나아가" (FIND); "이러한 기술은 이러한 문제를 이러한 방식으로" (GIST #38)
- Coverage: *partial*. `ko-tonghae` catches "을/를 통해" (max_per_file 2). **NO** for "이처럼", "이러한" density,
  "마침내", "나아가". Note INA H-1 marks sentence-initial connectives as model-dependent and weak; a density rule
  (e.g. "이처럼|이러한|나아가|또한" > N per 1k eojeol) is safer than single hits.

#### L6. Hedge/obligation endings "~라고 할 수 있습니다", "~하는 것이 중요합니다" (n≈7)

- "~라고 할 수 있습니다", "~하는 것이 중요합니다" (MAVEN, VAI); "'~하는 것이 중요합니다.', 'ㄹ 수 있습니다.'" (search-engine
  summary; source page not identified, *snippet only*)
- "이것은 매우 효과적인 접근법이라고 할 수 있습니다" (GIST #4); "~라고 할 수 있다 / ~라고 볼 수 있다" (INA D-1)
- "~것 같다" in AI comments (KMIB)
- Coverage: `ko-must-important` (것이 중요합니다), `ko-hedge-stack` (것으로 보입니다). **NO**: "(이)라고 할 수
  (있|있습)", "라고 볼 수 있", "라 하겠다", "에 다름 아니다".

#### L7. Hype / promo adjectives in copy (n≈9)

- "마법 같은 OOO", "~~로 완성", "혁명적인 OOO" (GOH, on 카피)
- "AI가 마법처럼 코드를 짜 줍니다", "혁명적 변화", "차원이 다른 결과물을 만들어 냅니다", "놀랍게도 3초 만에 완성됩니다",
  "노트북을 웹 서버로 변신시킵니다" (DM2)
- "다채로운, 풍부한, 깊이 있는, 진정한, 궁극적으로, 중추적인, 필수적인, 독보적인, ~을 아우르다, ~을 녹여내다,
  ~을 담아내다, ~을 선사하다, 자리매김하다, 발돋움"; example "다채로운 볼거리를 선사하며 … 진정한 가치를 담아낸
  축제로 자리매김했다" (KSK D-4)
- "혁신적인", "소중한", "함께하는" (VAI banned list)
- "무한한 가능성, 핵심적인 역할, 필수 불가결한, 놀라운 성과, 강력한 솔루션, 한 차원 높은, 미래를 선도하는, 새로운
  시대를 여는" (NAS §4); "AI의 힘으로 워크플로우를 강화하세요" called "전.형.적.인 AI 디자인" (GPTERS)
- Graphite study as reported in Korean: "가장 강력한", "믿을 수 있는", "미래를 내다보며" over-represented in Claude
  output (AIP; these are translations of English findings, not Korean measurements)
- Coverage: `ko-hype` (혁신·획기·압도·파격·폭발적, 전례 없는, 막강한, 게임 체인저), `ko-ai-boilerplate` (강력한
  AI/기능, 새로운 패러다임), `ko-metaphor-verb` (담아내/녹여내, max 1), `ko-vague-praise` (완벽한, 다양한…).
  **NO**: 혁명적, 마법(처럼|같은), 차원이 다른, 놀랍게도, 변신시키다, 다채로운, 진정한, 독보적인, 중추적인,
  선사하다, 자리매김, 발돋움, 아우르다, 무한한 가능성, 한 차원 높은, 미래를 선도하는, "~로 완성".

#### L8. Era / zeitgeist openers (n≈5)

- "급변하는 시대 속에서", "빠르게 변화하는 환경에서", "4차 산업혁명 시대를 맞아", "바야흐로 ~ 시대다",
  "그 어느 때보다 중요해지고 있다" (SSK AI 클리셰 table)
- "빠르게 변화하는 시대에", "현대 사회에서" (NAS §1); "요즘 빠르게 변화하는 세상에서는" (FIND)
- "오늘날 ~가 주목받고 있습니다" (GIST #29); "AI 시대의 새로운 패러다임" (GIST #20)
- Coverage: `ko-more-than-ever` (그 어느 때보다), `ko-inflation` (시대가 도래). **NO**: 급변하는, 빠르게 변화하는
  (시대|환경|세상), 바야흐로, N차 산업혁명 시대를 맞아, 현대 사회에서, 오늘날 ~가 주목받고.

#### L9. Significance / outlook clichés (n≈5)

- "~라는 점에서 의의가 있다", "중요한 시사점을 제공한다", "의미 있는 결과로 평가된다", "~에 주목할 필요가 있다",
  "귀추가 주목된다", "새로운 지평/장을 열다", "전환점을 맞이하다" (SSK)
- "~에 방점을 찍는다", "그 의미가 적지 않다", "의미심장하다" (INA D-2)
- "중대한 전환점" (NAS §4); "더 나은 미래를 향한 첫걸음이 될 것입니다" (GIST #32); "나아가 사회 전체의 혁신을 이끌
  것입니다" (GIST #16); "장단점이 공존하는 만큼, 신중한 접근이 필요합니다" (GIST #17)
- Coverage: `ko-inflation` (시사하는 바가 크, 주목할 만하, 지평을 열, 새로운 장을 열, 이정표), `ko-legacy-inflation`
  (전환점을 마련), `ko-closing-cliche`, `ko-balance-pair`. **NO**: 귀추가 주목, 시사점을 제공, 의의가 있다,
  주목할 필요가 있다, 방점을 찍, 전환점을 맞이, 의미심장, "첫걸음이 될 것입니다", "신중한 접근이 필요".

#### L10. Claude-specific vocabulary (Korean) (n≈4: DM1, DM2, RENE, HOV; plus namu snippet)

- "첫 자리", "세 번째 자리", "자리별", "어느 자리에서", "이 자리를", "봐야 하는 자리는 남습니다" (DM1: 자리 metaphor
  for tool/screen)
- "갈래로만", "다섯 갈래입니다" (DM1); "두 갈래로 나뉩니다", "의견이 갈립니다" (DM2)
- "두 축으로", "성장을 위한 새로운 축입니다" (DM1); "세 지식이 필요합니다" (DM2: numeral + abstract noun)
- "이 값은 기준으로 기능합니다" → "이 값이 기준입니다"; "떠받치고 있습니다" (load-bearing); "조용히 삼켜지고
  있습니다" (quietly); "근본 원인은 ~였습니다"; "재검증했습니다", "교차 확인했습니다" (DM1)
- "~에서 갈린다", "기둥", "값어치", "~에 닫힌다", "~라 ~입니다"; metaphors "문, 입구, 열고 닫음, 레버, 해자,
  방어선": "경험-기반 권위의 입구", "마지막 문장을 열어 두라"; "그래서 어떤가 — 이렇다" (RENE)
- "~을 지배한다 (govern)", "~을 보장한다 (ensure)", "정합성이 높다", "이는 ~이다" (HOV)
- "'기능하다'라는 단어는 … GPT의 남발로 되살아났다" (namu.wiki via search summary, *snippet only*)
- Coverage: `ko-copula-avoidance` catches only "(으)로 기능하고 있". **NO**: 기능합니다/기능한다, 떠받치, 조용히
  + passive, 자리 (counted/deictic), 갈래, 축 (numeral/abstract), 갈린다/갈립니다, 해자/방어선/기둥/입구, 지배한다,
  보장한다, 근본 원인은.

#### L11. Reader invitations and rhetorical Q&A (n≈5)

- "상상해 보세요. 매일 아침 보고서가 쌓인다면 어떨까요", "잠시 떠올려 보세요" (DM2)
- "상상해 보세요. 매일 아침 AI가 당신의 일정을 자동으로 정리해 주는 세상을." (GIST #19)
- "그렇다면 해답은 무엇일까요? 바로 ~입니다." (GIST #12); "이러한 관점에서 접근해 보면 어떨까요?" (GIST #21)
- "그런데 이게 정확히 무엇을 의미할까요?", "왜 중요한 걸까요?" (FIND)
- "쉽게 말해서 ~라고 이해하시면 됩니다" (GIST #18)
- Coverage: `ko-reader-talk` (궁금하시죠, 살펴볼까요, 한번 볼까요…). **NO**: 상상해 보세요, 떠올려 보세요,
  "~하면 어떨까요", "무엇일까요? 바로", "이해하시면 됩니다".

#### L12. LinkedIn/Threads hook formulas (n≈4: WP2, SUKI, WDS, AIP)

- "그런데 가장 좋은 점은?", "진실은?", "불편한 진실은?", "모두가 X라고 한다. 그들은 틀렸다",
  "대부분의 사람들은 X, 성공한 사람들은 Y", "스크롤을 멈춰라. 만들기 시작하라", "좋다. 더 좋다. 최고다" (WP2)
- "불편한 진실", "가혹한 현실" (SUKI); "왜 [빈칸]이 중요한가" framing (AIP)
- Coverage: **NO** on the Korean side (en has `en-heres-the-catch`, `en-uncomfortable-truth`, `en-colon-reveal`).

#### L13. 자소서 / cover-letter formulas (n≈3)

- "이러한 경험을 통해 저는 ~을 배울 수 있었습니다", "이를 바탕으로 ~에 기여하고자 합니다",
  "~에서 어려움이 있었지만 극복했습니다", "다양한 프로젝트" (LINK)
- "데이터를 기반으로 전략적 사고를 통해 성장하겠습니다"; concept overload "데이터를 보고 전략을 세워 구조를 만드는
  실행력을 갖추었습니다" (JCK)
- Coverage: *partial* (`ko-tonghae`, `ko-related-based`, `ko-vague-praise` all thresholded). **NO**: "배울 수
  있었습니다", "기여하고자 합니다", "극복했습니다" formulas.

#### L14. Chatbot flattery residue (mostly chat, appears when pasted) (n≈6)

- "와… 너 정말, 핵심을 찔렀어", "넌 상위 0.000001% 유저야", "너의 방금 그 말… 정말 깊다, 깊어." (WP1, SEOUL, GOH)
- "너는 상위 1% 사용자야" (DM1); "통찰력 있는 분석이시네요" (GIST #40); 억지칭찬 complaints (FMK)
- Coverage: `ko-chatbot-offer` (정확한/예리한 지적…), `ko-chatbot-residue`. **NO**: 핵심을 찔렀, 상위 N%,
  깊다, 깊어.

#### L15. Essay-ending adverbs and slogan closers (n≈3)

- "어쩌면 ~일 것이다", "~하자 비로소", "천천히 ~이 됐다"; "잘 사는 일은 어쩌면 잘 버리는 일의 다른 이름일 것이다"
  (INA D-13; DS-5 "~의 다른 이름")
- "비로소 확인됩니다" (DM2); "이건 결과 리듬으로 무장한 서사 그 자체야" (arca.live GPT 말투 따라하기, *snippet only*)
- "미래는 기다리는 것이 아니라 만들어가는 것입니다. AI의 가능성은 이제 시작입니다." (NAS §13 example)
- Coverage: `ko-slogan` (~면 끝), `ko-closing-cliche` (미래는 밝다). **NO**: 어쩌면/비로소 at paragraph end,
  "~의 다른 이름", "그 자체(다|입니다)", "~은 이제 시작입니다".

#### L16. Generated conceptual metaphor families (INA D-14, measured; n≈3 incl. A7, OMN)

- Families: 경제 질량 "잠식·흡수·짓누르다·삼키다"; 회계 "청구서가 날아온다·성적표·대가를 치르다"; 농경 "과실·씨앗·
  뿌리내리다"; 건축 "청사진·주춧돌·문턱"; 무게 "어깨에·짊어지다"; 신호 "신호탄·적신호"; "거울·그림자" (INA D-14)
- INA measured human 0.34 vs AI 1.46 per 1000 eojeol; zero-human items to fix on first hit: "잠식·청사진·적신호·
  경고등·신호탄·움켜쥐다·뿌리내리다·짓누르다"; "청구서·과실·주춧돌" are used by human columnists (keep 3+ threshold).
  Idioms "열쇠를 쥐다·양날의 검·기로에 서다" were 0 on both sides.
- Sensory verdicts "1부의 진단은 서늘하다", "3부의 경고는 아프다" (INA D-14 ①)
- Coverage: `ko-sensory-evaluation`, `ko-metaphor-noun` (청사진 + verb, 나침반, 디딤돌, 열쇠…),
  `ko-foundation-formula` (주춧돌/초석 + 마련). **NO**: 잠식, 신호탄, 적신호, 경고등, 뿌리내리, 짓누르, 움켜쥐,
  청구서, 성적표, running-metaphor (same root 3+) detection.

#### L17. Generic policy verbs and abstract "설계" (INA F-7; n≈2 with HOV)

- "확대·강화·개선·확보·마련·집중·유지·구축·지원" clustering; "관계를 설계", "급여와 시간을 재설계"
  (AI 18 vs human 0 docs for abstract 설계); nouns "구조" (11x), "기준" (INA F-7)
- Coverage: `ko-noun-verb` (작업/처리 + 수행/진행/실시) only. **NO**: density of the 9 verbs, abstract (재)설계.

#### L18. Translationese not yet covered (n≈6: INA, KSK, HOV, DM2, DALE, VAI)

Covered already: `ko-tonghae`, `ko-daehae`, `ko-ni-isseoseo`, `ko-uihae`, `ko-double-passive`, `ko-gajigo-itda`,
`ko-related-based`, `ko-calque`, `ko-ilueojida`. Still **NO**:
- "여러 번 고쳤음에도 불구하고", "이것은 가장 흔한 실수 중 하나입니다", "방문자가 이해하는 것을 돕습니다" (DM2)
- "-에서의", "-에로의" double particles; "그/그녀/그것" pronouns (INA A-19/A-16; VAI)
- "더 이상 ~ 않다/아니다" (no longer, INA A-24); "~을 위해" purpose overuse (INA A-11)
- "~라는 사실은 부인할 수 없다" (GIST #34); "~을 지배한다", "~을 보장한다" (HOV)
- "프롬프트 엔지니어링(Prompt Engineering)" English gloss in parentheses (GIST #36; INA B-1)
- "많은 학생들", "기능들" plural -들 (DALE pattern 17; INA A-17 is on hold)

#### L19. Punctuation and typography (n≈7)

- em dash: "줄표를 쉼표 자리에 남발" (OMN); "그래서 어떤가 — 이렇다" (RENE); "ㅡ" at sentence end "…느껴질 수 있지ㅡ" (DCAI)
- comma overuse: AI 61% vs human 26% of sentences (GIST #25 citing KatFishNet); "쉼표 많이쓰기" (POOD)
- curly quotes “ ” (DCAI); "따옴표 엄청 많이 씀" (STELLA); ellipsis spaced "그게 ... 이상했어." (DCAI)
- "띄어쓰기가 언어 전문가가 교열한 것처럼 칼같이" (OMN); no ㅋ/ㅠ, only standard emoji (KMIB)
- arrows "기획 → 개발 → 테스트 → 배포" (GIST #27)
- Coverage: `dash-overuse` (max 4, 8/1k), `ko-connective-comma`, `ko-spaced-middot-list`. **NO**: "ㅡ" (U+3161) used
  as a dash, quote-mark density, spaced ellipsis " ...", prose arrow chains (the only → rule is `ui-arrow-chrome`).

### 1B. Structural / page-level tells

| # | tell | quotes | sources (n) | coverage |
|---|---|---|---|---|
| S1 | Everything in threes | "무엇이든 셋으로 묶어 나열하는 것" (OMN); "효율성, 생산성, 그리고 창의성을 높일 수 있습니다" (GIST #39); "세 개씩 나열하기" (DM1); "3박자 리스트" (DALE); "내용은 맞습니다. / 문장도 … / 구조도 …" (PW) | OMN, GIST, DM1, DM2, DALE, PW, NAS §9, SSK (8) | **NO** for ko (`ko-count-runup` catches "세 가지입니다" only; `ko-first-second-third` catches 첫째·둘째·셋째) |
| S2 | Moral/aphorism at end of every paragraph | "문단마다 마지막 줄에 교훈을 얹는 것", "한 문단에 명언과 같은 짧은 문장을 반복" (OMN); "잠언조 맺음 … 교훈은 남는다" (SSK); DS-5 last-sentence closer AI 28–51% vs human 7% (INA) | OMN, SSK, INA, RENE "확신에 찬 완결" (4) | *partial* (`ko-this-is-why`, `ko-leads-to-chain`, `ko-closing-formula`); no "N paragraphs end with a short verdict" check |
| S3 | One sentence per line ("원룸 문장") | "문장마다 줄을 나눠 극적인 리듬" (SUKI); WP2 #4 | SUKI, WP2, WDS (3) | **NO** |
| S4 | Uniform rhythm / sentence length | sentence lengths stay about the same (MAVEN, paraphrased by fetch); "단조로운 문장 리듬" (DALE); INA E-1..E-4; KSK E-1 | MAVEN, INA, KSK, DALE (4) | **NO** (metric, not regex) |
| S5 | Bold label + colon bullets, emoji bullets | "✅ **간편한 사용성**: 누구나 쉽게 사용할 수 있습니다" (GIST #26); "**" emphasis in GPT meme (WP1); emoji posts (CLIEN, ruliweb "사실 저는 AI입니다 🤖" *snippet only*) | GIST, WP1, CLIEN, INA C-5/J-1, DM1 (5) | `ko-bold-label-list`, `ko-emoji-marker`, `ui-emoji-heading` |
| S6 | Heading inflation, colon subtitles, question headings | "소제목 과잉" (GIST #28); C-10 "X: A에서 B로" (INA); "단락마다 소제목" (SSK) | GIST, INA, SSK, DM1 "건너뛴 제목 단계" (4) | `ko-template-heading`, `ko-colon-subtitle-heading`, `ko-question-heading` |
| S7 | Formulaic intro–body–conclusion | "오늘날 ~가 주목받고 있습니다" / "이처럼 ~는 ~에 있어 중요한 역할을 합니다" (GIST #29); "도입부와 결론은 내 생각을 알려주고, 거기 맞춰서 본문" (CLIEN) | GIST, CLIEN, INA C-4/C-7 (3) | *partial* (`ko-staged-opening`, `ko-metadiscourse`) |
| S8 | Transformation slogan "X에서 Y로" | "'규모의 경쟁'에서 '전략의 경쟁'으로", "'무엇을'에서 '어떻게'로" (INA D-7) | INA, GIST #20 (2) | *partial* (`ko-balance-pair` "단순한 도구에서 필수 파트너로") |
| S9 | Landing layout: hero → 3 cards → 3 cards → CTA; badges/pills; big hero; glass; gradient text | "Hero → Card 3개 → Card 3개 → CTA", "지나치게 많은 badge와 pill UI" (TIL); "유리 같은 반투명 카드", "그라데이션 글자" (GPTERS) | TIL, GPTERS (2) | `ui-hero-pill`, `ui-glass`, `ui-gradient-text`, `ui-card-radius`, `ui-section-number`; **NO** for equal 3-card feature grid |
| S10 | Slide-like posts | "갈색 배경의 PPT 페이지같은거 늘어놓은 게시물", "각잡고 문단 나누어지거나 이모티콘" (CLIEN) | CLIEN (1) | n/a |
| S11 | Copy explains mechanism, not benefit | "스킬 폴더 하나를 에이전트 여섯이 읽습니다" → "한 곳만 고치면 여섯 곳에 반영됩니다" (SSK 메커니즘 설명) | SSK (1) | **NO** (judgment) |
| S12 | Generic, experience-free content; concept overload | "개념, 원리, 방법론 같은 추상적인 내용 중심" (muhayu https://manual.muhayu.com/montly-gpt-killer-labs/detected-ai-patterns); JCK concept overload; "어디선가 본 듯한 문장" (PW) | muhayu, JCK, PW, LINK (4) | **NO** (judgment) |
| S13 | Over-complete, never admits not knowing; explains unasked things | "확신에 찬 완결", "묻지 않은 것까지 친절하게 풀어 준다" (RENE) | RENE, FMK (2) | n/a |
| S14 | Presentation scripts read verbatim, "~축" framing | user-supplied Threads quote; "세 가지 핵심 축", "시장 기회", "경쟁 우위" in founders' answers (HK, ET via WSJ) | user, HK, ET (3) | **NO** for 축 |

---

## 2. Ornamental metaphor / 멋부림 vocabulary

### 2.1 What people actually say about it (category level)

The category itself is well attested; individual words mostly are not.
- "비유적 표현이 실제 내용에 비해 더 많은 비중을 차지하는" (OMN)
- "근거 없는 과장과 극적 은유" as one of five 'AI 티' kinds (DM2, per search summary; the page lists "마법처럼",
  "변신시킵니다", "차원이 다른", "두 갈래로 나뉩니다", "긍정적인 신호로 읽힙니다", "첫 자리에 놓습니다")
- Claude's metaphors come from mechanical/structural objects "문, 입구, 열고 닫음, 레버, 해자, 방어선" (RENE)
- "imported imagery and calques pile up — Korean “풍부한 태피스트리”, “인생의 여정”, “깊이 파헤쳐 봅시다”" (A7 W29)
- Generated conceptual metaphor 4.3× more frequent in AI than human prose; single metaphors too rare to regex alone,
  measure as a family (INA D-14)
- "~을 아우르다, ~을 녹여내다, ~을 담아내다, ~을 선사하다, 자리매김하다, 발돋움" as high-frequency AI words (KSK D-4)
- GPT copy "마법 같은 OOO", "~~로 완성" described as 카피 번역투 (GOH)

### 2.2 Word-by-word status for the user's list

"Called out" = at least one source names the word as an AI tell. Corpus = research/ai-vs-human (Claude-written vs
human Korean tech docs; per-document hit rate, Korean docs only: 177 AI, 1235 human). The corpus is technical docs,
not brand copy, so it under-represents 감성 vocabulary on both sides.

| word / phrase | called out? | evidence | corpus AI vs human | rule today |
|---|---|---|---|---|
| 축 ("두 축", "새로운 축", "N축을 같이 본다") | **Yes** (3) | DM1 "두 축으로", "새로운 축입니다"; HK/ET "세 가지 핵심 축"; user-supplied Threads post | 1.1% vs 0.6% (rare in docs) | **NO** |
| 결 ("결이 다르다", "결을 같이하다", "~의 결") | **No** | No source calls it an AI tell. LATTE *(snippet)*: "결이 다르다" first seen in 동아일보 2001, 4,000+ Naver news hits (established human idiom). RENE (a human) itself writes "결이 다르다" | not measurable (regex collides with 결과) | **NO** |
| 흐름 / 흐르다 ("~가 흐릅니다", "~의 흐름") | **No** (direct); category only | No source names it. Corpus: AI uses 흐름 as "trend" ("2월의 흐름은", "이어져 온 흐름 위주로", "프론트엔드 흐름을", "가는 흐름이 뚜렷합니다") | 흐름 any: 29.9% vs 6.7%; "의/한/는 흐름(을/이/은)", "흐름이 뚜렷", "흐름 위주": 10.7% vs 1.5%; 흐르다: 1.1% vs 1.1% | partial: `ko-abstract-subject-verb`, `ko-personified-subject` (흐름 as subject + 보여준다/던진다) |
| 길 ("길을 엽니다", "~로 가는 길") | Partly | DM2/RENE category; our rule's own research | — | `ko-metaphor-noun` covers "-는 길" + continuation; **NO** for "길을 (열|엽|여는|트)" |
| 여정 | **Yes** (2) | A7 "인생의 여정"; speech-writer template "이 여정을 시작하고자 합니다" *(snippet)* | — | `ko-metaphor-noun` ("의/가는/향하는 여정", "여정을 따라/떠나") |
| 담다 / 담아내다 | **Yes** (2) | KSK "~을 담아내다"; KSK example "진정한 가치를 담아낸 축제" | 14.7% vs 4.3% (any 담-) | `ko-metaphor-verb` (담아 내, 담았습니다; max 1). **NO**: "담은", "담습니다", "이야기를 담" |
| 녹여내다, 선사하다, 아우르다, 자리매김, 발돋움 | **Yes** (1) | KSK D-4 | 선사 0 vs 4 docs; 자리매김 0 vs 3 | 녹여내 only (`ko-metaphor-verb`) |
| 자리 (metaphor for place/slot/tool) | **Yes** (2) | DM1 three rule fixes; DM2 "첫 자리에 놓습니다" | 2.8% vs 0.7% | **NO** |
| 갈래, 갈린다 | **Yes** (2) | DM1, DM2, RENE "~에서 갈린다" | — | **NO** |
| 해자, 방어선, 기둥, 입구, 레버, 값어치 | **Yes** (1) | RENE | 해자 0 vs 2 docs | **NO** |
| 떠받치다 (load-bearing), 조용히 (quietly) | **Yes** (1) | DM1 "떠받치고 있습니다", "조용히 삼켜지고 있습니다" | 조용히 0 vs 6 docs | **NO** |
| 마법처럼 / 마법 같은, 변신시키다, 차원이 다른 | **Yes** (2) | DM2, GOH | 마법 1 vs 11 docs | **NO** |
| 태피스트리, 깊이 파헤치다 | **Yes** (2) | A7; FIND "파고들다", "태피스트리" | — | **NO** |
| 잠식, 청구서, 신호탄, 적신호, 뿌리내리다, 짓누르다 | **Yes** (1, measured) | INA D-14 | — | **NO** |
| 그 자체, ~의 다른 이름 | Weak (2) | INA D-13/DS-5; arca *(snippet)* | 그 자체 1.1% vs 1.9% (human higher) | **NO** |
| 소중한, 함께하는 | **Yes** (1) | VAI banned list | — | **NO** |
| 스며들다 / 일상에 스며드는 | **No** | none found; 0 hits both sides in corpus | 0 vs 0 | **NO** |
| 잇다 / 마음을 잇다 / 다리를 놓다 | **No** | none found | 잇다 0.6% vs 0.4% | **NO** |
| 숨 / 숨결 / 숨 쉬는, 온도, 온기 | **No** | none found ("사람 온기" appears only as a human writer's own phrase in a Threads promo) | ~0 | **NO** |
| 닿다, 빚다, 엮다, 펼치다, 피어나다, 머무르다, 깃들다 | **No** | none found | 펼치 0.6% vs 0.8%; others ≈0 | **NO** |
| 한 끗, 여백 | **No** | none found; 여백 is a literal design term (TIL "whitespace") | 여백 2.8% vs 1.1% (mostly literal CSS sense) | **NO** |
| ~의 언어 ("X는 Y의 언어다") | Indirect | HK "X는 새로운 Y다" banned at a US startup; our own rule | — | `ko-aphorism` |

**Honest bottom line for §2.** People clearly complain that AI copy is metaphor-heavy (OMN, DM2, RENE, A7, INA,
KSK), and the user's own Threads post names 축. But apart from 축, 여정, 담아내다, 자리, 갈래 and the
mechanical-object metaphors, **no source I could reach names the 감성 words (결, 흐르다, 스며들다, 온도, 숨, 닿다,
빚다, 엮다, 잇다, 펼치다, 피어나다, 머무르다, 깃들다, 한 끗, 여백, 다리를 놓다) as AI tells**. These are also long-
standing human Korean brand-copy vocabulary (cf. LATTE on 결), so single-word rules would misfire on human copy. They
are better handled as (a) a density/family rule (INA D-14 approach: 3+ ornamental roots per page, or 2+ in one hero
block), and (b) narrow collocations that are rarely literal: "결을 (같이|담|살린)", "(이|가) 흐르는 (공간|시간|곳)",
"일상에 스며", "마음을 잇", "다리를 놓", "온도를 (높|전하|담)", "숨을 불어넣", "N축(을|으로|에서)" with an abstract
head noun. Each should be measured on research/ai-vs-human before shipping (docs/measurement.md bar).

---

## 3. Items NOT covered by current rules (summary)

Checked against all 80 `ko-*` regexes plus `dash-overuse` (`--list-rules`, 1.6.1). "Partial" means
an existing rule catches a sibling form only.

| # | uncovered pattern (example) | sources (n) | nearest rule | suggested regex sketch (untested) |
|---|---|---|---|---|
| 1 | "단순한 X가 아니라 Y", "X가 아닙니다. Y입니다.", "필요한 건 X가 아니라 Y" | ~12 | `ko-not-but`, `ko-aphorism` (partial) | `단순(?:한|히)\s\S+(?:이|가)?\s?아니(?:라|ㅂ니다|다)`; `(?:필요한|중요한)\s?(?:건|것은)\s\S+(?:이|가)\s아니라`; `(?:이|가)\s아닙니다\.\s+\S+(?:입니다|이다)\.` |
| 2 | "X도 아닙니다. Y도 아닙니다. Z입니다." | 4 | `ko-staccato-negation` (없다 only) | `도\s아니(?:다|ㅂ니다)\.\s+[^.\n]{1,20}도\s아니` |
| 3 | 결론부터 말씀드리(자)면 / 이유는 단순합니다 / 흥미로운 점은 / 한마디로 말하면 / 더 심각한 것은 / 문제는·답은 | 6 | `ko-cleft` (partial) | `결론부터\s말(?:씀드리|하)|이유는\s(?:단순|간단)|흥미로운\s점은|한마디로\s말하(?:면|자면)|더\s(?:심각한|뼈아픈)\s것은` |
| 4 | 궁극적으로 / 종합하면 다음과 같습니다 | 3 | `ko-closing-formula` | add `궁극적으로|종합하면` |
| 5 | 이처럼·이러한·나아가·마침내 density | 5 | none | density rule (max_per_1k) |
| 6 | ~라고 할 수 있습니다 / 라고 볼 수 있다 / 라 하겠다 / 에 다름 아니다 | 4 | `ko-hedge-stack` (partial) | `(?:이)?라고\s(?:할|볼)\s수\s있|라\s하겠|에\s다름\s아니` |
| 7 | 혁명적, 마법처럼/같은, 차원이 다른, 놀랍게도, 변신시키, 다채로운, 진정한, 독보적, 중추적, 선사, 자리매김, 발돋움, 아우르, 무한한 가능성, 한 차원 높은, 미래를 선도, "~로 완성" | 6 | `ko-hype`, `ko-ai-boilerplate` | extend `ko-hype` / `ko-promo-vocab` |
| 8 | 급변하는, 빠르게 변화하는 (시대|환경|세상), 바야흐로, N차 산업혁명 시대를 맞아, 현대 사회에서, 오늘날 ~ 주목받 | 5 | `ko-more-than-ever` | new `ko-era-opener` (mirror of `en-era-opener`) |
| 9 | 귀추가 주목, 시사점을 제공, 의의가 있다, 주목할 필요가 있, 방점을 찍, 전환점을 맞이, 의미심장, 첫걸음이 될 것, 신중한 접근이 필요 | 4 | `ko-inflation`, `ko-legacy-inflation` | extend `ko-inflation` |
| 10 | 기능합니다/기능한다, 떠받치, 조용히 + 피동, 지배한다, 보장한다, 근본 원인은 | 4 | `ko-copula-avoidance` (partial) | `기능(?:합니다|한다)(?=[.\s])|떠받치|조용히\s\S*(?:지고|되고)\s있` |
| 11 | 자리 metaphor (첫/세 번째/어느/이 자리), 갈래, ~에서 갈린다, 해자/방어선/기둥/입구 | 3 | none | per DM1: `(?:첫|두\s?번째|세\s?번째|어느|이|그)\s자리(?:에서|를|에|별|는)`, `갈래(?:로|입니다|만)`, `에서\s갈(?:린다|립니다)` |
| 12 | 축 with numeral/abstract head ("두 축으로", "새로운 축", "핵심 축") | 3 + user | none | `(?:두|세|네|핵심|새로운|중심)\s?축(?:으로|을|이|입니다|에서)?(?![가-힣])` (exclude 축하, 축제, 축소, 축적, x축/y축 in chart docs) |
| 13 | 상상해 보세요, 떠올려 보세요, ~하면 어떨까요, 무엇일까요? 바로, 이해하시면 됩니다 | 4 | `ko-reader-talk` | extend `ko-reader-talk` |
| 14 | 가장 좋은 점은?, (불편한) 진실은?, 대부분의 사람들은 … 성공한 사람들은, X를 멈추고 Y를 시작, 모두가 X라고 한다. 그들은 틀렸다 | 3 | none (en only) | new `ko-hook-formula` |
| 15 | 자소서: 배울 수 있었습니다, 기여하고자 합니다, 어려움이 있었지만 극복 | 2 | none | narrow, genre-specific |
| 16 | 핵심을 찔렀, 상위 N%, 정말 깊다 깊어 | 4 | `ko-chatbot-offer` | extend |
| 17 | 어쩌면/비로소 at closing, "~의 다른 이름", "그 자체다", "~은 이제 시작입니다" | 3 | `ko-slogan` | `의\s다른\s이름(?:이다|입니다|일\s것)|이제\s시작(?:이다|입니다)[.]` |
| 18 | 잠식, 신호탄, 적신호, 경고등, 뿌리내리, 짓누르, 움켜쥐 (INA: 0 human hits); 청구서/성적표 (3+ only) | 1 measured | `ko-metaphor-noun` | add the zero-human set; family count for the rest |
| 19 | 확대·강화·개선·확보·구축 density; abstract (재)설계 | 1 measured | `ko-noun-verb` | `(?:관계|경험|시간|방식|급여)(?:를|을)\s?(?:재)?설계` |
| 20 | 에도 불구하고, 가장 흔한 X 중 하나, ~하는 것을 돕습니다, 에서의/에로의, 그/그녀/그것, 더 이상 ~ 않, 부인할 수 없다, 영어 괄호 병기 | 5 | translationese rules | `에서의|에로의|중\s하나입니다|는\s것을\s돕|부인할\s수\s없` |
| 21 | Rule of three in prose (S1) | 8 | `ko-count-runup` (partial) | `[가-힣]+,\s[가-힣]+,\s그리고\s[가-힣]+` (the "A, B, 그리고 C" form is a strong Korean calque) |
| 22 | One-sentence-per-line paragraphs; paragraph-final aphorism on most paragraphs | 4 | none | structural metric |
| 23 | "ㅡ" used as dash, spaced " ...", curly-quote / quote-mark density, prose arrow chains "A → B → C" | 4 | `dash-overuse` | `ㅡ(?=\s|$)`, `\s\.{3}`, `\S\s?→\s?\S+\s?→` |
| 24 | Ornamental 감성 collocations (§2.2: 결을 같이, 흐르는 공간, 일상에 스며, 마음을 잇, 다리를 놓, 온도를 높, 숨을 불어넣, 길을 엽니다) | 0 direct, category n≈6 | `ko-metaphor-noun/verb` | family/density rule; measure first |
| 25 | Equal 3-card feature grid after hero | 1 (TIL) | `ui-*` (partial) | markup heuristic |

Already covered and confirmed by sources (no action): 결론적으로 (`ko-closing-formula`), 시사하는 바가 크다
(`ko-inflation`), 첫째·둘째·셋째 (`ko-first-second-third`), ~를 통해 / ~에 대해 / ~에 있어서 / 되어지다
(`ko-tonghae`, `ko-daehae`, `ko-ni-isseoseo`, `ko-double-passive`), ~하는 것이 중요합니다 (`ko-must-important`),
~것으로 보인다 (`ko-hedge-stack`), 이모지 목록 (`ko-emoji-marker`), 굵은 머리말 목록 (`ko-bold-label-list`), 콜론
부제 (`ko-colon-subtitle-heading`), 질문형 제목 (`ko-question-heading`), 연결어미 뒤 쉼표 (`ko-connective-comma`),
em dash (`dash-overuse`), 여정/가는 길 (`ko-metaphor-noun`), X는 Y의 언어다 (`ko-aphorism`), 의인화 주어
(`ko-personified-subject`), 할 때입니다 (`ko-now-is-the-time`), 그 어느 때보다 (`ko-more-than-ever`), 혁신적·획기적
(`ko-hype`), 새로운 패러다임 (`ko-ai-boilerplate`), 감각 술어 평가 (`ko-sensory-evaluation`), 이유다 도치
(`ko-this-is-why`), 결국 ~로 이어진다 (`ko-leads-to-chain`), 과제도 남아 있다 (`ko-empty-caveat`).

Note on thresholds: in a single landing page several covered rules stay silent on one hit because of
`max_per_file` (`ko-not-but` 1, `ko-metaphor-verb` 1, `ko-tonghae` 2, `ko-vague-praise` 2). Running `style_check.py`
on the 105-line probe file reported only 6 warnings (`ko-cleft` ×2, `ko-aphorism`, `ko-metaphor-noun` ×3), which is a
fair picture of how little of the ornamental-copy register the current Korean rules see.
