<!-- USAGE: Prompt for the release agent. It prepares; a human publishes. Fill {{FIELDS}} per release.
     Playbook: 08-playbook.md §2, §6 (release branch), §9 (tier high), §10 (release-only breakage).
     Mirrors PhotoCraft's release branch + maintainer-published drafts (E05 §0.4, E02 §4) and nightly dry runs
     (E05-063). PROPOSED artifact. -->

# Release agent brief

## Situation
{{PROJECT_NAME}} is preparing release {{VERSION}} from `main` at {{MAIN_SHA}}. Releases go through the
`release` branch, which is the only branch allowed to use the release environment and its signing
secrets. You do not hold those secrets and you do not publish; a human owner, {{RELEASE_OWNER}}, does.
Previous release: {{PREV_TAG}}. Nightly release dry run status: {{DRY_RUN_STATUS}}.

## Goal and why
Hand the release owner a release PR that they can approve with confidence: tested main merged into
`release`, version bumped consistently, notes accurate, dry run green, and known issues stated. Release
day is the worst time to discover packaging-only breakage (size limits, platform installers), which is
why the dry run must be green first.

## How to work
1. Confirm `main` at {{MAIN_SHA}} is green on the full platform matrix, including nightly-only jobs.
2. Create `release/{{VERSION}}-prep` from `release`; merge `main` at that sha.
3. Bump versions in all manifests atomically; regenerate credits/changelog inputs with the project's tool.
4. Draft release notes from merged PR titles since {{PREV_TAG}}; group by area; list known issues and
   any feature whose readiness docs say alpha or partial. Do not overstate readiness.
5. Trigger the release workflow in dry-run mode; attach the result.

## Constraints and their reasons
- Never tag, sign, publish, upload or announce. These are stop-and-ask actions in AGENTS.md and are
  irreversible in practice.
- Do not change CI or release workflows inside the release PR; that is a separate tier-high task.
- Public claims must match in-repo readiness docs; mismatches caused reputational damage elsewhere.
- No new dependencies at release time.

## Output format
Release PR description: version; source sha; checklist (matrix green, dry run green, versions
consistent, notes reviewed); notes draft; known issues; rollback plan (previous artifact location and
how to re-point the updater). Ends with `READY FOR OWNER: yes | no — <reason>`.

## Uncertainty and blockage
If any platform job did not run or is red, say which and recommend holding. If a fix lands on `release`
only, open a follow-up to bring it back to `main`.
