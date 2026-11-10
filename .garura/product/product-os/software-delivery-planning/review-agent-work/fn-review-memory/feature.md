# Feature: See what memory holds, and approve or reject each memory update that waits for a person

## What it does
In the Memory section of Argus, the person sees what memory holds, the project's Garura memory and, once they pick an issue, that issue's short-term memory, and approves or rejects, one at a time and in their own words, each memory update that waits for a person; Garura then records the decision through the memory tool, and an approved update is written to its issue's short-term memory. Ask memory, a question box in plain words over the three tiers, is designed and only mocked.
- A memory update is an answer an agent drafted when no tier of memory held it. It waits for a person, and nothing in it is used before a person approves it.
- Each update shows on its own card: the issue, what was missing, the drafted entry, where the draft came from (the person, the web, the model or memory), its sources, and whether it blocks the work.
- The two answers, each needing the person's own words:
  - Approve: "Garura writes it to the issue's short-term memory."
  - Reject: "Nothing is written. Work that waits on it stays stopped."
- Ask memory: the person asks in plain words, and "the answer comes with the memory it came from". Underneath it is the same memory tool the agents use, which finds, searches and reads, with no index. It is mocked only: "no need to build this whole this now".
- Examples, in different kinds of project:
  - A shop's checkout: an update on how long a guest's cart is kept, drafted from the web, blocks the work; the product owner approves it with "yes, thirty days, as our policy says".
  - A clinic's booking app: an update on how long a reset link lasts, drafted by the model, is rejected with "ask our security lead first", and the work that waits on it stays stopped.
  - A school's timetable app: the person picks an issue and reads what its short-term memory holds, before they answer.
- How it meets the capability: "memories" are one of the things people review in the one tool, and Memory's own line says "people control what enters them".

Status: not built (#664). What exists is the memory tool's side, which already keeps each update and records a person's word on it: it raises an update (`propose`), lists them (`updates`), records the decision (`decide`), naming where it was made, "`review-tool`, or `session`", and writes an approved one (`apply`). Until Argus exists, "the person types the decision in a Claude Code session that records their exact reply". The story's text is behind the design: it writes an approved update to "Garura or Phoenix memory for a promotion", while the design says "Moving memory up is not done here".

## Inputs / Outputs
- In: the memory updates that wait for a person, and what Garura memory and the picked issue's short-term memory hold, turned by Garura into pieces of the review pack.
- In: the person's answer on each update, approve or reject, with their words.
- In, once built: a question in plain words for Ask memory.
- Out: for each update, the person's decision recorded through the memory tool, with who, their exact words, and that it was decided in the review tool.
- Out: for an approved update, the update written to its issue's short-term memory.
- Out, once built: an answer to the question, with the memory it came from.

## Rules & behavior
- One update at a time, each with the person's own words. The reason: "Only a person decides, one update at a time.", and "Nothing is approved in bulk, and an agent never answers one".
- Memory's rules decide what an answer does; Argus only takes it. The reason: the memory tool records the decision and writes the update, and Memory's line is that "people control what enters them".
- An approved update goes only to its issue's short-term memory. The reason: "STM - always STM".
- Nothing moves up to Garura memory or Phoenix memory from here. The reason: "Moving memory up is not done here".
- Ask memory uses the same memory tool as the agents, with no index; only the question is in plain words. The reason, in the product owner's words: "the same tool under both, just that the interface for tool should be nlp".
- Not decided: whether the Memory section lists Phoenix memory as well, or reaches it only through Ask memory.

## Acceptance criteria
- Given a memory update that waits for a person, when the review opens, then its card shows what was missing, the draft, where it came from, its sources and whether it blocks. This is not built.
- Given the person approves it with their words, when the answer is applied, then the memory tool shows it approved by that person, with their exact words, decided in the review tool, and the update is in its issue's short-term memory. This is not built.
- Given the person rejects it, when the answer is applied, then nothing is written to memory, and the work that waits on it stays stopped. This is not built.
- Given two updates, when the person tries to approve both at once, then the page does not allow it. This is not built.

## Out of scope
- What a memory update is, who may decide it, and moving memory up. Memory, in Standards, structure, settings and memory, owns them.
- The trace of each agent decision. Check each agent decision against the memory it rested on (fn-check-agent-decisions) covers it.
- Applying the answers in one commit. Finish the review and have every answer applied in one commit (fn-apply-answers) does it.

## Sources
- .garura/project/issues/617/specs/review-tool.md, the design, with the product owner's words: "the answer comes with the memory it came from", "no need to build this whole this now", "the same tool under both, just that the interface for tool should be nlp", "STM - always STM", "Nothing is approved in bulk, and an agent never answers one", "Moving memory up is not done here"
- .garura/project/issues/617/specs/review-tool-mockup.html: "Garura writes it to the issue's short-term memory.", "Nothing is written. Work that waits on it stays stopped."
- core/tools/memory/README.md: "`review-tool`, or `session`", "Only a person decides, one update at a time.", "the person types the decision in a Claude Code session that records their exact reply"
- docs/adr/037-agent-decisions-keep-a-trace-and-the-review-tool-has-five-sections.md: "It is mocked only for now."
- GitHub #664 (open): "Garura or Phoenix memory for a promotion"
- The list set on 2026-11-10, in .garura/project/issues/1021/context/capabilities.md: "people control what enters them"
