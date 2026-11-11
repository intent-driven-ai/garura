## Intent
- Goal: A change to a play that touches what it decides or guarantees is made in its ICE first, then carried only as far as it reaches, through the pre-flight checks, the workflow, the evals, the sub-agents and skills and the scripts, with every orphan removed; the play is compiled again with a fingerprint computed from the changed ICE, the play linter passes, and the person sees what changed, so the play and its intent never drift apart.
- Limit: Only wording with no change in meaning is edited directly in the compiled play, and its reason goes in the commit and the issue.
- Limit: What the change does not reach stays as it was.
- Limit: A play whose job is gone is not changed; a new one is built.
- Fails if: The compiled play says something its ICE does not, or its fingerprint was not computed from the changed ICE.
- Fails if: An eval or a recovery points to a constraint, failure condition or scenario that is gone, or something added has no eval.
- Fails if: A step, eval or script the change does not reach was changed.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the play's compiled file and its ICE source, which eval covers which constraint, failure condition and scenario, the person's change, the agent audit, the workflow shapes, the compiled-play example, the play's scripts, and the map of what runs next.
- Never read: any memory file by its path, and any ICE page.
- Persona: the technical lead or the developer, who changes a play of the team's harness; and the product owner, who approves the change to its intent.
- Scope: In: sorting the change into an intent change or a wording edit, mapping the play, naming the reach, changing the ICE, carrying the change through, removing orphans, compiling again, the fingerprint, the play linter and the summary. Out: building a new play, the play checker's rules, refusing an edit made without the play, the way past a checkpoint, and landing the change.

## Expectation
- Scenario: In an insurer's harness repository, the technical lead adds a failure condition to the claims play. /edit-play maps the play, names the reach, adds the failure condition to the ICE, adds its step eval and one recovery, computes the fingerprint again, and the play linter passes; the summary shows the new failure condition, its eval and its recovery. In a news site's harness, a developer fixes a typo in a play's brief as a direct edit, and the reason is in the commit.
- Done means: Someone other than the one who changed it compares the insurer's play and ICE before and after, and finds the new failure condition in the ICE with one eval and one recovery, no eval or recovery pointing to anything that is gone, every other step unchanged, the fingerprint equal to the hash of the new intent and expectation, and a passing play linter; and, for the news site, only the typo changed and the reason in the commit.
