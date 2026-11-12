# Eval plan file template

The shape of a plan's eval file: `eval.<plan-id>.md`, in the plan's evals folder (`.garura/project/plans/<plan-id>/evals/`).
A plan has one eval (ADR 069). This file puts the plan's feature files (`eval-feature.feature.md`, one for each Feature
issue of the plan's epic) together: one section for each slice the plan holds, in the order of the plan file's Slices
list, each with that slice's surface kind, its time limit and its features in its build order. It holds no scenario of
its own. Written by `/design-eval`; checked by its `check_eval.py`.

## Shape

```markdown
# Eval: plan <plan id> — epic #<epic issue>

Business intent "<intent title>" (#<plan id>).
Written by /design-eval from epic #<epic issue>, its Feature issues and the hidden file of each slice the plan holds.

## Pass rule

The eval passes only when every scenario of every feature file below passes. There is no score. A scenario that runs
past the time limit of its slice fails.

## Slice <slice id>

Surface: <the Surface line of this slice's hidden file>
Surface kind: <kind of the step library, for example command-line>
Time limit for each scenario: <n> seconds

Features, in build order:

1. Feature issue #<n> (<feature id>) — eval.<feature id>.feature.md
2. Feature issue #<n> (<feature id>) — eval.<feature id>.feature.md (held by epic #<other plan's epic>)

## Slice <next slice id>

Surface: ...
Surface kind: ...
Time limit for each scenario: <n> seconds

Features, in build order:

1. ...

## Out of the plan

- Feature issue #<n> (<feature id>) — eval.<feature id>.feature.md: its feature left the plan; kept, not run.

## Names

The usage guides (in the plan's `guides/` folder) map each name to the real thing the build made.

- [<a name>]: <what it is, in plain words>

## Context

From the Feature issues' Context guidance: what to read, what never to read, the persona, what is in and what is out.

- <one line each>
```

The rules for this file are in `standards/rules/eval-format.md`.
