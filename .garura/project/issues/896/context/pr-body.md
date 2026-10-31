## Story #896 — /shape-plan stops when the business intent already has a plan

Closes #896. Plan 717, under #718 (build a plan from a business intent).

### What a person gets

`/shape-plan <id>` makes an intent's plan once. When the intent already has a plan file — in the checked-out tree or on main — the play stops at pre-flight, before it opens a change, reads the model or writes anything, and says: "Plan <id> already exists for #<id>. /shape-plan makes a plan once. To change it (add an epic, a story, a feature, or a status), run /update-plan <id>." With no plan file, the first run works as before.

### What is in it

- **The check**: `core/components/plays/shape-plan/scripts/check_plan_absent.py` (exit 0 no plan, 3 a plan exists, 2 bad input), with 5 tests. On a stop it leaves no file behind.
- **/shape-plan's ICE, rebuilt through /edit-play**: new C14 (the pre-flight check), F13, S9 and REC13; the promises that only an existing plan could meet are removed (C4, C12, F6, S2–S5, REC6; C1 and C3 narrowed to one plan and one run); the Context names /update-plan as the play that changes a plan that exists. The compiled play follows; the play linter passes with no gap.
- **The product model**: fn-818's ICE (/shape-plan's feature) — "a second run makes no copies" becomes "when the plan exists, the play stops and points to /update-plan", and its open line on a slice that changes after a plan exists is settled. Changed through the model sub-agent and the page skill's named-line change.
- **ADR 063** (accepted 2026-10-31): /shape-plan makes the plan once; a plan that exists is changed only by /update-plan. It amends ADR 049 §1.2 and §2.
- **Round 1 review fixes**: the plan-exists stop runs no close (nothing left behind); the play names the update actions it no longer reaches; a part-way tracker failure points to /update-plan; recovery count and order. /shape-slice's Next Steps and the Next-line map name /update-plan for an intent that has a plan. fn-818's page: its "Fails if" line is whole, its out-of-scope names /update-plan, and it says the play is built.
- **Plan 717** marks #896 Done; the install record follows the reinstall.

### How it was checked

All 10 /shape-plan test files pass (124 checks). The play linter passes. The component linter finds nothing in /shape-plan. Run live on this repo: plans 717 and 788 stop with the pointer to /update-plan; a number with no plan goes on.

The scripts' code that brought an existing plan up to date is left in place and is no longer reached; taking it out is a later clean-up.

### Self-review

# Self-review: #896 (/shape-plan stops when the business intent already has a plan)

Rules: `~/.phoenix/core/memory/standards/rules/self-review.md` (base, no project override; resolution in `.garura/project/issues/896/context/resolved-rules.json`).
Branch: `plan/717/896-shape-plan-stops-on-existing-plan`. Base: `plan/717/base` (PR #1003). Pattern: plan-story branch under plan 717.
Size: 18 commits, 86 files, +7169 / -115. Outside the issue's own short-term memory folders (STM): 12 files, +324 / -115. The rest, 74 files, is run records, copies and review output under `.garura/project/issues/`.

Informational only. This is not the approve/reject gate (that is check-change).

## Suggested PR title

```
feat(shape-plan): stop at pre-flight when the intent already has a plan and point to /update-plan (#896)
```

## Context detected

| Group | Files |
|-------|-------|
| Play source (SKILL.md, ICE) | `core/components/plays/shape-plan/SKILL.md`, `core/components/plays/shape-plan/reference/ice.md` |
| Code and tests | `core/components/plays/shape-plan/scripts/check_plan_absent.py`, `core/components/plays/shape-plan/scripts/test_check_plan_absent.py` |
| Neighbouring play and memory rule (wording) | `core/components/plays/shape-slice/SKILL.md`, `core/components/memory/standards/rules/pipeline-next.md` |
| Decision records | `docs/adr/063-shape-plan-makes-the-plan-once-and-update-plan-changes-a-plan-that-exists.md` (new), `docs/adr/049-a-slice-is-shaped-then-planned-then-given-its-eval.md` (status line), `docs/adr/_index.md` |
| Product model | `.garura/product/product-os/software-delivery-planning/cap-718/fn-818/feature.md` |
| Plan | `.garura/project/plans/717.yaml` |
| Install record | `.garura/install-manifest.json` |
| STM run records | `.garura/project/issues/896/**` and `.garura/project/issues/_adr/20261031T051608Z/**` (74 files) |

Commit types: chore 12, docs 2, feat 1, fix 3. Every subject is `type(scope): ...` and carries `(#896)`.

## Scope checks

| Check | Status | Evidence |
|-------|--------|----------|
| Matches the issue | PASS | The scope of #896 is the pre-flight stop that points to /update-plan, ADR 063 recording it, and the round-1 review wording fixes. Each maps: the check script, its tests, the ICE and compiled play (feat `d81b0209`); fn-818's ICE lines (`ba7cb1ab`, `52399526`); plan 717 marking #896 Done (`fcf539f9`); ADR 063 with the ADR 049 amendment line and the index row (`3528803b`); wording in shape-plan (`faf0afc0`), and in shape-slice and the Next-line map in pipeline-next (`64b70298`). |
| No scope creep | PASS | Outside STM, every file is the play, its neighbour's Next step, its model feature, the plan, the decision records or the install record. The `ontology.md` copy under `_adr/.../context/memory/` is a run copy, not an edit to the ontology. |
| Reasonable size | REVIEW | Real change is small: 12 files, +324 / -115 (the new script 70 lines, its tests 75, ADR 063 67). The headline +7169 is mostly STM records and copies: the review diff copy (about 1141 lines), an ontology copy (892 lines) and the ADR run folder. A reviewer should read the 12 files and skip `.garura/project/issues/`. |
| No stray artifacts | REVIEW | No debug prints beyond the script's intended output, no commented-out blocks, no TODO/FIXME in the diff. Run copies (the ontology and ADR template copies, the review `pr.diff`, lint output) are committed under `.garura/project/issues/`; this is the repo's STM-evidence practice, but a person may judge the review `pr.diff` copy noise. |

## Quality checks

| Check | Status | Evidence |
|-------|--------|----------|
| Tests present | PASS | `test_check_plan_absent.py` has 5 cases (no plan: go on; plan in checkout and on main: stop and name /update-plan; plan on main only; plan in checkout only; non-digit ID refused). Run result: 5 passed, 0 failed. |
| Commits are clean | PASS | 18 of 18 subjects are conventional and carry `(#896)`. Each is one concern: play, model lines, plan, ADR, wording fixes, install record, STM records. |
| No secrets | PASS | Scan of the non-STM diff for key, token, password and key-file patterns found none; no `.pem`, `.key` or `.env` files; no absolute user paths added. |
| Docs in step | PASS | The play description, constraints, failure condition, scenario and recovery, fn-818's ICE and acceptance lines, shape-slice's Next Steps, the Next-line map, ADR 063 and the ADR 049 status line all say the play stops and points to /update-plan. |
| Nothing obviously broken | REVIEW | Merge check against the base is clean (no conflicts). `node core/tools/lint-components/index.js --target core/components` from the repo root reports 36 errors and 1 warning; none name shape-plan, shape-slice or pipeline-next, so they come from other parts of the tree. The plan file parses as YAML. Two open notes below. |

## Notes for the reviewer

1. Dead text left on purpose: `core/components/plays/shape-plan/SKILL.md` still describes the work-items script's `use`, `add-sections` and `move_out` actions and the `misplaced` handling (SE-4 and SE-19, around the work-items step). The text itself says this play does not reach them, because a run now starts with no plan file. The design leaves their removal for later; a follow-up issue would stop the play text and the scripts from drifting.
2. ADR 063 names one owed item: the ontology's Plan kind and Q30 still need a change through `/edit-ontology`. It is not in this diff, by design. Confirm it is tracked (the ADR's "Work This Creates").
3. `.garura/install-manifest.json` changes only the Phoenix memory version string. It is the harness reinstall record, not a hand edit of any deployed file.

## Blocking issues

None.

## Readiness

- Ready: yes
- Blocking count: 0
- Review required: 3 (size noise from STM records, stray-artifact judgment on committed copies, the lint and left-over-text notes)
- Recommendation: keep PR #1003 against `plan/717/base`.

```yaml
analysis:
  branch: plan/717/896-shape-plan-stops-on-existing-plan
  base: plan/717/base
  suggested_title: "feat(shape-plan): stop at pre-flight when the intent already has a plan and point to /update-plan (#896)"
  context:
    file_patterns_matched: [code, tests, documentation, adr, product-model, plan, stm-evidence]
    commit_types: [feat, fix, docs, chore]
  checklist:
    must_have:
      - {item: "Matches the issue", status: PASS}
      - {item: "No scope creep", status: PASS}
      - {item: "Tests present", status: PASS, evidence: "5 passed, 0 failed"}
      - {item: "No secrets", status: PASS}
      - {item: "Commits are clean", status: PASS}
      - {item: "No merge conflicts", status: PASS}
      - {item: "Nothing obviously broken", status: REVIEW, evidence: "36 lint errors in the tree, none in the changed parts; left-over text noted"}
    nice_to_have:
      - {item: "Reasonable size", status: REVIEW, evidence: "12 real files, +324/-115; the rest is STM records"}
      - {item: "No stray artifacts", status: REVIEW, evidence: "run copies committed under the issue folders"}
      - {item: "Docs in step", status: PASS}
  blocking_issues: []
  ready: true
  recommendation: "Create PR"
```
