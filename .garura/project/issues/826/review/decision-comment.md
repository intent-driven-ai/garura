Reviewer verdict (human, gate on): approve

PR #827, round 2. Recommended verdict: approve (no P1, no P2).

Round 1 fixes checked and in: M2 (the ICE rule names the plan play as its reader), M4 (`standards/rules/expectation-generation.md` covers a story's recovery), M5 (the running eval reads only the recovery parts), M6 (the Story says "limits"), and a real first name replaced by "the product owner". Round 2 found M7 (the rule's scope note) and M8 (a repeated phrase, "constraints" in the v10 log line); both fixed in f5762b1a.

The IDD routing table (`docs/philosophy/idd-principles.md`) holds on every row.

Deferred: M1 (ADR) → #824. M3 (encrypt the evals) → #828.

Checks: ontology check valid; change check scope (Story, Slice, Plan, ICE), version 9 → 10 with one log line, names ok; lint-components 121, same as base.
