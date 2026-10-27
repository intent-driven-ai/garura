# Questions — #844

Every question /shape-slice asked a person, and every gap it left as an assumption, with the answer. This file only grows (standards/rules/user-questions.md).

```yaml
questions:
- id: Q-intent-1
  kind: asked
  blocking: true
  asked_at: '2026-10-24T04:20:00Z'
  topic: intent
  question: Is the drafted page for business intent bi-788 confirmed as the product
    owner's own intent?
  proposed_answer: null
  basis: null
  pipeline_source: /shape-slice shape-slice-844-1
  pipeline_guess: null
  impact_if_unknown: The page is at stage proposed, and the ready rule says a node
    that serves only a proposed intent is not ready; the intent itself says no ICE
    that is not ready is shaped, so every part this slice adds stays blocked until
    a person confirms the page.
  user_decision: in_scope
  user_answer: yes — "The proposal of slice is accepted." (with the title "Agents
    design a named piece of work"; the proof line becomes "each of the three plays
    ends at one confirmation by the product owner")
  resolved_at: '2026-10-24T05:10:00Z'
  resolved_by_run: shape-slice-844-1
- id: Q-surface-1
  kind: asked
  blocking: true
  asked_at: '2026-10-24T04:20:00Z'
  topic: surface
  question: Which one command starts the shaping loop when the product owner tests
    it end to end?
  proposed_answer: null
  basis: null
  pipeline_source: /shape-slice shape-slice-844-1
  pipeline_guess: null
  impact_if_unknown: A slice has exactly one surface; the model and memory name no
    command that starts the three plays in a row, so a wrong choice either leaves
    out a feature (a new loop command) or tests the loop from the wrong entry.
  user_decision: in_scope
  user_answer: '"i run 3 plays - /shape-slice , and one that builds plan and one that
    will build evals. so it can be /shape-slice /shape-plan and /shape-eval." No loop:
    "this is not a loop."'
  resolved_at: '2026-10-24T05:10:00Z'
  resolved_by_run: shape-slice-844-1
- id: Q-capability-1
  kind: asked
  blocking: false
  asked_at: '2026-10-24T04:20:00Z'
  topic: capability
  question: Should the four shaping plays sit under one new capability for the shaping
    loop?
  proposed_answer: null
  basis: null
  pipeline_source: /shape-slice shape-slice-844-1
  pipeline_guess: null
  impact_if_unknown: No capability in the model serves bi-788, so the run must add
    one; splitting the plays across several capabilities changes which ICE each story
    is planned from.
  user_decision: in_scope
  user_answer: '"features - yes makes sense" — "features should be groups under capability
    and linked to domain"; reuse what exists, fill what exists in part, add missing
    domains and capabilities with research. Placed: Shape a slice (new), Build a plan
    cap-718 (fill), Write the hidden eval (new); domain Software delivery planning
    (new).'
  resolved_at: '2026-10-24T05:10:00Z'
  resolved_by_run: shape-slice-844-1
- id: Q-order-1
  kind: asked
  blocking: false
  asked_at: '2026-10-24T04:20:00Z'
  topic: order
  question: Should the one approval step be built last, after the eval play?
  proposed_answer: 'Yes. Build the one approval step last, after /shape-slice, the
    plan play and the eval play: the approval comes at the end and approves the slice,
    the plan and the eval, so the plays that make them come first.'
  basis:
    kind: model
    ref: '.garura/product/product-os/intents/bi-788.md lines 9-16 (line 14: ''The
      product owner gives one approval, at the end.'')'
  pipeline_source: /shape-slice shape-slice-844-1
  pipeline_guess: 'Yes. Build the one approval step last, after /shape-slice, the
    plan play and the eval play: the approval comes at the end and approves the slice,
    the plan and the eval, so the plays that make them come first.'
  impact_if_unknown: The approval shows the slice, the plan and the eval together,
    so building it before the plays it shows means it is tested against parts that
    do not exist yet.
  user_decision: in_scope
  user_answer: yes — /shape-slice, then /shape-plan, then /shape-eval; the loop and
    its one approval are left out.
  resolved_at: '2026-10-24T05:10:00Z'
  resolved_by_run: shape-slice-844-1
- id: Q-scope-1
  kind: asked
  blocking: false
  asked_at: '2026-10-24T04:20:00Z'
  topic: scope
  question: Does the slice need eval encryption (#828) to meet the proof that no builder
    can read the eval?
  proposed_answer: null
  basis: null
  pipeline_source: /shape-slice shape-slice-844-1
  pipeline_guess: null
  impact_if_unknown: Today only a read rule keeps builders out of a plan's evals folder
    (ADR 049); adding encryption adds a feature and moves the build order, while leaving
    it out means the proof rests on a rule nothing on disk enforces.
  user_decision: in_scope
  user_answer: '"encrypt and the loop is left out."'
  resolved_at: '2026-10-24T05:10:00Z'
  resolved_by_run: shape-slice-844-1
- id: Q-scope-2
  kind: asked
  blocking: false
  asked_at: '2026-10-24T04:20:00Z'
  topic: scope
  question: Does the slice need the author-slice skill (#838) for the step that picks
    the features?
  proposed_answer: 'No. The author-slice skill (#838) stays outside the slice: the
    agent picks the features, surface and tester inside /shape-slice, which is a play,
    so the step is run by a play and not by hand.'
  basis:
    kind: model
    ref: .garura/product/product-os/intents/bi-788.md line 15 ('A play runs each step.
      No step is done by hand.')
  pipeline_source: /shape-slice shape-slice-844-1
  pipeline_guess: 'No. The author-slice skill (#838) stays outside the slice: the
    agent picks the features, surface and tester inside /shape-slice, which is a play,
    so the step is run by a play and not by hand.'
  impact_if_unknown: The proof says a play runs each step; today the agent picks the
    slice's features, surface and tester itself inside /shape-slice, so adding the
    skill adds a feature, and leaving it out keeps that choice in the agent.
  user_decision: in_scope
  user_answer: accepted as proposed — the author-slice skill (#838) is left out.
  resolved_at: '2026-10-24T05:10:00Z'
  resolved_by_run: shape-slice-844-1
- id: Q-test-1
  kind: asked
  blocking: false
  asked_at: '2026-10-24T04:20:00Z'
  topic: test
  question: On which project does the product owner run the shaping loop to test the
    slice?
  proposed_answer: 'On Garura''s own repository, on a real business intent issue:
    the intent exists because no play designs the work for Garura''s own work.'
  basis:
    kind: model
    ref: .garura/product/product-os/intents/bi-788.md line 5 ('No play designs the
      work for Garura's own work')
  pipeline_source: /shape-slice shape-slice-844-1
  pipeline_guess: 'On Garura''s own repository, on a real business intent issue: the
    intent exists because no play designs the work for Garura''s own work.'
  impact_if_unknown: The intent is about Garura's own work, but the eval play (#798)
    names Griffin as the test project for a play; testing on the wrong project checks
    the loop against the wrong product model.
  user_decision: in_scope
  user_answer: accepted as proposed — on Garura's own repository, on a real business
    intent issue.
  resolved_at: '2026-10-24T05:10:00Z'
  resolved_by_run: shape-slice-844-1
```
