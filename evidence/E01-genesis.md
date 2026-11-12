# E01: Genesis and first week (2026-09-30 → 2026-10-08)

Stream: E01. Upstream: `storytold/photocraft`, pinned `main` = `74330157cb`. Clone path: see RESEARCH-BRIEF.
Unless stated otherwise, times are America/New_York (commit dates `-0400`, normalised with `TZ=America/New_York … --date=format-local`).
Scratch dir: `…/scratchpad/work/E01/` (no files were needed).

Scope note: the "first ~650 commits" in the brief match author dates through 2026-10-08. By committer date (ET), main has 762 commits up to the end of 2026-10-08. That is 6/15/24/24/61/106/59/210/257 per day (method in E01-030). The period covers tags v0.1.0 → v0.5.0.

---

## 1. Timeline

| Date/time (ET) | sha | Event | Significance | Label |
|---|---|---|---|---|
| 09-30 02:12 | `386b0566d3` | "init repo": README.md (4 lines: "photocraft / By the artcraft team") + `.gitignore` (`*~`) | Empty start, no spec committed | VERIFIED |
| 09-30 05:02 | `16941f7198` | "one-shot": 241 files, +42,241. 14 crates, 3 apps, xtask, CI, 6 docs, AGENTS.md (62 lines), 596 `#[test]` | Whole skeleton plus M0–M2 lands in one drop about 2h50m after init. No trailer | VERIFIED |
| 09-30 09:37 | `ae92ac20bf` | "continued wip": 181 files, +37,990/−404. Crates 14→19 | Second bulk drop. AGENTS.md gets "create manifests atomically" | VERIFIED |
| 09-30 11:15–11:37 | `a517477da8`,`b00b24739a`,`14c5c1bc51` | "readme, more impl" / "more work" / "readme, misc" | Terse messages, no trailers | VERIFIED |
| 10-01 08:25 | `536a7346fb` | "more algorithms, progress": +44,421. Adds `docs/parity.md` (518/625 menu items). AGENTS.md gets "Picking work", devlog rule and "Parallel agents" section | Parity-checklist planning method and multi-agent rules appear | VERIFIED |
| 10-01 10:49 | `d98bee4c94` | "progress, release workflows": `.github/workflows/release.yml`, `packaging/*`, `docs/releasing.md`, `docs/release-playbook.md`. AGENTS names sibling "…Craft" apps | Release pipeline on day 2 | VERIFIED |
| 10-01 13:25 | `1f1ddb2a47` | First commit with a `Co-Authored-By: Claude Opus 5.5` trailer. First mention of `craftrules` | Explicit AI attribution starts. Descriptive message bodies start at the same commit | VERIFIED |
| 10-01 13:27 | `1d61b33c54` | Release playbook moved to `../craftrules/release/playbook.md`. Local file becomes a pointer | Cross-repo shared standards | VERIFIED |
| 10-01 14:23 | `4eb75d6370` | Tags `v0.1.0` and `v0.1.1-rc.4` on the same commit (lightweight tags) | First tag | VERIFIED |
| 10-01 22:49 | `aa87012aab` | "…(+ in-progress work of other agents)": 162 files, +34,545. Body names parallel agents | First in-history statement of parallel agents at work | VERIFIED |
| 10-02 12:25 | `9c9a680e45` | "Remove references to Photon Studio from docs, AGENTS.md and code comments" | Reference app is erased from public docs | VERIFIED |
| 10-02 12:24 | `19739ccca8` | README: "clean-room reimplementation of Adobe Photoshop" plus a trademark notice | Public clean-room claim | VERIFIED |
| 10-02 13:47 | `c3bd22269f` | "Update AGENTS.md with tracking details" (committer GitHub, web edit). Tag `v0.1.1-rc.5` | Trivial web-UI edit | VERIFIED |
| 10-02 16:33 | `0c2d4bfd1a` | `docs/parity-estimate.md`: ~82% parity, "8 parallel agents", agent-hour estimates. Trailer `Claude Opus 4.8` | Effort is planned in agent-hours | VERIFIED |
| 10-03 02:56 | `58653e617b` | "625/625 menu items live (100%)" | Menu-breadth target reached | VERIFIED |
| 10-03 09:55 | `7750529bbb` | "Release 0.1.1", tag `v0.1.1` | First non-rc release tag after v0.1.0 | VERIFIED |
| 10-03 11:34 (author) | PR #8 head `ed6ee8a5ec` | First PR head ref (Torstein). Issue #1 was opened 2026-10-01 (WebFetch) | External community arrives | VERIFIED |
| 10-04 00:10 | `ed0b99964d` | AGENTS.md rule 9 "Never panic on input" | First rule added in response to failures | VERIFIED |
| 10-04 00:57 (commit) | `b6a95b6c8d` | First non-founder commit on main (storybored379, PR #17, committer GitHub) | Squash-merge workflow | VERIFIED |
| 10-04 01:25 | `b7cac05f69` | Founder's first PR-squashed commit "(#15) (#19)" | Founder switches to PR flow | VERIFIED |
| 10-04 10:08 | `9905db34ff` | First merge commit: "Merge pull request #32 from storytold/pr/license-standard" | Branch-based workflow | VERIFIED |
| 10-04 10:06 | `cf93edc99c` | LICENSE-MIT/APACHE, NOTICE, ATTRIBUTION.md ("craftrules standards/licensing.md") | Licensing and attribution | VERIFIED |
| 10-04 11:14 | `50a27e6c74` | "Never crash" section, `clippy.toml`, `unsafe_code = "forbid"` (#33). Fan-out into `pr/never-crash-*` branches #34–#59 | Rule pushed out through per-crate PRs | VERIFIED |
| 10-04 12:31 | `1fe689a7bf` | `book/` + SECURITY.md (Gh0stly, #35) | External security track | VERIFIED |
| 10-05 00:21 | `ad86321738` | Release 0.2.0 (#113), tag `v0.2.0` | First "signed and notarized release" (per ROADMAP.md progress log) | VERIFIED |
| 10-05 06:14 | `433b84fae7` | Roadmap "Honest parity assessment". AGENTS rule 0 says to read it first (#186) | Planning doc made the entry point for agents | VERIFIED |
| 10-05 10:53 | `0f955e6c82` | `scorecard/*.toml` + generated `docs/scorecard.md` (#239) | Machine-checked planning | VERIFIED |
| 10-07 17:10 (+0700) | `60224d3fb7` | Release 0.3.0 (#577) by BFlat, tag `v0.3.0` | Second maintainer cuts a release | VERIFIED |
| 10-07 21:22 | `44303db546` | About ▸ Contributors/Models tabs. AGENTS "Agents working for a contributor" (#898) | Model credits shipped in the product | VERIFIED |
| 10-08 10:01 | `e5e3e39752` | "Bump version to 0.5.0 (from 0.4.1)", tag `v0.5.0` | No v0.4.x tag exists | VERIFIED |
| 10-08 12:08 | `e3932fa7a3` | First `Claude-Session:` trailer cluster and first `claude/*` branch (callmeBalloch fork, committer "Claude") | Session-linked agent attribution from a contributor | VERIFIED |
| 10-08 14:57 | `3bab0d4f52` | First commit with author "Claude" (committer BFlat) | Agent as git author | VERIFIED |
| 10-10 | `607a8542f5`, `939c8f2c70` | `docs/decisions.md`, `docs/gaps.md`, `ROADMAP.md`, `docs/parity-checklist.md` appear (outside the window) | Later planning layer | VERIFIED |

---

## 2. Evidence entries

### E01-001: The repo starts empty; there is no spec or requirements document before code
- Label: VERIFIED
- Source: commit `386b0566d3` (2026-09-30 02:12)
- Data: `git show --stat 386b0566d3` → `.gitignore | 1`, `README.md | 4`. README text: "photocraft / =========== / By the artcraft team".
- Notes: No plan, spec or prompt file is ever committed before `16941f7198` (see E01-005 for where planning lived).

### E01-002: The "one-shot" commit inventory
- Label: VERIFIED
- Source: commit `16941f7198` (2026-09-30 05:02, author and committer Brandon Thomas, no body, no trailers)
- Data: `git show --shortstat` → `241 files changed, 42241 insertions(+)`. Rust: 124 `.rs` files, 33,955 lines (`git show --numstat --format= | awk '$3~/\.rs$/'`). `#[test]`: 596 occurrences in 61 files (`git grep -c '#\[test\]' 16941f7198`).
- Tree by dir (`git ls-tree -r --name-only | awk`):
  - 14 crates: algo(11 files), codecs(31), color(4), compose(6), doc(4), engine(8), geom(2), io(15), ops(2), paint(2), psd(29), raster(2), testkit(2), ui-egui(18)
  - apps: photocraft(4), photocraft-cli(2), photocraft-web(5)
  - `xtask/` (main.rs 272, layers.rs 498, stats.rs 149 lines; subcommands `layers|wasm|ci|corpus|stats`)
  - `.github/workflows/ci.yml` (109 lines)
  - `assets/` (71 icons, 6 font files), `Cargo.toml` (60), `Cargo.lock`, `.cargo/config.toml`
  - `crates/psd/README.md` (148), `crates/codecs/README.md` (121), fuzz crates for psd/codecs
- Docs (line counts from numstat): architecture.md 534, development.md 92, control-protocol.md 50, roadmap.md 39, ui-design.md 25, contributing.md 11. README.md 13 lines. AGENTS.md 62 lines.
- CI (`16941f7198:.github/workflows/ci.yml`): matrix `[ubuntu-latest, macos-latest, windows-latest]`, plus `cargo fmt --check`, `cargo test --workspace`, `clippy -D warnings`, `cargo xtask layers`, a wasm32 check job, and a fuzz job over 7 targets (psd parse/descriptor, codecs decode_*).

### E01-003: AGENTS.md at one-shot (62 lines). Summary of every rule
- Label: VERIFIED
- Source: `16941f7198:AGENTS.md:1-62`
- Content:
  - L1 title "guide for AI agents and contributors". L3: Rust only, no JS/TS.
  - §1 Orientation (L5–14): table of docs to read.
  - §2 Workspace map (L16–35): layers L0–L6. "**Layering is enforced** by `cargo xtask layers`" (L35). psd/codecs have no workspace deps. Nothing below ui-egui may use egui/eframe/winit/rfd.
  - §3 Golden rules (L37–45):
    1. Everything is a command (engine `commands.rs` + tests)
    2. No format or colour assumptions (8/16/32f, runtime colour model)
    3. Clean-room: "We studied Photon Studio (proprietary) and Photoshop for *behaviour and look only*. Never copy their code…" (L41)
    4. Tests are the gate (round-trip, synthetic, oracle, fuzz, PSD corpus must not regress)
    5. UI thin and data-driven (`state.rs` serde, `theme::Tokens`)
    6. Verify UI changes visually via `--control` + `ui.screenshot`
    7. Never break wasm
  - §4 "Before you finish a task" (L47–54): `cargo test -p`, `clippy -D warnings`, `xtask layers`, `xtask wasm`.
  - L56, parallel agents: "Parallel agents: use your own target dir (`CARGO_TARGET_DIR=target/agent-<name>`) … and edit only the crates you own."
  - §5 Tracking (L58–62): "`plan/` (local, gitignored): research, parity plan, execution plan, estimates." `docs/roadmap.md` holds milestones M0–M12. "`log/` (local, gitignored): the dev log."
- Notes: Parallel-agent operation is written into the very first commit of code.

### E01-004: Nothing in the one-shot states how it was produced
- Label: VERIFIED (absence)
- Source: commit `16941f7198` message is exactly `one-shot` (no body). `git grep -n -i -E 'claude|opus|codex|gpt|llm|prompt|one-shot' 16941f7198` (excluding assets and Cargo.lock) finds no tool or model attribution. "agent" appears only in AGENTS.md and the control-protocol context.
- The term "one-shot" is never explained. `git log main -i --grep='one-shot'` shows only later, unrelated uses (e.g. `0cb2e8cc99`, `afc817d1fa`). `git grep 'one-shot' 74330157cb -- '*.md'` finds only technical uses (consent/export).
- The only later self-description is the progress log, `74330157cb:ROADMAP.md:138` "| 2026-09-30 | First commit |".
- Notes: Per brief rule 4, AI involvement in `16941f7198` is UNKNOWN. The first explicit attribution comes 32 h later (E01-012).

### E01-005: Planning existed before code, in a private gitignored `plan/` directory
- Label: VERIFIED (statements) / INFERRED (that architecture.md came from plan/)
- Source: `16941f7198:.gitignore` contains `plan/` and `/log`. `16941f7198:AGENTS.md:60-62`. `16941f7198:docs/contributing.md:4` ("see `plan/` for the pending licence decision").
- `16941f7198:docs/architecture.md` (VERIFIED):
  - L3: "Status: draft v1 (2026-09-30)… candidates are discussed in [`rust-framework-options.md`]".
  - The tree diagram ends with "`└─ plan/  this directory`".
  - It links `photon-studio/06-menu-snapshot.md` and `photoshop-parity.md`.
  - `git ls-tree` and `git log --all` show that none of these files exist in any commit.
- INFERRED chain: architecture.md calls `plan/` "this directory" and links sibling files that were never committed. So it was most likely written inside the private `plan/` folder (research, parity plan, execution plan, estimates) and copied into `docs/`. The code was preceded by a written plan that is not public.
- Notes: The plan text survives only through this doc and roadmap.md.

### E01-006: Architecture doc framing (the plan's method)
- Label: VERIFIED
- Source: `16941f7198:docs/architecture.md:24`. Quote: "Photon does this, and it is the single best architectural idea in that app. Its 720-item menu tree (…06-menu-snapshot.md) is effectively our feature backlog."
- Also L30: "Clean-room with respect to Photon Studio… we must **not copy its source**… even though parts of it ship as readable source… Contributors should not paste from the extracted bundle."
- L426: "Photon does exactly this with Claude Code, Codex and Cursor, and it's worth copying the idea" (MCP/agent stdio).
- Notes: Method = study a reference app's behaviour and menu tree, then use that menu tree as the backlog.

### E01-007: Roadmap in the one-shot claims M0–M2 done on day 0, against an architecture plan of "1–2 wk" for Phase 0
- Label: VERIFIED
- Source: `16941f7198:docs/roadmap.md:3` "Updated 2026-09-30". L7–9: M0 Skeleton ✅, M1 Foundation ✅, M2 PSD v1 ✅ "134/135 real files byte-exact round trip". L39: "**Today's target: M0 + M1 + M2 + an M3 vertical slice.**"
- `16941f7198:docs/architecture.md` §15: "**0. Skeleton** (1–2 wk)".
- Notes: Each milestone has a DoD/acceptance column (L21: "must leave `main` green on all Tier-1 platforms plus a wasm build"). M11 DoD: "An agent completes 10 scripted edit tasks via MCP". M12: "`xtask parity` ≥ 90% of Photoshop menu checklist".

### E01-008: Explosive early growth in large checkpoint commits
- Label: VERIFIED
- Method: for each commit, `git grep -c '' $r -- '*.rs'` (sum = Rust lines), `git grep -c '#\[test\]'`, `ls-tree | grep -cE '^crates/[^/]+/Cargo.toml$'`, `git show --shortstat`
- Data:

| sha | msg | rs lines | tests | crates | shortstat (files, +, −) |
|---|---|---:|---:|---:|---|
| 16941f7198 | one-shot | 33,955 | 596 | 14 | 241, +42,241 |
| ae92ac20bf | continued wip | 69,345 | 898 | 19 | 181, +37,990, −404 |
| 14c5c1bc51 | readme, misc | 72,649 | 920 | 20 | 4, +1,063, −1 |
| 536a7346fb | more algorithms, progress | 115,594 | 1,317 | 20 | 213, +44,421, −768 |
| d98bee4c94 | progress, release workflows | 123,388 | 1,382 | 20 | 56, +2,603, −17 |
| aa87012aab | Analysis, notes… (+ other agents) | 157,418 | 1,634 | 20 | 162, +34,545, −689 |

### E01-009: Daily growth curve (end-of-day snapshot, first-parent main, ET)
- Label: VERIFIED
- Method: `r=$(git rev-list -1 --first-parent main --before="$d 23:59:59 -0400")`, then the counts as in E01-008. "crates" = `crates/*/Cargo.toml`, apps = `apps/*/Cargo.toml`.

| Day | endpoint | .rs files | Rust lines | `#[test]` | crates | apps | tracked files | AGENTS.md lines | docs/*.md |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 09-30 | 14c5c1bc51 | 228 | 72,649 | 920 | 20 | 3 | 384 | 68 | 7 |
| 10-01 | a9c3efbb51 | 433 | 158,514 | 1,642 | 20 | 3 | 659 | 95 | 10 |
| 10-02 | 2c40a93751 | 439 | 160,623 | 1,664 | 20 | 3 | 668 | 97 | 11 |
| 10-03 | 5f84a7add8 | 448 | 162,453 | 1,697 | 20 | 3 | 678 | 97 | 11 |
| 10-04 | 7e7864afae | 540 | 190,978 | 2,054 | 22 | 3 | 828 | 115 | 12 |
| 10-05 | a96a621dee | 645 | 231,347 | 2,590 | 23 | 3 | 961 | 133 | 13 |
| 10-06 | d38eefc8f7 | 675 | 243,804 | 2,800 | 23 | 3 | 1,000 | 133 | 14 |
| 10-07 | 452672765d | 776 | 290,211 | 3,611 | 24 | 3 | 1,127 | 151 | 21 |
| 10-08 | 3e8d54896d | 841 | 324,486 | 4,241 | 24 | 3 | 1,202 | 151 | 21 |

- Notes: Raw line counts include comments and blanks (not cloc). 158k Rust lines exist by the end of day 2. Growth slows on 10-02/10-03, then speeds up again once external PRs arrive (10-04 onward).

### E01-010: Commit-message style changes at one exact point
- Label: VERIFIED
- Method: per commit, `%s` length and non-trailer body line count, first 24 first-parent commits
- Data: `386b0566d3`…`d98bee4c94` (10 commits) have subjects of 8–27 chars, 0 body lines and no trailer ("one-shot", "continued wip", "more work", "work in progress", "progress, release workflows"). From `1f1ddb2a47` on, subjects run 48–100 chars with multi-line bodies and a `Co-Authored-By: Claude Opus 5.5` trailer. The exceptions are the terse untrailered `309e939b9a` "branding" and `1fc68c7411` "gitignore".
- Notes: Observed pattern: terse = no trailer, descriptive = trailer. Who wrote the terse ones is unknown (brief rule 4).

### E01-011: Attribution trailer census, first week
- Label: VERIFIED
- Method: `git log main --until=2026-10-09 --format=%B | grep -i -E '^(co-authored-by|claude-session)' | sed 's/<.*>//' | sort | uniq -c`
- Data (all commits, including squashed multi-trailer bodies):
  - Claude Opus 5.5: 419 (Co-Authored-By) + 305 (Co-authored-by)
  - "Claude Opus 5.5 (1M context)": 42+30
  - Claude Opus 4.8: 40+5
  - Claude Fable 5.1: 13+4
  - Claude Mythos 5.1: 13+4
  - bare "Claude": 24
  - Copilot: 53
  - `Claude-Session:` URLs: 54 (session_01UHgF…) + 13 (session_01GQPh…)
- Per-day count of commits whose message matches `co-authored-by: claude` (commit date ET; total/with-trailer): 09-30 6/0, 10-01 15/10, 10-02 24/20, 10-03 24/24, 10-04 61/55, 10-05 106/29, 10-06 59/23, 10-07 210/137, 10-08 257/170.
- Founder (author Brandon Thomas, through 10-08): 238 commits, 165 with a Claude trailer (`--author='Brandon Thomas' -i --grep='co-authored-by: claude' | wc -l`).

### E01-012: The first explicit AI attribution
- Label: VERIFIED
- Source: commit `1f1ddb2a47` (2026-10-01 13:25). Body ends "Co-Authored-By: Claude Opus 5.5". The first commit matching `--grep=Co-Authored-By` on main.
- Notes: About 32.4 h after the one-shot. A model-version mismatch shows up early: `0c2d4bfd1a` has the subject "remaining Opus 5.5 effort" but the trailer "Claude Opus 4.8". `ed0b99964d` also says 4.8. The trailer may therefore not be a reliable record of the model.

### E01-013: First explicit statement of parallel agents in history
- Label: VERIFIED
- Source: commit `aa87012aab` (2026-10-01 22:49). Quote: "Checkpoint: also contains compiling in-progress work from the parallel panels, type styles, File menu, photo, filters, UI-parity and fidelity agents, plus photocraft-cli serve."
- Notes: Commits here are workspace checkpoints that sweep up several agents' work, not one change each. That is the opposite of `docs/contributing.md:11` "Commits: small, focused" (`16941f7198`).

### E01-014: Parity estimate quantifies agent parallelism and plans effort in agent-hours
- Label: VERIFIED
- Source: `0c2d4bfd1a:docs/parity-estimate.md:3`: "how much Opus 5.5 work remains. Generated by assessment, not a tool".
- L55–57: "Two clocks: **agent-hours** (total model work) and **wall-clock** (with this session's observed ~6–8× parallelism…) This session landed ~70 menu items + major subsystems in a handful of wall-clock hours using 8 parallel agents".
- L75: "~25–40 wall-clock hours of parallel Opus 5.5 work" to 95%.
- Notes: This is the only first-week number for the agent count, and it is self-reported in a doc.

### E01-015: Generated parity checklist against the target app (planning method #1)
- Label: VERIFIED
- Source: `536a7346fb:docs/parity.md:3,5` (2026-10-01): "Generated by `cargo xtask parity` from `crates/ui-egui/src/menu_catalog.rs` (Photoshop's menu tree) and the live command registry. Do not edit by hand." "**518 of 625 menu items live (82.9%).**"
- The same commit adds to AGENTS.md: "When parity rises, raise `FLOOR` in `crates/ui-egui/src/parity.rs` (never lower it)."
- Progression: `aa87012aab` "Parity 600/625, FLOOR 595". `58653e617b` (10-03) "625/625 menu items live (100%)". Commits label progress "(parity 609)", "(parity 624/625, 99.8%)" (`a35fe54d7c`, `53b6f2bafb`).
- Notes: A target-app menu tree is encoded as data. A generator diffs it against the registry. A ratchet floor blocks regression. `58653e617b` carries a `Co-Authored-By: Claude Opus 4.8` trailer (cross-ref 2026-11-12, see errata #4).

### E01-016: "Picking work" and the devlog hand-off protocol (agent working rules)
- Label: VERIFIED
- Source: `536a7346fb:AGENTS.md` §4 "Picking work": "Priorities: important infrastructure first, then low-hanging parity, then the long tail." Sources: roadmap "Current focus" → `cargo xtask parity` → `log/devlog.md` "Still open".
- §5 "Before you finish a task" adds: "append a terse entry to `log/devlog.md`… Sessions can end abruptly (crashes, context limits), so the dev log plus a green tree is how the next agent picks up."
- §6 "Parallel agents" (L73–79): edit only files you own. Put new commands in a new `<area>_cmds.rs` module. "If someone else's in-progress edit breaks the build, wait and retry; don't fix their files." Write manifests atomically via temp file + `mv`. Delete `target/agent-*` dirs (~10 GB each).
- Notes: The dev log stays gitignored (`/log`), so the hand-off record is private.

### E01-017: Planning artefacts: first-appearance dates
- Label: VERIFIED
- Method: `git log main --diff-filter=A --reverse --format='%h %cd' -- <path> | head -1`

| Path | First add | Date |
|---|---|---|
| docs/roadmap.md | 16941f7198 | 09-30 05:02 |
| docs/parity.md | 536a7346fb | 10-01 08:25 |
| docs/release-playbook.md, docs/releasing.md, release.yml | d98bee4c94 | 10-01 10:49 |
| docs/parity-estimate.md | 0c2d4bfd1a | 10-02 16:33 |
| ATTRIBUTION.md, NOTICE, LICENSE-MIT/APACHE | cf93edc99c | 10-04 10:06 |
| clippy.toml | 50a27e6c74 | 10-04 11:14 |
| SECURITY.md, book/ | 1fe689a7bf | 10-04 12:31 |
| scorecard/*.toml, docs/scorecard.md | 0f955e6c82 | 10-05 10:53 |
| docs/decisions.md | 607a8542f5 | 10-10 05:05 |
| docs/gaps.md, ROADMAP.md, docs/parity-checklist.md | 939c8f2c70 | 10-10 15:09 |
| CLAUDE.md, .claude/, CONTRIBUTING.md (root), PR/issue templates, deny.toml, plan/, log/ | never on main | — |

### E01-018: Scorecard: generated, CI-checked planning (planning method #2)
- Label: VERIFIED
- Source: `0f955e6c82:docs/scorecard.md:3`: "Generated by `cargo xtask scorecard` from `perf/budgets.toml`, `perf/baseline.json`, `crates/io/tests/corpus.rs`, `scorecard/*.toml`… (CI runs `cargo xtask scorecard --check`)". Adds `scorecard/{automation,bugs,distribution,file_compat,reliability,tools,type,ui}.toml`.

### E01-019: "Honest parity assessment" becomes rule 0 for agents
- Label: VERIFIED
- Source: commit `433b84fae7` (10-05, #186). AGENTS diff: "0. **Read `docs/roadmap.md` → "Honest parity assessment" first.** … `docs/parity.md` (menu wiring) is not a measure of behaviour."
- Message: "overall estimate (feature surface ~60-70%, pro-switchable ~25-35%)".
- Notes: A self-correction. The menu-breadth metric (100% on 10-03, E01-015) is explicitly demoted.

### E01-020: Later planning docs (just outside the window) and their framing
- Label: VERIFIED
- `939c8f2c70:docs/gaps.md:5-8`: "Every known shortfall against Photoshop 2026 (27.11.0)… ranked by user impact… This is the work list agents pick from: take the highest-ranked entry that nobody is working on".
- `939c8f2c70:ROADMAP.md:3`: "**Stage: alpha** · next: beta… ~1,100–1,800 h away".
- `607a8542f5:docs/decisions.md:1,3`: "# Implementation decisions" / "## 2026-10-10: Smart Object contents identity (#2163)" (dated ADR-style log).
- `74330157cb:docs/target-app-parity.md:205`: "from the first commit (2026-09-30) to 2026-10-10: 1,152 commits on `main` and 1,004 merged PRs in 10.5 days. Median PR open-to-merge time is 3.4 h".

### E01-021: Clean-room claim evolves: from a named reference app to a public generic claim
- Label: VERIFIED
- Steps:
  - `16941f7198:AGENTS.md:41` and `docs/architecture.md:30` name Photon Studio and note it "ship[s] as readable source" and an "extracted bundle".
  - `9c9a680e45` (10-02 12:25) removes Photon Studio references from 7 files. AGENTS becomes "We studied Photoshop and other proprietary editors for *behaviour and look only*."
  - `19739ccca8` (10-02 12:24): README line 13 "an open-source, clean-room reimplementation of Adobe Photoshop, rebuilt in pure Rust". L246: "**Clean-room:** implemented from public specs and observed behaviour only." L315: Adobe trademark and non-affiliation notice.
  - `16941f7198:crates/psd/README.md:5`: "Clean-room implementation from Adobe's public *Photoshop File Formats Specification*… follows MIT-licensed psd-tools / ag-psd documentation".
  - `2149f7f646` (10-04): "NEF blocked (clean-room)".
- Notes: The clean-room status is asserted, not audited. No provenance process (e.g. separate spec/implementation teams) is documented in this window.

### E01-022: Licensing and attribution adopted from the shared standard on day 5
- Label: VERIFIED
- Source: commit `cf93edc99c` (10-04, PR #32, branch `pr/license-standard`). Message: "Adopt the Crafting Apps licensing standard (craftrules standards/licensing.md): LICENSE-MIT and LICENSE-APACHE (the repo had neither)…".
- `cf93edc99c:ATTRIBUTION.md:5-7`: "When you add an asset, add a row here in the same change; third-party assets must be permissively licensed".
- NOTICE L2: "Copyright (c) 2026 ArtCraft Team and the PhotoCraft contributors."
- Licence allowlist: none found in the window. `3e8d54896d:book/src/development/dependencies.md:7`: "No `cargo-deny` policy file… is present in the current tree." No `deny.toml` ever on main (E01-017).

### E01-023: External shared-standards repo `craftrules` and sibling "Craft" apps
- Label: VERIFIED
- Source:
  - `d98bee4c94:AGENTS.md:3` lists siblings "DrawCraft, FilmCraft, LightCraft, PrintCraft, DesignCraft, EffectsCraft, ArtCraft".
  - `1d61b33c54:AGENTS.md:3`: "Standards and learnings shared across the crafting apps live in `../craftrules`… Contribute reusable learnings there, never code; repos don't share code."
  - `1d61b33c54:docs/release-playbook.md`: "PhotoCraft is its reference implementation (`.github/workflows/release.yml`, `packaging/`, `cargo xtask version`)."
  - Standards cited: `standards/licensing.md` (`cf93edc99c`), `standards/never-crash.md` (`50a27e6c74`), `standards/contributors.md` (`44303db546`).
  - `f9b72468b4` (10-08, bfenty, #779): "the repository returns 404 to everyone outside the organization".
- Notes: Part of the process rules lives in a private repo. In this project, "reference implementation" means PhotoCraft is the reference *for the release recipe* used by sibling apps.

### E01-024: Release pipeline arrives on day 2, before any external user
- Label: VERIFIED
- Source: `d98bee4c94` adds `.github/workflows/release.yml` (L1: "every push to `release` builds signed installers for every platform"; `workflow_dispatch` with version override), `packaging/{macos,windows,linux,web}`, `xtask/src/{ico,version}.rs`.
- Tags (`git for-each-ref --sort=creatordate refs/tags`; all lightweight):
  - v0.1.0 and v0.1.1-rc.4 → `4eb75d6370` (10-01)
  - v0.1.1-rc.5 → `c3bd22269f` (10-02)
  - v0.1.1 → `7750529bbb` (10-03)
  - v0.2.0 → `ad86321738` (10-05)
  - v0.3.0 → `60224d3fb7` (10-07, by BFlat)
  - v0.5.0 → `e5e3e39752` (10-08, "from 0.4.1"; `git tag | grep -c 0.4` = 0)

### E01-025: Community arrival and switch to a PR workflow
- Label: VERIFIED (git) / VERIFIED via WebFetch summary (issue #1)
- Issue #1: https://github.com/storytold/photocraft/issues/1 (accessed 2026-11-12, via WebFetch summary). Opened by jlahijani on October 1, 2026: "I found this project from your comment on HN."
- First PR head: `refs/pull/8/head` = `ed6ee8a5ec` (Torstein, author 10-03 11:34, no Claude trailer). PR #11, #16, #17 heads carry Claude trailers (`git log -1 --format=%B refs/pull/N/head | grep -ic 'co-authored-by: claude'`).
- First non-founder commit on main: `b6a95b6c8d` (storybored379, #17, committer "GitHub" at 10-04 00:57).
- Founder's first `(#N)` commit: `b7cac05f69` "(#15) (#19)" (10-04 01:25).
- Distinct authors per day (`%an | sort -u`): 1,1,1,1,6,13,20,48,71. 131 distinct authors through 10-08.
- Committer census through 10-08: GitHub 715, Brandon Thomas 82, BFlat 43, Claude 23, Claude Opus 5.5 2.

### E01-026: First merge commits and branch-based flow
- Label: VERIFIED
- Source: `git log main --reverse --merges`:
  - `9905db34ff` (10-04 10:08) "Merge pull request #32 from storytold/pr/license-standard"
  - `6f1d0dc080` (10-04 11:56) "…#37 from storytold/ci/green"
  - Next is 10-08 (`e3932fa7a3`, fork branch `claude/kind-darwin-btjse2`).
- Oldest remote branches (`for-each-ref --sort=committerdate refs/remotes/origin`): 12 `pr/never-crash-*` (10-04), `fix/*`. Prefix census (whole repo): fix 122, community 45, feat 38, claude 38, pr 15.
- Notes: Squash merges dominate (committer GitHub). True merges are rare.

### E01-027: "Never crash" rule. Failure-driven steering, then a fan-out across crates
- Label: VERIFIED
- Source: `ed0b99964d` (10-04 00:10) adds rule 9: "A command's `run` closure and anything it calls must return `Err`, never panic… The panic_hunt integration test enforces this." Next: `bf111b524e` "add panic-fuzz harness".
- Then `50a27e6c74` (#33): "### Never crash (outranks feature work)", `unsafe_code = "forbid"`, "Standard: craftrules/standards/never-crash.md".
- Then 12 PRs (#34, #36, #38–#40, #54–#59) titled "Never crash: <crate group> is panic-free (Rule 9)", all committed 13:25–13:40 on 10-04.
- Notes: INFERRED: the per-crate split across branches committed within 15 minutes fits the AGENTS §6 rule that each agent edits only the crates it owns. Agent counts are not stated for these PRs.

### E01-028: Further early rules for agents
- Label: VERIFIED
- `10203e7a60` (10-05, #184): "**No Tauri, Electron or webview shells**".
- `536a7346fb:AGENTS.md:47` (rule 6): "When fetching assets, never put a person's name, email or other personal details in requests… use a generic `Photocraft-dev` User-Agent."
- `536a7346fb` rule 8: "**Performance is a feature.** … record before/after timings in the dev log."
- `44303db546` (10-07, #898): "**Agents working for a contributor:** when you prepare a PR, check whether your human's GitHub username has a `[people.<username>]` entry… ask them once". The same commit compiles a "Models" credits tab into Help ▸ About.

### E01-029: First agent-identity commits in git metadata
- Label: VERIFIED
- `e3932fa7a3` (10-08 12:08): author callmeBalloch, committer "Claude", branch `claude/kind-darwin-btjse2`.
- `f94bb1dc9b` is the first `Claude-Session: https://claude.ai/code/session_…` trailer on main.
- `3bab0d4f52` (10-08 14:57): author "Claude", committer BFlat.
- Notes: The founder's own commits in the window never carry `Claude-Session` (only Co-Authored-By).

### E01-030: Method for day counts
- Label: VERIFIED
- Method: `git log main --format=%h --since="$d 00:00 -0400" --until="$d 23:59:59 -0400" | wc -l` (committer date). Author-date counts (`--date=short | uniq -c`): 6, 15, 24, 26, 59, 102, 45, 188, 214 (= 679 to 10-08).

---

## Open questions / uncertainties
- How `16941f7198` (42k lines, 596 tests, about 2h50m after init) was produced is not stated anywhere in the repo. It has no trailer, the term "one-shot" is never defined, and no prompt or spec is committed. AI involvement for the first 10 commits is UNKNOWN.
- Contents of the private `plan/` (research, parity plan, execution plan, estimates), `log/devlog.md` and `craftrules` cannot be observed. Referenced but missing: `rust-framework-options.md`, `photon-studio/06-menu-snapshot.md`, `photoshop-parity.md`.
- Trailers name inconsistent models (Opus 5.5 vs 4.8 on related work, E01-012). Their accuracy as a model record cannot be checked.
- The "8 parallel agents" figure (E01-014) is self-reported. No per-agent identities exist in the first-week founder commits.
- Issues #1–#7 etc. come from a WebFetch summary only (lower fidelity). PR open/merge times were not fetched.
- The v0.4.x versions were never tagged, so the release history for 0.4 is unclear.
- Rust LOC is a raw line count (includes comments and blanks), not cloc.

## Leads for other streams
- Photon Studio as the original reference app, and its removal (`9c9a680e45`). The architecture says Photon "ship[s] as readable source" and mentions an "extracted bundle" (`16941f7198:docs/architecture.md:30`). This is relevant for a clean-room/IP stream.
- `docs/target-app-parity.md` calibration (1,004 merged PRs in 10.5 days, median 3.4 h open-to-merge): PR-throughput stream.
- Contributor/model credits system (`44303db546`, `contributors/people.toml`): attribution stream.
- Copilot co-author trailers (53 in week one) and Codex branch `codex/ui-suite-integration-20261010` (`97136485f0`): multi-vendor agent stream.
- BFlat as committer of "Claude"-authored commits and release 0.3.0 (`60224d3fb7`): maintainer-roles stream.
- Security track by Gh0stly (#35, #61, #72, #93): security stream.
- Community batch merges with re-authored follow-ups (`47884ada39` "Community batch follow-ups"): review-process stream.

## Methods-relevant takeaways
- Make the agent guide (AGENTS.md) a day-0 artefact. Put the architecture invariants, a "before you finish" checklist and parallel-agent rules in it from the first code commit (E01-003).
- Encode the target product's feature surface as data, generate a parity checklist from it, and ratchet with a never-lower FLOOR (E01-015).
- Then demote breadth metrics explicitly once they saturate, in favour of an "honest assessment" that agents must read first (E01-019).
- Give parallel agents mechanical isolation rules: a separate `CARGO_TARGET_DIR` per agent, file ownership, a new module per area, atomic manifest writes, and "don't fix others' in-progress files" (E01-003, E01-016).
- Plan for abrupt session ends: a dev log plus an always-green tree as the agent hand-off protocol (E01-016). Note the drawback: here the log is private.
- Enforce layering and portability in tooling (`cargo xtask layers`, wasm check) from the first CI file, not only in prose (E01-002).
- Turn observed failure classes into numbered rules backed by a test (panic_hunt). Then fan the fix out as per-crate PRs (E01-027).
- Put shared cross-project standards (release, licensing, never-crash) in a sibling rules repo. But keep cited rules reachable for outside contributors, which caused friction here (E01-023).
- Use generated, CI-checked scorecards (`--check`) instead of hand-edited status docs (E01-018).
- Ship release automation on day 2, so frequent tagged releases (v0.1→v0.5 in 8 days) are cheap (E01-024).
- Record AI involvement with explicit trailers from early on. Watch for model-name drift that weakens the record (E01-011, E01-012).
- Planning before code existed but stayed private (gitignored `plan/`). For auditability, commit the spec or plan, or a redacted version (E01-005).
