## Intent
- Goal: The Context guidance of each story in the tree gathered under the chosen item is turned into the context it points to, collected from memory into that story's short-term memory with each part's source, so the work is designed and built from the story and its context in one place and no ICE page is opened.
- Limit: Context comes from the project's code and memory first, then Garura memory, then Phoenix memory; only when none of them answers is it researched, and the research is used only after a person approves it as a memory update. Nothing comes from what the AI agent knows by itself.
- Limit: No ICE page, eval, hidden file or evals folder is read, even when the guidance names one, and nothing the guidance's Never read line names is collected.
- Limit: A part that no tier answers stays open with no default, and the rest is collected.
- Fails if: A part of the collected context has no source in the project, in memory or in a memory update a person approved.
- Fails if: The collected context holds anything from an ICE page, the eval, the hidden file or the evals folder, or anything the Never read line names.
- Fails if: A part that no tier answered is filled with a default or a guess.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the Context guidance of each story in the gathered tree, the project's code and its own memory for what each Read line points to, Garura memory, Phoenix memory, and the memory updates of the issue that a person approved.
- Never read: any ICE page, the plan's evals folder, the eval, the slice's hidden file, and what the story's Never read line names.
- Persona: the technical lead, who designs the work from each gathered story and its collected context.
- Scope: In: reading the guidance of each gathered story, collecting what it points to from memory, raising a memory update when no tier answers, and naming what stays open or was left out. Out: gathering the tree, writing the guidance, the project's standards and the design, and approving or moving a memory update.

## Expectation
- Scenario: The technical lead of a shop names the story "A guest pays by card", whose guidance says to read the payment rules and never to read saved card data. The payment rules are found in the project's own memory and put in the story's short-term memory with their source. A rule on card fees that no tier holds is researched and raised as a memory update, and stays open until a person approves it. No saved card data and no ICE page is read.
- Done means: Someone other than the one who collected the context reads it and finds behind each part a source in the project, in memory or in a memory update a person approved, finds nothing from an ICE page, the evals folder or what the Never read line names, and finds each open part named with no default.
