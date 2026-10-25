---
name: judge-grounding
description: Grade ONE product-model grounding doc (a domain.md, capability.md, feature.md or epic) for whether a stranger could understand it, and write the verdict JSON. It holds the grounding judge's rubric (five criteria), its prompt and its verdict shape — the one source for them (ADR 039 §7). It runs inside an isolated, clean-context judge sub-agent that is handed only the doc, its parent doc when there is one, and the kind's per-section guidance (and, in a fix round, the last verdict's failures); it never sees the brief or the author's reasoning. It only scores and evidences each criterion; the deterministic gate (grounding_gate.py, all-pass) decides pass or fail. Use when a play's content-quality eval judges a grounding doc it wrote.
user-invocable: false
model: sonnet
allowed-tools: Read, Write
---

# judge-grounding

The linter (`lint_grounding.py`) proves a grounding doc has the right *shape*. This skill
judges whether the *content* is understandable — the judgment a script cannot make. It is an
LLM-as-judge: a second model reads the doc and scores it against the bar in the grounding
content standard (`standards/schemas/product-os/grounding/_content-standard.md`).

This skill is the one source for the rubric, the judge prompt and the verdict shape. A play
does not restate them, and does not read them from memory: it dispatches a judge sub-agent,
and the sub-agent runs this skill.

## Input

The doc, its parent when there is one, and the kind's guidance for the doc's own stage — and only these
(plus, in a fix round, the last verdict's failures, and where to write the verdict):

| Field | Required | Description |
|-------|----------|-------------|
| `doc` | yes | The grounding doc under test (the file the play wrote this run). |
| `parent_doc` | no | Its parent: a capability's domain, a feature's capability. Only for `depth_gradient`. |
| `guidance` | yes | The kind's guidance for the doc's own stage — its per-section guidance, the stage's heading contract and the every-stage agent intent, cut from the kind's template by the play's `guidance_block.py --stage` (never the gold example), as `template-manager` put it in the issue's short-term memory. |
| `kind` | yes | `domain`, `capability`, `feature` or `epic`. |
| `prior_failures` | no | Only in a fix round: the failures of the last verdict on this doc, each `{"id", "evidence", "fix"}`. The play gets them from `grounding_gate.py prior`, which prints `{"round": "first"\|"fix", "prior_failures": [...]}`, and hands the list over only when `round` is `fix`. |
| `out_verdict` | yes | Where to write the verdict JSON. |

The guidance tells the judge what each section is *meant* to hold, so it judges a section
against its intended depth, not an invented one. The judge is NOT given the template's gold
example: handing it the answer turns judgment into pattern-matching.

Calibration finding (v1): without the section guidance, a skeptical judge over-penalizes
sections that are brief on purpose. For example, it demands a "why" on every feature
line when a capability's Features section is by design a brief linked index (the
detail lives in the child docs). Or it asks a feature to be written as a user story,
when our rules say a feature is a function, not a story. The guidance closes that gap.

## Process

### What the judge scores (5 criteria)

Link integrity is NOT here — it is mechanical, and the linter already does it. The judge
scores meaning:

1. **completeness** — every required section is substantive, not a placeholder.
2. **self_explanation** — each item carries the *why* or the implication, not just the
   *what*. "Local fixtures only" fails; the version that says *why* passes.
3. **discreteness_form** — discrete points, not flowing story-prose; Agile forms where
   required (acceptance as Given/When/Then; a feature states the function's behavior,
   never "as a user I want…").
4. **depth_gradient** — detail INCREASES from parent to child. Judged only when the parent
   doc is supplied (capability vs its domain, feature vs its capability); `na`
   otherwise (a domain has no parent; an epic is a delivery overlay).
5. **stranger_test** — the overall gate: a cold reader with no prior context can explain the
   node's *what*, *why*, and *edges* from this doc alone.

### The judge prompt

Judge the doc as this prompt says:

> You are a skeptical reviewer grading ONE product-model grounding doc for whether a
> stranger could understand it. You see the doc (and its parent doc if provided) and the
> guidance for this doc kind at its stage, which tells you what each section is meant to
> hold — judge each section against THAT, not against an expectation you invent. You do
> NOT see the brief that produced it or any author reasoning — if you find yourself
> filling in understanding the doc does not state, that is the doc failing, not you.
> Default every criterion to **fail** unless the doc clearly earns a pass.
>
> Score each criterion below for the doc. For each, return: the verdict
> (pass | fail | na), the exact text you judged (quote it word for word, inside straight
> double quotes), and — if not a pass — the
> concrete change that would make it pass. Be specific; "improve wording" is not a fix.
>
> Criteria (definitions above): completeness, self_explanation, discreteness_form,
> depth_gradient (na unless a parent doc is given), stranger_test.
>
> Return ONLY a JSON object in the verdict shape. No prose outside the JSON.

Read only `doc`, `parent_doc` and `guidance`, and use `prior_failures` when it is given. Do
not open the brief, other docs, or memory.

### Quote the doc exactly

Every `evidence` quotes the doc's exact text inside straight double quotes (`"…"`), so the
gate can find it in the doc. Copy the words as they stand; do not reword them. To cite
several places, give several quotes and join them with a space. To skip words inside one
quote, use `...`. A pass quotes too.

### A fix round: check the prior failures

The play reads `grounding_gate.py prior` first. Its output has this shape:

```json
{"round": "first|fix", "prior_failures": [{"id": "<criterion>", "evidence": "<quote>", "fix": "<fix>"}]}
```

When `round` is `first`, the play hands no `prior_failures`, and the doc is judged as above,
with no `prior` in the verdict. When `round` is `fix`, the play hands `prior_failures`.

When `prior_failures` is given, the doc was judged before and rewritten against those
fixes. Then also write `prior`: one entry for each prior failure, with its `id`, `fixed`
(`true` when the cited fix was made, `false` when it was not) and `evidence`, a quote of the
doc's text that shows it. Say only whether that fix was made; do not judge the point again
from the start. Your `fixed: true` is a claim, not the decision: the gate counts the fix as
made only when the doc changed and your quote is on the page now.

Still score all five criteria. A new point you raise is judged by the gate: on text that
changed, it stops the run; on text that did not change, it is a note the person sees at the
checkpoint. So quote the exact text the point rests on.

## Output

Write exactly this shape to `out_verdict`, and nothing else:

```json
{
  "doc": "<path>",
  "kind": "domain|capability|feature|epic",
  "criteria": [
    {"id": "completeness",      "verdict": "pass|fail|na", "evidence": "<quote>", "fix": "<concrete fix or empty>"},
    {"id": "self_explanation",  "verdict": "pass|fail|na", "evidence": "<quote>", "fix": ""},
    {"id": "discreteness_form", "verdict": "pass|fail|na", "evidence": "<quote>", "fix": ""},
    {"id": "depth_gradient",    "verdict": "pass|fail|na", "evidence": "<quote>", "fix": ""},
    {"id": "stranger_test",     "verdict": "pass|fail|na", "evidence": "<quote>", "fix": ""}
  ],
  "prior": [
    {"id": "<id of a prior failure>", "fixed": true, "evidence": "<quote>"}
  ]
}
```

`prior` is there only in a fix round (when `prior_failures` was given), with one entry for
each prior failure. In a first round, leave it out.

The judge does NOT decide overall pass or fail. It only scores and evidences. The gate decides,
so the judge cannot wave a doc through with a self-declared "overall: pass". The gate rule —
all-pass over the five criteria in a first round, failing closed on a missing criterion, and
how a fix round and a kept pass settle — is in `standards/rules/grounding-eval.md`, run by
each play's `grounding_gate.py`.

## Boundaries

- Writes only `out_verdict`.
- Never sees the play's context, the brief, or the author's reasoning: clean context is what
  stops context bleed and reward hacking.
- Never fixes the doc. The play's rewrite loop does, from the `fix` fields.
