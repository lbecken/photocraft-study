<!-- USAGE: Index of the templates that implement deliverables/08-playbook.md. Copy the files you need into your
     project (paths suggested below), replace every {{FIELD}}, and keep the evidence-ID comments or delete them.
     All templates are PROPOSED artifacts; comments with Exx IDs mark elements that mirror verified PhotoCraft practice. -->

# 09 — Templates for the AI Software Engineering Playbook

These files turn `deliverables/08-playbook.md` into things you can drop into a repository on day 0.
None of them is copied from PhotoCraft: PhotoCraft has no PR/issue templates, CODEOWNERS, role prompts
or ADR format on any ref examined (E02-020, E02 §6). Where an element mirrors something PhotoCraft
demonstrably does, an HTML comment names the evidence ID.

## Index

| File | Use it for | Copy to | Playbook section |
|---|---|---|---|
| `AGENTS.template.md` | Repo instruction file: orientation, workspace map, golden rules, picking work, definition of done with gate commands, parallel-agent rules, stop-and-ask, session-end checklist | `AGENTS.md` (+ one-line `CLAUDE.md` pointing to it) | §1, §4, §7, §9.3, §11 |
| `prompt-planner.md` | Brief for the planner / spec author | agent prompt library | §2, §3 (spec), §5 |
| `prompt-implementer.md` | Brief for an implementer in its own worktree | agent prompt library | §2, §6, §7 |
| `prompt-test-author.md` | Brief for the independent test author (different session) | agent prompt library | §2, §8 |
| `prompt-reviewer.md` | Brief for the verifier/reviewer (optional attacker stance) | agent prompt library | §2, §8, §9 |
| `prompt-integrator.md` | Brief for integration batches / merge queue | agent prompt library | §4.6, §6, §10 |
| `prompt-release.md` | Brief for the release-preparation agent (human publishes) | agent prompt library | §2, §6, §9, §10 |
| `prompt-triage.md` | Brief for issue/PR triage, duplicate detection, claim timeouts | agent prompt library | §2, §3, §4.4 |
| `task-spec.md` | Spec that implementer and test author both work from | `specs/<issue>.md` | §3, §4.2, §5, §9 |
| `adr.md` | Decision record for tier-high changes | `docs/adr/NNNN-<slug>.md` | §9, §11 |
| `review-checklist.md` | Review record; any "no" in B–D blocks | PR review comment | §8, §9 |
| `test-plan.md` | Independent test plan with base/head results and mutation check | `specs/<issue>.test-plan.md` | §8 |
| `handoff.md` | Session-end note; refreshed at each green checkpoint | `handoffs/YYYY-MM-DD-<session>.md` | §11 |
| `incident-postmortem.md` | Red main, escaped regression, data loss, vacuous test | `docs/incidents/YYYY-MM-DD-<slug>.md` | §10, §13 |
| `risk-tiers.md` | Tier table, stop-and-ask list, budgets, enforcement checklist | `docs/risk-tiers.md` + CODEOWNERS | §9, §12 |

## How the pieces fit (one task)

1. Triage (`prompt-triage.md`) labels the issue and sets a provisional tier from `risk-tiers.md`.
2. Planner (`prompt-planner.md`) writes `task-spec.md`; a maintainer approves it for medium, the owner for high.
3. Implementer (`prompt-implementer.md`) claims, works the loop, opens a draft PR, writes `handoff.md`.
4. Test author (`prompt-test-author.md`, separate session; tier medium/high) writes `test-plan.md` and tests that fail on base.
5. Reviewer (`prompt-reviewer.md`) fills `review-checklist.md`; human approves per tier.
6. Integrator (`prompt-integrator.md`) lands via merge queue or batch; incidents go to `incident-postmortem.md`.
7. Release agent (`prompt-release.md`) prepares; human publishes. Tier-high decisions get an `adr.md`.

## Adoption order
Day 0: `AGENTS.template.md`, `risk-tiers.md`, `handoff.md`, `task-spec.md`.
Week 1: role prompts, `review-checklist.md`, `test-plan.md`.
Month 1: `adr.md` in routine use, `incident-postmortem.md` feeding the metrics review (playbook §13–§14).

## Fill-in conventions
- `{{FIELD}}` = replace; `{{a / b}}` = choose one.
- Keep evidence comments (`<!-- E07-018 -->`) if you want to trace why a line exists; they do not render.
- Model names, budgets and agent counts are yours to set; PhotoCraft publishes none that can be reused
  (playbook §0, §12).
