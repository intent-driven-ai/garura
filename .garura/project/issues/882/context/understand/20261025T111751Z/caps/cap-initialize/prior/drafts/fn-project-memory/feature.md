# Feature: Build the project's memory

## What it does
- Runs after the product owner confirms the setup answers. It sets up the project's Garura memory from only the part of Phoenix memory those answers call for, so a project with no database, no front end or no permissions gets none of those standards.
- The install brings no memory of its own; this feature is where the project's memory is first made.
- It records the answers in the product profile, so every later play reads the same facts about the project without asking again.

## Inputs / Outputs
- In: the confirmed answers from fn-setup-questions: domains, kinds of features, technology standards, tools and frameworks, surfaces, and whether there is a database, personal data, permissions or a running service.
- In: Phoenix memory, read only through the memory tool, for the files those answers select.
- Out: the project's Garura memory, holding only the files the answers select, each with where it came from in Phoenix memory.
- Out: the answers recorded in the profile, each with the question it answers.
- Out: a short record of what was built: which memory files were taken and which were left out because the answers rule them out.

## Rules & behavior
- A memory file is taken only when an answer calls for it. A file that no answer selects stays in Phoenix memory, so the project's memory holds what fits and nothing else.
- Every read goes through the memory tool, because every part of Garura reads memory that way and the tool is what records where each file came from. No part of initialize reads a memory file by its path.
- The profile records the answers as the person gave them, because later plays treat the profile as the product owner's own word. Initialize never adds an answer the person did not give, and a proposed answer the person did not accept is never written.
- When an answer selects nothing in Phoenix memory (for example a tool memory has no standard for), the record says so in plain words, and the project's memory is built from the other answers. Our default; the sources do not say what happens then.
- When a run is repeated (fn-rerun-initialize), the memory is rebuilt from the new answers, and the record says which files were added and which were taken out.

## Acceptance criteria
- Given answers that say the project has no database, when the memory is built, then the project's Garura memory holds no database standard.
- Given answers that select a domain and a set of standards, when the memory is built, then each of those files is in the project's memory and names where it came from in Phoenix memory.
- Given the confirmed answers, when the memory is built, then the profile records each answer with its question.
- Given an answer that selects nothing in Phoenix memory, when the memory is built, then the record names that answer and the rest of the memory is still built.

## Out of scope
- Asking the questions and recording the person's reply (fn-setup-questions owns it).
- Recording the review rule groups (fn-review-rule-groups owns it).
- Moving the memory tool's home to Phoenix, and removing the machine-global Garura memory folder (later, by the business intent).
- Installed parts that read the source tree (#860).

## Sources
- GitHub #862: "the answers set up the project's Garura memory from only the part of Phoenix memory it needs, and the profile records them".
- GitHub #862, Rule 1: "The install brings no memory of its own; `initialize` builds the project's memory after it (recorded with the #653 plan, ADR 038, ADR 039)."
- GitHub #862, Out of scope: "Moving the memory tool's home to Phoenix", "Installed parts reading the source tree (#860)".
- Shelf: none (routing.yaml, unmatched).

## Agent intent (ICE)
- Goal: After the answers are confirmed, the project's Garura memory holds only the part of Phoenix memory the answers call for, each file naming where it came from.
- Goal: The profile records each answer with the question it answers.
- Limit: Read Phoenix memory only through the memory tool, and record in the profile no answer the person did not give.
- Fails if: the project's memory holds a standard an answer rules out, such as a database standard for a project with no database.
- Fails if: the profile holds an answer the product owner never gave or confirmed.
- Context: serves the product owner and every later play that reads the project's memory; reads the confirmed answers and Phoenix memory; out are the questions, the review rule groups and the memory tool's move to Phoenix.
- Checked by: run `initialize` on a test project with no database, then check that its Garura memory holds no database standard and that the profile lists each answer.
