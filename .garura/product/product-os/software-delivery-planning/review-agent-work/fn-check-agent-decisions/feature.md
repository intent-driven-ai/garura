# Feature: Check each agent decision against the memory it rested on

## What it does
In the Agent decisions section of Argus, the person reads every decision an agent made, grouped by play with the problems first, each with its trace: the steps the agent took, in order, each with what it looked for, what it found and its source shown in its place, the lines around it numbered and the lines the agent used marked, and whether that source still says the same; the person marks each decision as looking right, or sends it back so the agent decides again from memory as it is now.
- An agent decision is one choice an agent made from memory, such as how a product's shoppers sign in. Its trace is the steps that led there, each resting on memory lines.
- Each step's source is checked again and shows one of four states: the same, changed (with what the lines say now, in their place), gone, or no source. A decision with no trace at all is flagged.
- A decision that came from an approved memory update also shows what was missing, who approved it and their words.
- The source is shown as its memory, file and lines: the one exception to the plain-words rule, "because the person must check it". The fingerprint, the memory version and the ids sit in a fold, because "they are for the check, not for the person's judgement".
- Argus never reads the memory tool's answers itself. Garura turns each answer into pieces of the review pack.
- The person gives each decision one of two answers:
  - Looks right: "The decision stands as it is."
  - Send back: "The agent decides again, from memory as it is now."
- Examples, in different kinds of project:
  - A shop's checkout: the decision on how shoppers sign in rests on four steps, the product's profile, the domain that covers sign-in, its security level and the knowledge lines those select; all four still say the same, and the person marks it as looking right.
  - A clinic's booking app: one step's source changed since the decision was made, so it shows first, with the old lines and the lines now, and the person sends it back.
  - A team's planning tool: a decision with no trace is flagged at the top.
- How it meets the capability: "agent decisions" are one of the things the widened line names, and they show what the agents' work rests on.

Status: not built. What exists is the data it shows: an agent's decision is recorded with its trace (`cite`), and the check reads every step's source again and names each problem by its step (`citations --check`); inside a loop, a play's review record can carry each of its decisions with their traces.

## Inputs / Outputs
- In: the decision records of the run's issue, with their traces, and the memory tool's check of every step's source, turned by Garura into pieces of the review pack.
- In: for a decision from an approved memory update, that update's record.
- In: the person's answer on each decision, looks right or send back.
- Out: for a send-back, the decision handed back to the agent's play to decide again from memory as it is now.
- Out: for looks right, the answer kept, and nothing else written.

## Rules & behavior
- Every step is shown in its place, with the lines around it. The reason, in the product owner's words: "the source should show a few lines before and after".
- Every step's source is checked again, and problems come first. The reason: "The check names the step whose source changed or is gone.", and "Grouped by play, problems first."
- Argus reads no memory itself; Garura builds the pieces. The reason: reading the memory tool's answers in the page "would put the memory tool's words and contract inside the review tool, across the extraction line".
- A send-back has the agent decide again from memory as it is now; it never takes the person's own answer as memory. The reason: "Nothing from the model or the web is used without a memory update a person approved".
- Not decided: what a person's answer on an agent decision writes beyond that, since only the review step writes approval.

## Acceptance criteria
- Given a decision whose four steps' sources are unchanged, when the person opens it, then each step shows what it looked for, what it found and its source in place, with the used lines marked, and all four read the same. This is not built.
- Given a decision one of whose sources changed, when the section opens, then that decision is listed first, and the step shows the old lines and the lines now. This is not built.
- Given a decision with no trace, when the section opens, then it is flagged. This is not built.
- Given the person sends a decision back, when the agent decides again, then its new trace rests on memory as it is now. This is not built.

## Out of scope
- Recording a decision and its trace, and checking its sources. Memory, in Standards, structure, settings and memory, owns them.
- Approving a memory update. See what memory holds, and approve or reject each memory update that waits for a person (fn-review-memory) does it.
- Applying the answers in one commit. Finish the review and have every answer applied in one commit (fn-apply-answers) does it.

## Sources
- docs/adr/037-agent-decisions-keep-a-trace-and-the-review-tool-has-five-sections.md, with the product owner's words of 19 October 2026: "the source should show a few lines before and after", "The check names the step whose source changed or is gone.", "A decision with no trace is flagged.", "How do shoppers sign in?", "Nothing from the model or the web is used without a memory update a person approved"
- The review tool's design: "because the person must check it", "they are for the check, not for the person's judgement", "Grouped by play, problems first.", "would put the memory tool's words and contract inside the review tool, across the extraction line"
- The review tool's mockup: "The decision stands as it is.", "The agent decides again, from memory as it is now."
- core/tools/memory/README.md: "Records a decision and its trace in the issue's short-term memory", "reads every step's source again"
- core/components/plays/create-play/references/write_loop_review.py: "the record then carries every decision the play made, each with its trace"
- The lean the product owner agreed on 2026-11-10: "its line is widened to name business intents and agent decisions"
