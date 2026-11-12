# E09 — Feature case-study traces

Stream E09. Upstream clone pinned at `main` = `74330157cb` (2026-11-12). All shas are from
`/tmp/.../scratchpad/upstream/photocraft`. Times are given as recorded by git (author date `a:`,
committer date `c:`) and converted to UTC where an elapsed time is computed. "WF" = WebFetch summary
of a GitHub page, accessed 2026-11-12, lower fidelity.

Method notes (apply to all cases):
- `git log --all --grep`, `-S`/`-G`, `git log -- <path>`, `git branch -r --contains`, `git for-each-ref refs/pull`,
  `git merge-base`, `git rev-list --first-parent origin/main` (3,475 first-parent commits out of 12,396 total).
- "Squash" = main commit with one parent, committer `GitHub`, PR number in subject. "Rebase-merge" = one parent,
  committer = the merging human, branch tip absent from main but an equal-subject commit present.
- Test names were extracted with `git diff <mb> <head> | grep -A1 '^\+\s*#\[test' | grep -o 'fn [a-z_0-9]*'`.
- AI attribution is reported **only** as written in trailers/author fields/branch names (brief rule 4).

---

## Case A — MCP server / control protocol

### Commit-level table

| sha | date (as recorded) | author | AI trailer as written | branch / PR | files touched | tests added/changed |
|---|---|---|---|---|---|---|
| 16941f7198 | 2026-09-30 05:02 -0400 | Brandon Thomas | none | direct (root "one-shot", 241 files, +42,241) | `docs/control-protocol.md` (+50), `apps/photocraft/src/control_server.rs`, `crates/ui-egui/src/control.rs` | none specific |
| ae92ac20bf | 2026-09-30 09:37 -0400 | Brandon Thomas | none | direct ("continued wip", 181 files, +37,990) | new `crates/automation/` (`server.rs` 627, `bridge.rs` 137, `headless.rs` 157), `apps/photocraft-cli/src/lib.rs`, `docs/control-protocol.md` | `crates/automation/tests/mcp.rs` (+411): in-process server over tokio duplex; "Bridge mode against a fake control server"; `bridge_rejects_non_loopback` |
| cfecebbcfb | 2026-10-01 21:40 -0400 | Brandon Thomas | `Co-Authored-By: Claude Opus 5.5` | direct | `crates/automation/src/rpc.rs` (+349), `server.rs`, `docs/control-protocol.md` (+30) | `tests/mcp.rs` (+25) |
| 8a2f31c2c4 | 2026-10-03 | storybored379 | — | PR #16 | MCP: panicking command no longer wedges headless session | (see sha) |
| 1d832d3e84 | 2026-10-04 13:25 -0400 | Brandon Thomas | `Co-authored-by: Claude Opus 5.5` | PR #38 (`pr/never-crash-automation`) | automation + CLI panic-free | — |
| 55054b5fcc, 7eb3b2e072, 8f0f95959d | 2026-10-07 | BFlat | — | PRs #439, #546, #548 | user-report fixes (#415, #503–#514): batch `wait`, serve stdio survives a bad line, MCP `ui_pointer` button | — |
| 209831f77e / 07dafe23e0 | a: 2026-10-08 21:41 -0400 | harrisonoconnorhover | none | `community/1533-mcp-preview-index`, PR #1533 head = 07dafe23e0 | `server.rs` (+16), `docs/control-protocol.md` (+2) | `tests/mcp.rs` (+54): `bridge_previews_reject_document_indices`, `headless_previews_preserve_document_indices` |
| 0e0311d245 | c: 2026-10-09 11:12:46 +0700 (BFlat) | harrisonoconnorhover | none | rebase-merge of #1533 onto first-parent main | same | same |
| cff8daf185 (cherry-pick of 7406c26bd4 from `claude/integ-batch-7`) | c: 2026-10-09 11:12:46 +0700 | Claude | `Co-Authored-By: Claude Opus 5.5`, `Claude-Session: …session_01UHgFEH…` | landed with #1533; also 5774989896 on `community/1533-…` | `tests/mcp.rs` (1 line) | clippy 1.99 `as_chunks` in preview pixel check |
| 15e35cf605 | 2026-10-09 06:54 -0700 | storybored379 | `Co-Authored-By: Claude Opus 5.5` | squash, PR #1668 | creates `docs/mcp.md` (+64), `server/conventions.rs`, `progress.rs`, `transport.rs`, `workspace.rs` | `tests/mcp_wire.rs` (+147, raw JSON-RPC line transport: `malformed_line_recovers_and_modern_lists_are_complete`), `tests/mcp.rs` (+60), `video_cmds/tests.rs` |
| 7ba589e01c | 2026-11-05 | Khawar Zamman Wani | — | PR #8132 (#8129) | MCP headless waited commands as jobs | adds `crates/automation/tests/mcp_wait.rs` |

### E09-A-001 — The control protocol was specified as a doc inside the one-shot root commit, and MCP was declared a future wrapper of it
- Label: VERIFIED
- Source: 16941f7198:docs/control-protocol.md:3,15 (2026-09-30)
- Quote: "Each request is one JSON line" … "An MCP server will wrap this same protocol (milestone M11)."
- Notes: spec = method list + engine-command table; no separate requirements doc. The MCP server (rmcp) arrived 4h35m later in ae92ac20bf, with a 411-line test file — so spec, implementation and tests all came in large unattributed bulk commits (see E01 for one-shot genesis).

### E09-A-002 — MCP verification is in-process client tests plus a raw wire test, not golden transcripts
- Label: VERIFIED
- Source: ae92ac20bf:crates/automation/tests/mcp.rs:1 ("Spin the MCP server in-process (tokio duplex), call tools as a client."), :295–298 ("Bridge mode against a fake control server"); 15e35cf605:crates/automation/tests/mcp_wire.rs:1 ("Exercise the actual line transport, including recovery and modern result fields.")
- Method: `git ls-tree -r origin/main | grep -i mcp`; no `*.golden`/transcript fixtures found for MCP. At main, `tests/it/mcp.rs` has 53 `#[...]` attribute lines (`grep -c '#\['`).
- Notes: The bridge to the running app is tested against a fake control server, not the real GUI.

### E09-A-003 — The MCP evolved by cross-project "shared conventions" and by user-report batches
- Label: VERIFIED
- Source: commit 15e35cf605 (2026-10-09, PR #1668) body: "The MCP server follows the crafts' shared conventions (FilmCraft #28): core tools incl. render_preview, … strict argument keys (-32602), … -32700 recovery from malformed JSON lines."; commits 55054b5fcc/7eb3b2e072/8f0f95959d (2026-10-07) cite user issues #415, #503–#514.
- Method: `git log origin/main -i --grep=mcp` → 135 commits; `git log origin/main -- docs/mcp.md` → 14 commits; `-- crates/automation` → 431 commits.
- Notes: spec source shifts from in-repo doc (A-001) to a sibling project's issue (FilmCraft #28) to user reports.

### E09-A-004 — The community MCP fix #1533 landed in ~2.5 h, with a Claude integration-branch lint fix riding along
- Label: VERIFIED (times), INFERRED (that the Claude fix was produced while integrating batch 7)
- Source: 07dafe23e0 a: 2026-10-08T21:41-04:00 (= 01:41Z 10-09); 0e0311d245 c: 2026-10-09T11:12:46+07:00 (= 04:12Z) committer BFlat; cff8daf185 body "(cherry picked from commit 7406c26bd4…)", 7406c26bd4 is on `origin/claude/integ-batch-7` (a: 03:32Z).
- Notes: elapsed first commit → merge 2h31m; follow-up (clippy) 0 min after (same push). Chain: Claude integration branch found clippy 1.99 failure → fix cherry-picked into community branch → rebase-merged by maintainer BFlat. Review path for #1533 not fetched.

### Case A summary
Spec: in-repo protocol doc (one-shot) → sibling-project conventions (FilmCraft #28) → user issues. Tests: in-process client tests from day 0 (ae92ac20bf), wire-level test added with conventions (#1668). Elapsed: doc to MCP server 4h35m; doc to `docs/mcp.md` 9 days.

---

## Case B — Community bug #1381 fixed by an AI-authored branch

Chosen over #1248/#1286/#1323 because it has a regression test, an issue thread and a PR page. All four are summarized for comparison.

### Commit-level table

| sha | date | author / committer | AI trailer as written | branch / PR | files | tests |
|---|---|---|---|---|---|---|
| 0582884a5f | 2026-10-08 20:49:46 +0000 | Claude / Claude | `Co-Authored-By: Claude Opus 5.5`; `Claude-Session: https://claude.ai/code/session_01UHgFEHEsefoQoBParH47JA` | `claude/fix-1381-ime-empty-preedit` | `crates/ui-egui/src/type_tool.rs` (+6) | `crates/ui-egui/src/type_tool_tests.rs` (+26): `empty_ime_events_never_delete_the_selection` |
| d92bb1347b | 2026-10-09 00:24:57 +0000 | Claude | — | same branch; = `refs/pull/1421/head` | merge of `origin/main` (parents 0582884a5f, d2ad238e82) | — |
| c1cb455c7a | 2026-10-09 08:08:01 +0700 | BFlat / GitHub | `Claude-Session: …01UHgFEH…`, `Co-authored-by: Claude` | squash of PR #1421 onto main | same 2 files | same |

Sibling Claude fixes, same session id `session_01UHgFEH…` (VERIFIED, `git show`):

| issue | branch commit (UTC) | main squash (PR) | elapsed | regression test in same commit |
|---|---|---|---|---|
| #1248 | 345c28130f 10-08 19:26 | 88a47dc7c7 (#1392) 10-09 00:37Z | 5h11m | yes: `clipping_masks_apply_to_every_selected_layer` (`crates/engine/src/tests.rs`) |
| #1286 | f97318d0bb 10-08 18:08 | 3e8d788441 (#1331) 10-08 18:51Z | 43m | yes: `edit_menu_cmds/tests.rs` (+24) |
| #1323 | 988ad9558a 10-08 18:09 | 437b25bea9 (#1332) 10-08 18:52Z | 42m | **no** (only `transform_tool.rs` changed) |
| #1381 | 0582884a5f 10-08 20:49 | c1cb455c7a (#1421) 10-09 01:08Z | 4h18m | yes |

### E09-B-001 — Commit message structure of the Claude-authored fix branches is fixed and narrative
- Label: VERIFIED
- Source: commit 0582884a5f (2026-10-08)
- Quote: "Fix #1381: selecting type on Wayland no longer deletes it" / "…With nothing being composed, ime_update took that as \"replace the selection with nothing\" and deleted the selected text."
- Notes: pattern (all four): subject `Fix #N: <user-visible outcome>`; body = symptom → root cause → new behaviour (and Photoshop parity reference in #1248/#1286/#1323); trailers `Co-Authored-By: Claude Opus 5.5` + `Claude-Session`. No "Tests:" line; the test is in the diff. The code comment also cites the issue ("deleting the text as it was selected (#1381)", 0582884a5f:crates/ui-egui/src/type_tool.rs).

### E09-B-002 — Issue → diagnosis → PR → close was run by the maintainer account via Claude Code within ~1 day, without a human review
- Label: VERIFIED (WF)
- Source: https://github.com/storytold/photocraft/issues/1381 and /pull/1421 (WF, accessed 2026-11-12)
- Data: issue opened 2026-10-08 by hash-mc ("Ctrl + A deletes the text", Kubuntu Wayland); maintainer bflatastic diagnosed "empty preedit events on Wayland" in a comment marked "Generated by Claude Code"; PR #1421 opened by bflatastic, "No reviews", "4 of 7 checks passed" at merge; closed 2026-10-09 "Fixed on main by #1421" (also Claude-generated comment).
- Notes: the author field `Claude` + PR opened by human account + merge by the same human is the review path. Contrast with #1323 shipped with no test.

### E09-B-003 — The task premise "integrated via `claude/integ-batch-N`" is not supported for these four fixes
- Label: VERIFIED
- Method: `for i in 1..11; git log --format=%s origin/main..origin/claude/integ-batch-$i | grep -E '1392|1421|1381|1248|1331|1332|1286|1323'` → no hits; `git branch -r --contains 0582884a5f` → only its own branch.
- Notes: each fix was its own PR, squash-merged by BFlat. `claude/integ-batch-1..11` (2026-10-08 18:12Z → 10-09 14:18Z, all authored `Claude`) are octopus-style integration branches of *community* PRs ("Merge pr/1487", "Merge #1024 (carry)", "Merge refs/tmp/p1572") plus fix-ups such as 94c003452f "Regenerate docs/scorecard.md (stale on main since #1084)" and 7406c26bd4 (clippy). See Case A-004 for one fix-up travelling to main.

### E09-B-004 — Follow-ups
- Label: VERIFIED / INFERRED
- Source: `git log origin/main -G'empty preedit|ime_update' -- crates/ui-egui/src/type_tool.rs` → only refactors after the fix (5c9192bbe2 egui 0.37 migration, d3b0a76c3f lint, 668009e152/428414a61a/36199e41c3 file moves). No IME-regression fix found.
- INFERRED follow-up for #1248: 77a258b9a0 (2026-10-15, Tanish Manku, #5868) "Release Clipping Mask takes the layers above" changes the same command's semantics; the link to #1248 is not stated in the commit.

---

## Case C — The "never crash" campaign (2026-10-04)

### Commit-level table (all author Brandon Thomas; all main commits are squashes, committer GitHub, 1 parent)

| PR | branch (= `refs/pull/N/head`) | branch tip a: (-0400) | main sha, c: | scope as written | trailer |
|---|---|---|---|---|---|
| trigger | — (direct) | — | bf111b524e 00:24 | "Fix panics on malformed params; add panic-fuzz harness" | `Co-Authored-By: Claude Opus 4.8` |
| #33 | `pr/never-crash-steering` de807bb785 | 10:50 | 50a27e6c74 11:14 | AGENTS.md section, `clippy.toml`, `unsafe_code = "forbid"` | `Co-authored-by: Claude Opus 5.5` |
| #34 | `-formats` f9535d6b6a | 11:59 | 69f0e25d5f 13:25 | psd, codecs, format, io | same |
| #36 | `-cms` d3b3e1ade2 | 11:59 | 48d1a4f9e5 13:25 | cms | same |
| #39 | `-core` 55566337b8 | 11:59 | 296ced38d6 13:25 | text, color, doc, paint, geom, raster, compose, vector | same |
| #38 | `-automation` a5dec21e97 | 11:59 | 1d832d3e84 13:25 | automation (MCP/RPC), CLI | same |
| #40 | `-algo-ui-misc` f15f593c4f | 11:59 | 91ef877f2f 13:26 | algo pyramids, ui-egui parity | same |
| #54 | `-engine` 4bd7f4eeb1 | 12:18 | 4218d07f40 13:26 | engine (20 `*_cmds.rs` files) | same |
| #55 | `-gpu` c98d1770e7 | 12:26 | f8f48db78a 13:39 | GPU compositor | same |
| #56 | `-algo` d712c8faa6 | 12:32 | 6dffa0894c 13:40 | algo | same |
| #57 | `-ui` b02141e00e | 12:43 | 86cc989e72 13:40 | ui-egui | same |
| #58 | `-guard` 63b589318a | 12:54 | ab3ab92b4a 13:40 | last-resort `catch_unwind` guard | same |
| #59 | `-ops` 83ab5a521a | 12:55 | 2e80c781ee 13:40 | ops: attribute only | same |

Tests in campaign commits (VERIFIED from `--stat`): #34 adds `crates/codecs/tests/malformed.rs` (+50) incl. `tiff_empty_sample_format_is_an_error`; trigger adds `crates/engine/tests/panic_hunt.rs` (+48) and `paste_with_malformed_center_does_not_panic`. #54/#58/#59 change no test files.

### E09-C-001 — Trigger: a fuzz harness that found panics, ten hours before the campaign; standard imported from a shared org repo
- Label: VERIFIED
- Source: commit bf111b524e (2026-10-04 00:24 -0400)
- Quote: "Rule 9 (no panic on input). Fixes found via fuzzing: … Tests: paste_with_malformed_center_does_not_panic (fast regression) plus tests/panic_hunt.rs, an opt-in (#[ignore], run --ignored) fuzz that dispatches every command with adversarial params"
- Also: 50a27e6c74 body "Standard: craftrules/standards/never-crash.md" — the rule text was authored outside this repo (`../craftrules`), not visible here.

### E09-C-002 — The rule change: "Never crash (outranks feature work)" added at the top of AGENTS.md golden rules
- Label: VERIFIED
- Source: 50a27e6c74:AGENTS.md (diff hunk @@ -39 +39 @@), still present at origin/main:AGENTS.md:103; condensed as rule 1 at origin/main:AGENTS.md:27
- Quote: "Don't ship a feature by adding a panic path; fix a crash before building on top of it." / "**Prove it.** Every crash fix comes with a small synthetic regression test that panicked before the fix."
- Notes: Rule 9 ("Never panic on input") pre-existed and was re-pointed. Cross-ref E02.

### E09-C-003 — The mechanical guard is clippy deny attributes per crate root, counted by the scorecard; `pr/never-crash-guard` is a runtime net, not a lint
- Label: VERIFIED
- Source: ab3ab92b4a body (#58): "Session::execute wraps a command's run in catch_unwind … a new crash_guard module installs a logging panic hook"; 50a27e6c74 `clippy.toml` "lets tests use unwrap/expect/panic/indexing"; origin/main:xtask/src/scorecard.rs:420 `const NEVER_CRASH: &str = "deny(clippy::unwrap_used";`, :424 `fn never_crash(root)` lists crate roots lacking it (added 0f955e6c82, 2026-10-05, #239); origin/main:docs/scorecard.md:15 "never-crash lints on 28 of 28 crates; panic_hunt present", :284–285 REL-1/REL-2.
- Method: `git grep -l 'deny(clippy::unwrap_used' origin/main -- 'crates/*/src/lib.rs' 'apps/*/src/main.rs'` → 28.

### E09-C-004 — Decomposition: 12 single-commit branches prepared in ~2 h, landed serially in 15 min as stacked squashes
- Label: VERIFIED (times), INFERRED (stacking: each branch's merge-base equals the previous landed main commit, e.g. `pr/never-crash-ops` mb = ab3ab92b4a = #58)
- Method: `git merge-base origin/main origin/pr/never-crash-*`
- Elapsed: steering tip 10:50 → last landing 13:40:43 = 2h50m. Each PR trailered Claude Opus 5.5; review path unknown (no PR page fetched for #34–#59).

### E09-C-005 — Results / follow-ups
- Label: VERIFIED
- Data: `git log origin/main --since=2026-10-05 -i --grep=panic | wc -l` → 180 commits; `--grep=crash` since 10-04 → 60; one later commit adopts the campaign name: 5049a1d062 (2026-10-08, Tanish Manku, #869) "Never crash on hostile numbers: LUT sizes, Quick Selection points, link group ids". Trailers on Brandon Thomas commits 2026-10-04: 54× `Claude Opus 5.5`, 2× `Claude Opus 4.8`, 61 without (`git log --format='%(trailers:key=Co-authored-by,valueonly)'`).

---

## Case D — PSD as an oracle/corpus-driven feature

### Commit-level table

| sha (main) | date | author | trailer | PR / branch tip | files summary | tests / oracle |
|---|---|---|---|---|---|---|
| f225c290cc, 11b175e22b | 2026-10-04 12:58 -0400 | Brandon Thomas | — | `fix/psd-adjustment-roundtrip` (unmerged tips) | vibA, blnc, blwh, phfl, mixr adjustment blocks | "Corpus: export round-trip step and pass floors" |
| 574d0d3d53 | 2026-10-05 08:01 -0400 | Brandon Thomas | — (squash; branch tip 15d63afbc7 has no body) | #195 / `feat/psd-tools-corpus` | `xtask/psd_tools.rs`, `xtask/psd-tools-corpus.sha256` (309 lines), `crates/io/src/*`, `crates/psd/src/layer.rs` | `crates/io/tests/corpus.rs` (465 lines changed), `corpus_regressions.rs` (+167), `compose/src/tests.rs`; MIXED floor = 133 |
| 1d9d92341f | 2026-10-05 10:52 -0400 | Brandon Thomas | — | #224 / `fix/psd-effects` | `compose/effects.rs`, `gpu/compose.wgsl`, `io/examples/oracle_diff.rs` | `compose/src/tests.rs` (+47), `gpu/tests/parity.rs` (+18); subject "(113 -> 118 oracle passes)"; floor 145 |
| 8bac8926a3 | 2026-10-05 11:48 -0400 | Brandon Thomas | — | #233 / `fix/psd-strokes` | stroke effects | floor 146 |
| 968baf639e | 2026-10-05 17:47 -0400 | Brandon Thomas | — | #190 / `feat/photoshop-oracle-corpus` | `.github/workflows/ci.yml` (+23, corpus job), `xtask/src/corpus.rs`, `corpus_pins.rs`, `pinned.rs`, `photoshop-corpus.sha256` (256), `psd-corpus.sha256` (170), `docs/development.md` (+74) | new `crates/engine/tests/photoshop_oracles.rs` (+133); floors PSD_TOOLS 229, PHOTOSHOP 126 |
| f54d605e2c | 2026-11-05 21:41 +0530 | Khawar Zamman Wani | — | #10307 | `xtask/src/psd_write_oracle.rs`, `xtask/psd-write-oracle/starter.json` | `apps/photocraft-cli/tests/it/psd_write_oracle.rs` |
| a0e7169ed7 → 50bad2e3e9; 9cebb79f31 … c17e1c4b69 | 2026-11-12 00:37Z → 06:45Z | Dylan M. Taylor | none | `switch-craft-psd` (3) / `switch-photocraft-psd` (8) | "Use craft-psd from craft-libs; remove crates/psd", scorecard regen, lockfile, "Match brush import cap to shared decoder budget", "xtask: update layer fixtures after PSD extraction" | fixture updates only |
| 74330157cb | 2026-11-12 02:53:54 -0500 | Dylan M. Taylor | none | squash #13414 (= pinned main HEAD) | 294 files, +755 / −25,930 | — |

### E09-D-001 — "Correct" is defined as matching Photoshop's own merged composite within 2/255
- Label: VERIFIED
- Source: 968baf639e:docs/development.md:180 "**Composite oracle:** a PSD's embedded merged image is compared with our compositor's output."; 968baf639e:crates/engine/tests/photoshop_oracles.rs:24 `const PASS_TOL: f32 = 2.0 / 255.0;` ("Within two 8-bit steps of Photoshop (same tolerance as the io corpus)"), and its header: "every smart object is re-rendered … every type layer is re-laid-out … then compared with Photoshop's merged composite."
- Notes: the oracle is the file's own embedded composite (produced by Photoshop), so no Photoshop install is needed in CI. The later write oracle (f54d605e2c:xtask/src/psd_write_oracle.rs:1) says "Photoshop is a separate judge".

### E09-D-002 — Correctness is enforced by ratcheting pass floors over pinned, sha256-verified corpora run in CI
- Label: VERIFIED
- Source: origin/main:crates/io/tests/it/corpus.rs:35 ("Raise the floors when they improve"), :151/:155/:159 (floors), :435 `assert!(pass >= src.pass_floor, …)`; 968baf639e:docs/development.md:318–322 ("a missing corpus is a failure … never a silent skip"; "The CI `corpus` job runs … on every PR and on main").
- Data (pass_floor history; method: loop over `git log -G'pass_floor' -- crates/io/tests/{,it/}corpus.rs` printing the constants):

| commit | date | author | MIXED | PSD_TOOLS | PHOTOSHOP |
|---|---|---|---|---|---|
| 574d0d3d53 | 10-05 | Brandon Thomas | 133 | – | – |
| 1d9d92341f | 10-05 | Brandon Thomas | 145 | – | – |
| 968baf639e | 10-05 | Brandon Thomas | 146 | 229 | 126 |
| 452672765d | 10-08 | BFlat | 146 | 229 | 133 |
| becc27ac1c | 10-13 | Timothy Daly | 146 | 236 | 145 |
| a62ef68ca2 | 10-14 | Timothy Daly | 148 | 249 | 185 |
| b526378de4 | 10-22 | David Mann | 148 | 249 | 190 |

  20 floor-changing commits; floors never decrease. Corpora: 256 own Photoshop-authored PSDs (storytold/photocraft-corpus), 170 psd-tools/ag-psd files, 309 psd-tools files (968baf639e:docs/development.md:299–301).

### E09-D-003 — Contributors report fixes in oracle units
- Label: VERIFIED
- Source: subjects 1d9d92341f "(113 -> 118 oracle passes)"; 4c450b3879 (10-14, Timothy Daly) "(seven Lab oracles pass)"; 1e6f565a7b "(14 oracles pass)"; 00c16f2c6d "(six oracles pass)".
- Notes: the oracle count functions as the requirement and the acceptance metric at once.

### E09-D-004 — Extraction to craft-psd (#13414) was done in one ~7 h branch with no AI attribution and no PR body beyond the squash list
- Label: VERIFIED
- Source: a0e7169ed7 a: 2026-11-12T00:37:34Z; 74330157cb c: 2026-11-12T02:53:54-05:00 (07:53Z). Squash body lists the seven branch commits. `%(trailers)` empty on all branch commits.
- Notes: elapsed 7h16m; `crates/psd` removed (−25,930 lines), behaviour pinned by the corpus floors remaining in photocraft (INFERRED: the floors are the safety net for the swap; no commit says so).

### Case D summary
Spec = Photoshop-authored files + their embedded composites; decomposition by feature group (effects, strokes, type, adjustments) each reported as oracle-pass deltas; floors ratchet; CI corpus job. The `fix/psd-*` branch tips carry no message bodies, so method is visible only in tests/docs.

---

## Case E — egui 0.37 migration (planned, multi-step)

### Commit-level table

| sha | date | author | AI attribution as written | branch / PR | summary | tests / verification stated |
|---|---|---|---|---|---|---|
| 14c059c971 | 2026-10-25 02:14 +0100 | skylartaylor | none in trailers; branch `codex/…` | `codex/egui-037-photocraft-20261023` (PR #9363) | "M0.37: migrate PhotoCraft to egui 0.37"; 331 files, +15,728/−3,374; **adds `docs/egui-037-migration-plan.md` (1,632 lines)** | body: "All nine CI stages passed: 11,580 passing test executions, zero failures and 91 ignored across 93 summaries. Native/browser acceptance and paired app performance remain open." |
| c6d87dc1ea | 10-25 03:41 +0100 | skylartaylor | none | same | "reconcile current PhotoCraft main and qualify CI" (merge) | — |
| 47d552dced | 10-25 06:55 +0100 | skylartaylor | none | same | reconcile upstream modal/autosave changes (merge) | — |
| b1f73ab821 | 10-25 14:33 -0400 | Dylan M. Taylor | none | same | merge origin/main | — |
| 6e4f85e161 | 10-25 14:37 -0400 | Dylan M. Taylor | "Generated with Codebuff" / `Co-Authored-By: Codebuff` | same | "CodeRabbit review follow-ups on the migration": accessible names, eager font order | — |
| 54a0bc46fa | 10-25 14:48 -0400 | Dylan M. Taylor | none | = `refs/pull/9363/head` | rustfmt | — |
| 5c9192bbe2 | c: 2026-10-25 13:04:35 -0600 (GitHub) | skylar taylor-barrick | squash body: `Co-authored-by: Dylan M. Taylor`, `Co-authored-by: Codebuff` | main, 1 parent | squash of #9363 | fixtures `apps/photocraft/tests/fixtures/ui-0.14/0.15/0.37.ron`; `crates/engine/src/tests.rs` (+22) |
| 6f6e0d1793 … 3f2229b9ad (12 commits) | 10-25 20:07 +0100 → 10-26 06:42 +0100 | skylartaylor / skylar taylor-barrick | none | `codex/egui-037-photo-followup-20261025` = `refs/pull/9518/head` | "Reconcile the published squash merge while preserving qualified follow-up fixes", font validation, coverage workflow pins, "cover CJK fallback and font cache edge cases" | coverage + font tests |
| d641b96a52 | 2026-10-26 13:16 -0600 | skylar taylor-barrick | — | merge commit, PR #9518 | 14 commits merged | — |

### E09-E-001 — The plan was committed with the first migration commit and carries Codex-workspace paths
- Label: VERIFIED (authorship/paths); INFERRED (that a Codex agent drafted the plan — only the branch prefix and paths support it)
- Source: `git log --all -- docs/egui-037-migration-plan.md` → earliest 14c059c971 (skylartaylor); 14c059c971:docs/egui-037-migration-plan.md:45 "checkout `/home/codex/work/CraftApps/egui037-migration-20261022/egui`", :277 "`/home/codex/work/ssd2/task-evidence/egui037-migration-20261022/lifecycle-source-audit.md`", :40 "Those revisions are **historical, read-only evidence**. They are not accepted revisions".
- Notes: plan structure: decision summary (§1), dependency model and rollback (§2), source audit (§3), breaking changes mapped to files (§4), E1–E21b fork-patch audit (§5), winit patch audit (§6), craft-libs PR 199 (§7). Lines :106–107 require paired same-machine perf comparisons and forbid using the committed macOS `perf/baseline.json`. Plan later edited by others through 90d1468a7d (2026-11-07, Qingfei).

### E09-E-002 — Verification: full local CI-stage run + CodeRabbit + human approval; explicit "open gates"
- Label: VERIFIED (commit body), VERIFIED-WF (PR page)
- Source: 14c059c971 body (above); https://github.com/storytold/photocraft/pull/9363 (WF): "all nine local CI stages passed, with 11,592 passing test executions" (differs from the commit's 11,580 — later re-run); open gates "native GUI/IME testing, PRIMARY clipboard, packaged browser/runtime checks, and paired performance acceptance"; "human review and a human merge are required"; CodeRabbit 7 actionable comments (accessibility/font order) then 1; dylanmtaylor approved twice; "14 of 16 passed" checks.
- Notes: WF says "merge commit"; git shows 5c9192bbe2 has one parent and committer GitHub → squash (git evidence preferred).

### E09-E-003 — Tool attribution is mixed: `codex/` branch, Codebuff trailer, no Codex/Claude trailer
- Label: VERIFIED
- Source: 6e4f85e161 body "Generated with Codebuff / Co-Authored-By: Codebuff <noreply@codebuff.com>"; `%(trailers)` empty on all skylartaylor commits.
- Notes: per brief rule 4 the only attributions are the branch name (`codex/*`) and Codebuff on one commit.

### E09-E-004 — Fallout: a dozen adaptation/regression commits in the following days
- Label: VERIFIED
- Method: `git log origin/main --since=2026-10-25T19:00 -i --grep='egui 0.37\|egui037\|M0.37\|0\.37'`
- Data: 8812fe1e73 + 178d6c2235 (David Mann, merge + rustfmt "the egui 0.37 merge"); ef20eca473, bcbf693cf6 (Hector Villarreal, 10-25, "Tests: egui 0.37's Id::unique", "Preset menus: egui 0.37's dropdown label"); 5295017732/ea0a447df1/c484971fdf (Khawar Zamman Wani, 10-26, "Adapt to egui 0.37 renames" ×3 on different branches); b078e0e8a6 (#9575, aiongg, "review follow-ups to the shared docking and egui 0.37 merges"); 73ac7d9a25 (10-28, David Mann) "Arabic layer names and title read right to left again on egui 0.37" (a regression); #9518 follow-up branch (12 commits).
- Elapsed: 14c059c971 (01:14Z 10-25) → squash (19:04Z) 17h50m; → #9518 merge (19:16Z 10-26) 42h; → RTL regression fix 73ac7d9a25 (10-28) ~3.8 days.

---

## Case F — Box blur performance (docs/box-blur-performance.md)

Chosen because the doc is the most complete before/after record with a review-driven correction; budget rows are explicit.

### Commit-level table (PR #10426, merged by 4ed05762c0 "Merge pull request #10426 from ebosido444-ai/perf/box-line-kernel", 2026-11-11 00:18:50 -0700, Tanish Manku)

| sha | a: / c: | author | trailer | files | tests |
|---|---|---|---|---|---|
| a616cda46c (parent, row-pass work, PR #10425 per WF) | a: 2026-11-06 02:59 +0300 | ebosido444-ai | none | `crates/algo` | "compare the row-pass outputs by bits, so a signed-zero regression fails" |
| f0a816f844 | a: 10-31 07:52 +0300 / c: 11-06 03:00 +0300 | ebosido444-ai | none | `crates/algo/src/fxutil.rs` (+99), **new `docs/box-blur-performance.md` (+145)** | `fxutil::tests::cols_match_the_strided_walk` (bit-exact vs old walk) |
| 7082689b38 | a: 10-31 08:38 / c: 11-06 03:00 | ebosido444-ai | none | fxutil.rs, doc (+28/−21) | timing harness fix |
| e5301fc35a | a: 11-01 13:58 / c: 11-06 03:00 | ebosido444-ai | none | — | "sweep the radii in the column-gather differential check" |

### E09-F-001 — Hypothesis stated as a cache-traffic model, with the equivalence oracle defined in the same commit
- Label: VERIFIED
- Source: commit f0a816f844
- Quote: "A column walk reads one sample per row at a stride of `w * n`, so every sample pulls its own cache line … 8x the image's traffic" / "`fxutil::tests::cols_match_the_strided_walk` compares every `f32` bit against the strided walk … and all 16 `bench_filters2` rows hash identically to the base tree."

### E09-F-002 — Benchmark method and numbers as recorded in the doc
- Label: VERIFIED
- Source: origin/main:docs/box-blur-performance.md:71–98 (§Timings), :133–141 (§Reproduce)
- Data: i5-10300H, Windows 11, rustc 1.98.1, median of 5 (base) / 3 runs; base tree = `origin/main` in a detached worktree; 6000×4000 RGBA8: Reduce Noise 2430.8 → 1638.3 ms (1.48×), Tilt-Shift 2161.0 → 1532.9 (1.41×), Relight 3285.7 → 2405.3 (1.37×), Oil Paint 1.04×, Lighting Effects 0.95×. Doc also lists "discarded variants" and a "What this does not fix" section (:103).

### E09-F-003 — Review caught a measurement bug that inflated a published number
- Label: VERIFIED (commit), VERIFIED-WF (who asked)
- Source: commit 7082689b38 "From review: `cols_timing` ran the strided pass and then the strip pass on the same buffer … the 324x324 window measures 1.45x, not the 1.89x the old harness reported."; https://github.com/storytold/photocraft/pull/10426 (WF): CodeRabbit asked for independent input copies (and Criterion — declined); FredApps asked for multi-radius/odd-width equivalence and hardware details; tanish2k09 requested changes (rebase on #10425, confirm the doc is wanted), label "waiting on author"; 19 checks passed.

### E09-F-004 — The budget is not met and stays non-enforced; the doc says so
- Label: VERIFIED
- Source: origin/main:perf/budgets.toml:647–663 (P66 Relight, P67 Reduce Noise: `issue = 211`, `budget_ms = 1000`, `enforce = false  # 3.7 s / 2.8 s measured 2026-10-22`); :5–8 header ("`enforce = false` marks a target the code doesn't meet yet … flip it to true in the PR that meets it"; "never invent a number"); docs/box-blur-performance.md:105–106 ("their `perf/budgets.toml` targets (1 s on 24 MP) are not reachable from a kernel change"); :19–20 "no `perf/budgets.toml` entry" changed.
- Perf-nightly: origin/main:.github/workflows/perf-nightly.yml:3–7,17 (`cron: "23 3 * * *"`, fixed macOS runner, regression = p50 +15 % vs `perf/baseline.json`; budgets.toml `regression_pct = 15.0`, `baseline_min_runs = 5`).
- AI attribution: none in trailers or (per WF) PR text; the handle "ebosido444-ai" is a name only → **unknown**.
- Elapsed: first authored 10-31 04:52Z → merge 11-11 07:18Z = ~11 d 2.5 h (rebased 11-06).

---

## Case G — Security-hardening findings with `Finding:` trailers

### Commit-level table (summary; all author Dylan M. Taylor; no AI trailer on any)

| group | shas (main) | a: | c: | PRs | CWE mix |
|---|---|---|---|---|---|
| first | 42d8aad56f | 10-21 21:44 -0400 | same | #8417, merge commit 9852baa4ba (10-22 19:27 -0400) | CWE-407 |
| burst of 25 | 7c78c951e4 … f65832931b | 10-21 21:47 → 22:43 -0400 | 10-22 07:10–07:12 -0400 (committer Dylan) | #8420–#8452 range (rebase-merged; e.g. #8452 head 0785fd574b) | CWE-407 ×11, CWE-400 ×9, CWE-770 ×3, CWE-409 ×1, CWE-789 ×1 (all 27: 407×12, 400×9, 770×3, 409×2, 789×1; `grep -oE 'CWE-[0-9]+' | uniq -c`) |
| last | ef4e13dc2d | 10-22 06:22 -0400 | 10-22 19:44 | #8505, merge ee0d23f77a | CWE-409 |

Example tests (VERIFIED, diff grep): ef4e13dc2d `crates/io/tests/it/svg.rs` (+46): `gzip_compressed_embedded_svg_decompresses_once_with_a_size_cap`, `resolve_data_rejects_nested_gzip_and_handles_text_plain_svgz`; 42d8aad56f inline `trailing_descriptor_applies_outsets_to_first_matching_slice`; f65832931b none (+11 in `pattern.rs`).

### E09-G-001 — 27 unique findings, one PR per finding, landed within ~22 h
- Label: VERIFIED
- Method: `git log origin/main --grep='^Finding:'` → 27; `--all` → 52 (pre-rebase PR-head copies + main copies); unique `Finding` values → 27; `git for-each-ref refs/pull` subjects `^security\(` → 36 PRs (#8417–#8452, #8504, #8505, #8938–#8958).
- Notes: subjects follow `security(<crate>): <change>`; body = mechanism + fix; final trailer `Finding: <uuid> (CWE-NNN)`.

### E09-G-002 — The producing tool is not named anywhere in the repo or PRs examined
- Label: VERIFIED (absence)
- Source: `git grep -n -iE 'Finding:|CWE-' origin/main -- '*.md'` → no hits; PR #8417 and #8452 (WF) cite only the UUID + CWE, "It doesn't name the scanner, audit tool, or AI agent". 0 of 27 messages contain Claude/Codex/Generated (`grep -ciE`).
- Notes: UUID-per-finding + CWE strongly suggests an external finding tracker (INFERRED, low confidence); attribution: **unknown**.

### E09-G-003 — Fix + test pattern and review
- Label: VERIFIED
- Data: 11 of 27 finding commits add a `#[test]` (`git show | grep -E '^\+\s*#\[(tokio::)?test'`). PR bodies list "Validation: `cargo fmt`, `cargo test -p photocraft-compose --lib pattern` (5 passed)" (#8452, WF). Review: CodeRabbit on each; #8452 approved by FredApps, CodeRabbit raised an unaddressed aggregate-memory concern; #8417 "No reviews", "15 of 21 checks passed" (WF).

### E09-G-004 — The later `fix/sec-*` branches are a different series without `Finding:` trailers
- Label: VERIFIED
- Method: `git log -1 --format='%(trailers:key=Finding)'` on all 20 `origin/fix/sec-*` tips → empty; commits dated 2026-11-03 → 11-11, e.g. 59158ffdf2 "fix(io): bound Krita default pixels, XMP nesting, XCF RLE runs, SVG DTDs …", 2be2838f79 "address review: budget packed depth-1 mask source plus output". Batching differs: these are multi-finding bundles per area (`sec-io-parser-bounds`, `sec-engine-misc2`) with "address review" commits; 18 of 20 tips are still ahead of main (`git rev-list --count origin/main..<tip>` > 0) at the pin.

---

## Case H — Artboards: a feature that needed repeated correction

(Flatpak self-update was considered: fc6fcf67d8 → Release 0.22.1 83ef781382 → c5ff2474b2 → squash eee667f1d9 "Fix Flatpak updates and bump to 0.23.1 (#13322)", all 2026-11-11, Dylan M. Taylor, no message bodies → thinner; artboards chosen.)

### Commit-level table

| sha | date | author | trailer as written | PR / branch | summary | tests added |
|---|---|---|---|---|---|---|
| 7488ab413d | 2026-10-09 03:22Z | Claude | `Co-Authored-By: Claude Opus 5.5`, `Claude-Session: …01UHgFEH…` | `claude/fix-1531-artboards` | "duplicate artboards beside the original, drag boards with the Move tool" | (see diff) |
| 3e8d54896d | c: 10-09 10:54 +0700 | BFlat / GitHub | `Co-authored-by: Claude` | squash #1584 | same | — |
| 5e6cfa425d, 2159f6e640, 508e137b4c | 10-31 17:02Z → 11-01 12:07Z | Mohamed Mahjoub | `Claude Opus 5.5` / `Claude` | PR #10512 (issue #10218), `feat/artboard-auto-nesting` | Move tool auto-nests layers into the board they're dropped on; "true, floored middle" | 8 tests incl. `a_layer_moved_onto_another_artboard_joins_it`, `prevent_auto_nesting_keeps_the_layer_in_its_board`, `move_tool_drag_onto_another_artboard_nests_the_layer_there` |
| 5829929e81, 01ca6a69a9, b15ac4b016 | 11-05 04:06–05:39 +0100 | FredApps | none | same PR | maintainer merges main; "Document the auto-nesting rule and exclusions" | — |
| b152f4175e | c: 11-05 06:18 +0100 | Mohamed Mahjoub / GitHub | `Claude Opus 5.5`, `FredApps` | squash #10512 | — | — |
| fda2e9feea … 713585646e (7) | 10-31 17:51Z → 11-02 22:24Z | Mohamed Mahjoub | `Co-authored-by: Claude` on all | PR #10538 (issue #8788), `fix/paste-between-artboards` | iterations: "copied layers and true middle", "locked boards and the placement midpoint", "floored placement middle, pastes join smaller boards", "keep a clipped paste's clipping on a board" | 12 tests incl. `paste_into_another_artboard_keeps_the_place_on_the_board`, `content_centred_just_left_of_a_board_is_not_placed_in_it`, `a_clipped_paste_joining_a_board_stays_clipped_only_over_a_layer` |
| ca151c6b84 | c: 11-05 04:55 +0100 | Mohamed Mahjoub / GitHub | `Claude`, `FredApps` | squash #10538 | — | — |
| e7b8c5a72d, e6060a8e15, 243e21ecda, c1c83a3715, 340ae577bd, 2bcb07f298 | 11-05 11:45 → 13:53 +0100 | FredApps | `Co-Authored-By: Claude Opus 5.5` on 5 of 6 | `fix/artboard-followups-10512-10538` = `refs/pull/11441/head` | "(#10512 follow-up)", "(#10538 follow-up)", clippy, two review-driven commits | 9 tests incl. `a_clipping_base_moved_onto_another_artboard_takes_its_clipped_layers`, `paste_into_a_position_locked_artboards_own_mask_keeps_the_place_on_the_board`, `a_clipped_paste_off_the_board_lands_above_it_unclipped` |
| 3e27572e7a | c: 2026-11-05 14:53:49 +0100 | FredApps / GitHub | `Claude Opus 5.5`, `FredApps` | squash #11441 | — | — |

### E09-H-001 — Root-cause notes in the follow-up are explicit about what the original PRs missed
- Label: VERIFIED
- Source: commit 3e27572e7a (squash body of #11441)
- Quote: "Dragging the base of a clipping mask onto another artboard left its clipped layers on the old board, released, covering that whole board (auto_nest moved the base alone and clip_group::settle released the layers that lost it)."; "the clip has no source board, so board_shift doesn't move it onto B, and layer_place::insertion_point only checked the content centre when the anchor was the board itself."

### E09-H-002 — Corrections came from three sources: in-PR iteration, a post-merge tester, and bot review rounds
- Label: VERIFIED (git), VERIFIED-WF (#11441 page)
- Data: #10538 needed 4 "Paste between artboards: …" correction commits before merge (git); #11441 description (WF): three problems "that skylartaylor found on `main` after #10512 … and #10538"; "Generated with Claude Code"; CodeRabbit 3 review rounds, 2+2 actionable comments → commits 340ae577bd, 2bcb07f298 ("Keep the board shift for a mask paste into a position-locked artboard; an off-board paste above an artboard lands unclipped"); 27 of 29 checks passed.

### E09-H-003 — Elapsed times and what stabilized it
- Label: VERIFIED (times), INFERRED (stabilization)
- Data: #10538 first commit 10-31 17:51Z → squash 11-05 03:55Z = 4 d 10 h; #10512 10-31 17:02Z → 11-05 05:18Z = 4 d 12 h; follow-up #11441 10:45Z → 13:53Z (12:53Z) = 2h08m; first commit → last follow-up = 4 d 19 h 51 m.
- Method: `git log origin/main --no-merges --since=2026-11-05T14:00 -i --grep='artboard\|board'` → no further fixes to auto-nest/paste-between-boards; later artboard commits are new features (8040809f1f Actions mapping, 08a908d3f5 Guide Layout, 1df674997b PDF isolation).
- INFERRED: stabilization came from the test-per-rule pattern (29 named behaviour tests across the three PRs) after a human found semantic gaps the tests had not encoded. Overall `git log origin/main --no-merges -i --grep=artboard` → 124 commits, 47 in the two weeks of 2026-W40/41.

---

## Cross-case comparison

| ID | Case | spec source | decomposition | who/what implemented (as attributed) | test evidence in same commit? | independent verification | review type | time to merge (first commit → main) | # follow-up fixes |
|---|---|---|---|---|---|---|---|---|---|
| E09-X-A | MCP / control | in-repo `docs/control-protocol.md` (one-shot) → FilmCraft #28 conventions → user issues #415, #503–#514 | bulk commits, then per-feature PRs | Brandon Thomas (no trailer in genesis; Claude Opus 5.5 from 10-01); storybored379 + Claude (#1668); harrisonoconnorhover (#1533) | yes (tests/mcp.rs from day 0; mcp_wire.rs with #1668) | in-process client + fake bridge server; no golden transcripts | #1533 rebase-merged by BFlat; others squash | doc→server 4h35m; #1533 2h31m | ≥3 user-report PRs on 10-07; Claude clippy fix cff8daf185 |
| E09-X-B | #1381 Wayland IME | community issue (hash-mc) | 1 commit + merge from main | author `Claude` (Claude Opus 5.5, session id) | yes (`empty_ime_events_never_delete_the_selection`); #1323 sibling: no | CI only (4 of 7 checks passed, WF) | none ("No reviews", WF); maintainer squash | 4h18m (siblings 42m–5h11m) | 0 found |
| E09-X-C | Never crash | shared standard `craftrules/standards/never-crash.md` + fuzz findings (bf111b524e) | 12 per-area branches, 1 commit each, stacked | Brandon Thomas, `Co-authored-by: Claude Opus 5.5` on all 12 (trigger: Opus 4.8) | partly (#34 malformed.rs; #54/#58/#59 none) | panic_hunt fuzz (opt-in), clippy deny attrs, scorecard count 28/28 | unknown (pages not fetched); serial squashes in 15 min | 2h50m | 180 later "panic" commits; #869 reuses name |
| E09-X-D | PSD oracle/corpus | Photoshop's embedded composites; own Photoshop-authored corpus | by feature group, each reported as oracle-pass delta | Brandon Thomas (no trailers), later Timothy Daly, others; extraction Dylan M. Taylor (none) | yes (floors raised in same commit) | pinned sha256 corpora, 2/255 tolerance, CI corpus job | squash; #13414 squash | #13414 7h16m | 20 floor raises; extraction fixtures |
| E09-X-E | egui 0.37 | 1,632-line plan in-repo (Codex-workspace paths) | plan §§ E1–E21b, W-patches; 2 PRs | skylartaylor (`codex/*` branch, no trailer); Codebuff on 1 commit | CI-stage summary in body; fixtures | 9-stage local CI run; open gates listed | CodeRabbit ×2 + human approval ×2 (WF) | 17h50m (#9363); 42h (#9518) | ~10 adaptation/regression commits incl. RTL regression 73ac7d9a25 |
| E09-X-F | Box blur perf | #211 budgets (`perf/budgets.toml` P66/P67) | row pass (#10425) + column pass (#10426) | ebosido444-ai (no trailer → unknown) | yes (bit-exact differential test, hash equality of 16 bench rows) | before/after on base worktree; perf-nightly | CodeRabbit + FredApps + tanish2k09 (changes requested) | ~11 d 2.5 h | 1 measurement correction (1.89× → 1.45×) + radius sweep |
| E09-X-G | Security findings | external finding IDs (UUID + CWE), tool unnamed | 1 PR per finding (27), ~36 `security(` PRs | Dylan M. Taylor (no AI attribution) | 11 of 27 | CI (incl. corpus, wasm, SonarCloud per WF) | CodeRabbit; FredApps approval on #8452; #8417 none | ~0.5–22 h (burst rebase 10-22 07:10) | later `fix/sec-*` series (Nov), mostly unmerged |
| E09-X-H | Artboards | issues #8788, #10218; post-merge tester report (skylartaylor) | 2 PRs + 1 follow-up PR | Mohamed Mahjoub + Claude trailers; FredApps + Claude Opus 5.5 ("Generated with Claude Code") | yes (29 named tests over 3 PRs) | human tester on main; CodeRabbit 3 rounds | maintainer squash (FredApps) | 4 d 10–12 h; follow-up 2h08m | 4 in-PR corrections + 1 follow-up PR (6 commits) |

---

## Open questions / uncertainties
- Review path for the 12 never-crash PRs (#33–#59), #1668, #1533, #195/#224/#190 not fetched (WebFetch budget); "unknown".
- The tool that produced the `Finding:` UUIDs (E09-G-002) is not stated anywhere examined.
- Whether a Codex agent wrote the egui plan rests only on the `codex/` branch prefix and `/home/codex/…` paths (E09-E-001).
- `ebosido444-ai` handle may indicate an AI-operated account; no explicit attribution → unknown (E09-F-004).
- PR #10426 has 7 commits per WF; only 3 are between the merge parents in git (the rest presumably landed with #10425). Not reconciled.
- WF reported #1421 and #9363 as merge commits; git shows single-parent squashes. Git evidence preferred.
- #1248 → 77a258b9a0 follow-up linkage is inferred only.

## Leads for other streams
- `claude/integ-batch-1..11` (2026-10-08/09, author `Claude`): AI-run integration of community PRs with fix-ups (94c003452f scorecard regen, 7406c26bd4 clippy) — maintainer-side agent pipeline (E05/E02).
- Model strings vary: `Claude Opus 4.8` (bf111b524e), `Claude Opus 5.5`, `Claude Sonnet 5.5` (cd40d7875e), `GPT-6 (Codex)` (7fd610741b), `Codebuff` (6e4f85e161).
- "crafts' shared conventions (FilmCraft #28)" and `../craftrules/standards/never-crash.md`: cross-repo standards (org-level practice).
- Only 3,475 of 12,396 main commits are first-parent: heavy merge-commit integration later (e.g. "Merge approved PhotoCraft PR #5744" d34c7a92e0).
- `xtask/src/scorecard.rs` turns rules into counted metrics (never-crash coverage, parity count).

## Methods-relevant takeaways
- Turn a rule into a counted metric: never-crash deny-attribute coverage is computed by the scorecard (E09-C-003) — transferable as "lint coverage as a tracked number".
- External oracles + ratcheting floors define "correct" for format work without a human judging pixels (E09-D-001, D-002, D-003).
- A campaign can be decomposed into one-commit, per-crate branches landed serially in minutes when each is mechanical (E09-C-004).
- Agent-authored bug fixes carry a fixed message shape (symptom → root cause → behaviour) and a session-link trailer, giving traceability back to the agent session (E09-B-001).
- Same-commit regression tests were the norm but not enforced: #1323 shipped without one, and 16 of 27 security fixes added no `#[test]` (E09-B table, G-003).
- Perf claims are recorded in per-change docs with hardware, method, base-tree reproduction and "what this does not fix"; reviewers caught a harness bug that changed a published number (E09-F-002, F-003).
- Budgets that are not yet met are kept visible as `enforce = false` with a measured note, never deleted (E09-F-004).
- Large migrations used a committed plan with explicit open acceptance gates, and the PR stated what it did not claim (E09-E-001, E-002).
- Post-merge human testing still found semantic gaps in agent-assisted features that had many tests; the follow-up encoded each gap as a named test (E09-H-002, H-003).
- AI bot review (CodeRabbit) was used on most PRs examined and drove real changes (E09-E-002, F-003, H-002), but some PRs merged with no human review and failing checks (E09-B-002).
