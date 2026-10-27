## Eval for "The shaping loop turns a business intent into a testable slice, its plan and its eval" (slice sl-intent-to-design, epic #794)

This eval checks, from the outside, that the 4 stories of this slice do what they promise and that none of their 25 failure conditions happens: 46 scenarios, each pass or fail, and 2 item(s) it cannot test yet. In the table, 2/3 means two of the story's three lines have a scenario.

| Story | Scenarios | Goals | Expectations | Failure conditions | Untestable |
|---|---|---|---|---|---|
| #795 /shape-slice grills within the tier and assembles the slice that delivers the business intent | 12 | 3/3 | 3/3 | 6/6 | 0 |
| #818 The plan play makes the plan file, the epic and one story per feature | 8 | 3/3 | 3/3 | 7/7 | 0 |
| #798 The eval play writes the slice's eval: is the business intent met, tested on the slice's surface | 12 | 3/3 | 2/2 | 6/6 | 1 |
| #898 Agents build for the business intent, not only to pass the eval: the build is given the intent, never the eval | 14 | 4/4 | 3/3 | 6/6 | 1 |

Untestable (2):
- #798 F17 (partly tested): A person must read the steps of each scenario to see if they check only what the tag says, because no step of the library can judge that; the scenario checks only that every tag belongs to its story.
- #898 F24 (partly tested): A person must read the steps of each scenario to see if they check only what the tag says, because no step of the library can judge that; the scenario checks only that every tag belongs to its story.

The files: .garura/project/plans/788/evals/intent-to-design/ (open them for the detail).
