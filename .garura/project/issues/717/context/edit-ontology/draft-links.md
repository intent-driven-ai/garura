# Draft — the properties, links and rules (stage: links)

Need: the Plan kind drops its rule on when a plan lands on main (#717, ADR 060). Ontology version 12 now; this change makes it version 13.

## Opening

This draft shows the Plan kind's properties, links and rules as they will be after the change. One rule goes, and nothing takes its place. You decide three things: that the properties stay as they are, that the links stay as they are, and that the rules are the twelve below. When you say yes, the next stage writes version 13 of the ontology, with its example and its log line, and runs the check.

## Step 5 — The properties of the Plan kind, after the change

No property changes. The six properties stay word for word.

| Property | What it holds | Required |
|----------|---------------|----------|
| ID | The business intent's issue number | yes |
| Tree | Business Intent → Slice → Epic → Story (with its Feature) → Spike, Chore, Bug — each work item with its tracker issue and its state | yes |
| Now | The work item being worked on | while active |
| Needs plans | The other plans it needs — worked out from its features' capabilities' needs, never set by hand | no |
| Status | active, done or dropped | yes |
| Folder | Beside the plan file: `evals/<slug>/`, which holds the hidden file `failure-and-recovery.md` (written by `/shape-slice`) and the eval (written by the eval play), and `guides/` (written by the build), one entry for each slice whose home plan it is. The plan play writes nothing in `evals/`. A slice it holds whose home is another plan is pointed to from its Tree, never copied | yes, once it holds a slice |

## Step 6 — The links of the Plan kind, after the change

No link changes. The four links stay word for word.

| Direction | Other kind | Count | Meaning |
|-----------|-----------|-------|---------|
| this → other | Business Intent | one | It is given one business intent |
| this → other | Slice | many | It holds every slice that serves its business intent, read from the link "slice serves business intent" |
| this → other | Epic | many | It creates the epic for each slice it holds, with the stories of that epic, or uses the one that exists |
| this → other | Plan | many | It needs another plan |

The links from other kinds to the Plan kind also stay: Business Intent ("Its one plan is given it"), Slice ("A plan holds it") and Epic ("A plan created it"). Every kind these links name is defined in the ontology.

## Step 6 — The rules of the Plan kind, after the change

Twelve rules stay word for word, in the same order. The rule marked REMOVED goes, and nothing takes its place. The numbers are for this draft only; in the ontology the rules stay a list with no numbers.

1. It does three things, in this order: it is given a business intent, it holds the slices that serve it, it creates one epic for each slice, or uses the one that exists, and the stories of that epic. The plan play does them right after `/shape-slice`, with no stop between them.
2. A business intent has one plan, and never a second one. When a new slice is shaped for an intent that has a plan, the plan play adds the slice and its epic to that plan.
3. It holds every slice that serves its business intent, and finds them by reading the link "slice serves business intent". It does not pick, rank or test slices; the person chose the slice at `/shape-slice`.
4. It finds the work items that exist before it creates new ones. When a slice it holds already has an epic, it uses that epic.
5. The plan play writes only the plan file, the epic and the stories. It writes nothing in the evals folder; `/shape-slice` wrote the slice's hidden file there. It puts the goals, limits, Context guidance and expectations of the two ICE in the story, and the feature-to-story map on the epic. The failure and recovery conditions stay in the hidden file, never in the story.
6. The plan play reads every line of each ICE except the "Fails if" lines, which are `/shape-slice`'s. It is not a builder.
7. Its folder keeps the hidden file, the eval and the usage guide of each slice whose home plan it is (the plan for the business intent the slice was first shaped for). When it holds a slice whose home is another plan, it points to that plan's hidden file, eval and guide, and never copies them.
8. It needs another plan when a feature in it belongs to a capability that needs a capability whose features are in that plan.
9. Its plan file and the tracker always agree — its Tree and each epic's feature-to-story map show the same story for each feature; managing a plan changes both together and never touches branches or code.
- REMOVED: ~~A plan that needs another cannot land on main until that plan is done: the other plan has landed on main, or has been merged into this plan's branch.~~
10. Two plans that need each other are one plan.
11. A bug found after a plan is done sits under the Story that introduced it; no new plan is made, and the done plan is not reopened.
12. It holds no capability. A capability shows only through a feature.

The Plan kind has no States section, and this change adds none.

## What else stays

- No other kind changes: its properties, links, rules, states and example stay word for word. The whole ontology was read, and no other line names a branch or landing on main.
- No question changes. The 40 questions and their status stay as they are.
- The Plan kind's example stays. Its line "Needs plan #118, because Checkout needs Cart, whose features are in plan #118" still agrees with rule 8 and with the link "It needs another plan". It does not say when work goes into main.
- Nothing goes to "Not yet defined".

## The questions

### Q-L1 — Do the Plan kind's properties stay as they are?

**Question:** Must the six properties of the Plan kind stay word for word after the rule goes?

**Answer (proposed):** Yes. No property holds anything about a branch or about main. The property "Needs plans" stays, because it tells which other plans must be done first in the order of the work. It does not hold a plan's work off main.

**Why it matters:** If a property is removed with the rule, a play loses data it reads. For example, the plan play writes "Needs plans" from the capabilities of the features. If a property for branches is added, the ontology holds a delivery rule again, and it can say the opposite of ADR 060 again.

**Example:**
- A clinic: the plan "Patients book their own appointments online" still shows that it needs the plan for the patient list.
- A shop: the plan "Shoppers can check out without an account" still shows its status "active" and its work item now, the story "Guest checkout".
- A bank: the plan "Small businesses get a loan decision in one day" still keeps the hidden files, evals and guides of its slices in its folder.

### Q-L2 — Do the Plan kind's links stay as they are?

**Question:** Must the four links of the Plan kind stay word for word after the rule goes?

**Answer (proposed):** Yes. The four links say what a plan is given, what it holds, what it creates and which other plans it needs. None of them says when work goes into main. The link "It needs another plan" stays, because it tells the order of the work.

**Why it matters:** If the link "It needs another plan" goes, no kind can tell that one plan must wait for another, and the rule "Two plans that need each other are one plan" names a link that is not there. If a link is changed, the plays that follow it from a plan to its slices or epics can find the wrong items.

**Example:**
- A clinic: the booking plan still links to the patient-list plan, and the team still builds the patient list first.
- A shop: the checkout plan is still given one business intent and still holds the slice "Pay without an account".
- A bank: the loan plan still creates one epic for each of its two slices.

### Q-L3 — Is removing the landing rule the only change to the Plan kind's rules?

**Question:** Must the Plan kind keep twelve rules, the twelve listed above, after its rule on landing on main goes?

**Answer (proposed):** Yes. Only the rule "A plan that needs another cannot land on main until that plan is done" goes, and no rule takes its place. The other twelve stay word for word and in the same order. Rule 9 ("managing a plan never touches branches or code") now agrees with every other rule of the kind. The rule on when a plan's work goes into main is held by the harness standard (principle 8) and the work guide.

**Why it matters:** If the rule stays, the ontology says the opposite of ADR 060, and an agent or a review that reads the Plan kind can stop correct work. If a new rule takes its place, the ontology holds a delivery rule again. If another rule goes too, a play loses something it needs: for example, the plan play finds which other plans a plan needs from rule 8.

**Example:**
- A clinic: the team pauses the booking plan. Its finished work goes into main, also when the patient-list plan is not done. No rule of the Plan kind stops it.
- A shop: the checkout plan and the cart plan need each other. Rule 10 still says they are one plan.
- A bank: a bug is found in the loan plan after it is done. Rule 11 still says the bug sits under the story that introduced it, and no new plan is made.
