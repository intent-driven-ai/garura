# Questions — #866

Every question /shape-slice asked a person, and every gap it left as an assumption, with the answer. This file only grows (standards/rules/user-questions.md).

```yaml
questions:
- id: Q-change-1
  kind: asked
  blocking: false
  asked_at: '2026-10-25T06:38:59Z'
  topic: change
  question: When a feature is added to a slice or taken out of it after its plan exists,
    what must the plan play do with the stories of that slice?
  proposed_answer: 'When a feature comes into the slice, the plan play adds one story
    for it, so that each feature of the slice has a story; it makes no second story
    for a feature that has one; and nothing goes to the tracker before the product
    owner''s yes. What it does with the story of a feature that goes out is not set
    by the model: the product owner says.'
  basis:
    kind: model
    ref: product/product-os/software-delivery-planning/cap-718/fn-818/feature.md:20-22
      (a second run makes no copies; nothing goes to the tracker before the yes; what
      the play does when the slice changes is not set yet) and :44-46 (fails if a
      feature of the slice has no story, or a second story is made for one feature)
  pipeline_source: /shape-slice shape-slice-866-20261025T063859Z
  pipeline_guess: 'When a feature comes into the slice, the plan play adds one story
    for it, so that each feature of the slice has a story; it makes no second story
    for a feature that has one; and nothing goes to the tracker before the product
    owner''s yes. What it does with the story of a feature that goes out is not set
    by the model: the product owner says.'
  impact_if_unknown: If the plan play makes new stories, or deletes old ones, without
    a rule, the plan and the tracker stop agreeing, or the work already done on a
    story is lost.
  user_decision: in_scope
  user_answer: No duplicate stories for a feature. If a feature goes out of the slice,
    its story moves out of the plan; the plan play does not delete it. The story can
    stay in the tracker because it was already made.
  resolved_at: '2026-10-25T06:55:01Z'
  resolved_by_run: shape-slice-866-20261025T063859Z
- id: Q-evalformat-1
  kind: asked
  blocking: false
  asked_at: '2026-10-25T06:38:59Z'
  topic: eval
  question: In what form must the eval play write the eval of a slice, so that a person
    can run it from the outside?
  proposed_answer: 'The eval is written in the plan''s evals folder (.garura/project/plans/<plan-id>/evals/<slug>/).
    For each goal and expectation of the stories, and each failure condition of the
    slice''s hidden file, it holds one check run from the outside on the slice''s
    surface (for Garura often a run of the play on a test project), or a note that
    it cannot be tested yet. The layout of the file itself is not set by the model:
    the product owner says.'
  basis:
    kind: model
    ref: product/product-os/software-delivery-planning/shape-eval/fn-798/feature.md:11-13
      (one eval in the plan's evals folder; the format is not set yet), :18-20 (checks
      from the outside on the slice's surface, often a play on a test project; says
      when it cannot test a line yet) and :25 (each goal, expectation and failure
      condition has a check or a note)
  pipeline_source: /shape-slice shape-slice-866-20261025T063859Z
  pipeline_guess: 'The eval is written in the plan''s evals folder (.garura/project/plans/<plan-id>/evals/<slug>/).
    For each goal and expectation of the stories, and each failure condition of the
    slice''s hidden file, it holds one check run from the outside on the slice''s
    surface (for Garura often a run of the play on a test project), or a note that
    it cannot be tested yet. The layout of the file itself is not set by the model:
    the product owner says.'
  impact_if_unknown: If the form is not set, each eval is written in a different way,
    a person cannot run it the same way twice, and the eval play cannot be checked.
  user_decision: in_scope
  user_answer: yes, as proposed.
  resolved_at: '2026-10-25T06:55:01Z'
  resolved_by_run: shape-slice-866-20261025T063859Z
```
