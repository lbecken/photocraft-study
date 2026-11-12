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

For a *documented rule* (AGENTS.md text), `PC-VERIFIED` means the rule text is verified at the pin and is
marked "(stated)"; it says nothing about compliance. Where compliance is known to be uneven, the tag is `PC-PARTIAL`.

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
   GPU fail-on-skip, `scorecard --check` (E05-071, E05-024, E04-012).
4. *Ratchets*: FLOORs never lowered, shrink-only allowlists, "settings that do nothing" 66/129 → 8/199
   (E07-014, E05-072).
5. *Parallel-agent etiquette written from the first commit*: per-agent `CARGO_TARGET_DIR`, file
   ownership, new module per area, atomic manifest writes, "wait and retry, don't fix their files" (E06-050).
6. *Flake handling by root cause with measured before/after rates* (E07-007).
7. *Integration batches* coincided with zero red-main fix commits in W43–W45 (E07-005).

**Hollow spots to fix (evidence of weakness or failure).**
1. *No merge queue*: semantic merge skew between individually green PRs caused 11 of 21 catalogued
   red-main incidents (INFERRED classification); a manual "(merge queue)" practice appeared only on 11-08 (E07-003).
2. *Human review is mostly absent or label-only* on sampled PRs; approval seen once in E06's sample of 10
   and once in E05's sample of 6; about 4 in all ~22 sampled PR pages (E06-041, E05-035, errata #17). Accountability is a written rule, not a mechanism (E05-030).
3. *Vacuous tests*: 57 GPU checks passed without comparing anything (E07-018); fixes merged without
   regression tests needed a backfill campaign (E07-015).
4. *Surface before behaviour*: "625/625 menu items live" while basics were broken (E07-013, E07-017).
5. *Session memory is private*: `log/devlog.md` and `plan/` are gitignored (E02-004, E01-005).
6. *Many rules are stated-only*: check-then-claim, review-the-diff, report-only-what-ran, licence
   allowlist, no-agent-attribution (E02 §4). Practice diverges exactly there (E02 §4).
7. *Gates that look real but cannot fail*: 0 of 102 perf-budget rows (88 scenarios + 14 benches) enforced (E04-051, errata #11), stale fuzz matrix
   (E05-023), path filters on non-existent files (E05-033).
8. *Shared tracker docs as conflict hot spots*, including committed conflict markers (E07-020).

**Unknowns (do not fill them in from this playbook).**
- *Orchestration tooling*: no subagent/orchestrator config on main (E02 §6 "Subagents" row). How many
  agents ran at once is self-reported ("8 parallel agents", E01-014) or inferred from session trailers
  (max 10 distinct sessions on one day on main, 15 across all refs, E06-011).
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
| 1.2 | **One command registry**, JSON params in / JSON result out, each command a `CommandSpec` with id, params description, handler | `[PC-VERIFIED E04-010, E04-011]` (`crates/engine/src/cmd.rs:15`, ~76 ids day 1 → ~805, regex estimate); params are a free-text "JSON-ish" doc string, not a validated schema (E04-003) | Every front-end (GUI, CLI, RPC, MCP) dispatches by id. No business logic in click handlers. `[PROPOSED]` make params a validated schema from day 1. |
| 1.3 | **Layer rules enforced in CI** (crate may depend only on lower layers; new crates must be registered) | `[PC-VERIFIED E04-031]` (`cargo xtask layers`, CI since day 1) | `xtask layers` reads `cargo metadata`, fails on upward edges. Register-or-fail for new crates. |
| 1.4 | **UI must dispatch commands** — lexical scan with a shrink-only allowlist | `[PC-VERIFIED E04-012]` (`xtask panel-commands`, 4165c57f92) | Scan UI source for click handlers not calling `dispatch(id, …)`; allowlist file may only shrink. |
| 1.5 | **Control channel for self-inspection**: authenticated (token/HMAC) JSON channel with `ui.screenshot`, `ui.pointer`, plus an offscreen render example replaying scripts | `[PC-VERIFIED E04-013, E04-020, E04-021]`; use by dev agents traced only in 3 commits + 1 PR (E04-024) | Agent guide says "verify visually and look at the PNG". For an IDE: `ui.screenshot`, `editor.state`, `ui.focus`. |
| 1.6 | **Reuse the control interface as the UI-test driver** | `[PC-VERIFIED E04-023]` (32 files in `crates/ui-egui/tests`) | Test harness calls the same `control::handle` the agent uses. |
| 1.7 | **Fuzz every command** from the registry in one test | `[PC-VERIFIED E04-012]` (panic_hunt, in gate) | Iterate registry; send adversarial params; assert no panic, no hang (with a deadline). |
| 1.8 | **Oracles and pinned corpora** (reference outputs, sha256-pinned files, CPU-reference vs GPU tolerance) | `[PC-VERIFIED E04-036, E04-037]` (1,044 hashed corpus files, 78 parity tests) | For an IDE: pinned source corpora with expected parse trees, LSP transcripts, formatter outputs. |
| 1.9 | **Ratcheting floors** on corpus/parity metrics | `[PC-VERIFIED E01-015, E04-042]` | `FLOOR` constant in a test; CI fails if the metric drops below; raising is encouraged, lowering forbidden. |
| 1.10 | **Machine-readable goals** (TOML → generated doc, `--check` in CI) | `[PC-VERIFIED E04-050]` | `goals/*.toml` → `docs/scorecard.md`; gate fails if regenerated file differs. |
| 1.11 | **Behaviour metrics next to wiring metrics** | `[PC-PARTIAL E07-013]` — wiring metric (625/625 "live") over-claimed; behaviour metric added after user reports | `[PROPOSED]` for each wiring count, track a behaviour count (commands with ≥1 end-to-end test asserting an effect). Answers E07-013, E07-017. |
| 1.12 | **Compile-time completeness** (destructure structs in serializers so a new field breaks the build) | `[PC-VERIFIED E04-033]` (`AGENTS.md:191-194`) | Use `let Foo { a, b, c } = foo;` in every serializer. |
| 1.13 | **Never-crash baseline from day 1**: `unsafe_code = "forbid"`, clippy deny `unwrap/expect/panic` outside tests, last-resort `catch_unwind` around dispatch | `[PC-PARTIAL E07-009]` — added on day 5, after user crash reports (trigger INFERRED), as a 12-PR sweep | `[PROPOSED]` put it in the first commit instead. Answers E07-009 (F6). |
| 1.14 | **Perf budgets that can fail** | `[PC-PARTIAL E04-051]` — 102 rows (88 scenarios + 14 benches), 0 enforced (errata #11); baseline machine class may never match CI (E05-028) | `[PROPOSED]` enforce on a fixed runner class; unenforced budgets stay visible with `enforce = false` and a measured note (as E09-F-004). |
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
| **Implementer** | approved spec, owned-file list | branch + PR with code, tests it wrote, gate output, "not run" list | own worktree, own `CARGO_TARGET_DIR`, write owned files, run gate; push to own branch only | push to main; edit CI; add deps (tier high); edit files it doesn't own beyond surgical registry lines; claim tests passed that didn't run | `[PC-VERIFIED E06-050]` ownership/target-dir rules; `[PC-VERIFIED E02 §2.1 rule 7]` "Report only what ran" (stated; no check, E02 §4) |
| **Independent test author** | spec only (not the implementation diff, at first) | `test-plan.md` + tests that fail on main, pass on the branch | own worktree; write `tests/` only | read implementer's chat/session; weaken assertions to go green | `[PROPOSED]` answers vacuous tests E07-018 and missing tests E07-015 |
| **Verifier / reviewer** | PR diff, spec, test-plan, gate log | review against `review-checklist.md`; verdict + findings; mutation spot-check result | read-only on branch; may run gate and mutation tool | approve its own session's work; approve tier high alone | `[PC-PARTIAL E06-022]` reviewer+attacker agents in batch-8; CodeRabbit advisory (E06-040, E05-035) |
| **Integrator** | set of approved PRs | integration branch, conflict-resolution notes per file, green gate on the union, merge | write integration branch; regenerate generated files; no feature edits beyond conflict fixes | squash member PRs into one commit (loses provenance); resolve conflicts silently | `[PC-VERIFIED E06-022]` batches 7–20, file-by-file conflict notes (38609e5615); `[PC-PARTIAL E06-032]` regeneration at the batch gate, but PRs also regenerate |
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
| spec | triaged | planner writes `task-spec.md` | acceptance criteria testable; owned files listed; tier set | tier medium: maintainer approves spec; tier high: owner approves spec | `[PROPOSED]` (answers E07-013 surface-only work) |
| claim | approved spec, nobody else claimed | comment "claimed by <session>" on issue; label `in progress`; search open PRs for `#N` | claim visible; no open PR for same issue | no | `[PC-PARTIAL E02 §2.1 rule 2]` stated only, added 11-06; duplicates persisted (E07-019) |
| implement | claim held | edit → build → test loop (§7) | gate green locally | no | `[PC-VERIFIED E05-010]` gate |
| self-verify | gate green | implementer runs mutation on its new tests; fills "ran / not run" | PR opened as draft with evidence | no | `[PC-PARTIAL E07-018]` mutation used ad hoc ("Verified by mutation", 602344bae0) |
| independent-verify | draft PR; tier medium/high (tier low skips to review) | test author adds/validates tests from spec; fail-on-main proof | tests fail on base, pass on head | no | `[PROPOSED]` (answers E07-015, E07-018) |
| review | independent tests in | reviewer agent + bot; tier medium+: human | checklist complete; no blocking findings | tier medium: owner or maintainer; tier high: owner | `[PC-PARTIAL E06-041]` |
| integrate | approved | merge queue / integration batch re-runs gate on union | main green after merge | integrator; human for batch merge | `[PC-PARTIAL E07-003]` manual queue only |
| release | release window | release agent prepares; dry run | human publishes | always human | `[PC-PARTIAL E02 §4]` |
| follow-up | merged | close issue, update goal TOML, open follow-ups, handoff note | issue closed; tracker regenerated | no | `[PC-PARTIAL E06-032]` tracker co-updates in <14% of code commits |

Timeouts `[PROPOSED]`: a claim with no push for 24 h is released by triage (label removed, comment
posted). PR response clock: respond within 7 days, reminder at 14, closure eligible at 30, decided by a
maintainer, never automatic (`[PC-PARTIAL E02 §2.1 rule 14, E06-041]`: stated since 11-06; the
`waiting on author` label text says "Closed after 14 days", contradicting it; enforcement unknown).

---

## 4. Orchestration and parallelism

Finding: PhotoCraft scaled to hundreds of PRs in flight per day (peak 504 on 10-13, E06-051) using
structural isolation rules rather than an orchestrator; conflicts then concentrated in shared files,
generated docs and catalogs (E06-051, E07-019, E07-020). Orchestration tooling itself is unknown.

**4.1 How many agents** `[PROPOSED]`. Start with 2–3 implementers plus one reviewer per human owner;
add implementers only when the red-main minutes per week (§13) stays at zero for two weeks and review
lag stays under one day. PhotoCraft gives no reproducible number: "8 parallel agents" is self-reported
(E01-014); the busiest day shows 10 (main) / 15 (all refs) distinct session ids, median 3 / 5 per day,
a lower bound from partial trailers (E06-011).

**4.2 Partitioning.**
- File/module ownership per agent; listed in the spec. `[PC-VERIFIED E06-050]` (`AGENTS.md:172`).
- New feature → new module (`<area>_cmds.rs` with `specs()`), never grow a shared file.
  `[PC-VERIFIED E06-050]` (`AGENTS.md:173`).
- Large mechanical campaigns split per crate, one PR per crate. `[PC-VERIFIED E06-027, E07-009]`
  (12 never-crash PRs: #33 at 11:14, the other 11 within ~15 min, 13:25–13:40 on 10-04).

**4.3 Shared-file protocol** (registries, `Cargo.toml`, `Cargo.lock`, i18n catalogs, credits, tracker docs).

| Shared file kind | Rule | Tag |
|---|---|---|
| Registries (command list, layer table) | Append-only one-line edits; re-read before editing; registration via per-module `specs()` so the central file rarely changes | `[PC-VERIFIED E06-050]` |
| Manifests | Write atomically: temp file outside the workspace, then `mv` | `[PC-VERIFIED E06-050]` (`AGENTS.md:175`) |
| Lockfile | Only the dependency-change task (tier high) edits it; gate fails if `Cargo.lock` changes during the gate | `[PC-VERIFIED E05-010]` for the gate check (`git diff --exit-code -- Cargo.lock` in the shared gate, via WebFetch); ownership rule `[PROPOSED]` |
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
what serial CI can verify. `[PC-VERIFIED E06-021, E06-022]` (CI-only batches 10-08/09; merged batches 7–20,
7–48 distinct `Merge PR #N` messages each, 37–48 at the peak). `[PC-PARTIAL E07-002]` failing members were reverted inside the batch without a stated
reason; `[PROPOSED]` require a one-line reason per backed-out member.

**4.7 Dispatch loop** `[PROPOSED]` (PhotoCraft's orchestration tooling is unknown, E02 §6). The
orchestrator is a role held by the human owner or one planner session; it never implements.
1. Queue = issues with an approved `specs/<issue>.md`, ordered by goal-TOML priority; skip any with an
   open PR or a live claim (§4.4).
2. Assign only while running implementers < cap (§4.1) **and** no two in-flight specs list the same
   owned file; otherwise wait.
3. Each assignment = one fresh session with `prompt-implementer.md`, its own worktree and target dir.
4. On draft PR: start test-author (tier medium/high) and reviewer sessions; never reuse the
   implementer's session.
5. On a stop condition (§7.3) or handoff with blockers: route the question to planner/owner; the task
   returns to the queue only after the spec is amended.
6. Daily: read `STATE.md` and the newest handoffs, release stale claims, record §13 metrics.

---

## 5. Interface contracts

Finding: PhotoCraft's contracts that let agents work in parallel are the command registry (ids +
JSON params described in free text, E04-003), the layer table, and compile-time completeness checks; there is no documented public-API
freeze or contract-test suite beyond panic_hunt and MCP `agent_tasks` tests (E04-010, E04-026, E04-033).

| Contract | What it fixes | How agents use it in parallel | Tag |
|---|---|---|---|
| Command spec (`CommandSpec`: id, params, `run` returning JSON) | the boundary between core and every front-end | `[PROPOSED]` UI agent and core agent agree on the id + JSON before either writes code; UI work proceeds against a stub handler | `[PC-PARTIAL E04-010, E04-003]` id + JSON-in/JSON-out verified; params are a free-text "JSON-ish" description, not a validated schema, and there is no result schema |
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
| Main CI never cancelled | `[PC-VERIFIED E07-004, E05-004]` (07174271d5 / 01a63dee89) | PhotoCraft (`ci.yml:66-68`): group = `github.ref` for PR events, `github.run_id` otherwise, and `cancel-in-progress: ${{ github.event_name == 'pull_request' }}`; before the fix 80 of 83 main runs on 10-07 had been cancelled |
| **Real merge queue** (`merge_group` trigger; gate runs on main+PR before landing) | `[PC-PARTIAL E07-003]` only a manual "(merge queue)" re-merge from 11-08 (fda05f7b02); no `merge_group` in CI | `[PROPOSED]` enable GitHub merge queue from day 0; gate job listens to `merge_group`. Answers E07-003, E07-005, E05-052 |
| Integration branch for batches | `[PC-VERIFIED E06-021, E06-022]` | `integ/<date>-<n>`; integrator only; CI-only draft PR first; land with merge commit |
| Release branch | `[PC-VERIFIED E05 §0.4]` first tag off main 11-04 (v0.20.2; 11-05 UTC); tags on `release` from v0.22.0 (errata #30) | `release` receives merges of tested main; release environment and secrets bound to it |
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

- Write the failing test first; record that it failed. `[PC-PARTIAL E02 §2.1 rule 4, E07-015]` (stated:
  "Add a test that fails without the fix"; followed unevenly: 8 fixes needed a backfill).
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
| "Test fails without the fix" proof | `[PC-PARTIAL E02 §2.1 rule 4–5, E07-015]` stated; backfill needed for 8 fixes; 16 of 27 security fixes added no `#[test]` (E09-G-003) | `[PROPOSED]` CI job: check out base, apply only the PR's test files, expect failure; record in PR (sketch below) |
| Crash fixes carry a test that panicked before | `[PC-VERIFIED E07-009]` (`AGENTS.md:113`, stated; compliance not measured) | same base-revert job enforces it |
| Fail on skip | `[PC-VERIFIED E05-024, E07-018]` 2ff8f419cb after 57 GPU checks passed by returning early | tests print a skip marker; CI fails if any appears in required jobs; zero-match test filters are BLOCKED, not green (E05-022, E05-051) |
| Mutation spot-checks | `[PC-PARTIAL E07-018]` ad hoc ("Verified by mutation", 24 commits mention mutation) | `[PROPOSED]` `git diff $BASE...HEAD > pr.diff && cargo mutants --in-diff pr.diff` for tier medium+; surviving mutants listed in review |
| Ratcheting corpus floors | `[PC-VERIFIED E01-015, E09-D-001..003]` | FLOOR raised when metric rises; never lowered |
| Fuzz every command | `[PC-VERIFIED E04-012]` panic_hunt in gate | plus `[PC-PARTIAL E05-023]` cargo-fuzz targets exist (21) but dispatch-only and stale; `[PROPOSED]` nightly fuzz with matrix generated from targets |
| Flaky tests root-caused, measured | `[PC-VERIFIED E07-007, E05-053]` | commit records failure rate before/after (e.g. "failed 15 of 40 runs, the fixed one 0 of 40", 7091cb6b8c); retries were tried and dropped (E05-050) |
| Harness diversity | `[PC-VERIFIED E07-008]` (accidental: FreeBSD `cargo test` exposed a race nextest hid) | `[PROPOSED]` run one nightly job with plain `cargo test` |
| Environment-diverse fault injection on persistence | `[PC-PARTIAL E07-021]` SMB regression after a durability fix; fixed by error injection later | `[PROPOSED]` fault-injection matrix (network FS, read-only, fsync failure, permission denied) for save-path changes |
| Periodic backfill sweep | `[PC-PARTIAL E07-015]` one campaign (72e11802d4), not periodic | `[PROPOSED]` monthly: list fix commits with no test change (§13 query), backfill |

Base-revert job sketch `[PROPOSED]` (tier medium/high; a PR with no test-file changes fails it unless labelled `no-test: <reason>`):
```
git checkout $BASE && git checkout $HEAD -- $(git diff --name-only $BASE...$HEAD | grep -E '(^|/)tests?/|_tests?\.rs$')
cargo nextest run --workspace --no-fail-fast > base.log; test $? -ne 0   # at least one new test must fail on base
```
Inline `#[cfg(test)]` modules in non-test files need the reviewer's manual revert (rule 4 below) instead.
A base that fails only because the tests do not compile (new symbols) is not proof; the job log must show a
failing assertion, otherwise the reviewer's manual revert is required.

**Anti-vacuous-test rules** `[PROPOSED]` (each answers E07-018 examples):
1. Every test has at least one assertion on an observable effect (not only `is_ok()`).
2. No early `return` in a test body without the skip marker.
3. A test that never reaches the code under test fails coverage-on-diff (changed lines executed ≥ 1).
4. Reviewer deletes or inverts the fix locally; at least one new test must fail.
5. Bot findings like "passed even if nothing was painted" (c441fd350c) become a lint or a checklist line.

---

## 9. Approval thresholds

Finding: PhotoCraft's only documented approval rule is a closed stop-and-ask list (house rule 9,
`AGENTS.md:14`) plus "Don't add or change CI in a feature or fix PR" (`AGENTS.md:16, :212-214`);
who may merge and how many approvals are needed are **not documented** (E02 §6). Sampled PRs merged
with "No reviews" or label-only signals (E06-041, E05 §0.3). The tier table is `[PROPOSED]`.

**9.1 Risk tiers**

| Tier | Change kinds | Required evidence | Who approves | Merge path |
|---|---|---|---|---|
| **Low** | docs, comments, new tests only, i18n strings (non-structural) | gate green; for tests: they fail when target code is broken | reviewer agent | merge queue |
| **Medium** | feature or fix confined to one module/crate it owns; new command in a new module | gate green; independent tests fail-on-base; mutation spot-check; screenshot/JSON evidence for UI | reviewer agent **and** a human maintainer (label `ready to merge` is not enough without a review record) | merge queue or batch |
| **High** | shared contracts (command schema, stable ids, layer table, shared structs); persistence/save path; CI/workflows; dependencies/`Cargo.lock`; licensing/assets/fonts; security boundaries (control channel auth, plugin sandbox, parsers of untrusted input); release | all medium evidence + ADR + rollback plan + named human owner approval; fault-injection for persistence; licence check for deps | human owner (plus a second human for security/release) | merged alone, never inside a batch |

Mapping to evidence:
- CI changes high-tier: `[PC-PARTIAL E02 §2.1 rule 11, E02-014]` (stated; partly followed, E02 §4).
- Dependencies/licensing: `[PC-PARTIAL E02 §4]` allowlist stated, no `cargo-deny` check found.
  `[PROPOSED]` `cargo deny check licenses bans sources` in the gate.
- Persistence high-tier: `[PROPOSED]` answers E07-021 (save-path fix chain regressed SMB users;
  ≥5 PRs over 37 days, E07-026).
- Release: `[PC-PARTIAL E02 §4]` release environment bound to `release` branch, maintainer publishes.
- Contracts high-tier: `[PROPOSED]` answers E07-003 rows 15 and 19.

**9.2 Approval records.** An approval is a GitHub review (or signed comment) by a named person, not a
label. `[PROPOSED]` answers E06-041 (label applied and merged by the same maintainer; one approval in 10
sampled PRs). Required-review counts set in branch protection per path (CODEOWNERS for high-tier paths;
PhotoCraft has none, E02-020).

**9.3 Stop-and-ask list** (agent stops, writes the question, waits)
`[PC-VERIFIED E02-009, E02 §2.1 rule 9]` for the first eight items (documented since 11-06; releases partly
mechanical via the `release` environment, E02 §4; verbatim list: "licensing outside the
allowlist, publishing, releases, a new remote, secrets, spending money, destructive git, and anything
else hard to undo"); remaining items `[PROPOSED]`:
1. Licence outside the allowlist / new asset or font source.
2. Publishing anything (crates.io, store, website, social).
3. Releases, tags, signing.
4. Adding a git remote or pushing anywhere but own branch.
5. Secrets, tokens, personal data.
6. Spending money (paid APIs, runners, cloud).
7. Destructive git (force-push, history rewrite, branch delete on shared refs).
8. Anything hard to undo.
9. Lowering a FLOOR, adding to a shrink-only allowlist, disabling or skipping a test. `[PROPOSED]` answers E07-018.
10. Changing a stable command id/schema or the layer table. `[PROPOSED]` answers E07-003.
11. A save-path or data-format change. `[PROPOSED]` answers E07-021.
12. The task needs files outside the owned list. `[PROPOSED]` answers E07-019.

Everything else: keep working (anti-stall, §7.3).

---

## 10. Failure recovery

Finding: PhotoCraft repaired main by forward fixes, never by reverting on main's first-parent line
(0 of 23 reverts first-parent, E07-001); fix-main work was 59 commits (some cherry-pick duplicates), 40 with a
Claude/Anthropic or `Claude-Session` trailer, done by a few maintainers (E07-006). The prefer-mechanical column states what we recommend.

| Failure | Detection signal | Immediate action | Permanent fix (prefer mechanical) | Evidence |
|---|---|---|---|---|
| **Red main** | main push run fails (never cancelled) | owner of last merge (or on-call agent) opens `fix/main-<cause>` within 30 min; if not green in 60 min, revert the breaking merge `[PROPOSED]` | merge queue (§6); fail-fast gate order | `[PC-VERIFIED E07-004]`; TTF 3 min–13 h 12 min over the 17 incidents with a measured TTF, plus one latent ~6.9 d (E07 §2); `[PC-PARTIAL E07-001]` revert-on-main never used |
| **Semantic merge skew** | red main whose fix names two PRs | as red main | merge queue; contract-first split (§5) | `[PC-VERIFIED E07-003]` 11/21 incidents (INFERRED classification) |
| **Gate tightened mid-flight** | many PRs/main red on a new lint | land lint as warn, burn down, then deny via ratchet | ratchet: new denies only after count reaches 0 | `[PC-PARTIAL E07-005, E07-011]` `cognitive_complexity = deny` then reds on 11-11 |
| **Flaky test** | same test fails then passes on rerun; or nightly loop | quarantine with issue + owner, never silent retry | root-cause in code (own binary, lock, condition poll); record before/after rate | `[PC-VERIFIED E07-007]`; retries dropped (E05-050) |
| **Bad merge / conflict casualty** | conflict markers, dropped lines | fix PR | `[PROPOSED]` gate step `git grep -nE '^(<<<<<<<|>>>>>>>)'`; no shared status lines | `[PC-PARTIAL E07-020]` no mechanism found |
| **Regression from a fix** | issue reopened / duplicates referencing a fix PR | link to original PR; high-tier if persistence | environment-diverse tests for that area; follow-up count metric (§13) | `[PC-VERIFIED E07-021, E07-026]` |
| **Vacuous test discovered** | mutation survives; bot comment; skip marker | fix test; audit siblings | fail-on-skip; base-revert job | `[PC-VERIFIED E07-018]` |
| **Duplicate parallel work** | two PRs for one issue; duplicate keys | close the worse one ("look for a better PR") | claim check bot; consistency tests on catalogs | `[PC-PARTIAL E07-019]`, rule 6 stated |
| **Generated artefact stale** | `--check` fails after merge | regenerate in fix PR | only integrator/queue regenerates | `[PC-VERIFIED E07 F9]` (3c44319455) |
| **Agent stuck / looping** | > N cycles (§7.3), same diff reverted and reapplied, no commits in 2 h | stop session; handoff with diagnosis | spec quality review; smaller tasks | `[PROPOSED]` (no PhotoCraft data) |
| **Context exhaustion / abrupt end** | session ends without handoff | next session reads handoff + `git log`; tree must be green | handoff written at every green checkpoint | `[PC-VERIFIED E02-004]` ("Sessions can end abruptly … context limits") |
| **Conflicting parallel work in one tree** | build broken by unowned files | wait and retry | worktree per agent | `[PC-VERIFIED E06-050]` / `[PROPOSED]` worktrees |
| **Release-only breakage** | nightly release dry run fails | fix before release day | nightly dry run | `[PC-VERIFIED E05-062, E05-063]` (0.8.1 failed on wasm size) |
| **Shared threshold blocks unrelated PRs** | size/perf gate red on PRs that did not grow it | owner of the threshold fixes it | per-component budgets | `[PC-VERIFIED E07-027]` (24 MiB wasm gate) |

Rule-vs-check policy `[PROPOSED]`, derived from E02 §4 (rules with no check are the ones practice
diverges from; errata #5): every incident postmortem (template `incident-postmortem.md`) must end in a mechanical
check, a ratchet metric, or an explicit "rule only, because …" justification. PhotoCraft's own model:
"Guards say why" `[PC-VERIFIED E02 §2.1 rule 12]` (stated).

---

## 11. Session continuity

Finding: PhotoCraft's documented hand-off is "append a terse entry to `log/devlog.md` … the dev log
plus a green tree is how the next agent picks up" (`AGENTS.md:168`); both `log/` and `plan/` are
gitignored, so the main inter-session memory cannot be audited (E02-004, E01-005). Decisions are an
informal 2-entry dated log, not ADRs; a third entry seen on side branches is absent at HEAD (E02-025, E02 §5).

| Artifact | Location | Written when | Tag |
|---|---|---|---|
| Green tree | branch head | every checkpoint; never end red | `[PC-VERIFIED E02-004]` "Keep the tree building at every step" |
| Handoff note | `handoffs/YYYY-MM-DD-<session>.md` (in repo) | before session end and at each green checkpoint | `[PC-PARTIAL E02-004]` devlog exists but private; `[PROPOSED]` in-repo and public |
| State file | `STATE.md`: current goals, in-flight claims, blockers, next steps | session end | `[PROPOSED]` |
| Decision log (ADRs) | `docs/adr/NNNN-title.md`, numbered, status/context/decision/consequences | any tier-high change | `[PC-PARTIAL E02-025]` `docs/decisions.md` has 2 entries, no status field, no owner rule |
| Plan / spec | `specs/<issue>.md` committed | spec state | `[PC-PARTIAL E01-005, E09-E-001]` `plan/` private; egui migration plan committed with open gates |
| Devlog | `log/devlog.md` committed, append-only, one line per session | session end | `[PC-PARTIAL E02-004]` gitignored there |
| Machine-readable goals | `goals/*.toml` + generated doc | when a number moves | `[PC-VERIFIED E04-050]` |
| Honest assessment | `docs/where-we-stand.md` that agents read first | weekly | `[PC-VERIFIED E01-019, E07-013]` |

**Must be written before a session ends** `[PROPOSED]` (template `handoff.md`): what changed (shas),
what ran and its result, what did *not* run, open claims (keep or release), blockers and questions,
next concrete step, files touched outside ownership (should be none). Commit it with the work.
Shared rules must be readable by everyone: `[PC-PARTIAL E02 §2.1 rule 13]` ("no links to files a reader
cannot open"; machine-specific notes persist despite it, E02-027; the private `craftrules` repo failed for outside contributors, E01-023, E02-013).

---

## 12. Token / cost budgets

Finding: **PhotoCraft publishes no token, money or CI-minute cost data.** Its only effort unit is
"Opus 5.5 agent-hours, one agent working sequentially", self-reported and revised ~10× upward within 8
days (E02-008, E08-002, E08-005). The founder describes the community as a distributed token budget
(E08-018; third-party relay, costs undocumented). Everything in this section is `[PROPOSED]`, except the
CI-cost practices tagged.

**12.1 Per-task budgets by tier** `[PROPOSED]` (calibrate against your own data after 2 weeks, as
PhotoCraft recalibrated its estimates against its 1,004 merged PRs, `[PC-VERIFIED E08-002, E08-004]`;
the estimate itself is derived, not metered):

| Tier | Implementer budget | Reviewer + test author | Hard stop |
|---|---|---|---|
| Low | 1 session, ≤ 8 loop cycles | 1 short session | 2× budget → escalate |
| Medium | ≤ 2 sessions, ≤ 8 cycles each | 1 session each | 2× budget → re-spec / split |
| High | spec + ≤ 3 sessions | 2 reviewers (one adversarial) | any overrun → human decision |

Record actual tokens per session from your tool's usage report in the handoff note; budgets are
meaningless until measured. After two weeks, set each tier's token budget to the p75 of that tier's
merged tasks and keep the 2× hard stop; re-derive monthly (§14).

**12.2 Model selection by task type** `[PROPOSED]`: strongest available model for planning, contract
changes, review/attack, debugging red main; a cheaper model for mechanical edits (renames, i18n rows,
regeneration, label triage). PhotoCraft's trailers show many models (Opus, Sonnet, Haiku, Fable, Codex,
GPT, Qwen, E06 §2.1) but no policy on which to use for what; trailer model names are self-reports.

**12.3 Context hygiene** `[PROPOSED]`: give each agent a scoped reading list (spec + owned files +
AGENTS.md sections), not "read docs/"; keep digests of long docs; PhotoCraft's orientation table lists
14 docs to read (`AGENTS.md:58-75`, E02 §2.3) — too much for every task. Write handoff at ~70% context.

**12.4 When to stop and escalate**: budget overrun (12.1), stop conditions (§7.3), stop-and-ask (§9.3).

**12.5 CI-minute budgeting**

| Practice | Tag |
|---|---|
| Record runner-minute trade-offs next to config; path-select expensive platforms | `[PC-VERIFIED E05-005, E05-013]` |
| Rotate long sweeps by day so each PR pays a fraction | `[PC-VERIFIED E05-021]` |
| Cancel superseded PR runs, never main runs | `[PC-VERIFIED E07-004]` |
| Slow platforms nightly (FreeBSD, ARM64, perf) | `[PC-VERIFIED E05 §0.1]` |
| CI minutes per merged change tracked weekly | `[PROPOSED]` (§13) |

---

## 13. Metrics

Finding: PhotoCraft tracks product-goal metrics well (scorecard, FLOORs, dead-settings count, E07-014)
but no process metrics are published; every process number below was reconstructed by this study from
git (E03, E06, E07). All definitions `[PROPOSED]`; collection commands are adapted from the study's.

| Family | Metric | Definition | Collect from |
|---|---|---|---|
| Flow | Lead time | issue opened → merge on main | `gh issue view N --json createdAt` + merge commit date |
| Flow | PR lifetime | first commit on head → landing commit date (study method, E06-013) | `git log refs/pull/N/head ^<base>` min author date; `git log --first-parent main` |
| Flow | Review lag | PR ready → first human review | `gh pr view N --json reviews` |
| Quality | Red-main minutes / week | Σ(time main's latest completed run is red) | CI API: main push runs, ordered; never-cancel is a prerequisite (E07-004) |
| Quality | Fix-main commits / week | subjects matching `fix main|main red|red since` (E07 §2 regex) | `git log main -i -E --grep=…` |
| Quality | Escaped regressions | issues labelled `regression` whose cause is a merged PR | issue labels + "caused by #N" field |
| Quality | Vacuous-test findings | review/mutation findings tagged `vacuous-test` | PR review labels; commits with "Verified by mutation" (E07-018) |
| Quality | Revert-before-merge rate | reverts on non-first-parent commits ÷ merged PRs | `git log main -i -E --grep='^revert'` + `git rev-list --first-parent` membership (E07-001) |
| Quality | Follow-up fix count per feature | fix PRs referencing a feature within 30 days | issue links; E07-026 method |
| Verification | Change-with-tests share | non-merge commits touching tests ÷ all (E03-011 heuristic) | path regex + added `#[test]` lines |
| Verification | Fail-on-base proof share | PRs whose base-revert job shows ≥1 failing new test | CI artifact |
| Verification | Floors | current value vs FLOOR per corpus | gate output |
| Cost | Tokens per merged change | Σ session tokens ÷ merged PRs | handoff notes / tool usage export |
| Cost | CI minutes per merged change | Σ billable minutes ÷ merged PRs | CI usage API |
| Provenance | Attribution completeness | commits with `Co-Authored-By:` model trailer **and** session trailer ÷ AI-assisted commits | `git log --format=%b`; PhotoCraft: 274 session-trailer vs 3,780 Claude co-author commits on main (E06-011) |
| Provenance | Role separation | PRs where implementer session ≠ test-author session ≠ reviewer session | trailers `Agent-Role:` + session ids |

Targets and cadence `[PROPOSED]`: the owner reviews these weekly. Hard thresholds: red-main minutes > 0 in
two consecutive weeks freezes agent-count growth (§4.1); fail-on-base proof share below 100 % for tier
medium/high merges, or any role-separation violation, is a process incident (`incident-postmortem.md`);
all other metrics are trend-only until two weeks of baseline exist.

Attribution policy `[PROPOSED]`: require trailers in commits (machine-readable, enforced by a commit-msg
check) and decide PR-text disclosure explicitly. PhotoCraft's "No agent attribution" in PRs
(`AGENTS.md:20`) coexists with a product feature crediting models from trailers and was not uniformly
followed (`[PC-PARTIAL E02-011, E06-042]`); the richer `Model-Effort:` trailer reached only 25 non-merge commits
(27 including merges), all by one contributor — a personal convention, not project practice (E03-005, E02-016, errata #18).

---

## 14. Adoption sequence

**Day 0** (before the first agent writes product code)
1. Repo with `AGENTS.md` from `09-templates/AGENTS.template.md`; `CLAUDE.md` points to it. `[PC-VERIFIED E01-003, E02-001]`
2. Workspace skeleton: `core` (headless), `commands` registry, `ui`, `cli`, `xtask`. `[PC-VERIFIED E04 §0.1]`
3. `cargo xtask ci` with fmt, clippy deny, layers, tests, doc tests, lockfile check. `[PC-VERIFIED E05-010, E01-002]`
4. Never-crash lints + `unsafe_code = "forbid"` + command fuzzer stub. `[PROPOSED]` earlier than PhotoCraft (E07-009)
5. Branch protection on main; merge queue enabled; main runs never cancelled. `[PROPOSED]` (E07-003, E07-004)
6. Commit trailer convention + commit-msg hook. `[PROPOSED]` (E06-011)
7. `STATE.md`, `handoffs/`, `docs/adr/` committed. `[PROPOSED]` (E02-004)
8. `risk-tiers.md` and CODEOWNERS for high-tier paths. `[PROPOSED]` (E06-041)

**Week 1**
1. Control channel with screenshot + offscreen snapshot example; documented in AGENTS.md. `[PC-VERIFIED E04-020]`
2. Goals TOML + generated scorecard with `--check`. `[PC-VERIFIED E04-050]`
3. UI-dispatch scan with shrink-only allowlist. `[PC-VERIFIED E04-012]`
4. Fail-on-skip + zero-match-is-blocked in CI. `[PC-VERIFIED E05-024]` for GPU fail-on-skip (adopted on day 38 there, 2026-11-06); zero-match-is-blocked is a documented norm only (E05-051), CI check `[PROPOSED]`
5. Base-revert ("test fails without the fix") CI job. `[PROPOSED]` (E07-015)
6. Claim-check bot on PR open. `[PROPOSED]` (E07-019)
7. Release automation + nightly release dry run. `[PC-VERIFIED E01-024, E05-063]`
8. Run 2–3 implementers + 1 reviewer; measure red-main minutes and review lag.

**Month 1**
1. Pinned corpora/oracles with FLOORs per format/language. `[PC-VERIFIED E04-036]`
2. Mutation spot-checks for tier medium+. `[PROPOSED]` (E07-018)
3. Nightly fuzz with generated target matrix; nightly plain `cargo test`. `[PROPOSED]` (E05-023, E07-008)
4. Perf budgets on a fixed runner, enforced, with `enforce=false` only with a measured note. `[PROPOSED]` (E04-051)
5. `cargo deny` licence/source check. `[PROPOSED]` (E02 §4)
6. Integration batches when merge rate demands it, with file-by-file conflict notes. `[PC-VERIFIED E06-022]`
7. First metrics review (§13); recalibrate budgets (§12) and agent count (§4.1).
8. Monthly backfill sweep for fix commits without tests. `[PROPOSED]`; PhotoCraft ran one such campaign (`[PC-PARTIAL E07-015]`)

---

## Confidence and gaps

- **Strongest**: architecture preconditions (§1), gate composition (§7.2), parallel-agent etiquette
  (§4.2–4.3), failure classes and their observed fixes (§10) — all from git and file contents at the pin.
- **Weakest**: everything about human review, approvals and supervision rests on WebFetch summaries of
  ~22 PR pages (E05 §0.3, E06 §6, E09; errata #17: 4 explicit human approvals in total); branch-protection settings are invisible. If PhotoCraft enforces required
  reviews server-side, §9's "hollow spot" is overstated.
- **Not checkable**: orchestration tooling, number of concurrent agents, token/money cost, supervision
  hours, the private devlog/plan contents, external reusable workflows (`craft-common-actions`).
- **Proposed practices are untested here**: merge queue, independent test author, base-revert job, tier
  table and budgets answer observed failures but have no PhotoCraft evidence of effect. Integration
  batches coinciding with quiet red-main weeks (E07-005) is correlation, not proof.
- **Attribution**: ~half of commits carry no AI trailer; "unknown", not "human" (E03). Model names in
  trailers are self-reports.
- **What would change conclusions**: PR review data via the GitHub API; the contents of `log/devlog.md`;
  cost data from any maintainer.
- Citations here are evidence IDs; primary shas/PRs are carried where load-bearing and resolve through
  `deliverables/01-evidence-ledger.md`. `scripts/verify_citations.py` run after review (2026-11-12): 15 citations checked, 0 unresolved.
