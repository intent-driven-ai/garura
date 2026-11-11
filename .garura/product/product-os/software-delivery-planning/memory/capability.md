# Capability: Memory

## Directional intent
Memory: Agents decide from three tiers of memory (Phoenix global, Garura project, short-term), and people control what enters them.
These are the agreed words for the fifth capability of Standards, structure, settings and memory. The product owner set the list on 2026-11-11 and wrote: "continue as most of this is based on built. please proceed with creae pages and ICE as per the process and standards and consider them approved. show me only when you are ready for commit and cp". So this page is written from what Garura has built, and what is not built is drafted from the product owner's words and the issues. Two of the product owner's answers shape it. First, the engine's rules stay in Phoenix memory, read through the memory tool, and this intent's proof, "Nothing an agent decides from sits outside memory.", stands. Second, moving a page up a tier, and choosing what is learned, are this capability's work, done on a person's yes; the person gives that yes in the Memory section of Argus, and Run → Product proposes what was learned. The words this page uses:
- Memory is what an agent decides from. It has three tiers. Short-term memory is the folder of the one issue the work is on: its plans, specs and context, the questions asked of a person and the answers. Garura memory is the project's own memory: its memory folder, then its product model. Phoenix memory is the global memory that any project can use: standards, rules, templates, schemas and knowledge. It is its own git repository, with one copy on each machine.
- The memory tool is the one command every agent uses to find memory and to update it. A lookup goes to short-term memory, then Garura memory, then Phoenix memory, and stops at the first tier that answers.
- A memory update is an answer that an agent drafts when no tier holds what it needs. A person approves or rejects it. Nothing in it is used before a person approves it.
- A trace is the list of steps an agent took to make one decision. Each step says what the agent looked for, what it found and the memory lines that said so, with a fingerprint of that text.
- A promotion moves a page up a tier, from short-term memory to the project's Garura memory. Moving a page to Phoenix memory is not designed, needs an organisational change, and is to happen outside Garura.
- A play is a command a person or an agent types to run one piece of work from start to end. A loop runs plays in rounds until its goal is met. A sub-agent gathers the context; a skill does the work from what its sub-agent puts in short-term memory.

This capability does five jobs that are built, two of them in part:
- Find memory across three tiers through one tool.
- Let only a person decide a memory update, one at a time.
- Keep each decision's trace and check its sources.
- Make every agent read memory only through the tool, and fail a part that names a memory path. This one is built in part.
- Bring Phoenix memory to a machine and keep it current. This one is built in part: the download on first use is built.

And four jobs that are not built:
- Keep Phoenix memory in step with Garura's source, versioned per release with its notes.
- Move a page up a tier on a person's yes, and choose what is learned.
- Check what memory holds: pages out of date, and sources that changed.
- Keep what agents decide from inside memory: the machine-wide copy, Claude Code's own memory, and the rules.

The work is split between parts. A play reads no memory. Its sub-agents read memory through the tool and put what each skill needs in short-term memory, and a skill reads only that. In the memory guide every agent reads: "Only agents call the tool: a play asks its agents for what it needs, and a skill reads only what its agent puts in short-term memory."
Other capabilities hand their memory work here:
- Set a project up after the install (Initialize), in Install and distribute, builds a project's Garura memory from Phoenix memory, and leaves "how Phoenix memory reaches a machine and is brought up to date, what may enter each memory tier, and promotion" here.
- Install into a project lays the memory tool and its guide, and leaves "Retiring the machine-wide copy of all memory for every project" here. Upgrade a project leaves "Phoenix memory's own versions and notes" here.
- Review what agents make (Argus), in Developer tooling, shows the memory updates and each decision's trace, and there "A memory update is decided by the rules of Memory".
- Run plays as loops, in Orchestration, leaves "approving a memory update the knowledge step raises, and promoting a page to Garura or Phoenix memory" here.
- The three capabilities of Run → Product leave "choosing and promoting what is learned into Garura memory or Phoenix memory" here. Fifteen pages of Spec → Design and Design → Code hand promotion on without naming who owns it; four of them say an approved update moves up only by "a promotion a person makes on purpose, outside this work".
- Some of these pages also hand here promoting a page to Phoenix memory. That move is not Garura's: in the product owner's words of 2026-11-11, "Going to the Phoenix is not designed yet. That would need an organizational change."
This capability has three stops of its own. An agent that cannot go on without an update that waits for a person stops; the way past is a person's decision, and nothing reminds anyone. A tier that cannot be reached answers `tier_missing`; the way past is to point the tool's setting at a copy that can be reached. A read of another issue's short-term memory is refused; the way past is a promotion, which is not built. The way past each gate, and where what is owed is kept, belong to Give every gate a way past, in Orchestration.
It matters because "Agents follow the rules and memory they're given, so a loose rule or a wrong page reaches every later decision." In the product owner's words on #942 (a project's memory can be managed): "if memory is wrong its a major problem". And in the product owner's words on the memory system: "The system should work only within the memory, but not outside of it." It sits in software delivery planning with the other capabilities of Standards, structure, settings and memory, and the domain's first paragraph says so.

Features:
- Find memory across three tiers through one tool (fn-find-memory): an agent finds what it needs with one memory tool, which looks in the issue's short-term memory, then Garura memory, then Phoenix memory, stops at the first tier that answers, and gives every answer its tier, file, lines and fingerprint.
- Let only a person decide a memory update, one at a time (fn-person-decides-update): when no tier answers, an agent drafts the answer as a memory update in the issue's short-term memory, and only a person approves or rejects it, one at a time, with their exact reply on record; nothing reminds anyone of an update that waits.
- Keep each decision's trace and check its sources (fn-keep-decision-trace): each decision an agent makes is recorded with its trace, each step resting on memory lines with their fingerprint, and a check reads every source again and names the step whose source changed or is gone; a decision that a later one replaced cannot be marked yet (#852, replaced decisions in the trace check).
- Make every agent read memory only through the tool, and fail a part that names a memory path (fn-read-through-tool): every agent reads memory through the tool by one shared protocol and copies what its skills need into short-term memory, and the component linter fails a part that skips the protocol or names a memory folder. Built in part (#663, every part reads memory through the tool).
- Keep Phoenix memory in step with Garura's source, versioned per release with its notes (fn-phoenix-in-step): a change to a memory page in Garura's source reaches Phoenix memory in the same release, a check names every page where the two differ, and each release of Phoenix memory has a version and its own notes. Not built (#966 and #921, Phoenix memory in step and versioned; #949, Phoenix memory has fallen behind the source in 60 places).
- Bring Phoenix memory to a machine and keep it current (fn-bring-phoenix): the memory tool downloads Phoenix memory whole the first time a command needs it and reads it only at its approved version; one Phoenix install per machine is to lay it and bring it up to date. Built in part (#883, the Phoenix install).
- Move a page up a tier on a person's yes, and choose what is learned (fn-promote-page): a page moves from short-term memory to the project's Garura memory only on a person's yes in the Memory section of Argus, and what Run → Product learned is chosen by that person. Not built.
- Check what memory holds: pages out of date, sources that changed (fn-check-memory): a page that is out of date, or whose source changed, is named before an agent uses it, and every change to a project's memory shows in the review of its change with the result of the memory checks. Not built (#942, a project's memory can be managed).
- Keep what agents decide from inside memory: the machine-wide copy, Claude Code's own memory, and the rules (fn-decide-inside-memory): the machine-wide copy of all memory is retired, Claude Code's own memory for a project is held to a written guardrail, and the engine's rules stay in Phoenix memory, read through the tool. Not built (#839, Claude Code's own memory; ADR 055 section 8, the machine-wide copy).

What is not built yet:
- Phoenix memory differs from Garura's source in 60 places: 42 pages differ, 3 are in the source only and 15 are in Phoenix memory only. A change reaches Phoenix memory only by hand, and Phoenix memory has no version per release and no notes (#949, Phoenix memory behind the source in 60 places; #921 and #966, Phoenix memory in step and versioned).
- No play or command moves a page up a tier. The memory tool names "/learn-memory and /promote-memory plays", and the glossary marks the promotion play "not built yet".
- Nothing reminds anyone of a memory update that waits. Five wait today; the oldest has waited since 2026-10-24.
- A decision that a later decision replaced cannot be marked, so the trace check of such an issue never reads clean (#852, replaced decisions in the trace check).
- Five agents, the /fix-bug play and two skills still name the older memory field `ltm_context`, and #663 (every part reads memory through the tool) is open.
- Once Phoenix memory is on a machine, no command brings a newer version to it. The Phoenix install is planned only (#883, the Phoenix install).
- Nothing checks what memory holds before an agent uses it: "No linters and no rubric for memory." (#942, a project's memory can be managed).
- In this repository Garura memory has no memory folder, so it is only the product model.
- Agents also decide from files outside the tiers: the machine-wide copy of all memory, which the install still lays, Claude Code's own memory for the project (#839, review every Claude memory), and the rules files in the repository (#952, the way of working as engine rules and settings; #999, the rule for asking a person as an engine rule).

### Benefit hypothesis
- Who it serves: the developer, a person or an AI agent who builds the code, and every agent that decides from memory; the product owner, who approves or rejects each memory update and each promotion; and the capabilities that hand their memory work here: Set a project up after the install (Initialize), Install into a project and Upgrade a project, in Install and distribute; Review what agents make (Argus), in Developer tooling; Run plays as loops, in Orchestration; and the three capabilities of Run → Product.
- What we believe: when every agent decides only from memory it finds through one tool, and only a person lets anything new into memory or moves it up, a wrong page is seen before it reaches later decisions, and an answer one issue found can reach the next one, if the work stands on these rules:
  - A lookup goes to short-term memory, then Garura memory, then Phoenix memory, and short-term memory is only the issue's own.
  - Nothing from the model or the web is used before a person approves it.
  - Every memory write goes to the issue's short-term memory, and a page moves up a tier only on a person's yes.
  - Every decision keeps its trace, and its sources are checked again.
  - No part reads memory by a path.
  - The engine's rules stay in Phoenix memory, read through the tool.
- How we will know: this intent's proof, "Nothing an agent decides from sits outside memory."; every applied memory update names the person who approved it and their exact reply; the trace check of each issue reads clean, or names the step whose source changed; the component linter shows no memory error; and at each release no page differs between Phoenix memory and Garura's source without a person's decision on it.
  - The first does not hold today: agents also read the machine-wide copy, Claude Code's own memory and the rules files in the repository.
  - The third does not hold for an issue where a later decision replaced an earlier one (#852, replaced decisions in the trace check).
  - The fifth is not tested, because nothing compares the two at a release (#921, Phoenix memory up to date with its own release notes).

### Boundary (In / Out / Never)
- In: finding memory across the three tiers through one tool, in a fixed order, with every answer carrying its tier, file, lines and fingerprint.
- In: memory updates: raising one, a person's decision on each, one at a time, and writing an approved one to the issue's short-term memory.
- In: each decision's trace, and the check of its sources.
- In: the rule that every part reads memory only through the tool, the shared protocol, and the checks that fail a part that names a memory path.
- In: what may enter each memory tier, and what memory may hold.
- In: Phoenix memory: bringing it to a machine and keeping it current, keeping it in step with Garura's source, and its versions and notes.
- In, not built yet: moving a page up a tier and choosing what is learned, the checks of what memory holds, keeping what agents decide from inside memory, among them retiring the machine-wide copy, and moving the memory tool's home to a server, which is one setting once a server exists.
- Out: the cards where a person approves an update, reads a trace or says yes to a promotion. Review what agents make (Argus), in Developer tooling, owns them; what each answer does is this capability's.
- Out: proposing what was learned in use and in the market. Run → Product owns it; choosing and promoting it is this capability's.
- Out: building a project's own Garura memory from Phoenix memory after the install. Set a project up after the install (Initialize), in Install and distribute, owns it.
- Out: laying the memory tool, its settings and its guide in a project, and the install's check. Install into a project, in Install and distribute, owns them.
- Out: Garura's own release and its notes. Upgrade a project, in Install and distribute, owns them; Phoenix memory's own versions and notes are this capability's.
- Out: what the product model holds and how it is written. Product model (BI-11) owns it; the model is read here as part of Garura memory.
- Out: what each rule and standard says, and the component linter's other rules. Standards, in Standards, structure, settings and memory, owns them; keeping the rules in Phoenix memory, read through the tool, is this capability's.
- Out: where each tier's folder sits in a project, and what each of the tool's settings means. Structure and Settings, in Standards, structure, settings and memory, own them.
- Out: the questions a loop's knowledge step raises, and when the loop reaches the person. Run plays as loops, in Orchestration, owns them.
- Out: the way past each stop of this capability, and where what is owed is kept. Give every gate a way past, in Orchestration, owns them.
- Never: decide from the model or the web without a memory update a person approved. The reason: "Never answer from what you already know, and never from the web, without a memory update a person approved."
- Never: let an agent decide a memory update, or decide updates in bulk. The reason: "Only a person decides, one update at a time."
- Never: make a new memory outside the issue's short-term memory. The reason: "A new memory made outside short-term memory breaks the guardrail."
- Never: read a memory file by its path. The reason: "Never read a memory file by its path. Never take a memory path from a contract."
- Never: read another issue's short-term memory. The reason: "A read of another issue's short-term path is refused".
- Never: copy a Phoenix file into a project. The reason: "The tool reads Phoenix memory and never copies a file from it into the project".
- Never: promote memory without a person. The reason: Run → Product must not "Change an intent, or promote memory, without a person."

### Guiding rules
- One tool for every tier, so the agents do not change when memory moves to a server. The reason, in the product owner's words: "the impact on Garura and the agents is zero because they are always calling the tool."
- The lowest tier answers whenever it can. The reason: "So the lowest tier answers whenever it can, and Phoenix memory is reached only when the lower tiers have nothing."
- A tier that cannot be reached is said, and is never taken as nothing found. The reason: "`tier_missing` means a tier cannot be reached. Say so."
- Memory is written low and moved up on purpose. The reason, in the product owner's words: "memory, when written, will always go into STM, and it needs to be consciously promoted up."
- The engine's rules are memory. The reason: the glossary says Standards "Live in Phoenix memory", and the product owner's answer, as recorded: "the engine's rules stay in Phoenix memory, read through the memory tool, and the proof stands".
- Every change to Phoenix memory is a commit a person approves. The reason: "A person approves every promotion. Every change here is a commit."
- Not decided: whether a promotion is a play, a command of the memory tool, or a memory update aimed at Garura memory.
- Not decided: where the rule for asking a person lives, now that the engine's rules stay in Phoenix memory: it is a shared file today (#854, the rule for asking a person as a shared file), and #999 (the rule for asking a person as an engine rule) puts it in the engine.
- Not decided: what Claude Code's own memory for a project may hold, and what must go into the repository (#839, review every Claude memory).

## Sources
- .garura/project/issues/1021/context/capabilities.md, line 114, the list set on 2026-11-11: "Memory: Agents decide from three tiers of memory (Phoenix global, Garura project, short-term), and people control what enters them."; line 116, the product owner: "continue as most of this is based on built. please proceed with creae pages and ICE as per the process and standards and consider them approved. show me only when you are ready for commit and cp"; line 118, the product owner's answers as recorded: "3, the engine's rules stay in Phoenix memory, read through the memory tool, and the proof stands", "6, moving a page up a tier and choosing what is learned are Memory's, on a person's yes, decided in Argus's Memory section, with BI-6 proposing what was learned"; line 68: "Not on this list: choosing and promoting learnings to Garura or Phoenix memory (left to the review of Memory, in Standards, structure, settings and memory)"
- .garura/product/product-os/intents/bi-10.md, lines 5 and 12: "Agents follow the rules and memory they're given, so a loose rule or a wrong page reaches every later decision.", "Nothing an agent decides from sits outside memory."
- .garura/product/product-os/intents/bi-6.md, line 13: "Change an intent, or promote memory, without a person."
- core/tools/memory/README.md, lines 60-61, 85-86, 94 and 136: "The tool reads Phoenix memory and never copies a file from it into the project", "So the lowest tier answers whenever it can, and Phoenix memory is reached only when the lower tiers have nothing.", "A read of another issue's short-term path is refused", "Only a person decides, one update at a time."
- core/tools/memory/GUIDE.md, laid for every agent as the memory guide, lines 5-8 and 41: "Only agents call the tool: a play asks its agents for what it needs, and a skill reads only what its agent puts in short-term memory.", "Never answer from what you already know, and never from the web, without a memory update a person approved.", "`tier_missing` means a tier cannot be reached. Say so."
- core/tools/memory/updates.py, lines 7-8: "/learn-memory and /promote-memory plays"
- core/components/agents/_shared/memory-reading.md, line 13: "Never read a memory file by its path. Never take a memory path from a contract."
- core/grounding/glossary.md, lines 41 and 47: "`/promote-memory` (not built yet)", Standards "Live in Phoenix memory"
- docs/adr/035-agents-work-only-from-memory.md, lines 68 and 78, the product owner's words: "the impact on Garura and the agents is zero because they are always calling the tool.", "The system should work only within the memory, but not outside of it."
- docs/adr/039-memory-writes-go-to-short-term-memory-plays-read-no-memory.md, lines 39 and 46: "A new memory made outside short-term memory breaks the guardrail.", the product owner's words: "memory, when written, will always go into STM, and it needs to be consciously promoted up."
- docs/adr/055-installed-parts-read-only-installed-files.md, section 8, line 73: the install still writes the machine-wide copy of memory.
- README.md, in Phoenix memory, line 6, read through the memory tool: "A person approves every promotion. Every change here is a commit."
- .garura/product/product-os/software-delivery-planning/initialize/capability.md, line 58: "how Phoenix memory reaches a machine and is brought up to date, what may enter each memory tier, and promotion"
- .garura/product/product-os/software-delivery-planning/install-into-project/fn-take-out/feature.md, line 55: "Retiring the machine-wide copy of all memory for every project"
- .garura/product/product-os/software-delivery-planning/initialize/fn-project-memory/feature.md, line 56: "promotion, and moving the memory tool's home and the machine-wide copy of memory: Memory, in Standards, structure, settings and memory, owns them."
- .garura/product/product-os/software-delivery-planning/upgrade-project/fn-cut-release/feature.md, line 52: "Phoenix memory's own versions and notes"
- .garura/product/product-os/software-delivery-planning/review-agent-work/capability.md, line 34: "A memory update is decided by the rules of Memory"
- .garura/product/product-os/software-delivery-planning/run-plays-as-loops/capability.md, line 74: "approving a memory update the knowledge step raises, and promoting a page to Garura or Phoenix memory"
- .garura/product/product-os/software-delivery-planning/connect-use-and-market/capability.md, line 53, and the same words in build-or-update-product/capability.md, line 73, and understand-consumers-and-competition/capability.md, line 65: "choosing and promoting what is learned into Garura memory or Phoenix memory"
- .garura/product/product-os/software-delivery-planning/design-technology-architecture/capability.md, line 43, deployment-design/capability.md, line 65, environment-setup/capability.md, line 58, and manage-surfaces/capability.md, line 53: "a promotion a person makes on purpose, outside this work"; ten feature pages under them, and write-work-evals/fn-add-eval-steps/feature.md, quote the memory guide: "to Garura memory or Phoenix memory is a promotion a person makes on purpose"
- GitHub #942 (open), the product owner on 2026-10-28: "if memory is wrong its a major problem"; and "No linters and no rubric for memory."
- GitHub #653 (open, the memory system), #663 (open, every part reads memory through the tool), #852 (open, replaced decisions in the trace check), #839 (open, Claude Code's own memory), #883 (open, the Phoenix install), #921, #949 and #966 (open, Phoenix memory in step and versioned), #952 (open, the way of working as engine rules and settings), #854 (closed, the rule for asking a person as a shared file) and #999 (open, the rule for asking a person as an engine rule): the work named under What is not built yet.
- The memory tool's list of memory updates, 2026-11-11: 13 applied, 5 waiting, 1 rejected; the oldest waiting update was raised on 2026-10-24.
- The stock-take of this intent, .garura/project/issues/1021/context/bi-10-inventory/inventory.md, sections 5.1 to 5.8, 7.5, 7.7, 9, 10 and lean 6: the 60 places, the stops and their ways past, and the features.
- The short line beside each feature: the opening words of that feature's own page.
- Shelf: none. No knowledge shelf in any memory tier covers how an agent harness keeps its own memory; the experience shelf in Phoenix memory, knowledge/domains/experience.md, names "Guardrail & memory policy — scope what agents may do/remember." among the parts that govern agents built into a product, a loose match only.
- .garura/product/product-os/software-delivery-planning/domain.md, line 4: the domain's first paragraph, which does not name the capabilities of Standards, structure, settings and memory yet.
- .garura/product/product-os/software-delivery-planning/domain.md: "It also keeps the foundation every part stands on: the written standards and their checks, the builders a team uses for its own plays and loops, where everything lives, the settings, three tiers of memory, and the model each part runs on."
- .garura/project/issues/1021/context/bi-10-close/approval.md, line 3, the product owner's words of 2026-11-11: "Argus can only allow from short term to the project memory. Going to the Phoenix is not designed yet. That would need an organizational change."
