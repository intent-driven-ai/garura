# ADR 035 — Agents Work Only From Memory: Three Tiers, One Memory Tool, and a Memory Update Before Anything From Outside

**Status:** Proposed
**Date:** 2026-10-18
**Level:** framework
**Decided in:** #654 (spike: decide the memory system), under Feature #653 and business intent #606; plan item 1 (`.garura/project/issues/653/specs/plan.md`)
**Supersedes:** ADR 015 (in part — the resolution protocol R1–R4: its three layers and its fallback to the model's own reasoning; `ltm_context` and the resolution trace built on it; the agent and play updates that use them; and the learning play's promotion of the model's guesses into memory afterwards. Its Knowledge File Standard stands)
**Amends:** ADR 034 — §2 "What counts as memory" (now the three tiers, read through the memory tool), §3 "Never from the model alone" (when no tier answers, a memory update a person approves, written to memory first) and §6's "Run by hand, a play is unchanged" (the memory rule holds by hand too) · ADR 009 — Rule 3 "LTM paths are stable conventions", with its LTM Reference Paths and Skill Reference Pattern: skills find standards through the memory tool, never by a path · ADR 016 — the optional `ltm_context` input, the `resolution_trace_path` output and the Resolution Protocol Hook · ADR 017 — §1's `.garura/core/` "synced memory" and §2's synced `.garura/core/memory/` copy: a project holds only the subset it pulled · ADR 032 — §3 "Two review tools": the review tool gains a third view, Memory
**Affects:** `core/components/memory/` (everything in it seeds Phoenix memory, its one home outside Garura's code), `core/components/memory/knowledge/_DESIGN.md` (LOCKED: the knowledge base's home moves to Phoenix memory, and its search engine becomes the memory tool's Claude Code-style search in place of the planned server's facet matching, ranking and later semantic search; "a CLI, not MCP" is kept), `core/components/memory/standards/rules/resolution.md` (R1–R4 and the R4 fallback to the model), `core/components/memory/standards/rules/play-close.md` (every play's close reads its templates from the project copy, `ltm.project-target`), `core/components/memory/standards/rules/drive-contract.md` (rule 4, as ADR 034 left it), `core/grounding/glossary.md` (the Memory Architecture section, and the Global mode, Project mode and /install-garura rows), `.garura/core/config.yaml` (`components.memory`; `ltm.source`, `ltm.project-target`, `ltm.global-target`; `review-pr.standards_order`, a second lookup order), `core/components/plays/install-garura/` (`scripts/install.py` copies all of memory to `~/.garura/core/memory/`), the active agents in `core/components/agents/` that name memory paths (tech-designer, product-os-keeper, test-engineer, change-reviewer, repo-orchestrator, code-builder, quality-auditor, adr-keeper, business-intent-keeper, intent-resolver), the skills in `core/components/skills/` that name memory paths (among them kb-search, search-kb, propose-kb-node, and research-domain-context, which falls back to the web), the `/intent`, `/vision` and `/understand` plays (their ICE sources), the `/fix-bug` play (the one play that passes `ltm_context`), `core/tools/lint-components/` (a rule against memory paths), `CLAUDE.md` and `docs/components/memory.md`, and three things not built yet: the memory tool, Phoenix memory's repository, and the review tool's Memory view
**ICE impact:** The agent intents of every play whose agents read memory change, each through its ICE source and `/play-editor`. Their agents find and update memory only through the memory tool; when no tier answers they raise a memory update instead of turning to the model or the web; every decision names its memory. First `/intent`, `/vision` and `/understand` (plan item 8): the lines ADR 034 changed (`/intent` C4, C5 and Step 3; `/vision` C11; `/understand` C13) now read "memory" as the three tiers and "ask the person" as a memory update the person approves; `/vision`'s knowledge-base proposal, which rests on web research today, becomes a memory update. `/fix-bug` stops passing `ltm_context`. Then every other play and agent (plan item 10), including tech-designer and the research-domain-context skill, which fall back to the web or the model today. The Standard Play Close is shared scaffolding, not intent. The ICE kind does not change: an ICE's Context is still assembled from memory.
**Business intent check:** none — a framework decision on where agents find memory and what they may do when it holds nothing; no person's business intent changes, and the Business Intent kind's rules stand: only a person confirms or drops one (ADR 031)
**Related:** ADR 029 (drives), ADR 031 (business intent and ICE), ADR 033 (approval in the product model), ADR 008 (issue-centric STM), ADR 011 (STM as inter-skill transport), ADR 001 (three-layer hierarchy), #653, #654, #613 (Kickoff), #606, #641–#644 (the review tool)

## Context

ADR 034, accepted on 18 October, says that inside a drive a play answers from memory and names where each answer came from. A memory review the same day (`.garura/project/issues/613/specs/memory-review.md`) found that memory cannot support that today:

- Three copies of long-term memory exist, and they disagree: the source (`core/components/memory/`), the project copy (`.garura/core/memory/`) and the machine copy (`~/.garura/core/memory/`). The close of 28 of 32 plays reads the project copy. Nothing writes it any more, and projects Garura is installed into do not have it.
- 13 active agents and 32 active skills find memory by hard-coded paths.
- The one shared way in, `ltm_context` (ADR 015), is used by one play.
- ADR 015's rule R4 still lets an agent fall back to the model's own reasoning when memory holds nothing (`standards/rules/resolution.md`). Two agents still fall back to the web or the model.
- Nothing records which memory an answer came from in a way anyone checks.

Kapil chose to fix the whole memory system before the Kickoff drive (#613) is built, as Feature #653. This ADR records the decision that feature builds on. He set the model on 18 October:

> The memory system is accessed primarily by the subagents that we have created. The workflows
> we have placed, like a start change, grill vision, whatnot, make a call to subagents which
> are required for context gathering, and then they move forward. That context gathering is
> essentially where the memory comes from.

Two older records say they change only through a decision record: ADR 016's agent contract ("Any change requires a new ADR") and the knowledge base's design note (`core/components/memory/knowledge/_DESIGN.md`, LOCKED). This ADR is that record for both.

## Decision

### 1. Memory has three tiers

- **Phoenix memory** — the global memory, and the superset. It holds everything in Garura's memory today: the rulebook (rules, templates, schemas) and the knowledge base alike. It lives outside Garura.
- **Garura memory** — the project's long-term memory, inside the project's own `.garura/`. It holds two things: the subset of Phoenix memory this project needs, and what the project makes itself — its product model, its intents, its decisions and the person's answers.
- **Short-term memory** — per issue, in the issue's folder: the plans, specs and context of the work.

Agents also read the project's git repository, its product model and its intents.

Kapil: "Phoenix memory is the superset, and Garura memory is the subset. Phoenix memory gets everything." The project tier is called **Garura memory** — not "project memory" or "LTM" — so it is never confused with the memory Claude Code and Codex keep (Kapil: "ltm = project memory = garura memory. to ensure this is not confused from the memory that claude and codex use. so lets call it garura memory").

### 2. Phoenix memory has one home; a project pulls the subset it needs

- Until Griffin exists, Phoenix memory is its own git repository (for example `phoenix-memory`), cloned onto the machine. Every memory update is a commit, so it has history, review and versions.
- At install, a project pulls a starting set: Garura's rulebook and the memory guide (part 8). It pulls more whenever the tool goes up to Phoenix memory and finds something.
- A short list in the project records what it pulled and from which version of Phoenix memory.
- The two copies installed today, the machine copy and the project copy, give way to these two homes (plan item 3).

Kapil: "garura in each project will pull what the project needs.. but it can always go a level up to phoenix memory to get more if needd. this helps in content management and keep it small and clean".

### 3. Memory is read in order, and the lookup never blocks a play

The tool looks in short-term memory first, then Garura memory, then Phoenix memory. It stops at the first tier that answers. A piece the project has not pulled yet does not stop a play: the tool finds it a level up.

Kapil: "that should not stall garura plays. when needed, it looks hierarchically.. stm - then - ltm - then - global phoenix. this way ifit finds everyting in lowest tier it can stop and the content is protectted. installation is key so that it has some part of LTM build, but this is not blocking".

### 4. One tool finds and updates memory

- Agents and skills never read or write memory by a path. They call one **memory tool**, a command-line tool that both finds memory and updates it.
- The tool covers all three tiers, so every answer is cited the same way.
- The tool sits outside Garura. Today it searches folders. Later Griffin exposes it. Garura and its agents do not change when that happens.
- The tool searches the way Claude Code does: it finds files, searches their text and reads exact lines, with the same kind of tools (`sed`, the shell and the like). On a server later, it runs the same kind of tools.

Kapil: "When the subagent calls the tool, the tool knows to go and search a folder location. That way, tomorrow, when that folder location becomes an API exposed by Griffin, the impact on Garura and the agents is zero because they are always calling the tool." And: "this cli is for reteriving memory and also to update it". And: "this is critical as this is why claude-code is so good".

### 5. Nothing from the model or the web without an approved memory update

- When no tier answers, an agent does not decide from the model's own knowledge or from the web. It raises a **memory update**: what is missing, and a drafted entry.
- The model or the web may help draft the entry. Nothing in it is used until a person approves it.
- The approved update is written to memory first: to Garura memory for something only this project needs, or to Phoenix memory for something any project could use (plan item 5). The waiting work then decides from memory.
- Until the memory review exists (part 7), a person approves a memory update by typing.
- This holds for every agent and skill, run by hand or inside a drive.

Kapil: "If none of this is available, then and only then can subagents, the skills, or whatnot go to the LLM to ask for information or to do web research. At that point in time, human approval is absolutely needed ... we would rather want to first update the memory, the global memory, or the project memory before it can go back into anything else. The system should work only within the memory, but not outside of it." And: "If the system always works with the memory it has, then the drives can make all the decisions all by themselves."

### 6. Every decision names its memory

Every decision an agent makes names the memory it came from: the tier, the file and the lines it rests on. This widens ADR 034 §4 from a play's answers inside a drive to every decision. The shape of an answer and its source is settled in plan item 6.

### 7. A memory review

The review tool gains a **Memory** view, next to Intents and Product. It shows what each tier holds, the memory updates waiting for a person, and which memory each decision came from.

Kapil: "That way, when decisions are made by the underlying agentic systems, it knows which memory it refers to."

### 8. Every install carries the memory system

Installing Garura into a project installs the memory tool and a short memory guide every agent reads: the three tiers, what the tool does, and how memory works. The install checks that the tool works (plan item 7).

Kapil: "Anytime Garura gets installed, every project would need to know what that tool is, what it does, and how the memory works. Otherwise, the subagents will fail."

### 9. What this changes in older records

- **ADR 015** — superseded in part. R1–R4, its fallback to the model, `ltm_context`, the resolution trace built on it, and the learning play's promotion of the model's guesses give way to parts 3 to 6. Its Knowledge File Standard stands.
- **ADR 034 §2** — memory is the three tiers, read through the tool, with the git repository, the product model and the intents. **§3** — when no tier answers, the play raises a memory update a person approves, written to memory first. **§6** — "Run by hand, a play is unchanged" no longer holds for where an agent's answers come from. §4 stands and is widened by part 6.
- **ADR 009 Rule 3** — the memory tool, not a path, is the contract. Rules 1, 2, 4 and 5 stand.
- **ADR 016** — `ltm_context`, `resolution_trace_path` and the Resolution Protocol Hook go. The rest of the contract stands.
- **ADR 017 §1 and §2** — `.garura/core/` no longer holds a synced copy of all memory. The project holds the subset it pulled, with its list.
- **ADR 032 §3** — the review tool has a third view, Memory. The review of a drive's outcome is unchanged.
- **The knowledge base's design note** (`_DESIGN.md`) — the knowledge base lives in Phoenix memory and is searched by the memory tool. "A CLI, not MCP" is kept.

### 10. What this does not change

- Only a person confirms or drops a business intent (ADR 031).
- Short-term memory stays per issue (ADR 008).
- The seven retired agents are left as they are.
- The knowledge base stays behind a command-line tool, not an MCP server.

## Consequences

### Positive

- Agents decide only from memory, so a drive can make its own decisions without the model making things up.
- One home for each tier, one way in, and one way to cite. The three copies that disagree go away.
- Moving to Griffin changes the tool, not Garura or its agents.
- Each project's Garura memory stays small. More is always a level up.
- Every change to Phoenix memory is a commit, with history, review and versions.
- A gap in memory, once filled, is there for the next run.

### Negative / Risks

- **Thin memory means many memory updates at first.** Work that needs one waits for a person. Until the memory review exists, the person approves each one by typing.
- **Garura's rulebook moves into another repository.** A change to a play and to the rule it follows lands in two repositories.
- **A pulled piece can fall behind Phoenix memory.** The list of what was pulled, and from which version, is what shows it.
- **The move is broad.** 13 active agents, 32 active skills and the close of every play name memory paths today. Until each moves, the old and new ways in sit side by side.
- **Search is only as good as the content.** The knowledge base's design note names the real risk: overlapping or conflicting entries "return mush regardless of engine".
- **Not decided here:**
  - whether ADR 034's "learned checkpoint answers" stay on the list of memory (the memory review found they hold checkpoint verdicts, not answers);
  - whether the files a play passes between its own steps (ADR 011; ADR 016's `stm` paths) also go through the tool, or only memory lookups do;
  - whether the rest of a drive goes on while one memory update waits for a person;
  - where in `.garura/` Garura memory lives (plan item 3; ADR 017's whitelist).

## Alternatives Considered

- **Keep ADR 015: R1–R4, with a model fallback that `/learn` promotes later.** Lost: agents would decide from the model first and learn afterwards. Kapil wants memory updated first ("we would rather want to first update the memory … before it can go back into anything else").
- **Global memory holds only knowledge; Garura's rulebook stays with Garura's code.** Lost: Kapil chose everything ("everythign that is in garura … phoenix memory"). The project pulls the subset it needs.
- **Phoenix memory as a plain folder in the home directory, filled by the installer.** Lost: no history, review or versions. Kapil chose its own git repository.
- **A project pulls nothing at install; every piece on first need.** Lost: Kapil chose a starting set at install, never blocking a play.
- **The tool as an MCP server, or a search index (semantic, or numbered nodes).** Lost: the knowledge base's design note already says "server behind a CLI … Not MCP (too expensive per call)", and Kapil wants Claude Code-style search: "this is critical as this is why claude-code is so good".
- **Agents keep reading memory by their own paths.** Lost: the move to Griffin would change every agent. Kapil wants "the impact on Garura and the agents" to be zero.

## Work This Creates

None is filed yet. The stories are filed once this ADR is accepted (`.garura/user-provided/managing-work.md`). They are items 2 to 11 of the feature plan (`.garura/project/issues/653/specs/plan.md`):

- Item 2 — Write the memory tool's contract: its commands to find and update memory, what each returns, and its errors.
- Item 3 — Set up Phoenix memory, seeded from `core/components/memory/`, and the subset each project pulls; retire the two stale copies.
- Item 4 — Build the memory tool, with a folder engine across the three tiers.
- Item 5 — Memory updates instead of guesses: raise, approve, write, and decide from memory.
- Item 6 — Every decision names its memory, and a script checks each source.
- Item 7 — Every Garura install carries the memory tool, the memory guide and a check.
- Item 8 — Move Kickoff's agents and skills, and every play's close, onto the tool.
- Item 9 — Prove it on `/intent`, `/vision` and `/understand`, run by hand on a test project.
- Item 10 — Move every other agent and skill onto the tool; rewrite R1–R4; a lint rule fails any component that names a memory path.
- Item 11 — The memory review: a Memory view in the review tool (extends #641–#644).

## References

- `.garura/project/issues/653/specs/plan.md` — the feature plan; item 1 is this ADR, items 2 to 11 the work it creates
- `.garura/project/issues/613/specs/memory-review.md` — the memory review of 18 October
- `core/components/memory/knowledge/_DESIGN.md` — the knowledge base's design note (LOCKED)
- `core/components/memory/standards/rules/resolution.md` — R1–R4 today
- ADR 015 — LTM resolution protocol; ADR 034 — plays answer from memory inside a drive; ADR 009, ADR 016, ADR 017, ADR 032
