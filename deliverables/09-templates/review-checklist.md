<!-- USAGE: The reviewer agent (and any human reviewer) fills this in the PR as a review comment. Every box is
     answered yes / no / n/a with a note; any "no" in sections B–D blocks approval. Playbook: 08-playbook.md §8, §9.
     PROPOSED; items marked with evidence IDs mirror PhotoCraft rules or answer its observed failures. -->

# Review: PR #{{PR}} — {{TITLE}}

| Field | Value |
|---|---|
| Spec | `specs/{{issue}}.md` |
| Tier | {{low / medium / high}} |
| Reviewer | {{role + session id / handle}} |
| Implementer session | {{id}} (must differ from reviewer) |
| Test-author session | {{id}} (must differ from implementer) |

## A. Spec and scope
- [ ] Every acceptance criterion maps to a test or control-channel check.
- [ ] Only files listed as owned were changed (plus declared shared lines). <!-- E06-050 -->
- [ ] No contract change hidden in the diff (schema, stable id, layer table, shared struct, file format).
- [ ] No CI, dependency or `Cargo.lock` change unless this is that tier-high task. <!-- E02 §2.1 rule 11 -->
- [ ] No hand-edited generated files; no shared status-line edits. <!-- E07-020 -->

## B. Correctness
- [ ] Identifiers exist as used; description is true. <!-- E02 §2.1 rule 5 -->
- [ ] Behaviour observed (CLI JSON / screenshot), not only test output. <!-- E04-024 -->
- [ ] No `unwrap`/`expect`/`panic!`/`unsafe` in non-test code; errors returned for bad params.
- [ ] Platform-specific behaviour considered (paths, line endings, GPU absence).
- [ ] Persistence changes: failure modes tested (fsync failure, network FS, permissions). <!-- E07-021 -->

## C. Tests actually test
- [ ] Each new test fails on base / with the fix reverted (record how). <!-- E07-015 -->
- [ ] Mutation spot-check run; surviving mutants: {{list or none}}. <!-- E07-018 -->
- [ ] Every test asserts an observable effect; no assert-free or `is_ok()`-only tests.
- [ ] No early `return` without `SKIP:`; no ignored/disabled tests added.
- [ ] No fixed sleeps or frame windows; shared process state isolated. <!-- E07-007 -->
- [ ] FLOORs and shrink-only allowlists unchanged or tightened.

## D. Evidence and provenance
- [ ] `cargo xtask ci` result present and current for head sha.
- [ ] "Not run:" list present and acceptable. <!-- E02 §2.1 rule 7 -->
- [ ] Commit trailers: `Co-Authored-By`, `Agent-Session`, `Agent-Role`.
- [ ] Issue linked (`Fixes #N`); duplicates checked.

## E. Bot findings
| Bot | Finding | Confirmed? | Action |
|---|---|---|---|
| {{…}} | | | |

## Verdict
`VERDICT: {{approve | request-changes | escalate-to-owner}}`
Blocking findings (file:line — what — why — how verified):
1. {{…}}
Non-blocking notes:
- {{…}}
Unverified (could not run): {{…}}
Tier high: human owner approval still required — {{OWNER}}.
