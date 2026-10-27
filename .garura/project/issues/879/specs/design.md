# #879 — design (round 2, after PR #894 was rejected)

## The rule (the product owner, 2026-10-26)
- An epic holds only the work of its own slice: its stories, and the chores and other work that serve that slice.
- Work found along the way that does not serve the slice goes under its own epic. A plan may hold several epics when they serve the same business intent.
- Work that blocks the plan gets its own epic, is delivered, and merges back where it spawned.

## 1. The plan play (/edit-play — an intent change)
- C13 keeps its meaning and says it plainly: an epic's sub-issues are its slice's stories and the work under them; anything else under the epic is misplaced.
- The find step treats misplaced work like a duplicate today: it lists each item with its title, the brief shows it as "belongs under its own epic", and the run stops before any tracker write. The person moves it; the next run goes on.
- The tracker check fails on misplaced work with the same plain message (it cannot pass after a run, since the find step stops first).
- Drops from PR #894: "other children are allowed", the record's `others`, the brief's numbers-only line.

## 2. Plan 788's misplaced work under epic #794 (the product owner, 2026-10-26: "dont build epics. record stories or bugs - whatever category they are in. the shape slice and shape plan will pull them when they run.")
- No new epic. Each of the 16 items gets the issue type of its kind (the plan file's `kind`: feature -> Story, bug -> Bug, chore -> Chore), comes off #794's sub-issues, and moves out from under #794 in the plan file's tree. `/shape-slice` and `/shape-plan` pull them in when they run.
  - Story: #796, #816, #817, #820, #821, #828, #838
  - Bug: #826
  - Chore: #824, #825, #829, #830, #836, #837, #854
  - #831 was dropped (not planned): Chore, moved out the same way.
- No play moves work today. The moves run through the code-host adapter's verbs as a chore of #879, from this list, after the product owner's yes.

## 3. The blocker rule (the work guide, managing-work.md)
- Write the three lines of the rule above into "How does that land in the tracker?".

## Choices
- None left: the product owner settled A and B (no new epics; #796 is recorded as a Story and placed by /shape-slice).
