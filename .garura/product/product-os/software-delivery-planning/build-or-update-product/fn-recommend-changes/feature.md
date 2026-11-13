# Feature: Recommend each change to the product owner, and keep his answer

## What it does
Each change that may not go ahead on its own is shown to the product owner as a recommendation: the change, the findings and items it rests on, why, how sure it is, who decides and what it would set going; he approves it, changes it or turns it down, and his answer is kept word for word, with who, when and where, so that such a change starts only from his word, and one he turned down is not asked again without cause.
- A recommendation is a change written out for the product owner to decide. Recommending is the floor every project gets: a change is a recommendation unless the project's settings let its kind go ahead on its own.
- He reads one current list: what waits for him, what he answered, and, apart, what went ahead on its own and waits for his review, from Let the changes the product owner allows go ahead on their own, and show each one with a way back (fn-act-on-its-own). He reads it with the second capability's report of the findings.
- Each recommendation shows its findings whole, with their items, so he can check it without a search.
- He answers each recommendation in one of three ways:
  - approve: the change goes to Start each change down the path that builds it, through the part that owns each step (fn-start-changes), with the words he approved;
  - change: his words replace the draft, and the recommendation is shown again;
  - turn down: the recommendation is kept with his reason, and is raised again only when its findings move, such as new items that make a weak want strong, showing what moved.
- A recommendation he has not answered waits. No other recommendation or change waits for it.
- The list is ordered by facts a person can check, such as how many items a change rests on, never by the agent's own view of what matters.
- What it shows, for example, in different kinds of product: for a shop's checkout, new words on the delivery cost feature's page so the cost shows before the last step, resting on a want with its items from two connections; for a school's timetable app, a question on the intent that lessons are set a term ahead, because many parents ask for weekly changes; for a team's planning tool, a new business intent for planning across teams, for him to give in his own words.
- How it meets the capability: the product owner asked for "or at least making those recommendations" as the least this capability does, and a recommendation is worth something only when it reaches the person who decides and his answer is kept.

Status: not built. What exists covers only patterns for it:
- A memory update waits for a person, who decides it: "approve or reject, who, their exact reply, and where they decided". "Only a person decides, one update at a time."
- The old learning play, /learn-outcomes, is stale. It showed every proposed change at one checkpoint, and its writer notes that "/learn-outcomes surfaces low-confidence changes one by one at the checkpoint."
- The slice play's briefs show what was found with its basis: "A proposed answer always names its source; where none exists the question carries no proposed answer, and the count is shown."

## Inputs / Outputs
- In: each change that may not go ahead on its own, from Work out the change each finding calls for, with why and how sure (fn-propose-changes).
- In: the changes that went ahead on its own, from Let the changes the product owner allows go ahead on their own, and show each one with a way back (fn-act-on-its-own), to list apart.
- In: the product owner's answers so far, word for word.
- Out: one current list of recommendations for the product owner, with what waits, what he answered and what went ahead on its own.
- Out: each answer, kept word for word with who, when and where.
- Out: each approved change, with the words he approved, for Start each change down the path that builds it, through the part that owns each step (fn-start-changes).

## Rules & behavior
- Each recommendation shows what it rests on: its findings, whole, with their items. The reason: "A play that recommends an action must be able to name the source that backs it."
- His answer is kept word for word, with who, when and where. The reason: the memory update path keeps "the person and their reply exactly as given", so a later reader can see who decided and what they said.
- What he approves is exactly what goes on. The reason: the plan session holds the same, "What lands is exactly the list the person saw when they approved it."
- A turned-down recommendation is kept, and raised again only when its findings move. The reason: kept, it shows later why the change was not made; raised again with nothing new, it asks him the same question twice.
- An unanswered recommendation stops nothing else. The reason: nothing outside that change waits on it, and the product owner asked that this work be "built for high autonomy".
- Ordered by facts, never by the agent's view. The reason: an order a person cannot check is a judgment hidden in the layout.
- Not decided: where the list is kept and where he reads it, such as a file in the project, beside the second capability's report, or the planned review tool, whose agreed line names "ADRs, memories, domains, capabilities and ICE" and no recommendation.
- Not decided: whether he answers one recommendation at a time or many at once. The memory update path decides one at a time; the stale learning play took one answer for all of them.

## Acceptance criteria
- Given a recommendation, when it is shown, then it names its findings, their items, why, how sure it is and who decides.
- Given a recommendation he turns down with a reason, when the next run has the same findings, then it is not raised again and his words are kept.
- Given new items that make the want under a turned-down recommendation strong, when the list is updated, then it is raised again, showing what moved.
- Given a recommendation whose draft words he changed, when he approves it, then what goes on holds his words.
- Given a recommendation he has not answered, when other changes come, then none of them waits for it.

## Out of scope
- Working out the changes. Work out the change each finding calls for, with why and how sure (fn-propose-changes) does it.
- Letting a change go ahead on its own. Let the changes the product owner allows go ahead on their own, and show each one with a way back (fn-act-on-its-own) does it.
- Making the change. The part that owns it does, through Start each change down the path that builds it, through the part that owns each step (fn-start-changes).
- Building the review tool. Review what agents make, in Developer tooling, owns it.

## Sources
- The product owner on 2026-11-10, spelling tidied: "or at least making those recommendations", "This needs to be built for high autonomy."
- The capability list the product owner agreed on 2026-11-03: "Review what agents make (Argus): People review ADRs, memories, domains, capabilities and ICE in one tool."
- core/tools/memory/README.md: "approve or reject, who, their exact reply, and where they decided", "Only a person decides, one update at a time.", "the person and their reply exactly as given"
- core/components/skills/author-learnings/SKILL.md: "/learn-outcomes surfaces low-confidence changes one by one at the checkpoint."
- core/components/plays/shape-slice/SKILL.md: "A proposed answer always names its source; where none exists the question carries no proposed answer, and the count is shown."
- core/components/plays/update-plan/reference/ice.md: "What lands is exactly the list the person saw when they approved it."
- standards/rules/no-unbacked-recommendation.md, in Phoenix memory: "A play that recommends an action must be able to name the source that backs it."
