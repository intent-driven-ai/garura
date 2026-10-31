# Need (#1007)

From ADR 064 (accepted by the product owner, 2026-10-31): an item's status in a plan follows its
own issue. Closed as completed means Done; closed as not planned means Dropped. While its issue is
open, a person sets it. Nothing works a status out from the items under it: no roll-ups. A parent
never changes because its children closed. The plan's own Status and Direction stay the
person's.

Change only the Plan kind's rule line that says "A person sets the plan's Status and its
Direction, and the status of each item in its tree. Nothing works them out from the work: there
are no roll-ups. ... A play changes a status or the direction only when a person asked for it."
Write it without naming any play: the product owner says the ontology holds structure and rules
only. No new question, kind, link or property.

Issue: #1007. Source: docs/adr/064-an-items-status-in-a-plan-follows-its-own-issue-with-no-roll-ups.md

## Touches
Plan
