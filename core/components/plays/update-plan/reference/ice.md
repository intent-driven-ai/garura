# update-plan — ICE source

The clean ICE triple this play is compiled from. Update this and recompile via
edit-play; never hand-edit the compiled SKILL.md.

## Intent

A person manages one plan in a working session: they give instructions in their own words, the
play works out and checks what each one changes, keeps a running list, and on one plain
"approved" lands the whole list at once — the product model, the tracker and the plan file — so
that afterwards all three agree and nothing the person did not approve has changed.

A plan is the work toward one business intent, kept in its plan file on the plan's own branch.
Its statuses and its direction are what a person says they are, never worked out.

### Constraints

- C1 — The play finds the plan from its number, or from a description. A description's match is
  shown and the play waits for the person's yes. It never guesses a plan and never makes a new
  one.
- C2 — The play works only on the plan's branch. On any branch with uncommitted work — the
  plan's own branch included — it stops, names the files and changes nothing; the person cleans
  up. Otherwise it switches to the plan's branch and goes back to the starting branch at the end. For a plan with no branch,
  main's plan file is set to In Progress with the branch named, committed on main, and the branch
  is cut from that commit: the one write before approval.
- C3 — Each instruction is turned into list entries and each entry is checked against the
  plan's rules before it joins the list: the item kinds a plan may hold, a parent of the right
  kind, one story for each feature in an epic, a status the plan knows, no labels, an item
  closed with open work under it. A break is shown with what works instead. The person may
  override it ("do it anyway"); the override is recorded.
- C4 — A big change (dropping an epic, moving a feature between slices, any model change,
  closing an item with open work under it) is shown and confirmed before it joins the list.
- C5 — Nothing is written to the tracker, the product model or a plan file before a plain
  "approved", except C2's branch step. A question, a new instruction or "approved, but …" is
  answered or followed, the list is shown again and the play asks again. "Rejected" lands
  nothing and the session goes on: the person changes the list until it is ready, and the play
  asks again. "Abort" ends the session with nothing written: the list is dropped,
  any record the session wrote in the plan's own folder is put back as it was (by a script that
  records what it put back), a plan branch the
  session cut is undone (the branch is deleted and main's plan file is put back as it was, when
  nothing else has landed on that branch), and the session goes back where it started.
- C6 — What lands is exactly the list the person saw when they approved it. The check that the
  approval is for this very list leaves its own record before the first write.
- C7 — On "approved": the model first, then the tracker, then the plan file (it keeps no
  history), then the check that the three agree and nothing else changed, then one commit on the
  plan's branch, pushed, whose message names the person's instructions, the overrides and what is
  owed (git keeps the history); then back to the starting branch. It runs no change play, never merges a branch and
  never touches code. Writing the model only after "approved" is a declared exception to
  write-then-review (ADR 062); its containment holds: after the last model write and before the
  commit, the shared scoped-write guard puts back any model path outside the session's parts,
  and then nothing is committed and the person is told.
- C8 — A person sets every status and the plan's direction. Nothing is worked out from the work
  under an item: no roll-ups.
- C9 — Tracker changes go through the issue sub-agent and its skills; model changes through the
  model sub-agent and its skills. No hand edits of either.
- C10 — Every screen the person sees comes from the plan-update template. A question to the
  person is shown in the four parts of the shared asking rule (`_shared/asking-a-person.md`):
  the question, the answer we have, why it matters, and examples from different domains.
- C11 — A new feature found while the plan is in progress is placed under its capability, and in
  the slice the plan holds, with a thin ICE and both thin marks, linked to the business intent
  and to the issue that found it; its story goes under the slice's epic, with its line in the
  epic's feature-to-story map. Its confirm screen always warns that its ICE will be thin and can
  be deepened with `/discover-capabilities`. It may join a slice in progress (its epic past
  ready); then the confirm screen says so and names each such epic, with its status, as out of
  date (ADR 058, as amended by ADR 062). When the plan holds no slice, its story goes where the person
  names and the slice is recorded as owed. The play never writes the evals folder; the
  hidden-file entry and the eval scenarios are named as owed.
- C12 — The play ends by proving its Done means at close, never by its step list running out.

### Failure conditions

- F1 — A plan is guessed, or a new plan is made.
- F2 — The play switches away from a branch with uncommitted work, goes on over uncommitted
  work on the plan's own branch, or writes on a branch other than the plan's (beyond C2's
  main-first step).
- F3 — A write reaches the tracker, the model or a plan file before a plain "approved", other
  than C2's branch step.
- F4 — What lands differs from the list the person approved: more, less or changed.
- F5 — After the landing, the plan file and the tracker disagree — an item's status against its
  open or closed state and close reason, a title, a parent — or a dropped item stays open.
- F6 — An entry that breaks a rule joins the list without being shown, or an override is not in
  the landing's commit message.
- F7 — A status or the direction changes that the person did not ask for.
- F8 — A tracker or model write is made other than through the sub-agents' skills.
- F9 — A screen is worded by the play instead of the template.
- F10 — A new feature lands without its thin page, its model entry with both thin marks, or its
  story; or the evals folder is written; or what is owed is not named; or its confirm screen
  lacks the thin warning, or does not name the epic of a slice in progress as out of date.
- F11 — The close reports COMPLETED without the Done means held.
- F12 — The session does not end on the branch the person started on.
- F13 — A model path outside the session's parts is in the landing's commit, or the commit is
  made when the scoped-write guard put a path back.

## Context

- The approved designs: `.garura/project/issues/720/specs/design.md` (what the session is) and
  `build-design.md` (how it is built), plan 717, feature #720, stories #730 and #931, chore #917.
- The plan files: `.garura/project/plans/<id>.yaml`; the plan-view template's statuses (Not
  Started, In Progress, Now, Blocked, Done, Dropped for an item; Not Started, In Progress,
  Paused, Done, Dropped for a plan) and directions (1, 2, 3 or none). The item kinds: epic,
  feature, story, spike, chore, bug.
- The plan tool's plan-branch script (`.garura/core/tools/plan/plan_branch.py`): stop on
  uncommitted work (on every path), then stay, switch, or main first then the cut.
- The tracker rules (ontology, managing-work): an epic and a story have types and no labels; a
  bug sits under the story that brought it in; a spike or chore under a story.
- Skills: `author-plan-changes` and `track-plan-changes` (issue sub-agent); `enrich-grounding`
  and `link-model-part` (model sub-agent).
- The principle that a person is never stopped without a choice, and an override is recorded
  (#992); a stop on uncommitted work is the person's to clean up (the product owner,
  2026-10-30).
- ADR 062: the model is written only after "approved", a declared exception in the model-write
  rule (`standards/rules/direct-model-write.md`), contained by the shared scoped-write guard
  (`scoped_write_guard.py`, stamped beside the play's scripts); a new feature may join a slice
  in progress, amending ADR 058. The fix design of the PR #998 review:
  `.garura/project/issues/720/specs/fix-design-round-3.md`.
- The shared rule for asking a person (`_shared/asking-a-person.md`); the play's own fixed file
  steps (`session_files.py`: the plan's issue numbers, the abort restore, the guard).

## Expectation

### Success scenarios

- **S1 — product owner, several instructions, one approval.** Given a plan on its branch, when
  the person finishes an item, drops one, renames one, sets the plan's direction and types
  "approved", then the tracker and the plan file agree, and one commit is on the
  plan's branch. *Measure:* `session.json` reads `outcome: landed` and `ok: true`, and
  `agreement.json` reads `ok: true`.
- **S2 — developer, uncommitted work.** Given a story branch, or the plan's own branch, with an
  uncommitted file, when the person runs `/update-plan`, then the play stops, names the file and changes nothing.
  *Measure:* `branch.json` reads `action: stop` with the file named, and `session.json` reads
  `outcome: stopped` and `written: false`.
- **S3 — lead, a plan with no branch.** Given a plan with no branch, when the person runs
  `/update-plan`, then main's plan file reads In Progress with the branch named and the
  branch is cut from that commit. *Measure:* `branch.json` reads `action: cut` with a
  `main_commit`.
- **S4 — product owner, rejected, then abort.** Given a list, when the person types "rejected",
  then nothing lands and the play asks what to change; when they then type "abort", nothing is
  written, the list is dropped and the session is back where it started. *Measure:* `answer.json`
  reads `decision: abort` with `rejected` in its history, and `session.json` reads `outcome:
  aborted`, `written: false` and `back: true`.
- **S5 — product owner, an override.** Given an instruction that breaks a rule, when the person
  says "do it anyway" and approves, then the entry lands and the landing's commit message
  names the override. *Measure:* `commit.json` reads `overrides_recorded: true`.
- **S6 — product owner, a new feature in a plan with no slice.** Given a new feature, when it is
  approved, then the model has its thin page and its entry with both thin marks, its story is
  where the person named, the slice and the eval scenarios are named as owed, and the evals
  folder is unchanged. *Measure:* `agreement.json` reads `features_ok: true` and
  `evals_unchanged: true`.
- **S7 — anyone, a plan found by description.** Given a description, when the play matches one
  plan, then it shows the match and waits for a yes. *Measure:* `plan.json` reads `by:
  description` and `confirmed: true` before any other record.

### Recovery

| For | Trigger | Direction | Handoff |
|-----|---------|-----------|---------|
| F1 | a plan was picked without a number or a confirmed match, or a new plan was made | stop, show the candidates, and ask for the number | human |
| F2 | a switch away from uncommitted work, or a write on another branch | stop, name the branch and the files, and leave them for the person | human |
| F3 | a record of a write exists before the approval | stop, name the write, and leave it for the person to keep or undo | human |
| F4 | the list's fingerprint differs from the one the approval recorded | write nothing more, show the list again and ask again | autonomous |
| F5 | the agreement check names a difference | name each difference; re-run the landing for the ops the record does not have; a difference that remains goes to the person | human |
| F6 | a breaking entry is in the list without its override mark, or an override is missing from the commit message | take the entry out of the list, show the break, and ask again | autonomous |
| F7 | an entry changes a status or the direction that no instruction named | take the entry out and show the list again | autonomous |
| F8 | a tracker or model write was made outside the sub-agents' skills | stop and name it for the person | human |
| F9 | a screen line does not match the template | render it again from the template | autonomous |
| F10 | a new feature's page, entry, thin marks or story is missing, the evals folder changed, or what is owed is not named | re-run the model or tracker step for that feature; put back the evals folder; name what is owed in the commit message | autonomous |
| F11 | the close would report COMPLETED without the Done means held | surface the unmet clauses and close HALTED | autonomous |
| F12 | the session ended on another branch | switch back to the starting branch; if that is stopped by uncommitted work, name it for the person | autonomous |
| F13 | the guard report names a path outside the session's parts | the guard has put it back; commit nothing, name each path for the person, who decides | human |

### Done means

- D1 — the plan was found and the person answered. *Check:* `artifact_exists` `answer.json`.
- D2 — the session closed as it should: landed and agreeing, or nothing written. *Check:* `field_equals` `session.json` `ok` = true.
- D3 — the session ended on the starting branch. *Check:* `field_equals` `session.json` `back` = true.
