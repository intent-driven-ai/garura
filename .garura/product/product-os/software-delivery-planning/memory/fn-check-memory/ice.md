Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: Before an agent uses a page of memory, a check names it when it is out of date or its source changed, with why; and every change to a project's memory shows in the review of the change that made it, with the result of the memory checks, so agents decide only from memory people trust.
- Limit: The check does not change how agents look memory up: one memory tool, three tiers in order.
- Limit: The check changes no memory by itself; a page changes only through a person.
- Limit: Checking a decision's sources after it was made, and the differences between Phoenix memory and Garura's source, stay with their own features.
- Fails if: An agent uses a page whose source changed, and no check named it before.
- Fails if: A change to a project's memory reaches its review without the result of the memory checks.
- Fails if: The check changes a page, or the order in which agents look memory up.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the pages of each tier and the sources they name, the memory indexes, the changes to a project's memory in the change that made them, the fingerprints the tool gives, and the proofs and Must not of #942 (a project's memory can be managed).
- Never read: any memory file by its path, and any ICE page.
- Persona: the product owner, who reviews each change to the project's memory; and the developer, a person or an AI agent who builds the code and decides from memory.
- Scope: In: naming a page that is out of date or whose source changed before it is used, and the memory checks in the review of each change to a project's memory. Out: the trace check of decisions already made, the compare of Phoenix memory with Garura's source, reviewing a change against its standards, and showing memory to a person.

## Expectation
- Scenario: In a clinic's booking app, the page on reset links was written from a security rule that has since changed; when the developer's agent is about to use it, the check names the page and the changed rule. In a bank's payments service, a change adds a page to Garura memory, and its review shows the page with the result of the memory checks.
- Done means: Someone other than the one who built it reads the clinic's run and the bank's review, and finds the reset-link page named with its changed source before the agent used it, the bank's review showing the new page with its check result, and no page changed by the check.
