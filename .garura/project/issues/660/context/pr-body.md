## What this delivers

**Every Garura install now carries the memory system.** A project gets the memory tool, a short guide that every agent reads, and a check that the tool works. Kapil, 2026-10-18: "Anytime Garura gets installed, every project would need to know what that tool is, what it does, and how the memory works. Otherwise, the subagents will fail."

**The install brings no memory.** Phoenix memory reaches a machine the first time the tool needs it (Kapil, 2026-10-19: "install finishes without any memory"). A new play, `initialize`, will set up a project's own memory after the install. It is not designed or filed yet; the #653 plan records it.

- **The memory tool finds its own settings** (`core/tools/memory/memory.py`). With nothing set, it reads `settings.json` beside itself. A new setting, `phoenix_source`, names where Phoenix memory comes from. The first command that needs Phoenix memory and finds its place empty downloads it there (`pull.py`): whole or not at all, and never waiting for a password. `health` only reports. The tool's own folder is never answered as Garura memory. The contract did not change (still version 4).
- **The memory guide** (`core/tools/memory/GUIDE.md`): the three tiers, the one rule (memory only through the tool), finding memory and going up a tier, raising a memory update, keeping a decision's trace, and what an agent never does. Every command in it was run as written (`.garura/project/issues/660/evidence/guide-run.md`).
- **The install lays it** (`install-garura/scripts/memory_system.py`, called by `install.py` and by the public installer `installer/install.sh`). The tool goes to `.garura/tools/memory/` without its tests and samples, with `settings.json` beside it (kept on a re-install). The guide goes to `.claude/rules/garura-memory.md` for Claude Code, which every session and every custom sub-agent loads. For Codex it is one marked block in `AGENTS.md`, added to the project's own file.
- **The install checks it.** It runs the tool's `health` the way an agent does. It fails (exit 1, after writing the manifest) when python3 is older than 3.10, the tool cannot run, or short-term or Garura memory cannot be reached. Phoenix memory not downloaded yet is reported, not failed.
- **Uninstall reverses it.** It removes the tool, the guide file or only the `AGENTS.md` block, and short-term memory's folder only when it is empty. Phoenix memory's place on the machine is never removed.

What this does not do yet: no agent is moved onto the tool (#661, #663). `initialize` is not built. The tool points at a git repository, not a server address (Griffin, later).

Closes #660

## Where the issue text no longer matches

| Issue says | What happened |
|---|---|
| "An install whose tool cannot reach a tier fails with that tier named." | The install fails only when short-term or Garura memory cannot be reached. Phoenix memory is downloaded on first use, so an install without it passes and says so (Kapil, 2026-10-19: "install finishes without any memory") |
| The installer (the play) | The public installer `installer/install.sh`, which the README gives, carries the memory system too, through the same script. Found while building |

The GitHub text is not changed.

## How it was checked

- Memory tool: 142 tests pass (73 tool, 13 pull, 56 contract). 5 new tests fail on the old tool. The contract check passes with no boundary problems.
- Installer: 12 new tests pass (`install-garura/scripts/test_install.py`). Among them: an agent's search through the installed tool downloads Phoenix memory on first use; the tool's own files are not memory; uninstall keeps a project's own `AGENTS.md` text and its short-term work.
- **A fresh project** (`.garura/project/issues/660/evidence/fresh-project-test.md`): a Claude Code install finished with no memory, and its check passed. A real sub-agent there, asked only "which way back in must a password sign-in offer? Decide it from memory", used the tool on its own from the guide. Its first search downloaded Phoenix memory from GitHub. It answered "password reset", named `knowledge/domains/user-management.md` lines 61–62, and kept the trace with `cite`. A Codex install kept the project's own `AGENTS.md` and added one block. Uninstall removed the tool and the guide and kept the project's work.
- `lint-components`: 116 findings, the same as on main. `bash -n installer/install.sh` passes.
- Merges cleanly with main. No client, personal or secret text.

Not run: the public installer end to end (it downloads a published release, so its new step runs only after a release carries the script), and a Codex agent. Not checked: whether Codex's sandbox lets the tool download Phoenix memory.

## Self-review

The self-review is in `.garura/project/issues/660/context/self-review.md`: 0 blocking, 7 notes. The blocking check passes. The notes:

- The issue text is behind (in the table above). The plans close in the last commit before the merge.
- The public installer's new step is syntax-checked only. When its check fails, it stops before it writes the version file. The next run lays the memory system again, so a re-run recovers.
- The guide gives the tool's path from the project's root. An agent working in a subfolder would need the full path.
- A re-install deletes the old tool before it copies the new one. A copy that stops halfway leaves no tool, and the check then says so.
- Phoenix memory's address is a fixed default, written into each project's settings. A machine that cannot reach it gets `tier_missing` with git's reason. `--phoenix-source` or the settings file changes it.
- One note was wrong: it said a commit subject is 73 characters. It is 72.

Where to read: `memory_system.py`, the changes to `install.py`, `uninstall.py`, `memory.py`, `pull.py` and `install.sh`, `GUIDE.md`, and the two test files (about 700 lines). The rest is the README, the two `SKILL.md` files, plans and evidence.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
