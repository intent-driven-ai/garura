# Feature: Update the recommendations as the findings and the product change

## What it does
As the findings move, the product model changes, or the product owner changes which kinds of change may go ahead on their own, this feature updates the recommendations and the changes still in flight: one whose findings grew or faded shows it, one whose part was merged, retired or already changed is worked out again or withdrawn, with why, and a turned-down one is raised again only when its findings move; what held before stays readable with why it changed, so that the recommendations stay true to what consumers want now.
- The findings move when the second capability updates them: a want grows, fades or gains a new place, and a competitor is added or dropped.
- The model changes when an intent, capability or feature is added, changed, merged or retired, by this capability's changes or by any other part.
- What it updates, case by case:
  - a waiting recommendation whose findings grew or faded shows both the old and the new weight;
  - a waiting recommendation whose part was merged or retired is worked out again on the part that took its place, or withdrawn with why;
  - a waiting recommendation that another change already met is withdrawn, naming that change;
  - a turned-down recommendation is raised again when its findings move, showing what moved;
  - when the setting changes, it applies to what has not gone ahead yet, and nothing that went ahead is taken back by the setting alone.
- A change that already landed is never undone by an update. When its findings fade, taking it back is a new recommendation for the product owner.
- Each update keeps what held before: the recommendation as it was, what changed and why.
- It runs on its own each time the findings, the model or the setting change.
- What it updates, for example, in different kinds of product: for a team's planning tool, two capabilities are merged, and a recommendation on the old one is worked out again on the merged one; for a shop's checkout, the want for showing the delivery cost earlier fades after the cost moved to the first page, and the waiting recommendation is withdrawn, naming that change; for a clinic's booking app, a want for paying when booking, turned down while it was weak, grows strong over three months and is raised again.
- How it meets the capability: a recommendation is worth something only while its findings and its part still hold, and the product owner's wording rule for such parts is updating them "as the project changes".

Status: not built. What exists covers only patterns for it:
- The approved update features of other capabilities work this way: "a person confirms an update, and what held before stays readable with why it changed". Update the understanding as new items come in and the product changes does the same for the findings, and it is not built.

## Inputs / Outputs
- In: the findings as the second capability updated them, with what held before.
- In: the product model as it is now: the intent pages, the model's index, and the capability and feature pages.
- In: the waiting, turned-down and in-flight recommendations and changes, with their records.
- In: the project's setting for which kinds of change may go ahead on their own, as it is now.
- Out: each updated recommendation, with what held before, what changed and why.
- Out: each recommendation withdrawn, with why, and each raised again, with what moved.
- Out: each landed change whose findings faded, as a new recommendation to take it back.

## Rules & behavior
- What held before stays readable, with why it changed. The reason: the approved update features keep it the same way, and a later reader can see why a recommendation moved.
- A recommendation is withdrawn, never deleted. The reason: a recommendation deleted without a word would read as never made.
- A change in the model means the recommendations it touches are worked out again. The reason: a recommendation on a part that was merged or retired points nowhere.
- A landed change is never undone by an update. Taking it back is a new recommendation. The reason: what landed was approved or allowed, and undoing it is a change of its own that the product owner decides.
- A setting change applies to what has not gone ahead yet. The reason: what went ahead was allowed when it went, and taking it back is his choice, not the setting's.
- It runs on its own. The reason, in the product owner's words: "This needs to be built for high autonomy."
- Not decided: how long a want must fade before a waiting recommendation is withdrawn. It is a project setting, and no source sets it.
- Not decided: how the update learns that the model changed: by reading the model at each run, or by being told by the part that changed it.

## Acceptance criteria
- Given a waiting recommendation whose want grew, when the recommendations are updated, then it shows the want's weight before and after, with the items that moved it.
- Given a capability merged into another, when the recommendations are updated, then each waiting recommendation on the old capability is worked out again on the merged one, with why, and its old form stays readable.
- Given a turned-down recommendation whose want grew from weak to strong, when the recommendations are updated, then it is raised again, showing what moved.
- Given a landed change whose want faded, when the recommendations are updated, then the change stays as it is and a new recommendation to take it back is shown.

## Out of scope
- Updating the findings. Update the understanding as new items come in and the product changes, in the second capability, does it.
- Changing the model. The part that owns each page, link or part does it.
- Changing the setting. The product owner does it, through Let the changes the product owner allows go ahead on their own, and show each one with a way back (fn-act-on-its-own).

## Sources
- The product owner on 2026-11-10, spelling tidied: "This needs to be built for high autonomy."
- The product owner on 2026-11-07, in .garura/product/product-os/software-delivery-planning/design-technology-architecture/capability.md: "this should be reflected as updating arch. as the project changes."
- .garura/product/product-os/software-delivery-planning/environment-setup/fn-update-environments/feature.md: "a person confirms an update, and what held before stays readable with why it changed"
- .garura/product/product-os/software-delivery-planning/understand-consumers-and-competition/fn-update-understanding/feature.md: "As new items come in, the product model changes, or the product owner changes which competitors are followed, this feature updates the findings"
