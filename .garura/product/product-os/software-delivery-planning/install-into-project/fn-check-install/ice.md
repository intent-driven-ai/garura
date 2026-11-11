## Intent
- Goal: Once the parts are laid, the memory tool is checked the way an agent runs it, and must run and reach the project's short-term memory and Garura memory, and every laid tool must get its packages and load; whatever does not is named with what to fix, and the install ends as failed after its record is written, while Phoenix memory not yet on the machine is reported and never fails it, so no team starts work on a Garura that cannot run.
- Limit: The check runs the memory tool the way an agent does, never reads memory by a path, and brings no memory into the project.
- Limit: Phoenix memory not yet downloaded never fails the install, and short-term or Garura memory out of reach always does.
- Limit: Both front doors run the same check, and the record of what was laid is written before a failed check ends the install.
- Fails if: An install counts as done while the memory tool cannot run or reach short-term or Garura memory, or a laid tool does not load.
- Fails if: A failed check does not name what failed, or leaves no record of what was laid.
- Fails if: An install fails only because Phoenix memory is not on the machine yet.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the laid memory tool and its settings, the project's short-term memory folder and Garura memory, where Phoenix memory sits on the machine and where it is downloaded from, each laid tool with its packages and its smoke check, and the record of the install.
- Never read: any memory file by its path, and any ICE page.
- Persona: the product owner, who needs to know the installed Garura runs before the team uses it.
- Scope: In: checking the memory tool and its tiers, getting each tool's packages, loading each tool, and naming what failed. Out: how the memory tool works and when Phoenix memory arrives, laying the parts, and setting up the project's own memory.

## Expectation
- Scenario: A new recipe app's project is installed on a laptop that has never had Phoenix memory. The memory tool reaches short-term and Garura memory, Phoenix memory is reported as not there yet and due on first use, and the install counts as done. On a second project, a shop's checkout, one tool's packages cannot be fetched: the install stops, names the tool, and the record of what was laid is written.
- Done means: Someone other than the one who installed it reads the install's output and record, runs the memory tool's health command as an agent would, and finds each tier and each tool as the output said, and no install counted as done with a part that does not run.
