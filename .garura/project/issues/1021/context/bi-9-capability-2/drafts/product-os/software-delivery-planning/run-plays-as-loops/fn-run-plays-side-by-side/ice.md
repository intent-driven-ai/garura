Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: The plays of one round run at the same time only when the round meets all five conditions of the rule for fan-out with scoped writes: each play has its own write scope, fixed before it starts, with none inside another; no play writes a shared file, and one persist writes them after the join; each play's records go to its own path; no play reads another's output; and the guard checks the round's whole change before anything is committed. Otherwise the plays run in turn, and either way the round waits for every play and gives the same result.
- Limit: No play writes outside its declared write scope, and no play writes a shared file such as the spine.
- Limit: Nothing reads a play's output, and nothing is committed, before every play of the round has finished and the guard has passed.
- Limit: Plays that write code do not run at once under this rule.
- Fails if: A round runs its plays at once when any of the five conditions does not hold.
- Fails if: A changed file falls outside the round's declared scopes and the persist's shared files, and the change is committed.
- Fails if: The round's result differs from the result of the same plays run in turn.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the rule for fan-out with scoped writes, the round's plays and what each writes, each play's write scope and output paths, the shared files each play changes and its persist, the scoped-write guard, the shared run's rounds, and the plans for building code side by side.
- Never read: any memory file by its path, and any ICE page.
- Persona: the developer, a person or an AI agent who builds the code, who starts a loop and wants each round to take less time; and the product owner, who reads what the round wrote.
- Scope: In: checking the five conditions for a round, running its plays at once when they hold and in turn when they do not, the join, the one persist of the shared files, and the guard over the round's whole change. Out: how a round is run and decided, building code side by side, the rule and the guard as standards, what each play writes, and the link rules after the round.

## Expectation
- Scenario: In a shop's checkout project, a round has two plays that each write only their own pages and leave their spine changes in their own records. The five conditions hold, so both plays run at once; the round waits for both, one persist writes the spine, the guard finds every change inside the declared scopes, and the round's result matches a run of the same plays in turn. In a clinic's booking app, a round of the Discovery loop has a domain play whose folder holds the capability play's folders, so its plays run in turn.
- Done means: Someone other than the one who ran the loop reads the round's records, the guard's report and the commits, and finds for the shop both plays started before either finished, no read of their output before both finished, one write of the spine after the join, no change outside the declared scopes, and a result equal to the run in turn; and for the clinic the plays run one after another.
