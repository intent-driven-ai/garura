## Intent
- Goal: The person is reached only after a round that closed nothing new or at the round limit, and only after one knowledge step run by one agent has grouped the open questions and closed what the sources, memory, research or the context can close; then once, with one brief that shows what we understood, what we built, a few gaps each with its context and our proposed answer, and the pages waiting for approval; the person's typed reply decides every gap and page and reaches the next round's plays from the issue's short-term memory, or the person types stop and the loop closes halted with that reason.
- Limit: A question one play cannot answer never stops the loop; it is the loop's, and the person is never asked after a round that read again.
- Limit: No answer or page is used before a person approves it, and the agent never decides a memory update.
- Limit: The person never gets a bare question or a list of questions, only the brief, and the brief is rendered by a script, never by hand.
- Limit: A knowledge step whose check is still not clean after two fixes halts the loop.
- Fails if: The person is asked before the round's knowledge step ran and its check read clean, or after a round that read again.
- Fails if: An answer recorded for the next round did not come from the person's reply, or a gap or page is left undecided.
- Fails if: The person types stop and the loop goes on, or closes as done.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the round record that read ask, each play's file of open questions, the issue's memory updates still waiting, the loop's sources, what memory holds on each question, the knowledge step's records and its check, the brief, and the person's typed reply.
- Never read: any memory file by its path, and any ICE page.
- Persona: the product owner, who reads the brief, accepts or corrects each gap and page, or stops the loop.
- Scope: In: the open questions as the loop's, the knowledge step, its check, the brief, the person's reply and its record, and stop. Out: deciding after each round whether to ask, what a memory update holds and its promotion, each play's own questions, the review at the loop's end, and a way past a gate.

## Expectation
- Scenario: In a clinic's booking app, round two of the Discovery loop reads ask with five open questions; three of them, from three plays, ask who may cancel a booking. The knowledge step groups them into one gap, settles one question from the prototype's screens, drafts a knowledge page on how long a booking is held, and proposes an answer for the cancel gap from what the screens show. Its check reads clean. The product owner reads one brief, corrects the cancel gap by its id with their own answer and approves the page; round three's plays read the answer. In a team's planning tool, the product owner reads the brief and types stop.
- Done means: Someone other than the one who ran the loop reads the run's records, and finds for the clinic a round record reading ask before the brief, one group holding the three questions, a knowledge check reading clean before the brief was shown, the brief as rendered by its script, the person's reply recorded word for word with the cancel gap holding their own answer and the page approved, and round three's contract holding that answer; and for the planning tool a close reading halted with the reason that the person stopped at a question.
