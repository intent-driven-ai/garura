# Feature: List what serves an intent, and what sits in a domain

## What it does
From any business intent, a person lists the capabilities, features and slices that serve it, and from any domain, the intents that touch it and the capabilities in it, read from the links the model already keeps, so a person, and not only a play, can see what serves an intent and where it sits.
- The data is there today, in the model's index and pages:
  - each capability's index entry names the business intents it serves, and a feature serves its capability's intents;
  - each intent page's Touches list names the parts the intent reaches into, marked adds, changes or removes;
  - each slice's entry names the intents it serves, on the slice's side only;
  - each capability names its one domain, and each domain's entry names the intents that touch it, "for search only".
- Plays read it inside their runs: /shape-slice and /shape-plan find the slices that serve an intent, and the gap finder lists the intents nothing serves.
- No command lists it for a person, and no script searches by domain.
- The ontology asks both questions: "Given a business intent, which ICE do agents work on for it?" and "Given a business intent, which slices serve it?"
- A domain is for finding things. In the ontology: "It is never in a plan and never stops work." The old capability Link the product model said: "Domains do not decide when work starts, so search is their only job."
- Examples, in different kinds of project:
  - In a shop's checkout service, the product owner asks what serves "shoppers pay fast", and sees the Checkout and Saved cards capabilities, their features, and the one slice that serves it.
  - In a bank's lending service, the technical lead asks what sits in the Lending domain, and sees the Loan application and Credit decision capabilities and the intents that touch it.
  - In a clinic's booking app, a person asks what serves "patients cancel online", and sees that nothing does yet.
- How it meets the capability: Product model's proof is "From any intent, you can list what serves it."; this feature makes that list for a person.

Status: built in part. Built: the links on both sides, and the scripts inside /shape-slice, /shape-plan and the gap finder that read them. Not built, or open:
- A command that lists what serves an intent, and a search by domain.
- 21 links are kept on one side only, so a list from the intent and a list from the part do not agree today.
- Six of the 16 intent pages have no Touches list, Product model's own page among them.
- No check that no domain is in a plan file or names an issue.
- This page once said the model had no domains; it has one today, software delivery planning.
- Later views of the same links are planned elsewhere: the Intents view of the review tool, and a graph of the product, which is not approved to build.

## Inputs / Outputs
- In: an intent's id, or a domain's id.
- In: the model's index and the intent pages' Touches lists.
- Out: for an intent, each capability and feature that serves it, and each slice that serves it, each with its page. Not built.
- Out: for a domain, the intents that touch it and the capabilities in it, each with its page. Not built.

## Rules & behavior
- A list is read from the links the model keeps, the same from either side. The reason: "Thus a search from the intent and a search from the domain always give the same answer."
- The list reads files only and changes nothing. The reason: "The search reads only files and changes nothing, so it can run at any time."
- A domain is for finding things, never a level of a plan or a work item. The reason: "It is never in a plan and never stops work.", and "they are never an issue and never part of a plan."
- A domain never changes whether a part is ready. The reason: "A new or changed domain never changes whether something is ready".
- A slice's link to its intents is read from the slice's side. The reason: "A slice serves it — the link is kept on the slice's side only".
- Not decided: whether the list shows a link kept on one side only, and how it marks it.
- Not decided: whether the list is a command of its own, a view of the review tool, or both.

## Acceptance criteria
- Given an intent, when /shape-plan gathers its plan, then it finds every slice that serves the intent.
- Given an intent nothing serves, when the gap finder runs, then it names the intent.
- Given an intent, when a person asks what serves it, then the list shows each capability and feature that serves it and each slice that serves it, each with its page. This is not built.
- Given a test model where two intents touch a commerce domain and three capabilities name it, when a person asks for that domain, then the list shows exactly those two intents and three capabilities. This is not built.
- Given a plan file or a domain entry, when the structure check runs, then no plan holds a domain level and no domain names an issue, or each one is named as a finding. This is not built.

## Out of scope
- Keeping each link on both sides. Link the parts by the map's rules: what each serves, what it needs and what led us to find it (fn-725) does it.
- Closing a link kept on one side only. Find and close the gaps inside the model (fn-close-model-gaps) does it.
- Writing domain pages and filing a capability under its domain. Specify the product, in Product → Spec, owns them, through /discover-domains.
- Showing the plans and their trees. Orchestrate agent work through planning, in Orchestration, owns it.
- The review tool's views. Review what agents make (Argus), in Developer tooling, owns them.

## Sources
- .garura/product/product-os/features/fn-726/feature.md, the old page, lines 4, 7, 28 and 40: "A domain lists the business intents and capabilities in it.", "A new or changed domain never changes whether something is ready", "Thus a search from the intent and a search from the domain always give the same answer.", "The search reads only files and changes nothing, so it can run at any time."; line 39: "Garura's own model has no domains yet"
- The copy of the old page of Link the product model: "Domains do not decide when work starts, so search is their only job."
- .garura/product/product-os/intents/bi-11.md, line 12: "From any intent, you can list what serves it."
- standards/schemas/product-os/ontology.md, in Phoenix memory, lines 71, 101, 205, 305 and 318: "Given a business intent, which ICE do agents work on for it?", "Given a business intent, which slices serve it?", "A slice serves it — the link is kept on the slice's side only", "for search only", "It is never in a plan and never stops work."
- .garura/user-provided/managing-work.md, lines 26-27: "they are never an issue and never part of a plan."
- core/components/plays/shape-slice/scripts/find_serving_slice.py and core/components/plays/shape-plan/scripts/gather_plan.py: the scripts that find the slices serving an intent
- A read of the intent pages on 2026-11-11: 10 of 16 have a Touches list; Product model's own page, bi-11, has none
- The gap finder, run from the repository root on 2026-11-11: 21 links kept on one side only
- The stock-take (2026-11-11), sections 2.9 and 6 (item 2)
