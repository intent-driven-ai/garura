# Functionality: The component linter fails any name that breaks the standard

## What it does
lint-components checks every play, skill, agent and loop name against the rule file — verb list, word count, run- only for loops, reserved built-in words, no duplicate names across kinds.

## Agent intent (ICE)
- Goal: A name that breaks the standard cannot land.
- Limit: Reads the rule file; holds no rule of its own.
- Fails if: a name that breaks a rule passes.
- Checked by: fixtures: one passing and one failing name per rule.
