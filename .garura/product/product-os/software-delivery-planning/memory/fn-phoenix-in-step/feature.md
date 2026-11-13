# Feature: Keep Phoenix memory in step with Garura's source, versioned per release with its notes

## What it does
When a change to Garura changes a memory page in its source, Phoenix memory gets the same change in the same release, a check names every page where the two differ, and each release of Phoenix memory has a version and its own notes, so every project's agents decide from the rules Garura now follows.
- Phoenix memory is seeded from the memory folder of Garura's source, and every project's agents read it through the memory tool. A project holds no standards of its own, so what Phoenix memory says is what its agents decide from.
- Today the two differ in 60 places, in a file-by-file compare through the memory tool on 2026-11-11: 42 pages differ, 3 are in the source only, and 15 are in Phoenix memory only. A compare on 2026-10-28 gave the same count. Among them are the naming rules, so an installed project checks names against other rules than Garura's source.
- Today a change reaches Phoenix memory by hand: promotion today is a manual copy, commit and push into another repository, outside the change plays, with no record of which Garura change needed it.
- What this feature is to do, in full:
  - a change to Garura that changes a memory page also changes Phoenix memory, through the change plays, and the change is not done until both land;
  - a check names every page where Phoenix memory and Garura's source disagree, and a release does not go out with a gap nobody decided on;
  - Phoenix memory has a version per release, which matches the Garura release it goes with, and release notes for each: what pages were added, changed or removed, and why;
  - the direction of each page, from the source to Phoenix memory or Phoenix memory's own, is decided and written down.
- Before anything is promoted or deleted, each page is first checked for which side is newer, and why a page is on one side only.
- Also needed: a check that each standard the installed parts name is answered by the memory tool at the same content as Garura's source.
- Examples, in different kinds of project:
  - In a harness team's own repository, a change renames a loop in the naming rule. The same release changes Phoenix memory's naming rule, and the release notes name the page and why.
  - In a bank's payments service, the team installs the new release of Garura. Its agents read the review rules that match that release, not an older copy.
  - In a research team's data pipeline, a knowledge page exists only in Phoenix memory on purpose. Its direction is written down as Phoenix memory's own, and the check does not report it as a gap.
- How it meets the capability: agents "decide from three tiers of memory", and Phoenix memory is the tier every project shares, so a page left behind there reaches every project's later decisions.

Status: not built.

## Inputs / Outputs
- In: a change to Garura that changes a page in the memory folder of its source.
- In: Phoenix memory at its approved version, read through the memory tool.
- In: the direction of each page, once it is written down.
- Out: the same change in Phoenix memory, landed in the same release.
- Out: the check's list of every page where the two differ, each with its direction and whether a person decided on it.
- Out: Phoenix memory's version for the release, and its release notes.

## Rules & behavior
- A change that changes a memory page is not done until Phoenix memory has it too. The reason: "A change to Garura that changes a memory page also changes Phoenix memory, through the change plays, and the change is not done until both land."
- No release goes out with a gap nobody decided on. The reason: "a release does not go out with a gap nobody decided on."
- Each page's direction is written down. The reason: "The direction of each page (source to Phoenix, or Phoenix's own) is decided and written down, so a Phoenix-only page is not overwritten by mistake."
- A page on one side only is not deleted before its reason is known. The reason: "Do not delete a Phoenix-only page before knowing why it is there."
- Phoenix memory has a version per release, with its own notes. The reason, in the product owner's words: "the phoenix memory is kept up to date and memory needs versioning too, which goes per release and is its own release notes".
- Phoenix memory holds no names of a client, an organisation or a person. The reason: "No client, organisation or personal references."
- Not decided: how a page goes from Garura's source to the Phoenix memory repository without hand copying, through the change plays or through the Phoenix install.

## Acceptance criteria
- Given a change that edits a rule in the memory folder of Garura's source, when the change lands, then Phoenix memory holds the same rule in the same release. This is not built.
- Given a page that differs between the two with no decision on it, when a release is cut, then the check names the page and the release does not go out. This is not built.
- Given a page that is Phoenix memory's own, when the check runs, then it is reported with its direction and not as a gap. This is not built.
- Given a release, when Phoenix memory is versioned, then its version matches the Garura release and its notes name each page added, changed or removed, and why. This is not built.

## Out of scope
- Garura's own release, its version and its notes. Upgrade a project, in Install and distribute, owns them.
- Bringing a new version of Phoenix memory to a machine. Bring Phoenix memory to a machine and keep it current (fn-bring-phoenix) does it.
- Moving a project's answer or approved update up to Phoenix memory. Move a page up a tier on a person's yes, and choose what is learned (fn-promote-page) does it.
- What each rule, template and schema says. Standards, in Standards, structure, settings and memory, owns it.
- Opening, reviewing and landing the change. Ship every change the same way, in Developer tooling, owns it.

## Sources
- The capability list set on 2026-11-11: "Memory: Agents decide from three tiers of memory (Phoenix global, Garura project, short-term), and people control what enters them."
- The product owner on 2026-10-28: "the phoenix memory is kept up to date and memory needs versioning too, which goes per release and is its own release notes"
- README.md, in Phoenix memory, line 9, read through the memory tool: "No client, organisation or personal references."
- .garura/product/product-os/software-delivery-planning/upgrade-project/fn-cut-release/feature.md, line 52: "Phoenix memory's own versions and notes. Memory, in Standards, structure, settings and memory, owns them."
- .garura/product/product-os/software-delivery-planning/initialize/fn-883/feature.md, line 59: "How Garura's source memory reaches the Phoenix memory repository without hand copying"
- The stock-take (2026-11-11), sections 1.5, 5.5 and lean 11: the compare of 2026-11-11, and the naming rules among the 60 places.
