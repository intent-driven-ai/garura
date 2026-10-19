# Grounding Content-Quality Eval — v1

The linter (`lint_grounding.py`) proves a grounding doc has the right *shape*. This
eval proves the *content is actually understandable* — the judgment a script cannot
make. It is an **LLM-as-judge**: a second model reads the doc and scores it against
the bar in `standards/schemas/product-os/grounding/_content-standard.md`. The play
runs it after the linter passes; a fail sends the doc back to be rewritten against the
cited fixes, then re-judged.

The rubric (five criteria), the judge prompt and the verdict shape live in one place: the
`judge-grounding` skill (ADR 039 §7). The judge prompt is part of judging, not of a play. A
play does not restate them and does not read them here: it dispatches a judge sub-agent, and
the sub-agent runs `judge-grounding`. This file keeps the gate rule, how the judge runs, and
how the eval itself is trusted.

The five criteria, by name only: `completeness`, `self_explanation`, `discreteness_form`,
`depth_gradient` (`na` without a parent doc) and `stranger_test`. Their definitions are in
the skill.

## The gate rule

`grounding_gate.py` reads the verdict and applies **all-pass**: the doc passes iff
every one of the five criteria is `pass` or `na`. Any `fail` rejects the doc, and the
gate prints each failing criterion with its evidence and fix for the rewrite loop. A
verdict missing any of the five criteria fails closed (a judge that drops a criterion
is not trusted).

## How the judge runs — an isolated sub-agent

The judge ALWAYS runs as an in-harness sub-agent spawned with a CLEAN context: it
runs the `judge-grounding` skill with only the kind's per-section guidance + the doc (+ parent),
never the play's context, the brief, or the author's reasoning. The orchestrator spawns
it; it returns the verdict JSON, which the gate scores. Clean context is what stops
context bleed and reward hacking.

Optionally pin a different model for the sub-agent via `grounding-eval.judge.model`
(e.g. `claude-haiku-4-5-20251001`) for extra isolation — different weights judging the
output. Default `inherit` uses the session model. Either way it is a sub-agent running the
same skill and returning the same verdict shape.

## Calibration (how we trust the eval itself)

An untested judge lies. Before the eval gates any real play, it must separate known
answers: run it on the gold grounding docs (must pass) and the deliberately thin docs
(must fail). If it passes a thin doc, the prompt is too lenient — tighten and re-run.
This is the same known-good-passes / known-bad-fails loop the linter was proven with.
