# photocraft-study

Forensic research into **how** the public PhotoCraft project
(<https://github.com/storytold/photocraft>) is developed and maintained —
with emphasis on AI-agent methods and workflows, not just product architecture.

This repository holds research outputs only. Nothing here is pushed upstream.

## Layout

| Path | Purpose |
|---|---|
| `STATE.md` | Live project state, backlog, next steps (read first when resuming) |
| `CLAUDE.md` | Operating rules for any Claude Code session working here |
| `handoffs/` | Per-session handoff notes |
| `evidence/` | Raw evidence notes, one per research stream (`Exx-*.md`) |
| `data/` | Machine-generated tables (CSV/TSV) backing quantitative claims |
| `scripts/` | Reproducible extraction / verification scripts |
| `deliverables/` | The ten synthesized research products |

## Evidence labels

- **VERIFIED** — directly observed in a primary source (commit, file at a commit, PR page, developer-authored statement) and cited.
- **INFERRED** — reasoned from verified evidence; the reasoning chain is stated.
- **PROPOSED** — our own recommendation; not a PhotoCraft practice.

AI usage is never inferred from architecture alone — only from explicit
attribution (commit trailers, author identities, branch names, documents,
developer statements).

## Upstream snapshot

Pinned at `storytold/photocraft` `main` = `74330157cb601573ae4523a95bb9132822fc3918`
(2026-11-12). See `evidence/E00-source-identity.md`.
