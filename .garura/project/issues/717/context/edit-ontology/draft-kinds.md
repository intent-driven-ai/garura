# Draft — the kinds (stage: kinds)

Need: the Plan kind drops its rule on when a plan lands on main (#717, ADR 060). Ontology version 12 now; this change makes it version 13.

## Opening

No kind is added and no kind is removed. The Plan kind stays, and only one of its rules goes: the rule that a plan cannot land on main until every plan it needs is done. You decide two things: that no new kind is needed, and that this one rule is the only change to the Plan kind. When you say yes, the next stage shows the Plan kind's links and rules as they will be after the change.

## Step 2 — Reuse what exists

- **Plan** (ontology version 12, section "Plan") is the kind this need touches. It is reused as it is. Its what it is, who reads it, layer, place in the tracker, where it lives, its six properties, its four links and its example do not change.
- **The rule that goes** (the Plan kind's tenth rule, line 599): "A plan that needs another cannot land on main until that plan is done: the other plan has landed on main, or has been merged into this plan's branch."
- **The clash.** This rule says the opposite of the accepted decision ADR 060 (2026-10-29): a plan's branch merges into main when the plan pauses, also when its issues are still open, and plan order no longer holds a plan off main. The rule also clashes with the Plan kind's own ninth rule (line 598), which says that managing a plan "never touches branches or code". The tenth rule is the only place where the ontology talks about a branch or about main.
- **Where the delivery rule lives instead.** The harness standard, principle 8 "Branches follow the plan" (`docs/standards/harness-standard.md`), and the work guide, section "A plan's branch: start, pause, start again" (`.garura/user-provided/managing-work.md`). The change plays carry it (merge-change C9, F9, S6; propose-change S6; start-change C9). The ontology does not need to hold it.
- **What stays and is reused.** The property "Needs plans", the link "this → Plan, many: it needs another plan", the rule "It needs another plan when a feature in it belongs to a capability that needs a capability whose features are in that plan", the rule "Two plans that need each other are one plan", and every other rule of the Plan kind.
- **No other kind changes.** No other kind, link or question names a branch or landing on main (checked across the whole ontology).

## Step 3 — The terms

- **Plan** — the kind. Kept.
- **needs another plan** — the link. Kept: it tells the order of the work, not when work can go into main.
- **land on main**, **branch**, **pause**, **merge** — delivery words. They belong to the harness standard and the work guide, not to the ontology. After this change, no Plan rule uses them, except the ninth rule, which says that managing a plan never touches branches.

## Step 4 — The kinds

- **Plan** — reused. It stays the thread between the product layer and the work layer: it is given one business intent, holds every slice that serves it, and creates one epic for each slice with its stories. Read by both a person and an agent. It is not a branch and does not say when work goes into main.
- **Exactly what changes:** one line goes from the Plan kind's Rules — the tenth rule, quoted under step 2. Nothing is put in its place. Then the front matter goes from version 12 to version 13, the date `updated` becomes 2026-10-29, and the Log gets one line.
- **Why:** when a branch goes into main is a rule of delivery, not a fact about what a plan is or how it links. ADR 060 decided that rule in the other direction, and the harness standard and the work guide hold it now. If the line stays, the ontology says the opposite of an accepted decision, and an agent or a review that reads the Plan kind can stop correct work.

## The log line for version 13

- 2026-10-29 — v13 (#717, plan #717, with the product owner): the Plan kind drops the rule "A plan that needs another cannot land on main until that plan is done: the other plan has landed on main, or has been merged into this plan's branch." When a plan's branch goes into main is a rule of delivery, which the harness standard (principle 8) and the work guide hold; ADR 060 decides that a plan's branch merges into main when the plan pauses, also with its issues still open. The property "Needs plans", the link "needs another plan" and the other rules stay. No question and no other kind changes.

## The questions

### Q-K1 — Does this change need a new kind?

**Question:** Must the ontology get a new kind to hold when a plan's work goes into main?

**Answer (proposed):** No. When work goes into main is a rule of delivery. The harness standard (principle 8) and the work guide hold it. The ontology keeps the kinds it has, and the Plan kind is reused.

**Why it matters:** A new kind for branches would put a delivery rule back into the ontology. Then the ontology and the harness standard both hold the rule, and they can say different things again. That is the problem this change fixes.

**Example:**
- A clinic: the plan "Patients book their own appointments online" pauses. The clinic team's work goes into main. The ontology still shows only the plan, its slices and its epics. It shows no branch.
- A shop: the plan "Shoppers can check out without an account" starts again after a pause. The team cuts a new branch from main. The ontology does not change, because it has no kind for a branch.
- A bank: the loan officer's team pauses the plan "Small businesses get a loan decision in one day" with two stories open. The finished stories go into main. The ontology still shows the plan with its two open stories.

### Q-K2 — Is the landing rule the only change to the Plan kind?

**Question:** Must the Plan kind change in only one place: the removal of its rule "A plan that needs another cannot land on main until that plan is done"?

**Answer (proposed):** Yes. Only that rule goes, and nothing takes its place. The kind's description, its properties, its four links, its example and its other twelve rules stay word for word. The property "Needs plans" and the link "needs another plan" stay, because they tell the order of the work. The rule "managing a plan never touches branches or code" stays, because it now agrees with the rest of the kind.

**Why it matters:** If more of the Plan kind changes, a play that reads it can lose a rule it needs. For example, the plan play finds which other plans a plan needs from the rule on capabilities that need capabilities. If less changes, the ontology still holds a plan off main, against ADR 060.

**Example:**
- A clinic: the plan for online booking needs the plan for the patient list. After the change, the ontology still says the booking plan needs it. It no longer says the booking work must wait to go into main.
- A shop: the checkout plan and the cart plan need each other. After the change, the ontology still says they are one plan.
- A bank: a bug is found in the loan plan after it is done. After the change, the ontology still says the bug sits under the story that introduced it, and no new plan is made.

## A thing to know

- Each plan file has a field `branch` (for example `branch: null` while the plan is paused). The Plan kind does not list it as a property, and this change does not add it: the ontology says that managing a plan never touches branches. The field belongs to the plan rules in the work guide. Tell us if you want the ontology to name it in a later change.
