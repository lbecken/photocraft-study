# Synthesis brief for deliverable authors

You are writing one of ten research deliverables. Read this fully first, then
`evidence/RESEARCH-BRIEF.md` (the evidence rules still apply), then the evidence
files your task names — **in full**, not just their summaries.

## What the research is for
The reader wants to learn **how PhotoCraft (storytold/photocraft) was built and is
maintained with AI agents**, so they can reproduce the useful methods on their own
project (ultimately: an IntelliJ-like desktop IDE in Rust). They are an experienced
engineer. They will act on what you write, so precision beats polish and an honest
"unknown" beats a plausible guess.

## Source hierarchy
1. `evidence/E00…E09-*.md` and `data/E03_*.csv` in `/home/user/photocraft-study` —
   your primary input. Cite evidence IDs (`E05-021`) **and** carry through the
   underlying primary citation (sha, `sha:path:line`, PR number, URL) for every
   important claim, so each deliverable stands alone.
2. The upstream clone (read-only; path in `evidence/RESEARCH-BRIEF.md`) — use it to
   check, deepen or fill gaps. Any new fact you add must be cited the same way and
   listed in a final "New evidence gathered during synthesis" section.
3. Nothing else. No recollection, no general knowledge about the project.

## Labelling (mandatory, per claim or per table row)
- **VERIFIED** — observed in a primary source and cited.
- **INFERRED** — reasoned from verified evidence; give the chain in one clause.
- **PROPOSED** — our recommendation; never present it as a PhotoCraft practice.
Also distinguish, wherever it matters: *documented rule* vs *observed pattern in
history* vs *self-reported by developers (unverified)* vs *third-party claim*.

Hard limits: never infer AI usage from architecture or style; a commit without an
AI trailer is "attribution unknown", not "human". Never invent dates, metrics, model
names or agent counts. Names/handles only — no email addresses. Where evidence files
disagree with each other, say so and resolve it by checking the upstream clone.

## Writing
- Lead each section with the finding, then the evidence. Tables for anything
  enumerable. Short verbatim quotes (≤3 lines) for the passages that carry weight.
- Define project-specific terms on first use (e.g. "integration batch", "scorecard",
  "house rules", "panic_hunt"). The reader has not read the evidence files.
- State numbers with their unit, denominator and date range.
- No filler, no restating the task, no generic AI-engineering advice that is not
  tied to evidence (except in sections explicitly marked PROPOSED).
- End every deliverable with: `## Confidence and gaps` (what is weakest, what was
  not checkable, what would change the conclusion) and, if applicable,
  `## New evidence gathered during synthesis`.

## Mechanics
- Write only the file(s) assigned to you under `/home/user/photocraft-study/deliverables/`.
  Do not run mutating git commands in the research repo; the orchestrator commits.
- Before finishing, run
  `python3 /home/user/photocraft-study/scripts/verify_citations.py <upstream-clone> <your-file>`
  and fix or explicitly flag every unresolved citation (commits of *other* repos,
  e.g. craft-contrib, are expected to be unresolved — mark them "(external repo)").
- Final reply to the orchestrator: ≤200 words — what you wrote, the 5 most important
  conclusions, and anything in the evidence you found wrong or contradictory.
