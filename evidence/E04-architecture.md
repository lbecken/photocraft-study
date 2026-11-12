# E04: Architecture and agent-facing interfaces

Stream E04. Upstream clone pinned at `main` = `74330157cb` (2026-11-12). `U` below means the
upstream clone at `/tmp/claude-0/-home-user-photocraft-study/7ff807c1-b52f-5813-9884-82f19c193950/scratchpad/upstream/photocraft`.
Scratch scripts are in `.../scratchpad/work/E04/` (`count.py`, `log.txt` = `git log main --format=%H%x01%ad%x01%an%x01%B%x02`).
HEAD file citations use `HEAD:path:line`. "Dev agent" means an AI agent that develops or tests PhotoCraft.
"End-user agent" means an agent that drives the shipped product.

This file does not repeat material that is already elsewhere:
- the gate table for `cargo xtask ci` is in **E05 §0.2** and E05-016;
- the history of AGENTS.md rules is in **E02** (E02-002, E02-005);
- the one-shot inventory is in **E01** (E01-002, E01-006).

## 0. Summary tables

### 0.1 Item status

| # | Item | Exists (path) | First introduced | Size or shape at HEAD |
|---|---|---|---|---|
| 1 | Workspace: 24 crates, 4 apps, xtask | VERIFIED `HEAD:Cargo.toml:3` `members = ["crates/*", "apps/*", "xtask"]` | 16941f7198 2026-09-30 (14 crates, 3 apps) | 24 crates, 4 apps; ~18,030 test attributes, ~1.02 M lines of `.rs` (E04-004) |
| 2 | Headless engine | VERIFIED `crates/engine` has no egui, winit or wgpu dependency | 16941f7198 | 4,452 test attributes; tests build `Session::new()` directly |
| 3 | Command registry | VERIFIED `HEAD:crates/engine/src/cmd.rs:15` `pub struct CommandSpec` | 16941f7198 (`commands.rs`, 837 lines) | ~76 ids on day 1, ~805 at HEAD (regex estimate, E04-010) |
| 4 | Control protocol, CLI, serve, plugins | VERIFIED `docs/control-protocol.md`, `apps/photocraft-cli/src/args.rs:33-40`, `crates/plugins` | control 16941f7198; plugins 7a5c1930b3 2026-10-04 | control-protocol.md grew from 50 to 840 lines; CLI has 8 subcommands |
| 5 | MCP server | VERIFIED `crates/automation/src/server.rs` (rmcp) | ae92ac20bf 2026-09-30, 17 tools | 26 tools; headless and bridge modes |
| 6 | testkit and deterministic tests | VERIFIED `crates/testkit` (356 lines) | 16941f7198 (1-line stub) | GPU lock, perf, sweep. No golden images. kittest harness, lavapipe CI |
| 7 | Oracles and corpora | VERIFIED `xtask/*.sha256` (10 files), `xtask/src/psd_write_oracle.rs`, `crates/gpu/tests/it/parity.rs` | corpus 968baf639e 2026-10-05; GPU parity ae92ac20bf | 1,044 hashed corpus files; 78 GPU-vs-CPU parity tests |
| 8 | Mechanical architecture checks | VERIFIED `xtask/src/layers.rs`, `panel_commands.rs`, `clippy.toml`, workspace lints, CI source check | layers 16941f7198 (in CI on day 1) | 15 xtask subcommands (E04-030) |
| 9 | Scorecard and perf budgets | VERIFIED `scorecard/*.toml` (8 files), `perf/budgets.toml`, `docs/scorecard.md` | 0f955e6c82 2026-10-05 | 166 checklist items; 88 perf scenarios, 0 enforced |

### 0.2 Does the mechanism help agents develop or test PhotoCraft?

Key to the columns:
- **Documented for dev agents**: a primary doc tells developers or agents to use it while building or testing.
- **Observed in history**: commits, tests or PRs show the project using it that way.
- **Hypothesized only**: neither of the above.

| Mechanism | Documented for dev agents | Observed in history | Verdict |
|---|---|---|---|
| Control channel `--control` + `ui.screenshot` / `ui.pointer` | YES: AGENTS.md rule 6 since day 1 (E04-020) | YES: PR #7374 (Claude Code) checked a change through `ui.pointer`+`ui.screenshot` (E04-024); README images rendered this way (E04-022) | documented + observed |
| Offscreen `snapshot` example (drives control-protocol scripts) | YES: AGENTS.md rule 6 at HEAD; contributing.md (E04-021) | YES: c080ed3e72 "Snapshot-verified." (Claude Opus 4.8 trailer); d59d2b509f; tone-targets-validation.md (E04-024) | documented + observed (few commit-level traces) |
| `control::handle` inside kittest UI tests | Partly: development.md:469 says "screenshot checks through the control channel" | YES: 32 files under `crates/ui-egui/tests` and 71 `*tests*.rs` in `src` call it (E04-023) | documented + observed |
| CLI as a test harness | Partly: development.md › PSD write recipes | YES: `xtask psd-write-oracle` drives `photocraft-cli`, but CI does not run it (E04-041) | observed (manual) |
| MCP server | NO for dev agents. It is documented for end-user agents and verified by `agent_tasks` tests | Tests drive MCP like an agent would (E04-026); no evidence that dev agents verify their own work over MCP | product feature; its own acceptance tests |
| Enumerable command registry | YES: AGENTS.md rule 9 + `panic_hunt` (E04-012) | YES: `panic_hunt` fuzzes every command; part of the CI gate (E05 §0.2) | documented + observed |
| `xtask layers` | YES: AGENTS.md §2, §5 | YES: in CI since day 1 (E04-031) | documented + observed |
| `xtask panel-commands` | YES: AGENTS.md §5 | YES: CI gate; added by a Claude-co-authored commit (E04-032) | documented + observed |
| Scorecard / parity checklist / FLOOR | YES: AGENTS.md §4 "Picking work" | YES: `scorecard --check` is in CI; FLOOR test (E04-050) | documented + observed |
| Perf budgets | YES: AGENTS.md §5 | Partly: 0 of 88 budgets are enforced (E04-051) | documented; enforcement weak |
| `tests/interactions` JSON scenarios | NO (development-only runner; "Automated execution needs a separate shared workflow") | NOT in CI (E04-025) | exists, not used in CI |
| `scripts/ci-gpu-lavapipe.py` | Development.md: yes, as a CI determinism measure | YES: CI gate command (E04-037) | domain CI mechanism; agent link only hypothesized |
| Golden-image / `testkit::assert_image_eq` (in the plan) | Plan only (day-1 architecture §13) | NOT implemented: no `assert_image_eq`, no `xtask bless` (E04-035) | plan never realised |

## 1. Workspace and modularity

### E04-001 — Workspace layout at HEAD
- Label: VERIFIED
- Source: `HEAD:Cargo.toml:1-4`; `ls crates apps`
- Data: 24 crates: affinity algo automation cms codecs color compose doc engine format geom gpu io ipp ops paint plugins raster raw tablet testkit text ui-egui vector. 4 apps: photocraft, photocraft-cli, photocraft-web, photocraft-web-boot. Plus `xtask`. `default-members` leaves out the two web apps.
- Notes: README says "24 crates" (`HEAD:README.md:253`). `docs/architecture.md:10` still says "25 library crates" because it was counted before `crates/psd` was removed in 74330157cb.

### E04-002 — Internal dependency graph (normal deps; target-specific deps included)
- Label: VERIFIED
- Method: awk over each `Cargo.toml` `[dependencies]` and `[target.*.dependencies]` section.
- Data (direct internal deps only):

| Layer (xtask TABLE) | Crate | Internal deps | UI/GPU deps |
|---|---|---|---|
| L0 | geom, cms | — | — |
| L0 | color | cms | — |
| L0 | raster | color geom | — |
| Standalone | codecs | craft-dpx/exr/gif/heif/jpeg/raster-codecs/tga (external) | — |
| Standalone | affinity, raw, ipp, tablet | — | — |
| L1 | doc | color geom raster | — |
| L2 | ops | doc | — |
| L2 | paint, algo | color geom raster | — |
| L2 | text | craft-psd color doc geom raster | — |
| L2 | vector | color doc geom raster | — |
| L3 | compose | cms color doc geom raster vector | — |
| L3 | gpu | algo color compose doc geom raster | **wgpu** |
| L3 | format | craft-pcraft-format codecs color doc geom raster | — |
| L4 | io | craft-docpath craft-psd craft-pdf affinity algo cms codecs color compose doc format geom paint raster raw text vector | — |
| L4 | plugins | color geom raster | (wasmi) |
| L5 | engine | craft-print craft-psd algo cms codecs color compose doc format geom io ops paint plugins raster text vector (+ ipp on Unix) | **none** |
| L6 | automation | codecs compose doc engine format gpu io raster (+ rmcp) | wgpu |
| L6 | ui-egui | craft-i18n/print/psd/ui algo cms codecs color compose doc engine format geom gpu io paint plugins raster text vector | eframe egui egui_extras egui_kittest |
| test-only | testkit | — (dev-dependency of algo, engine, io, ui-egui) | — |
| L7 | apps/photocraft | automation codecs color compose doc engine format geom io raster tablet ui-egui | eframe egui winit |
| L7 | apps/photocraft-cli | automation codecs doc engine format io raster | — |
| L7 | apps/photocraft-web | codecs doc engine io raster ui-egui | eframe egui wasm-bindgen |

- Notes: every edge points downward. GPU code enters only at L3 (`gpu`) and is used only by L6 (automation, ui-egui). The engine does not depend on `gpu` at all. That differs from the plan, which made `gpu` an optional default feature of the engine (day-1 `docs/architecture.md` §3 rule 5, still at `HEAD:docs/architecture.md:184`).

### E04-003 — Day-1 architecture plan vs HEAD: what survived
- Label: VERIFIED (lists); INFERRED (judgement of "survival")
- Source: `16941f7198:docs/architecture.md` (534 lines), `HEAD:docs/architecture.md` (595 lines). `git diff --stat 16941f719 HEAD -- docs/architecture.md`: 103 insertions, 42 deletions. The file has 43 commits.
- Data:
  - The plan listed 25 crates. **19 exist** with the planned name and role: geom color raster doc ops algo paint text vector compose gpu codecs raw format io engine ui-egui automation testkit.
  - **`psd`** was built (one-shot), then removed in favour of external `craft-psd` (74330157cb, 2026-11-12).
  - **Never built**: viewport, adobe-assets (as its own crate), tools, platform.
  - **ml** was added in 620fef4291 (2026-10-08) and reverted in bb39b4a8dd (2026-10-25).
  - **Added, not in the plan**: cms, plugins (wasmi, not the planned wasmtime), tablet, affinity, ipp. Short-lived: heif, winprint.
  - HEAD keeps the 2026-09-30 plan verbatim under "# Design plan (2026-09-30)" (`HEAD:docs/architecture.md:32`). A "Current state (2026-10-10)" preface says "where the code differs, this summary wins" (`:7-8`).
- Notes: the principles survived intact: engine-first/headless-first, everything-is-a-command, CPU oracle + GPU, COW tiles, determinism, enforced layering (`HEAD:docs/architecture.md:52-57`). Two mechanisms changed shape:
  - Command params are a free-text "JSON-ish" doc string, not a validated schema. Compare day-1 §4.1 `params: serde_json::Value /* validated vs schema */` with `HEAD:crates/engine/src/cmd.rs:22-23`.
  - History stores whole-document snapshots, not op transactions. Compare day-1 §6 "A command produces a Transaction of ops" with `HEAD:crates/ops/src/lib.rs:1-6` "History therefore stores whole-document snapshots per transaction".

### E04-004 — Size now
- Label: VERIFIED
- Method: per directory, `grep -rE '#\[(tokio::)?test'` count and `.rs` line count.
- Data: 18,030 test attributes, 1,015,858 lines of `.rs` overall. Largest: ui-egui 7,380 tests / 390k lines; engine 4,452 / 232k; io 1,249 / 73k; algo 1,000 / 93k. The one-shot was 241 files, 42,241 insertions (`git show --shortstat 16941f719`).
- Notes: README "more than 1,700 tests" (`HEAD:README.md:258`) and README "500+ commands" (`:230`) are stale against both this count and `docs/architecture.md:12` (~8,040 on 2026-10-13). This is doc drift.

### E04-005 — Crate additions and removals (all `Cargo.toml` A/D events under crates/ and apps/)
- Label: VERIFIED
- Method: `git log --reverse --diff-filter=AD --name-status -- 'crates/*/Cargo.toml' 'apps/*/Cargo.toml'`
- Data:

| Date | Sha | Event |
|---|---|---|
| 2026-09-30 | 16941f7198 | A: 14 crates (algo codecs color compose doc engine geom io ops paint psd raster testkit ui-egui), 3 apps |
| 2026-09-30 | ae92ac20bf | A: automation format gpu text vector |
| 2026-09-30 | b00b24739a | A: cms |
| 2026-10-04 | 5bd3dac660 | A: raw (#65) |
| 2026-10-04 | 7a5c1930b3 | A: plugins (#67) |
| 2026-10-05 | 47f4abfed4 | A: tablet (#255) |
| 2026-10-07 | 47f9306fd0 | A: heif (#372) |
| 2026-10-08 | 1bb37eda05 | A: affinity |
| 2026-10-08 | 620fef4291 | A: ml |
| 2026-10-10 | 628a54b564 | A: winprint |
| 2026-10-13 | d9bc5a8cd5 | D: winprint ("Use shared native print transport") |
| 2026-10-15 | df055f3dcb | A: apps/photocraft-web-boot (#5941) |
| 2026-10-17 | 235e7578f3 | A: ipp (#3017) |
| 2026-10-25 | bb39b4a8dd | D: ml (revert of PR #1199) |
| 2026-11-11 | 5d4b68f04c | D: heif → craft-heif (#13076) |
| 2026-11-12 | 74330157cb | D: psd → craft-psd (#13414; 25 files, +893/−5,899) |

### E04-006 — Extraction to shared `craft-libs` crates (a cross-repo modularity strategy)
- Label: VERIFIED
- Source: `HEAD:Cargo.toml` `[workspace.dependencies]`, which has 16 `craft-*` git deps pinned by rev (craft-ui, craft-psd, craft-dpx, craft-tga, craft-gif, craft-exr, craft-raster-codecs, craft-print, craft-heif, craft-pdf, craft-docpath, craft-jpeg, craft-pcraft-format, craft-i18n, craft-update, …). `git log -i --grep='craft-libs\|shared crate\|Use shared\|Use craft-'` returns 30 commits.
- Data: the earliest are e398cc80b8 (2026-10-10, shared Color Picker) and ccee4894bd (2026-10-12, craft-print; branch `codex/photocraft-craft-print`). The wave is: 289dd0a874 (2026-11-02, .pcraft envelope), 5d4b68f04c (11-11, heif), 21bb9fda63 (11-12, "Use shared crates for raster codecs" #13416), 74330157cb (11-12, psd). Five unmerged `origin/switch-craft-*` branches are dated 2026-11-12: kra-ora-xcf, psd, raster-codecs, raw-dng, svg. One is `d82fdfc287` "WIP: read DNG with craft-raw (19 DNG tests fail; see the handoff notes)".
- Notes: AGENTS.md says "Shared Rust components live in storytold/craft-libs and are pinned by immutable git revision" (`HEAD:AGENTS.md:56`). CI checks that all git deps come from `github.com/storytold/` (E04-034). AGENTS.md §2 still lists `psd` as an L0 crate (`HEAD:AGENTS.md:82`), so it is stale after 74330157cb. The CI fuzz matrix still lists `crate: psd` targets (`HEAD:.github/workflows/ci.yml:453-464`).

## 2. Headless engine

### E04-007 — The engine is UI- and GPU-independent
- Label: VERIFIED
- Source: `HEAD:crates/engine/Cargo.toml`. Its deps are internal crates plus serde, serde_json, rayon, chrono, base64, blake3, roxmltree, semver, tempfile and craft-print/psd. There is no egui, eframe, winit, wgpu or rfd. `xtask/src/layers.rs:102` sets `UI_CRATES = ["egui","eframe","winit","egui_kittest","craft-ui","rfd","bevy*"]`, and `UI_MIN_LAYER = 6` (`:105`).
- Notes: the engine compiles for wasm (AGENTS.md rule 7, `HEAD:AGENTS.md:122`).

### E04-008 — Constructed and tested without a window
- Label: VERIFIED
- Source: `HEAD:crates/engine/tests/panic_hunt.rs:15-21` builds `Session::new()` and calls `s.execute("file.new", json!({...}))`. 135 files under `crates/engine/tests` call `Session::new()` (`grep -rln 'Session::new()' crates/engine/tests | wc -l`).
- Notes: the architecture principle reads "Every feature is reachable without a GUI: from tests, the CLI and MCP. The GUI is one client of the engine." (`16941f7198:docs/architecture.md:23`, unchanged at `HEAD:docs/architecture.md:52`). It names **tests** as a consumer from day 1. That is the only domain-neutral design statement tying headlessness to testing. It does not mention agents.

### E04-009 — Headless servers
- Label: VERIFIED
- Source: `HEAD:docs/control-protocol.md:473-490`: "`photocraft-cli serve` keeps one headless engine session … It is the fastest way for a script or agent to make many edits". Implementation is `crates/automation/src/rpc.rs`. MCP has a headless mode, "an in-process `photocraft_engine::Session`. There is no window" (`:383`).

## 3. Command-driven design

### E04-010 — `CommandSpec` registry: shape and growth
- Label: VERIFIED (type); INFERRED (counts are regex estimates)
- Source: `HEAD:crates/engine/src/cmd.rs:14-28`. The struct has `id`, `label`, `menu`, `shortcut`, `params: &'static str` ("Human/agent-readable parameter description (JSON-ish)"), `enabled`, `run: fn(&mut Session,&Value)->Result<Value>`, `journal`. The same struct is in the one-shot at `16941f7198:crates/engine/src/commands.rs:16-30`.
- Data: unique dotted ids in macro or `id:` position in non-test engine sources: **76** at 16941f7198 and **805** at HEAD. Top prefixes at HEAD: layer 170, edit 77, filter 71, file 59, type 56, image 50.
- Method: `python3 -I scratchpad/work/E04/count.py <rev>`. This is an upper-bound heuristic.
- Notes: docs give "~700 commands" (`HEAD:docs/architecture.md:17`, as of 2026-10-10). README gives "500+" (`HEAD:README.md:230`). The exact count would need `photocraft-cli commands`, which was not built (see Open questions). Commands are split over 195 files in `crates/engine/src/cmd/`.

### E04-011 — Single dispatch, JSON in and out, history integration
- Label: VERIFIED
- Source:
  - `HEAD:crates/engine/src/session/execute.rs:17` `pub fn execute(&mut self, id: &str, params: Value) -> Result<Value>`. Any command accepts `"coalesce"` so that it shares one history step (`:11-13`).
  - `:232` `pub fn edit(&mut self, label, f)` "Apply an undoable edit to the active document".
  - History is snapshot-based (`HEAD:crates/ops/src/lib.rs:1-6`).
  - contributing.md: each `run` "records exactly **one** history step" (`HEAD:docs/contributing.md:18-22`).
  - The params doc string "is what agents read through `commands` / `command_list`".

### E04-012 — The "UI must go through commands" rule is documented and mechanically enforced
- Label: VERIFIED
- Source:
  - AGENTS.md rule 1, "Everything is a command … The UI, CLI, control channel and MCP all dispatch commands by id" (`HEAD:AGENTS.md:116`; day-1 version `16941f7198:AGENTS.md:39`).
  - Enforcement: `cargo xtask panel-commands` (`HEAD:xtask/src/panel_commands.rs:1-28`, 728 lines), a lexical scanner for click handlers that mutate the document directly. Its allowlist "only shrinks" and has **1** entry at HEAD (from 2 when added).
  - Added in 4165c57f92 (2026-10-11, David Mann, `Co-Authored-By: Claude Opus 5.5 (1M context)`). It is part of `cargo xtask ci` (`HEAD:xtask/src/main.rs:287`).
  - Also: `panic_hunt` enumerates `command_specs()` and fuzzes every command (`HEAD:crates/engine/tests/panic_hunt.rs:1-5`). Added in bf111b524e (2026-10-04, `Co-Authored-By: Claude Opus 4.8`). It runs in the CI gate (`main.rs:290`).
- Notes: the module doc gives the rationale: "The UI, CLI, control channel and MCP stay equivalent only while panels dispatch engine commands by id" (`panel_commands.rs:3-4`). This is the clearest case of an architecture rule given a mechanical check. The check is lexical and incomplete by its own admission (`:20-24`).

## 4. Programmatic interfaces

### E04-013 — Control protocol: day 1 vs HEAD
- Label: VERIFIED
- Source: `16941f7198:docs/control-protocol.md` (50 lines) and `HEAD:docs/control-protocol.md` (840 lines).
- Day 1 had 14 methods: `engine.execute`, `engine.commands`, `ui.inspect`, `ui.set`, `ui.menu.invoke/list`, `ui.dialog.*`, `ui.window.*`, `ui.pointer`, `ui.resize`, `ui.screenshot`, `ui.focus`, `app.open/save`, `app.quit` (`16941f7198:docs/control-protocol.md:20-33`). It said "An MCP server will wrap this same protocol (milestone M11)" (`:16`).
- HEAD adds token/HMAC challenge auth (`HEAD:docs/control-protocol.md:11-40`), timeouts, jobs, preferences, the MCP bridge (`:379`), the headless server (`:473`) and transport limits.
- One method exists for testing: `ui.gpu.simulateLoss` … "For testing the fallback" (`HEAD:docs/control-protocol.md:117`).
- Transport is `apps/photocraft/src/control_server.rs`; handlers are in `crates/ui-egui/src/control.rs`.

### E04-014 — CLI subcommands
- Label: VERIFIED
- Source: `HEAD:apps/photocraft-cli/src/args.rs:33-40`: Convert, Info, Run, Batch, Droplet, Commands, Mcp, Serve. The CLI has 82 test attributes in `apps/photocraft-cli/tests/it/*.rs` (91 in the whole app, E04-004).

### E04-015 — Actions, batch, plugins, IPP
- Label: VERIFIED
- Source:
  - Action recording and playback: `crates/engine/src/actions_record.rs` and the `actions.*` commands. The scorecard row AUTO-219-3 reads "actions.record/stop/play/list commands for agents and the CLI" (`HEAD:scorecard/automation.toml`).
  - `photocraft-cli batch --actions grade.json` (`HEAD:README.md:240`).
  - Plugins: wasmi sandbox (`HEAD:crates/plugins/Cargo.toml:3`); ABI doc `docs/plugins.md` (190 lines).
  - `crates/ipp` is a CUPS print client (`235e7578f3`). It is **not** an automation interface.

## 5. MCP

### E04-016 — MCP server: first added and tool count
- Label: VERIFIED
- Source: `ae92ac20bf` (2026-09-30, Brandon Thomas, "continued wip", no AI trailer) adds `crates/automation` with `server.rs` (627 lines) and **17** `#[tool(` handlers: session_list doc_open doc_new doc_save doc_export doc_inspect doc_render_preview doc_select doc_close command_list command_run ui_inspect ui_screenshot ui_pointer ui_menu_invoke ui_set control_call.
- HEAD has **26** (`grep -c '#\[tool(' HEAD:crates/automation/src/server.rs`). The additions are doc_place, doc_replace_smart_object, doc_export_layers, doc_export_data_sets, doc_import_data_sets, render_preview, jobs_list, jobs_cancel, command_batch.
- Categories: session/doc (14), command/job (5), UI/bridge (6), raw `control_call` (1).
- `docs/mcp.md` was first added in 15e35cf605 (2026-10-09, storybored379, `Co-Authored-By: Claude Opus 5.5`), 216 lines at HEAD.
- Notes: the engine is wrapped through generic `command_list`/`command_run`, so the registry's growth (E04-010) reaches MCP without new tools.

### E04-017 — Bridged mode
- Label: VERIFIED
- Source: `HEAD:docs/control-protocol.md:384`: "**Bridge** (`photocraft-cli mcp --bridge 127.0.0.1:7878 …`): every tool is forwarded to a running `photocraft --control` … so agents see and drive the live app". The day-1 plan already had "Stdio for agent CLIs, and optionally loopback TCP with a token so it can attach to a running GUI. Photon does exactly this with Claude Code, Codex and Cursor" (`16941f7198:docs/architecture.md:426`).

### E04-018 — README "Built for agents" frames agents as **users** of the product
- Label: VERIFIED
- Source: `HEAD:README.md:228-249` (added 536a7346fb, 2026-10-01): "anything you can click, a script or an AI agent can do too". Milestone 7 of the day-1 plan reads "an agent edits a PSD through MCP" (`16941f7198:docs/architecture.md:523`). `docs/mcp.md:25` shows `claude mcp add photocraft -- photocraft-cli mcp …`.
- Notes: all MCP documentation addresses end-user agents. No primary source says MCP exists to help dev agents build PhotoCraft.

### E04-019 — "Every feature drivable by agents" is a stated product goal
- Label: VERIFIED
- Source: `HEAD:AGENTS.md:56` "…with better performance, and every feature drivable by agents". The phrase was introduced in 536a7346fb (2026-10-01; `git log -S`).

## 6. Use of agent-facing interfaces by the development process

### E04-020 — Day-1 AGENTS.md tells dev agents to verify UI through the control channel
- Label: VERIFIED
- Source: `16941f7198:AGENTS.md:44`: "**Verify UI changes visually.** Launch the app with `--control`, drive it, take `ui.screenshot`, and look at the PNG." Also `:12`, where `docs/control-protocol.md` is listed as "JSON control channel: how agents drive and screenshot the running app".
- Notes: this is a primary source designing a product interface (the control channel) partly as a **dev-agent self-verification** tool from day 1. Cross-ref E01-003, E02.

### E04-021 — HEAD version adds an offscreen, no-window path
- Label: VERIFIED
- Source:
  - `HEAD:AGENTS.md:121` "Render offscreen with `cargo run -p photocraft-ui-egui --example snapshot` (no window, no focus stealing), or launch with `--control` and take `ui.screenshot`. Look at the PNG. Screenshots … go in the PR description, never in the repo".
  - `HEAD:docs/contributing.md:13` "Verify visually (offscreen `snapshot` example or the control channel) before submitting".
  - `crates/ui-egui/examples/snapshot.rs:1-24` accepts `--script`, "a JSON array of `[method, params]` control-protocol calls". The example has existed since ae92ac20bf (2026-09-30).

### E04-022 — README images rendered through the control channel
- Label: VERIFIED (claim as stated in the README)
- Source: `HEAD:README.md:249` "Every image in this README was rendered that way". Added 536a7346fb (2026-10-01).

### E04-023 — The control protocol is used inside the project's own UI tests
- Label: VERIFIED
- Source:
  - `grep -rln 'control::handle\|ControlRequest'` matches 32 files in `crates/ui-egui/tests` and 71 `*tests*.rs` files in `crates/ui-egui/src`.
  - Example: `HEAD:crates/ui-egui/tests/it/camera_raw_histogram.rs:12-13` `control::ControlRequest::new("ui.menu.invoke", …); control::handle(h.state_mut(), &ctx, &request)` inside an egui_kittest harness.
  - `HEAD:docs/development.md:469` "UI: unit tests for widgets and state, plus screenshot checks through the control channel."
- Notes: this is direct evidence that an agent-facing interface doubles as a test driver. It does not show *who* wrote the tests.

### E04-024 — Commit and PR traces of dev agents verifying through these paths
- Label: VERIFIED (individual cases); counts are VERIFIED with the method shown
- Source and data:
  - c080ed3e72 (2026-10-03, Brandon Thomas, `Co-Authored-By: Claude Opus 4.8`): "Parity 608 -> 609; FLOOR 604. Snapshot-verified."
  - d59d2b509f (2026-10-10, mroxso): "Verified with the offscreen snapshot example: RGB green canvas goes (128,128,128) -> (0,128,0)…".
  - e4bc5c25e8 (2026-10-15, Stepan Pavlenko): "offscreen `snapshot` in Russian checked".
  - 2f42b1cc80 (2026-10-09, `Co-Authored-By: Claude Opus 5.5`): "agents read it via ui.inspect.cameraRaw and see it offscreen with the snapshot example or kittest".
  - PR #7374 (branch `claude/github-issue-7342-dfa793`, "Generated with Claude Code"; commit 4b2bee675e has a Claude Opus 5.5 co-author): "Also checked in the running app through the control channel (`ui.pointer` stroke held mid-drag, then `ui.screenshot`)" — https://github.com/storytold/photocraft/pull/7374 (accessed 2026-11-12, via WebFetch summary).
  - `HEAD:docs/tone-targets-validation.md:13` "Full-app offscreen before/after screenshots were inspected" (96dcb10fb5, Vlad Grankovsky, no AI trailer).
- Method: a regex over all 12,396 main commit messages (`log.txt`). Only 3 messages match "snapshot-verified / verified with the snapshot"; 1 matches "screenshot … verified"; 0 match "verified via control/MCP/CLI".
- Notes: AGENTS.md sends screenshots to PR descriptions, not commits, so commit messages under-count this practice. Only one PR was sampled (a second WebFetch hit a rate limit). The practice is documented and observed, but its frequency is unknown.

### E04-025 — `tests/interactions` JSON scenarios are not wired into CI
- Label: VERIFIED
- Source: a3ea9a4277 (2026-11-05, Perchenko Anton; #9190) added 10 JSON files under `tests/interactions/guide-edit/`. `HEAD:docs/guide-edit-interactions.md:20-22`: "The interaction-check runner is development-only … Automated execution needs a separate shared workflow and maintainer review." No workflow references it (`grep -rn tests/interactions`).

### E04-026 — MCP has scripted "agent task" acceptance tests (end-user framing)
- Label: VERIFIED
- Source: `HEAD:crates/automation/tests/it/agent_tasks.rs:1-4`: "M11 acceptance: an agent completes 10 scripted edit tasks over MCP … the way an agent would, and checks the outcome through `doc_inspect` … never engine internals." Added 536a7346fb (2026-10-01). Not `#[ignore]`d, so it runs in the workspace tests of the CI gate. `HEAD:docs/development.md:394-395` adds "so agents can verify what they did without a screenshot".
- Notes: these tests check that the **product** serves agents. They are not dev agents verifying their own changes.

## 7. Deterministic tests and testkit

### E04-027 — testkit is small and lacks the planned golden-image tooling
- Label: VERIFIED
- Source: `HEAD:crates/testkit/src/lib.rs` (10 lines). The modules are `gpu` (`gpu_lock`, which serialises wgpu tests because drivers crash under parallel devices: `gpu.rs:1-21`), `perf` (RSS sampler, p50/p95 JSON rows) and `sweep` (`Sweep` slices long test sweeps by UTC date; `PHOTOCRAFT_FULL_SWEEP=1` runs everything, `sweep.rs:1-20`). It was a 1-line stub at 16941f7198.
- Notes: the day-1 plan promised "`testkit::assert_image_eq(actual, "golden/name.png", tol)`; goldens regenerated by `xtask bless`" (`16941f7198:docs/architecture.md:440`). No `assert_image_eq` and no `bless` exist at HEAD (grep). Cross-ref E05-021.

### E04-028 — Headless UI testing with egui_kittest; no image snapshots
- Label: VERIFIED
- Source: `HEAD:crates/ui-egui/Cargo.toml:74` `egui_kittest = { …, features = ["wgpu", "snapshot", "eframe"] }` (in the one-shot). 822 `Harness::` uses in ui-egui src+tests. No `.snapshot(` calls and no committed snapshot PNGs. `HEAD:docs/development.md:93`: "pixel appearance is reviewed from the saved images rather than a golden-image test."
- Notes: visual correctness is judged by a human or agent looking at the image. Only pixel-value assertions are automated.

### E04-029 — Determinism measures
- Label: VERIFIED
- Source:
  - `HEAD:docs/architecture.md:57` principle 6, "same output across CPU and GPU (within tolerance), across thread counts … Noise is hashed from document coordinates".
  - `HEAD:docs/contributing.md:17` "deterministic (seeded randomness)".
  - `snapshot.rs` `--system-theme` gives a "deterministic OS appearance" and the "predictable renderer forces bilinear filtering".
  - `scripts/ci-gpu-lavapipe.py` (2ff8f419cb, 2026-11-06, FredApps, `Co-authored-by: Claude Opus 5.5`) re-runs the nextest `gpu` group on Mesa lavapipe and **fails on authored skips** or a missing "GPU parity backend: Vulkan" line (`:21-37`). It is part of the gate command (`HEAD:.github/workflows/ci.yml:172`).
  - `.config/nextest.toml:12-20` caps GPU tests at 4 threads.
- Notes: the plan's "across thread counts" claim has no dedicated test found (not searched exhaustively).

## 8. Reference implementations and oracles ("what is correct")

### E04-036 — Correctness = match the target app, through embedded oracles and pinned corpora
- Label: VERIFIED
- Source:
  - `HEAD:docs/architecture.md:356-358` "PSD files contain Photoshop's own merged composite … a free, large conformance test suite".
  - `HEAD:docs/development.md:1132-1145` `cargo xtask test-corpus -p io` compares our composite with Photoshop's merged image (PASS ≤ 2/255); floors in `crates/io/tests/it/corpus.rs` "never lower them".
  - Corpus manifests (lines = files): photoshop 258, psd-tools 309, psd 170, pngsuite 178, affinity 60, gimp 28, atn 16, pixls 11, heif 9, exr 5. Total 1,044 (`wc -l xtask/*.sha256`).
  - First manifests in 968baf639e (2026-10-05); last added 9163afbdcf (pngsuite, 2026-10-12).
  - `scripts/fetch-corpus.sh` = `cargo xtask corpus --all`.
  - CI `corpus` job (`HEAD:.github/workflows/ci.yml:340-380`, cache key = pins + sha256).

### E04-037 — CPU reference vs GPU parity tests
- Label: VERIFIED
- Source: `HEAD:crates/gpu/tests/it/parity.rs:1-2`: "every blend mode, adjustment, group/clip/mask/fill combination must match the reference compositor within 2/255". It has 78 `#[test]`s and was first added in ae92ac20bf. The CI lavapipe script forbids skipping them (E04-029). AGENTS.md calls `compose` "the oracle" (`HEAD:AGENTS.md:86`).

### E04-041 — PSD write oracle (CLI-driven, manual)
- Label: VERIFIED
- Source: `xtask/src/psd_write_oracle.rs:1` "Execute small PSD export recipes with the headless CLI. Photoshop is a separate judge." Added f54d605e2c (2026-11-05, Khawar Zamman Wani). `starter.json` is 194 lines. `HEAD:docs/development.md:1127-1130` "they do **not** prove that Photoshop can open the output … The ordinary CI corpus job does not yet run this recipe command".
- Notes: this is the clearest case of the **CLI used as the project's own test harness**. It is not automated.

### E04-042 — Parity documents as the definition of "done"
- Label: VERIFIED
- Source:
  - `docs/target-app-parity.md` ("The authoritative answer to 'how close is PhotoCraft to Photoshop'", `:5`). First added 939c8f2c70 (2026-10-10, together with parity-checklist.md and file-format-parity.md).
  - `docs/parity-checklist.md` is generated: "664 of 664 menu items live" (`:5`).
  - `FLOOR = 663` test at `HEAD:crates/ui-egui/src/menus/parity.rs:10` ("never lower it").
  - AGENTS.md cites the old path `crates/ui-egui/src/parity.rs` (`HEAD:AGENTS.md:119,143`), which is stale.
- Notes: the definition of correct for agents has three layers. INFERRED from the sources above:
  - (a) pixel oracles from Photoshop-authored files and CPU-vs-GPU tolerance;
  - (b) menu/command coverage counters with ratchet floors;
  - (c) human-written parity dimensions ranked in `gaps.md`.
  Cross-ref E01-015, E01-018.

## 9. Mechanical architecture checks

### E04-030 — xtask subcommands (15) at HEAD
- Label: VERIFIED
- Source: `HEAD:xtask/src/main.rs:24-59` (usage) and `:67-81` (dispatch). The first-added sha is that of the module file (`git log --diff-filter=A --reverse`).

| Subcommand | Checks or does | Module first added | In CI? |
|---|---|---|---|
| layers | crate layering, UI-crate ban below L6, standalone crates, testkit dev-only, unregistered crate = error | 16941f7198 | yes (gate, Windows job) |
| panel-commands | click handlers must dispatch command ids | 4165c57f92 2026-10-11 | yes (gate) |
| wasm | `cargo check` wasm32 | 16941f7198 | yes (gate) |
| test | nextest/cargo test + doctests | 16941f7198 (main.rs) | via `ci` |
| ci | fmt, clippy, layers, panel-commands, scorecard --check, test, panic_hunt, doctest, wasm, i18n (`main.rs:269-310`) | 16941f7198 (fewer steps) | yes (E05 §0.2) |
| corpus | fetch and sha256-verify pinned corpora | 968baf639e 2026-10-05 | yes (corpus job) |
| test-corpus | corpus-feature tests | 968baf639e | yes (corpus job) |
| stats | test/line counts | 16941f7198 | no |
| parity | regenerate parity-checklist.md | (main.rs) | no (the FLOOR test runs) |
| i18n-report | translation coverage; "never fails" | 9dd39df78d 2026-11-08 | yes, non-failing |
| perf | benches vs budgets/baseline | 0f955e6c82 2026-10-05 | `--quick` in CI; full nightly |
| scorecard | regenerate / `--check` staleness | 0f955e6c82 | yes (`--check`) |
| version | set workspace version | d98bee4c94 2026-10-01 | release only |
| ico | pack .ico | d98bee4c94 | packaging |
| psd-write-oracle | CLI-driven PSD edit recipes | f54d605e2c 2026-11-05 | no |

### E04-031 — `xtask layers` details
- Label: VERIFIED
- Source: `HEAD:xtask/src/layers.rs` (396 lines, 15 commits).
  - `TABLE` at `:35-75`. `INTRA_LAYER_ORDER` allows geom→cms→color→raster and compose→gpu (`:80`). `STANDALONE_EXCEPTIONS` is empty (`:93`). It has unit tests (`:266-380`).
  - The TABLE still reserves the never-built crates `tools`, `viewport`, `ml`, `platform` and `adobe-assets`. A stale comment about HEIF remains at `:41`.
  - In CI since the one-shot: `16941f7198:.github/workflows/ci.yml:60-61`.
  - Plan text: "checked by `cargo xtask layers` in CI, which parses `cargo metadata`" (`16941f7198:docs/architecture.md:132`).

### E04-032 — Lints as architecture and policy enforcement
- Label: VERIFIED
- Source:
  - `HEAD:Cargo.toml` `[workspace.lints]`: `unsafe_code = "forbid"`; clippy `cognitive_complexity`, `too_many_arguments` and `wildcard_imports` = deny; `dbg_macro`, `todo` = warn. The clippy block was added 604da9d06b (2026-10-27, Dylan M. Taylor, "Enforce workspace Clippy standards").
  - `HEAD:clippy.toml`: unwrap/expect/panic/indexing allowed in tests only; `disallowed-types = egui::ComboBox` → use `craft_ui::ComboBox` (07bd794686, 2026-10-27); `cognitive-complexity-threshold = 30`. File first added 50a27e6c74 (2026-10-04, "Never crash: steering rules, clippy.toml, forbid unsafe (#33)", `Co-authored-by: Claude Opus 5.5`).
  - Per-crate `#![deny(clippy::unwrap_used, …)]`. The scorecard reports "never-crash lints on 28 of 28 crates" (`HEAD:docs/scorecard.md` summary).
- Notes: a complexity ceiling of 30 and a ban on wildcard imports are domain-neutral size and complexity limits. No file-size limit was found.

### E04-033 — Compile-time completeness check for the native format
- Label: VERIFIED
- Source: `HEAD:crates/format/src/convert.rs:236,297`: "Destructured so a new `AlphaChannel` field fails to compile here until it is saved." `HEAD:AGENTS.md:189-194` §8. Both introduced in 536a7346fb / ae92ac20bf (2026-09-30/10-01).

### E04-034 — Supply-chain and source checks
- Label: VERIFIED
- Source: `HEAD:.github/workflows/ci.yml:93-127` "Git dependencies come from storytold". It parses `.cargo/config*` for source replacement or patches, runs `cargo metadata --locked`, and rejects `git+` sources outside `github.com/storytold/`. Added 6401cfdbe1 (2026-10-17, aiongg). Cross-ref E05-008.
- The "source policy" in branch `origin/fix/sec-source-policy-scope` is **not** an architecture check. It is the engine's runtime file-access policy for automation sessions: ed592c1005 (2026-11-03) "keep the session's source policy for Save for Web writer, Package and link refresh". The branch is unmerged at the pin (latest 63bc4ad025, 2026-11-11).

### E04-035 — House-rules workflow (instruction-file integrity)
- Label: VERIFIED
- Source: `HEAD:.github/workflows/house-rules.yml`. It triggers on changes to `AGENTS.md` / `CLAUDE.md` and calls `storytold/craft-common-actions/.github/workflows/house-rules.yml@main` with `rust: true`. Added 7d8648dfcb (2026-11-06, FredApps). The marked blocks in `HEAD:AGENTS.md:1,22` carry `source=dde09ea31e… sha256=…`.
- Notes: this is a domain-neutral check that keeps the agent instruction file in sync with the shared org rules. The shared workflow's logic is outside this repo and was not examined (INFERRED: it checks the hashed blocks). Cross-ref E02.

## 10. Scorecard and perf budgets

### E04-050 — Scorecard as machine-readable goals with a CI staleness check
- Label: VERIFIED
- Source: `scorecard/*.toml` (8 files, 1,199 lines). There are 166 `[[item]]`s: 113 `done`, 46 `partial`, 7 `missing` (`grep -ohE 'status *= *"[a-z]+"' | uniq -c`). Each item has `id`, `target`, `status`, `issue`, `note`, e.g. `HEAD:scorecard/automation.toml:8-12`. The header says "Statuses must be true on main. Verified against 4b53f62 on 2026-10-05".
- `docs/scorecard.md`: "Generated by `cargo xtask scorecard` … Do not edit by hand … (CI runs `cargo xtask scorecard --check`)" (`:3`).
- First added 0f955e6c82 (2026-10-05, Brandon Thomas, "#221"). AGENTS.md §4.1 tells agents to "Check `docs/scorecard.md` before picking work … Its numbers are measured; prefer them to estimates" (`HEAD:AGENTS.md:136-138`).

### E04-051 — Perf budgets exist but none are enforced
- Label: VERIFIED
- Source: `HEAD:perf/budgets.toml` has 88 `[[scenario]]`s, 0 with `enforce = true`, and 5 with `not_measurable`. The header says "`enforce = false` marks a target the code doesn't meet yet … flip it to true in the PR that meets it" and "never invent a number for them" (`:1-12`). The regression rule is p50 > 15 % and > 1 ms (`:16-18`).
- `perf/baseline.json` was last changed 3423864502 (2026-10-05).
- `docs/scorecard.md` baseline: "Apple M4 Pro … load average 224.90 … **contended baseline** … these numbers measure machine load, not the code".
- perf-nightly runs on `macos-15` (`HEAD:.github/workflows/perf-nightly.yml:43`). The scorecard says the regression check "runs only on machine class `macos-aarch64-apple-m4-pro-apple-m4-pro`".
- Notes: INFERRED. With 0 enforced budgets and a single contended baseline, the perf contract is mostly a reported goal list, not a gate. Whether the GitHub runner matches the baseline's machine class was not checked.

## 11. Domain-specific vs domain-neutral mechanisms

Label: INFERRED. The classification is ours; each row cites the evidence above.

| Domain-neutral (transferable) | Image-editor-specific |
|---|---|
| Headless core with UI only at the top layer, checked by a dependency-layer linter (E04-007, E04-031) | Embedded Photoshop composite as a free oracle (E04-036) |
| One command registry with enumerable specs and JSON params, used by UI, CLI, RPC and MCP (E04-010–012) | CPU reference compositor vs GPU parity within 2/255 (E04-037) |
| Lexical "UI must dispatch commands" check with a shrink-only allowlist (E04-012) | Corpora of Photoshop/GIMP/Affinity files with sha256 pins (E04-036) |
| Fuzz every registered command for panics (`panic_hunt`) (E04-012) | Photoshop menu catalog → generated parity checklist + FLOOR (E04-042) |
| Control channel that can inspect state, inject input and screenshot; offscreen render example that replays control scripts (E04-013, E04-021) | Multi-depth (8/16/32f) and colour-model test rules (`HEAD:AGENTS.md:117`) |
| Machine-readable scorecard with `--check` in CI (E04-050) | lavapipe software-GPU re-run (GPU-specific, E04-029) |
| Perf budgets file with "enforce once met" flags (E04-051) | `.pcraft` destructuring completeness check (pattern neutral, target specific; E04-033) |
| Git-source allowlist; shared house-rules block with a hash check (E04-034, E04-035) | |
| Shared library extraction pinned by rev (E04-006) | |

## Open questions / uncertainties
- **Exact command count.** The 76 → 805 figures are regex estimates. The exact count needs `photocraft-cli commands`, and the workspace was not built (4 cores, git deps from craft-libs).
- **How often dev agents verify visually.** Only one PR (#7374) was sampled via WebFetch. A second fetch hit a rate limit. Commit messages under-count this practice because AGENTS.md routes screenshots to PR bodies.
- **Squash-merged infrastructure commits.** Many of these carry no trailer (16941f7198, 0f955e6c82, 968baf639e, 74330157cb, …). Whether an agent wrote them is *unknown*, not human.
- **House-rules check.** The shared workflow's logic in craft-common-actions was not inspected.
- **Perf nightly.** Whether the GitHub `macos-15` runner ever matches the baseline machine class (that is, whether the regression gate ever fires) was not checked.
- **`agent_tasks` test count.** The 5+1+1 figure counts `#[test]`/`#[tokio::test]` attributes. The ten tasks may be grouped inside fewer test functions.
- **Thread-count determinism.** No test proving the architecture claim was located.

## Leads for other streams
- `d82fdfc287` (branch `switch-craft-raw-dng`, 2026-11-12): "19 DNG tests fail; see the handoff notes". This is hand-off practice in a WIP branch (E02/E03).
- `ccee4894bd` came from branch `codex/photocraft-craft-print` (2026-10-12). This is a Codex-named branch in the extraction wave (attribution stream).
- `docs/integration-testing/` (46c1347951, FredApps, 2026-10-29) is a 108-PR integration build record with a gate table. Release/QA stream.
- `HEAD:docs/development.md:248` example writes `evidence/shot.png`. This is a screenshot-as-evidence convention.
- Doc drift against HEAD (doc-maintenance stream):
  - AGENTS.md §2 still lists `psd`;
  - AGENTS.md cites `crates/ui-egui/src/parity.rs`;
  - README has 1,700 tests and 500+ commands;
  - architecture.md has 25 crates;
  - the CI fuzz matrix still lists `psd`.
- The perf baseline was recorded under load 224 on 14 cores (2026-10-05). It may reflect many concurrent local builds. Do not infer agent count from it.

## Methods-relevant takeaways
- Make the core headless and enumerable: a registry of JSON commands that tests, the CLI, RPC and MCP all reach. Fuzzing every command becomes a single test (E04-008, E04-010, E04-012).
- Turn architecture rules into cheap CI checks: a dependency-layer linter from day 1, plus a lexical "UI dispatches commands" scanner with a shrink-only allowlist (E04-031, E04-012).
- Give agents a way to *see* the product without a desktop: an offscreen render example that replays control-protocol scripts, and an authenticated control channel with screenshot. Write "verify visually and look at the PNG" into the agent guide (E04-020, E04-021, E04-024).
- Reuse the agent-facing control interface as the UI test driver, so product automation and test automation do not drift apart (E04-023).
- Define "correct" through external oracles: reference-app outputs embedded in files, pinned and hashed corpora, and a CPU reference vs GPU tolerance. Use ratchet floors that are never lowered (E04-036, E04-037, E04-042).
- Keep goals machine-readable and CI-checked: scorecard TOML → generated doc with `--check`; perf budgets with explicit "not measurable, never invent a number" fields (E04-050, E04-051).
- Compile-time completeness tricks (destructuring) stop agents from silently dropping fields in serializers (E04-033).
- Caveat: plan items such as golden images and `xtask bless` were never realised, and no perf budget is enforced. Documented intent is not the same as an active gate (E04-027, E04-051).
- Caveat: the docs drift quickly under high change rates (README, AGENTS.md crate map). Generated docs with `--check` stayed accurate; hand-written ones did not (E04-004, E04-006).
