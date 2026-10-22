# Capability: Installs follow the renames

## Directional intent
an install in a project that already has Garura removes the old names and lays the new ones, using the rename map.

## Agent intent (ICE)
- Goal: A project never ends up with an old and a new name side by side.
- Limit: Removes only components Garura installed.
- Fails if: an install leaves an old-name folder next to its new one.
- Checked by: install over a test project with the old names leaves only the new ones.
