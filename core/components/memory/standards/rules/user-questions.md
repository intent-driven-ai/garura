# Questions a Play Asks a Person

Every question that a play asks a person is a record. The play keeps it, with the answer,
so that the question is not lost and is not asked again.

Consumers: every play and skill that makes an inference it must show to a person.

This rule came from Rule 12 of the old product rules (`product.md`), which was deleted with
the old intent-epic pipeline (ADR 050). The meaning did not change.

## The rule

**Every question that a play asks a person goes into the issue's short-term memory, in
`{stm_base}<issue>/context/grounding-questions.md`. Each question has a unique ID, a place
for the person's answer, and it stays there for all the runs of that issue.**

A play always runs inside an issue (`/discover-domains`, `/discover-capabilities` or any
other play). So its questions and answers go to that issue (ADR 039 §1). They are memory in
short-term memory. Another issue finds them only after a person promotes them.

## Why the rule exists

A run talks with the person, but the talk is not kept. A question that a run shows at a
checkpoint (for example "how many people use it at the same time?", "is sign-in with
another account in scope?", "what is the cost limit?") is only in the prompt text. When the
person replies, the question goes away. If the person says "I do not know", or the session
ends before an answer, the question is lost. The next run asks it again from the start, and
nothing learns.

Questions are knowledge, and knowledge needs a place. A question in the issue's short-term
memory is a record that the person can edit, search and track, and that a person can
promote (ADR 039 §1: every memory write goes to short-term memory first).

## What each entry holds

Each time a run makes an inference (a value or a decision that the person did not give,
but that the run guessed), it adds one entry to the file:

```yaml
- id: Q-<topic>-<sequence>              # unique, the same in every run
  asked_at: <ISO-8601 timestamp>
  topic: scale | rate_limits | feature_count | cost_quota | scope_creep |
         time_windows | agent_budgets | experiment_config | oauth_providers |
         vocabulary | bounded_contexts
  question: "<the question, in plain words>"
  pipeline_source: "<which skill and which field>"
  pipeline_guess: "<what the run guessed, if it guessed>"
  impact_if_unknown: "<what happens if the person does not answer>"
  user_decision: null | in_scope | out_of_scope | deferred | replaced_with
  user_answer: null | "<free text>"
  resolved_at: null | <ISO-8601>
  resolved_by_run: null | <play run id>
  # Optional fields a play may add (/shape-slice writes all four):
  kind: asked | assumption               # asked = shown to the person; assumption = a gap
                                         #   not asked (over the question budget), with the
                                         #   run's written assumption in pipeline_guess
  blocking: true | false                 # true = only the person can answer it; it is
                                         #   always asked, and the run waits for its answer
  proposed_answer: null | "<text>"       # the answer the run proposes — only with a basis
  basis: null | {kind: model | memory | person, ref: "<page and lines, or the question id>"}
                                         # where the proposed answer comes from; a proposed
                                         #   answer with no basis is stripped (no-unbacked-
                                         #   recommendation.md)
```

## How the file is kept

- **It only grows.** A new run in the same issue adds new questions. It does not write over
  the old ones.
- **An answer is a fact.** A question that has `user_decision` and `user_answer` from an
  earlier run of the issue is not asked again. The run uses the answer as a fact.
- **Match by the question, not by the ID alone.** A question counts as already answered
  when its text (in lower case, without punctuation and extra spaces) matches an answered
  entry. A new question that reuses an ID the file already holds for another question gets
  a new ID, so it is asked and kept on its own.
- **Open questions come back.** A question that is `deferred` or `null` is shown again at
  the next checkpoint, until the person answers it.
- **Other issues do not see it.** Another issue does not see these answers until a person
  promotes them to Garura memory. Until then, that issue can ask again. This is correct.
- **Two writers.** The run adds questions. The person answers them in the file (the
  `user_decision` and `user_answer` fields). The run reads the answers on its next run.

## At a checkpoint

When a checkpoint has inferences, its prompt shows every open question from the file, with
the question text and the choices the person has. The person replies in one of three ways:

- **yes**, with answers (in the reply or in the file): the run continues and uses the
  answers as facts.
- **change: defer X and Y**: those questions stay open, the run uses the answers it has,
  and it continues.
- **stop**: the run stops, and the questions wait for the next run.

## What goes in the file

- Numbers that the run guessed (limits, quotas, scale targets, how long a token lasts).
- Decisions about a feature (is X in scope? is Y for a later release?).
- Words to confirm (is this the correct name for the thing?).
- Where one part of the product stops and another starts.
- Choices of an outside service (which sign-in providers?).

## What does not go in the file

- Who the person is, passwords, or personal data. The questions are about product decisions.
- The run's own state (status, evidence, commit IDs). That has its own place.
- Records that a play owns fully (the product model, plans, epics). Those have their own
  place.

## Enforcement

A skill that makes an inference writes the question to the issue's file before it shows the
inference at a checkpoint. A skill must not show an inference that is not in the file. A
check that finds an inference with no matching question (by ID) reports the violation
`uncaptured_inference`.
