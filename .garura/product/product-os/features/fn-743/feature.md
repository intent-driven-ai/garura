# Feature: Rename the harness plays and the loops

## What it does
play-creator → create-play, play-editor → edit-play, loop-creator → create-loop, loop-editor → edit-loop; the Discovery loop's command → run-discovery.

## Agent intent (ICE)
- Goal: The harness parts follow the standard.
- Limit: Names and references only.
- Fails if: an old harness name is still referenced.
- Checked by: the old-name check finds none of these names.
