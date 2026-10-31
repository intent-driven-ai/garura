## What this changes

Closes #1011.

The page of the capability #721 (start and land work against a plan) still said a plan reaches main "only when the plan is done". ADR 060 says a plan's branch lands on main whenever the plan pauses and its review approves it, even with issues of the plan still open. This changes the four lines that stated the old rule, through the model sub-agent and the page skill's named-line change, the same way the #673 page was changed in PR #1010:

- the direction line;
- the Goal;
- "Fails if": a plan's branch held off main for its open issues, or for a plan it needs;
- "Checked by": with one issue still open, the plan's branch lands on main once its review approves it, and that issue stays open.

Nothing else on the page or in the model changes. Plan 717 marks #1011 Done.

## Self-review

# Self-review: #1011 (bring the #721 capability page in line with ADR 060)

Branch: plan/717/1011-cap-721-landing-rule, checked against plan/717/base.
Rules used: the base self-review rules (standards/rules/self-review.md in Phoenix memory; no project override). Recorded in resolved-rules.json.
Method: the assess-pr skill, run on the branch diff. This review is advice. It is not the approve or reject gate.

## What the change is

Four lines of the #721 capability page now state the landing rule of ADR 060: an issue lands on its plan's branch, and the plan's branch lands on main whenever the plan pauses and its review approves it, even with issues still open. Plan 717 marks #1011 Done. The rest of the diff is run records for this issue.

## Scope checks

- Matches the issue: PASS. The four lines changed (the direction line, the Goal, "Fails if", "Checked by") are the four the approved design names, word for word.
- No scope creep: PASS. Outside the page, the plan file and the issue's own run folder, no file changed. The plan file changed in one line only (#1011 Not Started to Done), which the design asks for.
- Reasonable size: PASS. 4 lines changed on the page, 1 in the plan file. The other files are small run records.
- No stray artifacts: PASS. No scratch files or commented-out text. One run record (resolved-rules.json) is not yet committed; it belongs to this run and goes in with the run records.

## Does the page agree with the sources

- Agrees with ADR 060: PASS. The ADR decides that a plan's branch merges into main when the plan pauses, with issues still open. The page now says the same. The old wording ("only when it is done", "open issue holds it off main") is gone; a search of the page finds no trace of it.
- Agrees with the #673 feature page: PASS. The Goal, "Fails if" and "Checked by" lines say the same thing as the #673 page: no hold-back for open issues or for a plan it needs, and an open issue stays open after the landing.
- Nothing else on the page changed: PASS. The Limit line and the heading are as before.

## Quality checks

- Tests present: not needed. The change is a model page with no behavior of its own. Its "Checked by" line describes the test plan.
- Commits are clean: PASS. Five commits, all in conventional format and all naming #1011. Each is one concern: the page, the plan file, or run records.
- No secrets: PASS. The diff holds no credentials, tokens or keys.
- No absolute home paths: PASS. None in the added lines.
- Docs in step: PASS. ADR 060 and the #673 page are the sources and need no edit. No other page of the capability states the old rule.
- Nothing obviously broken: PASS. A trial merge of the branch into plan/717/base finds no conflict.

## Readiness

- Ready: yes.
- No blocking issues.
- Review required: a person should read the four changed lines once against ADR 060, because the page is the model's word on the rule.
