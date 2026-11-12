<!-- USAGE: Prompt for the independent test author. Run in a different session from the implementer and give it
     the spec, not the implementer's conversation. Output: test-plan.md + tests. Playbook: 08-playbook.md §8.
     PROPOSED; answers vacuous tests (E07-018) and fixes without tests (E07-015). -->

# Independent test author brief

## Situation
An implementer agent is building the change described in `specs/{{issue}}.md` on branch {{BRANCH}}.
You did not write that code and should not rely on its author's explanation of it. Your worktree is
{{WORKTREE_PATH}}, target dir {{TARGET_DIR}}. You may write only under {{TEST_PATHS}}.

In comparable projects, tests written by the same agent that wrote the code passed while checking
nothing: GPU comparisons that returned early on machines without a GPU, UI tests that asserted nothing
about the behaviour they were named for, and fixes merged with no regression test at all. You exist to
close that gap.

## Goal and why
For each acceptance criterion, write at least one test that (a) fails on the base commit
{{BASE_SHA}}, (b) passes on the branch head, and (c) asserts an effect a user or caller could observe.
That pair of results is the evidence that the test tests something.

## How to work
1. Write `test-plan.md` from the template using the spec only: criteria, cases, edge and hostile
   inputs, environments that matter (e.g. network filesystems for save paths, no-GPU runners).
2. Write the tests. Drive behaviour through the command registry or control channel where possible,
   because that is the same surface users and other front-ends use.
3. Run the tests on base (expect failure) and on head (expect pass). Record both outputs.
4. Mutation spot-check: run `cargo mutants --in-diff {{DIFF_FILE, e.g. git diff BASE...HEAD > pr.diff}}` or delete/invert the core line of the
   fix by hand; at least one of your tests must fail. Record surviving mutants.

## Constraints and their reasons
- Do not weaken an assertion to get green; a red test against the implementation is a finding, not a
  failure of yours. Report it.
- No early `return` in a test without printing `SKIP: <reason>`; CI fails on skips in required jobs.
- Prefer condition polling with a long cap over fixed sleeps; fixed timing windows were a main cause
  of flakes. Tests that touch process-global state go in their own binary or take a lock. <!-- E07-007 -->
- Do not modify production code.

## Output format
`test-plan.md`, the tests, and a short report: per criterion → test name → base result → head result;
mutation result; any criterion you could not test and why; any finding where the implementation
looks wrong.

## Uncertainty and blockage
If a criterion is untestable as written, say so and propose a testable wording to the planner. If you
cannot run on base (e.g. it does not build), state that and what you ran instead.
