# ADR 068 — Each Product Feature Has One Feature Issue That Names It and Holds Its Scope of Work, and No Feature in the Model Carries an Issue Number

**Status:** Accepted — amended in part by [ADR 069](069-the-plan-is-where-the-product-model-meets-the-work.md): Decision §1, last sentence, 'The business intent pages keep their Tracker line': the Business Intent kind loses the Tracker line, through /specify-ontology. 'every id stays as it is (for example bi-1 and fn-724)' stands: the ids stay as names (settled at acceptance). §2 to §6 stand; 'a second epic' in §4 now means another plan's epic; and amended in part by [ADR 070](070-each-feature-in-the-product-model-records-its-own-state.md): Decision §5, "When a feature is built (its Feature issue is closed)": a feature is built when its state in the model is Completed. It becomes Completed when its Feature issue closes as completed, and once, through the clean-up the person confirms, for a feature built before ADR 068. "Closing a Feature issue is a person's call, made through /reshape-plan finish", "every slice and plan that holds it counts it as complete" and "no roll-up, ADR 064 stands" stand. Also its ICE impact for /design-slice C6 and C7, "it reads each feature's Feature issue state through the tracker tool": it reads the feature's state from the model. §4's rule stands, and a Dropped feature is also left out. §1 to §4 and §6 stand.
**Date:** 2026-11-12
**Level:** framework
**Decided by:** Kapil Viren Ahuja · **Decided in:** #1051 (a Chore under #1025, "/shape-plan reuses an open story for a feature instead of filing a second one"), from checkpoint 1 of the ontology change for #1050
**Supersedes:** ADR 067 (in full — a play finds a feature's story by the `issue` that the feature's entry in the product model names, when no plan file marks it)
**Amends:** ADR 056 — Decision §1: the plan play also files one issue of type Feature for each product feature (a Feature issue), and a Story always sits inside a Feature issue; "An Epic is never filed as type Feature" stands; and Decision §2: when the plan file marks none, a play finds a feature's work by the issue of type Feature whose text carries the exact line `Represents: <feature id>`, never by its title; an epic is still found only by the plan file · ADR 048 — Decision §1, second bullet (the work layer is Epic, Feature, Story, Spike, Chore and Bug) and third bullet ("Domain, Capability, Feature, Slice, Source and ICE are never tracker issues. In the tracker, a Story stands for a Feature": a product feature now has exactly one Feature issue); Decision §3, first bullet ("It holds stories": an Epic holds Feature issues, with the Stories inside them) and second bullet in full ("A Story represents one feature and delivers it. There is one story for each feature in each epic. When a story is made, it writes its own scope of work from its feature's ICE and its capability's ICE": the Feature issue represents the feature, one in the whole tracker, and holds the scope of work written from those two ICE; a Story is a piece of work inside it); Consequences, Negative / Risks, "One story per feature in each epic means one feature can have several stories across epics"; Alternatives Considered, the Feature half of "Make Capability and Feature tracker issues too". The rest of ADR 048 stands · ADR 049 — Decision §1.2, the words "one story for each feature of the slice": the plan play finds or files one Feature issue for each feature of the slice that is not yet built, with the Stories inside it; and Decision §4, each place where the story holds or gives the scope of work and the Context guidance (the second bullet, "The story holds the goal, the limits and the expectations in its scope of work, and the Context guidance"; the third bullet, "the story's Context guidance" and "The builder reads the story"; the fifth bullet, the eval play "reads the epic, its stories and the hidden file"; and "When an ICE changes after its story is made, the story and its hidden-file entry are drift"): each now reads the Feature issue. The rest of ADR 049 stands · ADR 052 — Decision §3 ("The epic keeps the map from each feature to its story", and the eval play joins each hidden-file entry "to its story": the map names each feature's Feature issue, one line for each feature), §4 (the words "writes the story's scope of work and Context guidance": the Feature issue's) and §7 ("after its story and its hidden-file entry are made" and "the plan play makes the story again": the Feature issue). The rest of ADR 052 stands · ADR 057 — Decision §2 ("one story file for each story of the slice's epic: `eval.<feature-id>.feature.md`", its Gherkin `Feature:` "is the story", a scenario for each goal and expectation "of the story": one file for each Feature issue in the slice's epic, still named by feature id; its `Feature:` is the Feature issue), §3 ("the stories, in the order of the epic's feature-to-story map" and "the stories' Context guidance": the Feature issues) and §6 ("the counts for each story": for each Feature issue). The rest of ADR 057 stands
**Affects:** Through /specify-ontology (#1050): `core/components/memory/standards/schemas/product-os/ontology.md` (version 15: the flow line, line 11; the tracker paragraph, line 21; the answers at lines 30, 48, 84, 87 (Q20), 93, 96 and 156; the Feature kind, lines 384, 403 and 411; the Plan kind, lines 597, 598 and 624 to 626; the Epic kind and its feature-to-story map, lines 648 and 663; the Story kind, lines 697, 711, 712 and 713 (its scope of work and Context guidance move to the Feature issue) and 739) and `core/components/memory/standards/schemas/product-os/spine.yaml` (the `features` entry, lines 103 to 121, stays without `issue`; the `epics` entry's `issue_ref`, line 223, is not a feature and does not change) · On PR #1047's branch (`feature/1025-shape-plan-reuses-open-story`): `core/components/plays/shape-plan/reference/ice.md` and `SKILL.md`, through /fix-play; `core/components/plays/shape-plan/scripts/find_work_items.py`, `gather_plan.py`, `render_brief.py`, `write_work_items.py`, `check_drafts.py`, `check_plan.py` and `check_tracker.py`, with their tests · `core/components/skills/author-work-items/SKILL.md` (lines 3, 11, 41 and 42; Story mode, lines 63 to 66) · `core/components/plays/design-eval/` (`reference/ice.md` C1, C2, C3, C5, C8, C9, C16, F3, F4, F14 and F16; `scripts/gather_eval.py` lines 10, 11, 22 and 106 to 134; `scripts/place_eval.py` lines 9 and 10; `scripts/eval_common.py`; their tests), `core/components/skills/author-slice-eval/SKILL.md`, and the templates `core/components/memory/standards/templates/eval-story.feature.md` and `eval-slice.md` · `core/components/plays/reshape-plan/` (`SKILL.md` Step 9, the name-story dispatch, lines 403 to 420; `reference/ice.md` C11, C14, F10, S10, S11; `scripts/check_agreement.py` lines 23 and 149; `scripts/place_feature.py` lines 9, 10, 20 and 73; `scripts/feature_ice.py`) · `core/components/skills/link-model-part/` (`SKILL.md`, its description; `scripts/link_part.py` lines 21, 24, 40, 340 and 341, 432 to 435; its tests) · `core/components/agents/product-os-keeper.md` (line 74) · `core/components/skills/author-plan-changes/SKILL.md` (line 42) · `core/components/plays/design-slice/` (C6, C7) and `core/components/skills/author-slice/` · Garura's model, `.garura/product/product-os/_spine.yaml` (the 23 `issue` values on features fn-724 to fn-931, lines 737 to 1203, deleted only after the clean-up) · The tracker, through the clean-up: the 33 open issues of type Feature, and a Feature issue for each of the 23 features · `CLAUDE.md` (Work Tracking), `.garura/user-provided/managing-work.md` (lines 38 and 61), `core/grounding/glossary.md` (lines 63, 64 and 72) · Read, not changed: `core/components/skills/enrich-grounding/` (it writes no `issue`), `core/components/skills/platform-adapter/` (its `list-issues` and `create-issue-typed` verbs exist), `core/components/skills/author-intent-page/` (the intent pages keep their Tracker line)
**ICE impact:** /shape-plan, on PR #1047's branch, through /fix-play: C3 (a feature's work is found by the plan file's mark; when none, through the tracker tool, by the issue of type Feature whose text carries the exact line `Represents: <feature id>`; two such issues for one feature stop the run and go to the person; never by title; never a second Feature issue or Story; one Feature issue is filed for each feature not yet built, under the slice's epic, holding the feature's scope of work and Context guidance; when the Feature issue sits under another epic, the play asks the person which epic it goes under), C13 (three types: Epic, Feature and Story; the epic's map names Feature issues), F14 and REC14 (the failure is a second Feature issue or Story for one feature, a match by title, by a line that is not exact or on an issue not of type Feature, a duplicate not taken to the person, or a move to a second epic with no question), S10 and S11 (S11: a closed Feature issue means the feature is built), D1 (each feature of each slice has exactly one Feature issue); its reads of the model's `issue` go. author-work-items writes each feature's Feature issue (its title, scope of work and Context guidance) where it wrote a story, in plan mode and in story mode. /design-eval, through /fix-play: C1, C2, C3, C5, C8, C9, C16, F3, F4, F14 and F16 read the Feature issue where they read the story: one eval file for each Feature issue in the epic's map, still named by feature id; author-slice-eval follows. /reshape-plan, through /fix-play: C11 and F10 (a new feature lands with its thin page and its model entry, with no issue on the entry, and with a Feature issue that names it and holds its scope of work), C14 (a story for a feature in the model goes inside its Feature issue), S10 and S11 ("find #N in the model" reads the Feature issue's exact Represents line); "finish" on a Feature issue is the one way a feature becomes built; its Step 9 name-story dispatch goes. /design-slice: C6 and C7 (a slice pulls in only features that are not yet built; to know that, it reads each feature's Feature issue state through the tracker tool). Skills: link-model-part stops writing `issue` (a request that names one is refused), and the product-os-keeper agent's table says so; author-plan-changes's new-feature entry no longer carries a story for the model. The build play's context sub-agent, when it is rebuilt (#855, #819), reads the Context guidance from the Feature issue. No capability or feature ICE of the product changes, and the ICE kind does not change. The ontology is not an agent intent; its change follows through /specify-ontology (#1050)
**Business intent check:** none — no person's business intent is added, changed or dropped, and the Business Intent kind does not change. Part 1 names features only: the intent pages keep their Tracker line, and every id stays (bi-1, fn-724). The plan rebuild for business intent 1 waits on this record, but its page is not touched
**Related:** ADR 048, ADR 049, ADR 052, ADR 056, ADR 057, ADR 062, ADR 063, ADR 064, ADR 065, ADR 067, #1025, PR #1047, #1048, #1050, #1051

## Context

ADR 067 was accepted earlier on 2026-11-12. It put the link between a feature and its work in the product model: a feature's `issue` named the Story filed for it, and when no plan file marked the story, a play found it by that `issue`. /shape-plan's fix for #1025 (PR #1047) was built on that rule.

At checkpoint 1 of the ontology change (#1050), the product owner corrected the model:

- A link that is held on both sides drifts and costs upkeep. So the issue alone carries the link, and no feature in the model holds an issue number.
- Each unit of work is one issue, never two.
- Slices and plans only group features.

At the accept checkpoint of this record, the product owner made six changes ("change 1-6"). Part 1 now names features only. The Feature issue holds the feature's scope of work. A person closes a Feature issue. A play matches only an exact line on an issue of type Feature. And one clean-up comes before the 23 model values are deleted.

PR #1047 and the plan rebuild for business intent 1 wait on this rule.

What exists today (read on 2026-11-12):

- Garura's model has 239 features. 23 of them hold an `issue`, and each matches its own id (fn-724 names #724). The spine has no slices, and there are no plan files.
- The ontology (version 15) and the spine schema have no `issue` on a feature. ADR 067's change to them has not landed.
- The tracker holds 64 issues of type Feature, 33 of them open. None has a `Represents:` line. The ontology calls each such issue a feature item: a group of stories inside an epic that stands for nothing in the model. For example, #723 holds the stories of four features (#724, #725, #726 and #597), so the clean-up cannot map it to one feature; it is retyped. The 31 closed ones are never matched, because a play matches only the exact line.

Notes from the ADR keeper:

- The brief names only ADR 067. The keeper also marks ADR 056 §1 and §2, ADR 048 §1 and §3 (with one line each under Consequences and Alternatives) and ADR 049 §1.2 as amended in part. Each says that a feature is not an issue, or that a feature gets one story in each epic.
- Change 2 at acceptance (the Feature issue holds the scope of work and the Context guidance; the epic's map names Feature issues) amends three more ADRs in part. ADR 049 §4 says the story holds them. ADR 052 §3, §4 and §7 say the epic maps each feature to its story, and the plan play writes and remakes the story. ADR 057 §2, §3 and §6 give one eval file for each story. It also widens the ADR 048 §3 amendment to the second bullet's last sentence (a story writes its scope of work from two ICE).
- ADR 067's forward pointer on ADR 049 names "§2, the words 'one story for each feature of the slice'". Those words are in §1.2. The new pointer names §1.2. The old pointer stays, because an accepted ADR gains only pointers.
- ADR 064 is not amended, by the product owner's words at acceptance: "No roll-up (ADR 064 stands)". Part 5 agrees with its §1 (an item's status follows its own issue). Its §3 still holds: at a merge, merge-change sets Done the item whose issue landed, which is a Story, not its Feature issue.
- ADR 062 is not amended. Its Decision does not rule that /reshape-plan writes a feature's `issue`; that write is the play's Step 9, named only in one of its points for the accepter. Its §1 still holds when Step 9 goes: the guard runs after the last model write, which is then Step 8.
- ADR 065 is not amended. This decision goes further in the direction of its rule 3 (the model never names a plan) and its rule 4 (only tools know the tracker): a play finds a Feature issue through the tracker tool.
- ADR 063 is not amended: /reshape-plan still changes a plan that exists, and its "finish" is how a person closes a Feature issue. ADR 058, ADR 060 and ADR 061 do not change.
- No ADR records the feature item. It came from ontology version 14 (#720). Under this decision it goes: the clean-up maps or retypes each open one, and the ontology change (#1050) removes it.

## For the Person Who Accepts This

The changes at acceptance settle seven of the ten points the first draft raised: how far part 1 reaches, the 64 issues of type Feature, the 23 stories, where the scope of work lives, the eval's file names, who closes a Feature issue, and a search that finds the wrong issue. Three points stay open.

### A slice may not pull in a built feature, even when its end-to-end test needs that feature

- **What and where:** Part 4 of the decision ("A slice pulls in only features that are not yet built"). The ontology's Slice kind (line 424: features "that together give one vertical outcome a person can test end to end"); its Story kind (line 697: "when a later Slice includes a Feature again, that Slice's Epic gets its own Story"); /design-slice C2 (the run reads the product model and memory first) and C6.
- **What is wrong, or worth knowing:** A new slice whose surface needs a feature that is already built must leave that feature out. Its build order, its hidden file and its eval then do not name it. To know which features are built, /design-slice must also read the state of each feature's Feature issue from the tracker, through the tracker tool. Today it reads only the model and memory.
- **Why it matters:** A slice can pass its eval while a built feature it relies on is broken, and the person who tests the slice end to end meets a step the slice does not list.
- **What this decision does:** It keeps built features out of a slice, and lists /design-slice C6 and C7 as changed.
- **What you decide:** Whether a built feature stays out entirely, or a slice may list it as "relies on, already built", with no new work item, so that its eval still covers it.

### Two plans can hold one feature, but its Feature issue sits under one epic, and the plan check wants each item under its tracker parent

- **What and where:** Part 4 of the decision ("A Feature issue sits under one epic at a time"). /reshape-plan's agreement check, `core/components/plays/reshape-plan/scripts/check_agreement.py` ("the item's parent in the plan file is its parent in the tracker"); the Epic kind's feature-to-story map (ontology line 663), which now names Feature issues.
- **What is wrong, or worth knowing:** Plan B can hold a feature whose Feature issue sits under plan A's epic. Plan B's file cannot put that item under its own epic without failing the check. If the person moves the Feature issue to plan B's epic, plan A's tree and its epic's map name an item that is no longer under them, and nothing in a plan A session says so.
- **Why it matters:** Plan A loses work with no error, or plan B shows work it does not hold.
- **What this decision does:** It asks the person which epic, before the move. It says nothing about the other plan's file.
- **What you decide:** How plan B shows a feature whose Feature issue sits under another plan's epic, and whether a move updates the plan it leaves.

### PR #1047 is built on the record this one supersedes

- **What and where:** PR #1047, branch `feature/1025-shape-plan-reuses-open-story`: `core/components/plays/shape-plan/reference/ice.md` (C3 lines 21 to 31, C13 line 53, F14 line 88, S10 line 148, D1 line 158, REC14 line 198), `scripts/find_work_items.py`, `scripts/gather_plan.py`, `scripts/render_brief.py`, their tests and `scripts/test_support.py`.
- **What is wrong, or worth knowing:** C3 on that branch says "the feature's story is the issue that the feature's entry in the product model names (its `issue`)", and the scripts read that field. Under this decision the field is gone. The play must instead find (type Feature, exact `Represents:` line) or file a Feature issue for each feature, write the scope of work and the Context guidance on it, stop on a duplicate, and ask when a second epic holds it.
- **Why it matters:** If the PR lands as it is, /shape-plan reads a field the model no longer has, and finds nothing.
- **What this decision does:** It names the parts to change in its ICE impact. It changes nothing in the PR.
- **What you decide:** Whether PR #1047 is changed through /fix-play to match before it lands, or closed and the work done again.

## Decision

One tracker issue for each product feature, linked one way: from the issue to the product model.

### 1. No feature carries a tracker issue number

No feature in the product model carries a tracker issue number. The `issue` field on features is removed, and the 23 values now in Garura's model are deleted, after the clean-up below. No play or skill writes it again. The business intent pages keep their Tracker line, and every id stays as it is (for example bi-1 and fn-724).

### 2. Three units of work

In the tracker there are three units of work: Epic, Feature and Story.

- Each product feature has exactly one Feature issue. The Feature issue names its feature in its text (`Represents: <feature id>`), so the link runs one way, from the issue to the model.
- The Feature issue holds the feature's scope of work and its Context guidance, written from its ICE.
- Stories are the pieces of work inside it. A Story always sits inside a Feature issue.
- The epic's feature-to-story map names Feature issues, one line for each feature.
- Bug, Chore and Spike stay as they are today.

### 3. How a play finds a feature's issue

A play finds it by the plan file's mark. When the plan file marks none, the play searches the tracker, through the tracker tool. A match counts only when the issue is of type Feature and its text carries the exact line `Represents: <feature id>`. Two Feature issues that name one feature are a duplicate: the run stops and asks the person. A play never finds an issue by its title. It never makes a second issue for one feature or one story.

### 4. Slices and plans are groups

Slices and plans are many-to-many with features: two slices, or two plans, can hold the same feature. A slice pulls in only features that are not yet built. A Feature issue sits under one epic at a time. When a second epic needs it, the play asks the person which epic it goes under.

### 5. A built feature

When a feature is built (its Feature issue is closed), every slice and plan that holds it counts it as complete. Closing a Feature issue is a person's call, made through /reshape-plan "finish". Nothing closes it because its Stories closed: there is no roll-up, and ADR 064 stands.

### 6. An orphan Story

A Story with no Feature issue as its parent is matched to its feature by researching the product model. When no feature exists yet, the feature is created and its Feature issue is filed.

### What this changes in older ADRs

- **ADR 067** — superseded in full. Its parts that live on are stated here in a new form: never by title (part 3), and a closed issue means the feature is built (part 5, now on the Feature issue, not the Story). Its stops for an issue named for two features and for a feature in two slices of one plan go. A second epic now asks the person (part 4), and two Feature issues for one feature stop the run (part 3).
- **ADR 056 §1** — amended: the plan play also files a Feature issue, of type Feature, for each product feature, and a Story sits inside it. "An Epic is never filed as type Feature" stands. This record does not decide whether a Feature issue carries a label.
- **ADR 056 §2** — amended: when the plan file marks none, a play finds a feature's work by the issue of type Feature that carries the exact `Represents:` line, never by its title. An epic is still found only by the plan file.
- **ADR 048 §1, second and third bullets** — amended: the work layer is Epic, Feature, Story, Spike, Chore and Bug, and a product feature has exactly one Feature issue. Domain, Capability, Slice, Source and ICE are still never tracker issues.
- **ADR 048 §3, first and second bullets** — amended: an Epic holds Feature issues, with the Stories inside them. The Feature issue represents the feature, one in the whole tracker, not one in each epic, and it holds the scope of work written from the feature's ICE and its capability's ICE. A Story is a piece of work inside it.
- **ADR 048, Consequences and Alternatives** — the risk "one feature can have several stories across epics" no longer holds, and the Feature half of the lost option "Make Capability and Feature tracker issues too" is now chosen.
- **ADR 049 §1.2** — amended: "one story for each feature of the slice" now reads as one Feature issue for each feature of the slice that is not yet built, found or filed once, with its Stories inside it.
- **ADR 049 §4** — amended: the Feature issue, not the story, holds the goal, the limits, the expectations and the Context guidance. The context sub-agent reads the Feature issue's Context guidance, the eval play reads the epic and its Feature issues, and a changed ICE makes the Feature issue drift. The rest of §4 stands: no failure or recovery condition reaches the builder.
- **ADR 052 §3, §4 and §7** — amended: the epic's map names each feature's Feature issue; the plan play writes the Feature issue's scope of work and Context guidance; when an ICE changes, the plan play makes the Feature issue again. Each line of an ICE still has one reader.
- **ADR 057 §2, §3 and §6** — amended: the eval has one file for each Feature issue in the slice's epic, still named `eval.<feature-id>.feature.md`, and its Gherkin `Feature:` is the Feature issue. The slice file lists the Feature issues in the map's order, with their Context guidance. The summary gives the counts for each Feature issue.

## Consequences

### Positive

- There is one place to look for a feature's work: its Feature issue.
- A feature's scope of work is in one issue, so the builder and the eval read the same scope, and one eval file belongs to one feature.
- The link has one side to keep. The model and the tracker cannot disagree on it, because the model does not hold it.
- A feature never gets a second issue when a second slice or plan holds it, so no one must sort out duplicates. A duplicate that already exists stops the run and goes to the person.
- A renamed issue is still found, because no play matches by title.
- The tracker type Feature now means the same thing as the Feature kind of the model.

### Negative / Risks

- Finding a feature's work now needs a tracker search, through the tracker tool. An issue whose `Represents:` line is mistyped is not found, and the play files a second one.
- The clean-up must come before the 23 values are deleted. If the order slips, those 23 stories lose their only link, and part 6 must match them again.
- The scope of work moves from the Story to the Feature issue, so /shape-plan, author-work-items, /reshape-plan, /design-eval, author-slice-eval and the eval templates all change before the next plan is made.
- A slice may not pull in a built feature, so its eval does not cover a built feature its surface relies on.
- A feature whose Stories are all done still counts as not built until a person finishes its Feature issue in /reshape-plan. Until then a new slice can pull it in again.
- A feature held by two plans sits under one epic, so one plan's tree cannot show it under its own epic, and a move can leave the other plan out of date.
- PR #1047 rests on ADR 067 and must change before it lands.

## Alternatives Considered

- **ADR 067: the model holds the feature's story issue** — lost: the link has two sides to keep in step, and the model drifts from the tracker. The product owner prefers no two-way links.
- **One Story for each feature in each epic (the older rule in ADR 048 and ADR 049)** — lost: it files a second issue for the same feature whenever a second slice holds it.
- **Match an issue by its title** — lost: titles change, so a renamed issue would be filed again.

## Work This Creates

- After acceptance: ADR 067 set to superseded, with its pointer; forward pointers on ADR 056 (§1 and §2), ADR 048 (§1, §3, Consequences and Alternatives), ADR 049 (§1.2 and §4), ADR 052 (§3, §4 and §7) and ADR 057 (§2, §3 and §6); the ADR index rebuilt.
- One clean-up, done before the 23 model values are deleted:
  - map each open issue of type Feature (33 today) to its product feature by adding the `Represents: <feature id>` line, or retype it;
  - file or link a Feature issue for each of the 23 features whose stories would lose their only link (fn-724, fn-597, fn-725, fn-726, and fn-731 to fn-931), with its Story inside it.
- Then remove the 23 `issue` values from Garura's spine.
- /specify-ontology (#1050): the Feature, Story, Epic and Plan kinds, the tracker paragraph and Q20, as listed in Affects. The scope of work and the Context guidance move from the Story kind to the Feature issue, and the feature item goes. The Feature kind does not gain `issue`.
- PR #1047, through /fix-play on /shape-plan: C3, C13, F14, REC14, S10, S11 and D1, and its scripts; author-work-items writes the Feature issue.
- /fix-play on /design-eval: the constraints and failures that read the story, its scripts, author-slice-eval and the two eval templates: one eval file for each Feature issue.
- /fix-play on /reshape-plan: C11, C14, F10, S10 and S11; Step 9 removed; `check_agreement.py` and `place_feature.py`.
- /fix-play on /design-slice: C6 and C7, only features not yet built.
- link-model-part stops writing `issue`; the product-os-keeper agent's table says so.
- `CLAUDE.md`, `managing-work.md` and the glossary: Epic, then Feature issue (it holds the scope of work), then Story.

## References

- `.garura/project/issues/_adr/20261112T061525Z/brief.md` — the brief, with its Change at acceptance
- `docs/adr/067-a-play-finds-a-features-story-by-the-issue-the-model-names-when-no-plan-file-marks-it.md`
- `docs/adr/056-an-epic-and-a-story-are-marked-by-their-issue-type-with-no-label.md` — §1, §2
- `docs/adr/048-the-product-model-and-the-work-are-two-layers.md` — §1, §3
- `docs/adr/049-a-slice-is-shaped-then-planned-then-given-its-eval.md` — §1.2, §4
- `docs/adr/052-shape-slice-writes-the-hidden-file-and-proposes-a-thin-ice.md` — §3, §4, §7
- `docs/adr/057-a-slices-eval-is-plain-text-gherkin-that-runs-with-no-agent.md` — §2, §3, §6
- `docs/adr/064-an-items-status-in-a-plan-follows-its-own-issue-with-no-roll-ups.md` — §1, §2
- `docs/adr/065-the-models-index-is-changed-through-two-skills-the-model-never-names-a-plan-and-only-tools-know-the-tracker.md` — rules 3 and 4
- `core/components/memory/standards/schemas/product-os/ontology.md` (version 15) and `spine.yaml`
- PR #1047 — `core/components/plays/shape-plan/reference/ice.md` on its branch
