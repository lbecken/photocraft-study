# E00 — Source identity & access (2026-11-12)

### E00-001 — Upstream repository identity
- Label: VERIFIED
- Source: `git clone https://github.com/storytold/photocraft.git`; `git remote -v`; `git rev-parse HEAD`
- Data: origin = `https://github.com/storytold/photocraft.git`; `main` HEAD = `74330157cb601573ae4523a95bb9132822fc3918` ("Use craft-psd for PSD/PSB format code (#13414)", 2026-11-12). Full (non-shallow) clone.

### E00-002 — History extent
- Label: VERIFIED
- Method: `git log --oneline | wc -l`; `git rev-list --all --count`; `git log --reverse | head`
- Data: 12,396 commits reachable from `main`; 13,473 across all branch refs. First commit `386b0566d` "init repo" 2026-09-30 02:12 -0400; second `16941f719` "one-shot" 2026-09-30 05:02 -0400 (241 files, 42,241 insertions, includes `AGENTS.md`, `docs/architecture.md`). 4,067 merge commits; 3,475 first-parent commits on main.

### E00-003 — Refs available
- Label: VERIFIED
- Method: `git branch -a`; `git tag`; `git ls-remote origin 'refs/pull/*/head' | wc -l`
- Data: ~370 remote branches (namespaces incl. `claude/*`, `codex/*`, `community/*`, `fix/*`, `feat/*`, `pr/never-crash-*`, `sonar*/`, `jobs/*`, `land/*`); 27 tags `v0.1.0`…`v0.23.1`; 6,480 `refs/pull/*/head` refs (fetched locally).

### E00-004 — Access limits
- Label: VERIFIED
- Data: From the research sandbox, `curl` to github.com / api.github.com returns 403 (proxy policy); GitHub MCP tools are scoped to the research repo only. PR/issue pages are readable through the WebFetch tool, which returns model-summarized content with short quotes (tested on PR #13414: merged, CodeRabbit review + SonarQube Cloud quality-gate comment present). Issue/PR discussion evidence is therefore lower-fidelity than git evidence. Discord and private channels are not accessible.

### E00-005 — Commit attribution trailers exist at scale
- Label: VERIFIED
- Method: `git log --format='%(trailers:key=Co-authored-by,valueonly)' | sed 's/<.*//' | sort | uniq -c | sort -rn`
- Data (main, top): Claude Opus 5.5 3,565; Brandon Thomas 679; Claude Opus 5.5 (1M context) 652; Claude Sonnet 5.5 181; Claude Fable 5.1 167; Claude 54; Claude Haiku 5.5 49; Claude Opus 4.8 45; GPT-6 40; Cursor 38; Claude Fable 5.2 32; Codex 12. Other trailer keys: `Claude-Session:` 203, `Copilot-Session:` 43, `Model-Effort:` 27. Detailed breakdown in E03.
