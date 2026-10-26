# shape-eval — ICE source

The clean ICE triple this play is compiled from. Update this and recompile via
edit-play; never hand-edit the compiled SKILL.md.

## Intent

A person names a business intent whose plan /shape-plan made. /shape-eval writes, for each slice the plan holds, the
slice's one eval, in Gherkin, in the slice's evals folder: a scenario for each goal and each expectation of the slice's
stories, and for each failure condition in the slice's hidden file a scenario that shows it does not happen. It reads
only the epic, its stories and the hidden file. It never runs the eval. An eval is a fixed yardstick: a later run never
changes a scenario that is there.

### Constraints

- C1 — The run reads only the epic of each slice (with its feature-to-story map), the stories in that epic, and the
  slice's hidden file. It never reads an ICE page, the usage guide, the code or the product model.
- C2 — The run writes only the slice's eval, in the slice's evals folder in its home plan
  (`plans/<plan-id>/evals/<slug>/`), beside the hidden file: one story file for each story of the epic,
  `eval.<feature-id>.feature.md`, and one slice file, `eval.<slice-id>.md`. Nothing in the tracker, the model or
  anywhere else.
- C3 — Each story file is Markdown with Gherkin: one Gherkin `Feature:`, which is the story (never the slice), and its
  Scenarios with Given / When / Then. Each Then is an exact result a tester can see on the slice's surface (a value, a
  file, a message), so each scenario passes or fails. The slice file lists the stories in the slice's build order, with
  the surface, the tester and the pass rule: there is no score; the eval passes only when every scenario of every story
  passes.
- C4 — Each scenario is written from the outside: what a tester does on the slice's surface and what they see. When the
  surface is a play, the scenario runs the play on a test project.
- C5 — Every goal and every expectation of each story, and every failure condition in the hidden file, has at least one
  scenario, or a line under "Untestable" that says why. Each scenario is tagged with what it covers (the story, or
  the hidden-file entry and the condition's id), and covers only what a story or the hidden file says.
- C6 — The eval holds no handoff text, and no recovery: the running eval reads those from the hidden file later.
- C7 — An eval is a fixed yardstick. When a slice's eval exists, the run keeps every scenario as it is, adds scenarios
  only for what is not covered yet, and tags the scenarios of a feature that left the slice as out of the slice, never
  deleting them.
- C8 — A slice whose epic, stories or hidden file is missing gets no eval; the run names it and says why.
- C9 — Nothing is committed before the product owner's typed yes, at one checkpoint that no config value can skip. The
  person sees a short summary, never the eval itself: for each slice, one line per story with its counts (Scenarios,
  Goals covered, Expectations covered, Failure conditions covered, Untestable), each untestable item in one line with
  its reason, and where the eval files are. On a later run, the summary shows only what the run adds. A stop leaves no
  file.
- C10 — The run opens its own change with start-change and lands it through commit-change, propose-change,
  check-change and merge-change, on the plan's branch.
- C11 — Plain words (ASD-STE100) and personas; no real person's name.
- C12 — The eval is written to run deterministically, never by an agent: every step of every scenario is a sentence
  from the fixed step library of the slice's surface kind (command line, browser page, mobile app, backend endpoint),
  and each library sentence stands for one exact action or one exact check. The surface kind comes from the hidden
  file's Surface line. A slice whose surface kind has no step library yet gets no eval; the run names it and says why.
- C13 — What only the build will make (a command, a page address, a field) is written as a name ("the shape command",
  "the booking page"), never as a guess; the usage guide maps each name to the real thing later. The slice file lists
  every name the eval uses.
- C14 — The eval is bounded: it covers only its own slice's stories, and the slice file sets a time limit for each
  scenario (a scenario that runs out of time fails), so the count of scenarios and the longest run are known before
  it runs.
- C15 — No copy of the eval or of the hidden file stays in the run's short-term memory after the run: the drafts, the
  hidden-file copy and the copies of the slice's eval files from before the run are deleted when the eval is committed,
  and after a stop's undo. Only the eval files in the evals folder, and the run's records with no eval text, remain.
- C16 — Each story file records the exact text of each story line its scenarios cover (a "Lines covered" list: the tag
  and the line as the story said it). A later run compares each recorded line with the story's line now; for each
  scenario whose line moved or changed, it names the scenario for a person in the summary and in the run's record, and
  never rewrites or deletes it.

### Failure conditions

- F1 — The run read an ICE page, the usage guide, the code, or any file other than the epic, its stories and the
  hidden file.
- F2 — An eval was written outside the slice's evals folder, or the run wrote another file outside its own records.
- F3 — A story file is not Gherkin a tool can read, its `Feature:` is not its story, a Then is not an exact result a
  tester can see, or the slice file does not list every story in the slice's build order.
- F4 — A goal or an expectation of a story, or a failure condition in the hidden file, has no scenario and no
  "Untestable" line.
- F5 — A scenario covers nothing a story or the hidden file says, or tests from the inside (it reads the code or calls
  the product's parts directly).
- F6 — The eval holds handoff text or a recovery.
- F7 — A later run changed or deleted a scenario that was there.
- F8 — A slice with no epic, stories or hidden file got an eval, or the run did not name it.
- F9 — A commit before the yes, or a stop that left a file.
- F10 — The change landed outside the change plays, or on the wrong branch.
- F11 — A page names a real person, or a person cannot follow it.
- F12 — A step is not a sentence of the step library of the slice's surface kind, or a slice with no library for its
  surface kind got an eval.
- F13 — A step holds a guessed address, command or field in place of a name, or a name the eval uses is not in the
  slice file's list.
- F14 — The slice file has no time limit for its scenarios, or the eval covers a story that is not in its slice.
- F15 — A copy of the eval or of the hidden file stays in the run's short-term memory after the run.
- F16 — A story file does not record the line text its scenarios cover, or a later run does not name a scenario whose
  story line moved or changed, or rewrites it.

## Context

- The product model's words, read through the memory tool: the ontology
  (`standards/schemas/product-os/ontology.md`, v12: Slice with its Eval, Hidden file and Usage guide; Epic with its
  feature-to-story map; Story with its Scope of work and Context guidance; Q28, Q29, Q31, Q35, Q36).
- ADR 049 (the shaping loop: /shape-slice, then /shape-plan, then /shape-eval; where the eval, the hidden file and the
  usage guide live; how the ICE reaches the eval: through the stories and the hidden file, so each line of an ICE has
  one reading) and ADR 052 (/shape-slice writes the hidden file).
- The eval format (#798): the templates `standards/templates/eval-story.feature.md` and
  `standards/templates/eval-slice.md`, and the step library of each surface kind,
  `standards/schemas/eval/steps-<kind>.yaml` (the command line first). Cucumber's Markdown with Gherkin
  (`.feature.md`) is the form of a story file.
- The plan file `.garura/project/plans/<id>.yaml` (its epic nodes, `represents: <slice id>`), the tracker (the epic and
  its stories, read only, through the code-host adapter), and the slice's hidden file
  `.garura/project/plans/<id>/evals/<slug>/failure-and-recovery.md`.
- The agent that checks the copies and calls the skill: `evals-engineer`. The skill that writes the eval:
  `author-slice-eval` (new). `template-manager` hands out the templates, the step library, the approval prompt and the
  close templates.
- The product owner's decisions (2026-10-26, #798): Gherkin, no rubric and no score; the eval runs with no agent, its
  steps from the step library of the slice's surface kind; the layout (one story file per story, its `Feature:` is the
  story; one slice file); a short summary at the checkpoint, never the eval; /shape-eval only writes the eval.
- Personas: the product owner (runs /shape-eval, reads the summary, types yes); the eval runner, later, which runs the
  eval with no agent through the usage guide; the build, which is never given the eval (#898).

## Expectation

### Success scenarios

- S1 — (product owner, first eval) Given plan 788 with epic #794, its four stories and the slice's hidden file, and no
  eval yet, when the product owner runs /shape-eval 788 and types yes, then the evals folder holds four story files
  and one slice file. Measure: the eval file check reads ok — each story file parses as Gherkin, its `Feature:` names its
  story, every goal, expectation and failure condition has a scenario or an "Untestable" line, and the slice file
  lists the four stories in build order.
- S2 — (product owner, run again, nothing changed) Given an eval made by an earlier run and no change to the epic, its
  stories or the hidden file, when the product owner runs /shape-eval again, then no file changes. Measure: each eval
  file is byte for byte as it was, and the run's record lists no write.
- S3 — (product owner, the slice changed) Given an eval and a slice that gained one feature (with its story) and lost
  one, when the product owner runs /shape-eval and types yes, then a new story file is added, the story file of the
  feature that left is tagged out of the slice and stays, and the slice file lists the stories in the new order.
  Measure: the yardstick check reads ok — every scenario that was there is there, word for word.
- S4 — (product owner, a slice not ready) Given a plan whose second slice has no epic yet, when the product owner runs
  /shape-eval, then that slice gets no eval and the summary names it with the reason. Measure: the record lists the
  slice as skipped with its reason, and its evals folder holds no eval file.
- S5 — (product owner, stop) Given any plan, when the product owner types stop at the checkpoint, then no eval file is
  written. Measure: the write guard shows no change under the plans folder.
- S6 — (product owner, something not testable yet) Given a story whose goal says a part is not built yet, when the
  product owner runs /shape-eval and types yes, then that goal has an "Untestable" line with the reason, and no
  scenario. Measure: the eval file check lists it as not testable yet, and still reads ok.
- S7 — (product owner, a surface with no step library yet) Given a slice whose surface is a mobile app and no mobile
  step library exists, when the product owner runs /shape-eval, then that slice gets no eval and the summary names it
  with the reason. Measure: the record lists the slice as skipped (no step library), and its evals folder holds no eval
  file.

- S8 — (product owner, a story line changed) Given an eval made by an earlier run, and a story whose second goal line was
  reworded since, when the product owner runs /shape-eval, then the summary names the scenario tagged with that goal as
  "its story line changed", for a person to judge, and the scenario is word for word as it was. Measure: the eval file
  check lists the scenario under `moved`, and the yardstick check reads ok.

### Done means

- D1 — the eval file check reads ok: every story file parses as Gherkin with its story as its `Feature:`, every goal,
  expectation and failure condition is covered or named as untestable, no scenario covers anything else, every step is
  a sentence of the surface kind's step library, every name is listed, and the slice file lists every story in build
  order with a time limit.
  check: { type: field_equals, file: "context/shape-eval/eval-check.json", field: "ok", equals: true }
- D2 — the product owner's recorded answer is yes.
  check: { type: field_equals, file: "context/shape-eval/approval.json", field: "decision", equals: "yes" }
- D3 — the input check reads ok: the skill and the agent were given only the copies of the epic, its stories and the
  hidden file.
  check: { type: field_equals, file: "context/shape-eval/inputs-check.json", field: "ok", equals: true }
- D4 — the yardstick check reads ok: no scenario that was there changed or went away.
  check: { type: field_equals, file: "context/shape-eval/yardstick-check.json", field: "ok", equals: true }
- D5 — the write guard reads ok: the run changed no file outside the slices' eval files.
  check: { type: field_equals, file: "context/shape-eval/guard-report.json", field: "ok", equals: true }
- D6 — the copies are cleared: no draft, no hidden-file copy and no copy of an eval file is left in the run's
  short-term memory.
  check: { type: field_equals, file: "context/shape-eval/clear.json", field: "ok", equals: true }

### Recovery (one per failure condition)

- REC1 (F1) — throw away what was made from the wrong input, and make it again from the copies of the epic, its stories
  and the hidden file only. Handoff: autonomous.
- REC2 (F2) — undo each write outside the slice's eval files. Handoff: autonomous.
- REC3 (F3) — write the story file again as Gherkin, with its story as its `Feature:` and an exact Then, or write the
  slice file's list again in build order. Handoff: autonomous.
- REC4 (F4) — add the missing scenario, or the "Untestable" line with its reason. Handoff: autonomous.
- REC5 (F5) — take out the scenario that covers nothing the story or the hidden file says, or write it again from the
  outside, on the surface. Handoff: autonomous.
- REC6 (F6) — take out the handoff text or the recovery. Handoff: autonomous.
- REC7 (F7) — put back each scenario that was there, word for word, and add only what is new. Handoff: autonomous.
- REC8 (F8) — take back the eval of the slice that is not ready, and name it in the summary with its reason. Handoff:
  autonomous.
- REC9 (F9) — take the commit back, or undo the writes the stop left; show the summary again. Handoff: human.
- REC10 (F10) — land the change through the change plays, on the plan's branch. Handoff: human.
- REC11 (F11) — rewrite with personas and plain words. Handoff: autonomous.
- REC12 (F12) — write the step again with a sentence of the library; when the slice's surface kind has no library,
  take back its eval and name it in the summary. Handoff: autonomous.
- REC13 (F13) — put a name in place of the guess, and add each name to the slice file's list. Handoff: autonomous.
- REC14 (F14) — set the time limit in the slice file, and take out the story that is not in the slice. Handoff:
  autonomous.
- REC15 (F15) — delete the drafts, the hidden-file copy and the copies of the eval files from the run's short-term
  memory, and from its records commit when they were committed. Handoff: autonomous.
- REC16 (F16) — write the Lines covered list with each covered line's exact text; for a line that moved or changed, put
  back the scenario as it was and name it in the summary. Handoff: autonomous.
