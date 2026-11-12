# design-eval — ICE source

The clean ICE triple this play is compiled from. Update this and recompile via
fix-play; never hand-edit the compiled SKILL.md.

## Intent

A person names a business intent whose plan /shape-plan made. /design-eval writes the plan's ONE eval, in Gherkin, in the
plan's evals folder: a scenario for each goal and each expectation of the plan's Feature issues, and for each failure
condition in the hidden file of each slice the plan holds a scenario that shows it does not happen. The eval covers
every feature of every slice the plan holds that its Slices list does not mark Dropped, also a feature whose Feature
issue sits under another plan's epic (`held_by`); a dropped slice is left out, and so is a feature whose Feature issue
item in the plan file is Dropped. It reads only the plan's epic (with its feature-to-story map), the Feature issues the map names (their
scope of work and Context guidance) and the hidden file of each slice the plan holds. It never runs the eval. An eval
is a fixed yardstick: a later run never changes a scenario that is there.

### Constraints

- C1 — The run reads only the plan file (its `epic` mark, its Slices list and the status of each Feature issue item in
  its tree), the plan's epic (with its
  feature-to-story map, which maps each feature to its Feature issue), the Feature issues the map names (their scope
  of work and Context guidance; each of type Feature, with the exact line `Represents: <feature id>`), and the hidden
  file of each slice the plan holds (`evals/<slug>/failure-and-recovery.md`, in the folder of the plan for the slice's
  first intent). It never reads an ICE page, the usage guide, the code or the product model.
- C2 — The run writes only the plan's eval, in the plan's evals folder (`plans/<plan-id>/evals/`): one feature file
  for each Feature issue of the map, `eval.<feature-id>.feature.md`, and one plan file, `eval.<plan-id>.md`. Nothing
  in a slice's hidden-file folder, the tracker, the model or anywhere else.
- C3 — Each feature file is Markdown with Gherkin: one Gherkin `Feature:`, which is the Feature issue (never a slice,
  never a story), and its Scenarios with Given / When / Then. Each Then is an exact result a tester can see on the
  slice's surface (a value, a file, a message), so each scenario passes or fails. The plan file has one section for
  each slice the plan holds that is not Dropped, in the order of the plan's Slices list, and each section lists that slice's features in
  its build order (the order of its hidden file's entries), with the slice's surface kind and its time limit; the
  plan file has one pass rule: there is no score; the eval passes only when every scenario of every feature file
  passes.
- C4 — Each scenario is written from the outside: what a tester does on the slice's surface and what they see. When the
  surface is a play, the scenario runs the play on a test project.
- C5 — Every goal and every expectation of each Feature issue, and every failure condition of its feature in the
  hidden file, has at least one scenario, or a line under "Untestable" that says why. Each scenario is tagged with
  what it covers (the Feature issue's line, or the hidden-file entry's condition id), and covers only what the Feature
  issue or its feature's hidden-file entry says.
- C6 — The eval holds no handoff text, and no recovery: the running eval reads those from the hidden file later.
- C7 — An eval is a fixed yardstick. When the plan's eval exists, the run keeps every scenario as it is, adds
  scenarios only for what is not covered yet, and tags the feature file of a feature that left the plan as out of the
  plan, never deleting it.
- C8 — A plan whose epic, any Feature issue of its map, or the hidden file of any slice that is not Dropped is missing
  gets no eval; the run names each missing part and says why. A feature of the map that is in no slice's hidden file,
  or a Feature issue with no Scope of work, no exact `Represents:` line, or a type other than Feature, counts as
  missing. A dropped slice's missing hidden file does not block the eval.
- C9 — Nothing is committed before the product owner's typed yes, at one checkpoint that no config value can skip. The
  person sees a short summary, never the eval itself: for each slice, one line per Feature issue with its counts
  (Scenarios, Goals covered, Expectations covered, Failure conditions covered, Untestable), each untestable item in
  one line with its reason, and where the eval files are. On a later run, the summary shows only what the run adds. A
  stop leaves no file.
- C10 — The run opens its own change with start-work and lands it through commit-work, review-work,
  validate-work and merge-work, on the plan's branch.
- C11 — Plain words (ASD-STE100) and personas; no real person's name.
- C12 — The eval is written to run deterministically, never by an agent: every step of every scenario is a sentence
  from the fixed step library of the surface kind (command line, browser page, mobile app, backend endpoint), and each
  library sentence stands for one exact action or one exact check. Each slice's surface kind comes from its own hidden
  file's Surface line. A feature that sits in two slices of the plan is written once, with the step library and the
  hidden-file entry of the first slice in the Slices list that holds it. A plan with a slice whose surface kind has no
  step library yet gets no eval; the run names the slice and says why.
- C13 — What only the build will make (a command, a page address, a field) is written as a name ("the shape command",
  "the booking page"), never as a guess; the usage guide maps each name to the real thing later. The plan file lists
  every name the eval uses.
- C14 — The eval is bounded: it covers only the plan's features (the lines of its epic's map) that a slice which is not
  Dropped holds. A slice whose status in the plan file's Slices list is Dropped is left out: its features are not
  tested, it gets no section, and a feature that only dropped slices hold gets no feature file (one that a live slice
  also holds is tested through the live slice). A feature whose Feature issue item in the plan file's tree is Dropped
  is left out too (ontology v18: a feature dropped after it joined a plan stays listed there as Dropped, and the
  plan's eval does not test it): it gets no feature file and no line in its slice's section, and the summary names it
  under the reason "dropped from the plan". A feature file a run wrote for it earlier is kept and tagged out of the
  plan, as C7 says for a feature that left the plan. A feature that only Dropped items hold is not a missing part
  under C8 (its Feature issue and its hidden-file entry are not needed) and does not block the eval. Each slice section of the plan file sets a time limit for each scenario (a scenario that runs out of time fails), so the count of
  scenarios and the longest run are known before it runs.
- C15 — No copy of the eval or of a hidden file stays in the run's short-term memory after the run: the drafts, the
  hidden-file copies and the copies of the plan's eval files from before the run are deleted when the eval is
  committed, and after a stop's undo. Only the eval files in the evals folder, and the run's records with no eval
  text, remain.
- C16 — Each feature file records the exact text of each Feature issue line its scenarios cover (a "Lines covered"
  list: the tag and the line as the Feature issue said it). A later run compares each recorded line with the Feature
  issue's line now; for each scenario whose line moved or changed, it names the scenario for a person in the summary
  and in the run's record, and never rewrites or deletes it.

### Failure conditions

- F1 — The run read an ICE page, the usage guide, the code, or any file other than the plan file, the epic, its
  Feature issues and the slices' hidden files.
- F2 — An eval was written outside the plan's evals folder, or the run wrote another file outside its own records.
- F3 — A feature file is not Gherkin a tool can read, its `Feature:` is not its Feature issue, a Then is not an exact
  result a tester can see, or the plan file does not have one section for each slice that lists the slice's features
  in its build order.
- F4 — A goal or an expectation of a Feature issue, or a failure condition of its feature in a hidden file, has no
  scenario and no "Untestable" line.
- F5 — A scenario covers nothing a Feature issue or its feature's hidden-file entry says, or tests from the inside (it
  reads the code or calls the product's parts directly).
- F6 — The eval holds handoff text or a recovery.
- F7 — A later run changed or deleted a scenario that was there.
- F8 — A plan with no epic, a missing Feature issue or a missing hidden file got an eval, or the run did not name what
  is missing.
- F9 — A commit before the yes, or a stop that left a file.
- F10 — The change landed outside the change plays, or on the wrong branch.
- F11 — A page names a real person, or a person cannot follow it.
- F12 — A step is not a sentence of the step library of its slice's surface kind, or a plan with a slice that has no
  library for its surface kind got an eval.
- F13 — A step holds a guessed address, command or field in place of a name, or a name the eval uses is not in the
  plan file's list.
- F14 — A slice section of the plan file has no time limit for its scenarios, the eval covers a feature that is not in
  the plan's map, that only dropped slices hold or whose Feature issue item is Dropped, a dropped slice got a section,
  or a feature that only Dropped items hold blocked the eval.
- F15 — A copy of the eval or of a hidden file stays in the run's short-term memory after the run.
- F16 — A feature file does not record the line text its scenarios cover, or a later run does not name a scenario
  whose Feature issue line moved or changed, or rewrites it.

## Context

- The product model's words, read through the memory tool: the ontology
  (`standards/schemas/product-os/ontology.md`, v18: Plan with its Eval, Hidden files and Usage guides; Epic, one for
  each plan, with its feature-to-story map; Feature issue with its Represents line, Scope of work and Context
  guidance; Q28, Q29, Q31–Q36, Q56, Q57; Feature, its rules: a feature dropped after it joined a slice or a plan
  stays listed there as Dropped, but the plan does not build it and the plan's eval does not test it).
- ADR 068 (each product feature has one Feature issue that names it and holds its scope of work) and ADR 069 (the
  plan is where the product model meets the work: one epic and one eval for each plan; it supersedes ADR 049 and
  ADR 057 and restates what holds from them: plain-text Gherkin that runs with no agent, one file for each Feature
  issue, step libraries, a fixed yardstick, a summary and never the eval). ADR 052 (/design-slice writes the hidden
  file).
- The eval format: the templates `standards/templates/eval-feature.feature.md` and `standards/templates/eval-plan.md`,
  the rules page `standards/rules/eval-format.md`, and the step library of each surface kind,
  `standards/schemas/eval/steps-<kind>.yaml` (the command line first). Cucumber's Markdown with Gherkin
  (`.feature.md`) is the form of a feature file.
- The plan file `.garura/project/plans/<id>.yaml` (its `epic: <n>` mark and its Slices list), the tracker (the epic
  and its Feature issues, read only, through the code-host adapter), and each slice's hidden file
  `.garura/project/plans/<first-intent plan>/evals/<slug>/failure-and-recovery.md`.
- The agent that checks the copies and calls the skill: `evals-engineer`. The skill that writes the eval:
  `author-slice-eval`. `template-manager` hands out the templates, the step library, the approval prompt and the
  close templates.
- The product owner's decisions (2026-10-26, #798): Gherkin, no rubric and no score; the eval runs with no agent, its
  steps from the step library of the surface kind; a short summary at the checkpoint, never the eval; /design-eval
  only writes the eval. And (2026-11-12, #1025): the plan has one eval; one file for each Feature issue, whose
  `Feature:` is the Feature issue; one plan file with one section for each slice; `held_by` features are covered; a
  plan with a missing epic, Feature issue or hidden file gets no eval and is named. And (2026-11-12, #1025): a slice
  whose status in the Slices list is Dropped is left out of the eval; a feature a live slice also holds is still
  tested. And (ontology v18, #1025): a feature whose Feature issue item in the plan file is Dropped is left out of the
  eval; /design-eval reads this from the plan file's tree, never from the model.
- Personas: the product owner (runs /design-eval, reads the summary, types yes); the eval runner, later, which runs the
  eval with no agent through the usage guide; the build, which is never given the eval (#898).

## Expectation

### Success scenarios

- S1 — (product owner, first eval) Given plan 788 with epic #794, its four Feature issues and its slice's hidden file,
  and no eval yet, when the product owner runs /design-eval 788 and types yes, then the plan's evals folder holds four
  feature files and one plan file. Measure: the eval file check reads ok — each feature file parses as Gherkin, its
  `Feature:` names its Feature issue, every goal, expectation and failure condition has a scenario or an
  "Untestable" line, and the plan file's slice section lists the four features in build order.
- S2 — (product owner, run again, nothing changed) Given an eval made by an earlier run and no change to the epic, its
  Feature issues or the hidden files, when the product owner runs /design-eval again, then no file changes. Measure:
  each eval file is byte for byte as it was, and the run's record lists no write.
- S3 — (product owner, the plan changed) Given an eval and a plan whose slice gained one feature (with its Feature
  issue) and lost one, when the product owner runs /design-eval and types yes, then a new feature file is added, the
  feature file of the feature that left is tagged out of the plan and stays, and the plan file lists the features in
  the new order. Measure: the yardstick check reads ok — every scenario that was there is there, word for word.
- S4 — (product owner, a plan not ready) Given a plan whose second slice has no hidden file, when the product owner runs
  /design-eval, then the plan gets no eval and the summary names the slice with the reason. Measure: the record lists
  the plan as not ready with that reason, and its evals folder holds no eval file.
- S5 — (product owner, stop) Given any plan, when the product owner types stop at the checkpoint, then no eval file is
  written. Measure: the write guard shows no change under the plans folder.
- S6 — (product owner, something not testable yet) Given a Feature issue whose goal says a part is not built yet, when
  the product owner runs /design-eval and types yes, then that goal has an "Untestable" line with the reason, and no
  scenario. Measure: the eval file check lists it as not testable yet, and still reads ok.
- S7 — (product owner, a surface with no step library yet) Given a plan with a slice whose surface is a mobile app and
  no mobile step library exists, when the product owner runs /design-eval, then the plan gets no eval and the summary
  names the slice with the reason. Measure: the record lists the plan as not ready (no step library), and its evals
  folder holds no eval file.
- S8 — (product owner, a Feature issue line changed) Given an eval made by an earlier run, and a Feature issue whose
  second goal line was reworded since, when the product owner runs /design-eval, then the summary names the scenario
  tagged with that goal as "its line changed", for a person to judge, and the scenario is word for word as it was.
  Measure: the eval file check lists the scenario under `moved`, and the yardstick check reads ok.
- S9 — (product owner, a plan with two slices) Given a plan with two slices, each with its hidden file, and an epic
  whose map names a Feature issue for each feature of both slices, one of them `held_by` another plan's epic, when
  the product owner runs /design-eval and types yes, then the evals folder holds one feature file for each Feature
  issue, the `held_by` one included, and one plan file with two slice sections. Measure: the eval file check reads ok,
  and the plan file's two sections list each slice's features in build order with each slice's own surface kind.

- S10 — (product owner, a dropped slice) Given a plan with one live slice and one slice its Slices list marks Dropped,
  whose hidden file is missing, and an epic whose map also names a feature that only the dropped slice holds, when the
  product owner runs /design-eval and types yes, then the plan gets its eval with one section, for the live slice, and
  no feature file for the dropped slice's own feature. Measure: the eval file check reads ok, the plan file has no
  section for the dropped slice, and `inputs.json` lists the dropped slice and the feature left out with why.
- S11 — (product owner, a dropped feature) Given a plan with one live slice whose hidden file holds three features,
  and a plan file whose tree marks the Feature issue item of one of them Dropped, and an eval from an earlier run with
  a feature file for it, when the product owner runs /design-eval and types yes, then the plan gets its eval, the
  slice's section lists only the two live features, the earlier feature file stays tagged out of the plan, and the
  summary names the dropped feature under "dropped from the plan". Measure: `inputs.json` reads `ready: true` and
  lists the feature in `left_out` with the why "dropped from the plan", the eval file check and the yardstick check
  read ok, and the feature file carries `@out-of-plan`.

### Done means

- D1 — the eval file check reads ok: every feature file parses as Gherkin with its Feature issue as its `Feature:`,
  every goal, expectation and failure condition is covered or named as untestable, no scenario covers anything else,
  every step is a sentence of its surface kind's step library, every name is listed, and the plan file has one section
  for each slice that lists the slice's features in build order with a time limit.
  check: { type: field_equals, file: "context/design-eval/eval-check.json", field: "ok", equals: true }
- D2 — the product owner's recorded answer is yes.
  check: { type: field_equals, file: "context/design-eval/approval.json", field: "decision", equals: "yes" }
- D3 — the input check reads ok: the skill and the agent were given only the copies of the epic, its Feature issues
  and the hidden files.
  check: { type: field_equals, file: "context/design-eval/inputs-check.json", field: "ok", equals: true }
- D4 — the yardstick check reads ok: no scenario that was there changed or went away.
  check: { type: field_equals, file: "context/design-eval/yardstick-check.json", field: "ok", equals: true }
- D5 — the write guard reads ok: the run changed no file outside the plan's eval files.
  check: { type: field_equals, file: "context/design-eval/guard-report.json", field: "ok", equals: true }
- D6 — the copies are cleared: no draft, no hidden-file copy and no copy of an eval file is left in the run's
  short-term memory.
  check: { type: field_equals, file: "context/design-eval/clear.json", field: "ok", equals: true }

### Recovery (one per failure condition)

- REC1 (F1) — throw away what was made from the wrong input, and make it again from the copies of the epic, its Feature
  issues and the hidden files only. Handoff: autonomous.
- REC2 (F2) — undo each write outside the plan's eval files. Handoff: autonomous.
- REC3 (F3) — write the feature file again as Gherkin, with its Feature issue as its `Feature:` and an exact Then, or
  write the plan file's slice sections again, each with its features in build order. Handoff: autonomous.
- REC4 (F4) — add the missing scenario, or the "Untestable" line with its reason. Handoff: autonomous.
- REC5 (F5) — take out the scenario that covers nothing the Feature issue or the hidden file says, or write it again
  from the outside, on the surface. Handoff: autonomous.
- REC6 (F6) — take out the handoff text or the recovery. Handoff: autonomous.
- REC7 (F7) — put back each scenario that was there, word for word, and add only what is new. Handoff: autonomous.
- REC8 (F8) — take back the eval of the plan that is not ready, and name each missing part in the summary with its
  reason. Handoff: autonomous.
- REC9 (F9) — take the commit back, or undo the writes the stop left; show the summary again. Handoff: human.
- REC10 (F10) — land the change through the change plays, on the plan's branch. Handoff: human.
- REC11 (F11) — rewrite with personas and plain words. Handoff: autonomous.
- REC12 (F12) — write the step again with a sentence of the library; when a slice's surface kind has no library, take
  back the plan's eval and name the slice in the summary. Handoff: autonomous.
- REC13 (F13) — put a name in place of the guess, and add each name to the plan file's list. Handoff: autonomous.
- REC14 (F14) — set the time limit in each slice section of the plan file; take out the feature that is not in the
  plan's map, that only dropped slices hold or whose Feature issue item is Dropped (tag its earlier feature file out
  of the plan), and the section of a dropped slice; and take back the not-ready verdict that a feature only Dropped
  items hold caused. Handoff: autonomous.
- REC15 (F15) — delete the drafts, the hidden-file copies and the copies of the eval files from the run's short-term
  memory, and from its records commit when they were committed. Handoff: autonomous.
- REC16 (F16) — write the Lines covered list with each covered line's exact text; for a line that moved or changed, put
  back the scenario as it was and name it in the summary. Handoff: autonomous.
