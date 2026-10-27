# Landing evidence: plan/788/base into main (Story #915)

Branch tip e2871e44. Main is fully merged in.

## 1. Every commit not on main was reviewed

87 commits on the branch's own line: 44 merges and 43 direct commits.

- 14 merges bring main in. Main's side was reviewed on main.
- 29 merges are pull requests into plan/788/base or plan/756/base. Each has an approved review record (`review/decision.yaml`, decision: approve).
- 1 merge (36f70c3b) brought plan 722's line into plan 756's line without a pull request. Plan 722's three pull requests (#751, #752, #766) had no review. Every file they touched now matches main, so this landing brings none of their content.
- 43 direct commits: 35 run records, 4 plan-file updates, and 4 with content no review saw:
  - 277dff56 ADR 049, with its forward pointers on ADR 017 and ADR 048 (accepted by the product owner through /record-decision)
  - 56ea71a4 ADR 053, with its forward pointers on ADR 028 and ADR 033 (accepted the same way)
  - b71be9ea managing-work.md follows ADR 049
  - ad818869 the `.garura/.gitignore` change in a harness install
- e2871e44, the merge of main, resolved one clash in the plan file by hand.

Not reviewed yet: the four pieces above, the plan file as it stands, and the run records (scanned clean of home-folder paths and the company name in acedff7c).

## 2. The plan, its epics and GitHub agree

60 items in plan 788. For each, the plan's status and GitHub's state agree: every done item is closed, every open item is open.

| Plan | GitHub | Items |
|---|---|---|
| done | CLOSED | 41 |
| later | OPEN | 15 |
| next | OPEN | 3 |
| now | OPEN | 1 |

Every done item has commits on this branch, except #792 (a group; its five items are done) and #838 (built inside PR #853, as its closing note says).

Parent links that differ between the plan file and GitHub (closed issues keep their old marks, by managing-work.md):
- #815: plan under #792, GitHub parent none (CLOSED)
- #908: plan under #798, GitHub parent none (CLOSED)
- #882: plan under #788, GitHub parent 862 (CLOSED)

Open items, allowed by Story #915: #794 (the epic, now), #898, #796, #895 (next), #912, #913 and 13 parked chores and bugs (later).

## 3. Tests and linters

See `landing-tests.md`: 67 test files pass; no new linter finding against main.
