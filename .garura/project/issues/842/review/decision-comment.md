Reviewer verdict (human): approve

Round 2 of the review. All five round-1 findings are fixed (DF-1, DF-2, DF-3, Q-1, Q-2). The product owner's rule holds: in every agent step of /shape-slice the agent only gathers context, and a named skill does the work.

Checks: hidden acceptance checks 66 of 66; play script tests 313 pass; lint_play pass, 0 gaps; write guard copies the same as the source; no lint error in this change's files.

Four new P4 findings. The product owner decided to leave them as they are ("approved ignore the p4s"):
- DF-4: the skills_used row in the play's metadata puts "built for this play" in a bracket after author-failure-recovery.
- M-1: naming.md rule 2 repeats "Epic and slice are model words." and gives no example of a dropped word.
- PM-1: fn-818's acceptance line could say "an entry for each feature, with the story that delivers it".
- Q-3: record_questions.py writes the question record with a plain write, not the safe write.

Next: merge-change, on the product owner's typed "merge".
