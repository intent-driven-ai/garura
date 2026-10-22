# Self-review: #758 (ontology v6 + ADR 047), re-raise of PR #783

Rules: ~/.garura/core/memory/standards/rules/self-review.md (base, not an override). resolved-rules.json unchanged.
Diff: plan/756/base...HEAD. Informational only; the approve/reject gate is check-change.

Blocking findings: none.

## Since the last review
- PASS The ontology's opening paragraph now names the seven kinds (Business Intent, Source, ICE, Capability, Functionality, Work, Plan) and the edit-ontology play, as the product owner asked.
- PASS ADR 047 (docs/adr/047-the-ice-is-its-own-node.md), recorded by /record-decision, Status Accepted, Decided by the product owner. Amends ADR 031 (ICE parts: sections 1, 3, 4), ADR 033 (section 4 only) and ADR 043 (ICE parts: sections 1, 2, 3). Each older ADR gains only one forward pointer on its Status line; the ADR index has the new 047 row. The record-decision run records sit under .garura/project/issues/_adr/20261022-124516/.
- PASS The ADR commit also moves the round 1 review records into review/round1/ (pure renames, no content change). This is a record move, not scope creep.
- PASS Earlier fixes still hold: an ICE needs all three parts present; follow-up issues #759, #760, #761, #765 are pointed to.

## Scope
- PASS Matches the issue (#758: the ICE kind). Product file: ontology.md (v5 to v6). ADR 047 and the three pointer edits record the same decision, which the issue serves.
- PASS No scope creep. Everything else is run records under .garura/project/issues/.
- REVIEW Size (non-blocking). About 57 files and 8,000 added lines, but nearly all are STM records (pr.diff copies are about 4,000 lines). Real content: one schema file, one ADR, three one-line pointers, one index row.
- PASS No stray artifacts.

## Quality
- PASS Checks. No code changed; ontology check read valid on the last run.
- PASS Commits. feat/fix/docs/chore with scope, each references #758; the merge commit is a plain merge.
- PASS No secrets. Prose and JSON only.
- PASS Older ADRs untouched apart from the Status-line pointer, as the ADR rules require.
- REVIEW Docs in step (non-blocking). ADR 047 lists spine.yaml, ice.yaml, page templates, check scripts and glossary as affected; these are not changed here and are tracked in #759, #760, #761, #765.
- REVIEW (non-blocking) locked-model.md: the older "ready check" section still says a thin part such as an empty Context is partly ready; the later-decisions section overrides it. A one-line pointer would help.
- REVIEW (non-blocking) Log entries are not strictly in date order (predates this change).
