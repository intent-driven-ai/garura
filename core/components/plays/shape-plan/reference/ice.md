# shape-plan — ICE source

The clean ICE triple this play is compiled from. Update this and recompile via
edit-play; never hand-edit the compiled SKILL.md.

## Intent

A person names a business intent that `/shape-slice` has served with a slice. /shape-plan makes
the intent's one plan, or brings it up to date: the plan file, one epic for each slice the plan
holds, and one story for each feature of that slice. Each story is written from its feature's
ICE and that feature's capability's ICE, and holds no failure condition and no recovery
condition. A second run makes no copies.

### Constraints

- C1 — One plan for each business intent. The plan's ID is the intent's issue number. A new
  slice shaped for the same intent joins the same plan; no second plan is made.
- C2 — The plan holds every slice that serves the intent, read from the spine's link "slice
  serves business intent". The play never picks, ranks or tests a slice: the person chose it at
  `/shape-slice`.
- C3 — The play finds before it makes. An epic that already stands for a slice, or a story that
  already stands for a feature, is used and never made again: one epic for each slice, and one
  story for each feature in each epic. A work item stands for a slice or a feature when the plan
  file marks it so (`represents: <slice id>` on the epic, `represents: <feature id>` on the
  story); the play never matches a work item by its title.
- C4 — When a feature leaves the slice after its story exists, the story moves out of the plan
  (out of the plan file's tree and the epic's map) and stays in the tracker; it is never deleted.
  A feature that comes into the slice gets one story.
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
- C12 — On a story it finds, the play adds the "Scope of work" and the "Context guidance"
  sections when they are missing, and keeps every line a person wrote; it never rewrites or
  deletes a person's text.
- C13 — An epic and a story are marked in the tracker by the issue type field, with no label:
  an epic is an issue of type Feature, and a story is an issue of type Story.

### Failure conditions

- F1 — A feature of a slice the plan holds has no story, or a story in the plan stands for no
  feature of its slice.
- F2 — There is a second plan for one intent, a second epic for one slice, or a second story for
  one feature in one epic.
- F3 — A story, the epic or the plan file holds a failure condition or a recovery condition.
- F4 — The plan file's tree and the epic's feature-to-story map disagree.
- F5 — A tracker write happened before the product owner's yes, a write the person did not see
  in the brief happened, or a stop left a tracker write or a plan-file change behind.
- F6 — A story for a feature that left the slice was deleted, or stays in the plan.
- F7 — The run wrote outside the plan file, the epic and the stories (the evals folder, the
  product model, or any other file), or a found story lost a line a person wrote.
- F8 — A story was built from an ICE that is not ready, or a skipped part is not named in the
  brief.
- F9 — The change landed outside the change plays, or on the wrong branch.
- F10 — A page names a real person, or a person cannot follow it.
- F11 — An epic or a story carries a label, or an epic's issue type is not Feature, or a story's
  issue type is not Story.

## Context

- The product model: the ontology (`standards/schemas/product-os/ontology.md`, v11: Plan, Epic,
  Story, Slice, Feature, ICE), read through the memory tool; the spine (`_spine.yaml`: `slices`
  with `feature_refs` in build order and `intents`, `features` with their `capability`, `ices`
  with their thin mark) and each slice's record (`slices/<id>.yaml`).
- ADR 049 (the shaping loop: /shape-slice, then /shape-plan, then /shape-eval; one plan for each
  business intent; how the ICE reaches the story and the hidden file), ADR 052 (/shape-slice
  writes the hidden file), ADR 047 (the ICE and its ready check).
- The plan files: `.garura/project/plans/<id>.yaml` (id, title, status, branch, tree of work
  items, each with its issue, kind, title, status, `represents` and children). Plans are kept by
  hand until update-plan (#730) exists; the play writes only its slice, epic and story nodes and
  keeps every other node as it is.
- The rules: `managing-work.md` ("Type lives in the type field", "No labels, for now"; an Epic
  is filed as type Feature, the organization's type for it),
  `standards/rules/expectation-generation.md`, `_shared/asking-a-person.md`.
- The agent that gathers the model and runs the skill: `product-os-keeper`. The skill that
  writes the epic's title and each story's scope of work and Context guidance:
  `author-work-items` (new). The tracker writes go through the code-host adapter.
- The product owner's decisions: `.garura/project/issues/818/context/decisions.md` (Q-find-1,
  Q-found-1, Q-label-1, Q-change-1, and decision 5: the Epic's tracker type is Feature).
- Personas: the product owner (runs /shape-plan, approves the tracker writes, tracks the plan);
  the build play, which reads the stories; the eval play (#798), which reads the epic, its map
  and its stories.

## Expectation

### Success scenarios

- S1 — (product owner, first plan) Given an intent served by one slice with three features and no
  plan file, when the product owner runs /shape-plan and types yes, then the plan file, one epic
  and three stories exist, one for each feature, and the epic's map names the three stories.
  Measure: the plan check reads ok, the epic is in the tracker with type Feature and the three
  stories with type Story, none with a label, and no story holds a "Fails if" line of its two ICE.
- S2 — (product owner, second run) Given a plan made by an earlier run and no change to the slice,
  when the product owner runs /shape-plan again and types yes, then no new issue is made.
  Measure: the run's record lists no created issue, and the plan file is byte for byte as it was.
- S3 — (product owner, items made by hand) Given a plan file that marks a hand-made epic and its
  stories with `represents`, when the product owner runs /shape-plan and types yes, then the play
  uses them. Measure: no new issue is made; each marked story gains only the missing sections;
  every line a person wrote is still on it.
- S4 — (product owner, the slice changed) Given a plan whose slice lost one feature and gained
  another, when the product owner runs /shape-plan and types yes, then the story of the feature
  that left is out of the plan file's tree and the epic's map and is still open in the tracker,
  and the feature that came in has one new story and one new map line. Measure: the plan check
  reads ok and the moved-out issue's state is open.
- S5 — (product owner, a second slice) Given an intent whose plan holds one slice and a second
  slice shaped for it, when the product owner runs /shape-plan and types yes, then the same plan
  file gains the second slice and its epic. Measure: there is one plan file for the intent, with
  two slice nodes, each with its own epic.
- S6 — (product owner, stop) Given any plan, when the product owner types stop at the checkpoint,
  then nothing reaches the tracker. Measure: the run's record lists no tracker write, and the plan
  file and the tree are as they were at the run's start.
- S7 — (product owner, an ICE not ready) Given a slice where one feature's ICE is not ready, when
  the product owner runs /shape-plan, then that feature's story is not made and the brief names
  it, and the other stories are made after the yes. Measure: the record lists the skipped feature
  with its reason, the brief names it, and the plan check reads ok for the other features.

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
  says, the epic with type Feature and each story with type Story, and none with a label.
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
- REC6 (F6) — open the deleted story again, or take it out of the plan's tree and the epic's map,
  so it stays in the tracker and out of the plan. Handoff: human.
- REC7 (F7) — undo the write outside the allowed set, or put back the person's line on the found
  story. Handoff: autonomous.
- REC8 (F8) — take back the story built from the part that is not ready, skip the part, and name
  it in the brief. Handoff: autonomous.
- REC9 (F9) — land the change through the change plays, on the branch the target script gives.
  Handoff: human.
- REC10 (F10) — rewrite with personas and plain words. Handoff: autonomous.
- REC11 (F11) — take the label off, and set the issue type to Feature on an epic and to Story on
  a story. Handoff: autonomous.
