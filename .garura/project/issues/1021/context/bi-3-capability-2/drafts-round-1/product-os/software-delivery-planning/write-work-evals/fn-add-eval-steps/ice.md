Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: A slice on a kind of surface with no step library, or a check its library cannot say, gets the steps it needs: fixed sentences, each one exact action or one exact check with what a runner does for it, raised as a memory update and used by an eval only after a person approves it.
- Limit: Each sentence is one exact action or one exact check, and says what a runner does for it, with no judgment.
- Limit: Steps come from the project's own memory and code first, then Garura memory, then Phoenix memory; only when none of them answers is a step researched, and the research is used only after a person approves it as a memory update. Nothing comes from what the AI agent knows by itself.
- Limit: A library changes only through a memory update a person approves; a step names what only the build will make as a name, never a guessed address or command.
- Fails if: An eval uses a sentence that no person approved.
- Fails if: A sentence leaves a runner a choice, or does not say what a runner does for it.
- Fails if: A proposed sentence has no source in memory and no approved memory update.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the slice's kind of surface in the project's declared surfaces, the step library that exists for that kind, the lines that went under Untestable because the library could not say them, how the project's surface is reached and tested today in its code and memory, and the eval rules.
- Never read: the slice's eval files and hidden file, the usage guide and the code the build makes.
- Persona: the product owner, who approves a new or grown library before any eval uses it.
- Scope: In: proposing a new step library or new sentences for one, as a memory update. Out: declaring surfaces, writing scenarios, running the steps, and promoting the update into Phoenix memory.

## Expectation
- Scenario: A shop's checkout slice is on a browser page, and no browser library exists. A memory update proposes sentences such as opening a named page, pressing a named button and checking that a text shows, each with what a runner does for it, and names the project's existing page tests as their source. The slice gets no eval until the product owner approves the update.
- Done means: Someone other than the one who proposed the steps reads each sentence and finds one exact action or check, what a runner does for it, and a source in memory or an approved memory update, and finds no eval that used the sentences before the approval.
