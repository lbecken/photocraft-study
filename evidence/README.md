# Evidence notes

One file per research stream. Each entry:

```
### Exx-NNN — short claim
- Label: VERIFIED | INFERRED
- Source: <sha>:<path>[:line] | commit <sha> (date) | PR #N | URL (accessed date)
- Quote/Data: short verbatim excerpt or command output
- Method: command or procedure used (if quantitative)
- Notes: caveats, confidence, cross-refs
```

Every file ends with `## Open questions / uncertainties` and `## Leads for other streams`.

| ID | Stream | File |
|---|---|---|
| E00 | Source identity & access | E00-source-identity.md |
| E01 | Genesis & first week | E01-genesis.md |
| E02 | Agent-instruction docs history (AGENTS.md etc.) | E02-agent-instructions.md |
| E03 | Quantitative git forensics | E03-git-quant.md |
| E04 | Architecture & agent-facing interfaces | E04-architecture.md |
| E05 | Testing, CI, quality gates, release | E05-test-ci-release.md |
| E06 | Branch/PR/integration workflow & roles | E06-workflow-roles.md |
| E07 | Failures, corrections, campaigns | E07-failures.md |
| E08 | External sources & developer statements | E08-external.md |
| E09 | Feature case-study traces | E09-case-traces.md |
