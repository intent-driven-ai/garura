# Feature: Find where the spec and what's built no longer match

## What it does
It finds drift, the places where the spec no longer matches what the agents built and planned, and names each one to a person, for the person to decide.
- The spec is what the product model says the product is for and what it does: the business intents, and the domains, capabilities and features that serve them. A business intent is what a person or the organisation wants, in their own words. The product model is the shared map of the product that people and agents read.
- What is built is the code and the work that landed. What is planned is the work items in the team's tracker, each intent's issue there, and the plan files that hold the work items as a tree. The tracker is the tool where a team keeps its issues, such as GitHub.
- It looks at the inside of the work only: what the agents built, changed and planned. What users say or do once the product runs is not part of it. The Run → Product business intent (BI-6) asks for that.
- It looks for these kinds of drift, each a place where the spec and the work differ:
  - a part built, or a work item filed, that has no page in the model;
  - a page that says something the work no longer does;
  - a link between an intent and a part that is missing, held on one side only, or wrong;
  - an intent's issue in the tracker that says something its page does not;
  - a story that is out of date with its ICE. A story is the work item that delivers one feature, and an ICE is the agent's intent for one capability or feature. When the ICE changes after the story is written, the story no longer says what the ICE asks.
- For each difference, it says what the spec says, what the work shows, where each comes from, and which feature would fix it.
- After the person's yes, each fix is made by the feature or capability that owns the part, and the check runs again.
- The feature exists because the model falls behind the work. Features are found and built while the work is under way, stories are filed straight in the tracker, and plans are closed without the model being touched. Agents decide from the model, so a model that is out of date leads them in the wrong direction.

Status: not built. Older records send drift to an "Alignment loop", which has no approved name or place. What exists today covers only parts of it:
- The gap finder finds links to an intent held on one side only, and intents that no part serves. It looks inside the model only, and runs only in the discovery loop.
- The play that manages a plan in a working session checks that the plan file, the tracker and the model agree, but only for the items its own session changed.
- An older play, written to update the model to match what shipped, is marked stale and waits for a rebuild.

## Inputs / Outputs
- In: the spec: the intent pages, the model's index, and the pages of the domains, capabilities and features with their ICE. The index is the model's list of every part, with its parent and the intents it serves.
- In: what is planned: the plan files, the work items and each intent's issue, as the tracker holds them now.
- In: what is built: the code and its history in the repository.
- Out: a list of drift, with one entry for each difference: the part, what the spec says, what the work shows, where each comes from, and the feature that would fix it.
- Out, after the person's yes: each fix, made by the feature that owns it, and a second run of the check that finds nothing.

## Rules & behavior
- It names, and a person decides. The check changes no page and no work item. The reason: the spec is what the person approved, so a fix that nobody saw would change what they approved without their knowledge.
- It compares the spec with the agents' work only. It never compares the spec with what users say or do once the product runs. The reason: this capability keeps the spec true to what was built and planned. Whether the product serves its users is a different question, with its own evidence, and Run → Product asks it.
- What was built is the ground truth for the domains, capabilities and features. When their pages and the work disagree, the fix brings the page up to match the work. The reason: agents decide from the model, so the model must describe the product as it is.
- An intent is never brought to match the work by itself. A difference with an intent is named, and the person decides whether the intent or the work changes. The reason: an intent says what a person wants, and only a person confirms or drops one.
- Each finding says where it comes from. The reason: a person can then check each finding without a search.
- Each fix is made by the part that owns it. A page goes to Update the spec to match what's built (fn-update-spec-to-match-built). A link goes to Keep an intent's links current (fn-keep-intent-links-current). An intent that the work left behind goes to Replace or retire an intent (fn-replace-or-retire-intent). An intent's issue goes to Keep the tracker's words matched to the model (fn-keep-tracker-matched). A work item goes to Turn intents into agent work. The reason: each part then has one writer and one set of checks.
- A drift never stops a write. The model's rules say what holds once it is aligned, and a rule can stop work, never a write. The reason: what is found in the middle of the work is kept, and not lost while it waits for the right step.
- It is done when a second run finds nothing. The reason: only a clean second run shows that each fix landed.
- Not decided: where and when it runs. The capability expects a review after work lands. The product owner names the loop or the play that runs it.

## Acceptance criteria
- Given a story closed as done for a feature that has no page in the model, when the check runs, then it names the story and says that the model has no page for its feature.
- Given a capability page with a rule that the code no longer keeps, when the check runs, then it names the page, the line, and what the code does instead.
- Given an intent's issue whose title differs from the title on its page, when the check runs, then it names the issue, the page and the words on each side.
- Given a feature whose ICE changed after its story was written, when the check runs, then it names the story and the ICE.
- Given any drift it finds, when the check ends, then no page and no work item has changed.
- Given the person approved the fixes, when they land and the check runs again, then it finds nothing.

## Out of scope
- Comparing what happens in use with what was intended. The Run → Product business intent (BI-6) asks for it.
- Drift inside the model with no work in it, such as two ICE for one part, a thin mark kept in one place only, or the same part written twice. Manage the model owns it.
- Making the fixes. The features named above, and Turn intents into agent work for the work items, make them.

## Sources
- The product owner on 2026-11-07, on the capability: "the internal element: how the agents are working and making sure what the agents are implementing gets updated back here, not what the user is telling."
- The one line the product owner approved on 2026-11-07: "any drift between them is named and fixed"
- The capability page the product owner approved on 2026-11-07: "a review run after work lands names every place where the spec and the work disagree, before anyone builds on it."
- .garura/product/product-os/intents/bi-1.md: "An intent that drifts from the product gets named."
- GitHub #977 (open): "The product model falls behind the work.", "stories are filed straight in the tracker", "plans are closed without the model being touched", "Agents decide from the model, so a model that is out of date leads them wrong."
- GitHub #977 (open): "a feature built or filed with no page in the model, a page that says something the work no longer does, a link that is missing or wrong"
- GitHub #977 (open): "each finding says where it comes from", "What was built is the ground truth: the model is brought up to match it, not the other way round", "After the person's yes, the model is fixed and a second review finds nothing."
- GitHub #977 (open): "Approve the fixes, and have them written into the model by the plays that own each part."
- standards/schemas/product-os/ontology.md, in Phoenix memory: "The rules below say what holds once the product is **aligned**; they never stop a write.", "What a rule can stop is work, never a write", "Only a person confirms or drops it; an agent never does."
- standards/schemas/product-os/ontology.md, in Phoenix memory: "When one of those ICE changes after the story is made, its scope of work, its Context guidance and its feature's entry in the slice's hidden file are drift for the Alignment loop."
- standards/schemas/product-os/ontology.md, in Phoenix memory: "Two ICE for one part are drift", "When only one is there, it is drift for the Alignment loop."
- core/components/skills/find-model-gaps/SKILL.md: "Every `one_way` entry is a gap: a link is made only when both"
- core/components/skills/find-model-gaps/scripts/find_gaps.py: "`intents_unserved` — intent pages no capability or feature names in `intents`;"
- core/components/plays/update-plan/scripts/check_agreement.py: "after the landing, the plan file, the tracker and the model agree", "For each item the list names"
- core/components/plays/learn-outcomes/SKILL.md: "update the LIVING product model to match reality", "waits for the rebuild of the learn loop on the current product model"
- docs/adr/031-business-intent-and-ice.md: "(its own drive, not yet designed)"
- docs/adr/066-names-say-who-does-the-work-five-roles-own-the-verbs.md: "the Alignment loop is unapproved and unnamed", "It does not move into `/loop-run-product`"
- .garura/product/product-os/intents/bi-6.md: "What happens in use flows back."
- .garura/product/product-os/software-delivery-planning/turn-intents-into-work/capability.md: "A story is not written again when its ICE changes."
