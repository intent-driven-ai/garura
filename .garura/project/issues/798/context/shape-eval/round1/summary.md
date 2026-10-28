## Eval for "The shaping loop turns a business intent into a testable slice, its plan and its eval" (slice sl-intent-to-design, epic #794)

This eval checks, from the outside, that the 4 stories of this slice do what they promise and that none of their 25 failure conditions happens: 32 scenarios, each pass or fail, and 19 item(s) it cannot test yet. In the table, 2/3 means two of the story's three lines have a scenario.

| Story | Scenarios | Goals | Expectations | Failure conditions | Untestable |
|---|---|---|---|---|---|
| #795 /shape-slice grills within the tier and assembles the slice that delivers the business intent | 10 | 3/3 | 3/3 | 6/6 | 4 |
| #818 The plan play makes the plan file, the epic and one story per feature | 7 | 3/3 | 2/3 | 7/7 | 2 |
| #798 The eval play writes the slice's eval: is the business intent met, tested on the slice's surface | 8 | 3/3 | 2/2 | 6/6 | 5 |
| #898 Agents build for the business intent, not only to pass the eval: the build is given the intent, never the eval | 7 | 2/4 | 2/3 | 4/6 | 8 |

Untestable (19):
- #795 goal-2 (partly tested): A person walking through every feature of the slice on its surface needs the features built. This eval is written before the build, so it checks only the slice record: one surface and one tester.
- #795 goal-3 (partly tested): That each entry ends with exactly one way back needs a count of lines inside a Markdown file. The step library has no step that counts them.
- #795 F3 (partly tested): A failure line with no recovery, or with two recoveries, needs the same count of lines. The step library has no step for it. The scenario checks that the hidden file exists and holds the failure and recovery parts of each feature.
- #795 expectation-3 (partly tested): The words say a run on a real business intent. This eval runs in a test project, not on the real intent #788. The scenario for `@F1` checks the same result in the test project.
- #818 expectation-2 (partly tested): The scenario checks the section names, the labels Way back and Who fixes, and the Fails if lines. It does not compare a story with every other line of the hidden file. The step library has no step for that.
- #818 expectation-3: It needs the real business intent #717, its partner and the trees filed by hand on 2026-10-21. This eval runs in a test project that has none of them.
- #798 goal-2 (partly tested): The scenario checks that each tag is in each story file. It cannot tell a tag on a scenario from a tag on an Untestable line, because the step library has no step for that. It does not check that each scenario does the right thing.
- #798 F14 (partly tested): Same reason as for `@goal-2`: a tag on an Untestable line also counts as present.
- #798 F15 (partly tested): The stories do not say where a handoff plan is written or what it is called. The scenario checks the eval's own files for recovery text and for the failure conditions. It does not check a handoff plan.
- #798 F17 (partly tested): A scenario that checks something the business intent does not ask for needs a person to judge it. The scenario checks only that no tag from outside the story is in a story file.
- #798 F19 (partly tested): A build session that read the evals folder, and the flag in that build run's evidence, need a build. This slice does not run a build (#819). The scenario checks only the inputs of the build plays.
- #898 goal-1 (partly tested): A build skill, a build agent or a context sub-agent that a build starts is given its inputs when the build runs. This slice does not run a build (#819). The scenarios check the inputs of the build plays only.
- #898 goal-2: A build is given the business intent through the slice's stories only when a build runs. This slice does not run a build (#819).
- #898 goal-3: A build session that read the evals folder, and the flag in that build run's evidence, need a build session. This slice does not run a build (#819).
- #898 expectation-2: The test of the session-ledger check needs a build session and its ledger. This slice does not run a build (#819).
- #898 F21: A build session that read the plan's evals folder, and the flag in that build run's evidence, need a build session. This slice does not run a build (#819).
- #898 F22: A clean build session and a stopped build need a build session. This slice does not run a build (#819).
- #898 F23 (partly tested): A build session that read the evals folder, and the flag in that build run's evidence, need a build session. This slice does not run a build (#819). The scenario for `@F23` checks only the inputs of the build plays.
- #898 F24 (partly tested): A scenario that checks something the business intent does not ask for needs a person to judge it. The scenario checks only that no tag from outside the story is in a story file.

The files: .garura/project/plans/788/evals/intent-to-design/ (open them for the detail).
