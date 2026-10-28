# Decision brief — #920

Shape: markdown (a Garura framework decision, `docs/adr/`).

The product owner's words, 2026-10-28: "update the older ADRs, retire them too, and create new
ones, calling out that a bug was introduced. This bug means some part of memory is not right, the
memory in .garura which is used for agents to run."

## Decision

The Discovery loop's knowledge step is one step of the loop, run by the `knowledge-builder`
agent, which calls skills and the memory tool directly. `/search-knowledge`,
`/research-knowledge` and `/check-knowledge` stop being plays and are removed. Memory is reached
only through the memory tool: no skill searches memory or calls the tool itself; the agent
raises a researched knowledge page with the tool's `propose`. The repeat-question merge, the
step's one check and the reply recorder become scripts of the loop. The design is
`.garura/project/issues/920/specs/redesign.md`.

## Why now

ADR 042 made the step three "member plays" that no person runs. That was a bug:

- three pre-flights, stop conditions and closes per round, for one agent's job;
- two of the plays write their done record under old names, so the loop's done check cannot
  find them;
- the research skill calls the memory tool itself, against ADR 039 §2;
- `round_state.py` reads memory-update files by path;
- the memory search duplicated the memory tool.

The bug also left the memory agents run from wrong. This project holds no memory of its own, so
its agents read Phoenix memory. Phoenix memory teaches "member plays" in
`standards/rules/_index.md`, `pipeline-next.md` and `pipeline-position.md`. Three standards the
loop depends on (`loop-contract.md`, `naming.md`, `rename-map.yaml`) are in Garura's source but
missing from Phoenix memory, so no agent can find them through the memory tool. Garura's own
product model names the old plays in feature `fn-744`.

## Options considered

1. Keep the three plays and fix the done-record names. Rejected: no person runs them, and the
   ceremony stays.
2. Three skills, each called by its own agent dispatch. Rejected: three dispatches for one
   agent's job.
3. One loop step, one agent, skills plus direct memory-tool calls. Chosen.

## Decided by

The product owner, 2026-10-28 (#920).

## Decided in

Issue #920, this session.

## Older ADRs

Supersedes ADR 042 (retire it: its Status becomes Superseded with a forward pointer). Amends
ADR 041 §3 and §4 (the member plays). The ADR names the memory pages to correct and promote to
Phoenix memory.

## Change (the product owner, 2026-10-28)

"You tell me the things I should know. Make sure to give a bit more context. For example, you were telling me the Phoenix copies of the page are out of date in other ways. What Phoenix copy of the page? What other ways? … the agent broke the memory rule. By checking which memory rule, which agent. I think we should also update the ADR template so that things that I should know should be properly explained."

So: move every point found on the way out of Context into the new section "For the Person Who Accepts This" (the template in Garura's source, `core/components/memory/standards/templates/adr.md`, now has it; Phoenix memory's copy gets it when promoted under this change). Each point has five parts: what and where, what is wrong or worth knowing (the detail itself), why it matters, what this decision does, what you decide. At least these points:

1. Phoenix memory's `standards/rules/pipeline-position.md` (last changed in Phoenix on 2026-10-20) is older than Garura's source copy: it calls the play builder `play-creator` (now `/create-play`), names the review step `review-change` (now `/check-change`), so a play built from it gets a closing step that no longer exists; it lists plays by old names (`/vision`, `/understand`, `/grill`, `/intent`, `/adr` and others); it says "drive" and points to `drive-contract.md` and `check_drive_contract.py`. It also uses "members" for the change plays a play's position brings in, a different meaning this decision keeps.
2. Phoenix memory holds `standards/rules/drive-contract.md` (last changed 2026-10-20), the loop contract under its name before ADR 045, and has no `loop-contract.md`; a lookup of the loop contract finds the old drive version or nothing. Whether to delete it when the new page is promoted is the person's call.
3. Phoenix memory's ADR template (`standards/templates/adr.md`) is older than the source: it names `/adr`, `author-adr`, "drive", "Kickoff", `/intent`, `/vision`, `play-creator`, and the level `functionality`. Agents draft every ADR from it.
4. The wider gap: comparing Garura's source memory with Phoenix memory, 49 pages differ, 7 are in the source only and 16 are in Phoenix only. This decision fixes only the pages it touches; the rest is #921 (serving business intent #899).
5. While drafting this record, the adr-keeper agent listed and compared files inside the `phoenix-memory` repository by their paths, against the rule in `.claude/rules/garura-memory.md` ("You find it only through the memory tool… Never read a memory file by its path"). The tool gives each answer its tier and fingerprint, so a decision can cite it; a direct read skips that. The agent re-checked every fact it used through the tool. This change fixes the agent: `core/components/agents/adr-keeper.md` now says how to find and compare pages through the tool (`find --tier`, `--every-tier`, `read --tier`) and forbids reading memory by its path.
6. ADR 041's Status line says ADR 043 made "the connect step a member play too"; ADR 043's own text runs the connect step as two skills. After this decision no step of a loop is a member play.

Also add to Affects: `core/components/memory/standards/templates/adr.md`, `core/components/skills/author-decision/SKILL.md`, `core/components/agents/adr-keeper.md`; and to what is promoted to Phoenix memory: the ADR template.
