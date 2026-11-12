# E07 — Failures, corrections, and quality campaigns

Stream E07. Upstream clone pinned at `main` = `74330157cb601573ae4523a95bb9132822fc3918` (2026-11-12).
`$U` = upstream clone in the scratchpad; `$W` = `scratchpad/work/E07/`. All git commands were run in `$U`.
People named by public commit name or handle. Model names (e.g. "Claude Opus 5.5", "Claude Fable 5.1")
are copied from commit trailers as data. They are not verified model identities.

Cross-references, so this file does not repeat them: E05-004/E05-052 (red main), E05-053 (flake
root-causing), E05-024 (GPU tests that pass by skipping), E05-031/032 (Sonar and clippy), E02-006
(never-crash rules), and E02 revision table (AGENTS.md rule dates). Weekly corrective counts:
`data/E03_corrective_weekly.csv`.

---

## 0. Summary of headline numbers (all VERIFIED; commands given)

| Metric | Value | Command |
|---|---|---|
| Commits on main (all) / first-parent | 12,396 / 3,475 | `git log main --format=%H \| wc -l`; `git log --first-parent main --format=%H \| wc -l` |
| Non-merge commits on main | 8,329 | `git log main --no-merges --format=%h \| wc -l` |
| Non-merge commits with Claude/Codex trailer or `Claude-Session:` | 4,005 (48.1%) | `git log main --no-merges -i -E --grep='co-authored-by: (claude\|codex\|.*noreply@anthropic)\|claude-session:'` |
| Commits on main whose subject starts `Revert` | 23 (0.19% of 12,396) | `git log main -i -E --grep='^revert' --format=%h \| wc -l` |
| Of those, on the first-parent line of main | **0** | per-sha `git rev-list --first-parent main \| grep -c` |
| `Revert` commits on refs not in main (branches + PR heads) | 21 | `git log --all --not main -i -E --grep='^revert'` |
| Non-merge commits naming a red/broken main ("Fix main", "red since", "fails on main", …) | 59 (40 with an AI trailer); some are cherry-picked duplicates | regex in §2, `$W/mainfix.txt` |
| `Finding:` trailers (security), main / all refs | 27 / 52, all by Dylan M. Taylor | `git log main --grep='^Finding:'` |
| "Settings that do nothing" (scorecard prefs audit) | 66 of 129 (2026-10-05) → 8 of 199 (HEAD) | `git show <sha>:docs/scorecard.md \| grep -oE 'Settings that do nothing: [0-9]+ of [0-9]+'` |
| Integration-batch merges on first-parent main | 27 subjects contain "integration" (≈22 are batch branches) | `git log --first-parent main --format=%s \| grep -ic integration` |

---

## 1. Reverts

### 1.1 Catalogue (all `^Revert` commits reachable from main)

Landing PR = first first-parent commit of main that contains the revert, found by bisection
(`$W/landed.sh`: binary search over `git rev-list --first-parent --reverse main` with
`git merge-base --is-ancestor`). Δt = revert author date − original author date. Trailer = AI trailer on
the **original** commit. "—" = no trailer, so attribution is unknown.

| Revert sha | Date | Reverted (orig sha, author, trailer) | Δt | Stated reason | Landed via / what replaced it |
|---|---|---|---|---|---|
| 0134d2dc70 | 10-25 | ddb92be1fa "Merge PR #9455 raw band-by-band develop" (David Mann; Opus 5.5 1M) | 3h34 | none in message | integration-batch-8 (#9386, cece50d513). #9455 never reached main as its own PR (no `#9455` subject on first-parent) |
| 92f592684c | 10-25 | f12be92413 "Merge PR #9454 develop_half" (David Mann; Opus 5.5 1M) | 2h45 | none | batch-8. Not landed separately |
| 02074c9a87 | 10-25 | 3c1f33d73e "Merge PR #9183 .cube 1D shaper" (David Mann; Opus 5.5 1M) | 2h30 | none | batch-8 |
| c01dc04b5f | 10-25 | acd7e07252 "Merge PR #4573 Animation Effects" (David Mann; —) | 6h06 | followed by ac7de75007 "scorecard regenerated without #4573" | batch-8 |
| bb39b4a8dd + 6ab5c07751 | 10-25 | 5f2a7b9903 "Merge PR #1199 optional local models" + e8894aa9f9 integration fix-up (David Mann; Opus 5.5) | 56 min | none. Original body notes a Cargo.lock downgrade of ureq 3.5.0→3.4.2 | batch-8 |
| 459a25bd95 | 10-18 | f57bb1f3b1 "perf(gpu): batch resident overlap copies" (Elvis33LE; —) | ~2.6 d | none | aiongg integration-10 (#8355, ba40dffb25) |
| 25f21db893 | 11-03 | 89ed4cb284 "Stream native PSD and EXR imports…" (vistaero; —) | ~24 d | "so the GPU viewport streaming lands standalone. The import work is rescoped separately in #5331" | #5332 (fd32d25270). #5331 merged d0bff086d6 (11-03) |
| 27e0735af6 | 11-03 | b8621fd1ca CMYK Fill semantics (Khawar Zamman Wani; —) | 11.6 h | "independent of the PSD/TIFF memory admission work and ships in its own PR" | #10897 (503aa60f5a) |
| f3ce2e2b9e | 11-03 | 47ee3f6960 Gradient Overlay drag (Trevor Brown; **Claude Fable 5.1**) | 12 min | none | integration-batch-15 (#11203) |
| 23f1b8bce7, 947d4fd1b0 | 11-01 | d7bce26deb, de9c5e743e Image Size style scaling (yoriswind; —) | 1h42, 1h23 | none | integration-batch-12 (#10776) |
| 2de7a9c042 | 11-07 | c1662d4911 "Export: split nested groups…" (Triwarr; —) | ~30 h | none | #11647 (aae9b7ea61) |
| 70cb31610b | 10-12 | 2b5f0f5984 Levels Alt→Reset (funkvay-star; —) | ~16 h | "#3871 brings Alt+Cancel Reset to every adjustment dialog … so this PR keeps only the clipping display" | #3693 (41aa2b86f5). Superseded by #3871 (67e4b8a499) |
| 8f6f1d0cdb | 10-14 | 511f864778 (itself a "revert arrow-key guard" refactor) (safvanedge; —) | 28 min | none | integration-batch-10 (#10145) |
| b390bef334 | 11-08 | d3e8039f76 (object not in clone) | n/a | none | #11895 (b479d94e21) |
| 17663b160d | 10-31 | contributors display-name entry (qvest-ssels; revert carries Opus 5.5 trailer) | n/a | none | #10395 |

Other subjects the grep matched are not reverts of commits (e.g. 81925d7769 "Raw Defaults resolution on
Revert"; 3e33b115a5 is a test commit). Table rows: 23 `^Revert` hits minus the false positives.

### E07-001 — Main has no revert commits on its first-parent line. Every revert happened on a branch before merge
- Label: VERIFIED
- Source: loop over `git log main -i -E --grep='^revert'` with `git rev-list --first-parent main | grep -c <sha>` (all 0); `git log --first-parent main -i -E --grep='revert|back out|roll ?back'` returns no reverts.
- Data: 23 `^Revert` commits are reachable from main, and 0 of them are first-parent. 21 more `^Revert` commits exist only on unmerged refs.
- Notes: Revert rate is 23/12,396 = 0.19% of all commits, or 0/3,475 at PR granularity. Per ISO week (non-merge `^Revert`, `$W` script): W40 0, W41 0, W42 3, W43 6, W44 3, W45 5, W46 0. This matches `data/E03_corrective_weekly.csv`. INFERRED: bad changes are caught before main, either inside integration batches or by rescoping a PR. Main itself is repaired by forward fixes (§2), never by reverting.

### E07-002 — Maintainer "integration batches" act as a staging buffer where failing PRs are backed out
- Label: VERIFIED (mechanism); INFERRED (that the reverts were for breakage, since no reason is written)
- Source: cece50d513 (2026-10-25) "Merge pull request #9386 from davidmann4/integration-batch-8", body "Integration batch 8: 37 reviewed community PRs on main". Its second-parent history holds `Merge PR #…` commits, `Integration: …` repair commits and the six reverts above. First-parent batch merges: aiongg integration-2…10 (10-18 → 10-21), davidmann4 integration-batch-7…20 (10-23 → 11-06), FredApps integration/* (10-29, 10-30).
- Method: `git log --first-parent main --format='%h|%ad|%s' | grep -i integration`; `git log --first-parent cece50d513^1..cece50d513^2`.
- Data: 388 commits on main have subjects starting `Integration:` (`git log main --grep='^Integration:' -i -E | wc -l`).
- Notes: Integration batches did not exist for the first ~18 days. They appear after the red-main spike of W41 (§2). See also E05-052.

---

## 2. Broken main / CI incidents

Merge times come from the first-parent committer date (`$W/prmap.json`, built from `git log --first-parent main --format='%h|%cd|%s'`). All times are converted to UTC. TTF = fix-PR merge minus the merge of the later breaking PR.

| # | Fix commit (PR) | Breaking PR(s) | Root cause (quoted / paraphrased from fix message) | Class | TTF | Fixer (trailer) |
|---|---|---|---|---|---|---|
| 1 | da9adf82bc (#597) 10-07 | #533 | rustfmt "CI Format step red since #533" | fmt | 43 min | Brandon Thomas (—) |
| 2 | 6103da5278 (#798) 10-07 | #663 + #700 | "Format red on main since #663 + #700". Two PRs, each green alone | semantic merge skew | 28 min | Tanish Manku |
| 3 | 83ace1138e (#819) 10-07 | #711 | Format red | fmt | 20 min | Brandon Thomas |
| 4 | e1cf321183 (#822) 10-07 | #672 + #733 | Format red | merge skew | 3 min | Tanish Manku |
| 5 | 25f211500b (#834) 10-07 | #811 + #824 | "Both PRs added Korean labels … ko.tsv listed each twice" | duplicate parallel work | 37 min | Brandon Thomas (Opus 5.5) |
| 6 | 3689754ef2 (#876) 10-07 | #825 | default export became flat TIFF → corpus round trip "670 failures" | behaviour change vs. other test | 2h18 | Tanish Manku (Opus 5.5) |
| 7 | eec4af6551 (#1074) 10-08 | #865 + i18n | new path commands not in filesystem-param audit list; cs plural missing | cross-cutting audit | n/a | Brandon Thomas (Opus 5.5) |
| 8 | db3a77a0b6 (branch `claude/fix-main-pl-missing`) 10-08 | #1192 + concurrent UI PRs | "merged around the same time, so pl.tsv missed four strings" | merge skew (i18n) | n/a | Claude (Opus 5.5; `Claude-Session:` trailer) |
| 9 | 44d7902f08 (#1618), 6e558d2fc9 (#1620) 10-09 | #1232/#1516 + #1562 | el catalog incomplete, "main red since #1232 + #1562" | merge skew | 14 min, 3 min | Brandon Thomas |
| 10 | ee3ebfa748 (#2042) 10-09 | #1882 | Windows Debug-quoting doubles backslashes. "Windows CI red since #1882" | platform-only test | 1h08 | Brandon Thomas (Opus 5.5) |
| 11 | 184c226a76 (#4147) 10-12 | #3909, #3877, wasm growth | Windows path separator in test. A preview window broke another test. wasm "sat at the 24 MiB gate" | platform + size gate | 5h43 | Brandon Thomas (Opus 5.5) |
| 12 | 72b499a28f (#4694; branch `fix/main-wasm-tile-overlay`) 10-12 | #4217 | "used rayon's par_iter in ui-egui unconditionally … cargo xtask wasm failed on main" | wasm gate | 1h49 | Brandon Thomas (Opus 5.5) |
| 13 | 7bb10a7759 (#5873) 10-14 | #5448, #5670, #5135 | "fmt break" across three PRs | merge skew | 1h05 | Tanish Manku |
| 14 | df055f3dcb (#5941; branch `fix/main-ui-tests-1015`) 10-15 | #5614 vs #5208; #5779 | "#5614 renamed the built-in profile … after #5208 hard-coded '(Photocraft)'" | semantic merge skew | ~9h15 | Zuujis / Brandon Thomas (Opus 5.5) |
| 15 | 351149f0df (#6906) 10-17 | #5344 × #5616 | "#5344 added the export_presets field … #5616 … lacked the new field, so main stopped compiling (E0063)" | **compile break from two green PRs** | 13h12 | Joseph / 00xJ0 |
| 16 | 29e4039c72 (#9009) 10-23 | two PRs | "Two PRs that landed together each added [people.ronibalthazar]" → invalid TOML | duplicate parallel work | n/a | Brandon Thomas (Opus 5.5) |
| 17 | 3c44319455 (#11984; `fix/main-scorecard-stale`) 11-07 | #11322 | generated scorecard said 192 settings, audit counted 193 | generated-doc staleness | 2h04 | David Mann (Opus 5.5) |
| 18 | 47d3dcde33 (#13079) 11-11 | #12214 | "took draw_default_tool_cursor to a cognitive complexity of 31 (limit 30)" | new lint gate | 52 min | David Mann (**Fable 5.2**) |
| 19 | 06650357d8 / 71aad480b6 (#13128; `fix/main-tiff-dup-consts`) 11-11 | #9781 + #10983 | "each defined TAG_JPEG_TABLES and TAG_PREDICTOR … merged minutes apart, so main stopped compiling (E0428)". The two changes together also pushed `prepare` past the clippy complexity limit | **duplicate consts + lint** | 4h36 | Tanish Manku, FredApps (same PR: 3 more "Fix main" commits for #10597 vs #10203 and #11009 vs #10953) |
| 20 | 79a33dae9c (#13199; `fix/main-red-windows-pipette-cursor`) 11-11 | #12523 vs tests of #12145/#12301 | native pipette bitmap; old tests "still looked for the drawn pipette and failed on Windows unit" | platform-only, PR ran Linux only | 2h02 | David Mann (Opus 5.5) |
| 21 | 2383ea0a4a (#13257; `fix/main-red-automation-gpu-group`) 11-12 | #10842 | GPU backend tests "were not in the gpu test group, so nextest ran them alongside up to four other GPU tests on the lavapipe runner … segfaulted" | latent concurrency, GPU | ~6.9 d (latent) | David Mann (Opus 5.5) |

### E07-003 — The dominant red-main cause is semantic merge skew between PRs that were each green
- Label: VERIFIED (facts in rows 2, 4, 5, 8, 9, 13–16, 19); INFERRED (classification "dominant": 11 of the 21 incidents)
- Source: the commit messages quoted above. Typical wording: "#9781 and #10983 each defined … merged minutes apart" (06650357d8). "Two PRs that landed together each added …" (29e4039c72).
- Notes: There is no GitHub merge queue. The current `.github/workflows/ci.yml` has no `merge_group` trigger (`grep -rln merge_group .github/` returns nothing). Nine commits labelled "(merge queue)" by David Mann (11-08 → 11-11, e.g. fda05f7b02 "On main + #10448, so main's gate stays green after the merge") show a **manual** queue instead: main is merged into the PR and gates are re-run before merging. Cross-ref E05-052.

### E07-004 — Process change 1: main's CI runs were being cancelled, so red main went unseen
- Label: VERIFIED
- Source: commit 01a63dee89 / 07174271d5 (#800, 2026-10-07, Tanish Manku, Opus 5.5 trailer)
- Quote: "Between 09:56 and 20:34 UTC on 2026-10-07, 80 of 83 push runs on main were cancelled, and a formatting break from two PRs that were each green alone (#663 + #700) went unnoticed"
- Notes: Fix: `cancel-in-progress` only for pull_request. The same change made **PRs Linux-only** unless they touch platform paths or are labelled `full-ci`. INFERRED trade-off: Windows-only breaks (rows 10, 11, 20) then surface on main, not on the PR. Sonar got the same fix later: 5521968828 (10-23) "don't cancel superseded runs on main".

### E07-005 — Process change 2: red-main volume clusters in W41 and on 2026-11-11
- Label: VERIFIED (counts); INFERRED (causes)
- Method: dates of the 59 commits in `$W/mainfix.txt`: 10-07: 8, 10-09: 7, 10-12: 7, … 11-11: 11. Week totals (non-merge, regex `fix main|main red|red since|…`): W41 16, W42 4, W43–W45 0, W46 11.
- Notes: The quiet weeks W43–W45 coincide with integration batches (E07-002). The 11-11 spike coincides with a large merge wave (189 first-parent commits dated 11-11; 15 first-parent merges by David Mann on 11-12; `git log --first-parent main --format='%cd' --date=short | grep -c 2026-11-11`) and with the newly denied `cognitive_complexity` lint (604da9d06b, 10-27). Rows 18 and 19 and e17091578e "Fix main: clippy after the 11-11 merges" are lint-induced. INFERRED: tightening a gate turns merge skew into red main more often, because two compliant functions can combine into a non-compliant one.

### E07-006 — Fix-main work is mostly agent co-authored and done by a few maintainers
- Label: VERIFIED
- Method: over `$W/mainfix.txt` (59 commits): 40 carry a Claude/Anthropic or `Claude-Session` trailer. Authors: David Mann 11, Brandon Thomas 11, Tanish Manku 8, FredApps 5, BFlat 4, others ≤2.
- Notes: The two `claude/fix-main-*` branches (db3a77a0b6, bf2c67b19d, 2026-10-08) are authored by "Claude" with `Claude-Session:` trailers. These are direct agent sessions. The count includes cherry-pick duplicates (e.g. 06650357d8 and 71aad480b6).

---

## 3. Flaky / nondeterministic tests

| Fix (sha, date, PR) | Test / area | Cause (from message) | Fix | Measured rate |
|---|---|---|---|---|
| 27e047f19f / d71143e4d8 (10-05, #135; `fix/canvas-geom-undo-determinism`) | engine undo bit-exact test | process-global `psblend::set_text_gamma` toggled by a parallel test | move the test to its own binary. Document the hazard | "seen once on Windows CI" |
| c454af8d96 (10-05, #264) | text | font family order nondeterministic | deterministic ordering | — |
| 09bc2ac0c4 (10-07, #609) | algo cancel/progress | rayon workers report progress out of order. Non-atomic load→assert→store in the test | test tolerates order | "reproduced 1-in-300 under synthetic CPU load" |
| d8d2df4fba (10-09, #1856) | camera_raw_scope GPU tests | "Concurrent wgpu instances segfault in libvulkan" | `GPU_LOCK` serialisation | — |
| b54fdfd94f (10-11, #2997) | panic_hunt | first `type.create` scans system fonts 3.5–5 s, over the 4 s deadline | rerun on a fresh session before declaring a hang | — |
| 18c5420039 (10-11; `fix/flaky-tests-2026-10-11`) | 4 load-sensitive tests | global font generation bump. Fixed frame windows. 5 ms polls. Shared process caches | condition polls with 60 s cap. Own binary | "font test failed 6/6 … MCP test failed 9/30. After: 0" |
| 4e7a17cd5d (10-15; `fix/compose-identity-memo-race`) | compose effect identity cache | concurrent cache misses | serialise misses | — |
| 5b087699be (10-18, #7418; `fix/test-flakes-file-locks-portal`) | file-lock + portal tests | spawned children inherit flock fds. Message stream created after a message was sent | `CHILD_SPAWNS` RwLock. Create the stream before the thread | "about 6 failures in 15 runs"; "about 1 run in 25" |
| 6a39ccd52e (10-30, #9173) | GPU pipelines (Windows) | FXC shader blobs shared across threads | stop sharing | — |
| 7091cb6b8c (11-10, #12854; `fix/raster-memory-test-race`) | raster memory reservations | process-wide `RESERVED` under `cargo test` threads. "nextest … gives each test its own process, which hid it" | tests take turns | "failed 15 of 40 runs, the fixed one 0 of 40" |
| 2383ea0a4a (11-11, #13257) | automation GPU backend | not in nextest `gpu` group → concurrent GPU tests segfault | add to group | CI run 43051019603 |

### E07-007 — Flakes are root-caused to shared process state, timing windows or GPU concurrency, and fixed with measured rates
- Label: VERIFIED (each row); INFERRED (taxonomy)
- Notes: Three cause families. (a) Process-global state shared by threads in one test binary: text gamma, font generation, `RESERVED`, render caches, inherited fds. Fix: move to own binary or a lock. (b) Fixed time/frame budgets: frame windows, 4 s deadline, 5 ms polls. Fix: poll on a condition with a long cap. (c) GPU driver concurrency. Fix: `GPU_LOCK` or the nextest `gpu` group (introduced 3092d3b6f9, 10-10, #2414). The resulting rules are encoded in code (locks, groups, separate binaries). No AGENTS.md rule on flakes was found (`grep -n -i flak AGENTS.md` returns nothing). Before/after failure rates are a consistent message convention. Cross-ref E05-053.

### E07-008 — The test runner masked a race. nextest's process-per-test isolation hid shared state that `cargo test` exposed
- Label: VERIFIED
- Source: 7091cb6b8c (2026-11-10, FredApps): "nextest on Linux gives each test its own process, which hid it" (exposed by the FreeBSD job, which uses `cargo test`).
- Notes: INFERRED: running two harnesses (nextest and plain cargo test on FreeBSD) acted as an accidental diversity check.

---

## 4. Quality campaigns

### E07-009 — "Never crash" began on day 5, triggered by user crash reports. It was a 12-PR sweep in about 15 minutes
- Label: VERIFIED (timeline); INFERRED (trigger chain)
- Sources:
  - Issue #7 (opened 2026-10-03 by Suleman-Elahi): "Dies as soon as i open jpeg image to edit", wgpu panic "Format Rgba32Float is not renderable". Fixed by #22 / ae7d802726 (10-04 02:27 -0400). URL https://github.com/storytold/photocraft/issues/7 (accessed 2026-11-12, via WebFetch summary).
  - #16 8a2f31c2c4 and #17 b6a95b6c8d (10-03, storybored379, Opus 5.5 1M trailers): a panicking MCP command "wedges the headless session … losing unsaved work". Indexed Color panic.
  - ed0b99964d (10-04 00:10 -0400, Brandon Thomas, Opus 4.8): "AGENTS.md: add rule 9 — never panic on input".
  - bf111b524e (10-04 00:24): "Fix panics on malformed params; add panic-fuzz harness" (`tests/panic_hunt.rs`).
  - 50a27e6c74 (#33, 10-04 11:14): "Never crash: steering rules, clippy.toml, forbid unsafe". "Standard: craftrules/standards/never-crash.md" (an org-level standard).
  - Sweep: 69f0e25d5f (#34) … 2e80c781ee (#59), 11 squash merges between 13:25:17 and 13:40:43 -0400 on 10-04 (`git log main -i --grep='never crash'`). The 12 `pr/never-crash-*` branches each hold 1 commit dated 10-04 (`git rev-list --count main..origin/pr/never-crash-*` = 1 each). All carry the Opus 5.5 trailer (e.g. 4bd7f4eeb1, 63b589318a).
- Scope: e.g. `pr/never-crash-engine` 21 files, +128/−98. `pr/never-crash-guard` adds `catch_unwind` around `Session::execute` and a `crash_guard` module.
- Outcome: AGENTS.md §3 "Never crash (outranks feature work)" (`74330157cb:AGENTS.md:103`). Rust house rule 1 (`AGENTS.md:27`). "Every crash fix comes with a test that panicked before the fix" (`AGENTS.md:113`). Follow-on "hostile numbers" work: 47 main commits mention "hostile", spread over 10-04 → 11-08 (`git log main -i --grep=hostile`), e.g. 5049a1d062 (#869, 10-08) "Never crash on hostile numbers".
- Notes: The trigger chain is INFERRED: user crash issues #7/#4 and community panics #16/#17 came on 10-03, then the rule landed at 00:10 on 10-04, then the campaign ran that afternoon. The commit texts do not state the causal link. Cross-ref E02-006.

### E07-010 — Security hardening was a separate, later campaign by one maintainer, with opaque `Finding:` IDs
- Label: VERIFIED
- Data: 74 main commits with subject `^security`, first 8b1cbb741b (#61, 10-04, Gh0stly: "authenticate control channels"). 52 commits carry `Finding: <uuid> (CWE-…)` trailers (27 on main). All by Dylan M. Taylor, 2026-10-21 → 11-11. CWE mix: CWE-407 ×23, CWE-400 ×18, CWE-770 ×6, CWE-409 ×3, CWE-789 ×2. 21 `fix/sec-*` branches at HEAD, most still ahead of main (not merged as-is). The final wave on first-parent main is 11-11 (abeb16c96b … 3b43cb451a: "bound EXIF text decoding…", "checked sizes in encoders…", "limit zstd windows…").
- Method: `git log --all --format=%b --grep='^Finding:' | grep -oE 'CWE-[0-9]+' | sort | uniq -c`.
- Example: 4d4d530d2e "security(affinity): bound raw child-slot traversal work … Finding: 3973fcd0-… (CWE-400)".
- Notes: The tool that produced the Finding UUIDs is not named anywhere in the trailers. Unknown. SECURITY.md was created 10-04 (1fe689a7bf). E05-034 notes it has no private channel. The campaign is mostly algorithmic-complexity / DoS bounds (CWE-407/400), not memory safety. INFERRED: this follows from the `forbid(unsafe)` baseline.

### E07-011 — Sonar campaign (10-18 → 11-10) added gates whose side effect is red main
- Label: VERIFIED (dates); INFERRED (side effect)
- Source: SonarCloud badges 18f8d33577 (10-18). Scan 8e518d8169 + 87fa191818 (10-21). Same-day rule fixes S7630 (5933793982, "prevent script injection in fuzz workflow"), S6506, S7637, S7488. 3877bb1dbe (#9044, 10-25) "resolve SonarCloud maintainability issues". 604da9d06b (10-27): `cognitive_complexity = "deny"`, `too_many_arguments = "deny"`, `wildcard_imports = "deny"`, `cognitive-complexity-threshold = 30` (`74330157cb:clippy.toml:8`). Branches: `sonar/*` ×5, `sonar-fix/*` ×4, `fix/sonar-maintainability`.
- Data: 21 main commits mention sonar, 17 mention cognitive complexity / too many arguments (7 of them on 11-11).
- Notes: Side effect: E07-005 rows 18–19. Cross-ref E05-031/032.

### E07-012 — Mass reformat on day 5, recorded in `.git-blame-ignore-revs`
- Label: VERIFIED
- Source: f7eb6ea9e7 (2026-10-04 10:20, Brandon Thomas, Opus 5.5): "CI's `cargo fmt --all -- --check` has failed on every run because the repo had no rustfmt config and was never formatted". 345 files, +11,237/−11,468. 574d4fe7da adds it to `.git-blame-ignore-revs`, the only entry (`74330157cb:.git-blame-ignore-revs:3`).
- Notes: CI had been red on format "on every run" for the first 4 days. Format breaks remained the most frequent red-main class in W41 (rows 1–4, 13).

### E07-013 — Over-claimed parity was corrected publicly on day 6, after first user feedback
- Label: VERIFIED
- Source: 20783fdc70 (#182, 2026-10-05, Brandon Thomas, Opus 5.5; branch `docs/honest-parity` 8923fe8f63), adding to `docs/roadmap.md`:
  > "**We are far from real Photoshop parity.** `parity.md` says 625/625 menu items are live, but that only means each item dispatches *a* command."
  > "users hit broken basics that all counted as "live": … shortcuts that didn't fire after clicking a panel (214 failures in an audit)…"
  > "[`parity-estimate.md`] (~82%) counts feature surface and overstates user-facing readiness; treat it as an upper bound."
- Estimates it gave: feature surface 55–70%, "a working professional could switch today" 20–35%. Same day: 433b84fae7 (#186, `docs/where-we-stand`), and 10203e7a60 (#184, `docs/no-tauri`) "AGENTS.md: no Tauri, Electron or webview shells".
- HEAD: README still says "that measures wiring, not behaviour" (`74330157cb:README.md:312`). `docs/target-app-parity.md:283`: "Menu coverage (96%) overstates true parity".
- Notes: There is drift inside the correction itself. The revision table in `docs/target-app-parity.md:646` records the 10-05 assessment as "surface 60–70%, ready for real work 25–35%". The original commit says 55–70% and 20–35%. VERIFIED discrepancy. Cause unknown.

### E07-014 — "Settings that do nothing" became a measured, ratcheting metric (66/129 → 8/199)
- Label: VERIFIED
- Method: sampled `docs/scorecard.md` across its history (`git log main --first-parent --reverse -- docs/scorecard.md`, every 25th revision): 10-05 66/129; 10-07 60/135; 10-09 56/140; 10-10 51/141 → 46/149; 10-11 35/153; 10-12 30/154; 10-13 26/156; 10-15 26/166; 10-29 12/181; 11-07 10/195; HEAD 8/199 (`74330157cb:docs/scorecard.md:215`, "a heuristic lower bound").
- Notes: Settings that do nothing are inert UI. Wiring commits follow a naming pattern, e.g. "Type: wire the Use Escape to Commit preference (#1927)" (429b9fc6a5). INFERRED: placeholder surface was generated faster than behaviour, and the project turned that failure into a metric instead of a rule.

### E07-015 — Regression-test backfill campaign: "eight fixes merged without one"
- Label: VERIFIED
- Source: 72e11802d4 (#8690, 2026-10-25, skylar taylor-barrick), 8 files +275. It is the squash of `test/backfill-regression-tests` (9 commits, 10-22). Each test states what fails without the fix, e.g. "Without prune_thumbs the deleted layer's thumbnail is still cached".
- Notes: Evidence that the "test that fails without the fix" rule (house rule 4, `AGENTS.md:9`) was not always met before merge. Exact rule wording dates: see E02.

### E07-016 — Scorecard rows that under-claimed (stale "missing" rows) also cost agent sessions
- Label: VERIFIED
- Source: 984bc5c715 (#2894, 2026-10-11, Erica Franco): "AGENTS.md sends contributors to the scorecard's missing and partial rows when picking work, so a stale row costs someone a session: they sit down to write a test that is already there." Also fc00f1e5bc (10-07) "BUG-203 (atomic saves) is done - flip the stale rows".
- Notes: Doc/code drift runs in both directions. "stale" appears in 155 main commit messages.

---

## 5. Agent-specific failure modes acknowledged in history

Phrase counts (main, `git log main -i -F --grep=<p> | wc -l`): stub 11, placeholder 36, fake 15, "was never" 28, "dead code" 8, silently 102, no-op 61, duplicate 218, "does nothing" 22, "did nothing" 46, "settings that do nothing" 21, "without the fix" 47, mutation 24, "never ran" 9, "resolve conflicts" 46, CodeRabbit 453. hallucinat, "not actually", "never wired", "didn't actually", "false positive" and vibe: 0. "slop" (22) matches "slope", and "AI-generated" (8) matches CodeRabbit HTML comments. Both are false hits.

### E07-017 — UI controls shipped as decoration, then wired later
- Label: VERIFIED
- Source: c89c33c704 (10-03, Opus 4.8): "the options-bar Mode dropdown sets the session brush's blend mode (it was decorative)". 9dc394dfc8 (10-03, Opus 4.8): "The options-bar Fill dropdown was decorative." Plus E07-014 (66 dead settings on 10-05) and E07-013 (625/625 menu items "live").
- Notes: INFERRED class: "surface before behaviour". The codebase's own metric (menu wiring) rewarded it.

### E07-018 — Tests that passed without testing anything
- Label: VERIFIED
- Sources:
  - 2ff8f419cb (#7975, 2026-11-06, FredApps, Opus 5.5): on Linux CI, "57 GPU checks (50 GPU parity, 3 canvas, 2 adjustment preview parity, 2 effect-map recovery) returned early and passed without comparing anything". New step "fails unless … no test printed a skip".
  - 1a86826ab7 (10-23, ebosido444-ai): Windows pipeline test "passed without ever building a compositor pipeline and never reached FXC, the compiler this test exists for".
  - 602344bae0 (#5549, 10-15, agent-346022): "The mid-drag test asserted nothing about what the display gate does … It now asserts … Verified by mutation." Same message: another test "passed even with the dialog id removed".
  - c441fd350c (#11369, 11-06): a test "passed even if nothing was painted (CodeRabbit on #11369)".
  - a79db76e30 (11-06): "the Alt+H/Alt+P cases checked nothing".
  - 437cd7f0fe (11-09): a test "never exercised `grow_hint`".
- Notes: Detection came from CodeRabbit review, mutation checks and CI-environment audits. Correction mechanisms: fail-on-skip CI (2ff8f419cb) and the mutation check named in commit text ("mutation" appears in 24 commits). Cross-ref E05-024.

### E07-019 — Duplicated work from parallel landings (duplicate rows, tables, constants)
- Label: VERIFIED
- Sources: 25f211500b (ko rows), 29e4039c72 (people.toml table), 06650357d8 (TIFF consts E0428), 106776f598 (10-22, "main and #6658 both added 'Continue'"), 252a47ef76 (10-11, "i18n(cs): drop rows #3039 and #3454 both added"), b367a6118f (10-25, one Czech "New Snapshot").
- Notes: The project's rules respond with a "look for a better PR" house rule (`AGENTS.md:11`) and "Check, then claim" (`AGENTS.md:7`, added 2026-11-06 per 7d8648dfcb). At the PR level, 70cb31610b reverts a Levels change superseded by #3871. Sibling data: `data/E03_duplicates.csv`.

### E07-020 — Merge-conflict casualties
- Label: VERIFIED
- Sources: 8601a7b170 (10-15, David Mann): "The merge of main (5a4df1a3) committed unresolved conflict markers in the status lines of gaps.md, target-app-parity.md and ui-parity.md". 0eb6ba9dea (11-07): "The merge of main into #10730 dropped the first line of the comment". ea37bf8bd9 (11-08): "drop the map_pixels wrapper the main merge left unused". 4623c3068c (10-16): "Fix the detect chain after the main merge."
- Notes: INFERRED hotspot. AGENTS.md asks every PR that moves a number to "bump their status line and revision history" (`74330157cb:AGENTS.md:134-135`). That status line is a single very long line (`docs/target-app-parity.md:3`), and `docs/scorecard.md` is the 3rd most-touched file on main (443 non-merge commits). Every PR therefore edits the same lines, which produces conflicts.

### E07-021 — Fix-induced regressions in the save path (a data-loss class)
- Label: VERIFIED
- Chain:
  1. 82270711de (#230, 10-05): "one crash-safe atomic_write for every document write".
  2. Issue #7858 (10-19, denstu473): after a successful Save, a power loss reopened the previous document. Labelled `priority: critical` by the ticket-craft bot. Closed 10-22 via #8034 (https://github.com/storytold/photocraft/issues/7858, accessed 2026-11-12, via WebFetch summary). Code: 851ca348a7 "persist Windows save publication before acknowledgement". Design note `docs/windows-save-durability.md`.
  3. 0b779b4fec (#5420, 10-23, FinnNk, Opus 5.5): directory fsync result had been "discarded … so a save whose rename might not survive a power loss reported success" (fixes #4968). The same PR then needed a follow-up fix: "Treating that open failure as a failed flush made saves into such folders fail".
  4. Issue #9440 (10-25, relayed from Discord by the ticket-craft bot): saves to a mapped SMB drive loop. A contributor traced it to the strict flush policy "tied … to #8034"; 5 duplicate reports were merged into it (https://github.com/storytold/photocraft/issues/9440, accessed 2026-11-12, via WebFetch summary). Fixed 1253e79d68 (11-11): "Since #8034 (for #7858) every Windows flush failure fails the save".
  5. #11189 (11-04, Hartmut Nörenberg): "a vanished backup is not a recovery copy".
- Notes: About 17 days from report to fix for #9440. INFERRED class: a durability fix that is correct on local NTFS regressed network filesystems. The test matrix had no SMB case. The fix was reproduced "by injecting the error at the filesystem layer".

---

## 6. External criticism → response

### E07-022 — First user reports were answered within a day, and fixes named the issue
- Label: VERIFIED (via WebFetch summary for the issue page)
- Source: Issue #7 (10-03), maintainer "echelon" replied 10-04 that the stack trace "pinpointed it exactly". Closed by #22 the same day, with a fallback test (ae7d802726).
- Notes: Later, bug intake goes partly through a "ticket-craft" bot that relays Discord reports and adds labels and "Possibly related" links (#7858, #9440). Whether maintainer comments were AI-written cannot be determined from the summaries.

### E07-023 — Issue-referencing correction commits are common
- Label: VERIFIED
- Method: `git log main -i -E --grep='data loss|lose (their|the|your) work|lost work|loses work|corrupt|truncat(ed|es) the file|atomic' | wc -l` = 82.
- Notes: Not further classified. This is a lead for the issue-mining stream.

---

## 7. Rework indicators

### E07-024 — Fix-type share by week (two denominators; both heuristic)
- Label: VERIFIED (counts); INFERRED (interpretation)
- Method (script in `$W`, run inline): regex `^(fix|bugfix|hotfix)\b|^fix\(|^\w+(\(..\))?: fix|\bfix(es|ed)? #\d|^Fix\b` on subjects. The first-parent variant also matches branch names `from x/fix…`. Weeks start on Monday.

| Week of | Non-merge commits | fix-type | % | First-parent entries | fix-type | % |
|---|---|---|---|---|---|---|
| 09-28 | 128 | 8 | 6.2 | 124 | 8 | 6.5 |
| 10-05 | 1,564 | 269 | 17.2 | 1,424 | 256 | 18.0 |
| 10-12 | 1,872 | 355 | 19.0 | 912 | 204 | 22.4 |
| 10-19 | 1,757 | 357 | 20.3 | 295 | 60 | 20.3 |
| 10-26 | 1,141 | 72 | 6.3 | 73 | 15 | 20.5 |
| 11-02 | 1,480 | 170 | 11.5 | 321 | 155 | 48.3 |
| 11-09 | 387 | 77 | 19.9 | 326 | 211 | 64.7 |
| All | 8,329 | 1,308 | 15.7 | 3,475 | 909 | 26.2 |

- Caveat: many corrective subjects use plain language without "fix" (e.g. "… targets its mask again", 3525a1d2bc), so the counts are a lower bound. The November first-parent rise mostly reflects the switch from squash subjects to `Merge pull request … from x/fix/…` merges, where the branch name carries "fix". Do not read it as a quality drop. Prefer `data/E03_corrective_weekly.csv` / `E03_cc_types_weekly.csv` for consistent series.

### E07-025 — Files with the most fix commits are UI shell files
- Label: VERIFIED
- Method: `git log main --no-merges -i -E --grep='^(fix|bugfix)\b|^fix\(|^Fix\b|^[a-z-]+(\([a-z,-]+\))?: fix' --format= --name-only | sort | uniq -c | sort -rn`
- Data: `crates/ui-egui/src/canvas.rs` 112, `ui-egui/src/lib.rs` 77, `panels.rs` 65, `engine/src/atn_cmds.rs` 41 (+34 its tests), `docs/control-protocol.md` 32, `menus.rs` 31, `type_tool.rs` 27. These are also the most-touched files overall (`lib.rs` 623, `canvas.rs` 618 non-merge commits).

### E07-026 — Five features with ≥5 follow-up fix PRs
- Label: VERIFIED (lists); INFERRED (that these are "follow-ups")

| Feature | Initial landing | Follow-ups (examples) | Count method |
|---|---|---|---|
| Perspective Crop | 017d1aea1c (#2864, 10-11) | fd99c1f464, 22cacbf198, 193f495e5a (10-17); 5225b592fe (10-18); 745f535fda (10-19); 40c720f38e … fd0d543d0d (11-07, Hector Villarreal, 10 commits, several "CodeRabbit review"); 0a8eb9d6c8/3e81a3bcc4 (11-09); 76fb4cc58a (#13065, 11-11); PR #12237 merged 11-12 | 33 non-merge main commits matching `perspective crop\|pcrop`, 10-11 → 11-11 |
| Artboards | Artboard tool 2e0c426692 (#2862, 10-11); earlier PSD work 10-05 | overflow fixes 64da6bb455 (#1181), ba4dc112bb; #1531 duplicate/drag 3e8d54896d; `fix/artboard-followups-10512-10538` → 3e27572e7a (#11441, 11-05): "(#10512 follow-up)", "(#10538 follow-up)" | 124 non-merge commits mention artboard. 15 on 11-06 alone |
| Flatpak self-update | update check disabled in Flatpak 6b551c11e8 (10-22) | f1866aed06 (#9982, network), 2fccdcba8e (#9983, comment correction), 0d9a0f6613 (#10206, enable checks), 3ff283af35 (#10393, version pins), 83ef781382 "Release 0.22.1: fix Flatpak update permissions" (`patch/flatpak-update-0.22.1`, unmerged), eee667f1d9 (#13322, 11-11) "Fix Flatpak updates and bump to 0.23.1" | 6 PRs over 20 days. v0.22.0 (11-09) → v0.23.0 → v0.23.1 (both 11-11) |
| egui 0.37 migration | 5c9192bbe2 (#9363, 10-25), 246 files +8,720/−1,589 | 178d6c2235 "rustfmt the egui 0.37 merge", b078e0e8a6 (#9575 review follow-ups), c484971fdf (renames), 3f2229b9ad (CJK fallback), 73ac7d9a25 (10-28) "Arabic layer names … read right to left again on egui 0.37" | 18 commits matching `egui ?0?\.37\|egui037\|M0\.37`, 10-25 → 11-05 |
| Windows save durability | 82270711de (#230, 10-05) | E07-021 chain: 851ca348a7, 0b779b4fec (+ its own follow-up), 1253e79d68, #11189 (3 commits) | ≥5 PRs, 10-05 → 11-11 |

---

## 8. Dependency / tooling breakage

### E07-027 — Tooling and dependency breaks were handled as dedicated PRs
- Label: VERIFIED
- Items:
  - nextest: bf6e25af9a "Use relocated nextest binaries in process integration tests" + ddf9ca1e2d "ci: require nextest 0.9.150" (#9749, 10-26, skylar). Cross-ref E05-011 (pinned for an advisory).
  - wasm size: 37637dbd71 (#237, 10-05) "wasm 26.3 -> 18.8 MiB". 184c226a76 (10-12) opt-level z, 25,186,233 → 24,829,840 bytes, under the 24 MiB gate. df055f3dcb (10-15): wasm "sits at the 25 MiB per-file cap of Cloudflare Pages, so the 24 MiB gate failed unrelated PRs". Fix: ship gzip parts via new crate `apps/photocraft-web-boot`.
  - wasm build: 72b499a28f (rayon on wasm, row 12). `fix/wasm-size-limit` c78e72c0ec: an xtask parser broke after the catalog registry changed form.
  - egui 0.37: the plan doc `docs/egui-037-migration-plan.md` records "All nine CI stages passed: 11,590 passing test executions" and "Publication requires separate explicit approval; human review and human merge are required" (`74330157cb:docs/egui-037-migration-plan.md:3`). Branches `codex/egui-037-*` (Dylan M. Taylor, skylar taylor-barrick).
- Notes: The size gate failing "unrelated PRs" is a cost-externalising failure. A single shared threshold makes every PR red once any PR crosses it.

---

## 9. Taxonomy of failure modes

| # | Failure mode | Examples (VERIFIED facts) | Classification label | Corrective mechanism observed |
|---|---|---|---|---|
| F1 | Semantic merge skew (each PR green, union red) | 06650357d8, 351149f0df, df055f3dcb, 6103da5278 | INFERRED | manual "(merge queue)" re-merge (fda05f7b02), integration batches (cece50d513), main CI not cancelled (01a63dee89) |
| F2 | Duplicate work from parallel agents/contributors | 25f211500b, 29e4039c72, 106776f598, 252a47ef76 | INFERRED | consistency tests (`bundled_catalogs_are_consistent`), house rules 2/6 (`AGENTS.md:7,11`) |
| F3 | Surface without behaviour (decorative/inert UI, wiring metric over-claims) | c89c33c704, 9dc394dfc8, 20783fdc70 | INFERRED | prefs audit metric (E07-014), honest-parity doc (E07-013), panel-commands xtask (4165c57f92) |
| F4 | Vacuous tests (skip-as-pass, assert nothing) | 2ff8f419cb, 1a86826ab7, 602344bae0, a79db76e30 | INFERRED | fail-on-skip CI step, mutation checks, CodeRabbit review |
| F5 | Fixes merged without regression tests | 72e11802d4 ("eight fixes merged without one") | VERIFIED (self-described) | backfill campaign. House rule 4 |
| F6 | Crash on hostile input / driver variance | issue #7, b6a95b6c8d, 8a2f31c2c4 | VERIFIED | never-crash sweep, panic_hunt fuzz, clippy deny lints, catch_unwind guard (E07-009) |
| F7 | Shared-process-state test flakes | d71143e4d8, 7091cb6b8c, 5b087699be, 18c5420039 | INFERRED | separate binaries, locks, nextest gpu group, measured rates |
| F8 | Platform-only breakage invisible on Linux-only PRs | ee3ebfa748, 79a33dae9c, 184c226a76 | INFERRED | `full-ci` label, platform path filter (01a63dee89) |
| F9 | Generated artefacts going stale | 3c44319455 (scorecard 192 vs 193), 0b5803500c/ed6f989bc6/9d3447b153 (regenerate after merges) | INFERRED | CI staleness gate. Re-generation in the manual merge queue |
| F10 | Merge-conflict casualties in shared docs | 8601a7b170 (conflict markers committed), 0eb6ba9dea | INFERRED | ad hoc fixes only. No mechanism found |
| F11 | A fix that regresses an untested environment | 1253e79d68 (SMB) after #8034, 0b779b4fec follow-up | INFERRED | error-classification tables. Fault injection |
| F12 | Gate tightening causes post-merge reds | 47d3dcde33, 06650357d8 after 604da9d06b | INFERRED | none beyond fix-main PRs |
| F13 | Doc drift, in both directions | 984bc5c715 (stale "missing" rows), `target-app-parity.md:646` vs 20783fdc70 | VERIFIED facts / INFERRED class | status lines and revision histories (rule `AGENTS.md:131-135`) |

---

## 10. Observed corrective mechanisms (timeline)

| Date | Mechanism | Type | Source |
|---|---|---|---|
| 10-04 | rule 9 never panic. panic_hunt fuzz. never-crash steering + 11-PR sweep. forbid unsafe. catch_unwind guard | rule + check + campaign | ed0b99964d, bf111b524e, 50a27e6c74, ab3ab92b4a |
| 10-04 | workspace rustfmt + blame-ignore | campaign | f7eb6ea9e7, 574d4fe7da |
| 10-05 | honest parity assessment. "where we stand". no-Tauri rule | doc correction + rule | 20783fdc70, 433b84fae7, 10203e7a60 |
| 10-05 | scorecard with prefs audit (dead settings counted) | check/metric | 0f955e6c82 |
| 10-07 | main CI runs no longer cancelled. Linux-only PRs | CI change | 01a63dee89 |
| 10-10 | nextest `gpu` test group | check | 3092d3b6f9 |
| 10-11 | panel buttons must route via command ids (`xtask panel-commands`) | check | 4165c57f92 |
| 10-18 → | integration batches by maintainers | process | 5c89f16b60 … 6b0f7762e1 |
| 10-18 | CodeRabbit appears (first commit mention) | review bot | `git log main --grep=CodeRabbit` (earliest 10-18). 311 "CodeRabbit review" commits |
| 10-21 → 10-27 | SonarCloud + deny complexity lints | check | 8e518d8169, 604da9d06b |
| 10-25 | regression-test backfill | test backfill | 72e11802d4 |
| 11-06 | shared house rules (check-then-claim, report only what ran, review the diff, better PR) | rule | 7d8648dfcb |
| 11-06 | GPU tests on lavapipe, fail if skipped | check | 2ff8f419cb |
| 11-08 → | manual "(merge queue)" re-merge before merge | process | fda05f7b02 |

---

## Open questions / uncertainties
- Reasons for the integration-batch-8 reverts (#9455, #9454, #9183, #4573, #1199) are not in the commits. PR #9386's description was not fetched. This could be checked with WebFetch on pull/9386.
- Whether branch protection requires up-to-date branches. GitHub settings are not visible from git. "(merge queue)" commits suggest a manual practice, not a setting.
- The source tool behind the `Finding: <uuid>` trailers is unnamed.
- Causality for the never-crash trigger (issues #7, #16, #17 → rule 9) is inferred from timing only.
- Fix-type percentages depend on subject conventions that changed (squash → merge commits) in late October. Treat them as indicative only.
- 40/59 fix-main commits carry AI trailers. Absence of a trailer is "unknown", not "human". Since 11-06 house rule 15 discourages attribution in PRs (E02-011), which may depress later trailer rates.
- Original commit d3e8039f76 (reverted by b390bef334) is not in the clone. Δt unknown.
- WebFetch results are small-model summaries (lower fidelity). Quotes from them are short and unverified against raw HTML.

## Leads for other streams
- The ticket-craft bot relays Discord reports into issues and auto-labels priority (issues #7858, #9440). This is relevant to the issue-intake / bot-ecosystem stream.
- `docs/egui-037-migration-plan.md` references `plan-reviews/photocraft-v1.md` "independent review" and "evidence ledger". This is a multi-agent planning/review practice (E02 / planning stream).
- 21 `fix/sec-*` branches remain ahead of main at the pin. Their merge status (PRs open/closed) is a lead for the PR-lifecycle stream.
- `agent-346022` and `ebosido444-ai` are author handles that look like agents (602344bae0, 1a86826ab7). This is an attribution lead, but not evidence of AI use by itself.
- The 10-05 parity-number discrepancy (55–70/20–35 vs 60–70/25–35) is relevant to the metrics-integrity stream.
- integration-batch-8 merged 37 PRs in one merge (cece50d513). This is a throughput/review-depth lead for E05-035.

## Methods-relevant takeaways
- Keep main's CI runs uncancelled. Otherwise red main is invisible. The project lost most of a day's main runs to cancellation (E07-004).
- Expect semantic merge skew to dominate when many agents land in parallel. Use a real or manual merge queue, or staging integration batches. Here, batches coincided with zero red-main commits in W43–W45 (E07-002, E07-003, E07-005).
- Turn agent failure modes into ratcheting metrics instead of prose rules. Examples: "settings that do nothing" 66→8, parity floors (E07-014, E07-013).
- Distrust wiring metrics. "625/625 live" coexisted with broken basics in day-1 user feedback. Pair coverage numbers with behaviour tests (E07-013).
- Make CI fail when tests skip. 57 GPU checks were silently passing on a GPU-less runner (E07-018).
- Ask for "test fails without the fix" evidence and spot-check with mutation. Schedule periodic backfill sweeps for fixes merged without tests (E07-015, E07-018).
- Run a never-crash campaign early as a short, crate-partitioned sweep, backed by deny lints, a command fuzzer and a last-resort guard. Each crash fix carries a test that panicked before (E07-009).
- Put flaky-test fixes in code (locks, process isolation, condition polling) and record before/after failure rates in the commit (E07-007).
- Tightening lint gates mid-flight causes post-merge reds from combinations. Budget for fix-main PRs or check gates in the queue (E07-005, E07-011).
- Avoid "every PR edits the same status line" doc conventions. They create conflict-marker casualties (E07-020).
- Durability fixes need environment-diverse fault injection (SMB, permissions), or they regress real users (E07-021).
- When adding consistency tests for shared catalogs and registries, duplicate entries from parallel work become cheap one-line fixes instead of silent bugs (E07-019).
