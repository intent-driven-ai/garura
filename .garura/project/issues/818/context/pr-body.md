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

## For the product owner's eye

- The code-host adapter cannot set an issue type, edit a body, or take off a label or a sub-issue. Those 4 jobs run as fixed GitHub commands in `write_work_items.py`. They are tested only against a fake tracker. The first real run (`/shape-plan 788`) is their first test on GitHub.
- On a story it reuses, the play also sets type Story and takes off any label, so the tracker check passes on hand-made stories.
- Still to do as its own change: the ontology's "labelled work-item" lines for Epic and Story, with `/edit-ontology`.
