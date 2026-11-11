# Feature: Name an intent's drift

## What it does
Finds where an intent and the product no longer agree, and names the drift to a person.
- Drift is a difference between parts that the model's rules say should agree. Any play may write any part, in any order, and the rules say what holds once the model is aligned. So drift is expected, and it must be found and named.
- For a business intent, the cases the model's records name are:
  - a link held on one side only: a part's entry in the model's index names the intent and the intent's Touches list does not name the part, or the reverse;
  - an intent that no capability serves;
  - an ICE whose capability serves no confirmed intent. An ICE is the agent's intent for one capability or feature. Such an ICE is kept, and no work starts from it.
- One more case follows from where intents live: the intent's page and its issue in the tracker say different things.
- For each case it names the intent, the part or the issue, and what disagrees. It never changes a person's words itself.

Status: not built. Older records send drift to an "Alignment loop", which is not built and has no approved name or place. Today, the gap finder inside the discovery loop finds the first two cases, during discovery only.

## Inputs / Outputs
- In: the intent pages, the model's index, and each intent's stage.
- In: each intent's issue in the intents tracker.
- Out: a list of drift, one entry for each case, naming the intent, the part or issue, what disagrees and which side is missing, for a person to decide.

## Rules & behavior
- It names; it does not decide. Only a person confirms or drops an intent, and a change to its words is theirs. The reason: an agent that fixed the intent would replace what the person wants with what the agent found.
- A drift never stops a write. The rules say what holds once the model is aligned, and what a rule can stop is work, never a write. The reason: what is found in the middle of work is kept, not lost while it waits for the right step.
- It covers drift with an intent in it. Drift between other parts, such as two ICE for one part or a story out of date with its ICE, belongs to other work.
- Where it runs is not decided. The product owner names the loop or play that runs it later. Today, outside the discovery loop, nothing finds drift.

## Acceptance criteria
- Given a capability whose index entry names an intent whose Touches list does not name it, when the check runs, then it names the intent, the capability and the missing side.
- Given an intent that a person dropped while a capability still serves it, when the check runs, then it names both.
- Given any drift it finds, when the check ends, then no intent page has changed.

## Out of scope
- Making a missing link. The gap-closing step does it inside the discovery loop, and Keep an intent current (fn-keep-intent-current) keeps the intent's side.
- Drift with no intent in it: two ICE for one part, a thin mark kept in one place only, or a story out of date with its ICE. Manage the model and Turn intents into agent work own them.
- Sorting new input against the intents that exist, and a clash between two intents. Specify against what exists (fn-specify-against-existing) will do it.

## Sources
- The one line the product owner approved on 2026-11-03: "the intents stay up to date as the product evolves, with no drift"
- .garura/product/product-os/intents/bi-1.md: "An intent that drifts from the product gets named."
- standards/schemas/product-os/ontology.md, in Phoenix memory: "The rules below say what holds once the product is **aligned**; they never stop a write.", "Drift between them is found and fixed by the Alignment loop.", "What a rule can stop is work, never a write"
- standards/schemas/product-os/ontology.md, in Phoenix memory: "An ICE whose capability serves no confirmed business intent is kept, not worked on, and is drift for alignment, never a blocked write.", "Two ICE for one part are drift; the Alignment loop merges them."
- core/components/skills/find-model-gaps/SKILL.md: "Every `one_way` entry is a gap: a link is made only when both"
- core/components/skills/find-model-gaps/scripts/find_gaps.py: "`intents_unserved` — intent pages no capability or feature names in `intents`;"
- docs/adr/031-business-intent-and-ice.md: "(its own drive, not yet designed)", "Until the Alignment drive exists, drift is found only by the linter's warnings and the workable check."
- docs/adr/066-names-say-who-does-the-work-five-roles-own-the-verbs.md: "the Alignment loop is unapproved and unnamed"
- docs/adr/065-the-models-index-is-changed-through-two-skills-the-model-never-names-a-plan-and-only-tools-know-the-tracker.md: "Business intents and agent work each live in a tracker named in the project's settings."
