# Feature: Bring the current map to every project

## What it does
Every project reads the same current map by its place in memory, through the memory tool, so that the agents of every project write and check their model by the version that Garura's source holds.
- The settings name the map by its place in memory, not by a path: `ontology: standards/schemas/product-os/ontology.md`. A play hands that name to its agent, and the agent reads the map through the memory tool.
- Phoenix memory holds the map. On 2026-11-11 the memory tool answered it from Phoenix memory at version 15, and its 893 lines were the same as Garura's source, word for word. Garura memory in this repository holds no copy, so a lookup goes on to Phoenix memory.
- Plays read it this way today. /discover-intent's sub-agent reads "the ontology through the memory tool (by its name, the config's `product.ontology`)". /shape-slice's sub-agent copies the Business Intent kind into the issue's short-term memory through the memory tool, and hands that copy to the skill that drafts the intent.
- The gap that the current ontology and other current standards are in no memory tier was found when Phoenix memory held version 4. Its part on the map holds today. Its wider check, of every standard the parts read, is Memory's, so that Phoenix memory stays up to date as Garura is built.
- Examples, in different kinds of project:
  - In a clinic's booking app, the sub-agent that drafts a new intent reads the Business Intent kind through the memory tool, and gets version 15, the same as Garura's source.
  - In a bank's payments service, the project's own memory holds no copy of the map, so the memory tool answers from Phoenix memory.
  - In a game studio's build, a new version of the map reaches Phoenix memory, and the next run of a play reads it, with no file of the project changed.
- How it meets the capability: "People and agents share one agreed map" only when every project reads the same one.

Status: built. Not built, or open:
- A change to the map lands in Garura's source. It reaches Phoenix memory only by hand, and nothing checks that the two still agree after a change.
- Phoenix memory has no version for each release, and no notes.
- Phoenix memory still holds an old page template, for the Functionality kind that the map renamed Feature.

## Inputs / Outputs
- In: the settings' place of the map in memory.
- In: the issue the play works on, for the lookup.
- Out: the map, read from the first tier that holds it, with its fingerprint, or the part of it a skill needs, copied into the issue's short-term memory.

## Rules & behavior
- The map is named by its place in memory, not by a path. The reason: "The ontology — the shape of the product model — by its place in memory."
- An agent reads the map through the memory tool. The reason: "the agent reads it through the memory tool"
- A skill reads only what its sub-agent put in short-term memory. The reason: /shape-slice's sub-agent is told to "copy the ontology's Business Intent kind (the config's product.ontology) into short-term memory through the memory tool".
- Every project reads the same version. The reason: "People and agents share one agreed map of what a product is made of, changed only on purpose."
- Not decided: which version of the map a project reads when the Garura it has installed is older than the map in Phoenix memory.

## Acceptance criteria
- Given a project with no copy of the map in its own memory, when a play's agent looks the map up through the memory tool, then Phoenix memory answers it.
- Given Phoenix memory and Garura's source, when the map is read from both, then the two are the same, word for word.
- Given a play that needs one kind, when its agent gathers context, then it copies that kind into the issue's short-term memory through the memory tool, and the skill reads that copy.
- Given a new version of the map in Garura's source, when it lands, then Phoenix memory holds it in the same release. This is not built.

## Out of scope
- Keeping Phoenix memory in step with Garura's source, and its versions and notes. Memory, in Standards, structure, settings and memory, owns it, in Keep Phoenix memory in step with Garura's source, versioned per release with its notes.
- What the map says. Write down what a product is made of: the kinds, what each holds, how they link, the rules and a real example of each (fn-597) does it.
- The memory tool itself. Memory, in Standards, structure, settings and memory, owns it.

## Sources
- The capability list: "People and agents share one agreed map of what a product is made of, changed only on purpose."
- core/config.yaml, lines 181-183: "The ontology — the shape of the product model — by its place in memory.", "the agent reads it through the memory tool", "ontology: standards/schemas/product-os/ontology.md"
- core/components/plays/discover-intent/SKILL.md, line 75: "the ontology through the memory tool (by its name, the config's `product.ontology`)"
- core/components/plays/shape-slice/SKILL.md, line 251: "copy the ontology's Business Intent kind (the config's product.ontology) into short-term memory through the memory tool"
- The memory tool, run on 2026-11-11: `find` for the map answered from Phoenix memory, `standards/schemas/product-os/ontology.md`, and found nothing in Garura memory; a read of all 893 lines was the same as Garura's source, word for word. A `find` for the page templates found `functionality.md` in Phoenix memory beside `feature.md`.
- .garura/product/product-os/software-delivery-planning/memory/capability.md, line 42: Keep Phoenix memory in step with Garura's source, versioned per release with its notes (fn-phoenix-in-step); line 49: "A change reaches Phoenix memory only by hand, and Phoenix memory has no version per release and no notes"
- The stock-take of Product model (2026-11-11), section 1.3.
