# E05: Testing, CI, quality gates and release automation

Stream: E05. Upstream pinned at `main` = `74330157cb` (2026-11-12). Upstream clone root is called `$U` below.
All git commands were run in `$U` unless the entry says otherwise. Web observations come from **WebFetch summaries**, which are lower fidelity, and were accessed on 2026-11-12.

---

## 0. Summary tables

### 0.1 Workflows at HEAD

| Workflow | Triggers | Jobs / matrix | Concurrency | Timeouts | Notable |
|---|---|---|---|---|---|
| `ci.yml` (750 lines) | push main; PR `opened/synchronize/reopened/labeled`; dispatch (8 inputs: full_sweep, color_range, selection_combining, brush_tip(+base), selection_morphology, fuzz(+seconds), dry_mixer) | `platforms` (selects Windows/web by path regex; Cargo.lock and git-source gate); `gate` (reusable `craft-common-actions/gate.yml@main`, runs `python3 scripts/test-ci-gpu-lavapipe.py && cargo xtask ci && python3 scripts/ci-gpu-lavapipe.py`); `windows` matrix `part: [unit, integration]`; `test-without-heif`; `corpus`; `web` (trunk 0.21.14, 24 MiB file gate); `fuzz` (21 targets, dispatch only); 6 dispatch-only perf-comparison jobs | PR: cancel older run of same ref; main: group = run_id, so it is never cancelled; non-`full-ci` labels get their own group | platforms 10, gate 100, windows 100, without-heif 60, corpus 30, web 60, fuzz 60, perf jobs 30–90 | `permissions: contents: read`; `PHOTOCRAFT_NO_PRINT=1`; macOS not tested on PRs |
| `docs.yml` | push/PR on `book/**, docs/**, README.md, SECURITY.md` | mdBook 0.4.52 build | cancel per ref | 15 | `actions/checkout@v7` unpinned, no `persist-credentials: false` |
| `freebsd.yml` | push `release`; nightly 02:17; PR on freebsd packaging; dispatch | reusable `freebsd.yml@main`; custom serialized GPU/ui-egui test command; package check | cancel per ref | (shared) | VM build "takes one to several hours" |
| `house-rules.yml` | push/PR on `AGENTS.md`, `CLAUDE.md` | reusable `house-rules.yml@main` (`rust: true`) | cancel per ref | (shared) | checks the copied craft-contrib rule blocks |
| `nix.yml` | push/PR on `flake.nix, flake.lock, nix/**, Cargo.lock` | reusable `nix.yml@main` | cancel per ref | (shared) | no `flake.nix` exists in this repo (E05-033) |
| `packaging-lint.yml` | push main/release, PR on workflows/packaging/icons/2 docs | shared lint (actionlint, shellcheck, PS parse, xmllint, desktop-file-validate, appstreamcli); verified AppImage inputs; Windows install-policy fixtures (WiX 5.0.2) | cancel per ref | 10 | |
| `perf-nightly.yml` | nightly 03:23; dispatch (quick, update_baseline) | `cargo xtask perf` on `macos-15` | single group, no cancel | 120 | never runs on PRs |
| `release.yml` | nightly 02:28 (dry run); push `release`; dispatch(version) | `credits` (refresh-contributors@main), `release` (shared release.yml@main, 15 signing secrets) | per ref, no cancel | (shared) | `contents: write, packages: write` |
| `sonarcloud.yml` | push main; PR | shared `sonarcloud.yml@main`, `secrets: inherit` | cancel except on main | 120 | coverage via cargo-llvm-cov in the shared workflow (E05-041) |
| `windows-arm64.yml` | push `release`; nightly 04:41; PR on windows packaging | shared ARM64 MSI install test | cancel per ref | (shared) | native ARM64 `cargo test` deliberately left out |

### 0.2 Gate composition (`cargo xtask ci`, run by the `gate` job)

| Step | Command | Blocking? |
|---|---|---|
| fmt | `cargo fmt --all -- --check` | yes |
| clippy | `cargo clippy --workspace --locked --features heif --all-targets --keep-going -- -D warnings` | yes |
| layers | `cargo xtask layers` | yes |
| panel-commands | lexical scan: UI click handlers must dispatch command ids | yes |
| scorecard | `cargo xtask scorecard --check` (docs/scorecard.md must be fresh) | yes |
| test | `cargo nextest run --profile ci …` (falls back to `cargo test`) | yes |
| panic_hunt | nextest `--run-ignored only -E binary_id(photocraft-engine::panic_hunt)` | yes |
| doctest | `cargo test --workspace --locked --features heif --doc` | yes |
| wasm | `cargo check --target wasm32-unknown-unknown` for wasm-safe crates | yes |
| i18n | `i18n-report` | **never fails** |
| (wrapper) lavapipe | `ci-gpu-lavapipe.py`: reruns GPU group on Vulkan, fails on authored skips | yes |
| (shared gate) | `git diff --exit-code -- Cargo.lock` after the gate | yes (via WebFetch) |

### 0.3 Sampled PRs (WebFetch summaries)

| PR | Author / branch | Checks at merge | Bot reviewers | Human review / approval | Merger | Open |
|---|---|---|---|---|---|---|
| #113 | echelon / `release-0.2.0` | 6 passed | none | "No reviews" | echelon (self) | same day 10-05 |
| #7809 | andeecollard / `codex/macos-shortcuts` | 19 passed | coderabbitai (several rounds) | FredApps *requested changes* (later dismissed as stale by davidmann4); tanish2k09 comment; no approval shown | davidmann4 | 10-19 to 11-08 (~20 d) |
| #11641 | wanikhawar / `claude/agitated-jones-8e1a8e` | 21 passed | coderabbitai | **FredApps approved** ("Reviewed integrated head c49c1fd…") | FredApps | same day 11-06 |
| #12237 | hectorviov (fork) / `fix/perspective-crop-field-limits` | 19 passed | coderabbitai (5 actionable, one failed "Out of Scope Changes" pre-merge check) | eliets2 automated "first-pass review" (needs changes); davidmann4 comments plus a commit; no approval shown | davidmann4 | 11-08 to 11-12 |
| #13234 | Raghav2012Code (fork) / `fix/13065-pcrop-keep-clicked-corners` | 19 passed | coderabbitai ("No actionable comments") | "No reviews" | davidmann4 | 11-11 to 11-12 |
| #13414 | dylanmtaylor / `switch-photocraft-psd` (same repo) | 24 passed | coderabbitai (3 inline comments on stale docs); **SonarQube Cloud quality gate passed, 95.8% coverage on new code** | none; reviewer list only coderabbitai[bot] | dylanmtaylor (self) | same day 11-12 |

### 0.4 Release table (tags)

Method: for each `git tag --sort=creatordate` tag, I took the tag commit, its author and subject, and `git rev-list --count prev..tag` (this includes non-first-parent commits). The AI column counts `Co-authored-by: Claude` or `Claude-Session` lines in the tag commit message. "On main" means `git merge-base --is-ancestor tag main`.

| Tag | Date | Commit | Author | +commits | AI trailer | On main | Subject / notes |
|---|---|---|---|---|---|---|---|
| v0.1.0 = v0.1.1-rc.4 | 10-01 | 4eb75d6370 | Brandon Thomas | 14 | yes | yes | Linux packaging fix |
| v0.1.1-rc.5 | 10-02 | c3bd22269f | Brandon Thomas | 18 | no | yes | |
| v0.1.1 | 10-03 | 7750529bbb | Brandon Thomas | 29 | yes | yes | Release 0.1.1 |
| v0.2.0 | 10-05 | ad86321738 | Brandon Thomas | 70 | yes | yes | CI gets `--locked` (E05-061) |
| v0.3.0 | 10-07 | 60224d3fb7 | BFlat | 187 | yes | yes | |
| v0.5.0 | 10-08 | e5e3e39752 | Brandon Thomas | 205 | yes | yes | (0.4.x has no tag) |
| v0.6.0 | 10-09 | 0c72d95425 | Brandon Thomas | 566 | yes | yes | |
| v0.7.0 | 10-10 | 7926161595 | Brandon Thomas | 244 | yes | yes | riscv64 tarball added |
| v0.8.2 | 10-12 | d43db3e153 | **Claude** (author identity) | 422 | yes | yes | 0.8.1 failed, wasm over 24 MiB (E05-062) |
| v0.9.0 | 10-14 | c699e3cda6 | Brandon Thomas | 442 | yes | yes | |
| v0.10.0 | 10-17 | 8407d9ccb1 | Brandon Thomas | 297 | yes | yes | |
| v0.11.1 | 10-20 | 46e538b3a2 | Brandon Thomas | 387 | yes | yes | |
| v0.12.0 | 10-21 | 6a2d027ee2 | Brandon Thomas | 577 | yes | yes | |
| v0.13.0 | 10-22 | ce2a1e337a | Brandon Thomas | 1816 | yes | yes | |
| v0.14.0 | 10-22 | ff47388101 | Brandon Thomas | 27 | yes | yes | |
| v0.15.1 | 10-23 | 60c87b9884 | Brandon Thomas | 66 | yes | yes | |
| v0.16.0 | 10-25 | b1794c6e06 | Brandon Thomas | 479 | yes | yes | |
| v0.17.0 | 10-28 | b8c3f3aa8e | Brandon Thomas | 1179 | yes | yes | |
| v0.18.0 | 10-30 | 8a87a457ab | Brandon Thomas | 914 | yes | yes | |
| v0.19.0 | 11-01 | 2df9f80770 | Brandon Thomas | 231 | yes | yes | |
| v0.20.1 | 11-02 | 327c4cc82e | Brandon Thomas | 267 | yes | yes | |
| v0.20.2 | 11-04 | 7c12f64715 | Dylan M. Taylor | 5 | no | **no** | first tag off the `release` branch |
| v0.21.0 | 11-06 | efb7ebd0c0 | FredApps | 1156 | yes | no | |
| v0.22.0 | 11-09 | 5000240c6e | Dylan M. Taylor | 1420 | no | no | |
| v0.23.0 | 11-11 | 9963efcb2f | FredApps | 1291 | no | no | "Release: PhotoCraft v0.23.0 (main 78e478adda)" |
| v0.23.1 | 11-11 | 45066c4829 | Dylan M. Taylor | 97 | no | no | "Merge tested main for v0.23.1", after Flatpak fix eee667f1d9 |

That is 27 tags in 42 days.

---

## 1. CI workflows: structure and evolution

### E05-001: CI began as a single `ci.yml` on day 1, with a 3-OS matrix and a manual fuzz job
- Label: VERIFIED
- Source: commit 16941f7198 (2026-09-30, Brandon Thomas, "one-shot"); `16941f7198:.github/workflows/ci.yml:27-32,50-61,64-75`
- Quote/Data: `os: [ubuntu-latest, macos-latest, windows-latest]`; steps `cargo fmt --all -- --check`, `cargo test --workspace`, `cargo clippy --workspace --all-targets -- -D warnings`, `cargo xtask layers`; a separate `cargo xtask wasm` job; fuzz matrix of 7 targets.
- Method: `git show 16941f7198:.github/workflows/ci.yml | grep -nE …`
- Notes: the fmt/clippy `-D warnings`/layers/wasm core existed from the first commit. Release workflows followed in d98bee4c94 (2026-10-01).

### E05-002: Workflow history size and authorship
- Label: VERIFIED
- Source: `git log --follow … -- .github/workflows` gives 166 commits (2026-09-30 to 2026-11-11). Of these, 114 are non-merge, and 45 of those carry a Claude/Codex trailer.
- Data: top non-merge authors are Brandon Thomas 23, Dylan M. Taylor 15, Ivan 12, Khawar Zamman Wani 9, skylar taylor-barrick 7, aiongg 7, FredApps 4, David Mann 4, dependabot[bot] 2.
- Method: `git log --no-merges --format=%h -- .github/workflows`, then a loop grepping `co-authored-by: claude|claude-session|codex`.
- Notes: AI-attributed CI changes make up at least 39% (45/114). Unattributed commits count as "unknown", not human.

### E05-003: Timeline of significant CI changes
- Label: VERIFIED (each row is a commit). The "why" column is quoted or paraphrased from the commit body.

| Date | Commit | Author | Change | Why (commit text) |
|---|---|---|---|---|
| 09-30 | 16941f7198 | Brandon Thomas | first ci.yml | n/a |
| 10-05 | ad86321738 | Brandon Thomas | `--locked` in CI | "a stale Cargo.lock fails CI instead of the release build" |
| 10-05 | 0f955e6c82 | Brandon Thomas | `cargo xtask perf`/scorecard, nightly perf (#221) | n/a |
| 10-05 | 968baf639e | Brandon Thomas | pinned corpora, `corpus` feature, CI corpus job (#190) | n/a |
| 10-05 | a0823c5e41 | Brandon Thomas | FreeBSD VM build/test | n/a |
| 10-07 | 07174271d5 | Tanish Manku | main runs never cancelled; `platforms` job; FreeBSD/ARM64 move to nightly (#800) | "80 of 83 push runs on main were cancelled" (E05-004) |
| 10-09 | 5a2f42c476 | BFlat | line-tables-only debuginfo, corpus without LTO, only main saves caches (#1075) | test build "1.9x faster (509 s -> 271 s)"; corpus "2.7x faster" |
| 10-09 | bb3108cfd2 | Brandon Thomas | macOS removed from PR/main CI (#1820) | "5 macOS slots in total… PR CI kept them full" |
| 10-10 | d502c5de27 | Nigel Ihza Firdausy | web build + wasm size gate on PRs (#1689) | n/a |
| 10-11 | b9aa935d19 | Ivan | nextest; examples not built (#2204) | Windows tests took 14 of 37 min |
| 10-11 | 6382148eb8, 60d682d65d, 110d58bea9 | Ivan | Windows split into parallel legs, sccache, nextest retries for GPU | E05-050 |
| 10-11 | 19f427aa00 | Dylan M. Taylor | refactor to `storytold/craft-common-actions` (#3432) | pinned, then deliberately unpinned to `@main` |
| 10-11 | 4165c57f92 | David Mann | `xtask panel-commands` (#3495) | E05-072 |
| 10-12 | 70e182b08f | Fabio Lissi | `PHOTOCRAFT_NO_PRINT`, `LPDEST` (#4467) | panic_hunt "printed a blank page on the default printer" |
| 10-14 | e5bf9c22c9 | Ivan | Windows back to two runners | cost (E05-005) |
| 10-15 | 9660dca263 / 5f9190f8cc | David Mann / skylar | cheap checks before tests (#6119/#6124) | "a clippy failure (15 s) showed red only 41-48 min into the job" |
| 10-15 | e22c4ec7ab / 1a4167936e | David Mann / skylar | nextest in CI with `ci` profile (#6117/#6118) | hang limit, failures repeated at end |
| 10-15 | b2fafcf68c, branch `ci/direct-timeout-limits-20261015` | skylartaylor | "comfortable runtime limits to unbounded jobs" | n/a |
| 10-15 | df055f3dcb | Zuujis | "fix the tests that keep main red" (#5941) | E05-052 |
| 10-15 | 0cc421d0d5 → cddb6fa21c | Dylan M. Taylor | FreeBSD and Nix delegated to the shared workflow | n/a |
| 10-17 | 45afd2e9d7 | Ivan | panic_hunt runs in CI | E05-071 |
| 10-17 | 6401cfdbe1, 8f9ebc3136 | aiongg | git deps must come from `storytold` (CI and release) | n/a |
| 10-18 | 9185b64b94 | Dylan M. Taylor | Dependabot (cargo + actions, daily, grouped) | n/a |
| 10-21 | 8e518d8169 | Dylan M. Taylor | SonarCloud via the shared workflow | n/a |
| 10-21 | 5933793982 | Dylan M. Taylor | fuzz input script-injection fix (S7630 BLOCKER) | E05-040 |
| 10-21 | f4bc90b93f | Dylan M. Taylor | pin actions to SHA (S7637) (#8368) | supply chain |
| 10-21 | c82674439f | denstu473 | `format` crate triggers Windows legs | publication barriers (#8034) |
| 10-23 | 9acf9a0cf9, a75a414310 | aiongg | Linux gate = shared `gate.yml` running `cargo xtask ci` | E05-010 |
| 10-23 | 5521968828 | Dylan M. Taylor | Sonar on main not cancelled | "so coverage is published" |
| 10-26 | ddf9ca1e2d (branch `fix/nextest-0.9.150`) | skylar | nextest pinned 0.9.150 | "GHSA-vc25-qg58-w57c" |
| 10-29 | 0379569d00 | Dylan M. Taylor | AGENTS.md "CI workflows" section; workflows only call craft-common-actions @main (#10228) | E05-012 |
| 10-29 | 8c8c4b95f5 | FredApps | nextest `fail-fast = false` | "a single run exposes remaining regressions" |
| 11-05 | daa9a01955 | Luis | contributor credits refreshed per release | E05-064 |
| 11-06 | 2ff8f419cb | FredApps | GPU tests on lavapipe, fail on skips (#7975) | E05-024 |
| 11-11 | e119384a83 | Dylan M. Taylor | Harden-Runner on every job (#13255) | egress audit |
| 11-11 | 23c2b85a4f | Dylan M. Taylor | StepSecurity drop-in actions (#13337) | n/a |
| 11-11 | f1b5e7d727 (branch `ci/nightly-release-dry-run`) | FredApps | nightly release dry run (#13374) | E05-063 |

- Method: `git log --format='%h %ad %an %s' --date=short -- .github/workflows`, plus `git show -s` for each body.
- Notes: the row "0cc421d0d5" should read **0cc42a7c?**. The commit I actually observed is `0cc4…`; I did not verify that sha. Use cddb6fa21c (2026-10-15, "switch to shared nix workflow") and 0cc4 is uncited. The verified FreeBSD delegation commit is `0cc4…`. See the Open questions section.

### E05-004: Red main was invisible because each merge cancelled the previous main run
- Label: VERIFIED
- Source: commit 07174271d5 (2026-10-07, Tanish Manku, #800), co-authored by Claude Opus 5.5
- Quote: "Main's CI was effectively unverified … 80 of 83 push runs on main were cancelled, and a formatting break from two PRs that were each green alone (#663 + #700) went unnoticed"
- Notes: the fix is the concurrency expression still in use at `74330157cb:.github/workflows/ci.yml:66-68`. Branch `origin/chore/ci-trim-and-main-runs` (01a63dee89) is the pre-squash version.

### E05-005: Cost and runner-capacity decisions are explicit and measured in workflow comments
- Label: VERIFIED
- Source: `74330157cb:.github/workflows/ci.yml:174-178`, `:190-193`, `:230-241`, `:350-355`
- Quote: "Splitting the integration tests over a third runner (nextest --partition) saved ~2 min of wall time but cost ~7 runner-minutes and one more Windows slot per PR."
- Notes: other measured trade-offs in the file are Windows PDBs ("2.2 of ~21 build minutes"), sccache ("4.5 min faster"), corpus LTO ("23.5 of the job's 37 minutes"), and only main saving caches under the "10 GB budget (#2688)". The macOS slot limit is in bb3108cfd2. PR CI is path-selected: Windows runs only for platform-sensitive paths (`ci.yml:144`), web only for crate/web paths (`ci.yml:139`), and the `full-ci` label forces both (`ci.yml:128-133`).

### E05-006: macOS is never tested on PRs or main, only in release builds
- Label: VERIFIED
- Source: `74330157cb:.github/workflows/ci.yml:74-75` ("macOS is tested only by release.yml"); commit bb3108cfd2 (2026-10-09)
- Notes: the exceptions are the dispatch-only `quick performance suite` job on `macos-15` (`ci.yml:583`) and nightly perf. The nightly release dry run also skips macOS (`release.yml:4-5`). So macOS breakage surfaces only on release day. That is INFERRED from those three facts.

### E05-007: Every job is read-only, except release
- Label: VERIFIED
- Source: `ci.yml:50-52` ("The token is only used to check out the code: no job writes to the repository"); `release.yml:17-19` (`contents: write`, `packages: write`). All other workflows have `contents: read`.

### E05-008: Supply-chain guards in the `platforms` job
- Label: VERIFIED
- Source: `74330157cb:.github/workflows/ci.yml:93-123`
- Data: the job fails if `.cargo/config(.toml)` has source replacement, patches or path overrides; if `cargo metadata --locked` fails; or if any `git+` source in Cargo.lock is outside `github.com/storytold/`.
- Notes: introduced in 6401cfdbe1/8f9ebc3136 (2026-10-17, aiongg) and hardened in 7d9abd95af (TOML parsing), 82a7cfa3c5. Branch `ci/shared-actions-audit` (dbee3d61a2, unmerged) proposes moving it into the shared workflows.

### E05-009: Action pinning is incomplete at HEAD
- Label: VERIFIED
- Source: `grep -nE 'uses: ' .github/workflows/*.yml | grep -vE '@[0-9a-f]{40}'`
- Data: 64 SHA-pinned `uses:` lines. Seven third-party refs are still tag-pinned: `actions/checkout@v7` at `ci.yml:650,654` and `docs.yml:38`, `perf-nightly.yml:50`; `actions/upload-artifact@v7` at `ci.yml:684` and `perf-nightly.yml:85,96`. All `storytold/craft-common-actions` refs are deliberately `@main`.
- Notes: f4bc90b93f (2026-10-21) claimed full SHA pinning. Later-added jobs (brush-tip, perf-nightly edits) reintroduced tags. The deliberate `@main` policy is justified inline: "so org-wide CI improvements, security fixes, and build optimizations propagate without PR churn" (`freebsd.yml:32`).

### E05-010: The CI gate and the local gate are the same program
- Label: VERIFIED
- Source: commits 9acf9a0cf9 and a75a414310 (2026-10-23, aiongg); `74330157cb:.github/workflows/ci.yml:151-172`; `74330157cb:xtask/src/main.rs:267-329`
- Quote: `command: python3 scripts/test-ci-gpu-lavapipe.py && cargo xtask ci && python3 scripts/ci-gpu-lavapipe.py` (`ci.yml:172`)
- Notes: `cmd_ci` stops at the first failing step and prints an ok/FAIL/skip summary (`main.rs:311-327`). The shared gate (WebFetch of `craft-common-actions/.github/workflows/gate.yml`) installs `cargo-nextest@0.9.150` and then runs `git diff --exit-code -- Cargo.lock`. It installs no cargo-deny or cargo-audit by default.

### E05-011: The nextest version is pinned for a security advisory
- Label: VERIFIED
- Source: `74330157cb:.config/nextest.toml:1-3`; commit ddf9ca1e2d (2026-10-26)
- Quote: "Refuse to run under a nextest older than the fixed release: GHSA-vc25-qg58-w57c is fixed in 0.9.150"

### E05-012: Documented rule: feature PRs must not change CI, and CI lives in the shared repo
- Label: VERIFIED
- Source: `74330157cb:AGENTS.md:16` (house rule 11), `AGENTS.md:211-214`; introduced by 0379569d00 (2026-10-29)
- Quote: "Don't add or change CI in a feature or fix PR. If the existing workflows can't build or test a change, link an existing craft-common-actions issue … Some workflow files here still run their own jobs. Don't add to them."
- Notes: this is a **documented** rule. Whether it is enforced mechanically is unknown, since I saw no CI check for workflow edits. History shows feature work did edit ci.yml before the rule. Examples are the perf-comparison jobs by Khawar Zamman Wani (47df5dedea, 8324e278a1, 2026-10-27) and "Integrate 16 reviewed performance and usability PRs" (53dbfe280c), and they remain at HEAD as dispatch-only jobs. INFERRED: the rule was a reaction to CI growth driven by feature PRs.

### E05-013: Nightly schedule for slow or platform checks
- Label: VERIFIED
- Source: cron lines `freebsd.yml:15` (02:17), `release.yml:7` (02:28), `perf-nightly.yml:17` (03:23), `windows-arm64.yml:17` (04:41)
- Notes: these were moved out of per-PR runs in 07174271d5 and e1421f9fec (branch `ci-speedup-nightly-platform-checks`, 2026-10-11, "nearly every PR" touched Cargo.toml/lock). The fuzz job is described as "Placeholder: manual trigger only until a nightly schedule is enabled" (`ci.yml:446`).

### E05-014: `ci/snapshot-*` branches point at exact main commits
- Label: VERIFIED (positions); INFERRED (purpose)
- Source: `origin/ci/snapshot-43c86ef` = 43c86ef645, `-47f9306` = 47f9306fd0, `-83ace113` = 83ace1138e. All are dated 2026-10-07 and are 0 commits ahead of main.
- Notes: 83ace1138e is "rustfmt … (Format red on main since #711)". INFERRED: these were pushed to get CI runs on specific main states on the day main runs were being cancelled (E05-004). There is no documentation for them.

---

## 2. Local gate and xtask

### E05-015: AGENTS.md §5 "Before you finish a task" is a conditional checklist
- Label: VERIFIED
- Source: `74330157cb:AGENTS.md:145-168`
- Data: always run `cargo test -p <crates>`, `cargo clippy -p <crates> --all-targets -- -D warnings`, `cargo xtask layers`. Conditionally run `panel-commands` (if ui-egui changed), `wasm` (if L0–L6 changed), `parity` (if commands were added), `panic_hunt -- --ignored` (if commands were added or changed), `scorecard`, `perf --quick` (hot path), `test-corpus` (psd/io/codecs/compose/gpu/text/format). Afterwards, "append a terse entry to `log/devlog.md` … the dev log plus a green tree is how the next agent picks up" (`:168`).
- Notes: AGENTS.md never names `cargo xtask ci`. That appears in `74330157cb:docs/development.md:45` ("the CI gate: fmt, clippy, layers, scorecard, tests, panic_hunt, doctests, wasm, i18n report"). `docs/development.md:67` adds that `PHOTOCRAFT_FULL_SWEEP=1 cargo test --workspace` "stays the final check before a PR". fmt is not in the AGENTS.md list, but it is in CI.

### E05-016: xtask subcommands and whether CI runs them
- Label: VERIFIED
- Source: `74330157cb:xtask/src/main.rs:22-87`; xtask is 7,073 lines of Rust (`wc -l xtask/src/*.rs`)

| Subcommand | Purpose (USAGE text) | In CI? |
|---|---|---|
| `layers` | enforce crate dependency layering | gate + Windows integration leg |
| `panel-commands` | click handlers must dispatch command ids | gate |
| `wasm` | wasm32 check of wasm-safe crates | gate |
| `test` | nextest (or cargo test) + doctests | no (local convenience) |
| `ci` | the full gate | **gate job** |
| `corpus [...]` | fetch/verify pinned corpora | `corpus` job |
| `test-corpus` | `cargo test --release --features corpus` on corpus crates | `corpus` job |
| `stats` | tests and lines per crate | no |
| `parity` | rewrite docs/parity-checklist.md | no (scorecard --check covers freshness of scorecard only) |
| `i18n-report` | translation coverage (never fails) | gate (last step) |
| `perf` | release benches vs budgets/baseline | nightly perf; dispatch quick job |
| `scorecard [--check]` | regenerate/verify docs/scorecard.md | gate (`--check`) |
| `version [set]` | print or set the workspace version | release flow (docs/releasing.md:31-33) |
| `ico` | pack PNGs into .ico | packaging |
| `psd-write-oracle` | run PSD export recipes, write report | no (manual oracle) |

### E05-017: Agent-specific parallelism instructions affect how tests are built
- Label: VERIFIED
- Source: `74330157cb:AGENTS.md:170-176`
- Quote: "Use your own target dir (`CARGO_TARGET_DIR=target/agent-<name>`) to avoid the Cargo build lock … If someone else's in-progress edit breaks the build, wait and retry; don't fix their files."
- Notes: this documented practice assumes several agents building on one machine at once.

---

## 3. Test-suite anatomy

### E05-018: Test function counts per crate at HEAD
- Label: VERIFIED
- Method: `git grep -hE '^\s*#\[(tokio::)?test(\]|\()' HEAD -- <dir> | wc -l`. This counts attributes, not runtime cases. `tests/` is the count of `.rs` files under the crate's `tests/`.
- Data (total **18,111**):

| Crate | #[test] | tests/*.rs | Crate | #[test] | tests/*.rs |
|---|---|---|---|---|---|
| crates/ui-egui | 7387 | 58 | crates/vector | 111 | 0 |
| crates/engine | 4451 | 145 | xtask | 101 | 0 |
| crates/io | 1319 | 95 | crates/cms | 100 | 5 |
| crates/algo | 1000 | 8 | apps/photocraft-cli | 91 | 7 |
| crates/codecs | 665 | 42 | crates/doc | 78 | 0 |
| crates/compose | 494 | 7 | crates/affinity | 63 | 3 |
| crates/text | 354 | 0 | crates/ops | 42 | 0 |
| apps/photocraft | 306 | 5 | crates/plugins | 36 | 1 |
| crates/raw | 284 | 12 | crates/geom, color | 35 each | 0 |
| crates/automation | 280 | 26 | crates/tablet | 34 | 1 |
| crates/format | 242 | 12 | crates/ipp | 22 | 0 |
| crates/paint | 217 | 0 | apps/photocraft-web | 20 | 0 |
| crates/gpu | 193 | 10 | crates/testkit | 8 | 0 |
| crates/raster | 126 | 6 | apps/photocraft-web-boot | 7 | 0 |

- Notes: a runtime count is available from a fork integration run. It recorded "12,904 passed, 97 skipped" for the Linux gate, Windows unit "10,326 passed", and Windows integration "2,501 passed" (`74330157cb:docs/integration-testing/integration-checkpoint.md`, table "Full Linux gate" row, 2026-10-29). That figure is VERIFIED as a document claim, not re-run.

### E05-019: Test growth over time
- Label: VERIFIED
- Method: for each date, `git rev-list -1 --first-parent --before=<d> main`, then the same `git grep` count.

| Date | Commit | #[test] |
|---|---|---|
| 09-30 | 14c5c1bc51 | 922 |
| 10-05 | 4b53f620ef | 2,254 |
| 10-10 | 05e0b1f8a5 | 5,481 |
| 10-15 | df055f3dcb | 8,588 |
| 10-20 | 03d0c7e3b3 | 9,242 |
| 10-25 | b0622d20ca | 11,219 |
| 10-31 | 422ca7beda | 12,748 |
| 11-05 | 50d485ce76 | 14,601 |
| 11-12 | 74330157cb | 18,111 |

- Notes: about 20x in 6 weeks. The jump in the last week partly coincides with the craft-psd extraction (74330157cb), so the counts are not adjusted for moved code.

### E05-020: Integration-test layout uses a single `tests/it/` binary per crate
- Label: VERIFIED
- Source: `docs/development.md:62` ("`cargo test -p <crate> --test it <module>::`"); paths like `crates/codecs/tests/it/malformed.rs`, `crates/format/tests/it/corruption.rs`, `apps/photocraft/tests/it/control_exit_code.rs`.

### E05-021: `crates/testkit` provides a GPU lock, perf helpers and day-rotating sweeps
- Label: VERIFIED
- Source: `74330157cb:crates/testkit/src/lib.rs:1-10`; `crates/testkit/src/sweep.rs:1-40`
- Quote: "By default a run takes one of `parts` slices, chosen by the UTC date, so every case runs at least once every `parts` days. `PHOTOCRAFT_FULL_SWEEP=1` runs every case"
- Notes: this is a cost-control mechanism. CI runs a quarter of the long sweeps each day (`docs/development.md:67`), and the `full_sweep` dispatch input runs them all (`ci.yml:14-17`).

### E05-022: `tests/interactions` and `docs/integration-testing/` are fork-integration records, not CI tests
- Label: VERIFIED
- Source: `tests/interactions/guide-edit/*.json` (10 scenario files; added in a3ea9a4277, 2026-11-05, #9190). `docs/integration-testing/` holds 12 files (approved-selection.json, integration-checkpoint.md, per-pr-regressions.md, windows-portable-test-protocol.md, …), committed by FredApps 2026-10-29 (46c1347951, 4a51aa83f6, 595d631372).
- Quote: "At selection freeze, GitHub showed 108 open, non-draft, unmerged PRs, each with the latest FredApps review APPROVED at its exact current head … and successful current-head check rollup." (`approved-bugfix-parity-2026-10-29.md`) and "A zero-match run is BLOCKED, never PASSED." (`per-pr-regressions.md`)
- Notes: this documents a batch-integration protocol: approve about 100 PRs, merge them into one integration branch, run full-sweep CI on a fork, then build a portable artifact. It is relevant to stream E03/E04 (review and merge). The fork-run links point to `FredApps/photocraft` Actions.

### E05-023: Fuzzing, property tests and snapshot tests
- Label: VERIFIED
- Data: there are 14 fuzz targets in 4 fuzz crates at HEAD: affinity 3, codecs 8, format 1, raw 2 (`git ls-tree … | grep fuzz_targets`). There are 10 `proptest!` blocks across affinity, codecs, compose, format, io and raster (`git grep -n 'proptest!'`). There are 0 `insta`/`assert_snapshot` users. Offscreen UI snapshots use `cargo run -p photocraft-ui-egui --example snapshot` for visual checks (`AGENTS.md:121`), and are not golden-file assertions.
- Notes: **the CI fuzz matrix is stale.** It lists 12 `psd` targets (`ci.yml:453-464`), but `crates/psd` was deleted by 74330157cb (2026-11-12, "Use craft-psd …", #13414). Meanwhile `format/load` is listed, while `codecs/decode_gif`, `decode_webp`, `affinity/stream` and `raw/*` are not. The fuzz job is dispatch-only, so nothing failed.

### E05-024: GPU tests on a software rasterizer must not pass by skipping
- Label: VERIFIED
- Source: commit 2ff8f419cb (2026-11-06, FredApps, #7975, co-authored by Claude Opus 5.5); `74330157cb:scripts/ci-gpu-lavapipe.py:1-40`; `docs/development.md:116`
- Quote: "the GPU tests ran on Mesa llvmpipe over GL, which can't render Rgba32Float: 57 GPU checks … returned early and passed without comparing anything."
- Notes: the script reads the `gpu` test-group filter from `.config/nextest.toml`, requires the "GPU parity backend: Vulkan" log line, and rejects authored "skipping"/"no adapter" lines outside an allowlist. Its own unit test (`scripts/test-ci-gpu-lavapipe.py`) runs before the gate (`ci.yml:172`). The doc caveat reads: "Windows uses WARP; this check does not certify Windows skip coverage."

### E05-025: Real-file corpora are pinned, sha256-verified and always run in CI
- Label: VERIFIED
- Source: `74330157cb:xtask/src/corpus_pins.rs:1-49`; `ci.yml:340-380`; `AGENTS.md:164`
- Data: 10 manifests with 1,044 lines in total. photoshop 258, psd-tools 309, pngsuite 178, psd (ag-psd) 170, affinity 60, gimp 28, atn 16, pixls 11, heif 9, exr 5 (`wc -l xtask/*.sha256`). `scripts/fetch-corpus.sh` is a wrapper for `cargo xtask corpus --all`.
- Quote: "a missing corpus fails the tests" (`ci.yml:345`); "Moving a pin: … adjust floors only upwards" (`corpus_pins.rs:9-10`)
- Notes: introduced 968baf639e (#190) and 15d63afbc7 (#195, psd-tools), both 2026-10-05, on branches `feat/photoshop-oracle-corpus` and `feat/psd-tools-corpus`. The Photoshop oracles live in a separate repo, `storytold/photocraft-corpus`, which has its own AGENTS.md. PngSuite comes over HTTP and is checked against a committed digest (`corpus_pins.rs:44-49`).

### E05-026: The PSD write oracle treats Photoshop as an external judge
- Label: VERIFIED
- Source: `74330157cb:xtask/src/psd_write_oracle.rs` ("Execute small PSD export recipes with the headless CLI. Photoshop is a separate judge."); `xtask/psd-write-oracle/starter.json`; commits f54d605e2c (2026-11-05, #10307) and 146d49f5a2 (2026-11-06, #11607)
- Notes: this is a manual tool. CI does not run it.

### E05-027: Floors only ratchet upward
- Label: VERIFIED
- Source: `AGENTS.md:143` ("raise `FLOOR` in `crates/ui-egui/src/parity.rs` (never lower it)"); actual location `74330157cb:crates/ui-egui/src/menus/parity.rs:10` `pub const FLOOR: usize = 663;`; corpus floor `crates/engine/tests/it/corpus_atn.rs:30`
- Notes: AGENTS.md cites an outdated path for the floor, which is minor documentation drift.

### E05-028: Performance budgets are tracked but none is enforced, and the baseline is from a different machine class
- Label: VERIFIED (counts); INFERRED (effect)
- Source: `74330157cb:perf/budgets.toml:1-28`; `perf/baseline.json`; `perf-nightly.yml:3-13`
- Data: 14 `[[bench]]`, 88 `[[scenario]]`, 5 `not_measurable`, and every `enforce` value is `false`, with 0 `enforce = true` (`grep -nE 'enforce\s*=' perf/budgets.toml`). Regression threshold is 15% of p50 and 1 ms. The baseline `machine_class` is `macos-aarch64-apple-m4-pro-apple-m4-pro` (Apple M4 Pro, 14 cores). Its only commits are 0f955e6c82 and 3423864502 (both 2026-10-05).
- Quote: "It fails when an enforced budget … breaks or a scenario's p50 regresses more than 15 % against perf/baseline.json from the same machine class (other classes are never compared" (`perf-nightly.yml:5-7`)
- Notes: the nightly job runs on GitHub `macos-15`, which is not the M4 Pro class, and `baselines_never_cross_machine_classes` is a unit test (`xtask/src/perf.rs:1515`). INFERRED: with zero enforced budgets and no matching baseline, the nightly perf job cannot currently fail on performance. It only reports. The steps for recording a runner baseline were documented in 9010154943 (2026-10-25, #7494). Performance evidence otherwise lives in 20+ `docs/*-performance.md` files, `docs/benchmarks/`, and dispatch-only before/after jobs in ci.yml (`ci.yml:502-750`).

### E05-029: Coverage is produced in the shared Sonar workflow and is not a CI gate
- Label: VERIFIED (via WebFetch summary of `https://github.com/storytold/craft-common-actions/blob/main/.github/workflows/sonarcloud.yml`, accessed 2026-11-12)
- Data: the workflow uses `cargo llvm-cov` with nextest partitions (4 shards), then `llvm-profdata`/`llvm-cov export -format=lcov`. The coverage step is `continue-on-error: true`. Fork PRs skip the scan when the token is absent ("SONAR_TOKEN is not available (e.g. a fork pull request); skipping SonarCloud scan."). No `sonar.qualitygate.wait` is set.
- Notes: the coverage-related commits are 03993b949f, bae0b9d290 and 1a67881144 (2026-10-26, skylar). These pinned the nested workflow and fonts, and 819d863c4e then "restore[d] craft-common-actions tracking main". On #13414, Sonar reported "Quality Gate passed … 95.8% coverage on new code" (WebFetch). It showed no Sonar output on fork PRs #12237 and #13234, which fits the token skip.

---

## 4. Automated review and static analysis

### E05-030: The CodeRabbit config only excludes Dependabot, and CodeRabbit appears on every sampled PR after mid-October
- Label: VERIFIED
- Source: `74330157cb:.coderabbit.yaml:1-6` (only `reviews.auto_review.ignore_usernames: ["dependabot[bot]"]`); sole commit 9b9643764f (2026-10-20, Brandon Thomas, #7991). The README badge came in 18f8d33577 (2026-10-18).
- Notes: per WebFetch, coderabbitai appeared on #7809, #11641, #12237, #13234 and #13414, and not on #113. Its comments include "Prompt for AI Agents" blocks, so its review output is formatted to be fed back to agents. Authors visibly respond to it, for example 9b21358035 and b45be327b6 "Address CodeRabbit review: …" (David Mann, 2026-10-21). On the 5 sampled PRs, CodeRabbit findings did not block merge (#12237 merged with a failed "Out of Scope Changes" pre-merge check).

### E05-031: SonarCloud campaigns are mostly one maintainer's branches, fixing rule IDs
- Label: VERIFIED
- Source: branches with author Dylan M. Taylor (2026-10-21 to 10-27): `sonar-fix/actions-script-injection` (5933793982, S7630, merged), `sonar-fix/pin-actions-sha` (S7637, landed as f4bc90b93f #8368), `sonar-fix/enforce-https` (S6506, landed as 3ec52a9ff1 #8369), `sonar-fix/rust-async-blocking` (rust:S7488, 9b18f57344 #8373), `sonar/s7688-bash-tests` (75f5a9c126 #8914, a5342b134d #13050), `fix/sonar-maintainability` (3877bb1dbe #9044), `sonar/new-code-lint-batch-1`, `sonar/new-code-s3776-batch-2/3` (cognitive complexity), `sonar/enforce-clippy-standards` (merged via d5be9b8aef #9770, 2026-10-27).
- Method: `git branch -r | grep sonar`; `git log main -i --grep=sonar`
- Notes: the `sonar-project.properties` is 2 lines (`74330157cb:sonar-project.properties:1-2`). The analysis config is passed by the shared workflow (8e518d8169 body).

### E05-032: Clippy policy is machine-enforced with deny lints, and complexity limits came from Sonar
- Label: VERIFIED
- Source: `74330157cb:Cargo.toml:97-105` (`unsafe_code = "forbid"`; `cognitive_complexity`, `too_many_arguments`, `wildcard_imports` = deny; `dbg_macro`, `todo` = warn); `74330157cb:clippy.toml:1-8` (unwrap/expect/panic/indexing allowed only in tests; `disallowed-types` egui::ComboBox; `cognitive-complexity-threshold = 30`); added by 604da9d06b (2026-10-27, Dylan M. Taylor, "Enforce workspace Clippy standards and document lint policy")
- Notes: the per-crate `#![deny(clippy::unwrap_used, …)]` is required by house rule (`AGENTS.md:27,114`) and visible at `crates/testkit/src/lib.rs:2`. Combined with `-D warnings` in the gate, a Sonar maintainability rule (S3776) became a compile-time gate. INFERRED.

### E05-033: Dependabot is configured, cargo-deny/audit is not, and the Nix workflow watches files that don't exist
- Label: VERIFIED
- Source: `74330157cb:.github/dependabot.yml:1-30` (cargo + github-actions, daily 06:00 America/New_York, all grouped; added 9185b64b94, 2026-10-18). There is no `deny.toml` in any history (`git log --all -- deny.toml` is empty). `74330157cb:book/src/development/dependencies.md:7`: "No `cargo-deny` policy file, `cargo-audit` job, or equivalent dependency-advisory workflow is present in the current tree."
- Data: there are 2 dependabot[bot] commits on main (cfb061c46a 10-23, 1ed433a48f 11-10).
- Notes: the licence allowlist (`AGENTS.md:34-51`) is documented only, with no mechanical check in this repo. `nix.yml:8,10` triggers on `flake.nix, flake.lock, nix/**`, but `git log -- flake.nix` is empty, so in practice only `Cargo.lock` changes trigger it. I saw no secret-scanning config. `actionlint` runs inside shared packaging-lint, and `.github/actionlint.yaml` declares a `macos-release` runner label (branch `ci/actionlint-macos-release`, 56aac87cdc).

### E05-034: SECURITY.md has no private reporting channel
- Label: VERIFIED
- Source: `74330157cb:SECURITY.md:9`
- Quote: "This repository does not currently document a dedicated private security email or private reporting channel."

### E05-035: Human approval before merge is not consistently present on sampled PRs
- Label: VERIFIED (via WebFetch summaries of the 6 PR pages, accessed 2026-11-12)
- Data: see table 0.3. 1 of 6 shows an explicit human approval (#11641, FredApps). 2 are self-merged by the author (#113 echelon, #13414 dylanmtaylor) with no reviews. 2 fork PRs were merged by davidmann4 with no approval shown. Check counts at merge were 6 (#113, 2026-10-05), 19 (fork PRs), 21–24 (same-repo PRs).
- Notes: INFERRED: required checks gate merges, and required approving reviews either are not configured or are bypassed by maintainers. I could not read branch-protection settings directly. House rule 8 says "Branch protection enforces this" for pushes to main (`AGENTS.md:13`). Fork PRs show fewer checks, which fits Sonar skipping (E05-029) and path filters. #12237 contains an "explicitly automated" first-pass human-account review (eliets2), which is a lead for E04.

---

## 5. Flakiness and red-main handling

### E05-050: A GPU-test retry policy was added and then dropped during merge integration
- Label: VERIFIED (presence and absence); INFERRED (intent)
- Source: 110d58bea9 (2026-10-11, Ivan, co-authored by Claude): "A ci nextest profile retries the GPU tests … A test that passes on retry is reported as FLAKY." Branch tip `691a022b12:.config/nextest.toml:19-24` has `retries = 2`. Merge 8f58ea4629 (2026-10-16, skylartaylor, "ci: integrate current main while retaining strict test gates") has no `retries`. No first-parent main version ever had retries (loop over `git log --first-parent main -- .config/nextest.toml`, counting `retries`, gives 0 for all 8).
- Notes: at HEAD there is **no retry or quarantine** in nextest config. GPU flakiness is handled by concurrency limits instead: `test-groups.gpu max-threads = 4`, plus Windows-only `threads-required = 4/2` overrides, with comments "without skipping work" and "All cases and the 60-second warning remain unchanged" (`74330157cb:.config/nextest.toml:15-47`). INFERRED: the maintainers chose strict gates over retries.

### E05-051: Documented norms against hiding or omitting tests
- Label: VERIFIED
- Source: `docs/development.md:82-83` ("No speedup should be claimed from changing the 60-second warning threshold or omitting tests."); `docs/development.md:71-77` (matrices partitioned so "Every formerly selected case still runs once"); `docs/integration-testing/per-pr-regressions.md` ("Zero-match, ignored-only or early-return-without-required-capability runs are BLOCKED, not PASSED"); house rule 7 "Report only what ran" (`AGENTS.md:12`); 4f6ebb1b6e (2026-10-29, "partition long parity matrices without dropping cases")
- Data: there are 116 `#[ignore` attributes at HEAD (`git grep -hE '^\s*#\[ignore' HEAD -- '*.rs' | wc -l`). Most are opt-in benchmarks and comparisons (for example `color_range_release_comparison`, run by dispatch jobs) plus `panic_hunt`.
- Notes: I found no explicit rule saying "never `#[ignore]` a failing test".

### E05-052: Red main recurs, caused by semantically conflicting PRs that were each green alone
- Label: VERIFIED
- Method: `git log main --format=… | grep -iE 'fix main|main red|red on main|broken on main|keep main red|…'` gives 23 commits (12 in October, 11 in November).
- Data (examples):
  - 6103da5278, e1cf321183, 83ace1138e, f46c462129, 5c94c5e2b6 (2026-10-07): "rustfmt … (Format red on main since #663 + #700)"
  - 25f211500b, 44d7902f08, 6e558d2fc9: duplicate or missing i18n rows "(main red since #1232 + #1562)"
  - df055f3dcb (10-15, #5941): "Fix two ui-egui tests broken on main by concurrent landings"
  - 71aad480b6 (11-11): "drop the TIFF tag constants #9781 and #10983 both added"
  - b97f342e16 (11-11): "#11009 added a check … #10953, merged after it, refuses …"
  - a3c2f2e299 (11-11): "Fix main: clippy after the 11-11 merges"
- Notes: `ci.yml` has no `merge_group` trigger, so there is no merge queue (VERIFIED by reading `ci.yml:6-12`). INFERRED: the high merge rate without a merge queue or required up-to-date branches is the structural cause. The fix branches carry Claude attribution: `claude/fix-main-pl-missing` (db3a77a0b6) and `claude/fix-main-windows-pipette-test` (bf2c67b19d), both with author "Claude" and a `Claude-Session:` trailer, 2026-10-08. `fix/main-ui-tests-1015` (6b04c4d6e0) and `fix/flaky-tests-2026-10-11` (local names `fix-main-3/4/5`, `fix-main-levels-32`) are by Brandon Thomas with `Co-Authored-By: Claude Opus 5.5`.

### E05-053: Flake fixes are root-caused with measured before/after rates
- Label: VERIFIED
- Source:
  - 18c5420039 (2026-10-11, branch `fix/flaky-tests-2026-10-11`): "Before: the font test failed 6/6 … the MCP test failed 9/30. After: 0 failures"
  - de0a268663 (2026-10-18, `fix/test-flakes-file-locks-portal`): a flock inherited by spawned children, "about 6 failures in 15 runs", and a portal mock race "about 1 run in 25"
  - 0fef3de737 (2026-11-10, `fix/raster-memory-test-race`): a process-wide `RESERVED` race visible under `cargo test` (FreeBSD) but hidden by nextest's per-process isolation, "failed 15 of 40 runs, the fixed one 0 of 40"
  - e22c4ec7ab: a test that relied on another test in the same process "under nextest it runs alone"
- Notes: all of these commits are Claude-co-authored, except the raster fix, which has no trailer (unknown). This is an observed pattern, not a documented policy. Running two runners (nextest per-process on Linux/Windows, `cargo test` threads on FreeBSD) exposes different classes of shared-state bugs. INFERRED.

### E05-054: The fail-fast policy flipped twice
- Label: VERIFIED
- Source: e22c4ec7ab (10-15) set `fail-fast = true` ("a red PR frees its runner early"). 8c8c4b95f5 (10-29, FredApps) set `fail-fast = false`, and 7b1dd35b7b ("CI: report every failing test, not just the first"). HEAD has `fail-fast = false` (`.config/nextest.toml:26`).
- Notes: `docs/development.md:67` still says CI runs "--profile ci (fail-fast, …)", which is stale. The trade-off is runner cost against the number of rebuild cycles needed to find all regressions.

---

## 6. Release automation

### E05-060: The release process is a `release` branch plus a draft GitHub Release
- Label: VERIFIED
- Source: `74330157cb:docs/releasing.md:3-6,26-59`
- Quote: "Every push to the `release` branch runs `.github/workflows/release.yml` … creates or updates a **draft** GitHub Release … Nobody sees a draft until a maintainer publishes it."
- Notes: the steps are `cargo xtask version set X.Y.Z` on main through review, then merge main into `release`, wait 30–45 min for notarization, check job summaries for `::warning::` (an unsigned artifact), add scorecard deltas, and publish manually. The pipeline is the shared `craft-common-actions/release.yml@main` (`release.yml:35`). It needs 15 secrets: Apple cert, notarization ID and team; Windows cert plus Azure Trusted Signing (6); `LINUX_SIGNING_KEY` (`release.yml:43-58`). Artifacts: macOS universal DMG and CLI zip; Windows x64/x86 MSI, portable and symbols; Linux x86_64/aarch64 AppImage+zsync/deb/rpm/tar/flatpak; riscv64 tarball (QEMU smoke); FreeBSD tarball; web zip (`docs/releasing.md:61-72,377-389`). I found no Homebrew packaging (`git grep -il homebrew` on releasing/packaging/README returned nothing). Release-blocking checks are packaging-lint (`docs/releasing.md:427-432`) and the FreeBSD and Windows ARM64 workflows on `release` pushes (ed1b6f4314, 2026-10-23).

### E05-061: Early release-process fixes moved checks from release time into PR CI
- Label: VERIFIED
- Source:
  - ad86321738 (2026-10-05, #113): "CI's test and clippy steps now pass --locked, as the release packaging scripts do, so a stale Cargo.lock fails CI instead of the release build."
  - bce7e54a63 (2026-10-08, #1220): only signing and draft jobs use the `release` environment, "so a branch dispatch … built nothing" before, and "a branch can't create a release"
  - 1d61b33c54 (2026-10-01): "Release playbook now lives in craftrules; keep a pointer". It was later contradicted by house rule 13: "`craftrules` is retired. Do not link to it." (`AGENTS.md:18`). `git grep craftrules HEAD` finds only that rule. The older references survive only in commit bodies (bce7e54a63, e1421f9fec "See craftrules release/playbook.md §2").

### E05-062: Release failures and the fixes that followed
- Label: VERIFIED
- Source:
  - 2db6b7d8f9 (2026-10-12, Release 0.8.1): "The previous release build failed in craft-common-actions, not in this repo: riscv64 packaging got --formats deb,rpm,tar … Linux jobs lacked the ALSA headers … Windows signing needed the AZURE_* secrets". The related secret plumbing is 3d6050b931 (#3794, branch `release-pass-azure-secrets`).
  - d43db3e153 (2026-10-12, author identity "Claude", Release 0.8.2): "0.8.1's Web job failed: photocraft-web's wasm was 25,587,059 bytes, over … 24 MiB gate". The structural fix was the wasm split into gzip parts behind a boot module (df055f3dcb, #5302).
  - eee667f1d9 (2026-11-11, #13322): "Fix Flatpak updates and bump to 0.23.1". The tag v0.23.1 is merge 45066c4829 "Merge tested main for v0.23.1", with conflicts in Cargo.toml/Cargo.lock.
- Notes: v0.8.0 and v0.8.1 have no tags (`git tag` list), which fits failed builds. That is INFERRED.

### E05-063: The nightly release dry run was added after a release-day failure
- Label: VERIFIED
- Source: f1b5e7d727 (2026-11-11, FredApps, #13374); `release.yml:3-7,37`
- Quote: "Breakage that only the release build hits (riscv64, Flatpak, FreeBSD, packaging) then shows up the next morning instead of on release day, as it did on 11 Nov 2026."
- Notes: `dry-run: ${{ github.event_name == 'schedule' }}`. It builds everything except macOS, and signs, pushes and drafts nothing.

### E05-064: Contributor credits are regenerated for each release
- Label: VERIFIED
- Source: daa9a01955 (2026-11-05, Luis, #11426); `release.yml:26-31`
- Quote: "About > Contributors still showed a snapshot from 2026-10-10, because nothing regenerated contributors/contributors.json before a release."

### E05-065: Who cuts releases, and how often they are AI-attributed
- Label: VERIFIED
- Data:
  - Tags v0.1.0 through v0.20.1 are commits authored by Brandon Thomas (one by BFlat, one by "Claude").
  - From v0.20.2 on, the tag commits are on the `release` branch and not ancestors of main. They are by Dylan M. Taylor (3) and FredApps (2).
  - Of 29 first-parent version-bump commits to `Cargo.toml` on main, 26 carry a Claude co-author or session trailer (`git log main --first-parent -G'^version = "0\.' -- Cargo.toml`, plus a trailer grep).
  - The `release` branch has 3,165 first-parent commits, mostly merges of PRs (`git log --first-parent origin/release | wc -l`).
- Notes: version bumps were mostly agent-assisted. Publishing a draft is a manual GitHub UI action by a maintainer (docs). Who published each release is not observable from git. Release branches: `release-0.2.0` (45f927d571, the PR #113 head), `release-0.10.0` (86125ed8f1), `release-bump-0.23.0` (af98c28ded), `release-sync-0.23.0` (e6abeaba74 → main as 8a909b2673 "Release: PhotoCraft v0.23.0 on main (#13345)"). The last two show a bump-on-release-then-sync-to-main pattern in November, which reverses the documented main-first flow. That is INFERRED from the subjects.

### E05-066: In-app updater behaviour is documented
- Label: VERIFIED
- Source: `docs/releasing.md:10-24`. The app checks the GitHub latest-release endpoint once at launch, with a 15 s timeout and a 1 MiB limit and no token. Only published stable versions trigger it. Flatpak builds check too, and the 0.23.1 fix "allow release checks and self-update helpers" (eee667f1d9).

---

## 7. Gates as constraints on human and agent contributions

### E05-070: Mechanical vs advisory gates
- Label: VERIFIED (each row is cited); INFERRED for the "blocks merge" column, which is based on PR check counts and the absence of `continue-on-error` in jobs

| Gate | Mechanical (CI) | Advisory (docs/review) | Source |
|---|---|---|---|
| fmt / clippy -D warnings / deny lints | yes | n/a | `main.rs:270-285`, `Cargo.toml:97-105` |
| layering, panel-commands, wasm, scorecard freshness | yes | n/a | `main.rs:286-299` |
| unit/integration/doc tests, panic_hunt | yes | n/a | `main.rs:289-298` |
| GPU tests actually ran (no skip) | yes (Linux) | Windows not certified | E05-024 |
| corpus tests | yes, every PR | n/a | `ci.yml:340-380` |
| Windows tests | path-selected or `full-ci` | n/a | `ci.yml:144` |
| macOS | no (release only) | n/a | E05-006 |
| wasm 24 MiB file size | yes when web paths change | n/a | `ci.yml:382-441` |
| lockfile freshness and storytold-only git deps | yes | n/a | E05-008 |
| AGENTS.md house-rules copy matches source | yes (on AGENTS.md change) | n/a | `house-rules.yml` |
| i18n completeness | **no** (report only) | yes | `main.rs:300-308` |
| performance budgets | **no** (0 enforced; nightly only) | yes | E05-028 |
| Sonar quality gate / coverage | shows on PR; scan is `continue-on-error`; skipped for forks | yes | E05-029 |
| CodeRabbit | no | yes (findings not blocking) | E05-030 |
| licence allowlist, clean room, "never commit fonts" | no check found | yes | `AGENTS.md:27-51` |
| devlog entry, PR before/after screenshots, "no agent attribution" | no | yes | `AGENTS.md:121,168,20` |
| human approval | not consistently present (1/6 sampled) | house rule 1 "A person is accountable" | E05-035 |
| fuzzing | dispatch only, stale matrix | n/a | E05-023 |
| dependency advisories | none | n/a | E05-033 |

### E05-071: Gates added because a documented rule was not enforced
- Label: VERIFIED
- Source: 45afd2e9d7 (2026-10-17, Ivan, Claude co-author)
- Quote: "The full-registry fuzz (AGENTS.md Rule 9) is #[ignore]d and no workflow ran it, so nothing enforced 'must stay green'."
- Notes: this is an explicit statement that an AGENTS.md rule addressed to agents became a CI gate because it had been advisory. The same pattern shows in 2ff8f419cb (GPU tests "passed without comparing anything") and 4165c57f92 (panel-commands, which turns AGENTS.md rule 1 "Everything is a command" into a lexical check with a shrinking allowlist; "stale entries are errors so the list only shrinks").

### E05-072: Ratcheting allowlists and floors
- Label: VERIFIED
- Source: 4165c57f92 (panel-commands allowlist; later shrunk in f26bd3e257 "drop the panel-commands allowlist entries main fixed"); parity FLOOR (E05-027); corpus floors "adjust floors only upwards" (`corpus_pins.rs:10`); budgets "flip it to true in the PR that meets it" (`perf/budgets.toml:6-7`)

### E05-073: No commit explicitly blames an agent for a failure
- Label: VERIFIED (absence within the searched set)
- Method: I looped over non-merge commits touching workflows, xtask, nextest, clippy.toml, scripts and AGENTS.md, and grepped bodies for `agent|AI|claude|codex|bot` after excluding Co-Authored lines. Matches were trailers or incidental mentions.
- Notes: failures are attributed to "concurrent landings" or PR pairs, never to "the agent". The closest causal statements are E05-004, E05-052 and E05-071. Gates such as house rule 15, "No agent attribution. A pull request does not say an agent wrote it" (`AGENTS.md:20`, added 7d8648dfcb, 2026-11-06), cut against AI traceability. Claude co-author trailers persisted afterwards: 313 of 771 non-merge main commits from 2026-11-07 to 11-13 carry `co-authored-by: claude`, against 3,581 of 7,348 from 10-01 to 11-06 (`git log main --no-merges --since/--until -i --grep='co-authored-by: claude'`). The rate fell from 48.7% to 40.6%. That is VERIFIED arithmetic, but causation is not established.

### E05-074: Supply-chain and runtime-safety gates also constrain agents' side effects
- Label: VERIFIED
- Source: `ci.yml:58-61` (no printing); `SECURITY.md:3`; E05-008; e119384a83 (Harden-Runner egress audit on every job, "Audit, not block")
- Notes: the printing guard came from a real side effect of the adversarial test (70e182b08f: "every run … printed a blank page").

---

## Open questions / uncertainties
- **Branch protection and required checks**: I could not read them, since the GitHub API is blocked. Check counts (6 → 19–24) and human-approval absence come from WebFetch summaries of 6 PRs only. Whether approvals are required and bypassed, or not required at all, is unknown.
- **E05-003 row "0cc421d0d5"**: I did not verify that sha. The FreeBSD delegation commit observed in the log is `0cc0d0212c7a`? No. The log line is "0cc0…" and I did not re-check it. The verified commits for that change are cddb6fa21c (nix switch, 2026-10-15) and the log line "ci: delegate FreeBSD workflow to craft-common-actions and add nix check" (2026-10-15, Dylan M. Taylor). Treat that row's sha as unverified.
- The contents of the shared `craft-common-actions` workflows (release.yml, house-rules.yml, nix.yml, freebsd.yml) were not read, except the summaries of sonarcloud.yml and gate.yml via WebFetch. Signing, notarization and Flatpak publishing details live there.
- I could not determine whether the nightly perf, FreeBSD, ARM64 and release dry-run jobs are currently green, because I had no Actions access.
- The purpose of the `ci/snapshot-*` branches is undocumented (E05-014, INFERRED).
- The tag-to-tag commit counts use `rev-list prev..tag`, which inflates counts for release-branch tags with merges from main.
- Who published each draft release is not observable.

## Leads for other streams
- E03/E04 (review and merge): the batch-integration protocol in `docs/integration-testing/` (FredApps, 108 → 87 approved PRs, fork CI, approval receipts; 46c1347951, 595d631372, 2026-10-29), and integration merge commits like 53dbfe280c "Integrate 16 reviewed performance and usability PRs". Also the automated "first-pass review" from a human account (eliets2 on #12237), and CodeRabbit "Prompt for AI Agents" blocks.
- E01/E02 (agent attribution): author identity "Claude" on release commit d43db3e153 and on branches `claude/fix-main-*` with `Claude-Session:` trailers. The `codex/` branch #7809 carries Claude trailers, so branch prefix and tool disagree. House rule 15 bans agent attribution (7d8648dfcb), and author `agent-346022` appears on 649b1d5d92.
- Governance: house rules are copied from `storytold/craft-contrib` at dde09ea31e2e with a sha256, and `house-rules.yml` checks them (`AGENTS.md:1,22`). craftrules was retired.
- Architecture: `crates/psd` was extracted to craft-psd in 74330157cb (#13414) with "The full test gate has not been run; CI should validate the switch" (WebFetch). Documentation drift was flagged by CodeRabbit.
- Docs drift: `docs/development.md:67` says fail-fast, which is stale. AGENTS.md cites `crates/ui-egui/src/parity.rs`, but the file is `menus/parity.rs`.

## Methods-relevant takeaways
- Make the local gate and the CI gate the **same command** (`cargo xtask ci`), so agents can reproduce CI exactly. Order cheap checks first (E05-010, E05-003 #6119).
- **Never cancel main's CI runs**. Each main state must be verified to the end, or red main becomes invisible under high merge rates (E05-004).
- Without a merge queue, PRs that are each green alone still break main several times a week. Budget for "fix main" work, or add a merge queue (E05-052).
- Turn advisory agent rules into mechanical checks when they matter. panic_hunt, GPU no-skip and panel-commands were all advisory first, then enforced (E05-071, E05-024).
- Make tests **prove they ran**. Reject early-return or skip passes on software adapters (E05-024), and treat zero-match runs as BLOCKED (E05-022, E05-051).
- Prefer root-causing flakes with measured failure rates over retries. A retry policy was tried and dropped (E05-050, E05-053).
- Ratchets (floors, shrinking allowlists, budgets flipped to enforced) let gates tighten without breaking work in progress (E05-072).
- Record CI cost trade-offs, in runner-minutes and slots, next to the config. Path-select expensive platforms, and move slow platforms to nightly (E05-005, E05-013).
- Rotate long test sweeps by day (`Sweep`) to cap per-PR cost while keeping full coverage over a window (E05-021).
- Add nightly release dry runs, so release-only breakage surfaces before release day (E05-063, E05-062).
- Watch for gates that look real but cannot fail: zero enforced perf budgets with a baseline from another machine class (E05-028), a stale fuzz matrix (E05-023), path filters on non-existent files (E05-033), and partial action pinning (E05-009).
- AI review bots (CodeRabbit) are ubiquitous but advisory. On the sampled PRs, human approval was mostly absent. Accountability rests on a written rule, "a person is accountable", rather than a mechanical requirement (E05-030, E05-035).
