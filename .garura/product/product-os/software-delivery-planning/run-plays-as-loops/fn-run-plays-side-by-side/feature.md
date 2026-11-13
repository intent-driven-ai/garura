# Feature: Run a round's plays side by side

## What it does
The plays of one round run at the same time, each writing its own kind, instead of one after another, but only when the round meets every condition of the rule for fan-out with scoped writes. When it does not, the round runs its plays in turn, as today. So a round with several plays takes less time, and its result is the same.
- The rule is Garura's rule for running work at once while each part writes the product model, the scoped-write fan-out. It allows it "only when all five hold":
  - Each play has its own write scope, fixed before any play starts and checked by a script: no two scopes are the same, and "none sits inside another".
  - No play writes a shared file, a file that holds more than its own part, such as the spine, the profile, the decisions or an index. Each play puts its shared-file changes in its own record, and one persist writes them after every play has finished.
  - Each play's own records go to a path of its own.
  - No play reads another play's output.
  - The model is clean when the round starts. After the plays finish and the persist runs, the scoped-write guard checks the round's whole change against the declared scopes and the persist's shared files, and nothing is committed before the checks pass. No play runs git.
- The round waits for every play to finish before anything reads their output: the round's record, the step that closes the model's gaps, and the next round. The outputs are taken in the plays' order, so the round gives the same result whether its plays ran at once or in turn.
- A round that runs its plays at once says so by name, with each play's write scope, that no play writes a shared file, and where the plays join, as the rule asks of every fan-out.
- The shared run already holds one of the five: no play takes another play's output as its input. It names this feature as the next step: side by side comes once the scoped-write guard can tell two plays' writes apart.
- The Discovery loop's round does not meet two of the five today:
  - A domain's folder holds its capabilities' folders, so the domain play's scope would hold the capability play's scope, and the first condition fails.
  - The domain play and the capability play each write the spine through their own persist, so the second condition fails.
- The rule does not cover building code side by side. Plays that may touch the same files need a worktree each: a parallel build loop, with worktree isolation, is planned for that, and so are play chains that run on their own in parallel worktrees.
- Examples, in different kinds of project:
  - In a clinic's booking app, a round of the Discovery loop runs its three plays in turn, because the domain play's folder holds the capability play's folders and both of them write the spine.
  - In a shop's checkout project, a round whose two plays each write only their own pages, and leave their spine changes in their own records for one persist after the join, runs both plays at once and gives the same result as in turn.
  - In a bank's payments service, a round whose plays write code runs in turn; building code side by side waits for the worktrees of the planned parallel build loop.
- How it meets the capability: a loop runs its plays in rounds until the goal is met. Running a round's plays at once makes each round shorter, and the result stays what it would be in turn.

Status: not built. Today "The first build runs the plays one after another, in turn". Building code side by side is planned elsewhere: a parallel build loop, with worktree isolation, and self-contained play chains with parallel worktrees. Not built, or open:
- The scoped-write guard is built inside plays, for one step's work, such as /discover-capabilities; the shared run does not use it for a round.
- No loop's round meets the five conditions today, and no round says that it runs its plays at once.

## Inputs / Outputs
- In: the round's plays, each with its declared write scope, its own output paths, and its shared-file changes in a record of its own.
- In: the five conditions of the rule, checked before any play starts.
- Out: when all five hold, each play's pages, written at the same time, each inside its own scope; the shared files, written once after the join; and the guard's report on the round's whole change.
- Out: when any condition fails, the plays run one after another, as today.

## Rules & behavior
- At once only when all five conditions hold. The reason: the rule allows it "only when all five hold".
- Otherwise in turn. The reason: "If any condition fails, the step stays serial".
- The conditions are checked, not judged. The reason: "The conditions are a checklist the step declares, not a judgment call."
- No play's scope sits inside another's. The reason: the scopes are checked to be distinct, and "none sits inside another".
- Shared files are written once, after the join. The reason: "ONE keyed persist writes them after the join".
- The round waits for every play. The reason: "No later step ever sees a partial set."
- The result is the same at once or in turn. The reason: "Concurrency changes only timing, never the outcome."
- The round's whole change is checked after the join. The reason: the guard "checks the whole delta against the union of the declared scopes plus the persist's shared files", and fails the run "if any changed model path falls outside the run's declared write scope".
- No play reads another's output. The reason: "No play takes another play's output as its input".
- Building code at once is not in this rule. The reason: "Parallel code-building, where sub-tasks may touch the same files and need worktree isolation, is [a parallel build loop with worktree isolation] and is NOT covered here."
- Not decided: whether running a round's plays at once is worth it for a round that writes the product model.
- Not decided: how a play that writes many parts declares its write scope.

## Acceptance criteria
- Given a round whose plays meet all five conditions, when it runs, then its plays run at the same time, and nothing reads their output before every play has finished. This is not built.
- Given a round where one play's write scope sits inside another's, when it runs, then its plays run one after another. This is not built.
- Given a round whose plays ran at once, when they have all finished, then the shared files are written once, and the guard checks the round's whole change before anything is committed. This is not built.
- Given the same round run at once and in turn, when the two results are compared, then they are the same. This is not built.

## Out of scope
- How a round is run and decided. Run any loop the same way (fn-run-loop) does it.
- Building code side by side, each part in its own worktree. Design → Code (BI-3) owns them.
- The rule for fan-out and the scoped-write guard, as standards. Standards, in Standards, structure, settings and memory (BI-10), owns them.
- What each play writes. The transition intents, Product → Spec (BI-1), Spec → Design (BI-2), Design → Code (BI-3), Code → Validation (BI-4), Validation → Run (BI-5) and Run → Product (BI-6), own them.
- The link rules of the step that closes the model's gaps after the round. Manage the model, in Product model, owns them.

## Sources
- The product owner on 2026-11-10: "Run plays as loops: A person gives one goal, and a loop runs its plays until the goal is met."
- core/components/loops/_shared/loop-run.md, lines 153-159: "No play takes another play's output as its input", "The first build runs the plays one after another, in turn; side by side comes once the scoped-write guard can tell two plays' writes apart."
- standards/rules/concurrent-fanout.md, in Phoenix memory, lines 3-10, 26-51, 61-71 and 92-98: "a single step may run several independent sub-tasks at once", "Parallel code-building, where sub-tasks may touch the same files and need worktree isolation, is [a parallel build loop with worktree isolation] and is NOT covered here.", "If any condition fails, the step stays serial", "The conditions are a checklist the step declares, not a judgment call.", "only when all five hold", "the folder of the one node it owns (e.g. `product-os/<domain>/<capability>/`)", "none sits inside another", "the spine `_spine.yaml`, the profile, decisions, any index", "ONE keyed persist writes them after the join", "checks the whole delta against the union of the declared scopes plus the persist's shared files", "No sub-task runs git.", "No later step ever sees a partial set.", "Concurrency changes only timing, never the outcome.", "A scoped-write fan-out says so by name"
- core/components/plays/discover-capabilities/scripts/scoped_write_guard.py, lines 8-10: "if any changed model path falls outside the run's declared write scope"
- core/components/plays/discover-domains/SKILL.md, lines 37-38: "Every shared-file mutation (the spine `_spine.yaml` with its `profile` block, and the intent pages' Touches lists) is done by the deterministic keyed persist script"
- core/components/plays/discover-capabilities/SKILL.md, lines 35-36: "every shared-file mutation (the spine `_spine.yaml`, the profile, the box-move decisions) is done by the deterministic keyed persist script"
- The BI-9 research: "[a planned build loop] (parallel build loop with worktree isolation) and [a planned change to play chains] (self-contained play chains with parallel worktrees), both under BI-3."
