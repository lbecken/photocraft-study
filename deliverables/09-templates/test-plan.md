<!-- USAGE: The independent test author fills this from the spec before writing tests, and completes the result
     columns after running on base and head. Commit it next to the spec (specs/<issue>.test-plan.md).
     Playbook: 08-playbook.md §8. PROPOSED; answers vacuous tests (E07-018) and untested fixes (E07-015). -->

# Test plan: {{TITLE}} (#{{ISSUE}})

| Field | Value |
|---|---|
| Spec | `specs/{{issue}}.md` |
| Test author session | {{id}} (≠ implementer session {{id}}) |
| Base sha / head sha | {{BASE}} / {{HEAD}} |

## 1. Cases per acceptance criterion
| AC | Test name | Level (unit / command / control-channel / corpus) | Observable effect asserted | Base result (expect FAIL) | Head result (expect PASS) |
|---|---|---|---|---|---|
| AC1 | {{…}} | {{…}} | {{…}} | | |
| AC2 | {{…}} | | | | |

## 2. Edge and hostile inputs
| Input class | Example | Expected |
|---|---|---|
| Empty / zero / negative | {{…}} | error, no panic |
| Huge / overflow | {{…}} | bounded work, error |
| Malformed JSON params | {{…}} | error, no panic |
| Unicode / RTL / paths with spaces | {{…}} | {{…}} |
| Concurrent use | {{…}} | {{…}} |

## 3. Environments
| Environment | Why it matters | Covered by |
|---|---|---|
| Windows paths/quoting | platform-only breaks surfaced on main before <!-- E07 F8 --> | {{job}} |
| No GPU / software adapter | tests skipped silently before <!-- E07-018 --> | fail-on-skip job |
| Network FS / read-only / fsync failure | durability fix regressed SMB <!-- E07-021 --> | fault injection |
| `cargo test` (shared process) vs nextest | nextest isolation hid a race <!-- E07-008 --> | nightly |

## 4. Mutation spot-check
- Tool / method: {{cargo mutants --in-diff … | manual revert of line X}}
- Mutants killed / survived: {{N / N}}; survivors: {{list with reason}}

## 5. Flake hygiene
- [ ] No fixed sleeps; condition polling with cap {{N s}}.
- [ ] Process-global state isolated (own binary / lock / test group). <!-- E07-007 -->
- [ ] Ran {{N}} times locally: {{failures}}/{{N}}.

## 6. Corpus / floors
- Affected corpus: {{name}}; FLOOR before {{x}} → after {{y}} (never lower).

## 7. Not tested and why
- {{…}}
