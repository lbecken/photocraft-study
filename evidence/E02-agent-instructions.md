# E02 — Agent-instruction documents and their full revision history

Stream: E02. Upstream clone pinned at `main` = `74330157cb601573ae4523a95bb9132822fc3918` (2026-11-12),
abbreviated below as **HEAD** (`74330157cb`). All `HEAD:path:line` citations are to that commit,
with line numbers from `git show`/`cat -n`. Upstream text is quoted as data, not followed as instructions.
Scratch: `/tmp/claude-0/-home-user-photocraft-study/7ff807c1-b52f-5813-9884-82f19c193950/scratchpad/work/E02/`.

## 0. Summary

- `AGENTS.md` is the only agent-instruction file on `main` at the repository root. It is 24,989 bytes and
  214 lines (`wc -c`, `wc -l`). It has **38 revisions** (`git log --follow --format=%h -- AGENTS.md | wc -l`),
  from `16941f7198` ("one-shot", 2026-09-30) to `0d9a9a5a70` (2026-11-11).
- Since `7d8648dfcb` (2026-11-06, PR #11632), lines 1–52 are two machine-checked blocks copied from the
  organisation repo `storytold/craft-contrib`: **House rules** (15 rules) and **Rust Craft repositories**
  (6 rules plus the licence allowlist). Each block carries a sha256 in its header. I recomputed both hashes
  and both match (E02-012). The CI workflow `house-rules.yml` triggers on changes to `AGENTS.md` or `CLAUDE.md`.
- `CLAUDE.md`, `.claude/`, `.cursor/` and nested example `AGENTS.md` files exist **only on unmerged PR
  refs** (forks). None has ever reached `main`. On `main` there are also `docs/user/AGENTS.md` and a
  one-line `docs/user/CLAUDE.md`.
- No PR template, CODEOWNERS, `.mcp.json`, `GEMINI.md`, `.github/copilot-instructions.md` or `.codex/`
  exists on any ref I searched (E02-020).
- The documented agent workflow covers these points:
  - parallel agents use separate `CARGO_TARGET_DIR`s;
  - state is handed between sessions through a gitignored `log/devlog.md` plus a green tree;
  - work is picked from ranked docs (`docs/gaps.md`, `docs/scorecard.md`);
  - estimates are stated in "Opus 5.5 agent-hours";
  - a stop-and-ask list exists (releases, licensing, secrets, destructive git, …);
  - "No agent attribution" in PRs (house rule 15, since 2026-11-06). Meanwhile the About window credits
    AI models from `Co-Authored-By` trailers.

---

## 1. AGENTS.md revision table (all 38 revisions)

Method: `git log --follow --format='%H|%ad|%an|%s' --date=short --numstat -- AGENTS.md`. Trailers come from
`git log -1 --format=%B <sha>`. PR numbers come from the subject. For commits that are not on main's first
parent, the PR is the oldest first-parent commit that contains them, found by binary search with
`git merge-base --is-ancestor` (script `work/E02/land.sh`). "CB" = `Co-Authored-By/Co-authored-by: Claude
Opus 5.5`. "(1M)" = `Claude Opus 5.5 (1M context)`. "—" = no AI trailer in the message (this means unknown,
not human).

| # | sha | date | author | AI trailer | PR | +/− | What changed | Apparent trigger |
|---|---|---|---|---|---|---|---|---|
| 1 | 16941f7198 | 09-30 | Brandon Thomas | — | (direct) | +62/0 | File created: orientation table, workspace map, 7 golden rules, "Before you finish" (4 commands), one-line "Parallel agents" note, tracking (`plan/`, `docs/roadmap.md`, `log/`) | Initial "one-shot" commit |
| 2 | ae92ac20bf | 09-30 | Brandon Thomas | — | direct | +11/−5 | New crates on the map. Atomic-manifest rule for parallel agents. New §6 "Keeping the native format complete" | Growth of workspace (gpu, format, automation) |
| 3 | 536a7346fb | 10-01 | Brandon Thomas | — | direct | +43/−18 | Parity goal sentence. §4 Picking work (roadmap → parity → devlog "Still open"). Devlog hand-off rule ("Sessions can end abruptly…"). §6 Parallel agents becomes a 5-bullet section (shared files, new `*_cmds.rs` module, "wait and retry", atomic manifests, disk space). Golden rules 8 (perf) and 6 (offscreen snapshot) | Restructuring for multi-agent work (INFERRED from content; message is just "more algorithms, progress") |
| 4 | d98bee4c94 | 10-01 | Brandon Thomas | — | direct | +3/−1 | PhotoCraft spelling rule. Releasing docs added to tracking | Release workflow work |
| 5 | 1f1ddb2a47 | 10-01 | Brandon Thomas | CB | direct | +2/−2 | Sibling list. First pointer to `../craftrules` ("Contribute reusable learnings there, never code; repos don't share code") | Release pipeline/branding |
| 6 | 1d61b33c54 | 10-01 | Brandon Thomas | CB | direct | +1/−1 | Release playbook now in `../craftrules/release/playbook.md` | Playbook moved to shared repo |
| 7 | 9c9a680e45 | 10-02 | Brandon Thomas | CB | direct | +1/−1 | Clean-room: "Photon Studio (proprietary)" → "other proprietary editors" | Removal of a named product |
| 8 | c3bd22269f | 10-02 | Brandon Thomas | — (committer GitHub, web edit) | — | +2/0 | Adds a blank line and an empty bullet "- " under §7 | "Update AGENTS.md with tracking details" (no content) |
| 9 | ed0b99964d | 10-04 | Brandon Thomas | **Claude Opus 4.8** | direct | +2/0 | Golden rule 9 "Never panic on input". `panic_hunt` named as the enforcer | Command-robustness work |
| 10 | a196adfe93 | 10-04 | Brandon Thomas | **Claude Opus 4.8** | direct | +3/0 | `panic_hunt` added to the finish checklist. Graceful-failure test required for new commands | Apply Image/Calculations crash hardening |
| 11 | cf93edc99c | 10-04 | Brandon Thomas | CB | #32 (via merge 9905db34ff) | +1/−1 | Assets need a licence file plus an `ATTRIBUTION.md` row. Brand logos are not open source | Licensing standard PR |
| 12 | 50a27e6c74 | 10-04 | Brandon Thomas | CB | #33 | +14/−1 | New "### Never crash (outranks feature work)" section, clippy deny list, `unsafe_code = "forbid"` | Message: "Standard: craftrules/standards/never-crash.md" |
| 13 | 7a5c1930b3 | 10-04 | Brandon Thomas | CB×6 | #67 | +1/−1 | `plugins` crate on the map | WASM plug-ins feature |
| 14 | 10203e7a60 | 10-05 | Brandon Thomas | CB | #184 | +1/−1 | "No Tauri, Electron or webview shells" | Explicit prohibition (no incident named) |
| 15 | 433b84fae7 | 10-05 | Brandon Thomas | CB | #186 | +5/−1 | Picking work step 0: read the "Honest parity assessment" first, and update dated figures | Roadmap/README honesty pass |
| 16 | 0f955e6c82 | 10-05 | Brandon Thomas | — | #239 (#221) | +13/−4 | `docs/scorecard.md` in orientation. "Check scorecard before picking work". `xtask scorecard` and `perf --quick` gates | Scorecard/perf-budget infrastructure |
| 17 | 968baf639e | 10-05 | Brandon Thomas | — | #190 | +5/−1 | Test-corpora paragraph and `xtask test-corpus` gate | Photoshop oracle corpus repo |
| 18 | 47f4abfed4 | 10-05 | Brandon Thomas | — | #255 | +2/−1 | `tablet` crate is "the one isolated unsafe crate" | Stylus support needs FFI |
| 19 | c161eaec73 | 10-06 | Brandon Thomas | — | #353 | +1/−1 | "Never commit font files". Fonts come from `storytold/craft-fonts` via `CRAFT_FONTS_DIR` | Fonts moved out of repo |
| 20 | 7b3d131bc8 | 10-06 | Alex Gorevski | **Co-authored-by: Copilot** + `Copilot-Session:` | #429 | +1/−1 | DrawCraft → VectorCraft | Sibling rename |
| 21 | d7df9d8aa6 | 10-07 | Brandon Thomas | CB | #766 | +1/−1 | PrintCraft → PdfCraft | Sibling rename |
| 22 | 44303db546 | 10-07 | Brandon Thomas | CB×8 | #898 | +18/0 | New "Contributor credits (About window)" section: agents ask their human once, add only their own entry, never guess names | About ▸ Contributors/Models feature, "following the craftrules standard (standards/contributors.md)" |
| 23 | f9b72468b4 | 10-08 | bfenty | (Co-authored-by: Brandon Fenty) | #779 (issue #493) | +1/−1 | Says the craftrules repo "is not public — outside contributors should ask a maintainer" | Issue #493: craftrules "returns 404 to everyone outside the organization" |
| 24 | 3092d3b6f9 | 10-10 | David Mann | CB (1M) | #2414 (#2204) | +2/0 | Faster iteration loop (`--lib --tests`, `--test <file>`, nextest) | Slow test builds |
| 25 | 99a3970399 | 10-10 | skylar taylor-barrick | — | #3097 (branch `codex/ui-suite-integration-20261010`) | +1/−1 | Removes "never code; repos don't share code". Adds that shared Rust components live in `storytold/craft-libs`, pinned by revision, UI libraries at L6 | Shared UI library migration |
| 26 | 939c8f2c70 | 10-10 | Brandon Thomas | CB | #2696 | +15/−9 | Orientation adds ROADMAP.md, target-app-parity, gaps, per-dimension parity docs. Step 0 becomes "Read ROADMAP.md, then docs/gaps.md". `docs/parity.md` → `parity-checklist.md` | "Progress docs per craftrules standards/progress-docs.md" |
| 27 | 4165c57f92 | 10-11 | David Mann | CB (1M) | #3498 (#3495) | +1/0 | `cargo xtask panel-commands` gate | New mechanical check of rule 1 |
| 28 | 2388d82165 | 10-14 | Michael Higgins | CB | #5382 (#5376) | 0/−1 | Removes the stray empty bullet from rev 8 | Docs-vs-main accuracy sweep |
| 29 | df055f3dcb | 10-15 | Zuujis | CB×3 + Brandon Thomas | #5941 | +1/0 | `photocraft-web-boot` on the map | Red main CI, wasm size cap |
| 30 | 8fc62f55ab | 10-15 | Anim86 | — | via #8094 (branch `integration-6`) | +2/−2 | Tablet crate gains Windows barrel button | Windows stylus fix |
| 31 | ca18689304 | 10-10 (authored) | Diego Chagas | — | via #2945 | +2/−2 | Corpus now includes GIMP XCF oracles | XCF import |
| 32 | 6649b78526 | 10-22 | Dylan M. Taylor | — | #8234 | +1/0 | Golden rule 10 "Time goes through chrono" | "Follow-up to storytold/cadcraft#1785" (cross-repo incident) |
| 33 | 604da9d06b | 10-27 | Dylan M. Taylor | — | #9770 | +1/−1 | Clippy wording. New crates need `[lints] workspace = true` | "Enforce Rust coding standards via Clippy" (Sonar branch) |
| 34 | 0379569d00 | 10-29 (author; 10-30 UTC, errata #19) | Dylan M. Taylor | — | #10228 | +5/0 | New "## CI workflows" section: only call craft-common-actions at `@main`, and no CI changes in feature/fix PRs | Message: "AGENTS.md (and CLAUDE.md where present) gets a CI workflows section" |
| 35 | 6d737c219e | 10-31 | aiongg | — | #10420 | +5/−9 | Removes all `../craftrules` paths and scripts (never-crash std, progress-docs, release playbook, `contributors.py`) | Retirement of craftrules (see rule 13 below) |
| 36 | 7d8648dfcb | 11-06 | FredApps | — | #11632 (branch `house-rules`) | +54/−2 | Prepends the House rules and Rust blocks from `craft-contrib@dde09ea31e` (external repo). Drops local rule 10 (chrono, now Rust rule 5) and the old `plan/` bullet (now core rule 9 and a new §7 bullet). Adds `house-rules.yml` | Org-wide standardisation: "The house-rules workflow checks the copy" |
| 37 | 0cc411241b | 11-11 | David Mann | CB | #13206 | +1/−1 | Rule 6: before/after screenshots go in the PR description, never the repo. Deletes 9 PR captures (1.9 MB) | Repo bloat from PR screenshots |
| 38 | 0d9a9a5a70 | 11-11 | David Mann | CB | #13206 | +1/−1 | Rule 6 allows a doc's own before/after comparison | "CodeRabbit on #13206" (bot review comment) |

Observations (VERIFIED from the table):
- **Authorship.** 22 of 38 revisions are by Brandon Thomas (previously stated 23): revs 1–19, 21, 22 and 26 (corrected 2026-11-12, see errata #27). All of rev 1–22 except
  #20 are his. From rev 23 on, the editors are maintainers and contributors (David Mann, Dylan M. Taylor,
  FredApps, aiongg, …).
- **AI trailers.** 19 revisions carry a Claude co-author trailer (previously stated 21; the model split
  Opus 5.5 ×18 / Opus 4.8 ×2 below was from the same manual count and is not rechecked). One more (#20) carries a Copilot trailer. 18 carry none (previously stated 15). Method: manual
  count of the trailer column; recount by `grep -ciE 'co-authored-by: *claude'` over each body of `git log 74330157cb --follow -- AGENTS.md` (corrected 2026-11-12, see errata #27).
- **Triggers that can be identified:**
  - issue #493 (rev 23);
  - storytold/cadcraft#1785 (rev 32);
  - a CodeRabbit review comment (rev 38);
  - craftrules/craft-contrib standards: revs 12, 22, 26, 34, 35, 36.
  - Most other revisions follow features: each new crate or xtask gate is documented in the same PR.

---

## 2. Verbatim rule catalogue (HEAD = 74330157cb)

### 2.1 House rules (core block; source `storytold/craft-contrib` `standards/house-rules-core.md` @ `dde09ea31e`)
| Rule | Citation | Verbatim (excerpt) |
|---|---|---|
| Scope | HEAD:AGENTS.md:4 | "These apply in every Craft repository. A later rule may be stricter, not weaker. … Propose changes there, not in a copy." |
| 1 Accountability | :6 | "**A person is accountable.** Whoever runs an agent answers for what it opens and for its review comments." |
| 2 Claiming | :7 | "**Check, then claim.** … search pull requests for `#N` … Comment on the issue first. Release a claim you will not finish." |
| 3 | :8 | "**Verify, don't guess.** Open a definition before using it." |
| 4 | :9 | "**Keep fixes narrow and tested.** … Add a test that fails without the fix." |
| 5 | :10 | "**Review the diff before opening a pull request.** Identifiers exist as used, the test fails without the fix, nothing unrelated changed, and the description is true." |
| 6 | :11 | "**Look for a better pull request.** If another fixes the same thing, close yours when it is better or equal" |
| 7 | :12 | "**Report only what ran.** … Without a local build or test, say so and rely on CI before marking ready." |
| 8 main | :13 | "**`main` changes through a pull request.** Do not push to it. Branch protection enforces this. There is no exception." |
| 9 Stop-and-ask | :14 | "**Stop and ask only about** licensing outside the allowlist, publishing, releases, a new remote, secrets, spending money, destructive git, and anything else hard to undo. Otherwise keep working. `plan/` is a gitignored notebook, not rules." |
| 10 | :15 | "**Keep secrets and personal details out** of the repository, logs and requests." |
| 11 CI | :16 | "**CI stays shared.** Workflows call `storytold/craft-common-actions`. Do not change CI in a feature or fix pull request." |
| 12 | :17 | "**Guards say why.** A check that looks removable says what it prevents." |
| 13 | :18 | "**Instructions must be readable by everyone.** No notes about one machine, and no links to files a reader cannot open. `craftrules` is retired. Do not link to it." |
| 14 PR SLA | :19 | "Respond in 7 days, a reminder at 14, closure eligible at 30 … A maintainer decides closure; it is never automatic. Reuse search results, do not poll, and stop at a rate limit." |
| 15 Attribution | :20 | "**No agent attribution.** A pull request does not say an agent wrote it. A repository rule may not require that." |

### 2.2 Rust Craft repositories block (source `standards/house-rules-rust.md`)
| Rule | Citation | Verbatim (excerpt) |
|---|---|---|
| 1 Never crash | HEAD:AGENTS.md:27 | "Non-test code does not panic and has no `unsafe`, except where the repository file names an exception. … Every crash fix comes with a test that panicked before the fix." |
| 2 Clean room | :28 | "Learn from observed behaviour and public specifications. Do not copy another product's code, assets, strings or artwork. Check a dependency's licence before adding it." |
| 3 Assets/fonts | :29 | "recorded in `ATTRIBUTION.md` in the same change. Font files live in storytold/craft-fonts" |
| 4 Rust only | :30 | "No handwritten JavaScript or TypeScript, and no Tauri, Electron or webview shell … Craft PR Review's existing Tauri and TypeScript UI is one such exception." |
| 5 chrono | :31 | "**Time goes through `chrono`.** Do not hand-roll calendar conversion." |
| 6 Credits | :32 | "Add or edit only your own person's entry in `contributors/people.toml`, and only after asking them. Never guess a name or hand-edit `contributors.json`." |
| Licence allowlist | :34–51 | "An expression is allowed when every identifier is in this list. A repository may name a shorter list. It may not add an identifier here by editing its own copy". List: ISC, MIT, BSD-2/3-Clause, Apache-2.0, OFL-1.1, Ubuntu-font-1.0, Bitstream-Vera, CC0-1.0, CC-BY-4.0, CC-BY-SA-4.0, LicenseRef-Public-Domain |

### 2.3 Repository-specific body
| Topic | Citation | Verbatim (excerpt) |
|---|---|---|
| Audience | HEAD:AGENTS.md:54 | "# AGENTS.md: guide for AI agents and contributors" |
| Mission | :56 | "The goal is 1:1 Photoshop parity … and every feature drivable by agents. Read this file first, then `docs/`." |
| Orientation | :58–75 | Table of 14 rows: architecture, development, contributing, control-protocol, ui-design, ROADMAP, target-app-parity, gaps, roadmap, per-dimension parity, parity-checklist, scorecard, crate READMEs, photocraft-corpus |
| Workspace map / layering | :77–99 | "**Layering is enforced** by `cargo xtask layers`. A crate may depend only on lower layers. … A new crate must be registered in `xtask/src/layers.rs`." |
| Never crash | :103–114 | "### Never crash (outranks feature work)" … "**Non-test code never panics.** No `unwrap()`, `expect()`, `panic!` …" … "**Enforced by clippy.**" |
| Golden rule 1 | :116 | "**Everything is a command.** … The UI, CLI, control channel and MCP all dispatch commands by id." |
| Rule 3 Clean-room | :118 | "We studied Photoshop and other proprietary editors for *behaviour and look only*. Never copy their code, shaders, profiles or assets." |
| Rule 4 | :119 | "**Tests are the gate.** Every change comes with tests." |
| Rule 6 | :121 | "**Screenshots that show a PR's change (before/after evidence) go in the PR description, never in the repo**" … "use a generic `Photocraft-dev` User-Agent." |
| Rule 9 | :125 | "The `panic_hunt` integration test fuzzes every command with adversarial params and must stay green." |
| Picking work | :129–143 | "Priorities: important infrastructure first, then low-hanging parity, then the long tail." … "When parity rises, raise `FLOOR` … (never lower it)." |
| Definition of done | :145–160 | 10 gate commands (`cargo test`, `clippy -D warnings`, `xtask layers`, `panel-commands`, `wasm`, `parity`, `panic_hunt`, `scorecard`, `perf --quick`, `test-corpus`), most conditional on what was touched |
| Session hand-off | :168 | "Then append a terse entry to `log/devlog.md` … Sessions can end abruptly (crashes, context limits), so the dev log plus a green tree is how the next agent picks up. Keep the tree building at every step." |
| §6 Parallel agents | :172 | "Use your own target dir (`CARGO_TARGET_DIR=target/agent-<name>`) to avoid the Cargo build lock, and edit only the files you own. Shared files (…) get small, surgical edits; re-read before editing." |
| | :173 | "Put new commands in a **new module** (`engine/src/<area>_cmds.rs` with a `specs()` function) rather than growing a shared file." |
| | :174 | "If someone else's in-progress edit breaks the build, wait and retry; don't fix their files." |
| | :175 | "**Create or rewrite manifests atomically**: write to a temp file outside `crates/`, then `mv` it into place." |
| | :176 | "Disk space: each target dir is about 10 GB. Delete `target/agent-*` dirs of finished agents." |
| §7 Tracking | :181–187 | roadmap, parity docs, scorecard, releasing; "`plan/` is an optional gitignored notebook … Do not ask for it and do not stop when it is absent." "`log/` (local, gitignored): the dev log." |
| §8 Native format | :191–194 | "`photocraft-format` deliberately fails to compile when a `photocraft-doc` struct gains a field" |
| Credits | :201–209 | "**Agents working for a contributor:** … ask them once whether they want to be credited … add **only their own** entry … Never add, edit, guess or copy anyone else's entry" |
| CI workflows | :212–214 | "Don't add or change CI in a feature or fix PR." "Moving a job into craft-common-actions is its own task, never part of another PR" |

---

## 3. Other agent-instruction / agent-config files (all refs)

Method:
```
git log --all --diff-filter=AD --name-status -- 'CLAUDE.md' '**/CLAUDE.md' '.claude/**' '.codex/**'
  '.cursor/**' '.cursorrules' '.github/copilot-instructions.md' 'GEMINI.md' '**/AGENTS.md' '.mcp.json'
  '.coderabbit.yaml' 'sonar-project.properties' '.github/PULL_REQUEST_TEMPLATE*'
  '.github/ISSUE_TEMPLATE/**' 'CODEOWNERS' '.github/CODEOWNERS' '.git-blame-ignore-revs'
  '.github/instructions/**' '.github/prompts/**'
```
Containing refs were found with `git for-each-ref --contains`. Presence at HEAD was checked with
`git cat-file -e HEAD:<path>`.

| File | Exists at HEAD | Ever on main | Added / removed | Only ref(s) | Contents / notes |
|---|---|---|---|---|---|
| `AGENTS.md` (root) | yes | yes | 16941f7198 (09-30) | main | §1–2 |
| `docs/user/AGENTS.md` | yes (60 lines) | yes | c6fd71241d 2026-10-19, Fabio Lussi, PR #3951 | main | Rules for user docs: "Who reads this: Artists …, Discord mods …, and AI assistants looking things up" (HEAD:docs/user/AGENTS.md:10–11). Page rules, frontmatter, "Set `verified` to the latest release" (:38). Support PRs titled `docs(support): …`, "Review them like code: check every claim against the source" (:59–60). Its checker lives in another repo, and "A CI check will be added once it is on that repo's main branch" (:55) |
| `docs/user/CLAUDE.md` | yes (1 line) | yes | c6fd71241d | main | "Read `AGENTS.md` in this folder: it has the rules for the user docs." (:1). This is the only CLAUDE.md on main: a redirect stub |
| `CLAUDE.md` (root) | **no** | **no** | added 5aed6c2a25 (2026-10-08, Cody Chu), deleted 698f430be9 (2026-10-31, author "Claude", `Claude-Session:` trailer) | `refs/pull/11086/head` only | "Comfy PhotoCraft" fork entry point (68 lines). Has a "Delegation" section (E02-022). The deleting commit says CLAUDE.md is now "Untracked and gitignored (kept on the owner's PC)" |
| `.claude/skills/codebase-cartography-audit/**` (SKILL.md, PROMPT.md, 13 references, 6 scripts, 1 template) | no | no | 0407b1d835 / 366002fac6 / 9f4ba289d9 (2026-10-14, author "Claude") | `refs/pull/5433/head` only (fork of jeffreypalermo, via branch `claude/exciting-wright-g441bf`) | Claude skill: codebase audit with C4 diagrams, function points and "economic valuation". It says "Use when … reviewing AI-written changes at scale" and adapts itself "to … the cloud container" |
| `.cursor/rules/integration-safety.mdc` | no | no | 394f55c2f1 (2026-10-22, benjarogit) | `refs/pull/8540/head` only | `alwaysApply: true`. Temp-file, path, download allow-list and OAuth rules. Ends "rebase on the PR's current base before requesting review, and report only checks that were actually run" |
| `examples/{extensions,plugins}/*/AGENTS.md` (5 files) | no | no | 2b6aa0f5c8 (2026-10-16, brandongunderson) | `refs/pull/6479/head` only | Per-example guides (not read in depth) |
| `.github/ISSUE_TEMPLATE/*` | no | no | 00b3999846 (#6137), 0be8d35bc8 (#1312), 8172d204d1 (#5596, includes `joke_request.yml`) | PR refs only | Never merged, so main has **no issue templates** |
| `.coderabbit.yaml` | yes (6 lines) | yes | 9b9643764f 2026-10-20, Brandon Thomas, PR #7991 | main | Only setting: skip auto-review for `dependabot[bot]` (HEAD:.coderabbit.yaml:2–6). CodeRabbit runs with default config otherwise (it reviewed #13206 and #11632; E02-015) |
| `sonar-project.properties` | yes (2 lines) | yes | 87fa191818 2026-10-21, Dylan M. Taylor | main (+ two other PR-only adds) | `sonar.projectKey=storytold_photocraft`, `sonar.organization=storytold` |
| `.git-blame-ignore-revs` | yes (3 lines) | yes | 574d4fe7da 2026-10-04 | main (deleted only on PR refs #7212, #7649) | One rustfmt mass-format commit, f7eb6ea9e7 |
| `.github/dependabot.yml` | yes | yes | 9185b64b94 2026-10-18 | main | Cargo + Actions |
| `.github/workflows/house-rules.yml` | yes | yes | 7d8648dfcb 2026-11-06 | main | §4 |

**Not found on any ref** (same `git log --all` search returned nothing): `.github/PULL_REQUEST_TEMPLATE*`,
`.github/pull_request_template*`, `CODEOWNERS` (root, `.github/`, `docs/`), `.mcp.json`, `GEMINI.md`,
`.github/copilot-instructions.md`, `.github/instructions/**`, `.github/prompts/**`, `.codex/**`,
`.cursorrules`. `.dockerignore` lists `.agents` and `.codex` (HEAD:.dockerignore:3–4, added f0ae12dd22,
PR #1334). These directories are therefore expected in some contributors' local checkouts, but they are not
tracked. `docs/development.md` mentions `.mcp.json` only as a user configuration example for the product's
MCP server (HEAD:docs/development.md:363).

---

## 4. House rules: what is enforced mechanically vs only stated

| Rule / claim | Mechanism found | Status |
|---|---|---|
| The house-rules copy in AGENTS.md matches craft-contrib | `.github/workflows/house-rules.yml` triggers on push/PR touching `AGENTS.md`, `CLAUDE.md` or the workflow (HEAD:.github/workflows/house-rules.yml:3–15). It calls `storytold/craft-common-actions/.github/workflows/house-rules.yml@main` with `rust: true` (:26–28). The reusable workflow's code is not in this repo. Block hashes match the text (E02-012) | Mechanical (the check's logic is external, unseen) |
| 8: main only via PR, "Branch protection enforces this" | GitHub setting, not visible in git | Stated. Not verifiable from the clone |
| 11 / CI section: workflows only call craft-common-actions | `ci.yml` calls `gate.yml@main` (HEAD:.github/workflows/ci.yml:154) but still runs many local jobs. AGENTS.md:214 admits "Some workflow files here still run their own jobs" | Partially followed. No check found |
| Never crash: no unwrap/expect/panic, no unsafe | `Cargo.toml` `[workspace.lints.rust] unsafe_code = "forbid"` (HEAD:Cargo.toml:97–98). `clippy.toml` test-only allowances. `cargo xtask ci` runs clippy -D warnings and `panic_hunt` (HEAD:xtask/src/main.rs:33–34) | Mechanical |
| Layering | `cargo xtask layers` in CI (HEAD:.github/workflows/ci.yml:263; xtask ci) | Mechanical |
| Rule 1: UI dispatches commands | `cargo xtask panel-commands` with a shrink-only allowlist (commit 4165c57f92) | Mechanical |
| Scorecard / parity docs regenerated | `scorecard --check` in `xtask ci` | Mechanical |
| Licence allowlist | No `deny.toml`, no cargo-deny, no SPDX check found in `xtask/`, `scripts/` or `.github/` (`grep -rli 'spdx\|cargo.deny'` matched only `xtask/src/corpus_pins.rs`) | **Stated only** (unless inside external gate.yml, unknown) |
| Clean room, "never read/copy proprietary code" | none possible | Stated only |
| 2 Check-then-claim, 5 review diff, 6 better PR, 7 report only what ran, 14 PR timing | none in repo (no bot config, no PR template) | Stated only |
| 15 No agent attribution | none. Contradicted in practice by trailers (E02-016) and by the About ▸ Models feature (E02-017) | Stated only. Not followed |
| 9 Stop-and-ask list (releases etc.) | Releases are partly gated by the GitHub `release` environment, usable only from the `release` branch, and drafts are published by a maintainer (HEAD:docs/releasing.md:3–6, :58) | Partly mechanical |
| Assets in ATTRIBUTION.md, fonts not committed | none found | Stated only |

**craftrules → craft-contrib timeline** (VERIFIED from AGENTS.md history):

| Date | Revision | Event |
|---|---|---|
| 2026-10-01 | `1f1ddb2a47` | First pointer: "Standards and learnings shared across the crafting apps live in `../craftrules`" |
| 2026-10-01 | `1d61b33c54` | Release playbook moved there |
| 2026-10-04 | `50a27e6c74` | Never-crash std cited from there |
| 2026-10-07 | `44303db546` | contributors.py cited from there |
| 2026-10-10 | `939c8f2c70` | progress-docs std cited from there |
| 2026-10-08 | `f9b72468b4` | Repo acknowledged as non-public (issue #493) |
| 2026-10-31 | `6d737c219e` | All `../craftrules` references removed |
| 2026-11-06 | `7d8648dfcb` | Replaced by the public `storytold/craft-contrib` blocks plus rule 13 "`craftrules` is retired. Do not link to it." |

---

## 5. Contributor-facing docs

| Doc | Size / revs (main, `--follow`) | Process content |
|---|---|---|
| `docs/contributing.md` | 26 lines, 12 revs, first 16941f7198 | Rust only, MIT OR Apache-2.0, clean-room, never crash, commands not handlers, layering, tests, style. "**UI:** … attach before/after screenshots to PRs" (HEAD:docs/contributing.md:11). "**Commits:** small, focused, with a clear subject line." (:12). 7-step "Adding a command" checklist (:14–26). **No** review policy, no AI policy, no trailer convention |
| `docs/development.md` | 1,178 lines, 169 revs | Build/test, "`cargo xtask ci` # the CI gate: fmt, clippy, layers, scorecard, tests, panic_hunt, doctests, wasm, i18n report" (HEAD:docs/development.md:45). Faster loops and nextest (:56–67). Timing-claim hygiene: "No speedup should be claimed from changing the 60-second warning threshold or omitting tests." (:84). "MCP (agents)" (:321–408) is a product feature, with `agent_tasks.rs` as the MCP reference test (:395). No agent dev-process rules beyond AGENTS.md |
| `docs/decisions.md` | 34 lines, 2 entries at HEAD | Titled "Implementation decisions". Format: `## YYYY-MM-DD: <title> (#issue)` followed by prose rationale. **Not a numbered ADR log** (no status, context or consequences fields). Entries: 2026-10-10 Smart Object contents identity (#2163), from 607a8542f5 (Harrison O'Connor-Hoover, PR #2222); 2026-10-17 replaced file's ACL/named streams, from 8c12449819 (skylar taylor-barrick). A third entry, "2026-10-13: Editable starter actions (#4779)" (5d8980222a etc., harrisonoconnorhover), is absent at HEAD. 255ecc81d0 (FredApps, "Remove 21 requested PR contributions from the 108-PR integration") shows a version without it. No rule says who records decisions. AGENTS.md does not mention decisions.md (grep: 0 hits) |
| `docs/contributors.md` | 41 lines, 4 revs | "**About ▸ Models** credits the AI models named in `Co-Authored-By` trailers." (HEAD:docs/contributors.md:3–4). Self-credit rules (:29–41) |
| `SECURITY.md` | 52 lines, 3 revs (first 1fe689a7bf, Gh0stly, #35) | Vulnerability handling. "This repository does not currently document a dedicated private security email or private reporting channel." (HEAD:SECURITY.md:9). Nothing on agents or AI |
| `book/src/getting-started/contributing.md` | 18 lines (1fe689a7bf) | "Read `AGENTS.md` and the existing contribution guide before editing source." (HEAD:book/src/getting-started/contributing.md:3). Security-sensitive contributions must "State whether a change adds an implemented control, documents a limitation, or proposes later hardening." (:16) |

**AI-use policy and trailers.**
- `git grep -i` at HEAD for `Claude-Session`, `Model-Effort`, `Copilot-Session` → 0 files. `AI-generated` → 0.
  `trailer` → only HEAD:docs/contributors.md:4.
- No doc requires or forbids AI disclosure in commits. The only AI-attribution rule is house rule 15
  (PR text, not commits).
- Localization docs disclose AI tools per catalog, e.g. "Core terminology, contexts and plural messages
  were edited with OpenAI Codex." and "Automated checks and AI-assisted edits do not replace that review."
  (HEAD:docs/localization-az.md:30–37; also docs/localization-ru.md:54, localization-parity.md:68).

---

## 6. Matrix: topic → documented? where? since when?

| Topic | Documented? | Where (HEAD) | Since (sha, date) |
|---|---|---|---|
| Read-first orientation for agents | Yes | AGENTS.md:54–75; README "New contributors and AI agents: start with AGENTS.md" (README.md:276) | 16941f7198, 09-30 |
| Parallel agents: separate target dirs | Yes | AGENTS.md:172 | 16941f7198, 09-30 |
| Parallel agents: file ownership, shared-file edits, new modules, wait-and-retry | Yes | AGENTS.md:172–174 | 536a7346fb, 10-01 |
| Atomic manifest writes | Yes | AGENTS.md:175 | ae92ac20bf, 09-30 |
| Clean up agent target dirs | Yes | AGENTS.md:176 | 536a7346fb, 10-01 |
| Git worktrees | **No** rule. Only ad-hoc perf-doc recipes (`git worktree add --detach …`, e.g. docs/oil-paint-performance.md:89) and CI baseline (ci.yml:713) | — | — |
| Subagents / orchestration / delegation | **No** on main (grep `subagent` 0 hits; `orchestrat` only product code). Only the fork CLAUDE.md "Delegation" on PR #11086 | refs/pull/11086/head:CLAUDE.md:63–68 | 5aed6c2a25 (never merged) |
| Cross-session state / memory | Yes: `log/devlog.md` (gitignored) plus green tree; `plan/` optional notebook | AGENTS.md:141, :168, :186–187; .gitignore:2,7 | devlog 536a7346fb; `plan/` "do not ask" 7d8648dfcb, 11-06 |
| Context limits | Mentioned once: "Sessions can end abruptly (crashes, context limits)" | AGENTS.md:168 | 536a7346fb |
| Picking work / claiming | Yes: gaps.md ranked list "take the highest-ranked entry that nobody is working on" (docs/gaps.md:6–7); claim via issue comment (house rule 2) | AGENTS.md:7, :127–143 | 536a7346fb; claim rule 7d8648dfcb |
| Definition of done / quality gates | Yes | AGENTS.md:145–168; development.md:45 | grown from 4 commands (09-30) to 10 |
| Effort unit = agent-hours | Yes: "Hours are Opus 5.5 agent-hours, one agent working sequentially … **Human** marks what an agent can't finish alone." | docs/gaps.md:15–16; docs/roadmap.md:20–21; calibration docs/target-app-parity.md:203–222 | 939c8f2c70, 10-10 |
| Human approval / stop-and-ask | Yes | AGENTS.md:14 | 7d8648dfcb, 11-06 |
| Push to main | Forbidden | AGENTS.md:13 | 7d8648dfcb |
| Force-push / destructive git | Only via "destructive git" in the stop-and-ask list | AGENTS.md:14 | 7d8648dfcb |
| Merging PRs (who may merge) | **Not documented** (searched `merge`, `approv`, `reviewer`, `code review` in AGENTS/contributing/development/README/SECURITY/releasing) | — | — |
| Review requirements (number of approvals, CODEOWNERS) | **Not documented**; no CODEOWNERS on any ref | — | — |
| Running releases | Stop-and-ask, plus maintainer publishes drafts | AGENTS.md:14; docs/releasing.md:3–6 | releasing 10-01; rule 11-06 |
| Touching CI | Forbidden in feature/fix PRs | AGENTS.md:16, :212–214 | 0379569d00, 10-29 |
| Adding dependencies | "Check a dependency's licence before adding it" plus allowlist | AGENTS.md:28, :34–51 | 7d8648dfcb |
| Clean-room ("never copy their code") | Yes. Does not explicitly say "never read" proprietary source | AGENTS.md:28, :118; contributing.md:5 | 16941f7198 |
| Secrets / personal data in requests | Yes ("generic `Photocraft-dev` User-Agent") | AGENTS.md:15, :121 | 536a7346fb |
| Agent attribution in PRs | Forbidden in PR text | AGENTS.md:20 | 7d8648dfcb, 11-06 |
| Commit trailers (`Co-Authored-By`, `Claude-Session`, `Model-Effort`) | **Not documented** as a rule. `Co-Authored-By` trailers are consumed for About ▸ Models | docs/contributors.md:3–4 | 44303db546, 10-07 |
| Contributor credits by agents | Yes ("ask them once") | AGENTS.md:196–209 | 44303db546 |
| Screenshots in PRs | Yes | AGENTS.md:121; contributing.md:11 | 0cc411241b, 11-11 |
| PR responsiveness SLA | Yes (7/14/30 days) | AGENTS.md:19 | 7d8648dfcb |
| Bot reviewers (CodeRabbit, Sonar) | Config only, no rule on how to treat findings except "unconfirmed bot findings do not start the clock" | .coderabbit.yaml; AGENTS.md:19 | 10-20 / 10-21 |
| Issue/PR templates | **None** on main | — | — |
| Decision records | Informal dated log, 2 entries | docs/decisions.md | 607a8542f5, 10-10 |
| Tool permissions (allowed shell commands, sandbox) | **Not documented** (no `.claude/settings*`, no permission lists on any ref) | — | — |

---

## 7. Evidence entries

### E02-001 — AGENTS.md is the canonical agent guide, addressed to both AI agents and contributors
- Label: VERIFIED
- Source: HEAD:AGENTS.md:54; HEAD:README.md:276; HEAD:book/src/getting-started/contributing.md:3
- Quote/Data: "# AGENTS.md: guide for AI agents and contributors"; "New contributors and AI agents: start with [`AGENTS.md`]"
- Method: `cat -n AGENTS.md`; `git grep -n -i agent HEAD -- README.md`
- Notes: 24,989 bytes / 214 lines (`wc -c`, `wc -l`).

### E02-002 — AGENTS.md has 38 revisions over 43 days; it started as a 62-line "one-shot"
- Label: VERIFIED
- Source: commits 16941f7198 (2026-09-30) … 0d9a9a5a70 (2026-11-11)
- Data: 38 revisions; the first adds 62 lines (`--numstat`)
- Method: `git log --follow --format=%h -- AGENTS.md | wc -l`
- Notes: Full table in §1.

### E02-003 — The parallel-agents section existed from day one and was expanded on day two
- Label: VERIFIED
- Source: 16941f7198:AGENTS.md:56; 536a7346fb (2026-10-01) diff; HEAD:AGENTS.md:170–176
- Quote: "Parallel agents: use your own target dir (`CARGO_TARGET_DIR=target/agent-<name>`) to avoid the Cargo build lock, and edit only the crates you own." (16941f7198:AGENTS.md:56)
- Notes:
  - Day 2 promoted it to "## 6. Parallel agents" with five bullets: shared-file etiquette, new modules,
    wait-and-retry, atomic manifests, disk space.
  - It has been unchanged since 2026-10-01.
  - It assumes several agents edit one working tree concurrently: "If someone else's in-progress edit
    breaks the build, wait and retry".
  - Worktrees are not mentioned. INFERRED: the Cargo-lock and manifest-glob concerns point to a shared
    checkout.

### E02-004 — State hand-off between agent sessions is the gitignored dev log plus a green tree
- Label: VERIFIED
- Source: HEAD:AGENTS.md:168, :141, :187; HEAD:.gitignore:7; introduced 536a7346fb (2026-10-01)
- Quote: "Sessions can end abruptly (crashes, context limits), so the dev log plus a green tree is how the next agent picks up."
- Notes:
  - `log/` is local and not in git, so the hand-off medium is invisible to outside contributors and to
    this study.
  - The fork CLAUDE.md, by contrast, kept its devlog in-tree "so it survives machines and agents"
    (refs/pull/11086/head:CLAUDE.md:20–21).

### E02-005 — Definition of done grew from 4 to 10 gate commands, each added with its tool
- Label: VERIFIED
- Source: 16941f7198:AGENTS.md:49–54 (4 commands); HEAD:AGENTS.md:147–160 (10 commands)
- Notes: Additions and their revisions:

  | Gate | Revision |
  |---|---|
  | parity | 536a7346fb |
  | panic_hunt | a196adfe93 |
  | scorecard, perf | 0f955e6c82 |
  | test-corpus | 968baf639e |
  | panel-commands | 4165c57f92 |

  The pattern: each new xtask gate is documented in AGENTS.md in the same PR that builds it.

### E02-006 — Never-crash rules were steered by AGENTS.md and backed by lints and a fuzz test
- Label: VERIFIED
- Source: ed0b99964d (2026-10-04, Co-Authored-By Claude Opus 4.8); 50a27e6c74 (PR #33); HEAD:AGENTS.md:103–114, :125; HEAD:Cargo.toml:97–98; HEAD:xtask/src/main.rs:33–34
- Quote: 50a27e6c74 message: "AGENTS.md gets a prominent "Never crash" section at the top of the golden rules"; title "Never crash: steering rules, clippy.toml, forbid unsafe"
- Notes: The commit author calls them "steering rules", which marks AGENTS.md as a deliberate agent-steering
  tool. CI enforces them through clippy and `panic_hunt`.

### E02-007 — Work selection is document-driven and ranked for agents
- Label: VERIFIED
- Source: HEAD:AGENTS.md:129–143; HEAD:docs/gaps.md:6–7
- Quote: "This is the work list agents pick from: take the highest-ranked entry that nobody is working on" (docs/gaps.md:6–7)
- Notes: The order evolved:

  | Revision | Order of where to pick work |
  |---|---|
  | 536a7346fb | roadmap → parity → devlog |
  | 433b84fae7 | honest assessment first |
  | 0f955e6c82 | scorecard |
  | 939c8f2c70 | ROADMAP.md → gaps.md |

### E02-008 — Effort is planned in "Opus 5.5 agent-hours", with a "Human" marker for what agents can't do alone
- Label: VERIFIED
- Source: HEAD:docs/gaps.md:15–16; HEAD:docs/roadmap.md:20–21; HEAD:docs/target-app-parity.md:203–222; introduced 939c8f2c70 (2026-10-10, PR #2696)
- Quote: "Hours are Opus 5.5 agent-hours, one agent working sequentially, including tests. **Human** marks what an agent can't finish alone."
- Notes:
  - The calibration claims "~1,000 PRs so far represent about **2,000–4,000 agent-hours**". This is
    the project's own estimate, not a measurement; it is cited as documented, not as fact.
  - Examples of Human items: "opening exports in Photoshop on the owner's Mac", "owner decision #41"
    (docs/gaps.md:66, :244).

### E02-009 — Stop-and-ask list and main-protection rule, added 2026-11-06
- Label: VERIFIED
- Source: HEAD:AGENTS.md:13–14; 7d8648dfcb (PR #11632)
- Quote: "**Stop and ask only about** licensing outside the allowlist, publishing, releases, a new remote, secrets, spending money, destructive git, and anything else hard to undo. Otherwise keep working."
- Notes:
  - Before 2026-11-06, no AGENTS.md revision listed human-approval points (checked by reading every diff).
  - "Branch protection enforces this" cannot be verified from git.

### E02-010 — Explicit anti-stall instruction about the missing `plan/`
- Label: VERIFIED
- Source: HEAD:AGENTS.md:14, :186; earlier 16941f7198:AGENTS.md:60 ("`plan/` (local, gitignored): research, parity plan, execution plan, estimates.")
- Quote: "Do not ask for it and do not stop when it is absent."
- Notes:
  - INFERRED: written because agents without the owner's private `plan/` stopped or asked for it. The
    PR #11632 description (via WebFetch summary, accessed 2026-11-12) says only that "`plan/` is an
    optional notebook (core rule 9)".
  - No incident commit was found.

### E02-011 — "No agent attribution" in PRs is a house rule since 2026-11-06
- Label: VERIFIED
- Source: HEAD:AGENTS.md:20; 7d8648dfcb
- Quote: "**No agent attribution.** A pull request does not say an agent wrote it. A repository rule may not require that."
- Notes:
  - The WebFetch summary of craft-contrib `standards/house-rules-core.md` (accessed 2026-11-12) gives the
    same first sentence verbatim but paraphrases the second sentence inversely ("though a repository rule
    may require it").
  - The local copy is authoritative: hash-verified, E02-012.
  - The rule covers PRs, not commit trailers.

### E02-012 — The house-rules blocks are byte-exact copies, verified by sha256
- Label: VERIFIED
- Source: HEAD:AGENTS.md:1, :22 (headers); HEAD:.github/workflows/house-rules.yml:1–28
- Data:

  | Command | Output | Header value |
  |---|---|---|
  | `sed -n '2,20p' AGENTS.md \| sha256sum` | `540e6cea…92bb` | core header |
  | `sed -n '23,51p' AGENTS.md \| sha256sum` | `387e0ccb…3013` | rust header |

  Both outputs equal the header values.
- Notes:
  - The checking logic is the external reusable workflow `craft-common-actions/.../house-rules.yml@main`,
    not inspected.
  - The workflow also watches `CLAUDE.md` although none exists on main. Commit 0379569d00 also says
    "AGENTS.md (and CLAUDE.md where present)". INFERRED: an org-wide template for sibling repos that do
    have CLAUDE.md.

### E02-013 — craftrules was a private shared-standards repo, retired in favour of public craft-contrib
- Label: VERIFIED
- Source: 1f1ddb2a47 (2026-10-01); f9b72468b4 (2026-10-08, PR #779, issue #493); 6d737c219e (2026-10-31, PR #10420); HEAD:AGENTS.md:18
- Quote: f9b72468b4 message: "the repository returns 404 to everyone outside the organization, so the cited text is unreachable for outside contributors"; rule 13: "`craftrules` is retired. Do not link to it."
- Notes: Standards cited from craftrules: `never-crash.md`, `progress-docs.md`, `contributors.md`,
  `fonts.md`, `release/playbook.md`, `scripts/contributors.py`. Their content is not available in this
  clone.

### E02-014 — CI is centralised and off-limits to feature PRs
- Label: VERIFIED
- Source: 0379569d00 (2026-10-29, PR #10228); HEAD:AGENTS.md:16, :212–214; HEAD:.github/workflows/ci.yml:154
- Quote: "Don't add or change CI in a feature or fix PR."
- Notes: Partially aspirational: AGENTS.md:214 says some local jobs remain, and ci.yml still defines
  local jobs alongside `gate.yml@main`.

### E02-015 — Bot review feeds back into the agent rules
- Label: VERIFIED
- Source: 0d9a9a5a70 (2026-11-11) message
- Quote: "CodeRabbit on #13206: docs/multi-channel-editing.md displays before/after comparisons, which the rule keeps"
- Notes:
  - PR #11632 also received CodeRabbit comments, among them one on the licence allowlist versus the
    `unicode-ident` licence, and a human comment by eliets2 about pinning `@main` (WebFetch summary of
    https://github.com/storytold/photocraft/pull/11632, accessed 2026-11-12).
  - Whether those comments were resolved is unknown.

### E02-016 — Rule 15 notwithstanding, AI co-author trailers continue on main after 2026-11-06
- Label: VERIFIED
- Source: `git log main` counts
- Data:

  | Window | commits | `Co-Authored-By: Claude` | `Claude-Session:` | Copilot |
  |---|---|---|---|---|
  | until 2026-11-05 | 10,418 | 4,145 | 257 | 31 |
  | since 2026-11-06 | 1,799 | 498 | 15 | 0 |

  Overall: `Model-Effort:` 27 commits; `Co-Authored-By: Claude` 4,727 commits.
- Method: `git log main [--until|--since] -i --grep='Co-Authored-By: Claude' --format=%H | wc -l` (and the same for the other trailers)
- Notes:
  - Window boundary: date-only `--since/--until` use the current time of day, so the two windows cover 12,217 of 12,396 commits. With an exact cutoff at 7d8648dfcb's commit time, 1,805 commits follow it (499 with a Claude co-author) (cross-ref 2026-11-12, see errata #28). `Model-Effort:` 27 = 25 non-merge, all one contributor (cross-ref 2026-11-12, see errata #18).
  - Rule 15 governs PR text, so commit trailers do not strictly violate it.
  - The trailer share fell from ~40% to ~28%. INFERRED and confounded (who contributes changed); this is
    not proof of rule effect. Hand to the trailer stream.

### E02-017 — The product credits AI models from commit trailers (About ▸ Models)
- Label: VERIFIED
- Source: HEAD:docs/contributors.md:3–4; HEAD:crates/ui-egui/src/dialogs/credits.rs:505; HEAD:contributors/contributors.json:2470–2508 (ids `anthropic/claude-opus/5.5`, `anthropic/claude`, `anthropic/claude-opus/4.8`, `github/copilot`); introduced 44303db546 (2026-10-07, PR #898)
- Quote: "**About ▸ Models** credits the AI models named in `Co-Authored-By` trailers."
- Notes: This sits in tension with house rule 15 (E02-011). Both are documented and coexist at HEAD.

### E02-018 — Agents must ask their human before writing credit data
- Label: VERIFIED
- Source: HEAD:AGENTS.md:201–209, :32; 44303db546
- Quote: "**Agents working for a contributor:** … ask them once whether they want to be credited by more than their username"
- Notes: This is one of the few places where the docs model agents as "working for" a specific human.

### E02-019 — Clean-room rule forbids copying, not reading
- Label: VERIFIED
- Source: HEAD:AGENTS.md:28, :118; HEAD:docs/contributing.md:5; 16941f7198:AGENTS.md:41
- Quote: "We studied Photoshop and other proprietary editors for *behaviour and look only*. Never copy their code, shaders, profiles or assets."
- Notes:
  - No rule says agents must not read particular source code; the searched terms "never read" and "do not
    read" returned no hits in AGENTS.md or contributing.md.
  - A named product ("Photon Studio") was removed from the rule in 9c9a680e45.

### E02-020 — Common agent/process config files are absent on every ref
- Label: VERIFIED
- Source: `git log --all --diff-filter=AD` search (§3)
- Data: No PR template, CODEOWNERS, `.mcp.json`, GEMINI.md, copilot-instructions, `.codex/`, `.cursorrules`
  or `.github/prompts` on any ref. Issue templates exist only on unmerged PR refs (#1312, #5596, #6137).
- Notes: Review and ownership rules are therefore not encoded in repo config.

### E02-021 — CLAUDE.md exists on main only as a one-line redirect in docs/user
- Label: VERIFIED
- Source: HEAD:docs/user/CLAUDE.md:1; c6fd71241d (2026-10-19, PR #3951)
- Quote: "Read `AGENTS.md` in this folder: it has the rules for the user docs."
- Notes:
  - The repository standardises on AGENTS.md. CLAUDE.md is used only as a pointer.
  - The c6fd71241d message claims "a User docs rule in AGENTS.md", but root AGENTS.md is not in that
    commit's diff (`git show --stat`). The claim refers to docs/user/AGENTS.md (INFERRED).

### E02-022 — A fork's CLAUDE.md documents a multi-vendor delegation scheme (never merged)
- Label: VERIFIED
- Source: 5aed6c2a25:CLAUDE.md:63–68 (2026-10-08, Cody Chu), reachable only from refs/pull/11086/head
- Quote: "An orchestration skill routes grind work to Codex (read-only repo analysis, tests, git) and agy/Gemini (research, visual QA) when they are available. … Claude keeps architecture, implementation and acceptance."
- Notes:
  - This is a fork ("Comfy PhotoCraft") practice, not upstream policy.
  - It was later untracked by 698f430be9 (author "Claude", `Claude-Session:` trailer): "Untracked and
    gitignored (kept on the owner's PC): … CLAUDE.md".

### E02-023 — A Claude skill for auditing "AI-written changes at scale" was proposed in a fork PR
- Label: VERIFIED
- Source: refs/pull/5433/head:.claude/skills/codebase-cartography-audit/SKILL.md (commits 0407b1d835, 366002fac6, 2026-10-14, author "Claude"; merged in fork via branch `claude/exciting-wright-g441bf`)
- Quote: "Use when onboarding to PhotoCraft, reviewing AI-written changes at scale, or planning a refactor"
- Notes: Never on main. It shows outside contributors arriving with their own agent tooling.

### E02-024 — A Cursor rule set for agents was proposed in a PR, not merged
- Label: VERIFIED
- Source: 394f55c2f1:.cursor/rules/integration-safety.mdc:1–13 (2026-10-22, benjarogit; refs/pull/8540/head only)
- Quote: "Keep integrations reviewable: separate independent features into focused changes, rebase on the PR's current base before requesting review, and report only checks that were actually run."

### E02-025 — docs/decisions.md is a lightweight dated decision log, not an ADR system
- Label: VERIFIED
- Source: HEAD:docs/decisions.md:1–34; `git log --follow` (6 commits)
- Data: 2 entries at HEAD (2026-10-10 #2163; 2026-10-17 #7073/#7094/#7096). A third entry (2026-10-13
  #4779) appears only in side-branch revisions (5d8980222a, 5c60b4d50f, 2ecefa966a).
- Method: `grep -c '^## '` per revision
- Notes: Neither AGENTS.md nor contributing.md references it. Entries were written by feature authors in
  their own PRs.

### E02-026 — Rule changes are mostly co-authored with Claude and made in feature PRs
- Label: VERIFIED
- Source: §1 table
- Data: 19 of 38 AGENTS.md revisions carry a Claude co-author trailer (previously stated 21), 1 a Copilot trailer. Most edits ride
  along with feature PRs (#67, #190, #239, #255, #353, #898, #3498, #5941, …).
- Notes: AI involvement here counts only explicit trailers. The other 18 are "unknown" (previously stated 15) (corrected 2026-11-12, see errata #27).

### E02-027 — Machine-specific agent notes persist in docs despite rule 13
- Label: VERIFIED
- Source: HEAD:docs/tilt-shift-performance.md:4–5; HEAD:docs/egui-037-migration-plan.md:49, :1398–1402
- Quote: "Branch: `codex/tilt-shift-performance-20261010`. Worktree: `C:\Users\Colum\.codex\worktrees\6c32\photocraft`"; "`python3 /home/codex/work/maintenance/task.py run --job-id …`"
- Notes:
  - These are the only HEAD documentation hits for "worktree" tied to an agent tool (Codex worktrees) and
    for a task-runner wrapper.
  - House rule 13 ("No notes about one machine", 2026-11-06) is newer than both docs (2026-10-10 and
    2026-10-25).

### E02-028 — Integration-review records describe a per-PR local CI ritual
- Label: VERIFIED
- Source: HEAD:docs/integration-testing/approved-selection.json:7228, :7437
- Quote: "**Local CI** (fresh worktree merged with main, own target dir)"
- Notes: This is an observed practice in review bodies, not a documented rule. Lead for the
  integration/review stream.

---

## Open questions / uncertainties
- The contents of the external reusable workflows (`craft-common-actions` house-rules.yml and gate.yml)
  are not in the clone. So it is unknown:
  - what exactly the house-rules check verifies (presence, position, hash, source sha);
  - whether gate.yml checks licences.
- Branch-protection settings and required-review counts are not visible in git.
- The private `craftrules` standards, and the local `plan/` and `log/devlog.md`, are unavailable. The main
  inter-session memory artefact cannot be examined.
- Why `plan/` "do not ask / do not stop" was added: no incident commit was found (E02-010 is INFERRED).
- craft-contrib rule 15 wording was seen only via a WebFetch summary, which paraphrased it inconsistently.
  The local hash-verified copy is used instead.
- Whether the PR-only agent configs (#11086, #5433, #8540, #6479) were closed or merely left open was not
  checked (no API access; WebFetch was not run for each).
- Decision #4779's disappearance from decisions.md: the side-branch history was not fully traced.

## Leads for other streams
- **Trailer/attribution stream:**
  - E02-016 counts, including 27 `Model-Effort:` trailers on main.
  - Authors literally named "Claude" (0407b1d835, 698f430be9).
  - "(1M context)" trailers (3092d3b6f9, 4165c57f92).
  - Claude Opus 4.8 trailers (ed0b99964d, a196adfe93).
  - Copilot-Session trailer (7b3d131bc8).
- **Branch stream:** 38 `claude/*` and 5 `codex/*` remote branches (`git branch -r | grep -c`).
  `claude/integ-batch-1..11`. Codex branch `codex/ui-suite-integration-20261010` landed an AGENTS.md change
  (99a3970399 via PR #3097).
- **Integration stream:**
  - `docs/integration-testing/*` (approved-selection.json, integration-checkpoint.md, per-pr-regressions.md).
  - 255ecc81d0 "Remove 21 requested PR contributions from the 108-PR integration" (FredApps, 2026-10-29).
  - Integration branches such as `integration-6` (PR #8094).
- **CI stream:** `house-rules.yml` (7d8648dfcb); `0379569d00` moved windows-arm64 from a SHA pin to `@main`
  ("Intentionally tracked at @main …"); eliets2's objection on #11632.
- **Bot-review stream:** `.coderabbit.yaml` (9b9643764f); CodeRabbit comments driving rule edits
  (0d9a9a5a70); SonarCloud (87fa191818, PR #9770 "sonar/enforce-clippy-standards").
- **Cross-repo:** storytold/cadcraft#1785 triggered the chrono rule (6649b78526); storytold/craft-libs,
  craft-fonts, craft-i18n, photocraft-corpus (it has its own AGENTS.md per HEAD:AGENTS.md:164).
- **Localization stream:** AI-tool disclosure in localization docs (docs/localization-az.md:30–37).

## Methods-relevant takeaways
- Keep one agent-instruction file (AGENTS.md) as the canonical entry point. Point other tool-specific
  files (CLAUDE.md) at it rather than duplicating it (E02-001, E02-021).
- Document a new mechanical gate in the agent guide in the same PR that builds it, so the definition of
  done tracks the tooling (E02-005, E02-006).
- Pair a prose rule with an executable check (clippy deny, `panic_hunt`, `xtask layers`,
  `panel-commands`). Rules with no check (licence allowlist, rule 15, claim-before-coding) are the ones
  practice diverges from (§4, E02-016).
- Spell out concurrency etiquette for agents sharing one checkout: per-agent `CARGO_TARGET_DIR`, file
  ownership, new modules instead of shared-file growth, atomic manifest writes, "wait and retry, don't fix
  their files" (E02-003).
- Make session hand-off explicit: a terse devlog entry plus an always-green tree, justified by "context
  limits" (E02-004). The project keeps this log out of git, which hides it from collaborators; a fork chose
  in-tree instead.
- Give agents a ranked, machine-readable work queue, and have them update its evidence when they move a
  number (E02-007).
- Plan in agent-hours, and label what a human must do (E02-008).
- Write a short, closed stop-and-ask list plus an anti-stall rule ("do not ask for it and do not stop") so
  autonomous agents neither over-escalate nor take irreversible actions (E02-009, E02-010).
- Share rules across sibling repos as hash-verified blocks sourced from one public repo, and check them in
  CI. A private shared-rules repo failed for outside contributors (E02-012, E02-013).
- Close the loop from bot review to the rules: CodeRabbit findings led to precise rule wording (E02-015).
- Decide the attribution policy explicitly. Here the "no agent attribution in PRs" rule coexists with a
  product feature that credits models from commit trailers (E02-011, E02-017).
