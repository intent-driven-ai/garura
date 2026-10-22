# Self-review: #758 (ontology v6), re-raise of PR #783

Rules: ~/.garura/core/memory/standards/rules/self-review.md (base, not an override). resolved-rules.json unchanged.
Diff: plan/756/base...HEAD. Informational only; the approve/reject gate is check-change.

Blocking findings: none.

## Review fixes
Checked against the last fix(ontology) commit (85fb2c7d) and the current files.
- PASS (1) An ICE with Intent, Context or Expectation missing is not ready; a present but thin part can start. The ICE property table marks each part "missing makes it not ready"; the ready rule says "An ICE starts only with all three parts present... however thin or even wrong"; the Booking example (thin but complete, partly ready for no domain) and the new Order history example (Context missing, not ready) match; Q10 names a missing part. The old "empty Context is a gap" line is gone.
- PASS (2) The ontology points to #759 (linter check of an ICE's parts and links), #760 (three-answer ready check), #761 (plays that write ICE nodes, the ices spine list and ice.md page) and #765 (move of Garura's own model) in a "Not built yet" line under the ICE kind. The v6 log line also records the all-three-parts rule.
- PASS (3) locked-model.md has a "Later decisions (after the lock)" section recording one domain per capability (and a domain with one or more capabilities) and the all-three-parts rule from the PR #783 review.
- NOTE (non-blocking) In locked-model.md, the older "The ready check, on each ICE" section still says a thin part such as an empty Context is partly ready, and its Not ready line omits a missing part. The later-decisions section overrides it, but a reader of the top section alone would be misled. Consider a one-line pointer there.

## Scope
- PASS Matches the issue. The only product file changed is core/components/memory/standards/schemas/product-os/ontology.md (v5 to v6): ICE its own node per capability and functionality; business intent holds no ICE; needs / identified by between capabilities only; a capability has at most one domain; Q8-Q16 added; version up by one with one log line.
- PASS No scope creep. Every other changed file is a run record under .garura/project/issues/758/.
- PASS Size. One schema file plus records; reviewable in one sitting.
- PASS No stray artifacts. resolved-rules.json is tracked and unchanged. Run records (pr.diff, review files) are the expected STM evidence.

## Quality
- PASS Tests/checks. ontology-check.json reads valid; no code changed.
- PASS Commits. feat(ontology), fix(ontology) and chore(stm) are conventional and reference #758; the merge commit is a plain merge.
- PASS No secrets. Prose and JSON records only; no real names.
- PASS Internal consistency. Ready rule, property table, examples, Q10, and the Domain/Capability sections agree after the fix.
- REVIEW Docs in step (non-blocking). Spine schema, ice.yaml, glossary and plays that read ICE inline are not changed here; the ontology now points to #759, #760, #761 and #765 for them.
- REVIEW Small, non-blocking. Log entries are not strictly in date order (predates this change); the intro still says "this first version defines the Business Intent".
