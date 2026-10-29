## Summary

Plan 717 (people plan work toward a business intent) lands on main again while it pauses. Its branch carries one landed change:

- **PR #984** — #983: `/list-plans` shows each plan as a card — its direction (⏵ next, ⏵⏵ next in line, ⏵⏵⏵ later), number and business intent; its Status, Branch and Waits on; then each epic with its Progress. Each plan's Status and Direction are fields a person sets in the plan file, never worked out. All seven plans are Paused; #717 ⏵, #788 ⏵⏵. Reviewed by check-change (harness verdict approve, no blocking finding) and merged into `plan/717/base`.

After this merges: the plan-view template is promoted to Phoenix memory and the harness is reinstalled from main, back to back — the installed plan tool does not read the new template until it is replaced.

Open follow-ups (not in this change): the ontology's Plan kind gains the plan statuses and Direction through `/edit-ontology`; `/shape-plan`'s step file still says a plan's status is `active`; three lines of `/list-plans`' intent still name only "status".

Refs #717 — the plan stays open.

## Self-review

# Self-review: plan 717 branch lands on main after #983 (issue 717)

Rules file: the base `self-review.md` (resolved, no project override; record in `.garura/project/issues/717/context/resolved-rules.json`).
Diff: `main...HEAD`, branch `plan/717/base`. This review informs the reviewer; it is not the approve/reject gate. The rules file sets no blocking mark, so a finding here is marked REVIEW (the reviewer looks) and the Blocking issues section lists anything the reviewer must settle first.
This file replaces the earlier one written for the first raise of this branch.

## Change summary

- Landed change: PR #984, `plan/717/983-list-view-cards` into `plan/717/base` (#983, `/list-plans` shows each plan as a card: direction, status, branch, waits on, and each epic with its progress). It was reviewed on its own by the harness and approved (0 blocking findings; 1 P2, 4 P3, 5 P4). Verdict and findings: `.garura/project/issues/983/review/` (`decision.yaml`, `findings.yaml`).
- Fix commit: `f2ff5fbb` gives every plan a status (Not Started, In Progress, Paused, Done, Dropped) and a direction set by the product owner, and sets the seven plan files to match.
- Plan file update on this branch: `e1324108` pauses plan 717 on main again after #983 and `399b94df` marks #983 Done.
- The rest of the 13 commits are run records (`chore(stm)`) under `.garura/project/issues/983/`.
- Size: 66 files. 16 are hand-written (7 plan files, the plan tool and its tests, the `/list-plans` play, the plan-view template, 2 `shape-plan` script files, one README). 50 are run records and copied memory files. Hand-written part: about 194 lines added and 84 removed under `core/`.

## Scope checks

- PASS: Matches the issue. Every change under `core/` and the plan files serves #983 (the card view, the plan status and direction). Evidence: file list of `git diff --name-only main...HEAD`; the two `shape-plan` script edits only make a new plan file start with the new status (`Not Started`) and an empty direction, which the card view needs.
- REVIEW: No scope creep. The seven plan files change status from `active` to `Paused` on the product owner's word (comment in each file, 2026-10-29). That is a plan-state decision riding with the code change; the reviewer should confirm it is wanted in this landing. Plan 734 also had its status comment moved to its own line.
- PASS: Reasonable size. The hand-written part is small; the bulk is run records, which this repo commits on purpose.
- PASS: No stray artifacts. No debug prints, no scratch files, no commented-out blocks in added source lines. One `print(` hit is a test card title, not a debug print.

## Quality checks

- PASS: Tests present. `core/tools/plan/test_plan.py` grew by 55 lines. Run now: 17 tests, OK (`python3 -m unittest test_plan`). `write_plan_file` self-test: 9 passed, 0 failed. `check_list.py` was updated for the card output.
- PASS: Commits are clean. Conventional format throughout, each cites #983 or #717. Two `feat(plans)` commits for the code, the rest `chore(stm)` or `chore(plan)`.
- PASS: No secrets. Scanned added lines for GitHub tokens, `sk-` keys, AWS keys and private-key headers: none. No home-folder path or person's name in added lines (#982).
- REVIEW: Docs in step. The README of the plan tool and the template were updated, but the review of #983 found three places that were not (all still open on this branch):
  - The product ontology says a plan's status is "active, done or dropped" and has no direction; the plan tool now rejects `active` (finding M-1, P2). `core/components/plays/shape-plan/SKILL.md` line 339 still says `status: active`, while the script beside it now writes `Not Started`.
  - The template index row for `plan-view.md` still describes the old content (M-2, P3), and the template does not define "Paused" or the five plan statuses (M-3, P3).
  - The `/list-plans` ICE still names only the old unknown-status failure; the new unknown plan status or direction has no failure, scenario or recovery row (H-1, P3), and its Context line still lists only the six node statuses (H-2, P4).
- REVIEW: Nothing obviously broken. No leftover TODOs in the change. The component linter reports 36 errors and 1 warning on this branch (`.garura/project/issues/983/review/lint-components.json`), the same counts the #983 review recorded; they are older errors, not new ones from this change. The compiled `list-plans/SKILL.md` carries "changed by edit-play (#983, the cards)" in its provenance text; the harness rule says no edit notes in skill files, so confirm the compiler writes that text by rule (H-3, P4).

## Blocking issues

None that stop the raise. For the reviewer to settle first:

- M-1 (P2): the ontology and the `shape-plan` play text still say a plan's status is `active`, but the plan tool rejects it. Decide whether the ontology change (`/edit-ontology`) and the `shape-plan` text go in a named follow-up before this lands.

## Notes

- Working tree: `.garura/project/issues/717/context/resolved-rules.json` shows modified (only the missing newline at the end of the file). Nothing else is uncommitted.
- The #983 PR body and self-review said `resolved-rules.json` was untracked; it is tracked (finding Q37, P3). Not repeated here.
