## Intent
- Goal: In the Agent decisions section, the person reads every decision an agent made, grouped by play with the problems first, each with its trace, every step's source shown in its place with the lines around it and the used lines marked, and its state after a fresh check, the same, changed, gone or no source; they mark each decision as looking right or send it back so the agent decides again from memory as it is now, so no decision rests unseen on memory that changed.
- Limit: Every step's source is checked again before it is shown, and a decision with no trace is flagged.
- Limit: Argus reads no memory itself; every piece it shows comes from the review pack Garura built from the memory tool's answers.
- Limit: A send-back has the agent decide again only from memory; the person's comment is not memory.
- Fails if: A step whose source changed or is gone shows as the same, or a decision with no trace is not flagged.
- Fails if: A step is shown without the lines around it, or without the lines the agent used marked.
- Fails if: A decision sent back comes back resting on anything but memory as it is now.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the run's decision records with their traces, the memory tool's fresh check of every step's source, and the records of the approved memory updates the decisions came from.
- Never read: any memory file by its path, any memory update that still waits as a source to decide from, any ICE page, and production.
- Persona: the product owner, who wants to see what each of the agents' decisions rests on.
- Scope: In: showing each decision with its trace and each step's state, problems first, and the answer looks right or send back. Out: recording decisions and checking their sources, approving memory updates, and applying the answers in one commit.

## Expectation
- Scenario: A shop's checkout run made twelve decisions. The section opens with one whose step on the sign-in security level now reads changed, showing the old lines and the lines now; the product owner sends it back, and the agent decides again from memory as it is. The other eleven show every step the same, and he marks them as looking right.
- Done means: Someone other than the one who built it compares each decision shown with the memory tool's own check of the same records, and finds every step's state the same, every changed or missing source listed first, and every decision with no trace flagged.
