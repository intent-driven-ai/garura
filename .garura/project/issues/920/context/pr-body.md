## What this changes

The Discovery loop's knowledge step was built as three plays that no person runs (`/search-knowledge`, `/research-knowledge`, `/check-knowledge`). It is now one step of the loop, run by the `knowledge-builder` agent with the four skills that already existed, and three small scripts the loop owns: group the repeated questions, check the step's records, record the person's reply (ADR 059). The three plays are removed.

On the way it fixes the defects the unplanned epic #922 gathers:

- the loop's done check could never find two of the plays' records, because they kept their old names (#923);
- the loop's pre-flight named the plays and the loop by their old names, so it never read the loop's own settings (#924);
- the round script read waiting memory updates from their files instead of asking the memory tool (#925);
- the research skill called the memory tool itself, though only agents may (#926);
- the proposed-answers skill was handed no memory (#927);
- the ADR keeper agent read Phoenix memory by its file paths (#928).

It also adds a section to the ADR template that tells the person accepting a decision what was found on the way (#930), corrects the memory pages in Garura's source that taught the old setup, writes plan 606 for the unplanned epic, and adds the rule "An unplanned epic gathers defects being fixed together" to the work rules.

Not in this change: sending the corrected memory pages to Phoenix memory (#929, waits for the product owner's yes), and the Phoenix memory capability in the product model (after this lands).

Closes #920
Closes #923
Closes #924
Closes #925
Closes #926
Closes #927
Closes #928
Closes #930

## Checks

- Every test file in the source passes (64 files).
- The loop linter passes on the Discovery loop and the worked example.
- The component linter shows the same 36 errors as main, none new.

## Self-review

Blocking findings: 0

## What the change does

The Discovery loop used to run its "find, build and brief the missing knowledge" work as three
separate plays that no person ever runs. This change makes it one step, run by the
knowledge-builder agent (ADR 059, which retires ADR 042). The three plays are removed. Only
agents now call the memory tool. The memory rule pages, glossary and component docs are
corrected. Plan 606 and a work-tracking rule for the unplanned epic 922 are added.

Size: 13 commits, 105 files. 27 of those files are in the issue's own record folder. Outside
that, 78 files: about 2,500 lines added and 3,600 removed, mostly the three deleted plays.

## Scope checks

- Matches the issue: PASS. Every area touched (loop, knowledge-builder and its skills, the
  three removed plays, memory rules, ADRs, docs, plan 606, work rule) is named in ADR 059's
  "Affects" list or in the scope you gave for epic 922. The adr-keeper, author-decision and ADR
  template edits are also in ADR 059's list.
- No scope creep: PASS. No file outside that scope was found.
- Reasonable size: REVIEW (not blocking). It is large, but cohesive: it is one decision, and the
  line count is dominated by deleting three plays. ADR 059 explains the whole change in one
  place, which helps a reviewer.
- No stray artifacts: PASS for the diff. No debug prints or TODOs were added (the `print` calls
  found are the scripts' real JSON output). Outside the diff, two untracked files sit in the
  working folder and are not committed: CLAUDE.md.new and
  .garura/project/issues/920/context/resolved-rules.json. CLAUDE.md.new differs from CLAUDE.md.
  Keep it out of the commit unless you meant it.

## Quality checks

- Tests present: PASS. The moved loop scripts (group_questions, check_knowledge, record_review)
  are covered by the loop's tests. I ran the three test files: 9, 39 and 81 tests, all pass.
  The old plays' own tests were deleted along with them.
- Commits are clean: PASS. All 13 commits use the conventional format and end with (#920).
- No secrets: PASS. A scan of added lines for keys, tokens, passwords and private-key headers
  found nothing.
- Docs in step: PASS, with one note. Glossary, plays, loops and agents docs, the memory rule
  pages and the ADR index are updated, and ADR 042 is marked superseded. No stale reference to
  the three removed plays remains in core/ or docs/, except history that should stay: older
  ADRs, ADR 059, and the check-change play, which uses "check-knowledge" as the name of a
  memory shelf, not the removed play. Note: ADR 059 lists docs/components/skills.md,
  install.py and the product-model page fn-744 as affected, but none changed in this diff.
  skills.md and install.py hold no stale reference. fn-744 still has one line that maps
  "review-knowledge -> check-knowledge"; it reads as a rename history, so it may be fine, but
  look at it.
- Nothing obviously broken: PASS. The component checker reports 36 errors, and main reports the
  same 36. Four of them are in create-loop's SKILL.md, which this change edited, but the edit
  touched prose only and the same four errors exist on main. No merge conflicts with main
  (merge-tree is clean).

## Other rules checks (assess-pr's own rules for this kind of project)

- No merge conflicts: PASS (merge-tree clean).
- Agent, skill, play files changed: frontmatter and structure not changed by this diff; the
  checker finds nothing new.
- ADRs: ADR 059 has Status Accepted; ADR 042 Superseded. PASS.
- Components deploy (core/components changed): REVIEW. Install the changes into a project's
  .claude/ with install-garura after merge; this review did not do it.

## Result

Ready: yes. Blocking findings: 0. Items to look at: the large size, the untracked
CLAUDE.md.new, the fn-744 line, and the install step after merge.
