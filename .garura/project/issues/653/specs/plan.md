---
plan_for: 653
kind: feature
serves: "#653 — agents work only from memory, so drives can make their own decisions"
status: active
updated: 2026-10-20
now: 10
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
- The review tool's ADRs, Memory and Agent decisions sections (ADR 037) show the tiers,
  the waiting updates and ADRs, and each decision's trace; a person answers them on the
  Catch up cards.
- Moving the tool to Griffin means changing one setting.

## Where we are now

Decided, and nine pieces shipped: ADR 035 to ADR 040 (#654, #667, #659, #660, #661), the
contract (#655), Phoenix memory (#656), the memory tool (#657), memory updates (#658, PR #675),
decision traces (#659, PR #676), every install carrying the memory system (#660, PR #677),
Kickoff's plays getting memory only from their agents (#661, PR #678) and the proof on a test
project (#662, PR #679). The Kickoff milestone is passed: #613 picks up again. Next: item 10,
every other agent and skill onto the tool (#663), alongside the Kickoff build.

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
- **11. Moved: the memory review** — #664 is built with the whole review tool, all (2026-10-20: the review tool is now Argus, a Phoenix tool; #664 sits under its Feature #681.)
  sections inside Garura (since 2026-10-19: ADRs, Memory with Ask memory, and Agent
  decisions, in place of one "Memory and ADRs" section), in the #606 plan (item 8, the review). Kapil, 2026-10-18 (#658): "we will build the tool with all the sections inside garura - as part of 606 plan. it remains a local prototype for now."
  Until then, a local prototype page approves memory updates (#658 plan, item 5).
- **5. Shipped: memory updates** — #658, PR #675, approved by Kapil on 18 October. When
  no tier answers, an agent raises an update in the issue's short-term memory ("STM -
  always STM"), a person approves or rejects each one in the review tool (a local page on
  the tool's design until it is built), and the approved answer is written to the issue's
  short-term memory. A drive keeps going unless an update blocks. Contract version 3.
  Moving memory up is `/learn-memory` and `/promote-memory` (not filed). ADR 035 §5 and
  ADR 036 §2–§4 need amending.
- **6. Shipped: every decision keeps a trace** — #659, PR #676, approved by Kapil on 19
  October after a rejected first round. Each agent decision keeps a trace: the steps the
  agent took, each with its memory lines, the exact text, the memory version and the lines
  around (Kapil: "these are called traces"). `cite` and `citations` in the memory tool
  (contract version 4); the drive review record carries the decisions; the rule's "Every
  Decision Names Its Memory" section is in Garura and Phoenix memory; ADR 037 amends ADR
  035 §6/§7, ADR 036 §7 and ADR 032 §3, and the review tool has five sections. No agent
  calls `cite` yet (#661, #663).

- **7. Shipped: every install carries the memory system** — #660, PR #677, approved by Kapil
  on 19 October after two review rounds. Every install, by the play or the public installer
  (`installer/install.sh`), lays the memory tool at `.garura/tools/memory/` with its settings,
  short-term memory's folder, and the memory guide every agent reads
  (`.claude/rules/garura-memory.md`, or a marked block in `AGENTS.md` for Codex), and checks
  the tool reaches short-term and Garura memory. The install brings no memory: the tool
  downloads Phoenix memory on first use, with a time limit. ADR 038 (Kapil accepted it)
  records this and amends ADR 035 §2, §3, §4, §8 and ADR 017 §1, closing the amendment item 3
  left owed. A real sub-agent in a fresh project found memory through the tool from the guide
  alone. Not run: a Codex agent. `initialize` is not built.
- **8. Shipped: Kickoff's plays get memory only from their agents** — #661, PR #678, approved by
  Kapil on 20 October after two review rounds. ADR 039 (every memory write goes to short-term
  memory; a play reads no memory; the tool copies nothing; Phoenix memory at
  `~/.phoenix/core/memory`; the `.garura/` layout; `template-manager`; the judge prompt in
  `judge-grounding`; shared play blocks in one file) and ADR 040 (the config's source is
  `core/config.yaml`), both accepted by Kapil. `/intent`, `/vision` and `/understand` read no
  memory; `product-os-keeper` and `business-intent-keeper` read it only through the tool; every
  play's close lives in `core/components/plays/_shared/play-close.md`; the Kickoff runs live
  under the issue being worked on (Kapil: the issue ID governs); the knowledge router is
  removed. Proven by `/intent`'s draft step on a test project. Phoenix memory updated to match.
- **9. Shipped: Kickoff's three plays run from memory alone** — #662, PR #679, approved by Kapil
  on 20 October after two review rounds. On a test project, under one drive contract: 30 decision
  records, every one with a trace; a memory update raised by `/vision`, approved by Kapil and used
  by 14 `/understand` decisions; no answer from the model alone. Fixed from the run: typed
  approvals (`decided_in: session`, contract 5.1), decisions name their update, each issue keeps
  its own gate history, the judge's guidance per stage, `/intent`'s shared contract check.
  Written down for their own issues: the close not asking `template-manager`, a drive's
  uncommitted run files (#613), model-only drafts in a headless run.

### Milestone: the Kickoff drive can be built — passed (20 October, #662)

#613 picks up again here, at the runner's design. Items 10 and 11 run alongside
the Kickoff build.

### 10. Move every other agent and skill onto the tool — now

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

### Not yet placed: `initialize`, the play that sets up a project's memory

**Issue:** none yet.
**What:** a new play, run after the install. It reads Phoenix memory and asks the person
questions built from it — which domains, which functionalities, what technology
standards, tools and frameworks — each with choices to pick from, never something
random. The answers set up the project's Garura memory. Kapil, 2026-10-19: "After the
installation is finished, we then run a play. This play is not designed yet, and that
play is going to ask questions. That will read the Phoenix memory and will start setting
up the project's memory." And: "After install, let's call this whole thing
`initialize`." It is not designed yet; where it sits in this order is not decided.

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
- 2026-10-18 — Item 11 moved: the memory review (#664) is built with the review tool in the #606 plan.
- 2026-10-18 — Item 5 done: #658 approved by Kapil (PR #675). Now item 6 (#659).
- 2026-10-19 — Item 6 done: #659 approved by Kapil (PR #676, round 2); ADR 037 accepted. Now item 7 (#660).
- 2026-10-19 — Item 7 (#660) started. Kapil: the install brings no memory; the tool downloads Phoenix memory on first use; a new play, `initialize`, sets up a project's memory after the install (added as not yet placed).
- 2026-10-19 — Item 7 done: #660 approved by Kapil (PR #677, round 2); ADR 038 accepted (the install brings no memory; the tool in the project). Now item 8 (#661).
- 2026-10-20 — Item 8 done: #661 approved by Kapil (PR #678, round 2); ADR 039 and ADR 040 accepted. Now item 9 (#662).
- 2026-10-20 — Item 9 done: #662 approved by Kapil (PR #679, round 2). The Kickoff milestone is passed; #613 picks up. Now item 10 (#663).
