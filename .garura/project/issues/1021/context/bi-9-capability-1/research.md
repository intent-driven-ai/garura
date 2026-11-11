# Orchestrate agent work through planning: research and drafts (issue 1021, BI-9 capability 1)

Draft only. Nothing under `.garura/product/`, `.garura/core/`, `.claude/` or `core/`, on GitHub or in git changed. The drafts
are in `.garura/project/issues/1021/context/bi-9-capability-1/drafts/product-os/`:
- `software-delivery-planning/orchestrate-agent-work/`: the capability page and its ICE page, and the pages of the three
  new built features (fn-go-to-plan-branch, fn-know-what-next, fn-remove-plan), each with its ICE page.
- `features/fn-729/`, `features/fn-806/`, `features/fn-628/`, `features/fn-730/`: the four older features that join this
  capability, each page with its ICE page beside it, at the doc path the spine gives.
- `software-delivery-planning/shape-slice/fn-795/`: the older feature for the choice of the slice, at the doc path the
  spine gives, with its ICE page beside it. See "Gaps": this folder is the folder of the old slice capability.

In one line: this is built, at a small scale. Three views show the plans from the plan files alone, one approved session
sets every status and the direction on the plan's own branch, every run ends naming what comes next, /shape-slice chooses
the slice, and a skill removes a plan on a person's word. Not built: choosing which item is worked next, working out what
a plan waits on, and pausing a plan with its branch field kept true.

## What this run did besides reading

- It read the stock-take, `bi-9-inventory/inventory.md`, sections 1, 5, 6, 9, 10 and 11, and the record of the
  capability, `capabilities.md` lines 94-107.
- It read the built code and its docs, and every line it relies on held:
  - the plan tool: `core/tools/plan/README.md` (lines 1-81), `plan.py` (lines 1-309), `plan_branch.py` (lines 1-400);
  - /list-plans: `core/components/plays/list-plans/reference/ice.md` (lines 1-113), `SKILL.md` (lines 1-20, the
    steps at lines 51-58, 120-173, 212-220), `scripts/resolve_args.py`, `scripts/check_list.py` (docstring);
  - /show-plan: `core/components/plays/show-plan/reference/ice.md` (lines 1-123), `scripts/resolve_args.py`,
    `scripts/check_tree.py` (docstring);
  - /update-plan: `core/components/plays/update-plan/reference/ice.md` (lines 1-231), `SKILL.md` (lines 1-560), and
    the scripts `closed_on_github.py`, `commit_plan.py`, `check_entries.py`, `plan_ops.py`, `record_answer.py`,
    `write_plan_changes.py` (the status and direction lines);
  - the Next line: `core/components/plays/_shared/play-close.md` (lines 100-118), `core/tools/lint-play/lint_play.py`
    (lines 320-344), `core/components/loops/complete-discovery/SKILL.md` line 265;
  - /shape-slice: `core/components/plays/shape-slice/reference/ice.md` (lines 1-372), `SKILL.md` (front matter and
    lines 674-700), and `core/components/skills/author-slice/SKILL.md` (lines 3, 46-63, 173-175);
  - remove-plan: `core/components/skills/remove-plan/SKILL.md` (lines 1-58), `scripts/remove_plans.py` (docstring),
    `core/components/agents/project-orchestrator.md` lines 147 and 164; `core/components/skills/remove-model-part/SKILL.md`
    lines 50-90;
  - settings: `core/config.yaml` lines 66-71, 113-117 and 189-216;
  - ADR 049 §1-§2, ADR 051, ADR 052 §5, ADR 060, ADR 061 (lines 55-61), ADR 064 §1-§4, ADR 065 (§2, §3, lines 53-59,
    101-107, 183);
  - the plan files' top lines in `.garura/project/plans/` (their status, direction, branch and needs_plans only; no file
    under a plan's folder was opened).
- It read the approved pages it must not take from: BI-1's `turn-intents-into-work/capability.md` and
  `fn-change-work-items/feature.md` and `ice.md`; BI-8's `ship-every-change/capability.md`, `fn-commit-by-concern/`,
  `features/fn-731/feature.md`, `features/fn-673/` and `fn-land-plan-with-evidence/feature.md`; BI-3's
  `write-work-evals/capability.md` (line 91 and the lines that name /shape-slice); and the lines of other approved pages
  that hand work to Orchestration (`gather-work-under-item/fn-gather-item-tree/feature.md` lines 30, 34, 54;
  `build-work-test-first/capability.md` line 64; `build-work-test-first/fn-build-code-to-pass/feature.md` lines 25, 103;
  `install-into-project/fn-lay-guardrails/feature.md` lines 7, 19, 28, 39; `keep-spec-matched/fn-update-spec-to-match-built/feature.md` line 55).
- It read GitHub, read only: #1018, #1023, #992, #806, #729, #628, #730, #795, #1000, #1019, #855, #1005, #983, #953,
  #1007, #719, #720, #893, #819, #1014, #1035, #1033, #971 and #954 (title, state and body).
- It read memory only through the memory tool (`--issue 1021`, tier phoenix), and copied what it decided from into
  `bi-9-capability-1/memory/` with `manifest.json`: the grounding content standard and the capability and feature
  templates; the plan-view template (`standards/templates/plan-view.md`); the Next-line map
  (`standards/rules/pipeline-next.md`); and the ontology (`standards/schemas/product-os/ontology.md`, the Plan kind at
  lines 581-645 and the Slice kind at line 424). `find --glob "**/knowledge/domains/*.md" --every-tier` lists ten domain
  shelves in Phoenix memory, none on software delivery planning.
- No web research, so no memory update is drafted, and no decision trace was recorded with `memory.py cite`: the brief
  allowed writes only in this folder. No placement was run: the domain is settled at BI-9's close.
- The pages were written by hand in short-term memory, as on the earlier runs of #1021: no skill drafts pages of the
  approved shape outside the live model.

## The name

*Orchestrate agent work through planning*, id `cap-orchestrate-agent-work`, folder `orchestrate-agent-work`, as the brief
gives them. Its line, approved on 2026-11-10 (`capabilities.md` line 102): "A person chooses what is delivered next as a
slice, sees every plan and where it stands, and sets the order and status of the work as it runs."

Words the pages use, and why:
- **Plan**, **plan file**, **plan's branch**: as the ontology's Plan kind (lines 583, 587, 596), and as BI-1's page
  (`turn-intents-into-work/capability.md` line 39) and BI-8's page say them.
- **Item**: a work item in a plan's tree (epic, feature item, story, spike, chore, bug), with one of six statuses.
- **Session**: one run of /update-plan.
- **Slice**, **surface**, **tester**: as the ontology's Slice kind (line 424) and the author-slice skill (lines 46-63).
- **Next line**: the line the shared close prints (`play-close.md` lines 114-116).

## What is built, feature by feature

### 1. See every plan and where it stands (fn-729): built

- /list-plans, list mode. `plan.py` `listing()` (lines 211-252) prints one card per plan from the template's `list`
  block: the legend of directions, a heavy rule, the heading, the direction line only when set, the Status, Branch and
  Waits on rows, then each epic with Progress (done, open, and dropped when any). Items outside every epic are not shown.
- `load_plans()` (lines 63-93) refuses (exit 2) a file it cannot read, a plan with no title, a node with no issue, title
  or status, and a status, plan status or direction the template does not know. The play stops and names the file
  (list-plans ICE C6; F5).
- `resolve_args.py`: no argument is the list; `--graph` is the graph; anything else stops the play.
- `check_list.py` re-derives the view and writes `all_listed`, `in_order`, `template_used`, `as_set`, `same_twice`,
  `unchanged`, `graph_numbers_match`.
- Open: #1018 (/list-plans ends on a run summary instead of the plans).
- Stops a person with no way past: a plan file the template does not know; an unknown argument.

### 2. See every plan's branch against main (fn-806): built

- /list-plans --graph. `plan.py` `graph()` (lines 255-276): main first; each plan with a branch, its ahead and behind
  counts from `git rev-list --left-right --count`; the behind mark `⚠` when behind is not 0; one "on main" line.
- `plan_branch()` (lines 187-192): the branch the file names, else `plan/<id>/base` when git has it here or on the remote.
  A branch the file names that git does not have gives counts of `?` and no mark (lines 264-270).
- Found: the docstring (lines 21-22) says "When git is not installed, every plan shows as on main"; the code shows a plan
  whose file names a branch as on that branch even then, with counts of `?`. The page says only what the code does.

### 3. See one plan as a tree (fn-628): built

- /show-plan. `plan.py` `show()` (lines 169-184), `tree_lines()` (128-138), `finished_children()` (122-125),
  `hidden_counts()` (149-155). `resolve_args.py`: a typed number wins; with none, the branch name `plan/<id>/...`; a
  branch in no plan gets a plain message (exit 2). A number no plan has prints the no-plan line (exit 1).
- `check_tree.py` rebuilds the tree on its own and writes `lines_ok`, `hidden_ok`, `needs_ok`, `no_plan_plain`,
  `same_twice`, `unchanged`, `tree_ok`.
- #1018 says /show-plan has the same ending, "read from its steps and not seen in a run".

### 4. Set each item's status and the plan's status and direction in one approved session (fn-730): built

- /update-plan C8 (ICE lines 52-56), F7, F14. `check_entries.py` lines 124-140 (an item's status: a status the plan
  knows; Done or Dropped closes the issue; closing with open work under it, or dropping an epic, is big; an open status
  reopens a closed issue), lines 228-240 (`plan-status`, `plan-direction`). `plan_ops.py` line 19: the plan's status and
  direction write "nothing in the tracker (the plan file only)". `closed_on_github.py`: the items closed on GitHub but
  open in the plan file, Done or Dropped, never a parent. `record_answer.py`: only the plain word "approved" lands;
  "rejected" goes on; "abort" drops the list. `commit_plan.py`: one commit on the plan's branch; `Asked:`, `Override:`,
  `Owed:` lines.
- The same session holds BI-1's item changes (add, move, retitle, text, kind, new feature): `fn-change-work-items` and
  `fn-add-found-feature` own them. This page takes only `status`, `plan-status`, `plan-direction` and the
  "closed on GitHub" entries, and the parts of the session they need (the approval, the agreement, the commit).
- Stops with no way past: uncommitted work (the product owner, 2026-10-30, ICE lines 132-134). The way past that is
  built: "do it anyway" on a rule break, recorded as `Override:` in the commit.

### 5. Get onto a plan's branch for a session, and come back (fn-go-to-plan-branch): built

- `core/tools/plan/plan_branch.py` `go` (lines 157-238), `back` (lines 385-396), `abort` (lines 262-314); the stale copy
  (`drop_stale`, lines 241-254, #953); the remote call never prompts and times out (lines 66-92). /update-plan Step 3 and
  Step 13 (SKILL lines 150-166, 516-531).
- Join found: `go` holds the main-first cut of a plan with no branch (lines 186-238). The same script makes the cut for
  /start-change (README lines 63-65; docstring lines 50-51), which BI-8's Open each change where it will land (fn-731)
  holds (`features/fn-731/feature.md` line 10). So one call does both "get onto" and, for a plan with no branch, "cut".
  The page describes the cut as one path of `go` that the session calls, says the cut is BI-8's, and keeps `abort`'s undo
  of a cut the session made, because that undo is the session's own.

### 6. Know what comes next at the end of every run (fn-know-what-next): built

- The Next-line map (Phoenix memory `standards/rules/pipeline-next.md`, lines 1-95); `play-close.md` step C2 (lines
  114-116); `lint_play.py` `check_next_command()` (lines 321-344); the Discovery loop's close (`complete-discovery/SKILL.md`
  line 265). ADR 051 §1-§3.
- Out of step: the map still names /build-epic, /validate-epic, /release-epic and /release-increment (map lines 63-66),
  marked `stale: true` in their front matter and kept out of every install (`installer/install.sh` line 252); /refactor-code
  and /learn-outcomes are stale too. /fix-bug carries no stale mark. /shape-eval has `command: null` "the build stage (#819)
  is not built yet" (line 60).

### 7. Choose the slice that shows an intent is served (fn-795): built

- /shape-slice (ICE C1-C20, S1-S12), author-slice (shape, reuse, fix, edit modes). The checkpoint is pinned: "the person
  decides; never skipped by config" (SKILL line 676).
- Approved pages already give two of its parts to "the step that chooses the slice": writing an intent's page from its
  issue (`keep-spec-matched/fn-update-spec-to-match-built/feature.md` line 55) and proposing a thin ICE
  (`turn-intents-into-work/capability.md` line 44). The page takes both. It leaves out the hidden file (BI-3,
  `write-work-evals/capability.md` line 91) and the edit mode's lines of the hidden file.
- Split found: the edit mode (`--edit`, C20) is its own entry and changes a slice that exists, also one in progress.
  The page keeps it inside this feature, as the brief's list does, and the report names it.
- Stops a person with no way past: #1023 (/shape-slice must not run until the Agent-work tool lands).

### 8. Remove a plan on a person's approval (fn-remove-plan): built, not run

- `core/components/skills/remove-plan/` (SKILL.md lines 1-58; `remove_plans.py`); ADR 065 §2 (lines 133-135); listed by
  `project-orchestrator` (lines 147, 164); laid by the install (`install-garura/scripts/install.py`). No play runs it.
- Found: it refuses a plan whose `branch` is not null. Nothing writes `branch: null` when a plan pauses (ADR 061 lines
  55-61), so after a pause it refuses until a person edits the file. Today's seven plan files read `branch: null`, set by
  hand (their comments say so).

### Not built (no page, no ICE)

- Choose which item is worked next (fn-choose-next-item): approved pages hand it here (`fn-gather-item-tree/feature.md`
  line 30; `build-work-test-first/capability.md` line 64; `fn-build-code-to-pass/feature.md` lines 25 and 103). No play
  chooses; a person sets Now in a session. Practice only in `.garura/user-provided/managing-work.md` (inventory 1.8).
- Work out the plans a plan waits on from its parts' needs (fn-work-out-waits-on): the ontology says "worked out from its
  features' capabilities' needs, never set by hand" (line 600) and when (line 621); no script writes `needs_plans`; the
  views, `check_tree.py` and remove-plan read it.
- Pause a plan and start it again (fn-pause-plan): a session sets `status: Paused` (built, fn-730); landing the branch on
  main is BI-8's; nothing writes `branch: null` (ADR 061 lines 55-61; ADR 060 line 159). BI-8's page hands "Pausing a
  plan" here (`fn-land-plan-with-evidence/feature.md` line 42).

## Quotes copied from the old pages

The old pages, as they read on 2026-11-10, quoted word for word. The drafts cite this file for these quotes, so that no
draft names a removed capability or its page path.

From the old page of View plans (`capabilities/cap-719/capability.md`), line 4:
> show plans from the plan files alone — no tracker reads, no inference.

From the old page of Manage a plan with /update-plan (`capabilities/cap-720/capability.md`), line 4:
> a working session on one plan: a person gives instructions in their own words, the play checks each one against the product model, the rules for GitHub and how an epic holds its work, keeps a running list, and on a plain "approved" lands every change at once in the plan file, GitHub and the product model, on the plan's own branch. Orchestration only.

From the old page of Shape a slice (`software-delivery-planning/shape-slice/capability.md`), line 4:
> Shape the one slice that shows a business intent is served. A slice is an ordered group of features, from any capabilities, that a person can test end to end on one surface. This capability picks those features in build order, the one surface, and the person who tests it. It reads the product model and memory first, and asks the person only what neither answers. It writes the slice, its link "slice serves business intent", the slice record, the model parts the slice lacks (marked to be deepened later), and the slice's hidden file of failure and recovery conditions (decision 6 of #844). It never writes the plan, the epic, the stories or the eval: those are the work of other capabilities. It matters because every later step plans and checks this slice; a slice with no surface a person can test cannot be checked.

From the page fn-729 replaces (`features/fn-729/feature.md`), line 4:
> Print one list of every plan from the plan files: one line for each plan, with the plan's number and title, its branch, its Done count against its open count, what is Now or In Progress, and the plans it waits on (needs_plans). The marks and the layout come from the plan-view template.

From the page fn-806 replaces (`features/fn-806/feature.md`), line 14:
> - Context: serves anyone who works on plans, a person or an agent (bi-717); touches the plan files (.garura/project/plans/) and the git branches; out of scope: where a branch was cut from and where it returns to (the plan files do not hold them), and changing plans or branches (#720, #730).

From the page fn-628 replaces (`features/fn-628/feature.md`), line 9:
> - Goal: a reader coming back after two days knows where a plan stands from the tree alone.

From the page fn-730 replaces (`features/fn-730/feature.md`), line 4:
> a person opens a session on one plan with `/update-plan <id>` or a description, gives instructions in their own words, and approves; the play lands the changes in the plan file and GitHub together, on the plan's own branch. Changing an epic's or a story's text is one more instruction (#909 folded in).

From the page fn-795 replaces (`software-delivery-planning/shape-slice/fn-795/feature.md`), line 4:
> /shape-slice <intent> reads the business intent and the product model, asks the person only what the model and memory do not answer, and writes one slice into the spine with its link to the intent. It also writes the slice's hidden file (failure-and-recovery.md, one entry for each feature) in the plan's evals folder, and a thin ICE for each part the slice needs that has no ICE (ontology v11, ADR 052). It writes no plan, no epic, no story and no eval. Built in #795. Not built yet: the hidden file and the thin ICE need the play's /edit-play change (#842).

## Where the built code splits or joins the list differently

The list was not changed. These are for the product owner to decide:
1. **The step onto a plan's branch holds the cut.** `plan_branch.py go` both gets onto a branch and, for a plan with no
   branch, cuts it main first (lines 186-238). /update-plan is a second caller of that cut, besides /start-change, and
   BI-8's Open each change where it will land (fn-731) names only /start-change. fn-go-to-plan-branch says the cut is
   BI-8's and the session calls it, and keeps `abort`'s undo of the session's own cut here.
2. **/shape-slice joins more than the choice.** One run writes the intent's page when the model has none, fills the parts
   the slice needs, proposes thin ICE, writes the hidden file (BI-3) and, with `--edit`, edits a slice that exists, also
   one in progress. fn-795 takes the choice, the intent page and the thin ICE (two approved pages give those to "the step
   that chooses the slice"), the fills, and the edit of the slice's record and a part's one-line. It leaves the hidden
   file and the edit of its lines to BI-3. The edit mode could be a feature of its own.
3. **Pausing is split three ways.** Setting a plan to Paused is built inside fn-730; landing the paused plan's branch is
   built in BI-8 (fn-673); writing `branch: null` is built nowhere. fn-pause-plan is left as the unbuilt part.
4. **Items closed in the tracker.** The session's "closed on GitHub" entries are in fn-730, as the inventory's section 1.4
   has them; the stock-take's lean 5 lists "An item's status follows its own issue" as a feature of Track execution in
   the team's tracker. The tracker writes themselves (`track-plan-changes`) are left to Track execution.
5. **The Next line sits in the shared close.** fn-know-what-next takes the line and the map; the shared close that prints
   it, and the play check, are how plays are built (BI-10). The page names that edge.
6. fn-729 and fn-806 are one play, /list-plans, in two modes; kept as two features, as given.

## The Not decided lines on the drafts

- capability.md: "once agents build the work, who chooses which item is worked next: a person, the plan's direction, or
  a loop." (stock-take question 10)
- capability.md and fn-729: "whether a plan's Waits on is worked out from its parts' needs, set by a person, or dropped."
  (question 8)
- capability.md: "how the plan of a business intent is named now that intents live in their own tracker, where an
  intent's number can also be a work issue's number." (question 6)
- capability.md and fn-795: whether the pinned yes of /shape-slice (and the session's "approved") is a way past of its own
  kind, or an exception to Orchestration's Must not (#992; question 3).
- fn-go-to-plan-branch: "whether the stop on uncommitted work is a gate that needs a way past under Orchestration's Must
  not, or a stop kept on purpose (#992)."
- fn-730: "whether writing the plan's branch field as none when the plan pauses stays owed on #730 (the /update-plan
  session) or becomes its own issue." (ADR 061 line 61)

## Gaps

- **The merge of the three old capabilities will refuse as the model stands.** remove-model-part refuses while a page names
  a part being removed or its page path, and a capability folder that holds any other file (`SKILL.md` lines 76-85):
  - BI-1's approved `turn-intents-into-work/capability.md` line 72 names `cap-720`.
  - `features/fn-725/feature.md` line 54 names `cap-720`, and `features/fn-726/feature.md` line 57 names `cap-719`
    (both go to BI-11).
  - `intents/bi-788.md` line 27 links to `software-delivery-planning/shape-slice/capability.md`.
  - fn-795's page is in `software-delivery-planning/shape-slice/fn-795/`, the old slice capability's own folder, at the
    doc path the spine gives (line 918), as the brief asked. While it is there, that folder holds another file, so the
    merge refuses; the page and its ICE must move first (for example to `orchestrate-agent-work/fn-795/`).
  - fn-931 still sits under `cap-720` in the spine (line 1060); BI-1 took it, so a merge into this capability would move
    it here unless it moves to BI-1's capability first.
- **An approved BI-1 page quotes the old fn-730 page.** `fn-change-work-items/feature.md` line 55 cites
  `features/fn-730/feature.md`: "Changing an epic's or a story's text is one more instruction". The new fn-730 page does
  not hold that line, because item changes are BI-1's. When the new page replaces the old one, that quote loses its
  source; this file keeps the old line (above).
- **The structure check's detailed stage fails the approved capability shape.** `lint_grounding.py --kind capability
  --stage detailed` fails `ship-every-change/capability.md` itself, with the same five errors as this draft. The approved
  page's spine entry reads `detail: directional`, and this draft passes `--stage directional`.
- **No knowledge shelf covers running delivery work** (no tier; two waiting memory updates, mu-20261102-001 and
  mu-20261024-004, per the stock-take section 8). No built feature needed one.
- **Outside research is needed only for the three features that are not built:** how teams choose which item is worked
  next (and who may: a person, a rule of the plan, or a loop), how a plan's dependence on other plans is worked out and
  shown, and how a paused line of work is kept true and started again. None was done, by the brief.
- Found, not filed: `plan.py`'s docstring (lines 21-22) says every plan shows as on main when git is not installed; the
  code shows a plan whose file names a branch on that branch, with counts of `?`.

## Checks

Kept in `bi-9-capability-1/checks/`:
- `lint.json`: the structure check on each page. Every feature page passes `--kind feature --stage detailed`. The
  capability page fails `--stage detailed` and passes `--stage directional`, as the approved shape page does (see Gaps).
- `quotes.json`: 324 quotes, every one found word for word (whitespace collapsed) in the source it names; each quote in a
  page's body or its ICE page found in one of that page's sources. A test copy with one changed quote failed, as it
  should.
- `ice-shape.json`: nine ICE pages, each with Intent, Context and Expectation in order, one Goal, Limits and Fails if,
  the fixed Read opening, Never read, Persona and Scope, a Scenario, and a Done means checked by someone other than the
  doer; none thin; each part page reads built (or is the capability) and holds no ICE section.
- `names.json`: no draft names `cap-719`, `cap-720`, `cap-shape-slice`, their page paths, an old intent or a particular
  plan; no file here holds a home-folder or temp path or a person's name; each feature page has three examples or more,
  "How it meets the capability", a Status line, Given/When/Then criteria, owners in Out of scope and Sources; the
  capability's feature list matches the drafts, and the three features that are not built have no page.
