# 10 — Transferability: building an IntelliJ-like IDE in Rust with PhotoCraft's methods

Audience: an experienced engineer deciding how to set up an agent-heavy IDE project.
Labels: **VERIFIED** (observed in a primary source, cited by evidence ID, e.g. `E04-031`;
the evidence file carries the sha/path/PR), **INFERRED** (reasoned from verified evidence,
chain given), **PROPOSED** (our recommendation for the IDE; never a PhotoCraft practice).
Everything about the IDE in this document is PROPOSED unless it says otherwise.
Evidence base: `evidence/E01`–`E09` at upstream `main` `74330157cb` (2026-11-12).

Terms used throughout (PhotoCraft-specific):
- **command registry**: the engine's table of `CommandSpec`s (id, label, menu, params doc, `run` fn), dispatched by id from UI, CLI, control channel and MCP (E04-010, E04-011).
- **control channel**: a JSON protocol on a running app (`--control`) to inspect state, inject input, and take `ui.screenshot` (E04-013).
- **panic_hunt**: a test that enumerates every registered command and fuzzes it for panics; part of the CI gate (E04-012).
- **scorecard**: TOML goal files rendered into `docs/scorecard.md`, with a CI staleness check `--check` (E04-050).
- **FLOOR**: a ratchet constant that a test enforces and that may only rise (E04-042, E01-015).
- **integration batch**: a maintainer branch that bundles many PRs for one CI run and one conflict pass before landing (E07-002, E06-022).
- **house rules**: an org-wide rule block copied into AGENTS.md with a sha256 header, checked by a workflow (E02-012, E04-035).

---

## 1. Verdict

- **Direct (PROPOSED, high confidence):** headless core + `xtask layers` from day 1 (E04-007, E04-031); one action registry for every front-end + UI-dispatch check (E04-012); fuzz every action (E04-012); local gate == CI gate (E05 §0.2); generated docs with `--check` (E04-050); ratchet floors (E04-042); fail-on-skip (E05-024, E07-018); hash-checked shared rules (E02-012); agent-isolation rules (E01-016).
- **With adaptation:** the oracle strategy. Photoshop *gave* PhotoCraft "correct" (menu tree, embedded composites, corpora; E04-036, E04-042); an IDE must *build* it: compiler-as-oracle, differential LSP servers, round-trip/idempotence, incremental == from-scratch, pinned snapshot corpora. Also adapt control channel/screenshot, MCP/CLI, feature matrices, and perf budgets, which must be *enforced* (PhotoCraft: 0 of 88; E04-051).
- **Does not transfer:** reference-app parity as the progress metric (it measured wiring; E07-013); breadth-first fan-out from day 1 (an IDE core is deep and stateful); CPU-vs-GPU pixel parity as a core oracle.
- **Biggest risks:** (1) agents fan out onto an unstable incremental/semantic core, each feature encoding different wrong assumptions about invalidation, threading or undo; (2) green-but-hollow checks (feature counts, skip-passing tests, unenforced latency) as in E07-013, E07-018, E04-051; (3) individually green PRs colliding on shared semantic state, as in E05-052 but harder to detect.

---

## 2. Why PhotoCraft's method worked where it worked

Finding (INFERRED): PhotoCraft's throughput came from a problem shape in which (a) "correct" was
defined externally and cheaply checkable, (b) features were many, shallow and weakly coupled, and
(c) one headless entry point let agents exercise every feature without a GUI. Where any of these
was missing, the metrics stayed green while the product was not.

### 2.1 Enabling conditions

| Condition | PhotoCraft evidence | Label | Why it mattered for agents (INFERRED chain) |
|---|---|---|---|
| A reference product defines "correct" | Photoshop's menu tree encoded as data → generated parity checklist + FLOOR (E01-015, E04-042); `gaps.md` "the work list agents pick from" (E01-020) | VERIFIED | The backlog wrote itself: each menu item is a task with an obvious acceptance test ("dispatches a command"). |
| Embedded pixel oracle | PSD files carry Photoshop's own merged composite; corpus test passes at ≤2/255 (E04-036) | VERIFIED | An agent can judge its own compositing change without a human looking at pixels. |
| Pinned, hashed corpora | 1,044 files in 10 sha256 manifests; floors "never lower them" (E04-036) | VERIFIED | Reproducible targets; regressions are numbers, not opinions. |
| Internal reference implementation | CPU compositor is "the oracle"; 78 GPU-vs-CPU parity tests at 2/255 (E04-037) | VERIFIED | A second implementation checks the fast one. |
| Headless deterministic core | `crates/engine` has no UI/GPU deps; 135 test files build `Session::new()` (E04-007, E04-008); seeded randomness, coordinate-hashed noise (E04-029) | VERIFIED | Tests are cheap, parallel and repeatable. |
| One command registry behind every front-end | `CommandSpec` registry, ~76 → ~805 ids (regex estimate) (E04-010); UI/CLI/control/MCP all dispatch by id (E04-012) | VERIFIED (counts INFERRED) | A new feature is a new registry entry; fuzzing, docs, CLI and MCP reach it for free (E04-016). |
| Cheap objective checks in one gate | `cargo xtask ci`: fmt, clippy, layers, panel-commands, scorecard --check, test, panic_hunt, doctest, wasm (E05 §0.2) | VERIFIED | Agents can reproduce CI locally and iterate to green. |
| Breadth-first, weakly coupled surface | Typical change +52/−5 lines in 2 files; 77.5 % of non-merge commits touch tests (heuristic) (E03-011) | VERIFIED (numbers); INFERRED (coupling) | Many independent small tasks parallelise; conflicts are mostly textual. |

### 2.2 Where it was hollow

| Weakness | Evidence | Label | Lesson for the IDE (PROPOSED) |
|---|---|---|---|
| Parity metric measured wiring | "625/625 menu items are live … only means each item dispatches *a* command"; 214 shortcut failures in an audit; project re-estimated 55–70 % surface, 20–35 % switchable (E07-013: 20783fdc70; E01-019: 433b84fae7) | VERIFIED | Never let "feature exists" be the headline metric; measure behaviour against an oracle. |
| Perf budgets unenforced | 88 scenarios, 0 `enforce = true` (`74330157cb:perf/budgets.toml`); baseline recorded at load ~225 on another machine class (E04-051, E05-028) | VERIFIED | Latency is a core IDE requirement; budgets must gate on a fixed runner. |
| Tests that passed without testing | 57 GPU checks returned early and passed on CI's software rasterizer (2ff8f419cb); several tests asserted nothing (602344bae0, c441fd350c) (E07-018, E05-024) | VERIFIED | Fail on skip; require zero-match runs to be BLOCKED; mutation spot-checks. |
| Individually green PRs colliding | Recurring "main red since #X + #Y" fixes (e.g. 351149f0df, 06650357d8); 59 fix-main commits (E05-052, E07 §0) | VERIFIED | Real merge queue from day 1. |
| Save-path regressions | Durability fix correct on local NTFS broke SMB saves; ~17 days from report (#9440) to fix (1253e79d68) (E07-021) | VERIFIED | IDE file I/O (VFS, save, external change) needs environment-diverse fault injection. |
| Planned mechanisms never built | Validated param schema → free-text "JSON-ish" doc string; golden images/`xtask bless` never implemented; op-based history → snapshots (E04-003, E04-027) | VERIFIED | Build the contract-level mechanisms before fan-out; do not let them slide. |
| Doc drift | README/AGENTS.md crate map and counts stale; generated docs stayed accurate (E04-004, E04-006) | VERIFIED | Generate every number-bearing doc. |
| Shared-line conflict hotspots | Conflict markers committed into status lines; scorecard.md 3rd most-touched file (E07-020) | VERIFIED | No "every PR edits this line" conventions. |

INFERRED overall: the conditions in §2.1 are what made a six-week, ~1M-line (E04-004) build
feasible; the weaknesses in §2.2 are exactly the places where no cheap oracle existed (behaviour
vs wiring, timing, real filesystems, cross-PR semantics). An IDE has *more* of the second kind.

### 2.3 Where the analogy holds and breaks (INFERRED)

| PhotoCraft concept (evidence) | IDE counterpart | Holds? | Why |
|---|---|---|---|
| Document + layers in a `Session` (E04-008) | Project model + open files + derived indexes | Partly | IDE state is mostly *derived* and must stay consistent with source under edits |
| Command = one history step (E04-011) | Action = one undoable transaction | Yes for edits | Multi-file refactors and background analysis have no PhotoCraft analogue |
| Photoshop menu tree as backlog (E01-015) | IntelliJ/rust-analyzer feature lists | Weakly | A feature list says *what*, not *what output is correct*; no embedded oracle |
| Embedded composite as oracle (E04-036) | Compiler output on the same source | Yes, for diagnostics/types/refactor validity | Compiler covers analysis, not completion ranking or UX |
| CPU reference vs GPU (E04-037) | From-scratch vs incremental analysis | Yes | Same "two implementations, one trusted" structure |
| Pixel tolerance 2/255 (E04-036) | Exact equality (types, spans) or ranking metrics | Partly | Most IDE outputs are discrete; tolerance applies only to ranking/latency |
| Render latency (E04-051) | Keystroke-to-paint, completion latency | Yes, but more central | Latency is a primary IDE quality, not a secondary goal |
| File formats & corpora (E04-036) | Language versions, editions, cfgs, macros | Partly | Language semantics evolve; corpora need pinned toolchains too |
| Plugins via wasmi sandbox (E04-015) | Plugin API with long-term stability | Weakly | IDE plugin ecosystems depend on API stability for years |


---

## 3. Mechanism-by-mechanism transfer table

Transfer class: **direct** (same mechanism, new domain nouns), **adapt** (same idea, different
check), **none** (no useful IDE analogue, or harmful). PhotoCraft column VERIFIED unless marked;
IDE columns PROPOSED.

| # | PhotoCraft mechanism (evidence) | IDE equivalent | Class | Adaptation | Residual risk |
|---|---|---|---|---|---|
| 1 | Headless engine, no UI/GPU deps; tests build `Session::new()` (E04-007, E04-008) | Headless **workspace server**: opens a project, runs analysis and actions with no window | direct | Session state is long-lived (VFS, index, caches), not one document; tests need project fixtures, not blank canvases | Hidden UI-thread assumptions leak into core (e.g. "current editor"); must be banned by layering |
| 2 | Layered crates + `xtask layers` parsing `cargo metadata`, UI-crate ban below L6, in CI day 1 (E04-031, E04-002) | Same linter with IDE layers (§5) plus bans: no UI crates, no `std::thread::spawn`/blocking I/O in analysis layers | direct | Add rules for *concurrency* and *I/O* placement, not just dependency direction | Layering is necessary, not sufficient; runtime coupling via shared caches is invisible to `cargo metadata` |
| 3 | Command registry + `panel-commands` lexical check, shrink-only allowlist (1 entry at HEAD) (E04-010, E04-012) | Action registry (IntelliJ `AnAction` analogue) with typed param/result schemas; check that UI handlers only dispatch action ids | direct | Make params a **validated schema** (PhotoCraft planned this and shipped a free-text doc string, E04-003) | Lexical check is incomplete by its own admission (E04-012); back it with a runtime assertion that UI-originated mutations carry an action id |
| 4 | `panic_hunt`: fuzz every registered command (E04-012) | Fuzz every action on every fixture state, plus fuzz *edit sequences* against incremental analysis | adapt | Generator must produce schema-valid params and meaningful caret/selection states; add invariant checks (index consistency, tree well-formedness) beyond "no panic" | "No panic" is a weak oracle; without invariants this repeats the wiring trap |
| 5 | Control channel + `ui.screenshot`; offscreen `snapshot` example replaying control scripts; AGENTS.md "look at the PNG" (E04-013, E04-020, E04-021, E04-024) | Control channel exposing editor state as **structured data** (caret, decorations, completion popup items, inspection markers), plus screenshot for layout | adapt | Most IDE UI correctness is textual/structural; assert on structured state, use screenshots only for layout/rendering | Visual self-checks were rarely traced in history (3 commit messages, 1 PR sampled, E04-024); frequency unknown |
| 6 | Control protocol reused as UI test driver in kittest (32+71 files) (E04-023) | UI tests drive the same control channel | direct | — | Low |
| 7 | MCP server (26 tools, generic `command_list`/`command_run`) and CLI `serve` (E04-016, E04-009) | MCP/CLI over the workspace server: `actions list`, `action run`, `diagnostics`, `goto`, `find-usages` | direct | Agents developing the IDE should *use* it to check work; PhotoCraft has no evidence dev agents did so (E04-018, E04-026) | Product interface and dev-check interface can drift if not the same code path |
| 8 | testkit: GPU lock, perf sampler, date-rotated `Sweep`; no golden images (E04-027) | testkit with fixture-project builders, snapshot assertion + bless, deterministic scheduler, latency sampler | adapt | Build `bless`-style snapshot tooling **day 1** (PhotoCraft planned and never built it, E04-027) | Snapshot blessing becomes rubber-stamping; require reviewer sign-off on snapshot diffs |
| 9 | CPU reference vs GPU parity on software rasterizer, fail on skips (E04-037, E04-029, E05-024) | Reference vs optimised implementations: naive from-scratch analysis vs incremental; simple vs SIMD lexer | adapt | The "two implementations" idea transfers; GPU specifics do not (unless you write a custom renderer) | Reference implementation must itself be trusted — keep it small |
| 10 | Oracle/corpus floors: embedded composites, 1,044 hashed files, never-lower floors (E04-036) | Pinned corpora of real codebases (sha-pinned git revs) with ratcheting pass floors per check | adapt | Oracle is the compiler / differential servers, not a stored image (§4) | Corpus licensing and size; floors that measure "didn't crash" rather than "agreed with oracle" |
| 11 | Scorecard TOML → generated doc, `--check` in CI (E04-050) | Per-language feature matrix + quality metrics generated from tests, `--check` in CI | direct | Rows must cite a test that measures behaviour, not presence | Scorecard drift into a wiring metric (E07-013) |
| 12 | Perf budgets with `enforce` flag, "never invent a number" (E04-051, E09-F-004) | Latency budgets (keystroke-to-paint, completion p95, find-usages) | adapt | **Enforced on a fixed, dedicated runner** with a measured baseline; PhotoCraft had 0 of 88 enforced and a contended baseline (E05-028) | Noisy runners → flaky gates → gates turned off; use counters (allocations, query recomputations) as low-noise proxies |
| 13 | Parity checklist / `gaps.md` ranked work queue; estimates in agent-hours (E01-015, E01-020, E02-008, E08-002) | Ranked backlog per language/feature; agent-hour estimates calibrated against your own merged history | adapt | No reference menu tree; derive the queue from IntelliJ/rust-analyzer *feature lists* as inspiration, but acceptance must be oracle-based | PhotoCraft's own estimate was revised ~10× upward in 8 days (E08-005); treat early estimates as guesses |
| 14 | AGENTS.md day 0, hash-checked house rules, stop-and-ask list (E01-003, E02-009, E02-012) | Same | direct | Add IDE-specific invariants (threading, cancellation, VFS ownership) to the guide and back each with a check | Rules without checks diverge (E02 §4) |
| 15 | Integration batches (E07-002, E06-021, E06-022) | Real merge queue (serialised CI on the merge result) | adapt | Replace manual batches with automation; batch only many approved Medium PRs in one area (08 §4.6); High-tier changes land alone (08 §9.1) | Queue throughput limits; needs fast gate |
| 16 | Nightly release dry run (E05-063, E05-062) | Same, plus nightly "open the big corpus, index, run all inspections" smoke | direct | — | Nightly-only failures are noticed late |
| 17 | Compile-time completeness via destructuring (E04-033) | Same for settings serialisation, protocol types, plugin API structs | direct | — | Low |
| 18 | Golden-image testing (planned, never built) (E04-027) | Snapshot tests of trees/highlights/completions | adapt | Do it | Covered in row 8 |

---

## 4. Where an IDE is harder, and what replaces the missing oracle

Finding (INFERRED): PhotoCraft's strongest checks compared output to something Photoshop had
already produced (E04-036, E04-042). An IDE has no such single ground truth: correctness is
semantic, language-specific and often only defined relative to a compiler's behaviour. The work
is therefore to **manufacture** objective checks before agents are asked to produce features.
Every row below is PROPOSED.

### 4.1 Difficulty → replacement check

| IDE difficulty | Why it lacks PhotoCraft's oracle | Objective check that gives agents a target | Strength / caveat |
|---|---|---|---|
| **Parsing** (incl. error recovery) | No reference parse tree; recovery behaviour is a design choice | (a) Round-trip: `parse → print → parse` gives identical tree; lossless tree reproduces source byte-for-byte. (b) Differential: accept/reject agrees with the reference parser (for Rust, `syn` or a nightly parse-only rustc mode; full `rustc` also rejects code in later phases, so compare only syntax errors) on corpora and conformance suites. (c) Snapshot of trees on pinned corpora with ratcheting floor. (d) Fuzz random edits: tree never panics, spans stay in bounds | (a)(b) are strong; (c) needs reviewed blessing; recovery quality has no oracle → snapshot + human review |
| **Name resolution, type inference** | Semantics defined by the compiler, not a file | Differential vs the compiler: for every expression in a corpus, compare inferred types/resolved paths against compiler-derived facts. rustc exposes no stable resolution/type dump (save-analysis was removed), so derive them by compilation: inject `let _: <inferred type> = <expr>;` or a path-use probe at sampled sites and require `cargo check` to accept it (and reject a deliberately wrong type). Use an existing server (rust-analyzer) as a second opinion. Floors on agreement rate per corpus | Two oracles that disagree flag tasks for humans; never auto-accept "matches rust-analyzer" where rust-analyzer is known to be wrong |
| **Diagnostics** | Same | `cargo check --message-format=json` as oracle: IDE diagnostics on a pinned corpus vs compiler diagnostics (precision/recall per code), ratcheting | Strong for compiler-equivalent diagnostics; IDE-only lints need their own snapshot tests |
| **Refactoring safety** | No reference refactorer output | **Refactor → still compiles → tests still pass**: apply each refactoring at sampled sites in corpus projects, run `cargo check` and the project's tests. Plus inverse properties (rename A→B→A = identity when B is fresh; extract/inline round-trip) and "no semantic change" via the IDE's own resolver before/after, cross-checked by the compile-and-test result (no stable compiler API exposes resolved references) | The best oracle available; cost is high (compile per sample) → sample and rotate by day like PhotoCraft's `Sweep` (E04-027) |
| **Formatting** | Style is a spec | Idempotence `fmt(fmt(x)) == fmt(x)`; differential vs `rustfmt` where you aim for compatibility; parse-equivalence before/after | Strong, cheap |
| **Completion, highlighting, inlay hints** | Ranking/coverage is judgement | Snapshot tests of completion lists/highlight token streams on pinned corpora; "expected item present in top-k" metrics with floors; differential vs LSP servers | Ranking quality stays partly human; keep the metric *behavioural* (top-k hit), not "provider exists" |
| **Incremental computation** | The "correct" incremental result is the from-scratch result | **Index/analysis consistency**: after any edit sequence, incremental state == fresh from-scratch computation (query results, index contents, diagnostics), compared after normalising interned ids, file ids and unordered collections, which legitimately differ between runs. Fuzz edit sequences. This is the IDE analogue of CPU-vs-GPU parity (E04-037) | The single most important check; must not be skippable (E05-024 lesson) |
| **Latency budgets** | No reference timings | Enforced budgets on a dedicated fixed runner (keystroke→highlight, completion p95, open-project-to-ready); plus low-noise proxies: number of query recomputations, allocations, files re-parsed per edit | PhotoCraft's budgets never gated (E04-051); proxies avoid noisy-runner flakiness |
| **Long-lived mutable state & concurrency** (VFS, caches, background indexing, cancellation) | Image editor sessions are mostly single-document, snapshot history (E04-003, E04-011) | Deterministic scheduler in tests (seeded interleavings); loom-style model checks on core sync primitives; invariants checked after every fuzzed step; cancellation tests ("cancelled query leaves no partial state") | Hard; needs human-owned design (§6) |
| **File system reality** | — | Fault-injecting VFS backend: external modifications, renames under watch, slow/network FS, permission errors, case-insensitive FS, symlinks. PhotoCraft's save path regressed SMB users (E07-021) | Environment diversity must be in CI, not only on a developer's machine |
| **Editor session behaviour** | No reference app trace | **Deterministic replay**: every editor session is a command log (action ids + params + timestamps); replays produce identical document/index/UI state; bug reports attach logs; replays become regression tests | Requires that *all* mutations go through the action registry (§5) |
| **Undo/redo** | — | Property: `do; undo` restores document *and* derived state; `undo; redo` idempotent; fuzz action sequences with interleaved undo | PhotoCraft switched to whole-document snapshots (E04-003); an IDE likely needs per-file or transactional undo across files (refactorings) — design question for humans |
| **Plugin API stability** | — | API surface snapshot (public items + signatures) diffed in CI with semver classification; a corpus of sample plugins that must build and pass against every PR | Breaking changes need human approval — a stop-and-ask item |
| **LSP/DAP conformance** | Protocols have specs, not oracle binaries | Protocol conformance tests from the spec (message shapes, capability negotiation, ordering); differential: drive both your server and an existing one with recorded client traces; existing editors (VS Code, Neovim) as smoke clients | Spec ambiguity → snapshot the chosen behaviour |
| **Huge fixture codebases** | PhotoCraft's corpora are 1,044 files (E04-036) | Tiered corpora: tiny hand-written fixtures (unit), medium pinned crates (PR gate), very large repos (nightly, e.g. a multi-hundred-crate workspace). Pin by sha, cache by hash as PhotoCraft's `corpus` job does (E04-036) | CI cost; rotate big-corpus coverage by day |

### 4.2 Oracle hierarchy for agents (PROPOSED)

Rank checks by how much an agent can trust a green result:

1. **External-tool equivalence** — compiler accepts, tests pass, `rustfmt` agrees. Closest to PhotoCraft's embedded composite (E04-036).
2. **Internal properties** — round-trip, idempotence, incremental == from-scratch, undo inverse. Closest to CPU-vs-GPU parity (E04-037).
3. **Differential vs other implementations** — rust-analyzer, other LSP servers. Disagreements are triage tasks, not failures.
4. **Reviewed snapshots with ratchet floors** — stable but only as good as the blessing review.
5. **No-panic fuzzing** — necessary, never sufficient (`panic_hunt` analogue, E04-012).
6. **Presence/wiring counts** — do not use as progress metrics (E07-013).

INFERRED: PhotoCraft's agents had level 1 (via Photoshop's files) for free and leaned on level 6
for the headline number; the IDE must invest in levels 1–2 *before* fan-out.

### 4.3 Cost of the oracles (INFERRED / PROPOSED)

PhotoCraft's main oracles were cheap per run: a corpus comparison at ≤2/255 (E04-036) and a
CPU-vs-GPU comparison on a software rasterizer (E04-037, E04-029). The IDE's strongest oracles are
expensive: a refactor-compiles check costs a `cargo check` (and possibly a test run) per sampled
site; differential runs need a second server warmed on the same corpus. PROPOSED budget split:

| Check | PR gate | Merge queue | Nightly |
|---|---|---|---|
| Parse round-trip, format idempotence, schema completeness, layers | full | full | full |
| Incremental == from-scratch fuzz | fixed small seed set | larger seed set | long run, new seeds |
| Diagnostics vs `cargo check` | small fixtures | medium pinned corpus | large-repo corpus |
| Refactor compiles + tests pass | changed refactorings only, few sites | rotated sample (PhotoCraft `Sweep` pattern, E04-027) | full sample |
| Differential vs rust-analyzer / other servers | — | — | full; disagreements filed as triage issues |
| Latency budgets | proxy counters | fixed-runner timings | full scenario set |

The rotation idea is VERIFIED in PhotoCraft (`testkit::sweep` slices long sweeps by UTC date,
E04-027); its use for semantic oracles is PROPOSED. Nightly-only checks find problems late
(PhotoCraft's release-only failures motivated its nightly dry run, E05-063, E05-062), so every
nightly finding should become a PR-gate fixture.

---

## 5. Proposed IDE architecture for agent-checkability (PROPOSED)

Design goal: every behaviour an agent could change must be reachable headlessly, through one
registry, and checkable by an oracle from §4. Layers are enforced by an `xtask layers` analogue
from the first commit (copying E04-031).

### 5.1 Layer diagram

```
 L8  apps/ide (desktop shell)   apps/ide-cli   apps/ide-lsp   apps/ide-dap   apps/ide-mcp
        |                          |              |              |              |
 L7  ui-shell (egui/other; editor views, panels, keymaps, themes)   control-channel server
        |                                                            |
 L6  workspace-server  (headless: open project, run actions, events, command log, replay)
        |                     \
 L5  action-registry (ActionSpec: id, schema, enablement, run) <-- plugin-host (sandboxed, versioned API)
        |
 L4  refactor / intentions / inspections / formatting / completion   (one crate per family)
        |
 L3  semantic: incremental query engine, name resolution, types, index   (per-language crates)
        |
 L2  syntax: lexer, lossless trees, per-language grammars
        |
 L1  text: rope, line index, edits/diffs        vfs: file ids, snapshots, watcher abstraction
        |
 L0  base: ids, interning, cancellation token, diagnostics model, test-time deterministic scheduler
 ---------------------------------------------------------------------------------------------
 test-only: testkit (fixtures, snapshot+bless, fault-injecting VFS, replay, latency sampler)
```

### 5.2 Rules to enforce in CI

| Rule | Check | Copies PhotoCraft (VERIFIED) or fixes a weakness |
|---|---|---|
| Edges point downward only; unregistered crate = error | `xtask layers` over `cargo metadata` | Copies E04-031 |
| No UI crates below L7; no blocking I/O or thread spawning below L6 (only via L0 scheduler/VFS) | `xtask layers` + clippy `disallowed-methods`/`disallowed-types` | Extends E04-032 (`disallowed-types` was used for a UI widget) |
| Every UI mutation dispatches an action id | Lexical scan with shrink-only allowlist **plus** runtime assertion in debug builds | Copies E04-012; runtime half fixes its admitted incompleteness |
| `ActionSpec` params and results are typed and schema-validated; schema exported as JSON | Unit test: every registered action has a schema; fuzzer generates from it; CLI/MCP reject invalid params | **Fixes** E04-003 (schema planned, shipped as free-text "JSON-ish" doc) |
| Every action is fuzzed on fixture states with invariants checked | `action_hunt` (panic_hunt analogue) in the gate | Copies + strengthens E04-012 |
| Incremental == from-scratch after fuzzed edits | Consistency test in gate, not skippable | New (no PhotoCraft analogue beyond E04-037 pattern) |
| Tests prove they ran (no silent skip; zero-match filter = failure) | Gate wrapper parses runner output | Copies E05-024 fix; avoids E07-018 |
| Plugin API surface snapshot diff | `xtask api-check` | New |
| Generated docs (action catalog, feature matrix, scorecard) are fresh | `--check` | Copies E04-050 |
| Latency budgets enforced on fixed runner | `xtask perf --enforce` on dedicated hardware | **Fixes** E04-051 / E05-028 |
| Serialisers destructure structs | Code pattern + review | Copies E04-033 |
| Workspace lints: forbid unsafe outside an allowlisted crate set, deny unwrap outside tests, complexity ceiling | `[workspace.lints]`, `clippy.toml` | Copies E04-032 (unsafe allowlist is an adaptation: rope/interning may want unsafe) |

### 5.3 The action registry (IntelliJ `AnAction` analogue)

- **Shape (PROPOSED):** `ActionSpec { id, label, menu_path, default_keys, params: Schema, result: Schema, enabled: fn(&Ctx)->bool, run: fn(&mut Workspace, Params, Cancel)->Result<Out>, undo_kind }`. PhotoCraft's `CommandSpec` has id/label/menu/shortcut/params-doc/enabled/run/journal (E04-010) — the same shape minus typed schemas and cancellation.
- **Consumers:** menus, keymaps, command palette, control channel, CLI `run`, MCP `action_run`, LSP `workspace/executeCommand`, plugins, command log replay. One registry means fuzzing, docs and agent access scale with feature count, as PhotoCraft's MCP inherited ~805 commands through two generic tools (E04-016, E04-010 — count is a regex estimate).
- **Context:** IDE actions depend on caret, selection, focused file, project model. Make context an explicit, serialisable parameter (not ambient UI state) so headless replay and fuzzing can construct it. INFERRED from E04-008: PhotoCraft's headless tests worked because commands took the `Session` plus JSON.
- **Read vs write split:** queries (goto, find usages, hover) are actions with no undo and must run on snapshots concurrently; writes go through a single writer with transactional undo. This is a deliberate departure from PhotoCraft's snapshot history (E04-003), which would be too costly for multi-file refactors over large projects (INFERRED from scale, not measured).

### 5.4 Headless mode

`ide-cli open <project> --run <action> --params <json>`, `ide-cli serve` (JSON-RPC, like PhotoCraft's `serve`, E04-009), `ide-cli replay <log>`, and `ide-cli check <corpus>` (run diagnostics and compare with `cargo check`). Dev agents should be *told* in AGENTS.md to verify through these, mirroring PhotoCraft rule 6 ("Verify UI changes visually", E04-020), and the PR template should ask for the command transcript.

### 5.5 Agent guide skeleton for the IDE (PROPOSED)

PhotoCraft's AGENTS.md was a day-0 artefact with architecture invariants, a "before you finish"
checklist and parallel-agent rules (E01-003, E02 §0). The IDE equivalent should keep the same
structure, but every invariant must name its enforcing check (PhotoCraft's unchecked rules are the
ones practice diverged from; E02 §4):

| Section | Content | Enforced by |
|---|---|---|
| 0. Read first | The honest-status doc (generated feature matrix + known gaps) | `--check` on the generated doc (copies E01-019, E04-050) |
| 1. Everything is an action | New behaviour = new `ActionSpec` with schema | schema-completeness test; UI-dispatch scan |
| 2. Layers | Diagram from §5.1 | `xtask layers` |
| 3. Threading & cancellation | Analysis code is pure over snapshots; long work checks the cancel token | clippy `disallowed-methods`; deterministic-scheduler tests |
| 4. Incremental correctness | Any query change keeps incremental == from-scratch | consistency fuzz test |
| 5. Verify through the product | Run `ide-cli check`/`run`/`replay`; paste transcript in PR; screenshot for layout changes | PR template field; reviewer checklist |
| 6. Picking work | Ranked queue; claim before coding | claim board; registry uniqueness tests |
| 7. Parallel agents | Own worktree (playbook §6) and `CARGO_TARGET_DIR`, own module (E01-016) | claim check on PR open; owned-file scope check in review (08 §4.4) |
| 8. Before you finish | `cargo xtask ci` green locally; failing-before fixture for fixes | merge queue |
| 9. Stop and ask | Plugin API, index format, settings migrations, save path, release, licensing, secrets | path-based required reviewers |


---

## 6. Work decomposition for agents

Finding (INFERRED): PhotoCraft parallelised well because most tasks were "add one command behind
one menu item", touching ~2 files (E03-011), and collisions were mostly textual (duplicate i18n
rows, constants; E07-019) or same-line doc edits (E07-020). Its deepest structural decisions
(registry shape, layering, headless engine, history model) were all present in the first commit
(E04-003, E01-002) — whether written by agents or humans is unknown (no trailer; E04 Open questions).
An IDE has a larger deep core, and errors in it are semantic, not textual.

### 6.1 Classification (PROPOSED)

| Work | Shape | Parallelisable? | Supervision model | Contract it depends on |
|---|---|---|---|---|
| Inspections / lints | Many, independent; each is "pattern → diagnostic (+ fix)" | Yes — PhotoCraft-menu-like | Agents; Medium-tier review (08 §9.1); oracle = snapshot + compiler-agreement where applicable | Semantic query API, diagnostics model |
| Intentions / quick fixes | Many; each a small refactor | Yes | Agents; oracle = "still compiles + tests pass" on corpus samples | Refactor/edit API, undo model |
| Per-language syntax support (grammar, highlighting, folding, structure view) | One per language, internally deep-ish | Yes across languages | One agent stream per language; human sign-off on grammar design | Syntax tree API |
| UI panels (project view, structure, problems, VCS log) | Breadth | Yes | Agents; control-channel structured-state tests + screenshot | Action registry, event model |
| Keymaps (IntelliJ, VS Code, Vim emulation) | Data + small logic | Yes | Agents; oracle = keymap tables vs published references | Action ids |
| File-type support (TOML, JSON, YAML, Markdown) | Breadth | Yes | Agents | Syntax + VFS |
| Settings pages | Breadth | Yes | Agents; "settings that do nothing" metric (PhotoCraft's 66/129 → 8/199, E07-014) | Settings schema |
| Incremental query engine | Deep, contract-heavy | **No** | Human design owner + 1–2 supervised agents; ADRs | — (it *is* the contract) |
| VFS & file watching | Deep, platform-specific, durability-critical | **No** | Human owner; fault-injection required (E07-021) | — |
| Indexing (persistent, background) | Deep; consistency + latency | **No** initially | Human owner | Query engine, VFS |
| Undo/transaction model | Deep; crosses files | **No** | Human owner | Action registry |
| Threading / cancellation model | Deep; global | **No** | Human owner; model checking | — |
| Plugin API & host | Deep; stability commitment | **No** | Human owner; semver policy | Everything |
| Refactoring engine core (rename, move, extract framework) | Deep; correctness-critical | Partly (individual refactorings later) | Human owner for the framework; agents for individual refactorings once oracles exist | Semantic API, undo |

### 6.2 Sequencing (PROPOSED)

1. **Contracts first.** Write ADRs for the query engine, VFS, threading/cancellation, undo, action schema and plugin API. Each ADR names the invariant and the test that enforces it. PhotoCraft shows what happens when a planned contract is not built: the validated schema and op-based history both silently changed shape (E04-003).
2. **Contract tests before fan-out.** The incremental==from-scratch check, the action fuzzer with invariants, the undo inverse property, and the replay determinism test must exist and be in the gate before any breadth work is assigned.
3. **Fan out by family**, one crate or module per family (PhotoCraft rule "a new module per area", E01-016), with ownership recorded in a claim board (PhotoCraft's epics with "Free / Being worked on / Merged" tables, E06-034).
4. **Re-centralise periodically**: audits that turn observed failure classes into gates, as PhotoCraft did with never-crash (E07-009) and fail-on-skip (E07-018).

INFERRED justification: a breadth agent that encodes a wrong assumption about invalidation produces
a correct-looking feature whose bug surfaces only under specific edit sequences; with 50 such features,
changing the contract later means 50 rewrites. In PhotoCraft the analogous cost was low because
commands took a session + JSON and returned JSON (E04-011) — a narrow, stable contract.

### 6.3 Example task cards (PROPOSED)

A breadth task is ready for an agent only when its card names the oracle. Two contrasting cards:

- **Inspection "redundant clone" (playbook tier Medium).** Files: new module `inspections/redundant_clone.rs`, registry entry, fixtures. Acceptance: snapshot test on 10 positive and 10 negative fixtures; quick-fix applied to all corpus hits compiles and passes the corpus crates' tests; feature-matrix row generated. Parallel-safe: yes.
- **"Make goto-definition work across macro expansions" (Medium; High if it changes the query graph).** Touches the semantic layer and possibly the query graph. Acceptance: differential vs compiler-resolved spans on the corpus above the current floor; incremental consistency still zero mismatches; latency budget unchanged. Needs a human-reviewed design note first; not parallel-safe with other query-engine work.

INFERRED from PhotoCraft: its gap epics already list "Main files" per item to prevent collisions
(E06-034); adding "oracle" and "tier" fields is the IDE-specific extension.

---

## 7. Process transfer

The study's playbook (`deliverables/08-playbook.md`, written in parallel) covers risk tiers,
independent test authorship, a real merge queue, in-repo session state and provenance trailers.
This section lists only the IDE-specific gates and the PhotoCraft evidence each answers.

| Playbook topic | PhotoCraft evidence | IDE-specific application (PROPOSED) |
|---|---|---|
| **Risk tiers** | Human approval rarely visible; supervision mostly labels and merge decisions (E06-041, E05 §0.3); merge authority concentrated in few people (E03-008) Use the playbook's tiers (08 §9.1) unchanged. **Medium** — breadth work confined to its own module (inspection, intention, panel, keymap, file type, settings page): reviewer agent + human maintainer review record + oracle gates; semantic-analysis and individual-refactoring changes that alter no contract are also Medium, and the human reviewer additionally signs off oracle results and snapshot diffs. **High** — query engine, VFS, undo, threading, plugin API, index format, save/durability (shared contracts or persistence in 08 terms): ADR + named human owner approval, path-based required reviewers, merged alone. **Low** — docs and new tests only |
| **Independent test authorship** | Tests that asserted nothing; detection via CodeRabbit and mutation (E07-018); 16 of 27 security fixes added no `#[test]` (E09-G-003) | As in the playbook (08 §8): tests by a different session for every Medium/High change; for High, written from the ADR before the code; mutation testing on changed analysis code |
| **Real merge queue** | 59 fix-main commits; "red since #X + #Y" (E05-052); integration batches as manual staging (E07-002); never cancel main CI (E05-004) | Merge queue running the full gate on the merged result; main CI never cancelled; registry/catalog consistency tests (PhotoCraft found duplicate rows cheaply once such tests existed, E07-019) |
| **In-repo session state** | Hand-off via gitignored, private `log/devlog.md` (E02-004, E01-016) | Commit session state and claims in-repo (or in a tracker), so collaborators and reviewers can audit; avoid single shared status lines (E07-020) |
| **Provenance trailers** | Trailers on ~48 % of non-merge commits; session ids on few; model-name drift; late "no agent attribution" rule (E07 §0, E03-005, E01-012, E02-011) | Require `Co-Authored-By` + session id + model on every agent commit, enforced by a commit-msg check; decide attribution policy once |
| **Stop-and-ask list** | Closed list: releases, licensing, secrets, destructive git (E02-009) | Add: plugin API changes, persistent index format changes, settings schema migrations, anything that deletes user files |
| **Agent isolation** | Per-agent `CARGO_TARGET_DIR`, file ownership, new module per area, wait-don't-fix (E01-016, E02-003) | Same; plus per-agent corpus caches and a lock on shared fixture regeneration |

IDE-specific gates to add to the playbook's gate list (PROPOSED): incremental consistency; action
fuzz with invariants; refactor-compiles sample; diagnostics-vs-`cargo check` floor; parse round-trip;
format idempotence; replay determinism; latency budgets (enforced); plugin API diff; LSP conformance.

---

## 8. Staged plan (PROPOSED)

Parallelism note: PhotoCraft's only first-week agent count, "8 parallel agents" with "~6–8×
parallelism", is **self-reported** in a planning doc (E01-014, E08-005); later effort figures
(2,000–4,000 agent-hours for ~1,000 PRs) are the developer's derived estimates, not metered
(E08-004), and the project's own estimate rose ~10× within 8 days (E08-005, E08-002). The ranges
below are therefore reasoned from task shape and the gate's capacity, not from PhotoCraft numbers.
The binding constraint is usually review and merge-queue throughput, not agent count (INFERRED from
E03-008, E05-052).

### Phase 0 — Foundations (contracts, gates, oracles)

- **Scope:** workspace and `xtask` (layers, ci, scorecard, corpus, perf); L0–L1 (ids, cancellation, rope, VFS with fault-injecting backend); action registry with schemas; workspace-server skeleton; command log + replay; testkit (fixtures, snapshot+bless, deterministic scheduler); AGENTS.md with invariants and stop-and-ask list; ADRs for all High-tier components; merge queue; trailer check; dedicated perf runner.
- **Parallelism:** low — roughly 1–3 concurrent agent streams under one or two human design owners. Reason: almost every task edits a shared contract; parallel work here produces the "individually green, jointly broken" pattern (E05-052) in its most expensive form.
- **Exit gates (machine-checkable):**
  - `xtask ci` green on main, includes layers, action-schema completeness, action fuzz, fail-on-skip wrapper, `--check` on generated docs.
  - Replay test: recorded sessions replay to byte-identical state, 100 % of the replay corpus.
  - VFS fault-injection suite passes (external modify, rename, permission error, slow FS).
  - Perf runner produces a baseline with variance below a stated threshold over N repeated runs (threshold chosen and recorded, not invented).
  - Merge queue enabled; main CI non-cancellable.

### Phase 1 — Vertical slice for one language (Rust)

- **Scope:** lexer/parser with lossless trees; incremental query engine; name resolution and basic type inference for a subset; diagnostics; highlighting; goto definition; find usages; rename; formatting; one editor view and project panel; LSP adapter.
- **Parallelism:** moderate — roughly 3–8 streams, split by layer (parser / semantics / editor UI / LSP) once the layer APIs are frozen. Reason: layers communicate through the contracts from phase 0, so cross-stream collisions are API-level and caught by the gate.
- **Exit gates:**
  - Parse round-trip and lossless reproduction: 100 % on the medium pinned corpus (pinned crates).
  - Parser accept/reject agrees with `rustc` on the corpus above a floor, floor ratchets.
  - Incremental == from-scratch on fuzzed edit sequences: zero mismatches over a fixed number of seeds per PR, more nightly.
  - Diagnostics vs `cargo check`: precision/recall floors per diagnostic family, ratcheting.
  - Rename: on sampled sites, 100 % "still compiles + tests pass" on the corpus; inverse rename restores source.
  - Latency budgets for keystroke-to-highlight and completion **enforced** on the fixed runner.
  - LSP conformance suite passes; smoke test with at least one external editor client.

### Phase 2 — Fan-out

- **Scope:** inspections, intentions, more refactorings, panels, keymaps, file types, settings, second and third languages.
- **Parallelism:** high — tens of concurrent streams are plausible *if* each task maps to one module and has an oracle-backed acceptance test; cap by merge-queue throughput and human maintainer review capacity for Medium changes. Reason: this phase is shaped like PhotoCraft's menu work (E03-011, E01-015).
- **Exit gates:**
  - Every inspection/intention has: a snapshot test, a "fix compiles" corpus check, an entry in the generated feature matrix citing that test.
  - Scorecard rows cite behavioural tests; no presence-only metric is reported as progress (anti-E07-013).
  - "Settings that do nothing" count tracked and ratcheting down (E07-014 pattern).
  - Mutation score on changed analysis code above a floor.

### Phase 3 — Ecosystem

- **Scope:** plugin API 1.0 and host, DAP/debugger, build-tool integrations, VCS, marketplace, release channels.
- **Parallelism:** mixed — plugin API and debugger core back to low (High tier); integrations and sample plugins high.
- **Exit gates:**
  - API surface diff check enforced; semver classification required for every change.
  - Sample-plugin corpus builds and passes against every PR.
  - DAP conformance tests and recorded-trace differential against an existing adapter.
  - Nightly release dry run green for a stated number of consecutive nights (E05-063 pattern).
  - Nightly large-corpus smoke (open, index, inspect) within budget.

### 8.1 Summary

| Phase | Concurrent agent streams (reasoned range) | Human role | Gate that unlocks next phase |
|---|---|---|---|
| 0 Foundations | ~1–3 | Design owners write ADRs, review every change | Contract tests + replay + VFS fault suite + merge queue live |
| 1 Vertical slice | ~3–8 | Own semantic/query layers; review oracle results | Round-trip, consistency, diagnostics, rename and latency gates green |
| 2 Fan-out | tens, bounded by queue and review capacity | Medium-tier reviews; own High-tier paths; triage oracle disagreements | Feature matrix fully oracle-backed; mutation floor met |
| 3 Ecosystem | mixed | Own plugin API and debugger core | API diff, sample plugins, DAP conformance, release dry runs |

INFERRED: PhotoCraft effectively started in "phase 2" mode within days (E01-014) because its phase 0
and 1 were compressed into a single large initial commit plus a free external oracle; an IDE
should not expect to skip phases 0–1.

---

## 9. Risks and anti-patterns

Each row: a PhotoCraft failure (VERIFIED unless marked) → its IDE analogue (INFERRED) →
countermeasure (PROPOSED).

| # | PhotoCraft failure (evidence) | IDE analogue | Countermeasure |
|---|---|---|---|
| 1 | "625/625 live" while basics were broken; metric "measures wiring, not behaviour" (E07-013, E01-019) | "Supports 400 inspections" / "rename works" counted by provider registration | Feature matrix rows must cite oracle-backed tests; report agreement rates, not counts |
| 2 | 0 of 88 perf budgets enforced; contended baseline from another machine class (E04-051, E05-028) | Typing latency regresses unnoticed; users experience the IDE as slow | Fixed runner, enforced budgets from phase 1, low-noise proxy counters |
| 3 | 57 GPU tests returned early and passed (E07-018, E05-024) | Tests skip when a toolchain/corpus is missing (e.g. no `rustc` on runner, corpus not fetched) and pass | Fail on skip; zero-match = failure; CI asserts the oracle actually ran (print and grep "oracle: rustc x.y.z") |
| 4 | Each-green PRs broke main repeatedly (E05-052); manual integration batches as staging (E07-002) | Two PRs each change a query's invalidation and a dependent cache; both green alone | Merge queue on merged result; consistency tests in the gate |
| 5 | Durability fix broke SMB saves; ~17 days to fix (E07-021) | VFS/watcher changes correct on ext4 break on network drives, WSL, case-insensitive FS; lost edits | Fault-injecting VFS, OS matrix for Tier-2 I/O changes, stop-and-ask for save-path changes |
| 6 | Validated schema and op-transaction history planned, silently not built (E04-003); golden images never built (E04-027) | Core contracts drift during fan-out; schema-free actions make fuzzing and MCP brittle | Contract ADRs with enforcing tests; phase gates block fan-out until they exist |
| 7 | Hand-written docs drifted (README counts, AGENTS.md crate map) (E04-004, E04-006) | Agent guide describes a threading model the code no longer follows | Generate facts; keep invariants as tests; `--check` |
| 8 | Conflict markers committed into status lines; scorecard among most-touched files (E07-020, E03-016) | Shared feature-matrix or settings registry file edited by every PR | Generate central files at merge; one file per entry (registries as directories) |
| 9 | Duplicate rows/constants from parallel landings (E07-019) | Two agents implement the same inspection or action id | Registry uniqueness tests; claim board; "check, then claim" rule (E06-034) |
| 10 | Rules without checks diverged (licence allowlist, rule 15, claim-before-coding) (E02 §4, E02-016) | "Never block the UI thread" written but not checked | Every AGENTS.md invariant links to its check; unchecked rules listed as such |
| 11 | Main CI runs cancelled under high merge rate, hiding red main (E07-004, E05-004) | Same | Non-cancellable main runs |
| 12 | Same-commit regression tests not enforced; many security fixes without tests (E09-G-003) | Bug fixes in analysis without a reproducing fixture | Require a failing-before fixture for every fix (replay log or corpus snippet) |
| 13 | Public "one-shot"/rapid-parity claims vs in-repo "alpha" (E08-013, E08-019) | Announcing language support before oracles agree | Public claims quote the generated scorecard only |
| 14 | Effort estimate revised ~10× upward in 8 days (E08-005, E08-002) | Under-estimating the deep core by assuming PhotoCraft-like breadth throughput | Estimate the core separately; recalibrate from your own merged history |
| 15 | Post-merge human testing still found semantic gaps in well-tested features (E09-H-002) | Refactorings pass corpus samples but mis-handle macros, cfgs, proc-macros | Scheduled human dogfooding on real projects; convert each finding into a named corpus test |

---

## 10. Confidence and gaps

**Strongest parts.** The PhotoCraft mechanisms in §3 and §5.2 are VERIFIED in E04/E05 with
file-level citations; the classification of which mechanisms are domain-neutral follows E04 §11.
The failure modes in §2.2 and §9 are VERIFIED from commit text (E05-052, E07-013, E07-018, E07-021).

**Weakest parts.**
- **Causality.** That PhotoCraft's speed came from the enabling conditions in §2.1 is INFERRED. Other drivers — very large agent budgets, 582 contributors, the founder's prior experience, a community acting as a "distributed token budget" (E08-018, E03-008) — are not separable from architecture with the available evidence.
- **Who designed the core.** The day-1 architecture (registry, layering, headless engine) arrived in one untrailed commit (E01, E04 Open questions). Whether it was agent- or human-designed is unknown, so "agents can design the core" is neither supported nor refuted. This study recommends human ownership on general grounds (§6), which is PROPOSED, not evidenced.
- **Agent counts and effort.** Self-reported (E01-014, E08-005) or derived (E08-004). §8 parallelism ranges are reasoned, not measured.
- **How often dev agents used the control channel/screenshot to self-verify** is unknown (3 commit traces, 1 PR sampled; E04-024). The value of §3 row 5 for agents is therefore plausible, not demonstrated.
- **IDE-side claims are untested.** Oracle costs (compile-per-refactor sample, differential runs against rust-analyzer), latency-runner noise, and the cost of incremental==from-scratch checks on large corpora are estimates of difficulty, not measurements. Differential oracles against other LSP servers inherit their bugs.
- **Review and branch-protection settings** in PhotoCraft were not observable (E05 Open questions), so the risk-tier comparison in §7 rests on a 16-PR WebFetch sample (E05 §0.3, E06 §6).

**What would change the conclusion.**
- Evidence that PhotoCraft agents designed and evolved the core contracts unsupervised without rework would weaken §6's "humans own the deep core".
- A working, cheap semantic oracle for the target language beyond the compiler (e.g. a formal spec with executable semantics) would move more IDE work into the "direct" class.
- If an IDE prototype showed incremental==from-scratch checks too slow for the PR gate, §4's central check would have to move to nightly, increasing the risk in §9 row 4.

**Dependencies on other deliverables.** §7 refers to the playbook (`08-playbook.md`) by topic only;
if the playbook's tiers or gate list differ, §7's IDE-specific additions still apply but the tier
names should be aligned. The E05/E06 PR samples are WebFetch summaries (lower fidelity).

No new upstream evidence was gathered during synthesis; all PhotoCraft claims cite existing
evidence entries. Primary shas are carried only for the §2.2 failure rows; elsewhere they resolve through
the cited entry (`deliverables/01-evidence-ledger.md`).
