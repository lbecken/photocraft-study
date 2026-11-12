<!-- USAGE: Copy to docs/risk-tiers.md and adjust the path lists to your workspace; mirror the high-tier paths
     in CODEOWNERS and branch protection so the table is enforced, not only stated. Planner and triage agents
     assign tiers from this file. Playbook: 08-playbook.md §9. PROPOSED; PhotoCraft documents no approval tiers (E02 §6). -->

# Risk tiers and approvals

Rule: when a change fits more than one tier, the highest applies. When unsure, choose higher and say why.

## Tier table
| Tier | Change kinds | Paths (fill in) | Required evidence | Approvers | Merge path |
|---|---|---|---|---|---|
| **Low** | docs, comments, new tests only, non-structural i18n strings, typo fixes | `docs/**` (except adr, risk-tiers), `**/tests/**` (new files), `i18n/*.{{ext}}` | gate green; new tests fail when target code is broken | reviewer agent | merge queue |
| **Medium** | feature or fix inside one owned module/crate; new command in a new module; UI change dispatching existing commands | `{{crates/<feature>/**}}`, `{{crates/ui/src/<area>/**}}` | gate green; independent tests fail on base; mutation spot-check; screenshot/JSON evidence | reviewer agent + human maintainer review record | merge queue or integration batch |
| **High** | shared contracts (command schema, stable ids, layer table, shared structs); persistence / save path / file formats; CI and workflows; dependencies and `Cargo.lock`; licences, assets, fonts; security boundaries (control-channel auth, plugin sandbox, untrusted-input parsers); release | `{{crates/commands/src/registry.rs}}`, `xtask/src/layers.rs`, `{{crates/io/src/save*.rs}}`, `.github/**`, `Cargo.toml`, `Cargo.lock`, `deny.toml`, `{{crates/control/**}}`, `release/**` | all medium evidence + ADR + rollback plan; fault-injection for persistence; `cargo deny` for deps; second reviewer agent with attacker stance | human owner (+ second human for security and release) | merged alone, never batched |

## Why these lines (evidence)
- Contracts high: two individually green PRs changing and consuming one struct broke the build on main
  (E07-003, 351149f0df).
- Persistence high: a correct durability fix regressed network-filesystem saves for users (E07-021).
- CI high: "Do not change CI in a feature or fix pull request" (PhotoCraft house rule 11, E02 §2.1).
- Dependencies/licences high: PhotoCraft's licence allowlist is stated but not machine-checked (E02 §4).
- Approval records: label-only or "No reviews" merges were common in sampled PRs (E06-041).

## Stop-and-ask (any tier)
Licences outside the allowlist · publishing · releases/tags/signing · new remotes · secrets/personal
data · spending money · destructive git · lowering a FLOOR or growing a shrink-only allowlist · disabling
or skipping tests · changing stable ids/schemas/layer table · save-path or format changes · files outside
ownership · anything hard to undo. <!-- first eight from PhotoCraft house rule 9, E02 §2.1 -->

## Budgets per tier (calibrate after two weeks)
| Tier | Implementer sessions | Max edit–test cycles/session | Review sessions | On overrun |
|---|---|---|---|---|
| Low | 1 | 8 | 1 | escalate at 2× |
| Medium | ≤ 2 | 8 | 1 reviewer + 1 test author | re-spec or split |
| High | ≤ 3 after spec | 12 | 2 reviewers + test author | owner decides |

## Enforcement checklist
- [ ] CODEOWNERS lists high-tier paths → owner handles.
- [ ] Branch protection: required reviews per CODEOWNERS; merge queue required; no direct pushes.
- [ ] PR label `tier: <x>` set by triage; CI fails if diff touches high-tier paths but label is lower.
