Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: Everything a play run writes, its context, checks, evidence, review records and gate records, goes in the folder of the issue whose work made it, nothing goes in a global file, and every path in those records starts at the repository's root, so a person finds what each run did and decided with its work, and no record shows a person's home folder.
- Limit: No record goes in a global file unless a written rule first gives that place its structure.
- Limit: The scan of a push, the skip records, what is owed and the evidence setting stay with their owners.
- Fails if: A run's record sits outside its issue's folder with no written rule for that place.
- Fails if: A committed run record holds a home-folder path.
- Fails if: A gate record is written to a global ledger.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: short-term memory's settings and its five keys; where each play writes its working folder; the gate rule and the ledger setting; the folders of short-term memory that are not issues; the paths written in committed run records; and the issues that ask for records kept with their issue and written with repository paths.
- Never read: any memory file by its path, and any ICE page.
- Persona: the developer, a person or an AI agent who builds the code, whose runs write the records; and the product owner, who reads what a run did and decided.
- Scope: In: where each run's records go, in its issue's folder, and the paths written in them. Out: the scan of a push, the skip records, what is owed, the evidence setting, and which records a review reads.

## Expectation
- Scenario: In a bank's payments service, the technical lead records a decision by hand before its issue exists; once the issue is known, the run's brief and checks are in that issue's folder, and no folder outside an issue holds them. In an open-source library, the linter's record names each file from the repository's root, and a search of the committed records finds no home folder.
- Done means: Someone other than the one who ran the plays lists short-term memory and searches the committed run records, and finds every record in its issue's folder, nothing in a global file, and no home-folder path.
