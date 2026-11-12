# Verification record

Date 2026-11-12. Upstream pin `74330157cb601573ae4523a95bb9132822fc3918` (clone HEAD = pin, no drift).
This file records how the evidence (`evidence/E00`–`E09`) and deliverables (`02`–`10`, `09-templates/`) were checked,
what was corrected, and what is still weak.

## 1. Independent reviews

Three subagents each reviewed deliverables they had not written. They checked claims against the clone and `data/E03_*.csv`,
not against other deliverables. Each review's log is kept unedited.

| Review | Scope | Checked | Corrected / issues |
|---|---|---|---|
| `REVIEW-08-09-10.md` | playbook, templates, IDE transfer | 124 `[PC-VERIFIED/PARTIAL]` tags in 08; 74 PROPOSED items; 131 evidence-bearing lines in 10; 46 template comments | 27 tags corrected; 39 issues across 08/09/10 |
| `REVIEW-02-03-05.md` | chronology, architecture/process, role maps | ≈355 claims (≈150 shas resolved in 02) | 44 corrected |
| `REVIEW-04-06-07.md` | case studies, testing/CI/release, failures/productivity | ≈355 claims (≈125 shas in 04, 76 in 06, ≈45 in 07) | 51 issues |

Each review listed evidence-file errors it left unfixed. This close-out rechecked every candidate in the clone or CSVs,
applied all errata to the evidence (old values kept as "previously stated …", marked `(corrected 2026-11-12, see errata #N)`),
regenerated the ledger, and swept the deliverables for statements that contradict the errata.

## 2. Errata

- `01c-errata.md` now holds **40** errata (#1–#24 existing, #25–#40 new). Two existing rows were sharpened: #7 (`Finding:`
  trailers: 25 of the 27 on main are direct pushes, not PRs) and #16 (24 `Codex`-identity commits on main in total).
- Not added (see "Unconfirmed candidates"): the #13414 branch-name candidate, refuted (`refs/pull/13414/head` =
  `origin/switch-photocraft-psd`), and the E05-035 required-checks candidate, which duplicates #14.
- Applied to evidence: 62 edit sites in E01–E09. 30 are marked "corrected", 11 are "cross-ref" lines for reconciliations
  (#2, #4, #11, #15–#20, #24, #28, #31, #35), and the rest are inline errata references in table cells.
- Not applied to evidence, because the evidence was already right and the error was in deliverables: #5, #6, #7, #8.
  #10 was fixed in code (below).
- Consistency sweep: 14 deliverable statements fixed. Fork share 97 % → ≈96 % (06, 07); release-branch tags (06, 07, 08);
  #13414 branch name, time zone of the 10-22 security burst ×2, 2 h 08 m note and an errata pointer (04); never-crash
  "12 in 15 min" (03); date-window reconciliation and "failing checks" caveat (05); the 07 A.1 tally (next item).
- The 07 A.1 tally was recounted from the table's own last column: **9 with at least one mechanical correction
  (5 of them partial), 4 advisory/process only, 3 none**. This replaces the unreproducible "7 / 5 / 4".

## 3. Generated files

- `scripts/build_ledger.py` now truncates long cells at the last whitespace before the limit (220 chars for sources).
  A `sha:path` token is therefore never cut. The three false "no such path" hits in `01-evidence-ledger.md` are gone.
- `python3 scripts/build_ledger.py` runs cleanly and rebuilds `01-evidence-ledger.md`, `01b-uncertainty-register.md` and
  `evidence/DIGEST.md`. The ledger has **294 entries** (unchanged; no entry was added or removed, and titles were edited only
  in E09-C-004).

## 4. Citation verifier (final)

`python3 scripts/verify_citations.py <clone> evidence deliverables` → **2,108 citations checked, 23 unresolved** (this file included), all expected:
- 8 hits: the house-rules source commit of the external `storytold/craft-contrib` repo, each marked "external repo".
- 15 hits: the three non-existent shas of errata #9 (two wrong FreeBSD-delegation shas, corrected to `0cc161e2a8`
  by #13, and one reverted original that is not in the clone), cited only to say they do not exist. They appear in
  E05, E07, the generated 01b/DIGEST, 01c, 06 and the review logs.
- 0 unresolved in `01-evidence-ledger.md` (previously 3).

Evidence-ID check: all **252** distinct IDs cited in 02–08, 10, `09-templates/` and 01c
(`grep -ohE '\bE0[0-9](-[A-Z])?-[0-9]{3}[a-z]?\b'`) exist in the regenerated ledger.

## 5. Known residual weaknesses

- **Review and approval evidence is thin.** It rests on about 22 hand-picked PR pages, read only as WebFetch model summaries
  (4 explicit human approvals). Branch protection and required-check settings are invisible, so whether checks gate merges
  stays unresolved (errata #14).
- **WebFetch-only figures were not rechecked:** CodeRabbit round counts, "14 of 16", "19 checks", "27 of 29",
  SonarQube 95.8 %, the #10426 commit gap.
- **The playbook's PROPOSED thresholds are untested design choices.** These are the 30/60-min red-main response, 24 h claim
  timeout, 8/12 cycle caps, 70 % context, p75 token budgets and freeze rules. Each answers a cited failure; none has effect data.
- **Private artefacts are invisible.** `plan/`, `log/devlog.md`, prompts, orchestration tooling, agent counts at any
  moment, token or dollar cost, and human supervision time are not public. Absence of a trailer is "unknown", not human.
- **Press and third-party pages were partly blocked (403).** Third-party claims stay "source X claims Y".
- **Dates are not normalised everywhere.** Evidence mixes author (local) and committer UTC dates (errata #19). Only the
  chronology is consistently committer-UTC; the other deliverables convert only the dates that were found wrong.
- **Classification and causal claims stay INFERRED.** Examples: "11 of 21 red-main incidents are merge skew", "attribution
  fell through contributor mix", "every platform-removing economy caused a later red". These rest on small samples.
- **Method-dependent counts:** `#[test]` totals (18,014 / 18,024 / 18,111 by regex), landing-kind splits (03 B.6), and 598 vs
  599 merge PRs (errata #35) are each stated with their method, but they do not agree with one another.
- **The reviews were spot checks in places:** 07 B.7 rows 6–9 and 11–12, and E04-derived architecture counts (crate counts,
  ~805 commands), were not rechecked one by one.
- **Errata #16 is not fully traced.** 1 of the 24 `Codex`-identity commits (`9fdcbf93c2`) fits neither landing path.
