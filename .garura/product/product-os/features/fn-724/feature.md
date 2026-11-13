# Feature: Say whether work can start on each part: ready, partly ready or not ready, with the gaps

## What it does
Before a play plans or builds from a part, the ready check gives each part one of three answers, ready, partly ready or not ready, with what stops it and the gaps that do not, worked out each time from the index, the ICE pages and the intent pages, so the same model always gives the same answer and work starts on every part that can start.
- The three answers, in the check's words:
  - ready: "its capability serves a confirmed business intent, every capability it needs is done, and the ICE has all three parts (Intent, Context, Expectation). Work starts."
  - partly ready: "as ready, with gaps that do not stop work — no domain, no identified_by, or the thin mark (gap "thin ICE", ontology v11). Work starts; the gaps are listed."
  - not ready: "a part is missing or empty, no confirmed business intent reaches it, a needed capability is not done, a feature has no parent, or a part has no ICE. Work stops."
- A feature is read through its capability: its own intents and needs are not read.
- It reads the thin mark only, never how many lines an ICE has. When only one of the two thin marks is there, the gap names the drift.
- Whether a need is done comes from a list of the parts that are done. Without the list, the needs are listed but not judged.
- Four copies of the check, kept the same, run in /create-play's reference, /discover-intent, /shape-plan and /update-plan. /shape-plan skips a feature whose ICE is not ready, and names it.
- This feature comes from the old capability Link the product model, whose rule was "One answer for one model." Its first job was the one in its old title, a part is ready without a domain: "A missing domain is a warning, never a block."
- Its run on Garura's own model on 2026-11-11: 0 ready, 249 partly ready, 13 not ready. The gaps: "has no identified by" on 257 parts, "thin ICE" on 129, "has no domain yet" on 5.
- Examples, in different kinds of project:
  - In a clinic's booking app, the Booking capability has no domain yet, serves the confirmed intent "patients book online" and has a full ICE. It reads partly ready with the gap "has no domain yet", and work starts.
  - In a shop's checkout service, Refunds needs Payments, and the done list does not hold Payments. Refunds reads not ready, and the answer names Payments.
  - In a bank's payments service, a capability's only intent is still proposed. It reads not ready, and its page is kept as it was written.
- How it meets the capability: the map decides when work can start, part by part, without blocking work because the map is incomplete.

Status: built, in `check_ice_workable.py`, four copies kept the same, with its tests. It is out of step with the product owner's answers in two ways, named below. Not built, or open:
- It counts a missing "identified by" as a gap, as the ontology's rule says, so no part reads ready. By the product owner's answer of 2026-11-11, a part found on its own is not a gap. The rule changes through /edit-ontology, in Define what a product is made of, and the check follows.
- The 13 older parts whose ICE is still inside their page read not ready, "has no ICE", and /shape-plan would skip them: plays read the whole model by one rule once its index has ICE entries, so older parts break. This breaks Product model's Must not, "Block work because the model is incomplete". Each ICE section is to move to its own page.
- Without the done list, a capability with an open need reads ready, and nothing says the needs were not checked.
- Its older rule, kept for a model with no ICE list, still reads a feature's own needs. By the product owner's answer of 2026-11-11, a feature does not need another feature.

## Inputs / Outputs
- In: the index: each capability's intents, domain, needs and "identified by"; each feature's capability; each ICE's entry, its page and its thin mark.
- In: the business intent pages, whose stage line says proposed, confirmed, met or dropped.
- In, optional: a list of the parts that are done, and one part's id.
- Out: for each ICE, and each part with none, one answer, with what stops it and its gaps, and the counts of each answer, as JSON.
- Out: for one part, an exit code: 0 for ready or partly ready, 1 for not ready, 2 when the part is unknown or an input cannot be read.

## Rules & behavior
- One answer for one model. The reason, from the old capability's page: "One answer for one model. The ready check is a script, not a judgment. The same model always gives the same answer."
- It reads files only. The reason: "No git, no network, no LLM."
- The answer is worked out each run and never stored. The reason: "computed each run and never stored".
- It stops work, never a write. The reason: "Writing is never blocked; this check stops work, not writes."
- A missing domain is a gap, never a stop. The reason: "A missing domain is a warning, never a block."
- A part found on its own is not a gap. The reason, in the product owner's words: "I'll go with your proposal of no."
- A feature is read through its capability. The reason: "A feature's own `intents` and `depends_on` are not read (v6: it finds its business intents through its parent and never needs anything)."
- A thin ICE is a gap, and only its marks are read. The reason: "the check does not count lines or judge richness; it reads only the thin mark".
- The copies stay the same. The reason: "Thus every play gives the same ready answer for the same model."
- A need that was not checked is named. The reason, as asked: "A part with needs and no done list reads partly ready with the gap "needs not checked"".
- Not decided: how the check reads an older part whose ICE is still inside its page, by its own shape, or only once each ICE section moves to its own page.

## Acceptance criteria
- Given a capability with no domain that serves a confirmed intent, has an ICE with its three parts and needs nothing, when the check runs on it, then it reads partly ready with the gap "has no domain yet", and work starts.
- Given a capability whose only intent is proposed, when the check runs on it, then it reads not ready and names why.
- Given a capability with a need that the done list does not hold, when the check runs with the list, then it reads not ready and names the need.
- Given a part id that is not in the index, when the check runs on it, then it exits 2.
- Given the same index and pages, when the check runs twice, then it gives the same answers.
- Given a capability found on its own, with a confirmed intent, a full ICE and no need, when the check runs, then it reads ready with no gap. This is not built.
- Given a capability with needs and no done list, when the check runs, then it reads partly ready with the gap "needs not checked". This is not built.
- Given an older feature whose ICE is still inside its page, when /shape-plan runs, then the feature is not skipped for "has no ICE". This is not built.

## Out of scope
- The links the check reads. Link the parts by the map's rules: what each serves, what it needs and what led us to find it (fn-725) does them.
- What counts as a gap, as a rule of the ontology. Define what a product is made of, in Product model, owns it.
- Whether a part is approved. Keep each part's approval state, so agents build only from approved parts (fn-part-approval) does it.
- Choosing what to work on next, and in which order. Orchestrate agent work through planning, in Orchestration, owns it.

## Sources
- core/components/plays/create-play/references/check_ice_workable.py, lines 4-17, 34-36 and 44: "computed each run and never stored", the three answers as quoted, "A feature's own `intents` and `depends_on` are not read (v6: it finds its business intents through its parent and never needs anything).", "the check does not count lines or judge richness; it reads only the thin mark", "Without it, needs are listed but not judged. Writing is never blocked; this check stops work, not writes.", "No git, no network, no LLM."; its three other copies, in discover-intent, shape-plan and update-plan, are the same file (compared on 2026-11-11)
- core/components/plays/shape-plan/SKILL.md, line 5: "a feature whose ICE is not ready is skipped and named"
- .garura/product/product-os/features/fn-724/feature.md, the old page, lines 1, 4 and 28: "A capability or feature is ready without a domain", "A missing domain is a warning, never a block.", "Thus every play gives the same ready answer for the same model."
- The copy of the old page of Link the product model: "One answer for one model. The ready check is a script, not a judgment. The same model always gives the same answer."
- The capability list: "I don't understand question 4. I'll go with your proposal of no.", "a feature doesn't need another feature"
- standards/schemas/product-os/ontology.md, in Phoenix memory, line 369: "A missing domain or a missing "identified by" never stops work; it is a gap, and its ICE is partly ready."
- .garura/product/product-os/intents/bi-11.md, line 15: "Block work because the model is incomplete"
- The ready check, run from the repository root on 2026-11-11, writing its report outside the repository: 0 ready, 249 partly ready, 13 not ready
- The stock-take (2026-11-11), sections 1.5, 2.6 and 5: the gaps "has no identified by" on 257 parts, "thin ICE" on 129, "has no domain yet" on 5
