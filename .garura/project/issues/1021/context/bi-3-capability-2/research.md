# Write the evals that check the work: research and drafts (issue 1021, BI-3 capability 2)

Draft only. Nothing under `.garura/product/`, on GitHub or in git changed. The drafts are in `.garura/project/issues/1021/context/bi-3-capability-2/drafts/product-os/software-delivery-planning/write-work-evals/`: the capability page and its ICE page, and five feature pages, each with its ICE page. The name "Write the evals that check the work" is the one the approved Gather the work under a chosen plan item page already uses for this capability, so no approved line needs a new name.

What this run did besides reading:
- It copied the memory files it decided from into `bi-3-capability-2/memory/`, with `manifest.json`, all from Phoenix memory: the eval rules, the two eval templates, the step-library index and the command-line step library, the builder isolation rule, the recovery rule (`expectation-generation.md`), the ontology and the evidence-file template. Garura memory holds none of them.
- It read GitHub issues #898, #1023, #1033, #893, #912, #801, #819, #798, #828 and #978. No write.
- It did not open the eval files of the one plan that has them; it only listed the folder's name.
- It ran no placement: the domain (software delivery planning) was decided.
- The decisions made from memory are in `cite-request.json`, for the caller to record with `memory.py cite` (the tool writes outside this run's folder).
- The pages were written by hand in short-term memory, as on the earlier runs: no skill drafts pages of the approved shape outside the live model.

## What is built, and what is only planned

In one line: writing a slice's eval before the build is built and has run once; starting it from an item a person names, keeping the eval provably from the build, and running it are not built.

Built and live (installed in this repo):
- **The eval play, /shape-eval** (`core/components/plays/shape-eval/`). Started with a business intent's issue number, after /shape-plan. For each epic node of the plan file that stands for a slice, `gather_eval.py` reads the epic and its feature-to-story map and each story from the tracker, and the slice's hidden file, and copies them. The evals-engineer agent checks the copies are complete and calls author-slice-eval, which drafts one story file per story (`eval.<feature-id>.feature.md`, Markdown with Gherkin, its Feature is the story) and one slice file (`eval.<slice-id>.md`). `place_eval.py` places them and holds the yardstick; `check_eval.py` checks every format rule (up to three fix rounds); a write guard allows only the eval files; the product owner sees a summary (counts per story, untestable items), never the eval, and types yes; the copies are cleared from short-term memory. It never reads an ICE page, the usage guide, the code or the product model. It ran once (commit 36251ed6, "feat(eval): write the eval of business intent #788's slices (#798)"); #798 is closed.
- **Re-running /shape-eval** keeps every scenario word for word, adds only what is not covered, tags the story file of a feature that left the slice `@out-of-slice`, and names for a person each scenario whose story line moved or changed (C7, C16, S2, S3, S8).
- **The eval rules and templates** (`standards/rules/eval-format.md`, `standards/templates/eval-story.feature.md`, `eval-slice.md`) and **one step library**, the command line, which also covers a Claude Code play run in a test project (`standards/schemas/eval/steps-command-line.yaml`).
- **The hidden file**: /shape-slice's Step 8b, `write_hidden_file.py` (lines, write, check) with the author-failure-recovery skill, writes one entry per feature, one recovery (when, way back, who fixes) per "Fails if" line of the feature's ICE and its capability's ICE, keeps unchanged entries and ids, and shows the person the lines and counts in its brief. Known break: on today's model it finds no "Fails if" lines for the older features (#1033 item 4).
- **The read rule**: no builder, no skill that builds the software and no context sub-agent reads a plan's evals folder (CLAUDE.md, ADR 049 §4, ADR 057 §7, the ontology's Slice rules). It is a rule only; nothing on disk enforces it.
- **What a ledger check would read**: every play run's evidence names its session id and ledger file with start and end offsets (`standards/templates/evidence-file.md`; `session_stamp.py` sits in 33 play script folders).

Must not run now: /shape-eval reads the intent's issue from the wrong repo until the Agent-work tool lands (#1023). #1033 lists /shape-eval's scripts as not affected by the model-reading breaks. Findings from the eval play's review are left open (#912), among them "The whole hidden file, recovery lines included, is copied to the eval-writing skill."

Only planned:
- **Starting the eval from an item a person names.** The product owner's flow (list item 1 and 2 of 2026-11-09; the approved gather capability). /shape-eval starts from a business intent's whole plan.
- **The checks that the build was never given the eval** (fn-898, #898 open): a lint check over the build parts' inputs, and a ledger check that flags each read of the evals folder in the build run's evidence, never blocking.
- **Step libraries** for a browser page, a mobile app and a backend endpoint, "added when a slice first needs it" (`standards/schemas/eval/_index.md`). No part adds one.
- **The eval runner** (ADR 057: "The runner that runs the eval is not built yet (#819)"; #819 is closed, so the runner has no open issue). **The usage guide**, written by the build (ADR 049 §3), not built. **The handoff plan**, where it is kept "is not decided" (ADR 049). All three belong to running the eval, not to writing it.
- **Blocking a read by hook**: the old fn-898 page gives it to the guardrails (#893). #893's own text does not mention the evals folder.

Stale or dropped: author-steelman-evals (stale, /build-epic's refutation evals); author-encrypted-evals (stale; encryption dropped with #828 on 2026-10-26).

## The overlaps

### 1. With Gather the work under a chosen plan item (the first BI-3 capability)

**a. Who reads the test writer's part.** The approved gather pages split each story by script: the builder's part (title, goals, limits, Context guidance) and the test writer's part (the expectations). The approved capability page also says: "Out: writing the evals that check the work. Write the evals that check the work owns it, and it reads the work items itself."
1. **The test writer of the code-level tests (Build the work test first) reads the test writer's part; this capability reads the epic and its stories itself, from the plan file and the tracker, as /shape-eval does.** Gain: as built and as approved; the eval writer never touches what gathering hands to the build. Cost: the tracker is read twice, and two readers read the same expectations.
2. **This capability reads the test writer's part from gathering instead of the tracker.** Gain: one read, one split. Cost: the eval then waits on gathering; the approved gather line changes; the eval writer still reads the hidden file on its own, so it has two inputs from two places.
3. **Both read the test writer's part.** Gain: the outside evals and the code-level tests start from one copy. Cost: as option 2, and the two kinds of test become coupled.

Lean: 1. The drafts follow it.

**b. At what level an eval is written when the chosen item is a story, a feature item or an epic.** The ontology gives a slice one eval; ADR 057 gives each story its own file.
1. **The slice keeps one eval; a chosen item writes the story files of the stories under it, and the slice file.** An epic writes its slice's whole eval; a feature item or a story writes only its stories' files; the epic's other stories get theirs when they are chosen. Gain: matches "anything under it", the one-eval rule and the yardstick (a later run only adds). Cost: a slice's eval is whole only when every story of its epic has been chosen once.
2. **Any chosen item writes the whole eval of its slice.** Gain: the slice's eval is whole before any of its work is built. Cost: it writes evals for stories nobody chose, from outside the chosen tree.
3. **An eval for each chosen item, at its own level.** Cost: against one eval per slice; two evals of one slice can disagree.

Lean: 1. The drafts follow it. Named on the page as not decided: what is written when the chosen item is a chore, a bug or a spike (they have no goals or expectations of their own).

### 2. With Build the work test first (evals versus the code-level tests)

Decided: the code-level tests written before the code are capability 4's; this capability writes the outside checks on the surface.
1. **Two kinds of test, two owners, kept apart.** The evals: outside, on the surface, Gherkin, fixed steps, no agent, in the evals folder, written before the build. The code-level tests: inside the code, written by the build's test writer from the test writer's part and shown to fail before the code. The test writer never reads the evals; the eval writer never reads the code or its tests. Gain: matches the decided split and the ontology ("any skill that builds the software ... never reads its eval"). Cost: the same expectation is tested twice, at two levels, and the two can disagree.
2. **The code-level tests are derived from the evals.** Gain: one source for both. Cost: the build's test writer reads the evals folder, and the barrier the product owner asked for is gone.
3. **No code-level tests from the expectations; the evals stand for them.** Cost: against "all the tests for the work are written and shown to fail, then all the code".

Lean: 1. The drafts follow it. One more line drawn with no decision asked: the usage guide, which maps each name in an eval to the real command or page, is written by the build (ADR 049 §3). Not decided, and named on the page: how the build maps names it never sees.

### 3. With Code → Validation (running the evals and giving the verdict)

1. **Write here, run there.** This capability writes and keeps the evals; "Test with evals the builder never sees" (Code → Validation) runs them through the usage guide with the runner, gives the pass or fail, and writes the handoff plan from the recovery parts of the hidden file. Gain: matches ADR 049 ("The eval is read at two times"), BI-4's outcome as written, and the inventory's lean; the barrier between builder and checker becomes the line between two intents. Cost: the step library is shared by the writer here and the runner there, two owners of one format.
2. **This capability also runs the evals and gives the verdict.** Gain: one owner from writing to verdict ("check its own work"). Cost: BI-4's outcome is then served from BI-3, and the writer of a test also judges it.
3. **Code → Validation writes and runs them.** Cost: against his list item 2 for this intent.

Lean: 1. The drafts follow it. The step library stays here because the approved Manage surfaces page already gives "the step library of each kind of surface" to this capability (under its old name, Design for evaluation and testing).

### 4. With Orchestration and slicing (who writes the hidden file now that slicing leaves BI-3)

Today /shape-slice writes the hidden file when it shapes the slice (ADR 052 §1), before any plan exists. His note: "Slicing and making the plan leave this intent for wherever the plan is made (Orchestration, by his words; confirmed when Orchestration is reviewed)."
1. **This capability writes it, just before the evals, as the one reader of the "Fails if" lines.** Gain: everything in the evals folder has one owner, beside the only things that read it; slicing and planning stay free of failure lines, as he decided when he said the plan only plans (ADR 052: "First, the plan only plans: it must not write failure conditions."); the routing table already gives the failure conditions to the "Eval author". Cost: ADR 052 §1 and §4 change (the reader of the "Fails if" lines moves); the "never an ICE page" rule then holds for the eval-writing part only; built code moves out of /shape-slice.
2. **It stays with slicing, wherever slicing goes.** Gain: nothing built moves; ADR 052 stands. Cost: a capability that runs the work writes the yardstick's failure conditions, and writes them when the slice is shaped, long before the work is chosen, so an ICE change in between is drift.
3. **Turn intents into agent work writes it with the stories, from the same two ICE, as ADR 049 first said.** Gain: one reader of each ICE, at one moment. Cost: against his decision that the plan only plans, and the story writer then sees the lines it must keep out.

Lean: 1. The drafts follow it: the feature "Write what must never happen, and the way back from each" sits here, and its page names the move as not decided.

### 5. Where the checks that keep the evals from the build belong (fn-898)

His item 2 says "never shown to the builder"; the old capability held fn-898; the inventory leaned BI-4.
1. **Here.** Gain: one owner of "never shown to the builder", as his list item and the old capability have it; the check is run by someone other than the builder. Cost: it checks the build's inputs and sessions, which run in another capability.
2. **Build the work test first.** Gain: the build proves its own inputs. Cost: the doer checks itself.
3. **Code → Validation**, before the verdict. Gain: whether a pass counts is judged where the pass is given. Cost: an old part of this job moves to another intent.

Lean: 1. The drafts follow it. It overlaps the gather page's own check that the builder's part holds no expectation; that check reads one hand-off, this one reads every part that builds.

### Other neighbours (no decision asked)

- **Manage surfaces**: declares each surface and its kind; this capability reads the kind to pick the step library.
- **Design the work**: never reads the evals. Named as not decided on the keep-away page: whether design is checked the same way, since what it writes reaches the builder.
- **Turn intents into agent work**: its approved Out lines still name "Design slices" for the hidden file and "Design for evaluation and testing" for the eval; they are reworded when that capability moves to Orchestration. Not changed here.
- **#912**: the eval play's open review findings stay with the eval play.

## The persona

**The product owner**, who sees a summary of each eval, never the eval itself, types yes before anything is kept, and trusts a pass only when the build aimed at what was asked. From what is built: /shape-eval's personas are "the product owner (runs /shape-eval, reads the summary, types yes)", the eval runner later, and "the build, which is never given the eval (#898)"; #898's persona is "The product owner, who trusts an eval pass only when the build aimed at the intent."; the domain page "serves the product owner, who names the work and approves its design".

Weighed and set aside, by his split of roles ("designs are going to be done by ... a technical lead"; "The coding will be done by the developer, including the TDD"):
- **The technical lead**: names the item and designs the work. Against: what the design writes reaches the builder, so a designer who read the evals could carry tests to the build. In the drafts the technical lead names the item in the scenarios, and the product owner approves the summary.
- **The developer**: builds the code test first and must never see the evals, so cannot be the persona.

## Features found

- **Write the evals of the chosen work before it is built** (fn-write-work-evals). Built (/shape-eval), started from a business intent's plan today, not from a chosen item. Sources: /shape-eval SKILL.md and ICE (C1-C16), author-slice-eval, evals-engineer, gather_eval.py, ADR 057, ADR 049 §3-4, the eval rules and templates, his item 2, the approved gather page, commit 36251ed6; old fn-798.
- **Write what must never happen, and the way back from each** (fn-write-failure-conditions). Built in /shape-slice (write_hidden_file.py with author-failure-recovery); moving it here is the lean of overlap 4. Sources: write_hidden_file.py, author-failure-recovery, /shape-slice SKILL.md Step 8b and its brief, ADR 052, expectation-generation.md "A feature's recovery", the ontology's hidden file, #1033.
- **Update the evals as the work changes** (fn-update-evals). Built: /shape-eval run again (C7, C16, S2, S3, S8) and write_hidden_file.py's kept entries and ids. Not built: the round that remakes a story and its hidden-file entry together when an ICE changes (ADR 052 §7). Sources: /shape-eval ICE, eval-format.md "A fixed yardstick", ADR 057 §5, ADR 052 §7, write_hidden_file.py.
- **Add the steps an eval may use on a kind of surface** (fn-add-eval-steps). Not built: one library exists (command line); the others are planned "when a slice first needs it". Sources: `standards/schemas/eval/_index.md`, steps-command-line.yaml, ADR 057 (Negative / Risks), /shape-eval C12, the approved Manage surfaces page.
- **Keep the evals from the builder, and flag a build that read them** (fn-keep-evals-from-builder). Not built (#898). Sources: #898, old fn-898 with the product owner's answers Q-builders-1 and Q-flag-1, ADR 057 §7 and its risk, the ontology's Slice rule, the evidence-file template, the reference implementation's barrier section.

Candidates not drafted:
- **Run the eval and give the verdict; write the handoff plan; the runner**: Code → Validation (overlap 3).
- **Write the usage guide**: the build (ADR 049 §3).
- **Block a read of the evals folder by hook**: the guardrails (#893).
- **Steelman or encrypted evals**: stale or dropped.
- **Choose the item, gather the work, split each story**: the first BI-3 capability.

## Which old shape-eval lines carry over

From `shape-eval/capability.md` (cap-shape-eval):
- Line 4, "Write the eval that checks, from the outside, that a business intent is met on its slice's surface." Carries, as the capability's job.
- Line 4, "The eval is written before the build, from what the plan wrote: the epic, its stories and the slice's hidden file." Carries (Guiding rule "From what the work asks").
- Line 4, "It never reads an ICE page itself". Carries for writing an eval; the hidden-file feature becomes the one reader of the "Fails if" lines (overlap 4).
- Line 4, "no builder, no skill that builds the software and no context sub-agent is given that folder", and the build "is given the business intent, never the eval". Carries (Never line; keep-away feature).
- Line 4, "It matters because a builder that sees the test can build to the test, and then a pass proves nothing." Carries word for word in the Directional intent.
- Line 8, "To be deepened later: written by /shape-slice for bi-788 at the directional depth." Drops.
- ICE line 21, the Goal "Each slice has one eval that says, from the outside, if its business intent is met on the slice's surface." Carries, widened to the work under a chosen item.
- ICE lines 22-26 (read only the epic, stories and hidden file; write only in the evals folder; the three Fails if lines). Carry into the capability's ICE.
- ICE line 27, out are "running the eval, blocking a read by hook (#893)" and the later warnings; "encryption (#828) was dropped". Carries into Boundary Out lines.
- ICE line 28, "Checked by: /shape-eval run after /shape-plan writes the eval in the plan's evals folder, and no build play's inputs name that folder." Carries, reworded as two Done means checked by someone other than the doer.

From `shape-eval/fn-798/feature.md`:
- Line 4, "/shape-eval <intent> runs after /shape-plan, on its own" and "Not built yet (#798)". Do not carry: it is built, and the start moves to a chosen item.
- Inputs lines 9-11 (the epic with its feature-to-story map, the stories, the hidden file; one eval in the evals folder). Carry.
- Line 12, the handoff plan as an output. Moves to Code → Validation.
- Line 13, "Thin: the format of the eval and of the handoff plan is not set yet." Drops: ADR 057 set the format.
- Rules lines 16-21: "It reads only the epic, its stories and the hidden file", "The eval checks from the outside, on the slice's surface. For Garura that surface is often a play, so the eval runs the play on a test project", "The running eval reaches the slice only through its usage guide", "When the eval cannot test a goal, an expectation or a failure condition yet, it says so", "The eval stays in plain text in the repo." All carry (the play line made general).
- Acceptance criteria lines 24-25. Carry, reworded.
- Out of scope lines 28-31. "Running the eval after the build" and encryption carry; "The slice, the hidden file, the plan, the epic and the stories" carries except the hidden file (overlap 4).
- ICE lines 41-48. Goal, limits and Fails if carry into fn-write-work-evals' ICE; "Checked by: the product owner runs /shape-eval 788 ..." drops (it names a plan).

From `shape-eval/fn-898/feature.md`:
- Line 4 (the build is given the intent through the stories; the lint check; the ledger check that flags and does not stop; nothing is hidden). Carries whole.
- Inputs / Outputs lines 9-12. Carry. Line 13, "Thin: the shape of a flag in the evidence file is not set yet." Carries as a detail left to the build of the check.
- Rules lines 16-21. Carry, with one change: "Only /shape-slice (which writes the hidden file into the evals folder), /shape-eval and the eval itself may name the evals folder" becomes "only the parts that write the evals and the hidden file, and the eval when it runs".
- Line 22, what the ledger check does with no ledger. Carries as not decided.
- Acceptance criteria lines 25-27. Carry.
- Out of scope lines 30-34. Carry, with "Writing the stories that the build is given: /shape-plan writes them (fn-818)" pointing to Turn intents into agent work.
- ICE lines 46-53. Carry into fn-keep-evals-from-builder's thin ICE (two Goals merged into one).

## Gaps that matter, named on the pages as not built or not decided

- Nothing writes the evals from an item a person names.
- Nothing runs an eval: no runner, no usage guide. The evals are written and never run.
- Only the command-line step library exists.
- Nothing checks that the build was not given the evals, or flags a read (#898). Only the read rule holds.
- The hidden file finds no "Fails if" lines for older features on today's model (#1033), and who writes it now is open (overlap 4).
- No round remakes a story and its hidden-file entry together when an ICE changes.
- Not decided: what happens to a scenario a person judges no longer fits; how the build maps the eval's names it never sees; what is written for a chosen chore, bug or spike; whether design is held to the same rule; how a build that starts before its eval is shown to a person (no gate stops it).
- The plays that read the plan must not run until #1023 lands.

## Assumptions

- The test writer in the gather pages' split is the build's test writer of the code-level tests (capability 4), not this capability.
- The step library stays here, as the approved Manage surfaces page says, though the runner that does the steps sits in Code → Validation.
- A library lives in memory (Phoenix memory today), so adding or growing one is a memory update a person approves.
- The ICE of the three built features and of the capability carry no thin mark, because their job is built; the two features that are not built carry it. The capability's ICE has five Limits and four Fails if; the thin limit of three does not apply to it.

## Checks

- **Structure check** (`lint_grounding.py`): the capability page (`--kind capability --stage directional`) and the five feature pages (`--kind feature`): ok, no errors, no warnings.
- **ICE shape check** (a small script in the session's scratch folder): all six ICE pages hold Intent, Context and Expectation in order, exactly one Goal, at least one Limit and one Fails if, the fixed Read line, the Context labels in order (Read, Never read, Persona, Scope), a Scenario, and a Done means checked by someone other than the doer. The two thin pages open with the thin mark and hold three Limits and three Fails if each; the four others carry no thin mark. No part page holds an ICE section.
- **Quotes**: 159 quotes in the six Sources sections, each found word for word (spaces normalised) in its file: memory quotes against this run's copies in `memory/`, the product owner's words against `capabilities.md` and `bi-3-capability-1b/page-approvals.md`, GitHub quotes against the issue texts read today, the commit message against git. Every quote in a page body is also in that page's Sources, apart from the label "Fails if".
- **Words**: no page says lens, seed, lock or gate, names a real person, a home-folder path or a particular plan.

## Addendum, round 2 (2026-11-09): the two writing features merged

The product owner's reply is in `page-approvals.md`: "continue", read as a yes to the six leans and to merging the first two features. The round 1 drafts are kept as they were in `drafts-round-1/`. The redraft is in `drafts/product-os/software-delivery-planning/write-work-evals/`.

Why the merge: the list of what must never happen is written from the same work, at the same moment, as the evals, and each of its lines becomes a scenario in the eval.

What changed, page by page:
- **fn-write-work-evals, page and ICE (merged).** The feature is now "Write the evals of the chosen work, with what must never happen, before it is built". It keeps the folder `fn-write-work-evals`. It carries every rule, acceptance criterion and source of both round 1 pages that still holds:
  - What it does: first the hidden-file entry of each feature under the chosen item, then the story files and the slice file. The product owner sees the "Fails if" lines with their counts and the summary of the evals, never the evals.
  - Status: built in two plays, the eval play and the slice play. Writing the hidden file here changes ADR 052, as the approved lean says.
  - Rules: all of both pages, plus one new rule, "The hidden file first, then the evals, at the same moment", with its reason. The rule on a chosen feature item or story now covers the hidden-file entries too, by the approved lean ("a chosen feature or story writes only the test files under it").
  - Two "Not decided" lines of the hidden-file page are gone, because the product owner's yes settles them: who writes the hidden file (here, just before the evals), and when the slice's other features get their entries (when their stories are chosen).
  - Acceptance criteria: the 5 of the hidden-file page and the 6 of the eval page, 11 in all, with "to write the evals" added to the last, because the hidden-file part does read the "Fails if" lines.
  - Out of scope: the two "changing later" lines are merged, and so are the two "running and handoff" lines. The line that pointed to the removed feature is gone.
  - Sources: both lists without repeats, plus the product owner's yes in `page-approvals.md`.
  - ICE: one Goal, which covers the entries and the evals. It has 6 Limits and 7 Fails if, not thin, and two Done means, one for the entries and one for the evals. Its Scenario is the shop's card example, with the entry and the story file together.
- **fn-write-failure-conditions**: deleted from `drafts/`; still in `drafts-round-1/`.
- **The capability page**: the two feature lines in its Features list are now one line for the merged feature. Every other line is word for word as in round 1.
- **The capability's ICE page**: no change.
- **fn-update-evals page**: its two Out of scope lines that named the first evals and the first hidden-file entry are now one line, pointing to the merged feature. Every other line is word for word; its ICE page is unchanged.
- **fn-add-eval-steps page**: its one Out of scope line now uses the merged feature's name. Every other line is word for word; its ICE page is unchanged.
- **fn-keep-evals-from-builder**: no change.

Checks, round 2:
- **Structure check:** the capability page (directional) and all four feature pages are ok, with no errors and no warnings.
- **ICE shape check:** all five ICE pages pass: one Goal each, the fixed Read line, the Context labels in order, a Scenario, and a Done means checked by someone other than the doer. The two thin pages carry the thin mark with 3 Limits and 3 Fails if each. The three others carry no thin mark. No part page holds an ICE section.
- **Quotes:** all 162 quotes in the five Sources sections are found word for word in their files. Every quote in a page body is also in that page's Sources, apart from the label "Fails if".
- **Words:** no page has lens, seed, lock or gate, a real name, a home-folder path or a plan id.
- **Against round 1:** a diff shows changes only in the merged feature's two pages, the capability's Features list, one Out of scope line on each of fn-update-evals and fn-add-eval-steps, and the deleted folder.
