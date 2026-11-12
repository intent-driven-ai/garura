# Eval format rules

The rules of a plan's one eval (ADR 069): its feature files (`templates/eval-feature.feature.md`), one for each Feature
issue of the plan's epic, and its plan file (`templates/eval-plan.md`), kept in the plan's evals folder
(`.garura/project/plans/<plan-id>/evals/`), and the step library of each surface kind (`schemas/eval/steps-<kind>.yaml`).
`/design-eval` writes the eval by these rules, and its `check_eval.py` checks them. The eval covers every feature of
every slice the plan holds, also a feature whose Feature issue sits under another plan's epic (`held_by`), and no other.
A slice whose status in the plan file's Slices list is Dropped is left out: it gets no section, and a feature that only
dropped slices hold gets no feature file. A feature that a live slice also holds is tested through the live slice.
A feature whose Feature issue item in the plan file's tree is Dropped is left out too (ontology v18): it gets no feature
file and no line in its slice's section, and a feature file an earlier run wrote for it is kept under "Out of the plan".

## A feature file

- Its Gherkin `Feature:` is the Feature issue (`Feature issue #<n> — <title>`), with the tag `@feature-<n>` above it.
- One tag line above each `## Scenario:`, in backticks: what the scenario covers. `@goal-<n>` and `@expectation-<n>`
  are the n-th line of the Feature issue's "Goals:" and "Expectations:" lists in its "Scope of work" (counted from 1);
  `@F<n>` is a failure condition of the feature's entry in the hidden file. A scenario may carry more than one tag. It
  covers nothing else.
- Each step starts with `* ` and is a sentence of the step library, with Given, When, Then, And or But. A value is a
  literal in double quotes, or a name in square brackets for what only the build will make (`[the booking page]`);
  each name is listed in the plan file.
- Each Then is an exact result a tester can see. There is no score: the scenario passes only when every step passes.
- A failure-condition scenario shows that the condition does not happen. The recovery (when, way back, who fixes)
  stays in the hidden file: the feature file holds no recovery and no handoff text.
- `## Untestable` lists, one line each with its tag, every goal, expectation or failure condition that has no
  scenario, with the reason. It is prose to a Gherkin parser.
- A feature file whose feature left the plan keeps its file; its first tag line gains `@out-of-plan`. No scenario of a
  feature file is ever changed or deleted by a later run: a later run only adds scenarios and untestable lines.
- `## Lines covered` lists, one line each with its tag, the exact text of each Feature issue line (a "Goals:" or
  "Expectations:" line) that a scenario covers, as the Feature issue said it when the scenario was written.
- A feature that sits in two slices of the plan has one file. Its steps come from the step library of the first slice
  in the plan's Slices list that holds it, and its `@F<n>` tags from that slice's hidden-file entry.

## The plan file

- One `## Slice <slice id>` section for each slice the plan holds that is not Dropped, in the order of the plan file's
  Slices list.
- Each slice section has the slice's Surface line, its `Surface kind:` (from its own hidden file), its time limit (a
  whole number of seconds, more than 0) and its features in its build order: the order of the slice's hidden-file
  entries that the epic's map names. A Feature issue that sits under another plan's epic says
  `(held by epic #<n>)`.
- One pass rule for the whole plan.
- "Out of the plan" is there only when a feature file's feature left the plan, or was dropped from it.
- Every name a feature file uses is listed under "Names"; the list holds no name that no feature file uses.

## A fixed yardstick (ADR 069)

- A later run of `/design-eval` never changes or deletes a scenario that is there, and never changes a line of a
  feature file's "Lines covered" list. It only adds scenarios, Untestable lines and Lines covered lines for what is
  not covered yet.
- A tag `@goal-<k>` or `@expectation-<k>` points at the Feature issue's k-th line by its place. When the lists change
  later, a line can move, change or go away. A later run compares each recorded line with the Feature issue's line
  now, and names each scenario whose line moved, changed or went away for a person, in its summary and its record. It
  never rewrites the scenario: the person decides whether it still fits.
- A failure condition's tag `@F<n>` is the id the hidden file gives it, which stays with its condition.

## Never in an eval

- No recovery and no handoff text: not "the builder can fix this alone", not "a person must decide", not "Way back:",
  not "Who fixes:", and no recovery line of a hidden file. A phrase quoted in a "does not contain" step checks that
  the phrase is absent, so it does not count.
- No score: the eval passes only when every scenario of every feature file passes.
