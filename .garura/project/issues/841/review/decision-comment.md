Reviewer verdict (human): reject

Round 1. The product owner's word: reject; fix every P2 and P3 now; the P4s go to one chore.

To fix in this PR:
- DR-1 (P2): ADR 053 is accepted, so its line goes back as written; the old-name check skips ADR 053, which quotes old names on purpose.
- H1, H2 and M3 (P3): one ADR records the two decisions that have no record yet: the deprecated agents and skills are deleted (amends ADR 050 §3), and the asking rule is a shared skill file, not memory (amends ADR 039 §9).
- M1 (P3): pr.md marks the ADR rows (ARCH-23, DOC-04, DOC-05) as not scanned on docs/adr.
- Q-1 (P3): the 91 scanner hits on four new tool files are read rule by rule; real ones are fixed, and rows that fire on any code file with no shown defect are tuned; SEC-18 no longer matches a plain word.

To one chore (P4): H3, H4, M5 (DR-2 is fixed with DR-1; M4 needs no fix).

Answered, not open: M2 (the template stands alone, by the product owner's decision) and DR-3 (the ADR 028 and ADR 033 pointers are on the base, 56ea71a4).
