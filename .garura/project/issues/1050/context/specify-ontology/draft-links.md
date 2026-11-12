# Draft — the properties, links and rules (stage `links`, steps 5 and 6)

Need: #1050 (the ontology change for ADR 068: each product feature has one Feature issue that names it). Agreed: the questions Q19, Q20, Q26, Q43 and Q48 to Q53 (checkpoint 1), and the kinds with K1 to K4 as proposed (checkpoint 2).

## Opening

You decide the properties, the links and the rules of the eight kinds this change touches: the new Feature issue, and Feature, Story, Epic, Plan, Slice, Capability and ICE. Each kind below shows only what changes from today's ontology (version 15): a "-" line is today's text, shortened with "…" where it is long, and a "+" line is the new text. Four questions follow the diffs. Each "+" line that depends on an answer is marked "(L1)", "(L2)", "(L3)" or "(L4)". When you say yes, the `write` stage writes version 16 from this draft, with the examples (step 7), the answers of the changed questions, the flow line, the five links and the tracker paragraph, as agreed at checkpoints 1 and 2. When you change something, this stage is done again with your words first.

The kinds Business Intent, Source, Domain, Spike, Chore and Bug do not change.

## The changes

### Feature issue (new kind, work layer)

```diff
+ ### Feature issue
+
+ **What it is:** The one tracker issue that stands for one product feature, in the whole tracker. Its text names the feature in one exact line, `Represents: <feature id>`. That line is the only link between a feature and its work, and it points one way, from the tracker to the model. It holds the feature's scope of work and its Context guidance, written from the feature's ICE and its capability's ICE. It sits under one Epic at a time and holds the Stories of its feature. A person closes it through `/reshape-plan` "finish", and then the feature is built. It is not the Feature (the Feature is in the model; the Feature issue stands for it in the tracker), and it is not the old feature item (a group of stories that stood for nothing; it goes).
+ **Who reads it:** both
+ **Layer:** work
+ **In the tracker as:** an issue of type Feature, with no label (L3)
+ **Lives at:** the team's tracker, under its one epic, named in the plan file of each plan that holds its feature
+
+ **Properties**
+
+ | Property | What it holds | Required |
+ |----------|---------------|----------|
+ | Issue | The tracker issue's number or key | yes |
+ | Kind | Feature | yes |
+ | Title | The one thing its feature lets a person do, in one line | yes |
+ | State | open or closed, as the tracker holds it. Closed as completed means its feature is built (L4) | yes |
+ | Represents | The exact line `Represents: <feature id>` in its text, once, naming one feature | yes |
+ | Scope of work | Its own words for its feature's work, written by the plan play from every line of the feature's ICE and its capability's ICE except "Fails if": the goals, the limits, and what is expected (the scenarios, what "done" means, and the quality needs). It holds no failure condition and no recovery condition. Its slice's eval tests those things | yes |
+ | Context guidance | The four Context lines of its two ICE, in its own words: what to read, what never to read, the persona, and what is in and what is out. It says where to look; it holds no facts. The build play's context sub-agent reads it and collects the context; the eval play reads it | yes |
+ | Written from | The two ICE it read | yes |
+
+ **Relationships**
+
+ | Direction | Other kind | Count | Meaning |
+ |-----------|-----------|-------|---------|
+ | this → other | Feature | one | It stands for one feature. The link is kept on the issue only, never in the model |
+ | this → other | Epic | one | It sits under one epic at a time |
+ | this → other | ICE | two | It was written from its feature's ICE and that feature's capability's ICE |
+ | other → this | Story | many | A story sits inside it |
+ | other → this | Plan | many | A plan finds or files it, and shows it in its tree |
+
+ **Rules**
+
+ - Each feature has exactly one Feature issue in the whole tracker, open or closed. One Feature issue names one feature, never two.
+ - R3 — A play finds it by the `represents` mark in a plan file. When no plan file marks it, the play searches the tracker through the tracker tool. A match counts only when the issue is of type Feature and its text has the exact line `Represents: <feature id>`. A line that is not exact, or the line on an issue of another type, is not a match. A play never finds it by its title.
+ - Two issues of type Feature with the same `Represents:` line are a duplicate. The run stops and asks the person. A play never files a second Feature issue for a feature.
+ - The plan play files one only for a feature that is not yet built, and only when the search finds none.
+ - It sits under one epic at a time. When a second epic needs it, the play asks the person which epic it goes under, and does not move it without that answer.
+ - It never holds a failure condition or a recovery condition — not in its scope of work, its Context guidance, its title or its examples. `/design-slice` puts them in the slice's hidden file, in its feature's entry.
+ - It holds the Context guidance, never the context itself. When the build play runs for a Story inside it, its context sub-agent reads this Context guidance, collects the context, and puts it in the short-term memory of the issue being built. The sub-agent never opens an ICE page and never reads a plan's evals folder, also when the guidance names it. The builder reads the Feature issue, its Story and that collected context, never an ICE page.
+ - When one of its two ICE changes after it is made, its scope of work, its Context guidance and its feature's entry in the slice's hidden file are drift for the Alignment loop. They are not changed without a word. In the same Alignment round, the plan play makes the Feature issue again and `/design-slice` makes the entry again, from the same two ICE. When the change removes the thin mark, the entry's thin note goes too.
+ - A person closes it, through `/reshape-plan` "finish". Nothing closes it because its Stories closed: there is no roll-up. It can stay open with all its Stories closed.
+ - An issue of type Feature with no `Represents:` line is not a Feature issue. It is drift: it is given the line or another type, never read as a feature.
+ - It never needs anything and is never identified by anything. It links to no Domain and no Capability.
+ - R4 — It is filed with the issue type Feature and no label (L3). It is never an Epic: R1 stands.
+
+ **States**
+
+ open → closed as completed (its feature is built), by a person through `/reshape-plan` "finish"; open → closed as not planned, by a person through `/reshape-plan` "drop". A closed Feature issue is opened again only by a person (L4).
```

### Feature

```diff
- **What it is:** … It is not the v6 work type "Feature" (that work type is gone), not a Story (the work item that represents and delivers it) and not a Slice (a group of features).
+ **What it is:** … It is not its Feature issue (the one tracker issue that stands for it) and not a Slice (a group of features).
- **In the tracker as:** a **Story** — one Story in each Epic that delivers it. A Feature is not itself an issue type
+ **In the tracker as:** one **Feature issue**, in the whole tracker, whose text names it. The Feature holds no link to it

- | Delivered | Whether it has at least one closed Story — worked out each time it is asked, never stored | no — it is computed |
+ | Built | Whether its Feature issue is closed as completed — worked out each time it is asked, through the tracker tool, never stored (L4) | no — it is computed |

- | other → this | Story | many | A story represents it — one story in each epic that delivers it |
+ | other → this | Feature issue | one | Its one Feature issue names it. The link is kept on the issue only |

- - It can be in more than one slice. It is not an issue type.
+ - It can be in more than one slice and in more than one plan. It still has one Feature issue.
+ - It holds no tracker issue number. No property, page or spine entry of a feature names an issue. Only its Feature issue names it.
+ - It is built when a person closes its Feature issue as completed. Closed Stories do not build it. A built feature counts complete in every slice and every plan that holds it.
```

### Story

```diff
- **What it is:** The work item that represents one Feature and delivers it, and with it that Feature's part of its Capability. … It is written from its Feature's ICE and that Feature's Capability's ICE: its scope of work … and its Context guidance. … There is one Story for each Feature in each Epic: … that Slice's Epic gets its own Story for the Feature. It is not the Feature …
+ **What it is:** One piece of work inside one Feature issue. It always sits inside a Feature issue, and through it in one Epic. It does not stand for a feature: it reaches its feature only through its Feature issue. It holds no scope of work and no Context guidance of its own; its Feature issue holds them. A Feature issue can hold many Stories. It is not the Feature and not the Feature issue.
- **Lives at:** the team's tracker, inside its epic, named in its plan file
+ **Lives at:** the team's tracker, inside its Feature issue, named in its plan file

- | Title | What it delivers, in one line | yes |
+ | Title | Its piece of work, in one line | yes |
- | State | open or closed, as the tracker holds it; closed means delivered | yes |
+ | State | open or closed, as the tracker holds it; closed means its piece of work is done, not that its feature is built | yes |
- | Represents | The id of its one feature | yes |
- | Scope of work | Its own words for its work, written by the plan play … Its slice's eval tests those things | yes |
- | Context guidance | The four Context lines of its two ICE, in its own words, on the issue: … the eval play reads it | yes |
- | Written from | The two ICE it read | yes |

- | this → other | Feature | one | It represents and delivers one feature, with that feature's part of its capability |
- | this → other | Epic | one | It sits in exactly one epic |
- | this → other | ICE | two | It was written from its feature's ICE and that feature's capability's ICE |
+ | this → other | Feature issue | one | It sits inside exactly one Feature issue, and through it in one epic |

- - One story per feature in each epic: an epic never holds two stories for one feature.
- - Its feature is one of its epic's slice's features.
- - Its two ICE are the ICE of its feature and the ICE of that feature's capability. …
- - It never holds a failure condition or a recovery condition — not in its scope of work, its Context guidance, its title or its examples. …
- - It holds the Context guidance, never the context itself.
- - When the build play runs, its context sub-agent reads the story's Context guidance, … The builder reads the story and that collected context, and never an ICE page.
- - When one of those ICE changes after the story is made, its scope of work, … so the story and the hidden file never disagree. …
- - Closed means delivered.
+ - It always sits inside one Feature issue. It is never straight under an epic.
+ - It never holds a failure condition or a recovery condition — not in its title, its text or its examples.
+ - Closed means its piece of work is done. Its feature is built only when a person closes the Feature issue.
+ - A Story with no Feature issue as its parent (an orphan) is matched to its feature by research in the product model, and goes inside that feature's Feature issue. When no feature fits, the feature is made and its Feature issue is filed.
- - R3 — A play finds it by the `represents` mark in its plan file, never by its issue type and never by its title.
+ - R3 — A play finds it by its node in its plan file, under its Feature issue, never by its issue type and never by its title.
```

### Epic

```diff
- **What it is:** The work item that represents one Slice: … The plan play creates it, with its Stories, one for each Feature of its Slice, and keeps on it the map from each Feature to the Story that delivers it. … Its Slice's eval play reads it, with its Stories and its map, to learn … which Story each hidden-file entry is for. … new Stories can join it. …
+ **What it is:** The work item that represents one Slice: … The plan play creates it, with the Feature issues of its Slice's features that are not yet built, and keeps on it the map from each Feature to its Feature issue. … Its Slice's eval play reads it, with its Feature issues and its map, to learn … which Feature issue each hidden-file entry is for. … new Feature issues can join it. …

- | Feature-to-story map | For each feature of its slice, the story that delivers it, as a list "feature → story" on the issue. Written by the plan play when it makes the stories; a line is added when a story joins. Read by the eval play to join each hidden-file entry to its story | yes, once it holds a story |
+ | Feature-to-story map | For each feature of its slice, its Feature issue, as a list "feature → Feature issue" on the issue, one line for each feature. A Feature issue that sits under another epic is named with that epic (L1). Written by the plan play; a line is added when a feature joins. Read by the eval play to join each hidden-file entry to its Feature issue | yes, once it names a feature |

- | this → other | Story | many | It holds stories |
+ | other → this | Feature issue | many | A Feature issue sits under it, with its Stories inside |
- | other → this | Plan | one | A plan created it (the plan play), with its stories |
+ | other → this | Plan | one | A plan created it (the plan play), with its Feature issues |

- - Its stories are one for each feature of its slice; when its slice gains a feature, a new story joins it, with its line in the feature-to-story map. It never holds two stories for one feature.
+ - Its map has one line for each feature of its slice. When its slice gains a feature, the plan play finds or files that feature's Feature issue, and adds its line. It never names two Feature issues for one feature.
+ - It holds the Feature issue of each feature of its slice, except one that sits under another epic. A Feature issue sits under one epic at a time. When a second epic needs it, the play asks the person which epic it goes under, and does not move it without that answer.
- - It stays open: it is not closed when its stories are done.
+ - It stays open: it is not closed when its Feature issues are closed.
- - Its slice's eval play reads it, with its stories and its feature-to-story map, to learn what it delivers and which story each hidden-file entry is for. …
+ - Its slice's eval play reads it, with its Feature issues and its feature-to-story map, to learn what it delivers and which Feature issue each hidden-file entry is for. …
```

### Plan

```diff
- **What it is:** … (3) it **creates** one Epic for each Slice, or uses the one that exists, and the Stories of that Epic, one for each Feature of the Slice. … Its tree holds six item kinds, each under one kind of parent: epic, feature, story, spike, chore and bug. …
+ **What it is:** … (3) it **creates** one Epic for each Slice, or uses the one that exists, and finds or files the Feature issue of each Feature of the Slice that is not yet built. … Its tree holds six item kinds, each under one kind of parent: epic, feature (a Feature issue), story, spike, chore and bug. …

- | Item kinds | The six kinds of item its tree may hold, each under one kind of parent: an epic at the top; a feature item under an epic; a story under an epic or a feature item; a spike, a chore or a bug under a story | yes — every item names its kind |
+ | Item kinds | The six kinds of item its tree may hold, each under one kind of parent: an epic at the top; a feature (a Feature issue) under an epic; a story under a feature; a spike, a chore or a bug under a story | yes — every item names its kind |
- | Tree | Business Intent → Slice → Epic → (feature item →) Story (with its Feature) → Spike, Chore, Bug — each item with its tracker issue, its kind and its state | yes |
+ | Tree | Business Intent → Slice → Epic → Feature issue (with its `represents` mark) → Story → Spike, Chore, Bug — each item with its tracker issue, its kind and its state | yes |

- | this → other | Epic | many | It creates the epic for each slice it holds, with the stories of that epic, or uses the one that exists |
+ | this → other | Epic | many | It creates the epic for each slice it holds, or uses the one that exists |
+ | this → other | Feature issue | many | It finds or files the Feature issue of each feature of its slices that is not yet built, and shows it in its tree |

- - It does three things, in this order: … it creates one epic for each slice, or uses the one that exists, and the stories of that epic. …
+ - It does three things, in this order: … it creates one epic for each slice, or uses the one that exists, and finds or files the Feature issue of each feature of that slice that is not yet built. …
- - It finds the work items that exist before it creates new ones. When a slice it holds already has an epic, it uses that epic.
+ - It finds the work items that exist before it creates new ones. When a slice it holds already has an epic, it uses that epic. It finds a feature's Feature issue by the R3 rule of the Feature issue, and files one only when it finds none.
- - The plan play writes only the plan file, the epic and the stories. … It puts the goals, limits, Context guidance and expectations of the two ICE in the story, and the feature-to-story map on the epic. The failure and recovery conditions stay in the hidden file, never in the story.
+ - The plan play writes only the plan file, the epic and the Feature issues. … It puts the goals, limits, Context guidance and expectations of the two ICE in the Feature issue, and the feature-to-story map on the epic. The failure and recovery conditions stay in the hidden file, never in the Feature issue.
+ - Many plans can hold one feature, and it still has one Feature issue. The plan play adds only features that are not yet built. A feature built later stays in the plan and counts complete.
+ - A feature whose Feature issue sits under another plan's epic shows in its tree under its own epic, as an item of kind `feature` with that issue's number and the mark `held_by: <epic>`. Its Stories show only in the tree of the plan whose epic holds it. The agreement check reads the tracker parent of such an item as the `held_by` epic (L1).
+ - The person moves a Feature issue to another epic only in a `/reshape-plan` session of the plan it moves to. That session changes its own plan file and both epics' maps, and its landing's commit message names the plan it leaves as owed. The next session of that plan names the item, offers to mark it `held_by`, and never changes it unasked (L2).
- - Its plan file and the tracker always agree — its Tree and each epic's feature-to-story map show the same story for each feature. …
+ - Its plan file and the tracker always agree — its Tree and each epic's feature-to-story map show the same Feature issue for each feature. …
- - Its tree holds six kinds of item, each under one kind of parent: an epic at the top of the tree; a feature item under an epic; a story under an epic or a feature item; a spike, a chore or a bug under a story (a bug under the story that brought the defect in).
+ - Its tree holds six kinds of item, each under one kind of parent: an epic at the top of the tree; a feature (a Feature issue) under an epic; a story under a feature; a spike, a chore or a bug under a story (a bug under the story that brought the defect in).
- - An item of kind `feature` is a feature item: an issue of type Feature that groups some stories inside one epic. It stands for nothing in the product model: … a play finds the Story of a Feature by the `represents` mark only. A story under a feature item sits in the epic above it.
+ - An item of kind `feature` is a Feature issue. Its `represents` mark names its one feature, the same feature as the `Represents:` line in its text. A story under it sits in the epic above it.
- - Older plan files also hold the item kind `issue`, or an item under another parent (for example a bug under a feature item). That is drift, not an error: …
+ - Older plan files also hold the item kind `issue`, a story straight under an epic, an item of kind `feature` with no `represents` mark (an old feature item), or an item under another parent. That is drift, not an error: …
```

### Slice

```diff
- **What it is:** … `/design-slice` writes that link when it shapes the slice, …; it writes no plan, no epic, no story and no eval. …
+ **What it is:** … `/design-slice` writes that link when it shapes the slice, …; it writes no plan, no epic, no Feature issue, no story and no eval. It takes in only features that are not yet built. …

- | Eval | Its one eval: … what its epic delivers — every goal and expectation its stories carry is met, … Built by the eval play from the epic (with its feature-to-story map), the stories and the hidden file … | yes, once its epic and stories are made |
+ | Eval | Its one eval: … what its epic delivers — every goal and expectation its Feature issues carry is met, … Built by the eval play from the epic (with its feature-to-story map), the Feature issues it names and the hidden file … | yes, once its epic and Feature issues are made |
- | Hidden file | … Read by the eval play (all of it, joined to the stories through the epic's feature-to-story map) …
+ | Hidden file | … Read by the eval play (all of it, joined to the Feature issues through the epic's feature-to-story map) …

- - It serves one or more business intents. `/design-slice` writes the link … — no plan, no epic, no story and no eval.
+ - It serves one or more business intents. `/design-slice` writes the link … — no plan, no epic, no Feature issue, no story and no eval.
+ - It takes in only features that are not yet built. To know which are built, `/design-slice` reads the state of each feature's Feature issue through the tracker tool. A feature built after it joined stays in the slice and counts complete.
+ - Its features can be in other slices and plans. Each feature still has one Feature issue, not one for each slice.
- - Its eval reads four things, at two times. The eval play … reads its epic (with its feature-to-story map), the stories in that epic (their scope of work and Context guidance) and its hidden file, and joins each entry to its story through that map … or the one the plan play wrote into the stories (every other line).
+ - Its eval reads four things, at two times. The eval play … reads its epic (with its feature-to-story map), the Feature issues the map names (their scope of work and Context guidance) and its hidden file, and joins each entry to its Feature issue through that map … or the one the plan play wrote into the Feature issues (every other line).
- - When it gains a feature, `/design-slice` adds that feature's entry to the hidden file in the home plan's folder; the plan play then adds the story to the epic, with its line in the feature-to-story map.
+ - When it gains a feature, `/design-slice` adds that feature's entry to the hidden file in the home plan's folder; the plan play then finds or files that feature's Feature issue, and adds its line to the feature-to-story map.
```

### Capability (wording only, K2)

```diff
- **What it is:** … It is in the model only: no work item links to it — a Story reaches it through its Feature and reads its ICE from there. …
+ **What it is:** … It is in the model only: no work item links to it — a Feature issue reaches it through its Feature and is written from its ICE. …

- | Done | Whether every feature in it is delivered — worked out each time it is asked, never stored | no — it is computed |
+ | Done | Whether every feature in it is built — worked out each time it is asked, never stored | no — it is computed |

- - No work item links to it or carries its ICE. A Story reaches it through its Feature and reads its ICE from there.
+ - No work item links to it or carries its ICE. A Feature issue reaches it through its Feature and is written from its ICE.
- - It is done when every feature in it is delivered: each of its features has at least one closed Story, in any epic. A capability with no features is not done. An open Bug, Chore or Spike under a closed Story does not undo it.
+ - It is done when every feature in it is built: each of its features has its Feature issue closed as completed. A capability with no features is not done. An open Story, Bug, Chore or Spike inside a closed Feature issue does not undo it.
```

### ICE (wording only, K2)

```diff
- **What it is:** … the plan play reads every other line of a Feature's ICE and that Feature's Capability's ICE when it makes the Story, and writes the Story's scope of work and Context guidance from them. …
+ **What it is:** … the plan play reads every other line of a Feature's ICE and that Feature's Capability's ICE when it makes the Feature issue, and writes the Feature issue's scope of work and Context guidance from them. …

- | other → this | Story | many | A story is written from it — a story reads every line of its feature's ICE and that feature's capability's ICE except the "Fails if" lines |
+ | other → this | Feature issue | many | A Feature issue is written from it — from every line of its feature's ICE and that feature's capability's ICE except the "Fails if" lines |

- - No work item carries it. … The plan play, when it makes a Story, reads every other line of the Story's Feature's ICE and that Feature's Capability's ICE, and writes the Story's scope of work and Context guidance. The build play's context sub-agent and the builder never read it; they read the Story's Context guidance and the collected context. The Story's Context guidance is a copy: when the ICE's Context changes, it is drift (see Story). Epic, Spike, Chore and Bug read no ICE.
+ - No work item carries it. … The plan play, when it makes a Feature issue, reads every other line of its Feature's ICE and that Feature's Capability's ICE, and writes the Feature issue's scope of work and Context guidance. The build play's context sub-agent and the builder never read it; they read the Feature issue's Context guidance and the collected context. That Context guidance is a copy: when the ICE's Context changes, it is drift (see Feature issue). Epic, Story, Spike, Chore and Bug read no ICE.
- - The ready check gives one of three answers. … A needed capability is done when every feature in it is delivered.
+ - The ready check gives one of three answers. … A needed capability is done when every feature in it is built.
```

## Questions for you

You decide four points that ADR 068 leaves open. The first two are the point kept from checkpoint 1: how a second plan shows a feature whose Feature issue sits under the first plan's epic, and what a move does to the plan it leaves. The "+" lines marked L1 to L4 above follow the proposed answers; when you change an answer, those lines are written again with your words.

### L1 — How does a second plan show a feature that another plan's epic holds?

- **Question:** When plan B holds a feature whose Feature issue sits under plan A's epic, how does plan B's tree show it?
- **Answer (proposed):** Under plan B's own epic, as an item of kind `feature` with that Feature issue's number and the mark `held_by: <plan A's epic>`; plan B files no second issue, moves nothing, lists no Stories under it, and its epic's map names the Feature issue with the epic that holds it, so plan B's eval still finds it.
- **Why it matters:** With no mark, plan B either fails its agreement check (the tracker parent is plan A's epic) or leaves the feature out, and then plan B's eval cannot join the feature's hidden-file entry.
- **Example:** A school: plan "Parent view" shows "Mark attendance" with `held_by` the epic "Teacher day"; a shop: plan "Pay in one minute" shows "Guest checkout" with `held_by` Epic #121; a clinic: plan "Follow-up visits" shows "Send a reminder" with `held_by` Epic #341, and it turns Done in both plans when the clinic manager finishes #40.

### L2 — Does a move update the plan the Feature issue leaves?

- **Question:** When the person moves a Feature issue from plan A's epic to plan B's epic, what happens to plan A's plan file?
- **Answer (proposed):** The move is made only in a `/reshape-plan` session of plan B, which changes plan B's file and both epics' maps; it does not change plan A's file, because a plan changes only on its own branch, so the commit message names plan A as owed, and plan A's next session names the item and offers to mark it `held_by`, never changing it unasked.
- **Why it matters:** If no one names plan A, its tree shows work that is no longer under its epic and no one sees it; if plan B's session writes plan A's file, it writes off plan A's branch and breaks the rule that each plan changes in its own session.
- **Example:** A bank: the branch manager moves "Upload documents" to "Open an account", and the plan of "Loan in one day" shows it as owed until its next session; a school: the head teacher moves "Mark attendance" to "Parent view", and "Teacher day" names it at its next session; a shop: the store manager moves "Guest checkout", and the commit message names plan #120.

### L3 — Does a Feature issue carry a label?

- **Question:** Is a Feature issue filed with a label?
- **Answer (proposed):** No: it is filed with the issue type Feature and no label, the same as an Epic and a Story, because the type alone says what it is and the labels `product` and `work-item` belong to other kinds.
- **Why it matters:** A label on some Feature issues and not on others gives a search two ways to find one, and a play can miss the ones without it.
- **Example:** A clinic: Feature issue #40 has type Feature and no label; a shop: #71 is found by its type and its `Represents:` line, not by a label; a bank: a Feature issue found with the label `work-item` has the label taken off.

### L4 — Is a feature built when its Feature issue is closed as not planned?

- **Question:** When a person closes a Feature issue as not planned, is its feature built?
- **Answer (proposed):** No: only "closed as completed" means built; a feature whose Feature issue is closed as not planned is not built, a new slice can take it in, and the plan play then shows the closed issue to the person, who opens it again or leaves the feature out, and never files a second one.
- **Why it matters:** If any close counts as built, a dropped feature counts complete in every slice and plan that holds it, and a capability counts as done with work that was never made.
- **Example:** A shop: "Gift wrap" was dropped, so the capability Checkout is not done; a clinic: "Video visit" was dropped last year, and the new slice "Remote care" asks the clinic manager to open #88 again; a school: "Bus tracking" was dropped, and the new plan leaves it out on the head teacher's word.

## Sources

- `docs/adr/068-each-product-feature-has-one-feature-issue-that-names-it.md` — Decision parts 1 to 6; "For the Person Who Accepts This", the second point (the kept point, L1 and L2); part 2 and "What this changes in older ADRs", ADR 056 §1 ("This record does not decide whether a Feature issue carries a label", L3); part 5 and ADR 064 §1 (an item's status follows its own issue, L4).
- `core/components/memory/standards/schemas/product-os/ontology.md` (version 15) — Capability (lines 331, 347, 365, 366), Feature (381, 384, 394, 403, 411), Slice (424, 438, 439, 459, 464, 467), ICE (482, 505, 513, 514), Plan (583, 597, 598, 609, 614, 617, 618, 622, 624 to 626), Epic (648, 663, 671, 672, 677, 678, 680), Story (697, 701, 709 to 714, 720 to 722, 729 to 736, 739).
- `core/components/plays/reshape-plan/scripts/check_agreement.py` — its docstring: "the item's parent in the plan file is its parent in the tracker" (L1).
- `.garura/project/issues/1050/context/specify-ontology/draft-questions.md` and `draft-kinds.md` — the agreed questions and kinds.
