## What this delivers

**Every Garura install now carries the memory system.** A project gets the memory tool, a short guide that every agent reads, and a check that the tool works. Kapil, 2026-10-18: "Anytime Garura gets installed, every project would need to know what that tool is, what it does, and how the memory works. Otherwise, the subagents will fail."

**The install brings no memory.** Phoenix memory reaches a machine the first time the tool needs it (Kapil, 2026-10-19: "install finishes without any memory"). A new play, `initialize`, will set up a project's own memory after the install. It is not designed or filed yet; the #653 plan records it.

- **The memory tool finds its own settings** (`core/tools/memory/memory.py`). With nothing set, it reads `settings.json` beside itself. A new setting, `phoenix_source`, names where Phoenix memory comes from. The first command that needs Phoenix memory and finds its place empty downloads it there (`pull.py`): whole or not at all, and never waiting for a password. `health` only reports. The tool's own folder is never answered as Garura memory. The contract did not change (still version 4).
- **The memory guide** (`core/tools/memory/GUIDE.md`): the three tiers, the one rule (memory only through the tool), finding memory and going up a tier, raising a memory update, keeping a decision's trace, and what an agent never does. Every command in it was run as written (`.garura/project/issues/660/evidence/guide-run.md`).
- **The install lays it** (`install-garura/scripts/memory_system.py`, called by `install.py` and by the public installer `installer/install.sh`). The tool goes to `.garura/tools/memory/` without its tests and samples, with `settings.json` beside it (kept on a re-install). The guide goes to `.claude/rules/garura-memory.md` for Claude Code, which every session and every custom sub-agent loads. For Codex it is one marked block in `AGENTS.md`, added to the project's own file.
- **The install checks it.** It runs the tool's `health` the way an agent does. It fails (exit 1, after writing the manifest) when python3 is older than 3.10, the tool cannot run, or short-term or Garura memory cannot be reached. Phoenix memory not downloaded yet is reported, not failed.
- **Uninstall reverses it.** It removes the tool, the guide file or only the `AGENTS.md` block, and short-term memory's folder only when it is empty. Phoenix memory's place on the machine is never removed.

What this does not do yet: no agent is moved onto the tool (#661, #663). `initialize` is not built. The tool points at a git repository, not a server address (Griffin, later).

**ADR 038** (accepted by Kapil through `/adr`) records this: the install brings no memory, Phoenix memory arrives on first use, `initialize` sets up a project's memory, and the tool lives at `.garura/tools/memory/`. It amends ADR 035 §2, §3, §4, §8 and its Alternatives, and ADR 017 §1.

Closes #660

## Review rounds, and what was fixed

**Round 1** (harness approve, 0 blocking; 3 major, 12 minor, 5 small). Kapil chose to fix them and record the decision before the merge ("2"):

- The decision record said the opposite (ADR 035 §2 "a starting set at install"), and `.garura/tools/` was not in ADR 017's whitelist. Fixed by ADR 038.
- The first-use download had no time limit. It now stops after 600 seconds, puts `--` before its source, and says why when the copy cannot be put in its place.
- A re-install now copies the new tool whole beside the old one, then swaps. A copy that stops halfway keeps the tool and settings a person edited.
- `install.sh` now records its version before it stops on a failed check, as `install.py` writes its manifest first.
- The check: bad input exits 2. A not-ok answer in any shape fails with a message. It asks Phoenix memory's source whether it answers, and notes it when it does not.
- The guides now say what the code does. The old machine-wide copy is still laid. An existing `AGENTS.md` gains only the marked block. Agents run the tool from the project's root. A play's own working files are read directly. `initialize` is not built.

**Round 2** (`.garura/project/issues/660/review/round-2.yaml`): 16 fixed, 2 partly fixed, 1 not fixed, 1 carried, and 3 new. Fixed after round 2:

- A re-install that stops halfway left `.garura/tools/memory.new`, which a lookup read as Garura memory. The half copy is now removed, and uninstall removes one left behind.
- An answer the check cannot read now fails with a message.
- `installer/install.sh` is now run whole by 4 tests. They use a local Garura and a local Phoenix source in place of the network.
- Found while posting round 2: a git call that hit its time limit was stopped, but the password helper it started kept waiting on the macOS keychain, and the stuck helpers blocked the next push. The download and the install check now stop git and every helper it started at the limit. A test proves both are gone.

Carried (small): `install()` is 53 lines, against 50 on main. `uninstall()` and two files were over the limits on main already. A download folder stays beside Phoenix memory's place if the agent's shell kills the tool. No lookup reads that folder.

## Where the issue text no longer matches

| Issue says | What happened |
|---|---|
| "An install whose tool cannot reach a tier fails with that tier named." | The install fails only when short-term or Garura memory cannot be reached. Phoenix memory is downloaded on first use, so an install without it passes and says so (Kapil, 2026-10-19: "install finishes without any memory") |
| No decision record is named | The diff carries ADR 038, on Kapil's word after review round 1 ("2"); it amends ADR 035 and ADR 017 |
| The installer (the play) | The public installer `installer/install.sh`, which the README gives, carries the memory system too, through the same script. Found while building |

The GitHub text is not changed.

## How it was checked

- Memory tool: 145 tests pass (76 tool, 13 pull, 56 contract). 8 new tests fail on the old tool. The contract check passes with no boundary problems.
- Installer: 27 new tests pass (`install-garura/scripts/test_install.py`). 4 of them run `installer/install.sh` whole. They cover: an agent's search through the installed tool downloads Phoenix memory on first use; the tool's own files are not memory; uninstall keeps a project's own `AGENTS.md` text and its short-term work; and each error path above.
- **A fresh project** (`.garura/project/issues/660/evidence/fresh-project-test.md`): a Claude Code install finished with no memory, and its check passed. A real sub-agent there, asked only "which way back in must a password sign-in offer? Decide it from memory", used the tool on its own from the guide. Its first search downloaded Phoenix memory from GitHub. It answered "password reset", named `knowledge/domains/user-management.md` lines 61–62, and kept the trace with `cite`. A Codex install kept the project's own `AGENTS.md` and added one block. Uninstall removed the tool and the guide and kept the project's work.
- `lint-components`: 116 findings, the same as on main. `bash -n installer/install.sh` passes.
- Merges cleanly with main. No client, personal or secret text.

Not run: the public installer from a real published release (the tests serve it a local copy), and a Codex agent. Not checked: whether Codex's sandbox lets the tool download Phoenix memory. On this machine, inside this session, git waits on the macOS keychain when it calls GitHub; the new time limit stops that wait.

## Self-review

The self-review is in `.garura/project/issues/660/context/self-review.md`: 0 blocking, 7 notes. The blocking check passes. The notes:

- The issue text is behind (in the table above). The plans close in the last commit before the merge.
- The public installer's new step is syntax-checked only. When its check fails, it stops before it writes the version file. The next run lays the memory system again, so a re-run recovers.
- The guide gives the tool's path from the project's root. An agent working in a subfolder would need the full path.
- A re-install deletes the old tool before it copies the new one. A copy that stops halfway leaves no tool, and the check then says so.
- Phoenix memory's address is a fixed default, written into each project's settings. A machine that cannot reach it gets `tier_missing` with git's reason. `--phoenix-source` or the settings file changes it.
- One note was wrong: it said a commit subject is 73 characters. It is 72.

Where to read: ADR 038, `memory_system.py`, the changes to `install.py`, `uninstall.py`, `memory.py`, `pull.py` and `install.sh`, `GUIDE.md`, and the two test files (about 1,000 lines). The rest is the README, the two `SKILL.md` files, plans and evidence.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
