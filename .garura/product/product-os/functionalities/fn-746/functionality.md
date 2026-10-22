# Functionality: Rename the skills

## What it does
every skill renamed to the skill verb list (to be agreed with Kapil), including the duplicates kb-search / search-kb and the manage-plan skill.

## Agent intent (ICE)
- Goal: Skills follow the standard, with one meaning per verb.
- Limit: Names and references only.
- Fails if: two skills share a verb with different meanings, or an old name is still referenced.
- Checked by: the linter and the old-name check pass for every skill.
