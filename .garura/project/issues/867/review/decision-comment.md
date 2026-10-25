**Approve** — the product owner's verdict (human), check-change round 1.

- The copy script now accepts `version: null` from short-term and Garura memory, as the memory tool's contract allows, and still refuses a Phoenix answer with no version. 0 new lint errors against the base; the copy-script tests and the 11 hidden checks pass; the standards scan finds nothing.
- F1 (P3): a missing `version` field is treated the same as null, so that refusal is weaker than the contract. F2 (P4): one error message and one guide line. Both go to chore #872.
- Deviation: in Step 2 the review agent ran the branch's source copy of the script once, because the installed copy has the bug this PR fixes.

Records: `.garura/project/issues/867/review/`.
