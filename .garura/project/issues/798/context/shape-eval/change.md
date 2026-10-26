# The product owner's change (run 2)

The source: the review of PR #900, round 1. The product owner's words, 2026-10-26: "fix p2 and p3s", and "yes" to the fix plan. The first eval was taken back, so this run writes the eval from new. The slice and its hidden file were shaped again before this run: the hidden file now has 25 failure lines, and some line numbers changed (the old F13 is gone; F26 and F27 are new).

Write every scenario, every Untestable reason and every Names line in plain words: short sentences, one idea each, the real names of things.

1. Cover each failure condition in full, or name the part that is not covered (SE-2). A scenario that checks only part of a "Fails if" line leaves the rest uncovered. Put the rest under Untestable with its reason. In the first eval, fn-795's story had these gaps: the epic and the story in the tracker (F1); a failure line with no recovery, or two (F3); more than one surface, and no slice written when there is no surface (F4); every "Fails if" line, not only one (F6).
2. fn-798's checks (SE-3). A check that says "each story file" must look at every story file and every tag, or say under Untestable what it does not cover.
3. The ICE name in fn-818's check (SE-4). A name defined as "the text as the plan file holds it", then checked against the plan file, compares the file with itself and can never fail. The name must stand for the ICE as the product model gives it, and must leave out the "Fails if" lines (the plan file must hold none).
4. The ledger check (SE-5). A check that the /shape-eval run's ledger "does not contain feature.md" fails on a correct run: the play's own files (the template eval-story.feature.md, the files eval.fn-795.feature.md and others) match that text. Check for the paths of the product model's ICE pages instead (under .garura/product/product-os/).
5. The slice file's Context section (SE-6). It is guidance for the running eval, not a copy of the stories' Context guidance. The stories' "never read" lines are rules for the build; in the slice file they would tell the running eval not to read itself or the hidden file, whose recovery parts it must read.
6. fn-898 stays in the slice (Q1). (Round 1 put its checks of a build session under Untestable. The product owner's round 2 change replaces that: see item 7.)

# The product owner's change at the checkpoint (round 2)

Their words, 2026-10-26: "send it back.. i dont understand why these cant be tested"

The first draft put 19 items under Untestable. Almost all of them can be tested from the outside, in the test project, with the step library as it is. Write a scenario for each one. Keep an Untestable line only when no sentence of the step library can show the result at all, and then say in one plain sentence what is missing.

7. A check of a build session needs no real build. The scenario writes the build session's record itself (Given the file "<the session's ledger>" holds "<a read of the plan's evals folder>"), runs the check ([the ledger check]), and checks the flag in the build run's evidence, or that a clean record gets no flag and the check never stops the build. Do this for every item that said "needs a build" (#898 goal-1, goal-2, goal-3, expectation-2, F21, F22, F23; #798 F19).
8. A line that names the real intent or the real project (#795 expectation-3, #818 expectation-3) is tested in the test project, like every other scenario; the usage guide sets the project up. It is not untestable.
9. "A person walks every feature of the slice" (#795 goal-2) is what the whole eval does when it runs. Cover it with a scenario that runs the three plays in order on the surface and checks each one's result.
10. A place the stories do not name (#798 F15, the handoff plan) is a [name] listed under Names; the usage guide maps it. Write the scenario with the name.
11. A count the library has no step for (#795 goal-3 and F3: one recovery for each failure line; #798 goal-2 and F14: a tag on a scenario, not only on an Untestable line): check what the library can see — for example that the file holds each failure line's "When:", "Way back:" and "Who fixes:" parts, and that a story file holds "## Scenario:" under each tag. Keep an Untestable line only for the part no step can show.
12. "The eval checks something the business intent does not ask for" (#798 F17, #898 F24): write a scenario that checks each scenario tag of each story file is a goal, an expectation or a failure line of that story (the field and file steps can show it). Keep an Untestable line only for the part that needs a person to judge.
