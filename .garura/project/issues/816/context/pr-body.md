One change for four issues in plan 788. It sets how a slice links to a business intent and to its plan, gives /shape-slice a question budget, fixes a name in the old-name check, and adds one shared rule for how a play asks a person a question.

Closes #817. Closes #815. Closes #820. Refs #816 (it stays open: ADR 048 §2, the shaping loop, is recorded later as its own change, because /record-decision cannot join an open change — #822).

## What changes

- **#816 — ontology v9.** A slice serves one or more business intents. Each business intent has one plan; it holds every slice that serves the intent and makes one epic for each. A slice's eval is kept in `.garura/project/plans/<plan-id>/evals/<slice>/`, and the eval reads the epic and its stories, never the ICE. The build delivers a usage guide at `.garura/project/plans/<plan-id>/guides/<slice>.md`. Questions Q27–Q31 are added, Q7 and Q25 changed. CLAUDE.md now says a builder never reads a plan's evals folder.
- **#817 — question budget.** `core/config.yaml` gets `shape-slice.grill-tier: m`. New `core/components/plays/shape-slice/scripts/grill_budget.py`: `tier` gives the budget (xs 5, s 12, m 25, l 45, xl 70; absent gives m), `split` asks every blocking question and fills the rest of the budget in order; the rest become assumptions.
- **#815 — naming fix.** `FIRST_NEW_ADR` becomes `FIRST_RENAME_ADR` in `core/tools/naming/check_old_names.py`, with tests for ADR 049 and the superseded ADRs.
- **#820 — asking a person.** New rule `core/components/memory/standards/rules/asking-a-person.md` (each question has Question, Answer, Why it matters, Example; one thing per question; several examples). edit-ontology and author-product-ontology point to it. The lint check for it is #821.

## Checks

| Check | Result |
|---|---|
| Hidden eval (written first; failed 3/33 before the build) | 51 passed, 0 failed |
| `test_grill_budget.py` | 19 passed |
| `test_naming_tools.py` | 21 passed |
| Old-name check | 0 |
| Ontology check / change check | valid / scope, version, names ok |
| Component linter | 121 errors before and after (no new ones) |

## Self-review

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

🤖 Generated with [Claude Code](https://claude.com/claude-code)
