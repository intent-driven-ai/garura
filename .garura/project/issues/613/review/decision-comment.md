Harness verdict (gate off per gates.plays.review-change): approve

**What was reviewed.** Three kinds of change, sorted from the diff: a decision record (ADR 034, its pointer on ADR 029, the index row), #613 working notes (the Kickoff and lifecycle plans, the memory review, the draft memory system plan), and run records. None is design-bearing, so no design-grounding ran.

**Checks run.**
- ADR linter on ADR 034: valid, no problems. The index rebuilt from `docs/adr/` matches `_index.md`. ADR 029 changed only on its Status line.
- Standards scan (`quality-check-scoped`) over all 29 changed paths: no P1 or P2. 3 P3 and 6 P4 are path rules that fire whenever an ADR file is touched; they mark where ADR checks apply and are not defects.
- Every repo path named in the plans, the memory review and ADR 034 exists (44 checked; 4 were a branch name or paths inside the issue folder).
- ADR 034 reads Accepted; the run record shows Kapil's typed reply ("approved").

**Notes, not blocking.**
- The drive contract rule, the rules index and the glossary still carry ADR 029's old wording; ADR 034 names them as follow-up work (P3).
- ADR 034 cites #613 plan items by their numbers at acceptance; the plan's log maps them to the new numbers (P4).
- No review playbook covers STM working notes or run records yet (P4).
- The review shelf path the play binds (`./.garura/core/memory/knowledge/review/`) does not exist; the machine-global shelf was used, as in #617. The memory review covers this (P4).
- Three commit subjects run past 72 characters (P4).

**Routing.** Approve → merge-change. The merge to main waits for Kapil.
