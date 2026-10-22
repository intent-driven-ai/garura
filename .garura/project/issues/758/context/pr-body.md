Ontology version 6: the agent intent (ICE) is its own node, one for each capability and each functionality. A business intent holds no ICE.

This is the first real run of `/edit-ontology`. The product owner agreed all three checkpoints.

## What changes in the ontology

- **ICE:** its own page (`ice.md` in its part's folder) and its own spine entry, with three parts: Intent (goals, limits, fails if), Context (what the sub-agent reads, what it never reads, the persona, the scope) and Expectation (scenarios, done means, quality needs). It is for exactly one capability or functionality, and it has no link to a business intent.
- **Business intent:** links to its capabilities, and holds no ICE. Business intents keep "identified by" between them, as a connection, never a dependency. A new optional Rules field.
- **Capability:** serves one or more business intents, has at most one domain, and has one ICE. "Needs" and "identified by" join capabilities only.
- **Functionality:** exactly one parent capability and one ICE. It never needs anything.
- **Work:** each piece carries the ICE of its part. An ICE can have many pieces of work.
- **The ready check** moves to the ICE, with three answers: ready, partly ready, not ready.
- **Questions Q8–Q16** added; Q1–Q7 keep their wording.

## Checks

| Check | Result |
|---|---|
| Ontology check (`check_ontology.py`) | valid, 7 kinds, 0 problems |
| Change check: scope | only ICE, Business Intent, Capability, Functionality and Work changed |
| Change check: version | 5 → 6, dated 2026-10-22, one log line |
| Change check: names | no real names |
| Checkpoints | three yes answers from the product owner (`decisions.json`) |

## What follows (not in this PR)

- #759, #760: the linter and the ready check follow version 6.
- #761: the plays write ICE nodes. #765: Garura's own model moves (including fn-727 → fn-724 becoming cap-718 → cap-723).

## Review fixes (after the product owner's reject)

- An ICE starts only with all three parts present. A missing part makes it not ready. A thin or wrong part does not stop it: correctness and richness are the product owner's job.
- The ontology points to #759, #760, #761 and #765 for the parts it names that are not built yet.
- The run's locked model records the later decisions (one domain; the all-three-parts rule).

## Self-review


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

## Where it lands

Into `plan/756/base`. Closes #758 (closed by merge-change, because the host closes issues only on main). Part of #757, #756.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
