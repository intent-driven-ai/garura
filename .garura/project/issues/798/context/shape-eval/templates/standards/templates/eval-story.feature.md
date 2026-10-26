# Eval story file template

The shape of one story file of a slice's eval: `eval.<feature-id>.feature.md`, in the slice's evals folder
(`.garura/project/plans/<plan-id>/evals/<slug>/`), beside the hidden file. One file for each story of the slice's epic.
It is Markdown with Gherkin (Cucumber's `.feature.md` form): a person reads it as a Markdown page, and a Gherkin
parser reads its keyword lines. Its Gherkin `Feature:` is the story, never the slice. Written by `/shape-eval`
(`author-slice-eval`); checked by `/shape-eval`'s `check_eval.py`. It is never run by an agent: each step is a sentence
of the step library of the slice's surface kind (`standards/schemas/eval/steps-<kind>.yaml`), which a runner does
exactly.

## Shape

```markdown
`@story-<story issue>`
# Feature: Story #<story issue> — <story title>

Feature <feature id> of slice <slice id>, epic #<epic issue>. Written by /shape-eval from story #<story issue> and the
slice's hidden file.

## Background:
* Given [<a setup name>] is set up

`@goal-<n>`
## Scenario: <what a tester sees, in plain words>
* When I run "<command>"
* Then the exit code is 0
* And the file "<path>" exists

`@expectation-<n>`
## Scenario: <...>
* ...

`@F<n>`
## Scenario: <the failure condition does not happen, in plain words>
* ...

## Untestable

- `@goal-<n>`: <why it cannot be tested yet>
```

## Rules

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