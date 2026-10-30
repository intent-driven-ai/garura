# Feature: The /update-plan session — instructions, checks, one approval, one landing on the plan's branch

## What it does
a person opens a session on one plan with `/update-plan <id>` or a description, gives instructions in their own words, and approves; the play lands the changes in the plan file and GitHub together, on the plan's own branch. Changing an epic's or a story's text is one more instruction (#909 folded in).

## Agent intent (ICE)
- Goal: Every instruction the person approved reaches the plan file and GitHub, in one landing on the plan's branch, and they agree afterwards.
- Limit: Nothing is written to GitHub, the model or a plan file before a plain "approved", except the one step that gives a plan with no branch its branch (main's plan file set first, then the cut). It never merges a branch and never changes code.
- Fails if: a write to GitHub, the model or a plan file happens before approval, other than that branch step; GitHub is left behind or ahead of the plan file; a dropped item stays open; anything changes that the person did not approve; it switches away from a branch with uncommitted work.
- Checked by: a test session with several instructions (add, move, drop, finish, change a story's text, set Status and Direction), approved once; the compare of the plan file with GitHub finds no difference, and nothing outside the list changed.
