# Feature: The /update-plan session — instructions, checks, one approval, one landing on the plan's branch

## What it does
a person opens a session on one plan with `/update-plan <id>` or a description, gives instructions in their own words, and approves; the play lands the changes in the plan file and GitHub together, on the plan's own branch. Changing an epic's or a story's text is one more instruction (#909 folded in).

## Agent intent (ICE)
- Goal: Every instruction the person approved reaches the plan file and GitHub, in one landing on the plan's branch, and they agree afterwards.
- Limit: Nothing is written before a plain "approved". It never merges a branch and never changes code; it cuts the plan's branch only when the plan has none, with main's plan file set first.
- Fails if: a write happens before approval; GitHub is left behind or ahead of the plan file; a dropped item stays open; anything changes that the person did not approve; it switches away from a branch with uncommitted work.
- Checked by: a test session with several instructions (add, move, drop, finish, change a story's text, set Status and Direction), approved once; the compare of the plan file with GitHub finds no difference, and nothing outside the list changed.
