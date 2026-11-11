## Intent
- Goal: Each Garura part runs on the tier of model its source names, in whichever coding tool the team works in: the install folds each part's `model:` hint once into deep, standard or fast, and each tool's adapter writes that tier where the tool takes a model for that kind of part, so one source serves every tool.
- Limit: The tier a part's source names is carried as it is; the install never chooses, raises or lowers it.
- Limit: The engine's shared fold names no tool's model; each tool's model names live only in that tool's adapter.
- Limit: A missing or unknown value is read as standard, never left without a tier.
- Fails if: A sub-agent laid for a tool that takes a model on it runs without the tier its source names.
- Fails if: A part's laid tier differs from the tier its source names, or the engine's steps name a tool's model.
- Fails if: A tier a tool cannot take is lost and nothing tells the team.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: each part's `model:` hint in its source; the shared fold; each adapter's mapping; and, as approved in memory, where each tool takes a model for a sub-agent, a skill and a command.
- Never read: any memory file by its path, and any ICE page.
- Persona: the product owner, who wants each part to run on the tier its maker chose, whichever tool the team works in.
- Scope: In: folding each part's tier and carrying it into each tool's own setting. Out: which tier and effort each part runs on (Intelligent model routing), laying the parts themselves, and a model used beside the installed tool.

## Expectation
- Scenario: A bank's payments team installs Garura for Claude Code. The sub-agent that reviews a change names `opus` in its source, one that reads the tracker names `sonnet`, and a skill names `haiku`. After the install, the two sub-agents' files name `opus` and `sonnet`, and the skill's tier either reaches Claude Code in a form it takes, or the team is told it did not.
- Done means: Someone other than the one who ran the install compares each part's tier in its source with what was laid and with the report, and finds every tier either carried into the tool in a form it takes or told to the team as not carried, none changed, and no tool's model named in the engine's steps.
