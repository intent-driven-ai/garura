# Feature: Specify domains

## What it does
This feature finds each domain the product sits in and writes a full page for it. A domain is a field the industry names, such as customer relationship management or e-commerce. The feature asks two questions in order: which field does the product serve, and which job does it do there? Each answer can be a domain, so a product often sits in more than one. It works from business intents, a typed goal, a prototype's capture or any mix of them. With none of those, it asks for a goal.

Status: built.

## Inputs / Outputs
- In: business intents, if any. It accepts a proposed intent the same as a confirmed one.
- In: a typed goal, if any.
- In: a prototype's capture, if any: its views, its journeys and any write-up from the person.
- In: the knowledge shelves, which are what memory holds about a field, and research for a field no shelf holds.
- In: what the model already holds. It reads capabilities only as context and never changes them.
- Out: one full page for each domain, with its intent, business goal, guiding rules, the kinds of capability it covers in plain words, its scope and its sources.
- Out: one entry in the model's index for each domain, linked to the intents it serves.
- Out: one rough product profile, only when none exists: the product's stage, users, way of earning and surfaces (where people use it, such as the web), with coarse quality levels.
- Out: on each linked intent page, a line that names the domain and marks it as added or changed.
- Out: warnings for anything missing or odd, such as an intent page that is gone or an intent no domain serves.

## Rules & behavior
- A domain is a field that vendors, analysts and buyers name. A principle, a practice, a regulation or a quality, such as accessibility or compliance, is never a domain. Nor is the field of one feature many products share, such as comments, search or sign-in.
- A knowledge shelf comes first. A domain with no shelf gets a proposal that names it as its research names it, with the research links. The name never comes from the product's screens or sample data. The run records the proposal and goes on.
- From a capture, every main section must sit in a domain, with the line from the shelf or research that covers its work and where that line is from. For a section no field covers, the run researches the field that does that work and never stretches a found field over it.
- A domain that holds no main section is not written. It is not a field the product sits in.
- A page that exists is grown. A light page is raised to a full one and keeps what it said. An entry's depth never goes down, no domain is added twice, and a run with nothing new changes nothing.
- The page's Capabilities section describes kinds of capability in plain words. It names no capability entry, because capabilities have their own writer.
- The profile stays rough, at the directional state. The run never sets it firm, because the capabilities' real needs are not known yet.
- One checkpoint shows each domain and the profile, with the real changes to the model. A learned policy may pass a known shape of change with no wait, but only when no check found a blocking problem. Each crossing goes in a log. A cancel puts the model back.

## Acceptance criteria
- Given only a typed goal and an empty model, when the run is approved, then at least one domain has a full page and an index entry, the profile reads directional, and no capability exists.
- Given a domain page with no Sources section, when the grounding check runs, then it fails.
- Given a capture with a main section no listed domain covers, when the grounding check runs with the journeys, then it fails.
- Given a listed domain that holds no main section, when the grounding check runs with the journeys, then it fails.
- Given a model that needs nothing new, when the run goes again, then every model file stays byte for byte the same.
- Given an intent whose page is gone, when the run goes, then it completes and records a warning for that page.
- Given a person who cancels at the checkpoint, when the run ends, then the model returns to how it was.

## Out of scope
- Writing or placing capabilities and features. Specify capabilities (fn-specify-capabilities) does this.
- Firming the product profile. Specify capabilities (fn-specify-capabilities) does this too.
- Writing business intents. Specify intents (fn-specify-intents) does this.

## Sources
- The product owner approved this page and its ICE on 2026-11-06.
- core/components/plays/discover-domains/reference/ice.md: "Grounded, not invented", "A principle, a practice, a regulation or a quality", "Reads the product, not the sample", "Keep what is there", "Directional state", "Exactly one human checkpoint"
- core/components/plays/discover-domains/SKILL.md: "which field the product serves"
- core/components/skills/author-domains/SKILL.md: "A recognised domain, never a made-up one", "Every main section in a field that covers it"
