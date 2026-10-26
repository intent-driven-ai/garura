# Questions — #798

Every question /shape-slice asked a person, and every gap it left as an assumption, with the answer. This file only grows (standards/rules/user-questions.md).

```yaml
questions:
- id: Q-builders-1
  kind: asked
  blocking: false
  asked_at: '2026-10-26T06:32:34Z'
  topic: builders
  question: Which plays must the new check treat as build plays, whose inputs may
    never name the evals folder?
  proposed_answer: Every play, skill and agent that builds the software, and every
    context sub-agent it starts, is a build play for the check. Only /shape-slice
    (which writes the hidden file into the evals folder), /shape-eval and the eval
    itself may name the evals folder.
  basis:
    kind: model
    ref: product/product-os/software-delivery-planning/shape-eval/capability.md:4
  pipeline_source: /shape-slice shape-slice-798-898
  pipeline_guess: Every play, skill and agent that builds the software, and every
    context sub-agent it starts, is a build play for the check. Only /shape-slice
    (which writes the hidden file into the evals folder), /shape-eval and the eval
    itself may name the evals folder.
  impact_if_unknown: 'Garura has no build play for an epic yet (that work is business
    intent #819). If the check names only some plays, a play that builds code but
    is not on the list can be handed the eval, and a pass then proves less than the
    intent asks.'
  user_decision: accepted
  user_answer: yes — accepted as proposed
  resolved_at: '2026-10-26T06:52:29Z'
  resolved_by_run: shape-slice-798-898
- id: Q-flag-1
  kind: asked
  blocking: false
  asked_at: '2026-10-26T06:32:34Z'
  topic: flag
  question: Where must the product owner see the flag when a build session read the
    evals folder?
  proposed_answer: null
  basis: null
  pipeline_source: /shape-slice shape-slice-798-898
  pipeline_guess: null
  impact_if_unknown: The check does not block a build; it only makes the read visible.
    If the flag sits where no person looks, the shortcut stays hidden in practice,
    and the product owner trusts an eval pass that the builder could aim at.
  user_decision: in_scope
  user_answer: this gets recorded in evidence. We will build drift checks and evidence
    warnings in Griffin so that will be seen there. For now we should record this
    under evidence.
  resolved_at: '2026-10-26T06:54:02Z'
  resolved_by_run: shape-slice-798-898
- id: Q-proof-1
  kind: asked
  blocking: false
  asked_at: '2026-10-26T06:32:34Z'
  topic: proof
  question: Must the proof line of business intent 788 that says no builder can read
    the eval change to say that no builder is given the eval, with each read flagged?
  proposed_answer: Yes. Change the proof line 'The eval is kept in a place where no
    builder can read it.' to 'No builder is given the eval, and a check flags each
    build session that read the evals folder.'
  basis:
    kind: person
    ref: 798/specs/design.md:7-10
  pipeline_source: /shape-slice shape-slice-798-898
  pipeline_guess: Yes. Change the proof line 'The eval is kept in a place where no
    builder can read it.' to 'No builder is given the eval, and a check flags each
    build session that read the evals folder.'
  impact_if_unknown: 'The product owner dropped encryption: the eval is plain text
    in the repo, so a builder can open it. The intent page still says no builder can
    read it. If the words stay, the eval tests a promise the design no longer keeps,
    and the model and the intent disagree.'
  user_decision: accepted
  user_answer: yes — accepted as proposed
  resolved_at: '2026-10-26T06:52:29Z'
  resolved_by_run: shape-slice-798-898
```
