# Self-review: grouped change for #816, #817, #815, #820

Branch: plan/788/816-shape-slice-ontology-and-tier. Base: plan/788/base.
Rules used: standards/rules/self-review.md (base rules).

Result: No blockers. 0 blocking findings.

## Scope checks

- [PASS] Matches the issues. Each commit maps to one issue: ontology v9 and the CLAUDE.md rule (#816), the grill tier setting and grill_budget.py (#817), the old-name constant rename (#815), the asking-a-person rule and its two pointers (#820).
- [PASS] No scope creep. No file falls outside the four issues. The STM files are the normal run record for #816.
- [PASS] Size. About 30 files, but 17 are STM run records and an eval record. The source change is small and each issue is its own commit.
- [PASS] No stray artifacts. No debug prints or commented-out blocks in the source files. Merge test against the base shows no conflicts.

## Quality checks

- [PASS] Tests present. test_grill_budget.py covers all five tiers, the default, the bad tier, and the question split. test_naming_tools.py has a new case for #815. The hidden eval for #816 reads 51 passed, 0 failed.
- [PASS] Commits are clean. All use conventional format and name an issue.
- [PASS] No secrets. A scan of the diff found no credentials or tokens.
- [PASS] Docs in step. CLAUDE.md, the rules index, the ontology schema and the config comment all match the new behaviour.
- [PASS] Nothing obviously broken. The component linter shows 121 errors before and after the change, so there are no new ones.

## Notes (not blocking)

- The CLAUDE.md Work Tracking paragraph now has one long line where the evals sentence joins the plan-ID sentence. It reads correctly. A line break would help later.
- #816 stays open after merge, because the ADR 048 section 2 record is a later change. Use "Refs #816", not "Closes #816", in the PR. Close #817, #815 and #820.
- The eval result and eval script sit in the issue's evidence folder. This is fine, because they are run records and no builder reads them.
