# Feature: Brief the person only on what no play could close, and let them stop

## What it does
When a round ends with questions still open and the loop cannot go on alone, because a round closed nothing new or the round limit is reached, the loop first closes what it can of those questions in one step run by one agent, and only then reaches the person, once, with a brief: what we understood, what we built, a few gaps each with its context and our proposed answer, and the knowledge pages waiting for approval. The person's typed reply goes into the next round, or the person types stop.
- A question one play cannot answer is the loop's, not a stop. The play writes it in its own file of open questions, does all the work the question does not block, and finishes. The other plays, or the next round, may answer it.
- The person is never asked after a round that read again, only after one that read ask.
- The knowledge step, before anyone is asked:
  - a script groups the round's open questions, because the same question often comes from several plays, and adds the issue's memory updates still waiting;
  - the knowledge-builder agent, in one dispatch, confirms the groups, searches the loop's sources and then memory for each group, through the memory tool, and names the source of what it uses;
  - it closes each group one way: a screen the source should show becomes a note for the prototype; what research can answer becomes a drafted knowledge page, raised as a memory update for a person to approve; what the context settles is settled, with why; what only the person can confirm gets our proposed answer, with its basis and its context;
  - it has the brief written and rendered by a script, never by hand.
- A script checks the knowledge step. When the check is not clean, its report goes back to the agent at most twice; a step still not clean halts the loop.
- The brief. The loop shows it as it is and waits for a typed reply. A yes takes every proposal and every recommendation shown. The person may instead correct a gap, a settled point or a page by its id.
- The reply. A script checks it decides every gap and every page, and records it in the issue's short-term memory as the person's, with what each accepted proposal rested on. It maps each answer back to the questions it closes, play by play, so the next round's plays read it like any other answer. Each page decision is recorded through the memory tool; an approved page is not yet promoted.
- Stop. The person may type stop instead. The loop then closes halted, with the reason that it stopped at a question, and the questions it left open stay in the run's records under the issue.
- The brief never stops a person: a yes always takes the loop on, and stop always ends it.
- Examples, in different kinds of project:
  - In a clinic's booking app, three plays each ask who may cancel a booking. The step groups them into one gap, proposes an answer from what the prototype's screens show, and the product owner types yes.
  - In a shop's checkout project, the brief proposes how fast a payment must be confirmed. The product owner corrects that gap by its id with their own figure, and the next round's plays read it.
  - In a team's planning tool, the brief lists a knowledge page drafted from research. The product owner rejects the page and types stop, and the loop closes halted.
- How it meets the capability: "until the goal is met" does not mean asking the person at every step: the loop asks only what none of its plays, its memory or approved research could close, in one brief, and the person can always stop it.

Status: built, in the Shared Loop Run's knowledge step and brief, the knowledge-builder agent and the skills it calls, and three scripts. Not built, or open:
- A yes takes every proposal and every page at once. The loop principles name this as a gap.
- Only the Discovery loop runs this step today, because it is the only loop built, and its grouping of questions is written for questions about a product, such as its speed or its proof.
- An approved knowledge page is not promoted by the loop; a person promotes it later.

## Inputs / Outputs
- In: the round record that read ask, with the open questions and the issue's memory updates still waiting.
- In: each play's file of open questions.
- In: the loop's sources, such as a prototype's views and journeys.
- In: the person's typed reply to the brief: yes, corrections by id, or stop.
- Out: the question groups; the search, build and brief records; the brief as the person reads it; and the step's check.
- Out: knowledge pages raised as memory updates, waiting for a person.
- Out: the person's answers in the issue's short-term memory, mapped to each play's questions, and each page decision.
- Out: the next round's contract with those answers, or a halted close with the reason that the person stopped.

## Rules & behavior
- A question one play cannot answer is the loop's, not a stop. The reason: "The other plays, and the next round, may answer it."
- Ask only after a round that closed nothing new, or at the round limit. The reason: the loop asks "only what none of its plays, no memory and no approved research can answer", and "It does so after a round that answered nothing new, or at its round limit."
- Close what can be closed before asking. The reason, in the product owner's words: "asking 80 questions and then building memory doesn't seem realistic."
- One step, run by one agent. The reason: three plays for this work meant "three pre-flights, three loop-contract checks, three stop conditions and three closes, for one agent's job."
- A brief, never a questionnaire. The reason: the loop reaches the person "once per stop", "with a brief, never a questionnaire", so every question is about a draft the person can see.
- Nothing from the model alone. The reason: "Nothing from the model or the web is used before a person approves it", and a knowledge page waits: "nothing in them is used before approval".
- A step that cannot get clean is halted, never passed. The reason: "still not clean halts the loop".
- The reply must decide the whole brief. The reason: a reply that "leaves a gap or page undecided" is refused, so no gap is closed by silence.
- The answers reach the plays on the next round. The reason: the record maps each one back "so the next round's plays read them".
- The person may type stop. The reason: the loop "never picks an answer for itself", so the person must always be able to end it instead of answering.
- An agent never decides a memory update for a person. The reason: "An agent never decides a memory update."
- Not decided: whether one typed yes may still take every proposal and every page in the brief.

## Acceptance criteria
- Given a round that read again, when the loop goes on, then the person is not asked anything.
- Given a round that read ask, when the loop reaches the person, then the knowledge step ran first and its check reads clean, and the person sees the brief, never a bare question.
- Given the same question asked by three plays, when the questions are grouped, then they form one group and one gap in the brief.
- Given the person types yes, when the reply is recorded, then every gap takes our proposed answer and every page its recommendation, each answer is in the issue's short-term memory as the person's, and the next round's contract holds them.
- Given the person corrects one gap by its id, when the reply is recorded, then that gap holds the person's own answer.
- Given a reply that leaves a page undecided, when it is recorded, then it is refused.
- Given the person types stop, when the reply is read, then the loop closes halted with the reason that it stopped at a question.

## Out of scope
- Deciding after each round whether to go again or ask. Run any loop the same way (fn-run-loop) does it.
- What a memory update holds, its approval, and promoting a page to Garura or Phoenix memory. Memory, in Standards, structure, settings and memory (BI-10), owns them.
- The questions each play asks, and how it answers them from its sources. The transition intents, Product → Spec (BI-1), Spec → Design (BI-2), Design → Code (BI-3), Code → Validation (BI-4), Validation → Run (BI-5) and Run → Product (BI-6), own each loop's plays.
- The person's review of what the loop made, at its end. Review what agents make (Argus), in Developer tooling (BI-8), owns it.
- A way past a gate, and the one record of what is owed. Give every gate a way past owns them.

## Sources
- The product owner on 2026-11-10: "Run plays as loops: A person gives one goal, and a loop runs its plays until the goal is met."
- core/components/loops/_shared/loop-run.md, lines 151-183 and 258-350: "A question one play cannot answer is the **loop's** question, not a stop", "once per stop", "with a brief, never a questionnaire", "still not clean halts the loop", "an approved page is not yet promoted — a person promotes it later", "The person may type **stop**", "stopped_at_question"
- core/components/loops/complete-discovery/scripts/group_questions.py, lines 1-30: "the same business proof once per intent and once per play"
- core/components/loops/complete-discovery/scripts/record_review.py, lines 1-34: "so the next round's plays read them", "leaves a gap or page undecided"
- core/components/loops/complete-discovery/scripts/check_knowledge.py, lines 1-8: "This script checks the three records mechanically"
- core/components/loops/complete-discovery/scripts/round_state.py, lines 1-25: "The loop asks the person only what no play of the loop can answer."
- docs/adr/029-drives.md, line 36: "It never picks an answer for itself."
- docs/adr/041-a-drive-runs-in-rounds-and-owns-its-questions.md, the product owner on 2026-10-20, lines 20, 41-43, 52, 78 and 91: "asking 80 questions and then building memory doesn't seem realistic.", "The other plays, and the next round, may answer it.", "only what none of its plays, no memory and no approved research can answer", "It does so after a round that answered nothing new, or at its round limit.", "nothing in them is used before approval", "An agent never decides a memory update.", "Nothing from the model or the web is used before a person approves it"
- docs/adr/059-the-discovery-loops-knowledge-step-is-one-step-run-by-one-agent.md, lines 28-29: "three pre-flights, three loop-contract checks, three stop conditions and three closes, for one agent's job."
- docs/components/loops.md, line 57: "which invites cognitive surrender"
- standards/rules/loop-contract.md, in Phoenix memory, lines 84-99: "never picks an answer for itself"
- The stock-take of Orchestration (2026-11-10), sections 2.1, 5 and 11 (lean 4): the knowledge step and the brief, and the stop at the round limit.
