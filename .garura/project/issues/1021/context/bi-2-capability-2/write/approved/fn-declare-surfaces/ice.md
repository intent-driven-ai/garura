## Intent
- Goal: Each surface the project has is declared once for the whole project, with its kind, who opens it and what they do there, what it offers and how it behaves, and the guidelines every design on it must handle, each part with its reason, its source and the person who confirmed it.
- Limit: Each surface, property and guideline is proposed from the project's own memory and code first, then from Garura memory, then from Phoenix memory; only when none of them answers is it researched, and the research is used only after a person approves it as a memory update. Nothing comes from what the AI agent knows by itself.
- Limit: Each guideline serves a property of its surface or a quality level of the product profile, and never changes the profile.
- Limit: Only a person confirms a surface, a property or a guideline, and no work waits for one.
- Fails if: A surface, a property or a guideline is declared with no person's confirmation, or with nothing behind it but what the AI agent knows by itself.
- Fails if: An agent that designs a slice on a declared surface cannot find its properties and guidelines, and decides them alone with no gap named.
- Fails if: Work stops because a surface, a property or a guideline is not declared.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the project's code and its settings, such as the commands it installs, its pages and their layouts, its components and its style guide, the apps it ships and the endpoints other systems call; the Sources a person gave when the product was specified; the business intents and who asks for each; the rough list of surfaces and the quality levels in the product profile; Phoenix memory's learnings for each kind of surface and its domain shelves; and the project's set-up answers, when it has them.
- Persona: the product owner, who confirms each surface, its properties and its guidelines.
- Scope: In: proposing and declaring each surface of the whole project, with its kind, who opens it, what they do there, why, its properties and its guidelines. Out: updating the declared surfaces, each slice's surface and tester, designing a slice on its surface, testing each kind of surface, the technology of a surface and of its design system, the product profile, and moving a memory update into Phoenix memory.

## Expectation
- Scenario: A clinic's booking product is proposed a browser page where patients book a visit, from the prototype the product owner gave, with the screen sizes it serves and the design system its screens work within, from the style guide in the clinic's code, and an accessibility guideline at the level the product profile commits to. The product owner confirms them, and the export of the day's bookings stays off the list.
- Done means: An agent that did not declare the surfaces designs a slice on the booking page from the declaration alone, naming its screen sizes, its design system and its accessibility level, and a person other than the one who declared them finds a source and a confirmation behind each part.
