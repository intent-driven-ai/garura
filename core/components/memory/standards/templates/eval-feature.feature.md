# Eval feature file template

The shape of one feature file of a plan's eval: `eval.<feature-id>.feature.md`, in the plan's evals folder
(`.garura/project/plans/<plan-id>/evals/`). One file for each Feature issue the plan's epic maps, also one that sits
under another plan's epic (`held_by`). It is Markdown with Gherkin (Cucumber's `.feature.md` form): a person reads it as
a Markdown page, and a Gherkin parser reads its keyword lines. Its Gherkin `Feature:` is the Feature issue, never a
slice and never a story. Written by `/design-eval` (`author-slice-eval`); checked by `/design-eval`'s `check_eval.py`.
It is never run by an agent: each step is a sentence of the step library of the surface kind of the first slice in the
plan that holds the feature (`standards/schemas/eval/steps-<kind>.yaml`), which a runner does exactly.

## Shape

```markdown
`@feature-<Feature issue number>`
# Feature: Feature issue #<Feature issue number> — <Feature issue title>

Feature <feature id> of slice <slice id>, plan <plan id>, epic #<epic issue>. Written by /design-eval from Feature
issue #<Feature issue number> and the slice's hidden file.

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

- `@goal-<n>`: <the Feature issue's goal line, word for word>
- `@expectation-<n>`: <the Feature issue's expectation line, word for word>
```

The rules for this file are in `standards/rules/eval-format.md`.
