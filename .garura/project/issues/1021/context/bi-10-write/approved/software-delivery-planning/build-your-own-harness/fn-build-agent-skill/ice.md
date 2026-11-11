## Intent
- Goal: A team builds each new sub-agent and skill its plays need to the written standard for its kind, a sub-agent to gather context and check and a skill to do the work, and a check holds each one to that standard before a play uses it, so the parts a team adds work as Garura's own do, with no ICE of their own.
- Limit: A skill or a sub-agent carries no ICE; the intent stays in the play that runs it.
- Limit: A sub-agent passes the eleven principles before a play uses it.
- Limit: A missing skill is named and built, never worked around inside a sub-agent.
- Fails if: A new sub-agent or skill is used by a play without being checked against its standard.
- Fails if: A sub-agent does the work a skill is for, or a skill gathers context on its own.
- Fails if: The check passes a part that misses a section its standard asks for.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the play that needs the part, the written standards for sub-agents and skills, the agent audit, the sub-agents and skills that exist, the component linter's rules, and the product owner's answer on what carries an ICE.
- Never read: any memory file by its path, and any ICE page.
- Persona: the developer or the technical lead, who adds a sub-agent or a skill that a team's play needs.
- Scope: In: building a sub-agent or a skill to its standard, and checking it. Out: writing the standards and the component linter, the model each part runs on, where each part lives, and building the play that runs them.

## Expectation
- Scenario: In a bank's harness repository, a play needs a skill that drafts a payment risk note; the developer builds it to the skill standard, and the check passes it before the play runs it. In a game studio's harness repository, a skill written by hand without the standard's sections fails the check, which names each missing section.
- Done means: Someone other than the one who built them reads the bank's new skill against the skill standard and finds every section it asks for and a passing check on record before the play first ran it; and, for the studio, finds the check failed with each missing section named.
