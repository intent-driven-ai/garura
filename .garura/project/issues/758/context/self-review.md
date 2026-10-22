# Self-review: #758 (ontology v6)

Rules: ~/.garura/core/memory/standards/rules/self-review.md (base, not an override).
Diff: origin/plan/756/base...HEAD. Informational only; the approve/reject gate is check-change.

Blocking findings: none.

## Scope
- PASS Matches the issue. The only product file changed is core/components/memory/standards/schemas/product-os/ontology.md (v5 to v6): ICE becomes its own node per capability and functionality; business intent holds no ICE; needs / identified by between capabilities only; business intents keep identified by; a capability has at most one domain; Q8-Q16 added. change-check.json: scope_ok, version_ok (5 to 6, one log line), names_ok.
- PASS No scope creep. Every other file is run records under .garura/project/issues/758/context/.
- PASS Size. One schema file (262 lines changed) plus records; reviewable in one sitting. The branch also holds a merge of plan/756/base, which adds nothing new to the diff against that base.
- NOTE Stray artifact. resolved-rules.json is untracked (left in place, unchanged). Decide whether it is committed with the other run records.

## Quality
- PASS Tests/checks. ontology-check.json reads valid; no code changed.
- PASS Commits. feat(ontology) and chore(stm) are conventional and reference #758; the merge commit is a plain merge.
- PASS No secrets. Only prose and JSON run records; no real names (names_found empty).
- PASS Internal consistency. Read the file: intro flow, Business Intent ("holds no ICE"), ICE, Capability, Functionality, Work and Not yet defined (Domain holds no ICE) all agree; Q8-Q16 are numbered in order and each names the links that answer it.
- REVIEW Docs in step (non-blocking). The ontology now says ICE lives in `ice.md` with a new `ices` list in `_spine.yaml`. The spine schema, ice.yaml, glossary and plays that read ICE inline in capability/functionality pages are not changed here. Confirm a follow-up issue in plan #756 covers them.
- REVIEW Small, non-blocking. Log entries are not strictly in date order (the 2026-10-09 "On review of #631" line follows 2026-10-21; this predates the change). The intro still says "this first version defines the Business Intent".
