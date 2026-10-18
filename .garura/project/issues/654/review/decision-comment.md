Harness verdict (gate off per gates.plays.review-change): approve

**What was reviewed.** Three kinds of change, sorted from the diff: decision records (ADR 035, forward pointers on ADRs 009, 015, 016, 017, 032 and 034, the index row), working notes (the #653 feature plan moved from #613's folder, the #654 plan, the story texts, pointer lines in the #606 and #613 plans), and run records. None is design-bearing, so no design-grounding ran.

**Checks run.**
- ADR linter on ADR 035: valid, no problems. The index rebuilt from `docs/adr/` matches `_index.md`. Each older ADR changed by one pointer line (ADR 009 gained its first Status line).
- Standards scan (`quality-check-scoped`) over all 32 changed paths: no P1 or P2. 8 P3 and 16 P4 are path rules that fire whenever an ADR file is touched; they mark where ADR checks apply and are not defects.
- Every repo path named in ADR 035, the plans and the stories exists (39 checked; 2 were a branch name and an installer-relative path). Nothing still links to the moved plan's old path.
- ADR 035 reads Accepted; the run record shows Kapil's rename of the project tier to Garura memory and his "accept".

**Notes, not blocking.**
- Some files ADR 035 names under Affects have no story yet: `CLAUDE.md`, `docs/components/memory.md`, the memory keys in `.garura/core/config.yaml`, drive-contract rule 4, the glossary's install rows and the locked `knowledge/_DESIGN.md` (P3). Proposed to Kapil.
- ADR 009's added Status line reads "(not recorded)" above its own "Accepted" section (P4).
- ADR 035 says no story was filed yet; #655–#664 were filed later in this change (P4).
- The ADR scope check ran right after the record commit, on the pre-commit snapshot, and passed (P4).
- No review playbook covers working notes or run records; the ADR playbook still says no ADR linter exists (P4).
- Two commit subjects run past 72 characters (P4).

**Routing.** Approve → merge-change. The merge to main waits for Kapil.
