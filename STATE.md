# Project state

_Last updated: 2026-11-12 (end of session 01)_

## Phase
**Phase 2 — synthesis: 6 of 10 deliverables done; 4 deferred (02, 04, 05, 06) for budget.** Phase 1 evidence complete.

## Plan
1. Phase 0 — verify source, scaffold repo ✅
2. Phase 1 — parallel evidence streams E01–E09 → `evidence/`
3. Phase 2 — synthesize deliverables 01–10 → `deliverables/`
4. Phase 3 — citation verification (`scripts/verify_citations.py`), gap-filling, uncertainty register
5. Phase 4 — final review, handoff

## Stream status
| Stream | Status |
|---|---|
| E00 source identity | done |
| E01 genesis | done |
| E02 agent instructions | done (opus, complete file) |
| E03 git quant | done |
| E04 architecture | done |
| E05 test/CI/release | done (opus, complete file) |
| E06 workflow & roles | done |
| E07 failures | done |
| E08 external | done |
| E09 case traces | done |

## Deliverable status
| # | Deliverable | Status |
|---|---|---|
| 01 | Evidence ledger + uncertainty register | done (generated) + errata |
| 02 | Development chronology | deferred — evidence in E01/E02/E05/E07 |
| 03 | Architecture & process reconstruction | done |
| 04 | Feature case studies | deferred — evidence in E09 |
| 05 | AI agent & human role maps | deferred — evidence in E06 |
| 06 | Testing/CI/release analysis | deferred — evidence in E05 |
| 07 | Failure & productivity analysis | done |
| 08 | AI Software Engineering Playbook | done |
| 09 | Prompts & templates | done (16 files) |
| 10 | IDE transferability assessment | done |

## Backlog / next steps
1. Write deferred deliverables 02, 04, 05, 06 (prompts in `handoffs/2026-11-12-session-01.md`; one subagent each, read `deliverables/SYNTHESIS-BRIEF.md`).
2. Orchestrator review pass of 03/07/08/10 for cross-deliverable consistency (they were written in parallel; 10 refers to 08 by topic only). Apply `deliverables/01c-errata.md` back into the evidence files (E05, E07, E08).
3. Playbook 08: human review, approval tiers, role separation, token budgets and orchestration are PROPOSED (no PhotoCraft evidence) — consider validating them against a second case study.
4. Deepen thin evidence: PR-page sample is small (~27 PRs, WebFetch summaries); batch-8 revert reasons (PR #9386); tool behind `Finding:` trailers; Reddit and several press pages were blocked.
5. Re-pin and diff if upstream has moved past `74330157c`.

## Notes
- 2026-11-12: Opus weekly quota exhausted mid-run (resets 2026-11-14 16:00 UTC); remaining streams re-launched on Sonnet. Sonnet-produced evidence (E03 write-up, E04, E06–E09) should get an Opus/Fable spot-check of citations in Phase 3.

## Blockers
- None. (Push to origin works since 2026-11-12 19:00 UTC.)
- Model quotas have interrupted subagents twice (Opus weekly, then Opus 5-hour limit). Interrupted agents can be resumed with SendMessage; if not, relaunch from the prompts in `handoffs/`.
