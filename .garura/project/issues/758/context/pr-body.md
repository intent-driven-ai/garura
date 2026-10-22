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

## Self-review


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

## Where it lands

Into `plan/756/base`. Closes #758 (closed by merge-change, because the host closes issues only on main). Part of #757, #756.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
