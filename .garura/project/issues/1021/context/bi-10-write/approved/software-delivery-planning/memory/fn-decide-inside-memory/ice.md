## Intent
- Goal: Every page an agent decides from sits in one of the three tiers and is reached through the memory tool: the machine-wide copy of all memory is retired once the tool is fully live, Claude Code's own memory for a project holds only what a written guardrail allows while how the product is built goes into the repository, and the engine's rules stay in Phoenix memory, read through the tool, so nothing an agent decides from sits outside memory.
- Limit: No rule an agent decides from is kept only outside the tiers.
- Limit: Each Claude memory is kept, moved or deleted only on the product owner's word.
- Limit: Taking the copy out of the install, and what each rule says, stay with their owners.
- Fails if: An agent decides from the machine-wide copy, or from a page outside the tiers, after this is built.
- Fails if: Claude Code's own memory for a project holds how the product is built, with no copy of it in the repository.
- Fails if: An engine rule cannot be found through the memory tool.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: where the install lays the machine-wide copy and what reads it, Claude Code's own memory for the project and why each note was saved, the rules files every session reads, where the engine's rules sit in Phoenix memory, and the open issues on the way of working and the rule for asking a person.
- Never read: any memory file by its path, and any ICE page.
- Persona: the product owner, who decides what Claude Code's own memory may keep; and the developer, a person or an AI agent who builds the code and decides only from memory.
- Scope: In: retiring the machine-wide copy, the guardrail on Claude Code's own memory, and keeping the engine's rules in Phoenix memory, read through the tool. Out: taking the copy out of the install, what each rule says and sorting the way of working, the rule for asking a person, moving a page up a tier, and the read rule's checks.

## Expectation
- Scenario: In a shop's checkout service, the install lays no machine-wide copy, and an agent reads the review rule only through the tool, at Phoenix memory's approved version. In a bank's payments service, the product owner goes through the coding tool's own memory, moves a note on how plays are built into the repository, deletes the note, and the guardrail is written down.
- Done means: Someone other than the one who built it checks the shop's machine and the bank's repository, and finds no machine-wide copy, the review rule read through the tool, the bank's note in the repository and not in the coding tool's memory, and the guardrail written.
