## Intent
- Goal: Each surface the project has is declared once for the whole project, with its kind, who opens it, its properties and its guidelines, each with its reason, its source and the person who confirmed it, and every design on that surface follows them, while the surfaces are updated as the project changes.
- Limit: Each surface, property and guideline is proposed from the project's own memory and code first, then from Garura memory, then from Phoenix memory; only when none of them answers is it researched, and the research is used only after a person approves it as a memory update. Nothing comes from what the AI agent knows by itself.
- Limit: Nothing waits for the surfaces. A missing surface, property or guideline is named as a gap, and the work goes on.
- Limit: Only a person confirms a surface, a property, a guideline or an update, and an update replaces what held before without editing it, so the old declaration stays readable with why it changed.
- Fails if: A surface, a property or a guideline is declared with no person's confirmation, or with nothing behind it but what the AI agent knows by itself.
- Fails if: A slice's design on a declared surface breaks one of its properties or guidelines, and no gap or update explains it.
- Fails if: Work stops because a surface, a property or a guideline is not declared.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the project's code and its settings, such as the commands it installs, its pages and their layouts, its components and its style guide, and the apps it ships; what a person gave when the product was specified; the business intents and who asks for each; the surfaces declared so far, and the rough list and the quality levels in the product profile; Phoenix memory's learnings for each kind of surface; and the slices with the surface each is on.
- Persona: the product owner, who decides where people use the product and what each surface must handle.
- Scope: In: proposing, declaring and updating each surface of the project, with its kind, who opens it, what they do there, why, its properties and its guidelines. Out: the rest of the product profile, each slice's surface and tester, designing a slice on its surface, testing each kind of surface, the technology of a surface and of its design system, seeding memory and review rules, decision records, moving a memory update into Phoenix memory, deployment, environments and the lock.

## Expectation
- Scenario: A team's work tool is proposed a browser page where team leads plan the week, with the screen sizes it serves and the design system its screens work within, from the project's style guide and the Phoenix memory learnings for a browser surface. The product owner confirms them. Two slices designed later on that page follow the same screen sizes and design system, and when the product gains a mobile app, the surfaces are updated and what held before stays readable with why it changed.
- Done means: Someone other than the one who declared the surfaces checks each surface, property and guideline and finds its reason, a source in the project or in memory, and the person who confirmed it.
- Done means: Someone other than the slice's designer compares each slice's design with the properties and guidelines of its surface, and finds no difference that a gap or an update does not explain.
