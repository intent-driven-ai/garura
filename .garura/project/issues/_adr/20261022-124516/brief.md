# Decision brief — #758 (plan #756)

## Decision

The agent intent (ICE) becomes its own node in the product model (ontology version 6):

- One ICE for each capability and each functionality. It has its own page (`ice.md` in its part's folder) and its own spine entry.
- It has three parts: Intent (goals, limits, fails if), Context (the rules for the sub-agent that gathers context: what to read, what never to read, the persona, the scope) and Expectation (scenarios, done means, quality needs).
- A business intent holds no ICE. It links to its capabilities. Business intents keep "identified by" between them, as a connection, never a dependency.
- A functionality has exactly one parent capability. A capability has at most one domain.
- "Needs" and "identified by" join capabilities only. A functionality never needs anything.
- An ICE starts only when all three parts are present. A thin or wrong part does not stop it: correctness and richness are the product owner's job.
- The ready check moves to the ICE, with three answers: ready, partly ready, not ready.

## Why now

The product owner reviewed the ICE in ontology version 5, while detailing capability #723, and found it lacking: it had no identity of its own; it was six flat labels inside a capability or functionality page; its Context gave no rules to the sub-agent that gathers context; and its Expectation had no scenarios to build evals from.

## Options considered

- Keep the ICE as a section inside the page and only add the three part headings. Lost: the ICE still had no identity of its own, and a business intent could not be traced to it cleanly.
- One ICE for each pair of business intent and part. Lost (2026-10-22): the agent must merge two ICE before it builds one part.
- Chosen: one ICE for each part, its own node.

## Decided by

The product owner.

## Decided in

#758, through the three /edit-ontology checkpoints and the review of PR #783 (2026-10-22). Run records: `.garura/project/issues/758/context/edit-ontology/` (locked-model.md, decisions.json).

## Shape

markdown — Garura's own decision, in `docs/adr/`. It amends ADR 031 and ADR 043 in their ICE parts only (where the ICE lives, its shape, and the ready rule); the rest of each stays in force.

## Change at the accept step (the product owner, 2026-10-22)

The product owner's words: "An ICE with very good richness and not an approved business intent can still be stopped because the business intent hasn't been approved by someone to work on. Why would you want to send tokens on that part? An approved business intent with a thin ICE is absolutely okay. Maybe there is enough information sitting in the context that will make the ICE really work well. ... If they are thin or weak or not really good, and the outcome is bad, that's on the person. If it is rich enough, then the agents are going to do good work ... that part is an assessment." And: "putting a name in the ADR is absolutely fine. The person was approving it."

So:
- The gate is the business intent: an ICE whose capability serves no confirmed business intent is not ready — no tokens are spent on it, however rich the ICE is.
- The ICE itself needs no separate approval to be ready. ADR 033 §4's condition that the ICE and its part are approved is dropped; the business intent's confirmation stays. ADR 047 therefore also amends ADR 033 §4 (that part only).
- The richness of an ICE is assessed and reported, never a stop. A poor outcome from a thin ICE is on the person who wrote it.
- Decided by: Kapil Viren Ahuja.
