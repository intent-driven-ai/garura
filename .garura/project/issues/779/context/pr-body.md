## What this changes

Closes #779, closes #953.

Two items under #731 (start-change cuts a plan's branch, and each issue's branch from it), fixed together under plan 717.

- **#779 (start-change reads plan files from the checked-out branch).** The plan lookup now reads the plan files from git, never from the checkout. It fetches, reads each plan file at the latest main, and, when the plan's own branch is on GitHub, reads that branch's copy too: a plan session (/update-plan) writes there first, so an issue in either copy belongs to the plan. If the fetch fails, it reads the last fetched copies and the record says so. start-change's rule C9 and failure F9 changed and a new scenario S7 was added, through edit-play.
- **#953 (the findings left by round 2 of the PR #950 review).**
  1. A plan branch that is gone on GitHub but still here is deleted only when GitHub was reached and every commit on it is on main, or was on GitHub's plan branch. Otherwise start-change stops, keeps the copy and names the commits that would be lost. A failed push now stops the run.
  2. start-change's one-line description now says an issue in a plan gets a branch under its plan's branch.
  3. merge-change's rules and play now say the run records are committed on the branch the change landed on (main, or the plan's branch), not always "on main".
  4. Four test names no longer carry review labels.
  5. The #673 product-model page (merge-change lands an issue on its plan branch) now states ADR 060's rule: a plan's branch lands on main whenever the plan pauses and its review approves it. The design named the title, the description line and the Goal; the "Fails if" and "Checked by" lines stated the same old rule, so they changed too.

Note: commit cd780a32's message reads "say run records land on main". It means the opposite: the change makes the records land on the branch the change landed on. The files say it correctly; history is not rewritten.

Out of scope: #951 (the five small findings of round 1 of the same review) stays its own chore.

## Self-review

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
