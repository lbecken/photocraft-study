# 01c — Errata and reconciliations

Corrections found while synthesizing; where an evidence file and this list disagree, this list wins.

| # | Item | Correct reading | Found by |
|---|---|---|---|
| 1 | `Claude-Session:` trailer count | 274 commits on main (238 non-merge); 62 distinct sessions on main, 129 across all refs. The figure 304 in E08 does not reproduce. | D03 recount |
| 2 | Manual "(merge queue)" commits | 7 on main, 9 across all refs (E07 says nine without the distinction). | D03, D07 recounts |
| 3 | E07-013 parity "discrepancy" | Two same-day commits (#182, #186), not drift over time. | D07 |
| 4 | Attribution of the "625/625" parity commit and the "decorative settings" fixes | They carry `Claude Opus 4.8` trailers. | D07 |
| 5 | E02-016 | Concerns house rule 15 specifically; the general "rules without checks diverge" point is E02 §4. | D10 |
| 6 | `claude/fix-*` vs `claude/integ-batch-*` | Fix branches did not pass through the integ batches; the batches were CI-only PRs of community work (Oct 8–9). | E09, E06 |
| 7 | `Finding:` trailers | Belong to October `security(...)` PRs, not the November `fix/sec-*` branches. | E09 |
| 8 | AI-attribution share figures | Differences across E02/E03/E05/E07/E08 are denominator differences (non-merge vs first-parent vs date window); reconciled in `07-failures-productivity.md` §B.6. | D07 |
| 9 | Unresolved shas | `0cc421d0d5`, `0cc0d0212c7a` (E05, self-flagged unverified) and `d3e8039f76` (E07 line 56) do not exist in the pinned clone — treat the rows that cite them as unverified. `dde09ea31e` is a commit of the external `storytold/craft-contrib` repo. | citation verifier |
| 10 | Ledger truncation | Three "no such path" hits in `01-evidence-ledger.md` are citations cut at the 220-character column limit, not bad citations. | citation verifier |
