# Functionality: Rename the lifecycle and lens plays

## What it does
intent → discover-intent, vision → discover-domains, understand → discover-capabilities, shape → design-scope, roadmap → design-roadmap, grill → design-features, the seven lens plays → design-<lens>-lens, implement → build-feature, validate → validate-feature, launch → release-feature, deploy → release-increment, learn → learn-outcomes.

## Agent intent (ICE)
- Goal: The lifecycle plays follow the standard.
- Limit: Names only; moving these plays onto the new model is separate work.
- Fails if: an old name is still referenced.
- Checked by: the old-name check finds none of these names.
