# Capability: Orchestrate agent work through planning

To be deepened with `/discover-capabilities`. Everything below is a directional proposal, drafted from the product owner's one line and the words of business intent bi-9.

## Directional intent
The work of the agents can be orchestrated by careful planning that reads the slices and creates verticals for a clear and crisp end-to-end delivery.

This capability serves the business intent Orchestration (bi-9), where work is orchestrated across business intents, agent intents, the product model and work issues, and a person always knows what's happening and what's next. Its rough scope is the planning: reading the slices and creating the verticals. Running plays as loops, tracking execution in the team's tracker and managing ADRs are other capabilities under the same intent.

It matters because orchestration bridges intent and action: any work traces up to its intent and down to its result.

Features: none written yet. The product owner creates them later.

## Sources
- The capability list the product owner locked on 2026-11-02 (GitHub #1021), under Orchestration: "Orchestrate agent work through planning: The work of the agents can be orchestrated by careful planning that reads the slices and creates verticals for a clear and crisp end-to-end delivery."
- Business intent bi-9 (Orchestration), confirmed by the product owner on 2026-11-02. Outcome: "Work is orchestrated across business intents, agent intents, the product model and work issues, through planning and loops, tracked in the team's tracker, with ADRs recorded as decisions are made. A person always knows what's happening and what's next." Why: "Orchestration bridges intent and action." Proof it is met: "Any work traces up to its intent and down to its result." and "A person can see where everything stands."
- Shelf: none. No knowledge shelf covers software delivery planning, so nothing on this page comes from a shelf.

Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Agent intent (ICE)
- Goal: Planning reads the slices and creates verticals, so the work of the agents has a clear and crisp end-to-end delivery.
- Goal: A person can see where everything stands, and always knows what's happening and what's next.
- Limit: Planning never stops a person; every gate has a way past it that records what's owed.
- Fails if: planning leaves a vertical that does not deliver end to end.
- Fails if: a piece of the agents' work cannot be traced up to its intent and down to its result.
- Fails if: a person cannot see where everything stands.
- Context: serves the product owner, who asked for business intent bi-9, and the agents whose work is orchestrated; touches the slices, business intents, agent intents, the product model and work issues; out are running plays as loops, tracking execution in the team's tracker and managing ADRs, which are other capabilities.
- Checked by: read the verticals planning created from the slices and see that each delivers end to end, then take a piece of the agents' work, trace it up to its intent and down to its result, and confirm that a person can see where it stands.
