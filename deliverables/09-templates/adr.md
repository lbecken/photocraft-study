<!-- USAGE: Copy to docs/adr/NNNN-<slug>.md for every tier-high decision (contracts, persistence, dependencies,
     CI, security, licensing). Number sequentially; never delete — supersede instead. PhotoCraft's decision log
     (docs/decisions.md) had 2 dated prose entries, no status field, and one entry disappeared (E02 §5); this
     template adds the missing fields. Playbook: 08-playbook.md §9, §11. PROPOSED artifact. -->

# ADR {{NNNN}}: {{TITLE}}

| Field | Value |
|---|---|
| Status | {{proposed / accepted / superseded by ADR-XXXX / rejected}} |
| Date | {{YYYY-MM-DD}} |
| Deciders (human) | {{HANDLES}} |
| Drafted by | {{agent role + session id, or person}} |
| Related | issue #{{N}}, PR #{{N}}, spec `specs/{{issue}}.md` |
| Risk tier | high |

## Context
{{The forces at play: what problem, which constraints (performance, platform, licence, user data),
what evidence (benchmarks with hardware and method, incident links). Keep facts separate from opinion.}}

## Options considered
| Option | Pros | Cons | Evidence |
|---|---|---|---|
| A: {{…}} | | | |
| B: {{…}} | | | |
| C: do nothing | | | |

## Decision
{{The chosen option in one or two sentences, stated as a rule agents can follow, e.g. "All document
writes go through `atomic_write`; a flush failure fails the save except on {{list}}".}}

## Consequences
- Positive: {{…}}
- Negative / accepted risks: {{…}}
- Contracts affected: {{command ids, schemas, layer table, file formats}}
- Mechanical enforcement added: {{lint / xtask check / test name}}, or "rule only, because …"
  <!-- prefer a check: rules without checks diverge, E02-016 -->

## Verification
- How we will know it works: {{tests, corpus, metric and threshold}}
- Environments covered: {{e.g. local NTFS, SMB share, read-only dir}} <!-- E07-021 -->

## Rollback
{{How to revert safely; data-migration implications; who decides.}}

## Supersession log
- {{date}}: {{change, link to new ADR}}
