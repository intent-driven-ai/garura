# Capability: The naming checks, built before any rename

## Directional intent
the evals that prove names follow the standard — built first, failing on today's names, passing as each family is renamed (the product owner: build the eval first).

## Agent intent (ICE)
- Goal: No rename is called done by reading it; a check says so.
- Limit: Built and committed before any name changes.
- Fails if: a family is renamed before its check exists, or a check passes on today's names.
- Checked by: run on today's code, the checks fail and list every old name.
