# Feature: Check that the installed Garura runs before the team uses it

## What it does
Once the parts are laid, the install checks that the memory tool runs and reaches the project's short-term memory and Garura memory, and that every tool it laid loads; whatever does not is named with what to fix, and the install ends as failed, so no team starts work on a Garura that cannot run.
- The memory tool is the one way agents read memory. Short-term memory is this project's folders for each piece of work; Garura memory is the project's own memory, read before Phoenix memory; Phoenix memory is the shared memory on the machine that every project draws from.
- The check runs the memory tool's health command "the way an agent runs it", reading the settings laid beside the tool, so it sees what the agents will see.
- It fails when the tool cannot run, or cannot reach short-term memory or Garura memory.
- Phoenix memory not on the machine yet is reported, not failed. The memory tool downloads it the first time a command needs it, and the check asks Phoenix memory's source whether it answers, and notes it when it does not.
- Each tool the install laid gets its packages, and then a smoke check loads it: "A tool that does not load stops the install with a message that names it."
- The install record is written before a failed check ends the install, so the next run can see what was laid and lay it again.
- The report says each memory tier reached or not, each tool loaded or not, and what to fix.
- Examples, in different kinds of project:
  - On a laptop that has never had Phoenix memory, a new recipe app's install reports that Phoenix memory will arrive on first use, and still counts as done.
  - In a shop's checkout project where one tool's packages cannot be fetched, the install stops and names that tool.
  - In a clinic's booking app where the memory tool cannot reach short-term memory, the install fails and says the project's agents cannot use memory until it is fixed.
- How it meets the capability: an install the team cannot run is not yet "A team installs Garura", so every install proves itself before it counts.

Status: built, in both front doors: the memory system and the tools are laid and checked by the same two scripts, and "Both install paths call this". Two limits of what is built:
- The default release of the one-line command, v3.0.0, is older than both scripts, so an install of it lays no memory system and checks nothing: "This release has no memory system; skipped."
- The check runs only inside an install. Its script sits in the install play's folder, which no project receives, so a project cannot run the check again on its own.

## Inputs / Outputs
- In: the laid memory tool and its settings, which name short-term memory, Garura memory, where Phoenix memory sits on the machine and where it is downloaded from.
- In: each laid tool, with its packages or the list of packages it needs.
- In: the install record of this run.
- Out: for each memory tier, reached or not; for Phoenix memory, on the machine, or not yet and whether its source answers.
- Out: for each tool, loaded or not, with the first line of its error.
- Out: the install's end: done, or failed with what failed and what to fix, after the record is written.

## Rules & behavior
- Checked the way an agent runs it. The reason: the memory system runs the check "the way an agent runs it", so a pass means the agents can read memory too.
- Short-term or Garura memory out of reach fails the install. The reason: the project's agents decide from memory, and without it they cannot work.
- Phoenix memory not yet on the machine is reported, never failed. The reason: "The install does not fail when Phoenix memory is not on the machine yet.", because it arrives the first time the memory tool needs it.
- A tool that does not load stops the install and is named. The reason: "A laid tool must pass its smoke check.", and the plays run the tools after the install.
- The record first, then the failure. The reason: a failed check then "leaves an install the next run can see and lay again".
- No memory is read by a path, and none is brought in. The reason: agents reach memory only through the memory tool, and "install finishes without any memory."
- Both front doors run the same check. The reason: one engine is behind both.
- Not decided: whether a team can run the check again on its own after the install, without installing again.

## Acceptance criteria
- Given a laid memory tool that cannot reach short-term memory, when the install checks it, then the install ends as failed, names short-term memory, and the record is written.
- Given a machine with no Phoenix memory yet, when the install checks, then it reports that Phoenix memory is not there yet and still counts as done.
- Given a tool whose packages cannot be fetched or that does not load, when the install checks, then it stops and names the tool.
- Given the same version through either front door, when each installs, then the same checks run and report the same way.

## Out of scope
- How the memory tool works and when Phoenix memory reaches a machine. Memory, in Standards, structure, settings and memory, owns it.
- Laying the parts and the tools. Install Garura in one step, with a record of what it laid (fn-install-in-one-step) does it.
- Setting up the project's own memory. Set a project up after the install (Initialize) does it.
- Checking the project's own code. The review of each change does it.

## Sources
- The product owner on 2026-11-10: "Install into a project: A team installs Garura, chooses what it gets, and can take it out again."
- core/components/plays/install-garura/scripts/memory_system.py: "Both install paths call this", "The check runs the tool's health command the way an agent runs it", "Phoenix memory not downloaded yet is reported, not failed"
- core/components/plays/install-garura/scripts/tools_system.py: "A tool that does not load stops the install with a message that names it."
- installer/install.sh: "This release has no memory system; skipped.", "check leaves an install the next run can see and lay again"
- docs/adr/038-install-brings-no-memory.md: "The install does not fail when Phoenix memory is not on the machine yet.", "install finishes without any memory."
- docs/adr/055-installed-parts-read-only-installed-files.md: "A laid tool must pass its smoke check."
- core/components/plays/install-garura/SKILL.md: "the check asks its source whether it answers, and notes it when it does not."
- The release facts: git tag v3.0.0 of 2026-10-07; the v3.0.0 tree holds no `memory_system.py`.
