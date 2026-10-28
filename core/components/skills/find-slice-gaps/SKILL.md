---
name: find-slice-gaps
description: List each thing a slice needs that neither the product model nor memory answers, for /shape-slice, and write each as one question by the rule for asking a person — id, topic, question (one thing), why, examples from several domains, blocking, assume, and settled with its basis when the context answers it after all. The surface and the tester are never a question (author-slice proposes them). Rewrite mode rewrites only the questions that record_questions.py proposals refuses. Reads only what its agent put in short-term memory; writes questions.json only. Generative artifact production for /shape-slice. Use when /shape-slice needs the gaps of a slice written as questions, or some of them rewritten.
user-invocable: false
model: opus
allowed-tools: Read, Write
---

# find-slice-gaps

/shape-slice asks a person only what the model and memory cannot answer. This skill finds
those gaps for one business intent and writes each as a question a person can answer with no
other text open. It does not find the model's loose links (that is `find-model-gaps`, used by
the loops); it finds what this one slice needs.

## Input

| Field | Required | Meaning |
|-------|----------|---------|
| `mode` | no | `find` (the default) or `rewrite` |
| `intent_page` | yes | The business intent's page in the model |
| `gather` | yes | `gather.json`: each model page and memory line the agent read (tier, path, lines, fingerprint), with the short-term copies |
| `placement` | yes | The `find-work-placement` routing result for the intent's outcome |
| `record` | yes | The question record (`grounding-questions.md`): a question answered there is a fact and is never asked again |
| `asking_rule` | yes | The shared rule for asking a person, `_shared/asking-a-person.md`, beside the installed skills (`../_shared/asking-a-person.md` from this skill's folder); it is not memory. When `gather` has `rule_missing`, use the floor below |
| `skill_gaps` | no | Gaps that other skills returned as data (for example an `enrich-capability-ice` manifest's `gaps`) on an earlier round |
| `questions` | for `rewrite` | `questions.json` as it is |
| `problems` | for `rewrite` | `questions-checked.json` `shape_problems`: each refused question id with what is wrong |
| `out` | yes | Where to write `questions.json` |

## Process

### Find mode

1. **List what the slice needs.** From the intent's outcome, proof and must-not, and the
   placement, list each fact the slice cannot be shaped or built without: who may do what,
   which rule holds, how big it gets, what counts as done.
2. **Look for each fact in the context.** Look in `gather` (the model pages and the memory
   lines) and in `record`. When the context answers it, the fact is not a gap. When the
   context answers it only after a closer read, write the question with `settled: true` and
   its `basis` `{kind: model|memory|person, ref: <page and lines, or the question id>}`; the
   script moves it out, and it is never asked.
3. **Leave out the surface and the tester.** An intent does not depend on a surface, so the
   surface and the tester are never a gap: `author-slice` proposes them, and the person sees
   them in the brief.
4. **Write each gap as one question,** by `asking_rule`:
   - `id` — `Q-<topic>-<n>`, unique in the record;
   - `topic` — one plain word for what it is about;
   - `question` — asks one thing, with one question mark, and stands alone: it names the
     thing it is about and points to no other text ("above", "the previous");
   - `why` — what goes wrong if the answer is wrong;
   - `examples` — two or more example answers, each from a different domain, so the answer
     is not pulled into one field;
   - `blocking` — `true` only when the slice cannot be shaped without the answer and no one
     but the person can give it; else `false`;
   - `assume` — what the run assumes when the question is not asked (the budget may leave it
     out); never empty.
5. **Take the gaps other skills returned** (`skill_gaps`) and write each the same way.

### Rewrite mode

Rewrite only the questions that `problems` names, so each passes the shape: one thing, one
question mark, stands alone, a `why`, two or more examples. Keep the id, the topic, the
`blocking` value and the `assume` text. Keep every other question byte for byte.

### The floor, when the rule is missing

One thing per question; the parts Question, Answer, Why it matters and Example; examples from
several domains; each question stands alone; plain words; personas.

## Output

`questions.json`, a JSON list:

```json
[{"id": "Q-payment-1", "topic": "payment", "blocking": true,
  "question": "Must a patient pay before a booking is kept?",
  "why": "A slot kept with no payment can stay empty, and the clinic loses the visit.",
  "examples": ["a clinic: pay at the desk after the visit",
               "a shop: pay before the order is sent",
               "a library: no payment, the loan is free"],
  "assume": "A patient pays at the desk after the visit.",
  "settled": false, "basis": null}]
```

## Rules

- Never a question the model, memory or the record answers; mark it `settled` with its basis.
- Never a question about the surface or the tester.
- Each question asks one thing, stands alone, and has a why, two or more examples from
  different domains, `blocking` and `assume`.
- Never a proposed answer: `propose-answers` drafts those, from a named source only.
- Write `questions.json` only; never the record, the model or the brief.
- Plain words (ASD-STE100), personas only, no real names.
