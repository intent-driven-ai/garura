Harness verdict (gate off per gates.plays.review-change): approve

**What was reviewed.** Three kinds of change, sorted from the diff: decision records (ADR 036, and the Status lines of ADR 032, 034 and 035, and the index), plans and story texts (the #653 plan, the #654 story texts, the review tool plan), and run records. None is design-bearing: the review playbook for ADRs leaves the decision itself to the person, and Kapil accepted ADR 036.

**Checks run.**
- `adr.py lint` on ADR 036, 035, 034 and 032: valid. `adr.py guard` on ADR 036: no business intent changes.
- A fresh index rebuild is identical to `docs/adr/_index.md`; numbering runs 001 to 036 with no gap.
- ADR 032, 034 and 035 differ from main on their Status line only.
- Every path ADR 036 names exists; no dead links; `git diff --check` clean.
- `check_plan.py` on the #653 plan: no problems. The story texts parse.

**Findings — no blocker; two small (P4).**
- REV-1: the ADR review playbook says no ADR linter exists; `adr.py lint` does.
- REV-2: there is still no review playbook for STM plans and story texts, or for run records.

**Routing.** Approve → merge-change. The merge to main waits for Kapil.
