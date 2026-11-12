# E08 — External sources and developer statements

Stream E08. Access date for all URLs: 2026-11-12. Upstream clone pinned at `main` =
`74330157cb601573ae4523a95bb9132822fc3918`. Abbreviation: UP = upstream clone at
`/tmp/claude-0/-home-user-photocraft-study/7ff807c1-b52f-5813-9884-82f19c193950/scratchpad/upstream/photocraft`.
Raw downloads (HN JSON, website HTML) kept in `.../scratchpad/work/E08/`.

Reliability classes: **P1** = developer-authored primary (repo docs, project website,
developer's own posts); **P2** = journalism quoting developers; **P3** = third-party
commentary/speculation. Third-party method claims are VERIFIED only as "source X claims Y".

Identity note: GitHub login `echelon` = Brandon Thomas, from `UP@74330157cb:contributors/people.toml:41-43`
(`[people.echelon]` with `real_name = "Brandon Thomas"`). The HN account `echelon` is the same person by
**INFERENCE**. The HN profile says only "HN contrarian.", but the account calls the storytold repos "my 100% adobe clean room
reimplementations" (HN 49922904) and posts ArtCraft hiring ads (HN 48750050). A Reddit account
`u/ai_art_is_art` is attributed to him by a third party (HN 49961646, user slopinthebag) and by an X
post (x.com/iamsupersocks/status/2107560346269401548). That link is UNVERIFIED.

---

## 1. Source register

| ID | Source | Author / outlet | Published | Class | Access result |
|---|---|---|---|---|---|
| S01 | UP `README.md` (HEAD + 89-commit history) | ArtCraft team (Brandon Thomas, others) | 2026-09-30 → | P1 | OK (git) |
| S02 | UP `ROADMAP.md`, `docs/roadmap.md`, `docs/target-app-parity.md` | Brandon Thomas (commit 939c8f2c70, 0c2d4bfd1a) | 2026-10-02 / 2026-10-10 | P1 | OK (git) |
| S03 | UP `AGENTS.md` (house rules + §6 Parallel agents) | Brandon Thomas; FredApps (house-rules copy 7d8648dfcb) | 2026-10-01 → 2026-11-06 | P1 | OK (git) |
| S04 | UP `docs/contributors.md`, `contributors/contributors.json` | project | 2026-10-10 snapshot | P1 | OK (git) |
| S05 | UP `ATTRIBUTION.md` translation-disclosure rows | contributors (e.g. tronicum) | 2026-11-06 | P1 | OK (git) |
| S06 | UP `book/src/**` | project | 2026-10-04 → | P1 | OK; no method statements |
| S07 | https://photocraft.org | ArtCraft | n/d | P1 | OK (curl); web-app landing page only |
| S08 | https://getartcraft.com/, /apps, /apps/photocraft, /news, /faq, /press-kit, /apps/craft-anything | ArtCraft | n/d | P1 | OK (curl); /blog, /about, /press, /wiki = 404 |
| S09 | HN comments by `echelon` (Algolia API) | Brandon Thomas (inferred) | 2026-10-01 → 2026-11-11 | P1 | OK (hn.algolia.com API) |
| S10 | HN threads 49958850 (180 pts), 49986072, 49981449, 49938443 | community | 2026-10-02 → 10-07 | P3 (+P1 replies) | OK (Algolia) |
| S11 | Reddit r/Adobe 1wvyxjd and cross-posts (r/SaaS, r/OpenAI, r/GeminiAI, r/aiwars, r/vibecoding, r/Bard) | u/ai_art_is_art (attributed) | ~2026-10-02 | P1 if attribution holds | **FAILED**: curl 403; WebFetch "unable to fetch from www.reddit.com". Known only through press/HN quotes |
| S12 | Phoronix "AI Makes Open-Source, Clean Room Implementations…" | Phoronix | 2026-10 | P2/P3 | **FAILED** (WebFetch 403). Headline only, via search |
| S13 | Engadget "AI software clones are coming…" | Steve Dent | 2026-11-01 | P2 | OK (WebFetch summary) |
| S14 | siliconreport.com "Developer uses Claude to reverse-engineer…" | Margaret Chen | 2026-11-01 | P2 | OK (WebFetch summary) |
| S15 | PHLEARN "ArtCraft: Photoshop Cloned by AI in Two Weeks" | Aaron Nace | 2026-10-15 | P2 | OK (WebFetch summary) |
| S16 | VICE "Everything We Know About the Free Adobe Clones…" | Luis Prada | 2026-10-09 | P2 | OK (WebFetch summary) |
| S17 | Gizmodo "Someone Vibe Coded a Free Knockoff…" | Mike Pearl | 2026-10-07 | P2 | OK (WebFetch summary) |
| S18 | OrcaRouter blog "Claude Opus 5.5 Built 7 Adobe Clones in Rust: Reality Check" | unnamed | 2026-10-07 | P3 | OK (WebFetch summary) |
| S19 | Shokunin Studio "Attack of the Vibe Coded Photoshop Clones" | Shokunin Studio (competing app developer) | 2026-10-09 (+updates 10-14, 11-11) | P3 | OK (WebFetch summary) |
| S20 | Peter Rex Substack "A Start Is Not a Finish" | Peter Rex | 2026-11-09 | P3 | OK (WebFetch summary) |
| S21 | InfoWorld video "About that AI-powered clone…" (Dev with Serdar ep. 278) | Serdar Yegulalp | 2026-10-15 | P3 | OK (WebFetch summary of page) |
| S22 | letsdatascience.com "ArtCraft Updates PhotoCraft…" | LDS Team | 2026-10-14 | P3 | OK (WebFetch summary) |
| S23 | aiweekly.co "PhotoCraft ships Rust Photoshop clone with MCP agent server" | Alexis Dufresne | 2026-10-07 | P3 | OK (WebFetch summary) |
| S24 | Fstoppers "Is it legal to clone Photoshop with AI" (from LegalEagle video) | Alex Cooke | 2026-10-31 | P3 | OK (WebFetch summary) |
| S25 | OMG! Ubuntu "ArtCraft free Photoshop AI clone" | Joey Sneddon | 2026-10 (upd. 10-15) | P2/P3 | OK (WebFetch summary) |
| S26 | XDA "I tried several vibe-coded Photoshop alternatives…" | Patrick Hearn | 2026-10-29 | P3 | OK (WebFetch summary) |
| S27 | Notebookcheck, AppleInsider, TweakTown, pasqualepillitteri.it (21619) | various | 2026-10 | P2/P3 | **FAILED** (403 / 403 / 403 / 502) |
| S28 | t3n.de, kunalganglani.com ("PhotoCraft: The Vibe-Coded Rust Photo Editor [2026]"), techaeris, pbxscience, levelup.gitconnected (member-only), alternativeto | various | n/d | — | **NOT RETRIEVED**: no t3n article found by search; kunalganglani gave 403 (Cloudflare) to both WebFetch and curl; techaeris link has no title; levelup is paywalled; others not fetched |
| S29 | https://github.com/storytold (org page) | GitHub/ArtCraft | — | P1 metadata | OK (WebFetch summary) |
| S30 | https://github.com/storytold/photocraft (repo page) | GitHub | — | P1 metadata | OK (WebFetch summary) |
| S31 | https://github.com/storytold/craft-contrib and `rfcs/0006-coding-agents.md` | ArtCraft maintainers (author not shown) | n/d | **P1** | OK (WebFetch summary + verbatim quotes on request) |
| S32 | https://github.com/storytold/photocraft/releases | github-actions | 2026-11-06 → 11-12 | P1 | OK (first 100k chars only) |
| S33 | https://github.com/storytold/photocraft/wiki, /discussions | GitHub | — | — | No wiki tab; Discussions 404 (not enabled) |
| S34 | Product Hunt "PhotoCraft"; HN 46614201; photocraftonline.org | unrelated makers | 2026-01 / 2026-10 | n/a | **Name collisions**: an unrelated iOS app by Deva Vinoth, and a third-party site. Excluded |

---

## 2. Evidence entries: in-repo developer statements (P1)

### E08-001 — The README has never described how PhotoCraft is developed (AI use, agents, models)
- Label: VERIFIED
- Source: `README.md` history on main (89 commits); commits a517477da8 (2026-09-30), 536a7346fb (2026-10-01)
- Quote/Data: `git log -S` hits for "Claude" (536a7346fb) are only the painter "Claude Monet" in image captions. "AI agent" and "agents" (a517477da8, 536a7346fb) appear only in the sense "drivable by agents". `-G'(Claude Code|codex|written with|built with|AI-generated|AI-assisted|agentic|LLM|coding agent|Anthropic|OpenAI|copilot|cursor|vibe)'` matches one commit, a96a621dee (FreeBSD platform lines), which is not about method.
- Method: `git log main -S<term> -- README.md` for Claude, Codex, "AI agent", vibe, "written by", Opus, LLM, Anthropic, "AI-assisted", "AI-written"; plus `-G` regex above.
- Notes: In the README, "agent" always means agents *using* the product ("Built for agents", `README.md:228-250`; "New contributors and AI agents: start with AGENTS.md", `README.md:276`), never agents *building* it. Credits read "Made by the ArtCraft team and community" (`README.md` footer). The ArtCraft site says "Built the hard way. Every Crafting App is written from scratch in Rust" (S08), and also says nothing about AI.

### E08-002 — The project's planning docs measure all effort in "Opus 5.5 agent wall-clock hours"
- Label: VERIFIED
- Source: `74330157cb:ROADMAP.md:14-16`; `74330157cb:docs/roadmap.md:20-21`; added in commit 939c8f2c70 (2026-10-10, Brandon Thomas, PR #2696)
- Quote/Data: "Hours are Opus 5.5 agent wall-clock hours for one agent working sequentially, calibrated from this repository's 1,004 merged PRs … About 80% of the work parallelizes."
- Method: `git log main -S"Opus 5.5 agent wall-clock"`
- Notes: This is the strongest P1 statement that the project plans its work as Claude Opus 5.5 agent labour.

### E08-003 — Developer doc: "the repository has sustained 10–20 concurrent agents"
- Label: VERIFIED (as a statement); the agent count itself is UNCORROBORATED here
- Source: `74330157cb:docs/target-app-parity.md:234-236`; commit 939c8f2c70 (2026-10-10)
- Quote/Data: "About 80% parallelizes: areas are independent crates and command modules, and the repository has sustained 10–20 concurrent agents. At ~12 agents, beta is roughly 100–150 wall-clock hours."
- Notes: This is the only developer statement about concurrency at repository level. The document gives no measurement method for "10–20". Lead for E-streams that measure concurrency (overlapping PR lifetimes, `Claude-Session` ids).

### E08-004 — Calibration statement: about 1,004 PRs in 10.5 days, median open-to-merge 3.4 h, 2–4 agent-hours per PR, 2,000–4,000 agent-hours in total
- Label: VERIFIED (statement); commit count partly CORROBORATED
- Source: `74330157cb:docs/target-app-parity.md:205-222`
- Quote/Data: "1,152 commits on `main` and 1,004 merged PRs in 10.5 days. Median PR open-to-merge time is 3.4 h (p75 6.4 h, p90 14.3 h …)… the ~1,000 PRs so far represent about **2,000–4,000 agent-hours**"
- Method/check: `git log main --since=2026-09-30 --until=2026-10-10T23:59 | wc -l` = 1380. The doc says 1,152. Its time cutoff is not stated, so the difference may be a cutoff difference. `contributors.json` snapshot head 9d3ba499ad (2026-10-10T23:09Z) records `commits: 1302`.
- Notes: The agent-hours figure is the developer's *derived estimate* (PRs × assumed hours), not a metered value. No token or dollar figure is given.

### E08-005 — The earliest effort estimate (2026-10-02): "8 parallel agents" in one session, and 95% parity in "25–40 wall-clock hours"
- Label: VERIFIED
- Source: commit 0c2d4bfd1a (2026-10-02, Brandon Thomas; trailer `Co-Authored-By: Claude Opus 4.8`), file `docs/parity-estimate.md`. Now kept at `74330157cb:docs/target-app-parity.md:322-343,350`
- Quote/Data: "This session landed ~70 menu items + major subsystems in a handful of wall-clock hours using 8 parallel agents, so wall-clock ≈ agent-hours ÷ 6." Also "~140–220 agent-hours ≈ 25–40 wall-clock hours" to 95%. Also "Wall-clock assumes 6–8 independent arcs in parallel with their own target dirs, as this session ran."
- Notes: This is the source of the widely repeated "8 parallel agents" figure (S18 and the search summary). Eight days later the estimate was replaced (E08-002): beta became 1,100–1,800 agent-hours and full parity 2,300–4,100. That is roughly a 10× upward revision, which the project made itself and kept "for the record". The commit that writes "Opus 5.5 effort" carries an **Opus 4.8** co-author trailer, a small inconsistency.

### E08-006 — Tasks reserved for humans ("Needs a human"), including an installed copy of Photoshop for checks
- Label: VERIFIED
- Source: `74330157cb:docs/target-app-parity.md:238-242`; also `:244-253` ("How to re-measure")
- Quote/Data: "Needs a human. Owner decisions on the AI backend (#41 …) and plug-in hosting …; Windows code-signing material; tablet hardware checks …; native-speaker review of every catalog; checking exports by opening them in Photoshop (the owner's machine has it installed)."
- Notes: Re-measurement reads files from the installed Photoshop: the `.kys` shortcuts file, `Info.plist` and the PiPL flags of its format plug-ins (`:247-250`). This is relevant to the clean-room debate (E08-020). It is inspection of shipped resource and metadata files, not decompilation, as far as the doc says.

### E08-007 — AGENTS.md documents a parallel-agent working practice
- Label: VERIFIED
- Source: `74330157cb:AGENTS.md:168-176` (section first added in 536a7346fb, 2026-10-01)
- Quote/Data: "Use your own target dir (`CARGO_TARGET_DIR=target/agent-<name>`) … edit only the files you own." Also "If someone else's in-progress edit breaks the build, wait and retry". Also "Sessions can end abruptly (crashes, context limits), so the dev log plus a green tree is how the next agent picks up."
- Notes: The practice is documented. It is corroborated by the early commit aa87012aab (2026-10-01): "Analysis, notes, proof views, workspaces (+ in-progress work of other agents)". The `log/devlog.md` is gitignored (`AGENTS.md:209`), so the agents' handoff log is **not public**.

### E08-008 — House rule 15, "No agent attribution" (added 2026-11-06)
- Label: VERIFIED
- Source: `74330157cb:AGENTS.md:20`; added by commit 7d8648dfcb (2026-11-06, FredApps, "Copy the shared house rules into AGENTS.md"); source given as `standards/house-rules-core.md` in `storytold/craft-contrib`
- Quote/Data: "**No agent attribution.** A pull request does not say an agent wrote it. A repository rule may not require that."
- Method/check: share of main commits with a `Co-Authored-By: Claude` trailer = 685/2160 (31.7%) for 2026-10-27..11-05 and 459/1669 (27.5%) since 2026-11-06 (python regex over `git log --format=%B`).
- Notes: The rule bans *PR text* attribution. It does not explicitly ban commit trailers. The rule means a lack of attribution after 2026-11-06 is weaker evidence of a human author. The same file says "`craftrules` is retired. Do not link to it." (`AGENTS.md:18`). The early commit 1d61b33c54 (2026-10-01) says "Release playbook now lives in craftrules", so a shared rules repo existed.

### E08-009 — Rule 1: "A person is accountable" for every agent
- Label: VERIFIED
- Source: `74330157cb:AGENTS.md:6,10,12`
- Quote/Data: "Whoever runs an agent answers for what it opens and for its review comments." Also "Review the diff before opening a pull request." Also "Report only what ran."
- Notes: This is a documented *norm* of human accountability. It conflicts with E08-016 (the founder's "no human review" remark, whose scope is ambiguous).

### E08-010 — The About ▸ Models tab credits AI models from Co-Authored-By trailers
- Label: VERIFIED
- Source: `74330157cb:docs/contributors.md:3-4`; `74330157cb:contributors/contributors.json` (`models` array, line 2468 →; snapshot head 9d3ba499ad, 2026-10-10)
- Quote/Data: snapshot model commit counts: anthropic/claude-opus/5.5 736; anthropic/claude 49; claude-opus/4.8 46; claude-fable/5.1 14; github/copilot 6; claude-mythos/5.1 4; claude-sonnet/5.5 3; openai/gpt/6 2; alibaba/qwen-flash/3.8 1; claude-haiku/4.5 1; anysphere/cursor 1; cognition/devin 1.
- Method: `python3 -I` json load of `contributors.json`
- Notes: AI credit is a *product feature*. The in-repo copy is stale ("the copy in the repository is not updated", `docs/contributors.md`). Release builds regenerate it. Trailer tallies across all of main (12,396 commits) differ widely, e.g. "Claude Opus 5.5" 3,565 + "(1M context)" 652 (`git log main --format='%(trailers:key=Co-Authored-By,valueonly)'`). See the E-trailer streams.

### E08-011 — Translation rows disclose machine translation, e.g. "@tronicum with Claude Code, AI-assisted (machine-translated)"
- Label: VERIFIED
- Source: commit 653a177e6f (2026-11-06, tronicum) `ATTRIBUTION.md` (later moved to craft-i18n by acc88b3203, 2026-11-08)
- Quote/Data: "@tronicum with Claude Code, AI-assisted (machine-translated); not yet reviewed by a native speaker"
- Notes: This is the only explicit "built with Claude Code" disclosure text found in the repo's prose docs. It covers translations only.

### E08-012 — The repository's first commit is literally named "one-shot", adding 42,241 lines
- Label: VERIFIED
- Source: commit 16941f7198 (2026-09-30 05:02 -0400, Brandon Thomas), the second commit after 386b0566d3 "init repo"
- Data: `git show --shortstat 16941f7198` gives "241 files changed, 42241 insertions(+)". All 19 commits before 2026-10-02T03:05Z are by Brandon Thomas, totalling 175,514 added lines. The first Claude trailer appears at 1f1ddb2a47 (2026-10-01 13:25).
- Notes: This matches the founder's "I just one-shotted Photoshop" (E08-013). How the 42k-line commit was produced is invisible: no trailer, no session link, and no pre-history is published.

---

## 3. Evidence entries: developer statements outside the repo (P1, HN)

All quotes come from the Algolia API (`https://hn.algolia.com/api/v1/items/<id>`), author `echelon`. They are full-text, not summaries.

### E08-013 — "I just one-shotted Photoshop. The whole thing." (HN 49928088, 2026-10-01T23:05Z)
- Label: VERIFIED (statement)
- Source: https://news.ycombinator.com/item?id=49928088 (thread "Ask HN: Who is hiring? (October 2026)")
- Quote: "Software is over. But for real. I just one-shotted Photoshop. The whole thing."
- Git: the history at that time is 19 commits including "one-shot" (E08-012). The "whole thing" claim is CONTRADICTED by the project's own later docs (alpha, ~45% ready, `ROADMAP.md:3`) and by 12,000+ later commits. Press widely repeats the quote (S16 VICE, S20, S24, critic comments on HN 49976461).

### E08-014 — "I'm currently using Opus 5.5 to create 100% pure-Rust … implementations of Adobe's entire suite" (HN 49934844, 2026-10-02)
- Label: VERIFIED (statement)
- Source: https://news.ycombinator.com/item?id=49934844
- Quote: "I'm currently using Opus 5.5 to create 100% pure-Rust, immediate mode rendering, open source implementations of Adobe's entire suite". Also "I got bit by the dark pattern 'cancellation fee' one too many times."
- Git: CORROBORATED. "Claude Opus 5.5" is the dominant trailer (E08-010), and 226 of Brandon Thomas's 301 main commits carry a Claude co-author trailer (regex count).

### E08-015 — Tooling: "vanilla Claude Code", "occasionally Codex", no hand-written code since February
- Label: VERIFIED (statements)
- Source: HN 50029182 (2026-10-10): "We're using vanilla Claude Code for ArtCraft apps [1], but we are especially careful not to touch Ghidra." HN 49977572 (2026-10-06): "Now it's Claude Code and ever so occasionally Codex. I never do work in IDEs by hand anymore. I stopped writing code entirely in February". HN 50325139 (2026-11-01): "Every time Anthropic limits what we can do, I start switching more of my process to open weights. Planning with Claude, implementation with Kimi."
- Git: "Claude Code" use is CORROBORATED. There are 304 main commits with a `Claude-Session:` trailer and 3 with "Generated with [Claude Code]". "Codex" appears in 15 co-author trailers. Kimi does not appear in any trailer surfaced by the trailer grep. **UNCORROBORATED**: the Kimi remark may not concern PhotoCraft.
- Notes: "vanilla" implies no custom orchestration harness. That is a developer claim with no detail.

### E08-016 — "100% AI software factory and no human review" (HN 50434834, 2026-11-10)
- Label: VERIFIED (statement); scope AMBIGUOUS
- Source: https://news.ycombinator.com/item?id=50434834 (story "A year after the 100% AI mandate…")
- Quote: "We're leaning in with 100% AI software factory and no human review. We're making lots of revenue too. The era of human always in the loop software is over."
- Notes: The comment does not name PhotoCraft. "making lots of revenue" points more to the commercial ArtCraft Studio than to the free Crafting Apps. It contradicts the documented norm "A person is accountable" (E08-009), and the repo shows CodeRabbit review badges (`README.md:29`). It must not be read as a description of PhotoCraft review practice without corroboration (lead: E-review streams).

### E08-017 — Clean-room statements: no decompilation, no Ghidra, no Adobe sources
- Label: VERIFIED (statements)
- Source: HN 50029110 (2026-10-10): "we explicitly do not use reverse engineering. We do not decompile binaries, we do everything 100% clean room … We cannot look at Adobe sources. Use of Ghidra is disallowed." Also P1 `README.md:257`: "implemented from public specs and observed behaviour only. No proprietary code, shaders or assets."
- Git: UNCORROBORATED by git. It cannot be proven from history. The repo does document inspecting installed-Photoshop resource files and comparing against Photoshop renders (E08-006, `README.md` "composite oracle compares our render with Photoshop's own merged image").

### E08-018 — Community-as-method: "Let the community token spend … diffuse into the products"
- Label: VERIFIED (statements)
- Source: HN 49976861 (2026-10-06): "Let the community token spend have time to diffuse into the products. This effort needs a community to climb the quality and parity gradients." HN 49962334 (2026-10-05): "I needed to seed a community that could help contribute bug reports and PRs." HN 49959605 (2026-10-05): "I'll need lots of help. (Anyone want to join me? I'll pay stipends and bug bounties.)" HN 50333851 (2026-11-02), answering "can't be done by LLM agent swarms yet": "We think it can be. This is just Pareto principle. We're hill climbing the finer curves."
- Git: CORROBORATED in direction. The author list broadens quickly: top authors on main are David Mann 2,523, aiongg 1,113, yoriswind 508, … and Brandon Thomas 301 (`git log main --format=%an | sort | uniq -c`). The snapshot lists 189 contributor logins by 2026-10-10 (`contributors.json`).
- Notes: This is the founder's stated maintenance model: outside contributors spend their own agent tokens. Cost is thereby distributed and not disclosed.

### E08-019 — Readiness walk-back and the Reddit "100% parity within a month" claim
- Label: VERIFIED for HN; Reddit quote known only second-hand
- Source: HN 49959605 (2026-10-05): "These are still super early alpha … I'm going to try to drive these to 100% parity but it's going to take a minute." HN 49960035: "I didn't mean to publish the repos so soon." Reddit (via HN 49961646 quoting u/ai_art_is_art): "We should be in 'Beta' stage / ~100% parity within a month." PHLEARN (S15) quotes "within a month".
- Git: CONTRADICTED by the project's own docs one month later. On 2026-11-12, `ROADMAP.md:1-3` still says "Stage: alpha", with beta "~1,100–1,800 h away".

### E08-020 — The founder on Rust as "the agentic AI language" and on the multi-agent build bottleneck
- Label: VERIFIED (statement)
- Source: HN 49922867 (2026-10-01)
- Quote: "Rust is the best language to serialize agentic LLM output to … we need to start thinking about making the artifact cache non-blocking so multiple agents can work simultaneously"
- Notes: This matches the `CARGO_TARGET_DIR=target/agent-<name>` practice (E08-007) and the ~10 GB per target dir note (`AGENTS.md:176`).

---

## 4. Evidence entries: press and third parties (P2/P3)

### E08-021 — Press method claims derive from the founder's HN/Reddit posts. No outlet reports an interview.
- Label: VERIFIED (as "sources claim")
- Source: S13 Engadget (2026-11-01), S14 siliconreport (2026-11-01), S16 VICE (2026-10-09), S17 Gizmodo (2026-10-07), S15 PHLEARN (2026-10-15), S25 OMG! Ubuntu; all via WebFetch summary
- Data: Every outlet names Claude Opus 5.5 and cites HN or Reddit. Gizmodo quotes the Reddit post: AI "help me recreate 7 of the top Adobe apps", "not just some casual vibe coder", "15-year industry veteran". PHLEARN quotes Thomas via PetaPixel: "charged me the 'cancellation fee' on multiple occasions". No outlet reports agent counts, cost, time per feature or review process. The fetched pages show no evidence that any outlet contacted the developers. The press-kit page invites interview requests via Discord (S08).
- Notes: Engadget, siliconreport and VICE (citing Ars Technica) say he used Claude "to reverse-engineer" Adobe apps. That framing is CONTRADICTED by the developer's own statements (E08-017). It looks like an inaccurate paraphrase by the press.

### E08-022 — PHLEARN: "61% of PhotoCraft's changes named a Claude model as co-author" (counted 2026-10-15)
- Label: VERIFIED (claim); CORROBORATED-BY-GIT with a first-parent denominator
- Source: S15 https://phlearn.com/magazine/artcraft-photoshop-lightroom-clones/ (WebFetch summary)
- Method/check: up to 2026-10-15T23:59, first-parent main gives 1,411/2,286 = **61.7%** with a `Co-Authored-By: Claude` trailer. All commits: 1,855/3,491 = 53.1%. Non-merge: 1,674/2,969 = 56.4%.
- Notes: The article does not give its method. The first-parent figure matches.

### E08-023 — OrcaRouter: "8 parallel agents", ~6–8× parallelism, and "a person ran integration, tests, and release"
- Label: VERIFIED (claim)
- Source: S18 https://www.orcarouter.ai/blog/artcraft-opus-5-5-seven-adobe-clones-in-rust (2026-10-07, WebFetch summary)
- Notes: The "8 parallel agents" figure is quoted correctly from the repo (E08-005, CORROBORATED as a quote of the repo). The "per-subsystem agents with own target dirs" description matches `AGENTS.md:172`. The "person ran integration/tests/release" claim is the article's own inference, without a source (UNCORROBORATED). It reports **no** token or dollar figure.

### E08-024 — Third-party claim of "AI decompilation" (Bluesky, via aiweekly)
- Label: VERIFIED (claim exists); UNCORROBORATED
- Source: S23 aiweekly.co (2026-10-07). It reports that Alejandra Caraballo wrote on Bluesky that the project was assisted by AI decompilation. The article did not verify this.
- Notes: The developer denies it (E08-017). No git evidence either way was checked (lead: search history for Ghidra or disassembly tooling).

### E08-025 — Critical commentary on quality, "vibe-coded" status and maintainability
- Label: VERIFIED (as claims)
- Sources: S19 Shokunin ("Over a dozen updates later Photocraft 0.23.0 still has a worse brush engine than image editors had in the 90s"; "hundreds of bug reports filed each day"; the author runs a competing app). S13 Engadget (users report deleted images, randomly merged layers; quotes critics "this codebase will be unmaintainable in a few months" and TheGingerBill's "utter AI-driven slop"). S20 Peter Rex (data-safety bugs; "these estimates tend to slip"). S17 Gizmodo (Free Transform unreliable). S26 XDA (positive, "vibe-coded" label). HN 49961271 ("Essentially nothing works", 2026-10-05). HN 49959750/49959826 ("its all vibe coding"); counter-view HN 49960997 ("That's not vibe coding").
- Notes: Shokunin and the others offer **no** developer reply found. The founder's replies on HN are E08-018/019 (asks for patience and community help). Engadget's "cannot open native PSD files" claim conflicts with P1 corpus claims (`README.md:222-224`), so it is untested here.

### E08-026 — Legal and clean-room debate
- Label: VERIFIED (as claims)
- Sources: S24 Fstoppers/LegalEagle (questions whether an AI model "can stay on the clean side"; patents are not avoided by independent creation). HN 49996130 (qarl: two-agent spec/implement clean-room "is very easy"). HN 49996708 (wg0: perhaps "started with screenshots of every screen and menu"). S19 (claims feeding Adobe screenshots to Claude breaks Adobe ToS). S15 PHLEARN (cites Sega v. Accolade, Google v. Oracle).
- Notes: There is no developer statement that agents were split into spec-writer and implementer roles. The two-agent model is third-party speculation. The developer's documented "observed behaviour" process includes measuring the installed app (E08-006).

### E08-027 — Project websites contain no build-method statements
- Label: VERIFIED
- Source: S07 https://photocraft.org (title "PhotoCraft - Free Open-Source Photo Editor in your web browser"); S08 getartcraft.com pages
- Data: case-insensitive regex for claude|codex|agent|anthropic|built with|written|vibe|llm|opus over the extracted text. Hits are only product-facing ("Agent-ready … built for automation and AI agents", "written entirely in Rust", "Built the hard way. Every Crafting App is written from scratch in Rust"). /news has 2 posts (2026-01-16, 2026-01-30), neither about the Crafting Apps. The Craft Anything page markets "work with a coding agent to build … your own project" (an ArtCraft product that itself promotes agent-built clones).
- Method: `curl` + `python3 -I scratchpad/work/E08x.py <file> <regex>`

### E08-028 — Org RFC-0006 "coding agents": "much of the current PR volume comes from coding agents"
- Label: VERIFIED (via WebFetch, verbatim quotes requested)
- Source: https://github.com/storytold/craft-contrib/blob/main/rfcs/0006-coding-agents.md (accessed 2026-11-12; no author or date shown on the page)
- Quote: "The craft apps welcome AI-assisted contributions, and much of the current PR volume comes from coding agents." Also "Running agents on hundreds of issues across eleven repositories taught us which instructions prevent those mistakes." Observed failure modes: "duplicate PRs, fixes for bugs already fixed on `main`, PRs left as drafts, or code that uses functions that don't exist." On attribution: "That line is redundant here, and a repository rule may not require it."
- Notes: This is the most direct **P1 statement about maintenance by agents** and about agent failure modes. It is the origin of house rules 1–15 (E08-008/009). It also states that `CLAUDE.md` should import `@AGENTS.md`. The RFC gives **no** agent count limit, tooling or cost (cost appears only as "spending money" on the stop-and-ask list). The run on "hundreds of issues across eleven repositories" has no date or agent count. Lead for the PR streams: test the duplicate-PR and already-fixed rates.

### E08-029 — Public repository metadata on 2026-11-12
- Label: VERIFIED (WebFetch summary)
- Source: S30 https://github.com/storytold/photocraft; S29 https://github.com/storytold
- Data: About = "PhotoCraft: An open-source photo editor written from scratch in pure Rust". 78.9k stars, 14.0k forks, 335 watching. Issues tab 2.8k, PRs tab 1.3k (open counts as shown on the tabs). "12,487 Commits" (the local main has 12,396 at the pin; the page may be newer). The org has 80 repositories, and craft-libs is listed. The org description is "Open Source Tools and Models for Makers, Builders, and Creatives". Neither page mentions AI development.
- Notes: The About text changed from "clean-room reimplementation of Adobe Photoshop" (as quoted by the press in early October and by the Gitee/Passw mirrors) to "photo editor written from scratch". The README still says "clean-room reimplementation" (`README.md:17`). The date of the About change could not be checked, because GitHub API access is blocked.

### E08-030 — Release notes credit contributors and show "Integration batch" bundles but no AI disclosure
- Label: VERIFIED (WebFetch summary, partial page)
- Source: S32 https://github.com/storytold/photocraft/releases
- Data: v0.21.0 (11-06) through v0.23.1 (11-12) are published by github-actions and list 47, 61, 71 and 11 contributors. The notes include "Integration batch 13: 13 parity epic PRs on main" and "Integration batch 19: epic PRs (WIP)". Tags v0.22.0 and v0.23.1 are GPG-signed by dylanmtaylor. No AI, agent or Claude mention appears in the visible text.
- Notes: "Integration batch … epic PRs" is a P1 workflow signal of batching many PRs onto main. Lead for the merge-workflow streams. The local tag list shows 27 tags from v0.1.0 (2026-10-01) to v0.23.1 (`git for-each-ref refs/tags`).

### E08-031 — No public statements found from other maintainers
- Label: VERIFIED (negative result)
- Source: WebSearch "PhotoCraft maintainer David Mann OR Dylan Taylor OR aiongg …" (2026-11-12). HN Algolia searches were made only for `echelon`.
- Notes: The search found only a release-note credit for davidmann4 (PR #2981, via releasebot.io). There is no method statement by David Mann (2,523 commits), aiongg (1,113) or Dylan M. Taylor (release signer).

---

## 5. Claims matrix

| # | Claim about method | Sources (class) | Git corroboration |
|---|---|---|---|
| C1 | Built mainly with Claude Opus 5.5 | E08-014 (P1); S13–S17 (P2) | CORROBORATED-BY-GIT (Opus 5.5 is the dominant trailer; 226/301 founder commits have Claude trailers) |
| C2 | Uses "vanilla Claude Code" | E08-015 (P1) | CORROBORATED-BY-GIT for Claude Code (304 `Claude-Session:` trailers); "vanilla" UNCORROBORATED |
| C3 | Occasionally Codex; other models | E08-015 (P1); E08-010 (P1) | CORROBORATED (15 Codex, 40 GPT-6, Cursor, Copilot trailers) |
| C4 | "Planning with Claude, implementation with Kimi" | E08-015 (P1, scope unclear) | UNCORROBORATED (no Kimi trailer seen) |
| C5 | Photoshop was "one-shotted" | E08-013 (P1); S16, S20, S24 (P2/P3) | Partly: a commit literally named "one-shot" (+42,241 lines). "Whole thing" CONTRADICTED by alpha status and 12k later commits |
| C6 | 8 parallel agents in one early session; 6–8× parallelism | E08-005 (P1); S18 (P3) | UNCORROBORATED quantitatively; "other agents" mentioned in commit aa87012aab |
| C7 | 10–20 concurrent agents sustained | E08-003 (P1) | UNCORROBORATED (lead for concurrency streams) |
| C8 | ~1,000 PRs, 1,152 commits in 10.5 days; median merge 3.4 h | E08-004 (P1) | Partly CORROBORATED: 1,380 commits by 10-10 end (cutoff unknown) |
| C9 | 2,000–4,000 agent-hours spent by 2026-10-10 | E08-004 (P1) | UNCORROBORATED (derived estimate, not metered) |
| C10 | ~61% of changes Claude co-authored (2026-10-15) | S15 (P2) | CORROBORATED-BY-GIT (61.7% first-parent) |
| C11 | Clean room: no decompilation, no Ghidra, no Adobe code | E08-017 (P1); README | UNCORROBORATED (not provable from git); method includes reading installed-Photoshop resource files (E08-006) |
| C12 | "Reverse-engineered" with Claude | S13, S14, S16 (P2) | CONTRADICTED by P1 statements; no git evidence of decompilation was checked |
| C13 | AI decompilation assisted | S23 citing Bluesky (P3) | UNCORROBORATED |
| C14 | Every PR has an accountable human; diffs are reviewed | E08-009 (P1 norm) | Not checked here (lead) |
| C15 | "100% AI software factory and no human review" | E08-016 (P1, scope ambiguous) | Not checked here; conflicts with C14 and with CodeRabbit badge |
| C16 | "Within a month" to ~100% parity / beta | Reddit via HN (P1 second-hand); S15 | CONTRADICTED (still alpha on 2026-11-12, `ROADMAP.md:3`) |
| C17 | Built in "about two weeks" | S15 (P2 headline) | Consistent with first commit 2026-09-30 → v0.8.2 2026-10-12 for an *alpha* (tags); not a finished product |
| C18 | Community contributors spend their own tokens | E08-018 (P1) | CORROBORATED in direction (189 logins by 10-10; David Mann 2,523 commits) |
| C19 | AI attribution is credited in the product | E08-010 (P1) | CORROBORATED (`contributors.json` `models`) |
| C20 | PRs must not say an agent wrote them (from 2026-11-06) | E08-008 (P1) | CORROBORATED-BY-GIT (rule present; Claude-trailer share 31.7% → 27.5%) |
| C21 | Cost "real but modest" | S18 (P3) | UNCORROBORATED; no figure anywhere |
| C22 | "Much of the current PR volume comes from coding agents" | E08-028 (P1, org RFC) | CORROBORATED in direction (4,727/12,396 main commits have a Claude co-author trailer; more than half until mid-October) |
| C23 | Typical agent failure modes: duplicate PRs, already-fixed bugs, abandoned drafts, nonexistent functions | E08-028 (P1) | Not checked here (lead for PR streams) |

## 6. Method questions with no developer statement found

Searches covered the README, docs, AGENTS.md, book, websites, HN (Algolia, all `echelon` comments since 2026-09-30) and the press above. None of them answered these questions:
1. **Token spend or dollar cost** of building or maintaining PhotoCraft. Only "Only have to pay the price once" (HN 49959674) and "community token spend".
2. **Orchestration tooling**: how parallel agents were launched, assigned and merged. Beyond "vanilla Claude Code" and per-agent target dirs, nothing.
3. **Prompts and specs**: no published prompts, task specs or the `plan/` notebook (gitignored, `AGENTS.md:208`). The dev log is also gitignored.
4. **Measured concurrent agents over time**. Only "8" (one session, 10-02) and "10–20" (10-10), with no method.
5. **Human review process for merges**: who merges, and how much human reading occurs. Only the norm in E08-009 and the ambiguous remark in E08-016.
6. **Failure and rollback rates**, abandoned agent sessions, reverted PRs. No statement.
7. **How the 42,241-line "one-shot" commit was produced**: prompt, model, duration.
8. **The split between the founder's own agents and community agents**, and whether maintainers (David Mann, aiongg, Dylan M. Taylor) run agent fleets. No public statements by these maintainers were found (E08-031). RFC-0006 says only that "much" of the PR volume is agent-driven (E08-028).
9. **Model choice rationale** and model switching (Opus 4.8 → 5.5, Fable, Mythos trailers). No statement.
10. **Testing strategy as an agent guardrail**: documented in AGENTS.md (gates), but no developer statement on how well it worked.

## Open questions / uncertainties
- Reddit (primary founder posts) could not be read: curl 403, WebFetch refused. Quotes rely on HN and press relays.
- Phoronix, Notebookcheck, AppleInsider, TweakTown and pasqualepillitteri failed. t3n and kunalganglani articles were not found by search.
- All press entries are WebFetch small-model summaries. Short quotes there are lower-fidelity.
- HN `echelon` = Brandon Thomas is inferred (same handle as the GitHub login, ownership claims); it is not stated on the profile.
- The scope of the "no human review" remark (E08-016) is unclear.
- Other maintainers were searched only by web search (E08-031). X/Twitter, YouTube (e.g. youtube.com/watch?v=BGShygDux9o cited in HN 50333271; LegalEagle) and Discord were not read directly.
- RFC-0006 and craft-contrib were read only through WebFetch. The RFC's author, date and status are not shown. The `standards/house-rules-*.md` files were not fetched.
- When the GitHub About text dropped "clean-room reimplementation of Adobe Photoshop" is unknown (E08-029).

## Leads for other streams
- Concurrency claims (E08-003, E08-005): measure overlapping PR lifetimes and distinct `Claude-Session` ids per hour around 2026-10-01..10-10 and later.
- Commit aa87012aab (2026-10-01) "(+ in-progress work of other agents)": early multi-agent evidence.
- Commit 16941f7198 "one-shot" (+42,241 lines, no trailer).
- Commit 0c2d4bfd1a carries an Opus 4.8 trailer while estimating Opus 5.5 effort.
- Commit 7d8648dfcb (2026-11-06): the house rules arrive from `storytold/craft-contrib`, including "No agent attribution". Test for an attribution drop after that date.
- `craftrules` retired (`AGENTS.md:18`); commit 1d61b33c54 moved the release playbook there.
- Engadget's "cannot open PSD" claim vs. the corpus claims: for testing streams.
- aiweekly's "AI decompilation" claim: search history for disassembly or decompiler artefacts.

## Methods-relevant takeaways
- State effort in model-specific agent-hours and recalibrate against your own merged-PR history. PhotoCraft did this and revised its estimate about 10× upward within 8 days (E08-002, E08-004, E08-005).
- Write down the parallel-agent mechanics: separate build dirs, file ownership, atomic manifest writes, wait instead of fixing others' breakage (E08-007, E08-020).
- Plan for abrupt session ends with a handoff log and an always-green tree. PhotoCraft keeps that log private, which costs external auditability (E08-007).
- List explicitly the decisions that need a human: licensing, signing, hardware, native-speaker review, checks against the reference app (E08-006).
- Put human accountability per agent run into the house rules (E08-009). Public founder rhetoric ("no human review", E08-016) can undercut that norm.
- Credit models in the product from trailers (E08-010). Note that a later "no agent attribution" rule erodes the same data (E08-008).
- Public "one-shot" and "within a month" claims invite reputational blowback when the project's own docs say alpha (E08-013, E08-019, E08-025). Keep public claims aligned with the in-repo readiness docs.
- Use the community as a distributed token budget. This is a stated strategy (E08-018), and its costs and quality control are undocumented.
- Turn observed agent failure modes into org-wide rules that are copied into each repo with integrity checks. RFC-0006 lists duplicate PRs, already-fixed bugs, abandoned drafts and invented functions, and each rule answers one of them (E08-028, E08-008).
- A clean-room claim needs a documented procedure. "Observed behaviour" here includes reading installed-app resource files and comparing renders (E08-006, E08-017, E08-026).
