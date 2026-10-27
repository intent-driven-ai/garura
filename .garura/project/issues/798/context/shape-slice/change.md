# The person's change (run 3)

The source: the review of PR #900, round 2 (`.garura/project/issues/798/review/decision.yaml` and `decision-comment.md`). The product owner's words, 2026-10-27: "Defect 1: lock it. 2, 3, and 4: you fix it."

The slice sl-intent-to-design and every model page stay as run 2 left them. Only the hidden file changes, in the "who fixes" lines below. Draft the entries of fn-818 and fn-898 again (`--redraft fn-818 --redraft fn-898`), and keep the meaning of every other recovery.

1. Defect 2. fn-818's fixes for F8 and F11 catch a story that holds a failure line the builder must never see. They go back to "a person must decide": the builder must not edit the stories it builds against after it has read a leaked line.
2. Defect 3. fn-818's fixes for F10 (make tracker issues "after the product owner's yes") and F7 (write a missing story) go to "a person must decide": both need the product owner's yes.
3. Defect 4. fn-898's fix for F24 ("the eval checks something the intent does not ask for") goes to "a person must decide", the same as F17 of fn-798. fn-898's fix for F25 names neither the eval nor the hidden file (fn-898 builds the two checks that catch a build reading the evals, not the eval), or it goes to a person.

The rule for naming things in a fix (the product owner's answer, question Q-recovery-1-4 of #798): a fix given to the builder may name what the feature itself builds; it never names the test that found the failure.
