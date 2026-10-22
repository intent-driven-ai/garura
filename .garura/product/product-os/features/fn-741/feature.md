# Feature: A rename map, and a check that no old name is left

## What it does
one file mapping every old name to its new name, and a check that finds any old name still used outside past records and older ADRs.

## Agent intent (ICE)
- Goal: Every rename is complete, everywhere it is referenced.
- Limit: Past run records and older ADRs keep their old words.
- Fails if: an old name is still referenced in a component, doc or test.
- Checked by: on today's code the check lists every old name; after each batch it lists none for that batch.
