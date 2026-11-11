## Intent
- Goal: Each decision an agent makes is recorded in the issue's short-term memory with its question, answer, who decided, the play and its trace, each step with what the agent looked for, what it found and a source read first through the tool, kept with its exact text, version, fingerprint and the lines around it, and naming the approved update it rests on; and a check reads every source again and names, by its step, a source that changed or is gone and a decision with no trace, so a person sees what each decision rested on and when that memory no longer says it.
- Limit: A step's source is read before it is recorded; a source that is gone or changed is refused.
- Limit: Decision records stay in the issue's short-term memory, and no lookup returns them.
- Limit: Showing a trace to a person, and sending a decision back, stay with Review what agents make (Argus).
- Fails if: A decision is recorded with a source that memory no longer holds as it was read, or with no trace and no flag.
- Fails if: The check misses a step whose source changed or is gone, or names a problem without its step.
- Fails if: An agent decides from its own earlier decision record.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the memory tool's contract for `cite` and `citations`, the issue's decision records and where they are kept, the `read` answers each step took its lines and fingerprint from, the approved updates a decision rests on, and the open issue on replaced decisions.
- Never read: any memory file by its path, and any ICE page; nor another issue's short-term memory.
- Persona: the developer, a person or an AI agent who builds the code and records each decision with its trace; and the product owner, who later reads what a decision rested on.
- Scope: In: recording a decision with its trace, keeping each source's text and the lines around it, naming the update a decision rests on, and the check of every source; and, not built yet, marking a decision that a later one replaced. Out: showing traces to a person and sending a decision back, finding memory, deciding an update, and checking a page before any agent uses it.

## Expectation
- Scenario: In a shop's checkout service, an agent records how shoppers sign in, in four steps, each with its lines and fingerprint from Phoenix memory and the product's profile. A month later the knowledge page behind the fourth step changes, and the check names that record and its fourth step, with the lines now and the lines around them. In a game studio's build, a decision on build caching rests on an update the product owner approved, and its record names the update.
- Done means: Someone other than the one who built it reads the two issues' decision records and runs the check, and finds the shop's record with four steps, each with its exact text, fingerprint and lines around it; the check naming only the fourth step as changed; the studio's record naming the approved update; and no decision record among the hits of any lookup.
