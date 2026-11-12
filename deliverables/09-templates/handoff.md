<!-- USAGE: Every agent session writes one before ending (and refreshes it at each green checkpoint), saved as
     handoffs/YYYY-MM-DD-<session>.md and committed with the work. Mirrors PhotoCraft's devlog + green-tree hand-off
     (AGENTS.md:168, E02-004) but kept in-repo and public, since PhotoCraft's log is gitignored. Playbook: 08-playbook.md §11. -->

# Handoff: {{DATE}} — {{ROLE}} — session {{SESSION_ID}}

| Field | Value |
|---|---|
| Task | #{{ISSUE}} / `specs/{{issue}}.md` |
| Branch / worktree | {{BRANCH}} / {{PATH}} |
| Head sha | {{SHA}} |
| Tree state | {{builds + gate green / builds, gate red: <which step> / does not build: <why>}} |
| Session ended because | {{done / stop condition: … / context limit / blocked / budget}} |
| Tokens used (if known) | {{N}} · cycles used {{N}}/{{max}} |

## 1. What changed
| Commit | Summary |
|---|---|
| {{sha}} | {{…}} |

## 2. What ran (exact commands and results)
```
{{cargo xtask ci → summary line}}
{{focused test commands → pass/fail counts}}
```

## 3. What did not run, and why
- {{e.g. Windows job — no runner locally; relying on merge queue}}

## 4. Claims
- Held: {{issue #N — keep / release}}
- Released: {{…}} (comment posted on issue: yes/no)

## 5. Open questions / blockers
- {{question}} → needs {{OWNER / planner / reviewer}}
- Stop-and-ask item hit: {{none / which}}

## 6. Decisions made (and whether an ADR is needed)
- {{decision}} — ADR: {{yes, draft at docs/adr/NNNN / no, because …}}

## 7. Next concrete step
{{One or two sentences a fresh session can act on without re-reading this conversation.}}

## 8. Hygiene
- [ ] Files touched outside ownership: {{none / list + reason}}
- [ ] `STATE.md` updated
- [ ] Target dir {{TARGET_DIR}} deleted (if task finished)
- [ ] Nothing secret or personal in this note
