<!-- USAGE: Write one for every red-main incident, escaped regression, data-loss report or vacuous-test discovery,
     saved as docs/incidents/YYYY-MM-DD-<slug>.md. Blameless; the required output is a mechanical check or an
     explicit reason why only a rule is possible. Playbook: 08-playbook.md §10, §13. PROPOSED; classes from E07 §9. -->

# Incident: {{TITLE}}

| Field | Value |
|---|---|
| Date detected / resolved | {{YYYY-MM-DD HH:MM UTC}} / {{…}} |
| Detection signal | {{main CI run #, issue #, review comment, mutation run}} |
| Severity | {{red main / user-facing regression / data loss / vacuous test / other}} |
| Time to fix (TTF) | {{minutes}} — from breaking merge to green main |
| Red-main minutes | {{N}} |
| Responders | {{roles/sessions/handles}} |

## 1. What happened
{{Two to five sentences, facts only, with shas and PR numbers.}}

## 2. Failure class (pick one or more)
- [ ] F1 semantic merge skew (each PR green, union red)
- [ ] F2 duplicate parallel work
- [ ] F3 surface without behaviour
- [ ] F4 vacuous test
- [ ] F5 fix merged without regression test
- [ ] F6 crash on hostile input
- [ ] F7 shared-process-state flake
- [ ] F8 platform-only breakage not run on PR
- [ ] F9 generated artefact stale
- [ ] F10 merge-conflict casualty
- [ ] F11 fix regressed an untested environment
- [ ] F12 gate tightening caused post-merge red
- [ ] F13 doc drift
- [ ] other: {{…}}
<!-- taxonomy from E07 §9 -->

## 3. Timeline (UTC)
| Time | Event |
|---|---|
| {{…}} | breaking change merged ({{PR}}) |
| {{…}} | detected |
| {{…}} | fix merged ({{PR}}) |

## 4. Why existing checks missed it
{{Which gate step should have caught it and why it did not: not run on PR, cancelled run, skipped
test, no test for this environment, check is advisory only, etc.}}

## 5. Immediate fix
{{PR, what changed. Revert considered? Why/why not.}}

## 6. Permanent fix (required)
| Type | Description | Owner | Due | PR |
|---|---|---|---|---|
| Mechanical check / ratchet / test | {{…}} | | | |
| Rule only (justify why no check is possible) | {{…}} | | | |
<!-- prefer mechanical: stated-only rules are where practice diverged, E02 §4 -->

## 7. Metric impact
- Added to metrics: red-main minutes {{N}}; escaped regression {{yes/no}}; vacuous-test finding {{yes/no}}.

## 8. Follow-ups
- {{issue #}}
