Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: Each of the three clouds, AWS, GCP and Azure, has a dedicated cartridge that the design reads, holding that cloud's services a physical architecture maps onto, its container platforms and how to work out what running on it costs, each entry with its source, in the same shape for all three.
- Limit: Each entry is drawn from the project's own records first, then from Garura memory, then from Phoenix memory; only when none of them answers is it researched, and the research is used only after a person approves it as a memory update. Nothing comes from what the AI agent knows by itself.
- Limit: A cartridge holds what one cloud offers, never a project's choice, and never the value of a secret.
- Limit: Only a person confirms a cartridge, and no work waits for one.
- Fails if: A cartridge entry has nothing behind it but what the AI agent knows by itself.
- Fails if: The three cartridges answer in different shapes, so the costs drawn from them cannot be set side by side.
- Fails if: Work stops because a cartridge, or an entry in one, is missing.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the project's own records for each cloud, such as infrastructure files that already use its services; Phoenix memory's learnings for running on each cloud; the shape memory already gives a cloud environment, with its region, the service that runs each part, its managed services with what drives their cost, and its store for secrets; and approved memory updates from earlier research on a cloud.
- Never read: the value of any secret, such as a cloud account's key.
- Persona: the devops engineer, who confirms each cloud's cartridge.
- Scope: In: preparing and confirming one cartridge for each of AWS, GCP and Azure, with its services, its container platforms and how to work out what running on it costs. Out: choosing the cloud and mapping the project onto it, updating a cartridge, setting up environments, deploying, deciding where a cartridge lives, and moving a memory update into Phoenix memory.

## Expectation
- Scenario: The three cartridges are prepared. The GCP one draws on Phoenix memory's learning for running there; the AWS and Azure ones draw on research a person approved as memory updates. A project with one deployable unit and one database is mapped onto each, finding a service that runs containers and a managed database on every cloud, and its cost comes out for one team, a wider trial and the whole company in the same form on all three.
- Done means: Someone other than the one who prepared the cartridges maps one physical architecture onto each, finds every entry it uses backed by a source and a person's confirmation, and sets the three costs side by side.
