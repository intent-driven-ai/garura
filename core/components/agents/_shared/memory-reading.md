# Memory Reading Protocol

How an agent gets what its skills need from memory. Each agent that uses the memory tool points
to this file. The agent's own file says what it puts in short-term memory, and the path it
hands each skill.

This file is not memory. The install lays it in the installed shared folder, at
`.claude/skills/_shared/memory-reading.md`, beside its script `copy_memory.py`.

## The rule

- Read memory only through the memory tool, from the project root:
  `python3 .garura/core/tools/memory/memory.py`.
- Never read a memory file by its path. Never take a memory path from a contract.
- Never answer from what you already know, and never from the web.

## The steps

1. **Find** what the task needs. The tool looks in short-term memory, then Garura memory, then
   Phoenix memory, and stops at the first tier that answers:

   ```
   python3 .garura/core/tools/memory/memory.py find --issue <issue> --glob "<glob>"
   ```

   A run with no issue leaves out `--issue`. Its lookup starts at Garura memory.

2. **Copy** each file a skill needs into the issue's short-term memory. The copy goes to
   `<issue folder>/context/memory/<path as found>`, and the manifest is
   `<issue folder>/context/memory/manifest.json`. One command reads the file and writes the
   copy and its line in the manifest (tier, path, version, fingerprint, copy):

   ```
   python3 .garura/core/tools/memory/memory.py read --issue <issue> --tier <tier> --path <path> \
     | python3 .claude/skills/_shared/copy_memory.py <short-term copy> <manifest>
   ```

   The script writes the text unchanged. A second copy of the same file replaces its line in
   the manifest. When the tool refuses the read, the script writes nothing, says why, and
   exits 1.

   When your own file names another copy folder (for example a folder for one job of a
   concurrent fan-out), put the copies and the manifest in that folder. Never write a copy
   folder or a manifest that another agent of the same run writes.

3. **Hand** each skill the short-term paths, never a path in memory. A skill reads only
   short-term memory and the working files of its play.

4. **When no tier holds what the task needs**, do not fill the gap. Say so in your output, and
   name what is missing. When your own file says to raise a memory update, raise it with the
   tool's `propose` command. A person approves it before anyone uses it.

5. **When the tool says `tier_missing`**, a tier cannot be reached. Say so. It never means
   "nothing found".

## What you never do

- Read a memory file with Read, Grep, Glob or a shell command.
- Write to Garura memory or Phoenix memory. Every memory write goes to the issue's short-term
  memory.
- Decide from another issue's short-term memory, or from a memory update that waits for a
  person.
