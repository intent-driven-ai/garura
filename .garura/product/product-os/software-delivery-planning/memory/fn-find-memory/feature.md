# Feature: Find memory across three tiers through one tool

## What it does
An agent finds what it needs to decide with one memory tool, which looks in the issue's short-term memory, then Garura memory, then Phoenix memory, stops at the first tier that answers and gives every answer its tier, file, lines and fingerprint, so every agent finds memory the same way and every decision can name what it rested on.
- The tool has four commands to find memory: `health` reports each tier, reachable or not, and its version; `find` finds files by a name pattern; `search` searches the text of files and returns each hit with its tier, file and line; `read` reads exact lines of one file and returns them with a fingerprint of that text.
- The lookup order is short-term memory, then Garura memory, then Phoenix memory. Inside Garura memory, the project's memory folder answers before its product model. The lookup stops at the first tier that answers.
  - A request may ask one tier only, or every tier; with every tier, the answer still names the first tier in the order that has a result.
  - A lookup never skips a tier. A tier with no setting, or one the tool cannot reach, is the error `tier_missing`, never "nothing found".
  - An empty answer, after every tier was looked in, is the cue to raise a memory update.
- Short-term memory is only the folder of the issue the lookup names. A read of another issue's folder, or a path that steps outside its tier, is refused. A lookup with no issue starts at Garura memory.
- Phoenix memory is read only at its approved version, and the tool never copies a file from it into the project.
- A lookup never finds an update that waits for a person, or a decision record.
- The tool takes the place of each tier from its settings, never from a fixed path. It works on folders today; a server engine is one setting away, and the agents do not change when it comes.
- It finds memory the way Claude Code searches: it finds files, searches their text and reads exact lines, with no index.
- What is not memory: the record of past checkpoint answers, which is a checkpoint tool, and a play's own working files, which its steps read and write directly.
- Examples, in different kinds of project:
  - In a clinic's booking app, the developer's agent searches for how long a password reset link lasts. The issue's short-term memory and Garura memory have nothing, and Phoenix memory's user-management page answers, with its lines and fingerprint.
  - In a bank's payments service, the project's Garura memory holds its own rule on retrying a failed payment, so the lookup stops there and never reaches Phoenix memory.
  - In a game studio's build, Phoenix memory's place on a new machine is empty and its source does not answer. The lookup answers `tier_missing` for Phoenix memory, and the agent says so instead of deciding.
- How it meets the capability: "Agents decide from three tiers of memory" only when every agent reaches all three the same way, in the same order, and every answer says where it came from.

Status: built, in the memory tool (contract version 5) and its memory guide, which the install lays for every agent; built under #657 (closed, the memory tool finds memory across the three tiers) and #661 (closed, plays read memory only through the tool), under #653 (open, the memory system). Not built, or open:
- In this repository Garura memory has no memory folder, so it is only the product model: "In this repository that folder was removed on 2026-10-26" (#942, a project's memory can be managed).
- The server engine is not built: the folder engine is "the only engine built". Moving the tool's home to a server is one setting once a server exists.
- Ask memory, a question box in plain words over the three tiers, is mocked only, in Review what agents make (Argus).

## Inputs / Outputs
- In: a request from an agent: the command, the issue the work is on when there is one, and a name pattern, a text pattern or a path with its lines; and, when asked, one tier or every tier.
- In: the tool's settings: where each tier lives, Phoenix memory's source and its approved version.
- Out: one answer per request, as one line of JSON: the tiers looked in, the tier that answered, and each hit or text with its tier, file, lines and fingerprint, and, for Phoenix memory, its version.
- Out: an error the agent must name, such as `tier_missing` or a refused request, never an answer that hides it.

## Rules & behavior
- A lookup stops at the first tier that answers. The reason: "So the lowest tier answers whenever it can, and Phoenix memory is reached only when the lower tiers have nothing."
- Short-term memory is the named issue's only. The reason, in the product owner's words, recorded in ADR 036: "When a short-term memory is looked up, it is looked up only in the current issue, not the other issues. That is critical."
- A lookup never skips a tier, and a tier that cannot be reached is said. The reason: "A lookup never skips a tier.", and "`tier_missing` means a tier cannot be reached. Say so."
- Phoenix memory is read only at its approved version. The reason: "Working-tree edits and unmerged commits are never read."
- Nothing is copied from Phoenix memory. The reason: "The tool reads Phoenix memory and never copies a file from it into the project", and, in the product owner's words, "You don't need to copy the entire file."
- A waiting update and a decision record are never found. The reason: "a draft is used only once a person approved it and it was applied", and "an agent never decides from its own earlier decision".
- The places come from settings, never from fixed paths. The reason: "The tool learns where each tier lives from its settings, never from a fixed path."
- One tool, so the agents do not change when memory moves. The reason: "Agents that call it do not change when that happens, because they only ever talk to this tool".
- The search has no index. The reason, in the product owner's words: "this is critical as this is why claude-code is so good".
- Every answer carries its source. The reason: every piece of text the tool returns "carries its tier, file, lines and fingerprint."

## Acceptance criteria
- Given a search with an issue, when short-term memory has nothing and Garura memory has a hit, then the answer names Garura memory as the tier that answered, and Phoenix memory is not looked in.
- Given a read of a path in another issue's short-term memory, when the request names the issue it works on, then the tool refuses it with `bad_request`.
- Given a Phoenix memory place that is empty and a source that does not answer, when a search reaches Phoenix memory, then the answer is `tier_missing` for Phoenix memory, with the reason.
- Given a file in Phoenix memory edited on disk and not merged, when it is read, then the tool returns the text at the approved version.
- Given an update that waits for a person, when a search matches its text, then the search does not return it.
- Given a read of exact lines, when the tool answers, then the text comes with its tier, file, lines and a fingerprint of that text.
- Given a server for memory, when the tool's engine setting names it, then the agents find memory with no change to them. This is not built.

## Out of scope
- Raising a memory update and a person's decision on it. Let only a person decide a memory update, one at a time (fn-person-decides-update) does it.
- Recording a decision with its trace. Keep each decision's trace and check its sources (fn-keep-decision-trace) does it.
- Copying what a skill needs into short-term memory, and the checks that no part reads memory by a path. Make every agent read memory only through the tool, and fail a part that names a memory path (fn-read-through-tool) does it.
- Downloading Phoenix memory to the machine and keeping it current. Bring Phoenix memory to a machine and keep it current (fn-bring-phoenix) does it.
- Laying the tool, its settings and its guide in a project. Install into a project, in Install and distribute, owns it.
- What each setting of the tool means, and where settings files live. Settings, in Standards, structure, settings and memory, owns it.
- Ask memory, the question box in plain words. Review what agents make (Argus), in Developer tooling, owns it.

## Sources
- .garura/project/issues/1021/context/capabilities.md, line 114, the list set on 2026-11-11: "Memory: Agents decide from three tiers of memory (Phoenix global, Garura project, short-term), and people control what enters them."
- core/tools/memory/README.md, lines 3-5, 8-11, 33-48, 57-63, 84-111, 158-160 and 224-230: "Agents that call it do not change when that happens, because they only ever talk to this tool", "The tool learns where each tier lives from its settings, never from a fixed path.", "a draft is used only once a person approved it and it was applied", "an agent never decides from its own earlier decision", "the only engine built", "The tool reads Phoenix memory and never copies a file from it into the project", "So the lowest tier answers whenever it can, and Phoenix memory is reached only when the lower tiers have nothing.", "A lookup never skips a tier.", "carries its tier, file, lines and fingerprint.", and the two things that are not memory
- core/tools/memory/GUIDE.md, line 41: "`tier_missing` means a tier cannot be reached. Say so."
- core/tools/memory/pull.py, line 10: "Working-tree edits and unmerged commits are never read."
- docs/adr/035-agents-work-only-from-memory.md, section 4, line 68, the product owner's words: "this is critical as this is why claude-code is so good"
- docs/adr/036-approved-answer-lands-in-short-term-memory.md, section 1, line 43, the product owner's words: "When a short-term memory is looked up, it is looked up only in the current issue, not the other issues. That is critical."
- docs/adr/039-memory-writes-go-to-short-term-memory-plays-read-no-memory.md, section 4, line 72, the product owner's words: "You don't need to copy the entire file."
- The memory tool's `health` answer, 2026-11-11: all three tiers reachable, Phoenix memory at version b2e40bff2131.
- GitHub #657 and #661 (closed): the tool and the plays reading through it; #653 (open): the memory system.
- GitHub #942 (open): "In this repository that folder was removed on 2026-10-26"
- .garura/product/product-os/software-delivery-planning/review-agent-work/fn-review-memory/feature.md: Ask memory is mocked only.
- The stock-take, .garura/project/issues/1021/context/bi-10-inventory/inventory.md, sections 5.1 and 5.4.
