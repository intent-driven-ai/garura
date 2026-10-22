# Self-review: #777 (plan #756), with bug #778

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
