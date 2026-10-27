# Feature: List every plan, from the plan files alone

## What it does
one list of every plan — its ID, its business intent, what is now, and who it waits on.

## Agent intent (ICE)
- Goal: Anyone sees every active plan at once.
- Limit: Reads the plan files only.
- Fails if: a plan in the plans folder is missing from the list.
- Checked by: a test folder with three plans lists all three.
