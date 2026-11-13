# Feature: Move a page up a tier on a person's yes, and choose what is learned

## What it does
A page moves up a tier, from an issue's short-term memory to the project's Garura memory, only when a person says yes to it in the Memory section of Argus, and what Run → Product learned is proposed there for that person to choose, so an answer one issue found can reach the next issue without anyone copying it by hand. Nothing moves from a project to Phoenix memory.
- A promotion moves a page up a tier. "A person makes it on purpose, outside the work". It is the only way a page an issue found reaches Garura memory.
- Every memory write goes to the issue's short-term memory first: a person's answer to a question, and an approved memory update. Until an answer is promoted, another issue does not find it, "and may ask again. That is expected."
- What may enter each tier: short-term memory takes the issue's own work and its approved updates; Garura memory takes what `initialize` builds for the project from Phoenix memory, the product model its own plays write, and a promotion a person said yes to; Phoenix memory is not changed from a project: moving a page to it is not designed, needs an organisational change, and is to happen outside Garura.
- Who does what, in the product owner's answer of 2026-11-11: moving a page up and choosing what is learned are this capability's, on a person's yes; the person gives the yes in the Memory section of Argus, in Developer tooling, for a move to Garura memory only: "Argus can only allow from short term to the project memory."; and Run → Product proposes what was learned.
- Today a promotion is by hand. No play or command of the tool moves a page up a tier. The tool names "/learn-memory and /promote-memory plays", and the glossary marks the promotion play "not built yet". Into Phoenix memory, "Promotion today is a manual copy, commit and push into another repository".
- What is planned around it, in open issues:
  - The Learn loop's recipe is still to be decided, with two plays: "`/learn` — take what was learned from short-term memory into Garura memory." and "`/promote` — send it from Garura memory to Phoenix memory."
  - The Memory and ADRs section of Argus is to let a person approve a memory update on a card in Argus, and write it to its tier: "the issue's short-term memory for a researched answer, Garura or Phoenix memory for a promotion."
  - The tool's contract already shapes an update applied to Phoenix memory, which "carries its commit"; today `propose` takes only short-term memory.
- Examples, in different kinds of project:
  - In a clinic's booking app, an approved answer on how long a reset link lasts sits in one issue's short-term memory. The product owner says yes to it in Argus, and it moves to the project's Garura memory, where the next issue finds it.
  - In a shop's checkout service, Run → Product learns from support tickets that guests drop out at the address form. It proposes the learning; the product owner chooses to keep it in the project's Garura memory, and not to send it up to Phoenix memory.
  - In a bank's payments service, a rule on how refunds are named has proved itself in one issue. The technical lead says yes to it in Argus, and it moves to the bank's Garura memory; it does not go to Phoenix memory, which no project changes.
- How it meets the capability: "people control what enters them" holds for the higher tiers only when nothing moves up without a person's yes.

Status: not built. Named in ADR 036 section 3 and in the glossary. Planned around it: deciding the Learn loop's recipe (learn into Garura memory, promote to Phoenix memory, find drift) and the Memory and ADRs section of the review tool.

## Inputs / Outputs
- In: a page in an issue's short-term memory, such as an approved memory update or a person's answer.
- In: what Run → Product learned and proposes to keep.
- In: the person's yes or no, with their words, given in the Memory section of Argus.
- Out, on a yes: the page in the project's Garura memory, with a record of who said yes and their words.
- Out, on a no: nothing moves, and the no is recorded.

## Rules & behavior
- Only a person promotes. The reason: "A person approves every promotion."
- A promotion is its own step, outside the work. The reason: "It happens outside the piece of work, as its own memory update that a person approves."
- Memory is written low and moved up on purpose. The reason, in the product owner's words, recorded in ADR 039: "memory, when written, will always go into STM, and it needs to be consciously promoted up."
- Nothing is promoted on its own. The reason: Run → Product must not "Change an intent, or promote memory, without a person."
- Nothing moves from a project to Phoenix memory. The reason, in the product owner's words: "Going to the Phoenix is not designed yet. That would need an organizational change."
- Argus takes the person's yes for a move to Garura memory only. The reason, in the product owner's words: "Argus can only allow from short term to the project memory."
- Not decided: whether a promotion is a play, a command of the memory tool, or a memory update aimed at Garura memory.
- Not decided: how a move to Phoenix memory is designed, and which product outside Garura makes it.
- Not decided: how the Memory section of Argus shows a page that waits for a person's yes to move to Garura memory, beside the updates that wait.

## Acceptance criteria
- Given an approved answer in one issue's short-term memory, when the product owner says yes to promoting it, then it is in Garura memory and the next issue's lookup finds it there. This is not built.
- Given a page in a project's Garura memory, when anyone in the project tries to move it to Phoenix memory, then nothing moves. This is not built.
- Given a learning that Run → Product proposes, when the product owner says no, then nothing moves and the no is recorded. This is not built.
- Given no person's yes, when anything tries to move a page up a tier, then nothing moves. This is not built.

## Out of scope
- The card and the person's yes or no. Review what agents make (Argus), in Developer tooling, owns it.
- Proposing what was learned in use and in the market. Run → Product owns it.
- Deciding a memory update in the issue's short-term memory. Let only a person decide a memory update, one at a time (fn-person-decides-update) does it.
- Keeping Phoenix memory in step with Garura's source. Keep Phoenix memory in step with Garura's source, versioned per release with its notes (fn-phoenix-in-step) does it.
- Building a project's own Garura memory from Phoenix memory. Set a project up after the install (Initialize), in Install and distribute, owns it.
- When a loop reaches the person with what its knowledge step raised. Run plays as loops, in Orchestration, owns it.
- Moving a page to Phoenix memory. It is not designed, needs an organisational change, and another product, outside Garura, is to own it.

## Sources
- The product owner's answer as recorded (2026-11-11): "6, moving a page up a tier and choosing what is learned are Memory's, on a person's yes, decided in Argus's Memory section, with BI-6 proposing what was learned"; "choosing and promoting learnings to Garura or Phoenix memory (left to the review of Memory, in Standards, structure, settings and memory)"; "people control what enters them"
- core/grounding/glossary.md, lines 37, 38 and 41: Garura memory is "filled by `initialize` and promotion; written as work only by plays built to write the product model", Phoenix memory is "changed only by promotion", and a promotion: "A person makes it on purpose, outside the work", "`/promote-memory` (not built yet)", "The only way Garura and Phoenix memory change"
- core/tools/memory/README.md, lines 152-154 and 197-199: "and may ask again. That is expected.", "carries its commit."
- core/tools/memory/updates.py, lines 7-8 and 96: "/learn-memory and /promote-memory plays"; `propose` sets the target tier to short-term memory.
- README.md, in Phoenix memory, lines 6 and 9, read through the memory tool: "What a project learns moves up a tier at a time", "A person approves every promotion. Every change here is a commit.", "No client, organisation or personal references."
- docs/adr/036-approved-answer-lands-in-short-term-memory.md, section 3, line 56: "It happens outside the piece of work, as its own memory update that a person approves."
- docs/adr/039-memory-writes-go-to-short-term-memory-plays-read-no-memory.md, section 1, line 46, the product owner's words: "memory, when written, will always go into STM, and it needs to be consciously promoted up."
- .garura/product/product-os/intents/bi-6.md, line 13: "Change an intent, or promote memory, without a person."
- .garura/product/product-os/software-delivery-planning/review-agent-work/fn-review-memory/feature.md, line 31: "Moving memory up is not done here"; and review-agent-work/capability.md, line 88: "what a memory update is, who may decide it, and moving memory up. Memory, in Standards, structure, settings and memory, owns them."
- .garura/product/product-os/software-delivery-planning/run-plays-as-loops/fn-brief-open-points/feature.md, line 63: "What a memory update holds, its approval, and promoting a page to Garura or Phoenix memory. Memory, in Standards, structure, settings and memory (BI-10), owns them."
- .garura/product/product-os/software-delivery-planning/initialize/fn-883/feature.md, line 59: "promoting a person's answer or an approved memory update from a project up to Phoenix memory: Memory owns them, because both change what every project on the machine draws from."
- The stock-take (2026-11-11), sections 5.5, 5.8, 7.5 and 10, item 8.
- The product owner's words of 2026-11-11: "Argus can only allow from short term to the project memory. Going to the Phoenix is not designed yet. That would need an organizational change."
