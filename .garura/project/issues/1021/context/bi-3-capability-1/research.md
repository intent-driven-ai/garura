# Design slices: research and drafts (issue 1021, BI-3 capability 1)

Draft only. Nothing under `.garura/product/`, on GitHub or in git changed. The drafts are under `.garura/project/issues/1021/context/bi-3-capability-1/drafts/product-os/software-delivery-planning/design-slices/`: the capability page and its ICE page, and two feature pages, each with its ICE page. The capability is built, so no ICE page carries the thin mark.

What this run did besides reading:
- It copied what it read from memory through the memory tool into `bi-3-capability-1/memory/`, with `manifest.json`.
- It ran no placement: the domain (software delivery planning) was decided by the product owner.
- It read GitHub issues (no write) to find planned work and known breaks.
- It checked each page with the structure check, each ICE page with a small shape check, and every quote in a Sources section against its file. The record is `lint.json`.
- The decisions this run made from memory are in `cite-request.json`, for the caller to record with `memory.py cite` (recording them writes outside `bi-3-capability-1/`).
- The pages were written by hand in short-term memory, as the brief asked and as the BI-2 capabilities were. No skill drafts pages of the approved shape into short-term memory: the page skills (`enrich-capability-ice`, `enrich-grounding`) write only into the live model. That missing skill is named here, as on the earlier runs, not worked around further.

## What is built, and what is only planned

In one line: the job is built and live. `/shape-slice` designs the one slice that shows a business intent is served, reuses a slice that already serves it, fills the model with what the slice needs, and lets a person edit a slice in their own words. What is not built: choosing the surface from declared surfaces, research through a memory update, a second slice for an intent while the first is not in progress, a check that a slice needs nothing from a later slice, and moving a feature in or out by a person's edit.

### Built and live

- **The play `/shape-slice`** (`core/components/plays/shape-slice/`, compiled from `reference/ice.md`, C1 to C20, changed through `/edit-play` in #842, #908 and #798). A person names a business intent by its issue number. The run:
  - reads the intent from the product model, and writes the intent's page from the issue when the model has none, and says so (C1);
  - reads the model and memory first, and places the intent's outcome on the model's domains, capabilities and features (`find-work-placement`, over the domain shelves);
  - lists each gap that neither answers as one question (`find-slice-gaps`), drafts a proposed answer only from a named source (`propose-answers`), and asks within the configured question tier; each gap not asked becomes a written assumption; every question and answer is kept in the issue's short-term memory, and an answered question is never asked again (C2 to C5, C10);
  - asks before it shapes the slice only for a gap that blocks it and that no one but the person can answer; the surface and the tester are never a question (C3);
  - chooses, through `author-slice`, the one surface, the tester (a persona), the features from any capability in build order, with why that order, and what is left out; when nothing names a surface a person can test end to end, it writes no slice and says why (C6);
  - reuses a slice that already serves the intent (it lists the intent, or has the same features and surface), pulls a feature in or pushes one out so the slice stays testable end to end, and never touches a slice in progress, whose epic is past ready; it shapes a new slice instead (C7, `find_serving_slice.py`);
  - adds or fills every domain, capability and feature the slice needs, each page in its folder and marked to be deepened, brings the pages it uses up to the current rules, and proposes a thin ICE with both thin marks for a part with none; it warns the person and never sends them back (C8, C16);
  - writes the slice into the model's index with its link "slice serves business intent" and its record (`persist_slice.py`, six fields);
  - writes the slice's hidden file of failure and recovery conditions in the evals folder of its home plan (C15, `write_hidden_file.py`, `author-failure-recovery`);
  - runs the model check, the write guard and the trace check, shows one brief, and keeps nothing before the person's typed yes; a change shapes again, a stop undoes every write (C11, C12, C17);
  - opens and lands its own change through the change steps (C13).
- **The edit option** (`/shape-slice #<intent> --edit: <words>`, C20, #908, ADR 058). The person's own words become an exact list of changes; only the slice's name, its outcome and the tester's action, a part's one-line, and the when, way back or who fixes of a named line of the hidden file may change. A slice in progress may be edited; the brief says so and names its epic as out of date. A history line keeps who asked, when and their words. Anything else is refused (`edit_slice.py`, `author-slice` edit mode: "a feature in or out, a failure line, an eval, code" are not editable).
- **The slice in the ontology** (`standards/schemas/product-os/ontology.md`, v15, Phoenix memory): an ordered group of features from any capabilities, each small enough that a person can test its result, with one screen or surface a person can test end to end; it serves one or more business intents; it holds no ICE and is not an issue type; whether its work has started is shown by its epic; what must come first comes from its capabilities' needs; inside it, the builder picks its own build order.
- **The slice in the model today**: one slice, `sl-intent-to-design`, linked to bi-788, the old business intent the reorganisation retires. Its tester is the product owner, on the Claude Code command line.
- **The two index skills**: `link-model-part` adds features to a slice that exists ("a slice itself is shaped only by /shape-slice"); `/update-plan` uses it for a feature found during work (ADR 062). `remove-model-part` removes a slice and its record once a person approves, and touches nothing under the plans folder.
- **The plan tool** sees a slice only through its epic: each plan node may carry `represents` (the slice or feature it stands for). It has no view of slices of its own.

### Known breaks (filed)

- **#1033** (open), item 4: since the model's index has ICE entries, `slice_check.py` reports "thin mark drift" on older thin parts of the existing slice, and `write_hidden_file.py` finds no "Fails if" lines for older features. Both read the whole model by the new rule. The model check is this capability's; the hidden file is named under the overlap below.
- **#912** (open), P3: a fresh run after a stop can start from an old start copy. It fails loudly, and the person's yes still gates every write. Left off the pages as a small detail.
- **#913** (open): small findings on the edit option. Left off the pages.

### Only planned

- **The agreed capability line**: "Design slices: The work is cut into vertical slices a person can test end to end. (unique: vertical slices)".
- **BI-3**: why "Left alone, agents build horizontally, and nothing can be tested until the end. Vertical slices usually get left to people."; proof "Each slice can be tested end to end by one person on one surface." and "How a slice is tested is designed before it's built."; must not "Tell the builder the steps, or deliver work that only a later slice makes testable."
- **The approved pages already give this capability its job**: Turn intents into agent work ("Out: choosing the slice and writing its hidden file. Design slices owns them.", and "Design slices proposes a thin one where a slice needs it"); Manage surfaces ("Each slice picks its one surface from the declared ones", and choosing the surface and the tester is Design slices'); Keep the spec matched ("Design slices writes an intent's page from its issue when the model has none."); BI-1's research put "missing model pages are written on the fly as light pages" here.
- **The agreed names**: "/design-slice (was /shape-slice)". The drafts name the live play, `/shape-slice`, where they say what is built.
- **The tracker.** BI-3's sub-issues are about the older design flow: #608 (decide the old loop's recipe, which includes ordering the slices, a job ADR 053 dropped: "No play orders the slices across the product."), #595 (`/grill` cuts any slice), #565 (one issue per slice for the older design passes), #609, #501, and #978 (a person designs a story with the agent, which belongs to designing each slice). #561 (open, written for the older play) plans a check that a slice's stated outcome is delivered by what the slice holds. #895 (open) leaves "blocker work as its own slice" for the product owner to decide.

### In memory

- **Phoenix memory** holds the slice's rules (the ontology), the old epic rule "An epic is a vertical slice a user can interact with and a reviewer can verify end to end. It is never a horizontal layer like "set up the database" or "build the API."" (`standards/rules/epics.md`, written for a retired pipeline), and domain shelves that name the first path a person walks end to end in their field, for example the commerce shelf: "Build this spine first, end to end, before any enrichment." Memory has no learning on how to cut an intent into slices, how big a slice should be, or how to order a sequence of slices.
- **Phoenix memory's slice schema is out of date**: `standards/schemas/product-os/slice.yaml` there is v1 (one domain per slice, with order, effort and the old chain), while the play writes v2. The ontology (v15) is current. An agent that reads the slice schema from Phoenix memory gets the old shape until a person promotes v2.
- **Garura memory** holds the approved model pages and the one slice. No tier was missing.

## The overlaps, and how the line could be drawn

### With Design for evaluation and testing: who writes the slice's hidden file

The hidden file holds, for each feature of the slice, each "Fails if" line of its two ICE and exactly one recovery for each (when the eval sees it, the way back, who fixes). The eval reads it; no builder does. As built, `/shape-slice` writes it right after the slice (ADR 052). Four approved lines on three BI-1 pages name Design slices as its writer, and two more name both siblings: Turn intents into agent work capability ("Out: choosing the slice and writing its hidden file. Design slices owns them." and its rule "The "Fails if" lines go to the slice's hidden file, which Design slices writes."), Cut an intent into epics and stories ("The slice and its hidden file of failure conditions. Design slices writes them."), Write a story from its ICE ("The slice's hidden file, written from the "Fails if" lines. Design slices writes it."), and Add a feature found during work (two lines naming both).

1. **Here, as built and as approved.** Design slices writes the hidden file when it designs the slice, and adds an entry when the slice gains a feature. Design for evaluation and testing reads it to write the eval. Gain: nothing approved changes; the file is written at the moment the slice's features are chosen. Cost: how a slice is tested sits in two capabilities: what must never happen here, what must happen there. And the job does not match this capability's one line, "The work is cut into vertical slices", which says nothing about failure conditions.
2. **In Design for evaluation and testing.** Everything about how a slice is tested sits in one capability: the hidden file and the eval. The play can still write the file at the moment the slice is designed; a capability is a job, not a play. Gain: each BI-3 proof line maps to one capability ("Each slice can be tested end to end by one person on one surface" here, "How a slice is tested is designed before it's built" there), and it matches the sibling's one line, "How each slice will be tested is designed along with the slice", and Bring the design together's list, which names testing as its own part of the design. Cost: the six approved BI-1 lines above are reworded through named lines; nothing else changes (the ontology names the play, not a capability).
3. **Split.** The failure lines are listed here, from the ICE, and the recoveries are drafted there. Cost: one file with two owners and two moments, and the rule "exactly one recovery for each line" is then checked across two capabilities.

**My lean is option 2.** The product owner's standing rule is that each feature is a job the capability does and shows how it meets the capability. Writing failure and recovery conditions meets "how each slice will be tested", not "the work is cut into vertical slices". The drafts follow option 2: they hold no hidden-file feature, and they put the hidden file Out, owned by Design for evaluation and testing, with a note that the same run writes it today. **Under option 1**, a third feature is added here, "Write the slice's hidden file", built: one entry for each feature of the slice, one recovery for each "Fails if" line of its two ICE, "the builder can fix this alone" or "a person must decide", a thin ICE named in its entry, a kept entry changed only by an approved edit, and no copy of its lines outside the evals folder (sources: `/shape-slice` C15, F15, `write_hidden_file.py`, `author-failure-recovery`, ADR 052 §1 and §4, `standards/rules/expectation-generation.md` "A feature's recovery"). The Out line becomes an In line, and the edit option's hidden-file lines move into Update a slice.

### With Turn intents into agent work (BI-1, approved)

The approved pages draw most of the line: here, the slice in the model; there, one epic for each slice and one story for each feature, in the tracker. The grey zone: a feature found during work joins a slice through an `/update-plan` session (ADR 062, `link-model-part` with `add_features`), also a slice in progress.

1. **As approved and built.** Turn intents into agent work may add a found feature to a slice, in the session the person approves, and names what is owed for it. Design slices designs slices and makes every other change to them, and reads a feature that joined that way. Cost: two capabilities change one slice's list of features.
2. **Every change to a slice's features moves here.** Turn intents into agent work only hands the found feature over and adds its story. Cost: reopens the approved Add a feature found during work and ADR 062's one approval for one session.
3. **A found feature waits for the next slice design.** Cost: against ADR 062; work in progress goes on without the feature.

My lean is option 1. It changes nothing approved, and a feature found during work is a work event the person approves in one session. The drafts follow it.

### With designing each slice (agreed under another name, to be renamed) and Bring the design together

1. **What the slice is, here; how it looks and works, there.** Here: the slice's features in build order, its one surface, its tester and what the tester does there, and what is left out. Designing each slice: how the slice looks and works on its surface (its screens, flows and states) and which parts of the architecture it passes through, built on the project's positions. Bring the design together joins those designs, and how the slice is tested, into the one slice. Cost: when the design there finds the slice cannot work as cut (a feature is missing), it comes back here as an update.
2. **The surface and the tester move there.** Cost: reopens the approved Manage surfaces Out line ("Design slices ... owns it"), and the ontology says a thing with no surface is not a slice, so a slice could not be written here.
3. **One capability for both.** Cost: against the agreed list, which keeps them apart.

My lean is option 1. The drafts follow it.

### With BI-2's capabilities (approved)

Manage surfaces is the one that touches this capability: the approved page says each slice picks its one surface from the declared ones. As built, `author-slice` proposes the surface from the intent page, the model and the placement, because nothing declares surfaces yet (#553, open).

1. **Pick from the declared surfaces; propose when none is declared.** A slice picks its surface from the declared ones. When none fits or none is declared, it proposes one from the model and memory, names the gap, and the work goes on; a new surface goes to Manage surfaces as an update for a person to confirm. Cost: until Manage surfaces is built, every slice carries that gap.
2. **A slice names any surface, and Manage surfaces adds it later.** Cost: against the approved "Each slice picks its one surface from the declared ones"; surfaces drift.
3. **Designing a slice waits for declared surfaces.** Cost: against BI-2's "Block other work. Each design can be run at any time." and against the rule that the harness never stops a person.

My lean is option 1. The drafts follow it.

The architecture, the deployment design and the environments: no decision asked. A slice is designed and built on them and never chooses them ("Each slice is then designed and built on the project's architecture, and does not choose its own.").

### Other neighbours

No decision asked; the drafts draw these lines:
- **Specify the product.** It writes the ICE and the first pages of the model. Design slices adds a part a slice needs and the model lacks, at the depth known, and proposes a thin ICE for a part with none, as the approved BI-1 page says. It writes an intent's page from its issue when the model has none, as the approved Keep the spec matched page says.
- **Keep the spec matched to what's built.** It repoints or retires a business intent, which may repoint a slice. Out here.
- **Orchestrate agent work through planning.** The order the work runs in. No step orders the slices across the product (ADR 053). Out here.
- **Build the work (BI-4).** The builder picks its own steps inside a slice (ontology). A slice says which features, in which order a tester can test them, never the steps. That is how the drafts read BI-3's "Tell the builder the steps".
- **Test with evals the builder never sees.** It runs the eval. Out here.
- **Run plays as loops.** The old plan for one approval over the three shaping plays (#796) was closed as not planned. Out here.

## The persona

The drafts name **the product owner**, because what is built says so: the play's ICE gives "Personas: the product owner (gives the intent, answers, approves)", and each of its scenarios is "(product owner, ...)". Each slice also names a persona who tests it, its tester, chosen per slice (the one slice in the model has the product owner as its tester). The plays and agents after it, Turn intents into agent work and Design for evaluation and testing, read the slice.

## Features found

Two features, each built. They follow the shape the product owner asked for on the earlier capabilities: one job is one feature, and a later change is an update as the project changes.

- **Design a slice for a business intent** (fn-design-slice). Built. From a business intent, proposes the one surface, its tester, the features from any capability in build order and what is left out, from the model and memory first; asks only what neither answers, in one brief; reuses a slice that already serves the intent; adds what the slice needs to the model, with a thin ICE where a part has none; and writes the slice with its link to the intent after the product owner's yes. Sources: `/shape-slice` (C1 to C13, C16, C17, C19), `author-slice` (shape and reuse modes), `find-slice-gaps`, `propose-answers`, `author-slice-brief`, `find_serving_slice.py`, `persist_slice.py`, `persist_fills.py`; ADR 049, 052, 053; the ontology's Slice kind; GitHub #795, #838, #842 (closed); old pages cap-shape-slice and fn-795.
- **Update a slice as the project changes** (fn-update-slice). Built, except the parts named as not built. Changes a slice that exists: in a person's own words, after they see each change and say yes (also a slice in progress, with its epic named as out of date); by a later design for an intent it serves (a feature pulled in or pushed out, new name, outcome or tester's action, never a slice in progress); and takes a slice out once a person approves. Sources: `/shape-slice` C7 and C20, `edit_slice.py`, `author-slice` edit and reuse modes, `persist_slice.py`; `remove-model-part`; ADR 058, ADR 062; GitHub #908 (closed).

Candidates not drafted as features of their own:
- **Write the slice's hidden file.** Built. Under the lean, it belongs to Design for evaluation and testing; under option 1 it is the third feature here (see the overlap).
- **Write an intent's page when the model has none**, **add what a slice needs to the model**, **propose a thin ICE**, **ask only what the model and memory cannot answer**, and **reuse a slice that already serves the intent**. Each is built, and each is a step of designing a slice, so each sits inside fn-design-slice, as one job.
- **Add a feature found during work to a slice.** Built, and owned by Turn intents into agent work (overlap option 1).
- **Order the slices across the product.** Dropped by ADR 053; not a feature.
- **Design several slices for one intent at once, or the next slice for an intent.** Nothing records it as planned. As built, a second slice is designed for an intent only when the first is in progress. Named as a gap.

## Which lines of the old pages carry over

The old pages are `.garura/product/product-os/software-delivery-planning/shape-slice/capability.md` (cap-shape-slice) and `.../shape-slice/fn-795/feature.md`. They are not changed here.

### The old capability page (cap-shape-slice)

- Line 1, "# Capability: Shape a slice": does not carry. The agreed name is "Design slices".
- Line 4, the directional intent:
  - "Shape the one slice that shows a business intent is served.": carries in meaning, as designing a slice for a business intent.
  - "A slice is an ordered group of features, from any capabilities, that a person can test end to end on one surface.": carries, as the definition on every page.
  - "This capability picks those features in build order, the one surface, and the person who tests it.": carries.
  - "It reads the product model and memory first, and asks the person only what neither answers.": carries.
  - "It writes the slice, its link "slice serves business intent", the slice record, the model parts the slice lacks (marked to be deepened later), and the slice's hidden file of failure and recovery conditions (decision 6 of #844).": carries, except the hidden file (Out under the lean) and the pointer to another issue's decisions, replaced by ADR 052.
  - "It never writes the plan, the epic, the stories or the eval: those are the work of other capabilities.": carries, with the capabilities named.
  - "It matters because every later step plans and checks this slice; a slice with no surface a person can test cannot be checked.": carries.
- Line 6, "To be deepened later: written by /shape-slice for bi-788 ...": does not carry. The old intent is retired, and the new page is written at its full depth.
- Lines 9 to 13, Sources: ADR 049 (Decision 1.1), ADR 052 (Decisions 1 and 5), ADR 048 (Decision 2, the slice definition) and GitHub #795 carry. The User Story Mapping line does not carry: it is a web source, and under the standing rule research is used only after a person approves it as a memory update.
- Line 15, the Thin line: does not carry. The part is built.
- Lines 17 to 26, the ICE inside the page: moves to its own `ice.md`; a part's page holds no ICE section.
  - Line 18 (Goal, one slice, one surface, build order): carries as the one Goal.
  - Line 19 (Goal, the hidden file): does not carry under the lean; and an ICE has exactly one Goal.
  - Line 20 (Limit, write only ...): carries, without the hidden file.
  - Line 21 (Limit, ask only what the model and memory do not answer, within the question tier): carries.
  - Lines 22 and 23 (Fails if: no surface, no tester or more than one surface; a question the model or memory answers): carry.
  - Line 24 (Fails if: a line missing from the hidden file): does not carry under the lean.
  - Line 25 (Context): carries, split into Read, Never read, Persona and Scope, in plain words, without file paths.
  - Line 26 (Checked by): carries as a Done means, checked by someone other than the doer, without the hidden file.

### The old feature page (fn-795)

- Line 1, "# Feature: /shape-slice writes the slice and its hidden file": does not carry. A feature is named as the job a person can do, not as a play.
- Line 4: "/shape-slice <intent> reads the business intent and the product model, asks the person only what the model and memory do not answer, and writes one slice into the spine with its link to the intent." carries. "It also writes the slice's hidden file ..." carries only under option 1. "and a thin ICE for each part the slice needs that has no ICE" carries. "It writes no plan, no epic, no story and no eval." carries. "Built in #795." carries as a source. "Not built yet: the hidden file and the thin ICE need the play's /edit-play change (#842)." does not carry: #842 built them.
- Line 6, the deepen note: does not carry.
- Lines 9 to 13, Inputs and Outputs: all carry (the intent page or its issue; the model and memory; the person's answers; one slice with its features, surface, tester and link; the pages the slice needs, marked to be deepened).
- Line 14, "Out (not built yet, #842): the slice's hidden file": does not carry under the lean; under option 1 it carries without "not built yet".
- Lines 17 to 19, 21 (model and memory first; an assumption for each gap not asked; reuse a slice that serves; nothing kept before yes, stop undoes every write): carry.
- Line 20 ("The confirmation shows the slice only ... (decision 4)"): carries in part. The brief now also shows each assumption, the thin-ICE warning, a reuse's differences and the model check's warnings; the pointer to another issue's decisions does not carry.
- Line 22 (the thin ICE): carries, without "Not built yet (#842)".
- Lines 25 to 27 (acceptance: one slice serves the intent after yes; no second slice; no plan, epic, story or eval): carry. Line 28 (the hidden file in the evals folder) carries only under option 1. Line 29 ("Thin: the checks for the hidden file wait ..."): does not carry.
- Lines 32, 33 and 36 (Out: the plan, epic and stories; the eval; the checks that no build is given the evals folder): carry, with today's capability names. Line 34 (the loop and its one approval, #796): does not carry, #796 was closed as not planned. Line 35 (eval encryption, dropped; the author-slice skill, built): does not carry.
- Lines 39 to 41, Sources: GitHub #795 and ADR 052 carry; the ADR 057 line carries only for the hidden file, so under the lean it goes to the sibling.
- Lines 45 to 53, the ICE inside the page: moves to `ice.md`. Line 46 (Goal) and lines 49 and 50 (Fails if: writes a plan, epic, story or eval; a second slice for an intent already served) carry; line 47 (Goal, the hidden file) and line 51 (Fails if, the hidden file) do not carry under the lean; line 48 (Limit) carries without the hidden-file path; line 52 (Context) carries in plain words; line 53 (Checked by) does not carry as written, because it names one particular plan; it carries as a Done means without it.

## Gaps that matter, each named as not built on the pages

- **The surface is not picked from declared surfaces.** Nothing declares the project's surfaces yet (#553), so each slice's surface is proposed from the model and the placement.
- **No research through a memory update.** When nothing in the model or memory backs an answer, the question carries no proposed answer and the person answers it. Researching it and raising a memory update for a person to approve is not built in this capability.
- **A slice is not checked for needing a later slice.** Nothing checks that every part of the slice's outcome is delivered by its own features (#561 plans such a check, written for the older play), or that the slice leans on no feature that only a later slice brings. This is BI-3's must-not, "deliver work that only a later slice makes testable".
- **One intent, one slice at a time.** A second slice is designed for an intent only when the first is in progress. Cutting an intent into a sequence of slices is not built.
- **A person cannot move a feature in or out of a slice by an edit.** The edit refuses it; only a later design run pulls in or pushes out, and only for a slice not in progress.
- **The model check breaks on older parts** (#1033) since the model's index lists ICE pages.
- **Memory has no learning on how to cut work into slices**, and Phoenix memory's slice schema is out of date (v1).

## Open points for the product owner

- Who writes the hidden file: option 1, 2 or 3. The drafts follow option 2.
- The line with Turn intents into agent work: option 1, 2 or 3. The drafts follow option 1.
- The line with designing each slice: option 1, 2 or 3. The drafts follow option 1.
- The surface of a slice and Manage surfaces: option 1, 2 or 3. The drafts follow option 1.
- The persona: the product owner, from what is built.
- The feature names, each led by a verb as on the other capabilities: "Design a slice for a business intent", "Update a slice as the project changes".
- How the drafts read "Tell the builder the steps": a slice gives its features and the order a tester can test them, never how to build them. He may read it otherwise.
- Not on the pages, left to him (#895): whether blocker work, which no person can test end to end, may be its own slice.

## Details left out of the pages

Left for an agent that builds or changes these parts to find in the code: the play's step numbers, its scripts' exit codes and file names, the question tier's sizes, the slice record's fields, and the small findings of #912 and #913.

## What this run read from memory

Through the memory tool, copied to `.garura/project/issues/1021/context/bi-3-capability-1/memory/` with `manifest.json`: from Phoenix memory, the ontology (v15), the slice and spine schemas, the capability and feature grounding templates, the expectation-generation rule, the epic rule, the surface contract, the pipeline rule, the eval format rule, the schema index, the modular monolith learning and the commerce shelf. From Garura memory, the lines of the approved pages and of BI-3 read for the decision traces (see `cite-request.json`). No tier was missing.

## Checks

- **Structure check** (`python3 .claude/skills/discover-capabilities/scripts/lint_grounding.py`): `--kind capability --stage directional` on the capability page, `--kind feature` on each of the two feature pages. All three read ok, with no error and no warning, on the first run and again after the last change.
- **ICE shape check** on the three ICE pages: no thin mark (each part is built); Intent, Context and Expectation in order; exactly one Goal; Limits and Fails if (the capability has four of each, each feature three); the fixed Read line first; the Context labels in order (Read, Never read, Persona, Scope); a Scenario; and a Done means checked by someone other than the doer. All three read ok. No part page holds an ICE section.
- **Quotes**: 115 quotes in the Sources sections, checked word for word against their files (memory quotes against this run's short-term copies in `memory/`, the agreed one line and the capability list against `.garura/project/issues/1021/context/capabilities.md`), and the business intent's words quoted in the page bodies against `.garura/product/product-os/intents/bi-3.md`. None missing. Thirteen Sources lines carry no quote by design: the GitHub lines, the old parts taken over, the short line beside each feature, and the shelf line.
- **Words**: no page uses "lens" or "lenses", names a real person, a home-folder path or a particular plan, or says anything about seeding memory, a design lock or a gate. The one word hit is the agreed list's own heading, "The capability list the product owner locked on 2026-11-03", worded as on the approved pages.
- The record is `lint.json`. The check script ran from the session's scratch folder and is not kept here.
