## Intent
- Goal: Each play and each loop is compiled from its ICE source, its compiled part records the fingerprint of that ICE as it is now, a change to what it decides or guarantees is made in its ICE first and compiled again, and a check fails any play or loop whose compiled part no longer matches its ICE.
- Limit: Only plays and loops carry an ICE; skills and sub-agents follow the written standard for their kind.
- Limit: A change that alters no guarantee is a direct edit to the compiled part, and its ICE does not change.
- Limit: A play written by hand is named as such, with the reason it has no ICE source.
- Fails if: A play or loop changes what it decides or guarantees in its compiled part and not in its ICE.
- Fails if: A compiled play or loop records a fingerprint that is not its ICE's as it is now, and no check fails it.
- Fails if: A play or loop has no ICE source and is not named as written by hand.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: each play's and loop's ICE source and compiled part, the fingerprint in its metadata, the rule for an intent change and a direct edit, the play linter and the loop linter, and the plays written by hand with the reason each has no ICE source.
- Never read: any memory file by its path, and any ICE page.
- Persona: the developer, a person or an AI agent who builds the code, here a play or a loop; and the technical lead, who decides whether a change is an intent change.
- Scope: In: compiling each play and loop from its ICE, the fingerprint, the rule for an intent change and a direct edit, and the check of the match. Out: the builders themselves, what a good ICE holds, the standard for skills and sub-agents, and running the checks on every part.

## Expectation
- Scenario: In a bank's payments service, the refund play gains a limit in its ICE and is compiled again; its fingerprint changes and the compiled play holds the limit. A week later someone changes the ICE again and does not compile; the check fails the play and names the rebuild. In a harness repository, the words of a play's closing report are edited in the compiled play only, and its ICE and fingerprint stay as they were.
- Done means: Someone other than the one who compiled the parts reads each play's and loop's ICE source and compiled part, computes each fingerprint, and finds every compiled part's fingerprint equal to its ICE's, every limit of each ICE in its compiled part, and each play with no ICE source named as written by hand.
