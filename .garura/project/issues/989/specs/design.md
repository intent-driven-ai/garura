# Design — #989 and #991: start a plan's work, and land a plan's branch on main

Approved by the product owner on 2026-10-31, after two rounds in one session. Plan 717,
capability #721 (start and land work against a plan). One change: branch
`plan/717/989-plan-branch-start-and-propose`, under `plan/717/base`.

Grounded in: the #720 design (`.garura/project/issues/720/specs/design.md`, "Which copy of a plan
counts"), ADR 060 (a plan's branch merges into main when the plan pauses), ADR 061 (a plan's
branch is cut by the play that starts the plan's work, main first, through one shared script).
No new ADR: 060 and 061 already decide the cut and the landing.

## #989 — start-change starts a plan on its own, and stays open for any change

start-change is not locked to a plan. Starting a plan is one more thing it can start, on top of
what it does today.

- **Whatever is typed works as today.** An issue number, or a short description of the change (a
  bug fix, a chore, a story, a feature, anything). A description goes back to GitHub, finds the
  matching issue (or files one), confirms it, and starts: branch, working folder, as today.
- **Nothing typed does nothing.** With no number, no description and no `plan <id>`, it stops with
  one line: "Tell me what to start: an issue number, a short description, or plan <id>." It never
  reads the change from the branch name. (Today, on `plan/717/base` with nothing typed, the
  pre-flight took 717 — the business intent — as the change; this design removes that lock.)
  Picking up earlier work still works by typing that issue's number.
- **Starting a plan: `/start-change plan <id>`** — only with the word `plan`. A bare number
  always means an issue, as today.
  - The plan is read from main (from git, never the checkout).
  - The plan has no branch: main's plan file is set to In Progress with `branch: plan/<id>/base`,
    committed and pushed on main; `plan/<id>/base` is cut from that commit and pushed. It stops:
    no issue is looked up, no story branch is cut, nothing is committed on the plan's branch (it
    equals main's tip). The run's notes go in a working folder that is not committed.
  - The plan's branch exists: it switches to it and changes nothing.
  - The plan is Done or Dropped, or no plan has that number: it stops with a plain message.
- **A story in a plan with no branch** also cuts the plan's branch main first, through the same
  shared script, then cuts the story's branch from it. (Today that path cuts the plan's branch
  without touching main's plan file.)
- **The stale-copy rule moves into the shared script.** start-change's rule (#953) — a local copy
  of a plan branch that is gone on origin is deleted and cut fresh only when every commit on it is
  on main; else it stops and names the commits — moves into the plan tool's branch script, so
  /update-plan gets it too. Today the shared script would switch to such a copy.

## #991 — /propose-change asks Status and Direction; the branch's plan file replaces main's

- When `/propose-change` raises a plan's own branch (`plan/<id>/base`) for main, it first asks, in
  one message, before any push: the plan's **Status** (Not Started, In Progress, Paused, Done,
  Dropped) and its **Direction** (1 next, 2 next in line, 3 later, or none). An answer it does not
  know is asked again. The gate switch never skips this question.
- Status and Direction are plain text a person sets; nothing is worked out from them, and no status
  changes what a play does. Whatever the Status, the branch field is set empty: merge-change
  deletes the branch after the merge, and the next start cuts a fresh one from main.
- In the commit it already makes before raising, it writes the answers into the branch's plan
  file, merges the latest main into the plan's branch keeping the branch's plan file whole, and
  names in the pull request's review section every change main made to that plan file since the
  branch was cut. The branch's version replaces main's.
- `/merge-change`, before it merges a plan's branch, checks that main's plan file has not changed
  since the raise. If it has, it stops and says to run `/propose-change` again. A blended plan
  file never lands. After the merge, main's plan file equals the branch's.
- `/check-change` does not change.

## Build

Three plays change what they promise, each through its ICE and `/edit-play`:

- start-change — Intent, C2, C9, C6 (no resume from the branch name), a new constraint for plan
  mode and for "nothing typed", new failure conditions, S3 and S5 measures, new scenarios (start a
  plan; start it again; a number no plan has; nothing typed; a description on a plan's branch).
- propose-change — a new constraint (ask Status and Direction for `kind: plan`, never gated), a new
  failure condition, S6 extended.
- merge-change — a pre-merge check on a plan's file; a new failure condition and scenario.

The plan tool (`core/tools/plan/`): the stale-copy rule in `plan_branch.py`, and one new script that
readies a plan's file for landing (writes Status, Direction, empty branch; brings main in keeping
the plan file; records the differences), each with tests.

The work-management guide (`.garura/user-provided/managing-work.md`), section "A plan's branch:
start, pause, start again", may need a line on `/start-change plan <id>`. That file is the product
owner's: the line is named to him, not written.
