# Feature: Update the understanding as new items come in and the product changes

## What it does
As new items come in, the product model changes, or the product owner changes which competitors are followed, this feature updates the findings: a want that grows or fades, a new want, a place whose part was added, changed, merged or retired, and a competitor added or dropped; what held before stays readable with why it changed, so the understanding stays current and its history shows how each want moved.
- New items rest under the wants they bear on, or start a new want. A want that stops coming up is marked as fading, never deleted.
- When the model changes, an intent, capability or feature is added, changed, merged or retired, and the places of the findings it touches are worked out again, with why.
- A competitor to add or drop is proposed from what changed, such as a rival people now name often, or one no one names any more, and from the product owner's word; he says yes to each. What was found about a dropped competitor stays readable.
- Each update keeps what held before: the finding as it was, what changed, and why, such as the new items that moved its count.
- It runs on its own each time new items come in or the model changes, without a person's yes, except for a change to the competitors followed.
- What it updates, for example, in different kinds of product: for a clinic's booking app, the want for evening appointments grows after a new clinic joins, and its old count stays readable; for a team's planning tool, two capabilities are merged, and the wants placed on the old one are placed again on the merged one; for a recipe app, a rival closes and stops being named, so dropping it is proposed.
- How it meets the capability: what consumers want and what rivals do changes over time, and a finding placed on a part that no longer exists points nowhere, so the understanding is worth something only while it is kept current.

Status: not built. What exists covers only patterns for it:
- The approved update features of other capabilities work this way: "a person confirms an update, and what held before stays readable with why it changed". Update the connections as the product and its tools change does the same for the first capability of Run → Product. None of them is built.
- The product owner's wording, on the project's architecture: "this should be reflected as updating arch. as the project changes."

## Inputs / Outputs
- In: the new items the first capability took in, and the records of its reads.
- In: the product model as it is now: the intent pages, the model's index, and the capability and feature pages.
- In: the earlier findings with their places, and the competitors followed.
- In: the product owner's word on a competitor to add or drop.
- Out: each updated finding, with what held before, what changed and why.
- Out: each want newly marked as fading, and each place worked out again, with why.
- Out: each competitor proposed to add or drop, with its source, for the product owner's yes.

## Rules & behavior
- What held before stays readable, with why it changed. The reason: the approved update features keep it the same way, and how a want moved over time can be read only from what it was before.
- A want that stops coming up is marked as fading, never deleted. The reason: a want can come back, and a want deleted without a word would read as never asked.
- A change in the model means the places it touches are worked out again. The reason: a finding placed on a part that was merged or retired points nowhere.
- The product owner says yes to each competitor added or dropped. The reason: who the competition is, is his judgment, as when it was first chosen.
- It runs on its own otherwise. The reason, in the product owner's words: "This needs to be built for high autonomy."
- Memory first, then research through a memory update a person approves. The reason: no update comes from what the AI agent knows by itself.
- Not decided: how long a want must stop coming up to be marked as fading. It is a project setting, and no source sets it.
- Not decided: how the update learns that the model changed: by reading the model at each run, or by being told by the part that changed it.

## Acceptance criteria
- Given new items that add to a want, when the understanding is updated, then the want shows its new count and its count before, with the items that moved it.
- Given a capability merged into another, when the understanding is updated, then each finding placed on the old capability is placed again, with why, and its old place stays readable.
- Given a want with no new item for the time the project sets, when the understanding is updated, then it is marked as fading and still listed.
- Given a rival that people no longer name, when dropping it is proposed, then it is still followed until the product owner's yes, and what was found about it stays readable after.

## Out of scope
- Drawing the first findings. Understand what consumers want, from what is taken in (fn-understand-consumer-wants) and Understand what the competition is doing, from what people say about it (fn-understand-competition) do it.
- Changing the product model. Keep the spec matched to what's built changes its pages and links, and the third capability of Run → Product recommends changes.
- Changing the connections. Update the connections as the product and its tools change does it.

## Sources
- The product owner on 2026-11-10, spelling tidied: "This needs to be built for high autonomy."
- The product owner on 2026-11-07, in .garura/product/product-os/software-delivery-planning/design-technology-architecture/capability.md: "this should be reflected as updating arch. as the project changes."
- .garura/product/product-os/software-delivery-planning/environment-setup/fn-update-environments/feature.md: "a person confirms an update, and what held before stays readable with why it changed"
- .garura/product/product-os/software-delivery-planning/connect-use-and-market/fn-update-connections/feature.md: "As the product and its tools change, this feature proposes a new, changed or dropped connection"
- .garura/product/product-os/software-delivery-planning/keep-spec-matched/capability.md: "In: keeping each intent's links to the parts that serve it current."
