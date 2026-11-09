# Feature: Keep the evals from the builder, and flag a build that read them

## What it does
The build of the chosen work is given what the work asks, through its stories, and never the evals, the hidden file or the plan's evals folder. This feature checks that it is so, and makes visible each build that read the evals folder anyway.
- The build is every part that builds the work: the builder, the test writer of the code-level tests, the helper that collects each story's context, and any part they start. The builder is the developer who builds the code test first.
- A lint check reads the inputs of each part that builds, its hand-offs and its context files, and fails a part whose inputs name the evals folder, an eval or the hidden file.
- After a build, a ledger check reads that build session's ledger, the record of what the session did, found through the session that the build run's evidence names, and flags each read of the plan's evals folder.
- The ledger check never stops the build. It records the flag in that build run's evidence, so the shortcut is visible. In the product owner's words: "For now we should record this under evidence."
- Nothing is encrypted. The evals stay plain text in the repository, and they are simply not part of what the build is given.
- How it meets the capability: an eval proves something only when the build did not see it. In the product owner's words: "the code, when being written, should not get to see what tests there were".

Status: not built (#898). What exists covers only part of it:
- A read rule: no builder, no part that builds the software and no context helper reads a plan's evals folder. Nothing on disk stops a part that breaks it.
- Each play run's evidence names its session and the session's ledger file, with where the run starts and ends in it, so a check can find what the build read.
- The old build play, /build-epic, is stale. It passed the evals only to the play and its checker, and checked each hand-off before it was sent.
- Blocking a read with a hook is left to the guardrails the install will lay (#893), which the install does not lay today.

## Inputs / Outputs
- In, for the lint check: the inputs of each part that builds the work, its hand-offs and its context files.
- In, for the ledger check: the build session's ledger, found through the session named in that build run's evidence.
- Out, from the lint check: a pass, or a failure that names each part and each of its inputs that names the evals folder, an eval or the hidden file.
- Out, from the ledger check: one flag in that build run's evidence for each read of the evals folder, and none for a clean session.

## Rules & behavior
- The build is given what the work asks, through its stories, and never the eval. The reason, in the product owner's words: "I just want to make sure that when the agents are building, they don't only think through the evals, but they look at the intent and build for that."
- Every part that builds the work is checked, not a list of some of them. Only the parts that write the evals and the hidden file, and the eval when it runs, may name the evals folder. The reason: when the list named only some parts, a part that builds and is not on it could be given the eval, and a pass would prove less.
- The ledger check flags a read and never blocks the build. The reason: it makes the shortcut visible, and blocking is the guardrails' work.
- The flag goes into the build run's evidence, and for now only there. The reason, in the product owner's words: "For now we should record this under evidence."
- A clean build session gets no flag. The reason: a flag must always mean a real read.
- Not decided: what the ledger check does when it cannot find a build session's ledger.
- Not decided: whether the design of the work is checked the same way. What the design writes reaches the builder.

## Acceptance criteria
- Given the parts that build the work, when the lint check runs, then it fails each part whose inputs name the evals folder, an eval or the hidden file, and passes when none does.
- Given a build session whose ledger shows one read of the evals folder, when the ledger check runs, then that build run's evidence holds one flag that names the read, and the build was not stopped.
- Given a clean build session, when the ledger check runs, then that build run's evidence holds no flag.

## Out of scope
- Blocking a read of the evals folder with a hook. The guardrails the install will lay may do it (#893).
- Encrypting the evals. The product owner dropped it.
- Showing the flag anywhere but the build run's evidence. It is for later.
- Splitting each story so the builder's part holds no expectation. Gather the work under a chosen plan item does it.
- Handing each agent of the build only its part. Build the work test first does it.

## Sources
- GitHub #898 (open): "I just want to make sure that when the agents are building, they don't only think through the evals, but they look at the intent and build for that.", "A check flags any build that read the evals folder.", "It does not block; it makes the shortcut visible."
- GitHub #898 (open): "No build play, build skill or build helper is handed the eval or the hidden file, or their folder. Nothing is hidden: the eval is simply not part of the brief."
- GitHub #898 (open): "No build play's inputs (contracts, context files) name the evals folder, the eval or the hidden file; a lint check fails one that does."
- .garura/product/product-os/software-delivery-planning/shape-eval/fn-898/feature.md: "For now we should record this under evidence.", "When the list named only some plays, a play that builds code and is not on the list could be given the eval, and a pass would prove less than the intent asks."
- .garura/product/product-os/software-delivery-planning/shape-eval/fn-898/feature.md: "A build session with no read of the evals folder passes with no flag, so a flag always means a real read.", "Thin: what the ledger check does when it cannot find a build session's ledger is not set yet."
- .garura/product/product-os/software-delivery-planning/shape-eval/fn-898/feature.md: "Blocking a read by hook is the guardrails work (#893).", "The flag is recorded in the build run's evidence, and for now only there"
- The product owner on 2026-11-09, in .garura/project/issues/1021/context/capabilities.md: "the code, when being written, should not get to see what tests there were", "The builder never sees the tests; a separate check runs them."
- docs/adr/057-a-slices-eval-is-plain-text-gherkin-that-runs-with-no-agent.md: "#828 is dropped.", "only the read rule keeps the eval from the builder. A play or an agent that breaks the rule is not stopped by anything on disk."
- docs/philosophy/garura-reference-implementation.md: "the evals path is passed only to the play and to `quality-auditor`.", "The evals are not encrypted — isolation comes from which sub-agent receives which contract, checked before every dispatch."
- core/components/plays/build-epic/SKILL.md: "waits for the rebuild of the execute loop on the plan and eval plays"
- standards/templates/evidence-file.md, in Phoenix memory: "session_id: {Claude Code session UUID from session_stamp.py, or null}", "ledger_file: {path to the session's JSONL ledger, or null}"
- standards/schemas/product-os/ontology.md, in Phoenix memory: "A builder agent, any skill that builds the software, or the build play's context sub-agent never reads its eval or its hidden file, and never reads a plan's evals folder."
- CLAUDE.md: "No agent or skill that builds the software reads that folder; only the eval play and the eval itself do."
