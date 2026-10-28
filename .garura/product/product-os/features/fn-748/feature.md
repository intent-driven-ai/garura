# Feature: An install removes old names and lays the new ones

## What it does
install-garura reads the rename map, removes each old-name component it installed, and lays the new one; uninstall-garura knows both names.

## Agent intent (ICE)
- Goal: Installed projects follow the renames with no manual clean-up.
- Limit: Never removes a component the project wrote itself.
- Fails if: an old-name component survives an install.
- Checked by: an install test over a project with old names: only new names remain, project files untouched.
