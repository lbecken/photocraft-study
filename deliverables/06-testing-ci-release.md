# 06 — Testing, CI and release analysis

Scope: the verification system that let PhotoCraft (`storytold/photocraft`) ship a tagged build about
every 1.6 days while roughly half of its commits carry an AI trailer. What the system is, where it is
strong, and where it only looks strong. Upstream pinned at `main` = `74330157cb` (2026-11-12).
History: 2026-09-30 → 2026-11-12.

Inputs: E05 (primary), E04 (testkit, oracles, architecture checks, scorecard, perf), E07 (red main,
flakes, vacuous tests), E02 (definition of done), E03 (test growth, `data/E03_tests_weekly.csv`,
`data/E03_growth.csv`, `data/E03_releases.csv`), E06 and E09 (review and verification in traced cases).
`deliverables/01c-errata.md` overrides the evidence files where they disagree. The failure taxonomy
(F1–F16) is from `deliverables/07-failures-productivity.md` and is cited, not re-derived. PROPOSED items
are aligned with `deliverables/08-playbook.md` §7–9.

Labels: **VERIFIED** = seen in a primary source and cited. **INFERRED** = reasoned from verified facts
(chain given). **PROPOSED** = our recommendation, never a PhotoCraft practice. A commit without an AI
trailer is "attribution unknown". Web observations are WebFetch summaries (lower fidelity, accessed
2026-11-12).

### Terms used below
- **Gate**: a check whose failure is meant to stop a merge or a release. **Mechanical** gates fail
  without human judgement; **advisory** gates are prose, labels or bot comments.
- **`cargo xtask ci`**: the single Rust program that is both the local and the CI gate
  (`74330157cb:xtask/src/main.rs:267-329`). It runs steps in order and stops at the first failure.
- **Architecture checks**: `cargo xtask layers` (crate dependency layering) and `cargo xtask
  panel-commands` (UI click handlers must dispatch engine command ids, not mutate the document).
- **House rules**: 15 org-wide rules copied into `AGENTS.md:1-20` from the external
  `storytold/craft-contrib` repo, hash-checked by `house-rules.yml` (7d8648dfcb, 2026-11-06).
- **panic_hunt**: an `#[ignore]`d integration test that enumerates every registered command and
  dispatches it with hostile parameters (`crates/engine/tests/panic_hunt.rs`, added bf111b524e).
- **Oracle**: an external judge of correctness, here Photoshop's own merged composite embedded in each
  PSD, or the CPU reference compositor for GPU output.
- **Floor**: a minimum pass count asserted by a test, which may only be raised ("ratchet").
- **Scorecard**: `docs/scorecard.md`, generated from `scorecard/*.toml` and source scans by `cargo xtask
  scorecard`; CI fails if it is stale.
- **lavapipe**: Mesa's software Vulkan driver, used to run GPU tests on GPU-less CI runners.
- **Integration batch**: a maintainer branch that merges many community PRs, repairs them, and lands
  as one merge commit (E07-002, E06-022).
- **Red main**: CI failing on `main` after a merge. **Semantic merge skew**: two PRs green alone, red
  together.

---

## Executive finding

**Finding (INFERRED from §1–§7).** PhotoCraft stays shippable through three things working together:
1. **One fast, local-equals-CI gate** (`cargo xtask ci`) that bundles style, lint-as-policy,
   architecture checks, ~18,000 test functions and a command fuzzer, so any agent can reproduce CI
   before pushing (E05-010).
2. **External definitions of "correct"** that agents cannot argue with: pinned, hashed corpora judged
   against Photoshop's own composites at 2/255, CPU-vs-GPU parity, and floors that only ratchet up
   (E04-036, E04-037, E09-D-002).
3. **Fast forward-repair of main** instead of prevention: 21 traced red-main incidents with a median
   time-to-fix of 68 minutes (07 §A.1 F1), zero reverts on main's first-parent line (E07-001), and
   repair and backout done inside integration batches.

It is **hollow** in four places: merge-time integrity (no merge queue; individually-green PRs collide,
E07-003); review (bots on every later PR, human approval visible on a minority of about 20 sampled
pages, E05-035, E06-041); performance (0 of 102 budget rows enforced, baseline from another machine
class, E05-028); and platform coverage (macOS only on release day, Windows path-selected, E05-006).
Several gates that look real cannot fail at all (§7).

---

## 1. The verification stack

**Finding.** The stack has eleven layers. The fast layers are mechanical and blocking on every PR. The
slow, platform and performance layers are path-selected, nightly, dispatch-only or report-only. Nearly
every layer after day 1 was added in response to a named failure (column "Introduced to stop").

### 1.1 Diagram (fastest/local → slowest/nightly)

```
 local / every PR (Linux)                                    path-selected        nightly / release / manual
 ─────────────────────────────────────────────────────────  ──────────────────   ──────────────────────────
 platforms job: Cargo.lock + git-source policy (10 min)  ─┐  windows (unit,      FreeBSD VM build+test 02:17
 cargo xtask ci (gate job, 100 min cap):                  │   integration legs)  release dry run 02:28 (no macOS)
   fmt → clippy -D warnings (+deny lints)                 │  web build +         perf-nightly macOS 03:23
   → layers → panel-commands → scorecard --check          │   24 MiB wasm gate   Windows ARM64 MSI 04:41
   → nextest (ci profile) → panic_hunt → doctest          │  house-rules (on     fuzz (dispatch only)
   → wasm check → i18n report (never fails)               │   AGENTS.md change)  6 perf comparisons (dispatch)
 + lavapipe re-run of GPU group, fail on skip             │  packaging-lint      release on `release` push
 + git diff --exit-code Cargo.lock                        │  docs (mdBook)       (signed, draft)
 test-without-heif · corpus (pinned, hashed, floors)      │
 SonarCloud (coverage continue-on-error; skipped on forks)│
 CodeRabbit review (advisory)                            ─┘
```
Sources: `74330157cb:.github/workflows/ci.yml:6-12,76-470`, E05 §0.1–0.2, cron lines E05-013.

### 1.2 Layer table

| # | Layer | What it checks | When | Blocking? | Introduced | Introduced to stop (evidence) | Cost notes | Label |
|---|---|---|---|---|---|---|---|---|
| L1 | Local gate = CI gate | `cargo xtask ci`: fmt, clippy `-D warnings`, layers, panel-commands, scorecard `--check`, nextest, panic_hunt, doctest, wasm, i18n report (`xtask/src/main.rs:267-329`) | local before PR; `gate` job on every PR and main push | yes, except i18n | 16941f7198 (day 1, fewer steps); CI runs `xtask ci` via shared `gate.yml` since 9acf9a0cf9/a75a414310 (10-23) | local/CI divergence (INFERRED from "same program" design, E05-010) | 100 min cap (`ci.yml:151-172`); cheap steps first after "a clippy failure (15 s) showed red only 41-48 min into the job" (9660dca263, 10-15) | VERIFIED |
| L2a | fmt | `cargo fmt --all -- --check` | gate | yes | day 1, but "failed on every run because the repo … was never formatted" until f7eb6ea9e7 (10-04) | — | most frequent red-main class in W41 (07 F1) | VERIFIED |
| L2b | clippy as policy | `-D warnings`; `unsafe_code = "forbid"`; deny `cognitive_complexity` (30), `too_many_arguments`, `wildcard_imports`; unwrap/expect/panic test-only; `egui::ComboBox` disallowed (`Cargo.toml:97-105`, `clippy.toml:1-8`) | gate | yes | clippy.toml 50a27e6c74 (10-04, never-crash); complexity deny 604da9d06b (10-27, Sonar campaign) | panics on hostile input (issue #7, #16/#17; E07-009); Sonar S3776 (E05-032) | the 10-27 deny later produced post-merge reds (47d3dcde33, 06650357d8; 07 F9) | VERIFIED |
| L3a | layers | crate dependency table, UI crates only at L6+, unregistered crate = error (`xtask/src/layers.rs`) | gate + Windows integration leg | yes | 16941f7198 (in CI day 1) | architecture drift (design plan, E04-031) | seconds (parses `cargo metadata`) | VERIFIED |
| L3b | panel-commands | lexical scan: click handlers dispatch command ids; shrink-only allowlist, 1 entry at HEAD (`xtask/src/panel_commands.rs:1-28`) | gate | yes | 4165c57f92 (10-11, Claude Opus 5.5 trailer) | AGENTS rule 1 "Everything is a command" being advisory (E05-071) | lexical; "incomplete by its own admission" (`panel_commands.rs:20-24`) | VERIFIED |
| L3c | source policy | `.cargo/config*` has no source replacement/patches; `cargo metadata --locked`; every `git+` dep from `github.com/storytold/` (`ci.yml:93-127`) | `platforms` job, every PR | yes | 6401cfdbe1/8f9ebc3136 (10-17) | supply-chain substitution (no incident named) | <10 min | VERIFIED |
| L3d | house rules | copied rule blocks match `craft-contrib@dde09ea31e` (external repo) by sha256 | on AGENTS.md/CLAUDE.md change | yes (shared workflow, logic not inspected) | 7d8648dfcb (11-06) | drift of agent instructions across repos (E02-012) | trivial | VERIFIED (trigger) / INFERRED (logic) |
| L4 | unit / integration / doc tests | ~18,000 `#[test]`s, one `tests/it/` binary per crate, nextest `ci` profile: `fail-fast = false`, 60 s slow warning, terminate after 10 periods (`.config/nextest.toml:26-29`) | gate | yes | day 1; nextest in CI e22c4ec7ab/1a4167936e (10-15); version pinned 0.9.150 for GHSA-vc25-qg58-w57c (ddf9ca1e2d, 10-26) | Windows tests "took 14 of 37 min" (b9aa935d19); hangs | GPU group capped at 4 threads; no retries, no quarantine (E05-050) | VERIFIED |
| L5 | command fuzzing (`panic_hunt`) | every command in `command_specs()` with adversarial params must not panic | gate (`--run-ignored only`) | yes | harness bf111b524e (10-04); **in CI only from 45afd2e9d7 (10-17)** | "The full-registry fuzz (AGENTS.md Rule 9) is #[ignore]d and no workflow ran it" (45afd2e9d7) | side effect: "printed a blank page on the default printer" → `PHOTOCRAFT_NO_PRINT` (70e182b08f, 10-12) | VERIFIED |
| L6 | control-channel / UI interaction tests | egui_kittest harnesses that drive the app through `control::handle` (32 test files + 71 `*tests*.rs`, E04-023); MCP "agent task" acceptance tests (`crates/automation/tests/it/agent_tasks.rs`, 536a7346fb) | gate (ordinary tests) | yes | day 1–10-01 | — | **no image goldens**: "pixel appearance is reviewed from the saved images" (`docs/development.md:93`); `tests/interactions/*.json` not in CI (E04-025) | VERIFIED |
| L7 | GPU-vs-CPU parity on software Vulkan | 78 parity tests "must match the reference compositor within 2/255" (`crates/gpu/tests/it/parity.rs:1-2`); `scripts/ci-gpu-lavapipe.py` re-runs the nextest `gpu` group on lavapipe, requires "GPU parity backend: Vulkan", fails on authored skip lines | gate command (`ci.yml:172`), Linux only | yes | parity tests ae92ac20bf (09-30); fail-on-skip 2ff8f419cb (11-06) | "57 GPU checks … returned early and passed without comparing anything" (2ff8f419cb) | script has its own unit test run first; "Windows uses WARP; this check does not certify Windows skip coverage" (`docs/development.md:116`) | VERIFIED |
| L8 | corpus / oracle tests with floors | 10 sha256 manifests, 1,044 files (`xtask/*.sha256`); Photoshop composite within 2/255; pass floors that "adjust floors only upwards" (`xtask/src/corpus_pins.rs:9-10`); "a missing corpus fails the tests" (`ci.yml:345`) | `corpus` job, every PR and main (no path filter, `ci.yml:340-341`) | yes | 968baf639e, 15d63afbc7 (10-05) | — (built with the PSD work, E09 Case D) | 30 min cap; LTO dropped: "2.7x faster" (5a2f42c476) | VERIFIED |
| L9 | scorecard freshness | `docs/scorecard.md` regenerated output equals committed file | gate | yes | 0f955e6c82 (10-05) | stale "missing" rows cost agent sessions (984bc5c715) | caused red main once: 192 vs 193 settings (3c44319455) | VERIFIED |
| L10a | CodeRabbit | AI review on every non-Dependabot PR; comments include "Prompt for AI Agents" blocks (`.coderabbit.yaml:1-6`) | every PR from ~10-18 | **no** (#12237 merged with a failed pre-merge check) | 9b9643764f (10-20; first commit mention 10-18) | — | 453 commit messages mention CodeRabbit (E07 §5) | VERIFIED (WebFetch for PR pages) |
| L10b | SonarCloud | coverage via `cargo llvm-cov` (4 shards), quality gate shown on PR | every PR and main; **skipped on fork PRs** | **no** (coverage `continue-on-error: true`; no `sonar.qualitygate.wait`) | 8e518d8169 (10-21) | — | 120 min cap; main runs not cancelled "so coverage is published" (5521968828) | VERIFIED (WebFetch of shared workflow) |
| L10c | Dependabot | cargo + actions, daily, grouped (`.github/dependabot.yml`) | daily | n/a | 9185b64b94 (10-18) | — | no cargo-deny/cargo-audit anywhere (E05-033) | VERIFIED |
| L11a | platform jobs | Windows `unit`/`integration` legs (path-selected or `full-ci` label); web build with 24 MiB per-file wasm gate (path-selected); FreeBSD VM and Windows ARM64 MSI nightly and on `release` push; macOS **only** in `release.yml` | see column | yes when run | Windows split 10-11 (Ivan); web gate d502c5de27 (10-10); platforms to nightly 07174271d5 (10-07), e1421f9fec (10-11); macOS dropped bb3108cfd2 (10-09) | runner cost: "5 macOS slots in total" (bb3108cfd2); "nearly every PR" touched Cargo files (e1421f9fec) | FreeBSD VM "takes one to several hours" (E05 §0.1) | VERIFIED |
| L11b | perf | `cargo xtask perf` vs `perf/budgets.toml` and `perf/baseline.json` | nightly macOS 03:23; `--quick` only in a dispatch-only job (`ci.yml:578-600`) | **cannot fail in practice** (0 enforced; baseline class mismatch) | 0f955e6c82 (10-05) | — | baseline recorded under "load average 224.90" (E04-051) | VERIFIED / INFERRED (cannot fail) |
| L11c | cargo-fuzz | 21 matrix entries in `ci.yml:448-470` vs 14 targets in the tree; 12 `psd` entries name a deleted crate | dispatch only: "Placeholder: manual trigger only" (`ci.yml:446-447`) | n/a | day 1 (7 targets) | — | stale matrix never fails because it never runs (E05-023) | VERIFIED |
| L12 | release dry run | every release build except macOS, nothing signed or published (`release.yml:3-7,37`) | nightly 02:28 | reports | f1b5e7d727 (11-11) | "Breakage that only the release build hits … shows up the next morning instead of on release day, as it did on 11 Nov 2026" | — | VERIFIED |

Discrepancy resolved against the clone: E04-030 lists `perf --quick` as "in CI"; at HEAD it runs only
in `selection-morphology-quick-perf`, which is gated on dispatch inputs (`ci.yml:578-579`). E05-016
is correct.

### 1.3 What the table says (INFERRED)
- **Two speeds, one owner.** Everything that is cheap, deterministic and Linux-runnable is blocking
  per PR. Everything slow (FreeBSD, ARM64, macOS, perf, fuzz) is nightly, dispatch or release-only.
  The trade-offs are written next to the config in runner-minutes (`ci.yml:174-178,190-193,230-241`,
  E05-005). This is the main cost lever, and it is also the source of F3 blind spots (07 §A.1).
- **Policy lives in lints.** House-rule and AGENTS.md prose ("never panic", "UI goes through
  commands", "complexity ≤ 30") became compile-time or gate-time failures (E05-032, E05-071). The
  rules that stayed prose (licence allowlist, "no CI change in feature PRs", "test fails without the
  fix") have no check (E02 §4, E05-070).
- **The volume is real.** Test functions grew 922 → 18,111 between 09-30 and 11-12 (E05-019,
  `git grep` count; E03 counts 915 → 18,014 with a different regex, `data/E03_growth.csv`). 6,459 of
  8,329 non-merge commits (77.5%) touch tests; 80.8% of AI-attributed commits vs 74.4% of the rest
  (`data/E03_tests_weekly.csv`, E03-011). The weekly share never fell below 64.5% (W40) and peaked
  at 85.3% (W41).

---

## 2. Definition of "correct"

**Finding.** PhotoCraft's strongest move is giving agents targets that are external, numeric and
monotone. Where the target was an external artefact (Photoshop composites, CPU reference), it held.
Where the target was an internal count (menu items wired, settings present, tests passing), it was
gamed or wrong at least once, and the project responded by adding a second, behavioural metric rather
than deleting the first.

### 2.1 The targets

| Target | What "pass" means | Where | Ratchet | Label |
|---|---|---|---|---|
| Reference-app composite | PSD's embedded Photoshop composite vs our compositor, `PASS_TOL = 2.0/255.0` | `968baf639e:crates/engine/tests/photoshop_oracles.rs:24`; `crates/io/tests/it/corpus.rs:435` `assert!(pass >= src.pass_floor …)` | floors: MIXED 133→148, PSD_TOOLS 229→249, PHOTOSHOP 126→190 over 20 floor-changing commits, never decreasing (E09-D-002) | VERIFIED |
| Pinned corpora | 1,044 files in 10 sha256 manifests; missing corpus = failure, "never a silent skip" (`968baf639e:docs/development.md:318-322`) | `xtask/src/corpus_pins.rs` | "adjust floors only upwards" (`:9-10`) | VERIFIED |
| CPU oracle vs GPU | 78 parity tests within 2/255; AGENTS calls `compose` "the oracle" (`AGENTS.md:86`) | `crates/gpu/tests/it/parity.rs` | n/a | VERIFIED |
| Menu parity checklist | generated "664 of 664 menu items live"; `FLOOR = 663` (`crates/ui-egui/src/menus/parity.rs:10`, "never lower it") | `docs/parity-checklist.md:5` | FLOOR | VERIFIED |
| Scorecard | 166 items (113 done / 46 partial / 7 missing); "Statuses must be true on main"; never-crash lint coverage 28/28 crates; "Settings that do nothing" count | `scorecard/*.toml`, `docs/scorecard.md` | dead settings 66/129 (10-05) → 8/199 (HEAD) (E07-014) | VERIFIED |
| Perf budgets | p50 within budget; regression > 15% and > 1 ms vs same-machine-class baseline | `perf/budgets.toml:1-28` | "flip it to true in the PR that meets it" (`:6-7`) — none flipped | VERIFIED |
| "Test fails without the fix" | house rule 4 and §5 "Prove it" (`AGENTS.md:9,113`) | prose | none | VERIFIED (rule) |

Contributors report progress in oracle units: "(113 -> 118 oracle passes)" (1d9d92341f), "(seven Lab
oracles pass)" (4c450b3879) (E09-D-003). The oracle count is requirement and acceptance metric at
once. The psd → craft-psd extraction (74330157cb, −25,930 lines) shipped with the floors as the
only stated safety net; the PR said "The full test gate has not been run; CI should validate the
switch" (E05 leads, WebFetch). INFERRED: the floors made that swap reviewable without a human reading
the diff.

### 2.2 Where the target was wrong or gameable

| Case | What happened | Detected by | Response | Label |
|---|---|---|---|---|
| Menu-wiring parity | "625/625 menu items live (100%)" (58653e617b, 10-03, Claude Opus 4.8 trailer, errata #4). Two days later: "that only means each item dispatches *a* command"; "shortcuts that didn't fire … (214 failures in an audit)" (20783fdc70, #182) | first user feedback | honest-parity doc; AGENTS step 0 reads it first (433b84fae7); README still "measures wiring, not behaviour" (`README.md:312`) | VERIFIED (07 F5) |
| Inert settings | "it was decorative" (c89c33c704, 9dc394dfc8); 66 of 129 settings did nothing on 10-05 | scorecard prefs audit | counted as a metric (66 → 8); not a gate | VERIFIED (07 F6) |
| Skip-passing GPU tests | 57 GPU checks on llvmpipe "returned early and passed without comparing anything"; how long is unknown (parity tests exist from 09-30, fix 11-06) | CI-environment audit (2ff8f419cb) | lavapipe re-run that fails on skip (Linux only) | VERIFIED (07 F4) |
| Tests asserting nothing | "The mid-drag test asserted nothing … Verified by mutation" (602344bae0); Windows pipeline test "never reached FXC, the compiler this test exists for" (1a86826ab7); "passed even if nothing was painted (CodeRabbit on #11369)" (c441fd350c); "the Alt+H/Alt+P cases checked nothing" (a79db76e30) | mutation by hand, CodeRabbit, audits | case-by-case fixes; no mechanical rule | VERIFIED (E07-018) |
| Fixes without regression tests | "eight fixes merged without one" (72e11802d4, #8690); #1323 merged with no test (E09-B); 16 of 27 `Finding:` security fixes added no `#[test]` (E09-G-003) | backfill campaign | one-off backfill | VERIFIED |
| Unenforced perf budgets | 0 of 102 rows enforced (14 `[[bench]]` + 88 `[[scenario]]`); box blur "3.7 s / 2.8 s measured" vs 1 s budget kept `enforce = false` (`perf/budgets.toml:647-663`) | this study | none; the convention is honest but static | VERIFIED (07 F11) |
| Self-reported counts | integration PRs report "10,793 tests passed" (#9386), "12,514 of 12,521 passing, with the 7 failures explained" (#13396); egui PR body 11,580 vs PR page 11,592 executions (E09-E-002) | — | none; house rule 7 "Report only what ran" | VERIFIED (WebFetch) |

**Pattern (INFERRED).** External oracles were never found wrong in the evidence; internal counters
were wrong in both directions (over-claim 625/625, under-claim stale "missing" rows, 984bc5c715). A
counter that measures *presence* (menu item dispatches, test exists, test passed) is gameable by an
agent without intent; a counter that measures *agreement with an outside judge* is not.

---

## 3. Gate evolution: cause → gate, and what the economies cost

**Finding.** Gates arrived in two waves. Days 1–6 (09-30 → 10-05) built the *content* gates (lints,
layers, fuzz harness, corpora, scorecard). Days 7–17 (10-07 → 10-17) were about *making CI actually
run and finish*: uncancelled main, cheap-first ordering, nextest, timeouts, and putting already
documented rules into CI. From 10-18 the additions are review bots, static analysis and supply chain,
and the last week adds anti-hollowness checks (fail-on-skip, release dry run). The trigger is almost
always a named incident in the commit body, often an AI-attributed one. E05-073 found no commit that
blames an agent: causes are written as "concurrent landings" or PR pairs.

### 3.1 Cause → gate pairs (VERIFIED unless marked)

| Date | Cause (quoted from the commit) | Gate or change | Commit | Lag |
|---|---|---|---|---|
| 09-30 → 10-04 | "CI's `cargo fmt --all -- --check` has failed on every run because the repo had no rustfmt config and was never formatted" | workspace rustfmt + `.git-blame-ignore-revs` | f7eb6ea9e7 | 4 days of red fmt |
| 10-03 → 10-04 | user crash issue #7 (wgpu `Rgba32Float`); community panics #16/#17 | rule 9, panic_hunt harness, clippy.toml, `forbid(unsafe)`, `catch_unwind` guard, 12-PR sweep | ed0b99964d, bf111b524e, 50a27e6c74, ab3ab92b4a | ~1 day (trigger chain INFERRED, E07-009) |
| 10-05 | "a stale Cargo.lock fails CI instead of the release build" | `--locked` in CI | ad86321738 | — |
| 10-07 | "80 of 83 push runs on main were cancelled, and a formatting break from two PRs that were each green alone (#663 + #700) went unnoticed" | main runs never cancelled; PR CI Linux-only by path | 07174271d5 (#800) | same day |
| 10-09/10 | "Concurrent wgpu instances segfault in libvulkan" | `GPU_LOCK`; nextest `gpu` test group | d8d2df4fba, 3092d3b6f9 | — |
| 10-11 | AGENTS rule 1 "Everything is a command" unchecked | `xtask panel-commands`, shrink-only allowlist | 4165c57f92 | 12 days after rule |
| 10-12 | panic_hunt "printed a blank page on the default printer" | `PHOTOCRAFT_NO_PRINT`, `LPDEST` | 70e182b08f | — |
| 10-12 → 10-15 | 0.8.1 web job: wasm "25,587,059 bytes, over … 24 MiB gate"; gate then "failed unrelated PRs" | wasm split into gzip parts behind a boot crate | d43db3e153, df055f3dcb | 3 days |
| 10-15 | "a clippy failure (15 s) showed red only 41-48 min into the job" | cheap checks before tests | 9660dca263 / 5f9190f8cc | — |
| 10-15 | hangs, one failure per rebuild | nextest `ci` profile, runtime limits on unbounded jobs | e22c4ec7ab, 1a4167936e, b2fafcf68c | — |
| 10-17 | "The full-registry fuzz (AGENTS.md Rule 9) is #[ignore]d and no workflow ran it" | panic_hunt in the CI gate | 45afd2e9d7 | 13 days after rule |
| 10-17 | (no incident named) | git deps only from `storytold` | 6401cfdbe1 | — |
| 10-21 | Sonar S7630 BLOCKER: script injection in the fuzz workflow input | fixed; actions pinned to SHA (S7637) | 5933793982, f4bc90b93f | same day |
| 10-26 | nextest advisory GHSA-vc25-qg58-w57c | `nextest-version = "0.9.150"` | ddf9ca1e2d | — |
| 10-27 | Sonar S3776 cognitive complexity | clippy `cognitive_complexity = "deny"`, threshold 30 | 604da9d06b | — |
| 10-29 | feature PRs growing ci.yml (INFERRED, E05-012) | AGENTS "Don't add or change CI in a feature or fix PR" | 0379569d00 | prose only |
| 10-29 | fail-fast hid later regressions: "a single run exposes remaining regressions" | `fail-fast = false` | 8c8c4b95f5 | reverses e22c4ec7ab |
| 11-06 | "57 GPU checks … passed without comparing anything" | lavapipe re-run, fail on skip | 2ff8f419cb | unknown latency |
| 11-11 | release-day breakage "as it did on 11 Nov 2026" | nightly release dry run | f1b5e7d727 | same day |
| 11-11 | egress visibility (no incident) | Harden-Runner on every job, `egress-policy: audit` | e119384a83 | audit, not block |
| 11-12 | automation GPU tests outside the `gpu` group "segfaulted" on lavapipe | added to the group | 2383ea0a4a | ~6.9 days latent (07 F8) |

Two cases show the **documented-rule → mechanical-gate** lag directly: panic_hunt (13 days) and
panel-commands (rule since day 1, check on day 12). The others show **incident → gate within a day**.
INFERRED: the project's gates are reactive; the guide (AGENTS.md) runs ahead of the checks, and the
check is built when the gap bites.

### 3.2 Cost-control moves and the regressions they caused

| Economy | Evidence | Saving (as written) | What it cost | Label |
|---|---|---|---|---|
| PR CI Linux-only; Windows by path regex or `full-ci` label | 07174271d5; `ci.yml:128-144` | runner slots | Windows-only reds on main: ee3ebfa748 ("Windows CI red since #1882", 10-09), 184c226a76 (10-12), 79a33dae9c ("PR ran Linux only", 11-11) | VERIFIED |
| macOS removed from PR and main CI | bb3108cfd2 (10-09): "5 macOS slots in total… PR CI kept them full" | 5 slots | macOS only tested at release; the dry run also skips it (`release.yml:4-5`) | VERIFIED / INFERRED (release-day exposure) |
| FreeBSD, ARM64 to nightly | 07174271d5, e1421f9fec | hours per PR | FreeBSD's plain `cargo test` was the only harness that exposed a race nextest hid (7091cb6b8c: "failed 15 of 40 runs"); found nightly, not on the PR | VERIFIED |
| Day-rotating sweeps (`testkit::Sweep`, a quarter per UTC day) | `crates/testkit/src/sweep.rs:1-40`; `docs/development.md:67` | ~4× on long sweeps | a case can stay unexercised for up to 3 days after a breaking merge (INFERRED from "every case runs at least once every `parts` days") | VERIFIED / INFERRED |
| Partitioned matrices without dropping cases | 4f6ebb1b6e; `docs/development.md:71-77,82-83` ("No speedup should be claimed from … omitting tests") | wall time | none found — this is the counter-example: cost cut with a no-drop invariant | VERIFIED |
| Caches saved only by main; line-tables debuginfo; corpus without LTO | 5a2f42c476 | "1.9x faster (509 s -> 271 s)"; corpus "2.7x faster" | none found | VERIFIED |
| Windows third runner removed | `ci.yml:174-178`: "saved ~2 min of wall time but cost ~7 runner-minutes and one more Windows slot per PR" | 7 runner-min/PR | slower Windows feedback | VERIFIED |
| fail-fast on (10-15) then off (10-29) | e22c4ec7ab, 8c8c4b95f5 | "a red PR frees its runner early" | extra rebuild cycles per regression; reverted | VERIFIED |
| GPU retries tried, then dropped | 110d58bea9 (branch only, `retries = 2`); 8f58ea4629 "retaining strict test gates"; no first-parent version ever had retries | flake noise | none: flakes root-caused with measured rates instead (E07-007) | VERIFIED |
| Fuzz dispatch-only | `ci.yml:446-447` | 60 min × targets | matrix drifted to 12 deleted `psd` targets with nothing noticing (E05-023) | VERIFIED |
| Sonar skipped on forks (token) | E05-029 | secret safety | ~97% of merge-PR sources are forks (E06/E03 leads), so most community PRs get no Sonar signal (INFERRED) | VERIFIED / INFERRED |

**Finding (INFERRED).** The economies that removed a *platform* (Windows by path, macOS, FreeBSD) each
caused at least one later red main or release-day failure. The economies that kept every case but ran
it more cheaply (partitioning, caches, debuginfo, day rotation) caused none in the evidence. The
documented invariant "every formerly selected case still runs once" is the line between the two.

---

## 4. Review as a gate

**Finding.** Review is not a gate in the mechanical sense. Bot review is ubiquitous from mid-October and
visibly changes code; human approval appears on a minority of sampled PRs; several PRs were merged by
their own author, or by a maintainer, with "No reviews". The written rule is accountability ("A person
is accountable. Whoever runs an agent answers for what it opens", `AGENTS.md:6`), not approval. Who
may merge and how many approvals are required is not documented (08 §9, E02 §6).

### 4.1 Sample (all WebFetch summaries, accessed 2026-11-12)

| Source | PRs | Bot review | Explicit human approval | Merged by |
|---|---|---|---|---|
| E05 §0.3 | #113, #7809, #11641, #12237, #13234, #13414 | CodeRabbit on 5/6 (not #113, 10-05); Sonar shown on #13414 only | 1/6 (#11641, FredApps, "Reviewed integrated head c49c1fd…") | self: #113, #13414; maintainer without approval: #7809 (change request dismissed as stale), #12237, #13234 |
| E06 §6 | #33, #1261, #1335, #1344, #2792, #7848, #9386, #11059, #11062, #12945 | 0/5 early (#33–#2792); 5/5 from 10-19 | 1/10 (#7848, FredApps) | "No reviews" on #33, #1261, #1344, #2792; label `ready to merge` applied and merged by the same maintainer (#11062) |
| E09 | #1421, #9363, #10426, #11441, #8452, #8417 | CodeRabbit on all from 10-19 | #9363 (dylanmtaylor ×2), #8452 (FredApps) | #1421 opened and merged by the operator of the Claude session, "No reviews" |

Totals (INFERRED arithmetic over distinct PRs above, 22 pages): explicit human approval on 4
(#11641, #7848, #9363, #8452);
"No reviews" or no approval visible on at least 12. **Sample size: 22 of about 6,480 PR heads**
(RESEARCH-BRIEF), chosen by hand, not at random. These are WebFetch summaries, which can miss review
threads on long pages (E06 confidence notes).

### 4.2 What review demonstrably did
- **Caught measurement and logic bugs.** CodeRabbit asked for independent input copies, and the box
  blur speed-up was corrected from 1.89× to 1.45× (7082689b38, E09-F-003). CodeRabbit flagged a test
  that "passed even if nothing was painted" (c441fd350c). 311 commits are titled "CodeRabbit review"
  (E07 §10).
- **Was formatted for agents.** CodeRabbit comments carry "Prompt for AI Agents" blocks (E05-030); the
  loop "integrator agent fixes → bot review → agent addresses bot findings" is explicit on #13396
  (E06-043).
- **Agent-on-agent review was claimed.** Integration batch #9386: "two independent agents per PR (a
  reviewer and an attacker)", "each PR's code reverted on the branch, its named tests fail" (E06-022,
  self-reported, not verifiable from git).
- **Human testing found what tests missed.** Artboard follow-up #11441 fixed three problems "that
  skylartaylor found on `main`" after two PRs with many named tests (E09-H-002).

### 4.3 What is documented vs not

| Item | Status | Source |
|---|---|---|
| "main changes through a pull request … Branch protection enforces this" | stated; settings not visible | `AGENTS.md:13`; E02 §4 |
| Required approvals / CODEOWNERS | **not documented**, no CODEOWNERS | 08 §9.2, E02-020 |
| Required status checks | **not observable**; "X of Y checks passed" at merge (#33 "2 of 5", #1421 "4 of 7", #8417 "15 of 21") may count skipped path-selected jobs as not passed, so these do not prove failing checks were overridden | E06 §6, E09-B-002, E09-G-003 |
| CodeRabbit findings block merge | **no**: #12237 merged with a failed "Out of Scope Changes" check | E05-030 |
| Batch protocol: "the latest FredApps review APPROVED at its exact current head" for 108 PRs | documented once, for the 10-29 fork integration | `docs/integration-testing/approved-selection-*.md`, E05-022 |
| "Publication requires separate explicit approval; human review and human merge are required" | stated in one migration plan | `docs/egui-037-migration-plan.md:3` |

**Finding (INFERRED).** Review rigor is a property of the integrator, not of the repository. The
same repo shows unreviewed same-day merges (founder era, 10-04 → 10-11), agent-reviewed batches
(10-23 → 11-06) and per-head human approval receipts (FredApps, 10-29; #11641). Copying the checks
copies none of this; copying the *protocol* requires writing it down as a gate.

---

## 5. Merge-time integrity

**Finding.** The weakest point of the system is between "PR green" and "main green". There is no
merge queue (`ci.yml:6-12` has no `merge_group`; `grep -rln merge_group .github/` is empty, E07-003).
GitHub tests each PR against its own base, so two green PRs can produce a red main. This was the
dominant red-main cause (11 of 21 traced incidents, 07 F1). The project answered with process
(integration batches, a manual "(merge queue)", uncancelled main runs), not with a mechanism.

### 5.1 Collisions that passed every per-PR gate (VERIFIED, E07 §2)
- Compile breaks: "#5344 added the export_presets field … #5616 … lacked the new field, so main stopped
  compiling (E0063)" (351149f0df, TTF 13 h 12 m); "#9781 and #10983 each defined TAG_JPEG_TABLES and
  TAG_PREDICTOR … merged minutes apart, so main stopped compiling (E0428)" (06650357d8).
- Lint combinations: two compliant changes "pushed `prepare` past the clippy complexity limit"
  (06650357d8); "Fix main: clippy after the 11-11 merges" (a3c2f2e299).
- Duplicate catalog rows and tables: 25f211500b (ko.tsv), 29e4039c72 (people.toml), 252a47ef76 (cs).
- Generated doc: scorecard 192 vs 193 settings (3c44319455).

TTF median 68 min, range 3 min – 13 h 12 m, n = 17 (07 §A.1). Commits naming red main by week: W41
16, W42 4, W43–W45 0, W46 11 (E07-005). The W46 spike is 11-11: a large merge wave (189 first-parent
commits that day) on top of the 10-27 complexity deny.

### 5.2 The compensating practices

| Practice | Period | Mechanism | Evidence | Effect |
|---|---|---|---|---|
| Uncancelled main runs | from 10-07 | every main state is verified to the end (`ci.yml:66-68`) | 07174271d5 | makes red main **visible**, not prevented |
| `ci/snapshot-*` branches | 10-07 | branches at exact main commits, 0 ahead | E05-014 | purpose INFERRED: get CI on specific main states while main runs were being cancelled |
| CI-only integration trains `claude/integ-batch-1..11` | 10-08/09 | one CI run over N community PRs; draft PR "CI only (do not merge)"; members then squash-merged one by one | PR #1335 (WebFetch), E06-021 | pre-merge union test, operator INFERRED (BFlat) |
| Integration batches `aiongg/integration-2..10`, `davidmann4/integration-batch-7..20` | 10-18 → 11-06 | merge N PRs + main into a branch, repair, run the gate, land as one merge commit | cece50d513 (#9386, 37 PRs), E06-022 table | union is tested before main; W43–W45 had 0 red-main commits (correlation, INFERRED) |
| Pre-merge reverts inside batches | 10-25, 11-01, 11-03 | back out a failing member on the batch branch | batch-8: reverts of #9455, #9454, #9183, #4573, #1199 (+ fix-up) within 56 min – 6 h of merge (E07 §1.1) | 0 of 23 `^Revert` commits are on main's first-parent line (E07-001) |
| Manual "(merge queue)" | 11-08 → 11-11 | merge main into the PR, re-run gates, then merge: "On main + #10448, so main's gate stays green after the merge" | fda05f7b02; **7 commits on main, 9 across all refs** (errata #2) | manual, one maintainer (David Mann) |
| Forward fix-main PRs | throughout | 59 non-merge commits name a red main, 40 with an AI trailer; dedicated branches such as `claude/fix-main-pl-missing` (db3a77a0b6, author identity Claude) | E07-006 | repair, not prevention |

**INFERRED interpretation.** The batch period is a hand-built merge queue with a backout step. It
worked while one integrator ran it and stopped when merges returned to per-PR merges on 11-07 →
11-11, which is where red main came back. A batch also makes reverts invisible to main's history: the
revert rate at PR granularity is 0/3,475 first-parent commits, but 23 reverts happened in batch
branches (E07-001). Read "zero reverts on main" as "backouts moved upstream of main", not "nothing
needed backing out".

---

## 6. Release pipeline

**Finding.** Releases are cheap because almost all verification happens before them: a tag is a
version bump on an already-green main, built and signed by a shared workflow into a **draft** GitHub
Release that a maintainer publishes by hand (`docs/releasing.md:3-6`). The weak spots are the parts
that only the release build exercises (signing, packaging, riscv64, Flatpak, macOS). Until 11-11
these failed on release day; three `.0` version bumps were never tagged and were followed within hours
by a platform fix and a `.1` tag (new evidence below).

### 6.1 Tag cadence (condensed; UTC dates from `data/E03_releases.csv`)

| Phase | Tags | Dates (UTC) | Cut by (tag-commit author) | On main? | Gap between tags | Notes |
|---|---|---|---|---|---|---|
| Bootstrap | v0.1.0 (= v0.1.1-rc.4), v0.1.1-rc.5, v0.1.1 | 10-01 → 10-03 | Brandon Thomas | yes | 0.8–1.0 d | Linux packaging fix (4eb75d6370) |
| Main-line | v0.2.0 … v0.20.1 (19 tags) | 10-05 → 11-03 | Brandon Thomas, except v0.3.0 (BFlat) and v0.8.2 (author identity "Claude", d43db3e153) | yes | 0.19–3.47 d | untagged bumps: 0.4.x, 0.8.0/0.8.1 (failed builds, INFERRED), 0.11.0, 0.15.0, 0.20.0 |
| Release branch | v0.20.2, v0.21.0, v0.22.0, v0.23.0, v0.23.1 | 11-05 → 11-12 | Dylan M. Taylor (3), FredApps (2) | **no** (on `origin/release`) | 0.29–2.67 d | v0.23.1 = "Merge tested main for v0.23.1" after Flatpak fix eee667f1d9 |

27 tags, 26 distinct tagged commits, 41.4 days, **median gap 1.6 days** (E03-015); the mean over the
26 gaps is 1.59 days (`python3` over `days_since_prev_tag` in `data/E03_releases.csv`). E05 §0.4
dates some tags a day earlier than E03 (local vs UTC committer dates, e.g. v0.23.1 = 11-11 local,
11-12 02:55 UTC); this file uses UTC. Of 29 first-parent version-bump commits to `Cargo.toml` on main,
26 carry a Claude trailer (E05-065). Who *published* each draft is not observable from git.

### 6.2 Model
- **Main-first, then branch.** Documented flow: `cargo xtask version set X.Y.Z` on main through review,
  merge main into `release`, wait 30–45 min for notarization, check job summaries for `::warning::`
  (unsigned artefact), add scorecard deltas, publish (`docs/releasing.md:26-59`, E05-060).
- **Observed in November**: `release-bump-0.23.0` (af98c28ded) and `release-sync-0.23.0`
  (e6abeaba74 → 8a909b2673 "Release: PhotoCraft v0.23.0 on main (#13345)") bump on the release side and
  sync back to main. That reverses the documented order (INFERRED from subjects, E05-065).
- **Permissions**: only `release.yml` has `contents: write` / `packages: write`; every other job is
  read-only (`ci.yml:50-52`, E05-007). Only signing and draft jobs use the `release` environment, so "a
  branch can't create a release" (bce7e54a63, #1220).
- **Release-blocking checks**: packaging-lint (actionlint, shellcheck, desktop-file-validate,
  appstreamcli, WiX fixtures), FreeBSD and Windows ARM64 workflows on `release` pushes (ed1b6f4314,
  10-23; `docs/releasing.md:427-432`).
- **Packaging matrix** (`docs/releasing.md:61-72,377-389`): macOS universal DMG + CLI zip; Windows
  x64/x86 MSI, portable, symbols; Linux x86_64/aarch64 AppImage+zsync, deb, rpm, tar, Flatpak; riscv64
  tarball (QEMU smoke test); FreeBSD tarball; web zip. 15 signing secrets (Apple cert/notarization,
  Windows cert + Azure Trusted Signing, `LINUX_SIGNING_KEY`, `release.yml:43-58`). No Homebrew.
- **Credits** regenerated each release after About showed a 10-10 snapshot (daa9a01955, 11-05).

### 6.3 Known release failures and fixes

| Release | Failure (quoted) | Fix | Moved left? | Source |
|---|---|---|---|---|
| (pre-0.2.0) | stale Cargo.lock would fail the release build | `--locked` in PR CI | yes | ad86321738 |
| 0.8.1 | "riscv64 packaging got --formats deb,rpm,tar … Linux jobs lacked the ALSA headers … Windows signing needed the AZURE_* secrets" | shared-workflow fixes, secret plumbing (3d6050b931) | no | 2db6b7d8f9 |
| 0.8.1 → 0.8.2 | web wasm "25,587,059 bytes, over … 24 MiB gate" | opt-level z, then gzip parts (df055f3dcb) | partly (size gate on PRs since 10-10) | d43db3e153 |
| 0.11.0 → 0.11.1 | (bump cd79a5a9e8 untagged) "Format: build on FreeBSD (rustix has no xattr calls there)" | 8ede07b096, tag the same day | no (FreeBSD nightly) | new evidence |
| 0.15.0 → 0.15.1 | (bump e6d6fb45a4 untagged) "packaging(macos): retry stapling when Apple's ticket lookup drops (#8995)" | 4991f6377e | no (macOS release-only) | new evidence |
| 0.20.0 → 0.20.1 | (bump 24d4f4db9f untagged) "Packaging: run the cross-built CLI's --version check without the malloc re-exec" | eed8bd27d2 | no | new evidence |
| 0.22.x → 0.23.1 | Flatpak update permissions: 6 PRs over 20 days; 0.22.1 patch branch never merged | eee667f1d9 (#13322) | no | 07 F10, E07-026 |
| 11-11 | release-day breakage (riscv64, Flatpak, FreeBSD, packaging) | nightly release dry run | yes, except macOS | f1b5e7d727 |

INFERRED (chain: untagged `.0` bump → same-day platform/packaging commit → `.1` tag): at least three
of the 26 tagged releases needed a platform fix that no PR gate could have caught, because the
platform is not in PR CI. The dry run fixes this for everything except macOS, which is exactly the
0.15.0 case.

---

## 7. Gate scorecard

Ratings: **ME** = mechanical and effective (blocks, and evidence shows it catching or preventing real
failures); **MH** = mechanical but hollow (runs, but cannot fail, or fails on the wrong thing, or
covers less than it claims); **ADV** = advisory; **ABS** = absent.

| Gate | Rating | Evidence |
|---|---|---|
| Local gate = CI gate (`xtask ci`) | ME | same program (E05-010); stop-at-first-failure summary; caught every class in 07 F1 on main |
| fmt | ME | red main 5 times in W41 (07 F1 rows 1–4, 13), each fixed in 3–65 min |
| clippy `-D warnings` + deny lints | ME, with a side effect | never-crash lints on 28/28 crates (`docs/scorecard.md`); complexity deny created post-merge reds (07 F9) |
| layers | ME | in CI since day 1; every internal edge points down at HEAD (E04-002) — evidence of prevention is absence of violations, not a caught incident |
| panel-commands | ME (partial) | allowlist shrank 2 → 1; lexical and admittedly incomplete (`panel_commands.rs:20-24`) |
| git-source / lockfile policy | ME | `git diff --exit-code -- Cargo.lock` + storytold-only sources (E05-008); no incident recorded |
| unit/integration tests | ME | caught collisions and platform breaks on main (07 F1/F3); no retries, flakes root-caused (E07-007) |
| panic_hunt | ME (after 10-17) | 13 days as an unenforced rule first (45afd2e9d7); fuzz finds drove the never-crash sweep (bf111b524e) |
| GPU parity on lavapipe, fail on skip | ME on Linux / MH before 11-06 and on Windows | 57 skip-passing checks (2ff8f419cb); "does not certify Windows skip coverage" |
| corpus + floors | ME | every PR, hashed pins, floors only up, 20 raises (E09-D-002); safety net for psd extraction |
| scorecard `--check` | ME for freshness / MH for truth | catches stale generation (3c44319455); does not check that `status = "done"` is true |
| menu parity FLOOR | MH | measures wiring; "625/625 live" with broken basics (20783fdc70) |
| control-channel UI tests | ME for logic / ABS for pixels | kittest + `control::handle`; no golden images, planned `assert_image_eq`/`xtask bless` never built (E04-027) |
| `tests/interactions` scenarios | ABS (in CI) | "development-only" (E04-025) |
| i18n report | MH | "never fails" by design (`main.rs:300-308`) |
| perf budgets / nightly perf | MH | 0/102 enforced, baseline M4 Pro vs `macos-15`, recorded under load 224 (E05-028, E04-051) |
| cargo-fuzz | MH | dispatch-only, 21 matrix entries vs 14 real targets, 12 deleted `psd` entries (E05-023) |
| nix workflow | MH | triggers on `flake.nix`, which never existed (E05-033) |
| action SHA pinning | MH (partial) | 64 pinned, 7 tag-pinned refs reintroduced after f4bc90b93f (E05-009) |
| Harden-Runner | ADV | `egress-policy: audit` (e119384a83) |
| Windows tests | ME when run / partial coverage | path-selected; 3 Windows-only reds reached main (07 F3) |
| macOS tests | ABS before release | `ci.yml:74-75`; 0.15.0 stapling failure |
| FreeBSD, ARM64 | ME nightly / ABS per PR | race found only by FreeBSD `cargo test` (7091cb6b8c); 0.11.0 FreeBSD build fix |
| release dry run | ME (new, except macOS) | f1b5e7d727; effect after 11-11 not yet observable |
| CodeRabbit | ADV (effective as advice) | real fixes (7082689b38, c441fd350c); does not block (#12237) |
| SonarCloud | ADV | coverage `continue-on-error`; skipped on forks (E05-029) |
| Dependabot | ADV | 2 dependabot commits on main (E05-033) |
| cargo-deny / audit / licence allowlist | ABS | no `deny.toml` in any history; "No `cargo-deny` policy file …" (`book/src/development/dependencies.md:7`) |
| "test fails without the fix" | ADV | "eight fixes merged without one" (72e11802d4); 16/27 security fixes without `#[test]` (E09-G-003) |
| "no CI change in feature PRs" | ADV | no check found (E05-012) |
| human approval | ADV | 4 of 22 sampled pages show one (§4.1) |
| merge queue | ABS (manual substitute) | no `merge_group`; 7 manual "(merge queue)" commits (errata #2) |
| mutation testing | ABS (ad hoc) | "Verified by mutation" in commit text; 24 commits mention mutation (E07 §5) |
| secret scanning / private security channel | ABS | `SECURITY.md:9` (E05-034) |

Count (INFERRED, by each row's first rating): of 34 rows, 15 are ME (several partial), 6 MH, 7 ADV,
6 ABS. The ME rows are all
fast, Linux, deterministic and owned in this repo; the MH rows are concentrated in checks that run
rarely (nightly, dispatch, path triggers) or measure presence instead of behaviour.

---

## 8. Transferable principles and proposed improvements

### 8.1 Principles (INFERRED from the above; each tied to evidence)

1. **Make the local gate and CI gate one command, cheapest step first.** Agents then reproduce CI
   before pushing, and red appears in seconds for lint-class failures. (E05-010; 9660dca263)
2. **Turn every rule an agent must obey into a failing check, and expect a lag if you don't.** The
   two documented rules that became checks late (panic_hunt 13 days, panel-commands 12 days) were
   violated in the meantime; rules that never became checks (licence, "test fails without fix", CI
   edits) are still violated or unverifiable. (E05-071, E07-015, E05-012)
3. **Define correctness by an outside judge, then ratchet.** Reference outputs embedded in real files,
   hashed corpora, CPU-vs-GPU tolerance, floors that only rise. These were never shown gameable;
   presence counters were. (E04-036, E09-D-002, 20783fdc70)
4. **Make tests prove they ran.** Fail on skip lines, require the backend marker, treat zero-match
   filters as BLOCKED. Skip-as-pass hid 57 GPU checks. (2ff8f419cb; `per-pr-regressions.md`, E05-022)
5. **Never cancel main's CI.** Cancelling turned red main invisible for most of a day. (07174271d5)
6. **Cut CI cost by running cases less often, not by dropping platforms.** Partitioning, rotation and
   caching caused no recorded regression; removing Windows/macOS/FreeBSD from PRs caused several.
   (§3.2; 4f6ebb1b6e; ee3ebfa748, 79a33dae9c, 4991f6377e)
7. **Root-cause flakes with measured rates instead of retrying.** Retries were tried and dropped; every
   recorded flake fix states before/after failure rates. (E05-050, E07-007)
8. **Run a second harness somewhere.** nextest process isolation hid a race that plain `cargo test`
   found. (7091cb6b8c, E07-008)
9. **Test the union, not just the PR.** At high merge rates without a queue, skew is the dominant
   red-main cause; integration batches with in-branch backouts coincided with three quiet weeks.
   (E07-003, E07-005, E07-001)
10. **Exercise the release build nightly.** Release-only failures recurred until a dry run existed.
    (f1b5e7d727; §6.3)
11. **Audit for gates that cannot fail.** Zero enforced budgets, a cross-machine baseline, a stale
    fuzz matrix, a path filter on a missing file, a never-failing step. (E05-028, E05-023, E05-033)
12. **Format bot review for agents, but do not mistake it for approval.** CodeRabbit's agent prompts
    drove real fixes; it never blocked. (E05-030, E09-F-003, #12237)

### 8.2 PROPOSED improvements (not PhotoCraft practice; consistent with 08 §7–9)

| # | Proposal | Answers | Shape |
|---|---|---|---|
| P1 | **Real merge queue** (`merge_group` trigger; required checks run on the queued union) | F1 skew, §5 | gate job + corpus on the queue; batch size small enough that bisecting a failure is cheap; keeps the batch "backout" step automatic (08 §9.1 "merge queue" path) |
| P2 | **Fail-on-base test job** | "test fails without the fix" advisory (72e11802d4, E09-G-003) | check out the base, apply only the PR's test files, expect at least one new test to fail; record in the PR (08 §8) |
| P3 | **Mutation testing on the diff** | vacuous tests (E07-018) | `cargo mutants --in-diff` for medium/high-risk PRs; surviving mutants listed in review (08 §8) |
| P4 | **Enforced perf budgets on a fixed runner class** | F11 (0/102 enforced) | record a baseline on the CI runner class (the 10-25 recipe, 9010154943); enforce a handful of budgets first; ratchet like floors |
| P5 | **Required independent review for defined risk classes** | review theatre (§4) | CODEOWNERS + required approvals for persistence, CI, dependencies, security boundaries, release (08 §9.1 high tier); approval = review record, not a label (08 §9.2) |
| P6 | **Gate rollout procedure: warn → measure → deny, checked in the queue** | gate-induced reds (07 F9) | new lint as warning with a count in the scorecard; deny only when count is 0 on main and in the queue |
| P7 | **Nightly fuzz with a generated matrix** | stale dispatch-only fuzz (E05-023) | derive targets from `fuzz/fuzz_targets/*`; fail if the list and the tree disagree (08 §8) |
| P8 | **macOS in the nightly dry run** (unsigned build + smoke test) | 0.15.0 stapling, macOS release-only | one macOS slot nightly, not per PR |
| P9 | **Platform canary on a schedule against main** | Windows-only reds after Linux-only PRs | nightly full Windows legs on main if the path filter skipped them since the last run |
| P10 | **Dependency and licence gate** | licence allowlist stated only (E02 §4) | `cargo deny check licenses bans sources advisories` in the gate (08 §9.1 mapping) |
| P11 | **"Cannot fail" audit as a test** | i18n report, nix triggers, perf | a script that fails if a workflow's path triggers match no file, or a step is unconditional `Ok` without a `report-only` label (08 §7.2 note) |
| P12 | **Pixel goldens for a small UI set** | no visual assertion (E04-027) | the day-1 plan's `assert_image_eq` + `bless` for 20–50 key screens, rendered with the deterministic offscreen `snapshot` example |
| P13 | **One nightly plain `cargo test` job on Linux** | harness diversity was accidental (E07-008) | as in 08 §8 |

---

## Confidence and gaps

- **Strongest**: §1 and §3. Every layer and date comes from the workflow files and commit bodies at the
  pin, re-checked against the clone for the gate steps (`xtask/src/main.rs:267-329`), job conditions
  (`ci.yml:76-470`), and the dry-run trigger (`release.yml:1-12,37`).
- **Weakest**: §4 (review). 22 hand-picked PR pages, WebFetch summaries only. "X of Y checks passed" is
  ambiguous between failed and skipped. Branch protection and required checks are not visible; a
  setting requiring approvals or up-to-date branches would change §4 and §5.
- **Not checkable**: whether nightly FreeBSD, ARM64, perf and dry-run jobs are currently green (no
  Actions access); the logic of shared `craft-common-actions` workflows beyond WebFetch summaries of
  `gate.yml` and `sonarcloud.yml`; who published each release draft; whether the GitHub `macos-15`
  runner ever matches the perf baseline class.
- **Causality**: the link between integration batches and the W43–W45 absence of red-main commits is a
  correlation (07 F1). The claim that three `.0` releases failed on platform builds is INFERRED from
  untagged bumps followed by same-day fixes; no failed run was observed.
- **Evidence disagreements found**:
  - E04-030 lists `perf --quick` as "in CI"; at HEAD it is dispatch-only (`ci.yml:578-600`). E05-016 is right.
  - E05-003's FreeBSD-delegation sha `0cc421d0d5` (unresolved; does not exist in the clone) is wrong (errata #9); the commit is
    **0cc161e2a8** (2026-10-15, Dylan M. Taylor, "ci: delegate FreeBSD workflow to craft-common-actions
    and add nix check").
  - `#[test]` counts: 18,111 (E05-018), 18,030 (E04-004), 18,014 (E03) — three regexes; none re-run.
  - "(merge queue)" commits: 7 on main, 9 all refs (errata #2), not 9 as in E07-003.
  - Tag dates differ by a day between E05 §0.4 and E03 (local vs UTC); UTC used here.
  - E05 §0.3 treats check counts as evidence that required checks gate merges; E06/E09 show merges at
    "2 of 5" and "4 of 7" passed. Both readings fit if skipped jobs are counted as not passed;
    unresolved.
- **What would change the conclusions**: Actions history showing how often main was red and for how
  long (would replace commit-message proxies); branch-protection data; per-PR attribution of the
  breaking PRs in E07 §2.

## New evidence gathered during synthesis

- 0cc161e2a8 (2026-10-15, Dylan M. Taylor): "ci: delegate FreeBSD workflow to craft-common-actions and
  add nix check" (`git log --format='%h %ad %an %s' --date=short -- .github/workflows/freebsd.yml`).
- `74330157cb:.github/workflows/ci.yml:578-600`: `cargo xtask perf --quick` runs only in job
  `selection-morphology-quick-perf`, `if:` on five dispatch inputs; `runs-on: macos-15`.
- `74330157cb:.github/workflows/ci.yml:340-341`: `corpus` job has no path filter (runs on every PR except
  non-`full-ci` label events); `fuzz` job `if: github.event_name == 'workflow_dispatch' && inputs.fuzz`
  (`:447`); `grep -c 'crate:' ci.yml` = 21 matrix entries.
- `74330157cb:xtask/src/main.rs:267-329`: step order fmt, clippy, layers, panel-commands, scorecard,
  test, panic_hunt, doctest, wasm, i18n; i18n comment "it never fails CI".
- Untagged `.0` bumps followed by a platform fix and a `.1` tag (`git log main --grep=<ver>`;
  `git log --first-parent <bump>..<tag>`):
  - cd79a5a9e8 "Release 0.11.0" (10-20) → 8ede07b096 "Format: build on FreeBSD (rustix has no xattr
    calls there)" → v0.11.1 46e538b3a2 (10-20).
  - e6d6fb45a4 "Release 0.15.0" (10-23) → 4991f6377e "packaging(macos): retry stapling when Apple's
    ticket lookup drops (#8995)" → v0.15.1 60c87b9884 (10-23).
  - 24d4f4db9f "Release 0.20.0" (11-02) → eed8bd27d2 "Packaging: run the cross-built CLI's --version
    check without the malloc re-exec" → v0.20.1 327c4cc82e (11-02).
  - v0.11.1, v0.15.1 and v0.20.1 tag commits are by Brandon Thomas with `Co-Authored-By: Claude Opus 5.5`.
- Mean gap between tags: 1.59 days over 26 gaps (`data/E03_releases.csv`, `days_since_prev_tag`).
