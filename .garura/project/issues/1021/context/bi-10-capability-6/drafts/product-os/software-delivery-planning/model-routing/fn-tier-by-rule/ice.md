## Intent
- Goal: Every Garura part names in its source the model tier, and the effort, that its job needs, chosen by one written rule for its kind, so it runs on the right model and effort for its job; a project may change a part's tier in its own settings, and the part then runs on the project's tier; and a skill's own tier takes effect in Claude Code, tried first on one skill and checked.
- Limit: A part names a tier, `best`, `opus`, `sonnet` or `haiku`, never a coding tool's model id.
- Limit: The maker's tier in the source is the default; a project's change lives in its own settings and never edits the part's source.
- Limit: A skill's tier is laid for Claude Code on one skill first, and on the others only after that one is checked.
- Limit: Carrying the tier into each coding tool stays with Install and distribute; this feature decides the tier and never lays it.
- Fails if: A part names no tier, or a tier the written rule for its kind does not give, and says no reason.
- Fails if: A part runs on a tier other than the one its project's settings or, where they name none, its source names.
- Fails if: A skill's tier is laid for every skill before the one skill tried first was checked.
- Fails if: A part's source names a coding tool's model id in place of a tier.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: each part's `model:` and `effort:` lines in its source; the written rule for tiers in the skills doc and the list of sub-agents' models in the agents doc; the reasons some parts give for their tier; the project's settings; the install's fold of tiers and what Claude Code keeps; where each coding tool takes a model and an effort, as approved in memory; and Phoenix memory's page on choosing a model for each step.
- Never read: any memory file by its path, and any ICE page.
- Persona: the developer or the technical lead who builds a part and names its tier and effort; and a team that changes a part's tier for its own project.
- Scope: In: the written rule for each kind of part's tier and effort, each part's default in its source, a project's own tier in its settings, and trying a skill's tier in Claude Code on one skill first. Out: carrying the tier into each coding tool, the rest of each kind's written standard and its linter, keeping the settings file, and moving a part on the record of its runs.

## Expectation
- Scenario: In a bank's payments service, a developer writes a new skill that only commits files and names `haiku` by the rule, and a new sub-agent that reviews each change with `opus` and `effort: high`. The skill is the one tried first: laid for Claude Code, it runs on the fast tier, and that check reads pass before any other skill's tier is laid. In a clinic's booking app, the team sets its drafting skill to `sonnet` in the project's settings; the skill runs on `sonnet`, and its source still names `opus`.
- Done means: Someone other than the one who built the parts reads each part's source, the written rule, the project's settings and the record of the one-skill check, and finds every part naming the tier and effort its rule gives, or its reason; no coding tool's model id in any source; the bank's skill checked on the fast tier before any other skill's tier was laid; and the clinic's skill running on `sonnet` with its source unchanged.
