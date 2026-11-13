# Feature: Change the model's index only through the two index skills

## What it does
Every play and skill that adds, changes or takes out a part in the model's index does it through the two index skills, link-model-part and remove-model-part, in place of a script of its own, so the index has one way in, each change is all or nothing and lists what it changed, and a reviewer can tell a play that broke the rule from one not yet moved.
- The decision, ADR 065 rule 1: "`link-model-part` adds or changes a part. `remove-model-part` takes a part out, with the name of the person who approved it." "Plays move onto these two skills over time, in place of writing the index with their own scripts."
- Who writes through them today: the keeper, for a part found during work, an ICE's entry, an old part a person approved taking in, and a take-out a person approved; and /update-plan, for a feature found in a planning session.
- Who still writes with a script of its own: "`/discover-domains`, `/discover-capabilities`, `/shape-slice`, `/learn-outcomes`, `/shape-measure-lens`, `/build-epic`, `/validate-epic`, `/release-epic`". The first three are live; the other five are marked stale.
- What the skills must still grow, as asked: "a new slice, the product profile, an epic's status."
- Inside a loop, the gap closer is a third writer for now.
- The product owner's reason: "The product owner wants no redundant writers: if something needs to change the index, it uses the skill."
- Examples, in different kinds of project:
  - In a clinic's booking app, /shape-slice writes a new slice for "patients book online". Once moved, it asks the keeper, and link-model-part writes the slice's entry.
  - In a shop's checkout service, /discover-capabilities saves three capabilities, and the index changes only through link-model-part, with every file it changed listed.
  - In a bank's payments service, a reviewer reads a change that writes the index with a play's own script, and can tell from the play's ICE that it has not moved yet.
- How it meets the capability: the map is "added to, changed and pruned" through one door, so every change to the index is made, checked and listed the same way.

Status: built in part. Built: the two index skills, each all or nothing, with their tests, and the keeper and /update-plan writing the index through them. Not built, or open:
- Three live plays, /discover-domains, /discover-capabilities and /shape-slice, still write the index with their own scripts, and five stale plays too.
- The skills do not yet write a new slice, the product profile or an epic's status: "Neither skill writes the profile block in the spine or an epic's status."
- The gap closer still writes the index itself inside a loop.
- The copy of the model-write rule in Phoenix memory still reads: "Outside a loop, the play's keyed script is still the only writer of shared files." ADR 065 names that rule among what it changes.

## Inputs / Outputs
- In: a request from the play or the run that asks: each part, its kind, and what to add, change or take out; for a take-out, the person who approved it.
- In: the model's index and its pages.
- Out: the changed index, its comments and layout kept.
- Out: the skill's report, with what was written, changed or removed, and every file changed.

## Rules & behavior
- Two skills write the index: one adds or changes, one takes out. The reason: "`link-model-part` adds or changes a part. `remove-model-part` takes a part out, with the name of the person who approved it."
- Each changes only what its request names, and lists every file. The reason: "Each changes only what its request names, and the links that would otherwise point at nothing, stays inside the model, and lists every file it changed."
- No play keeps a writer of its own once the skill can do the change. The reason: "if something needs to change the index, it uses the skill."
- Until a skill can do a change, the play's own script keeps it. The reason: "what the two skills can't do yet stays with its play until they can."
- A stale play moves when it is rebuilt. The reason: "Stale plays move when they are rebuilt, not before."
- The index keeps its comments and layout. The reason: "the spine keeps its comments and layout."
- Not decided: when each live play moves; in ADR 065's words, ""Over time" has no date and no list."
- Not decided: the name of the skill that takes a part out. As asked: "The verb `remove` is not decided here."

## Acceptance criteria
- Given a part found during work, when the keeper adds it, then its entry is written by link-model-part and by no other script.
- Given a take-out with the person's name, when it runs, then only remove-model-part changes the index, and its report names the person.
- Given a run of /shape-slice that writes a new slice, when it saves, then the index changes through the two skills. This is not built.
- Given a run of /discover-capabilities, when it saves its capabilities, then the index changes through the two skills, and the play's ICE says so. This is not built.
- Given a round of a loop that closes gaps, when it writes the index, then it does so through the two skills. This is not built.

## Out of scope
- The words of each page. Change a part from words a person approved (fn-change-part) does them, through the page skill.
- Rebuilding each play from its ICE to move it. Build your own harness, in Standards, structure, settings and memory, owns /edit-play, which does it.
- Keeping Phoenix memory's copy of the model-write rule in step. Memory, in Standards, structure, settings and memory, owns it.
- What a take-out may remove. Take a part out on a person's named approval (fn-take-part-out) does it.

## Sources
- docs/adr/065-the-models-index-is-changed-through-two-skills-the-model-never-names-a-plan-and-only-tools-know-the-tracker.md, line 9: the Affects line names `core/components/memory/standards/rules/direct-model-write.md`; line 48: "Neither skill writes the profile block in the spine or an epic's status. "Over time" has no date and no list."; line 131: "`link-model-part` adds or changes a part. `remove-model-part` takes a part out, with the name of the person who approved it. Each changes only what its request names, and the links that would otherwise point at nothing, stays inside the model, and lists every file it changed. Plays move onto these two skills over time, in place of writing the index with their own scripts.", "what the two skills can't do yet stays with its play until they can."
- core/components/skills/link-model-part/SKILL.md, line 3: "the spine keeps its comments and layout"
- core/components/agents/product-os-keeper.md, lines 102-109: the routes through link-model-part and remove-model-part, /update-plan's among them
- standards/rules/direct-model-write.md, in Phoenix memory, lines 51-52: "Outside a loop, the play's keyed script is still the only writer of shared files."
- core/components/plays/learn-outcomes, shape-measure-lens, build-epic, validate-epic and release-epic: each SKILL.md reads "stale: true"
- The stock-take (2026-11-11), sections 2.1 and 2.10
