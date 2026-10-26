## Eval for slice sl-intent-to-design (epic #794): 4 stories, 43 scenarios

| Story | Scenarios | Goals | Expectations | Failure conditions | Untestable |
|---|---|---|---|---|---|
| #795 /shape-slice grills within the tier and assembles the slice that delivers the business intent | 10 | 2/3 | 2/3 | 6/6 | 2 |
| #818 The plan play makes the plan file, the epic and one story per feature | 12 | 3/3 | 2/3 | 6/6 | 1 |
| #798 The eval play writes the slice's eval: is the business intent met, tested on the slice's surface | 9 | 3/3 | 2/2 | 4/6 | 2 |
| #898 Agents build for the business intent, not only to pass the eval: the build is given the intent, never the eval | 12 | 4/4 | 3/3 | 5/6 | 1 |

Untestable (6):
- #795 goal-3: the story says the hidden file's entries, each closed by exactly one way back, are not built yet (decision 6 adds them), and no library sentence counts the way-back lines of a Markdown file. That the hidden file exists and holds a recovery part is checked under `@expectation-1` and `@F3`.
- #795 expectation-2: no library sentence lists every new file of a project, so "no other new file appears outside the product model" cannot be checked as a whole. The plans folder and the evals folder are checked under `@expectation-3`.
- #818 expectation-3: the trees filed by hand on 2026-10-21 for #717 and its partner are not in the story, so no exact result can be written. The eval can compare them when the usage guide maps them.
- #798 F15: a handoff plan is written only when a check of the eval fails after the build, and this eval writes none, so there is no handoff plan to check yet.
- #798 F17: no library sentence can say that a check asks for more than the goals, expectations and failure conditions of the stories; each scenario of the story files carries the tag of the line that it covers, and a person reads the tags.
- #898 F24: no library sentence can say that a check asks for more than the goals, expectations and failure conditions of the stories; each scenario of the story files carries the tag of the line that it covers, and a person reads the tags.

The files: .garura/project/plans/788/evals/intent-to-design/ (open them for the detail).
