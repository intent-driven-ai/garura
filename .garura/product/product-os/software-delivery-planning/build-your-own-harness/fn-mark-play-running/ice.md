Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: Every play writes a record that it is running when it starts and clears it at its close, where the guardrails the install lays and the review of each change can read it, so an edit, a commit or a script run made inside a play can be told from the same act done by hand as a shortcut.
- Limit: The marker is the play's own record; the guardrails, their way past and the review's check stay with their owners.
- Limit: Every play built or compiled again carries the marker in the same way.
- Limit: A marker never claims a run that did not happen.
- Fails if: A play runs and leaves no record that it is running, or its record stays after its close.
- Fails if: A guardrail cannot tell an act inside a play from the same act done by hand.
- Fails if: Two plays built at different times write their markers in different ways.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the proposed design of the guardrails laid by the install, the session stamp each play writes today, the shared close, the play compiler's shared scripts, the guardrails the install is to lay, and the review of each change.
- Never read: any memory file by its path, and any ICE page.
- Persona: the developer or an agent who runs a play, and the technical lead who wants no shortcut taken past one.
- Scope: In: the record a play writes at its start and clears at its close, the same in every play. Out: what each guardrail guards and its way past, laying the guardrails, the hook's form in each coding tool, and the review's check.

## Expectation
- Scenario: In a shop's harness repository, /edit-play starts and writes its marker; the guardrail lets its edit to a compiled play through, and when the run closes the marker is gone. An agent then edits a compiled play by hand, and the guardrail finds no marker and names the play to run. In a bank's harness, the review of a change finds a commit that changed a play with no run of /edit-play on record.
- Done means: Someone other than the one who built the marker runs two plays and finds each one's record on disk while it runs and gone after its close, finds the record written the same way in both, and finds that an edit made by hand with no record was told apart from the edit made inside /edit-play.
