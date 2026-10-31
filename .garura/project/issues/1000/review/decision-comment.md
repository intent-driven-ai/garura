Harness verdict (gate off per gates.plays.check-change): approve

No P1. Seven categories reviewed: the plays (harness), the memory rule pages, the scripts, the tests, the harness standard, the run records and the plan file.

What ran: every suite passes (show-plan 7; resolve_plan 23; submit_pr 3; merge_plan 10; merge_scripts 15; setup_branch 13); the 30 pre-flight copies match their main copy; ruff is clean; the play linter passes on show-plan, start-change and merge-change; the component linter's 36 errors are all there before. /show-plan's branch reading was tried on 17 branch names; the standard's new sentence matches ADR 060 decision 4.

For the product owner (P2, HC1): merge-change's "capability close" closes the top node of the plan's tree, which in a plan is the Epic. The ontology says an Epic stays open when its work is done and that nothing rolls up (#1007, ADR 064). The new check in this PR would harden that close. Decision needed before the merge.

To fix in this change:
- Q01/HC4 (P3): when the PR's number is known but the host lookup fails, on_target can still read true from the requested base. Q02: no test for that path.
- HC2 (P3): the new SE-9 wording does not match S5 and the script (every issue under it, at any level).
- Memory F-1 (P3): cut-branch keeps a word-for-word copy of git.md's old branch table.
- Small: an empty plans base-path gives no default (Q05/HC6); non-ASCII digits in a branch name (Q04); what a null on_target means is not written down (Q03/HC5); git.md's feature example and the rules index line (F-2, F-3); pipeline-position's long clause (F-4).
