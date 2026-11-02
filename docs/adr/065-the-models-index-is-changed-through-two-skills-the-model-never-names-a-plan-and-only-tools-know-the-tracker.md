# ADR 065 — The Model's Index Is Changed Through Two Skills, a Person May Approve Deleting a Plan, the Model Never Names a Plan, and Only Tools Know the Tracker

**Status:** Accepted
**Date:** 2026-11-02
**Level:** framework
**Decided by:** Kapil Viren Ahuja
**Decided in:** #1021, with the skills landed in #1019
**Amends:** ADR 026 — Decision, "Containment split", the sentence "Every shared file ... is written solely by the play's deterministic keyed script", for the spine only: the spine is changed through link-model-part and remove-model-part, and plays move onto them over time. The profile and decisions/ stay with the play's script, and the rest of the split stands · ADR 044 — §2, the sentence "Outside a drive, nothing changes. A play's keyed persist script is still the only writer of shared model files". The rest of §2, the gap-closing script inside a loop, stands for now · ADR 063 — §2, "A plan that exists is changed only by /update-plan": a whole plan, with its folder, may also be deleted on a person's named approval, through remove-plan; and its words "the change reaches GitHub" now read "the tracker". §1 and §3 stand · ADR 005 — "Skill Execution Preferences": `gh` in the first row of its table, and its example "Preferred: Use gh CLI directly". A skill reaches a tracker only through the tool. The order of preference stands for everything else · ADR 064 — §1 and §4, the word only: "its own GitHub issue" and "closed on GitHub" now read as its own issue in the tracker. The rule stands
**Affects:** `core/components/memory/standards/rules/direct-model-write.md` (rule 3, and the new rule that the model never names a plan) · `core/components/agents/product-os-keeper.md` (its rule on who writes the spine) · `core/config.yaml` (its `trackers` settings, the code host's own setting and the wrong `github.owner`) · `core/tools/` (the Agent-work tool, recorded as a feature) · the parts that reach the tracker today and move onto the tool over time: `core/components/skills/platform-adapter/`, `core/components/plays/create-play/references/platform_adapter.py` and the copies stamped from it, `core/components/plays/merge-change/scripts/read_merge_state.py` and `core/components/plays/create-play/references/read_merge_state.py`, `core/components/skills/open-pr/`, `core/components/skills/merge-pr/`, `core/components/skills/track-issue/`, `core/components/skills/track-plan-changes/`, `core/components/agents/project-orchestrator.md`, `core/components/agents/code-builder.md` and `core/components/agents/repo-orchestrator.md`
**ICE impact:** This record changes no play's goal or limit by itself. (1) The product-os-keeper agent's rule on who writes the spine is widened to the two skills. (2) Each model-writing play's ICE changes through /edit-play when that play moves onto the two skills. (3) As each moves onto the tool, the agents repo-orchestrator, project-orchestrator and code-builder stop naming a tracker, and play ICE lines that name GitHub, such as /update-plan's "closed on GitHub", say the tracker. (4) "Checked by" and Context lines on model ICE that name one particular plan are reworded in the change for #1021. The ontology (read at version 15) and the ICE kind do not change.
**Business intent check:** kind — rule 4 says where the Business Intent kind is kept: in the tracker the settings name, which may be its own and not the work's. The kind's properties, links and rules in the ontology do not change. No person's business intent changes: this record adds, changes and drops none
**Related:** ADR 005, ADR 026, ADR 029, ADR 044, ADR 048, ADR 049, ADR 056, ADR 057, ADR 062, ADR 063, ADR 064, #1019, PR #1020, #1021

## Context

This record is only about how this project is built. Which business intents exist, and what the product model holds, are requirements, and the product owner changes them directly.

The product owner decided on 2026-11-02 to keep business intents in a tracker of their own, so they have their own short numbers, and to delete the hand-kept plans and rebuild them through the shaping plays. Doing that needed skills that write the model's index (the spine, `_spine.yaml`) outside a play, which the current rule does not allow. The review of PR #1020 found that the model-write rule already names those writers, with no decision behind them (findings MEM-5 and F1). ADR 044 shows how a new writer is recorded: an ADR that amends ADR 026.

The product owner also wants a team to be able to choose GitHub, GitLab, Jira or Linear as a setting, with nothing hard-coded.

Notes from the ADR keeper:

- The brief names no older ADR, so each one below was judged by reading it. A search for ADRs that say a play or a skill reaches the tracker directly found ADR 005 and the wording of ADR 063 and ADR 064.
- The business-intent check is `kind`, not `none`, because rule 4 says where the Business Intent kind is kept. No person's business intent changes.

## For the Person Who Accepts This

### Rule 1's first words, "changes only what its request names", were narrower than what remove-model-part does

- **What and where:** `core/components/skills/remove-model-part/scripts/remove_part.py` lines 233 to 242; finding F8 of the review of PR #1020
- **What is wrong, or worth knowing:** A capability merge moves the merged capability's features to the survivor, and rewrites `identified_by` and `depends_on` on every other part that named it. The request names only the two ends. The same skill also repoints a part from one business intent to another, which is a change, not a take-out; link-model-part cannot do that, because it can only add an intent (`add_intents`).
- **Why it matters:** A reader would trust the sentence and a reviewer would find it false. The review of PR #1020 already raised it.
- **What this decision does:** It widens the sentence, so it says what the script does.
- **What you decide:** Decided: the sentence is widened, as rule 1 under Decision now says.

### A third skill writes the index today, and it can remove a part with no approver's name

- **What and where:** `core/components/skills/link-model-gaps/scripts/apply_links.py`; ADR 044 §2; `core/components/memory/standards/rules/direct-model-write.md` rule 3
- **What is wrong, or worth knowing:** Inside a loop, this script writes the spine and the Touches lists, moves pages, and merges duplicates, which removes a node. Its key is an agreed gaps.json, not a person's name. The brief says two skills is the fewest that fits and rejects many skills that each write the index their own way, but it says only that plays move over, and this is a skill.
- **Why it matters:** Read strictly, rule 1 breaks on every round of a loop. Read loosely, a third writer stays, and it takes parts out without the name rule 1 asks for.
- **What this decision does:** It leaves ADR 044's exception inside a loop standing for now.
- **What you decide:** Decided: it stays for now inside a loop and folds into the two skills over time.

### The two skills cannot yet do everything the play scripts write

- **What and where:** `core/components/plays/shape-slice/scripts/persist_slice.py` and `edit_slice.py`; `core/components/plays/discover-capabilities/scripts/persist_understand.py`; `core/components/plays/discover-domains/scripts/persist_seed.py`; `core/components/plays/learn-outcomes/scripts/persist_learn.py`; the epic status scripts in `core/components/plays/build-epic/`, `validate-epic/` and `release-epic/`
- **What is wrong, or worth knowing:** link-model-part writes domain, capability and feature entries. For a slice it only adds features, because only /shape-slice shapes a slice. Neither skill writes the profile block in the spine or an epic's status. "Over time" has no date and no list. Until a play moves, its own script keeps writing.
- **Why it matters:** While plays move there are two ways to write the index, and a reviewer cannot tell a play not yet moved from a play that broke the rule.
- **What this decision does:** It amends ADR 026 for the spine only. The profile and decisions/ stay with the play's script.
- **What you decide:** Decided: a new slice, the profile and an epic's status stay with their plays until the skills grow.

### Rule 3 means one particular plan, and ten places break it today

- **What and where:** Under `.garura/product/product-os/`: `_spine.yaml` line 619; the pages cap-718 line 24, cap-719 line 10, fn-795 line 53, fn-798 line 48, fn-818 line 60, fn-628 line 14, fn-881 line 77, fn-931 line 33, fn-597 line 47
- **What is wrong, or worth knowing:** "Names a plan" means naming one particular plan. A feature whose job is plans may still describe plans and their folder (`.garura/project/plans/<plan-id>/evals/<slug>/`). These ten break it, for example "the tree for plan #717 matches its plan file" and "runs /shape-eval 788". The spine line and fn-931's line came from an /update-plan session, so the next session can write the same. Nothing checks for it. remove-model-part looks only for a part's own id.
- **Why it matters:** The rule is broken on the day it is accepted, and a stricter reading would forbid whole features about plans.
- **What this decision does:** It states the rule. It changes no page.
- **What you decide:** Decided: it means one particular plan. The ten places are fixed in the change for #1021.

### Rule 3 could reach a person's own words on one intent page

- **What and where:** `.garura/product/product-os/intents/`: the **Plan:** lines at bi-717 line 13, bi-722 line 15, bi-734 line 15 and bi-756 line 20; and bi-756 line 14, in its Proof it is met
- **What is wrong, or worth knowing:** The four **Plan:** lines name a plan file. They are not one of the kind's properties (ontology, lines 181 to 196), and author-intent-page drops such a line on a rewrite. bi-756 line 14 is different: it is a confirmed Proof line, "Garura's own model (plans #717, #722 and #734) is moved to the new shape".
- **Why it matters:** An ADR never changes a person's business intent, and applied to that Proof line rule 3 would. The guard does not catch this, because it reads only the Affects line and intent titles, so it is shown here.
- **What this decision does:** It changes none of these pages.
- **What you decide:** Decided: this falls away, because those intent pages are deleted or rewritten in that change.

### Rule 4 has no tool yet

- **What and where:** `core/tools/`; `core/config.yaml` lines 7 to 23; the parts listed under Affects
- **What is wrong, or worth knowing:** `core/tools/` holds no tracker tool. The `platform-adapter` skill, eight copies of `platform_adapter.py`, two copies of `read_merge_state.py`, the skills open-pr, merge-pr and track-issue, and the agents project-orchestrator, code-builder and repo-orchestrator all name `gh` or `glab`. Beyond them, 47 files under plays, skills and agents use the word GitHub. No script reads the new `trackers` settings yet, and they are uncommitted in the working tree. The adapter reads the older `platform:` line. The older `github.owner` says `kapilvirenahuja`, while `trackers.work.owner` and the repo address say `intent-driven-ai`. If the adapter stops being a skill, ADR 046's naming exception for `platform-adapter` is a later change, not part of this record.
- **Why it matters:** Until a part moves, it still names the tracker, and a reviewer reads that as not moved yet, not as broken. Two settings for one tracker can disagree, and on the owner they already do.
- **What this decision does:** It states the rule, with parts moving onto the tool over time. It builds no tool and moves no part.
- **What you decide:** Decided: parts move over time. The tool is the Agent-work tool, starting from the platform-adapter skill, recorded as a feature.

### Rule 4 speaks of trackers, and pull requests live on a code host

- **What and where:** `core/components/skills/platform-adapter/SKILL.md` (its 25 verbs); `core/config.yaml`
- **What is wrong, or worth knowing:** The adapter's verbs mix pull requests (view-pr, comment-pr) with issues. A team on Jira or Linear still has its pull requests on GitHub or GitLab. The `trackers` settings name where intents and agent work live, and nothing names the code host except the older `platform:` line.
- **Why it matters:** The tool's shape depends on this. Without an answer, one setting would end up meaning two things.
- **What this decision does:** It adds, under rule 4, that the code host is its own setting and the tool reads both.
- **What you decide:** Decided: the code host stays its own setting, and the tool reads both. The wrong `github.owner` is fixed as part of that feature.

### A real parent and child link between an epic and its intent would cross trackers

- **What and where:** `.garura/user-provided/managing-work.md` lines 50 and 94; `CLAUDE.md` line 146; ADR 029 §3
- **What is wrong, or worth knowing:** managing-work.md says every Epic serves its intents "as a real parent/child link in the tracker", and an unplanned epic is "that intent's sub-issue". With intents in their own tracker, that link crosses trackers. Between two platforms, such as Jira and GitHub, the keeper knows of no such link; between two GitHub repos it has not checked. The ontology does not need one: an Epic reaches its intents through its slice (the Epic kind's relationships).
- **Why it matters:** A person or play following that text tries to make a link that may fail, so it has to be proven across trackers before a team relies on it.
- **What this decision does:** It keeps the text of managing-work.md, and it leaves ADR 029 §3.
- **What you decide:** Decided: the real link stays, as the product owner asked, including across trackers.

### A bare issue number will soon mean two issues

- **What and where:** `.garura/project/issues/<issue>/`; the memory tool's `--issue`; `(#N)` in commit messages
- **What is wrong, or worth knowing:** The tracker `intent-driven-ai/garura-intents` exists and holds no issues today, so its numbers start low. The work tracker's numbers pass 1000, so low numbers such as #65 will exist in both. `(#65)` in a commit links to the work tracker. Short-term memory is one folder for each bare number, and the folders 65 and 91 already exist for work issues. /shape-slice and /shape-plan already keep theirs under their change issue, not the intent; older folders under intent numbers (606, 680, 717, 734, 788) hold past records.
- **Why it matters:** A person following a link lands on the wrong issue. A run that used an intent's number as its issue would reach a different issue's short-term memory, with no error.
- **What this decision does:** It records here how a number is written.
- **What you decide:** Decided: BI-7 means an intent and #7 means work, in text. Short-term memory folders belong to work issues only.

### Deleting a plan also deletes its evals, and rebuilding it makes a second set of stories

- **What and where:** Rule 2; `core/components/skills/remove-plan/`; ADR 057 §5; ADR 056 §2; /shape-plan
- **What is wrong, or worth knowing:** A plan's folder holds its slices' evals. ADR 057 §5 says a later run of /shape-eval never deletes a scenario, so that "a later run cannot weaken an eval"; remove-plan is not that play, so the words hold, but a rebuilt eval is a new yardstick with nothing comparing it to the old one. /shape-plan makes one story for each feature and does not reuse an open one; #1021 lists that fix as outside its change. ADR 056 §2 says a play finds an epic or a story by its plan file, so once the file is gone no play can find the ones that exist.
- **Why it matters:** Two stories for one feature, for whoever picks up the work, and a weaker eval could go unseen.
- **What this decision does:** It allows the deletion and leaves ADR 056 and ADR 057 as they are.
- **What you decide:** Decided: accepted. /shape-plan is fixed before the first rebuild.

### Agents read Phoenix memory, which still holds the old rule and has no verb `remove`

- **What and where:** Phoenix memory's copies of `direct-model-write.md` and `naming.yaml`; `core/components/memory/standards/rules/naming.yaml` line 56; findings F1, MEM-1 and MEM-2 of the review of PR #1020
- **What is wrong, or worth knowing:** A search of Phoenix memory today finds no "Outside a play" paragraph, though the source has it. So an agent reading through the memory tool still reads that only a play's script writes the index. The verb is the same: it is in the source's naming.yaml, absent from Phoenix memory and from ADR 046 §5, and the brief says it is not decided here. So remove-model-part and remove-plan fail the naming lint in a project that reads Phoenix's copy. The harness standard says a change to the naming standard is recorded as an ADR; at the brief's word, this one does not.
- **Why it matters:** An agent can act on the old rule, and a new project sees two naming errors on parts it did not write.
- **What this decision does:** It changes the rule in the source. It touches neither Phoenix memory nor the verb.
- **What you decide:** Decided: it stays as it is for now, because the verbs change next.

### The text of #1021 no longer matches this record

- **What and where:** #1021, its sections "Also in this change" and "Not in this change"
- **What is wrong, or worth knowing:** It says this record "also covers what this replaces in ADR 028", which it no longer does. It does not mention rule 3, rule 4, the `trackers` settings, a tracker tool, or intents living in their own tracker.
- **Why it matters:** #1021 is the work order, and its Done line is read back against it.
- **What this decision does:** Nothing. The keeper does not write to the tracker.
- **What you decide:** Decided: it is updated in that change.

## Decision

Four rules for how this project is built.

### 1. The model's index is changed through two skills

`link-model-part` adds or changes a part. `remove-model-part` takes a part out, with the name of the person who approved it. Each changes only what its request names, and the links that would otherwise point at nothing, stays inside the model, and lists every file it changed. Plays move onto these two skills over time, in place of writing the index with their own scripts. Today's rule, that only a play's own script writes the index, no longer holds. `link-model-gaps` stays for now inside a loop, and what the two skills can't do yet stays with its play until they can.

### 2. A person can approve deleting a plan

A plan is not only changed through `/update-plan`. A whole plan, with its folder, may be deleted on a person's named approval, through `remove-plan`.

### 3. The product model never names a plan

Plans sit outside the model and come and go, so no model page may depend on one. Naming a plan means naming one particular plan. A part about plans may still describe them.

### 4. Only tools know the tracker

Business intents and agent work each live in a tracker named in the project's settings. Tools read the settings and know how to reach the tracker. Plays, skills and sub-agents know only the tool, never the tracker. Parts move onto the tool over time. The code host is its own setting, and the tool reads both.

### What this changes in older ADRs

- **ADR 026** — amended: Decision, "Containment split", "Every shared file ... is written solely by the play's deterministic keyed script", for the spine only. The profile and `decisions/` stay with the play's script, and the rest of the split stands.
- **ADR 044** — amended: §2, "Outside a drive, nothing changes. A play's keyed persist script is still the only writer of shared model files". The rest of §2, the gap-closing script inside a loop, stands for now.
- **ADR 063** — amended: §2, "A plan that exists is changed only by /update-plan", under rule 2; and its words "the change reaches GitHub" now read "the tracker". §1 and §3 stand.
- **ADR 005** — amended: "Skill Execution Preferences", `gh` in the first row of its table and the example "Preferred: Use gh CLI directly". A skill reaches a tracker only through the tool. The order of preference stands for everything else.
- **ADR 064** — amended, the word only: §1 and §4, "its own GitHub issue" and "closed on GitHub" now read as its own issue in the tracker. The rule stands.

### What this does not change

- The five loops, the ontology and the verb `remove`: the brief leaves all three as they are, so ADR 028, ADR 045 and ADR 046 stand. The ontology's Plan kind already keeps a plan's status and branch off the model's pages, and rule 3 goes further than that in the same direction.
- No person's business intent. **ADR 031** (only a person confirms or drops one), **ADR 033** and **ADR 047** stand.
- **ADR 029 §3** — the parent and child link stays real, so its rule holds.
- **ADR 030** — an agent gathers the issue and its links; it does not say how, so the tool fits.
- **ADR 043** — the gap skills inside a loop stand.
- **ADR 048** — the Plan is a file and the thread between the two layers, which fits rule 3.
- **ADR 049** — one plan for each business intent stands, and §3's home plan is "worked out, never stored", which also fits rule 3.
- **ADR 056 and ADR 057** — both stand; the point on deleting a plan names what follows from them.
- **ADR 052, ADR 058, ADR 060, ADR 061 and ADR 062** — the hidden file, a slice in progress, a plan's branch, and `/update-plan`'s use of `link-model-part` all stand.
- **ADR 010** — its risk note names `gh issue view` for a skill that no longer exists, so nothing is left to change.
- **ADR 007, ADR 017, ADR 032, ADR 035, ADR 039, ADR 040, ADR 050, ADR 053, ADR 054, ADR 055 and ADR 059** — they share only a path or a play name with this decision. ADR 040's rule that the config's source is `core/config.yaml` also fits rule 4.

## Consequences

### Positive

- Over time the index has the fewest writers that fit, so one place holds the checks on it.
- Outside a loop, taking a part out names the person who approved it, and deleting a plan always does.
- The model does not go out of date when a plan is deleted or rebuilt.
- A team can choose its tracker as a setting, and a new tracker means changing one tool.
- Intents and agent work are kept clearly apart.

### Negative / Risks

- While plays move onto the two skills, there are two ways to write the index, and a new slice, the profile and an epic's status stay with their plays until the skills grow.
- Until `link-model-gaps` folds in, a third writer stays inside a loop, and it can remove a node with no approver's name.
- Rule 4 asks for a tool that does not exist yet, and until parts move, many of them still reach the tracker directly.
- Rule 3 is broken in ten places until the change for #1021 fixes them, and nothing checks it afterwards.
- Deleting a plan deletes its evals, and rebuilding it can make a second set of stories until `/shape-plan` is fixed.
- BI-7 and #7 are told apart only by how they are written, and nothing checks that yet.
- The real parent and child link across trackers is not proven: the keeper knows of no such link between two platforms and has not checked one between two GitHub repos.
- Agents reading through the memory tool still read the old rule until it reaches Phoenix memory, after the verbs change.
- Containment for the two skills rests on the request, the folder check and the list of changed files, not on a play's write scope.

## Alternatives Considered

- **Keep the rule that only a play's script writes the index, and invoke a play for every change** — a play is too heavy for a single index change, and the product owner wants the index changed through skills.
- **Many skills or plays that each write the index their own way** — redundant, and that is how it is today. Two skills is the fewest that fits, because taking a part out needs an approver's name and adding one does not.
- **Keep the old plans and move their items between plans** — hand-kept trees are harder to keep true than plans rebuilt by the plays.
- **Keep intents in the work repo and reserve numbers for them** — GitHub has one running number per repo, shared with pull requests, and cannot reserve any.
- **Our own short ID on top of the issue number** — the product owner chose a separate tracker, which gives real numbers and keeps intents and work clearly apart.
- **Name the tracker in plays, skills and sub-agents** — every new tracker would mean changing them all.

## Work This Creates

- After acceptance, the forward pointers on ADR 005, ADR 026, ADR 044, ADR 063 and ADR 064
- direct-model-write.md: rule 3's new wording and the rule that the model never names a plan; findings F8, MEM-6 and MEM-7; its Authority header (lines 7 to 9), which should name this ADR (finding F1)
- product-os-keeper.md: its rule on who writes the spine cites this ADR
- In the change for #1021: reword the ten places that name a plan, and update the text of #1021
- Move each model-writing play onto the two skills, through /edit-play, as the skills grow to cover a new slice, the profile and an epic's status
- Fold link-model-gaps into the two skills, over time
- Record the Agent-work tool as a feature, starting from the platform-adapter skill: it reads the tracker settings and the code host's own setting, the wrong `github.owner` is fixed with it, and plays, skills and agents move onto it over time
- Prove the real parent and child link across trackers before a team relies on it
- Fix /shape-plan so it reuses open stories, before the first rebuild
- Promote the rule to Phoenix memory after the verbs change

## References

- .garura/project/issues/_adr/20261102-030220/brief.md
- .garura/project/issues/1019/review/findings.yaml, findings MEM-1, MEM-2, MEM-5, MEM-6, MEM-7, F1 and F8
- core/components/memory/standards/rules/direct-model-write.md
- core/config.yaml
- ADR 005, ADR 026, ADR 044, ADR 056, ADR 057, ADR 063, ADR 064
