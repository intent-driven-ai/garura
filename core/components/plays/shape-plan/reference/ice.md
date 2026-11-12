# shape-plan — ICE source

The clean ICE triple this play is compiled from. Update this and recompile via
fix-play; never hand-edit the compiled SKILL.md.

## Intent

A person names a business intent that `/design-slice` has served with a slice. /shape-plan makes
the intent's one plan, once:
- the plan file, with the business intent at the top, the `epic:` mark, and a Slices list with
  each slice at Not Started;
- ONE epic for the plan;
- one Feature issue for each feature of the plan's slices that is not Completed and not
  Dropped, found or filed (a closed one is opened again on the person's yes, never filed twice);
- in the product model, one field: each Unplanned feature it takes in is set to Planned.

It reads each feature's state from the model, never from the tracker. Each Feature issue holds
its scope of work and Context guidance, written from its feature's ICE and its capability's
ICE, and holds no failure condition and no recovery condition. The play files no Stories: those
are pieces of work that come later, from the build. When the intent already has a plan,
/shape-plan does not run: /reshape-plan changes a plan that exists.

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
  epic holds the feature-to-story map, one line for each feature the plan takes in (a
  `held_by` feature's line names the epic that holds it), and the map always agrees with the
  plan file's tree.
- C7 — The play writes only the plan file, the epic and the Feature issues (with the issues
  C17 opens again), and in the product model only the `status` of the features C18 names. It
  writes nothing in the plan's evals folder and nothing else in the product model.
- C8 — Nothing goes to the tracker or the product model before the product owner's typed yes,
  at one checkpoint that no config value can skip. The person sees, before the yes, every
  tracker write and every state change the run will make. A stop leaves no tracker write, no
  plan-file change and no model change. (The shaping loop's one checkpoint, #796, later moves
  this checkpoint to the end of the loop.)
- C9 — The play files a Feature issue only from a ready ICE (the ready check). A feature whose
  ICE is not ready is skipped: no Feature issue is filed, changed or opened again for it, its
  state does not change, and the run names it in the brief; the play never guesses its
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
- C16 — The state comes from the model. The play reads each feature's state from the `status`
  of its spine entry: Unplanned, Planned, In progress, Completed or Dropped. A feature with no
  `status`, or a value outside the five, is treated as Unplanned, and the brief names it under
  "Had no state". A Completed feature is left out of the plan and named under "Built, left
  out"; a Dropped feature is left out and named under "Dropped, left out". Neither gets a tree
  node or a map line, and the play does not search the tracker for it or write to its issue.
  The play never reads "built" from the tracker.
- C17 — A closed Feature issue is opened again, never filed twice. When a feature the plan
  takes in has a Feature issue closed as not planned, or closed as completed while the feature
  is not Completed, the brief shows the closed issue under "Opened again", with how it was
  closed. On the person's yes, the same issue is opened again and goes under the plan's epic
  like any found Feature issue. The play never files a second Feature issue for the feature.
- C18 — The plan sets Planned. After the yes, after the tracker writes and the plan file, each
  feature the plan takes in that is Unplanned is set to Planned in the model, through the
  `product-os-keeper` agent calling the `link-model-part` skill (mode `update`, `status:
  Planned`, `by: shape-plan (#<plan id>)`). A feature that is already Planned or In progress
  keeps its state. The brief lists each state change. The play's scoped write guard allows, in
  the model, only the spine file, and a check after the write reads the spine against the
  start of the run: each feature taken in reads Planned or kept its state, and nothing else in
  the model changed.

### Failure conditions

- F1 — A feature of the plan that is not Completed and not Dropped and whose ICE is ready has
  no Feature issue in the plan, or the plan holds a Feature issue for a feature that is in none of its slices.
- F2 — There is a second plan for one intent, a second epic for one plan, or a second Feature
  issue for one feature.
- F3 — A Feature issue, the epic or the plan file holds a failure condition or a recovery
  condition.
- F4 — The plan file's tree and the epic's feature-to-story map disagree, or the plan file has no
  business intent at the top, no `epic:` mark, or no Slices list with each slice at Not Started.
- F5 — A tracker write or a model change happened before the product owner's yes, a write the
  person did not see in the brief happened, or a stop left a tracker write, a plan-file change
  or a model change behind.
- F7 — The run wrote outside the plan file, the epic, the Feature issues and the `status` of
  the features C18 names (the evals folder, any other part of the product model, or any other
  file).
- F8 — A Feature issue was filed, changed or opened again from an ICE that is not ready, a
  skipped feature's state changed, or a skipped feature is not named in the brief.
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
- F16 — A Completed or Dropped feature was put in the plan, was searched for in the tracker,
  or had its issue written to, or the brief did not name it under "Built, left out" or "Dropped,
  left out"; the run read "built" from the tracker; or a feature with no state, or a value
  outside the five, was not treated as Unplanned or not named under "Had no state".
- F17 — A feature the plan takes in has a Feature issue closed as not planned, or closed as
  completed while the feature is not Completed, and the brief did not show it under "Opened
  again", it was opened again without the yes, it is still closed after the yes, or a second
  Feature issue was filed for the feature.
- F18 — After the run, a feature the plan takes in that was Unplanned does not read Planned; a
  Planned or In progress feature's state changed; a state change is not in the brief; the
  model write came before the tracker writes and the plan file, or did not go through
  `product-os-keeper` and `link-model-part`; or anything else in the model changed (another
  field, another feature, another file).

## Context

- The product model: the ontology (`standards/schemas/product-os/ontology.md`, v18: Plan, Epic,
  Feature issue, Story, Chore, Slice, Feature with its Status and States, ICE; Q48 to Q69),
  read through the memory tool; the spine (`_spine.yaml`: `slices` with `feature_refs` in build
  order and `intents`, `features` with their `capability` and `status`, `ices` with their thin
  mark) and each slice's record (`slices/<id>.yaml`). The model holds no issue number and no
  plan (ADR 069): a play reads no issue from it.
- ADR 070 (each feature records its own state, `status`, one of Unplanned, Planned, In
  progress, Completed or Dropped; plays read "built" from the model; the play that takes a
  feature into a plan sets Planned), ADR 068 (each product feature has one Feature issue that
  names it with the exact line `Represents: <feature id>`, holds its scope of work and Context
  guidance, and is found by the plan file's mark or by that line, never by title), ADR 069
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
- The agent that gathers the model and runs the skills: `product-os-keeper`. The skill that
  writes the epic's title and each Feature issue's title, scope of work and Context guidance:
  `author-work-items`. The skill that sets a feature's state in the spine: `link-model-part`
  (mode `update`, `status`). The tracker reads, the search and the writes go through the
  code-host adapter.
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
  distinct ready feature that is not Completed and not Dropped (the shared feature once); the plan file has one
  `epic:` mark, a Slices list with both slices at Not Started, and one feature node for each;
  and the plan check and the tracker check read ok.
- S15 — (product owner, a duplicate) Given two issues of type Feature that carry the same exact
  `Represents:` line, when the product owner runs /shape-plan, then the run stops before any
  tracker write and names both. Measure: `work-items.json` reads `ok: false` and its
  `duplicates` names the feature and both issues; there is no `tracker-record.json`; and no
  plan file is written.

- S16 — (product owner, a closed Feature issue opened again) Given no plan file and an
  Unplanned feature whose Feature issue is closed as not planned, when the product owner runs
  /shape-plan and types yes, then the same issue is opened again, under the plan's epic, and no
  second Feature issue is filed. Measure: `work-items.json` lists the feature as `reopen` with
  its issue; `brief.md` names it, with its issue number, under "Opened again"; after the write
  the issue is open and a sub-issue of the epic, `tracker-record.json` `reopened` names it and
  `created` holds no Feature issue for the feature; and the plan check and the tracker check
  read ok.
- S17 — (product owner, built and dropped features left out) Given no plan file and a slice
  where one feature reads Completed and one reads Dropped in the model, when the product owner
  runs /shape-plan and types yes, then both are left out of the plan and named. Measure:
  `work-items.json` lists them as `completed` and `dropped` with no issue (no tracker search);
  `brief.md` names one under "Built, left out" and one under "Dropped, left out"; the plan file
  has no node for either and the map no line; their states in the spine are as they were; and
  the plan check reads ok with both in `left_out`.
- S18 — (product owner, the plan sets Planned) Given no plan file and a slice with one
  Unplanned, one Planned and one In progress feature, when the product owner runs /shape-plan
  and types yes, then the Unplanned feature reads Planned in the model and the other two keep
  their states. Measure: `work-items.json` `state_changes` names only the Unplanned feature;
  `brief.md` lists that one change under "State changes in the product model";
  `planned-request.json` asks `link-model-part` for that one feature, mode `update`, `status:
  Planned`; after the write `state-check.json` and `guard-report.json` read `ok: true`.
- S19 — (product owner, a feature with no state) Given no plan file and a feature whose spine
  entry has no `status`, or a value outside the five, when the product owner runs /shape-plan
  and types yes, then it is treated as Unplanned, named under "Had no state", taken into the
  plan and set to Planned. Measure: `gather.json` gives the feature `state: Unplanned` and
  `had_no_state: true`; `brief.md` names it under "Had no state"; its Feature issue is in the
  plan; and after the write the spine reads `status: Planned` for it and `state-check.json`
  reads `ok: true`.

### Done means

- D1 — the plan check reads ok: each ready feature of each slice the plan holds that is not
  Completed and not Dropped has exactly one Feature issue node under the plan's one epic (or is
  named as skipped or left out), the plan file carries the business intent, the `epic:` mark and the Slices list, and the
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
- D5 — the write guard reads ok: the run changed no file outside the plan file and, in the
  product model, the spine.
  check: { type: field_equals, file: "context/shape-plan/guard-report.json", field: "ok", equals: true }
- D6 — the state check reads ok: each feature the plan takes in reads Planned or kept its
  state, and nothing else in the model changed.
  check: { type: field_equals, file: "context/shape-plan/state-check.json", field: "ok", equals: true }

### Recovery (one per failure condition)

- REC1 (F1) — file the missing Feature issue (or open the closed one again); take a Feature issue that stands for no feature of
  the plan's slices off the epic and out of the plan. Handoff: autonomous.
- REC2 (F2) — keep the first plan, epic or Feature issue, take the copy out of the plan, and tell
  the person which one was kept. Handoff: human.
- REC3 (F3) — take the line out and draft the Feature issue or the epic again from the two ICE
  without the "Fails if" lines. Handoff: autonomous.
- REC4 (F4) — write the plan file's top, tree and the epic's map again from the run's record, so
  they agree. Handoff: autonomous.
- REC5 (F5) — undo each tracker write the record lists, put back the plan file and the spine
  as they were; show the brief again. Handoff: human.
- REC7 (F7) — undo the write outside the allowed set. Handoff: autonomous.
- REC8 (F8) — take back the Feature issue filed, changed or opened again from the feature that
  is not ready, put back its state, skip the feature, and name it in the brief. Handoff:
  autonomous.
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
- REC16 (F16) — take the Completed or Dropped feature's node and map line out of the plan,
  undo any write to its issue, name it under "Built, left out" or "Dropped, left out", read
  the state again from the spine, and name each feature with no state under "Had no state".
  Handoff: autonomous.
- REC17 (F17) — show the closed Feature issue under "Opened again" and ask again; after the yes,
  open the same issue again and put it under the epic; take back a second Feature issue filed
  for the feature. Handoff: human.
- REC18 (F18) — put back the spine as it was at the run's start (the guard's restore), then
  run the state step again from `planned-request.json`, through `product-os-keeper` and
  `link-model-part`, and run the state check again. Handoff: autonomous.
