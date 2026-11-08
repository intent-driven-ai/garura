Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: When a deployment needs an environment that is not built yet, that environment is built on its own from the one design of the underlying technology and its declaration, after a person's yes, counts as built only when a separate check shows it answers, and is then kept apart from the others, changed only by a confirmed update and taken down only when a person asks, each step recorded.
- Limit: An environment is built only when a deployment to it is needed, only from what its declaration and the design hold, one at a time, and a change to one never changes another; a missing part is named as a gap, never guessed.
- Limit: Production is never built, changed or deployed to, and no environment's data comes from production.
- Limit: Only a person says yes to a build or asks for a take-down; a failed build leaves things as they were and is not tried again on its own, and no record or log holds the value of a secret.
- Fails if: An environment is built with no person's yes, before a deployment needs it, or from something its declaration and the design do not hold, with no gap named.
- Fails if: Anything here builds, changes or deploys to production, or fills an environment with data taken from production.
- Fails if: An environment is counted as built while it does not answer, a failed build leaves a half-built environment, or a build or change of one environment changes another.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the environment's declaration; the one design of the underlying technology in the deployment design, with where secrets and settings are kept; the files that carry out the design, such as infrastructure files and container files; the records of earlier builds, changes and take-downs; and the deployment that needs the environment.
- Never read: the value of any secret, such as a password or a key, and anything in production, such as its data.
- Persona: the devops engineer, who says yes before an environment is built and decides when one is taken down.
- Scope: In: building each environment on its own when a deployment needs it, checking that it answers, keeping it apart, applying a confirmed update to it, taking it down when a person asks, and recording each step. Out: declaring and updating the environments, designing the underlying technology, the path and the tests, deploying each change, making the infrastructure and container files, running the tests, and production.

## Expectation
- Scenario: A team's planning tool has dev built and running. A change passes its checks in dev and must move on to testing, which is declared and not built. The devops engineer sees testing's declaration and what will be built, and says yes. Testing is built from the same design as dev, with its own made-up data and its own size, and a separate check shows it answers; nothing in dev changes. Pre-production stays declared and not built, because no release has moved there yet. A request to deploy to production is refused.
- Done means: Someone other than the one who built the environments reads the records and finds, for each build, change and take-down, the environment, the declaration and design it came from, the check that shows it answers, the person who said yes and no secret's value, and finds no environment built before a deployment needed it and none that is production.
