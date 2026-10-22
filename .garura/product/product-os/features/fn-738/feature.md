# Feature: One ADR that replaces ADR 006 and ADR 018

## What it does
a decision record, through /adr, that adopts the naming standard and supersedes ADR 006 (naming conventions) and ADR 018 (short pipeline play names).

## Agent intent (ICE)
- Goal: The naming decision is on the record, with what it replaces.
- Limit: Older ADRs get a forward pointer only.
- Fails if: an older ADR still reads as the rule in force.
- Checked by: ADR 006 and 018 carry a superseded-by pointer; the ADR index lists the new one.
