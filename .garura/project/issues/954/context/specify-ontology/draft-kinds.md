# Draft — the kinds (stage `kinds`, steps 2 to 4)

Need: #954 (make the product ontology match ADR 069: the plan is where the product model meets the work). Agreed questions, at checkpoint 1: Q1, Q7, Q18, Q20, Q28 to Q33, Q35, Q36, Q40 and Q43 (changed), and Q54 to Q63 (new).

## Opening

You decide which kinds change, and what each one now means. Six kinds change: the Plan, the Epic, the Slice, the Business Intent and the Chore change in meaning, and the Feature issue changes in two lines. Four kinds on the list do not change (Domain, Capability, Feature, Story), and three questions for you are at the end. When you type yes, the next stage (`links`) writes the final words of the properties, links and rules of these kinds; when you change something, this stage is done again with your words first.

How to read a grey block: a "-" line is today's text, shortened; a "+" line is the new text. Lines that do not change are not shown. The head of each kind (What it is, In the tracker as, Lives at) is the text this stage proposes. The property, link and rule lines show what changes; the `links` stage writes their final words.

## Step 2 — What we reuse

- **Reused as they are:** Source, ICE, Spike and Bug (no agreed question reaches them), and Domain, Capability, Feature and Story (see "Kinds that do not change").
- **Reused with a change:** Plan, Epic, Slice, Business Intent, Chore and Feature issue.
- **Reused rules:**
  - "One plan for each business intent; its ID is the intent's issue number" (Plan, line 638; Business Intent, line 227). The ids stay as names (Q59).
  - "Operational facts live in the plan file only, never in the product model" (Plan, line 655). The new rule for the whole model (K1) widens it.
  - "No property, page or spine entry of a feature names an issue" (Feature, line 430). K1 widens it to every kind.
  - The `held_by` mark (Plan, line 650), R1 and R3 (Epic), "no roll-ups" and "a person sets each status" (Plan, line 647).
  - The hidden file, the two times the eval is read, and the handoff plan (Slice, lines 486 to 488) keep their meaning. They move from the Slice to the Plan.
- **Clashes found:**
  - **One epic, many slices.** Today an Epic "represents one slice" (line 674, property Represents at line 688), and one epic is shared by two plans (lines 482, 706). Q55 gives each plan one epic. So an epic stands for no slice, and the shared epic goes.
  - **The word `represents`.** In a plan file it marks two things today: the epic's slice and the Feature issue's feature. After this change, only a Feature issue stands for something. The plan file still marks its one epic (Q20), and the `links` stage names that mark.
  - **"Home plan".** Today a slice keeps its eval, its hidden file and its usage guide in its home plan's folder (line 484). Q28 and Q31 give the eval and the guides to each plan. Only the hidden file stays in the plan for the intent the slice was first shaped for (Q33, Q40).
  - **Links in a business reader's page.** "What was done ... with links to the finished work items" (line 213) breaks Q60. The Tracker line on the page breaks Q59.
  - **"In the tracker as" for a product kind.** The Slice says "an Epic" (line 447). Q54 says a slice names no epic, so the Slice is "none — model only", like the Domain.
  - **Where a slice's progress is read.** "Shown by its Epic" (line 483) breaks Q58. The status goes to the plan file, still never on the slice.
  - **"Agent decision".** ADR 037 uses it for an agent's traced choice in a run. The product owner's words use it for what an ADR records. This ontology uses neither: it says "a decision about the code" for an ADR (Q63), as ADR 069 does.

## Step 3 — The terms

| Term | Kind of word | Meaning now | Change |
|------|--------------|-------------|--------|
| Epic | noun | The one work item of a plan. It holds the Feature issues of all the plan's slices, and the plan's chores | **meaning changes** (was: the work item that represents one slice) |
| eval | noun | The one eval of a plan. It tests every feature of every slice the plan holds | **meaning changes** (was: a slice's eval) |
| usage guide | noun | What the build delivers so that the plan's eval can reach the built product. Kept in the plan's guides folder; its layout is left to the `/design-eval` rework | **owner moves** (was: one guide for each slice) |
| hidden file | noun | One file for each slice, `failure-and-recovery.md`, in `evals/<slug>/` of the plan for the intent the slice was first shaped for. The slice names no hidden file | **owner moves** (its content does not change) |
| home plan | noun | Was "the plan whose folder keeps a slice's eval, hidden file and guide". The plain words "the plan for the intent the slice was first shaped for" replace it | **goes** |
| slice status | noun | The status that a plan file records for each slice it holds. A person sets it. Two plans that hold one slice each record their own | **new** |
| in progress (of a slice) | adjective | A plan file that holds the slice records it so | **meaning changes** (was: its epic is past ready) |
| feature-to-story map | noun | The epic's list, one line for each feature of each slice the plan holds | **widens** (was: each feature of one slice) |
| `held_by` | noun | A Feature issue that sits under another plan's epic. Same meaning; now "another epic" is always another plan's epic | reused |
| `represents` (on an epic) | noun | Goes. An epic stands for no slice | **goes** |
| lands (a done plan) | verb | A done plan merges into main only when its eval passes. A paused plan still merges | **new** |
| What was done | noun | What was delivered for an intent and the value it brought, in plain words, with no link to a work item | **meaning changes** |
| Tracker line | noun | The line on an intent page that named its issue | **goes** |
| reference to the work side | noun | A name, number, link, path or field in the model that points at one particular plan, plan folder, eval, hidden file, epic or tracker issue, or at the tracker. A part about plans may still describe plans in general | **new** |
| `created_by`, `updated_by` | noun | Name the play or the agent and what it did, never an issue | **meaning narrows** |
| product decision | noun | The person's answer to a play's question, kept as the content of the part it decides. Not a record | **new** |
| decision record | noun | Leaves the model. No part holds or links to one | **goes** |
| ADR | noun | A decision about the code: how the agents and plays work, and how the product is built. Kept in the project's ADR folder, never in the model | **new in this ontology** |
| holds, has, sits under | verb | A plan holds slices and has one epic. A chore sits under a story or under the plan's epic | **changes** |

## Step 4 — The kinds

### Plan

**What changes, and why:** The plan becomes the one place where the model meets the work (Q54). It has one epic (Q1, Q7, Q55), records each slice with its status (Q7, Q58), and has one eval, which must pass before a done plan lands (Q28, Q29, Q56, Q57). Its folder keeps that eval, the hidden files and the guides (Q31, Q33, Q40). A new slice joins it through `/reshape-plan` (Q30). A chore can sit under its epic (Q43). The rules on the eval move to it from the Slice (Q29, Q32, Q35).

```diff
- **What it is:** The thread between the product layer and the work layer ... The plan play makes it right after `/design-slice` ... — or, when its business intent already has a plan, adds that slice to it. ... (3) it **creates** one Epic for each Slice, or uses the one that exists, and finds or files the Feature issue of each Feature of the Slice that is not yet built. ... Its folder keeps the hidden files, evals and usage guides of its slices. ...
+ **What it is:** The one place where the product model meets the work, kept in the repo so that anyone — on any day — can see where the work for one business intent stands and carry on without re-reading every issue. The product model names no plan; the plan names the parts of the model it works on. The plan play makes it once, right after `/design-slice`, with no stop between them. It does three things, in this order: (1) it **is given** one Business Intent; (2) it **holds** every Slice that serves that intent, found by reading the link "slice serves business intent", and records each slice with its status, which a person sets; (3) it **has one Epic**, which holds the Feature issue of each Feature of all its slices and the plan's chores, and it finds or files the Feature issue of each Feature that is not yet built. It has one **eval**, which tests every feature of every slice it holds; a done plan lands on main only when that eval passes. Its folder keeps that eval, the hidden file of each slice first shaped for its intent, and the usage guides. A new slice joins a plan that exists through `/reshape-plan`. (The rest of today's text stays: ID, Status, Direction, item kinds, branch, `/reshape-plan`, no history, operational facts, not Claude Code's plan mode.)
- **Lives at:** ... `.garura/project/plans/<id>/` beside it, which holds `evals/` (one folder for each slice whose eval is kept here, with its hidden file `failure-and-recovery.md` and its eval; ...) and `guides/` (one guide for each such slice); ...
+ **Lives at:** ... `.garura/project/plans/<id>/` beside it, which holds `evals/` (the plan's one eval, and `evals/<slug>/` with the hidden file `failure-and-recovery.md` of each slice first shaped for its intent; `/design-slice` can make it before the plan file exists) and `guides/` (the usage guides the build delivers; their layout is left to the `/design-eval` rework); ... (the branch part stays)
```

Property, link and rule lines that change:

```diff
- | Item kinds | ... a spike, a chore or a bug under a story |
+ | Item kinds | ... the plan's one epic at the top; a feature (a Feature issue) under the epic; a story under a feature; a spike or a bug under a story; a chore under a story or under the epic | (Q43)
- | Tree | Business Intent → Slice → Epic → Feature issue ... |
+ | Tree | Business Intent → its Slices, each with its status, and its one Epic → Feature issue → Story → Spike, Chore, Bug; a Chore can also sit under the Epic | (Q7, Q58)
+ | Slices | Each slice it holds, with that slice's status, set by a person | new (Q58)
+ | Eval | Its one eval, moved from the Slice: it covers every feature of every slice it holds, `held_by` ones included | new (Q28, Q29, Q56)
- | Folder | ... one entry for each slice whose home plan it is ... |
+ | Folder | as in Lives at: the one eval, the hidden files of the slices first shaped for its intent, the usage guides | (Q31, Q33, Q40)
- | this → other | Epic | many | It creates the epic for each slice it holds, or uses the one that exists |
+ | this → other | Epic | one | It has one epic | (Q55)
+ | other → this | Chore | many | A chore for the plan as a whole sits under its epic | (Q43, through the Epic)
- It does three things ... it creates one epic for each slice, or uses the one that exists ...
+ It does three things ... it has one epic, and finds or files the Feature issue of each feature not yet built | (Q1, Q7)
- When a new slice is shaped for an intent that has a plan, the plan play adds the slice and its epic to that plan.
+ When a new slice is shaped for an intent that has a plan, `/reshape-plan` adds the slice: the plan file records it, and its Feature issues go under the plan's one epic. No second epic, no second plan | (Q30)
- When a slice it holds already has an epic, it uses that epic.
+ (goes) | (Q55)
- Its folder keeps the hidden file, the eval and the usage guide of each slice whose home plan it is ...
+ Its folder keeps its one eval and the hidden file of each slice first shaped for its intent. A slice first shaped for another intent: it points to that plan's hidden file and never copies it | (Q28, Q33)
+ The eval's rules, moved from the Slice: the two times it is read, the handoff plan, and "a builder never reads a plan's evals folder" | (Q29, Q32, Q35)
+ A done plan lands on main only when its eval passes. Until the eval runner (#801) exists, the harness runs the eval by hand. A paused plan still merges into main | new (Q57)
+ It records each slice it holds with its status, and a person sets it. Two plans that hold one slice each record their own. The model is not asked | new (Q58)
```

**Who reads it:** both (no change). **Layer** and **In the tracker as:** no change.

**Log line:** Plan: the one place where the model meets the work; it has one epic, which holds the Feature issues of all its slices and its chores; it records each slice with a status a person sets; it has one eval, which covers every feature of its slices, and a done plan lands only when that eval passes (by hand until #801); its folder keeps that eval, the hidden files of the slices first shaped for its intent and the guides; a new slice joins it through `/reshape-plan` (Q1, Q7, Q28 to Q33, Q35, Q40, Q43, Q55 to Q58).

### Epic

**What changes, and why:** An epic now belongs to a plan, not to a slice: one for each plan (Q55). It holds the Feature issues of all the plan's slices and the plan's chores (Q1, Q43). Its map has a line for each feature of each slice (Q36). It serves its plan's one intent. The shared epic goes (Q18, Q56). A play finds it by the plan file's mark, and the mark no longer names a slice (Q20).

```diff
- **What it is:** The work item that represents one Slice: one Epic for each Slice a Plan holds. The plan play creates it, finds or files the Feature issue of each Feature of its Slice ... It serves the business intents its Slice serves. Its Slice's eval play reads it ... It is not a Slice (the Slice is in the model; the Epic is the work that delivers it), and it is not in the product model: ...
+ **What it is:** The one work item of a Plan: each plan has exactly one Epic. It holds the Feature issue of each Feature of every Slice the plan holds, with their Stories inside them, and the plan's chores. The plan play creates it, finds or files the Feature issues, and keeps on it the map from each Feature to its Feature issue, one line for each feature of each slice. It serves its plan's one business intent. The plan's eval play reads it, with its Feature issues and its map. It knows no capability and has no ICE. It is long-lived: it stays open when its work is done, and new Feature issues can join it. It does not stand for a Slice: no slice names it, and the plan file names the slices. It is not in the product model: the spine's `epics` list and the `epic.md` pages leave the model.
```

Property, link and rule lines that change:

```diff
- | Represents | The id of its one slice |
+ (goes) | (Q18, Q20)
- | Feature-to-story map | For each feature of its slice, its Feature issue ... |
+ | Feature-to-story map | For each feature of each slice its plan holds, its Feature issue ... | (Q36)
- | this → other | Slice | one | It represents one slice |
+ (goes) | (Q18)
- | this → other | Business Intent | many | ... the ones its slice serves ... |
+ | this → other | Business Intent | one | It serves its plan's business intent | (Q55)
- | other → this | Plan | one | A plan created it ... |
+ | other → this | Plan | one | It is its plan's one epic | (Q55)
+ | other → this | Chore | many | A chore for the plan as a whole sits under it | (Q43)
- One slice has at most one epic. When the slice is in a second plan, that plan uses this epic, and the epic serves both business intents.
+ Each plan has its own epic. When two plans hold one slice, a Feature issue sits under one plan's epic, and the other plan shows it as `held_by` | (Q18, Q56)
- Its slice's eval play reads it ...
+ Its plan's eval play reads it ... | (Q29)
- R3 — A play finds it by the `represents` mark in its plan file ...
+ R3 — A play finds it by its plan file's mark (the `links` stage names the mark), never by its issue type and never by its title | (Q20)
```

**Who reads it**, **In the tracker as**, **Lives at:** no change.

**Log line:** Epic: one for each plan, not one for each slice; it holds the Feature issues of all the plan's slices and the plan's chores; its map has one line for each feature of each slice; it serves its plan's one intent; it stands for no slice, and the epic shared by two plans goes; a play finds it by the plan file's mark (Q1, Q18, Q20, Q36, Q43, Q55, Q56).

### Slice

**What changes, and why:** A slice names nothing on the work side (Q54): no plan, plan folder, epic, eval, hidden file or usage guide. Its eval, its hidden file and its usage guide move to the Plan (Q28, Q29, Q31, Q33, Q40). Whether its work is in progress is read from the plan files (Q58). In the tracker it is nothing: no epic stands for it (Q18).

```diff
- **What it is:** ... it writes no plan, no epic, no Feature issue, no story and no eval. It takes in only features that are not yet built. It has one **eval**, which tests ... what its epic delivers; one **hidden file**, beside the eval, ...; and one **usage guide**, which tells the eval how to reach the slice. It lives in the product model. It is not an Epic: the Slice is in the model; the Epic is the work item that represents and delivers it.
+ **What it is:** ... it writes no plan, no epic, no Feature issue, no story and no eval. It takes in only features that are not yet built. It names no plan, plan folder, epic, eval, hidden file or usage guide: each plan that holds it names it. Each plan that holds it tests its features in that plan's one eval. On the work side, `/design-slice` writes one hidden file for it, in the folder of the plan for the intent it was first shaped for; nothing in the model stores that place. Whether its work is in progress is read from the plan files that hold it, never from the model. It lives in the product model. It is not an Epic: an Epic belongs to a plan and holds the Feature issues of all that plan's slices.
- **In the tracker as:** an **Epic** — one Epic for the Slice, made when the plan play adds the slice to a plan. A Slice is not itself an issue type
+ **In the tracker as:** none — model only. The Feature issues of its features sit under the epic of each plan that holds it. A Slice is not an issue type
- **Lives at:** the spine's `slices` list — ... Its eval and its hidden file `failure-and-recovery.md` are at `.garura/project/plans/<plan-id>/evals/<slug>/` and its usage guide at `.garura/project/plans/<plan-id>/guides/<slug>.md`, where `<plan-id>` is ... `/design-slice` makes the eval folder, also when no plan file exists yet
+ **Lives at:** the spine's `slices` list — `id`, `slug`, `feature_refs`, `vertical`, `intents` and `record`, as today (the fields that go, go, as today). Nothing in the model says where its hidden file is.
```

Property, link and rule lines that change:

```diff
- | Eval | Its one eval ... | ; | Hidden file | ... | ; | Usage guide | ... |
+ (all three leave the Slice; the Plan holds the eval and keeps the hidden file and the guides) | (Q28, Q31, Q33)
- | other → this | Epic | one | At most one epic represents it |
+ (goes) | (Q18)
- It has at most one Epic. A second plan that holds it uses that Epic ...
+ (goes) | (Q55)
- Whether its work has started is shown by its Epic, not by a status on the slice.
+ Whether its work is in progress is read from each plan file that holds it, never from a status on the slice | (Q58)
- It has one eval, one hidden file and one usage guide, also when two plans hold it ... home plan ...
+ (moves to the Plan, as its eval and its folder) | (Q28, Q33)
- the builder rule, the two times the eval is read, the handoff plan, the folder `/design-slice` makes, the guide (lines 485 to 491)
+ (move to the Plan, with their meaning kept) | (Q29, Q31, Q32, Q35, Q40)
+ It names no plan, plan folder, epic, eval, hidden file or usage guide | new (Q54)
```

**Who reads it**, **Layer:** no change. The three examples lose their paths and their epics (the `write` stage).

**Log line:** Slice: names no plan, plan folder, epic, eval, hidden file or usage guide, and in the tracker it is nothing; its eval, hidden file and usage guide move to the plan, and the hidden file stays in the plan for the intent it was first shaped for; whether it is in progress is read from the plan files that hold it (Q18, Q28, Q29, Q31 to Q33, Q35, Q40, Q54, Q58).

### Business Intent

**What changes, and why:** Its page names no plan, no tracker issue and no work item: the Tracker line goes (Q54, Q59). What was done keeps what was delivered and its value, with no link (Q60). One epic serves it, its plan's (Q55). The intent still has an issue in the tracker, and the ids stay as names (Q59).

```diff
- **What it is:** ... It is the person's interface to the product, and it is for tracking. It holds no ICE ...
+ **What it is:** ... It is the person's interface to the product, and it is for tracking. Its page names no plan, no tracker issue and no work item: its plan and the tracker point at it. It holds no ICE ...
- **In the tracker as:** an issue labelled `product` — the only kind with that label
+ **In the tracker as:** an issue labelled `product` — the only kind with that label. Its page does not name the issue; the plan's ID is the issue's number
```

Property, link and rule lines that change:

```diff
- | What was done | What was delivered for it and the value each piece brought, with links to the finished work items — updated as work finishes |
+ | What was done | What was delivered for it and the value each piece brought, in plain words; it links to no work item — updated as work finishes | (Q60)
- | other → this | Epic | many | An epic serves it |
+ | other → this | Epic | one | The epic of its plan serves it | (Q55)
- It is a destination: sources, capabilities, slices, its plan and its epics point at it.
+ It is a destination: sources, capabilities, slices, its plan and its plan's epic point at it | (Q55)
+ Its page has no Tracker line and names no plan, epic or work item. Its id (`bi-<n>`) stays as a name | new (Q59)
```

**Who reads it**, **Layer**, **Lives at:** no change. The examples lose "one tracker issue" and the epic names (the `write` stage).

**Log line:** Business Intent: its page has no Tracker line and names no plan, epic or work item; What was done says what was delivered and its value with no link to a work item; the epic of its plan serves it; it still has an issue labelled `product`, and its id stays as a name (Q54, Q55, Q59, Q60).

### Chore

**What changes, and why:** A chore can now sit under the plan's one epic, for upkeep of the plan as a whole, as well as under a story (Q1, Q7, Q43). The need's list named it; ADR 069 §3 says "a plan's chores sit in the plan, under its one epic".

```diff
- **What it is:** Upkeep work for a Story. It is a child of one Story. It holds no ICE and links to no feature.
+ **What it is:** Upkeep work in a plan. It is a child of one Story, or of the plan's one Epic when the upkeep is for the plan as a whole and no story owns it. It holds no ICE and links to no feature.
- **Lives at:** the team's tracker, as a child of its story, named in its plan file
+ **Lives at:** the team's tracker, as a child of its story or of its plan's epic, named in its plan file
```

Property, link and rule lines that change:

```diff
- | Parent | Its one story |
+ | Parent | Its one story, or its plan's one epic | (Q43)
+ | this → other | Epic | one | It is a child of its plan's epic, when no story owns it | (Q43)
- It reaches its feature, its epic and its business intent through its story.
+ Under a story, it reaches its feature, its epic and its business intent through that story. Under the epic, it reaches the business intent through the epic, and it has no feature | (Q43)
```

**Who reads it**, **In the tracker as:** no change.

**Log line:** Chore: upkeep work in a plan; a child of one story, or of the plan's one epic when the upkeep is for the plan as a whole (Q1, Q43).

### Feature issue (two lines)

**What changes, and why:** Its head does not change. Two lines follow the one epic and the one eval: another epic is always another plan's epic (Q18, Q55), and the plan's eval tests its scope of work (Q56).

```diff
- | Scope of work | ... Its slice's eval tests those things |
+ | Scope of work | ... The eval of each plan that holds its feature tests those things | (Q56)
- It sits under one epic at a time. When a second epic needs it, the play asks the person which epic it goes under ...
+ It sits under one plan's epic at a time. When another plan's epic needs it, the play asks the person which epic it goes under ...; the other plan shows it as `held_by` | (Q18, Q55)
```

**Log line:** Feature issue: wording only; another epic is now another plan's epic, and the eval of each plan that holds its feature tests its scope of work (Q18, Q55, Q56).

### Kinds that do not change

- **Domain** — It is model only and names no work item today. The new rule for the whole model (K1) covers its spine `intents` and its metadata. No agreed question changes the kind.
- **Capability** — It names no work item today, and its examples still hold: an epic can keep its title ("One-day decision") as a plan's one epic. The rule for the whole model covers its spine entry.
- **Feature** — Its rule "no property, page or spine entry of a feature names an issue" (line 430) stays as it is. K1 widens it to every kind. It can still be in many slices and plans.
- **Story** — It still sits inside one Feature issue, and through it in one epic. Chores can still sit under it. Its examples still hold.
- Not on the need's list, and not changed: **Source**, **ICE**, **Spike**, **Bug**.

### Outside the kinds (written at the `write` stage)

The opening (still fourteen kinds; the Plan becomes "the one place where the model meets the work"), the flow line (line 11), links 1 and 4 (lines 15 and 18), the tracker paragraph (line 21: "an Epic represents a Slice" goes), and the answers of the 24 agreed questions. The new rule for the whole model, if K1 is yes:

```diff
+ **The model knows no plan, no tracker and no decision record.** No part of the product model holds a reference to the work side: no plan id, plan folder, eval, hidden file, epic, tracker issue number or link, or the tracker — not in a page, its Sources, a spine entry or the spine's metadata. The links run one way, from the work side to the model: a plan names its slices, and a Feature issue names its feature. The spine's `created_by` and `updated_by` name the play or the agent and what it did, never an issue. Git history keeps where a part came from. A part whose subject is plans may still describe plans in general. No decision record lives in the model, and no part links to one: a product decision is the person's answer, kept as the content of the part it decides; an ADR records a decision about the code and is kept in the project's ADR folder.
```

### The version log entry (one line, drafted)

- 2026-11-12 — v17 (#954, ADR 069, with the product owner): the Plan is the one place where the product model meets the work, and the model knows no plan, no tracker and no decision record — a new rule for the whole model: no part holds a reference to the work side (plan, plan folder, eval, hidden file, epic, tracker issue or the tracker), `created_by` and `updated_by` name the play or agent, never an issue, git history keeps where a part came from, a product decision is the content of the part it decides, and an ADR records a decision about the code, outside the model. A plan has one Epic, which holds the Feature issues of all its slices and the plan's chores, records each slice with a status a person sets, and has one eval that covers every feature of its slices; a done plan lands on main only when that eval passes (by hand until #801). Epic: one for each plan; it stands for no slice; the shared epic goes. Slice: names no plan, epic, eval, hidden file or guide, and is model only; its eval, hidden file and guide move to the plan. Business Intent: no Tracker line, and What was done links to no work item. Chore: may sit under the plan's epic. Feature issue: wording only. Changed kinds: Plan, Epic, Slice, Business Intent, Chore, Feature issue. Q1, Q7, Q18, Q20, Q28 to Q33, Q35, Q36, Q40 and Q43 change; Q54 to Q63 are added.

## Kept for the `links` stage (not asked here)

- The name of the plan file's mark for its one epic, now that `represents` names only a feature (Q20).
- The values of a slice status in the plan file (for example the item statuses: Not Started, In Progress, Done, Dropped), set by a person (Q58).
- When a chore goes under the epic and when under a story (Q43).

## Questions for you

### K1 — Does the "no reference to the work side" rule live once, for the whole model?

- **Question:** Does the ontology state, once and for the whole model, that no part names the work side, in place of a rule in each kind?
- **Answer (proposed):** Yes. One paragraph beside the five links, as drafted above under "Outside the kinds". The Feature keeps its own rule (line 430), and the new paragraph widens it to every kind. Domain, Capability, Feature and Story then need no change of their own. The Slice and the Business Intent still get a rule of their own, because Q54, Q59 and Q60 name them.
- **Why it matters:** With a rule in each kind, a kind that someone adds later can miss it. Then a page of that kind cites an issue and nobody sees it.
- **Example:**
  - A clinic: the "Appointments" domain page cites no issue in its Sources, because the rule covers every kind.
  - A shop: the spine entry of "Checkout" says "created by `/specify-capabilities`", not an issue number.
  - A bank: a new kind "Journey", added next year, names no plan from its first day.
  - A school: the "Enrolment" capability page still describes "a plan" in general words, which the rule allows.

### K2 — Does the product profile go under "Not yet defined"?

- **Question:** Does the ontology list the product profile under "Not yet defined", because Q62 names it?
- **Answer (proposed):** Yes, with one line: "Product Profile — the product's box: its levels, gates and compliance; a raised level and its gate are the person's answer to a box-move." Q62 is then marked "partly", because it leans on a kind not yet defined. Defining the profile as a kind is other work (the feature "Define the product profile and the product decision as kinds of the map", which keeps only its profile half).
- **Why it matters:** The template says nothing may point at an unknown word. If Q62 names the profile and the ontology does not list it, a reader cannot find what the profile is, and Q62 looks fully answered when it is not.
- **Example:**
  - A clinic: "security level high" is on the profile; a reader of Q62 finds one line that says what the profile is.
  - A bank: a raised security level and its gate are on the profile, and Q62 shows "partly" until the profile is a kind.
  - A shop: "PCI compliance: yes" is on the profile, named in the list and not yet defined.

### K3 — Is an ADR a kind of this ontology?

- **Question:** Does the product ontology add a kind for the ADR?
- **Answer (proposed):** No. An ADR is a decision about the code, outside the product model, so it is not a kind of the product. Q63 is answered by the new rule for the whole model, and its "Answered by" line names the kinds that hold no decision record (Business Intent, Domain, Capability, Feature, Slice, ICE). Q63 is marked "answered". A product decision is not a kind either, as ADR 069 decided: it is the content of the part it decides.
- **Why it matters:** If the ADR becomes a kind, the product ontology starts to describe how the code is built, and the line between the product and the code that Q62 and Q63 draw gets blurred.
- **Example:**
  - A shop: "pay through one payment service" is an ADR in the shop's ADR folder; the ontology defines no kind for it.
  - A clinic: "store bookings in one database" is an ADR; the clinic's model names it nowhere.
  - A school: "send forms as PDF" is an ADR; the "Enrolment" capability page does not link to it.
  - A bank: "a decision within one day" is the intent's proof, a product decision; the bank's model holds it, and no ADR does.

## Sources

- `docs/adr/069-the-plan-is-where-the-product-model-meets-the-work.md` — Decision §1 to §8, Affects (the ontology lines), and "Work This Creates".
- `docs/adr/068-each-product-feature-has-one-feature-issue-that-names-it.md` — its status line: "a second epic" in §4 now means another plan's epic; the ids stay as names.
- `core/components/memory/standards/schemas/product-os/ontology.md` (version 16) — Business Intent (lines 193 to 268), Slice (lines 444 to 500), Plan (lines 605 to 670), Epic (lines 674 to 720), Feature issue (lines 724 to 779), Chore (lines 871 to 904), the Feature's rule (line 430), the opening (lines 9 to 21).
- `.garura/project/issues/954/context/specify-ontology/draft-questions.md` — the 24 agreed questions.
- `.garura/project/issues/954/context/memory/standards/templates/product-ontology.md` — "Not yet defined": nothing points at an unknown word.
