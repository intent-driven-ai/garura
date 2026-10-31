Harness verdict (gate off per gates.plays.check-change): reject

One blocker. Five kinds of work reviewed: the three plays (harness), the scripts, the tests, the plan tool README, and the issue's run records.

What ran: the plan tool suite (57) and start-change's suite (12) pass; ruff is clean on the 9 changed scripts; the play linter passes start-change, propose-change and merge-change; the component linter's 37 findings are all in files this change does not touch; ICE fingerprints match.

Blocker (P1):
- R-01: setup_branch.py's own test (`create-play/references/test_setup_branch.py`, a script, not a unittest module) is red — 4 checks fail and it crashes. Its scratch repo has no plan file and no plan tool, and one check expects the old push message.

To fix in this change:
- R-02 (P2): cutting a plan's branch when main's plan file already says In Progress on that branch fails on an empty commit. Plan 717's file on main reads exactly that today.
- H4 (P3, raised to fix): loops and the injected start step call start-change with no argument; "nothing typed starts nothing" may now stop them.
- H5 (P3): propose-change readies the plan file before the self-review; a later stop leaves a merge and an uncommitted plan file behind.
- H6 (P3): new Recovery rows in start-change and merge-change sit outside their tables (a blank line).
- H7 (P3): start-change's Plan path close still names issue paths and "run build next".
- plan_land.py `ready` leaves a merge half done if a later git step fails; `updated:` is not added when missing.

For the product owner (decisions):
- H1 (P2): merge-change now holds a plan's branch off main for a second reason (main's plan file changed since the raise, or no landing record). ADR 060 §4 says only breaking main holds it back — an ADR amendment, or a different rule.
- H2 (P2): an issue inside a Done or Dropped plan (a bug found later) can no longer be started, because its plan's branch is cut through the plan tool, which refuses a closed plan.
- H3 (P2): the Status and Direction question does not follow the rule for asking a person (one thing per question, an opening, examples).
- H8 (P3): no ADR records that propose-change now writes Status, Direction and the empty branch, and that the branch's plan file lands whole; ADR 061's "until #989" text is now stale.

Full list: `.garura/project/issues/989/review/findings.yaml`.
