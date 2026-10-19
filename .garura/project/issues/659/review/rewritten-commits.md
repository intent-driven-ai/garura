# Rewritten commits

On 19 October 2026, before the merge, the branch was rewritten once. Kapil chose this.

Why: two review records held a full workspace path, 116 times each. The records are
`lint-components.json` and `pr.diff` in this folder. A merge keeps every branch commit, so the
path would have gone into main's history. The rewrite makes each such path repo-relative.

What changed: only those two files, in each commit from the first review record onward. The
commit messages, authors and dates are the same. The code is the same.

What it means for these records: the self-review and the review records name the old commit
ids, because they were written before the rewrite. Read each old id as its new id:

| Old id | New id | Commit |
|---|---|---|
| `192fd932` | `58769ab7` | chore(stm): record review-change run artifacts (#659) |
| `9541205e` | `bac4c8ec` | fix(memory-tool): hidden memory stays hidden, however spelled (#659) |
| `afeaa2df` | `fc8308e9` | fix(memory-tool): three small faults from the #676 review (#659) |
| `b24dc3f0` | `9937dbff` | docs(memory): the trace rule says when it binds and what to do (#659) |
| `14e434b6` | `83cb18c6` | docs(review-tool): agent decisions reach the page as pack pieces (#659) |
| `b8a9d1a6` | `543c2e9e` | docs(adr): ADR 037 — agent decisions keep a trace; five sections (#659) |
| `2cb6eb75` | `65b61276` | docs(memory): the trace rule and the cite command name ADR 037 (#659) |
| `547a1b7e` | `f2f38356` | fix(memory-tool): three notes from the round 2 self-review (#659) |
| `700f4355` | `881448d2` | chore(stm): record propose-change run artifacts (#659) |
| `c4fdb575` | `a1e42edc` | docs(review-tool): the mock's sample ADR is not numbered 037 (#659) |
| `4553fe26` | `b39aa9b7` | chore(stm): record propose-change run artifacts (#659) |
| `43c07a6a` | `f36fc440` | chore(stm): record review-change run artifacts (#659) |
| `6cdb119c` | `1a8a3c9f` | fix(memory-tool): the four round-2 items, before the merge (#659) |
| `d19c616e` | `ba1eb016` | chore(plan): close the #659 plan and move memory to #660 (#659) |

The 24 commits before `192fd932` did not change.
