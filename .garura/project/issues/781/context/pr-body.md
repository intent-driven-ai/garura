Four small fixes from the round 2 review of PR #780 (the edit-ontology play). Text only; no play guarantee changes, so these are direct edits.

## What changes

- **edit-ontology, close:** the delivery report leaves out the Next line, because the play is `meta_exempt` and has no entry in the Next-line map.
- **author-product-ontology:** the Input table names each stage's draft (`draft`, `questions`, `kinds`, `links`), and the Output says what each stage returns.
- **product-os-keeper:** a mapping row for "change the product ontology" → `author-product-ontology`, run one stage at a time by /edit-ontology.
- **pipeline-position rule:** states the condition — a meta play that opens and lands its own change is `both` — instead of naming /edit-ontology as the exception.

## Checks

| Check | Result |
|---|---|
| `lint_play.py` on edit-ontology | PASS, 0 gaps |
| Component linter | 121 errors before and after; no new error |
| Linter tests | naming and skill-invocable tests pass |

## Not in this PR

The issue's fifth item — copy in the fixed `preflight.py` from plan #717 — waits until plan #717's fix reaches this branch.

## Self-review

# Self-review: #781 (edit-ontology review notes)

Rules: the base self-review rules, as recorded in resolved-rules.json (not an override).
Diff reviewed: plan/756/base...HEAD. Informational only; not the approve/reject gate.

Blocking findings: none.

## Scope checks

- Matches the issue: PASS. The four text changes are the four done-when items:
  - edit-ontology C2 leaves the Next line out, with the reason (meta_exempt, not in the Next-line map).
  - author-product-ontology names each stage's draft input and output (draft, questions, kinds, links; draft or paths returned).
  - product-os-keeper has a mapping row for changing the product ontology.
  - pipeline-position.md states the condition ("a meta play that opens and lands its own change") in both places, not the play's name as the exception.
- No scope creep: PASS. Four source files plus the issue's own working notes. The fifth item (re-copy the fixed preflight.py from plan #717) is deliberately left out because that fix has not reached this branch; recorded here so it is not read as a miss.
- Reasonable size: PASS. About 20 changed lines of source across 4 files.
- No stray artifacts: PASS. No debug output or scratch files. The working notes under the issue's context folder are the expected short-term memory record. resolved-rules.json is untracked and still to be committed with the run record; left unchanged as instructed.

## Quality checks

- Tests present: PASS (not needed). Prose-only edits. lint_play on edit-ontology: 0 gaps (as reported). Component linter: 121 errors before and after, no new error (as reported; not re-run here).
- Commits are clean: PASS. Six commits since the base: conventional format, one concern each, each references #781.
- No secrets: PASS. Scanned the diff for key and token patterns; none.
- Docs in step: PASS. The pipeline-position change keeps the list entry for edit-ontology (still `both`) and the linter note consistent with each other.
- Nothing obviously broken: PASS, with one note (non-blocking). edit-ontology step C2 still renders a "Next Steps" section; this is a different block from the Next line and is consistent with the change.
- No real names, no absolute local paths in the diff: PASS.

## Where it lands

Into `plan/756/base`. Closes #781 (closed by merge-change, because the host closes issues only on main). Part of #776, #756.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
