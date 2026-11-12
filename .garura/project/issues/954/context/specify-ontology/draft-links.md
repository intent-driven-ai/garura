# Draft — the properties, links and rules (stage `links`, steps 5 and 6)

Need: #954 (make the product ontology match ADR 069: the plan is where the product model meets the work). Agreed at checkpoint 1: the 24 questions. Agreed at checkpoint 2: the kinds draft, with K1, K2 and K3 as proposed.

## Opening

You decide the final words of the properties, the links and the rules of the six kinds that change, and three points that the kinds stage kept for this stage: the name of the plan file's mark for its one epic, the statuses of a slice in a plan file, and when a chore goes under the epic. When you type yes, the `write` stage writes these words, the examples and the answers to the 24 questions into the ontology and runs its check. When you change something, this stage is done again with your words first.

How to read a grey block: a "-" line is today's text in the ontology, quoted; a "+" line is the final text. Only what is new since the kinds draft is shown. A line that the kinds draft already showed in its final words (each "(goes)" line, the heads of the kinds, and the rule for the whole model) is not shown again. A "(the rest stays)" note means the words after it do not change.

The three points, in short (each is a full question at the end):

- **L1** — The mark is `epic: <issue number>`, one line at the top of the plan file.
- **L2** — A slice has one of four statuses in a plan file: Not Started, In Progress, Done or Dropped.
- **L3** — A chore goes under a story when the upkeep is for that one story's work; otherwise under the plan's epic.

## Plan

**Properties** — the new and the changed lines (Item kinds, Tree and Folder change; Epic, Slices, Eval, Hidden files and Usage guides are new; the hidden file, the eval and the guide move here from the Slice):

```diff
- | Item kinds | The six kinds of item its tree may hold, each under one kind of parent: an epic at the top; a feature (a Feature issue) under an epic; a story under a feature; a spike, a chore or a bug under a story | yes — every item names its kind |
+ | Item kinds | The six kinds of item its tree may hold, each under one kind of parent: its one epic at the top; a feature (a Feature issue) under the epic; a story under a feature; a spike or a bug under a story; a chore under a story or under the epic | yes — every item names its kind |
- | Tree | Business Intent → Slice → Epic → Feature issue (with its `represents` mark) → Story → Spike, Chore, Bug — each item with its tracker issue, its kind and its state | yes |
+ | Tree | Its one Epic → Feature issue (with its `represents` mark) → Story → Spike, Chore, Bug; a Chore can also sit straight under the Epic — each item with its tracker issue, its kind and its status. A slice is not an item of the tree: the Slices list records it | yes |
+ | Business intent | The business intent it serves, by its title and its id (its issue number, which is also the plan's ID; the model names it `bi-<n>`), on the first line of the plan file, at the top above the tree. A plan serves one business intent: the one it is given. The plan-view template (`standards/templates/plan-view.md`), which `/view-plan` and `/list-plans` use, shows it at the top of each plan, above the tree | yes |
+ | Epic | The mark `epic: <issue number>`, one line at the top of the plan file: the issue number of its one epic. The epic at the top of its Tree has the same number | yes, once its epic is made |
+ | Slices | The list `slices`: each slice it holds, by its id, with its status — Not Started, In Progress, Done or Dropped. A person sets each status; nothing works it out | yes, once it holds a slice |
+ | Eval | Its one eval. It tests, from the outside, on the built product, every feature of every slice it holds, also a feature whose Feature issue sits under another plan's epic (`held_by`): every goal and expectation its Feature issues carry is met, and no failure condition in the hidden files of its slices happens. Built by the eval play from its epic (with the feature-to-story map), the Feature issues the map names and the hidden file of each slice it holds. Kept in its `evals/` folder | yes, once its epic and Feature issues are made |
+ | Hidden files | `failure-and-recovery.md` in `evals/<slug>/`, one for each slice it holds that was first shaped for its intent: one entry for each feature of the slice. (Today's text of the Slice's "Hidden file" property, from "the feature (its id and name)" to the end, moves here word for word; "The ids never leave the eval folder" becomes "The ids never leave the plan's evals folder".) | yes, once such a slice is shaped |
+ | Usage guides | What each surface is (a browser page, a mobile app, a command line command or a backend endpoint), how to reach it, and the steps a person takes. Delivered by the build, in its `guides/` folder. How the guides are laid out is left to the `/design-eval` rework | yes, once a slice it holds is built |
- | Folder | Beside the plan file: `evals/<slug>/`, which holds the hidden file `failure-and-recovery.md` (written by `/design-slice`) and the eval (written by the eval play), and `guides/` (written by the build), one entry for each slice whose home plan it is. The plan play writes nothing in `evals/`. A slice it holds whose home is another plan is pointed to from its Tree, never copied | yes, once it holds a slice |
+ | Folder | Beside the plan file: `evals/`, which holds its one eval (written by the eval play) and `evals/<slug>/` with the hidden file of each slice first shaped for its intent (written by `/design-slice`, also before the plan file exists); and `guides/` (written by the build). The plan play writes nothing in `evals/`. For a slice first shaped for another intent, the plays work out that plan's folder from the slice's first intent; the plan file stores no path, and nothing is copied | yes, once it holds a slice |
```

**Relationships:**

```diff
- | this → other | Slice | many | It holds every slice that serves its business intent, read from the link "slice serves business intent" |
+ | this → other | Slice | many | It holds every slice that serves its business intent, read from the link "slice serves business intent", and records each in its Slices list with its status |
- | this → other | Epic | many | It creates the epic for each slice it holds, or uses the one that exists |
+ | this → other | Epic | one | It has one epic, named by its `epic` mark. The plan play creates it once |
+ | other → this | Chore | many | A chore for the plan as a whole sits in it, straight under its epic, and its Tree names it |
```

**Rules** — the changed rules:

```diff
- It does three things, in this order: it is given a business intent, it holds the slices that serve it, it creates one epic for each slice, or uses the one that exists, and finds or files the Feature issue of each feature of that slice that is not yet built. The plan play does them right after `/design-slice`, with no stop between them.
+ It does three things, in this order: it is given a business intent; it holds the slices that serve it and records each with its status; it has one epic, which the plan play creates once, and it finds or files the Feature issue of each feature of its slices that is not yet built. The plan play does them right after `/design-slice`, with no stop between them, and makes a plan only once.
- A business intent has one plan, and never a second one. When a new slice is shaped for an intent that has a plan, the plan play adds the slice and its epic to that plan.
+ A business intent has one plan, and never a second one. When a new slice is shaped for an intent that has a plan, `/reshape-plan` adds it on a person's instruction: the plan file records it in its Slices list with the status Not Started, and its Feature issues go under the plan's one epic. No second epic and no second plan is made.
- It finds the work items that exist before it creates new ones. When a slice it holds already has an epic, it uses that epic. It finds a feature's Feature issue by the R3 rule of the Feature issue, and files one only when it finds none.
+ It finds the work items that exist before it creates new ones. It finds its epic by its `epic` mark, and a feature's Feature issue by the R3 rule of the Feature issue, and files one only when it finds none.
- Its folder keeps the hidden file, the eval and the usage guide of each slice whose home plan it is (the plan for the business intent the slice was first shaped for). When it holds a slice whose home is another plan, it points to that plan's hidden file, eval and guide, and never copies them.
+ Its folder keeps its one eval, its usage guides, and the hidden file of each slice it holds that was first shaped for its intent. When it holds a slice first shaped for another intent, its eval reads that plan's hidden file and never copies it. The plays work out the place from the slice's first intent; nothing in the model or the plan file stores it.
- A person sets the plan's Status and its Direction. Each item in its tree follows its own issue: (the rest stays)
+ A person sets the plan's Status, its Direction and the status of each slice in its Slices list. Each item in its tree follows its own issue: (the rest stays)
- Its tree holds six kinds of item, each under one kind of parent: an epic at the top of the tree; a feature (a Feature issue) under an epic; a story under a feature; a spike, a chore or a bug under a story (a bug under the story that brought the defect in).
+ Its tree holds six kinds of item, each under one kind of parent: its one epic at the top of the tree; a feature (a Feature issue) under the epic; a story under a feature; a spike or a bug under a story (a bug under the story that brought the defect in); a chore under a story, or under the epic (the Chore's rules say which).
- A feature whose Feature issue sits under another plan's epic shows in its tree under its own epic, as an item of kind `feature` with that issue's number and the mark `held_by: <epic>`. (the rest stays)
+ A feature whose Feature issue sits under another plan's epic shows in its tree under its one epic, as an item of kind `feature` with that issue's number and the mark `held_by: <epic>`. (the rest stays)
- Older plan files also hold the item kind `issue`, a story straight under an epic, an item of kind `feature` with no `represents` mark (an old feature item), or an item under another parent. That is drift, not an error: (the rest stays)
+ Older plan files also hold the item kind `issue`, a story straight under an epic, an item of kind `feature` with no `represents` mark (an old feature item), an item under another parent, an epic with a `represents` mark (an old epic for one slice), more than one epic, or no `epic` mark and no Slices list. That is drift, not an error: (the rest stays)
- Its Status, its Direction, its Branch, its item kinds, the status of each item and the record of its changes are operational. (the rest stays)
+ Its Status, its Direction, its Branch, its `epic` mark, its item kinds, the status of each slice and of each item, and the record of its changes are operational. (the rest stays)
```

**Rules** — new, and moved here from the Slice (their meaning is kept; "its slice" becomes "the plan" or "each slice it holds"):

```diff
+ It records each slice it holds with its status: Not Started, In Progress, Done or Dropped. A person sets it, through `/reshape-plan`. Nothing works it out from the Feature issues or the stories: a slice is not Done because they closed. A slice is in progress when a plan file that holds it records In Progress. When two plans hold one slice, each plan file records the slice's status for itself. `/design-slice` and `/reshape-plan` read it there; the model is not asked, and it holds no status of a slice.
+ A done plan lands on main only when its eval passes. Until the eval runner exists (#801, the runner that runs an eval with no agent), the harness runs the eval by hand before a done plan lands. A paused plan still merges into main.
+ A builder agent, any skill that builds the software, or the build play's context sub-agent never reads its eval or a hidden file, and never reads a plan's evals folder.
+ Its eval reads four things, at two times. The eval play, when it builds the eval, reads its epic (with its feature-to-story map), the Feature issues the map names (their scope of work and Context guidance) and the hidden file of each slice it holds, and joins each entry to its Feature issue through that map — never the usage guides or the code, which are what the build makes. The eval, when it runs after the build, reads the eval, the usage guides, the Context guidance the eval play put in the eval, and, in the hidden files, only the recovery parts of each entry (when, way back, who fixes), never the failure conditions — and reaches the built product only through the guides. Neither reads the ICE of a feature or a capability (the rest of today's sentence stays).
+ Each hidden file in its folder is written by `/design-slice` when it shapes the slice, from each feature's ICE and that feature's capability's ICE, by `standards/rules/expectation-generation.md`: each feature of the slice has one entry, with its failure conditions and exactly one recovery condition for each "Fails if" line, marked "the builder can fix this alone" or "a person must decide". When one of the two ICE is thin, the entry says so.
+ When its eval finds a failure, it writes a handoff plan from the recovery condition: what the product does wrong, as a symptom, and the way back. (the rest of today's rule stays word for word)
+ When a slice it holds gains a feature, `/design-slice` adds that feature's entry to the slice's hidden file, in the folder of the plan for the slice's first intent. Then `/reshape-plan` finds or files that feature's Feature issue under the epic, and adds its line to the feature-to-story map. The plan's eval is then out of date.
+ `/design-slice` makes `evals/<slug>/` in the folder of the plan for the slice's first intent, also when no plan file exists yet. The plan play later writes the plan file beside it and finds the folder there.
+ The build delivers the usage guides in the guides folder, beside the evals folder but not in it, so the builder writes the guide and never sees the eval.
```

**States:** no change.

## Epic

**Properties:**

```diff
- | Feature-to-story map | For each feature of its slice, its Feature issue, as a list "feature → Feature issue" on the issue, one line for each feature. A Feature issue that sits under another epic is named with that epic. Written by the plan play; a line is added when a feature joins. Read by the eval play to join each hidden-file entry to its Feature issue | yes, once it names a feature |
+ | Feature-to-story map | For each feature of each slice its plan holds, its Feature issue, as a list "feature → Feature issue" on the issue, one line for each feature. A feature in two of the plan's slices has one line. A Feature issue that sits under another plan's epic is named with that epic. Written by the plan play; `/reshape-plan` adds a line when a feature or a slice joins the plan. Read by the eval play to join each hidden-file entry to its Feature issue | yes, once it names a feature |
```

**Relationships:**

```diff
- | this → other | Business Intent | many | It serves one or more business intents — the ones its slice serves; it has no list of its own apart from its slice |
+ | this → other | Business Intent | one | It serves its plan's one business intent; it has no list of its own |
- | other → this | Plan | one | A plan created it (the plan play), with its Feature issues |
+ | other → this | Plan | one | It is its plan's one epic: the plan play created it once, and the plan file names it by its `epic` mark |
+ | other → this | Chore | many | A chore for the plan as a whole sits straight under it |
```

**Rules:**

```diff
- Its map has one line for each feature of its slice. When its slice gains a feature, the plan play finds or files that feature's Feature issue, and adds its line. It never names two Feature issues for one feature.
+ Its map has one line for each feature of each slice its plan holds. When a slice of its plan gains a feature, or a slice joins its plan, the play finds or files each new feature's Feature issue and adds its line. It never names two Feature issues for one feature.
- It holds the Feature issue of each feature of its slice, except one that sits under another epic. A Feature issue sits under one epic at a time. When a second epic needs it, the play asks the person which epic it goes under, and does not move it without that answer.
+ It holds the Feature issue of each feature of every slice its plan holds, except one that sits under another plan's epic (`held_by`). A Feature issue sits under one epic at a time. When another plan's epic needs it, the play asks the person which epic it goes under, and does not move it without that answer.
- One slice has at most one epic. When the slice is in a second plan, that plan uses this epic, and the epic serves both business intents.
+ Each plan has exactly one epic, and each epic belongs to one plan. When two plans hold one slice, each plan has its own epic: a Feature issue of that slice sits under one of them, and the other plan shows it as `held_by`. There is no unplanned epic: work that no slice holds sits in its intent's plan, under the plan's epic.
- Its slice's eval play reads it, with its Feature issues and its feature-to-story map, to learn what it delivers and which Feature issue each hidden-file entry is for. So its title says what a person can see the product do, not how it is built.
+ Its plan's eval play reads it, with its Feature issues and its feature-to-story map, to learn what the plan delivers and which Feature issue each hidden-file entry is for. So its title says what a person can see the product do, not how it is built.
+ It also holds the plan's chores for the plan as a whole, straight under it. A bug still sits under the story that brought the defect in, never straight under the epic.
- R3 — A play finds it by the `represents` mark in its plan file, never by its issue type and never by its title.
+ R3 — A play finds it by its plan file's `epic` mark, never by its issue type and never by its title. An epic with a `represents` mark in a plan file is an old epic for one slice: it is drift, not the plan's epic.
```

## Slice

**Relationships:**

```diff
- | this → other | ICE | many | Its hidden file is written from the "Fails if" lines of its features' ICE and their capabilities' ICE; it holds no ICE |
+ | this → other | ICE | many | Its features' failure and recovery conditions are written, on the work side, from the "Fails if" lines of its features' ICE and their capabilities' ICE; it holds no ICE |
- | other → this | Plan | many | A plan holds it — every plan for a business intent it serves |
+ | other → this | Plan | many | A plan holds it — every plan for a business intent it serves — and records its status there. The slice names no plan |
```

**Rules:**

```diff
- It holds no ICE. It is not an issue type.
+ It holds no ICE. It is not an issue type, and no epic stands for it.
- It names no plan, plan folder, epic, eval, hidden file or usage guide
+ It names no plan, plan folder, epic, eval, hidden file or usage guide — not in its spine entry, its record or a page. Each plan that holds it names it.
- It has one eval, one hidden file and one usage guide, also when two plans hold it. All three are kept in the folder of its home plan: the plan for the business intent it was first shaped for. Another plan that holds it points to them and never copies them.
+ Each plan that holds it tests its features in that plan's one eval. `/design-slice` writes one hidden file for it, also when two plans hold it, in the folder of the plan for the intent it was first shaped for. The Plan's rules say where it is and who reads it.
- It has one hidden file, `failure-and-recovery.md`, in its eval folder. `/design-slice` writes it when it shapes the slice, (the rest)
+ (moves to the Plan, as "Each hidden file in its folder …")
- When it gains a feature, `/design-slice` adds that feature's entry to the hidden file in the home plan's folder; the plan play then finds or files that feature's Feature issue, and adds its line to the feature-to-story map.
+ (moves to the Plan, as "When a slice it holds gains a feature …")
```

The first "-" line of the second pair is the kinds draft's line, not today's text: this stage adds its last words.

## Business Intent

**Rules:**

```diff
- Its page has no Tracker line and names no plan, epic or work item. Its id (`bi-<n>`) stays as a name
+ Its page has no Tracker line and names no plan, epic, work item or tracker issue — not in its Sources and not in its What was done. Its id (`bi-<n>`) stays as a name. Its plan and the tracker point at it: the plan's ID is its issue number.
```

The "-" line is the kinds draft's line: this stage adds its last words.

## Chore

**Relationships:**

```diff
- | this → other | Story | one | It is a child of one story |
+ | this → other | Story | one | It is a child of one story, when the upkeep is for that story's work |
- | this → other | Epic | one | It is a child of its plan's epic, when no story owns it
+ | this → other | Epic | one | It is a child of its plan's epic, when the upkeep is not for one story's work. It has one parent: a story or the epic, never both |
```

**Rules** — new (the answer to L3):

```diff
+ It goes under a story when the upkeep is for that story's work: the story cannot be finished without it. It goes under the plan's epic when the upkeep is for the plan as a whole, for the work of more than one story, or for no story. It never goes straight under a Feature issue. The person who adds it decides, through `/reshape-plan`; the play proposes the parent by this rule, and asks when the chore fits both.
+ Under the epic, it is in no feature: no Feature issue and no slice counts it, and the plan's eval does not test it.
```

## Feature issue

The two lines are as the kinds draft showed them. One more line follows them:

```diff
- | this → other | Epic | one | It sits under one epic at a time |
+ | this → other | Epic | one | It sits under one plan's epic at a time |
```

## The rule for the whole model (K1) — its place and its last words

It goes after the tracker paragraph (today's line 21) and before "**Nothing is blocked**", as one paragraph that starts "**The model knows no plan, no tracker and no decision record.**". The agreed words stay. This stage adds two sentences, from ADR 069 §2, after "Git history keeps where a part came from.":

```diff
+ The spine has no `epics` list, and no part of the model holds a work status: whether a slice is in progress is read from the plan files. The ids that exist (`bi-<n>`, `fn-<n>`) stay as names.
```

## Not yet defined (K2)

```diff
- None. Every kind a question or a relationship names is defined above.
+ - **Product Profile** — the product's box: its levels, gates and compliance. A raised level and its gate are the person's answer to a box-move, kept on the profile, not in a decision record.
```

## For the `write` stage (not asked)

- Q20's answer names the `epic` mark; Q58's answer names the four statuses; Q43's answer points to the Chore's rule.
- The examples of the Plan, the Epic, the Slice, the Business Intent and the Chore follow these words: each plan has `epic:` and a Slices list; no slice has a path or an epic; no intent says "one tracker issue"; one chore sits under an epic.

## Questions for you

### L1 — The name of the plan file's mark for its one epic

- **Question:** What is the name of the mark in a plan file that says which issue is the plan's one epic?
- **Answer (proposed):** `epic`, on one line at the top of the plan file, beside the plan's status and direction: `epic: <issue number>`. The epic at the top of the plan's tree has the same number, and the plan's agreement check tests that the two match. The mark `represents` stays for a Feature issue only. We do not propose the item kind `epic` alone as the mark, because an older plan file can hold several epics, and the kind cannot tell the plan's epic from an old epic for one slice. We do not propose `represents: <plan id>`, because then one word has two meanings again.
- **Why it matters:** A play finds the plan's epic only by this mark, never by the issue type or the title. If the mark is not clear, or one word has two meanings, a play can take an old epic for one slice as the plan's epic and put new Feature issues under the wrong epic.
- **Example:**
  - A clinic: the plan for "Patients book their own appointments online" reads `epic: 341`, and its tree starts with epic 341.
  - A shop: plan 150 reads `epic: 151`. Its tree shows Feature issue 122 under epic 151 with `held_by: 121`, because 122 sits under plan 120's epic.
  - A bank: an older plan file holds two epics, each with a `represents` mark, and no `epic` line. That is drift: `/reshape-plan` names it and asks the bank's product owner which epic becomes the plan's epic.
  - A school: the plan for "Parents enrol a child online" reads `epic: 612`, and a play that searches the tracker for issues of type Epic does not use that search to find it.

### L2 — The statuses of a slice in a plan file

- **Question:** Which statuses can a person give a slice in a plan file?
- **Answer (proposed):** Four: Not Started, In Progress, Done and Dropped, with the same names and meanings as the statuses of the items in a plan. A slice that joins a plan starts at Not Started. A slice is in progress only when its status is In Progress. We leave out Now and Blocked: they say that one open change works on an item, or that one item waits, and the tree already shows that on the Feature issues and stories. We leave out Paused: it is a status of a whole plan. The plan view already knows the four names and their marks.
- **Why it matters:** `/design-slice` and `/reshape-plan` read this status to decide whether they may reshape a slice. If the values are not clear, a play can reshape a slice that a builder works on, or stop on a slice that no one works on.
- **Example:**
  - A clinic: "Self-booking" is In Progress in the booking plan, so `/design-slice` does not reshape it.
  - A shop: "Pay in one minute" is Done in one plan and Not Started in the other; each plan file says it for itself, and the model says nothing.
  - A bank: the bank's product owner sets "Upload once" to Dropped in the loan plan, after the bank chose a partner service. The slice stays in the model.
  - A school: "Pay the fee online" joins the enrolment plan through `/reshape-plan` with the status Not Started.

### L3 — When a chore goes under the plan's epic

- **Question:** When does a chore go under the plan's epic, and not under a story?
- **Answer (proposed):** A chore goes under a story when the upkeep is for that story's work, so that the story cannot be finished without it. It goes under the plan's epic when the upkeep is for the plan as a whole, for the work of more than one story, or for no story. It never goes straight under a Feature issue. The person who adds it decides, in `/reshape-plan`; the play proposes the parent by this rule, and asks when the chore fits both. A chore under the epic is in no feature: no Feature issue and no slice counts it, and the plan's eval does not test it.
- **Why it matters:** If every chore must have a story, upkeep for the whole plan goes under a story it does not belong to, and that story looks unfinished for the wrong reason. If chores go under the epic when a story needs them, the builder of that story does not see the upkeep its work needs.
- **Example:**
  - A clinic: "Add the slots table" goes under the story "Pick a free slot", because only that story needs it. "Move the old bookings to the new calendar" goes under the plan's epic.
  - A shop: "Add the guest orders table" goes under the story "Guest checkout". "Clean the old cart data" goes under the plan's epic.
  - A bank: "Move the scoring rules to config" goes under the story "Score the application". "Update the rate config that two stories read" goes under the plan's epic.
  - A school: "Archive last year's paper forms" serves no story, so it goes under the plan's epic.

## Sources

- `docs/adr/069-the-plan-is-where-the-product-model-meets-the-work.md` — Decision §2 (the model holds no work status; the spine has no `epics` list; the ids stay as names), §3 (one epic; a plan's chores under it; a bug under its story), §4 (one eval; lands only when it passes; by hand until #801; a paused plan still merges), §5 (the plan file records each slice and its status), §6 (`/reshape-plan` adds a slice), §7 (no unplanned epic), §9.3 and §9.4 (where the files live; the two times the eval is read; the read rule), and "What this changes in older ADRs" (ADR 063 §3: a feature that joins makes the plan's eval out of date).
- `docs/adr/068-each-product-feature-has-one-feature-issue-that-names-it.md` — the Feature issue's `represents` mark and `Represents:` line, which stay for the Feature issue only.
- `core/components/memory/standards/schemas/product-os/ontology.md` (version 16) — Business Intent (lines 191 to 268), Slice (lines 442 to 500), Plan (lines 603 to 670), Epic (lines 672 to 720), Feature issue (lines 722 to 779), Chore (lines 869 to 904), Not yet defined (lines 944 to 946).
- `standards/templates/plan-view.md` (Phoenix memory, lines 11 to 22; copy at `.garura/project/issues/954/context/memory/standards/templates/plan-view.md`) — the six statuses of a plan's items and their meanings, which L2 reuses in part.
- `core/components/plays/shape-plan/scripts/write_plan_file.py` (lines 8 to 11) — today the plan file marks each epic with `represents: <slice id>`, which L1 replaces with `epic`.
- `.garura/project/issues/954/context/specify-ontology/draft-kinds.md` — the agreed kinds draft and the three points it kept for this stage.
