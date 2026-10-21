# Functionality: Naming rules: verbs, run- for loops, no tool built-ins, two-word plays

## What it does
the naming rules — one verb list with one meaning per verb, loops named run-<phase>, plays verb-object (at most two words), skills from the skill verb list, agents domain-role, no name that is or starts with a Claude Code or Codex built-in, no shortened words.

## Agent intent (ICE)
- Goal: Every name follows one rule a person learns once.
- Limit: No exceptions except the two named one-word plays (next, focus).
- Fails if: two parts can follow different naming shapes, or a verb means two things.
- Checked by: the rule file lists every verb with one meaning; the linter rules match it one to one.
