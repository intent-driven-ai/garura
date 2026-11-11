# Feature: Build a harness in a team's own repository, against a written architecture

## What it does
A team installs Garura's builders in its own repository and builds its own harness there, reading a written architecture of what each part may do, so any team can build its own harness on Garura's foundation without Garura's source.
- Who builds: in the product owner's second answer, the one who builds is any team, in its own repository, "which needs a new ADR changing ADR 055 section 5". The intent's outcome says: "Teams can build their own harness on it."
- What is built: the install's harness kind. It lays the four builders, the plays that land each change, the plan plays and a few more, with the sub-agents and skills they call, and "nothing product-facing". It lays no loop: "a harness repo builds loops but runs none".
- A product project gets no builder: "A product project's ADLC has no use for them, so no target ever receives them under `full`."
- Where it stops today: the builders work on Garura's source layout. /create-loop "writes the compiled loop into core/components/loops/<loop>/", and /create-play reads its rules by source paths. So a team builds its own plays and loops only in a repository laid out like Garura's source.
- Why: this is by design today. ADR 055 section 5 names the builders among the parts that "work on the source by design", and the harness standard calls them "the exception, by design". Running them on the installed layout needs a new ADR that changes ADR 055 section 5. That ADR is not recorded, and nothing of it is built.
- A first step exists: the loop linter finds the stamped scripts' sources in either layout, "the source tree, or the installed builders".
- The written architecture is planned: #933 (an architecture memory for a team building a harness) is to add pages in Phoenix memory on "the parts and what each may do", what calls what, memory, what a run leaves behind, "the folders: the source, the installed copy, short-term memory", and the decided patterns, each with its decision record. A team reads them "without taking the whole of Garura, and a review tests a change against it". It sits under #967 (a team builds a harness from a written architecture).
- The harness standard is already "written so that a team can take it and build its own harness the same way".
- Not there: a starter for a new harness repository, and a guide to building one; the usage folder holds a README and one play page.
- Examples, in different kinds of project:
  - In a retailer's own repository, the team installs Garura and builds a play that checks refunds, beside Garura's plays, with /create-play and no Garura source folders.
  - In an insurer's repository, the technical lead builds a claims loop and reads the architecture pages to check that its sub-agent reads memory only through the memory tool.
  - In a design agency's repository, the team uses Garura's plays and builds none, so it installs the full kind and no builder is laid.
- How it meets the capability: the one the capability's line speaks to is any team, in its own repository, and this feature lets that team build there.

Status: built in part (the install's harness kind), planned in part (#933, the architecture memory, under #967). Not built, or open:
- The builders do not run on the installed layout, and the new ADR that changes ADR 055 section 5 is not recorded.
- The architecture pages of #933 are not written.
- No starter for a new harness repository, and no guide.
- A product project that wants to build its own plays has no way past but to install the harness kind, which drops the product plays and records nothing.
- Whether a team outside Garura has built its own harness with the builders: not confirmed.

## Inputs / Outputs
- In: the team's repository, and the kind of install it chose.
- In: the builders and their references, as the install lays them.
- In: the architecture pages, once written, read through the memory tool.
- Out: the team's own plays and loops, built and checked by the same builders and linters as Garura's own.
- Out: in a harness repository, the builders and the change plays laid, and no product loop.

## Rules & behavior
- Any team, in its own repository, builds its own harness. The reason, in the product owner's words: "is any team in its own repository, which needs a new ADR changing ADR 055 section 5"
- A harness repository carries only what builds a harness. The reason: the harness kind is for repositories "that must carry only the meta plays, the change chain, and the workers those plays dispatch — nothing product-facing."
- A harness repository runs no loop. The reason: "a harness repo builds loops but runs none"
- A product project gets no builder today. The reason: "A product project's ADLC has no use for them, so no target ever receives them under `full`."
- A part that reaches into the source fails outside Garura. The reason: "A part that reaches into the source works only inside Garura's own repository, and fails everywhere else."
- The architecture is read through the memory tool and cited. The reason: #933 is done when "a review agent can find them through the memory tool and cite them."
- Not decided: what the new ADR changes in ADR 055 section 5: whether the builders work on the installed layout only, or on both layouts.
- Not decided: whether a product project may get the builders beside its product plays.
- Not decided: whether a starter for a new harness repository, or a guide to building one, is part of this feature.

## Acceptance criteria
- Given a repository that installs the harness kind, when the install ends, then the four builders, the change plays and the parts they call are laid, and no loop is.
- Given a repository that installs the full kind, when the install ends, then no builder is laid.
- Given a team's repository with Garura installed and no Garura source folders, when the technical lead builds a play and a loop there, then both are built where the installed layout keeps them, and both linters pass. This is not built.
- Given the architecture pages in Phoenix memory, when a review checks a change in a team's harness, then the review finds the pages through the memory tool and cites the pattern the change breaks. This is not built.

## Out of scope
- Choosing the kind of install, laying it and taking it out. Install into a project, in Install and distribute, owns it.
- Where each part lives, in the source and once installed. Structure, in Standards, structure, settings and memory, owns it.
- The severity a review gives each finding against the architecture (#934, one severity for findings and defects, P1 to P4). Standards, in Standards, structure, settings and memory, owns it.
- Moving the architecture pages up into Phoenix memory. Memory, in Standards, structure, settings and memory, owns it.
- Recording the new ADR that changes ADR 055 section 5. Manage ADRs, in Orchestration, owns the record.
- Building and changing each play and loop. Build a play from its ICE (fn-build-play) and Build a loop from its ICE (fn-build-loop) do it.

## Sources
- .garura/project/issues/1021/context/capabilities.md, lines 117-118, the product owner on 2026-11-11: "You can keep building your harness with your own plays, loops, sub-agents and skills, in a consistent way.", "is any team in its own repository, which needs a new ADR changing ADR 055 section 5"
- .garura/product/product-os/intents/bi-10.md, line 3: "Teams can build their own harness on it."
- core/components/plays/install-garura/scripts/install.py, lines 203-215 and 265: "that must carry only the meta plays, the change chain, and the workers those plays dispatch — nothing product-facing.", "A product project's ADLC has no use for them, so no target ever receives them under `full`.", "a harness repo builds loops but runs none"
- core/components/plays/create-loop/SKILL.md, lines 7-8: "writes the compiled loop into core/components/loops/<loop>/"
- core/components/plays/create-play/SKILL.md, lines 275 and 388: the rules read by source paths, "../../memory/standards/rules/pipeline-position.md" and "core/components/memory/standards/rules/pipeline-next.md"
- docs/adr/055-installed-parts-read-only-installed-files.md, section 5, line 57: "These parts work on the source by design, and the rule does not apply to them"
- docs/standards/harness-standard.md, lines 4-5, 129 and 137-138: "written so that a team can take it and build its own harness the same way", "the exception, by design", "A part that reaches into the source works only inside Garura's own repository, and fails everywhere else."
- core/components/plays/create-loop/scripts/lint_loop.py, line 193: "Where the stamped scripts' sources live: the source tree, or the installed builders."
- GitHub #933 (open): "the parts and what each may do", "the folders: the source, the installed copy, short-term memory", "without taking the whole of Garura, and a review tests a change against it", "a review agent can find them through the memory tool and cite them."
- GitHub #967 (open): "A team building a harness has an architecture memory to build and review against, and every finding carries one severity."
- docs/usage/: a README and one play page, create-pr.md.
- The stock-take of this intent, .garura/project/issues/1021/context/bi-10-inventory/inventory.md, sections 2.2, 2.4, 2.5, 9 and 10 (item 3): "Whether a team outside Garura has done so: not confirmed."
