# Gather an epic's work from the plan: research and drafts (issue 1021, BI-3 capability 1)

Draft only. Nothing under `.garura/product/`, on GitHub or in git changed. The drafts are in `.garura/project/issues/1021/context/bi-3-capability-1b/drafts/product-os/software-delivery-planning/gather-epic-work/`: the capability page and its ICE page, and two feature pages, each with its ICE page. Nothing of the capability is built, so all three ICE pages carry the thin mark. The earlier draft, Design slices (`bi-3-capability-1/`), is superseded; only its facts were reused.

What this run did besides reading:
- It copied the two memory files it decided from (the builder isolation rule and the ontology, both from Phoenix memory) into `bi-3-capability-1b/memory/`, with `manifest.json`.
- It read GitHub issues #1023, #978, #646, #964, #976, #954 and #975. No write.
- It ran no placement: the domain (software delivery planning) was decided.
- The decisions made from memory are in `cite-request.json`, for the caller to record with `memory.py cite`.
- The pages were written by hand in short-term memory, as on the earlier runs: no skill drafts pages of the approved shape outside the live model.

## What is built, and what is only planned

In one line: nothing gathers an epic's work for a build. Parts exist that read what gathering needs.

Built and live (each reads, none gathers):
- **The plan tool** (`core/tools/plan/README.md`): prints one plan's tree from its file, with each item's issue, kind, title, status and its `represents` mark. The plan file's six item kinds: epic at the top, feature item under an epic, story under an epic or a feature item, spike, chore and bug under a story.
- **track-plan-changes, read mode** (`core/components/skills/track-plan-changes/SKILL.md`): reads a plan's issues from the tracker, "Each issue's title, type, labels, state and close reason, text, parent and sub-issues."
- **platform-adapter `view-issue`**: an issue's type, parent and sub-issues, GitHub and GitLab only.
- **find_work_items.py** (/shape-plan): finds each epic and story by the plan file's mark; "A title is never compared."
- **The story's fixed parts** (`write_work_items.py`, `author-work-items`): "Scope of work" with Goals, Limits and Expectations, then "Context guidance" (Read, Never read, Persona, In and out), then "Written from: <the two ICE pages>". The expectations hold "the scenarios, what "done" means, the quality needs". A script can therefore split a story the same way every time.
- **The memory tool**: find, read and copy with a fingerprint, raise a memory update, record a trace.
- **The ready check** (`check_ice_workable.py`): ready, partly ready or not ready; "no play plans, breaks down or builds from it" when not workable.

Built but stale:
- **/build-epic**: started from one epic record in the spine (`check_ready_epic.py`: "In the spine + grounding model an epic is an" entry), which ADR 048 took out of the model. Its Step 3 had one agent capture the epic's whole context, each entry with its source, by reading the feature ICE pages (now forbidden). Its isolation rules handed each builder only its piece and the spec, "NEVER the whole `plan.yaml`, a sibling piece, a free-repo directive, a test" piece's files, evals or pass criteria. code-builder's TDD mode (built, not stale) still reads the tests it must pass, which his new rule forbids.

Only planned:
- **Gathering an epic's work**: the product owner's list item 1 of 2026-11-09 (`capabilities.md` line 27). No issue.
- **The build's context sub-agent**: ontology (Phoenix memory, line 734), ADR 049 §4, the approved Turn intents into agent work page ("The build step that reads a story's Context guidance and collects its context is not built."), fn-898 ("A build's inputs are the slice's stories and the context that the build's context sub-agent collects").
- **The Agent-work tool** (#1023, open): the one tool that knows the tracker (ADR 065 rule 4). Until it lands the plan plays must not run, so no new epic exists to gather.
- **The checks that no build was given the eval** (fn-898, #898): a lint over the build's inputs; it would read what this capability hands the builder.

## The rule that shapes most of it: what the builder may receive

The sources disagree, and the drafts follow the product owner:
- His words, 2026-11-09: "the code, when being written, should not get to see what tests there were". The brief: the builder never receives an eval, a test or a success scenario.
- Phoenix memory, `standards/rules/builder-isolation.md` line 35: "The builder never receives success_scenarios under any circumstance."
- Against it: the routing table (`docs/philosophy/idd-principles.md`, "Success scenarios (Expectation) | ✓" for the builder), ontology v10, ADR 049 ("The story gets the goal, the limits, the expectations"), and the approved Turn intents into agent work page ("The builder reads the story"). Today a story's expectations hold its scenarios.

## The overlaps

### With Orchestrate agent work through planning (choosing the epic, running the work)

Decided: choosing which epic comes next is Orchestration's. Open is who starts the gathering and what happens to the status.
1. **A person or Orchestration names the epic; gathering starts from it, reads each item's status and sets none.** Gain: matches the approved boundary ("Out: running the work once it exists: its order, the status of each item ...") and /update-plan's "A person sets every status". Cost: the plan shows nothing until someone marks the work as started.
2. **Gathering also marks the epic as being worked on in the plan file.** Gain: the plan shows the build started. Cost: gathering then writes the plan file and a status, both owned elsewhere.
3. **With no epic named, gathering takes the epic of the plan's current item.** Gain: one step less. Cost: it picks work, which is Orchestration's.

Lean: 1. The drafts follow it.

### With Turn intents into agent work (makes the epics and stories)

The question: the story's expectations hold its scenarios, and the builder must not see them.
1. **Gathering splits each story: the builder's share holds the title, goals, limits and Context guidance; the test share holds the expectations; the line naming the ICE pages goes to neither.** The story stays as it is. Gain: nothing approved changes in how stories are made; a script does the cut. Cost: approved lines that say "the builder reads the story" are reworded later, and a quality need written among the expectations reaches the builder only if the story writer puts it among the limits.
2. **The story itself stops holding scenarios; Turn intents into agent work writes them where no builder reads.** Gain: nothing to cut. Cost: reopens the approved pages, the ontology and the story writer; the test writer and the eval play then read two places.
3. **The builder gets the whole story, as the routing table and ontology say; only evals, tests and failure lines stay out.** Gain: no change. Cost: against his words and the builder isolation rule.

Lean: 1. The drafts follow it. Line drawn with no decision asked: gathering never changes a work item or the plan file; it names a mismatch (an item missing from the tracker, a wrong parent, a story without its parts, an epic map that differs from the tree) and Change the work items fixes it.

### With Write the evals that check the work

1. **The eval writer reads the epic and its stories itself, as /shape-eval does today; gathering hands it nothing and never reads the evals folder.** Gain: as built; gathering stays far from the eval. Cost: the tracker is read twice.
2. **Gathering hands the eval writer the test share.** Gain: one read. Cost: the eval writer still reads the hidden file on its own, so it has two inputs.
3. **Gathering also gathers the hidden file for the eval writer.** Cost: failure lines then sit beside the builder's share, and the ontology forbids the context sub-agent from reading it.

Lean: 1. The drafts follow it.

### With Design the work

1. **Design starts from the builder's share and the collected context, and reads the project's standards and the BI-2 positions itself.** Gain: what design writes may reach the builder, so design never holds a test either. Cost: design does a second set of memory reads.
2. **Gathering also collects the project's standards and positions for the design.** Gain: one gathering. Cost: gathering then judges what a design needs.
3. **Design gathers its own work from the plan.** Cost: two readers of one epic that can disagree.

Lean: 1. The drafts follow it.

### With Build the work test first

1. **Gathering prepares the work items, the collected context and the two shares; the build hands each agent its share and keeps the tests it writes from the builder.** Gain: "gathered with care" sits in one place, before any agent starts. Cost: one approved line moves: Write a story from its ICE, "Collecting the context when the build runs. Build the work does this."
2. **Gathering only lists the work items; collecting context and cutting the shares stay with the build, as the approved line says.** Gain: no approved line moves. Cost: this capability shrinks to a list read from the plan.
3. **Gathering collects everything into one set, and the build cuts each agent's share when it hands it on, as /build-epic did.** Gain: the cut sits close to its use. Cost: the scenarios sit beside the builder's material until the cut, and the check of the builder's input must read every hand-off.

Lean: 1. The drafts follow it.

### Other neighbours (no decision asked)

- **Fix defects test first**: a bug gathered here is handed on to it.
- **#954** (one epic per plan): on record, but decided here: an epic stands for one slice.
- **#646 and #964** (agents build only from approved pieces): a check before work starts, left out under the decided "no gate".
- **#976** (several issues in one change): Developer tooling.

## The persona

The developer, a person or an agent who starts the build of an epic, from what is built: /build-epic's scenarios are "(developer, end to end)", /fix-bug's are "(developer, end to end)", and the approved Environment setup page names "the developer, a person or an agent who builds the project's code". Also the agent that builds each story, as the approved Turn intents into agent work page says. Not the product owner: gathering needs no approval.

## Features found

- **Gather an epic's work items from the plan** (fn-gather-epic-work). Not built. From a named epic, finds every story (also under a feature item) and each story's chores, bugs and spikes in the plan file, reads their text through the tool that knows the tracker, keeps each status, splits each story into the builder's share and the test share, and names mismatches. Sources: his list item 1 (2026-11-09); the plan tool; track-plan-changes read; find_work_items.py; write_work_items.py and author-work-items (the story's parts); /build-epic (stale); the ontology's plan tree, Epic R3 and map rule; builder-isolation; ADR 065 rule 4; #1023.
- **Collect each story's context from its guidance** (fn-collect-story-context). Not built. Reads each story's Context guidance and collects what it points to, memory first, research only through an approved memory update, into the story's short-term memory with each part's source; never an ICE page, the eval, the hidden file, the evals folder or what the Never read line names. Sources: the ontology (line 734); ADR 049 §4; the approved Turn intents page line 20; Write a story from its ICE; fn-898; /build-epic Step 3 (stale); the memory tool guide.

Candidates not drafted:
- **Choose the next epic**: Orchestration's, decided.
- **Update the gathered work as the plan changes**: no source records it as planned.
- **The Agent-work tool**: Orchestration's tracker work; gathering uses it.
- **Seeding the memory a build needs**: decided out.
- **Cutting each builder's piece inside the build** (/build-epic's piece cut): Build the work test first's.

## Gaps that matter, named on the pages as not built or not decided

- Nothing gathers an epic's work; the old play's epic record is gone.
- The Agent-work tool (#1023) is not built.
- Nothing keeps a story's expectations out of what the builder receives.
- A story is not written again when its ICE changes.
- Not decided: how a test written in a chore's, bug's or spike's text is kept out of the builder's share (they have no fixed parts).
- Not decided: whether the project's existing tests may be collected as context.
- Memory has no rule on gathering, beyond the ontology and the builder isolation rule.

## Checks

- **Structure check** (`lint_grounding.py`): capability (`--kind capability --stage directional`) and both features (`--kind feature`): ok, no error, no warning.
- **ICE shape check** (a small script in the session's scratch folder): all three ICE pages open with the thin mark, hold Intent, Context and Expectation in order, exactly one Goal, three Limits and three Fails if, the fixed Read line, the Context labels in order, a Scenario and Done means checked by someone other than the doer. No part page holds an ICE section.
- **Quotes**: 85 quotes in the three Sources sections, each found word for word (spaces normalised) in its file: memory quotes against this run's copies in `memory/`, the product owner's words against `capabilities.md`, the #1023 quote against the issue text. Every quote in the page bodies is also found in that page's sources. One quote holding the word "lens" was replaced.
- **Words**: no page says lens, seed, lock or gate, names a real person, a home-folder path or a particular plan.

## Addendum, round 2 (2026-11-09): the redraft to the product owner's clarification

His words are in `page-approvals.md`. The round 1 drafts are kept as they were in `drafts-round-1/`. The redraft is in `drafts/product-os/software-delivery-planning/gather-work-under-item/`, and the round 1 folder `gather-epic-work/` was removed from `drafts/`.

What changed:
- **The starting point.** The capability no longer starts only from an epic. The technical lead names one item by its ID, at any level of the plan: an epic, a feature item, a story, or a chore, bug or spike. The capability gathers that item and every item under it, every level down, and nothing outside it. His words: "I should say an ID, and anything under it should all be planned"; "The entire tree needs to be handled."
- **The names.** The capability is now "Gather the work under a chosen plan item" (folder `gather-work-under-item`). Its first feature is now "Gather the whole tree under a chosen item" (`fn-gather-item-tree`, which replaces `fn-gather-epic-work`). "Collect each story's context from its guidance" keeps its name and folder.
- **Why the whole tree.** Everything under the chosen item is then designed and coded in the same run ("everything under it gets designed"). The capability page and the first feature both say so.
- **The low-level design moves to Design the work.** The classes, the functions, the reusable patterns, the code samples and the surface design are named in the capability's Out line, and in the first feature's Out of scope, as what Design the work does with the gathered tree.
- **The persona.** It is now the technical lead, who names the plan item and designs the work from what is gathered. His words: "designs are going to be done by, let's say, a technical lead or an architect, maybe a technical lead. The coding will be done by the developer, including the TDD." The developer appears only as the builder, in a later capability. This changed every Persona line, the Benefit hypothesis's "Who it serves", and the three Scenarios.
- **Kept as drafted.** No status is set. Each story is split by script into the builder's part and the test writer's part, with the expectations going only to the test writer. The eval writer reads the work items itself. Design reads the project's standards itself. The build hands each agent only its part. The context feature changed only where the chosen item is no longer always an epic.
- **New rules on the first feature.** An ID that no plan holds is named, and nothing is gathered ("nothing is guessed"; /show-plan's "A number no plan has gets a plain message"). An item from outside the chosen tree is never gathered, because everything gathered is designed and built in the same run.
- **New open points named on the pages:**
  - whether a person may name the plan itself, to gather every epic in it;
  - how a test written in the text of a feature item, chore, bug or spike is kept from the builder, since those items have no fixed parts;
  - when the chosen item is a chore, a bug or a spike, its tree holds no story, so whether its story's Context guidance is read for its context.
- **Assumptions.**
  - The plan file has no item kind called "test". The "tests" in his description of the tree are taken as work items of the kinds the plan holds, and they are gathered like any other item under the chosen one.
  - His "features" under an epic are the plan's feature items.
  - An epic can sit in two plans. Which plan's tree is read in that case is left as a detail for the build.

Checks, round 2:
- **Structure check:** the capability page (directional) and both feature pages read ok, with no errors and no warnings.
- **ICE shape check:** all three ICE pages pass. Each has the thin mark, one Goal, three Limits, three Fails if, the fixed Read line, the Context labels in order, a Scenario, and Done means checked by someone other than the doer.
- **Quotes:** all 102 Sources quotes were found word for word in their files: his new words against `page-approvals.md`, his earlier words against `capabilities.md`, and memory quotes against the copies in `memory/`. Every quote in the page bodies is in that page's sources. The one quoted phrase not in a source is the example story title "A guest pays by card" in a Scenario, which is the shop example in `core/components/skills/author-work-items/SKILL.md`.
- **Words:** no page says lens, seed, lock or gate, names a real person, a home-folder path or a particular plan, or names the developer as its persona.
