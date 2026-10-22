Garura gets a play for changing its product ontology, `/edit-ontology`. From now on, ontology work runs through a play, not by a person running a skill.

## What changes

- **New play `edit-ontology`** (story #777, plan #756), built with create-play from its ICE (`reference/ice.md`). It opens its own change, has `product-os-keeper` run `author-product-ontology` in four stages, and stops three times for the product owner's typed yes: the questions, the kinds, and the links and rules. Then it writes the ontology, runs `check_ontology.py` until it reads valid, runs a new change check (only the needed kinds changed, the version is up by one with one log line, no real names), and lands through the four change plays. lint_play: PASS.
- **Bug #778:** `author-product-ontology` is `user-invocable: false`, with a Stages section for the play. The "meta-utility skill" exception is removed from `docs/components/skills.md`. A new linter rule, `structural/skill-user-invocable`, fails any skill a person can start.
- **Install:** `edit-ontology` is a meta play, installed only by `--scope harness`.

## Checks

| Check | Result |
|---|---|
| New script tests (11) | written first, failed, then pass |
| New linter rule test | pass |
| All test suites (41) | pass |
| lint_play on edit-ontology | PASS, 0 gaps |
| Component linter | 121 errors and 2 warnings, the same as main |
| Old-name check | 0 |

## Review fixes (after the product owner's reject)

- `product-os-keeper` lists `author-product-ontology`, used by `/edit-ontology`.
- The skill's Input table names `stage`, `change` and `problems`.
- `standards/rules/pipeline-position.md` names `/edit-ontology` as the one meta play with position both.

## Self-review


Rules: ~/.garura/core/memory/standards/rules/self-review.md (base, not an override; see resolved-rules.json).
Reviewed: git diff origin/plan/756/base...HEAD. Informational only. No blocking findings.

## Review fixes
Product owner rejected PR #780 at check-change for three findings. All three are fixed by commit dc00dd95 (confirmed in the diff).
- PASS 1. core/components/agents/product-os-keeper.md now lists `author-product-ontology` in its skills table, used by /edit-ontology, and /edit-ontology is added to the agent description.
- PASS 2. core/components/skills/author-product-ontology/SKILL.md Input table now names `stage` (scope, kinds, links, write), `change` and `problems`.
- PASS 3. standards/rules/pipeline-position.md now lists /edit-ontology under `both` and states it is the one meta play with position both (also in the linter note).

## Scope checks
- PASS Matches the issue. The diff holds the new edit-ontology play, the #778 fix (author-product-ontology made non-user-invocable, skills.md, new lint rule), the install-garura entry, and the three review fixes. Each maps to #777 or #778.
- PASS No scope creep. The install-garura wording change follows from #778. The pipeline-next.md line is the meta_exempt listing for the new play.
- REVIEW Size. 20 source/doc files, about 1,500 added lines, mostly the new play (SKILL.md 378 lines, ICE, 6 scripts and a test). Large but one cohesive unit in four coherent commits; reviewable play by play.
- REVIEW Stray artifacts. The diff also carries about 2,000 lines of STM records under .garura/project/issues/777 (review/pr.diff, findings, decision files from the earlier check-change run). These are the normal run record, not source, but pr.diff is bulky. No commented-out blocks, debug prints or scratch files in source; print() in the play scripts is intentional JSON output.

## Quality checks
- PASS Tests present. test_edit_ontology_scripts.py, skill-invocable.test.js, and test_edit_ontology_goes_to_harness_repos_only in test_install.py.
- PASS Commits clean. Four feat/fix commits in conventional format, each tagged (#777), plus chore(stm) record commits.
- PASS No secrets. Grep of added source lines for TODO/FIXME/secret/key patterns found none (only a test helper line matching "passed").
- PASS Docs in step. skills.md, install-garura SKILL.md and install.py updated; the three fixes update the agent, skill and rules docs they affect.
- PASS Nothing obviously broken. No TODO/FIXME blockers in the new play. Working tree clean.

## Observations (non-blocking)
- Old "meta-utility" wording remains only in past issue records, which are history.
- Test and lint suites were not re-run in this review; the earlier run reported all passing, and dc00dd95 changed only prose in three files.

Blocking findings: none.

## Where it lands

Into `plan/756/base`. The first real run of the play is #758 (the ICE as its own kind).

Closes #777 and #778 (closed by merge-change, because the host closes issues only on main). Part of #776, #756.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
