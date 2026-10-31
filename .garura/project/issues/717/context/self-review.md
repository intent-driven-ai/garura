# Self-review: plan 717 branch lands on main (issue 717)

Rules file: the base `self-review.md` (resolved, no project override; recorded in `.garura/project/issues/717/context/resolved-rules.json`).
Diff: `origin/main...HEAD`, branch `plan/717/base` into `main`. This review informs the reviewer; it is not the approve/reject gate. A finding is marked REVIEW (the reviewer looks); the last section lists what, if anything, must be settled before the raise.
This file replaces the earlier one written for the previous landing of this branch (#986). The PR body must say "Refs #717", never "Closes": business intent #717 stays open.

## Change summary

- Plan 717 is Done. `.garura/project/plans/717.yaml` reads `status: Done`. Its tree has 35 nodes: 31 Done, 4 Dropped, none open. The epic #956 is Done.
- This landing carries 251 commits, 937 files, about 1.02 million added lines. Almost all of it is run records. Where the files sit:
  - `.garura/project/issues/`: 749 files, about 1.0 million added lines. Run records and copied memory files. The 720 folder alone is 898k lines, because its review runs keep five full copies of the PR diff (`review/pr.diff` and `review/run-1` to `run-5`).
  - `core/`: 159 files, about 12.9k lines. The hand-written part: `update-plan` (27 files), `create-play` (13), `shape-plan` (11), `start-change` (10), `shape-slice` (10), memory standards (10), `show-plan` (7), `merge-change` (6), `track-plan-changes` (5), a few skills, `core/tools/plan` and `lint-components`.
  - `docs/`: 10 files (ADRs 026, 049, 058, 060 to 064, the ADR index, the harness standard).
  - `.garura/product/product-os/`: 16 model pages and the spine. `.garura/project/plans/717.yaml`: 1 file. `.garura/user-provided/managing-work.md`: 1 file. `.garura/install-manifest.json`: 1 file.
  - `.claude/`: 0 files. Installed copies are not in this diff.
- Stories landed in this round (10 pull requests into `plan/717/base`): #995 (#993, change named lines on any model page), #998 (#720, `/update-plan`), #1003 (#896, `/shape-plan` stops when a plan exists), #1006 (#1005, `/show-plan` shows finished children), #1008 (#1007, status follows its own issue), #1009 (#1001, one session folder and the model in `/update-plan`), #1010 (#779, plan lookup and safe delete), #1012 (#1011, the #721 page states ADR 060's landing rule), #1013 (#1000, `/show-plan` with no number), #1016 (#989, start a plan's work on its own).
- Earlier in the same plan, already on main from earlier landings: #732, #733, #980, #984, #987.

## Scope checks

- PASS: Matches the issue. Every story of plan 717 landed on `plan/717/base` through its own reviewed pull request. `gh pr list --base plan/717/base --state merged` lists 15 pull requests. 5 (#732, #733, #980, #984, #987) are already on main from earlier landings. The other 10 each have a merge commit on this branch (10 `Merge pull request` commits on the first-parent line), and each of their issue folders holds a harness `decision.yaml` that reads `decision: approve` (issues 993, 720, 896, 1005, 1007, 1001, 779, 1011, 1000, 989).
- PASS: Commits that came in without a pull request are the expected kind only. The 25 first-parent commits that are not pull-request merges are: `chore(stm)` run records (12), `chore(plan)` plan-file upkeep (11), `chore(install)` (1, the harness reinstall record for #1005), and one `Merge remote-tracking branch 'origin/main' into plan/717/base` (`de258784`, brings main into the plan branch before PR #995; clean). No code or feature commit was made straight on the plan branch. `origin/main` is an ancestor of HEAD, so there is no conflict with main.
- PASS: No scope creep. Hand-written paths map to the plan's stories (plan tools, the plan plays, the model pages and ADRs the stories wrote). Two `revert` commits (`56442848` for #991, `c3e15154` for #951) take back work that was taken out of this plan, so their net effect is nothing.
- REVIEW: Reasonable size. The raw size is far past one sitting (937 files). The hand-written part is about 13k lines in 159 `core/` files plus 10 docs and 16 model pages, and each part was reviewed in its own pull request. The reviewer should read by pull request, not this diff. Big run-record copies of PR diffs under `.garura/project/issues/720/review/` (about 890k lines) are generated output that the repo commits on purpose.
- PASS: No stray artifacts in product files. Added lines under `core/` and `docs/` carry no TODO, FIXME or debug print except the `console.log` of a test reporter line inside a run-record diff copy. No scratch files outside `.garura/project/issues/`.

## Quality checks

- PASS: Tests present. Behavior changes carry tests: `core/tools/plan` (3 test files), `update-plan` (2), `start-change`, `merge-change`, `show-plan` (2), and more under `shape-plan`, `shape-slice` and `install-garura`. Run now: `core/tools/plan` 46 tests OK; `update-plan` 10 and 56 OK; `start-change` 12 OK; `merge-change` 3 OK; `show-plan` 2 and 5 OK.
- PASS: Nothing obviously broken by this branch. `lint-components` from the repo root reports 36 errors and 1 warning, all in 11 files this branch does not change (`create-loop`, `create-play`, `edit-loop`, `edit-play`, `install-garura`, `uninstall-garura`, `check-quality`, `find-matching-issues`, `merge-pr`, `open-pr`, `propose-kb-node`). None is new from this plan. (I could not run the linter on main in a clean copy, so "not new" rests on the branch touching none of those files.)
- PASS: Commits are clean. Every non-merge commit uses a conventional prefix and cites an issue number. No commit message says "Closes", "Fixes" or "Resolves" #717. No `Co-Authored-By` or "generated with" line in any commit message.
- PASS: No secrets. A scan of every changed file that exists for GitHub tokens, `sk-` keys, AWS keys, Slack tokens and private-key headers finds none. No environment file, certificate or key file is in the diff.
- PASS: Nothing from a client or private notes. The employer's name appears once, in `.garura/project/issues/993/review/quality-findings.yaml`, inside the list of patterns that check searched for and did not find. No client name, vault path or personal-notes content in the diff.
- REVIEW: Docs in step. ADRs 060 to 064, the model pages, the plan README (`core/tools/plan/README.md`) and `managing-work.md` moved with the work. The pull-request reviews carry their own findings for each story (`.garura/project/issues/<n>/review/findings.yaml`); open items were left on those pull requests, not fixed here.
- FIXED: A person's home-folder path was in 4 committed run-record files, on a public repository. The commit "chore(stm): take personal and client references out of the run records of #989, #993 and #1011 (#717)" took it out, and the uncommitted `resolved-rules.json` now reads the `~` form. Checked on HEAD with `git grep -i -I -l` for each of five strings (the owner's user name, the dashed home-folder prefix, the scratch-folder prefix, the employer's name, the personal-vault name): 0 files for each. A diff of `~/cto/` paths shows no file on the branch that main lacks (the same 4 files hold such paths on both).

## What must be settled first

Blocking findings: none.

Notes:

- The older commits on this branch still carry those strings in their history, so the landing on main should not carry those commits (a decision for the product owner at merge time).
- The PR body must read "Refs #717". It must not close business intent #717.
