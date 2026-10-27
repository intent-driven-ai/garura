# Eval format rules

The rules of a slice's eval (ADR 057): its story files (`templates/eval-story.feature.md`) and its slice file
(`templates/eval-slice.md`), kept in the slice's evals folder in its home plan
(`.garura/project/plans/<plan-id>/evals/<slug>/`), and the step library of each surface kind
(`schemas/eval/steps-<kind>.yaml`). `/shape-eval` writes the eval by these rules, and its `check_eval.py` checks them.

## A story file

- One tag line above each `## Scenario:`, in backticks: what the scenario covers. `@goal-<n>` and `@expectation-<n>`
  are the n-th line of the story's "Goals:" and "Expectations:" lists in its "Scope of work" (counted from 1);
  `@F<n>` is a failure condition of the story's feature in the slice's hidden file. A scenario may carry more than one
  tag. It covers nothing else.
- Each step starts with `* ` and is a sentence of the step library, with Given, When, Then, And or But. A value is a
  literal in double quotes, or a name in square brackets for what only the build will make (`[the booking page]`);
  each name is listed in the slice file.
- Each Then is an exact result a tester can see. There is no score: the scenario passes only when every step passes.
- A failure-condition scenario shows that the condition does not happen. The recovery (when, way back, who fixes)
  stays in the hidden file: the story file holds no recovery and no handoff text.
- `## Untestable` lists, one line each with its tag, every goal, expectation or failure condition that has no
  scenario, with the reason. It is prose to a Gherkin parser.
- A story whose feature left the slice keeps its file; its first tag line gains `@out-of-slice`. No scenario of a
  story file is ever changed or deleted by a later run: a later run only adds scenarios and untestable lines.
- `## Lines covered` lists, one line each with its tag, the exact text of each story line (a "Goals:" or
  "Expectations:" line) that a scenario covers, as the story said it when the scenario was written.

## The slice file

- The build order is the order of the epic's feature-to-story map.
- "Out of the slice" is there only when a story file's feature left the slice.
- Every name a story file uses is listed under "Names"; the list holds no name that no story file uses.
- The time limit is a whole number of seconds, more than 0.

## A fixed yardstick (ADR 057)

- A later run of `/shape-eval` never changes or deletes a scenario that is there, and never changes a line of a
  story file's "Lines covered" list. It only adds scenarios, Untestable lines and Lines covered lines for what is not
  covered yet.
- A tag `@goal-<k>` or `@expectation-<k>` points at the story's k-th line by its place. When a story's lists change
  later, a line can move, change or go away. A later run compares each recorded line with the story's line now, and
  names each scenario whose line moved, changed or went away for a person, in its summary and its record. It never
  rewrites the scenario: the person decides whether it still fits.
- A failure condition's tag `@F<n>` is the id the hidden file gives it, which stays with its condition.

## Never in an eval

- No recovery and no handoff text: not "the builder can fix this alone", not "a person must decide", not "Way back:",
  not "Who fixes:", and no recovery line of the hidden file. A phrase quoted in a "does not contain" step checks that
  the phrase is absent, so it does not count.
- No score: the eval passes only when every scenario of every story passes.
