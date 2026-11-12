# E03 — Quantitative git forensics (2026-11-12)

Scope: numbers describing the development process of `storytold/photocraft`, computed on
`main` pinned at `74330157cb601573ae4523a95bb9132822fc3918` (2026-11-12). Interpretation is
kept to what the numbers support; every number below comes from the two scripts and the CSVs
listed here. All figures VERIFIED (direct computation) unless labelled INFERRED.

## 0. Reproduction

```bash
UPSTREAM=<scratch>/upstream/photocraft          # read-only clone, PR heads fetched
python3 scripts/e03_git_quant.py "$UPSTREAM"    # ~30 s; writes data/E03_*.csv (43 files), prints a report
python3 scripts/e03_growth.py   "$UPSTREAM"    # ~7 s;  writes data/E03_growth.csv, data/E03_growth_crates.csv
```
Both scripts: Python 3 stdlib only, optional `--pin SHA`, read-only on the clone.
Core extraction (in `e03_git_quant.py`):
`git log <PIN> --no-renames --numstat --format=%x1e%H%x1f%P%x1f%an%x1f%ae%x1f%aI%x1f%cn%x1f%ce%x1f%cI%x1f%B%x1f`,
`git rev-list --first-parent <PIN>`, `git log <PIN> --no-merges --no-renames -p -U0 -- '*.rs'` (test attributes),
`git for-each-ref refs/pull refs/remotes/origin refs/tags`.
Growth (`e03_growth.py`): `git ls-tree -r -l <snap>` + `git cat-file --batch` on blobs.

## 1. Method & caveats (read before using any number)

| # | Caveat | Effect / how handled |
|---|---|---|
| C1 | **Two landing styles coexist.** Squash PRs land as one first-parent commit (`… (#N)`, committer `GitHub`); merge-commit PRs (`Merge pull request #N from owner/branch`) bring the whole branch history (incl. its own "merge main into branch" sync merges) onto main. | "Commits" is not a unit of work: a merge-style PR contributes many commits, a squash PR one. Every table distinguishes all / first-parent / non-merge where relevant. Prefer **first-parent** or **PR counts** for throughput. |
| C2 | **Merges have no numstat**; sizes/hot-spots use non-merge commits only. Side-branch commits of merge-style PRs and the squash commit of squash PRs are both "non-merge" — the same work is never counted twice on main *for a given PR*, but the granularity differs by PR style. | Size stats split `first_parent_squash` vs `side_branch`. |
| C3 | **Co-author trailers on squashed PRs.** GitHub squash bodies concatenate the PR's commit messages, so `Co-authored-by` lines can appear mid-body (sometimes with `* ` list markers). | Trailers are matched **anywhere in the body** (`^[\s*>-]*co-authored-by:` case-insensitive; both `Co-authored-by` and `Co-Authored-By` normalised). Counts are **per commit** (deduped per commit). Variant "last paragraph only": 4,081 vs 4,097 commits — negligible difference. |
| C4 | **Squash commits' author date = merge time.** For all 2,691 GitHub-committed first-parent non-merge commits, author time == committer time (`git log --first-parent --no-merges --format='%at %ct %cn'`). | Hour-of-day for squash commits reflects *merge* time, with a tz offset GitHub chose; `E03_hours.csv` also gives side-branch-only columns. |
| C5 | **Timezones.** Day/week buckets = committer date converted to **UTC**, ISO weeks (W40 starts Mon 2026-09-28; W46 is partial, Mon–Thu). "Local" hours use the commit's own recorded author offset. Author-date-by-day is also provided (`total_by_author_date_utc`). | |
| C6 | **Author aliasing.** Names sharing an e-mail (GitHub noreply addresses keyed by numeric user id) were union-merged → 628 raw names → **582 canonical authors**. Shared addresses (`noreply@anthropic.com`, `noreply@github.com`, `noreply@openai.com`, `*.invalid/.local`) are *not* used to merge. Mapping in `data/E03_alias_map.csv` (names only). Look-alike names with different e-mails were **not** merged (e.g. "Fabio Lissi" / "Fabio Lussi"). | Some genuine aliases may remain unmerged; some generic names ("Daniel", "scott") were merged only because they share an e-mail. |
| C7 | **AI attribution = explicit only** (brief rule 4). AI co-author: name matches `Claude…|GPT-…|Codex|OpenAI Codex|Cursor( Agent)?|Copilot|Codebuff|Devin|DeepSeek…|Qwen…|Gemini…|Grok…` **or** e-mail at anthropic.com/openai.com/cursor.com/codebuff.com/qwen.ai/deepseek.com/`+Copilot@users.noreply`. `coderabbitai[bot]` (9 commits) is counted as a *review bot*, not an AI co-author. Ambiguous identities (`photocraft-agent UNCONFIGURED`, `agent-346022`, `ebosido444-ai`, `envy-ai`) are **not** counted as AI. AI author identity = author name `Claude`, `Claude Opus 5.5`, `Codex` or anthropic/openai e-mail. "No AI attribution" means **unknown**, not "human". | |
| C8 | **Bots.** `dependabot[bot]` 2 commits; `Branch Sync` 16 merge commits; committer `GitHub` = web-flow. | Negligible for totals. |
| C9 | **Duplicates.** 241 non-merge commits share (author, subject) with another; 168 are extra copies, 69 have identical subject *and* numstat (cherry-pick/rebase copies on different branches). Example: `cb5243bf78` and `b97f342e16` (both 2026-11-11, "Fix main: SVG raster depth test…"). | ≤2 % inflation of non-merge counts (`data/E03_duplicates.csv`). |
| C10 | **`(#N)` on side-branch commits is author-written text**, often an *issue* number, not a PR (e.g. `9db37a9c49` "…(#13072)" landed via merge PR #13176). Only first-parent squash `(#N)` is treated as a PR number. | 1,461 side commits carry a `(#N)` suffix and are excluded from PR counts. |

## 2. Commits per week (E03_commits_weekly.csv; daily in E03_commits_daily.csv)

| ISO week | total | first-parent | merges | non-merge | fp non-merge | distinct authors | cumulative |
|---|---|---|---|---|---|---|---|
| 2026-W40 (Wed 09-30 → Sun 10-04) | 126 | 120 | 2 | 124 | 118 | 6 | 126 |
| 2026-W41 | 1,622 | 1,384 | 98 | 1,524 | 1,376 | 232 | 1,748 |
| 2026-W42 | 2,681 | 955 | 765 | 1,916 | 937 | 277 | 4,429 |
| 2026-W43 | 3,086 | 291 | 1,352 | 1,734 | 242 | 203 | 7,515 |
| 2026-W44 | 1,718 | 77 | 593 | 1,125 | 36 | 77 | 9,233 |
| 2026-W45 | 2,400 | 326 | 883 | 1,517 | 93 | 93 | 11,633 |
| 2026-W46 (partial, to 11-12) | 763 | 322 | 374 | 389 | 69 | 54 | 12,396 |
| **Total** | **12,396** | **3,475** | **4,067** | **8,329** | **2,871** | 582 | |

Reconciliation: weekly and daily sums both = 12,396 (asserted in script); `git rev-list --no-merges --count` = 8,329, `--merges` = 4,067.
First 14 days (UTC, total commits): 6, 10, 18, 35, 57, 108, 36, 200, 217, 390, 305, 366, 431, 528 (09-30 … 10-13).
Busiest days: 2026-10-21 780 commits (15 first-parent, 437 merges); 2026-10-22 767; 2026-10-13 528.

### First-parent landing kinds (E03_first_parent_kinds_weekly.csv)

| week | squash by GitHub with (#N) | merge PR commit | direct push (committer ≠ GitHub) | other |
|---|---|---|---|---|
| W40 | 45 | 2 | 71 | 2 |
| W41 | 1,326 | 8 | 50 | 0 |
| W42 | 925 | 12 | 6 | 12 |
| W43 | 197 | 49 | 45 | 0 |
| W44 | 29 | 41 | 6 | 1 |
| W45 | 90 | 233 | 3 | 0 |
| W46 | 63 | 253 | 0 | 6 |
| **Total** | **2,675** | **598** | **181** | 21 |

Direct (non-GitHub-committed) first-parent commits by author: Brandon Thomas 99, Dylan M. Taylor 36, Claude 14, Nigel Ihza Firdausy 10, others ≤3 (`E03_first_parent_direct_by_author.csv`).

### E03-001 — History size and shape
- Label: VERIFIED
- Source: main @ 74330157cb (2026-11-12); `data/E03_commits_weekly.csv`
- Data: 12,396 commits (8,329 non-merge, 4,067 merges); first-parent chain 3,475 (2,871 non-merge + 604 merges). Span 2026-09-30 → 2026-11-12 (44 UTC days).
- Method: `scripts/e03_git_quant.py`; cross-checked with `git rev-list --count/--merges/--no-merges`.
- Notes: 3,463 of the 4,067 merges are *side* merges (mostly "merge main into branch" syncs) brought in by merge-style PRs (C1).

### E03-002 — Landing style shifted from squash to merge commits
- Label: VERIFIED
- Source: `data/E03_pr_weekly.csv`, `E03_first_parent_kinds_weekly.csv`
- Data: share of landed PRs that were squash-merged: W40 95.7 %, W41 99.4 %, W42 98.7 %, W43 80.1 %, W44 41.4 %, W45 27.6 %, W46 19.9 %. Merge-PR commits 2 → 8 → 12 → 49 → 41 → 233 → 253 per week.
- Method: first-parent subjects: `^Merge pull request #(\d+) from` vs non-merge `\(#(\d+)\)\s*$`.
- Notes: why it shifted is not established here (→ E06). Because merge-style PRs import branch histories, raw commit counts from W43 on are inflated relative to PR counts (C1).

## 3. AI attribution (non-merge commits; E03_attr_weekly.csv)

| week | non-merge | AI co-author line | AI author identity | Claude-Session | Copilot-Session | Model-Effort | "Generated with" | **any AI attr.** | no AI attr. | human co-author |
|---|---|---|---|---|---|---|---|---|---|---|
| W40 | 124 | 105 | 0 | 0 | 0 | 0 | 0 | 105 (84.7 %) | 19 | 10 |
| W41 | 1,524 | 954 | 19 | 69 | 31 | 0 | 5 | 957 (62.8 %) | 567 | 493 |
| W42 | 1,916 | 1,011 | 19 | 60 | 0 | 0 | 3 | 1,021 (53.3 %) | 895 | 351 |
| W43 | 1,734 | 847 | 7 | 45 | 0 | 0 | 8 | 856 (49.4 %) | 878 | 161 |
| W44 | 1,125 | 415 | 6 | 17 | 0 | 0 | 0 | 415 (36.9 %) | 710 | 55 |
| W45 | 1,517 | 676 | 30 | 38 | 0 | 16 | 3 | 687 (45.3 %) | 830 | 116 |
| W46 | 389 | 89 | 0 | 9 | 0 | 9 | 0 | 89 (22.9 %) | 300 | 28 |
| **Total** | **8,329** | **4,097** | **81** | **238** | **31** | **25** | **19** | **4,130 (49.6 %)** | **4,199** | 1,214 |

First-parent non-merge only (one row per landed squash/direct change): 1,700 of 2,871 (59.2 %) carry any AI attribution.
Independent check: `git log main --no-merges -i -E --grep='co-authored-by:.*(anthropic\.com|openai\.com|cursor\.com|codebuff|copilot@|qwen\.ai|deepseek|…)'` → 4,095 (script: 4,097; the difference is list-marker-prefixed lines that `--grep` anchoring misses).

### Per co-author string, exactly as written (E03_attr_models_summary.csv; weekly in E03_attr_models_weekly.csv)

| string | non-merge commits | of which first-parent | all incl. merges | first day | last day |
|---|---|---|---|---|---|
| Claude Opus 5.5 | 3,158 | 1,355 | 3,604 | 2026-10-01 | 2026-11-11 |
| Claude Opus 5.5 (1M context) | 444 | 187 | 655 | 2026-10-04 | 2026-11-09 |
| Claude Sonnet 5.5 | 157 | 15 | 182 | 2026-10-05 | 2026-11-11 |
| Claude Fable 5.1 | 137 | 21 | 167 | 2026-10-08 | 2026-11-09 |
| Claude | 53 | 45 | 56 | 2026-10-08 | 2026-11-10 |
| Claude Opus 4.8 | 45 | 45 | 45 | 2026-10-02 | 2026-10-04 |
| Claude Haiku 5.5 | 40 | 17 | 42 | 2026-10-16 | 2026-10-30 |
| Cursor | 36 | 6 | 38 | 2026-10-09 | 2026-10-20 |
| Copilot | 31 | 31 | 31 | 2026-10-07 | 2026-10-08 |
| GPT-6 | 22 | 3 | 40 | 2026-10-12 | 2026-10-22 |
| Claude Fable 5.2 | 12 | 0 | 32 | 2026-11-10 | 2026-11-11 |
| Codex | 12 | 10 | 12 | 2026-10-12 | 2026-11-10 |
| Codebuff | 8 | 7 | 9 | 2026-10-23 | 2026-10-25 |
| Claude Opus 5 | 5 | 0 | 5 | 2026-10-31 | 2026-11-02 |
| Claude Sonnet 5 | 4 | 0 | 4 | 2026-10-11 | 2026-10-31 |
| Cursor Agent | 4 | 4 | 4 | 2026-10-14 | 2026-10-14 |
| Claude Mythos 5.1 | 4 | 4 | 4 | 2026-10-07 | 2026-10-08 |
| Claude Sonnet 4.6 | 3 | 0 | 3 | 2026-10-27 | 2026-10-28 |
| OpenAI Codex | 3 | 0 | 3 | 2026-10-17 | 2026-10-19 |
| GPT-6 (Codex) | 2 | 2 | 2 | 2026-10-09 | 2026-10-09 |
| Claude Opus 4.8 (1M context), Qwen 3.8 Flash, Claude Haiku 4.5, DeepSeek, Devin | 1 each | 1 each | 1 each | 10-05…10-14 | |

Days are committer-date UTC of the commits carrying the string (a squash commit's date is its merge date, C4). A commit can carry several strings, so the column does not sum to 4,097.
First occurrences (by committer date): Claude Opus 5.5 `1f1ddb2a47` (2026-10-01); Claude Opus 4.8 `0c2d4bfd1a` (2026-10-02); Claude Opus 5.5 (1M context) `b6a95b6c8d` (2026-10-04); Copilot `1cb5af9218` (2026-10-07); GPT-6 `61c52c08db` (2026-10-12; first *plain* `GPT-6` — the first GPT-6-family line is `GPT-6 (Codex)` on `7fd610741b`, 2026-10-09, previously not stated (corrected 2026-11-12, see errata #29)); Claude Fable 5.2 `e530d6c9f4` (2026-11-10). Command: `git log main -i -F --grep='<string>' --reverse --format='%h %cs' | head -1`.

AI author identities (E03_ai_author_identity.csv): `Claude` 62 non-merge + 32 merge commits (first `3bab0d4f52`, 2026-10-09); `Codex` 18 + 6; `Claude Opus 5.5` 1 + 1. Committer `Claude` on 102 commits.
Session trailers: `Claude-Session:` 238 non-merge commits, **62 distinct values**, `f94bb1dc9b` (2026-10-08) … `54ea149f2f` (2026-11-10). `Copilot-Session:` 31 commits, 5 distinct values, only 2026-10-07/08. `Model-Effort:` 25 commits (2026-11-07 … 2026-11-11), 8 distinct values:

| Model-Effort value (verbatim) | lines |
|---|---|
| Opus 5.5 drove; Opus 5.5 briefed; Sonnet 5.5 wrote at medium | 12 |
| Opus 5.5 drove and briefed; Sonnet 5.5 wrote at medium | 6 |
| Opus 5.5 drove and wrote (review fix, no brief) | 2 |
| Opus 5.5 drove and wrote | 2 |
| Opus 5.5 drove; Fable 5.1 briefed; Sonnet 5.5 wrote at medium | 2 |
| Opus 5.5 drove; Fable 5.1 decided; Sonnet 5.5 wrote at medium | 1 |
| Opus 5.5 drove and wrote (CI fix) | 1 |
| Opus 5.5 drove and resolved | 1 |

Human co-authors (context): `Brandon Thomas` appears as co-author on 678 non-merge commits; next FredApps 58, Fabio Lussi 38 (`E03_coauthors_nonai_top.csv`).

### Share of each human author's non-merge commits with AI trailers (top 25, aliases merged; E03_attr_by_author.csv)

| author | non-merge | AI co-author | % | most common string |
|---|---|---|---|---|
| David Mann | 978 | 964 | 98.6 | Claude Opus 5.5 |
| aiongg | 430 | 0 | 0.0 | — |
| Hector Villarreal | 417 | 348 | 83.5 | Claude Opus 5.5 |
| yoriswind | 416 | 0 | 0.0 | — |
| Brandon Thomas | 296 | 225 | 76.0 | Claude Opus 5.5 |
| Khawar Zamman Wani | 271 | 89 | 32.8 | Claude Opus 5.5 |
| vangel76 (+Valentin Klein) | 259 | 248 | 95.8 | Claude Opus 5.5 |
| Nigel Ihza Firdausy | 205 | 63 | 30.7 | Claude Opus 5.5 |
| Dylan M. Taylor | 195 | 9 | 4.6 | Codebuff |
| FredApps | 131 | 10 | 7.6 | Claude Opus 5.5 |
| rmsff | 120 | 0 | 0.0 | — |
| Higgs32584 | 118 | 118 | 100.0 | Claude Opus 5.5 |
| Trevor Brown | 115 | 114 | 99.1 | Claude Fable 5.1 |
| Finn Newick (+FinnNk) | 96 | 96 | 100.0 | Claude Opus 5.5 |
| Korg1ch | 94 | 1 | 1.1 | Claude Opus 5.5 |
| BFlat | 87 | 84 | 96.6 | Claude Opus 5.5 |
| skylar taylor-barrick | 78 | 1 | 1.3 | Codebuff |
| RickiNano | 75 | 28 | 37.3 | Claude Opus 5.5 |
| MarekSpodBiedry | 74 | 2 | 2.7 | Claude Opus 5.5 |
| dotCooCoo | 71 | 1 | 1.4 | Claude Opus 5.5 |
| jonathnwxh | 71 | 16 | 22.5 | Codex |
| Marco Arnulfo | 63 | 3 | 4.8 | Claude Opus 5.5 |
| ljkx | 60 | 42 | 70.0 | Claude Opus 5.5 |
| Vikram Bhaskaran | 59 | 10 | 16.9 | Claude Opus 5.5 |
| abc2cb | 58 | 44 | 75.9 | Claude Opus 5.5 |

Distribution is bimodal: authors are mostly near 0 % or >90 %. 0 % means "no explicit trailer", not "no AI" (C7).

### E03-003 — About half of non-merge commits carry explicit AI attribution
- Label: VERIFIED
- Source: `data/E03_attr_weekly.csv`
- Data: 4,130 / 8,329 non-merge (49.6 %); 1,700 / 2,871 first-parent non-merge (59.2 %). Share falls from 84.7 % (W40) to 22.9 % (W46, partial).
- Method: §1 C3/C7 rules.
- Notes: the falling share coincides with the rise of merge-style PRs and of authors with 0 % trailers (aiongg, yoriswind, rmsff); whether these authors use AI without trailers is unknown.

### E03-004 — "Claude Opus 5.5" dominates attributed commits
- Label: VERIFIED
- Source: `data/E03_attr_models_summary.csv`
- Data: Claude Opus 5.5 3,158 non-merge commits (77 % of 4,097 AI-co-authored), plus "(1M context)" variant 444. 25 distinct AI strings; non-Anthropic tools together < 4 % (Cursor 36+4, Copilot 31, GPT-6 22+2, Codex 12+3, Codebuff 8, others 1).
- Notes: model strings are whatever the tool wrote into the trailer; they are not verified model usage.

### E03-005 — Structured multi-model trailers appear only in the last week
- Label: VERIFIED
- Source: commits `b29fdc5a29` (2026-11-07 author date; 11-08 committer UTC, errata #19) … `cbd96a4de6` (2026-11-11); `data/E03_model_effort_values.csv`
- Data: 25 commits with `Model-Effort:` (non-merge; 27 incl. merges, all by Trevor Brown, merged by David Mann (cross-ref 2026-11-12, see errata #18)); 8 distinct values, e.g. "Opus 5.5 drove; Opus 5.5 briefed; Sonnet 5.5 wrote at medium" (12).
- Notes: documents a driver/briefer/writer role split in the commit metadata itself (→ E02/E06 for whether it is a documented convention).

### E03-006 — AI agents commit under their own identity rarely
- Label: VERIFIED
- Source: `data/E03_ai_author_identity.csv`
- Data: author `Claude` 94 commits (62 non-merge), `Codex` 24, `Claude Opus 5.5` 2 — 120 / 12,396 (1.0 %). 14 first-parent commits on main were committed directly by `Claude` (not via GitHub).

## 4. Authors (E03_authors_top40.csv, E03_authors_weekly.csv, E03_newcomers_daily.csv)

| week | distinct authors | newcomers | cumulative |
|---|---|---|---|
| W40 | 6 | 6 | 6 |
| W41 | 232 | 227 | 233 |
| W42 | 277 | 192 | 425 |
| W43 | 203 | 94 | 519 |
| W44 | 77 | 26 | 545 |
| W45 | 93 | 31 | 576 |
| W46 | 54 | 6 | 582 |

Top authors (canonical, all commits incl. merges; first/last = author date UTC; active = distinct author days):

| author | commits | non-merge | merges | first-parent | first | last | active days |
|---|---|---|---|---|---|---|---|
| David Mann | 2,523 | 978 | 1,545 | 534 | 10-09 | 11-12 | 35 |
| aiongg | 1,113 | 430 | 683 | 74 | 10-16 | 11-02 | 18 |
| yoriswind | 508 | 416 | 92 | 0 | 10-30 | 11-08 | 10 |
| Hector Villarreal | 431 | 417 | 14 | 8 | 10-18 | 11-12 | 16 |
| Khawar Zamman Wani | 365 | 271 | 94 | 63 | 10-14 | 11-11 | 24 |
| vangel76 | 356 | 259 | 97 | 167 | 10-10 | 11-09 | 25 |
| FredApps | 325 | 131 | 194 | 74 | 10-12 | 11-11 | 16 |
| Brandon Thomas | 301 | 296 | 5 | 289 | 09-30 | 11-03 | 26 |
| Nigel Ihza Firdausy | 229 | 205 | 24 | 138 | 10-05 | 10-23 | 14 |
| Dylan M. Taylor | 225 | 195 | 30 | 154 | 10-11 | 11-12 | 23 |
| Higgs32584 | 179 | 118 | 61 | 0 | 10-14 | 11-06 | 12 |
| Trevor Brown | 146 | 115 | 31 | 0 | 11-02 | 11-11 | 9 |

(Rows 13–40 in CSV.) Top-1 author = 20.4 % of all commits; top-10 = 51.4 % (6,376/12,396).

**Who merges.** All 598 first-parent `Merge pull request #N from` commits (599 by a plain `^Merge pull request` subject match, errata #35) have committer `GitHub`; the *author* of a web-flow merge commit is the person who clicked merge: David Mann 356, Tanish Manku 71, aiongg 68, FredApps 48, Dylan M. Taylor 26, skylar taylor-barrick 19, BFlat 8, Brandon Thomas 2, five others 1 each (603 incl. 5 side). Source owners of those 603: **111 distinct owners; `storytold` 23 (3.8 %)**, forks 580 — top davidmann4 76, hectorviov 65, rmsff 60, aiongg 28, RickiNano 26 (`E03_mergepr_by_source_owner.csv`). Who squash-merged a squash PR is **not recoverable** from git (author = PR author, committer = GitHub).
Local merge-commit makers (committer = author): David Mann 1,176, aiongg 615, FredApps 146, vangel76 97, Khawar Zamman Wani 93, yoriswind 92 (`E03_merge_commit_committers.csv`).

### E03-007 — 582 contributors in 6 weeks, front-loaded
- Label: VERIFIED
- Source: `data/E03_authors_weekly.csv`
- Data: 582 canonical author identities; 425 had appeared by end of W42 (day 19); weekly distinct authors peak 277 (W42) then 54–93.
- Notes: includes AI identities (Claude, Codex) and bots; aliasing caveat C6.

### E03-008 — Merge-button concentration
- Label: VERIFIED
- Source: `data/E03_mergepr_by_merger.csv`
- Data: David Mann authored 356 / 603 (59 %) web-flow merge-PR commits; 96.2 % (580 / 603) of merged merge-style PRs came from fork branches (previously stated 97 %; `data/E03_mergepr_by_source_owner.csv`, 23 from `storytold`) (corrected 2026-11-12, see errata #40).

## 5. PR flow (E03_pr_daily.csv, E03_pr_weekly.csv, E03_pr_heads_status.csv)

- Landed PRs identified from first-parent subjects: **2,687 distinct squash PR numbers** (2,690 commits; 3 numbers recur) + **598 merge-commit PRs** = **3,285** distinct numbers, no overlap (3,288 landings, since three squash numbers recur, errata #20; 598 uses the regex `^Merge pull request #(\d+) from`, 599 by plain subject match, errata #35); 4 more first-parent non-PR merges carry `(#N)`.
- Peak PR-landing days (UTC): 10-09 332, 10-13 311, 10-10 258, 10-12 245, 10-11 224.
- `refs/pull/N/head`: **6,480** heads, numbers 8 … 13,454.

| PR head status | heads |
|---|---|
| head is ancestor of main **and** number in a first-parent subject | 608 |
| ancestor, number only mentioned in some other main subject (e.g. "Merge PR #N into … batch", integration PRs) | 908 |
| ancestor, number absent from main subjects | 35 |
| **not** ancestor, number in first-parent subject (typical squash-merged) | 2,662 |
| not ancestor, number mentioned elsewhere | 29 |
| not ancestor, number absent (closed / open / superseded / landed by other means) | 2,238 |

Limits: (a) a squash-merged PR's head is never an ancestor, so "ancestor" alone undercounts; (b) a PR can land via another PR (batch/integration branches) — its head becomes an ancestor without its number in a first-parent subject (the 908+35); (c) "not ancestor + absent" mixes closed, still-open and re-done PRs — open/closed state is not in git; (d) 15 numbers that landed have no fetched head.
So **merged (any evidence) ≈ 4,213 heads (65 %)**, no evidence 2,238 (35 %) — INFERRED upper/lower bounds, not GitHub state.

Number-space growth (`running_max_*` columns): highest `#N` in first-parent subjects 1,489 by 10-08, 5,105 by 10-13, 7,564 by 10-18, 9,989 by 10-28, 12,190 by 11-07, 13,416 by 11-12; highest PR-head number 13,454.

### E03-009 — Implied issue volume (shared issue/PR number space)
- Label: INFERRED
- Source: `data/E03_pr_heads_status.csv`, `E03_pr_daily.csv`
- Data: max number 13,454 − 6,480 PR heads ⇒ ≈ 6,974 numbers not used by surviving PRs.
- Chain: GitHub issues and PRs share one counter; refs/pull exists for every PR not deleted by GitHub ⇒ the remainder are issues (or deleted PRs/spam). Roughly half the number space is issues. Not verified against the issue tracker (blocked, E00-004).

## 6. Branch namespaces (E03_branch_prefixes.csv; weekly: E03_branch_prefixes_weekly_mergepr.csv / _into.csv)

Columns: remote branches (367, excl. `origin/HEAD`); source branch of `Merge pull request … from owner/<branch>` (603 occurrences, all distinct); target branch of sync merges `Merge … into <branch>` (2,116 occurrences, 710 distinct). 1,348 merges match neither pattern (e.g. "Merge remote-tracking branch 'origin/main'" without "into").

| prefix | remote | merge-PR source | sync "into" occ. | sync "into" distinct |
|---|---|---|---|---|
| `fix/` | 122 | 343 | 737 | 294 |
| `community/` | 45 | 7 | 1 | 1 |
| `feat/` | 38 | 53 | 349 | 86 |
| `claude/` | 38 | 6 | 18 | 10 |
| `issue-*` | 28 | 0 | 2 | 1 |
| `pr/` | 15 | 1 | 3 | 2 |
| `sonar*` | 9 | 2 | 0 | 0 |
| `ci/`, `ci-*` | 9 | 9 | 0 | 0 |
| `switch-*` | 8 | 0 | 0 | 0 |
| `perf/` | 7 | 26 | 37 | 22 |
| `release*` | 6 | 0 | 1 | 1 |
| `codex/` | 5 | 40 | 62 | 21 |
| `chore/` | 4 | 4 | 0 | 0 |
| `jobs/` | 3 | 0 | 0 | 0 |
| `docs/` | 3 | 2 | 19 | 2 |
| `land/` | 2 | 0 | 0 | 0 |
| `fix-*` | 2 | 7 | 6 | 3 |
| `batch/`, `test/`, `dependabot/`, `main` | 1 each | 0/1/2/2 | 0/0/0/24 | |
| `integration*` | 0 | 24 | 62 | 14 |
| `security/` | 0 | 11 | 0 | 0 |
| `feature/` | 0 | 1 | 15 | 4 |
| `integ-batch*`, `copilot/`, `cursor/` | 0 | 0 | 0 | 0 |
| other with `/` | 6 | 9 | 53 | 33 |
| other, no `/` | 13 | 53 | 724 | 214 |
| **Total** | **367** | **603** | **2,116** | **710** |

Most frequent "other" prefixes: `pr-*` 53 distinct sync targets, `review/` 6, `ahdfix-*` 5 (`E03_branch_other_prefixes.csv`). Merge-PR `fix/` sources by week: 0,0,3,5,12,142,181.

### E03-010 — Branch naming: `fix/` dominates; AI-named namespaces are a minority
- Label: VERIFIED
- Source: `data/E03_branch_prefixes.csv`
- Data: `fix/` = 33 % of remote branches, 57 % of merge-PR sources. `claude/` 38 remote but 6 merge-PR sources; `codex/` 5 remote but 40 merge-PR sources.
- Notes: branch names are attribution signals only where they name a tool (`claude/`, `codex/`); squash PR branch names are not in git (lost on squash).

## 7. Change size (E03_size_summary.csv, E03_size_weekly.csv, E03_largest30.csv)

Non-merge, `--no-renames` numstat (binary files count 0 lines; renames counted as delete+add).

| subset | n | ins median | ins p90 | ins max | del median | del p90 | files median | files p90 | files max |
|---|---|---|---|---|---|---|---|---|---|
| all non-merge | 8,329 | 52 | 418 | 107,573 | 5 | 54 | 2 | 10 | 572 |
| AI-attributed | 4,130 | 51 | 364 | 34,545 | 5 | 37 | 2 | 11 | 345 |
| no AI attribution | 4,199 | 52 | 484 | 107,573 | 5 | 101 | 2 | 9 | 572 |
| first-parent (squash/direct) | 2,871 | 82 | 583 | 44,421 | 6 | 43 | 3 | 17 | 296 |
| side-branch | 5,458 | 40 | 361 | 107,573 | 4 | 62 | 2 | 7 | 572 |
| first-parent, AI | 1,700 | 88.5 | 631 | 34,545 | 7 | 45 | 3 | 19 | 246 |
| first-parent, no AI | 1,171 | 71 | 514 | 44,421 | 5 | 40 | 2 | 12 | 296 |

Weekly median insertions (all): 69, 92, 53, 36, 64, 43, 60. Total +2,151,549 / −956,046 lines.
Largest commits (ins+del): `501b7f3459` 2026-10-26 aiongg "refactor(engine): move the *_cmds modules under cmd/" (+107,573/−107,472, 460 files); `acc88b3203` 2026-11-08 Martin Ball "chore(i18n): delete the in-repo catalogs…" (−145,893); `a6428d3dfb` 2026-10-22 aiongg "Build each crate's integration tests as one binary" (572 files); early bulk commits by Brandon Thomas `16941f7198` "one-shot" (+42,241, 2026-09-30), `536a7346fb` (+44,421, 10-01), `aa87012aab` (+34,545, 10-02, subject contains "(+ in-progress work of other agents)"). 9 of the top 30 are aiongg's 2026-10-26 module-move series (moves inflate size due to `--no-renames`).

**Tests heuristic** (stated): a non-merge commit "touches tests" if any changed path matches `(^|/)tests?/|_tests?\.rs$|(^|/)tests?\.rs$|(^|/)testkit/` **or** its `-U0` patch adds a line matching `^\+\s*#\[(test|cfg\(test\))\]` in a `.rs` file. Inline Rust unit tests are therefore caught; edits to existing tests inside non-test-named files without new attributes are not.

| week | non-merge | test path | adds test attr | either | % |
|---|---|---|---|---|---|
| W40 | 124 | 53 | 74 | 80 | 64.5 |
| W41 | 1,524 | 804 | 1,230 | 1,300 | 85.3 |
| W42 | 1,916 | 906 | 1,362 | 1,485 | 77.5 |
| W43 | 1,734 | 770 | 980 | 1,191 | 68.7 |
| W44 | 1,125 | 716 | 692 | 834 | 74.1 |
| W45 | 1,517 | 1,160 | 900 | 1,254 | 82.7 |
| W46 | 389 | 296 | 246 | 315 | 81.0 |
| **Total** | **8,329** | 4,705 | 5,484 | **6,459** | **77.5** |

AI-attributed: 3,337 / 4,130 (80.8 %) touch tests; no AI attribution: 3,122 / 4,199 (74.4 %).

### E03-011 — Typical change is small and usually carries tests
- Label: VERIFIED
- Source: `data/E03_size_summary.csv`, `E03_tests_weekly.csv`
- Data: median non-merge commit +52/−5 lines in 2 files; landed (first-parent) changes median +82 in 3 files; 77.5 % of non-merge commits touch tests by the stated heuristic.
- Notes: AI vs non-AI differences in size are small (medians 51 vs 52); not a basis for causal claims.

## 8. Codebase growth (E03_growth.csv, E03_growth_crates.csv)

Snapshot = last first-parent commit of each UTC day (first 14 days) / ISO week, plus the pin.

| snapshot | commit | .rs files | Rust LOC (non-blank) | `#[test]` | `#[cfg(test)]` | packages | docs/*.md (top / all) | AGENTS.md bytes / lines |
|---|---|---|---|---|---|---|---|---|
| day 09-30 | 14c5c1bc51 | 228 | 68,332 | 915 | 103 | 27 | 6 / 7 | 4,631 / 68 |
| day 10-01 | 309e939b9a | 349 | 116,206 | 1,379 | 181 | 27 | 9 / 10 | 8,656 / 95 |
| day 10-02 | 79fd79c2ae | 437 | 150,765 | 1,655 | 248 | 27 | 10 / 11 | 8,658 / 97 |
| day 10-03 | 5f84a7add8 | 448 | 152,956 | 1,692 | 258 | 27 | 10 / 11 | 8,658 / 97 |
| W40 end (10-04) | ff53be714d | 529 | 176,430 | 2,001 | 302 | 31 | 11 / 12 | 11,800 / 115 |
| day 10-05 | 3423864502 | 645 | 217,343 | 2,584 | 371 | 32 | 12 / 13 | 15,318 / 133 |
| day 10-06 | ba9272be7d | 673 | 227,363 | 2,760 | 389 | 32 | 13 / 14 | 15,804 / 133 |
| day 10-07 | 6f39aba7f2 | 748 | 263,561 | 3,467 | 446 | 33 | 19 / 20 | 15,804 / 133 |
| day 10-08 | 4cb7cf3931 | 811 | 290,823 | 3,977 | 486 | 33 | 20 / 21 | 17,206 / 151 |
| day 10-09 | 1330899aca | 965 | 349,237 | 5,082 | 583 | 35 | 25 / 26 | 17,206 / 151 |
| day 10-10 | 953390a36e | 1,066 | 388,840 | 5,856 | 648 | 35 | 39 / 40 | 18,322 / 159 |
| W41 end (10-11) | f1059f1885 | 1,161 | 430,996 | 6,566 | 724 | 35 | 44 / 45 | 18,448 / 159 |
| day 10-12 | 5981a02e64 | 1,236 | 471,251 | 7,300 | 757 | 35 | 46 / 47 | 18,448 / 159 |
| day 10-13 | 99e1138877 | 1,305 | 506,751 | 8,032 | 802 | 35 | 50 / 51 | 18,448 / 159 |
| W42 end | 4d4de45305 | 1,384 | 552,308 | 9,045 | 862 | 37 | 51 / 72 | 18,573 / 159 |
| W43 end | 3877bb1dbe | 1,564 | 654,428 | 11,308 | 1,001 | 37 | 63 / 86 | 19,238 / 160 |
| W44 end | 24be8ea6e2 | 2,105 | 743,027 | 13,096 | 1,324 | 37 | 67 / 95 | 19,191 / 161 |
| W45 end | eda0af1911 | 2,479 | 909,024 | 16,636 | 1,579 | 37 | 77 / 105 | 24,700 / 214 |
| pin (W46) | 74330157cb | 2,594 | 955,603 | 18,014 | 1,765 | 34 | 82 / 110 | 24,989 / 214 |

"packages" = `Cargo.toml` files containing `[package]` (includes apps, xtask, examples).
Largest groups at pin (non-blank Rust LOC): crates/ui-egui 366,477 (12,477 at day 1), crates/engine 218,192, crates/algo 88,690, crates/io 68,789, crates/codecs 28,788, crates/compose 24,353, crates/text 19,119, crates/raw 18,431, crates/gpu 16,421, apps/photocraft 15,403. `crates/psd` (6,814 LOC on day 1) and `crates/heif` are absent at the pin (the pin commit replaces in-repo PSD code with `craft-psd`).

### E03-012 — ~0.96 M lines of Rust in 44 days
- Label: VERIFIED
- Source: `data/E03_growth.csv`
- Data: 68,332 → 955,603 non-blank Rust LOC; `#[test]` 915 → 18,014; AGENTS.md 4,631 → 24,989 bytes (68 → 214 lines); docs/**/*.md 7 → 110.
- Notes: includes tests and generated/data-like Rust; LOC is not effort.

## 9. Corrective activity & commit types (E03_corrective_weekly.csv, E03_cc_types_weekly.csv)

Subject regexes (case-insensitive) on non-merge commits:

| week | non-merge | revert | `Revert "` | fix main | main red/broken | flaky | fix ci | hotfix | regress* | follow-up | fmt | clippy |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| W40 | 124 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 4 |
| W41 | 1,524 | 0 | 0 | 1 | 3 | 4 | 0 | 0 | 4 | 10 | 11 | 6 |
| W42 | 1,916 | 4 | 3 | 1 | 3 | 2 | 0 | 0 | 13 | 8 | 36 | 9 |
| W43 | 1,734 | 7 | 6 | 0 | 0 | 2 | 0 | 0 | 8 | 5 | 29 | 4 |
| W44 | 1,125 | 4 | 3 | 0 | 0 | 1 | 1 | 0 | 21 | 3 | 4 | 33 |
| W45 | 1,517 | 6 | 5 | 0 | 0 | 1 | 1 | 0 | 15 | 4 | 8 | 7 |
| W46 | 389 | 0 | 0 | 11 | 0 | 1 | 0 | 0 | 3 | 0 | 4 | 3 |
| **Total** | 8,329 | 21 | 17 | 13 | 6 | 11 | 2 | 0 | 64 | 30 | 93 | 66 |

Regexes in script (`CORR`). "regress*" includes ~11 "regression test/guard" subjects (not corrective). "fix main" W46: 11 commits on 2026-11-11 (e.g. `a3c2f2e299` "Fix main: clippy after the 11-11 merges", `79a33dae9c` "Fix main: eyedropper cursor tests…(#12523)"); earlier "main red since #811 + #824" style i18n fixes (`25f211500b`, 2026-10-07). Plain-English subjects starting `Fix`/`Fixes`/`Fixed`: 1,257 non-merge.

Conventional-commit prefix (`^(type)(scope)?!?:`), non-merge:

| week | typed % | fix | test(s) | refactor | docs | perf | feat | i18n | ci | security | fix % of typed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| W40 | 13.7 | 2 | 2 | 0 | 3 | 6 | 2 | 0 | 0 | 2 | 11.8 |
| W41 | 22.2 | 201 | 16 | 2 | 20 | 17 | 38 | 26 | 13 | 1 | 59.3 |
| W42 | 34.6 | 299 | 84 | 14 | 44 | 60 | 67 | 50 | 18 | 3 | 45.1 |
| W43 | 37.9 | 310 | 103 | 19 | 50 | 35 | 31 | 24 | 18 | 54 | 47.1 |
| W44 | 44.8 | 67 | 56 | 257 | 38 | 42 | 13 | 21 | 8 | 0 | 13.3 |
| W45 | 21.2 | 146 | 74 | 1 | 21 | 15 | 18 | 19 | 9 | 1 | 45.5 |
| W46 | 31.4 | 66 | 31 | 0 | 5 | 4 | 5 | 0 | 6 | 0 | 54.1 |
| **Total** | **31.5** | **1,091** | 366 | 293 | 181 | 179 | 174 | 140 | 72 | 61 | **41.6** |

(style 40, chore 17, build 10 also; untyped 5,705.) First-parent only: 2,069 untyped of 2,871; fix 447, perf 85, feat 75, security 48, i18n 42 (`E03_cc_types_first_parent.csv`). W44 refactor spike = aiongg's 2026-10-26 module-move series.

### E03-013 — Explicit revert/"fix main" activity is low in count
- Label: VERIFIED
- Source: `data/E03_corrective_weekly.csv`
- Data: 17 `Revert "` commits and 13 "fix main" subjects among 8,329 non-merge; `fix:`-typed = 41.6 % of conventionally typed commits (1,091/2,624) but only 31.5 % of commits are typed at all.
- Notes: subject regexes miss corrective work described in prose; see E07 for qualitative failures. Example revert: `bb39b4a8dd` (2026-10-25) reverting "Merge PR #1199 …".

## 10. Temporal patterns (E03_hours.csv, E03_weekday.csv, E03_hours_top_authors_utc.csv, E03_author_stretches_top30.csv, E03_author_busiest_days.csv)

Non-merge commits by hour (author date): local-time peak 18:00 (633), trough 05:00 (184); UTC peak 18:00 (575), trough 09:00 (217). No hour has < 184 commits in either clock — activity spans all 24 h. AI-attributed local: peak 15:00 (244), trough 04:00 (81). Weekday (local): Sun 1,399 and Mon 1,362 highest; Fri 1,006 lowest; AI-attributed highest Sun 817.
Top authors' recorded tz offsets: David Mann +0000/+0100/+0200; aiongg +0000/−0400 (235 of 430 commits at 18:00 UTC); Hector Villarreal −0600; yoriswind −0700/−0800; Brandon Thomas −0400/−0500; Khawar Zamman Wani +0530; Nigel Ihza Firdausy +0700.
Repo-level: the longest gap with no commit (committer time) after day 1 is 10.8 h (from 2026-10-06 00:54 UTC); after 2026-10-06 no gap exceeds 5.2 h (`E03_repo_quiet_gaps_top10.csv`).

Per-author continuous stretches (consecutive author timestamps ≤ 60 min apart; top 5):

| author | hours | commits | start (UTC) |
|---|---|---|---|
| yoriswind | 17.7 | 122 | 2026-11-01 13:33 |
| David Mann | 15.9 | 193 | 2026-11-07 10:51 |
| Hector Villarreal | 14.7 | 98 | 2026-11-07 16:55 |
| yoriswind | 12.2 | 60 | 2026-11-04 17:00 |
| David Mann | 10.7 | 128 | 2026-10-22 09:50 |

Busiest day and burst structure (non-merge, author dates; "disjoint areas" = consecutive commits ≤ 5 min apart whose touched areas — `crates/<x>`, `apps/<x>` or top dir — do not overlap):

| author | busiest day | commits | median gap (min) | gaps ≤ 5 min | all pairs ≤ 5 min | of which disjoint areas | AI-attributed (all days) |
|---|---|---|---|---|---|---|---|
| David Mann | 10-25 | 103 | 4.6 | 52 | 377 | 183 | 964 / 978 |
| aiongg | 10-26 | 262 | 0.0 | 242 | 327 | 90 | 0 / 430 |
| Hector Villarreal | 11-01 | 83 | 2.8 | 57 | 175 | 47 | 348 / 417 |
| yoriswind | 11-04 | 109 | 4.2 | 62 | 149 | 33 | 0 / 416 |
| Brandon Thomas | 10-05 | 65 | 1.1 | 34 | 99 | 41 | 225 / 296 |
| Dylan M. Taylor | 10-22 | 42 | 1.9 | 34 | 114 | 76 | 9 / 195 |
| Nigel Ihza Firdausy | 10-13 | 46 | 2.5 | 28 | 98 | 39 | 63 / 205 |
| rmsff | 11-10 | 60 | 0.3 | 33 | 58 | 1 | 0 / 120 |

### E03-014 — Same-identity commit bursts touching unrelated areas
- Label: VERIFIED (numbers) / INFERRED (meaning)
- Source: `data/E03_author_busiest_days.csv`
- Data: David Mann: 377 consecutive-commit pairs ≤ 5 min apart, 183 of them in disjoint code areas; 103 commits on 2026-10-25 with 4.6-min median gap.
- Notes: consistent with parallel sessions under one identity, but equally with batch rebasing/committing prepared work (aiongg's 0.0-min median = identical author timestamps of a scripted series). Author dates survive rebase; do not read as proof of parallel agents.

## 11. Releases (E03_releases.csv, E03_tags_off_main.csv)

27 tags (lightweight). Ordered by commit date; "commits since prev" = `git rev-list --count prev..tag` (first-parent in brackets).

| tag | commit | date (UTC) | on main | since prev (fp) | days |
|---|---|---|---|---|---|
| v0.1.0 / v0.1.1-rc.4 | 4eb75d6370 | 10-01 18:23 | yes | 14 (14) | — |
| v0.1.1-rc.5 | c3bd22269f | 10-02 17:47 | yes | 18 (18) | 0.98 |
| v0.1.1 | 7750529bbb | 10-03 13:55 | yes | 29 (29) | 0.84 |
| v0.2.0 | ad86321738 | 10-05 04:21 | yes | 70 (64) | 1.60 |
| v0.3.0 | 60224d3fb7 | 10-07 10:10 | yes | 187 (187) | 2.24 |
| v0.5.0 | e5e3e39752 | 10-08 14:01 | yes | 205 (205) | 1.16 |
| v0.6.0 | 0c72d95425 | 10-10 02:11 | yes | 566 (520) | 1.51 |
| v0.7.0 | 7926161595 | 10-11 01:36 | yes | 244 (244) | 0.98 |
| v0.8.2 | d43db3e153 | 10-12 16:57 | yes | 422 (417) | 1.64 |
| v0.9.0 | c699e3cda6 | 10-14 14:16 | yes | 442 (394) | 1.89 |
| v0.10.0 | 8407d9ccb1 | 10-18 01:28 | yes | 297 (263) | 3.47 |
| v0.11.1 | 46e538b3a2 | 10-20 12:47 | yes | 387 (169) | 2.47 |
| v0.12.0 | 6a2d027ee2 | 10-21 17:59 | yes | 577 (8) | 1.22 |
| v0.13.0 | ce2a1e337a | 10-22 19:39 | yes | 1,816 (54) | 1.07 |
| v0.14.0 | ff47388101 | 10-23 00:06 | yes | 27 (9) | 0.19 |
| v0.15.1 | 60c87b9884 | 10-23 21:11 | yes | 66 (31) | 0.88 |
| v0.16.0 | b1794c6e06 | 10-25 13:45 | yes | 479 (82) | 1.69 |
| v0.17.0 | b8c3f3aa8e | 10-28 16:25 | yes | 1,179 (65) | 3.11 |
| v0.18.0 | 8a87a457ab | 10-31 03:26 | yes | 914 (35) | 2.46 |
| v0.19.0 | 2df9f80770 | 11-01 18:58 | yes | 231 (18) | 1.65 |
| v0.20.1 | 327c4cc82e | 11-03 00:47 | yes | 267 (11) | 1.24 |
| v0.20.2 | 7c12f64715 | 11-05 00:49 | **no** | 5 (5) | 2.00 |
| v0.21.0 | efb7ebd0c0 | 11-06 19:32 | **no** | 1,156 (3) | 1.78 |
| v0.22.0 | 5000240c6e | 11-09 11:33 | **no** (origin/release) | 1,420 (184) | 2.67 |
| v0.23.0 | 9963efcb2f | 11-11 19:53 | **no** (origin/release) | 1,291 (1) | 2.35 |
| v0.23.1 | 45066c4829 | 11-12 02:55 | **no** (origin/release) | 97 (1) | 0.29 |

Version numbers v0.4.x, v0.11.0, v0.15.0, v0.20.0 have no tag. v0.20.2 and v0.21.0 are contained in no remote branch.

### E03-015 — Release cadence ≈ every 1.6 days; release line leaves main from v0.20.2
- Label: VERIFIED
- Source: `data/E03_releases.csv`, `E03_tags_off_main.csv`
- Data: 26 distinct tagged commits in 41.4 days (v0.1.0 10-01 → v0.23.1 11-12); median inter-tag gap 1.6 days. Tags from v0.20.2 (2026-11-05) are not ancestors of main; v0.22.0–v0.23.1 lie on `origin/release`.
- Notes: tags are lightweight, so date = tagged commit's date, not tagging time.

## 12. File hot-spots (E03_hotspots_top40.csv, E03_churn_special_weekly.csv)

Top files by non-merge commits touching: `crates/ui-egui/src/lib.rs` 623, `crates/ui-egui/src/canvas.rs` 618, `docs/scorecard.md` 443, `crates/ui-egui/src/panels.rs` 429, then 16 i18n catalogs `crates/ui-egui/src/i18n/*.tsv` (298–381 each), `docs/control-protocol.md` 273, `Cargo.lock` 222, `crates/engine/src/lib.rs` 218, `crates/engine/src/commands.rs` 200, `docs/gaps.md` 199, `docs/ui-parity.md` 181, `docs/development.md` 169.

| week | AGENTS.md commits / lines | docs/** commits / lines | .github/workflows/** commits / lines | Cargo.lock commits |
|---|---|---|---|---|
| W40 | 13 / 177 | 36 / 2,905 | 5 / 506 | 19 |
| W41 | 14 / 89 | 397 / 9,397 | 44 / 1,677 | 54 |
| W42 | 2 / 2 | 354 / 4,905 | 22 / 476 | 44 |
| W43 | 3 / 9 | 292 / 11,698 | 29 / 741 | 53 |
| W44 | 3 / 21 | 166 / 62,891 | 23 / 512 | 14 |
| W45 | 1 / 56 | 233 / 3,656 | 7 / 100 | 29 |
| W46 | 2 / 4 | 29 / 385 | 5 / 153 | 9 |
| **Total** | **38 / 358** | **1,507 / 95,837** | **135 / 4,165** | 222 |

### E03-016 — Documentation files are among the most-edited files
- Label: VERIFIED
- Source: `data/E03_hotspots_top40.csv`
- Data: `docs/scorecard.md` is the 3rd most-touched file (443 commits); 5 docs/*.md files in top 40; docs/** touched by 1,507 non-merge commits (18 %). AGENTS.md touched by 38 commits, 27 of them in the first two weeks.
- Notes: W44 docs line spike (62,891) is dominated by FredApps' integration-protocol documents (`46c1347951`, `82da13f531`, 2026-10-29).

## Open questions / uncertainties
- Who squash-merged each squash PR and PR open/closed state are not in git (needs GitHub UI/API, blocked; WebFetch spot checks only).
- Model strings in trailers are tool-written self-reports; whether "Claude Opus 5.5 (1M context)" vs "Claude Opus 5.5" reflects distinct configurations is unknown.
- 4,199 non-merge commits have no AI attribution — AI use there is unknown, not absent. Several high-volume authors (aiongg, yoriswind, rmsff) have 0 trailers.
- Alias merging is e-mail-based only; residual unmerged aliases are likely (e.g. "Fabio Lissi"/"Fabio Lussi").
- Corrective-activity regexes on subjects are crude; "regression" mixes fixes and regression tests.
- Burst/parallelism metrics cannot separate parallel sessions from batch rebases (author dates survive rebase).
- The 2,238 PR heads with no merge evidence cannot be split into closed/open/superseded from git.
- Why the landing style flipped from squash (W41–W42) to merge commits (W45–W46) is not established.

## Leads for other streams
- E06: merge-PR concentration (David Mann 356/603 merges); ≈96 % (580 / 603) of merge-PR sources are forks (previously stated 97 %, errata #40); `Merge PR #N into …` subjects (24) and `Integration:`-prefixed subjects (381; `git log main --format=%s | grep -cE '^Integration:'`); `integration*` branches; release branch `origin/release` carries v0.22.0–v0.23.1.
- E06/E09: `aa87012aab` (2026-10-02, Brandon Thomas) subject "(+ in-progress work of other agents)"; FredApps 108-PR integration docs `46c1347951`, `82da13f531`, `255ecc81d0` (2026-10-29).
- E02: `Model-Effort:` trailers (`b29fdc5a29` … `cbd96a4de6`, 2026-11-07…11 author dates; 11-08…11 UTC, errata #19) with "drove / briefed / wrote" roles — check whether AGENTS.md/docs prescribe them; AGENTS.md size 4.6 kB → 25.0 kB, +5.5 kB in W45.
- E07: 2026-11-11 "Fix main" cluster (11 commits, e.g. `a3c2f2e299`, `71aad480b6`) after a merge wave; revert `bb39b4a8dd` (2026-10-25); duplicate fix commits `cb5243bf78`/`b97f342e16`.
- E05: `a6428d3dfb` (2026-10-22) "Build each crate's integration tests as one binary" (572 files); `#[test]` count 18,014 at pin; `docs/scorecard.md` most-touched doc.
- E04: removal of `crates/psd`/`crates/heif` in favour of external `craft-*` crates (pin `74330157cb`, `21bb9fda63`); aiongg module reorganisation 2026-10-26 (`501b7f3459` et al.).
- E08: Brandon Thomas as co-author on 678 commits — check public statements on role.

## Methods-relevant takeaways
- Machine-readable AI attribution in commit trailers (co-author + session id + model/effort role line) makes AI involvement measurable at scale; here it covers ~50 % of commits (E03-003, E03-004, E03-005).
- Adopting a richer, structured trailer (`Model-Effort:` with driver/briefer/writer roles) late shows the convention can evolve without tooling changes — but only 25 commits use it (non-merge; 27 total, all one contributor, errata #18), so adoption needs enforcement to be useful (E03-005).
- Landing-style choice matters for metrics: squash merges keep main's first-parent history one-change-per-PR; merge commits import sync merges and inflate commit counts 3–4× — pick one and measure on PRs, not commits (E03-001, E03-002).
- A high-throughput, many-contributor AI-assisted project kept typical changes small (median +52/−5, 2 files) and ~78 % of commits touching tests (E03-011).
- Very frequent tagging (median 1.6 days) with a split to a `release` branch once main velocity rose (E03-015).
- Merge-button authority concentrated in very few people despite 582 contributors (E03-008) — a review/integration bottleneck pattern to plan for.
- Agent identities committing under their own name are rare (1 %); attribution mostly flows through human authors with AI trailers, so per-human AI share is the better unit (E03-006, §3 author table).
- "Fix main" clusters after merge waves (E03-013) suggest batch integration needs a post-merge green-main step.
- Docs that agents and humans co-maintain (scorecard, gaps, parity, control protocol) become top hot-spots — budget for doc churn and merge conflicts on them (E03-016).
- Same-identity sub-5-minute commit bursts across unrelated crates are measurable but ambiguous; recording session ids per commit (as `Claude-Session:` does on 238 commits) is what would disambiguate parallel agents (E03-014).
