Reviewer verdict (human, gate on): reject — fix all findings in this PR, then raise again

PR #840, round 1. Recommended verdict: approve (no P1; 4 P2, 7 P3, 5 P4).

To fix in this PR:
- P2: a slice that already serves the intent must be reused even when the new shape has other features (C7, S3).
- P2: the slice record `persist_slice` writes must match `slice.yaml` v2, and a reused slice's record gains the intent; `slice.yaml` and `spine.yaml` must agree on who writes slices.
- P2: the old-chain plays that still use removed slice fields (`/shape-scope`, `/shape-roadmap`, `/shape-measure-lens`, `build-epic`'s ready check) are stated as a known gap here and tracked in #837 (and #818 for build-epic's epic).
- P3: question record matches by meaning, not by id alone; a "change" undoes this run's intent-page edits; a script checks the yes before the commit; the question check fails on an unanswered question; decisions keep a memory trace; the play points to #838; the utility-agent count is right.
- P4: the two glue steps get scripts; the spine field count in the text is right; ids and paths stay inside the model; the spine write is safe if the run stops; the cardinal-rule table and user-questions.md list the new fields.

Not a finding: the rules added to CLAUDE.md and managing-work.md were moved there on the product owner's request.
