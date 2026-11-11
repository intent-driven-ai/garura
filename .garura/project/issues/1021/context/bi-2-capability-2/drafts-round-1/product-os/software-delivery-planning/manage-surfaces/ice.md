Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: The project's surfaces are declared once for the whole project, each with its kind, who opens it and what they do there, its reason, its source and the person who confirmed it, and every slice is designed and tested on one of them, while the surfaces are updated as the project changes.
- Limit: Each surface and its kind are proposed from the project's own memory and code first, then from Garura memory, then from Phoenix memory; only when none of them answers is it researched, and the research is used only after a person approves it as a memory update. Nothing comes from what the AI agent knows by itself.
- Limit: Nothing waits for the surfaces. A missing surface or an open kind is named as a gap, and the work goes on.
- Limit: Only a person confirms a surface, its kind or an update, and an update replaces what held before without editing it, so the old surfaces stay readable with why they changed.
- Fails if: A surface or its kind is declared with no person's confirmation, or with nothing behind it but what the AI agent knows by itself.
- Fails if: A slice is designed on a surface whose kind nobody declared, and no gap is named.
- Fails if: Work stops because a surface is not declared.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the project's code and its settings, such as the commands it installs, the pages it serves and the apps it ships; what a person gave when the product was specified; the business intents and who asks for each; the surfaces declared so far and the rough list in the product profile; and the slices with the surface each is on.
- Persona: the product owner, who decides where people use the product.
- Scope: In: proposing, declaring and updating the project's surfaces, each with its kind, who opens it, what they do there and why. Out: the rest of the product profile, each slice's surface and tester, designing a surface for a slice, testing each kind of surface, the technology of each surface, seeding memory and review rules, decision records, moving a memory update into Phoenix memory, deployment, environments and the lock.

## Expectation
- Scenario: A team's work tool is proposed two surfaces: a browser page where team leads plan the week, from the prototype the product owner gave, and a command line the engineers run, from the command its code installs. The product owner confirms both, with the reason for each kind. When the product later gains a mobile app, the surfaces are updated, and what held before stays readable with why it changed.
- Done means: Someone other than the one who declared the surfaces checks each one and finds its kind, who opens it, its reason, a source in the project or in memory, and the person who confirmed it.
- Done means: Someone other than the slice's designer compares the surface of each slice with the declared surfaces, and finds each one on the list or named as a gap.
