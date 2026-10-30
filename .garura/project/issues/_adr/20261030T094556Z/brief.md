# Decision brief

## Decision

A plan's branch is cut by the play that starts the plan's work — `/update-plan` now, and
`start-change` once #989 (start-change starts a plan on its own) is built — through one shared
script, the plan tool's `plan_branch.py`. When the plan has no branch: main's plan file is set to
In Progress with the branch named, committed and pushed on main, and `plan/<id>/base` is cut from
that commit. A failed push of main takes the commit back. An abort undoes a cut that holds nothing
else (the branch is deleted, and main's plan file is put back by a revert commit). Managing a plan
still never merges a branch and never touches code.

## Why now

The PR #998 review (findings HF-1 and MEM-1) found that ontology v14's Plan kind and `/update-plan`
cut the plan's branch, while ADR 060 ("managing a plan never touches branches or code", ontology
line 598 at the time) and start-change's ICE C9 give the cut to start-change alone, and no ADR
records the change.

## Options considered

1. Amend ADR 060: managing a plan may cut the plan's branch, main first, through the shared script.
   Chosen in #720's approved design (2026-10-30): a person who starts a session on a plan with no
   branch has started its work, and one script keeps every cut the same.
2. `/update-plan` refuses a plan with no branch and sends the person to `/start-change` first.
   Lost: start-change cuts a story's branch too, and #989 (starting a plan on its own) is not built;
   the person is sent away for a step the session can do safely.
3. Leave it unrecorded. Lost: the ontology, ADR 060 and start-change's C9 would disagree with no
   record of why.

## Decided by

The product owner.

## Decided in

#720 (manage a plan with /update-plan), plan 717, on `plan/717/720-update-plan`, PR #998 — the
review's findings HF-1 and MEM-1 asked for this record.

## Shape

markdown — a framework decision (plans and the change plays). It amends ADR 060. start-change's
ICE C9 follows when #989 is built. No business intent changes.
