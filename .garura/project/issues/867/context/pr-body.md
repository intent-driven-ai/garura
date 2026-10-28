Agents can now copy a file from short-term or Garura memory into the issue's short-term memory. Before, the shared copy script refused every such read, because those two tiers are plain folders and the memory tool answers them with `version: null`. The script and its test only knew Phoenix answers, which always have a version.

Closes #867.

## What changes

- `core/components/agents/_shared/copy_memory.py` accepts `version: null` when the tier is `short-term` or `garura`, and records `"version": null` in that file's manifest entry. It still refuses an answer with no tier, path or fingerprint, and a Phoenix answer with no version.
- `test_copy_memory.py`: 5 new tests (Garura and short-term answers with no version are copied and recorded; a Phoenix answer with no version is refused; no tier, no path refused). 16 tests pass.
- `memory-reading.md` (the agents' shared memory guide): one line says short-term and Garura memory answer with no version, and the manifest records null.

## Checks

| Check | Result |
|---|---|
| Hidden acceptance checks, written before the fix and kept from the builder | 11 / 11 pass (6 failed before the fix) |
| test_copy_memory.py | 16 pass |
| install tests | 74 OK |
| Component lint | no error in a touched file |

Found in the /shape-slice 788 re-run (#866), where every Garura memory copy had to be worked around.
