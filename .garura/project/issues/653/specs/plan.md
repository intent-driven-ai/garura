---
plan_for: 653
kind: feature
serves: "#653 — agents work only from memory, so drives can make their own decisions"
status: active
updated: 2026-10-18
now: 5
serves_plan: 606
serves_item: 8
---

# Plan — #653: Garura's memory system

This is a plan, not a design. It says what gets done, in what order, and why
that order. How each item is built is decided in its own issue.

Kapil chose B on 2026-10-18: fix the whole memory system now, before the
Kickoff drive is built, as its own feature with its own issues and branches.
Filed as Feature #653 under #606. It was drafted in #613's folder and moved here.

## What we are trying to reach

**Kapil's model** (2026-10-18). Plays call sub-agents to gather context, and
that is where memory is read. Memory has three tiers:

- **Phoenix memory** — the global memory, and the superset: it holds
  everything that is in Garura's memory today, the rulebook (rules, templates,
  schemas) and the knowledge alike. It lives outside Garura (in Griffin, later).
- **Garura memory** — the project's long-term memory, inside the project's own
  `.garura/`. It holds the subset of Phoenix memory this project needs, pulled
  in when Garura is installed and whenever more is needed, and what the project
  makes itself (its product model, intents, decisions, and the person's
  answers). Kapil named it Garura memory so it is never confused with the memory
  Claude Code and Codex keep.
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

A **Memory and ADRs** section, in the review tool beside Intents and Product,
shows what each tier holds, the memory updates and ADRs waiting for a person,
and which memory each decision came from (ADR 036 §7).

**What is true today** (`.garura/project/issues/613/specs/memory-review.md`, and a map of every agent):
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
- When Garura memory has no answer, the tool goes up to Phoenix memory
  before anything else.
- Every Garura install carries the tool and a short memory guide, and checks
  the tool works, so agents in any project know the three tiers and how to use
  them.
- The tool searches like Claude Code and returns, for every result, the tier,
  the file, the lines and a fingerprint of the text. Missing memory is an
  error, never "nothing found".
- Nothing comes from the model or the web unless a person approved a memory
  update first, and the decision was then made from memory.
- Every decision an agent makes names the memory it came from, and a script
  checks the source exists and has not changed.
- The Memory and ADRs section shows the tiers, the waiting updates and ADRs, and
  each decision's source; a person answers them on the Catch up cards.
- Moving the tool to Griffin means changing one setting.

## Where we are now

Decided, and four pieces shipped: ADR 035 and ADR 036 (#654, #667), the contract (#655),
Phoenix memory with `pull` and `pulled` (#656), and the memory tool (#657, PR #674).
Next: item 5, memory updates (#658), starting with the two fixes from the #674 review.

## The plan, in order

### Done

- **1. Decided: the memory system** — #654. ADR 035, accepted by Kapil on 18 October
  (`docs/adr/035-agents-work-only-from-memory.md`). Three tiers
  (Phoenix memory, Garura memory, short-term memory); lookup order short-term →
  Garura → Phoenix, stopping at the first tier that answers and never blocking a
  play; one tool that finds and updates memory; a memory update a person
  approves before any model or web answer; every decision names its memory.
  Supersedes ADR 015 in part; amends ADR 034, 009, 016, 017 and 032. Amended
  the same day by ADR 036 (#667,
  `docs/adr/036-approved-answer-lands-in-short-term-memory.md`): short-term
  memory is the current issue only; an approved researched answer lands in the
  issue's short-term memory, and promotion to Garura or Phoenix memory happens
  outside the work; a person's own answer goes to Garura memory; learned
  checkpoint answers are not memory; a play's own working files stay direct;
  memory and ADRs are reviewed in the review tool's Memory and ADRs section.
  Still open: whether a drive keeps going while one update waits, and the
  folder for Garura memory.
- **2. Built: the memory tool's contract** — #655. Version 1 in
  `core/tools/memory/contract/v1.json`, with a plain guide, 20 sample answers,
  23 broken samples and a check with its own tests. Eleven commands; every piece
  of text carries tier, file, lines and fingerprint; a lookup never skips a tier;
  every lookup names its issue, and short-term memory is that issue only.
  Settled with Kapil: learned checkpoint answers are not memory; a play's own
  working files stay direct; an approved researched answer goes to the issue's
  short-term memory, and promotion happens outside the work. Lands with #655's
  pull request.

- **3. Shipped: Phoenix memory and pull** — #656, PR #671, merged 18 October. `intent-driven-ai/phoenix-memory` (private) holds all of `core/components/memory/`; `pull` and `pulled` (`core/tools/memory/pull.py`) bring a piece into Garura memory and show what is behind; dead memory settings removed; the PR review rules are read from Garura memory. Changed on Kapil's word: the installer pulls nothing (three set-up plays will fill a project's first memory), `core/components/memory/` is removed after the memory tool (item 10), and the `.garura/` clean-up is #670. ADR 035 §2 still needs its amendment (its own `/adr` change).
- **4. Shipped: the memory tool** — #657, PR #674, approved by Kapil on 18 October.
  `core/tools/memory/memory.py` finds, searches and reads across short-term, Garura and
  Phoenix memory in that order, reads Phoenix memory only at its approved version, and
  pulls a Phoenix file into Garura memory when it is read. Contract version 2: a lookup of
  Garura or Phoenix memory works without an issue. Kapil's login and change-password test
  passed on a fresh project. No agent calls it yet (item 8). ADR 035 §2 and ADR 036 §1
  need amending for these decisions.

### 5. Memory updates instead of guesses — now

**Issue:** #658. Its plan: `.garura/project/issues/658/specs/plan.md`.
**First:** two faults from the PR #674 review, fixed before any agent uses the tool: the
contract's `pull` request (`{path}`) is refused by the tool; and a read from Phoenix
memory can overwrite a different file at the same path in Garura memory.
**What:** when no memory answers, the agent raises a memory update: what is
missing, which tier it belongs in, a drafted entry, and where the draft came
from (the person, the web, the model — marked). Nothing is used until a person
approves it. The approved answer is written to the issue's short-term memory,
and the waiting work decides from memory (ADR 036 §2). A draft from the web or
the model never goes straight to Garura or Phoenix memory. Moving an answer up
— to Garura memory for something only this project needs, to Phoenix memory
for something any project could use — is a promotion: its own memory update, a
person approves it, and it happens outside the work (ADR 036 §3). A person's
own answers to questions become Garura memory
with stable ids, so they are never asked twice (Garura's existing question
store, `standards/rules/product.md` rule 12). The knowledge-base proposal
(`propose-kb-node`) becomes one kind of memory update. Until the memory review
exists, the person approves by typing.
Kapil, 2026-10-18 (#657 plan, item 1): memory updates land in short-term
memory only. Moving them up is a set of plays, not this tool: `learn` reads
short-term memory and learns into Garura memory; `promote` sends a version of
Garura memory to Phoenix memory for an approval that sits outside Garura, and
the reader cannot use Phoenix memory until it is approved. Kapil named three
plays and described two; the plays are not filed yet.
**Why here:** without it, "only from memory" stops every time memory is thin.
**Done when:** a gap, an update, an approval, a write and an answer from memory
run end to end on a sample.
**Needs:** item 4.

### 6. Every decision names its memory

**Issue:** #659.
**What:** one shape for an answer and its source, built on the trace format
Garura already has. Agents write it to short-term memory; a script checks each
named source exists and its fingerprint still matches; a drive's review record
carries them.
**Why here:** the memory review and the drive's review both show these.
**Done when:** the check fails an answer that names no source, or a source that
changed.
**Needs:** item 4.

### 7. Every Garura install carries the memory system

**Issue:** #660.
**What:** installing Garura into a project installs the memory tool and a short
memory guide every agent reads: the three tiers (Phoenix memory, Garura memory,
short-term memory), what the tool does, how to find memory, go up to
Phoenix memory, update it, name a source, and raise a memory update. The
install checks the tool runs and reaches each tier, and fails if it does not.
Kapil, 2026-10-18: the three tiers "should be part of the Garura installation.
Anytime Garura gets installed, every project would need to know what that tool
is, what it does, and how the memory works. Otherwise, the subagents will fail."
**Why here:** the agents moved in items 8 and 10 rely on it in every project,
not only in Garura's own repo.
**Done when:** a fresh install into a test project has the tool and the guide,
its check passes, and an agent there finds a piece of memory through the tool.
**Needs:** items 3 to 6.

### 8. Move Kickoff's agents and skills onto the tool

**Issue:** #661.
**What:** the agents and skills `/intent`, `/vision` and `/understand` use, and
the close of every play, read memory only through the tool, raise memory
updates, and name their sources. Play changes go through each play's ICE source
and `/play-editor`.
Also: rule 4 of the drive contract, its row in the rules index and the
glossary's Drive entry say what ADR 034 and ADR 035 decided.
Kapil, 2026-10-18 ("1"): agents move after items 5 to 7, so each agent changes once,
with lookup, memory updates and named sources together. Only agents call the tool and
build context; skills read short-term memory only (Kapil, 2026-10-18), so the story
texts of #661 and #663 ("agents and skills") need that fix when Kapil asks.
**Why here:** Kickoff waits on these three plays, so they move first.
**Done when:** the three plays and every play's close name no memory path.
**Needs:** items 5, 6 and 7.

### 9. Prove it on Kickoff's three plays

**Issue:** #662.
**What:** run `/intent`, `/vision` and `/understand` by hand on a test project:
every answer names its memory, a gap raises an update, nothing comes from the
model alone.
**Why here:** only a real run shows the system works before a drive relies on it.
**Done when:** the run is recorded.
**Needs:** item 8.

### Milestone: the Kickoff drive can be built

#613 picks up again here, at the runner's design. Items 10 and 11 run alongside
the Kickoff build.

### 10. Move every other agent and skill onto the tool

**Issue:** #663.
**What:** the remaining active agents and skills, including the two that still
fall back to the web or the model (`tech-designer`, `research-domain-context`);
the R1–R4 rule rewritten; a lint rule that fails any component naming a memory
path. The seven retired agents are not installed and are left as they are.
Also: `CLAUDE.md`, `docs/components/memory.md` and the glossary's install rows
describe the three tiers and the tool, and the locked knowledge-base design note
(`knowledge/_DESIGN.md`) is rewritten under ADR 035.
**Done when:** the lint passes across every component.
**Needs:** item 9.

### 11. The memory review

**Issue:** #664.
**What:** a third section in the review tool, **Memory and ADRs**, next to
Intents and Product. It shows short-term, Garura and Phoenix memory: what each
tier holds, the memory updates waiting for a person (accept, send back, drop,
or leave for later), and which memory each decision came from. It also shows the ADRs waiting for a
person. Every memory review and ADR review happens there, with the same card
method as intents and product: Catch up (#644), one card per change, swipe
right to accept, swipe left to leave for later.
**Done when:** a person approves a memory update and accepts an ADR on a card
in the tool, and sees a decision's source there.
**Needs:** items 5 and 6, and the review tool (#641–#644).
**Also:** decided in ADR 036 §7 (#667). Building it includes the `/adr` intent
change: its pinned accept, typed today, moves onto a card in this section,
through its ICE source and `/play-editor`. Two points stay open in ADR 036 and
are settled with Kapil before building: whether a product decision waiting for
a person is reviewed here or under Decisions in the Product view, and who
writes the approval when a person swipes right (ADR 033 §6).

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
- 2026-10-18 — Kapil: the memory system is part of every Garura install, or the
  sub-agents fail. Added item 7 (every install carries the tool, the memory
  guide and a check); items 7 to 10 became 8 to 11. The Kickoff milestone now
  follows item 9.
- 2026-10-18 — Kapil: "file the memory feature". Filed Feature #653 under #606
  and Spike #654 (item 1) under #653. Moved this plan from #613's folder. The
  stories for items 2 to 11 wait for item 1's accepted decision, per the filing
  rules (a story is filed once its feature's decision is settled).
- 2026-10-18 — Item 1 done: ADR 035 accepted. Kapil named the project tier
  **Garura memory** ("ltm = project memory = garura memory"), so it is not
  confused with the memory Claude Code and Codex keep. Now on item 2; its story
  is filed once Kapil says so (#654 plan item 2).
- 2026-10-18 — Kapil: "file the stories". Items 2 to 11 filed as Stories #655 to #664 under #653 (texts: `.garura/project/issues/654/specs/stories.yaml`).
- 2026-10-18 — Kapil: "update the stories … merge this as part of our current
  plan". The files ADR 035 names under Affects that no story covered were added
  to existing items, not new ones: config keys to item 3 (#656), the drive
  contract's rule 4 to item 8 (#661), the docs, glossary rows and the locked
  knowledge-base design note to item 10 (#663). The three stories were edited to
  match.
- 2026-10-18 — Item 2 built on #655: the contract, samples and check. Now on item 3 (#656).
- 2026-10-18 — Kapil, on where reviews happen: "There needs to be a third
  section of memory and ADRs in it, where it should be showing the STM, LTM,
  and Phoenix memory allowed. Any reviews that happen happen there, and the
  same card sweeping next method should be used." Item 11 now reads Memory and
  ADRs, with the Catch up cards (#644).
- 2026-10-18 — Kapil, on #655: when no tier answers, a person approves the
  researched answer and it goes into the issue's short-term memory; promotion
  to Garura or Phoenix memory happens outside the work. Short-term lookups read
  only the current issue. This touches item 5 (#658): an approved update lands
  in short-term memory first. ADR 035 §5 needs an amendment for it.
- 2026-10-18 — ADR 036 accepted by Kapil (#667): "accept and update plan. pdate
  items and story 664. pdate adr". Item 1 names it; item 5 now writes the
  approved answer to the issue's short-term memory, with promotion as its own
  update; item 11 points to ADR 036 §7. Story #664 rewritten to match. The
  review tool plan (`.garura/project/issues/617/specs/review-tool.md` §4) gains
  the third section. Story #658's filed text still says the approved update is
  written to Garura or Phoenix memory; item 5 here holds the current rule.
- 2026-10-18 — Item 3 done: #656 merged (PR #671). Now item 4 (#657).
- 2026-10-18 — Kapil: memory updates land in short-term memory only; `learn` and `promote` plays move memory up; unapproved Phoenix memory is not read (item 5 note).
- 2026-10-18 — Kapil kept the order: the agents move onto the tool in #661 after #658–#660, not right after #657. No agent calls the tool yet.
- 2026-10-18 — Item 4 done: #657 approved by Kapil (PR #674). Now item 5 (#658).
