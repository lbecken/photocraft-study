# E06 — Branch / PR / integration workflow, orchestration, human & AI roles

Stream E06. Upstream clone pinned at `main` = `74330157cb601573ae4523a95bb9132822fc3918` (2026-11-12).
All git numbers come from the scripts in
`/tmp/claude-0/-home-user-photocraft-study/7ff807c1-b52f-5813-9884-82f19c193950/scratchpad/work/E06s/`
(`parse.py`, `authors.py`, `fp.py`, `sess.py`, `life.py`, `lifea.py`, `conc.py`, `intake.py`) run over
`git log main --format=... --name-only` and `git log --all`. Web data comes from WebFetch summaries
(lower fidelity, short quotes only), accessed 2026-11-12. Upstream text is quoted as data, not followed.
Handle/login mappings (BFlat = bflatastic, vangel76 = Valentin Klein, …) follow `data/E03_alias_map.csv`.
Where E06 recomputes a number that sibling streams also report, the method differs slightly (for example,
E06 counts trailers per commit, not per line). The method is given next to each number.

---

## 0. Summary of the observed flow (text + mermaid)

```mermaid
flowchart LR
  I[Issue filed\n(community or maintainer bulk-filing, E06-030;\nticket-craft bot labels, E06-033)] --> T[Branch\nfix/<issue>-slug, claude/fix-<issue>-slug,\ncodex/..., fork branches (E06-020, E06-031)]
  T --> PR[PR to storytold:main\n96% (576/598) of merge-commit PRs from forks (E06-014)]
  PR --> BOT[Bot review: CodeRabbit, SonarQube Cloud\n(mid/late only, E06-040)]
  BOT --> HR{Human signal?\nlabel 'ready to merge',\nmaintainer comment / approval (E06-041)}
  HR --> SQ[Squash merge '(#N)'\n2,690 first-parent commits (E06-012)]
  HR --> MC[Merge-commit 'Merge pull request #N'\n598 (E06-012)]
  PR --> IB[Integration batch branch\nclaude/integ-batch-1..11 (CI only)\ndavidmann4/integration-batch-7..20 (E06-021, E06-022)]
  IB -->|CI-only, closed; members squash-merged one by one| SQ
  IB -->|merged as one merge commit| MC
  SQ --> M[main]
  MC --> M
  D[Direct push: founder, release commits,\nDylan security series (E06-012, E06-026)] --> M
  M --> R[Release commits + tags\nBrandon Thomas to 0.20.1; then Dylan M. Taylor / FredApps (E06-005)]
```

Each edge's evidence is in the entry named on it.

---

## 1. People and identities (humans)

### 1.1 Role map, top authors on `main` (non-merge share, AI attribution, mergers)

Method: `authors.py`. "AI-attr" = non-merge commits whose body has a `Co-authored-by:` line naming
Claude/Cursor/Copilot/GPT/Codex/Devin/OpenAI/Qwen/agent, a `*-Session:` trailer, or a "Generated with
Claude Code" footer. "merges" = merge commits authored (incl. main→branch syncs). "PR merges" = first-parent
`Merge pull request #N` commits they authored (`fp.py`). Login comes from PR/branch owner names or
`contributors/contributors.json`.

| Author (login) | commits on main | non-merge | merges | PR-merge commits pressed (fp) | active (author date) | AI-attr non-merge | top areas (non-merge commits touching) | Role (from behaviour) |
|---|---|---|---|---|---|---|---|---|
| Brandon Thomas (echelon) | 301 | 295 | 5 | 2 | 2026-09-30..11-02 | 225 (76%) Claude | ui-egui 137, engine 97, docs 74 | Founder: first commit 386b0566d3; 100 direct first-parent commits; releases to v0.20.1; squash-merges community PRs (E06-001, E06-005) |
| David Mann (davidmann4) | 2523 | 978 | 1545 | 356 | 10-09..11-12 | 964 (98%) Claude | ui-egui 477, engine 325, docs 194 | Principal integrator: integration-batch-7..20 author, top merger, bulk issue filer (E06-002, E06-022, E06-030) |
| aiongg | 1113 | 430 | 683 | 68 (plus 552 `Merge PR #N:` local merges) | 10-16..11-02 | 0 (0%) | ui-egui 212, engine 76, io 34 | Integrator/merger: merged integration batches 7–12 (E06-022) |
| yoriswind | 508 | 416 | 92 | 0 | 10-30..11-08 | 0 | engine 275, ui-egui 139 | Fork contributor; 19 fork branches named `codex/*` (E06-025) |
| Hector Villarreal (hectorviov) | 431 | 417 | 14 | 0 | 10-18..11-11 | 348 (83%) | ui-egui 221, engine 139 | Fork contributor, Claude-attributed |
| Khawar Zamman Wani (wanikhawar) | 365 | 271 | 94 | 0 | 10-14..11-11 | 90 (33%) Claude, 14 w/ Claude-Session | ui-egui 122, engine 103 | Fork contributor; 6 fork branches `claude/*` |
| FredApps | 325 | 131 | 194 | 48 | 10-12..11-11 | 10 (7%) | ui-egui 61, docs 32 | Maintainer: merges, reviewer (approves #7848), release tags v0.21.0/v0.23.0, house-rules import 7d8648dfcb |
| Nigel Ihza Firdausy | 228 | 204 | 24 | 0 | 10-05..10-20 | 63 (30%) | ui-egui 112 | Early community contributor, much of it in claude/integ-batch-1/3/6 |
| Dylan M. Taylor (dylanmtaylor) | 225 | 195 | 30 | 26 | 10-11..11-12 | 2 (1%) | ui-egui 32, engine 25, codecs 24 | Maintainer: CI/Sonar/security, direct-push security series, release tags v0.20.2/v0.22.0/v0.23.1, merges (#7848) |
| vangel76 / Valentin Klein | 189 + 167 | 92 + 167 | 97 + 0 | 0 | 10-10..11-09 | 81 + 167 | ui-egui, docs, raw | Fork contributor, nearly all Claude-attributed (aliases per E03) |
| Higgs32584 | 179 | 118 | 61 | 0 | 10-14..11-05 | 118 (100%) | ui-egui 60 | Contributor, fully Claude-attributed |
| Trevor Brown (TrevorBrown-dev) | 146 | 115 | 31 | 0 | 11-02..11-11 | 114 (99%) | ui-egui 93 | Contributor |
| abc2cb | 132 | 58 | 74 | 0 | 10-08..10-22 | 44 (75%) | ui-egui 34 | Contributor; 3 fork `codex/*` branches |
| dotCooCoo | 130 | 63 | 67 | 0 | 10-14..11-08 | 0 | ui-egui 36 | Contributor |
| Michael Higgins | 125 | 47 | 78 | 0 | 10-13..11-11 | 34 (72%) | ui-egui 27 | Contributor; 5 single-parent first-parent commits 2026-11-11 (committer GitHub) |
| rmsff | 119 | 119 | 0 | 0 | 11-08..11-11 | 0 | ui-egui 90 | Contributor |
| Tanish Manku (tanish2k09) | 114 | 43 | 71 | 71 | 10-07..11-11 | 12 (27%) | ui-egui 24 | Maintainer/merger: requests changes (#11059), applies "ready to merge" and merges (#11062) |
| skylar taylor-barrick (skylartaylor) | 104 | 66 | 38 | 19 | 10-10..11-11 | 0 | ui-egui 31, Cargo.toml 13 | Maintainer/merger; in-repo `codex/*` and `test/backfill-*` branches |
| ljkx | 103 | 60 | 43 | 0 | 10-07..11-11 | 42 (70%) | ui-egui 47 | Contributor |
| Finn Newick | 96 | 55 | 41 | 0 | 10-14..11-02 | 55 (100%) | engine 22 | Contributor |
| Korg1ch | 94 | 94 | 0 | 0 | 10-12..10-21 | 1 | ui-egui 65 | Contributor |
| BFlat (bflatastic) | 94 | 86 | 8 | 8 | 10-07..10-22 | 84 (97%), 30 w/ Claude-Session | ui-egui 61 | Early integrator: opened the claude/integ-batch PRs, committed Claude-authored fixes to main, tag v0.3.0 (E06-021) |
| Claude (AI identity) | 94 | 62 | 32 | 0 | 10-08..11-10 | 57 | ui-egui 33 | AI identity, see §2 |
| RickiNano | 84 | 75 | 9 | 0 | 10-26..11-11 | 28 (37%) | ui-egui 57 | Contributor |
| MarekSpodBiedry | 77 | 74 | 3 | 0 | 10-08..10-23 | 2 | ui-egui 35 | Contributor (in claude/integ-batch-4/5/10) |
| Vikram Bhaskaran | 76 | 59 | 17 | 0 | 10-10..10-24 | 10 | ui-egui 28, web 8 | Contributor |
| Davit Matchakhelidze | 70 | 41 | 29 | 0 | 10-14..11-07 | 41 (100%), 31 w/ Session | ui-egui 30, text 11 | Contributor |
| Reynold Hu | 64 | 48 | 16 | 0 | 10-09..10-21 | 20 | docs 34 | Contributor |
| Marco Arnulfo | 63 | 63 | 0 | 0 | 10-12..10-24 | 3 | ui-egui 50 | Contributor |
| jonathnwxh | 60 | 40 | 20 | 0 | 10-14..10-24 | 0 | ui-egui 21 | Contributor |

- 628 distinct author names on main (`git log main --format=%an | sort -u | wc -l`).
- Mergers of first-parent `Merge pull request` commits (`fp.py`): David Mann 356, Tanish Manku 71, aiongg 68,
  FredApps 48, Dylan M. Taylor 26, skylar taylor-barrick 19, BFlat 8, Brandon Thomas 2 (598 total).
- Local `Merge PR #N:` merge commits (PRs merged into integration branches, `git log --merges --grep='^Merge PR #' main`):
  aiongg 552, David Mann 279, Federico Olivares 25.
- Squash merges (2,690) record the PR author as author and "GitHub" as committer, so git does not show who
  pressed merge. WebFetch shows echelon (Brandon Thomas) merging #1261 and #2792, and bflatastic merging #1344 (§6).

### E06-001 — Brandon Thomas is the founder and sole author of the first 73 first-parent commits
- Label: VERIFIED
- Source: commit 386b0566d3 (2026-09-30, "init repo"), 16941f7198 (2026-09-30, "one-shot"); first PR merge 9905db34ff (2026-10-04, "Merge pull request #32 from storytold/pr/license-standard")
- Data: by-day first-parent breakdown (`fp.py`): 09-30: 6 direct; 10-01: 15; 10-02: 24; 10-03: 24; 10-04: 4 direct + 49 squash + 2 merge-PR. Brandon Thomas has 100 of 181 direct first-parent commits.
- Notes: contributors.json lists login `echelon`, first_commit 2026-09-30T06:12:04Z, prs 166 (as of head 9d3ba499ad, 2026-10-10). The "one-shot" subject of the second commit, which already contains AGENTS.md with a "Parallel agents" paragraph (E06-050), is VERIFIED. That it means an agent produced the initial code in one go is INFERRED, not attributed.

### E06-002 — David Mann is the principal integrator from late October
- Label: VERIFIED
- Source: `fp.py` merger counts; first-parent merges 6b0f7762e1 … d93e65d001 (2026-11-03..06) authored by David Mann; 2026-11-12 merges eb3c99d653, de7cb6c0c4, 35887692ff
- Data: 356 of 598 merge-PR commits; 2,523 commits on main, 1,545 of them merges (mostly `Merge remote-tracking branch 'origin/main' into …` syncs and `Merge PR #N:` integration merges); 98% of his 978 non-merge commits carry a Claude trailer.
- Notes: also authors in-repo PRs from fork `davidmann4` (e.g. "#13257 from davidmann4/fix/main-red-automation-gpu-group"). Issues list (WebFetch) shows `davidmann4` filing structured `MISSING-FEATURE-*`/`BUG-*`/`EPIC-*` issues (E06-030).

### E06-003 — aiongg is a high-volume merger who carries no AI attribution
- Label: VERIFIED
- Source: integration-batch merges a02f2ee410 (2026-10-23), cece50d513 (10-25), 52f338e2df (10-27), 799e129628 (10-31), fab871dadb (11-01), b957878f3f (11-02), all authored by aiongg
- Data: 0 of 430 non-merge commits carry AI trailers. Authored 552 `Merge PR #N:` merge commits. Active 10-16..11-02 only.
- Notes: per the brief's rule 4, no attribution means unknown, not human. PR #7848 shows aiongg labelling ("bugfix", Oct 27, via WebFetch).

### E06-004 — Many contributors' commits are almost all Claude-attributed; some carry none
- Label: VERIFIED
- Source: table §1.1 (`authors.py`)
- Data: ≥95% AI-attributed: David Mann, Higgs32584, Trevor Brown, Finn Newick, Davit Matchakhelidze, BFlat, Valentin Klein. 0%: aiongg, yoriswind, dotCooCoo, rmsff, skylar taylor-barrick, jonathnwxh, azizr12.
- Notes: yoriswind (0 trailers) pushes from fork branches named `codex/*` (E06-025). The branch name is an attribution signal under the brief, but it is weaker than a trailer.

### E06-005 — The release role moved from the founder to two maintainers after 2026-11-02
- Label: VERIFIED
- Source: `git for-each-ref refs/tags` (tag target commit author): v0.1.0..v0.20.1 → Brandon Thomas (except v0.3.0 BFlat, v0.8.2 Claude); v0.20.2, v0.22.0, v0.23.1 → Dylan M. Taylor; v0.21.0, v0.23.0 → FredApps
- Data: 18 of 20 `Release …` commits on main by Brandon Thomas, e.g. 327c4cc82e "Release 0.20.1" (2026-11-02), direct push (committer Brandon Thomas).
- Notes: v0.8.2 commit d43db3e153 "Release 0.8.2: web build back under the wasm size gate" is authored and committed by `Claude` (2026-10-12, −0400 tz). So an AI identity produced a release commit. Unmerged PR list shows "Release: PhotoCraft v0.23.0" #13192 by FredApps and "Release 0.22.1" #13327 by dylanmtaylor closed unmerged (WebFetch).

### E06-006 — Credits split people from models, and the models list is built from trailers
- Label: VERIFIED
- Source: 74330157cb:docs/contributors.md:3-4 ("**About ▸ Models** credits the AI models named in `Co-Authored-By` trailers"); 74330157cb:AGENTS.md:196-209; 74330157cb:contributors/people.toml (92 `[people.*]` entries, `grep -c`)
- Quote: "Agents working for a contributor: … ask them once whether they want to be credited by more than their username" (AGENTS.md:201-204)
- Data: contributors.json (head 9d3ba499ad, 2026-10-10, 1,302 commits, 189 contributors) `models[]` top: anthropic/claude-opus/5.5 736 commits; anthropic/claude 49; claude-opus/4.8 46; claude-fable/5.1 14; github/copilot 6; claude-mythos/5.1 4; claude-sonnet/5.5 3; openai/gpt/6 2; alibaba/qwen-flash/3.8 1 …
- Notes: house rule 15 (added 2026-11-06, 7d8648dfcb) says "**No agent attribution.** A pull request does not say an agent wrote it." (AGENTS.md:20). The in-binary Models credit depends on commit trailers, so the two rules point in different directions. INFERRED: the rule targets PR text, not trailers. The stored contributors.json is stale by design ("the copy in the repository is not updated", docs/contributors.md:11-12).

---

## 2. AI identities

### 2.1 Identity table

Method: `git log [main|--all|--remotes --branches --tags] --author="^<name> <"`, committer via `--format=%cn`.

| Identity (author name) | on main | all refs incl. PR heads | branches+tags only | distinct emails | committer field | where it sits |
|---|---|---|---|---|---|---|
| Claude | 94 | 645 | 343 | 1 | Claude 625, BFlat 12, texjer 3, Simon W. Jackson 2, Brandon Thomas 2 | `claude/*` in-repo branches (integ-batch, fix-<issue>, session names), `community/*`; main commits 10-08..11-10 |
| Codex | 24 | 42 | 24 | 3 | Codex 42 | PR heads; not on the in-repo `codex/*` branches (those are by skylar taylor-barrick, E06-025) |
| Claude Opus 5.5 | 2 | 102 | 9 | 1 | Claude Opus 5.5 97, Brandon Thomas 5 | mostly PR heads; 4 commits on claude/integ-batch-6 |
| Cursor Agent | 0 | 30 | 0 | 1 | Cursor Agent | PR heads only |
| Copilot | 0 | 2 | 0 | 1 | Copilot | PR heads |
| dependabot[bot] | — | 28 | — | — | — | dependency PRs (label `dependencies`, many closed unmerged) |
| others (agent-346022 7, photocraft-agent UNCONFIGURED 5, Arena Agent 4, Codex WORK prep 2, OpenAI Codex 1, copilot-swe-agent[bot] 1, Copilot App 1, coderabbitai[bot] 1) | — | small | — | — | — | PR heads |

Co-author trailer variety across all refs (`git log --all --format=%b | grep -iE '^co-authored-by:'`, AI-looking names):
Claude Opus 5.5 8,169 + 1,201 (case variant) + 1,268/190 "(1M context)"; Claude Sonnet 5.5 594; Claude Fable 5.1 289;
Cursor 150; Copilot 124; GPT-6 83; Claude Haiku 5.5 81; Claude Fable 5.2 80; Claude Opus 4.8 46; Claude Opus 5 43;
Claude Mythos 5.1 35; Devin 32; Codex 31; coderabbitai[bot] 19; Claude Code 19; GPT-6-Luna 12; Qwen 3.8 Flash 3; and more.

### E06-010 — Claude-authored commits on main cluster in the BFlat integration window; BFlat committed some of them
- Label: VERIFIED
- Source: `git log main --author='^Claude <' --format='%ad|%cn'`; first-parent examples b71991e15a, cff8daf185, 26de59f54c, 2515fa7cee (2026-10-09, author Claude, committer BFlat, +07:00 commit tz)
- Data: Claude commits by author date on main: 10-08 6 and 10-09 6 committed by BFlat, and 14 more on 10-09 committed by Claude. After that 1–19/day to 11-10 (peak 11-02 19).
- Notes: cff8daf185 on main has the same subject as 7406c26bd4 on claude/integ-batch-7 ("automation test: as_chunks for the preview pixel check"). INFERRED: fix-ups made on integration branches were cherry-picked onto main by BFlat.

### E06-011 — Session trailers: 62 Claude sessions on main, 129 across all refs, mostly short
- Label: VERIFIED
- Method: `sess.py`. Session id = last path segment of the `Claude-Session:` URL (all `https://claude.ai/code/<id>`). Copilot sessions use a UUID.
- Data:

| scope | commits with trailer | distinct sessions | commits/session min/med/p90/max | singletons | span (h, first→last author date) med/p90/max | days with ≥1 session | max sessions same day | median sessions/day |
|---|---|---|---|---|---|---|---|---|
| main, Claude-Session | 274 | 62 | 1 / 1 / 6 / 52 | 32 | 0.0 / 29.7 / 561.6 | 33 | 10 (2026-10-13); 8 (10-14) | 3 |
| all refs, Claude-Session | 914 | 129 | 1 / 2 / 14 / 127 | 37 | 1.9 / 73.2 / 561.6 | 36 | 15 (10-13); 14 (10-31); 12 (11-03) | 5 |
| main, Copilot-Session | 31 | 5 | 1 / 7 / 9 / 19 | 1 | 8.3 / 25.3 / 26.8 | 3 | 5 (10-07) | 2 |
| all refs, Copilot-Session | 90 | 6 | 2 / 15 / 21 / 44 | 0 | 9.4 / 25.6 / 32.1 | 4 | 5 (10-07) | 2.5 |

- Sessions per author name (all refs): Claude 51, Nicolas Falesy 12, Khawar Zamman Wani 8, Leel Wasanatha 7, Shehan Kavishka 6, … All Copilot sessions: Alex Gorevski (+1 under author "Copilot").
- Notes: "same day" counts distinct session ids whose commits have author dates on that day. That is evidence of overlapping sessions, not proof that they ran at the same moment. A 561 h span likely comes from rebased or cherry-picked commits that kept old author dates (INFERRED). Session trailers cover only a small part of AI-attributed commits (274 session-trailer commits vs 3,780 main commits with a `Co-authored-by: Claude…` line; `git log main --format=%b` + regex `^co-authored-by:\s*claude`), so they undercount sessions.

---

## 3. Branch namespaces (in-repo `refs/remotes/origin/*`, 367 refs)

Method: for each remote branch, `git rev-list --count main..<b>`, `merge-base --is-ancestor`, authors and AI-trailer
lines of `main..<b>` → `branches.tsv`, then grouped. "AI>0" = branches with ≥1 AI-trailer line among unmerged
commits. Squash-merged branches show as "not ancestor". So "ancestor" counts only fast-forward or merge-commit landings.

| Namespace | # | date range (first unique commit .. tip) | ancestor of main | AI>0 | main authors (unique commits) | Observed purpose |
|---|---|---|---|---|---|---|
| `fix/*` (non-sec, non-numbered) | 97 | 10-04..11-11 | 7 | 36 | Brandon Thomas 103, Dylan M. Taylor 35, Tanish Manku 25, FredApps 10 | maintainer fix branches |
| (no prefix) | 60 | 10-05..11-12 | 3 | 42 | Brandon Thomas 48, Dylan 40, Claude 35, bflatastic 30 | misc: `release*`, `switch-craft-*` (shared-lib migration) |
| `community/<issue>-<slug>` | 45 | 10-06..10-09 | 7 | 29 | Claude 32, Nigel Ihza Firdausy 10, bflatastic 4 | community PRs copied into the repo to be fixed up/integrated (E06-023) |
| `feat/*` | 38 | 10-04..10-30 | 0 | 18 | Brandon Thomas 61, Tanish Manku 33 | features |
| `fix/sec-*` | 20 | 11-02..11-11 | 2 | 0 | Dylan M. Taylor 75 | security-bounds hardening PRs (E06-026) |
| `claude/fix-<issue>-<slug>` | 17 | 10-08..10-09 | 0 | 17 | Claude 28 | agent issue fixes, PRs opened by bflatastic (E06-024) |
| `pr/*` | 15 | 10-04..10-06 | 0 | 12 | Brandon Thomas 15 | 12 `pr/never-crash-*` + 3 others (E06-027) |
| `claude/integ-batch-1..11` | 11 | 10-08..10-09 | 0 | 11 | Claude 147, Nigel 33, MarekSpodBiedry 21, shmuelbiller1 16 | CI-only integration trains (E06-021) |
| `claude/*` other | 10 | 10-08..10-11 | 0 | 10 | Claude 11 | `claude/fix-main-*`, `claude/regen-scorecard`, `claude/docs-…`, session-named `claude/friendly-ritchie-iqt0sh`, `claude/loving-hypatia-7xc95z` |
| `ci/*` | 7 | 10-07..11-11 | 4 | 1 | FredApps 2, Brandon 1 | 3 `ci/snapshot-<sha>` all ancestors (10-07) |
| `perf/*` | 7 | 10-04..10-10 | 0 | 4 | Brandon 11, Tanish 3 | perf |
| `codex/*` | 5 | 10-14..11-07 | 3 | 0 | skylar taylor-barrick 7 | human-authored, no trailers; e.g. PR #7848 (E06-025) |
| `sonar/*` + `sonar-fix/*` | 5 + 4 | 10-21..10-27 | 0 + 1 | 0 | Dylan M. Taylor 42 | SonarCloud rule clean-up (`s3776`, `s7688`, `enforce-clippy-standards` 27 commits) |
| `chore/*`, `docs/*`, `jobs/*`, `land/*`, `batch/*`, `build/*`, `test/*`, `patch/*`, `wip/*`, `screenshots/*`, `i18n/*`, `formats/*`, `dependabot/*` | 4,3,3,2,1,1,1,1,1,1,1,1,1 | — | — | — | see entries | E06-027/028 |

### E06-020 — In-repo `claude/*` branches all date from 10-08..10-11 and are all authored by the `Claude` identity
- Label: VERIFIED
- Source: `branches.tsv`; e.g. claude/fix-1271-system-title-bar (PR #1344), claude/fix-1313-tab-hides-panels (PR #1388), claude/regen-scorecard (PR #1532)
- Data: 38 `claude/*` branches = 17 `claude/fix-<issue>-*` + 11 `claude/integ-batch-*` + 10 other. First unique commit dates 2026-10-08..10-11. Every one has AI trailers.
- Notes: after 10-11 no new in-repo `claude/*` branches appear, but `claude/*` branch names keep appearing on forks (6 merged from `wanikhawar`). The `<adjective>-<name>-<id>` names (friendly-ritchie-iqt0sh, loving-hypatia-7xc95z) match Claude Code web-session default branch naming (INFERRED from the pattern; this research repo's own branch `claude/magical-hypatia-jwtvty` has the same shape).

### E06-021 — `claude/integ-batch-1..11` were CI-only integration trains (2026-10-08/09); members were squash-merged one by one
- Label: VERIFIED (structure); INFERRED (operator)
- Source: PR #1335 (claude/integ-batch-1 → main; via WebFetch summary): "CI only (do not merge): integration of community batch 1", opened and closed by bflatastic on 2026-10-08, "This draft PR exists only to run CI", "🤖 Generated with Claude Code" + session link, "No reviews". Batch tips map to PR heads #1335, #1346, #1362, #1407, #1454, #1514, #1564, #1625, #1670, #1740, #1804 (`grep <tip> pullheads`). None appears on main as `(#N)`.
- Data: first-parent of batch-1 = 12 `Merge branch 'pr-NNNN' into claude/integ-batch-1` commits, all 18:12:38–39 UTC on 10-08, author and committer Claude. Batch-2 uses `Merge #NNNN`, batch-7 `Merge pr/NNNN` (22 merges in 1 minute, then fix-ups: 2c82295e4c "fmt: batch 7 conflict resolution in vector_ui.rs tests", 17ff15802a merging origin/main with `# Conflicts: crates/ui-egui/src/vector_ui.rs`). Batch-11 merges `community/*` branches and `pNNNN`. Unique-commit totals: batch-1 37, -3 44, -7 48, -10 44, -8 38 (others 13–34).
- Member PRs on main as separate squashes: #1261 f9ccdda1e2, #1279 7d78e1dd2c, #1269 a5f9029c20, #1155 93694cf2f6 (the last three 01:56:40–01:57:01 +07:00 on 10-09). #1441 7ad869eb32 and #1718/#1785 also landed separately.
- Notes: the same machine/tz (+07:00) appears on BFlat-committed Claude commits (E06-010). INFERRED: BFlat ran a Claude agent that assembled batches to get one CI run for N community PRs, then squash-merged each PR when green. The squash committer field is "GitHub", so the person who merged is not recorded in git.

### E06-022 — `davidmann4/integration-batch-7..20`: fork-hosted integration PRs merged as merge commits (10-23..11-06)
- Label: VERIFIED
- Source: first-parent merges a02f2ee410 (#8663, b7, aiongg, 10-23) … 6b0f7762e1 (#11671, b20, David Mann, 11-06). PR #9386 via WebFetch summary.
- Data (per batch: unique commits / merges / distinct `Merge PR #N` messages / main-syncs / commits with Claude trailer / merger):

| batch | PR | merged | merger | commits | merges | PRs merged | main syncs | Claude-trailer commits | body first line |
|---|---|---|---|---|---|---|---|---|---|
| 7 | #8663 | 10-23 | aiongg | 339 | 143 | 48 | 41 | 123 | "Integration batch: 44 PRs on main" |
| 8 | #9386 | 10-25 | aiongg | 372 | 179 | 43 | 40 | 132 | "37 reviewed community PRs on main" |
| 9 | #9775 | 10-27 | aiongg | 141 | 54 | 21 | 24 | 64 | "21 PRs on main" |
| 10 | #10145 | 10-31 | aiongg | 197 | 97 | 20 | 45 | 38 | "18 PRs on main" |
| 11 | #10535 | 11-01 | aiongg | 69 | 18 | 9 | 8 | 38 | "9 ATN PRs on main" |
| 12 | #10776 | 11-02 | aiongg | 174 | 25 | 14 | 4 | 84 | "14 Actions PRs on main" |
| 13 | #10952 | 11-03 | David Mann | 134 | 49 | 0 | 21 | 15 | "13 parity epic PRs on main" |
| 14 | #11157 | 11-04 | David Mann | 63 | 21 | 13 | 5 | 12 | "9 PRs planned" |
| 15 | #11203 | 11-04 | David Mann | 39 | 13 | 8 | 4 | 18 | "Crop, Free Transform and Actions epic PRs" |
| 16 | #11278 | 11-04 | David Mann | 91 | 24 | 10 | 7 | 13 | "9 epic PRs on main" |
| 17 | #11320 | 11-05 | David Mann | 166 | 35 | 10 | 12 | 35 | "14 epic PRs" |
| 18 | #11563 | 11-06 | David Mann | 95 | 29 | 23 | 2 | 45 | "23 epic PRs (toolbar, move, selection, artboard, menus)" |
| 19 | #11643 | 11-06 | David Mann | 84 | 24 | 10 | 11 | 46 | "epic PRs (WIP)" |
| 20 | #11671 | 11-06 | David Mann | 51 | 19 | 7 | 9 | 18 | "7 i18n PRs (Thai, Hebrew, Urdu, Tamil, Azerbaijani, Romanian, Korean)" |

- Method: `git rev-list --count M^1..M^2`, `--merges`, `grep -oE '^Merge (PR|pull request) #[0-9]+' | sort -u`.
- PR #9386 description (via WebFetch summary): review method "two independent agents per PR (a reviewer and an attacker)", "every claim checked against code, spec or a run"; gate "fmt, workspace check, layers, clippy `-D warnings`, i18n catalogs, parity and scorecard freshness"; "each PR's code reverted on the branch, its named tests fail"; self-reported "10,793 tests passed"; "Please merge with "Create a merge commit" or a fast-forward push … Squash or rebase would rewrite the commits, and the 37 PRs would stay open"; "Generated with Claude Code". CodeRabbit left review comments, and commits say issues were "Found by CodeRabbit on #9386". No human approval was visible. Merged by aiongg on 10-26 with 12 checks passed.
- Conflict-resolution commits carry Claude trailers and explain each resolution, e.g. 38609e5615 (2026-10-25, "Merge PR #8885: … Merged with our fix-up branch pr-8885-fixup … Conflicts resolved: …", `Co-Authored-By: Claude Opus 5.5`) and 4365c0537d "Integration: merge main, resolve conflicts (#8885)" ("people.toml takes main's entries plus jasallen's own … docs/scorecard.md is regenerated").
- Notes: this is the main path by which community PRs reached main after 10-20. First-parent merges/day drop (E06-013) because batches carry many PRs per merge commit. The batch numbering continues from the claude/integ-batch series; whether the two are one pipeline is unverified.

### E06-023 — `community/<issue>-<slug>`: community PR heads copied into the repo and given Claude fix-ups (10-06..10-09)
- Label: VERIFIED (data); INFERRED (purpose)
- Source: `branches.tsv`; e.g. community/1168-non-unicode-args (PR #1359, 6 Claude commits), community/1240-psd-text-fill (Rage 1 + Claude 1; merged into claude/integ-batch-1 by 5d921c7859), community/1297-batch-layer-move (Nigel 8 + Claude 1)
- Data: 45 branches. Unique commits: Claude 32, Nigel Ihza Firdausy 10, bflatastic 4, others 1–3. 29/45 have AI-trailer lines. 7 are ancestors of main (e.g. community/1462-labmix, 1706-corpus, merged through batch-11). Earliest (community/384…435, 10-06) carry bflatastic + original authors, not Claude.
- Notes: PR #1335's linked "#1368 … carries #1240" (WebFetch) fits the pattern "re-land a community PR with a maintainer/agent fix-up". 7 merge-PR commits on main come from storytold/community/* heads (`forkbr.txt`).

### E06-024 — `claude/fix-<issue>-<slug>`: a same-day issue-fix sweep on 2026-10-08/09
- Label: VERIFIED
- Source: 17 branches, issue numbers 1248–1544 (`branches.tsv`); PR #1344 via WebFetch summary: opened and merged by bflatastic on 10-08, commits under the `claude` account, sections "What"/"Tests", "Closes #1271"/"Closes #1316", "🤖 Generated with Claude Code" + session link, "No reviews", "8 checks passed"
- Data: 15 of 17 branches have first commit on 10-08 (1248, 1271, 1272, 1275, 1286, 1288, 1313, 1323, 1354, 1357, 1371, 1380, 1381, 1387 + fix-main-*), the rest on 10-09.
- Notes: INFERRED: one operator (bflatastic) ran a batch of Claude sessions over open issues. Neither git nor the PR page shows how many ran at the same time.

### E06-025 — `codex/*` branch names do not reliably mean Codex-authored commits
- Label: VERIFIED
- Source: in-repo codex/* (5): authors skylar taylor-barrick 7, 0 AI trailers; PR #7848 (codex/pr7281-smudge-correctness, via WebFetch): no AI disclosure, commits carry "Co-Authored-By: Claude Opus 5.5", approved by FredApps, merged by dylanmtaylor on 10-30. Fork merges: 40 from `<owner>/codex/*` (yoriswind 19, Bobderto 5, vistaero 4, abc2cb 3 …), e.g. 28d2b499b5 (#11062).
- Data: the `Codex` author identity has 24 commits on main, 42 in all refs, 3 emails, and appears on PR heads, not on `codex/*` branches.
- Notes: branch name and trailer give conflicting signals (Codex branch, Claude trailer). Treat `codex/` as weak attribution.

### E06-026 — Dylan M. Taylor's `fix/sec-*` and `sonar*/` series: human-only attribution, CodeRabbit + Sonar reviewed
- Label: VERIFIED
- Source: 20 `fix/sec-*` branches (11-02..11-11), 0 AI-trailer lines; 9 `sonar*/` branches (10-21..10-27). PR #11059 (fix/sec-command-work-bounds, via WebFetch): sections "What was wrong / What changed / Blast radius / Checks", "Not run: full workspace tests (shared build host)", CodeRabbit ~4 reviews ("Merge Risk: Moderate", docstring-coverage check failed), SonarQube "Quality Gate passed … 95.0% Coverage on New Code", tanish2k09 asked for changes ("Push when ready and we'll take another look"), label "waiting on author", still open on 11-12.
- Data: 37 direct first-parent commits by Dylan, incl. a 2026-10-22 07:10–07:12 run of ~30 `security(...)` commits (c5a6afcf68 … c3c6c63074), author = committer = Dylan M. Taylor, no `(#N)`.
- Notes: the brief estimated ≈25 `fix/sec-*` branches; this count is 20 (`grep -c '^fix/sec-' branches.tsv`). The direct pushes predate house rule 8 "main changes through a pull request … no exception" (added 11-06, 7d8648dfcb).

### E06-027 — Founder-era stacking and splitting: `pr/never-crash-*`, `jobs/*`, `land/*`, `batch-followups`
- Label: VERIFIED
- Source:
  - 12 `pr/never-crash-*` branches, each 1 Brandon Thomas commit with AI trailer, 2026-10-04. Landed as squashes #33 (50a27e6c74, 11:14) then #34–#59 within 13:25:17–13:40:43 (69f0e25d5f … 2e80c781ee). PR #33 (via WebFetch): "Generated with Claude Code" footer, "Checks" section listing gates already failing on main, "No reviews", merged with "2 of 5 checks passed".
  - `jobs/engine-210` → `jobs/ui-210` stacked. 7a44cf3280 on `jobs/ui-210-main`: "Re-lands #290, which was merged into its stacked base branch (jobs/engine-210) instead of main. Same tree as the gated #290 commit 39152db."
  - `land/pr-344` (Brandon, "Dock: visible splitter grips … (#295)"), `land/pr-1068` (bflatastic author, Brandon committer, "(#578)"): maintainers re-landing an existing PR on an in-repo branch.
  - `batch-followups` (2 commits, 10-05, "Follow-up to #102").
- Notes: INFERRED: one large agent change was split by crate into 12 PRs that were merged back-to-back in about 15 minutes, i.e. PRs used as CI/record units rather than review units.

### E06-028 — Other namespaces
- Label: VERIFIED
- Source: `branches.tsv`
- Data: `batch/a-ui-workflow-hardening` (PR #11007; 33 unique commits, bflatastic 20, Dylan 8, mariusmartin 3; 11-02..11-03). `test/backfill-regression-tests` (PR #8690; skylar taylor-barrick 9 commits, 10-22). `ci/snapshot-43c86ef/-47f9306/-83ace113` (all ancestors of main, 10-07). `build/craft-update-495e597` (Dylan, 10-25; shared craft-libs revision bump). `switch-craft-*` / `switch-photocraft-*` (no prefix, migration to shared crates).

---

## 4. Merge mechanics over time

### E06-012 — Main went from direct pushes (09-30..10-03) to PRs on 10-04, then mostly squash merges, then merge commits
- Label: VERIFIED
- Method: `fp.py` over `git rev-list --first-parent main` (3,475 commits)
- Data: squash `(#N)` 2,690; `Merge pull request #N` 598; single-parent without `(#N)` 181; other merges 6.

| period (commit date) | direct | squash | merge-PR |
|---|---|---|---|
| 09-30..10-03 | 69 | 0 | 0 |
| 10-04 | 4 | 49 | 2 |
| 10-05..10-11 | 35 | 1,381 | 8 |
| 10-12..10-15 | 11 | 729 | 3 |
| 10-16..10-31 | 51 | 372 | 94 |
| 11-01..11-12 | 11 | 159 | 491 |

- Notes: direct commits after 10-04 by committer: Dylan M. Taylor 37, Brandon Thomas 30 (mostly `Release …`), BFlat 28, GitHub 14 (e.g. Michael Higgins and Terra854 on 11-11, single-parent and committer GitHub without `(#N)`, likely rebase-merges: INFERRED), Claude 1. Merge style changed from squash to merge commit around 10-20, matching the integration-batch PRs' explicit request for merge commits (E06-022).

### E06-013 — PR lifetime (first commit on head → landing on main) grew from hours to days
- Label: VERIFIED
- Method: `life.py`/`lifea.py`. For each first-parent squash/merge with `refs/pull/N/head` (3,271 of 3,288), first = min author date of `git log refs/pull/N/head ^<merge first parent>`, end = commit date of the landing commit. Author dates can predate PR opening (rebases/cherry-picks), so these are upper bounds on PR-open time.
- Data:

| subset | n | p25 | median | p75 | p90 | <1h | >7d | median commits/PR | single-commit PRs |
|---|---|---|---|---|---|---|---|---|---|
| all | 3,271 | 2.8 h | 10.1 h | 24.3 h | 117.8 h | 14% | 8% | 2 | 41% |
| squash | 2,673 | 2.3 h | 8.2 h | 18.1 h | 51.4 h | 16% | 2% | 2 | 45% |
| merge-commit | 598 | 8.8 h | 52.1 h | 250 h | 360 h | 4% | 33% | 4 | 20% |
| landed 09-30..10-09 | 915 | 0.6 h | 2.8 h | 6.5 h | 15.1 h | 30% | 0% | 1 | 58% |
| 10-10..10-19 | 1,466 | 5.2 h | 12.3 h | 21.5 h | 52.5 h | 10% | 0% | 2 | 40% |
| 10-20..10-31 | 243 | 2.9 h | 16.7 h | 68.0 h | 215.8 h | 14% | 14% | 2 | 38% |
| 11-01..11-12 | 647 | 10.8 h | 68.3 h | 218.4 h | 351.2 h | 2% | 34% | 4 | 19% |

- Merge bursts (`conc.py`): max 49 landings within a 10-minute window (ending 2026-10-10 17:17:38 UTC). Peak landing days: 10-09 323, 10-13 311, 10-10 258.

### E06-014 — Most merge-commit PRs come from forks
- Label: VERIFIED
- Method: owner parsed from `Merge pull request #N from <owner>/<branch>` (`lifea.py`, `forkbr.txt`)
- Data: 576 of 598 from forks, 22 from `storytold/*` (<10-20: 9/24 in-repo; 10-20..31: 5/83; Nov: 8/491). 108 distinct fork owners. Fork branch first segment: fix 342, feat 53, codex 40, perf 26, security 11, community 7, claude 6, ci 6.
- Notes: for squash merges, git cannot tell whether the source was a fork. contributors.json and PR pages (e.g. #1261 Ni-zav fork, #2792 vangel76 fork) show forks were common from the start.

### E06-015 — PR volume and unmerged heads
- Label: VERIFIED (git) / via WebFetch summary (web counts)
- Data: 6,480 `refs/pull/*/head` refs. Pulls page: Open 1,298, Closed 5,178. Closed-unmerged filter: 912 (37 pages). Of 3,288 first-parent landings, 3,271 have heads. `data/E03_pr_heads_status.csv` classifies 2,238 heads as not ancestor and number absent from main (unmerged or merged elsewhere).
- Sample of closed-unmerged (WebFetch, 2026-11-12): dependabot group bumps (#13125, #13110, #12470, #12278, #11676); releases superseded (#13192 "Release: PhotoCraft v0.23.0" FredApps; #13327 "Release 0.22.1" dylanmtaylor); i18n languages by tronicum (#12365 sw, #12364 ha, #12348 te, #12347 mr); duplicate fixes (#11854, #11846 DuBearte; #11713 TrevorBrown-dev); self-withdrawn (#12945 makzumi: "I need to review a few things, i'll re-open when ready"); junk (#11849 title ".").

---

## 5. Task intake and decomposition

### E06-030 — Issues: very high volume, label-based triage, bulk structured filing by the lead integrator
- Label: VERIFIED via WebFetch summary
- Source: https://github.com/storytold/photocraft/issues, /labels, /labels?page=2 (accessed 2026-11-12)
- Data: 2,804 open issues. 52 labels, including `missing feature`, `parity`, `priority: critical/high/medium/low`, `in progress`, `duplicate`, `needs decision` ("Held for a maintainer decision; don't merge, close, or replace until a maintainer removes it"), `ready to merge` ("Reviewed: correct, complete and tested; waiting for a maintainer to merge"), `waiting on author` ("Closed after 14 days without reply"), `small extra`, `plugin candidate`, `full-ci` ("Runs the full CI matrix … on a PR"), `spam`. 12 of the first 25 open issues (#13458–#13472) were filed by `davidmann4` with machine-style titles (`EPIC-CUSTOM-SHAPE-TOOL`, `MISSING-FEATURE-CUSTOM-SHAPE-TOOL-ALIGN-EDGES`, `BUG-CUSTOM-SHAPE-TOOL-HISTORY-NAME`).
- Notes: no `.github/ISSUE_TEMPLATE*` or PR template exists in the repo (`find .github -type f`; none in history via `--diff-filter=AD`). /issues/new/choose needed sign-in. That issue labelling or filing is agent-driven is INFERRED only (titles look generated); there is no explicit attribution on the list page.

### E06-031 — Issue→branch→commit mapping conventions
- Label: VERIFIED
- Method: `intake.py` over non-merge main commits
- Data:

| period | non-merge commits | subject has `(#N)` | subject `(#issue…) (#PR)` | body/subject "fixes/closes/resolves #N" | touch crates/ or apps/ | code + tracker same commit | share |
|---|---|---|---|---|---|---|---|
| 10-01..09 | 1,064 | 927 | 327 | 97 | 979 | 99 | 10.1% |
| 10-10..19 | 2,787 | 1,845 | 759 | 152 | 2,602 | 341 | 13.1% |
| 10-20..31 | 2,403 | 702 | 47 | 53 | 2,166 | 173 | 8.0% |
| 11-01..12 | 2,074 | 698 | 43 | 63 | 1,957 | 90 | 4.6% |

- Tracker files: docs/gaps.md, docs/parity-checklist.md, scorecard/*.toml, docs/scorecard.md, ROADMAP.md, docs/*-parity.md, docs/target-app-parity.md, docs/roadmap.md. Per-period touches, e.g. 10-10..19: docs/*-parity.md 210, docs/scorecard.md 209, scorecard/*.toml 132, docs/gaps.md 110, target-app-parity 41.
- Notes: the `Title (#issue) (#PR)` squash subject (e.g. 7d78e1dd2c "… (#1260) (#1279)") was the main issue link in early October. It fades after 10-20, when merge commits take over and the subject no longer carries the PR number. Branch names `fix/<issue>-…`, `claude/fix-<issue>-…`, `community/<issue>-…` and fork `fix/13065-…` carry issue numbers.

### E06-032 — Documented intake rules vs. observed tracker co-updates
- Label: VERIFIED (doc) / INFERRED (comparison)
- Source: 74330157cb:AGENTS.md:127-143 (§4 Picking work: "Read `ROADMAP.md`, then `docs/gaps.md` … update the parity doc and gap entry it belongs to, with the date"); :178-187 (§7); :7 (house rule 2 "Check, then claim … Comment on the issue first. Release a claim you will not finish.", added 11-06)
- Notes: under 14% of code commits in any period touch a tracker in the same commit (E06-031), and the share falls over time. INFERRED: the "update the tracker in the same change" rule is followed in a minority of commits. Some tracker updates may be in sibling commits of the same PR (not measured). Integration fix-ups regenerate scorecard "at the batch gate" (38609e5615), so trackers are partly refreshed centrally.

---

## 6. Review and supervision (PR sample; all via WebFetch summary, accessed 2026-11-12)

Sample chosen to avoid E05's (#113, #7809, #11641, #12237, #13234, #13414).

| PR | period | opened by / head | description | AI disclosure | bot review | human review | merged by / when | elapsed |
|---|---|---|---|---|---|---|---|---|
| #33 | early | echelon / pr/never-crash-steering | bullets + "Checks" (lists already-failing gates) | "Generated with Claude Code" + Claude Opus 5.5 trailer | none | "No reviews" | merged 10-04, "2 of 5 checks passed" | same day |
| #1261 | early | Ni-zav fork / fix/remember-guide-layout-values-1203 | Summary/Changes/Tests/Expected/Validation, "Closes #1203" | none | none | "No reviews"; echelon: "This has landed on `main`" | echelon, 10-08, 7 checks | same day |
| #1335 | early | bflatastic / claude/integ-batch-1 | "CI only (do not merge)", 12 included PRs | "Generated with Claude Code" + session link | none | "No reviews" | closed unmerged by bflatastic, 10-08 | same day |
| #1344 | early | bflatastic (commits by `claude`) / claude/fix-1271-system-title-bar | What/Tests, "Closes #1271", "Closes #1316" | "Generated with Claude Code" + session link | none | "No reviews" | bflatastic, 10-08, 8 checks | same day |
| #2792 | early-mid | vangel76 fork / fix/2786-cli-batch-action-set | "Fixes #2786", Root cause/Fix/Tests/Commands | "Generated with Claude Code" + trailer | none | "No reviews"; echelon "Landed as is." | echelon, 10-11, 7/8 checks | ~1 day |
| #7848 | mid | skylartaylor / codex/pr7281-smudge-correctness | problem, landing order, Validation ("5,212 tests passed") | none in text; Claude trailer in commits | CodeRabbit (Minimal risk; docstring 74% < 80%) | FredApps comment "not an approval", then approved 10-20; aiongg labelled | dylanmtaylor, 10-30, 19 checks | 11 days |
| #9386 | mid-late | davidmann4 fork / integration-batch-8 | TL;DR, PR table, conflict notes, fix-up table, Testing | "Generated with Claude Code"; "two independent agents per PR (a reviewer and an attacker)" | CodeRabbit comments | none visible | aiongg, 10-26, 12 checks | ~1 day (PR) / branch from 10-08 |
| #11059 | late | dylanmtaylor / fix/sec-command-work-bounds | What was wrong/What changed/Blast radius/Checks, "Not run: …" | none | CodeRabbit ×~4, SonarQube "Quality Gate passed" | tanish2k09 requested changes (comment), "waiting on author" label | open 11-12 | 9+ days |
| #11062 | late | yoriswind fork / codex/artboard-move-overflow | prose, coverage list | none (branch name only) | CodeRabbit walkthrough + nitpicks, suggested aiongg as reviewer | tanish2k09 added "ready to merge" 11-05 | tanish2k09, 11-11, 18 checks | 8 days |
| #12945 | late, rejected | makzumi fork / stage-a-layout | What/Why first/Checks + "Summary by CodeRabbit" | none | CodeRabbit 3 actionable comments, docstring 75% | none | self-closed 11-10 | same day |

### E06-040 — Bot review appears mid-October; early PRs had no review at all
- Label: VERIFIED via WebFetch summary (sample of 10)
- Data: 0/5 early PRs (#33, #1261, #1335, #1344, #2792) show any review, bot or human. 5/5 sampled PRs from 10-19 onward show CodeRabbit. SonarQube Cloud appears on #11059 (SonarCloud workflow added 8e518d8169, 2026-10-21, Dylan M. Taylor).
- Notes: small sample. E05 holds the CI side.

### E06-041 — Human supervision is mostly labels, merge decisions and occasional change requests
- Label: VERIFIED (sample) / INFERRED (generalisation)
- Data: human approval seen once (#7848, FredApps), change request once (#11059, tanish2k09), "ready to merge" label applied then merged by the same maintainer (#11062). Early merges by echelon/bflatastic happen with "No reviews". Integration-batch PR #9386 states agent-based review ("two independent agents per PR") and no visible human approval before aiongg merged.
- Notes: house rule 1 "A person is accountable. Whoever runs an agent answers for what it opens" (AGENTS.md:6) and rule 14's 7/14/30-day response clock (AGENTS.md:19, added 11-06) codify this. The `waiting on author` label text ("Closed after 14 days") differs from rule 14 ("closure eligible at 30 … never automatic").

### E06-042 — AI disclosure in PR text depends on the author, not the period; it continues after the "No agent attribution" rule
- Label: VERIFIED (sample)
- Data: "Generated with Claude Code" appears in #33, #1335, #1344, #2792 (echelon, bflatastic, vangel76) and in davidmann4's integration PRs #9386 (10-25) and #13396 (11-12, draft). It is absent from #1261, #7848 (text; Claude trailers in commits), #11059, #11062, #12945.
- Notes: house rule 15 "**No agent attribution.** A pull request does not say an agent wrote it." (AGENTS.md:20, added 2026-11-06 by 7d8648dfcb, copied from storytold/craft-contrib). The lead integrator's 11-12 PR still discloses, so the rule is not uniformly followed, or is read as a ban on *requiring* attribution ("A repository rule may not require that"). INFERRED; sample of 11.

### E06-043 — Integration PRs ask the bot for review and record a manual-test plan; human review is still not visible
- Label: VERIFIED via WebFetch summary
- Source: PR #13396 (davidmann4:integration-mcp, draft, opened 2026-11-12)
- Data: "Please don't merge yet: a manual test in the real app is planned for 2026-11-13". The author asked CodeRabbit for a review ("review plz and take this carrot"). CodeRabbit posted 16 actionable comments, "Merge Risk: Moderate", and suggested reviewers wanikhawar, fredapps, aiongg (none assigned). Follow-up commit "Batch: CodeRabbit findings on the MCP connection". Self-reported gate "12,514 of 12,521 passing, with the 7 failures explained". Included PRs #11363 (ingling) and #5525 (Furoxfufu), whose authors appear as co-author trailers.
- Notes: shows the loop "integrator agent fixes → bot review → agent addresses bot findings → human manual test before merge".

### 6.1 Issue sample (via WebFetch summary, accessed 2026-11-12)

| Issue | opened by / date | structure | triage | closure / link | AI signal |
|---|---|---|---|---|---|
| #210 | echelon, 10-05 | Description / Goal / Targets (time-budget table) / Work | labels performance, reliability | open; commits "part of #210" (#289, #290) 10-06; fork commits by arhammusheer | none on page |
| #1271 | szponciciel04, 10-08 | one paragraph + screenshot | no labels | closed same day by bflatastic via #1344 | maintainer reply "Generated by Claude Code" |
| #13451 | womb4t, 11-12 | Summary / Environment / Steps / Root cause / Expected / Suggested fixes / Workarounds | 5 labels incl. `priority: critical`, `in progress`, all added by the **ticket-craft** app | bot comment "This is being worked on in #10121" + related issues | bot |
| #13458 | davidmann4, 11-12 | TL;DR / Goal / How this was measured / Already works on main / How to pick something up / Free to pick up (13 child issues #13459–#13472 with "Main files") / Being worked on / Merged / Still open | labels multiple issues, parity, priority: medium, ui; ticket-craft comment proposing a split | asks contributors to open a draft PR "Fixes #<issue>" | measured "through the control channel", items "created from the measured spec" |

### E06-033 — A third-party GitHub App, ticket-craft, triages issues: labels, duplicates, "being worked on" links
- Label: VERIFIED via WebFetch summary
- Source: issues #13451, #13458; https://github.com/apps/ticket-craft (developer `juansebsol`, website tickets.artcraft.build, "No description")
- Data: on #13451 ticket-craft applied all 5 labels and commented with the in-progress PR and related issues. On #13458 it suggested splitting the epic. The open-issue list shows many `duplicate` + `in progress` combinations (#13445, #13447, #13450, #13453, #13455).
- Notes: no mention of ticket-craft in the repo (`git log --all --grep`, `git grep` empty), so its configuration is outside this repo. Whether it uses an LLM is unknown (the app page does not say). The label vocabulary `in progress` serves as a claim marker, applied by the bot.

### E06-034 — Epic issues are written as work queues for agents and contributors
- Label: VERIFIED (structure) / INFERRED (intent)
- Source: issue #13458 (via WebFetch summary)
- Data: the epic has "How to pick something up" (4 steps), "Free to pick up / Being worked on / Merged" tables and per-item "Main files". It was produced by driving the app "through the control channel".
- Notes: this matches house rule 2 "Check, then claim" (AGENTS.md:7) and AGENTS.md §4. INFERRED: the epic is a hand-off format meant to stop parallel workers from colliding.

---

## 7. Parallelism evidence

### E06-050 — "Parallel agents" guidance has existed since day 1 and grew within 24 h
- Label: VERIFIED
- Source: 16941f7198:AGENTS.md:56 (2026-09-30 "one-shot"): "Parallel agents: use your own target dir (`CARGO_TARGET_DIR=target/agent-<name>`) to avoid the Cargo build lock, and edit only the crates you own. Keep every `Cargo.toml` valid at all times…"; expanded in 536a7346fb (2026-10-01) with "surgical" shared-file edits, "If someone else's in-progress edit breaks the build, wait and retry", "Disk space … Delete `target/agent-*` dirs", and the dev-log hand-off "Sessions can end abruptly" (`git log -S`). Current text 74330157cb:AGENTS.md:170-176.
- Quote: "Put new commands in a **new module** (`engine/src/<area>_cmds.rs` with a `specs()` function) rather than growing a shared file." (AGENTS.md:173)
- Notes: the guidance assumes several agents in one working tree (shared target dir, builds broken by "someone else's in-progress edit"). No mention of git worktrees, locks or claim files. Claiming work by commenting on the issue appears only in house rule 2 (11-06). Conflict avoidance is structural (new modules, atomic manifest writes via `mv`). Manifests are created "atomically … then `mv` it into place" (AGENTS.md:175, from ae92ac20bf 2026-09-30).

### E06-051 — Observed concurrency: hundreds of PRs in flight per day; conflicts concentrate in shared files
- Label: VERIFIED (counts) / INFERRED (cause)
- Method: `conc.py`. A landed PR counts as "in flight" on each UTC day from its first head commit to its landing. Unmerged PRs are excluded, so these are lower bounds.
- Data: in flight (landed PRs only): 10-07 227, 10-09 381, 10-11 451, 10-13 504 (peak), 10-20 90 (trough), 11-04 302, 11-11 194. Same-day Claude sessions up to 15 (E06-011). Conflict notes name shared files: `crates/ui-egui/src/vector_ui.rs` (17ff15802a), `crates/ui-egui/src/panels.rs`, `crop_size.rs`, `docs/context-menu-parity.md`, `docs/gaps.md` (731eae5efb), `Cargo.lock`/`crates/io/Cargo.toml`, `contributors/people.toml`, `docs/scorecard.md` (38609e5615, 4365c0537d).
- Notes: tracker docs and generated files (scorecard, parity docs, people.toml) recur in conflict lists. INFERRED: the per-PR tracker update rule (§5) creates conflict hot spots that integration batches then resolve "as unions" (PR #9386, via WebFetch).

---

## Open questions / uncertainties
- Who pressed merge on 2,690 squash merges: git records committer "GitHub". Only the WebFetch sample names mergers.
- Whether the BFlat (+07:00) Claude operator and the bflatastic account are the same person relies on `data/E03_alias_map.csv`. The "same operator ran claude/integ-batch and committed Claude commits" link is INFERRED from tz + committer field.
- How claude/integ-batch-N relates to davidmann4/integration-batch-7..20 (numbering continues, but authors differ). Batches 1–6 of the davidmann4 series were not found on main as merge commits.
- Session counts undercount AI sessions: most AI-attributed commits have no session trailer. Session spans are affected by rebases.
- PR lifetimes use first-commit author date, not PR-open time (not in git). Upper bound on open-to-merge.
- WebFetch summaries may miss review threads on long pages (e.g. #9386 truncated at 100k chars, second part read). Only 4 issue pages and 11 PR pages were sampled (a WebFetch quota interruption cut the sample short).
- The brief's ≈25 `fix/sec-*` and ≈203 Claude-Session commits differ from these counts (20; 274 main commits with a session trailer) because of different counting methods.
- Discussions/wiki/projects pages were not fetched.

## Leads for other streams
- Release by an AI identity: d43db3e153 "Release 0.8.2" authored+committed by `Claude` (2026-10-12) and tag v0.8.2 → E05 (release process).
- House rules block imported from storytold/craft-contrib with a checksum-verifying workflow `.github/workflows/house-rules.yml` (7d8648dfcb, 2026-11-06) → E02.
- Conflicting attribution policy: Models credit compiled from trailers (docs/contributors.md:3-4) vs "No agent attribution" (AGENTS.md:20) → E02/E03.
- `Co-authored-by: coderabbitai[bot]` in 19 commits (all refs) → bot-suggested patches applied (E05).
- Model name variety in trailers (Claude Fable 5.1/5.2, Mythos 5.1, GPT-6-Luna, Qwen 3.8 Flash, Devin) → E03.
- Direct-push security series 2026-10-22 (c5a6afcf68…c3c6c63074) without PRs → E05/E07 security.
- Bulk machine-titled issue filing by davidmann4 (#13458–#13472) → issue/epic generation practice.

## Methods-relevant takeaways
- Integration trains: bundle N independent PRs into one branch to get one CI run and one conflict-resolution pass, then land by merge commit so the member PRs close themselves (E06-021, E06-022).
- Record conflict resolutions in the merge commit message, file by file with the reasoning (38609e5615, 4365c0537d) (E06-022).
- "CI only (do not merge)" PRs as a cheap combined-test gate before merging members one by one (E06-021).
- Splitting a large agent change by crate into PRs merged back-to-back keeps history reviewable per area, even when nobody reviews the PRs (E06-027).
- Encoding the issue number in the branch name and squash subject (`fix/<issue>-slug`, `Title (#issue) (#PR)`) gives cheap issue→commit traceability. It erodes when merge style changes (E06-031).
- Structural parallel-agent rules (own target dir, new module per feature, atomic manifest writes, wait instead of fixing others' broken files) from day 1 (E06-050).
- Shared generated/tracker files become conflict hot spots under high concurrency. Regenerate them centrally at the integration gate (E06-051, E06-032).
- Label-driven supervision (`ready to merge`, `waiting on author`, `needs decision`) plus bot review (CodeRabbit, Sonar) is how a few maintainers gate hundreds of in-flight PRs (E06-030, E06-041).
- Session trailers (`Claude-Session:`) make agent work countable and traceable per session. Coverage was partial here, which limits their value (E06-011).
- Explicit "who is accountable" rules for agent operators (house rule 1) and a response-time clock (rule 14) are written down, but arrived late (11-06) (E06-041).
- An issue-triage bot that applies labels, links in-progress PRs and flags duplicates keeps a 2,800-issue backlog navigable; epics with "free / being worked on / merged" tables act as claim boards (E06-033, E06-034).
- Branch-name attribution (`codex/*`) can contradict trailers. Use trailers and identity fields as primary (E06-025).
