# #1007 — an item's status in the plan file follows its own GitHub issue

Approved by the product owner, 2026-10-31 ("yes", then "approved" for the story on plan 717).
A change of direction: the ontology said a person sets every item's status and a play changes a
status only when a person asked.

## The rule

- An item's status follows its own issue: closed as completed means Done; closed as not planned
  means Dropped.
- No roll-ups: nothing is worked out from children. A parent (for example epic #956) never
  changes because its children closed.

## What changes

1. A decision record (/record-decision) and the ontology's Plan rule line (/edit-ontology, one
   line, no new question or kind).
2. The plan tool gets a `set-status` command that sets one item's status in a plan file and keeps
   its layout and comments, with tests. Plays call the installed tool.
3. merge-change: when it closes an issue that sits in a plan, it also sets that item Done in the
   plan file, in the same records commit on the plan's branch (/edit-play, test).
4. /update-plan: when a session starts, each item whose issue is closed on GitHub but open in the
   plan file goes on the list as "closed on GitHub"; it lands with the person's "approved"
   (/edit-play, the C8 rule, script and test).

## Out of scope (recorded)

merge-change also closes a capability on GitHub once every issue under it is closed: a roll-up
on the GitHub side. Recorded, not changed here.
