## Intent
- Goal: A person who asks what to focus on sees at most ten issues of the work tracker that one fixed mode selects, each with its number, title, a reason built from the signals that selected it and its kind, and a play only where the fixed table names one, the same list every time for the same issues and mode, with nothing written to any issue.
- Limit: The mode is today, review or recent, never guessed; a mode it does not know gives no list.
- Limit: The kind and the play come only from the fixed table; where it names none, no recommendation is shown, and their count is.
- Limit: It never writes to an issue, and never reads the plan files or the product model.
- Fails if: More than ten entries are shown, or the count of the rest is missing or wrong.
- Fails if: An entry carries a play the table does not name for it, or a play that does not exist.
- Fails if: Any issue in the tracker changed during the run.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the mode asked for, the work tracker's issues with their states, dates, labels, types and assignees, the login of the one who runs it, the kind table, and the plays the project has.
- Never read: any memory file by its path, and any ICE page.
- Persona: the developer, a person or an AI agent who builds the code, who picks up the next piece of work; and the technical lead, who looks at the work in flight.
- Scope: In: the three modes, the fixed order, the cap and the count of the rest, the reason, and the kind and the play from the table. Out: the plan views, the order of the work, the plays' names, the tracker of business intents, and any write.

## Expectation
- Scenario: In a recipe app's tracker with 40 open issues, a developer asks with no mode. It shows ten unassigned issues that are not blocked, the most recently touched first, says how many more matched, and names a play only beside the defects the table maps to the bug fix play. The technical lead then asks for review and sees, first, a story that was assigned 20 days ago and is untouched since.
- Done means: Someone other than the one who ran it reads the tracker before and after and the two lists, and finds the tracker unchanged, at most ten entries in each list in the fixed order, the right count of the rest, and no play named that the table does not name or that does not exist.
