Reviewer verdict (human, gate on): approve

PR #808, round 1. Recommended verdict: approve (no P1; 4 P2, 5 P3, 3 P4).

Checks: check_ontology valid; change check scope, version (6 → 7, one log line) and names ok; all three checkpoints agreed (13 recorded answers); edit-ontology tests 11 passed. v7 says exactly what the three agreed drafts say (draft hashes match decisions.json).

Findings carried to #807 (approved as they are here):
- P2: no ADR yet for v7; it reverses ADR 019 / 024 (epic record in the model), ADR 028 (slice realized stamp; epics cut by /shape-features) and ADR 031 §1 (every work item carries an ICE); the old work-type model was never an ADR. ADR 047's core rule holds; only its word "functionality" changes. → ADR 048 via /record-decision in #807.
- P3: glossary (Slice, Epic, Functionality) out of step; Source lacks the Layer and "In the tracker as" lines; the template does not define them; draft-questions.md open point 3 shows round 9 wording (the ontology follows the final answer).
- P4: long opening; live names stay "functionality" until #807.

Next: merge-change into plan/788/base.
