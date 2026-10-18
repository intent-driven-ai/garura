# Brief — Garura's memory system: three tiers, one memory tool, a memory update before any guess

Shape: markdown (a framework decision, `docs/adr/`).

## Decision

Kapil set Garura's memory system on 2026-10-18. In his words, from the conversation that day:

**What memory is, and who reads it.**

> The memory system is accessed primarily by the subagents that we have created. The workflows
> we have placed, like a start change, grill vision, whatnot, make a call to subagents which
> are required for context gathering, and then they move forward. That context gathering is
> essentially where the memory comes from.

**Three tiers.**

> There needs to be a global memory. There is a global memory that gets installed when the
> Garura gets installed. That's number one: global memory. Then there is a project-specific
> memory that goes into .garura within the project itself. Once the work happens, you go into
> a short-term memory (STM) that gets created in the issue on which we are working, where all
> the plans and specs and everything are getting created.

> The subagents then also need to read through the Git repository, the product model, the
> intents, and all of these are various positions from which it can read the information and
> then start collecting the decisions that need to be made.

**Phoenix memory is the superset; a project holds the subset it needs.**

> everythign that is in garura. this global mamoery - lets call it phoenix memory. garura in
> each project will pull what the project needs.. but it can always go a level up to phoenix
> memory to get more if needd. this helps in content management and keep it small and clean

> In other words, Phoenix memory is the superset, and Garura memory is the subset. Phoenix
> memory gets everything. The Garura memory, when installed in a project, holds a subset of
> the global Phoenix memory, but whatever the project needs.

Asked where Phoenix memory lives until Griffin exists, Kapil chose **its own git repository**
(for example `phoenix-memory`), cloned onto the machine, which the tool searches; every memory
update is a commit, so it has history, review and versions (reply "1 A").

Asked how a project picks the subset it pulls, Kapil chose **a starting set at install** —
Garura's rulebook and the memory guide — and more pulled whenever the tool goes up and finds
something, with a short list in the project recording what it pulled and from which version
(reply "2 A"), and added:

> 2A is okay, but that should not stall garura plays. when needed, it looks hierarchically..
> stm - then - ltm - then - global phoenix. this way ifit finds everyting in lowest tier it can
> stop and the content is protectted. installation is key so that it has some part of LTM
> build, but this is not blocking

**Only within memory; a memory update before anything from outside.**

> If none of this is available, then and only then can subagents, the skills, or whatnot go to
> the LLM to ask for information or to do web research. At that point in time, human approval
> is absolutely needed, because what we want to make sure of is that agents work within the
> realm of global memory, local short-term GitHub, or whatnot. In case they ever have to go
> out, we would rather want to first update the memory, the global memory, or the project
> memory before it can go back into anything else. The system should work only within the
> memory, but not outside of it.

> If the system always works with the memory it has, then the drives can make all the
> decisions all by themselves. In other words, assuming when a drive runs and it has to make a
> decision, it can't find anything and it goes out, it needs to spawn off a thread saying, "We
> need a memory update to happen." That memory update will update one of those memories that
> fundamentally will help it make the decision.

**One tool, outside Garura, that finds and updates memory.**

> the global memory is going to sit outside of Garura, so searching the global memory should
> be through an API or a tool that we would be building. The tool is going to be eventually
> exposed by Griffin, but right now, let's build the tool in a manner where the tool is the one
> which is given access to the subagent. When the subagent calls the tool, the tool knows to go
> and search a folder location. That way, tomorrow, when that folder location becomes an API
> exposed by Griffin, the impact on Garura and the agents is zero because they are always
> calling the tool.

> this cli is for reteriving memory and also to update it

**The tool searches the way Claude Code does.**

> the tool should use claudecode like search tools liek sed, bash adn other toosl that makes
> claude-code such a winner. even when we goto cli that will internally run similar tools on
> server. this is critical as this is why claude-code is so good

**A memory review.**

> The tool that we were building, the prototype for business and intent stuff, now also needs
> to have a memory review tool that understands these different kinds of memories in what we
> are working on and where the information is coming from. That way, when decisions are made
> by the underlying agentic systems, it knows which memory it refers to.

**Part of every install.**

> The Phoenix memory, the long-term memory, and the short-term memory are key parts of the
> architecture, and they should be part of the Garura installation. Anytime Garura gets
> installed, every project would need to know what that tool is, what it does, and how the
> memory works. Otherwise, the subagents will fail.

Choices Kapil was shown and did not change (2026-10-18): the one tool covers all three tiers,
so every answer is cited the same way; until the memory review exists, a person approves a
memory update by typing; the seven retired agents are left as they are.

## Why now

ADR 034 (accepted 2026-10-18) says that inside a drive a play answers from memory and names
where each answer came from. The memory review of the same day
(`.garura/project/issues/613/specs/memory-review.md`) found memory cannot support that: three
copies of long-term memory that disagree; 13 active agents and 32 active skills that read
memory by hard-coded paths; a shared way in (`ltm_context`, ADR 015) that one play uses; a rule
(ADR 015's R4) that lets an agent fall back to the model's own reasoning; and nothing that
records which memory an answer came from. Kapil chose to fix the whole memory system before the
Kickoff drive (#613) is built, as Feature #653. This spike (#654) records the decision the
feature builds on.

## Options considered

- **Keep ADR 015 (R1–R4 with a model fallback that `/learn` promotes later).** Lost: agents
  decide from the model first and learn afterwards; Kapil wants memory updated first ("we would
  rather want to first update the memory … before it can go back into anything else").
- **Global memory holds only knowledge; Garura's rulebook stays with Garura's code.** Lost:
  Kapil chose everything ("everythign that is in garura … phoenix memory"); the project pulls
  the subset it needs.
- **Phoenix memory as a plain folder in the home directory, filled by the installer.** Lost: no
  history, review or versions (Kapil chose its own git repository, "1 A").
- **A project pulls nothing at install; every piece on first need.** Lost: Kapil chose a
  starting set at install ("2 A"), never blocking a play.
- **The tool as an MCP server, or a search index (semantic or numbered nodes).** Lost: the
  knowledge base design note already says "server behind a CLI … Not MCP (too expensive per
  call)" (`core/components/memory/knowledge/_DESIGN.md`), and Kapil: Claude Code-style search
  "is critical as this is why claude-code is so good".
- **Agents keep reading memory by their own paths.** Lost: the move to Griffin would change
  every agent; Kapil wants "the impact on Garura and the agents" to be zero.

## Decided by

Kapil Ahuja, 2026-10-18.

## Decided in

#654 (spike), under Feature #653 and business intent #606. Plan:
`.garura/project/issues/653/specs/plan.md`, item 1.

## Change at acceptance (Kapil, 2026-10-18)

> ltm = project memory = garura memory. to ensure this is not confused from the memory that
> claude and codex use. so lets call it garura memory

The project tier is named **Garura memory** throughout.
