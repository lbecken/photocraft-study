# Project state

_Last updated: 2026-11-12 (session 01)_

## Phase
**Phase 1 — evidence gathering** (in progress)

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
| E03 git quant | data+scripts done; write-up running (sonnet) |
| E04 architecture | re-running (sonnet) |
| E05 test/CI/release | done (opus, complete file) |
| E06 workflow & roles | re-running (sonnet) |
| E07 failures | re-running (sonnet) |
| E08 external | re-running (sonnet) |
| E09 case traces | re-running (sonnet) |

## Deliverable status
| # | Deliverable | Status |
|---|---|---|
| 01 | Evidence ledger + uncertainty register | pending |
| 02 | Development chronology | pending |
| 03 | Architecture & process reconstruction | pending |
| 04 | Feature case studies | pending |
| 05 | AI agent & human role maps | pending |
| 06 | Testing/CI/release analysis | pending |
| 07 | Failure & productivity analysis | pending |
| 08 | AI Software Engineering Playbook | pending |
| 09 | Prompts & templates | pending |
| 10 | IDE transferability assessment | pending |

## Backlog / next steps
- See newest file in `handoffs/`.

## Notes
- 2026-11-12: Opus weekly quota exhausted mid-run (resets 2026-11-14 16:00 UTC); remaining streams re-launched on Sonnet. Sonnet-produced evidence (E03 write-up, E04, E06–E09) should get an Opus/Fable spot-check of citations in Phase 3.

## Blockers
- **Push to `origin` fails (HTTP 403: Claude GitHub App lacks access to `lbecken/photocraft-study`).**
  Commits are local only until the owner installs/re-links the GitHub App. Retry `git push -u origin claude/magical-hypatia-jwtvty` each session.
