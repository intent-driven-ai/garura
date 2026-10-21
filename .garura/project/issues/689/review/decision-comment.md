Harness verdict (gate off per gates.plays.review-change): approve

No finding blocks the merge (0 P1).

- Tests: all 14 changed test files pass.
- Linters: /intent, /vision and /understand pass the play linter; the Kickoff drive passes the drive linter. The components linter shows the same errors as main; the 6 new ones on the two gap skills are fixed in this PR.
- Standards scan: 0 P1. The P2 to P4 rows are mostly whole-file checklist rows and keyword matches (for example `join` read as SQL), not located defects.

Design findings to follow up (none blocks):
- P2 harness: `close-model-gaps` changes the live model, but the keeper's rules on main still forbid that, and no scoped-write guard runs around it.
- P2 memory: the ontology still says "no play owns a kind", while the spine now says each play writes one kind inside Kickoff. The two rules need to be reconciled in the ontology itself.
- P2 memory: a functionality may now have no capability. The ontology kind text and the functionality template do not say so yet.
- P3: stale template headers name the wrong play; "Sources" is used for two things; `direct-model-write.md` rule 7 (each play commits) conflicts with the drive's one commit per round; drive-creator and lint_drive still say "fixed order"; `drive-run.md` gains rules against ADR 029 section 2; the installed CLAUDE.md text has no ICE source.
- P4: Kickoff's task list still chains the plays; two keeper table rows are short one cell.

Full record: `.garura/project/issues/689/review/findings.yaml`.
