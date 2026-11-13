# Feature: Merge each change where it lands, on the review's approval and a person's yes

## What it does
Once the outside review approved a change, the change can be merged and a person typed yes, it is merged into the branch it lands on: the checkout moves to that branch with the latest, the change's branch is deleted, an issue in a plan is closed with its own item set Done, and the run records are committed there, so every change lands the same way and a person always says yes first.
- Where it lands, read from the branch name, never guessed:
  - an issue in a plan merges into its plan's branch;
  - a plan's own branch merges into main whenever the plan pauses, with issues of the plan still open; those issues stay open and stay in the plan;
  - a one-off change merges into main.
- The machine checks come first: the review's verdict reads approve, the change can be merged with no conflict, and no required check fails. When one of them is false, the merge stops and names it, and "the human is not asked", because there is nothing to approve.
- Then the person's typed yes. It always waits, and no setting, policy or record of earlier yeses turns it off. The merge goes ahead only on the typed yes, and the record keeps the three checks it stood on.
- The pull request's own target must be where the branch lands; otherwise nothing is merged.
- After the merge: the checkout is on the branch the change landed on, with the latest; the change's branch is deleted here and on the code host.
- An issue that landed on its plan's branch is closed by the merge, because the code host closes issues only on main, and its own item in the plan file is set Done. Only that item changes; nothing rolls up to the item above it.
- The run records of the merge are committed on the branch the change landed on and pushed, with no second question, because the person's yes on the merge already covers that bookkeeping.
- A merge run again on a change that is already merged does nothing more and ends cleanly.
- Inside a loop, the loop's end merges the same way, with the same typed yes.
- Examples, in different kinds of project:
  - In a shop's checkout project, an approved one-off fix waits for the product owner's yes, then lands on main, and its branch is gone.
  - In a clinic's booking app, an approved story of a running plan lands on the plan's branch; its issue closes and its item reads Done, while the epic above it stays open.
  - In a team's planning tool, the plan pauses with one story still open: the plan's branch is raised to main, approved and merged after the yes, and the open story stays open in the plan.
- How it meets the capability: this is the end of "from opening to merge", with "a person's yes": every change merges where it belongs, and only after the review approved it and a person said yes.

Status: built, in /merge-change, with its yes pinned. Its first form landed an issue on its plan's branch and a plan on main whenever it pauses. Setting the item Done came later (ADR 064). Not built, or open:
- The merge also closes the item above a landed issue once every issue under it is closed, such as the epic. This is against the rule that nothing rolls up, and it is a decision the product owner has not taken.
- It records an empty merge commit after a merge, stops when the change has no review folder yet, and cannot recover after an error from the code host during the merge.
- When a plan's branch lands on main, nothing shows that every commit on it was reviewed. Land a plan's branch on main with evidence that every commit was reviewed (fn-land-plan-with-evidence) adds it.

## Inputs / Outputs
- In: the change's pull request and its branch.
- In: the review's verdict and who decided it, as the review recorded it.
- In: whether the change can be merged, and the result of its required checks, from the code host.
- In: the person's typed yes or no.
- In: for an issue in a plan, the plan files.
- Out: the change merged where it lands, the checkout there with the latest, and the change's branch deleted.
- Out: for an issue in a plan, the issue closed and its own item set Done in the plan file.
- Out: the merge's record, with the three checks, the yes, whether the change merged and whether its branch is gone, committed on the branch the change landed on and pushed.

## Rules & behavior
- The person says yes to every merge, and no setting turns it off. The reason: "Merging is a decision taken with a human looking at the diff", and the land "always keeps its human beat".
- The machine checks come before the person. The reason: a person is asked only about a change that can land; when the review has not approved or the change cannot merge, "there is nothing to approve".
- The merge reads the verdict and never judges. The reason: the review is Check the code against its standards'; the merge marks a change approved only when the verdict reads approve, so a reject always stops it.
- An issue in a plan merges into its plan's branch, never main. The reason: a plan's work stays together while it runs.
- A plan's branch lands on main whenever the plan pauses, with its issues still open; plan order does not hold a plan off main. The reason: "open work is no reason to hold it off main", and the product owner's words: "branch should not be stopped to merge just because plan is not complete."
- Only breaking main holds a plan's branch back, and the machine checks guard that. The reason: the review, a clean merge and the required checks are what show main will still work.
- A landed issue changes only its own item. The reason: "An item's status in a plan file follows its own GitHub issue.", and "A parent never changes because its children closed".
- The merge's records ride on the yes. The reason: "the bookkeeping push rides on that authorization, no second ask."; a push that fails is shown as owed, never silent.
- Not decided: whether the typed yes is the way past this checkpoint that Orchestration's Must not asks for, or a stop kept on purpose.
- Not decided: what the setting `review-pr.bypass` should do; no script reads it.

## Acceptance criteria
- Given a test plan with one issue still open, when its branch is raised to main, approved and given the yes, then it lands on main, and that issue stays open and in the plan.
- Given an approved story in a plan, when the person types yes, then it lands on the plan's branch, not main, its issue is closed, its item reads Done, the item above it is unchanged, and the story's branch is gone here and on the code host.
- Given a change the review rejected, when the merge runs, then it stops, names the verdict, and does not ask the person.
- Given an approved change that cannot be merged because of a conflict, when the merge runs, then it stops and does not ask the person.
- Given an approved change, when the person types no, then nothing is merged.
- Given a change already merged, when the merge runs again, then no second merge is tried and the run ends cleanly.

## Out of scope
- The review and its verdict, and who decides it. Check the code against its standards, in Code → Validation, owns them.
- Showing that every commit on a plan's branch was reviewed when it lands on main. Land a plan's branch on main with evidence that every commit was reviewed (fn-land-plan-with-evidence) does it.
- Cutting a plan's branch again when its work starts again. Open each change where it will land (fn-731) does it.
- Changing a plan's other items, its status and its direction. Turn intents into agent work, in Product → Spec, and Orchestration own them.

## Sources
- The product owner on 2026-11-10: "Ship every change the same way: Every change goes from opening to merge through the same steps, with a self-review, an outside review and a person's yes.", "yes, record it with self-review dropped"
- core/components/plays/merge-change/SKILL.md: "no config value, policy, or ledger turns it off", "there is nothing to approve, so the human is not asked", "The merge proceeds solely on the typed approval", "only that item, no roll-up"
- core/components/plays/merge-change/reference/ice.md: "open work is no reason to hold it off main", "always presents and waits for a typed human approval"
- core/components/plays/merge-change/scripts/merge_pr.py: "because the code host closes issues only on main", "the bookkeeping push rides on that authorization, no second ask."
- core/components/plays/merge-change/scripts/read_merge_state.py: "Approved iff the review verdict decision reads approve."
- core/components/loops/_shared/loop-run.md: "the merge keeping its pinned human approval"
- standards/rules/gate-config.md, in Phoenix memory: "merging to main is the one irreversible action in the chain, so the actual land always keeps its human beat"
- .garura/user-provided/managing-work.md: "Merging is a decision taken with a human looking at the diff"
- docs/adr/060-a-plans-branch-merges-into-main-when-the-plan-pauses.md, the product owner on 2026-10-28: "branch should not be stopped to merge just because plan is not complete."
- docs/adr/064-an-items-status-in-a-plan-follows-its-own-issue-with-no-roll-ups.md: "An item's status in a plan file follows its own GitHub issue.", "A parent never changes because its children closed"
- The page this one replaces, .garura/product/product-os/features/fn-673/feature.md as it read on 2026-11-10: "An issue in a plan merges into its plan's branch.", "Plan order does not hold a plan off main."
- .garura/product/product-os/software-delivery-planning/check-code-against-standards/ice.md: "the product owner gives the merge their yes in Developer tooling."
- .garura/product/product-os/intents/bi-9.md: "Stop a person. Every gate has a way past it that records what's owed."
- core/config.yaml: "bypass: true"
