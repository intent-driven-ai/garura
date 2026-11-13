# Feature: Show the findings to the product owner, and hand them to the next capability

## What it does
When the findings are drawn or change, this feature shows the product owner one current report of what consumers want and what the competition is doing, each finding with the items it rests on, how sure it is and where it is placed, with what is new or has moved since he last read it, and hands the same findings, whole, to the next capability of Run → Product, so that what needs to be done next starts from them.
- The report holds every finding, in parts: the wants, placed on the product; what the competition is doing; the possible new needs that fit no part; the findings against an intent; and, apart, the defects and the parts no page names, each with the owner it is named for.
- Each finding shows its items, its counts and how sure it is. The weak findings are in a part of their own, marked weak, and are never left out.
- The findings are ordered by facts a person can check, such as how many items they rest on, never by the agent's own view of what matters.
- What is new or has moved since the last report is marked, so the product owner reads what changed first.
- Nothing waits for his yes, because nothing outside the findings changes. Only the choice of competitors to follow asks for his yes, and that is asked where it is proposed.
- The next capability of Run → Product takes the same findings, with their items, counts, weak marks and places, never a summary of them.
- It says what consumers want and what the competition is doing. What to do about it, building a feature or changing the model, or recommending it, is the next capability's work.
- What it shows, for example, in different kinds of product: for a shop's checkout, that the want about the delivery cost grew this month and now rests on two connections; for a clinic's booking app, a new possible need, paying when booking, marked weak; for a team's planning tool, a defect on its board view named for its fixer, apart from the wants.
- How it meets the capability: the understanding is worth something only when it reaches the person who decides and the capability that acts, and the product owner wants work of this kind done by an agent, as he said of continuous integration, "basically reflecting and telling us what needs to be done."

Status: not built. Nothing shows a product's wants or competitors to anyone. What exists covers only patterns for it:
- The plays' briefs show a person what was found with its basis: in the slice play, "A proposed answer always names its source; where none exists the question carries no proposed answer, and the count is shown."
- The cardinal rule in memory on recommendations: "The gap is reported."
- A review tool where people review what agents make is planned, and not built for findings of this kind.

## Inputs / Outputs
- In: each finding with its items, counts, weak mark and places, from Place each finding on the intents, capabilities and features it bears on (fn-place-findings).
- In: the earlier report, to mark what is new or has moved.
- In: the project's setting for when the report reaches the product owner.
- Out: one current report for the product owner, in the parts above, with what is new or moved marked.
- Out: the same findings, whole, for the third capability of Run → Product.

## Rules & behavior
- Every finding is shown, and a weak one is shown as weak, in a part of its own. The reason: a weak finding shown as strong sends the next step after the wrong change, and memory's cardinal rule asks that "The gap is reported."
- Each finding shows what it rests on. The reason: "Each finding says where it comes from. The reason: a person can then check each finding without a search."
- Ordered by facts, never by the agent's view. The reason: an order a person cannot check is a judgment hidden in the layout.
- Nothing waits for a yes. The reason: nothing outside the findings changes, and the product owner asked for this work to be "built for high autonomy".
- Handed on whole. The next capability gets the findings as written, never a summary. The reason: what it builds or recommends must rest on the same items a person can check.
- It says what is wanted, never what to do. The reason: building features, or updating the product intent model, "or at least making those recommendations", is the next capability's, by the product owner's list.
- Not decided: how often the report reaches the product owner, and which change is big enough to tell him before the next report. These are project settings, and no source sets them.
- Not decided: where the report is kept and where he reads it, such as a file in the project or the planned review tool.

## Acceptance criteria
- Given findings with one weak want, when the report is shown, then the weak want is in the part for weak findings, marked weak, with its items.
- Given a want that rests on more items than last month, when the report is shown, then it is marked as moved, with both counts.
- Given a defect named for Fix defects test first, when the report is shown, then it is apart from the wants, with its owner named.
- Given the findings handed to the next capability, when they are compared with the report, then they hold the same findings, items, counts, weak marks and places.
- Given any report, when it ends, then nothing outside the findings has changed and no yes was asked except for a competitor to follow.

## Out of scope
- Drawing and placing the findings. Understand what consumers want, from what is taken in (fn-understand-consumer-wants), Understand what the competition is doing, from what people say about it (fn-understand-competition) and Place each finding on the intents, capabilities and features it bears on (fn-place-findings) do them.
- Recommending or making a change. The third capability of Run → Product does it.
- Building the review tool. Review what agents make, in Developer tooling, owns it.

## Sources
- The product owner on 2026-11-10, spelling tidied: "start building features into the product or start updating the product intent model automatically, or at least making those recommendations", "This needs to be built for high autonomy.", "basically reflecting and telling us what needs to be done."
- The list the product owner set on 2026-11-10: "Build features into the product, or update the product intent model, automatically, or at least recommend those changes."
- The capability list the product owner agreed on 2026-11-03, in the same file: "Review what agents make (Argus): People review ADRs, memories, domains, capabilities and ICE in one tool."
- .garura/product/product-os/software-delivery-planning/keep-spec-matched/fn-find-spec-drift/feature.md: "Each finding says where it comes from. The reason: a person can then check each finding without a search."
- core/components/plays/shape-slice/SKILL.md: "A proposed answer always names its source; where none exists the question carries no proposed answer, and the count is shown."
- standards/rules/no-unbacked-recommendation.md, in Phoenix memory: "The gap is reported."
