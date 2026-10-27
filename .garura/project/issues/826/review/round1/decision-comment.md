Reviewer verdict (human, gate on): reject — fix the findings, then raise again

PR #827, round 1. Recommended verdict: approve (no P1; 4 P3, 2 P4). The routing table holds on every row.

The reviewer asked to fix these in this PR:
- M2: the ICE section still says "only a Story reads it"; the plan play also reads it.
- M4: `standards/rules/expectation-generation.md` covers a play's recovery, not a story's; v10 relies on it for stories.
- M5: the running eval must read only the recovery parts of the hidden file.
- M6: the Story says "constraints" where the ICE says "limits".
- Two old ontology lines carry a real first name; replace it with "the product owner".

Follow-ups: M1 (no ADR for the hidden file and the Context guidance) goes into #824. M3 (the hidden file is protected by a read rule, not encryption) gets its own issue.
