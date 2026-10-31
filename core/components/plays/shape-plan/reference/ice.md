# shape-plan — ICE source

The clean ICE triple this play is compiled from. Update this and recompile via
edit-play; never hand-edit the compiled SKILL.md.

## Intent

A person names a business intent that `/shape-slice` has served with a slice. /shape-plan makes
the intent's one plan, once: the plan file, one epic for each slice the plan holds, and one
story for each feature of that slice. Each story is written from its feature's ICE and that
feature's capability's ICE, and holds no failure condition and no recovery condition. When the
intent already has a plan, /shape-plan does not run: /update-plan changes a plan that exists.

### Constraints

- C1 — One plan for each business intent. The plan's ID is the intent's issue number; no second
  plan is made.
- C2 — The plan holds every slice that serves the intent, read from the spine's link "slice
  serves business intent". The play never picks, ranks or tests a slice: the person chose it at
  `/shape-slice`.
- C3 — Within its one run, the play never makes an epic or a story twice: one epic for each
  slice, and one story for each feature in each epic. A work item stands for a slice or a
  feature when the plan file marks it so (`represents: <slice id>` on the epic,
  `represents: <feature id>` on the story); the play never matches a work item by its title.
- C5 — Each story holds its scope of work (the goals, the limits and the expectations) and its
  Context guidance (the four Context lines: what to read, what never to read, the persona, what
  is in and what is out), in its own words, written from every line of its feature's ICE and its
  capability's ICE except the "Fails if" lines. The play never reads the "Fails if" lines. No
  story, no epic and no plan file holds a failure condition or a recovery condition.
- C6 — The epic's title says what a person can see the product do, not how it is built. The
  epic holds the feature-to-story map, one line for each feature of its slice, and the map always
  agrees with the plan file's tree.
- C7 — The play writes only the plan file, the epic and the stories. It writes nothing in the
  plan's evals folder and nothing in the product model.
- C8 — Nothing goes to the tracker before the product owner's typed yes, at one checkpoint that
  no config value can skip. The person sees, before the yes, every tracker write the run will
  make. A stop leaves no tracker write and no plan-file change. (The shaping loop's one
  checkpoint, #796, later moves this checkpoint to the end of the loop.)
- C9 — The play builds a story only from a ready ICE (the ready check). A part whose ICE is not
  ready is skipped, its story is not made, and the run names it in the brief; the play never
  guesses its content.
- C10 — The play opens its own change with start-change and lands it through commit-change,
  propose-change, check-change and merge-change, on the plan's branch when the intent has one.
- C11 — Plain words (ASD-STE100) and personas in the brief, the epic, the stories and the plan
  file; no real person's name.
- C13 — An epic and a story are marked in the tracker by the issue type field, with no label:
  an epic is an issue of type Epic, and a story is an issue of type Story. An epic stands for its
  slice: its sub-issues are the stories of its slice, and the work under a story hangs from that
  story. Anything else under an epic is misplaced work: the play names each item with its title
  and writes nothing until a person files it in its own place (its own story, bug or chore, which
  `/shape-slice` and `/shape-plan` place when they run) (#879).

- C14 — When the intent already has a plan file (`<plans>/<id>.yaml`, in the checked-out tree or
  on main), the play stops at pre-flight, before start-change and before any read of the model
  or any write, and says the plan exists and that /update-plan changes it. This is a
  pre-flight check: the play that changes an existing plan is
  /update-plan.

### Failure conditions

- F1 — A feature of a slice the plan holds has no story, or a story in the plan stands for no
  feature of its slice.
- F2 — There is a second plan for one intent, a second epic for one slice, or a second story for
  one feature in one epic.
- F3 — A story, the epic or the plan file holds a failure condition or a recovery condition.
- F4 — The plan file's tree and the epic's feature-to-story map disagree.
- F5 — A tracker write happened before the product owner's yes, a write the person did not see
  in the brief happened, or a stop left a tracker write or a plan-file change behind.
- F7 — The run wrote outside the plan file, the epic and the stories (the evals folder, the
  product model, or any other file).
- F8 — A story was built from an ICE that is not ready, or a skipped part is not named in the
  brief.
- F9 — The change landed outside the change plays, or on the wrong branch.
- F10 — A page names a real person, or a person cannot follow it.
- F11 — An epic or a story carries a label, or an epic's issue type is not Epic, or a story's
  issue type is not Story.
- F12 — An epic holds a sub-issue that is not a story of its slice, and the run wrote to the
  tracker, or did not name that item with its title.
- F13 — The intent already had a plan file, and the run went on past pre-flight: it opened a
  change, read the model, or wrote anything; or it stopped without naming /update-plan.

## Context

- The product model: the ontology (`standards/schemas/product-os/ontology.md`, v11: Plan, Epic,
  Story, Slice, Feature, ICE), read through the memory tool; the spine (`_spine.yaml`: `slices`
  with `feature_refs` in build order and `intents`, `features` with their `capability`, `ices`
  with their thin mark) and each slice's record (`slices/<id>.yaml`).
- ADR 049 (the shaping loop: /shape-slice, then /shape-plan, then /shape-eval; one plan for each
  business intent; how the ICE reaches the story and the hidden file), ADR 052 (/shape-slice
  writes the hidden file), ADR 047 (the ICE and its ready check).
- The plan files: `.garura/project/plans/<id>.yaml` (id, title, status, branch, tree of work
  items, each with its issue, kind, title, status, `represents` and children). /shape-plan makes
  a plan file once; `/update-plan` (#720, #730) changes a plan that exists — a new epic, story,
  feature, bug or status — in one session the product owner approves.
- The rules: `managing-work.md` ("Type lives in the type field", "No labels, for now"; an Epic
  is filed as type Epic),
  `standards/rules/expectation-generation.md`, `_shared/asking-a-person.md`.
- The agent that gathers the model and runs the skill: `product-os-keeper`. The skill that
  writes the epic's title and each story's scope of work and Context guidance:
  `author-work-items` (new). The tracker writes go through the code-host adapter.
- The product owner's decisions: `.garura/project/issues/818/context/decisions.md` (Q-find-1,
  Q-found-1, Q-label-1, Q-change-1). #875 replaced decision 5 (the Epic's tracker type was
  Feature, while the organization had no Epic type): an Epic is now type Epic.
- Personas: the product owner (runs /shape-plan, approves the tracker writes, tracks the plan);
  the build play, which reads the stories; the eval play (#798), which reads the epic, its map
  and its stories.

## Expectation

### Success scenarios

- S1 — (product owner, first plan) Given an intent served by one slice with three features and no
  plan file, when the product owner runs /shape-plan and types yes, then the plan file, one epic
  and three stories exist, one for each feature, and the epic's map names the three stories.
  Measure: the plan check reads ok, the epic is in the tracker with type Epic and the three
  stories with type Story, none with a label, and no story holds a "Fails if" line of its two ICE.
- S6 — (product owner, stop) Given any plan, when the product owner types stop at the checkpoint,
  then nothing reaches the tracker. Measure: the run's record lists no tracker write, and the plan
  file and the tree are as they were at the run's start.
- S7 — (product owner, an ICE not ready) Given a slice where one feature's ICE is not ready, when
  the product owner runs /shape-plan, then that feature's story is not made and the brief names
  it, and the other stories are made after the yes. Measure: the record lists the skipped feature
  with its reason, the brief names it, and the plan check reads ok for the other features.
- S8 — (product owner, misplaced work) Given an epic that holds work that is not a story of its
  slice (for example closed chores filed under the epic), when the product owner runs
  /shape-plan, then the run names each item with its title as not this slice's work and stops
  before any tracker write. Measure: `work-items.json` lists each item in `misplaced` with its
  title, there is no `tracker-record.json`, and the plan file is as it was.

- S9 — (product owner, a plan that exists) Given an intent that already has a plan file, when the
  product owner runs /shape-plan, then the play stops at pre-flight and points to /update-plan.
  Measure: the check's record reads `exists: true` and its message names `/update-plan <id>`;
  no change issue, no branch, no short-term folder and no tracker write was made, no file is left
  behind, and the plan file is as it was.

### Done means

- D1 — the plan check reads ok: each feature of each slice the plan holds has exactly one story
  (or is named as skipped), and the plan file's tree agrees with each epic's map.
  check: { type: field_equals, file: "context/shape-plan/plan-check.json", field: "ok", equals: true }
- D2 — the product owner's recorded answer is yes.
  check: { type: field_equals, file: "context/shape-plan/approval.json", field: "decision", equals: "yes" }
- D3 — the draft check reads ok: no story and no epic holds a failure or recovery condition, and
  each story has its scope of work and its Context guidance.
  check: { type: field_equals, file: "context/shape-plan/drafts-check.json", field: "ok", equals: true }
- D4 — the tracker check reads ok: each work item the run wrote is in the tracker as the record
  says, the epic with type Epic and each story with type Story, and none with a label.
  check: { type: field_equals, file: "context/shape-plan/tracker-check.json", field: "ok", equals: true }
- D5 — the write guard reads ok: the run changed no file outside the plan file.
  check: { type: field_equals, file: "context/shape-plan/guard-report.json", field: "ok", equals: true }

### Recovery (one per failure condition)

- REC1 (F1) — make the missing story; move a story that stands for no feature of its slice out
  of the plan. Handoff: autonomous.
- REC2 (F2) — keep the first plan, epic or story, move the copy out of the plan, and tell the
  person which one was kept. Handoff: human.
- REC3 (F3) — take the line out and draft the story or the epic again from the two ICE without
  the "Fails if" lines. Handoff: autonomous.
- REC4 (F4) — write the plan file's tree and the epic's map again from the run's record, so they
  agree. Handoff: autonomous.
- REC5 (F5) — undo each tracker write the record lists and put back the plan file as it was;
  show the brief again. Handoff: human.
- REC7 (F7) — undo the write outside the allowed set. Handoff: autonomous.
- REC8 (F8) — take back the story built from the part that is not ready, skip the part, and name
  it in the brief. Handoff: autonomous.
- REC9 (F9) — land the change through the change plays, on the branch the target script gives.
  Handoff: human.
- REC10 (F10) — rewrite with personas and plain words. Handoff: autonomous.
- REC11 (F11) — take the label off, and set the issue type to Epic on an epic and to Story on
  a story. Handoff: autonomous.
- REC12 (F12) — stop before any tracker write and name each misplaced item with its title; a
  person files it in its own place and takes it off the epic, then runs the play again.
  Handoff: human.
- REC13 (F13) — stop the run, undo whatever it opened or wrote after pre-flight (the change
  issue's branch and short-term folder, any tracker write), and show the product owner that the
  plan exists and that `/update-plan <id>` changes it. Handoff: human.
