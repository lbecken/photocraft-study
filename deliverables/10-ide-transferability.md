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

**Directly transferable (PROPOSED, high confidence):** a headless core with UI only at the top
layer, checked by a dependency-layer linter from day 1 (E04-007, E04-031); one action registry
dispatched by every front-end, with a "UI must dispatch actions" check (E04-012); fuzzing every
registered action (E04-012); the local gate and CI gate as one command (E05 §0.2); generated status
docs with `--check` (E04-050); ratchet floors (E04-042); fail-on-skip CI (E05-024, E07-018);
hash-checked shared agent rules (E02-012); agent-isolation rules (E01-016, E02-003).

**Transfers with adaptation:** the oracle strategy. PhotoCraft's "correct" was mostly *given* by
Photoshop (menu tree, embedded composites, corpora; E04-036, E04-042). An IDE has no single
reference binary, so you must *build* oracles: the compiler, differential LSP servers,
round-trip/idempotence properties, incremental-equals-from-scratch checks, and pinned
snapshot corpora. Also adapt: control channel + screenshot, MCP/CLI, perf budgets (which must be
*enforced*, unlike PhotoCraft's 0 of 88; E04-051), parity checklist (as per-language feature matrices).

**Does not transfer:** "parity with the reference app" as the main progress metric (it measured
wiring: E07-013); breadth-first fan-out on day 1 (an IDE's core is deep and stateful); CPU-vs-GPU
pixel parity as a *core* oracle (only relevant to a custom renderer).

**Three biggest risks:** (1) agents fan out onto an unstable incremental/semantic core and every
feature encodes a different wrong assumption about invalidation, threading or undo; (2) green-but-hollow
checks — feature counts, skip-passing tests, unenforced latency budgets — repeating E07-013,
E07-018, E04-051; (3) parallel PRs that are each green colliding on shared state (indexes,
registries, settings schemas) as in E05-052, worse because IDE coupling is semantic.

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
| Parity metric measured wiring | "625/625 menu items are live … only means each item dispatches *a* command"; 214 shortcut failures in an audit; project re-estimated 55–70 % surface, 20–35 % switchable (E07-013, E01-019) | VERIFIED | Never let "feature exists" be the headline metric; measure behaviour against an oracle. |
| Perf budgets unenforced | 88 scenarios, 0 `enforce = true`; baseline recorded at load ~225 on another machine class (E04-051, E05-028) | VERIFIED | Latency is a core IDE requirement; budgets must gate on a fixed runner. |
| Tests that passed without testing | 57 GPU checks returned early and passed on GPU-less CI; several tests asserted nothing (E07-018, E05-024) | VERIFIED | Fail on skip; require zero-match runs to be BLOCKED; mutation spot-checks. |
| Individually green PRs colliding | Recurring "main red since #X + #Y" fixes; 59 fix-main commits (E05-052, E07 §0) | VERIFIED | Real merge queue from day 1. |
| Save-path regressions | Durability fix correct on local NTFS broke SMB saves; ~17 days to fix (E07-021) | VERIFIED | IDE file I/O (VFS, save, external change) needs environment-diverse fault injection. |
| Planned mechanisms never built | Validated param schema → free-text "JSON-ish" doc string; golden images/`xtask bless` never implemented; op-based history → snapshots (E04-003, E04-027) | VERIFIED | Build the contract-level mechanisms before fan-out; do not let them slide. |
| Doc drift | README/AGENTS.md crate map and counts stale; generated docs stayed accurate (E04-004, E04-006) | VERIFIED | Generate every number-bearing doc. |
| Shared-line conflict hotspots | Conflict markers committed into status lines; scorecard.md 3rd most-touched file (E07-020) | VERIFIED | No "every PR edits this line" conventions. |

INFERRED overall: the conditions in §2.1 are what made a six-week, ~1M-line (E04-004) build
feasible; the weaknesses in §2.2 are exactly the places where no cheap oracle existed (behaviour
vs wiring, timing, real filesystems, cross-PR semantics). An IDE has *more* of the second kind.

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
| 14 | AGENTS.md day 0, hash-checked house rules, stop-and-ask list (E01-003, E02-009, E02-012) | Same | direct | Add IDE-specific invariants (threading, cancellation, VFS ownership) to the guide and back each with a check | Rules without checks diverge (E02-016) |
| 15 | Integration batches (E07-002, E06-021, E06-022) | Real merge queue (serialised CI on the merge result) | adapt | Replace manual batches with automation; keep batches only for large cross-cutting landings | Queue throughput limits; needs fast gate |
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
| **Parsing** (incl. error recovery) | No reference parse tree; recovery behaviour is a design choice | (a) Round-trip: `parse → print → parse` gives identical tree; lossless tree reproduces source byte-for-byte. (b) Differential: accept/reject agrees with `rustc` (or the language's reference parser) on corpora and conformance suites. (c) Snapshot of trees on pinned corpora with ratcheting floor. (d) Fuzz random edits: tree never panics, spans stay in bounds | (a)(b) are strong; (c) needs reviewed blessing; recovery quality has no oracle → snapshot + human review |
| **Name resolution, type inference** | Semantics defined by the compiler, not a file | Differential vs the compiler: for every expression in a corpus, compare inferred types/resolved paths against compiler output (e.g. rustc's save-analysis-like dumps or `cargo check` diagnostics) and against an existing server (rust-analyzer) as a second opinion. Floors on agreement rate per corpus | Two oracles that disagree flag tasks for humans; never auto-accept "matches rust-analyzer" where rust-analyzer is known to be wrong |
| **Diagnostics** | Same | `cargo check --message-format=json` as oracle: IDE diagnostics on a pinned corpus vs compiler diagnostics (precision/recall per code), ratcheting | Strong for compiler-equivalent diagnostics; IDE-only lints need their own snapshot tests |
| **Refactoring safety** | No reference refactorer output | **Refactor → still compiles → tests still pass**: apply each refactoring at sampled sites in corpus projects, run `cargo check` and the project's tests. Plus inverse properties (rename A→B→A = identity; extract/inline round-trip) and "no semantic change" via comparing compiler-resolved references before/after | The best oracle available; cost is high (compile per sample) → sample and rotate by day like PhotoCraft's `Sweep` (E04-027) |
| **Formatting** | Style is a spec | Idempotence `fmt(fmt(x)) == fmt(x)`; differential vs `rustfmt` where you aim for compatibility; parse-equivalence before/after | Strong, cheap |
| **Completion, highlighting, inlay hints** | Ranking/coverage is judgement | Snapshot tests of completion lists/highlight token streams on pinned corpora; "expected item present in top-k" metrics with floors; differential vs LSP servers | Ranking quality stays partly human; keep the metric *behavioural* (top-k hit), not "provider exists" |
| **Incremental computation** | The "correct" incremental result is the from-scratch result | **Index/analysis consistency**: after any edit sequence, incremental state == fresh from-scratch computation (query results, index contents, diagnostics). Fuzz edit sequences. This is the IDE analogue of CPU-vs-GPU parity (E04-037) | The single most important check; must not be skippable (E05-024 lesson) |
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
