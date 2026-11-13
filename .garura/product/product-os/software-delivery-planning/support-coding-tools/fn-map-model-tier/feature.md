# Feature: Map each part's model tier onto each tool's own setting

## What it does
Each Garura part names in its source the tier of model it needs, and the install carries that tier into the coding tool's own setting for that kind of part, so the part runs on the tier its maker chose in whichever tool the team works in. It is the one piece that every tool's adapter, the part of the install that lays Garura in one tool's shape, shares.
- What a part names: a `model:` hint in the front of its file. In the install play's words, "That value is a *tier* signal, not a literal host model id."
- One fold, shared by every adapter: `best`, `deep` and `opus` become deep; `sonnet` becomes standard; `haiku` becomes fast; a missing or unknown value becomes standard. In the shared helpers' words, "This is the seam that lets one source serve both Claude and Codex."
- Each adapter then maps the tier onto its own tool:
  - Claude Code keeps it on each sub-agent, written as `opus`, `sonnet` or `haiku`, and drops it on each skill, play and loop, because "A Claude skill has no model field".
  - The stopped Codex adapter writes it as a note in each skill, "Recommended Codex profile", and writes three profiles with a model and an effort, because "the per-skill tier can't be *pinned*".
  - GitHub Copilot, Antigravity and Factory have no adapter yet. Where each tool takes a model, as approved in memory: Claude Code "for a sub-agent and for a skill"; Codex "for a custom agent", while "skills inherit from the parent"; GitHub Copilot on a custom agent in its IDEs and on a prompt file, as "in VS Code a prompt file names its model", while "A model field for a skill is not stated"; Antigravity on a custom sub-agent, as a tier, "inherit, flash or pro", while for a skill "No model field is listed"; and Factory "for a custom droid, not for a skill".
- What the parts carry today: 17 sub-agents name a tier (12 `sonnet`, 4 `opus`, 1 `haiku`); 75 skills, plays and loops name one (39 `sonnet`, 23 `opus`, 8 `best`, 4 `haiku`, and one with no value). The Claude Code adapter keeps the 17 and drops the 75.
- The line with Intelligent model routing: which tier and effort each part should run on, and when that changes, is routing's: "Each part runs on the right model and effort for its job, for speed and token cost, on each harness that supports it." This feature carries only the tier the part already names, and never chooses one.
- Examples, in different kinds of project:
  - In a bank's payments service on Claude Code, the sub-agent that reviews a change names `opus`, and its laid file names `opus`.
  - In a shop's checkout project, a skill that names `haiku` is laid for Claude Code without it today, so it runs on the session's model.
  - In a news site's team on Codex, after the redesign, each part's tier would reach Codex in the form Codex can hold.
- How it meets the capability: "Each tool gets what it supports." covers the model as well as the files: a part laid without its tier runs on the model of whoever calls it, as the Claude Code adapter says of a skill, "the agent that invokes the skill carries the model".

Status: built in part.
- Built: the fold (core/components/plays/install-garura/scripts/adapters/common.py lines 29-49), and the Claude Code adapter's tier on each sub-agent.
- Gap: the tier on each skill, play and loop is dropped for Claude Code.
- Stopped: the Codex mapping, with the rest of the Codex adapter.
- Not built: the mapping for GitHub Copilot, Antigravity and Factory.
- Effort is not carried: the fold reads only the tier, and only the Codex profiles name an effort.

## Inputs / Outputs
- In: each part's `model:` hint, as its source names it.
- In: the coding tool the team works in, and what that tool takes as a model for each kind of part, as approved in memory.
- Out: each part laid with its tier in the tool's own setting, where the tool takes one.
- Out: for the report, each part whose tier the tool could not take.

## Rules & behavior
- A part names a tier, never a tool's model id. The reason: "That value is a *tier* signal, not a literal host model id.", so one source serves every tool, and a new tool maps the same three tiers.
- The fold is shared and the mapping is the adapter's. The reason: the install play says that when you find yourself "special-casing a host's model names or file layout in the orchestrator, stop — that belongs in the adapter."
- An unknown or missing value is read as standard. The reason: the fold must give every part a tier, and standard is its default.
- The tier is carried, never chosen. The reason: "which model each part runs on belongs to Intelligent model routing".
- A sub-agent keeps its tier. The reason: an older copier "stripped every `model:` line, so deployed agents lost their tier".
- Not decided: what the install does with a tier a tool cannot take for a kind of part: leave it out and say so, write it in another form, or refuse to lay that part.

## Acceptance criteria
- Given a sub-agent whose source names `best`, when it is laid for Claude Code, then its file names `opus`.
- Given a part whose source names no model, or a value the fold does not know, when it is folded, then its tier is standard.
- Given a part whose source tier is changed by Intelligent model routing, when Garura is installed again, then the new tier is laid.
- Given a skill, play or loop whose source names a tier, when it is laid for a tool, then the tier reaches the tool in a form the tool takes, or the team is told it did not. This is not built: for Claude Code the line is dropped and nothing tells the team.

## Out of scope
- Which tier and effort each part runs on, and changing it. Intelligent model routing, in Standards, structure, settings and memory, owns it.
- Laying the parts themselves in each tool's shape. Each tool's own feature does it.
- A model used beside the installed tool, such as the model that checks a loop or writes tests. It is a setting of those plays, not an install.

## Sources
- core/components/plays/install-garura/SKILL.md: "That value is a *tier* signal, not a literal host model id.", "special-casing a host's model names or file layout in the orchestrator, stop — that belongs in the adapter."
- core/components/plays/install-garura/scripts/adapters/common.py: "This is the seam that lets one source serve both Claude and Codex.", the fold at lines 29-49
- core/components/plays/install-garura/scripts/adapters/claude.py: "A Claude skill has no model field", "the agent that invokes the skill carries the model", "stripped every `model:` line, so deployed agents lost their tier"
- core/components/plays/install-garura/scripts/adapters/codex.py: "Recommended Codex profile", "the per-skill tier can't be *pinned*"
- The list the product owner set on 2026-11-10: "Intelligent model routing: Each part runs on the right model and effort for its job, for speed and token cost, on each harness that supports it."
- .garura/product/product-os/intents/bi-7.md: "Each tool gets what it supports."
- .garura/product/product-os/software-delivery-planning/build-work-test-first/fn-write-failing-tests/feature.md: "which model each part runs on belongs to Intelligent model routing"
- The count of parts that name a tier: `grep "^model:"` over core/components on 2026-11-10.
- The research note "What Claude Code loads from a project" (read 2026-11-10), approved by the product owner on 2026-11-10 as mu-20261110-001: "for a sub-agent and for a skill"
- The research note "What Codex loads from a project" (read 2026-11-10), approved by the product owner on 2026-11-10 as mu-20261110-002: "for a custom agent", "skills inherit from the parent"
- The research note "What GitHub Copilot loads from a project" (read 2026-11-10), approved by the product owner on 2026-11-10 as mu-20261110-003: "the how-to names the model property for VS Code, JetBrains IDEs, Eclipse and Xcode", "A model field for a skill is not stated", "in VS Code a prompt file names its model"
- The research note "What Antigravity loads from a project" (read 2026-11-10), approved by the product owner on 2026-11-10 as mu-20261110-004: "No model field is listed", "inherit, flash or pro"
- The research note "What Factory loads from a project" (read 2026-11-10), approved by the product owner on 2026-11-10 as mu-20261110-005: "for a custom droid, not for a skill"
