# Feature: Harness principles and practices: why we build this way, and how

## What it does
the principles (play orchestrates, agents gather context, skills do the work, scripts do mechanical parts, loops run plays, intent through ICE, nothing blocked, evals first) and the practices that follow, each with its reason.

## Agent intent (ICE)
- Goal: A client understands why each rule exists.
- Limit: Points to the ADRs; does not repeat them.
- Fails if: a practice has no reason given, or contradicts an accepted ADR.
- Checked by: each principle names the ADR or decision it comes from.
