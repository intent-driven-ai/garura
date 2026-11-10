# Capability: Ship every change the same way

## Directional intent
Ship every change the same way: Every change goes from opening to merge through the same steps, with an outside review and a person's yes.
These are the product owner's words for the first capability of Developer tooling, with the self-review dropped from the agreed line: "yes, record it with self-review dropped". There is one review, after the pull request. The words this page uses:
- A change is one piece of work raised for review and merged on its own, such as a pull request on GitHub. Each change is for an issue, an item in the team's tracker that says what the work is.
- A branch is the line of work in the repository where a change is made before it is merged. A change lands on the branch it merges into.
- A plan is the tree of work items toward one business intent. While its work runs, a plan has its own branch; each issue in the plan gets a branch from it and lands back on it. A change for an issue in no plan is a one-off change, and it lands on main.
- The change plays are the five commands that do this path: /start-change opens a change, /commit-change commits it, /propose-change raises it, /check-change reviews it and /merge-change merges it. A play is a command a person or an agent types to run one piece of work from start to end. The last four also run at the end of every play and every loop that ends a piece of work; a loop is a command that runs plays in rounds until its goal is met.
- A checkpoint is a place where a play waits for a person's typed yes. A machine check is a script check that stops the play when it fails, whatever the settings say.
- The run records are the files a play writes about its own run. They are kept with the issue in short-term memory, the issue's own working folder, and they land with the change.

This capability does eight jobs:
- Open each change where it will land.
- Commit each change by concern, with its issue named and nothing sensitive.
- Raise each change for review against where it lands, after the machine checks.
- Merge each change where it lands, on the review's approval and a person's yes.
- Land a plan's branch on main with evidence that every commit on it was reviewed.
- Land several ready issues in one change.
- Scan every push for client, company and personal references.
- Keep the docs and command pages in step with each change.

The path is the same whoever starts it: a person by hand, a play at its end, or a loop at its end. In the agreed names, the work plays are ones "anyone can run".
The review between the raise and the merge is one step of this path, and it is not this capability's. Check the code against its standards, in Code → Validation, reviews each change and gives the verdict: "reviewing a change against its standards" is that capability's. This capability runs the review and its merge reads the verdict; it never judges a change.
The merge always waits for a person's typed yes. Reviewing what agents made, at the level of the outcome, is the second capability of Developer tooling, Review what agents make (Argus): a loop's run ends with that review, and the person's answers are applied before the change lands here. In the decision on that review: "The pull request only lands it. The merge stays pinned to the person."
The path works only in the project's repository and on its code host, and production is never touched.
It matters because every change that lands the same way can be traced from its issue to its merge, nothing lands without the review and a person's yes, and nothing sensitive reaches the repository. It sits in software delivery planning with Review what agents make (Argus), and the domain's first paragraph says so.

Features:
- Open each change where it will land (fn-731): a person names the change, and its issue is found or filed, its branch is cut from the branch it will land on, and its working folder is made.
- Commit each change by concern, with its issue named and nothing sensitive (fn-commit-by-concern): every changed file is committed on the change's branch in commits of one concern each, each naming its issue, and a sensitive file stops the commit.
- Raise each change for review against where it lands (fn-raise-change): after the machine checks, the branch is pushed and one pull request is opened against the branch the change will land on, naming its issue.
- Merge each change where it lands, on the review's approval and a person's yes (fn-673): once the review approved the change and a person typed yes, it is merged where its branch lands, its branch is deleted, and an issue in a plan is closed with its item set Done.
- Land a plan's branch on main with evidence that every commit was reviewed (fn-land-plan-with-evidence): when a plan pauses, its landing shows that every commit on its branch was reviewed and that the plan, its epics and the commits agree.
- Land several ready issues in one change (fn-land-several-issues): a person groups several ready issues, and one run of the path lands them all and closes each.
- Scan every push for client, company and personal references (fn-scan-every-push): every push a change play makes is scanned first, and a reference stops it.
- Keep the docs and command pages in step with each change (fn-keep-docs-in-step): a change that adds, renames, retires or changes a command brings the docs and command pages it alters, and a check fails it while they disagree.

What is not built yet:
- The self-review is still run. Today the raise has an agent review the change against the self-review rules before the pull request opens, and a script stops the raise on a blocking line of it. It is to be taken out: in the product owner's words, "one review, after the pull request". Its three hard checks, a clean tree, the issue named and nothing sensitive, stay as machine checks.
- No push is scanned for client, company or personal references, and run records still carry home-folder paths (#888, #672, #982, #914).
- When a plan's branch lands on main, nothing shows that every commit on it was reviewed (#915).
- One run of the path opens and lands one issue (#976).
- Nothing keeps the docs and command pages in step with the plays (#973, #529).
- The merge closes the item above a landed issue once every issue under it is closed, against the rule that nothing rolls up (#1014).
- Open defects in the commit's record and its clean-tree check (#537, #857, #996), and in the merge's record and recovery (#579, #583, #787).
- The path runs on GitHub. The GitLab path is written but "UNTESTED here".

### Benefit hypothesis
- Who it serves: the developer, a person or an AI agent who builds the code, who opens, commits and raises each change; the product owner, who starts a plan's work, gives each merge their yes and keeps client and personal references out of the repository; the plays and loops that end their work through this path; and Check the code against its standards, whose verdict the merge reads.
- What we believe: when every change goes through the same steps, each one can be traced from its issue to its merge, nothing lands without the review and a person's yes, and nothing sensitive reaches the repository, if the work stands on these rules:
  - One path for every change, whoever starts it.
  - Where a change lands is read from its branch and the plan files, never guessed.
  - Machine checks, not a person, hold the clean tree, the issue named and nothing sensitive.
  - The merge reads the review's verdict and waits for a person's yes.
  - Every push is scanned before it leaves the machine.
- How we will know: for one-off changes and for issues in a plan alike, every merged pull request names its issue in each commit and in the pull request, has an approval verdict and a recorded person's yes before the merge, and leaves no branch behind; no issue in a plan lands on main; and no push carries a secret, a client or company name, or a home-folder path.
  - The last is not tested today, because no push is scanned.

### Boundary (In / Out / Never)
- In: opening each change: what the person names, the issue found or filed, its branch where it will land, a plan's branch when the plan's work starts, and the issue's working folder.
- In: committing each change by concern, with its issue named and a sensitive file stopped.
- In: raising each change against where it lands, after the machine checks.
- In: running the outside review as one step, and merging on its approval and a person's yes: the branch deleted, an issue in a plan closed and its own item set Done, and the run records landed.
- In: landing a plan's branch on main whenever the plan pauses, with evidence that every commit on it was reviewed.
- In: landing several ready issues in one change.
- In: scanning every push a change play makes.
- In: keeping the docs and command pages in step with each change.
- Out: reviewing the change against its standards, the verdict, and who decides it. Check the code against its standards, in Code → Validation, owns them; this path runs the review and reads the verdict.
- Out: reviewing what agents made at the level of the outcome, in the review tool, and applying the person's answers. Review what agents make (Argus), in Developer tooling, owns it.
- Out: making and changing a plan, its items, their statuses and the order of the work, other than a landed issue's own item set Done. Turn intents into agent work, in Product → Spec, and Orchestration own them.
- Out: laying the change plays into a project. Install into a project owns it.
- Out: the plays' names, and the settings that turn each checkpoint on or off. Standards, structure, settings and memory owns them.
- Never: merge without a person's typed yes. The reason: "Merging is a decision taken with a human looking at the diff", and the merge's checkpoint is pinned: "no config value, policy, or ledger turns it off".
- Never: judge a change. The reason: "the change under review is never its own standard", and the review is Check the code against its standards'.
- Never: land an issue in a plan on main, or hold a plan's branch off main for its open work. The reason: "A plan's branch is never kept off main just because the plan is not done", and an issue in a plan lands back on its plan's branch.
- Never: commit or push a secret, or a client, company or personal reference. The reason, in the product owner's words: "No client reference and no personal reference — not in files, not in history".
- Never: commit on main, or start a change the person did not name. The reason: "Work is committed on a feature branch, never on main.", and "Nothing typed starts nothing".
- Never: touch production. The path works only in the repository and on its code host. The reason, in the product owner's words: "We are never touching production."

### Guiding rules
- One path for every change. A one-off change, an issue in a plan, a plan's own branch and a loop's run all go through the same steps, to a different branch. The reason: "every change lands the same way", in the order "all four, in order, every time."; inside a loop, "The loop opens and lands the change."
- One review, after the pull request. The reason: the product owner chose it on 2026-10-20, "one review, after the pull request", and confirmed it on 2026-11-10: "yes, record it with self-review dropped".
- The hard checks are machine checks before the pull request opens. The reason: in the product owner's words, the self-review's "hard checks (no secrets, a clean tree, the issue named) become machine checks before the pull request opens"; and a checkpoint is off only when it is "granted only in the same change that adds the replacement checks".
- Where a change lands is read, never guessed: from the branch name for the raise and the merge, and from the plan files in git for the opening. The reason: a guessed target lands an issue in a plan on main, and "Open work in a plan never holds its branch off main".
- A plan's branch lands on main whenever the plan pauses, once its review approves it; only breaking main holds it back. The reason, in the product owner's words: "start a plan with a branch, and when we want to pause a plan, merge it. branch should not be stopped to merge just because plan is not complete."
- The machine checks first, then the person. When the review has not approved, the change cannot be merged or a required check fails, the merge stops and "there is nothing to approve, so the human is not asked". The reason: a person's yes is asked only for a change that can land.
- A landed issue changes only its own item. The reason: "An item's status in a plan file follows its own GitHub issue.", and "A parent never changes because its children closed".
- What a play writes about its run lands with the change, and the merge's own records ride on the person's yes. The reason: "the bookkeeping push rides on that authorization, no second ask."
- Running a step again is safe: no second issue, branch or pull request, and a merged change is not merged twice. The reason: a step stopped part way is run again, and a second copy splits the work.
- Not decided: whether the merge's typed yes is the way past the merge's checkpoint that Orchestration's Must not asks for, or a stop kept on purpose (#992).
- Not decided: what the setting `review-pr.bypass` should do; no script reads it, and a reject always stops the merge.
- Not decided: whether the commits that reach a branch with no pull request of their own count as changes of this path: main's plan file when a plan's work starts, a plan session's commit on the plan's branch, and the merge's own run records.

## Sources
- The product owner on 2026-11-10, in .garura/project/issues/1021/context/bi-8-capability-1/page-approvals.md: "Ship every change the same way: Every change goes from opening to merge through the same steps, with a self-review, an outside review and a person's yes.", "yes, record it with self-review dropped"
- .garura/project/issues/1021/context/capabilities.md, the list set on 2026-11-10: "with the self-review dropped: one review, after the pull request", "the outside review stays BI-4's, as one step of this path"; and the note of 2026-11-09: "reviewing a change against its standards is BI-4's"
- .garura/project/issues/613/specs/plan.md, the product owner on 2026-10-20: "one review, after the pull request", "hard checks (no secrets, a clean tree, the issue named) become machine checks before the pull request opens"
- .garura/project/issues/1021/context/names.md: "Work plays: anyone can run them, under Developer tooling"
- .garura/product/product-os/intents/bi-8.md: "People judge what agents made at the level of the outcome"
- .garura/product/product-os/intents/bi-9.md: "Stop a person. Every gate has a way past it that records what's owed."
- .garura/product/product-os/software-delivery-planning/check-code-against-standards/capability.md: "A change is one piece of work raised for review and merged on its own, such as a pull request on GitHub."
- .garura/product/product-os/software-delivery-planning/build-work-test-first/capability.md: "The developer is a person or an AI agent who builds the code."
- .garura/product/product-os/software-delivery-planning/environment-setup/capability.md, the product owner on 2026-11-08: "We are never touching production."
- core/components/plays/start-change/reference/ice.md: "Nothing typed starts nothing"
- core/components/plays/commit-change/reference/ice.md: "Work is committed on a feature branch, never on main."
- core/components/plays/propose-change/scripts/resolve_target.py: "Open work in a plan never holds its branch off main"
- core/components/plays/check-change/SKILL.md: "the change under review is never its own standard"
- core/components/plays/check-change/scripts/platform_adapter.py: "UNTESTED here"
- core/components/plays/merge-change/SKILL.md: "no config value, policy, or ledger turns it off", "there is nothing to approve, so the human is not asked"
- core/components/plays/merge-change/scripts/merge_pr.py: "the bookkeeping push rides on that authorization, no second ask."
- core/components/loops/_shared/loop-run.md: "the merge keeping its pinned human approval"
- core/config.yaml: "bypass: true"
- .garura/user-provided/managing-work.md: "Merging is a decision taken with a human looking at the diff"
- docs/adr/025-level-3-redefined-skeleton-and-loop.md: "all four, in order, every time."
- docs/adr/028-agentic-lifecycle-five-loops.md: "every change lands the same way"
- docs/adr/032-drive-review-of-outcomes.md: "The pull request only lands it. The merge stays pinned to the person."
- docs/adr/060-a-plans-branch-merges-into-main-when-the-plan-pauses.md, the product owner on 2026-10-28: "start a plan with a branch, and when we want to pause a plan, merge it. branch should not be stopped to merge just because plan is not complete.", "A plan's branch is never kept off main just because the plan is not done."
- docs/adr/064-an-items-status-in-a-plan-follows-its-own-issue-with-no-roll-ups.md: "An item's status in a plan file follows its own GitHub issue.", "A parent never changes because its children closed"
- standards/rules/loop-contract.md, in Phoenix memory: "The loop opens and lands the change."
- standards/rules/gate-config.md, in Phoenix memory: "granted only in the same change that adds the replacement checks"
- GitHub #982 (open), the product owner's rule of 2026-10-18: "No client reference and no personal reference — not in files, not in history"
- GitHub #992 (open): "The harness never stops a person."
- GitHub #888, #672, #914, #915, #976, #973, #529 and #1014 (open): the planned work and the known defect named under What is not built yet.
- The stock-take of Developer tooling, .garura/project/issues/1021/context/bi-8-inventory/inventory.md, sections 1, 3, 4, 6 and 7.
- The short line beside each feature: the opening words of that feature's own page.
- Shelf: none. No knowledge shelf in any memory tier covers how a team lands a change.
- .garura/product/product-os/software-delivery-planning/domain.md: "It also lands every change the same way, with an outside review and a person's yes, and gives people one tool to review what agents made."
