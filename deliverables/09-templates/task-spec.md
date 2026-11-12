<!-- USAGE: Copy to specs/<issue>.md. The planner fills it; a maintainer (medium) or the owner (high) approves it
     before anyone claims the task. Implementer and test author both work from this file only.
     Playbook: 08-playbook.md §3 (spec, claim), §4.2, §5, §9. PROPOSED artifact. -->

# Spec: {{TITLE}} (#{{ISSUE}})

| Field | Value |
|---|---|
| Issue | #{{ISSUE}} |
| Author (planner session) | {{SESSION_ID}} |
| Risk tier | {{low / medium / high}} — reason: {{WHY}} |
| Spec approved by | {{HUMAN or "n/a (low)"}} on {{DATE}} |
| Claimed by | {{ROLE SESSION BRANCH}} <!-- claim also posted on the issue; E02 §2.1 rule 2 --> |
| Related ADRs / PRs | {{LIST}} |
| Duplicates checked | {{search terms used; results}} |

## 1. Problem
{{What the user or caller observes today, with a reproduction: command id + JSON, or UI steps.}}

## 2. Desired behaviour
{{What they observe after the change. Describe behaviour, not wiring: "pressing Ctrl+S in a dirty
editor writes the file and clears the dirty marker", not "add a Save menu item".}}
<!-- answers surface-without-behaviour, E07-013 / E07-017 -->

## 3. Acceptance criteria (each must be testable)
| # | Criterion | How verified (test name / control-channel check) |
|---|---|---|
| AC1 | {{…}} | {{…}} |
| AC2 | {{…}} | {{…}} |
| AC3 | Hostile input to any new command returns an error, never panics | command fuzzer covers new ids |

## 4. Scope and ownership
- Files owned (create/modify): {{LIST}}
- New module(s): {{e.g. crates/commands/src/<area>_cmds.rs with specs()}} <!-- E06-050 -->
- Shared lines expected to change: {{e.g. one line in registry.rs}} or "none"
- Out of scope: {{LIST}}

## 5. Contract changes
- Command ids added: {{id → params schema → result schema}}
- Stable ids / schemas / layer table / shared structs changed: {{none, or: STOP — split into a contract task}}
- File-format or persistence changes: {{none, or describe; tier high}}

## 6. Test plan sketch
- Unit: {{…}}
- Integration via command registry / control channel: {{…}}
- Environments that matter: {{e.g. Windows paths, network FS, no-GPU runner}}
- Corpus / FLOOR affected: {{name, current value}}

## 7. Evidence expected in the PR
- [ ] `cargo xtask ci` summary
- [ ] each AC → test, failing on base, passing on head
- [ ] screenshot / JSON for user-visible behaviour
- [ ] "Not run:" list

## 8. Budget
- Sessions: {{N}}; max edit–test cycles: {{N}}; escalate to {{OWNER}} on overrun.

## 9. Open questions
- {{UNVERIFIED: …}}
