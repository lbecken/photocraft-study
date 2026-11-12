# 05 — AI agent and human role maps

Scope: who (people) and what (AI systems, bots, CI) did which work in `storytold/photocraft`, shown by
behaviour in the public record. Upstream pinned at `main` = `74330157cb` (2026-11-12). Corrections in
`01c-errata.md` override the evidence files and are applied here. In particular, `Claude-Session:` =
274 commits on main (238 non-merge), 62 distinct sessions on main and 129 across all refs.

Labels: **VERIFIED** = observed in a primary source and cited. **INFERRED** = reasoned from verified
evidence, with the chain given. **PROPOSED** = our recommendation, never a PhotoCraft practice.
"Rule" means documented in the repo. "Observed" means a pattern in history. "Self-reported" means a
developer statement that we have not verified. A commit without an AI trailer has **attribution
unknown**; it is not counted as "human" (brief rule 4).

Terms used below:
- **House rules**: the 15-rule block that `AGENTS.md:1-20` has carried since 2026-11-06 (7d8648dfcb). It is copied byte-for-byte from the org repo `storytold/craft-contrib`, which is an external repo (E02-012).
- **Integration batch**: a branch that merges many community PRs, resolves their conflicts and runs CI once. There were two series: `claude/integ-batch-1..11` (10-08/09) and `davidmann4/integration-batch-7..20` (10-23..11-06) (E06-021/022).
- **AI-attributed**: the commit body has an AI `Co-authored-by:` line, a `*-Session:` trailer or a "Generated with" footer (E03 §1 C7).
- **Merge-PR commit**: a first-parent `Merge pull request #N from owner/branch` commit. Its *author* is the person who clicked merge (E03 §4). For squash merges the merger is **not** recorded in git (author = PR author, committer = GitHub).

---

## Summary of findings

1. **No role is documented by name.** No CODEOWNERS file, merge policy or review requirement exists on
   any ref (E02-020, E02 §6). All human roles below are INFERRED from behaviour. Two things are
   documented: the accountability rule ("A person is accountable", `AGENTS.md:6`) and a closed
   stop-and-ask list (`AGENTS.md:14`). Both arrived late, on 2026-11-06.
2. **Merge authority is concentrated; authorship is not.** 582 canonical authors appear on main
   (E03-007). Eight people clicked 597 of the 603 web-flow merge-PR commits, and David Mann alone
   clicked 356 (59%) (`data/E03_mergepr_by_merger.csv`).
3. **Per-author AI attribution clusters at the poles.** Of the 25 largest human authors, 6 have ≥95% of their
   non-merge commits AI-attributed, 9 have ≤5%, and 10 fall in between (`data/E03_attr_by_author.csv`). The heaviest
   integrators sit at both poles: David Mann 98.6%, aiongg 0.0%.
4. **AI shows up mostly as a co-author on a human's commit.** 4,097 of 8,329 non-merge commits carry an
   AI co-author line. Only 120 of 12,396 commits (1.0%) have an AI *author* identity (E03-003, E03-006).
   Claude Opus 5.5 strings make up 3,602 of the 4,097 co-authored commits (both spellings, E03-004).
5. **AI systems held more roles than "implementer".** The record also shows AI as integration-batch
   builder (Claude identity, 10-08/09), release-commit author (d43db3e153), claimed reviewer/attacker
   pair (PR #9386, self-reported), bot reviewer (CodeRabbit), triage app (ticket-craft; LLM use
   unknown) and a driver/briefer/writer split (`Model-Effort:`, one contributor only). Each is evidenced
   below together with what it cannot show.
6. **Humans kept merge, release publication, and in late months labels and change requests.** In the
   ~22 PR pages read (E05, E06, E09), visible human approval is rare: 4 PRs with an explicit approval (#7848, #11641, #8452, #9363; E06-041, E05-035, E09).
   The documented accountability rule is not mechanically enforced.
7. **Attribution policy conflicts with itself.** House rule 15 says "No agent attribution" in PRs.
   The product's About ▸ Models screen is built from `Co-Authored-By` trailers
   (`docs/contributors.md:3-4`). Trailers continue after the rule (E02-016).

---

## 1. Human role map

Method: authorship and merge counts come from `scripts/e03_git_quant.py` (E03) and E06's `authors.py` /
`fp.py`. Where they differ the two use different alias merging (E03 C6). AI share = E03
`with_any_ai_attr / nonmerge_commits`. Review behaviour comes from WebFetch summaries of ~22 PR pages (E05 §0.3, E06 §6, E09), which are lower
fidelity. Unless a row says otherwise, every role assignment is
**INFERRED from the cited behaviour**, because no document names these roles.

### 1.1 Role table

| Role (INFERRED unless noted) | Who (public name / handle) | Active (author date, UTC) | Behavioural evidence (counts, source) | Own work vs AI-attributed work | Decisions observed in their hands |
|---|---|---|---|---|---|
| **Founder / product owner** | Brandon Thomas (`echelon`; `contributors/people.toml:41-43`) | 09-30 → 11-03 | First commit 386b0566d3 and "one-shot" 16941f7198 (+42,241 lines). Authored all 69 direct first-parent commits 09-30..10-03 (E06-012). 99 direct first-parent commits overall (`E03_first_parent_direct_by_author.csv`). 22 of 38 AGENTS.md revisions (recount; E02 §1 says 23). Author of ROADMAP/agent-hour planning (939c8f2c70). Co-author on 678 non-merge commits (`E03_coauthors_nonai_top.csv`) | 225/296 non-merge commits (76.0%) AI-attributed, mostly "Claude Opus 5.5". Early "Claude Opus 4.8" on 45 commits 10-02..10-04 (`E03_attr_models_summary.csv`). The one-shot root commit carries no trailer (unknown) | Set the rules (AGENTS.md revs 1–19, 21, 22, 26), the release role (18 of 20 `Release …` commits, tags v0.1.0..v0.20.1, E06-005), squash-merges of community PRs (#1261, #2792 "Landed as is.", via WebFetch, E06 §6). "Needs a human" list is owner-held (`docs/target-app-parity.md:238-242`, E08-006) |
| **Early integrator / agent operator** | BFlat (`bflatastic`) | 10-07 → 10-22 | Opened the CI-only batch PRs #1335 ff. and agent fix PRs #1344/#1421 (WebFetch). Committer of 12 first-parent `Claude`-authored commits (E06-010). 8 merge-PR clicks. Tag v0.3.0 (E06-005) | 84/87 non-merge (96.6%) AI-attributed; 30 with `Claude-Session` (E06 §1.1). Issue diagnoses posted as "Generated by Claude Code" (#1381, E09-B-002) | Merged agent-authored PRs with "No reviews" (#1344, #1421: "4 of 7 checks passed", E09-B-002) |
| **Principal integrator / merger** | David Mann (`davidmann4`) | 10-09 → 11-12 | 356 of 603 merge-PR clicks (`E03_mergepr_by_merger.csv`). Author of `integration-batch-13..20` merge commits (E06-022). 279 local `Merge PR #N:` merges. 1,176 self-committed merge commits (`E03_merge_commit_committers.csv`). Manual "(merge queue)" commits from 11-08 (7 on main, errata #2) | 964/978 non-merge (98.6%) AI-attributed, Claude Opus 5.5 | Merge of fork PRs without visible approval (#12237, #13234, E05-035). Dismissed a stale change request (#7809). Holds a PR back for a manual test ("Please don't merge yet: a manual test in the real app is planned", #13396, E06-043) |
| **Integrator / merger (no attribution)** | aiongg | 10-16 → 11-02 | Merged integration batches 7–12 (a02f2ee410 … b957878f3f, E06-003). 68 merge-PR clicks. 552 local `Merge PR #N:` merges. The CI gate became `cargo xtask ci` via shared `gate.yml` (9acf9a0cf9, E05-010). Supply-chain guard 6401cfdbe1. Module reorganisation 501b7f3459 | 0/430 non-merge with an AI trailer. **New:** 13 commits authored by the `Codex` identity reached main through aiongg's own PR #8577 (`aiongg/r4`, merge 6d807ba34c, 2026-10-22; §New evidence). The 0% therefore does not mean "no AI" | Merged batch PR #9386, whose stated review was by agents, with no human approval visible (E06-022) |
| **Maintainer: CI, security, platform, release** | Dylan M. Taylor (`dylanmtaylor`) | 10-11 → 11-12 | 26 merge-PR clicks. 36 direct first-parent commits, among them a 32-commit `security(...)` run on 10-22, 11:10–11:12 UTC (E06-026; recount). SonarCloud (8e518d8169), Dependabot (9185b64b94), Harden-Runner (e119384a83). AGENTS.md CI section (0379569d00). Tags v0.20.2, v0.22.0, v0.23.1; GPG-signed v0.22.0/v0.23.1 (E08-030). PSD extraction #13414 | 9/195 (4.6%) AI-attributed; most common string "Codebuff" (one egui follow-up says "Generated with Codebuff", 6e4f85e161). Security series: 0 AI trailers, tool unnamed (E09-G-002) | Release cutting after 11-02. Self-merge #13414 with no reviews (E05 §0.3). Merged #7848 |
| **Maintainer: reviewer / integrator, release** | FredApps | 10-12 → 11-11 | 48 merge-PR clicks; 146 local merge commits. Approvals on #7848, #11641, #8452 (WebFetch). 108-PR fork integration protocol "each with the latest FredApps review APPROVED at its exact current head" (`docs/integration-testing/`, E05-022). Imported the house rules (7d8648dfcb). Tags v0.21.0, v0.23.0. Nightly release dry run f1b5e7d727 | 10/131 (7.6%) AI-attributed. Artboard follow-up #11441 "Generated with Claude Code", Claude Opus 5.5 on 5 of 6 commits (E09-H-002) | Only maintainer with repeated explicit approvals in the sample. Changed agent rules (house rules) and CI |
| **Maintainer: reviewer-approver, labeller** | Tanish Manku (`tanish2k09`) | 10-07 → 11-11 | 71 merge-PR clicks. Requested changes on #11059 and #10426. Applied "ready to merge" and merged #11062 (E06-041). CI concurrency fix 07174271d5 ("80 of 83 push runs on main were cancelled") | 12/43 (27%, E06 §1.1) AI-attributed | Labels as approval signal ("ready to merge" = "Reviewed: correct, complete and tested", E06-030) |
| **Maintainer / merger, migrations** | skylar taylor-barrick (`skylartaylor`) | 10-10 → 11-11 | 19 merge-PR clicks. In-repo `codex/*` branches; egui 0.37 migration with a 1,632-line plan (14c059c971, E09-E-001). Post-merge tester who found artboard gaps (E09-H-002). `test/backfill-regression-tests` (#8690) | 1/78 (1.3%) AI-attributed. `codex/` branch names and `/home/codex/...` paths in the plan, but no Codex trailer: attribution weak (E06-025, E09-E-003) | Required "human review and a human merge" on #9363 (WebFetch, E09-E-002) |
| **Issue triager / epic filer** | David Mann (human account); ticket-craft (app, §2.7) | Nov sample | 12 of the first 25 open issues (#13458–#13472) filed by `davidmann4` with machine-style titles, e.g. `EPIC-CUSTOM-SHAPE-TOOL`. The epic was "measured through the control channel" (E06-030, E06-034) | Generated-looking titles. That an agent filed them is **INFERRED only**: the list page shows no attribution | Work decomposition into claimable child issues ("Free to pick up / Being worked on / Merged") |
| **Fork-based community contributors** | 108 distinct fork owners on merge-PR commits (E06-014); e.g. Hector Villarreal, yoriswind, vangel76/Valentin Klein, Khawar Zamman Wani, Higgs32584, Trevor Brown, Finn Newick, Mohamed Mahjoub, Lcoding15 | 10-05 → 11-12 | 576 of 598 merge-commit PRs from forks (E06-014). Top fork source owners: davidmann4 76, hectorviov 65, rmsff 60 (E03 §4) | Bimodal, §3.6. Tools as recorded: Claude Opus 5.5 (most), Fable 5.1 (Trevor Brown), Codex identity (yoriswind fork `codex/*` PRs #11221/#11852/#11711), Cursor, Copilot, GPT-6, Codebuff (`E03_attr_models_summary.csv`) | None reserved. One self-withdrawal is visible (#12945) |
| **Testers / reporters** | community issue authors (e.g. hash-mc #1381, womb4t #13451); skylar taylor-barrick (post-merge test, #11441) | throughout | ~6,974 issue numbers implied by the shared number space (E03-009, INFERRED); 2,804 open issues (E06-030, WebFetch) | — | Defined the work for agent fix sweeps (E09-B) |
| **Human-only tasks (documented)** | "owner" | — | "Needs a human. Owner decisions on the AI backend (#41 …); Windows code-signing material; tablet hardware checks; native-speaker review …; checking exports by opening them in Photoshop" (`docs/target-app-parity.md:238-242`) | — | **VERIFIED (rule)**: the doc names these as human tasks |

### 1.2 Decisions that appear reserved to humans

| Decision | Status | Evidence | Label |
|---|---|---|---|
| Merge to main | Every observed merge click is a human account (8 people account for 597 of 603 merge-PR commits). The 14 first-parent commits committed directly by `Claude` (E03-006) are the exception | `E03_mergepr_by_merger.csv`. Squash mergers are not recorded in git | OBSERVED; no rule says who may merge (E02 §6) |
| Push to main | "**`main` changes through a pull request.** Do not push to it. Branch protection enforces this. There is no exception." | `AGENTS.md:13`, since 2026-11-06 | VERIFIED (rule). Branch protection itself is not visible |
| Releases | Release is on the stop-and-ask list. "Nobody sees a draft until a maintainer publishes it." Signing secrets live in the `release` environment | `AGENTS.md:14`; `docs/releasing.md:3-6`; `release.yml:43-58` (E05-060) | VERIFIED (rule + partly mechanical). Exception: d43db3e153 "Release 0.8.2" has the `Claude` identity as author and committer (E06-005) |
| Licensing, publishing, new remote, secrets, money, destructive git | "**Stop and ask only about** … Otherwise keep working." | `AGENTS.md:14` | VERIFIED (rule, no check) |
| Accountability for agent output | "**A person is accountable.** Whoever runs an agent answers for what it opens and for its review comments." | `AGENTS.md:6` | VERIFIED (rule, no check) |
| Credit entries | "Agents working for a contributor: … ask them once whether they want to be credited" | `AGENTS.md:201-204` (E02-018) | VERIFIED (rule) |
| PR closure | "A maintainer decides closure; it is never automatic." | `AGENTS.md:19` | VERIFIED (rule). Conflicts with the `waiting on author` label text "Closed after 14 days" (E06-041) |
| "Hold" | `needs decision` label: "Held for a maintainer decision; don't merge, close, or replace until a maintainer removes it" | labels page (WebFetch, E06-030) | VERIFIED via WebFetch summary |

---
## 2. AI role map

Each row lists only what the record shows, the human it was attached to, and what is unknown. Three
things are unknown in **every** row, so they are not repeated: the prompts, the autonomy settings
(permission mode, tool allow-lists) and how closely a human watched the run. No permission config
exists on any ref (E02 §6 "Tool permissions … Not documented").

### 2.1 (a) Co-author on a human's commit

Finding: this is the dominant form. 4,097 of 8,329 non-merge commits on main (49.2%) carry an AI
co-author line. With session trailers and footers added, "any AI attribution" covers 4,130 (49.6%).
On first-parent non-merge commits the share is 1,700 of 2,871 (59.2%). The share falls from 84.7% in
W40 to 22.9% in W46 (partial week) (E03-003, `data/E03_attr_weekly.csv`). VERIFIED.

| Co-author string (verbatim) | non-merge commits | of which first-parent | first → last (committer date UTC) |
|---|---|---|---|
| Claude Opus 5.5 | 3,158 | 1,355 | 10-01 → 11-11 |
| Claude Opus 5.5 (1M context) | 444 | 187 | 10-04 → 11-09 |
| Claude Sonnet 5.5 | 157 | 15 | 10-05 → 11-11 |
| Claude Fable 5.1 | 137 | 21 | 10-08 → 11-09 |
| Claude | 53 | 45 | 10-08 → 11-10 |
| Claude Opus 4.8 | 45 | 45 | 10-02 → 10-04 |
| Claude Haiku 5.5 | 40 | 17 | 10-16 → 10-30 |
| Cursor / Cursor Agent | 36 / 4 | 6 / 4 | 10-09 → 10-20 / 10-14 |
| Copilot | 31 | 31 | 10-07 → 10-08 |
| GPT-6 / GPT-6 (Codex) | 22 / 2 | 3 / 2 | 10-12 → 10-22 / 10-09 |
| Codex / OpenAI Codex | 12 / 3 | 10 / 0 | 10-12 → 11-10 / 10-17 → 10-19 |
| Claude Fable 5.2 | 12 | 0 | 11-10 → 11-11 |
| Codebuff | 8 | 7 | 10-23 → 10-25 |
| Claude Opus 5, Sonnet 5, Mythos 5.1, Sonnet 4.6 | 5, 4, 4, 3 | 0, 0, 4, 0 | 10-07 … 11-02 |
| Claude Opus 4.8 (1M context), Qwen 3.8 Flash, Claude Haiku 4.5, DeepSeek, Devin | 1 each | 1 each | 10-05 … 10-14 |

Source: `data/E03_attr_models_summary.csv`, VERIFIED. A commit can carry several strings.
- **Attached human:** the commit author. Every top AI-heavy author is a human account (table §3.6).
- **What it demonstrably did:** nothing beyond the trailer's existence. A trailer is a self-report written by the tool or the person. It does not show model usage or the share of lines an agent wrote (E03-004 note).
- **Unknown:** whether "(1M context)" marks a different configuration (E03 open questions). Also unknown is how much of each commit the human edited.
- **Developer statements:** "I'm currently using Opus 5.5 to create 100% pure-Rust … implementations" (HN 49934844). "vanilla Claude Code … occasionally Codex" (HN 50029182, 49977572) (E08-014/015). Self-reported; the dominant trailer corroborates the Opus 5.5 part.

### 2.2 (b) AI as commit author identity

Finding: rare. 120 of 12,396 commits on main (1.0%): `Claude` 94 (62 non-merge), `Codex` 24 (18
non-merge), `Claude Opus 5.5` 2 (`data/E03_ai_author_identity.csv`, E03-006). VERIFIED.

| Identity | main | all refs | Where it sits | How it reached main (first-parent landing; script in §New evidence) | Attached human |
|---|---|---|---|---|---|
| `Claude` | 94 (10-08 → 11-10) | 645 | in-repo `claude/integ-batch-1..11`, `claude/fix-<issue>-*`, `claude/fix-main-*`, session-named `claude/friendly-ritchie-iqt0sh`; `community/*` fix-ups (E06-020, E06-023) | 14 first-parent commits committed directly (12 with committer BFlat, 2 with committer Claude). The rest came inside merge PRs: davidmann4 integration batches 7/8/9/10 (3+6+3+14), Lcoding15 fork PRs (≥36, merged by David Mann and Tanish Manku), `storytold/community/*` PRs merged by BFlat | BFlat for the 10-08/09 work (committer field, +07:00 tz, E06-010). Otherwise the fork owner or integrator (INFERRED from landing path) |
| `Codex` | 24 (10-17 → 11-07) | 42 | PR heads and fork branches. Not on in-repo `codex/*` branches (E06-025) | **New:** 13 via aiongg's PR #8577 (`aiongg/r4`, 10-22). 10 via yoriswind fork `codex/*` PRs #11221/#11852/#11711 (merged by David Mann). 1 via #11168 (hnoerenberg, merged by FredApps) | aiongg and yoriswind, both of whom carry 0 AI trailers (§3.6) |
| `Claude Opus 5.5` | 2 | 102 | mostly PR heads; 4 commits on `claude/integ-batch-6` | via `storytold/community/1462-labmix` PR #1896, merged by BFlat | BFlat |
| `Cursor Agent`, `Copilot`, `copilot-swe-agent[bot]`, `OpenAI Codex`, `Arena Agent`, `photocraft-agent UNCONFIGURED`, `agent-346022` | 0 on main | 30, 2, 1, 1, 4, 5, 7 | PR heads only | did not land | unknown |

- **Branch namespaces:** the 38 in-repo `claude/*` branches all date from 10-08..10-11 and are all by the `Claude` identity (E06-020). The 5 in-repo `codex/*` branches are by skylar taylor-barrick with no trailers. Of 40 fork `codex/*` merge sources, yoriswind owns 19 (E06-025). A `codex/` branch name is weak attribution: PR #7848 (`codex/…`) carries Claude trailers (E06-025).
- **Unknown:** whether identity commits ran without a human in the loop. The commit identity records only the git config of the tool.

### 2.3 (c) Session-tagged work

Finding: per-session trailers exist for a small minority of AI-attributed commits. Most sessions are
short (median 1 commit on main), and many are distinct on a single day. VERIFIED (E06-011 `sess.py`;
counts per errata #1).

| Scope | commits | distinct sessions | commits/session min / median / p90 / max | singletons | days with ≥1 session | max sessions same day |
|---|---|---|---|---|---|---|
| main, `Claude-Session:` | 274 (238 non-merge) | 62 | 1 / 1 / 6 / 52 | 32 | 33 | 10 (2026-10-13) |
| all refs, `Claude-Session:` | 914 | 129 | 1 / 2 / 14 / 127 | 37 | 36 | 15 (2026-10-13) |
| main, `Copilot-Session:` | 31 | 5 | 1 / 7 / 9 / 19 | 1 | 3 | 5 (2026-10-07) |
| all refs, `Copilot-Session:` | 90 | 6 | 2 / 15 / 21 / 44 | 0 | 4 | 5 (2026-10-07) |

- **Attached humans (all refs):** sessions are grouped by commit author. The `Claude` identity has 51, Nicolas Falesy 12, Khawar Zamman Wani 8, Leel Wasanatha 7, Shehan Kavishka 6. All Copilot sessions belong to Alex Gorevski, plus one under the author `Copilot` (E06-011). One session id (`session_01UHgFEH…`) spans the 10-08 fix sweep (#1248, #1286, #1323, #1381), the batch-7 clippy fix and the artboard fix #1584 (E09-B, E09-A-004, E09-H). INFERRED: one long Claude Code session driven by BFlat handled several issues one after another.
- **Limits:** session trailers cover 274 commits, against 3,780 main commits with a `Co-authored-by: Claude…` line (E06-011), so they undercount sessions. "Same day" means distinct ids on one author-date day, not proven concurrency (E06-011, E03-014).
- **Unknown:** session length in tokens or time, and whether sessions were run from the web or the CLI. The `adjective-name-id` branch names match Claude Code web default naming (INFERRED, E06-020).

### 2.4 (d) `Model-Effort:` trailers: a driver / briefer / writer split

Finding: 25 non-merge commits on main (27 incl. 2 merges), 2026-11-08 UTC (b29fdc5a29; author date 11-07) → 11-11
(cbd96a4de6). **New:** all 27 are by **one contributor, Trevor Brown**. All landed through his fork
PRs `TrevorBrown-dev/*` (#12212, #12274, #12298, #12299, #12382, #12402, #12815, #13073, #13150,
#13215), each merged by David Mann (§New evidence). The convention appears in no repo document:
`git grep Model-Effort` at HEAD → 0 files (E02 §5). VERIFIED.

| Value (verbatim) | lines | Division of labour it describes (INFERRED from the verbs) |
|---|---|---|
| Opus 5.5 drove; Opus 5.5 briefed; Sonnet 5.5 wrote at medium | 12 | a lead model ran the session and wrote the brief; a smaller model wrote the code at "medium" effort |
| Opus 5.5 drove and briefed; Sonnet 5.5 wrote at medium | 6 | same, stated compactly |
| Opus 5.5 drove; Fable 5.1 briefed; Sonnet 5.5 wrote at medium | 2 | three models: driver, separate brief-writer, implementer |
| Opus 5.5 drove; Fable 5.1 decided; Sonnet 5.5 wrote at medium | 1 | a "decider" model in place of the briefer |
| Opus 5.5 drove and wrote | 2 | single model, no delegation |
| Opus 5.5 drove and wrote (review fix, no brief) | 2 | driver fixed review findings itself |
| Opus 5.5 drove and wrote (CI fix) | 1 | driver fixed CI itself |
| Opus 5.5 drove and resolved | 1 | driver resolved (presumably conflicts; INFERRED) |

Source: `data/E03_model_effort_values.csv`.
- **Attached human:** Trevor Brown. 114/115 (99.1%) of his non-merge commits are AI-attributed, most often with "Claude Fable 5.1" (`E03_attr_by_author.csv`).
- **What it shows:** one contributor's orchestration pattern. A senior model delegates implementation to a cheaper model, and the driver does fixes itself.
- **Unknown:** the harness (subagents or separate sessions), what "medium" means, and whether anyone else used the pattern without the trailer. It is **not** project practice (03 B.9 "Agent roles" row).

### 2.5 (e) Integration-batch builder

| Series | AI role evidenced | Human attached | Source | Unknown |
|---|---|---|---|---|
| `claude/integ-batch-1..11` (10-08 → 10-09) | Author **and committer** `Claude` on the batch merges: 12 `Merge branch 'pr-NNNN' into claude/integ-batch-1` commits within 1 second on 10-08. Conflict fix-ups ("fmt: batch 7 conflict resolution", 2c82295e4c). Scorecard regeneration (94c003452f) | bflatastic opened and closed each PR as "CI only (do not merge)", "🤖 Generated with Claude Code" + session link, "No reviews" (#1335, WebFetch) | E06-021, E09-B-003 | Whether one session built all 11 |
| `davidmann4/integration-batch-7..20` (10-23 → 11-06) | Batch branches contain Claude-trailered commits (38 to 132 per batch). Conflict-resolution merges explain each file, e.g. 38609e5615 "Conflicts resolved: …" with `Co-Authored-By: Claude Opus 5.5`. 26 `Claude`-identity commits came in via batches 7–10 | David Mann (author of batch merges 13–20; 98.6% AI-attributed); aiongg merged 7–12 | E06-022 | Which batch steps were agent-run and which were manual. The relation to the `claude/` series is unverified (errata #6) |

INFERRED: integration work is the activity with the most explicit agent involvement after
implementation. Conflict resolution and generated-file regeneration were delegated to agents, and a
human clicked merge.

### 2.6 (f) Reviewer agents and review bots

| Reviewer | What it did (evidenced) | Attached human | Blocking? | Source | Unknown |
|---|---|---|---|---|---|
| "two independent agents per PR (a reviewer and an attacker)" | Claimed in the batch-8 PR #9386 description: "every claim checked against code, spec or a run"; "each PR's code reverted on the branch, its named tests fail" | David Mann (PR author); merged by aiongg with no visible human approval | n/a | PR #9386 via WebFetch summary (E06-022) | **Self-reported only.** The review outputs were not committed. Whether other batches used it is unknown (03 U6) |
| Automated "first-pass review" from a human account | eliets2 posted a review described as automated ("needs changes") on #12237 | eliets2 | no (#12237 merged by David Mann) | E05 §0.3, E05-035 (WebFetch) | Tool and frequency |
| CodeRabbit (`coderabbitai[bot]`) | On 5/5 sampled PRs from 10-19 on and 0/5 earlier (E06-040). Posts walkthroughs, "Merge Risk", "Prompt for AI Agents" blocks and suggested reviewers (E05-030, E06-043). Authors respond: "Address CodeRabbit review" commits (9b21358035); 255 commits on main mention "CodeRabbit review" (recount; E07 §10's 311 does not reproduce). One comment changed an agent rule (0d9a9a5a70, E02-015). `Co-authored-by: coderabbitai[bot]` on 19 commits across all refs (E06 §2.1) | the PR author is asked to act; integrators request it ("review plz", #13396) | **no**: #12237 merged with a failed pre-merge check (E05-030) | `.coderabbit.yaml:2-6` (only skips Dependabot) | Whether it uses an LLM is not stated in the repo |
| SonarQube Cloud | Quality gate and new-code coverage on same-repo PRs ("95.8% coverage on new code", #13414). Skipped on fork PRs without the token | Dylan M. Taylor set it up (8e518d8169) | scan `continue-on-error` (E05-029) | E05-029/031 | — |

### 2.7 (g) Triage bot

ticket-craft (GitHub App; listed developer `juansebsol`) applied all 5 labels on #13451 (including
`priority: critical` and `in progress`), linked the in-progress PR and related issues, and proposed
splitting epic #13458. VERIFIED via WebFetch summary (E06-033). Nothing about it appears in the repo
(`git grep` empty), so its configuration lives outside. **Whether it uses an LLM is unknown** (the app
page gives "No description"). Attached human: none visible.

### 2.8 (h) Release commit author

d43db3e153 "Release 0.8.2: web build back under the wasm size gate" (2026-10-12) has the `Claude`
identity as **author and committer**, and tag v0.8.2 points to it (E06-005, E05-062). Separately, 26 of
29 first-parent version-bump commits carry a Claude trailer (E05-065). VERIFIED. **Attached human:**
unknown for d43db3e153 (−0400 tz, the founder's offset, E03 §10, INFERRED weakly). Publishing the
draft release was a maintainer action by rule (`docs/releasing.md:3-6`). Who published is not in git.

### 2.9 (i) Campaign executor

| Campaign | AI role evidenced | Human | Source | Unknown |
|---|---|---|---|---|
| Never-crash (10-04) | Trigger commit bf111b524e has a `Claude Opus 4.8` trailer. Then 12 single-commit `pr/never-crash-*` branches, each with a `Claude Opus 5.5` trailer, landed as squashes: #33 at 15:14 UTC, then #34–#59 (11 PRs) within 15 minutes, 17:25–17:40 UTC (13:25–13:40 −0400). PR #33: "Generated with Claude Code", "No reviews", "2 of 5 checks passed" | Brandon Thomas (author of all 12) | E09-C-004, E06-027 | How the split into 12 PRs was produced. Review of #34–#59 not fetched |
| Security findings (10-22 on main) | 27 `security(<crate>): …` commits with `Finding: <uuid> (CWE-NNN)` trailers; 11 of 27 add a `#[test]`. 0 of 27 name Claude, Codex or a generator | Dylan M. Taylor | E09-G-001..003 (errata #7: October, not `fix/sec-*`) | The tool that produced the findings. **Attribution unknown** |
| Agent issue-fix sweep (10-08/09) | 17 `claude/fix-<issue>-*` branches, 15 started on 10-08. Times from fix to main: 42 min → 5h11m | BFlat | E06-024, E09-B | Concurrency |
| Regression-test backfill (10-22/25) | "eight fixes merged without one" (72e11802d4) | skylar taylor-barrick (`test/backfill-*`) | 03 B.8 | AI involvement: no trailer, unknown |

### 2.10 (j) End-user agent via MCP (product feature, not a development role)

The product exposes its command registry to external agents over a control channel and an MCP server
(`docs/control-protocol.md`, `crates/automation`, from ae92ac20bf on 09-30; E09-A). README: "Built
for agents" (E08-001). This is a **product role**: agents *use* PhotoCraft. It has one development
side effect. Maintainers drive the app "through the control channel" to measure parity for epics
(#13458, E06-034), so the product's agent interface doubles as a test and measurement tool for
developers (INFERRED). Kept separate from §2.1–2.9.

---
## 3. Human–AI interaction patterns

Six working arrangements can be told apart in the data. Each one is a pattern observed in history; none
is documented as a practice.

### 3.1 Founder with agents, solo phase (09-30 → 10-03)
- **Evidence:** all 69 direct first-parent commits up to 10-03 are by Brandon Thomas (E06-012). The "one-shot" root (16941f7198, +42,241 lines) carries no trailer. Its AGENTS.md already contains "Parallel agents: use your own target dir (`CARGO_TARGET_DIR=target/agent-<name>`)" (16941f7198:AGENTS.md:56, E06-050). aa87012aab (10-02) has the subject "(+ in-progress work of other agents)". The first Claude trailer appears on 10-01 (1f1ddb2a47).
- **Numbers:** W40 had 124 non-merge commits, 84.7% of them AI-attributed (`E03_attr_weekly.csv`). Self-reported: "8 parallel agents" in one session (0c2d4bfd1a, docs/target-app-parity.md:322-343; E08-005).
- **Limits:** agents ran under the founder's git identity, so the agent count cannot be seen in git. How the one-shot was produced is unknown (03 U1).

### 3.2 Operator runs agent sweeps and agent-built batches, merges them himself (BFlat, 10-07 → 10-22)
- **Evidence:** 17 `claude/fix-<issue>` branches, 11 CI-only `claude/integ-batch` PRs, and 12 `Claude`-authored commits that BFlat committed to main (E06-010/021/024). PRs show "No reviews". Issue replies are Claude-generated (E09-B-002).
- **Numbers:** 96.6% AI-attributed; issue to fix on main in 42 min – 5h11m (E09-B table).
- **Limits:** the operator link rests on the committer field and the +07:00 tz (E06 open questions).

### 3.3 Maintainer drives high-volume AI-attributed work *and* holds the merge button (David Mann)
- **Evidence:** 964/978 non-merge commits AI-attributed (98.6%), 356 merge clicks, author of batch merges 13–20, the manual "(merge queue)", and machine-style epic filing (§1.1). 377 consecutive-commit pairs ≤5 min apart, 183 of them in disjoint code areas (E03-014).
- **Limits:** the burst metric fits parallel sessions and batch rebasing equally well (E03-014). No public statement by him exists (E08-031). This is the arrangement where author, integrator and merger are the same person-plus-agents, and no second human is visible on the sampled PRs he merged (#12237, #13234, E05-035).

### 3.4 Maintainer with no AI attribution who integrates (aiongg)
- **Evidence:** 0/430 trailers, 552 local `Merge PR #N:` merges, merger of batches 7–12 (E06-003). **New:** 13 `Codex`-identity commits arrived via his PR #8577 (§2.2). His 10-26 series has identical author timestamps (median gap 0.0 min, E03 §10), consistent with scripted commits.
- **Limits:** the 0% is "no trailer", not "no AI". The Codex-identity commits show that at least some of his landed work was agent-authored.

### 3.5 Maintainers with low attribution in reviewer, CI and release roles (FredApps, Dylan M. Taylor, Tanish Manku, skylar taylor-barrick)
- **Evidence:** 1.3–27% AI-attributed (§1.1). These four carry the visible review acts: approvals (FredApps), change requests (tanish2k09), "human review and a human merge are required" (#9363). They also own CI and release (§1.1).
- **Limits:** the review sample is ~22 PR pages (E05 §0.3, E06 §6, E09).

### 3.6 Fork contributors with assorted tools, and the per-author distribution
Finding: contributors split mostly into "almost always attributed" and "never attributed", with a
smaller middle group. VERIFIED (counts); the reason for the split is unknown.

Distribution (non-merge commits on main; humans only, so the AI identities `Claude`, `Codex` and
`Claude Opus 5.5` are excluded; aliases merged per `data/E03_alias_map.csv`; script
`work/D05/bimodal.py`, §New evidence):

| share of an author's non-merge commits AI-attributed | authors with ≥20 commits (n=65) | authors with ≥50 commits (n=28) |
|---|---|---|
| 0–5% | 20 | 10 |
| >5–25% | 9 | 3 |
| >25–50% | 7 | 4 |
| >50–75% | 2 | 1 |
| >75–<95% | 5 | 3 |
| 95–100% | 22 | 7 |

With ≥20 commits, 42 of 65 authors (65%) sit in the outer bins. Examples (`E03_attr_by_author.csv`):
- **≥95%:** David Mann 98.6, Higgs32584 100, Finn Newick 100, Trevor Brown 99.1, BFlat 96.6, vangel76 95.8.
- **0%:** aiongg, yoriswind, rmsff.
- **Middle:** Hector Villarreal 83.5, Brandon Thomas 76.0, Khawar Zamman Wani 33.2, Nigel Ihza Firdausy 30.7.

Tools named by contributors are mostly Claude strings. The minority strings are tied to individuals:
- Copilot + Copilot-Session: Alex Gorevski (10-07/08).
- Codebuff: Dylan M. Taylor and skylar taylor-barrick.
- Codex: jonathnwxh's most common string. The Codex identity appears in yoriswind's fork `codex/*` PRs.
- Fable 5.1: Trevor Brown.
- GPT-6: 22 commits 10-12..10-22.

(`E03_attr_models_summary.csv`, `E03_attr_by_author.csv`, E06-011.)

INFERRED: attribution reflects each contributor's tool defaults and habits, not a project rule. No
document requires trailers (E02 §5). So a 0% author is not evidence of manual work: yoriswind has 0
trailers yet 10 `Codex`-identity commits landed via his PRs.

### 3.7 Bot-authored branches opened by a human as "CI only" PRs
- **Evidence:** #1335 "CI only (do not merge): integration of community batch 1", "This draft PR exists only to run CI", opened and closed the same day by bflatastic. Its member PRs were squash-merged one by one (E06-021).
- **Function:** the agent assembled the batch, CI gave a combined verdict, and the human merged the members. The PR was used as a test harness, not as a review unit.
- **Limits:** batch tips were mapped to PR heads, but the merge order of members vs batch results is only partly traced.

---

## 4. RACI-style matrix

R = does the work, A = answerable / final say, C = consulted (gives input before), I = informed,
— = no evidence of a role.

Cell tags:
- **V** = VERIFIED documented rule (cited).
- **O** = OBSERVED pattern (cited).
- **U** = UNKNOWN: the role is plausible, but there is no evidence either way.

Cells are left as "—" or U rather than filled by assumption. The "AI coding agents" column covers AI
acting as co-author or identity (§2.1–2.5). "Review/triage bots" means CodeRabbit, SonarQube Cloud
and ticket-craft.

| Activity | Founder | Maintainers | Community contributors | AI coding agents | Review / triage bots | CI |
|---|---|---|---|---|---|---|
| Specify (what to build) | R/A O: ROADMAP, gaps.md, honest-parity doc (939c8f2c70, 433b84fae7) | R O: epics #13458 (David Mann); migration plan 14c059c971 (skylar) | R O: issues define fixes (#1381) | U: epic text "created from the measured spec" (#13458); author not attributed | C O: ticket-craft proposes epic split (E06-033) | — |
| Decompose | R O: 12 never-crash PRs (E09-C-004) | R O: epic child issues #13459–#13472 | — | R O (one contributor): "Fable 5.1 briefed" (`Model-Effort`, §2.4); otherwise U | — | — |
| Implement | R O: 76% AI-attributed | R O | R O | R O: 49.6% of non-merge commits attributed; 1.0% under AI identity | C O: 19 `coderabbitai[bot]` co-author lines (all refs) | — |
| Write tests | R O | R O: backfill campaign (72e11802d4) | R O | R O: 80.8% of AI-attributed commits touch tests vs 74.4% of non-attributed (E03 §7, heuristic) | — | — |
| Run local gate | — | U | U: self-reported "Validation"/"Not run" sections (#11059, #8452) | R V: "Before you finish" list addressed to agents (`AGENTS.md:145-168`); "Report only what ran" (`:12`); execution U | — | — |
| Review | U: early merges "No reviews" (#33, #1261) | R O: FredApps approvals, tanish2k09 change requests; rare (4 approved PRs in ~22 pages) | — | R O (self-reported): reviewer + attacker agents (#9386); first-pass automated review (eliets2, #12237) | R O: CodeRabbit on all sampled PRs from 10-19 (E06-040), advisory | U: checks run on every sampled PR, but whether they are required is unresolved (merges with 2 of 5 and 4 of 7 passed; 01c-errata #14) |
| Approve | A O (to 11-02) | A O: approval or "ready to merge" label (#11062); "a person is accountable" V (`AGENTS.md:6`) | — | — | — (not blocking, E05-030) | U: not established that checks gate merges (01c-errata #14) |
| Merge | R/A O: 2 merge clicks; squash merges of #1261, #2792 | R/A O: 597 of 603 merge clicks by 8 people (`E03_mergepr_by_merger.csv`) | — | R O (rare): 14 first-parent commits committed by `Claude` (E03-006) | — | — |
| Resolve conflicts | — | A O: batch mergers | — | R O: Claude-trailered conflict merges (38609e5615, 2c82295e4c) | — | — |
| Fix red main | R O: `fix/main-*` with Claude trailer (E05-052) | R O: "Fix main" commits 11-11 (a3c2f2e299) | R O: Zuujis #5941 | R O: `claude/fix-main-*` (author `Claude`, E05-052) | — | I O: main runs never cancelled (07174271d5) |
| Cut release | R/A O: v0.1.0..v0.20.1 | R/A O: Dylan, FredApps from v0.20.2; publish draft V (`docs/releasing.md:3-6`); stop-and-ask V (`AGENTS.md:14`) | — | R O: d43db3e153 authored by `Claude`; 26/29 version bumps AI-trailered (E05-065) | — | R O: `release.yml` builds and signs; nightly dry run (f1b5e7d727) |
| Triage issues | U | R O: labels (aiongg on #7848; tanish2k09) | R O: reporters | U | R O: ticket-craft labels, duplicates, "in progress" links (E06-033) | — |
| Update trackers | R V: "update the parity doc and gap entry … with the date" (`AGENTS.md:127-143`) | R O: central scorecard regeneration at the batch gate (38609e5615) | R O: <14% of code commits touch a tracker (E06-031/032) | R V (rule addressed to agents); observed share U | — | A O: `scorecard --check` fails stale scorecard (E05 §0.2) |
| Change agent rules (AGENTS.md) | R/A O: 22 of 38 revisions (recount) | R O: house-rules import (FredApps, 7d8648dfcb); CI section (Dylan) | R O: bfenty #779 | R O: 19 of 38 revisions carry a Claude trailer (recount; E02-026 says 21) | C O: CodeRabbit comment → rule edit (0d9a9a5a70) | R O: `house-rules.yml` checks the copied block |
| Change CI | R O: 23 workflow commits | R/A O: Dylan, Ivan, FredApps, aiongg; V: "Don't add or change CI in a feature or fix PR" (`AGENTS.md:16`) | R O (pre-rule): perf jobs by Khawar Zamman Wani (E05-012) | R O: ≥39% of non-merge workflow commits AI-trailered (45/114, E05-002) | C O: Sonar rule IDs drove CI fixes (E05-031) | — |

Reading: the A column for review and approval is thin. The only documented "A" is the generic
accountability rule, and no mechanism ties it to a named person per PR. INFERRED from the empty
CODEOWNERS and approval policy (E02 §6) and the samples above.

---
## 5. Supervision and accountability

Finding: supervision is written down as norms for each agent operator, added on 2026-11-06. Its only
mechanical backing is CI checks (whether they are required for merge is unresolved, 01c-errata #14) and the
release environment. Human review before merge is
visible in a minority of the sampled PRs.

### 5.1 Documented (rule)

| Rule (verbatim excerpt) | Location | Since | Check |
|---|---|---|---|
| "**A person is accountable.** Whoever runs an agent answers for what it opens and for its review comments." | `AGENTS.md:6` | 7d8648dfcb, 11-06 | none |
| "**Review the diff before opening a pull request.**" / "**Report only what ran.**" | `AGENTS.md:10`, `:12` | 11-06 | none |
| "**`main` changes through a pull request.** Do not push to it. Branch protection enforces this." | `AGENTS.md:13` | 11-06 | branch protection not visible in git |
| "**Stop and ask only about** licensing outside the allowlist, publishing, releases, a new remote, secrets, spending money, destructive git, and anything else hard to undo. Otherwise keep working." | `AGENTS.md:14` | 11-06 | releases are partly mechanical (draft + `release` env, E02 §4) |
| "Respond in 7 days … A maintainer decides closure; it is never automatic." | `AGENTS.md:19` | 11-06 | none |
| "**No agent attribution.** A pull request does not say an agent wrote it. A repository rule may not require that." | `AGENTS.md:20` | 11-06 | none |
| "**Human** marks what an agent can't finish alone." | `docs/gaps.md:15-16` | 939c8f2c70, 10-10 | — |

Before 11-06 no AGENTS.md revision listed human-approval points (E02-009, checked diff by diff).
Org RFC-0006 explains the rules as answers to agent failure modes: "duplicate PRs, fixes for bugs
already fixed on `main`, PRs left as drafts, or code that uses functions that don't exist"
(craft-contrib, external repo, WebFetch, E08-028).

### 5.2 Observed

| Observation | Evidence | Label |
|---|---|---|
| Self-merges with no reviews | #113 (echelon, release PR), #13414 (dylanmtaylor, 24 checks), #1344/#1421 (bflatastic, agent-authored) | OBSERVED (WebFetch), E05 §0.3, E09-B-002 |
| Merges with "No reviews" and not all checks reported passed (skipped jobs may count as not passed, errata #14) | #33 "2 of 5 checks passed"; #1421 "4 of 7 checks passed" | OBSERVED (WebFetch), E06 §6, E09-B-002 |
| Labels as approval | "ready to merge" = "Reviewed: correct, complete and tested; waiting for a maintainer to merge". Applied and then merged by the same maintainer (#11062) | OBSERVED, E06-030/041 |
| Agent review replacing human approval on a batch | #9386: agent reviewer + attacker claimed; merged by aiongg; no human approval visible | OBSERVED (self-reported method), E06-022 |
| Explicit approvals | FredApps on #7848, #11641, #8452. Dylan M. Taylor approved #9363 twice | OBSERVED, E06 §6, E05 §0.3, E09-E-002, E09-G-003 |
| Human gate before merge | #13396 "Please don't merge yet: a manual test in the real app is planned" | OBSERVED, E06-043 |
| Post-merge human testing | skylartaylor found three artboard problems on main after #10512/#10538, fixed in #11441 | OBSERVED, E09-H-002 |
| Direct pushes to main after PRs began | Dylan's 32 `security(...)` commits on 10-22; release commits; all before rule 8 | OBSERVED, E06-026 |

Rate: across the ~22 PR pages read (10 in E06, 6 in E05, ~6 in E09: #1421, #8417, #8452, #9363, #10426, #11441), 4 merged or decided PRs show an explicit
human approval (#7848, #11641, #8452, #9363). The others show labels, comments or nothing. The sample
was chosen by hand, not at random, so this is not a rate estimate (INFERRED).

### 5.3 The "no human review" remark vs the documented rule

- **Developer statement (self-reported, scope ambiguous):** "We're leaning in with 100% AI software factory and no human review. We're making lots of revenue too. The era of human always in the loop software is over." (HN 50434834, 2026-11-10, account `echelon`; E08-016).
- **Documented rule, in force four days earlier:** "A person is accountable" (`AGENTS.md:6`, 11-06).
- **Reconciliation (INFERRED):**
  1. The remark does not name PhotoCraft, and "revenue" points more to ArtCraft's commercial product (E08-016).
  2. The rule demands *accountability*, not *review*: an operator can answer for an agent's PR without anyone reading it.
  3. The observed record has both. There are merges with no visible review (§5.2) and maintainer approvals and change requests, the latter mostly after mid-October.
- **Conclusion:** the record neither proves nor refutes the remark for PhotoCraft. Founder-era merges (#33, #1261, #2792: "No reviews") match it. The maintainer era partly does not.

### 5.4 The attribution conflict

| Side | Text / data | Source |
|---|---|---|
| Product credits models from trailers | "**About ▸ Models** credits the AI models named in `Co-Authored-By` trailers." Snapshot counts: anthropic/claude-opus/5.5 736 commits, etc. | `docs/contributors.md:3-4`; `contributors/contributors.json` (head 9d3ba499ad); E06-006, E08-010 |
| Credits are regenerated per release | "nothing regenerated contributors/contributors.json before a release" → fixed | daa9a01955 (11-05), E05-064 |
| House rule 15 | "No agent attribution. A pull request does not say an agent wrote it." | `AGENTS.md:20`, 11-06 |
| Practice after the rule | `Co-Authored-By: Claude` on 498 of 1,799 main commits since 11-06 (vs 4,145 of 10,418 before; date-only windows, see errata #28: with an exact cutoff at 7d8648dfcb, 499 of 1,805); "Generated with Claude Code" still in davidmann4's #13396 (11-12) | E02-016, E06-042 |

INFERRED: the rule addresses PR *text*, not commit trailers (E02-011). So the two are compatible
in the letter but opposed in effect. Everything that discourages disclosure erodes the data the
Models screen and any audit depend on. The falling trailer share after 11-06 cannot be attributed to
the rule, because the contributor mix changed too (E02-016, E05-073).

---

## 6. What cannot be established

| Question | Why not | Closest evidence |
|---|---|---|
| Number of agents running at any moment | Agents run under human git identities; session trailers cover a minority of commits; author dates survive rebases | Self-reported "8 parallel agents" (10-02) and "10–20 concurrent agents" (10-10) without method (E08-003/005); ≤15 distinct session ids on one day (E06-011); 504 landed PRs in flight on 10-13 (E06-051) |
| Orchestration tooling | No harness config on any ref; `plan/` and `log/devlog.md` gitignored | "vanilla Claude Code" (HN 50029182); `Model-Effort` driver/briefer/writer (one contributor); fork CLAUDE.md "Delegation" never merged (E02-022) |
| How much each human reads before merge | Squash mergers are not in git; branch protection not visible; ~22 PR pages sampled via summaries | §5.2 |
| Autonomy level per agent | No permission files; the stop-and-ask list is prose | `AGENTS.md:14`; anti-stall "Do not ask for it and do not stop when it is absent" (`:186`, E02-010) |
| AI share of the ~50% unattributed commits | Absence of a trailer = unknown; rule 15 discourages disclosure | Codex-identity commits in 0%-trailer authors' PRs (§2.2) |
| Who operated d43db3e153 (Claude release commit) and the security-finding tool | No attached human or tool named | E06-005, E09-G-002 |
| Whether ticket-craft or CodeRabbit used LLMs on this repo | Configuration lives outside the repo | E06-033, `.coderabbit.yaml` |
| Whether "reviewer + attacker" agents were used beyond batch 8 | Review outputs not committed; only one PR page read | E06-022, 03 U6 |
| Whether `davidmann4` issues were agent-filed | No attribution on the list page | E06-030 |

---

## 7. Role design lessons and a PROPOSED role model

### 7.1 Lessons (INFERRED, tied to evidence)

1. **Implementation scales with agents. Merge authority did not.** 582 authors fed 8 merge-clickers, and one person took 59% of merge clicks (E03-008). Median merge-commit PR lifetime was 52 h, and 68 h for PRs landed in November (E06-013). The bottleneck moved to integration, which the project then automated with agent-built batches (§2.5).
2. **When the integrator is also the AI-heavy author and the merger, no second party is visible.** David Mann merged fork PRs with no approval shown (E05-035), and his batch PR #9386 relied on agent review (E06-022). Red-main clusters followed merge waves (11-11: 11 "Fix main" commits, E03-013). This is a separation-of-duties gap, not a quality verdict.
3. **Rules that name a role but not a person are unenforceable.** "A person is accountable" has no CODEOWNERS file, approval count or per-PR accountable field behind it (E02 §6). Compare the gates that did change behaviour: `panic_hunt`, lavapipe fail-on-skip and panel-commands, all mechanical (E05-071).
4. **Agent review exists, but it leaves no record.** The reviewer/attacker method (#9386) is the most interesting role in the data, and the least auditable: its findings were not committed (03 U6).
5. **Provenance is the cheapest role evidence, and it was partial and later discouraged.** Session trailers cover 274 commits on main (errata #1). `Model-Effort` was used by one contributor. Rule 15 pushes against disclosure (§5.4). Without these trailers the questions in §6 cannot be answered even in principle.
6. **Bots took on triage and first-pass review successfully but stayed advisory.** CodeRabbit findings changed code and even rules (0d9a9a5a70), yet did not block merges (#12237) (E05-030). The design choice to keep it advisory is defensible. The gap is that no human approval took its place.
7. **Humans kept the irreversible steps:** release publication, signing secrets, stop-and-ask items and the "Needs a human" list (§1.2). This held up. The one exception is the AI-authored release commit d43db3e153, which was still published by a human-held draft step by rule.

### 7.2 PROPOSED role model

**PROPOSED — not a PhotoCraft practice.** It is aligned with `08-playbook.md` §2 (Planner, Implementer,
Independent test author, Verifier, Integrator, Release agent, Triage agent, Human owner) and keeps
that playbook's separation rules ("No role approves work produced in its own session"). It differs from
08 §2 in four places, listed after the table.

| Role | Kind | Responsibility | Must never | Gap it fixes (evidence) |
|---|---|---|---|---|
| Human owner / accountable person | human, named per PR | listed in an `Accountable:` trailer; approves at the risk tier set in 08 §9 | approve a PR whose agent session they ran, for tier ≥ medium | accountability rule without a named person (§5.1, lesson 3) |
| Planner / spec author | agent or human | task spec with owned files and acceptance tests (08 §2) | write production code | epics as work queues exist (#13458), but specs are not committed (03 B.9) |
| Implementer | agent | code + tests + gate log + "not run" list | push to main; mark own work reviewed | "Report only what ran" is prose only (§5.1) |
| Independent verifier (reviewer + attacker) | agent, separate session | reviews against the spec; reverts the implementation and confirms its tests fail; **commits the review record** (`reviews/<PR>.md` or a PR-comment link in a trailer) | review its own session's work | #9386 method unrecorded (lesson 4) |
| Integrator | agent | builds the batch, resolves conflicts with per-file notes, regenerates generated files, runs the gate on the union | squash away member provenance | matches observed batches 7–20 (E06-022) |
| **Merge steward** | human, ≠ the integrator's operator | merges a batch only after checking the verifier records and the union gate; owns post-merge green-main for 24 h | merge a batch they authored or operated | author = integrator = merger (lesson 2); 11-11 red-main cluster (E03-013) |
| Release manager | human | publishes the draft; holds signing secrets | delegate publishing | already true by rule (§1.2) |
| Triage bot | bot | labels, duplicates, claim links, split proposals | close issues or set `priority: critical` without a human | ticket-craft (E06-033) |
| Review bot | bot | first-pass findings in agent-consumable form | count as an approval | CodeRabbit advisory (E05-030) |

Provenance trailers, kept rather than banned (PROPOSED). Every agent-produced commit carries:
- `Co-Authored-By: <model>`;
- `Agent-Session: <id>`;
- `Agent-Role: implementer|verifier|integrator|…` (a generalised `Model-Effort:`);
- `Accountable: <handle>`.

A CI check rejects commits whose body names an agent tool but lacks `Accountable:`. PR prose may stay
free of attribution, so the intent of rule 15 is kept for PR text. The audit data that About ▸ Models
and §6 need is kept too.

**Where this differs from 08 §2, and why:**
1. It adds a separate human **merge steward**. 08 §2 gives merge rights to the "Human owner" generally. Here the evidence shows that one human acting as AI-heavy author, integrator and merger was the actual pattern (§3.3), so the model makes the merger distinct from the integrator's operator.
2. It requires the verifier to **commit** its review record, because the one observed instance left none.
3. It adds an `Accountable:` trailer. 08 §13 covers provenance in general; this names the person.
4. It keeps the playbook's independent test author as optional. PhotoCraft gives no evidence for or against that role, so its value here is unproven. 08 keeps it for other reasons (E07-018).

---

## Confidence and gaps

- **Strongest:** authorship, merge-click and trailer counts (git, scripted, reproducible); `Model-Effort` and Codex-identity landing paths (recomputed here); the rule texts (hash-verified AGENTS.md).
- **Weakest:** everything about review. It rests on WebFetch summaries of ~22 hand-picked PR pages, with no branch-protection data. The operator links (BFlat ↔ Claude commits; the founder ↔ d43db3e153) rest on committer fields and timezones. The "reviewer + attacker" method is a single self-report.
- **Not checkable:** squash-merge clickers (2,690 PRs), permission and autonomy settings, `plan/` and `log/devlog.md`, third-party bot configuration, prompts.
- **What would change conclusions:** branch-protection settings with required approvals (would weaken lessons 2–3); committed review records from batch agents (would turn lesson 4 around); a full crawl of PR pages for approvals (would replace the sample-based §5.2).
- **Evidence inconsistencies resolved:**
  - Session counts follow errata #1 (274/238; E08's 304 not reproduced).
  - E06 lists BFlat as 84/86 non-merge while E03 gives 84/87 (alias merging); E03 is used.
  - E02-016 counts 27 `Model-Effort` commits and E03 counts 25: the difference is merges (25 non-merge + 2 merges, verified here).
  - E06-025's statement that `Codex` "is not on the in-repo `codex/*` branches" holds, but the identity *does* sit on fork `codex/*` branches (yoriswind) and in aiongg's PR #8577 (new).
  - E06 says aiongg "carries no AI attribution". That is correct for trailers, but 13 Codex-identity commits reached main through his PR.

## New evidence gathered during synthesis

Run at pin `74330157cb` in the upstream clone. Scripts are in
`/tmp/claude-0/-home-user-photocraft-study/7ff807c1-b52f-5813-9884-82f19c193950/scratchpad/work/D05/`.

1. **`Model-Effort:` authorship.** `git log main --grep='^Model-Effort:' --format='%an|%P'` gives 27 commits, all by Trevor Brown (25 non-merge + 2 merges), first b29fdc5a29 (2026-11-08 UTC; author date 11-07), last cbd96a4de6 (2026-11-11).
2. **Model-Effort landing.** `landing.py <clone> '^Model-Effort:' grep` maps each commit to the first-parent commit that brought it in. All 27 landed via `Merge pull request #… from TrevorBrown-dev/…` commits authored by David Mann: #12815 (6), #12298 (5), #12212 (5), #12402 (3), #13073 (2), #12299 (2), #13215, #13150, #12382, #12274 (1 each).
3. **`Codex` identity landing.** `landing.py <clone> '^Codex <' author` gives 24 commits on main, author dates 10-17 → 11-07:
   - 13 via merge 6d807ba34c "Merge pull request #8577 from aiongg/r4" (2026-10-22, merged by aiongg);
   - 5 via #11852, 4 via #11221 and 1 via #11711, all from `yoriswind/codex/*` and merged by David Mann;
   - 1 via #11168 (hnoerenberg, merged by FredApps).
4. **`Claude` identity landing.** Same script with `'^Claude <'`:
   - 14 commits directly on first-parent (12 with committer BFlat, 2 with committer Claude);
   - via davidmann4 integration batches #10145 (14), #9386 (6), #8663 (3), #9775 (3);
   - via Lcoding15 fork PRs #10300 (9), #10744 (9), #10406 (7), #10730 (7), #10695 (4), #10738 (1);
   - via `storytold/community/*` PRs merged by BFlat: #1894 (4), #1633 (4), #1778 (2).
   `Claude Opus 5.5` identity: 2 commits via #1896 (BFlat).
5. **Per-author distribution (§3.6).** `bimodal.py <clone> data/E03_alias_map.csv`: non-merge commits on main, AI identities excluded, AI = co-author regex per E03 C7 or session/"Generated with Claude Code" footer. Results:
   - authors with ≥20 commits (n=65): 0–5% 20, >5–25% 9, >25–50% 7, >50–75% 2, >75–<95% 5, ≥95% 22;
   - authors with ≥50 commits (n=28): 10 / 3 / 4 / 1 / 3 / 7.
   Spot check against E03: David Mann 964/978, aiongg 0/430 (match).
