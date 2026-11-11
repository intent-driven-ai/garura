# Feature: Raise each change for review against where it lands

## What it does
When a change is committed, the machine checks run first, then the branch is pushed and one pull request is opened against the branch the change will land on, naming its issue and carrying the play's run records, so the outside review can start.
- The machine checks before the pull request opens. In the product owner's words, the self-review's "hard checks (no secrets, a clean tree, the issue named) become machine checks before the pull request opens":
  - On a change's branch: never main.
  - A clean tree: every change is committed. Uncommitted work stops the raise, with nothing pushed.
  - The issue named: the pull request names its issue, as each commit already does.
  - No secrets: a sensitive file has already stopped the commit (Commit each change by concern, with its issue named and nothing sensitive). The scan of the push for client, company and personal references is Scan every push for client, company and personal references (fn-scan-every-push), which is not built.
- Where it lands, read from the branch name, never guessed:
  - an issue in a plan, `plan/<id>/<issue>-<slug>`, lands on its plan's branch, `plan/<id>/base`;
  - a plan's own branch lands on main, while the plan is still in progress;
  - a one-off change lands on main.
- The play's run records are committed before the push, so the pull request carries them and the tree stays clean.
- One pull request for each branch. A second run, such as after a fix the review asked for, updates the open pull request instead of opening another one.
- The raise's checkpoint is off by setting: no person is asked here, the machine checks carry what the person was checking, and the skip is recorded.
- The outside review is the next step, and it is not this feature's: Check the code against its standards reviews the change on the pull request.
- Examples, in different kinds of project:
  - In a shop's checkout project, a one-off fix is raised as one pull request to main.
  - In a team's planning tool, a story of a running plan is raised against the plan's branch, not main.
  - In a bank's payments service, a developer tries to raise a change with a file still uncommitted; the raise stops, and nothing is pushed.
- How it meets the capability: this is the step between the commit and the outside review: every change reaches the review as one pull request against where it lands, after the same machine checks.

Status: built, in /propose-change, with the self-review still in it:
- Today the raise first has an agent review the change against the self-review rules, and the checklist goes into the pull request. A script then stops the raise when a line of that checklist reads blocking. It is to be taken out, as the product owner chose: "one review, after the pull request". The script that reads the checklist goes with it, and the three hard checks above are the raise's named machine checks.
- No pull request template; each body is made fresh (#517).
- #452 (the raise halting on its own run records) is open, though the play now commits them before the push.
- Not built and not shaped: a check that each commit that changed a play, the ontology or a decision record has a matching play run on record. Lay Garura's guardrails with the install leaves "the check in the review of each change" to this path; #893 proposes it inside the review. Not decided: whether it runs here, as one more machine check before the pull request opens, or inside the review.

## Inputs / Outputs
- In: the committed change on its branch.
- In: the issue, read from the branch name.
- In: the branch name, which says where the change lands.
- In: any pull request already open for the branch.
- Out: the branch pushed to the code host.
- Out: one pull request against where the change lands, naming its issue, opened or updated.
- Out: the run records, committed on the branch and carried by the pull request, with the target and the pull request's number.

## Rules & behavior
- Every hard check is a machine check, and no setting turns one off. The reason: the raise's checkpoint is off, and a checkpoint is off only when it is "granted only in the same change that adds the replacement checks".
- Uncommitted work stops the raise. The reason: work left behind is not in the pull request that the review reads.
- The pull request names its issue. The reason: the review reads the change against its issue, and the merge closes it.
- The target is read from the branch name. The reason: a guessed target lands an issue in a plan on main; and "Open work in a plan never holds its branch off main", so a plan's own branch always targets main.
- One pull request for each branch. The reason: a second pull request splits the review and the record.
- No review before the pull request. The reason, in the product owner's words: "one review, after the pull request".
- The run records go with the pull request. The reason: the review and a reader later see what the play did, and the tree stays clean.

## Acceptance criteria
- Given a story's branch in a plan, when it is raised, then the pull request's target on the code host is the plan's branch.
- Given a plan's own branch, when it is raised, then the pull request's target is main and it names the plan's issue.
- Given a one-off change, when it is raised, then the pull request's target is main and it names the change's issue.
- Given uncommitted work on the branch, when the raise runs, then it stops before any push and no pull request is opened.
- Given a branch with an open pull request, when it is raised again after a fix, then the same pull request is updated and the branch has one open pull request.

## Out of scope
- Committing the work, and stopping a sensitive file. Commit each change by concern, with its issue named and nothing sensitive (fn-commit-by-concern) does it.
- Reviewing the change and giving the verdict. Check the code against its standards, in Code → Validation, does it.
- Scanning the push. Scan every push for client, company and personal references (fn-scan-every-push) does it.
- Merging. Merge each change where it lands, on the review's approval and a person's yes (fn-673) does it.

## Sources
- The product owner on 2026-10-20, in .garura/project/issues/613/specs/plan.md: "one review, after the pull request", "hard checks (no secrets, a clean tree, the issue named) become machine checks before the pull request opens"
- The product owner on 2026-11-10, in .garura/project/issues/1021/context/bi-8-capability-1/page-approvals.md: "yes, record it with self-review dropped"
- core/components/plays/propose-change/SKILL.md: "run a self-review on its scope and quality, push the branch, and open a pull request that carries that review against where the branch lands", "Working tree is clean (change is committed)", "the PR body references the issue", "this run updates it (refreshes the self-review and body) instead of opening a second one"
- core/components/plays/propose-change/scripts/resolve_target.py: "Open work in a plan never holds its branch off main"
- core/components/plays/propose-change/scripts/check_self_review.py: "machine replacement for propose-change's confirm-raise gate (#467)"
- standards/rules/gate-config.md, in Phoenix memory: "granted only in the same change that adds the replacement checks"
- standards/rules/self-review.md, in Phoenix memory: "The output is an informational checklist that travels in the PR."
- .garura/product/product-os/software-delivery-planning/install-into-project/fn-lay-guardrails/feature.md: "The run marker inside each play, and the check in the review of each change. How a play is built, and Ship every change the same way, own them."
- GitHub #517 (open): "Give pull requests a template so every raise says the same things"
- GitHub #452 (open): "propose-change halts on its own evidence files at push time"
- GitHub #893 (open): "refuses a pull request when a commit that changed a play, the ontology or an ADR has no matching play run on record"
