Reviewer verdict (human, gate on): approve

PR #786, round 1. Recommended verdict: approve (no P1 findings; 5 P3, 12 P4).

Checks: test_lint_ice 14 passed; test_lint_grounding 36 passed (12 copies identical); test_vision_scripts 47 passed; component linter 121 errors before and after; Garura's model lints the same before and after.

Design: the rules match ontology v6 (missing or empty part = error; thin part = no error; business-intent link = error; part with no ICE = warning; no ices list = not checked).

P3 findings, approved as they are:
1. check_ices crashes (AttributeError) on an ices item that is not a mapping, instead of reporting it.
2. A doc path is not kept inside the model root.
3. The "two ICE for one part" test accepts either of two messages.
4. No test proves check_spine calls check_ices.
5. The spine schema header still says ICE content is written inline.

Next: merge-change into plan/756/base.
