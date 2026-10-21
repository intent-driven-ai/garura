# Functionality: Update, edit or delete a plan file, and connect it to its issues

## What it does
add, move, drop or finish a node, or delete a plan — in the plan file and in the tracker (create, re-parent, close) together. Work can go on in the plan file; the sync brings the tracker up to date.

## Agent intent (ICE)
- Goal: Any change to a plan reaches both the plan file and the tracker.
- Limit: Never touches branches or code.
- Fails if: the tracker is left behind, or a dropped node stays open.
- Checked by: a test edits a plan three ways and the compare finds no difference.
