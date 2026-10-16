**Harness verdict (gate off per gates.plays.review-change): approve**

No blocking (P1) findings. 23 in all, from 7 categories: harness and memory were design-checked against main's committed rules (ADR 026, ADR 031, ontology v3, the standards rules), the rest by the standards linter. 11 are fixed in this PR, including all 4 P2s. 12 small ones stay open; none blocks.

Fixed in this PR:
- **P2**: the keep check missed a page that was edited and then moved out of the holding folder. Fixed: a moved page is compared with its old version, and a holding page placed nowhere counts as lost (`a8a3fa75`).
- **P2**: two capabilities with the same name could overwrite each other when placed. Fixed: the save script refuses a clashing placement before writing anything (`a8a3fa75`).
- **P2**: pages `/intent` wrote before this change failed the page checker. Fixed: a linked page with no agent-intent section is now a warning, not an error, so earlier pages still pass (`df6f48f0`).
- **P2**: the write-safety rule file (`direct-model-write.md`) did not describe the new remove-only and modify-only rules or /vision's new scope. Fixed (`cc48e1c1`).
- **P3**: broken spine files crashed two scripts; an ICE with no goal could be saved; short variable names; outdated lines in the /vision play, the keeper agent, the schema index and spine comments; a change-log sentence in the /vision play. All fixed (`a8a3fa75`, `7518fe30`, `cc48e1c1`).

Open, not blocking:
- **P3**: /vision's done checks prove "kept" but not the two-way links or placements (these are covered by step evals only).
- **P3**: no ADR records that /intent may now place capabilities and write light domains (ADR 031 part 3 gave that to /vision), and the v4 ontology approval lives only in the branch log.
- **P3**: the spine `intents` field now means both "built from" and "touched by" on capabilities and functionalities.
- **P3**: a domain entry with no `detail` and a one-section page passes as light.
- **P4**: small wording drift, a few gold examples, ICE property names vs section labels, test files opened without `with`, "holding folder" undefined in docs.

Checks run: all 20 test files under `core/` pass. `lint_play` passes on /intent and /vision. The ontology checker passes. All shared-script copies are byte-identical (15, 12 and 3).
