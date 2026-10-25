The plan play, `/shape-plan`, is built: the second play of the shaping loop (ADR 049). For a business intent that `/shape-slice` has served with a slice, it makes the intent's one plan, or brings it up to date. The plan is the plan file, one epic for each slice and one story for each feature. Each story is written from its feature's ICE and its capability's ICE, and holds no failure or recovery condition. A second run makes no copies.

Closes #818.

## What changes

- **The play** `core/components/plays/shape-plan/`: compiled with `/create-play` from its ICE (`reference/ice.md`, C1–C13, F1–F11, S1–S7, D1–D5). It is position both: start-change at the head, the end sequence before the close. It has one pinned checkpoint: the person sees every tracker write and the plan-file change before typing yes, and nothing reaches the tracker before that.
- **9 new scripts**, each with its test:
  - `gather_plan.py` reads the slices that serve the intent, runs the ready check, and writes clean ICE copies with every "Fails if" line removed.
  - `find_work_items.py` finds the work items marked with `represents`, and never matches by title.
  - `check_drafts.py` checks the drafts.
  - `render_brief.py` builds the brief.
  - `record_approval.py` records the person's answer.
  - `write_work_items.py` writes to the tracker only after yes.
  - `write_plan_file.py` writes the plan file line by line, so other nodes and comments stay.
  - `check_plan.py` and `check_tracker.py` are the close checks.
  - 7 scripts are copied unchanged from create-play.
- **The new skill** `author-work-items`: it writes the epic's title and each story's scope of work and Context guidance from the clean ICE copies.
- **product-os-keeper** names the play and the skill.
- **The next-command map**: /shape-slice now points to /shape-plan. /shape-plan points to nothing yet, because the eval play (#798) is not built.
- **managing-work.md**: an Epic is filed with issue type **Feature**. The organization has no Epic type. The kind keeps its name, Epic.

## The product owner's decisions

`.garura/project/issues/818/context/decisions.md`:
- Q-find-1: items are found by `represents` marks. Plan 788's #794, #795, #818 and #798 are marked on main.
- Q-found-1: a found story gets only its missing sections, and the person's lines are kept.
- Q-label-1 and decision 5: issue type Feature for an epic and Story for a story, with no label.
- Q-change-1: a feature that leaves the slice has its story moved out of the plan, not deleted.

## Checks

| Check | Result |
|---|---|
| Hidden acceptance checks (16), written before the build and kept from the builder | 16 / 16 pass (15 failed before) |
| Tests beside the scripts | 10 files, 118 checks pass |
| lint_play on shape-plan and shape-slice | PASS, 0 gaps |
| Fingerprint | matches `reference/ice.md` |
| Component lint | no error in a new or touched file |

## Round 2 — the review's P2 and P3 findings fixed (decision 6)

- **DF-1:** each new issue is made in one GitHub call with its type and its parent. The run's record is saved after every tracker write. A record from a run that failed part way still gives the plan file its marks, so the next run reuses what the first run made. A test makes the third write fail.
- **DF-2:** a "Fails if" line with lines under it is removed in full from the clean copy, and the draft check compares every line of the block.
- **DF-3:** the skill reads only `skill-input.json` and the clean copies, and no ICE page path. "Written from" is filled by the tracker writer.
- **DF-4:** the shared code-host adapter gains five verbs (`create-issue-typed`, `set-issue-type`, `edit-issue-body`, `remove-label`, `remove-sub-issue`). On GitLab they stop with a plain message. All 6 copies are identical, and the play's scripts run no raw `gh`. The adapter skill page lists 21 verbs.
- **DF-5:** the yes records the sha256 of the brief, the work list and the drafts. A change after the yes is refused, and nothing is written.

| Round 2 check | Result |
|---|---|
| Hidden acceptance checks (21; 5 new) | 21 / 21 pass |
| Tests beside shape-plan and shape-slice, and the adapter's tests | all pass |
| lint_play (source map) / fingerprint / component lint | PASS / matches / no new error |

DF-6, the ontology's "labelled work-item" lines, gets its own `/edit-ontology` change next. The P4 findings go to one parked chore.

## For the product owner's eye

- The new adapter verbs are tested with a fake runner. The first real run (`/shape-plan 788`) is their first test on GitHub.
- On a story it reuses, the play also sets type Story and takes off any label, so the tracker check passes on hand-made stories.
- Still to do as its own change: the ontology's "labelled work-item" lines for Epic and Story, with `/edit-ontology`.
