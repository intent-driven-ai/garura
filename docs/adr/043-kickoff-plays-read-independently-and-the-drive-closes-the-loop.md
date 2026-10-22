# ADR 043 — The Kickoff Drive's Plays Read the Prototype on Their Own, Any Node Is Written Without Its Parent, and the Drive Connects the Nodes and Closes the Loop

**Status:** Accepted — amended in part by [ADR 047](047-the-ice-is-its-own-node.md): §1 (an ICE has exactly one part), §2 (the ICE is written as its own node), §3 (the ready rule) — the ICE parts only
**Date:** 2026-10-21
**Level:** framework
**Decided by:** Kapil Viren Ahuja 
**Decided in:** #689 — the session of 20–21 October 2026, after Kickoff run 7 on the Argus mockup and the single-play tests of /intent and /vision
**Amends:** ADR 029 — §6 "The first drive: Kickoff": the fixed order `/intent` → `/vision` → `/understand` and its table (`/vision` no longer takes `/intent`'s output as its goal; `/understand` no longer runs once for each capability `/vision` seeded), and "The prototype is the input": the input is the prototype plus a short write-up · ADR 031 — §3 "ICE is placed at once; the domain comes later": a functionality may also be written before its capability; and §2's "Drift is found and fixed by an Alignment drive": inside a drive, the drive's gap skills connect what its plays wrote · ADR 033 — §4 "Approval follows links": a node is not approved and not workable until it is attributed · ADR 041 — §1 "A drive runs its plays in rounds until its job is done": no fixed order, the two gap skills after each round, the next round on the work they give out · ADR 026 — Decision, "Clean tree in, committed delta out": inside a drive, plays may run side by side and the drive commits the round once
**Affects:** `core/components/memory/standards/schemas/product-os/spine.yaml` (functionality `capability` field, tree rules, on-disk layout, fill rules), `core/components/memory/standards/schemas/product-os/ontology.md`, every `lint_grounding.py` copy (12, under `core/components/plays/*/scripts/`), `core/components/plays/intent/scripts/check_ice_workable.py`, `core/components/plays/play-creator/references/check_ice_workable.py`, `core/components/drives/_shared/drive-run.md` (R3, R5), `core/components/drives/kickoff/` (`reference/ice.md` C2–C5, F4, Plays, Done means; `scripts/round_state.py`, `write_drive_contract.py`, `commit_run_files.py`), `core/components/memory/standards/rules/drive-contract.md` (rules 3 and 5, "One contract for the whole drive", the `plays` field), `core/components/plays/drive-creator/` (references, `scripts/lint_drive.py`), `core/components/plays/drive-editor/scripts/lint_drive.py`, `core/components/plays/intent/`, `core/components/plays/vision/`, `core/components/plays/understand/`, `core/components/skills/author-business-intent/`, `core/components/skills/author-vision-seed/`, `core/components/skills/enrich-capability-ice/`, `core/components/agents/prototype-reader.md`, `core/grounding/glossary.md` (Drive entry)
**ICE impact:** Agent intents change for `/intent`, `/vision`, `/understand`, the Kickoff drive and the `prototype-reader` agent. `/intent` drafts the business intents from the shared capture and the write-up, and writes nothing else. `/vision` writes domains from the screens and research, and nothing else. `/understand` writes capabilities and functionalities, each with its ICE, from the screens. The Kickoff drive takes the write-up, runs its plays in no fixed order, runs the two gap skills after each round, gives the missing work to the play that does it, and loops until every node is connected and covered, or until its round limit. The two gap skills are new; no new play. The `prototype-reader` plans its walk from the walkthrough. The ICE workable check also needs attribution. The ICE kind keeps its shape.
**Business intent check:** none — a framework decision on how the model is written and how a drive runs; no person's business intent changes, and the Business Intent kind's rules stand (only a person confirms or drops one, ADR 031)
**Related:** ADR 026, ADR 029, ADR 031, ADR 032, ADR 033, ADR 041, ADR 042, #689, #613, #612

## Context

Kickoff run 7 (20 October 2026, on the Argus mockup) ran its plays in a chain. `/intent` wrote intents framed around the drive. `/vision` took them as its goal and invented a domain ("Drive review"). `/understand` then detailed the wrong capabilities and made a screen panel into a functionality. One error at the top spread to every node below it.

The earlier fixes under #689 made each play read the screens itself. The chain is what is left. Two rules hold it in place. The spine says a functionality must name a capability (REQUIRED), so `/understand` cannot write before `/vision`. And the drive runs its plays in a fixed order (ADR 029 §6, ADR 041 §1).

The plays also run on their own, outside a drive. Kapil (21 October): "I run vision, which identifies the domain, but it won't have functionality and capabilities available. Somebody will have to go back and run it manually. The whole point of a drive is that these loops are closed … It's not just connecting the three. It's really connecting the three meaningfully so that the work gets done."

The doctrine "anyone writes; align later" (Kapil, 8 October, #612; ADR 031 §2) already says no play owns a kind. The spine schema and the drive's fixed order still contradict it. Kapil (21 October): "It's not a tree structure. They are independent functions, and the drive's job is to find and connect everything later on … everybody can write anything, but it is not approved, not ready, until there is an attribution."

A prototype alone is also not enough. `/vision` had to guess the product's field: it found Human Oversight and missed SDLC / Developer Experience and Requirements management. Kapil: "prototype isn't enough … a small write up … that explains the prototype … this will guide the drive and internally plays very well."

The keeper found one more ADR this decision touches: ADR 026's "Clean tree in, committed delta out". The brief does not name it. The person who accepts should check it.

## Decision

### 1. Every kind is written on its own

A business intent, an ICE, a domain, a capability and a functionality are independent nodes. No parent is required. A capability may have no domain yet. A functionality may have no capability yet: it waits in a holding folder, `functionalities/<id>/`, as capabilities do today. The spine's rule "a functionality names a capability — REQUIRED" changes to match. The nested folder layout is no longer the only home of a node.

### 2. Each Kickoff play writes one kind, and nothing else

- `/intent` writes business intents only. It no longer writes a proposed capability for each ICE.
- `/vision` writes domains only. It no longer writes or places capabilities.
- `/understand` writes capabilities and functionalities, each with its ICE.

Each play reads the screens for its own kind. No play writes another play's kind, so two plays never write the same thing twice. (This narrows ADR 031 §2's "anyone writes" for these three plays: the kinds stay independent, and each has one writer.)

### 3. A node is ready only once it is attributed

A node is not approved and not workable until it is linked: functionality → capability → domain, and its ICE → a confirmed business intent. Unlinked nodes are kept. They are shown as not ready. No agent works on them.

### 4. The drive closes the loop

A play run on its own writes only its own kind. Run alone, `/vision` finds the domain, but no capability or functionality exists until someone runs `/understand` by hand. Everything not yet linked stays visible as not ready.

Inside a drive, the drive does that work. After each round it has the model checked by two skills, invoked through the `product-os-keeper` agent (the drive holds no judgment of its own, ADR 029). `find-model-gaps` reads every node and reports what is not connected, what is a duplicate, and what is missing. `close-model-gaps` then does what can be done in the model itself, and hands the rest back to the drive:

- It **connects**. It attributes each functionality to its capability and each capability to its domain. It links them to the intents they serve. It merges two nodes that are the same thing.
- It **finds the work that is still missing and gives it to the play that does it.** A capability with no functionalities goes to `/understand`. A screen that no node covers goes to the play that writes that kind. An intent that no capability serves goes to `/understand`. A capability no domain holds goes to `/vision`. A screen whose need no intent names goes to `/intent`.

The next round runs those plays on exactly that work. The drive goes on until every node is connected and nothing on the screens is left uncovered. If it reaches its round limit first, it briefs the person (ADR 042). This meaningful connection, so that the work gets done, is the value a drive adds over running the plays by hand.

### 5. The plays read the prototype independently

The `prototype-reader` agent reads the prototype once. Its capture (views, words, journeys) is shared. `/intent` drafts the business intents from it. `/vision` drafts the domains, by research. `/understand` drafts the capabilities and functionalities. Each reads the screens; none reads another play's output. So their readings are independent, and their agreement is the check.

No play waits for another. They may run side by side. Writes to the one shared spine file are made in turn. Inside a drive, the drive commits the round once. The first build runs the plays in turn; side by side comes once the scoped-write guard can tell two plays' writes apart.

### 6. Two skills, used by the shared drive run

`find-model-gaps` and `close-model-gaps` are skills, not plays, so later plays can use them too (for example plays that show the model's state, find its gaps, or fix them with the person — not designed here). The shared drive run (`drive-run.md`) calls them after each round, for every drive whose plays write the product model. Today that is Kickoff.

### 7. The prototype comes with a short write-up

Kickoff takes, beside the prototype, a few lines from the person in five parts:

1. what the product is;
2. who uses it;
3. the field it serves and the job it does there;
4. what on the screens is only sample data;
5. a walkthrough of the steps a person takes.

Without the write-up, the drive asks for it first, in its questions-first step. Every play reads it as a Source. The `prototype-reader` plans its walk from the walkthrough. The intents and the model still come from the screens; the write-up guides the reading.

### 8. Running the drive, or running the plays by hand, is the person's choice

Run by hand, each play writes only its own kind, and the person runs the next play when they want the rest. Run as a drive, the person gets everything — intents, domains, capabilities and functionalities, connected — and reviews it all at the end. Neither path is a fault: the plays stay usable on their own, and the drive is how the loop closes without the person.

### What this changes in older ADRs

- **ADR 029 §6** — Kickoff no longer runs `/intent` → `/vision` → `/understand` in order. `/vision` does not take `/intent`'s output as its goal. `/understand` does not wait for `/vision`'s capabilities. The input is the prototype and the write-up.
- **ADR 031 §3** — widened: a functionality may be written before its capability, as a capability may be written before its domain. **§2** — inside a drive, the gap skills connect what the plays wrote; and "anyone writes" narrows for `/intent`, `/vision` and `/understand`: each writes one kind. This ADR does not decide whether the Alignment drive is still needed for drift outside a drive.
- **ADR 033 §4** — widened: workable now also needs attribution (functionality → capability → domain). This also widens ADR 031 §4 as ADR 033 already amended it.
- **ADR 041 §1** — a round runs the plays in no fixed order, then the two gap skills. The next round runs only the plays given work. Done means every node is connected and nothing on the screens is uncovered.
- **ADR 026** — "Clean tree in, committed delta out": inside a drive, the plays do not each commit before the next starts; the drive commits the round once.

### What this does not change

- ADR 029 §2 (questions first) — kept; the write-up is asked for there. §3 and §4 — kept; this decision makes §4 stronger.
- The Business Intent kind's rules (ADR 031): only a person confirms or drops a business intent, and work starts only from an ICE built from a confirmed intent.
- The memory rules (ADRs 034, 035, 036, 039). The write-up is a Source the person gives, not memory.

## Consequences

### Positive

- An error in one play no longer flows into the others. Each play reads the screens, so a wrong intent cannot invent a domain or wrong capabilities below it.
- The three readings are independent, so where they agree the model is more likely right, and where they differ `find-model-gaps` reports it.
- Any play can write what it finds at once. `/understand` does not wait for `/vision`.
- Inside a drive, the loop closes without a person: missing work goes to the play that does it.
- Run on its own, a play leaves its gaps in plain view as not-ready nodes.
- The write-up states the product's field, so plays do not guess it.

### Negative / Risks

- The model can hold many unlinked nodes for a time. Readers and tools must show "not ready" clearly, or people will take a loose node for an approved one.
- `close-model-gaps` must merge duplicates correctly. A wrong merge joins two different things; a missed merge leaves two copies.
- Side-by-side plays share one working tree. ADR 026's scoped-diff guard reads the git diff over the whole model and cannot tell two plays' writes apart. "Writes to the spine made in turn" covers the spine file, not the guard.
- Many files change: the spine, the ontology, 12 linter copies, two workable checks, the shared drive run, the drive contract, the drive compiler and editor, three plays, the Kickoff drive and one agent.
- The person must write the write-up. Without it, the drive stops at its first step to ask.

## Alternatives Considered

- **Keep the chain (`/intent` → `/vision` → `/understand`), each reading the screens** — an early error still flows down, and `/understand` still cannot write a functionality before `/vision` writes its capability.
- **Run the three plays fully at once, with nothing that connects their output** — two plays write the same thing twice, nothing links the nodes, and the model never comes together.
- **Read side by side into drafts only, then save from an agreed draft** — lost for now. It needs a draft-only mode in every play. Independent nodes plus the gap skills give the same check with less change. Running the plays side by side stays allowed (part 4).
- **No write-up; infer the field from the screens** — `/vision` had to guess the field and got it wrong (it found Human Oversight and missed SDLC / Developer Experience and Requirements management). The person states it in a few lines.

## Work This Creates

- Build the two skills, `find-model-gaps` and `close-model-gaps`, with a check script each, and call them from `drive-run.md` after each round.
- Later, its own story: plays that show the model's state, find its gaps and fix them with the person (with Argus); they can reuse the two skills.
- Define the write-up's five-part shape.
- Spine and ontology: an optional `capability` on a functionality, the holding folder `functionalities/<id>/`, readiness by attribution.
- Every `lint_grounding.py` copy: a functionality with no capability is a warning, not an error; a named capability that does not exist stays an error. Both `check_ice_workable.py` copies: workable also needs attribution.
- The Kickoff drive's ICE (C2–C5, F4, Plays, Done means) through `/drive-editor`; `drive-run.md` R3 and R5; `round_state.py`, `write_drive_contract.py`, `commit_run_files.py`; `drive-contract.md` rules 3 and 5; `/drive-creator` and `/drive-editor` lint.
- `/intent`, `/vision` and `/understand` ICE through `/play-editor`; the `prototype-reader` agent.
- The glossary's Drive entry.
- Run Kickoff again on the Argus mockup, with a write-up.

## References

- Brief: `.garura/project/issues/689/context/adr/20261021-015459/brief.md`
- `core/components/memory/standards/schemas/product-os/spine.yaml`
- `core/components/drives/kickoff/reference/ice.md`
- `core/components/drives/_shared/drive-run.md`
- `core/components/memory/standards/rules/drive-contract.md`
- ADR 029, ADR 031, ADR 033, ADR 041, ADR 042, ADR 026
