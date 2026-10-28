# ADR 059 — The Discovery Loop's Knowledge Step Is One Step Run by One Agent, the Three Knowledge Plays Are Removed, and the Memory That Taught Them Is Corrected

**Status:** Accepted
**Date:** 2026-10-28
**Level:** framework
**Decided by:** Kapil Viren Ahuja
**Decided in:** #920 (the knowledge steps become skills), the session of 2026-10-28; design `.garura/project/issues/920/specs/redesign.md`
**Supersedes:** ADR 042 (in full — the three knowledge member plays; what still holds of its §2, §3 and §4 is restated here, parts 4 and 5)
**Amends:** ADR 041 — §3 "Before it asks, the drive builds the memory it lacks" (as amended by ADR 042): the work is one step of the loop, run by the `knowledge-builder` agent, not member plays; §4 "Member plays" (as amended by ADR 042, and by ADR 043's pointer): a loop has no member plays; §5 "The person's questions, when they come" (as amended by ADR 042): the person gets the knowledge brief, restated in part 4 · ADR 039 — §2 "A play is a pure workflow and reads no memory" and §10's line on ADR 035 §4 ("only agents call the tool"), as amended by ADR 042: the one read-only exception, the memory tool's `updates`, passes from "a knowledge play's own check script" to the Discovery loop's scripts `check_knowledge.py` and `round_state.py`; the rest of §2 stands, and no skill calls the tool · ADR 044 — §1 "The Shared Drive Run owns the steps between plays" (now the Shared Loop Run, ADR 045): its run steps gain the knowledge step (R5c close the open questions, R5b show the knowledge brief and record the reply); it is a run step, not a product rule, so the rest of §1 stands · ADR 046 — §4 "Plays take the verb of what they do", the clause "knowledge plays `search`, `research`, `check`": there are no knowledge plays; `check` stays a change-play verb, and the skill verb `research` (§5) stands
**Affects:** removed — `core/components/plays/search-knowledge/`, `core/components/plays/research-knowledge/`, `core/components/plays/check-knowledge/` (each `SKILL.md`, `reference/`, `scripts/`, `stop-condition.yaml`); the agent and skills — `core/components/agents/knowledge-builder.md`, `core/components/skills/author-knowledge-page/SKILL.md`, `core/components/skills/author-knowledge-brief/` (`SKILL.md`, `scripts/render_brief.py`), `core/components/skills/find-answers-in-sources/SKILL.md`, `core/components/skills/propose-answers/SKILL.md`; the loop — `core/components/loops/complete-discovery/` (`SKILL.md`, `reference/ice.md` C5, `scripts/loop_preflight.py`, `scripts/round_state.py`, and new loop scripts `group_questions.py`, `check_knowledge.py`, `record_review.py`), `core/components/loops/_shared/loop-run.md` (R5c, R5b); the loop builders — `core/components/plays/create-loop/` (`SKILL.md`, `references/loop_preflight.py`, `references/test_loop_scripts.py`, `references/compiled-loop-example/`, `scripts/lint_loop.py`), `core/components/plays/edit-loop/scripts/lint_loop.py`; the memory rules, corrected in source and then promoted to Phoenix memory — `core/components/memory/standards/rules/_index.md`, `pipeline-next.md`, `pipeline-position.md`, `loop-contract.md`, `naming.md`, `naming.yaml`, `rename-map.yaml`; Phoenix memory — `standards/rules/_index.md`, `pipeline-next.md`, `pipeline-position.md` and `standards/templates/adr.md` corrected, `loop-contract.md`, `naming.md`, `naming.yaml` and `rename-map.yaml` added; docs and install — `core/grounding/glossary.md` (the Loop entry), `docs/components/plays.md`, `docs/components/loops.md`, `docs/components/agents.md`, `docs/components/skills.md`, `core/components/plays/install-garura/scripts/install.py`; the product model — `.garura/product/product-os/features/fn-744/feature.md`; decision records — `core/components/memory/standards/templates/adr.md` (the section for the person who accepts a record, and its rule; promoted to Phoenix memory too), `core/components/skills/author-decision/SKILL.md` (writes that section), `core/components/agents/adr-keeper.md` (gathers its points; reaches memory only through the memory tool)
**ICE impact:** Agent intents change for the Discovery loop and the `knowledge-builder` agent. The loop's C5 stops naming `/search-knowledge` and `/research-knowledge`: before it asks, the loop runs one step that closes the open questions (an intent change, through `/edit-loop`). The agent gets one contract for the whole step and calls the skills and the memory tool itself. `author-knowledge-page` only drafts the page and stops calling the memory tool. The three plays' own ICE go with them. `/create-loop` compiles every new loop with this step and no member plays. `propose-answers` is unchanged for `/shape-slice`. The `adr-keeper` agent also gathers the points for the person who accepts a record, and reaches memory only through the memory tool; `author-decision` writes those points as their own section. No ontology kind changes; the ICE kind keeps its shape.
**Business intent check:** none — a framework decision on how a loop closes its open questions, how it reaches memory, and how a decision record is written; no person's business intent changes, and the Business Intent kind's rules stand (ADR 031)
**Related:** ADR 029, ADR 035, ADR 038, ADR 039, ADR 041, ADR 042, ADR 043, ADR 044, ADR 045, ADR 046, #920, #921, #899, #686

## Context

When a round of the Discovery loop ends with questions none of its plays answered, the loop must
close them before it asks the person: answer what the prototype shows, answer what memory holds,
draft a researched page for what research can answer, propose an answer for what only the person
can confirm, and write the brief the person reads.

ADR 042 made that work three plays that run only inside a loop: `/search-knowledge`,
`/research-knowledge` and `/check-knowledge`. No person runs them, and each one hands its work to
the same agent, `knowledge-builder`.

**ADR 042 introduced a bug.** Under #920 we found what it caused:

- Each round runs three pre-flights, three loop-contract checks, three stop conditions and three
  closes, for one agent's job.
- Two of the plays write their done record under their old names. `/research-knowledge` writes
  `stop-condition-build-knowledge.yaml` and `/check-knowledge` writes
  `stop-condition-review-knowledge.yaml`. So the loop's done check cannot find them.
- The research skill, `author-knowledge-page`, calls the memory tool itself (`propose`). ADR 039 §2
  says no skill does that; a skill reads only what its agent puts in short-term memory.
- The loop's `round_state.py` reads memory-update files by their path. ADR 042 left this as
  follow-up work.
- The plays' memory search did again what the memory tool already does.

**The bug also left the memory that agents run from wrong.** This project holds no memory of its
own yet (ADR 038; the `initialize` play is not built), so its agents read Phoenix memory, the one
copy on each machine. What Phoenix memory says is what the agents decide from. Checked through the
memory tool on 2026-10-28 (Phoenix memory version 23387be24c0d):

- `standards/rules/pipeline-next.md` teaches the knowledge "member plays": line 21, and lines 76–79,
  "Loop members (run by a loop inside its rounds, never on their own)".
- `standards/rules/_index.md` says the loop "runs its knowledge plays" (line 56). It also lists
  `naming.md`, `naming.yaml`, `rename-map.yaml` and `loop-contract.md` (lines 13–15 and 56), which
  Phoenix memory does not hold.
- `standards/rules/pipeline-position.md` speaks of "member plays".
- `loop-contract.md`, `naming.md` and `rename-map.yaml` exist in Garura's source
  (`core/components/memory/standards/rules/`) but in no memory tier, so no agent can find them
  through the memory tool.
- Garura's own product model names the old plays in feature `fn-744`.

The product owner asked for the older records to be updated and ADR 042 retired, with the bug
called out (2026-10-28): "update the older ADRs, retire them too, and create new ones, calling out
that a bug was introduced. This bug means some part of memory is not right, the memory in .garura
which is used for agents to run." Asked to review the first draft, the product owner also asked
that what was found on the way be explained in full, and that the ADR template make every record
do so. Those points are in the next section.

## For the Person Who Accepts This

Each point below was found on the way, outside what this decision set out to do.

### Phoenix memory's page on where a play sits in the pipeline is older than Garura's, and teaches names that no longer exist

- **What and where:** the rule page `standards/rules/pipeline-position.md` in Phoenix memory (memory tool: tier phoenix, version 23387be24c0d, fingerprint `sha256:8d332a3c4b3c…`), against Garura's source copy `core/components/memory/standards/rules/pipeline-position.md` (last changed in this repository on 2026-10-24, commit bf570ece). The brief dates the Phoenix copy to 2026-10-20; the memory tool reports the tier's version, not a date for one page.
- **What is wrong, or worth knowing:** the Phoenix copy calls the play builder `play-creator` (lines 4, 5, 31, 34 and on; it is now `/create-play`). It names the review step of the end sequence `review-change` (lines 35, 50, 70, 71 and 118; it is now `/check-change`). It lists the plays by their old names (lines 11–14: `/vision`, `/understand`, `/measure`, `/grill`, `/learn`, `/refactor`, `/intent`, `/adr`, `/arch`, `/ux`, `/implement`, `/roadmap`, `/marketing`, `/run`, `/launch`, `/shape`, `/agentic`, `/quality`, `/validate`, `/deploy`, `/next`, `/focus`). It says "drive" and points to `drive-contract.md` (lines 15–17 and 120) and to `check_drive_contract.py` (line 19). The source copy has the new names throughout (`create-play`, `check-change`, `/discover-intent`, `/record-decision`, "loop", `loop-contract.md`, `check_loop_contract.py`). Separately, both copies use "members" (lines 47–56 in Phoenix) for the six change plays a play's position brings in: `start-change` and the four end plays. That is a different meaning from the knowledge "member plays" this decision removes.
- **Why it matters:** every agent in this project reads this page from Phoenix memory, because the project has no memory of its own. A play built from it gets an end sequence whose third step, `review-change`, no longer exists, so the built play cannot land its change. An agent that looks up a play by the names on this page finds nothing.
- **What this decision does:** promotes Garura's source copy to Phoenix memory (part 6), with its wording checked so that "member" reads only as the six change plays. It keeps that meaning of "members"; it retires only the knowledge member plays.
- **What you decide:** nothing beyond accepting this record.

### Phoenix memory holds the loop contract only under its old name, the drive contract

- **What and where:** the rule page `standards/rules/drive-contract.md` in Phoenix memory (memory tool: tier phoenix, version 23387be24c0d, fingerprint `sha256:32588ee0ef37…`). No tier holds `standards/rules/loop-contract.md` (memory tool: `find --every-tier`, no match). Garura's source has `core/components/memory/standards/rules/loop-contract.md`. The brief dates the Phoenix page to 2026-10-20.
- **What is wrong, or worth knowing:** `drive-contract.md` opens "# Drive Contract … A drive is a run of plays that keeps going until its goal is met" (lines 1–6). ADR 045 renamed the drive to the loop, and this page to the loop contract, in Garura's source; the rename did not reach Phoenix memory. The page still says `/build-memory` "builds the memory it lacks before it asks" (lines 124–125), the one play ADR 042 split into three.
- **Why it matters:** an agent that looks up the loop contract through the memory tool finds nothing, or, by a search for the contract's words, the old drive version, which teaches drives, `/build-memory` and old field names. The loop and the plays that run inside it depend on that contract.
- **What this decision does:** adds `loop-contract.md` to Phoenix memory by promotion (part 6), after its lines 131–132, which cite ADR 042's member plays, are corrected in the source.
- **What you decide:** whether `standards/rules/drive-contract.md` is deleted from Phoenix memory when `loop-contract.md` is promoted. Left there, a search can still find the old drive version.

### Phoenix memory's ADR template, which every decision record is drafted from, is older than Garura's

- **What and where:** the template `standards/templates/adr.md` in Phoenix memory (memory tool: tier phoenix, version 23387be24c0d, fingerprint `sha256:8be7c19d1725…`), against Garura's source copy `core/components/memory/standards/templates/adr.md`. The copy this run of `/record-decision` was handed (`.garura/project/issues/_adr/20261028T034030Z/context/templates/standards/templates/adr.md`) is the Phoenix copy.
- **What is wrong, or worth knowing:** the Phoenix copy names the play `/adr` and the skill `author-adr` (lines 12 and 52; now `/record-decision` and `author-decision`). It says "Inside a drive … at the drive's final review" (line 57). It offers the level `functionality` (lines 26, 69 and 122; now `feature`). Its example names `/intent`, `/vision`, "Kickoff" and `play-creator` (lines 154–156). It has no section for the person who accepts the record: that section and its rule are new in the source copy on this branch, made under this change.
- **Why it matters:** every ADR, in this project and in any project that reads Phoenix memory, is drafted from this template. Drafted from the old copy, a record names plays that are gone, can take a level the model no longer has, and has no place to tell the person who accepts it what was found on the way. This record itself was handed the old copy; its new section was taken from the source.
- **What this decision does:** adds the ADR template to the pages promoted to Phoenix memory (part 6). The source copy already has the new names and the new section (part 7).
- **What you decide:** nothing beyond accepting this record.

### Garura's source memory and Phoenix memory differ far beyond the pages this decision touches

- **What and where:** Garura's source memory (`core/components/memory/`) against Phoenix memory, as a whole.
- **What is wrong, or worth knowing:** counted on 2026-10-28: 49 pages differ between the two, 7 pages are in the source only, and 16 are in Phoenix memory only. These counts come from the comparison named in the next point, which read the files by their paths; they have not been counted again through the memory tool.
- **Why it matters:** each differing page is a place where the agents of this project may decide from an older rule than the one Garura is built with, the same way as the three points above.
- **What this decision does:** fixes only the pages it touches: `_index.md`, `pipeline-next.md`, `pipeline-position.md`, `loop-contract.md`, `naming.md`, `naming.yaml`, `rename-map.yaml` and the ADR template. The rest is #921 ("Phoenix memory stays up to date as Garura is built, and is versioned per release with its own release notes"), which serves business intent #899 ("A person works across Garura's repositories in one change: the source, Phoenix memory and the projects stay in step").
- **What you decide:** nothing here; #921 takes the rest. When #921 is worked, the counts should be taken again through the memory tool.

### The ADR keeper agent broke the memory rule while drafting this record

- **What and where:** the `adr-keeper` agent (`core/components/agents/adr-keeper.md`), in the first draft of this record on 2026-10-28, run by hand inside #920. The rule is `.claude/rules/garura-memory.md`.
- **What is wrong, or worth knowing:** the agent listed and compared files inside the `phoenix-memory` repository by their paths. The rule says: "You find it only through the memory tool, run from the project's root folder. Never read a memory file by its path." The agent then checked again, through the memory tool, every fact it used. In this round, the three Phoenix pages above were read through the tool (`read --tier phoenix`) and the missing pages looked up with `find --every-tier`, with the fingerprints given above. The counts in the point above are the one thing that still rests on the path comparison.
- **Why it matters:** the memory tool gives each answer its tier and its fingerprint, so a decision can cite what it rests on (`cite`) and a later check can say when that source changed (`citations --check`). A read by path skips that: nothing records which tier said what, and nothing flags it when the page changes.
- **What this decision does:** fixes the agent. `core/components/agents/adr-keeper.md` now says how to find and compare pages through the tool (`find --tier`, `--every-tier`, `read --tier`), treats Garura's source memory as repository files, and forbids reading, listing or comparing memory by its path in any tier (part 7).
- **What you decide:** nothing beyond accepting this record.

### ADR 041's status line says the connect step is a member play; ADR 043 itself says it is not

- **What and where:** the Status line of ADR 041 (`docs/adr/041-a-drive-runs-in-rounds-and-owns-its-questions.md`, line 3), and ADR 043 (`docs/adr/043-kickoff-plays-read-independently-and-the-drive-closes-the-loop.md`).
- **What is wrong, or worth knowing:** ADR 041's forward pointer for ADR 043 ends: "And §4 'Member plays' (as amended by ADR 042): the connect step is a member play too." ADR 043's own text runs the connect step as two skills, `find-model-gaps` and `close-model-gaps`, "skills, not plays" (line 65), and its ICE impact says "The two gap skills are new; no new play" (line 10).
- **Why it matters:** a reader of ADR 041 alone would think a loop has a second member play, and look for a play that does not exist.
- **What this decision does:** after it, no step of a loop is a member play (ADR 041 §4 is amended). An accepted ADR is not edited; the forward pointer this decision writes on ADR 041 says so.
- **What you decide:** nothing.

### A fourth standard is missing from Phoenix memory: the machine half of the naming rules

- **What and where:** `standards/rules/naming.yaml`: in Garura's source (`core/components/memory/standards/rules/naming.yaml`), in no memory tier (memory tool: `find --every-tier`, no match).
- **What is wrong, or worth knowing:** the brief names three standards the loop depends on that Phoenix memory lacks: `loop-contract.md`, `naming.md` and `rename-map.yaml`. `naming.yaml` is missing the same way. Phoenix memory's own `_index.md` lists it (line 14: "The machine half: the verb lists, industry terms, reserved built-in commands").
- **Why it matters:** an agent that follows the index to the verb lists finds nothing, so it cannot check a new name against the naming standard (ADR 046).
- **What this decision does:** adds `naming.yaml` to Phoenix memory with the other pages (part 6), after its lines 15, 23 and 24 drop the knowledge-play verbs.
- **What you decide:** nothing beyond accepting this record.

## Decision

### 1. The knowledge step is one step of the loop, run by one agent

When a round ends with open questions, the loop runs one step: "close the open questions". The
`knowledge-builder` agent runs it, through one contract. There are no plays in it.

- The loop's script `group_questions.py` merges the questions asked again.
- The agent answers from the loop's sources with the skill `find-answers-in-sources`.
- The agent looks in memory itself, through the memory tool (`search`, `find`, `read`, `cite`).
  No skill does this.
- For what research can answer, the skill `author-knowledge-page` drafts the page. The agent raises
  it with the memory tool's `propose`, for a person to approve (ADR 035).
- For what only the person can confirm, the skill `propose-answers` drafts our proposed answer, with
  its basis.
- The skill `author-knowledge-brief` writes the knowledge brief.

### 2. The three knowledge plays are removed

`/search-knowledge`, `/research-knowledge` and `/check-knowledge` stop being plays. Their folders,
stop conditions and stamped scripts go. A loop has no member plays: the "member plays" in
`loop_preflight.py`, both `lint_loop.py`, `pipeline-next.md` and the loop docs go. The change plays
a loop runs stay as they are.

### 3. One check, run by the loop

The three plays' checks become one loop script, `check_knowledge.py`, with the same checks. The loop
runs it after the agent and sends a failure back to the agent at most twice. The reply recorder,
`record_review.py`, becomes a loop script too.

### 4. What still holds from ADR 042

ADR 042 is retired, but these parts of it stay, now as part of this decision:

- **The person gets a brief, never a questionnaire.** The brief says what we understood, what we
  built and where the gaps are: at most seven gaps, each with its context and our proposed answer.
  It shows every point closed as settled, with why. It lists the knowledge pages waiting for
  approval, each with what it says, its sources and our recommendation. The person replies "yes" or
  corrects a gap, a settled point or a page by its id.
- **The loop shows the brief and records the reply.** The reply is recorded in the issue's
  short-term memory, `from: person`, keeping what each accepted proposal rested on. Each page
  decision is recorded through the memory tool's `decide` (ADR 041 §8). An approved page is not
  promoted; a person promotes it later.

### 5. Memory only through the memory tool

The agent is the only part of the step that looks in memory. No skill calls the memory tool. Two
scripts may ask the tool one read-only thing, its `updates` (the issue's waiting memory updates):
the loop's `check_knowledge.py`, and `round_state.py`, which stops reading memory-update files by
their path. The waiting updates are listed once by the agent and once by the check script.

### 6. The memory the agents read is corrected

The pages that teach the old shape are corrected in Garura's source,
`core/components/memory/standards/rules/`, and then promoted to Phoenix memory:

- corrected: `_index.md`, `pipeline-next.md`, `pipeline-position.md`, `loop-contract.md`,
  `naming.md`, `naming.yaml`, `rename-map.yaml`, and the ADR template
  (`core/components/memory/standards/templates/adr.md`);
- added to Phoenix memory, where they are missing today: `loop-contract.md`, `naming.md`,
  `naming.yaml`, `rename-map.yaml`;
- replaced in Phoenix memory by the source copy: `pipeline-position.md` and the ADR template.

Promotion is a person's deliberate act, outside the work (ADR 039 §1). This record names the pages;
it does not promote them.

### 7. A decision record tells the person who accepts it what was found on the way, in full

The product owner (2026-10-28): "I think we should also update the ADR template so that things
that I should know should be properly explained."

- The ADR template gains the section "For the Person Who Accepts This", right after Context, and
  the field `for_the_accepter`. Each point has its own heading and five parts: what it is and
  where; what is wrong, or worth knowing; why it matters; what this decision does; what the
  person decides. A point gives the detail itself (the lines, the names, the dates), never a
  summary.
- `author-decision` writes that section from the points the `adr-keeper` agent gathers.
- `adr-keeper` reaches memory only through the memory tool, never by a path, in any tier.
- The template is promoted to Phoenix memory with the other pages (part 6).

### What this changes in older ADRs

- **ADR 042** — superseded in full. What still holds is in parts 4 and 5.
- **ADR 041 §3** — the loop closes what it lacks with one step run by one agent, not member plays.
- **ADR 041 §4** — a loop has no member plays. So ADR 041's own change to ADR 029 §4 ("holds for
  work plays, not member plays") no longer exempts anything: ADR 029 §4 holds for every play a loop
  runs.
- **ADR 041 §5** — the person gets the knowledge brief (part 4).
- **ADR 039 §2 and §10's line on ADR 035 §4** — the read-only `updates` exception belongs to the
  loop's `check_knowledge.py` and `round_state.py`. The rest of §2 stands: no skill calls the tool.
- **ADR 044 §1** — the Shared Loop Run also owns the knowledge step. It is a run step, not a product
  rule.
- **ADR 046 §4** — the clause "knowledge plays `search`, `research`, `check`" goes.

### What this does not change

Nothing from research is used before a person approves it (ADR 035). A question one play cannot
answer is still the loop's (ADR 041 §2). The loop still reads no memory itself; it records the
person's decisions through `decide` (ADR 041 §8). The connect step's two skills (ADR 043) stand.

## Consequences

### Positive

- One agent dispatch per round for the step, one check, and one place a failure points to.
- The done-record mismatch goes, because its cause goes.
- Every memory call is the agent's, or a named read-only script's. No skill calls the tool.
- Once the pages are promoted, agents that read Phoenix memory learn the real shape, and can find
  the loop contract and the naming rules.
- The person who accepts a record sees each thing found on the way in full, in one place, with
  what they decide.

### Negative / Risks

- Until the corrected pages are promoted, agents in this project still read the old shape from
  Phoenix memory, and still cannot find `loop-contract.md`, `naming.md`, `naming.yaml` or
  `rename-map.yaml`.
- Two scripts now call the memory tool's `updates`, where ADR 042 allowed one. The exception must
  stay read-only.
- One step does more. Its one check, `check_knowledge.py`, must catch what three plays' checks
  caught.
- A project installed before this change keeps the three plays until its next install retires
  them.
- `propose-answers` says it drafts from memory, but in this flow it is handed no memory. The design
  names this (`redesign.md`); it is not fixed here.
- Until the ADR template is promoted, `/record-decision` hands its agents the old Phoenix copy,
  which has no section for the person who accepts a record.

## Alternatives Considered

- **Keep the three plays and fix the done-record names** — lost: no person runs them, and the
  ceremony of three pre-flights, stop conditions and closes per round stays.
- **Three skills, each called by its own agent dispatch** — lost: three dispatches for one agent's
  job.

## Work This Creates

- Change the Discovery loop's C5 and its step through `/edit-loop complete-discovery` (an intent
  change).
- Direct edits: `loop-run.md` R5b and R5c, `/create-loop`'s references and example loop,
  `knowledge-builder`, `author-knowledge-page`, and the skills that name the plays.
- Remove the three play folders; update `loop_preflight.py`, both `lint_loop.py`, the tests and
  the installer's lists.
- Correct the memory pages in `core/components/memory/standards/` and promote them to Phoenix
  memory (part 6), the ADR template with them. Whether Phoenix memory's
  `standards/rules/drive-contract.md` is deleted is the person's call (see "For the Person Who
  Accepts This").
- The rest of the gap between Garura's source memory and Phoenix memory: #921.
- Update the glossary, `docs/components/` and feature `fn-744`'s page.
- After acceptance, `/record-decision` writes the forward pointers on ADR 042 (superseded) and on
  ADR 041, ADR 039, ADR 044 and ADR 046 (amended in part).

## References

- Brief: `.garura/project/issues/_adr/20261028T034030Z/brief.md`
- Design: `.garura/project/issues/920/specs/redesign.md`
- ADR 042 — `docs/adr/042-a-drive-finds-builds-and-reviews-the-knowledge-it-lacks.md`
- ADR 041 — `docs/adr/041-a-drive-runs-in-rounds-and-owns-its-questions.md`
- ADR 039 — `docs/adr/039-memory-writes-go-to-short-term-memory-plays-read-no-memory.md`
- ADR 044 — `docs/adr/044-the-shared-drive-run-owns-the-steps-between-plays.md`
- ADR 046 — `docs/adr/046-one-naming-standard-for-every-harness-part.md`
- `core/components/loops/_shared/loop-run.md` — the Shared Loop Run
- `core/components/memory/standards/templates/adr.md` — the ADR template, with the section for the person who accepts a record
- `.claude/rules/garura-memory.md` — the memory rule
- #921 — Phoenix memory stays up to date as Garura is built
