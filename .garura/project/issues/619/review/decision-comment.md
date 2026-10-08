**Harness verdict (gate off per gates.plays.review-change): APPROVE — after three rounds**

- **Round 1:** 35 findings (1 P2, 17 P3, 17 P4). All fixed: issue reads keep type, parent, children and full text; an older gh falls back instead of failing; the plan check matches whole issue numbers; the template became `work-plan.md` with its rules in `rules/work-plan.md`; the agent, skill, docs and ADRs were aligned.
- **Round 2:** 30 confirmed fixed; 7 new small items (0 P1/P2). All fixed.
- **Round 3:** 6 of 8 confirmed fixed; 5 small P4 items left — finished plan items now keep their number so `serves_item` is checked exactly, the GitLab path of the version probe is tested, and three wordings corrected. All fixed.

Final checks on the branch: adapter tests 37/37, plan-check tests 27/27, ruff clean on every changed file, the four `platform_adapter.py` copies identical, component lint unchanged from main (113), both real plans valid.

Not in this PR: E741 lint in `preflight.py` and `session_stamp.py` (pre-existing); deploying the new files to `~/.garura` needs `/install-garura` after merge.
