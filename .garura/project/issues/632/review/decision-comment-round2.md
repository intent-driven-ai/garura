**Harness verdict, round 2 (gate off per gates.plays.review-change): approve**

Round 1's 33 findings: 30 closed in round 1, 1 recorded as a follow-up in the #632 plan, and the last 2 (the scope check's drive limit, three missing tests) closed in this round.

Round 2 reviewed the round-1 fixes and found 8 (3 P2, 2 P3, 3 P4; none blocking), all caused by those fixes and all fixed, each with a test:
- a full supersede of an ADR already superseded by another is now caught before anything is written (not after the new ADR is accepted);
- the first ADR in a project with no ADR folder creates it again;
- two partial supersedes on a YAML decision both point back (`amended_by`);
- the clean-tree rule is in the play's intent source and actually runs at the end of Step 0;
- a stopped run keeps its lint and guard records; per-run session markers; the Next map's standalone comment; a note on older product decisions.

The scope check now also catches a second change to a file already changed before the run (inside a drive).

Checks: `lint_play` pass (adr, intent); tests 43 + 37 pass; ruff clean; the two `adr.py` copies identical.

Refs #632
