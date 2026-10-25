# #883 All memory in Garura's source is Phoenix memory: one install lays it, initialize gives each project its own blocks

**All memory in Garura's source is Phoenix memory.** The memory written in Garura's source files is what gets deployed, so it is all Phoenix memory. One install lays the whole Phoenix memory on a machine, once. Then `initialize` sets up each project, and gives it only the memory blocks that fit it. A person installs Garura (Phoenix) once and initializes many projects, each with different memory blocks (the product owner, 2026-10-25).

## Why

Today the source memory and Phoenix memory drift apart. They are kept in step by hand. On 2026-10-25 the feature page template was in the source but in no memory tier, and Phoenix memory still had the old `functionality.md` (#868). A play that wrote a feature page could not be judged until the template was promoted by hand.

## Done when

- Every memory file in Garura's source is classed as Phoenix memory. No source memory file is "project memory" or sits outside Phoenix memory.
- The install lays the whole Phoenix memory from the source on the machine, once. A second install brings it up to date. No hand promotion is needed.
- `initialize` builds a project's Garura memory from Phoenix memory, with only the blocks its answers call for.
- Two projects on one machine, initialized with different answers, get different memory blocks from the one Phoenix memory.
- A play reads memory only through the memory tool, as now.

## Context

- Under business intent #862 (initialize). Not planned yet.
- Related: #868 (current standards are in no memory tier), ADR 035 (memory tiers), the rule that the install brings no project memory of its own.
