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

## Since round 2

- **Opening line:** the ontology's first paragraph now names the seven kinds (Business Intent, Source, ICE, Capability, Functionality, Work, Plan) and says it grows through the `edit-ontology` play. The product owner asked for this.
- **ADR 047** (`docs/adr/047-the-ice-is-its-own-node.md`), recorded with `/record-decision` and accepted by the product owner. It amends ADR 031 (§1, §3, §4), ADR 033 (§4) and ADR 043 (§1, §2, §3), in their ICE parts only. Each older ADR gets one forward pointer on its Status line, so a reader is sent to ADR 047. The ADR index is rebuilt. The gate is the business intent's confirmation; an ICE needs no separate approval.
- The round 1 review records move into `review/round1/` (renames only).

## Self-review

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

## Where it lands

Into `plan/756/base`. Closes #758 (closed by merge-change, because the host closes issues only on main). Part of #757, #756.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
