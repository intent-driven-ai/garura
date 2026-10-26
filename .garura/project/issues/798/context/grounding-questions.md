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
- id: Q-recovery-1
  kind: asked
  blocking: false
  asked_at: '2026-10-26T13:44:19Z'
  topic: recovery
  question: When the thing a feature builds is itself the hidden list of failure lines,
    the tests folder or a check, may the fix that the builder is given name that thing
    as part of what it builds?
  proposed_answer: Yes. Where the hidden list, the tests folder or a check is the
    very thing the feature builds (fn-795 writes the hidden file; fn-898 builds the
    lint check and the ledger check), a fix given to the builder names it as that
    product, because it is what the builder sees and changes in the product. It never
    names the eval, or the check that found the failure. Every other fix given to
    the builder names none of them, and a fix that cannot be said without them goes
    to 'a person must decide'.
  basis:
    kind: memory
    ref: phoenix standards/rules/expectation-generation.md:88-92
  pipeline_source: /shape-slice shape-slice-20261026-run2
  pipeline_guess: Yes. Where the hidden list, the tests folder or a check is the very
    thing the feature builds (fn-795 writes the hidden file; fn-898 builds the lint
    check and the ledger check), a fix given to the builder names it as that product,
    because it is what the builder sees and changes in the product. It never names
    the eval, or the check that found the failure. Every other fix given to the builder
    names none of them, and a fix that cannot be said without them goes to 'a person
    must decide'.
  impact_if_unknown: The rule says a fix given to the builder never names the tests
    folder, the eval, the hidden list or the check that found the failure. Read word
    for word, the fixes for the play that writes the hidden list, and for the checks
    that flag a build that read the tests, lose their meaning or all go to a person,
    so the builder can fix fewer things alone. Read too loosely, a builder gets a
    pointer to the tests, builds to pass them, and a pass proves less than the business
    intent asks.
  user_decision: null
  user_answer: null
  resolved_at: null
  resolved_by_run: null
- id: Q-recovery-1-2
  kind: asked
  blocking: false
  asked_at: '2026-10-26T14:48:15Z'
  topic: recovery
  question: When a feature builds the hidden file, the plan's evals folder or a check,
    may the fix that the builder gets name that thing?
  proposed_answer: Yes. When a feature builds the hidden file, the plan's evals folder
    or a check, the fix that the builder gets may name that thing. It is part of the
    product that the builder sees and changes. For example, fn-795 writes the hidden
    file, and fn-898 builds the lint check and the ledger check. The fix never names
    the eval, or the check that found the failure. Every other fix that the builder
    gets names none of them. A fix that cannot be said without them goes to 'a person
    must decide'.
  basis:
    kind: memory
    ref: phoenix standards/rules/expectation-generation.md:88-92
  pipeline_source: /shape-slice shape-slice-20261026-run2-round2
  pipeline_guess: Yes. When a feature builds the hidden file, the plan's evals folder
    or a check, the fix that the builder gets may name that thing. It is part of the
    product that the builder sees and changes. For example, fn-795 writes the hidden
    file, and fn-898 builds the lint check and the ledger check. The fix never names
    the eval, or the check that found the failure. Every other fix that the builder
    gets names none of them. A fix that cannot be said without them goes to 'a person
    must decide'.
  impact_if_unknown: 'The hidden file (failure-and-recovery.md) lists how each feature
    can fail. It also says how to fix each failure. Some features of this slice build
    one of these things: fn-795 writes the hidden file, and fn-898 builds the lint
    check and the ledger check. The recovery rule says a fix for the builder never
    names the evals folder, the eval, the hidden file or the check that found the
    failure (expectation-generation.md, lines 88-92). The rule does not say what happens
    when the feature builds one of these things. If the fix cannot name it, the builder
    cannot fix these features alone, and each fix goes to a person. If the fix names
    too much, the builder learns where the eval is, and a pass proves less.'
  user_decision: null
  user_answer: null
  resolved_at: null
  resolved_by_run: null
- id: Q-recovery-1-3
  kind: asked
  blocking: false
  asked_at: '2026-10-26T14:55:40Z'
  topic: recovery
  question: When a feature builds the hidden file, the plan's evals folder or a check,
    may the fix that the builder gets name that thing?
  proposed_answer: Yes. When a feature builds the hidden file, the plan's evals folder
    or a check, the fix that the builder gets may name that thing. It is part of the
    product that the builder sees and changes. For example, fn-795 writes the hidden
    file, and fn-898 builds the lint check and the ledger check. The fix never names
    the eval, or the check that found the failure. Every other fix that the builder
    gets names none of them. A fix that cannot be said without them goes to 'a person
    must decide'.
  basis:
    kind: memory
    ref: phoenix standards/rules/expectation-generation.md:88-92
  pipeline_source: /shape-slice shape-slice-20261026-run2-round2
  pipeline_guess: Yes. When a feature builds the hidden file, the plan's evals folder
    or a check, the fix that the builder gets may name that thing. It is part of the
    product that the builder sees and changes. For example, fn-795 writes the hidden
    file, and fn-898 builds the lint check and the ledger check. The fix never names
    the eval, or the check that found the failure. Every other fix that the builder
    gets names none of them. A fix that cannot be said without them goes to 'a person
    must decide'.
  impact_if_unknown: 'The hidden file (failure-and-recovery.md) lists how each feature
    can fail. It also says how to fix each failure. Some features of this slice build
    one of these things: fn-795 writes the hidden file, and fn-898 builds the lint
    check and the ledger check. The recovery rule says a fix for the builder never
    names the evals folder, the eval, the hidden file or the check that found the
    failure (expectation-generation.md, lines 88-92). The rule does not say what happens
    when the feature builds one of these things. If the fix cannot name it, the builder
    cannot fix these features alone, and each fix goes to a person. If the fix names
    too much, the builder learns where the eval is, and a pass proves less.'
  user_decision: null
  user_answer: null
  resolved_at: null
  resolved_by_run: null
- id: Q-recovery-1-4
  kind: asked
  blocking: false
  asked_at: '2026-10-26T15:47:19Z'
  topic: recovery
  question: Some features build the test files themselves. When one of them breaks,
    may the fix we give the builder name those test files?
  proposed_answer: Yes. The fix may name the test file that the feature builds. It
    never says which test caught the problem.
  basis:
    kind: memory
    ref: phoenix standards/rules/expectation-generation.md:88-92
  pipeline_source: /shape-slice shape-slice-20261026-run2-round2
  pipeline_guess: Yes. The fix may name the test file that the feature builds. It
    never says which test caught the problem.
  impact_if_unknown: 'The hidden file lists, for every feature, the cases where it
    breaks, and the fix for each case. Some of those fixes go to the builder. The
    rule says a builder''s fix never names the test files (the hidden file and the
    evals folder), so the builder never learns where the tests are. But two features
    in this slice build those very files: /shape-slice writes the hidden file, and
    fn-898 builds the check that catches a build reading the evals folder. Their fixes
    cannot be written without naming those files. If the answer is no, five fixes
    move from the builder to a person.'
  user_decision: in_scope
  user_answer: 'What we''re building is Shape Slice. Why does it care about what it
    is building? All you have to do is to build this play called Shape Slice. The
    question you were asking me: it builds the files for itself. Why does it even
    matter? Why is that question important?'
  resolved_at: '2026-10-26T15:51:37Z'
  resolved_by_run: shape-slice-20261026-run2-round2
```
