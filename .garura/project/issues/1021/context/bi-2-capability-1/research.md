# Design the technology and architecture: research and drafts (issue 1021, BI-2 capability 1)

Draft only. Nothing under `.garura/product/`, on GitHub or in git changed. The drafts are under `.garura/project/issues/1021/context/bi-2-capability-1/drafts/product-os/software-delivery-planning/design-technology-architecture/`: the capability page and its ICE page, and three feature pages, each with its ICE page.

What this run did besides reading:
- It ran the placement skill (find-work-placement) over the ten domain shelves of memory. No shelf covers this work; the result is `placement/routing-result.json` (unmatched).
- It checked each draft page with the structure check and checked every quote in a Sources section against its file. The record is `lint.json`.
- The pages were written by hand in short-term memory, as the brief asked. No skill drafts pages of the approved BI-1 shape into short-term memory: the capability skill writes only to the live model, and in the older page shape with the ICE inline.

## What is built, and what is only planned

In one line: nothing in the current flow sets a technology or architecture position for the whole project. A position is one choice that holds for the whole project, written down with its reasons. What exists is older, stale or a piece another capability owns.

Built, but not for the whole project, or not reachable:
- **The architecture design play, stale, one slice at a time.** `core/components/plays/shape-architecture-lens/` writes one slice's architecture lens: the parts the slice passes through, its technology with versions, and how it runs end to end. It is marked stale ("waits for the rebuild of the design plays after the shaping loop (#855, ADR 053)"), so no install lays it. It does not set project-wide positions, but it leans on them: "The stack is a material choice recorded as a slice-level decision the whole product references; it is sized by the profile box, not invented per slice", and its recovery says "reuse the product decision if one exists". As built, the first slice decides the technology of the whole project. Its choices must rest on memory, "never the model's taste". The other design plays (`shape-ux-lens`, `shape-quality-lens`, `shape-agentic-lens`, `shape-run-lens`, and the dropped marketing and measure ones) are stale too, and each designs one slice.
- **An older skill that writes a project-wide architecture.** `core/components/skills/author-technical-approach/` writes `architecture.yaml` for the product (output "e.g., `.garura/product/architecture/`"): principles, the layout of deployable units, quality targets, a technology stack that names each product and version with a reason, platforms, outside services, risks, deployment, observability and an agent design. It never overwrites a LOCKED file ("drop to DRAFT first"). The tech-designer agent lists it, but no play calls it, and its inputs (`features.yaml`, `product.yaml`, `roadmap.yaml`) came from the retired planning chain, deleted by ADR 050. It cannot run in the current flow.
- **A deleted project-wide architecture chain.** ADR 050 deleted "the `derive-*` skills for capability selection, design patterns, logical architecture, NFR spec, physical architecture, quality vision, systems inventory and tech stack". Its rule file is gone from the source but still in Phoenix memory (`standards/rules/architecture.md`, "Canonical rules governing the six /arch artifacts").
- **What agents read today.** The tech-designer agent treats a locked project file as the answer ("if LOCKED, use as authoritative"). Every ICE's Read line sends an agent to "the project's existing memory and its existing implementation" first. So today an agent takes the technology from the project's code; a new project gets whatever its first builder picks.

Built, and owned elsewhere, that this capability would stand on:
- **Memory to propose from.** Phoenix memory's knowledge base has an `architecture/` shelf ("product-condition → best-fit architecture ladders") and a `technology/` shelf ("specific technology/stack choices and the conditions they fit"). Each learning lists its conditions and what comes after it (`evolve_when`), for example the modular monolith, "the default start", gives way to microservices, "earned, not started with".
- **Decision records that can be replaced.** `/record-decision` writes "a product decision, a `decision.yaml` record" beside its node; "Only a person accepts an ADR"; and "accepted decisions are not edited — supersede or amend with a new record". Manage ADRs owns this.
- **The product profile.** Its shape (stage, users, monetization, surfaces) and its quality box (a level and a gate for speed, security, accessibility, scalability, reliability, privacy, observability and ease of change), plus compliance. /discover-domains sketches it and /discover-capabilities firms it. Specify the product owns it.

Only planned:
- ADR 028 §2 item 3: "Design the project, one area at a time, once per project: UX, tech architecture, agentic, quality, run" (marketing was dropped by ADR 066). "These set the project's guidelines, rules, and guardrails. Every slice follows them." "Each design area is skippable." Its Open question 3, "Where do the project-wide design outputs live in the product model?", was deferred to the ontology, and ontology v15 has no kind for it.
- ADR 014 (older): "architecture is product-scoped, not epic-scoped". GitHub #426 (closed) said the same.
- The names agreed on 2026-11-03: "/design-architecture (was /shape-architecture-lens)", under Designer. The name does not say whether it designs a project or a slice.
- GitHub #608 (open, a question): "How a skipped design area is recorded, so a later loop knows it was skipped and not forgotten."
- Initialize (not built; in the model as `cap-initialize`): its setup questions cover "the technology standards, the tools and frameworks", to choose the memory blocks the project gets, for example "Java or .NET, a React front end or none".
- BI-2: "Each position is written down and can change later."

Not this capability: GitHub #933 and #967 (open) are about an architecture memory for teams that build a harness on the Phoenix architecture, which is Garura's own architecture, under Standards and Build your own harness. They are not a product's technology positions.

## The overlaps, and how the line could be drawn

### With "Use the lenses on each slice" (BI-3, Design → Code)

The design plays, the architecture one included, are per slice. The question is whether a project-wide design step lives here and the per-slice lens there, or the architecture play moves here.

1. **Split by reach.** This capability sets the positions once for the project. Each slice's architecture lens, under BI-3, picks which parts the slice passes through and what crosses each seam, using the technology set here, and never picks its own. When a slice needs something no position covers, it names the gap, and a person sets a position here. The stale play is rebuilt as the per-slice lens and reads the positions. The cost: one more step before slices, and the per-slice lens loses its own technology choice.
2. **The architecture play moves here.** `/design-architecture` is rebuilt to run once for the project, as ADR 028 says ("once per project"), and BI-3 keeps only reading the positions for each slice. The cost: BI-3 loses its architecture lens, and the per-slice parts (which parts a slice passes through, its seams, its end-to-end build) need a home, perhaps under "Bring the design together for a vertical slice".
3. **Positions grow out of slices.** Keep the stale play's way: the first slice's choice becomes the project's decision, later slices reuse it, and this capability only names and changes those decisions. The cost: the first slice decides for the whole project, against BI-2 ("set for the whole project"), ADR 028 and ADR 014.

My lean is option 1. It keeps one job in each place: the whole project here, one slice there. It follows ADR 028's "once per project ... Every slice follows them", and the stale play already expects "the product decision" to exist. The drafts follow option 1.

### With "Manage ADRs" (Orchestration)

A position is a decision on how the project is built, and Manage ADRs' agreed line is "Decisions on how the project is built are recorded closely as they're made".

1. **This capability decides; Manage ADRs records.** Each position is written as a product decision record through Manage ADRs: a person accepts it, and a change is a new record that replaces it. This capability owns what the position says, how it is proposed and from which source. The cost: the positions in force are read from a set of records, not from one page, and the record shape must suit a project-wide choice (its `node_ref` and `level`).
2. **A positions record here, and a decision for each change.** This capability keeps one current record of all positions; each change also gets a decision record through Manage ADRs that says why. The cost: two records for one thing, which can disagree.
3. **Everything here.** This capability writes and replaces its own position records; Manage ADRs keeps Garura's own decisions and the ones no other capability owns. The cost: two writers of decision records, with two sets of checks.

My lean is option 1: one writer of decision records, and the record shape already does what the BI-2 proof asks (written down, replaced and never edited, accepted by a person). The drafts put the decision record Out, to Manage ADRs, and still say "Not decided: where the positions are kept, and whether each is a decision record", because the ontology has no kind for either. Under option 2 or 3, the capability's Out line on decision records changes.

### With "Seed the memory for the lenses" (part of initialize)

Initialize's setup questions (not built) ask about "the technology standards, the tools and frameworks", and the answers choose the memory the project gets. That answer is a technology position in all but name.

1. **Set here, read there.** This capability owns the technology positions. Initialize proposes its technology answers from the positions when they exist, and seeding brings the memory that matches them. When initialize runs first, right after the install and before any position, its confirmed technology answer is written as the first position here. The cost: initialize's setup-questions page changes in a few lines (it is not built, so only words change).
2. **Initialize sets the first technology positions.** Its answers, kept in the product profile, are the project's first positions; this capability adds the architecture and owns every later change. The cost: the technology lives in two places (the profile and the positions), or the profile, which Specify the product owns, grows a technology part.
3. **All technology questions move here.** Initialize stops asking about technology, and seeding only reads the positions. The cost: initialize cannot choose memory blocks on a fresh project until this capability has run.

My lean is option 1: one record for each technology choice, and initialize stays where the agreed list puts it. The drafts put seeding Out and say it reads the positions.

### With the product profile, which Specify the product fills

Specify the product's approved page has "In: setting each capability's quality and compliance needs, and rolling them up into the product profile." The profile says what the product must be; positions say what it is built with and in what shape.

1. **Read, never write.** This capability reads the profile to size each position and never writes it. A position that would need a quality level moved goes back through Specify's roll-up and a decision ("The box moves ONLY by an approved decision."). The cost: none on the approved pages; the sizing rule must be built.
2. **The profile gains a technology part.** One record holds the shape, the quality box and the technology. The cost: two writers of one record, a schema change, and the profile's meaning ("THE BOX — the product's committed boundaries") widens.
3. **Firming the quality box moves here.** Quality levels are what an architecture must meet, so this capability firms them, and Specify only sets each capability's needs. The cost: reopens Specify's approved In line and its roll-up.

My lean is option 1. The drafts follow it: the profile is Out and an input.

### The siblings under BI-2

No decision needed, but the drafts draw these lines:
- The profile's `surfaces` list belongs to Manage surfaces; this capability does not set surfaces.
- The platform the product runs on and its environments go to Deployment design and Environment setup. The older skill had deployment in the same file as the stack, and memory has hosting learnings on its technology shelf (for example a GCP runtime for a modular monolith), so this line may need a second look when Deployment design is drafted.
- Locking belongs to Lock the design. The older skill had a lock ("drop to DRAFT first"); the drafts leave how a position changes after the lock as not decided.

## The domain

Every BI-1 part sits in software delivery planning. Its page says "This domain turns a business intent into work that agents can build" and "Its job comes before the build". The placement run found no shelf for this work (`placement/routing-result.json`).

1. **Software delivery planning, widened by one line.** The capability sits with the BI-1 parts. Setting positions comes before the build, and Garura's own lifecycle puts "design the project once" in the same stage as cutting slices (`docs/philosophy/idsd.md`, Shape). The domain already holds initialize, which is not "intent into work" either. The cost: the domain's first line does not cover positions, so it needs a named-lines change to add them.
2. **A new domain for the design stage.** All six Spec → Design capabilities sit in one new domain, named as the field names it, with outside sources, through the nothing-fits path (propose-kb-node). The cost: a new domain page and its research; and the placement rule says a domain is a field an industry names itself by, never a practice, a test that "software architecture" or "software design" may fail as much as the current domain does.
3. **No domain yet.** The capability waits in the holding folder until BI-2's other capabilities are drafted, and then one domain is chosen for all six. The ontology allows a missing domain as a gap. The cost: the capability is not ready until it is attributed, and the question only moves.

My lean is option 1, with the domain's first line widened later. The drafts sit under `software-delivery-planning/`. Under option 2 or 3, only the folder and the one domain line in the capability page change.

## Features found

Three features, none built. Each ICE is thin.

- **Set the project's technology** (fn-set-technology). Not built. Sets what the whole project is built with (languages, frameworks, data stores, outside platforms, each with its version), proposed from the project's code or memory and confirmed by a person. Sources: the agreed one line; ADR 028 §2 item 3; ADR 014; `author-technical-approach` (its stack section, no caller); the stale architecture play's stack decision "the whole product references"; initialize's technology questions; memory's technology shelf.
- **Set the project's architecture** (fn-set-architecture). Not built. Sets the shape of the whole system: its style, its main parts with one job each, and the seams between them. Sources: the agreed one line; ADR 028 §2 item 3; ADR 014 and #426; `author-technical-approach` (its topology and deployable units); the deleted logical and physical architecture skills (ADR 050); the architecture lens schema in Phoenix memory (parts by layer: experience, process, domain, cross-cutting); memory's architecture shelf.
- **Change a position as the project evolves** (fn-change-position). Not built. Replaces a position the project has outgrown, keeping the old one, marked replaced, with why. Sources: the agreed one line ("can evolve"); BI-2's proof ("can change later"); the decision schema's replace-never-edit rule and `/record-decision`; the stale play's "accepted decisions are superseded, never edited in place"; memory's `evolve_when` on each learning.

Candidates not drafted:
- **Check built work against the positions.** No list or page records it as planned. The deleted chain had a validator for its own files, and #967 is about a harness's own architecture. Named here only.
- **Project-wide agent design and quality positions.** ADR 028 lists agentic and quality as project-wide design areas, and the older skill had an agent design section. The agreed BI-2 list names only technology and architecture, surfaces, deployment and environments. Left out; an open point below.
- **Technical risks for the whole project.** The older skill had a risks section. No agreed list names it.
- **Record a skipped position.** #608 asks how a skipped design area is recorded. It is a question in a spike, not a planned feature, so the drafts carry it as a rule of the capability ("the gap stays on record"), not a feature.

## Gaps that matter

- **Nothing sets a project-wide position today.** Agents take the technology from the code, so a new project's first builder decides for every later one. This is what BI-2's "Without shared positions, each builder invents its own answer" warns of.
- **As built, the first slice decides the whole project's stack.** The stale architecture play records the stack as "a slice-level decision the whole product references" and reuses it.
- **The model has no place for a position.** ADR 028 deferred it to the ontology; ontology v15 defines no such kind and lists none as not yet defined. Until this is settled, the pages say "Not decided".
- **Old parts can be read as current.** The older skill still sits in the source and in tech-designer's skill list; `core/config.yaml` still names a product folder `architecture/` ("build-architecture output") that no current part writes; and Phoenix memory still holds the rule file of the deleted architecture chain. An agent can find each and take it as today's way.
- **Changing a position after the lock is not settled.** The capability says positions evolve; Lock the design says a design is locked before agents take over. How the two meet is for Lock the design to settle when it is built.

## Open points for the product owner

- The line with "Use the lenses on each slice": option 1, 2 or 3. The drafts follow option 1.
- The line with "Manage ADRs": option 1, 2 or 3. The drafts follow option 1.
- The line with "Seed the memory for the lenses": option 1, 2 or 3. The drafts follow option 1.
- The line with the product profile: option 1, 2 or 3. The drafts follow option 1.
- The domain: option 1, 2 or 3. The drafts follow option 1.
- Whether project-wide agent design and quality positions belong here, elsewhere under BI-2, or only in the per-slice lenses.
- The persona. The drafts name "the architect", from the stale play's scenarios ("(architect, first run)"); no model page names this persona yet. The product owner may prefer "the product owner".
- The capability's own ICE carries no thin mark, as the brief says only an unbuilt feature's does. Nothing of the capability is built, so the product owner may want it thin too.
- Whether a position is one record per choice or one page of all positions in force. This follows from the Manage ADRs line.

## Details left out of the pages

The pages hold what each part does, its main rules with their reasons, the gaps that matter and the checks that prove it. Left out, for an agent that builds these parts to find in the code and memory:
- The fields of the older `architecture.yaml` and of the decision record (`node_ref`, `level`, `supersedes`, `superseded_by`).
- The condition keys of each memory learning (stage, team size, scale, deploy cadence) and how a learning is matched.
- The layer names of the architecture lens and the contract fields of each seam.
- How the stale play guards its writes, its gate and its checks.

## Structure check

`python3 .claude/skills/discover-capabilities/scripts/lint_grounding.py` on each page: `--kind capability --stage directional` for the capability and `--kind feature` for each feature. All four pages read ok, with no error and no warning, on the first run; nothing had to be fixed. The record is `.garura/project/issues/1021/context/bi-2-capability-1/lint.json`.

The structure check has no kind for an ICE page, so a small check in the same record tested each of the four ICE pages: the three sections in order, exactly one Goal, at least one Limit, Fails if and Done means, the fixed Read line first, the Context labels in order (Read, Never read, Persona, Scope), a Done means checked by someone other than the doer, and the thin mark on the three features and not on the capability. All four read ok. No ICE page has a Never read line: nothing found says what these parts must not read.

Every quote in a Sources section was checked against its file, word for word: 108 quotes, none missing. Two Sources lines carry no quote: the short line beside each feature, and the shelf line.

## What this run read from memory

Through the memory tool, from Phoenix memory, copied to `.garura/project/issues/1021/context/bi-2-capability-1/memory/` with `manifest.json`: the ontology, the ICE rubric, the capability, feature and content-standard grounding templates, the product profile and decision schemas, the ADR template, the architecture lens schema and its index, the old architecture and design rules, the knowledge base index, the ten domain shelves, three architecture learnings and one technology learning. No tier was missing. Three decisions and their traces are in `cite-request.json`, for the caller to record; this run writes nothing outside `bi-2-capability-1/`.
