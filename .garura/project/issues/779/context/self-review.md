# Self-review: #779 and #953 (one change, plan 717)

Branch: plan/717/779-plan-lookup-and-safe-delete. Compared with plan/717/base (the PR base).
Rules: the standard self-review rules (path in resolved-rules.json). This is a checklist for
the reader of the PR. It is not the approve or reject step.

Findings that stop the raise: none.

## Scope checks

- Matches the issue: pass. The change does what the approved design says, in both parts.
  - #779: the plan lookup reads plan files from git (latest origin/main, plus the plan's own
    branch when that is on origin). It never reads the checkout. A failed fetch reads the last
    fetched copies and records fetched:false. The start-change ICE got C9, F9 and the new S7,
    and the compiled play was rebuilt from it (its fingerprint matches the ICE file).
  - #953: a stale local plan branch is deleted only when origin was reached and every commit
    is on main or was on origin's plan branch; otherwise the run stops and names the commits.
    Pushes are checked. The "on main" wording for run records is fixed in the merge-change
    ICE and compiled play. The review labels are out of the test names. The fn-673 page now
    states ADR 060's rule.
- No scope creep: pass. Nothing for #951 is in the diff. The plan 717 file changes only the
  two Done marks for #779 and #953.
- The fn-673 model page went one step past the design. The design named the title, line 4 and
  the Goal. The Fails if and Checked by lines changed too, because they stated the same old
  rule (a plan lands on main only when done). Noted, kept, and not a stop: leaving them would
  have left the page contradicting itself.
- Reasonable size: pass. About 460 lines of real change in 13 files (two scripts, each kept as
  one copy in create-play/references and one in start-change/scripts, byte for byte the same;
  three test files; two plays' ICE and compiled text; one model page; one plan file). The
  rest is the run records in the issue's folder.
- No stray artifacts: pass. The run records under the issue's context folder are the normal
  chore(stm) commits of this pipeline. The only untracked file is resolved-rules.json, which is
  this review's own input and is not part of the change.

## Quality checks

- Tests present: pass. All three test files were run from the create-play/references folder.
  - test_resolve_plan.py: 18 passed, 0 failed (includes an old checkout whose main copy holds
    the issue, an issue only on the plan branch's copy, no network, and no origin/main).
  - test_setup_branch.py: 12 passed, 0 failed (includes the unpushed-work stop, the
    pushed-before-deleted fresh cut, and the failed origin lookup that deletes nothing).
  - test_merge_plan.py: 10 passed, 0 failed.
- Commits are clean: pass with one note. Every commit is conventional and names #779 or #953.
  Note: commit cd780a32 reads "say run records land on main". It means the run records land
  on the branch the change landed on (main, or the plan's branch). The files say it right. The
  history is not rewritten; this note is the record.
- No secrets: pass. The diff holds plan text, scripts, tests and run records. No keys, tokens
  or passwords. No absolute home paths in the changed plays, scripts or the design file.
- Docs in step: pass. The start-change description, the ICE and the compiled play agree, the
  merge-change ICE and compiled play agree, and the plan file and model page match the work.
- Nothing obviously broken: pass. The component linter reports 36 errors and 1 warning for the
  whole components folder. None is in start-change, merge-change or the changed scripts; they
  are in files this change does not touch (for example create-play/SKILL.md). Not caused here.

## Pre-merge reminders (from the design, not for this review to do)

- Reinstall from this branch before the merge. Promote memory only if a memory file changed
  (none did).
- Out of scope and untouched: #951.
