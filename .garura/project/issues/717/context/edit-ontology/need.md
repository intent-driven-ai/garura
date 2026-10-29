# Need — the Plan kind drops its branch-landing rule

Issue: #717 (plan 717), on plan/717/base, landing with PR #950.

In the product owner's words (2026-10-29): "fix it. why is ontology even referring to plan??" — and, on the answer: a plan is given a business intent and finds the slices that serve it, so the Plan kind stays.

The need: ADR 060 (accepted 2026-10-29) decides that a plan's branch merges into main when the plan pauses, even with issues still open, and that plan order no longer holds a plan off main. The Plan kind's rule "A plan that needs another cannot land on main until that plan is done: the other plan has landed on main, or has been merged into this plan's branch." says the opposite. When a branch lands is a delivery rule, held by the harness standard (principle 8) and the plan rules; the ontology says what a plan is and how it links, and its own rule says managing a plan never touches branches or code. So that one rule leaves the ontology. The "needs another plan" link and the Plan kind's other rules stay.

## Touches

Plan
