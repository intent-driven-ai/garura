# Design — #720 Manage a plan: `/update-plan`

Approved by the product owner on 2026-10-30 ("720 approved"), after two rounds on 2026-10-29/30.
Plan 717. Stories: #730 (the session), #931 (the model part); #909 folds into #730.

## What it is

One play, `/update-plan`, is a working session on one plan. A person gives instructions in their
own words, one or many at a time; the play works with them until they approve, then lands every
change at once: the plan file, GitHub and the product model, in agreement. There are no
sub-commands (no `--edit`, no `--check`, no "mark done" syntax): it is an execution, from start to
the person's approval.

## Which copy of a plan counts

- Only two copies matter: the plan's own branch (`plan/<id>/base`) and main. Every other branch
  holds the copy it was cut with; the play ignores it and tracks nothing about it.
- Whenever a plan's branch is cut — starting a plan (#989), `/start-change` on a story in a plan
  with no branch, or `/update-plan` on a plan with no branch — main's plan file is set first to
  In Progress with the branch named, committed on main, and the branch is cut from that commit.
  Main's copy then says "the work is on `plan/<id>/base`"; it may be behind, and that is all.
- The plan's branch is the only place a plan changes. When it lands on main, main's plan file
  becomes the branch's plan file, whole. A difference on main is named by the check, and the
  branch's version replaces it.
- When a plan's branch is proposed for main, `/propose-change` asks the person for the plan's
  Status and Direction and writes them in the commit it makes before raising; the merge carries
  them. Nothing is worked out (a story under #721).

## How it starts

`/update-plan <id>` or `/update-plan <a description>`.

- With a description, the play finds the plan from the plans' business intents and items, shows
  the match and waits for the person's confirmation. It never guesses and never makes a new plan
  (`/shape-plan`'s work).
- It gets onto the plan's branch:
  - on it already: it stays;
  - on main: it switches to the plan's branch; when the plan has none, it cuts one as above;
  - on any other branch, including a story branch of the same plan: it checks nothing is
    uncommitted there (else it stops and names the files), switches, and switches back at the end.
- The update never gets a branch of its own: it works on the plan's branch.

## The session

For each instruction the play:

- works out what it changes — the plan file, the GitHub issues (new, re-parented, closed,
  reopened, text changed), the product model (a feature, its thin page, its slice, its place in
  the model's index);
- checks it before it agrees — against the model, the rules for GitHub (types, real parent links,
  a bug under a story, no labels) and how an epic holds its work (one slice per epic, one story per
  feature, the epic's feature-to-story list matching the plan). When it would break something, it
  says so and offers what works; it does not just agree;
- adds it to a running list in the plan's short-term memory. That list is the design of the update.

Small changes get one line. Big ones are shown and confirmed before they join the list: dropping an
epic, moving a feature between slices, a model change, closing an item with open work under it.
Nothing is written to GitHub, the model or the plan file during the session.

## How it ends: approve or reject

- The play shows the whole list and asks: approved or rejected.
- Only a plain "approved" lands it. A question, a new direction, or "approve, but…" is not an
  approval: the play answers or follows it, shows the list again and asks again.
- "Rejected" ends the session with nothing written; the list stays in short-term memory.

On "approved":

1. the model changes, through the model sub-agent and its skills;
2. the GitHub changes, through the issue sub-agent and its skills;
3. the plan file, through a script, with a history line (who asked, when, their instructions);
4. a check that the plan file, GitHub and the model agree, and that nothing beyond the list
   changed — else it stops and names the difference;
5. one commit on the plan's branch, pushed. No start-, propose-, check- or merge-change.

Then it switches back to where the person started. The plan's branch reaches main later through
propose-change, check-change and merge-change, like all its other work.

## Rules it keeps

- A person sets every Status and Direction; nothing is worked out, and there are no roll-ups (an
  epic can be closed with open stories).
- It never cuts a branch except as above, never merges one, and never touches code.
- Changes go through sub-agents and skills; no hand edits of the model or the issues.
- It writes down which item kinds a plan may hold (#917, point 3).

## The stories

- **#730** — the session, finding the plan, the branch rules, approve or reject, the landing and the
  agreement check; the plan's item kinds written down. #909 folds in: changing an epic's or a
  story's text is one more instruction.
- **#931** — the model part: a new feature found mid-plan gets its thin page and joins its slice.
  Needs #979's thin-page path (plan 722).

## Related

- #989 — start-change starts a plan on its own (main first, then the cut).
- The story under #721 — `/propose-change` asks Status and Direction when a plan's branch is
  proposed for main; the branch's plan file replaces main's.
- #779 — start-change reads plan files from the checked-out branch.
- #990 — the product model moves with the work (the principle: choices, not gates).
