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
| 11 | Perf budget counts ("0 of 88" vs "0 of 102") | Both describe `perf/budgets.toml` at the pin: 102 rows = 14 `[[bench]]` + 88 `[[scenario]]`; zero have `enforce = true` (57 explicit `enforce = false`). Use "0 of 102 rows (88 scenarios + 14 benches)". | D06; orchestrator recount (`git show 74330157c:perf/budgets.toml \| grep -c`) |
| 12 | E04-030 "`perf --quick` runs in CI" | It runs only on manual dispatch / nightly, never on PRs. | D06 |
| 13 | FreeBSD-delegation commit | Correct sha is `0cc161e2a8` (replaces the unverified `0cc421d0d5` in E05). | D06 |
| 14 | "Required checks gate merges" (E05) | Unresolved: E06/E09 samples show merges with 2 of 5 and 4 of 7 checks passed; skipped jobs may be counted as not passed. Do not state that checks are required for merge. | D06 |
| 15 | Untagged version bumps | 0.11.0, 0.15.0 and 0.20.0 were bumped but never tagged, each followed by a same-day platform fix; that the release builds failed is INFERRED (no failed run observed). | D06 |
