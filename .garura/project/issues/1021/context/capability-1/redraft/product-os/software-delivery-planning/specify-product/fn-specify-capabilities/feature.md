# Feature: Specify capabilities

## What it does
This feature writes a full page for each capability, creates the capability's features with their pages, and sets what the capability needs in quality and compliance. It takes its work from three places: the capabilities a person names, every capability in the model still at the directional depth, and the capabilities a prototype's screens show. A capability at the directional depth has a short page with only its directional intent. This feature raises it to full depth, called detailed in the model's index, with its benefit hypothesis, boundary, guiding rules and features. One run does all of them together. It is the last detailing step, so the writing is complete but still in product words, not code. The earlier steps are Specify intents and Specify domains, which write the business intents and the domains, but it needs neither to run first.
A product owner gets from it the detailed capabilities and features that later shaping work turns into slices a person can test end to end.

Status: built, except checking each ICE against the rubric. An ICE is the agent's intent for one capability or feature: what an agent must make true there, for whom, and how it is checked. The rubric is the written rule for what a good ICE looks like.

## Inputs / Outputs
- In: the names of the capabilities to detail, if any.
- In: a prototype's capture, if any: its views, its journeys and any write-up from the person.
- In: for a named capability the model lacks, the person's answers: what it is, why it matters and which existing domain it joins.
- In: the capability's knowledge shelf, and the product profile as it stands when the run starts. The product profile holds the product's shape and the quality levels it commits to.
- Out: one full page for each capability, with its benefit hypothesis, boundary, guiding rules, features and sources.
- Out: one page for each feature, with what it does, its inputs and outputs, its rules, its acceptance criteria, what is out of scope and its sources.
- Out: index entries for each capability and feature.
- Out: each capability's quality needs, each with a level (none, low, medium, high or xhigh), a target someone can measure and how it is checked, and any compliance regimes it triggers.
- Out: the firmed product profile, and one decision record for each move of its committed levels.

## Rules & behavior
- A capability seeded here holds only what its source said: the person's recorded answers, or the screens it was read from. The save refuses any other seed. The save is the one script step that writes the model's index, the profile and the decision records.
- A named capability the model lacks starts with questions. The run asks for all of them at once, before it opens any change. With no answer, or a domain the model lacks, it stops and says what it needs, and it leaves nothing behind. Inside the loop, that capability becomes the loop's question and the others go on. The loop is the discovery loop, which reads a prototype once and runs Specify intents, Specify domains and this feature on that reading, in rounds.
- A capability from the screens with no known domain waits in a holding folder. The holding folder is a place in the model for capabilities whose domain is not known yet. It is kept, and it is not ready until it is linked to a domain.
- From a capture, a feature is something a person does or sees on the screens, named in the words its users would use. One panel, count or label is a part of the feature that shows it, never a feature of its own.
- Each page says where it is seen: each screen with its exact words, in quotes. A check tests each quote against the prototype's text.
- A behaviour the screens do not show is written as our default and marked as ours. It is never left as an open question. Only a business rule that the agent intent cannot be written without goes back as a gap.
- Quality levels only go up. Each level in the profile becomes the highest of the current level and each capability's need. Each capability is measured against the profile as it stood at the start, so one capability's move cannot hide behind another's.
- The first run firms a still-rough profile to set, with no decision record. Set means its levels are now committed. The reason there is no record: a rough profile has no committed level yet, so firming it moves nothing. On a set profile, a need above its level stops at the checkpoint as its own line, and each move gets its own decision record. The checkpoint is the one point where the run shows the person every change and, run by hand, waits for a yes before anything is committed. Inside the loop, these records read proposed.
- One run has one save, one checkpoint and one commit for all its capabilities. The reason: one capability at a time was too slow, and the person approves every capability and every profile move together, before anything is committed. If one cannot pass its checks, the whole run stops and nothing is committed.
- The structure check reads the label and the length of each agent intent line. An agent intent line is one line of an ICE, such as its Goal. No step reads the ICE rubric yet. So nothing checks yet that an ICE keeps the rubric's rules, such as exactly one Goal.

## Acceptance criteria
- Given a capability at directional depth and no names, when the run is approved, then its page and entry read detailed and it has at least one feature, each with an entry and a page.
- Given a named capability already at full depth, when the run starts, then it stops and does not detail it again.
- Given a named capability the model lacks and no answers, when the run starts by hand, then it stops before any change opens and says what it needs.
- Given a capture and a capability with no known domain, when the run saves, then its page is in the holding folder and its domain is empty.
- Given a page that quotes words the prototype does not have, when the sources check runs, then it reports that quote.
- Given a set profile and a need above it, when the run reaches the checkpoint, then the checkpoint shows the capability, the dimension and the levels from and to as one line.
- Given three capabilities and one that cannot pass its checks, when the run ends, then nothing is committed.

## Out of scope
- Writing business intents. Specify intents (fn-specify-intents) does this.
- Writing domain pages. Specify domains (fn-specify-domains) does this.
- Shaping slices or setting priorities. Later shaping work does this.

## Sources
- The product owner approved this page and its ICE on 2026-11-06.
- core/components/plays/discover-capabilities/reference/ice.md: "One run details every target", "The screens decide the capabilities and the features", "The capability's NFR needs are per-capability and concrete", "Profile roll-up is monotonic-up", "One run, all or nothing"
- core/components/plays/discover-capabilities/scripts/check_sources.py: "quoted string (in double quotes) on a source line is on the prototype"
- core/components/plays/discover-capabilities/scripts/lint_grounding.py: "The agent intent section: labelled bullets only, known labels, at least one Goal."
- core/components/skills/enrich-capability-ice/SKILL.md: "Fill what the screen does not show; never leave it open.", "Every page says where it is seen"
- standards/rules/ice-rubric.md, in Phoenix memory: "What a good ICE looks like."
- core/components/plays/discover-capabilities/reference/ice.md: "promote its `capability.md` from the directional stage to the detailed stage (benefit hypothesis, boundary, guiding rules, features)", "one at a time is too slow", "one human checkpoint that approves every target's detailed grounding and every box-move before anything is committed", "On a still-directional box the roll-up establishes it and firms it to `set`.", "Against an already-`set` box, a need (an NFR level or a compliance regime) that exceeds the committed ceiling is an out-of-box event", "in the holding folder `capabilities/<capability>/` with its domain empty", "is done by the deterministic keyed persist script"
- core/components/plays/discover-domains/reference/ice.md: "Each kind has one writer: /discover-intent writes business intents, /discover-domains writes domains, /discover-capabilities writes capabilities and features. None needs another to run first", "shaping the detailed model into slices a person can test end to end"
- core/components/loops/complete-discovery/SKILL.md: "reads the prototype once and runs /discover-intent, /discover-domains and /discover-capabilities on that one reading"
- standards/schemas/product-os/ontology.md, in Phoenix memory: "The agent's intent for one capability or one feature: what an agent must make true there, for whom, and how it will be checked."
- standards/rules/ice-rubric.md, in Phoenix memory: "Exactly one. This is not negotiable."
