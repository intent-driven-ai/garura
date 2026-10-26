## Summary

Closes #798. The eval play, `/shape-eval`, the third play of the shaping loop (ADR 049): for each slice of a business intent's plan it reads only the epic, its stories and the slice's hidden file, and writes the slice's eval in Gherkin — one story file per story (`eval.<feature-id>.feature.md`, its Gherkin Feature is the story) and one slice file (`eval.<slice-id>.md`). Every step is a sentence of the step library of the slice's surface kind and every Then is exact, so the eval later runs with no agent and no score; an eval is a fixed yardstick. The product owner sees a short summary, never the eval.

In the same change (one pipeline run, each issue in its own place):

- **The eval format as a standard** — the story and slice templates and the command-line step library; promoted to Phoenix memory (`intent-driven-ai/phoenix-memory` 7671173). **ADR 057** records it and amends ADR 049 (the evals are not encrypted; #828 was dropped). The IDD principles page is updated to match.
- **The agent `evals-engineer`** now has one job (check the copies, call `author-slice-eval`); its /build-epic and encrypted parts are gone. The new skill `author-slice-eval` writes every scenario.
- **Four /shape-slice fixes (story #795):** a plain yes accepts only a question with a proposed answer and never overwrites a typed answer (P2); the Touches list keeps every line a person wrote, in all six copies of the shared module (P2); a reshaped kept slice's record takes the new outcome and tester action, listed as differences (P2); a brief shown again shows the person's answer (P3). Each with tests that fail on the old code.
- **The slice gains fn-898 (#898)** through `/shape-slice 788`, the model repaired with the play's own recovery, and `/shape-plan 788` gave #898 its scope of work and put it on epic #794's map.
- **The first eval:** `/shape-eval 788` wrote `plans/788/evals/intent-to-design/` — 4 story files, 43 scenarios, 6 untestable items named with their reasons. The run found two bugs in the play's own checks, fixed with tests.
- The Next map hands `/shape-plan` to `/shape-eval`; the install list gains the play, its skill and its agent.

Size: 217 files; about 159 are run records under `.garura/project/issues/`, about 58 are the change itself.

Not in this change: #898's checks (no build is given the eval; flag a build session that read it) — set aside by the product owner; running the eval (#819). Filed along the way: #899 (work across Garura's repositories in one change).

## Self-review

# Self-review — #798 (/shape-eval)

Branch `plan/788/798-shape-eval` against `plan/788/base` (`git diff plan/788/base...HEAD`).
Rules: `/Users/kapilahuja/.garura/core/memory/standards/rules/self-review.md` (base file, no project override; see `resolved-rules.json`).
This review is informational. It is not the approve/reject gate; `check-change` owns that.

Blocking findings: none.

## What the change holds

23 commits, 217 files, +14,970 / -209 lines. 159 of the files (about 10,160 added lines) are run records kept in `.garura/project/issues/`. The other 58 files (about 4,800 added lines) are the real change:

- the new /shape-eval play, with 13 scripts, its ICE, its stop condition and a test file
- the author-slice-eval skill, and the evals-engineer agent cut to one job
- the eval format standard: story and slice templates, and the command-line step library
- ADR 057, which amends ADR 049, and the matching edits to `idd-principles.md` and the ADR index
- four /shape-slice script fixes (story #795)
- the shared Touches module fix in six copies
- the model repair for business intent #788, the slice sl-intent-to-design and its new feature fn-898 (#898), and the plan file
- the first eval of plan 788 (four story files, the slice file, the failure-and-recovery file)
- the pipeline hand-off: `pipeline-next.md` and the install list in `install.py`

## Scope checks

- Matches the issue: PASS. Every non-record file maps to one of the items the change names (#798, #795, #898). Nothing else rides along. Three commits cite #795 or #898 instead of #798 because they are the child stories folded into this one change.
- No scope creep: PASS. The six `intent_touches.py` copies have the same checksum (6fd2af28...), so the fix is the same in all six. The `install.py` edit adds only the three new parts (play, skill, agent).
- Reasonable size: REVIEW. The diff is large in raw lines, but about 70% is run records, and the rest follows the one new play. A reviewer should read the 58 real files and skim the records. Suggest the PR description says so.
- No stray artifacts: PASS. No debug prints, no backup or temp files and no `__pycache__` are tracked. The matches for "token" in the diff are words in the prose, not credentials. One file is left over untracked: `.garura/project/issues/798/context/resolved-rules.json`. It is this run's own record and the play commits it with the self-review.

## Quality checks

- Tests present: PASS. All the test files that cover changed code were run, none failed: the shape-eval scripts (34 checks), `test_persist_slice.py` (100), `test_render_brief.py` (29), `test_shape_slice_scripts.py` (124), `test_intent_touches.py` (21). The shape-eval tests cover the scripts only. The play's end-to-end run is shown by the run records and the first eval of plan 788, not by a test.
- Commits are clean: PASS. Every subject is conventional (`feat`, `fix`, `docs`, `chore`) with a scope and an issue number. Each commit is one concern (ADR, templates, play, skill and agent, fixes, model, records).
- No secrets: PASS. The scan for keys, tokens and private-key headers over the non-record diff found nothing.
- Docs in step: PASS. ADR 057 is written (Accepted) and listed in the ADR index. ADR 049's status line now says what 057 amends. `idd-principles.md` no longer says the evals are encrypted. `pipeline-next.md` points /shape-plan on to /shape-eval. The install manifest lists the three new parts.
- Nothing obviously broken: PASS. The component linter (`node core/tools/lint-components/index.js --target core/components`, from the repo root) reports 36 errors, but none in a file this change touches; they are in older parts. All four changed YAML files parse. No merge conflict with the base (`git merge-tree` wrote a tree).

## Notes for the reviewer

- The linter's 36 old errors are not caused by this change and not fixed by it.
- ADR 057 amends only three named places in ADR 049 (the sentence on encrypting evals, the "Until #828" risk and the #828 work item). #828 was dropped from the plan in this change.
