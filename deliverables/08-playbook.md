# 08 — AI Software Engineering Playbook (derived from PhotoCraft)

Audience: an engineer starting a large Rust desktop project (e.g. an IDE) with AI coding agents.
Basis: evidence streams E01–E09 on storytold/photocraft, pinned at main `74330157cb` (2026-11-12).
Templates that implement this playbook: `deliverables/09-templates/` (index in its `README.md`).

**Tags used on every practice**

| Tag | Meaning |
|---|---|
| `[PC-VERIFIED Exx-NNN]` | PhotoCraft demonstrably does this; the ID points to the evidence entry (and its primary sha/PR citation). |
| `[PC-PARTIAL Exx-NNN]` | PhotoCraft does a weaker or advisory version, adopted it late, or it failed; the text says how. |
| `[PROPOSED]` | Our improvement. Each names the observed failure it answers (E07/E05 IDs). Not a PhotoCraft practice. |

Terms used below (defined on first use in the evidence): **house rules** = the 15 shared rules copied
hash-verified into `AGENTS.md:1-52` from `storytold/craft-contrib` (E02-012); **integration batch** =
a branch bundling many PRs for one CI run and one conflict-resolution pass, then landed as one merge
(E06-021, E06-022); **scorecard** = TOML goal files rendered into `docs/scorecard.md` and checked for
freshness in CI (E04-050); **panic_hunt** = an integration test that fuzzes every registered command
with adversarial params (E04-012); **FLOOR** = a never-lowered minimum for a parity/corpus metric (E01-015);
**gate** = `cargo xtask ci`, the single local+CI check command (E05-010).

---

## 0. What PhotoCraft's evidence does and does not support

**Scale, for calibration (VERIFIED).** 12,396 commits on main, 3,475 first-parent, 8,329 non-merge
(E07 §0); 4,005 of 8,329 non-merge commits (48.1%) carry a Claude/Codex trailer or `Claude-Session:`
(E07 §0); 27 tags in 42 days (E05 §0.4); landed PRs median lifetime 10.1 h, rising to 68.3 h in
November (E06-013); up to 504 PRs in flight per day (E06-051).

**Strengths worth copying (evidence is strong).**
1. *Checkable architecture from day 1*: headless engine, one command registry reached by UI/CLI/control
   channel/MCP, CI-enforced layer linter (E04-008, E04-010, E04-031). This is what made agent work
   verifiable at all.
2. *One gate command*, identical locally and in CI, cheap steps first (E05-010).
3. *Advisory rules turned into mechanical checks* once they mattered: panic_hunt, panel-commands,
   GPU fail-on-skip, `scorecard --check` (E05-071, E05-024, E04-032).
4. *Ratchets*: FLOORs never lowered, shrink-only allowlists, "settings that do nothing" 66/129 → 8/199
   (E07-014, E05-072).
5. *Parallel-agent etiquette written from the first commit*: per-agent `CARGO_TARGET_DIR`, file
   ownership, new module per area, atomic manifest writes, "wait and retry, don't fix their files" (E06-050).
6. *Flake handling by root cause with measured before/after rates* (E07-007).
7. *Integration batches* coincided with zero red-main fix commits in W43–W45 (E07-005).

**Hollow spots to fix (evidence of weakness or failure).**
1. *No merge queue*: semantic merge skew between individually green PRs caused 11 of 21 catalogued
   red-main incidents; a manual "(merge queue)" practice appeared only on 11-08 (E07-003).
2. *Human review is mostly absent or label-only* on sampled PRs; approval seen once in a sample of 10
   (E06-041, E05-035). Accountability is a written rule, not a mechanism (E05-030).
3. *Vacuous tests*: 57 GPU checks passed without comparing anything (E07-018); fixes merged without
   regression tests needed a backfill campaign (E07-015).
4. *Surface before behaviour*: "625/625 menu items live" while basics were broken (E07-013, E07-017).
5. *Session memory is private*: `log/devlog.md` and `plan/` are gitignored (E02-004, E01-005).
6. *Many rules are stated-only*: check-then-claim, review-the-diff, report-only-what-ran, licence
   allowlist, no-agent-attribution (E02 §4). Practice diverges exactly there (E02-016).
7. *Gates that look real but cannot fail*: 0 of 88 perf budgets enforced (E04-051), stale fuzz matrix
   (E05-023), path filters on non-existent files (E05-033).
8. *Shared tracker docs as conflict hot spots*, including committed conflict markers (E07-020).

**Unknowns (do not fill them in from this playbook).**
- *Orchestration tooling*: no subagent/orchestrator config on main (E02 §6 "Subagents" row). How many
  agents ran at once is self-reported ("8 parallel agents", E01-014) or inferred from session trailers
  (max 15 distinct sessions per day, E06-011).
- *Token and money cost*: PhotoCraft publishes none. Effort is stated in "Opus 5.5 agent-hours",
  self-reported, and was revised ~10× upward in 8 days (E08-002, E08-005, E02-008).
- *Supervision time*: no data on human hours per merged change.
- *Branch protection / required reviews*: not visible from git (E05 open questions).
- *How the 42k-line "one-shot" commit was produced* (E01 open questions).
- *Whether AI-unattributed commits used AI*: unknown, not "human" (E03 open questions).

Consequence for this playbook: the *structure* (architecture, gates, ratchets, parallel rules) is
evidence-backed; the *roles, approval tiers, budgets and metrics* are mostly `[PROPOSED]`, designed
against PhotoCraft's observed failures.

---

## 1. Preconditions: architecture that makes agent work checkable

Finding: PhotoCraft's agent throughput rests on an architecture where every feature is an enumerable,
headless, JSON-addressable command; agents could then be checked by fuzzers, layer linters and
oracles instead of by human reading (E04-008, E04-010, E04-012).

| # | Precondition | Tag | How to do it (operational) |
|---|---|---|---|
| 1.1 | **Headless core crate** with no UI/windowing/GPU-surface deps; tests construct the session directly | `[PC-VERIFIED E04 §0.1 item 2]` | `crates/core` depends on nothing UI; add it to the layer table (1.3) so a UI import fails CI. |
| 1.2 | **One command registry**, JSON params in / JSON result out, each command a `CommandSpec` with id, schema, handler | `[PC-VERIFIED E04-010]` (`crates/engine/src/cmd.rs:15`, ~76 ids day 1 → ~805) | Every front-end (GUI, CLI, RPC, MCP) dispatches by id. No business logic in click handlers. |
| 1.3 | **Layer rules enforced in CI** (crate may depend only on lower layers; new crates must be registered) | `[PC-VERIFIED E04-031]` (`cargo xtask layers`, CI since day 1) | `xtask layers` reads `cargo metadata`, fails on upward edges. Register-or-fail for new crates. |
| 1.4 | **UI must dispatch commands** — lexical scan with a shrink-only allowlist | `[PC-VERIFIED E04-032]` (`xtask panel-commands`, 4165c57f92) | Scan UI source for click handlers not calling `dispatch(id, …)`; allowlist file may only shrink. |
| 1.5 | **Control channel for self-inspection**: authenticated local socket with `ui.screenshot`, `ui.pointer`, plus an offscreen render example replaying scripts | `[PC-VERIFIED E04-020, E04-024]` | Agent guide says "verify visually and look at the PNG". For an IDE: `ui.screenshot`, `editor.state`, `ui.focus`. |
| 1.6 | **Reuse the control interface as the UI-test driver** | `[PC-VERIFIED E04-023]` (32 files in `crates/ui-egui/tests`) | Test harness calls the same `control::handle` the agent uses. |
| 1.7 | **Fuzz every command** from the registry in one test | `[PC-VERIFIED E04-012]` (panic_hunt, in gate) | Iterate registry; send adversarial params; assert no panic, no hang (with a deadline). |
| 1.8 | **Oracles and pinned corpora** (reference outputs, sha256-pinned files, CPU-reference vs GPU tolerance) | `[PC-VERIFIED E04-036, E04-037]` (1,044 hashed corpus files, 78 parity tests) | For an IDE: pinned source corpora with expected parse trees, LSP transcripts, formatter outputs. |
| 1.9 | **Ratcheting floors** on corpus/parity metrics | `[PC-VERIFIED E01-015, E04-042]` | `FLOOR` constant in a test; CI fails if the metric drops below; raising is encouraged, lowering forbidden. |
| 1.10 | **Machine-readable goals** (TOML → generated doc, `--check` in CI) | `[PC-VERIFIED E04-050]` | `goals/*.toml` → `docs/scorecard.md`; gate fails if regenerated file differs. |
| 1.11 | **Behaviour metrics next to wiring metrics** | `[PC-PARTIAL E07-013]` — wiring metric (625/625 "live") over-claimed; behaviour metric added after user reports | `[PROPOSED]` for each wiring count, track a behaviour count (commands with ≥1 end-to-end test asserting an effect). Answers E07-013, E07-017. |
| 1.12 | **Compile-time completeness** (destructure structs in serializers so a new field breaks the build) | `[PC-VERIFIED E04-033]` (`AGENTS.md:191-194`) | Use `let Foo { a, b, c } = foo;` in every serializer. |
| 1.13 | **Never-crash baseline from day 1**: `unsafe_code = "forbid"`, clippy deny `unwrap/expect/panic` outside tests, last-resort `catch_unwind` around dispatch | `[PC-PARTIAL E07-009]` — added on day 5 after user crash reports, as a 12-PR sweep | `[PROPOSED]` put it in the first commit instead. Answers E07-009 (F6). |
| 1.14 | **Perf budgets that can fail** | `[PC-PARTIAL E04-051]` — 88 scenarios, 0 enforced; baseline machine class may never match CI (E05-028) | `[PROPOSED]` enforce on a fixed runner class; unenforced budgets stay visible with `enforce = false` and a measured note (as E09-F-004). |
| 1.15 | **Golden images / bless command** | `[PC-PARTIAL E04-035]` — planned, never built | `[PROPOSED]` build `xtask bless` with review-required diffs if visual output matters. |

Day-0 test: an agent with no GUI must be able to (a) list all commands, (b) run any one headless with
JSON, (c) see a screenshot of the GUI state it produced, (d) run the gate. If any of these is missing,
fix it before scaling agents.

---

## 2. Agent roles and responsibilities

Finding: PhotoCraft documents no role split; roles are observable only from behaviour — founder,
integrators who ran agents over batches, maintainers who label/merge, contributors who run their own
agents, and a third-party triage bot (E06 §1.1, E06-033). One integration PR states "two independent
agents per PR (a reviewer and an attacker)" (E06-022, PR #9386). The table below is therefore
`[PROPOSED]` except where tagged.

| Role | Inputs | Outputs / hand-off artifact | Tools & permissions (least privilege) | Must never | Evidence |
|---|---|---|---|---|---|
| **Planner / spec author** | issue, goal TOML, ADRs, code map | `task-spec.md` (acceptance criteria, files owned, risk tier, test plan sketch) | read repo; write `specs/`, issues; no build cache needed | write production code; mark own spec approved for tier ≥ medium | `[PC-PARTIAL E06-034]` epics with "free / being worked on / merged" and "Main files" tables; committed migration plan with open gates (E09-E-001) |
| **Implementer** | approved spec, owned-file list | branch + PR with code, tests it wrote, gate output, "not run" list | own worktree, own `CARGO_TARGET_DIR`, write owned files, run gate; push to own branch only | push to main; edit CI; add deps (tier high); edit files it doesn't own beyond surgical registry lines; claim tests passed that didn't run | `[PC-VERIFIED E06-050]` ownership/target-dir rules; `[PC-VERIFIED E02 §2.1 rule 7]` "Report only what ran" (stated only) |
| **Independent test author** | spec only (not the implementation diff, at first) | `test-plan.md` + tests that fail on main, pass on the branch | own worktree; write `tests/` only | read implementer's chat/session; weaken assertions to go green | `[PROPOSED]` answers vacuous tests E07-018 and missing tests E07-015 |
| **Verifier / reviewer** | PR diff, spec, test-plan, gate log | review against `review-checklist.md`; verdict + findings; mutation spot-check result | read-only on branch; may run gate and mutation tool | approve its own session's work; approve tier high alone | `[PC-PARTIAL E06-022]` reviewer+attacker agents in batch-8; CodeRabbit advisory (E06-040, E05-035) |
| **Integrator** | set of approved PRs | integration branch, conflict-resolution notes per file, green gate on the union, merge | write integration branch; regenerate generated files; no feature edits beyond conflict fixes | squash member PRs into one commit (loses provenance); resolve conflicts silently | `[PC-VERIFIED E06-022]` batches 7–20, file-by-file conflict notes (38609e5615); `[PC-VERIFIED E06-032]` central regeneration |
| **Release agent** | green main sha, changelog inputs | release PR on `release` branch, notes, dry-run result | release branch only; no signing secrets (human-held environment) | publish, tag or sign without human approval | `[PC-PARTIAL E05 §0.4, E02 §4]` release environment usable only from `release`; drafts published by a maintainer; one release commit authored by the Claude identity (E06-005) |
| **Triage agent** | new issues, PR list | labels, duplicate links, "in progress" links, split proposals | issue/label write; no code write | close issues automatically; assign priority `critical` without human confirm | `[PC-VERIFIED E06-033]` ticket-craft app (external, LLM use unknown) |
| **Human owner** | everything above | approvals per tier (§9), decisions (ADRs), accountability for each agent run | merge rights, secrets, release environment | delegate high-tier approval to an agent; merge on "No reviews" for tier ≥ medium | `[PC-PARTIAL E06-041]` house rule 1 "A person is accountable" (AGENTS.md:6), but approvals rarely visible |

Separation rules `[PROPOSED]` (answer E07-018, E07-015, E06-041):
- The test author and reviewer must be **different sessions** from the implementer; record session ids
  in trailers so this is checkable (§13 provenance).
- No role approves work produced in its own session.
- Each role's prompt lives in `09-templates/prompt-<role>.md`.

---

## 3. Task lifecycle state machine

Finding: PhotoCraft's observed flow is issue → branch → PR → (bot review) → human label/merge or
integration batch → main → release (E06 §0). Spec and independent-verify states are not observed as
distinct steps; they are `[PROPOSED]`.

```
intake → spec → claim → implement → self-verify → independent-verify → review → integrate → release → follow-up
   ↑                                      │ fail            │ fail           │ fail        │ red main
   └──────────────── triage ◄─────────────┴─────────────────┴────────────────┴─────────────┘
```

| State | Entry criteria | Work | Exit criteria | Human approval? | Tag |
|---|---|---|---|---|---|
| intake | issue exists | triage agent labels, links duplicates, sets tier guess | labelled; not a duplicate | no | `[PC-VERIFIED E06-033]` |
| spec | triaged | planner writes `task-spec.md` | acceptance criteria testable; owned files listed; tier set | tier high: owner approves spec | `[PROPOSED]` (answers E07-013 surface-only work) |
| claim | approved spec, nobody else claimed | comment "claimed by <session>" on issue; label `in progress`; search open PRs for `#N` | claim visible; no open PR for same issue | no | `[PC-PARTIAL E02 §2.1 rule 2]` stated only, added 11-06; duplicates persisted (E07-019) |
| implement | claim held | edit → build → test loop (§7) | gate green locally | no | `[PC-VERIFIED E05-010]` gate |
| self-verify | gate green | implementer runs mutation on its new tests; fills "ran / not run" | PR opened as draft with evidence | no | `[PC-PARTIAL E07-018]` mutation used ad hoc ("Verified by mutation", 602344bae0) |
| independent-verify | draft PR | test author adds/validates tests from spec; fail-on-main proof | tests fail on base, pass on head | no | `[PROPOSED]` (answers E07-015, E07-018) |
| review | independent tests in | reviewer agent + bot; tier medium+: human | checklist complete; no blocking findings | tier medium: owner or maintainer; tier high: owner | `[PC-PARTIAL E06-041]` |
| integrate | approved | merge queue / integration batch re-runs gate on union | main green after merge | integrator; human for batch merge | `[PC-PARTIAL E07-003]` manual queue only |
| release | release window | release agent prepares; dry run | human publishes | always human | `[PC-PARTIAL E02 §4]` |
| follow-up | merged | close issue, update goal TOML, open follow-ups, handoff note | issue closed; tracker regenerated | no | `[PC-PARTIAL E06-032]` tracker co-updates in <14% of code commits |

Timeouts `[PROPOSED]`: a claim with no push for 24 h is released by triage; a PR without response
for 7 days gets a reminder, eligible for closure at 30 (`[PC-VERIFIED E02 §2.1 rule 14]` states this
clock; enforcement unknown).

---

## 4. Orchestration and parallelism

Finding: PhotoCraft scaled to hundreds of PRs in flight per day (peak 504 on 10-13, E06-051) using
structural isolation rules rather than an orchestrator; conflicts then concentrated in shared files,
generated docs and catalogs (E06-051, E07-019, E07-020). Orchestration tooling itself is unknown.

**4.1 How many agents** `[PROPOSED]`. Start with 2–3 implementers plus one reviewer per human owner;
add implementers only when the red-main minutes per week (§13) stays at zero for two weeks and review
lag stays under one day. PhotoCraft gives no reproducible number: "8 parallel agents" is self-reported
(E01-014); 10–15 distinct session ids per day is a lower bound from partial trailers (E06-011).

**4.2 Partitioning.**
- File/module ownership per agent; listed in the spec. `[PC-VERIFIED E06-050]` (`AGENTS.md:172`).
- New feature → new module (`<area>_cmds.rs` with `specs()`), never grow a shared file.
  `[PC-VERIFIED E06-050]` (`AGENTS.md:173`).
- Large mechanical campaigns split per crate, one PR per crate. `[PC-VERIFIED E06-027, E09-C-004]`
  (12 never-crash PRs merged in ~15 min).

**4.3 Shared-file protocol** (registries, `Cargo.toml`, `Cargo.lock`, i18n catalogs, credits, tracker docs).

| Shared file kind | Rule | Tag |
|---|---|---|
| Registries (command list, layer table) | Append-only one-line edits; re-read before editing; registration via per-module `specs()` so the central file rarely changes | `[PC-VERIFIED E06-050]` |
| Manifests | Write atomically: temp file outside the workspace, then `mv` | `[PC-VERIFIED E06-050]` (`AGENTS.md:175`) |
| Lockfile | Only the dependency-change task (tier high) edits it; gate fails if `Cargo.lock` changes during the gate | `[PC-VERIFIED E05 §0.2]` (`git diff --exit-code -- Cargo.lock`, via WebFetch) |
| i18n catalogs / credits TOML | Consistency test rejects duplicate keys; regenerate centrally | `[PC-PARTIAL E07-019]` consistency test exists; duplicates still broke main (25f211500b, 29e4039c72) |
| Generated docs (scorecard) | Never hand-edit; regenerate in the integrator step only; feature PRs edit the TOML source | `[PC-PARTIAL E06-032, E07 F9]` regeneration at batch gate, but PRs also regenerated → staleness reds (3c44319455) |
| Status lines / revision histories | Do not require every PR to edit one shared line | `[PROPOSED]` answers E07-020 (conflict markers committed, 8601a7b170) |

**4.4 Claim protocol** `[PROPOSED]`, mechanising house rule 2 (stated only, E02 §4):
1. `gh pr list --search "#N in:body,title"`; if any open PR, stop and comment instead.
2. Comment on the issue `claim: <role> <session-id> <branch>`; add label `in progress`.
3. A bot (or CI job on PR open) fails a PR whose issue already has another open PR linked.
4. Release the claim with a comment if abandoning. Answers E07-019 (F2).

**4.5 Conflict handling.** In one checkout, "If someone else's in-progress edit breaks the build, wait
and retry; don't fix their files" `[PC-VERIFIED E06-050]`. With worktrees (§6) this case disappears;
conflicts move to integration, where the integrator records each resolution file by file in the merge
message `[PC-VERIFIED E06-022]` (38609e5615).

**4.6 When to batch.** Batch when ≥5 approved PRs touch overlapping areas or when the merge rate exceeds
what serial CI can verify. `[PC-VERIFIED E06-021, E06-022]` (CI-only batches 10-08; merged batches 7–20,
10–48 PRs each). `[PC-PARTIAL E07-002]` failing members were reverted inside the batch without a stated
reason; `[PROPOSED]` require a one-line reason per backed-out member.

---

## 5. Interface contracts

Finding: PhotoCraft's contracts that let agents work in parallel are the command registry (ids +
JSON schemas), the layer table, and compile-time completeness checks; there is no documented public-API
freeze or contract-test suite beyond panic_hunt and MCP `agent_tasks` tests (E04-010, E04-026, E04-033).

| Contract | What it fixes | How agents use it in parallel | Tag |
|---|---|---|---|
| Command schema (`CommandSpec`: id, params schema, result shape) | the boundary between core and every front-end | UI agent and core agent agree on the id + JSON before either writes code; UI work proceeds against a stub handler | `[PC-VERIFIED E04-010]` |
| Layer table (`xtask/src/layers.rs`) | allowed dependency edges | an agent cannot "just import" a higher crate; CI rejects it | `[PC-VERIFIED E04-031]` |
| Control protocol doc (`docs/control-protocol.md`, 50 → 840 lines) | external automation surface | agents verify via the same protocol users script against | `[PC-VERIFIED E04 §0.1 item 4]` |
| Completeness by destructuring | serializer covers all fields | adding a field forces format work in the same PR | `[PC-VERIFIED E04-033]` |
| Contract tests per command (schema round-trip, error on bad params, no panic) | behaviour of each id | generated from the registry; new ids are covered automatically | `[PC-PARTIAL E04-012]` panic_hunt covers no-panic only; `[PROPOSED]` add schema round-trip + "has ≥1 effect test" check |
| Public API freeze points | which signatures/ids may change | `[PROPOSED]` mark ids `stable` in the registry; changing a stable id/schema is tier high and needs an ADR | `[PROPOSED]` answers E07-003 row 15 (new struct field + concurrent PR → E0063 compile break) |

Operational rule `[PROPOSED]`: a task that changes a contract (schema, layer, stable id, shared struct)
is split: (1) contract PR, tier high, merged alone; (2) consumer PRs after it lands. This removes the
"two green PRs, one added a field, union does not compile" class (E07-003 rows 15, 19).

---

## 6. Branch / worktree strategy

Finding: PhotoCraft's parallel rules assume several agents in **one working tree** sharing a target
directory and builds broken by others' edits (E06-050); git worktrees are not mentioned (E02 §6). Main
had no merge queue; the semantic-skew class dominated red main (E07-003).

| Practice | Tag | Detail |
|---|---|---|
| One **git worktree** per agent | `[PROPOSED]` answers the "someone else's edit broke my build" case E06-050 | `git worktree add ../wt/<agent> -b <branch> origin/main` |
| One **build target dir** per agent | `[PC-VERIFIED E06-050]` | `CARGO_TARGET_DIR=target/agent-<name>`; ~10 GB each; delete when finished (`AGENTS.md:176`) |
| Branch naming `<kind>/<issue>-<slug>` | `[PC-VERIFIED E06-031]` (`fix/<issue>-…`, `claude/fix-<issue>-…`) | kinds: `feat fix test docs chore contract release integ`. Do not encode tool name as attribution (E06-025: `codex/*` contradicted trailers) |
| Short-lived branches (target < 1 day) | `[PC-PARTIAL E06-013]` median 2.8 h early, 68.3 h in November | `[PROPOSED]` claim timeout 24 h (§3) |
| Rebase policy | `[PROPOSED]` | rebase own branch on main before review; never rebase a branch others built on; integrator merges (does not squash) batch members to keep provenance (`[PC-VERIFIED E06-022]` batch PRs required merge commits) |
| `main` only via PR | `[PC-PARTIAL E02 §2.1 rule 8]` | stated "Branch protection enforces this" from 11-06; direct pushes before that (E06-026). `[PROPOSED]` enable protection on day 0 |
| Main CI never cancelled | `[PC-VERIFIED E07-004]` (01a63dee89) | `concurrency: group: ${{ github.event_name == 'push' && github.run_id || github.ref }}`; 80 of 83 main runs had been cancelled |
| **Real merge queue** (`merge_group` trigger; gate runs on main+PR before landing) | `[PC-PARTIAL E07-003]` only a manual "(merge queue)" re-merge from 11-08 (fda05f7b02); no `merge_group` in CI | `[PROPOSED]` enable GitHub merge queue from day 0; gate job listens to `merge_group`. Answers E07-003, E07-005, E05-052 |
| Integration branch for batches | `[PC-VERIFIED E06-021, E06-022]` | `integ/<date>-<n>`; integrator only; CI-only draft PR first; land with merge commit |
| Release branch | `[PC-VERIFIED E05 §0.4]` first tag off `release` 11-04 | `release` receives merges of tested main; release environment and secrets bound to it |
| Platform coverage on PR vs main | `[PC-PARTIAL E07-004, E07 F8]` PRs Linux-only unless path/label; Windows breaks surfaced on main | `[PROPOSED]` run the full platform matrix in the merge queue, not on every PR push |

---

## 7. Autonomous implementation loop

Finding: PhotoCraft's definition of done is a list of gate commands, most conditional on what was
touched, plus a hand-off rule "Keep the tree building at every step" (E02 §2.3, `AGENTS.md:145-168`).
Iteration limits and stop conditions are not documented; those are `[PROPOSED]`.

**7.1 Loop**

```
read spec + owned files → write failing test → edit → cargo check (fast) → focused tests
  → inspect (control-channel screenshot / CLI JSON) → debug → repeat
  → full local gate → self-verify (mutation spot-check) → draft PR with evidence
```

- Write the failing test first; record that it failed. `[PC-VERIFIED E02 §2.1 rule 4]` (stated:
  "Add a test that fails without the fix"; followed unevenly, E07-015).
- Inspect the real behaviour, not only test output: offscreen snapshot or `ui.screenshot`.
  `[PC-VERIFIED E04-024]`.
- "Verify, don't guess. Open a definition before using it." `[PC-VERIFIED E02 §2.1 rule 3]` (stated).

**7.2 Local gate command list** (adapt names; PhotoCraft's equivalents in brackets, `[PC-VERIFIED E05 §0.2]`)

| Order | Command | Blocking |
|---|---|---|
| 1 | `cargo fmt --all -- --check` | yes |
| 2 | `cargo clippy --workspace --locked --all-targets -- -D warnings` | yes |
| 3 | `cargo xtask layers` | yes |
| 4 | `cargo xtask ui-dispatch` [panel-commands] | yes |
| 5 | `cargo xtask goals --check` [scorecard --check] | yes |
| 6 | `cargo nextest run --profile ci --workspace --locked` | yes |
| 7 | `cargo nextest run --run-ignored only -E 'binary_id(core::command_fuzz)'` [panic_hunt] | yes |
| 8 | `cargo test --workspace --doc --locked` | yes |
| 9 | `cargo xtask no-skips` [lavapipe fail-on-skip] | yes |
| 10 | `git diff --exit-code -- Cargo.lock` | yes |

All wrapped as `cargo xtask ci`, the same command CI runs. `[PC-VERIFIED E05-010]`. Never ship a
"never fails" step (PhotoCraft's `i18n-report` never fails, E05 §0.2) unless it is labelled report-only.

**7.3 Stop conditions** `[PROPOSED]`

| Condition | Action |
|---|---|
| Gate green, evidence written | stop; open draft PR |
| Same failing test after 3 edit cycles with no new information | stop; write blocker in handoff; ask reviewer/owner |
| 8 total edit→test cycles on one task (tier low/medium) / 12 (high) | stop; escalate with diagnosis |
| Need to edit a file outside the owned list (beyond surgical registry line) | stop; ask planner to amend spec |
| Any stop-and-ask item (§9.3) | stop immediately |
| Build broken by code you don't own | worktrees: rebase; shared tree: "wait and retry, don't fix their files" `[PC-VERIFIED E06-050]` |
| Context > ~70% used | write handoff (§11) and end session `[PROPOSED]`, answers context-limit ends noted in `AGENTS.md:168` |

Anti-stall rule: when an optional input is absent, proceed. `[PC-VERIFIED E02 §2.3]` ("`plan/` … Do not
ask for it and do not stop when it is absent").

---

## 8. Independent testing

Finding: PhotoCraft's test volume is high (77.5% of non-merge commits touch tests, E03-011; ~18,030 test
attributes, E04 §0.1) but quality failures were vacuous tests and fixes without regression tests, caught
late by CodeRabbit, mutation and environment audits (E07-018, E07-015). Same-agent testing is the norm;
no independent test-author role is documented.

| Practice | Tag | Operational rule |
|---|---|---|
| Tests by a different session than the implementer | `[PROPOSED]` answers E07-018, E07-015 | test author gets spec, not implementer chat; session ids in trailers prove separation |
| "Test fails without the fix" proof | `[PC-PARTIAL E02 §2.1 rule 4–5, E07-015]` stated; backfill needed for 8 fixes; 16 of 27 security fixes added no `#[test]` (E09 G-003) | `[PROPOSED]` CI job: check out base, apply only the PR's test files, expect failure; record in PR |
| Crash fixes carry a test that panicked before | `[PC-VERIFIED E07-009]` (`AGENTS.md:113`, stated) | same base-revert job enforces it |
| Fail on skip | `[PC-VERIFIED E05-024, E07-018]` 2ff8f419cb after 57 GPU checks passed by returning early | tests print a skip marker; CI fails if any appears in required jobs; zero-match test filters are BLOCKED, not green (E05-022, E05-051) |
| Mutation spot-checks | `[PC-PARTIAL E07-018]` ad hoc ("Verified by mutation", 24 commits mention mutation) | `[PROPOSED]` `cargo mutants --in-diff` on changed files for tier medium+; surviving mutants listed in review |
| Ratcheting corpus floors | `[PC-VERIFIED E01-015, E09-D-001..003]` | FLOOR raised when metric rises; never lowered |
| Fuzz every command | `[PC-VERIFIED E04-012]` panic_hunt in gate | plus `[PC-PARTIAL E05-023]` cargo-fuzz targets exist (21) but dispatch-only and stale; `[PROPOSED]` nightly fuzz with matrix generated from targets |
| Flaky tests root-caused, measured | `[PC-VERIFIED E07-007, E05-053]` | commit records failure rate before/after (e.g. "failed 15 of 40 runs, the fixed one 0 of 40", 7091cb6b8c); retries were tried and dropped (E05-050) |
| Harness diversity | `[PC-VERIFIED E07-008]` (accidental: FreeBSD `cargo test` exposed a race nextest hid) | `[PROPOSED]` run one nightly job with plain `cargo test` |
| Environment-diverse fault injection on persistence | `[PC-PARTIAL E07-021]` SMB regression after a durability fix; fixed by error injection later | `[PROPOSED]` fault-injection matrix (network FS, read-only, fsync failure, permission denied) for save-path changes |
| Periodic backfill sweep | `[PC-VERIFIED E07-015]` (72e11802d4) | `[PROPOSED]` monthly: list fix commits with no test change (§13 query), backfill |

**Anti-vacuous-test rules** `[PROPOSED]` (each answers E07-018 examples):
1. Every test has at least one assertion on an observable effect (not only `is_ok()`).
2. No early `return` in a test body without the skip marker.
3. A test that never reaches the code under test fails coverage-on-diff (changed lines executed ≥ 1).
4. Reviewer deletes or inverts the fix locally; at least one new test must fail.
5. Bot findings like "passed even if nothing was painted" (c441fd350c) become a lint or a checklist line.

