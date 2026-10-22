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

## Self-review


Rules: ~/.garura/core/memory/standards/rules/self-review.md (base, not an override).
Informational only. No blocking findings.

## Scope checks
- PASS Matches the issue. The diff holds the new edit-ontology play, the #778 fix (author-product-ontology made non-user-invocable, skills.md, new lint rule) and the install-garura entry. Each maps to #777 or #778.
- PASS No scope creep. The install-garura wording change (meta-utility -> harness-only) follows from #778. The pipeline-next.md line is the meta_exempt listing for the new play.
- REVIEW Size. 25 files, about 1,600 added lines, mostly the new play (compiled SKILL.md 378 lines, ICE, 6 scripts + test). Large but one cohesive unit and split into three coherent commits; fine to review play-by-play.
- PASS No stray artifacts. No commented-out blocks or scratch files. print() calls in the play scripts are intentional JSON output. The .garura/project/issues/777/context files are the normal STM record.
- NOTE Untracked resolved-rules.json is this review's input and not part of the diff.

## Quality checks
- PASS Tests present. New play scripts have test_edit_ontology_scripts.py; the new lint rule has skill-invocable.test.js; install has test_edit_ontology_goes_to_harness_repos_only. Reported: all 41 suites pass.
- PASS Commits clean. Three feat/fix commits in conventional format, each tagged (#777), plus chore(stm) record commits.
- PASS No secrets. Grep of the new play for key/secret/token found only prose about token spend, no credentials.
- PASS Docs in step. skills.md drops the meta-utility exception and updates the frontmatter table; install-garura SKILL.md and install.py wording updated.
- PASS Nothing obviously broken. No TODO/FIXME in the new play. Lint-components shows the same 121 older errors and 2 warnings as main (none new). Old-name check: 0.

## Observations (non-blocking)
- Old "meta-utility" wording remains only in past issue records under .garura/project/issues, which are history and should stay.
- The new lint rule checks both `user-invocable` and the misspelling `user-invokable`; good.

Blocking findings: none.

## Where it lands

Into `plan/756/base`. The first real run of the play is #758 (the ICE as its own kind).

Closes #777 and #778 (closed by merge-change, because the host closes issues only on main). Part of #776, #756.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
