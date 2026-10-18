Harness verdict (gate off per gates.plays.review-change): approve

**What was reviewed.** Four kinds of change, sorted from the diff: decision records (ADR 032, ADR 033, forward pointers on 026, 029, 030, 031, the index), one philosophy page (`docs/philosophy/idsd.md`), #617 working notes (plans, the review-tool plan and mockup), and run records. None is design-bearing, so no design-grounding ran.

**Checks run.**
- ADR linter on ADR 032 and ADR 033: valid, no problems. The index rebuilt from `docs/adr/` matches `_index.md`.
- Standards scan (`quality-check-scoped`) over all 45 changed paths: no P1 or P2. 7 P3 and 14 P4 are path rules that fire whenever an ADR file is touched; they mark where ADR checks apply and are not defects.
- Every repo path named in the ADRs and the #617 notes exists (19 checked), except `core/tools/outcome-review/`, the planned home of the tool (#641–#644) — expected (P4).
- Both ADRs read Accepted; the run records show Kapil's typed accept for each.

**Notes, not blocking.**
- No review playbook covers STM working notes or run records yet (P4).
- The merge stays with a person.
