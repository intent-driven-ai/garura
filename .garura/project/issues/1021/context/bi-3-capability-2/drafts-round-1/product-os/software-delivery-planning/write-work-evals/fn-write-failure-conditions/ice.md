## Intent
- Goal: Each feature whose story is under the chosen item has its entry in the slice's hidden file, with each "Fails if" line of its ICE and its capability's ICE, each with its own id and exactly one recovery that says when it shows, the way back and who fixes it, and the entry says which of the two ICE is thin.
- Limit: Exactly one recovery for each "Fails if" line; never two lines merged and never one split.
- Limit: The way back is guidance, never code, a file name or a command, and when the builder can fix it alone it names what the builder sees and changes in the product, never the evals folder, the eval, the hidden file or the check.
- Limit: Who fixes is "the builder can fix this alone" or "a person must decide", and a person decides when money moves, a person's data reaches the wrong person, an approval is needed, the ICE does not settle a choice, or the step cannot be undone.
- Limit: The entry is written only in the hidden file in the slice's evals folder; no failure condition or id goes into an epic, a story or the plan file, and no part that builds the work reads the file.
- Fails if: A "Fails if" line of the feature's ICE or its capability's ICE is missing from its entry, or has no recovery or more than one.
- Fails if: A way back holds code, a file name or a command, or names the evals folder, the eval, the hidden file or the check.
- Fails if: A failure condition or its id is in an epic, a story or the plan file, or in what a part that builds the work receives.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the features whose stories are under the chosen item, through the epic's map of features to stories, the "Fails if" lines of each feature's ICE and its capability's ICE with their thin marks, the slice and the surface a person tests it on, the rule for a feature's recovery, and the entries the hidden file already has.
- Never read: the eval files of the slice, the usage guide and the code.
- Persona: the product owner, who sees the "Fails if" lines, how many the builder can fix alone and how many a person must decide, before the file is kept.
- Scope: In: each feature's entry, with its failure conditions, their ids and one recovery each, and what the person sees. Out: the ICE and its lines, choosing the slice, updating an entry, the eval and the handoff plan.

## Expectation
- Scenario: The technical lead of a shop names the story for paying by card. Its feature's ICE says "Fails if: a card is charged twice", and its capability's ICE has one more "Fails if" line. The entry holds two failure conditions with their ids. The first gets: when, one order has two charges; way back, refund the second charge; who fixes, a person must decide, because money goes out. The product owner sees both lines and the counts before the file is kept. No story, epic or plan file holds either line.
- Done means: Someone other than the one who wrote the entry compares it with the "Fails if" lines of the two ICE, and finds each line once with exactly one recovery, no code or name of the evals in any way back, and no failure condition in the stories, the epic or the plan file.
