# Feature: Let only a person decide a memory update, one at a time

## What it does
When no tier of memory answers, an agent drafts the answer as a memory update in the issue's short-term memory, and only a person approves or rejects it, one update at a time, with their exact reply on record, so nothing from the model or the web enters memory, or is used, without a person.
- An agent raises an update with `propose`. It holds what is missing, the drafted entry, where the draft came from (a person, the web, the model or memory), its sources, who asked for it, and whether it blocks the work.
- Every update goes to the issue's own short-term memory. Its target must be in that issue's folder, and never in the folder where the updates themselves are kept.
- An update moves through four states: waiting, then approved or rejected, then applied.
- A person decides each update with `decide`: approve or reject, who decided, their exact reply, and where they decided, in the review tool or in a session. Until the cards of Argus are built, the person types the decision in a Claude Code session that records their exact reply.
- A person decides an update once. A second decision on the same update is refused.
- `apply` writes an approved update to its target in the issue's short-term memory. It refuses an update no one approved, and it refuses one whose target changed after the update was raised.
- The work goes on while an update waits, unless it cannot go on without it. Then the update says it blocks, and the agent stops.
- No lookup finds an update that waits, and no agent decides from one.
- Today, through the tool: 13 updates applied, 5 waiting and 1 rejected. The oldest waiting update was raised on 2026-10-24. Three of the five ask where the rule for asking a person lives, which ADR 054 later settled as a shared file.
- Examples, in different kinds of project:
  - In a shop's checkout service, an agent drafts from the web how long a guest's cart is kept, marks the update as blocking, and stops. The product owner approves it with "yes, thirty days, as our policy says", and the answer is written to the issue's short-term memory.
  - In a clinic's booking app, an agent drafts with the model how long a reset link lasts. The product owner rejects it with "ask our security lead first"; nothing is written, and the work that waits on it stays stopped.
  - In a news site's publishing tool, an agent raises an update that does not block. It goes on with the rest of the work, and the person decides the update a day later.
- How it meets the capability: "people control what enters them" is this feature: nothing a model or a web page drafted enters memory until a person says so, one update at a time.

Status: built, in the memory tool's `propose`, `updates`, `decide` and `apply`; built under #658 (closed, an agent raises a memory update a person approves) and #662 (closed, which added deciding in a session); decided in ADR 035 and ADR 036. Not built, or open:
- Nothing reminds anyone of an update that waits, and an update has no end date. Five wait today; the oldest has waited since 2026-10-24.
- The cards where a person decides each update in the Memory section of Argus are not built (#664, the Memory and ADRs section); a person types the decision in a session.
- The tool records the name it is given; it does not check that the one who decides is a person.

## Inputs / Outputs
- In: from an agent: the issue, what is missing, the drafted entry, where the draft came from, its sources, who asks, and whether it blocks.
- In: from a person: approve or reject, their name, their exact reply, and where they decided.
- Out: the update, kept as one file in the issue's short-term memory, with its state.
- Out: for an approved update, its entry written to its target in the issue's short-term memory, with a fingerprint of what was written.
- Out: the list of updates, all of them or those in one state.

## Rules & behavior
- Only a person decides, one update at a time. The reason: "Only a person decides, one update at a time."
- Nothing in an update is used before a person approves it. The reason: "Nothing in it is used until a person approves it."
- Every update goes to the issue's short-term memory. The reason: "A draft from the web or the model never goes straight to Garura or Phoenix memory."
- A person decides an update once. The reason: the tool refuses a second decision because "a person decides an update once."
- An update no one approved is never written. The reason: "only an update a person approved is written."
- An approved update is not written over a target that changed. The reason: the tool answers that the target "changed after the update was proposed; propose again from the current text."
- The work goes on unless the update blocks it. The reason: "Your work goes on while the update waits, unless you cannot go on without it."
- No agent decides from an update that waits. The reason: "Never decide from another issue's short-term memory, from a waiting memory update, or from an earlier decision record."
- The person's own words are kept. The reason: `decide` records "a person's word on a waiting update: approve or reject, who, their exact reply, and where they decided".
- Not decided: whether an update that waits gets a reminder or an end date, and who is reminded.
- Not decided: whether the tool itself checks that the one who decides is a person, or the memory guide and Argus alone hold that rule.

## Acceptance criteria
- Given no tier answers, when an agent raises an update, then it is waiting in the issue's short-term memory, with what was asked exactly as given.
- Given an update whose target is in another issue's folder, when it is raised, then the tool refuses it.
- Given a waiting update, when a person approves it with their words, then it reads approved, with that person, their exact reply and where they decided.
- Given an approved update, when a second decision is sent, then the tool refuses it.
- Given a waiting or rejected update, when it is applied, then nothing is written and the answer is `not_approved`.
- Given an approved update whose target changed after it was raised, when it is applied, then nothing is written and the answer is `changed`.
- Given a waiting update, when an agent searches memory for its text, then the search does not return it.
- Given an update that has waited a week, when the person opens their work, then they are reminded of it. This is not built.

## Out of scope
- The card where a person approves or rejects an update, and Ask memory. Review what agents make (Argus), in Developer tooling, owns them.
- Moving an approved answer up to Garura memory or Phoenix memory. Move a page up a tier on a person's yes, and choose what is learned (fn-promote-page) does it.
- Finding memory, and the cue to raise an update. Find memory across three tiers through one tool (fn-find-memory) does it.
- When a loop reaches the person with the updates its knowledge step raised. Run plays as loops, in Orchestration, owns it.
- The way past an update that blocks, and where what is owed is kept. Give every gate a way past, in Orchestration, owns them.

## Sources
- .garura/project/issues/1021/context/capabilities.md, line 114, the list set on 2026-11-11: "people control what enters them"
- core/tools/memory/README.md, lines 134-139 and 143-151: "Nothing in it is used until a person approves it.", "a person's word on a waiting update: approve or reject, who, their exact reply, and where they decided", "Only a person decides, one update at a time.", the four states, and "the person types the decision in a Claude Code session that records their exact reply"
- core/tools/memory/updates.py, lines 88-93, 114-115, 128-129 and 130-132: the target in the issue's own folder, "a person decides an update once.", "only an update a person approved is written.", "changed after the update was proposed; propose again from the current text."
- core/tools/memory/GUIDE.md, lines 57-58 and 87-88: "Your work goes on while the update waits, unless you cannot go on without it.", "Never decide from another issue's short-term memory, from a waiting memory update, or from an earlier decision record."
- docs/adr/036-approved-answer-lands-in-short-term-memory.md, section 2, line 50: "A draft from the web or the model never goes straight to Garura or Phoenix memory."
- docs/adr/035-agents-work-only-from-memory.md, section 5: when no tier answers, an agent raises a memory update, and nothing in it is used until a person approves it.
- The memory tool's list of memory updates, 2026-11-11: 13 applied, 5 waiting, 1 rejected; the oldest waiting update, mu-20261024-001 of #844, raised on 2026-10-24.
- docs/adr/054-the-last-deprecated-parts-are-deleted-and-the-asking-rule-is-a-shared-skill-file.md: the rule for asking a person is a shared file.
- GitHub #658 and #662 (closed): updates, and deciding in a session; #664 (open): the Memory and ADRs section of the review tool.
- .garura/product/product-os/software-delivery-planning/review-agent-work/fn-review-memory/feature.md: the card where the person decides; the examples of the cart and the reset link follow its own.
- The stock-take, .garura/project/issues/1021/context/bi-10-inventory/inventory.md, sections 5.2 and 9.
