---
plan_for: none yet — a draft; it moves to its own issue's folder once filed
kind: feature
serves: "#606 — drives make their own decisions because they work only from memory"
status: draft
updated: 2026-10-18
now: 1
---

# Plan — Garura's memory system

This is a plan, not a design. It says what gets done, in what order, and why
that order. How each item is built is decided in its own issue.

Kapil chose B on 2026-10-18: fix the whole memory system now, before the
Kickoff drive is built, as its own feature with its own issues and branches.
This plan is drafted inside #613 because no issue holds it yet.

## What we are trying to reach

**Kapil's model** (2026-10-18). Plays call sub-agents to gather context, and
that is where memory is read. Memory has three tiers:

- **Phoenix memory** — the global memory, and the superset: it holds
  everything that is in Garura's memory today, the rulebook (rules, templates,
  schemas) and the knowledge alike. It lives outside Garura (in Griffin, later).
- **Project memory** — long-term memory inside the project's own `.garura/`, in
  two parts: the **Garura memory** — the subset of Phoenix memory this project
  needs, pulled in when Garura is installed and whenever more is needed — and
  what the project makes itself (its product model, intents, decisions, and the
  person's answers).
- **Short-term memory** — per issue: the plans, specs and context of the work.

Kapil, 2026-10-18: "Phoenix memory is the superset, and Garura memory is the
subset. Phoenix memory gets everything." A project pulls only what it needs, and
can always go a level up to Phoenix memory for more. That keeps each project's
memory small and clean.

Agents also read the git repository, the product model and the intents.
**Only when none of these holds an answer** may an agent go to the model or the
web — and then only through a **memory update** a person approves. The update
is written into memory first, and the decision is then made from memory. "The
system should work only within the memory." That is what lets a drive make its
own decisions.

Agents never read or write memory by a path. They call **one memory tool**, a
command-line tool that both **finds memory and updates it**. Today it works on
folders; later it calls Griffin; agents and Garura do not change.
The tool **searches the way Claude Code does** — find files, search their text,
read exact lines — on the laptop now, and the same way on the server later
(Kapil: "this is critical as this is why claude-code is so good").

A **memory review**, in the review tool beside Intents and Product, shows what
each tier holds, the memory updates waiting for a person, and which memory each
decision came from.

**What is true today** (`specs/memory-review.md`, and a map of every agent):
memory is files that each agent and skill finds by its own path. Three copies of
long-term memory exist and disagree. 13 active agents and 32 active skills name
memory paths directly; every play's close reads a copy installed projects do not
have. The one shared way in (`ltm_context`, ADR 015) is used by one play. Two
agents still fall back to the web or the model's own reasoning, which ADR 015
allows and ADR 034 now forbids inside a drive. Nothing records which memory an
answer came from in a way anyone checks.

## When this plan is done

- Every agent and skill reads and updates memory only through the memory tool;
  a lint check fails any component that names a memory path.
- Phoenix memory has one home outside Garura. Each project holds only the subset
  it pulled, and knows which version of Phoenix memory each piece came from, so
  it can tell when a piece is behind.
- When the project's memory has no answer, the tool goes up to Phoenix memory
  before anything else.
- The tool searches like Claude Code and returns, for every result, the tier,
  the file, the lines and a fingerprint of the text. Missing memory is an
  error, never "nothing found".
- Nothing comes from the model or the web unless a person approved a memory
  update first, and the decision was then made from memory.
- Every decision an agent makes names the memory it came from, and a script
  checks the source exists and has not changed.
- The memory review shows the tiers, the waiting updates and each decision's
  source.
- Moving the tool to Griffin means changing one setting.

## Where we are now

Reviewed, nothing built. The review (`specs/memory-review.md`) and the map of
how agents read memory are done. Kapil set the model above and chose B. Next:
item 1, the decision record.

## The plan, in order

### 1. Decide the memory system — now

**Issue:** none yet.
**What:** record Kapil's model as an ADR: the three tiers and what lives in
each, and where the git repo, product model and intents fit; Phoenix memory as
the superset, holding everything in Garura's memory, with one home outside
Garura's code; the Garura memory in a project as the subset it pulls, and going
up to Phoenix memory for more; the memory tool as the only way to read and
update memory (a command-line tool, Claude Code-style search, folders now,
Griffin later); the order agents read in (the issue's short-term memory, then
the project, then Phoenix memory); no answer from the model or the web without an approved
memory update; how a memory update starts, who approves it, where it is
written, and how the waiting work picks up again; every decision names its
memory.
**Why here:** it replaces ADR 015 (the R1–R4 rule, its model fallback, and
`ltm_context`) and changes ADR 034, ADR 009, ADR 017 and the locked knowledge
base design note — each needs a decision record before anything is built.
**Done when:** the ADR is accepted, made with `/adr`.
**Needs:** nothing.

### 2. Write the memory tool's contract

**Issue:** none yet.
**What:** the written agreement between agents and the tool: its commands to
find memory (find, search, read, go up to Phoenix memory, cite) and to update it
(pull a piece into the project, propose an update, list updates, apply an
approved update),
what each returns, and its errors. Same rules as the review tool: its own
folder, a version number, no Garura names inside, the engine behind it
swappable.
**Why here:** every later item builds against it, and it is what makes the move
to Griffin cost nothing.
**Done when:** the contract file exists and sample answers pass its check.
**Needs:** item 1.

### 3. Set up Phoenix memory, and the subset each project pulls

**Issue:** none yet.
**What:** Phoenix memory gets its one home outside Garura's code, seeded from
everything in `core/components/memory/` (the shelves deleted in #434 left
out). Installing Garura no longer copies all of memory: it pulls the subset the
project needs into the project's Garura memory, and records which version of
Phoenix memory each piece came from. The two stale copies are retired
(`~/.garura/core/memory/` and `.garura/core/memory/`). The installer writes
correct settings into projects it installs into. Project memory's own folders
are settled (product model, the person's own files, the person's answers).
**Why here:** the tool needs a known place for each tier.
**Done when:** an install into a test project pulls only what it needs, a piece
pulled later arrives on request, and a check shows which pulled pieces are
behind Phoenix memory.
**Needs:** item 1.

### 4. Build the memory tool

**Issue:** none yet.
**What:** the command-line tool from the contract, with a folder engine that
finds, searches and reads exact lines across the three tiers, going up to
Phoenix memory when the project has no answer, and that writes approved updates
and pulls pieces into the project. Every result carries its tier, file, lines
and fingerprint. It works the same from Claude Code and Codex.
**Why here:** items 5 to 8 call it.
**Done when:** its tests pass on sample memory, and nothing in its folder names
Garura.
**Needs:** items 2 and 3.

### 5. Memory updates instead of guesses

**Issue:** none yet.
**What:** when no memory answers, the agent raises a memory update: what is
missing, which tier it belongs in, a drafted entry, and where the draft came
from (the person, the web, the model — marked). Nothing is used until a person
approves it. The approved update is written to its tier — the project's own
memory for something only this project needs, Phoenix memory for something any
project could use — and the waiting work decides from memory. A person's answers to questions become project memory
with stable ids, so they are never asked twice (Garura's existing question
store, `standards/rules/product.md` rule 12). The knowledge-base proposal
(`propose-kb-node`) becomes one kind of memory update. Until the memory review
exists, the person approves by typing.
**Why here:** without it, "only from memory" stops every time memory is thin.
**Done when:** a gap, an update, an approval, a write and an answer from memory
run end to end on a sample.
**Needs:** item 4.

### 6. Every decision names its memory

**Issue:** none yet.
**What:** one shape for an answer and its source, built on the trace format
Garura already has. Agents write it to short-term memory; a script checks each
named source exists and its fingerprint still matches; a drive's review record
carries them.
**Why here:** the memory review and the drive's review both show these.
**Done when:** the check fails an answer that names no source, or a source that
changed.
**Needs:** item 4.

### 7. Move Kickoff's agents and skills onto the tool

**Issue:** none yet.
**What:** the agents and skills `/intent`, `/vision` and `/understand` use, and
the close of every play, read memory only through the tool, raise memory
updates, and name their sources. Play changes go through each play's ICE source
and `/play-editor`.
**Why here:** Kickoff waits on these three plays, so they move first.
**Done when:** the three plays and every play's close name no memory path.
**Needs:** items 5 and 6.

### 8. Prove it on Kickoff's three plays

**Issue:** none yet.
**What:** run `/intent`, `/vision` and `/understand` by hand on a test project:
every answer names its memory, a gap raises an update, nothing comes from the
model alone.
**Why here:** only a real run shows the system works before a drive relies on it.
**Done when:** the run is recorded.
**Needs:** item 7.

### Milestone: the Kickoff drive can be built

#613 picks up again here, at the runner's design. Items 9 and 10 run alongside
the Kickoff build.

### 9. Move every other agent and skill onto the tool

**Issue:** none yet.
**What:** the remaining active agents and skills, including the two that still
fall back to the web or the model (`tech-designer`, `research-domain-context`);
the R1–R4 rule rewritten; a lint rule that fails any component naming a memory
path. The seven retired agents are not installed and are left as they are.
**Done when:** the lint passes across every component.
**Needs:** item 8.

### 10. The memory review

**Issue:** none yet — it extends the review tool's stories (#641–#644).
**What:** a Memory view in the review tool, next to Intents and Product: what
each tier holds, the memory updates waiting for a person (approve, change,
reject), and which memory each decision came from.
**Done when:** a person approves a memory update and sees a decision's source in
the tool.
**Needs:** items 5 and 6, and the review tool (#641–#644).

## Log

- 2026-10-18 — Drafted in #613 from Kapil's memory model (three tiers; one tool;
  memory updates before any model or web answer; a memory review; Griffin
  later; Claude Code-style search), his choice B, the memory review, and a map
  of how every agent reads memory today. Not filed; no issue holds it yet.
- 2026-10-18 — Kapil's answers: the tool both finds and updates memory; the work
  is its own feature, with its own issues and branches; global memory is
  **Phoenix memory**, the superset holding everything in Garura's memory; the
  Garura memory in a project is the subset it pulls, and it can go up to
  Phoenix memory for more ("keep it small and clean"). Items 1 to 5 changed to
  match.
