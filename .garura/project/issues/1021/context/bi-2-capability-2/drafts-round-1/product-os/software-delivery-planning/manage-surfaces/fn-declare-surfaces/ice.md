Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: The project's surfaces are declared once for the whole project, each with its name, its kind, who opens it and what they do there, and with its reason, its source and the person who confirmed it.
- Limit: Each surface and its kind are proposed from the project's own memory and code first, then from Garura memory, then from Phoenix memory; only when none of them answers is it researched, and the research is used only after a person approves it as a memory update. Nothing comes from what the AI agent knows by itself.
- Limit: Only surfaces are declared; a file the product hands out, such as an export, is not one.
- Limit: Only a person confirms a surface or its kind, and no work waits for one.
- Fails if: A surface or its kind is declared with no person's confirmation, or with nothing behind it but what the AI agent knows by itself.
- Fails if: The list holds something that is not a surface, or misses a surface that a slice is on, and no gap is named.
- Fails if: Work stops because a surface is not declared.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the project's code and its settings, such as the commands it installs, the pages it serves, the apps it ships and the endpoints other systems call; the Sources a person gave when the product was specified; the business intents and who asks for each; the rough list of surfaces in the product profile; and the project's set-up answers, when it has them.
- Persona: the product owner, who confirms each surface and its kind.
- Scope: In: proposing and declaring each surface of the whole project, with its kind, who opens it, what they do there and why. Out: updating the declared surfaces, each slice's surface and tester, designing a surface for a slice, testing each kind of surface, the technology of each surface, the rest of the product profile, and moving a memory update into Phoenix memory.

## Expectation
- Scenario: A clinic's booking product is proposed a browser page where patients book a visit, from the prototype the product owner gave, and an API that the clinic's records system calls, from the endpoint its code serves. The product owner confirms both, with the reason for each kind, and the export of the day's bookings stays off the list.
- Done means: An agent that did not declare the surfaces reads them and names each surface, its kind, who opens it, what they do there and why, and a person other than the one who declared them agrees, finding a source and a confirmation behind each.
