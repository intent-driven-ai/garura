# #883 All memory in Garura's source is Phoenix memory: one install lays it, initialize gives each project its own blocks

**All memory in Garura's source is Phoenix memory, and it reaches projects in three steps** (the product owner, 2026-10-25):

1. **The Phoenix install, once per machine.** It lays Phoenix memory from the `phoenix-memory` repo at `~/.phoenix`. The memory tool reads Phoenix memory only through its own interface. Today that interface points at `~/.phoenix`; later it points at a remote place, and nothing else changes.
2. **The Garura install, once per project.** It lays only the pieces: the plays, agents, skills, tools and the memory tool. It lays no memory. "Garura cannot install its memory."
3. **`initialize`, after the Garura install.** It asks the questions that decide which memory fits the project (for example Java or .NET, a React front end or none) and sets up the project's Garura memory from Phoenix memory. It can run again to bring changes in.

A person installs Phoenix once on a machine and initializes many projects, each with different memory blocks.

## Why

Today the source memory and the `phoenix-memory` repo drift apart. They are kept in step by hand. On 2026-10-25 the feature page template was in the source but in no memory tier, and Phoenix memory still had the old `functionality.md` (#868). A play that wrote a feature page could not be judged until the template was promoted by hand.

## Done when

- Every memory file in Garura's source is classed as Phoenix memory.
- The Phoenix install lays Phoenix memory from the `phoenix-memory` repo; a second Phoenix install brings it up to date.
- The Garura install lays no memory of its own.
- `initialize` builds the project's Garura memory from Phoenix memory, with only the blocks its answers call for, and can run again to take in changes.
- Two projects on one machine, initialized with different answers, get different memory blocks from the one Phoenix memory.
- A play reads memory only through the memory tool.

## Open

- How the source memory reaches the `phoenix-memory` repo without hand copying (#868).

## Context

- Under business intent #862 (initialize). Not planned yet.
- ADR 038 already says the Garura install brings no memory. It says the memory tool downloads Phoenix memory on first use; this story replaces that with the Phoenix install.

