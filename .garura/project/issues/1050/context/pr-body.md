## What this changes

**Product ontology v16: each product feature has exactly one Feature issue in the tracker, which names the feature, and the model holds no issue number** (ADR 068). The three checkpoints were agreed by the product owner through /specify-ontology.

- **New kind, Feature issue.** One issue of type Feature, with no label, per product feature. It names the feature with `Represents: <feature id>`. It holds the feature's scope of work and Context guidance, sits under one epic at a time, and holds its Stories. A person closes it through /reshape-plan "finish". Only "closed as completed" means built.
- **Story** is now a piece of work inside a Feature issue. **Epic** holds Feature issues. **Plan** and **Slice** group features many-to-many and take in only features not yet built. A plan shows a feature held by another plan's epic as `held_by`.
- **Capability** and **ICE** change wording only.
- **Questions:** Q19, Q20, Q26 and Q43 changed, with their follow-ons. Q48–Q53 are new.

Closes #1050

## How to review it

- `core/components/memory/standards/schemas/product-os/ontology.md`: the only source change.
- The ontology check and the change check both pass: only the agreed kinds changed, the version is up by one with one log line, and no real names appear.
- Everything else is run records: the three agreed drafts, the decisions, the checks, and memory copies.
- The installed copy updates only when an install is run.

## Self-review

# Self-review: issue #1050 (the ontology says each product feature has one Feature issue that names it)

Branch: feature/1050-ontology-feature-names-its-story, base: main.
Rules used: the base self-review rules in Phoenix memory (standards/rules/self-review.md), read through the memory tool. No project override exists (see resolved-rules.json).
Verdict: ready to raise. Blocking findings: none.

## What the change is

The product ontology moves from version 15 to version 16, written by /specify-ontology after the product owner agreed three checkpoints, as ADR 068 (on main) decided. A new kind, the Feature issue, is added. The Feature, Story, Epic, Plan and Slice kinds change, the Capability and ICE wording changes, and some questions are changed or new.

Two areas changed, nothing else:
- core/components/memory/standards/schemas/product-os/ontology.md (+186, -109 lines).
- Run records under .garura/project/issues/1050/ (the drafts, decisions, the checks, the memory copy of the ontology template, the start-work context). No source, play, skill, agent or doc file outside those two areas is touched.

The branch also carries a merge of main. It brings nothing of its own: the diff against main shows only the two areas above.

## Scope checks

- [PASS] Matches the issue. The ontology diff is the v16 change the issue asks for, and ADR 068 is the decision behind it.
- [PASS] No scope creep. The change check (.garura/project/issues/1050/context/specify-ontology/change-check.json) reads scope_ok true: the kinds that changed are Capability, Epic, Feature, Feature issue, ICE, Plan, Slice and Story, and all eight are on the allowed list. Nothing is out of scope.
- [PASS] Reasonable size. One ontology file changed by about 300 lines; the rest of the diff is run records that no reviewer needs to read line by line.
- [PASS] No stray artifacts. No commented-out blocks, debug output or scratch files in the diff. One untracked file is left: .garura/project/issues/1050/context/resolved-rules.json, the record of this review's rules; the play commits it with the review.

## Quality checks

- [PASS] Ontology check. Run on the changed ontology, it reads valid true with no problems. It lists 14 kinds, Feature issue among them. Questions Q3 (partly answered) and Q4 (not yet answered) were open in the same way on main, so the change did not cause them.
- [PASS] Change check. change-check.json reads scope_ok true, version_ok true (15 to 16, updated 2026-11-12, one new log line) and names_ok true (no real names found).
- [PASS] Tests. No code changed, so there is no test to add. The ontology check and the change check are the tests for this kind of change, and both pass.
- [PASS] Commits are clean. Three commits of its own: one feat(ontology) and two chore(stm), all in conventional format and each naming #1050. The merge commit of main has the plain merge message. No commit carries an attribution line.
- [PASS] No secrets. No keys, tokens or passwords in the diff.
- [PASS] No personal references. A search of the changed files finds no personal name, company name, home folder or temp path.
- [PASS] No merge conflicts with main (a trial merge of main and the branch came out clean).
- [PASS] Docs in step. The ontology is itself the document, and ADR 068, which explains the decision, is already on main. No README or usage doc names the changed kinds.
- [PASS] Nothing obviously broken. No leftover TODO or FIXME in the ontology file.

## Notes for the reviewer (none stop the raise)

- The source change is in core/components, so the project's own installed copy is out of date until the install runs. Per the repo rule, the install is run only when asked, so this is a note and not a finding.
- The ontology check reports Q3 and Q4 as not fully answered. This is how main already stands; it is raised here only so nobody reads it as new.
