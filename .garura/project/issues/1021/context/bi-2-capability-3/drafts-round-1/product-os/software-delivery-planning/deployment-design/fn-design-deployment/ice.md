Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: How the product is deployed is set once for the whole project, with where it runs and in what form, the path a change takes to the people who use it, how a release goes live, is checked and is rolled back, how stored data survives it, where secrets are kept and what running it costs, each part with its reason, its source and the person who confirmed it.
- Limit: Each part is proposed from the project's own memory and code first, then from Garura memory, then from Phoenix memory; only when none of them answers is it researched, and the research is used only after a person approves it as a memory update. Nothing comes from what the AI agent knows by itself.
- Limit: Every part of the architecture gets a place to run, every release gets a way back that keeps stored data, and the design never holds the value of a secret.
- Limit: Only a person confirms a part, and no work waits for one.
- Fails if: A part of the design is set with no person's confirmation, or with nothing behind it but what the AI agent knows by itself.
- Fails if: An agent that prepares a release cannot find in the design where a part runs or how the release is taken back, and decides it alone with no gap named.
- Fails if: Work stops because a part of the design is missing.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the project's code and its settings, such as its container files, its pipeline files, its deploy scripts, its infrastructure files and its hosting settings; the architecture set so far, with its parts and their technology, and the declared surfaces; the quality levels and the compliance needs in the product profile; Phoenix memory's architecture and technology learnings for deploying, releasing and running a product, with the conditions each fits; and the project's set-up answers, when it has them.
- Never read: the value of any secret, such as a password or a key.
- Persona: the devops engineer, who confirms how the product is deployed, released and rolled back.
- Scope: In: proposing and setting the project's deployment design: the platform, where each part runs and in what form, the path, the release and how it is checked, the rollback, stored data, secrets and settings, the cost and the rules every release keeps. Out: updating the design, which environments exist and how each is set up, the architecture and its technology, the surfaces, each slice's run design, building, testing, delivering and deploying the work, the files that carry out the design, the product profile, and moving a memory update into Phoenix memory.

## Expectation
- Scenario: A team's planning tool, one deployable unit with a browser page, is proposed a design from its container file and a Phoenix memory learning for its architecture and stage: it runs as a container on a managed service, a release goes to one team first and then to everyone, the team knows it is up when the page answers, a rollback turns the new behaviour off without losing stored data, secrets live only in the platform's secrets store, and the cost is shown for one team, a wider trial and the whole company. The devops engineer confirms it.
- Done means: An agent that did not make the design prepares a release from the design alone, naming where each part runs, the path, the checks, the way back and where the secrets are kept, and a person other than the one who made the design finds a source and a confirmation behind each part.
