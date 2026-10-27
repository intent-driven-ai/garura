# Eval slice file template

The shape of a slice's eval file: `eval.<slice-id>.md`, in the slice's evals folder
(`.garura/project/plans/<plan-id>/evals/<slug>/`). It puts the slice's story files (`eval-story.feature.md`) together
in the slice's build order. It holds no scenario of its own. Written by `/shape-eval`; checked by its `check_eval.py`.

## Shape

```markdown
# Eval: slice <slice id> — epic #<epic issue>

Plan <plan id>, business intent "<intent title>" (#<intent issue>).
Surface: <the hidden file's Surface line>
Surface kind: <kind of the step library, for example command-line>
Time limit for each scenario: <n> seconds
Written by /shape-eval from epic #<epic issue>, its stories and the slice's hidden file.

## Pass rule

The eval passes only when every scenario of every story below passes. There is no score. A scenario that runs past the
time limit fails.

## Stories, in build order

1. Story #<n> (<feature id>) — eval.<feature id>.feature.md
2. ...

## Out of the slice

- Story #<n> (<feature id>) — eval.<feature id>.feature.md: its feature left the slice; kept, not run.

## Names

The usage guide (`guides/<slug>.md`) maps each name to the real thing the build made.

- [<a name>]: <what it is, in plain words>

## Context

From the stories' Context guidance: what to read, what never to read, the persona, what is in and what is out.

- <one line each>
```

The rules for this file are in `standards/rules/eval-format.md`.