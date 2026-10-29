# Draft — the questions (stage: scope)

Need: the Plan kind drops its rule on when a plan lands on main (#717, ADR 060). Ontology version 12 now.

## Opening

None of the 40 questions the ontology answers changes, and no question is added. No question asks when a plan's work lands on main, so removing that rule takes no answer away. You decide one thing: that the ontology does not answer this question. When you say yes, the next stage removes the rule from the Plan kind and keeps the kind, its link "needs another plan" and its other rules.

## The questions

### Q-A — Is "when may a plan's branch land on main?" a question for the ontology?

**Question:** Must the product ontology answer when the work of a plan may go into main?

**Answer (proposed):** No. The ontology says what a plan is and how it links to other things. When a branch goes into main is a rule of delivery. The harness standard (principle 8) and the plan rules in the work guide hold that rule. The Plan kind already says that managing a plan never touches branches or code. So the Plan kind does not get this question, and its rule "a plan that needs another cannot land on main until that plan is done" goes. The link "needs another plan" stays. It tells the order of work, not when work can go into main.

**Why it matters:** If the ontology keeps the rule, it says the opposite of the accepted decision (ADR 060). That decision says a plan's work goes into main when the plan pauses, also when its issues are still open. Then an agent or a review that reads the Plan kind sees a plan on main against its rule, and it can stop work that is correct.

**Example:**
- A clinic: the plan "Patients book their own appointments online" needs the plan for the patient list. The team pauses the booking plan. Its finished work goes into main, also when the patient-list plan is not done. The ontology still shows that the booking plan needs the patient-list plan.
- A shop: the plan "Shoppers can check out without an account" needs the cart plan. The shop manager pauses checkout to fix a cart problem first. The checkout work goes into main, and the cart fix is cut from main.
- A bank: the plan "Small businesses get a loan decision in one day" needs the document plan. The loan officer's team pauses the loan plan with two stories open. The finished stories go into main, and the two open stories stay in the plan.

## What stays

- The other 40 questions (Q1 to Q40) stay as they are.
- The Plan kind, its property "Needs plans", its link "needs another plan" and its rules "It needs another plan when…" and "Two plans that need each other are one plan" stay.
- A thing to know: no question in the list asks "which other plans does this plan need?". The link "needs another plan" was there before this change and answers no listed question. This change does not add that question. Tell us if you want it in a later change.
