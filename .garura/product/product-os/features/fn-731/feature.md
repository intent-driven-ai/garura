# Feature: start-change cuts a plan's branch, and each issue's branch from it

## What it does
when work on a plan starts, start-change cuts the plan's branch from main; for each issue in the plan it cuts the issue's branch from the plan branch, and takes the latest main into the plan branch first. First in this plan's order (Kapil, 2026-10-21).

## Agent intent (ICE)
- Goal: Every issue in a plan works on a branch cut from its plan's branch.
- Limit: A one-off fix outside any plan still branches from main.
- Fails if: an issue in a plan is cut from main, or the plan branch is behind main when an issue branch is cut.
- Checked by: a test plan: start-change on two of its issues gives two branches off the plan branch, which holds the latest main.
