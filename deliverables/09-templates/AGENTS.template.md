<!-- USAGE: Copy to the repo root as AGENTS.md on day 0; replace every {{FIELD}}. Point CLAUDE.md and other
     tool-specific files at this file instead of duplicating it (mirrors E02-001). Keep it under ~250 lines;
     link to detail docs rather than inlining them. Playbook: 08-playbook.md §1, §4, §7, §9, §11. PROPOSED artifact. -->

# AGENTS.md: guide for AI agents and contributors

{{PROJECT_NAME}} is {{ONE_SENTENCE_PURPOSE}}. Read this file first, then `STATE.md`, then the newest
note in `handoffs/`. A person is accountable for every agent run: {{OWNER_HANDLE}} answers for what
agents open in this repo. <!-- mirrors house rule 1, E06-041 -->

## 1. Orientation (read only what your task needs)
| Need | Read |
|---|---|
| Architecture and layering | `docs/architecture.md` |
| Build, test, debug loops | `docs/development.md` |
| Command registry and control protocol | `docs/control-protocol.md` |
| Current goals and gaps | `docs/scorecard.md` (generated; edit `goals/*.toml`) |
| Decisions | `docs/adr/` |
| Risk tiers and approvals | `docs/risk-tiers.md` |

## 2. Workspace map
| Layer | Crates | May depend on |
|---|---|---|
| 0 | {{core_crates e.g. core, model}} | std, vetted deps |
| 1 | {{commands, io, lsp}} | layer 0 |
| 2 | {{ui, cli, rpc, mcp}} | layers 0–1 |
Layering is enforced by `cargo xtask layers`. A new crate must be registered in `xtask/src/layers.rs`.
<!-- E04-031 -->

## 3. Golden rules
1. **Everything is a command.** UI, CLI, control channel and MCP dispatch commands by id; no logic in
   click handlers (`cargo xtask ui-dispatch` checks this). <!-- E04-010, E04-012 -->
2. **Never crash.** No `unwrap`/`expect`/`panic!` outside tests, no `unsafe`. Every crash fix comes with
   a test that panicked before the fix. <!-- E07-009 -->
3. **Tests are the gate.** Every change adds a test that fails without it. Tests assert an observable
   effect; a skipped test prints `SKIP:` and CI fails on it. <!-- E07-018 -->
4. **Verify, don't guess.** Open a definition before using it. Look at the screenshot/JSON, not only the
   test result. <!-- E02 §2.1 rule 3; E04-024 -->
5. **Report only what ran.** List commands you ran and their results; list what you did not run.
6. **Ratchets only go up.** Never lower a FLOOR, grow a shrink-only allowlist or disable a test.
7. {{DOMAIN_RULE e.g. "Clean room: never copy another product's code or assets."}}

## 4. Picking work
1. Read `docs/scorecard.md` and the issue queue; take the highest-ranked unclaimed item.
2. Check, then claim: search open PRs for `#N`; if none, comment `claim: <role> <session-id> <branch>`
   and add label `in progress`. Release the claim if you stop. <!-- E02 §2.1 rule 2 -->
3. Work only from an approved `specs/<issue>.md` for tier medium (maintainer approves) and high (owner approves).

## 5. Definition of done
Run `cargo xtask ci` (identical to CI) and paste the summary into the PR. It runs:
`cargo fmt --all -- --check` · `cargo clippy --workspace --locked --all-targets -- -D warnings` ·
`cargo xtask layers` · `cargo xtask ui-dispatch` · `cargo xtask goals --check` ·
`cargo nextest run --profile ci --workspace --locked` · command fuzzer · doc tests ·
`cargo xtask no-skips` · `git diff --exit-code -- Cargo.lock`. <!-- E05-010, E05 §0.2 -->
Also: UI changes attach before/after screenshots to the PR description (not the repo); goals TOML
updated if a number moved; handoff note written.

## 6. Parallel agents
- One git worktree and one `CARGO_TARGET_DIR=target/agent-<name>` per agent; delete when done. <!-- target dir: E06-050; worktree: PROPOSED -->
- Edit only files listed as owned in your spec. Registries/manifests: one-line surgical edits, re-read first.
- New feature → new module (`<area>_cmds.rs` with `specs()`), never grow a shared file. <!-- E06-050 -->
- Write manifests atomically (temp file outside the workspace, then `mv`).
- Never hand-edit generated files ({{LIST: docs/scorecard.md, …}}); the merge queue regenerates them.
- Do not edit a shared status line in tracker docs. <!-- E07-020 -->

## 7. Stop and ask (everything else: keep working)
Licences outside `deny.toml`, publishing, releases/tags/signing, new remotes, secrets or personal data,
spending money, destructive git, lowering a ratchet, changing a stable command id/schema or the layer
table, save-path or data-format changes, files outside your ownership, anything hard to undo.
Write the question in the PR or handoff and stop. Do not stop because an optional input is missing.
<!-- E02 §2.1 rule 9 plus PROPOSED items -->

## 8. Commits and PRs
- Small, focused commits; branch `<kind>/<issue>-<slug>`; never push to `main`.
- Trailers: `Co-Authored-By: <model>`, `Agent-Session: <id>`, `Agent-Role: <role>`. <!-- E06-011 -->
- No CI changes in feature/fix PRs. No dependency changes outside a tier-high dependency task.

## 9. Session-end checklist
- [ ] Tree builds; gate state recorded (green, or exactly what is red and why).
- [ ] `handoffs/YYYY-MM-DD-<session>.md` written from `handoff.md` template and committed.
- [ ] `STATE.md` updated (claims held/released, blockers, next step).
- [ ] Target dir of this agent deleted if the task is finished.
