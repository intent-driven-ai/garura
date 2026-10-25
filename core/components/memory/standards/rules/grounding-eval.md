# Grounding Content-Quality Eval — v2

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
is not trusted). All-pass is the rule for a doc's first round, and for a gate run with
no judge state.

## How the gate settles

A judge reads the same page a little differently each time. Without a memory of its last
verdict, it finds a new point on every round, and the rewrite loop never ends. So the gate
keeps a judge state: one record for each judged doc, in a state folder the play names. The
record holds the fingerprint at the last verdict, whether it passed, the last failures, the
doc's text at that verdict (the snapshot) and the notes.

- **The kept pass.** The fingerprint is a hash of the doc, its parent doc, the guidance the
  judge was given and the judge's own text (the `judge-grounding` skill file, given with
  `--judge`), each kept apart. A pass is kept while all four are the same:
  `grounding_gate.py kept` says so, and the play does not dispatch a judge for that doc
  again. A change to any one of the four ends the kept pass, and the doc is judged again. So
  a stricter judge ends the old passes: a pass given by a looser judge is not kept.
- **The fix round.** When a doc has a record, the next verdict is a fix round.
  `grounding_gate.py prior` gives the last failures, and the play hands them to the judge.
  The judge says, for each one, whether the cited fix was made, with a quote. The gate
  decides, not the judge: a last failure counts as fixed only when the judge says
  `fixed: true`, the doc's text changed since the verdict that failed, and every quote in
  the judge's evidence is found on the page now. Otherwise it fails, and so does a last
  failure the judge does not answer (it fails closed). The judge still scores the five
  criteria, but a new point stops the run only when it rests on text that changed since the
  last verdict.
- **The notes.** A new point is a note when its evidence quotes the doc and every quote is
  found in the snapshot: it is about text that did not change. A note never blocks. The
  record keeps its notes, and `grounding_gate.py kept` prints them too. At the checkpoint
  the play runs `grounding_gate.py notes`, which collects every note in the state (passed
  and kept docs included) into one file, and shows them to the person, who may act on them.
  A new point with no quote, or with a quote not in the snapshot, is a failure.

A missing criterion still fails closed in every round. This is why the judge quotes the
doc's exact text inside straight double quotes: the gate finds each quote in the snapshot to
tell changed text from unchanged text.

## How the judge runs — an isolated sub-agent

The judge ALWAYS runs as an in-harness sub-agent spawned with a CLEAN context: it
runs the `judge-grounding` skill with only the kind's guidance for the doc's own stage (its per-section
guidance, the stage's heading contract and the every-stage agent intent, cut by `guidance_block.py
--stage`; never the gold example) + the doc (+ parent),
never the play's context, the brief, or the author's reasoning. The orchestrator spawns
it; it returns the verdict JSON, which the gate scores. Clean context is what stops
context bleed and reward hacking.

In a fix round the judge also gets its own earlier failures for that doc
(`prior_failures`), and only those. It still gets no brief, no author reasoning and no gold
example. This keeps the clean-context aim: the failures are the judge's own words from its
last verdict, not the author's. They tell the judge what it asked for, not why the author
wrote what they wrote, so they cannot argue a doc through. The gate, not the judge, still
decides whether each fix was made.

Optionally pin a different model for the sub-agent via `grounding-eval.judge.model`
(e.g. `claude-haiku-4-5-20251001`) for extra isolation — different weights judging the
output. Default `inherit` uses the session model. Either way it is a sub-agent running the
same skill and returning the same verdict shape.

## Calibration (how we trust the eval itself)

An untested judge lies. Before the eval gates any real play, it must separate known
answers: run it on the gold grounding docs (must pass) and the deliberately thin docs
(must fail). If it passes a thin doc, the prompt is too lenient — tighten and re-run.
This is the same known-good-passes / known-bad-fails loop the linter was proven with.

A calibration run uses no judge state: every doc is judged fresh, in a first round, with
all-pass. A kept pass or a note would hide what the judge itself says about the doc, and
that is what calibration tests.
