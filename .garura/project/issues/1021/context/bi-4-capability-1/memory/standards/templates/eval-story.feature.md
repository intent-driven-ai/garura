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

## Lines covered

- `@goal-<n>`: <the story's goal line, word for word>
- `@expectation-<n>`: <the story's expectation line, word for word>
```

The rules for this file are in `standards/rules/eval-format.md`.