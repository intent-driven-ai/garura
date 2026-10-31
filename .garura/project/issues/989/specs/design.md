# Design — #989: start a plan's work on its own, and keep start-change open for any change

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

## #991 — dropped from this change (2026-10-31)

After the first review the product owner took #991 out: "Proposing a change is simple: the work is
finished. The commit is done, so propose, review, merge … I don't want this complication."
propose-change and merge-change stay as they were, and the landing script is not built. A plan's
Status and Direction are set with /update-plan, as today; when a plan's branch merges, git carries
its plan file like any other file.

## Round 2 — fixes from the first review of PR #1016

- An issue in a plan that main marks Done or Dropped (a bug found later) starts as an issue in no
  plan: a feature branch off main, and the record says why. A closed plan's branch is never cut.
- When main's plan file already reads In Progress on `plan/<id>/base`, the cut has nothing to
  commit on main and cuts the branch from main's tip.
- setup_branch.py's own test is brought up to date (a plan file and the plan tool in its scratch repo).

## Build

start-change changes what it promises, through its ICE and `/edit-play`. The plan tool's
`plan_branch.py` gets the stale-copy rule and the cut with nothing to commit on main, with tests.
