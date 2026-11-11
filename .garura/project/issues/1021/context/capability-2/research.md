# Turn intents into agent work: research and drafts (issue 1021, capability 2)

Draft only. Nothing under `.garura/product/`, on GitHub or in git changed. The drafts are under `.garura/project/issues/1021/context/capability-2/drafts/product-os/software-delivery-planning/turn-intents-into-work/`.

## The boundary the drafts are written under

The product owner settled it on 2026-11-06, in their words: "we narrow orchestration.. thats what an orchestrator will do".

What that means, as it was passed on to this run:
- Turn intents into agent work (business intent Product → Spec, bi-1) owns turning a confirmed business intent into the work items agents execute: epics, stories, chores, bugs and spikes. That includes what /shape-plan and the author-work-items skill do today (one epic for each slice, one story for each feature, each story written from its ICE) and changing those work items later.
- Orchestrate agent work through planning (business intent Orchestration, bi-9) is narrowed to running that work once it exists: putting it in order, running the loops, and tracking it in the tracker.
- The plays that do this work belong to the orchestrator role, for example /shape-plan. A role says who runs a play. It does not change which capability the play serves.
- A plan file and its branch sit outside the product model, and no page names a particular plan.

No draft was written under an earlier assumption. The research had leaned to a narrower line (only the story's words here) before the decision came; the drafts were written after it, to the settled line.

## The overlap question, in plain words

Yes. Before the decision, the work items that "Turn intents into agent work" makes were the same epics and stories that /shape-plan makes for "Orchestrate agent work through planning". The evidence:
- What is built: /shape-plan is given one business intent, reads every slice the model links to it, and in one run makes one epic for each slice and one story for each feature. One call of one skill (author-work-items) writes the epic titles and every story together, and one checkpoint approves them all. So the "verticals" that planning creates (the epics) and the stories this capability makes came from the same run.
- The ontology, in Phoenix memory: the Plan kind "creates one Epic for each Slice, or uses the one that exists, and the Stories of that Epic, one for each Feature of the Slice", and the Story kind says "The plan play makes it when it creates the Epic."
- The old model: Build a plan (cap-718), "a plan file, one epic per slice and one story per feature", was set to merge into Orchestrate agent work through planning, while this capability's one line says the same about stories.

The three ways the line could be drawn, kept for the record:
1. The verticals with planning, the agent's unit of work here. Planning makes the plan and one epic for each slice, and files them; this capability writes each story's words from its ICE. Both one lines stay true, but one run and one skill call are split across two capabilities and two business intents.
2. One capability. The two merge into one that serves both bi-1 and bi-9. This matches the build, but Product → Spec loses its own capability for "a spec agents can act on".
3. Make here, run there. This capability makes and changes the work items; planning runs them (order, status, loops, tracking). One play maps to one capability, and planning's one line ("reads the slices and creates verticals") then needs new words.

The product owner chose the third.

## Which built pieces fall where

Under Turn intents into agent work (bi-1):
- /shape-plan, the first cut of an intent into work items: its scripts gather_plan.py (the slices and the clean ICE copies), find_work_items.py (finds what exists, by mark), check_drafts.py, render_brief.py, record_approval.py, write_work_items.py (files the epics and stories), write_plan_file.py, check_plan.py and check_tracker.py.
- The author-work-items skill: the epic titles and the story words, and its story mode for one story in a session.
- The work-item side of /update-plan: the author-plan-changes skill (instructions into list entries), check_entries.py (the rules for kinds and parents), add_entries.py, the track-plan-changes skill (the tracker writes), write_plan_changes.py, check_agreement.py, feature_ice.py (a story for a model feature, #1002), and place_feature.py with the find-work-placement skill (a found feature, #931).
- The old model parts it takes in: Build a plan (cap-718) with fn-727, fn-728 and fn-818; and from Manage a plan (cap-720), the work-item changes of fn-730 and all of fn-931.
- Part of old fn-727 goes elsewhere: "missing model pages are written on the fly as light pages" is now /shape-slice's work (Design slices). /shape-plan writes no model page.

Stays with Orchestrate agent work through planning (bi-9, running the work):
- The status of each item and the plan's Status and Direction, which an /update-plan session sets (finish, drop, start, Now, Blocked), and the items closed in the tracker that a session lists at its start (#1007, merge-change sets an item Done).
- Seeing the work: /list-plans, /show-plan and the plan tool (old cap-719: fn-729, fn-628, fn-806), and /list-focus-issues.
- Plan branches: start-change and merge-change on a plan's branch, the plan tool's plan_branch.py, and the branch step of /update-plan (old cap-721: fn-731, fn-673).
- The per-issue plan of what is done next and in what order (the author-plan-file skill).
- Running plays as loops (complete-discovery) and managing ADRs (record-decision), as the agreed list already says.

Stays with the other neighbours:
- Design slices (bi-3): /shape-slice, author-slice, find-slice-gaps, and author-failure-recovery (the hidden file). /shape-slice also writes an intent's page from its issue when the model has none.
- Design for evaluation and testing (bi-3): /shape-eval and author-slice-eval.
- Build the work (Code → Validation): /build-epic and author-build-plan, which cut an epic into stories, tasks, tests and docs inside the build.
- Ship every change the same way (Developer tooling): start-change filing a change issue from a short description (track-issue, validate_issue.py), and commit-change mapping changes to issues (find-matching-issues).
- Manage the model: the thin page and model entry of a part found during work (enrich-grounding, link-model-part). Add a feature found during work asks these skills to write.
- Shared tools that no one capability owns: track-issue, platform-adapter, and find-work-placement, which Specify the product and Design slices use too.

Not placed: the remove-plan skill. It deletes plan files once a person approves. It neither makes work items nor runs them, so the product owner places it.

## Features found

Each is built. No feature is drafted as not built: neither the agreed list nor an old model page records a planned feature for this capability that is not built.

- Cut an intent into epics and stories (fn-cut-intent-into-work). Built. Makes one epic for each slice that serves a confirmed intent and one story for each ready feature, files them after the product owner's yes, and writes the plan file's tree. Source: core/components/plays/shape-plan/ (its ICE, SKILL.md and scripts); GitHub #818, #727 and #728 (closed); old pages cap-718, fn-727, fn-728 and fn-818.
- Write a story from its ICE (fn-write-story-from-ice). Built. Writes a story's title, scope of work and Context guidance from its feature's ICE and its capability's ICE, with the "Fails if" lines taken out, and a script checks it. Source: core/components/skills/author-work-items/SKILL.md, shape-plan's gather_plan.py and check_drafts.py, update-plan's feature_ice.py; GitHub #1002 (closed).
- Change the work items (fn-change-work-items). Built. In an /update-plan session, adds, moves, renames, rewrites and re-kinds epics, stories, chores, bugs, spikes and feature items, checked against the rules and landed on one approval. Source: core/components/plays/update-plan/reference/ice.md (C3 to C7, C14) and check_entries.py; GitHub #730 (closed); old page fn-730.
- Add a feature found during work (fn-add-found-feature). Built. Places a found feature under its capability, in its slice and under its epic, and lands its thin page, model entry and story on one approval. Source: update-plan's ice.md (C11) and SKILL.md, place_feature.py; GitHub #931 (closed); old page fn-931.

## Gaps that matter, each named as not built on the pages

- No builder reads a story yet. The ontology says the build's context step reads a story's Context guidance and collects the context, and no built play or agent does it. /build-epic reads the spine's epic list and epic pages, which ontology v7 took out of the model. So the proof of Product → Spec, "An agent acts on the spec without asking again", has nothing to test it today. Build the work owns the fix.
- A later slice is not added in one step. The ontology says the plan play adds a new slice and its epic to the plan an intent already has. /shape-plan stops when the plan file exists, and /update-plan has no instruction for a whole slice, so its epic and stories go in one item at a time.
- A story is not written again when its ICE changes. The ontology calls this drift for the Alignment loop, which is not built.
- No check stops a story from naming the eval or the folder that holds it. The old page fn-818 sets the rule; check_drafts.py looks for failure lines and recovery phrases, not for the eval's name.

## Open points for the product owner

- "Tasks" in the one line. The agreed one line says "stories, issues and tasks", and the decision names epics, stories, chores, bugs and spikes. The model has no task kind, and the only built step that cuts tasks is inside /build-epic, at build time. Either the one line drops "tasks", or a feature for tasks is added and its home decided (here or Build the work).
- Two candidate features, not drafted because nothing records them as features: write a story again when its ICE changes (an ontology rule), and add a later slice to an intent's work items in one step (an ontology rule, and named in the old page fn-818).
- Where remove-plan goes.
- The line inside one /update-plan session. The drafts put adding, moving, renaming, rewriting and re-kinding items here, and every status change (finish, drop, start, Now, Blocked) with tracking in bi-9. Dropping an item closes its issue as not planned; that reads as tracking, but the product owner may see it as changing the work.
- Orchestrate agent work through planning's one line ("reads the slices and creates verticals") now describes work this capability does. It needs new words to match the narrowed scope.

## Details left out of the pages

The pages hold what each part does, its main rules with their reasons, the gaps that matter and the checks that prove it. An agent that builds or changes these parts finds the rest in the code:
- The names and fields of each run record (gather.json, work-items.json, approval.json with its fingerprints, tracker-record.json, changes.yaml).
- The plan file's fields, its six item statuses and its five plan statuses.
- The finder's "add-sections" and "move out" actions, which /shape-plan cannot reach because it runs only when no plan file exists.
- The session folder and its self-clean, the template screens, and the list commands "show the list" and "take out 3".
- The lookup "find #N in the model", which names a story's feature and adds nothing to the list.
- The ontology's rule that a spike comes only after its story is built; no check holds it.
- How a tracker write that stopped part way is picked up again.
- The change plays that open and land /shape-plan's own change.

## Structure check

`python3 .claude/skills/discover-capabilities/scripts/lint_grounding.py` on each page, with `--kind capability --stage directional` for the capability and `--kind feature` for each feature: all five pages read ok, with no error and no warning. The record is `.garura/project/issues/1021/context/capability-2/lint.json`.

The structure check has no kind for an ICE page, so a small check in the same record tested each of the five ICE pages: the three sections in order, exactly one Goal, at least one Limit and one Fails if, at least one Done means, the fixed Read line, and no thin mark (every part is built). All five read ok.

Every quote in a Sources section was checked against its file, word for word: none is missing.

## What this run read from memory

Five files from Phoenix memory, through the memory tool, copied to `.garura/project/issues/1021/context/capability-2/memory/` with `manifest.json`: the ICE rubric, the ontology, and the capability, feature and content-standard grounding templates. The decision and its trace are in `cite-request.json`, for the caller to record; this run writes nothing outside `capability-2/`.
