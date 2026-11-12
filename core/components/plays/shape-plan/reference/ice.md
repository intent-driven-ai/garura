# shape-plan — ICE source

The clean ICE triple this play is compiled from. Update this and recompile via
fix-play; never hand-edit the compiled SKILL.md.

## Intent

A person names a business intent that `/design-slice` has served with a slice. /shape-plan makes
the intent's one plan, once:
- the plan file, with the business intent at the top, the `epic:` mark, and a Slices list with
  each slice at Not Started;
- ONE epic for the plan;
- one Feature issue for each feature not yet built, across all the plan's slices.

Each Feature issue holds its scope of work and Context guidance, written from its feature's ICE
and its capability's ICE, and holds no failure condition and no recovery condition. The play
files no Stories: those are pieces of work that come later, from the build. When the intent
already has a plan, /shape-plan does not run: /reshape-plan changes a plan that exists.

### Constraints

- C1 — One plan for each business intent. The plan's ID is the intent's issue number; no second
  plan is made.
- C2 — The plan holds every slice that serves the intent, read from the spine's link "slice
  serves business intent". The play never picks, ranks or tests a slice: the person chose it at
  `/design-slice`.
- C3 — How a work item is found. The plan's epic is found by the plan file's `epic:` mark. A
  feature's issue is found by its `represents` mark in the plan file; when there is none, it is
  found through the tracker tool by an issue of type Feature that carries the exact line
  `Represents: <feature id>`, open or closed. A play never finds an issue by its title, and
  never reads an issue number from the product model. When two Feature issues name one
  feature, the run names both and stops before any tracker write, and the person decides. A
  Feature issue that sits under another plan's epic is shown as `held_by` that epic; the play
  never moves it without the person's answer. Within its one run the play never makes the epic
  or a Feature issue twice: a feature in two slices of the plan has one Feature issue.
- C5 — Each Feature issue holds its scope of work (the goals, the limits and the expectations)
  and its Context guidance (the four Context lines: what to read, what never to read, the
  persona, what is in and what is out), in its own words, written from every line of its
  feature's ICE and its capability's ICE except the "Fails if" lines. The play never reads the
  "Fails if" lines. No Feature issue, no epic and no plan file holds a failure condition or a
  recovery condition.
- C6 — The epic's title says what a person can see the product do, not how it is built. The
  epic holds the feature-to-story map, one line for each feature of the plan that is not built
  (a `held_by` feature's line names the epic that holds it), and the map always agrees with
  the plan file's tree.
- C7 — The play writes only the plan file, the epic and the Feature issues (and moves the old
  stories C15 names). It writes nothing in the plan's evals folder and nothing in the product
  model.
- C8 — Nothing goes to the tracker before the product owner's typed yes, at one checkpoint that
  no config value can skip. The person sees, before the yes, every tracker write the run will
  make. A stop leaves no tracker write and no plan-file change. (The shaping loop's one
  checkpoint, #796, later moves this checkpoint to the end of the loop.)
- C9 — The play files a Feature issue only from a ready ICE (the ready check). A feature whose
  ICE is not ready is skipped: no Feature issue is filed or changed for it, no old work is
  searched or moved for it, and the run names it in the brief; the play never guesses its
  content.
- C10 — The play opens its own change with start-work and lands it through commit-work,
  review-work, validate-work and merge-work, on the plan's branch when the intent has one.
- C11 — Plain words (ASD-STE100) and personas in the brief, the epic, the Feature issues and the
  plan file; no real person's name.
- C13 — The tracker shape. The plan's epic is an issue of type Epic, with no label. Each Feature
  issue is an issue of type Feature, with no label, a sub-issue of the epic. The epic stands for
  the plan, not for a slice. Anything else under the epic that the plan file does not place is
  misplaced work: the play names each item with its title and writes nothing until a person
  files it in its own place (#879).
- C14 — When the intent already has a plan file (`<plans>/<id>.yaml`, in the checked-out tree or
  on main), the play stops at pre-flight, before start-work and before any read of the model
  or any write, and says the plan exists and that /reshape-plan changes it. This is a
  pre-flight check: the play that changes an existing plan is /reshape-plan.
- C15 — Clean as you go. For a ready feature with no Feature issue, the play searches the
  tracker, through the tracker tool, for old work on that feature: an issue of type Story whose
  text names the feature's id or whose title names the feature, and an old issue of type
  Feature that names the feature but has no exact `Represents:` line. It proposes one action in
  the brief: an old open story is found → file the Feature issue and move each such story
  inside it (the brief names the parent each story leaves); only finished old work is found
  (closed as completed) → file the Feature issue already closed as completed, so the feature
  counts as built and is left out of the plan; nothing is found → file a new Feature issue. An
  old issue of type Feature is named in the brief and left as it is. One old story that two
  features claim is a problem: the run names it and stops. Nothing happens without the
  person's yes. The play looks only at the plan's own features.
- C16 — Built features. A feature whose Feature issue is closed as completed is built. It is not
  put in the plan (no tree node, no map line), nothing is written to its issue, and the brief
  names it as left out. A feature whose Feature issue is closed as not planned is not built,
  and it is left out of the plan too: its issue stays as it is (no reopen, no move, no new
  issue), it gets no tree node and no map line, and the brief names it, with its issue number,
  under "Not planned, left out". The run goes on.

### Failure conditions

- F1 — A feature of the plan that is not built and whose ICE is ready has no Feature issue in
  the plan, or the plan holds a Feature issue for a feature that is in none of its slices.
- F2 — There is a second plan for one intent, a second epic for one plan, or a second Feature
  issue for one feature.
- F3 — A Feature issue, the epic or the plan file holds a failure condition or a recovery
  condition.
- F4 — The plan file's tree and the epic's feature-to-story map disagree, or the plan file has no
  business intent at the top, no `epic:` mark, or no Slices list with each slice at Not Started.
- F5 — A tracker write happened before the product owner's yes, a write the person did not see
  in the brief happened, or a stop left a tracker write or a plan-file change behind.
- F7 — The run wrote outside the plan file, the epic, the Feature issues and the moves C15
  names (the evals folder, the product model, or any other file).
- F8 — A Feature issue was filed or changed from an ICE that is not ready, or a skipped feature
  is not named in the brief.
- F9 — The change landed outside the change plays, or on the wrong branch.
- F10 — A page names a real person, or a person cannot follow it.
- F11 — The epic or a Feature issue carries a label, the epic's issue type is not Epic, a Feature
  issue's type is not Feature, a Feature issue is not a sub-issue of the epic (unless it is
  `held_by`), or the run filed a Story.
- F12 — The epic holds a sub-issue that the plan does not place, and the run wrote to the
  tracker, or did not name that item with its title.
- F13 — The intent already had a plan file, and the run went on past pre-flight: it opened a
  change, read the model, or wrote anything; or it stopped without naming /reshape-plan.
- F14 — The run found an issue by its title or by an issue number in the product model; matched
  a line that is not exact, or an issue that is not of type Feature; filed a second Feature
  issue for a feature that has one; wrote past two Feature issues that name one feature without
  naming both and stopping; or moved a `held_by` Feature issue without the person's answer.
- F15 — For a feature with no Feature issue, the run did not search for old work, or did
  something other than the one action the brief proposed: an old open story was not moved
  inside the new Feature issue, or was moved with no brief line naming the parent it leaves;
  finished old work did not give a Feature issue closed as completed, or its feature stayed in
  the plan; or the run searched or wrote for a feature outside the plan, or wrote past an old
  story that two features claim.
- F16 — A feature whose Feature issue is closed as completed or as not planned was put in the
  plan, its issue was written to (reopened, moved or changed), a new Feature issue was filed for
  it, or the brief did not name it as left out (a not-planned one under "Not planned, left out",
  with its issue number); or the run stopped for a Feature issue closed as not planned.

## Context

- The product model: the ontology (`standards/schemas/product-os/ontology.md`, v17: Plan, Epic,
  Feature issue, Story, Chore, Slice, Feature, ICE; Q48 to Q63), read through the memory tool;
  the spine (`_spine.yaml`: `slices` with `feature_refs` in build order and `intents`,
  `features` with their `capability`, `ices` with their thin mark) and each slice's record
  (`slices/<id>.yaml`). The model holds no issue number and no plan (ADR 069): a play reads no
  issue from it.
- ADR 068 (each product feature has one Feature issue that names it with the exact line
  `Represents: <feature id>`, holds its scope of work and Context guidance, and is found by the
  plan file's mark or by that line, never by title; closed as completed means built), ADR 069
  (the plan is where the model meets the work: one epic for each plan, the plan file names its
  business intent, its `epic:` mark and its Slices list; one eval for each plan), ADR 052
  (/design-slice writes the hidden file), ADR 047 (the ICE and its ready check).
- The plan files: `.garura/project/plans/<id>.yaml` (the business intent at the top, id, title,
  status, direction, `epic`, `slices`, and a tree: the epic, with each Feature issue under it,
  each node with its issue, kind, title, status, `represents`, and `held_by` when another
  plan's epic holds it). /shape-plan makes a plan file once; `/reshape-plan` changes a plan that
  exists, in one session the product owner approves.
- The rules: `managing-work.md` ("Type lives in the type field", "No labels, for now"),
  `standards/rules/expectation-generation.md`, `_shared/asking-a-person.md`.
- The agent that gathers the model and runs the skill: `product-os-keeper`. The skill that
  writes the epic's title and each Feature issue's title, scope of work and Context guidance:
  `author-work-items`. The tracker reads, the search and the writes go through the code-host
  adapter.
- The product owner's decisions: `.garura/project/issues/818/context/decisions.md` (Q-find-1,
  Q-found-1, Q-label-1, Q-change-1); `.garura/project/issues/1025/context/` (the approved
  design of this rework).
- Personas: the product owner (runs /shape-plan, approves the tracker writes, tracks the plan);
  the build play, which reads the Feature issues; the eval play, which reads the epic, its map
  and its Feature issues.

## Expectation

### Success scenarios

- S1 — (product owner, first plan) Given an intent served by one slice with three features and no
  plan file, when the product owner runs /shape-plan and types yes, then the plan file, one epic
  and three Feature issues exist, one for each feature, and the epic's map names the three.
  Measure: the plan check reads ok, the epic is in the tracker with type Epic and the three
  Feature issues with type Feature, each a sub-issue of the epic, none with a label, no Story
  was filed, and no Feature issue holds a "Fails if" line of its two ICE.
- S6 — (product owner, stop) Given any plan, when the product owner types stop at the checkpoint,
  then nothing reaches the tracker. Measure: the run's record lists no tracker write, and the plan
  file and the tree are as they were at the run's start.
- S7 — (product owner, an ICE not ready) Given a slice where one feature's ICE is not ready, when
  the product owner runs /shape-plan, then that feature gets no Feature issue and the brief
  names it, and the other Feature issues are filed after the yes. Measure: the record lists the
  skipped feature with its reason, the brief names it, and the plan check reads ok for the other
  features.
- S8 — (product owner, misplaced work) Given an epic named by the plan file's `epic:` mark that
  holds work the plan does not place (for example closed chores filed under it), when the
  product owner runs the find, then the run names each item with its title as not this plan's
  work and stops before any tracker write. Measure: `work-items.json` lists each item in
  `misplaced` with its title, there is no `tracker-record.json`, and the plan file is as it was.
- S9 — (product owner, a plan that exists) Given an intent that already has a plan file, when the
  product owner runs /shape-plan, then the play stops at pre-flight and points to /reshape-plan.
  Measure: the check's record reads `exists: true` and its message names `/reshape-plan <id>`;
  no change issue, no branch, no short-term folder and no tracker write was made, no file is left
  behind, and the plan file is as it was.
- S12 — (product owner, two slices) Given no plan file and an intent served by two slices that
  hold four features between them, one feature in both, when the product owner runs /shape-plan
  and types yes, then one epic and one Feature issue for each pending feature of both slices
  exist. Measure: `tracker-record.json` `created` holds one epic and one Feature issue for each
  distinct ready feature that is not built (the shared feature once); the plan file has one
  `epic:` mark, a Slices list with both slices at Not Started, and one feature node for each;
  and the plan check and the tracker check read ok.
- S13 — (product owner, an old open story) Given no plan file and a feature with no Feature issue
  whose id an open Story names in its text, under another parent, when the product owner runs
  /shape-plan and types yes, then a Feature issue is filed for the feature and the story is moved
  inside it. Measure: `work-items.json` lists the feature as `make-and-move` with the story and
  the parent it leaves; `brief.md` names the move and that parent; after the write the story is
  a sub-issue of the new Feature issue; and the tracker check reads ok.
- S14 — (product owner, old finished work) Given no plan file and a feature with no Feature issue
  whose only old work is a Story closed as completed, when the product owner runs /shape-plan and
  types yes, then a Feature issue is filed already closed as completed, and the feature is left
  out of the plan. Measure: `work-items.json` lists the feature as `make-closed`; `brief.md`
  names it as left out; the tracker holds a Feature issue with its exact `Represents:` line,
  closed as completed; the plan file has no node for the feature and the map no line; and the
  plan check reads ok with the feature in `left_out`.
- S15 — (product owner, a duplicate) Given two issues of type Feature that carry the same exact
  `Represents:` line, when the product owner runs /shape-plan, then the run stops before any
  tracker write and names both. Measure: `work-items.json` reads `ok: false` and its
  `duplicates` names the feature and both issues; there is no `tracker-record.json`; and no
  plan file is written.

- S16 — (product owner, a feature not planned) Given no plan file and a feature whose Feature
  issue is closed as not planned, when the product owner runs /shape-plan and types yes, then
  the run goes on, the feature is left out of the plan, and its Feature issue stays as it is.
  Measure: `work-items.json` lists the feature as `not-planned` with its issue and reads
  `ok: true`; `brief.md` names it, with its issue number, under "Not planned, left out"; the
  issue is still closed as not planned with its body unchanged and no new Feature issue for the
  feature; the plan file has no node for it and the map no line; and the plan check reads ok
  with the feature in `left_out`.

### Done means

- D1 — the plan check reads ok: each ready feature of each slice the plan holds that is not built
  has exactly one Feature issue node under the plan's one epic (or is named as skipped or left
  out), the plan file carries the business intent, the `epic:` mark and the Slices list, and the
  plan file's tree agrees with the epic's map.
  check: { type: field_equals, file: "context/shape-plan/plan-check.json", field: "ok", equals: true }
- D2 — the product owner's recorded answer is yes.
  check: { type: field_equals, file: "context/shape-plan/approval.json", field: "decision", equals: "yes" }
- D3 — the draft check reads ok: no Feature issue and no epic holds a failure or recovery
  condition, and each Feature issue has its scope of work and its Context guidance.
  check: { type: field_equals, file: "context/shape-plan/drafts-check.json", field: "ok", equals: true }
- D4 — the tracker check reads ok: each work item the run wrote is in the tracker as the record
  says, the epic with type Epic and each Feature issue with type Feature and its exact
  `Represents:` line, none with a label.
  check: { type: field_equals, file: "context/shape-plan/tracker-check.json", field: "ok", equals: true }
- D5 — the write guard reads ok: the run changed no file outside the plan file.
  check: { type: field_equals, file: "context/shape-plan/guard-report.json", field: "ok", equals: true }

### Recovery (one per failure condition)

- REC1 (F1) — file the missing Feature issue; take a Feature issue that stands for no feature of
  the plan's slices off the epic and out of the plan. Handoff: autonomous.
- REC2 (F2) — keep the first plan, epic or Feature issue, take the copy out of the plan, and tell
  the person which one was kept. Handoff: human.
- REC3 (F3) — take the line out and draft the Feature issue or the epic again from the two ICE
  without the "Fails if" lines. Handoff: autonomous.
- REC4 (F4) — write the plan file's top, tree and the epic's map again from the run's record, so
  they agree. Handoff: autonomous.
- REC5 (F5) — undo each tracker write the record lists and put back the plan file as it was;
  show the brief again. Handoff: human.
- REC7 (F7) — undo the write outside the allowed set. Handoff: autonomous.
- REC8 (F8) — take back the Feature issue filed or changed from the feature that is not ready,
  skip the feature, and name it in the brief. Handoff: autonomous.
- REC9 (F9) — land the change through the change plays, on the branch the target script gives.
  Handoff: human.
- REC10 (F10) — rewrite with personas and plain words. Handoff: autonomous.
- REC11 (F11) — take the label off, set the issue type to Epic on the epic and to Feature on a
  Feature issue, make each Feature issue that is not `held_by` a sub-issue of the epic, and take
  back a Story the run filed. Handoff: autonomous.
- REC12 (F12) — stop before any tracker write and name each misplaced item with its title; a
  person files it in its own place and takes it off the epic, then runs the play again.
  Handoff: human.
- REC13 (F13) — stop the run, undo whatever it opened or wrote after pre-flight (the change
  issue's branch and short-term folder, any tracker write), and show the product owner that the
  plan exists and that `/reshape-plan <id>` changes it. Handoff: human.
- REC14 (F14) — take back the second Feature issue and use the one the exact line names; put
  back a `held_by` Feature issue that was moved; for two Feature issues that name one feature,
  stop before any tracker write and name both — a person keeps one and gives the other another
  type or line, then runs the play again. Handoff: human.
- REC15 (F15) — run the old-work search for the feature, and do the one action it gives: move
  the old open story inside the Feature issue and name the parent it left, or close the Feature
  issue as completed and take the feature out of the plan; undo a search result or a write for
  a feature outside the plan; for an old story two features claim, stop and name it — a person
  says which feature it is for. Handoff: human.
- REC16 (F16) — take the feature's node and map line out of the plan, undo any write to its
  closed Feature issue, take back a new Feature issue filed for it, and name it in the brief as
  left out (a not-planned one under "Not planned, left out", with its issue number); a run that
  stopped for a not-planned Feature issue is run again. Handoff: autonomous.
