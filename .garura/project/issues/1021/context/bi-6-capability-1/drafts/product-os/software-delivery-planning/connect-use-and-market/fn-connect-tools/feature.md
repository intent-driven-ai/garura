# Feature: Choose the tools and forums a project reads, and connect to them

## What it does
When the product owner wants the project to learn from how its product is used and what is said about it, this feature proposes the connections the project should have, records each one the product owner says yes to, and proves each with a first read, so the reads that follow start from tools and places a person chose.
- A connection is one outside tool or forum the project reads: a web analytics tool, a product analytics tool, a user feedback tool or a forum, in the product owner's words "tools that access web analytics, product analytics, user feedback, and forums like Reddit".
- Each connection is proposed from memory first: the project's own code and memory, such as an analytics tool the product's code already loads or a feedback form it already sends somewhere, then Garura memory, then Phoenix memory. A forum, or a topic in it, comes from the product owner's word or the project's memory. Each proposal names its source, and the product owner keeps, changes or drops it.
- For each connection the product owner says yes to, the project's settings record:
  - its name and what it is read for: how the product is used, or what people say about it and its market;
  - what part of it is read, such as one product in an analytics tool, or one forum and its topics;
  - where its access key is kept, never the key itself.
- A first read proves each connection. It changes nothing in the tool. A connection that the first read cannot reach is named, with the reason, and is not used until it reads.
- Plays, skills and sub-agents never name a tool or forum. They call one tool, which reads the settings and knows how to reach each connection.
- What it proposes, for example, in different kinds of product: for a shop's checkout, the product analytics tool its pages already load; for a clinic's booking app, the feedback tool its app sends messages to; for a team's planning tool, a forum where teams compare planning tools, from the product owner's word.
- How it meets the capability: every read of use and of what people say runs only on a connection chosen here, so the capability takes in only what a person agreed it may read.

Status: not built. What exists covers only patterns for it:
- The tracker is reached this way today. The settings name it, "Tools read this; plays, skills and sub-agents never name a tracker.", and the code host's own command line holds the access, so the settings hold no key. Nothing names an analytics tool, a feedback tool or a forum.
- Initialize, the project set-up step planned after the install, asks a short set of questions about the project and runs again when the project changes. It is not built, and it asks nothing about connections.
- No memory tier says which tools and forums a project can connect to, or how each is reached.

## Inputs / Outputs
- In: the product owner's wish to learn from use and the market, and each choice and yes.
- In: the project's code and settings, which may already name an analytics or feedback tool.
- In: the product's declared surfaces, from Manage surfaces.
- In: where the project keeps its secrets, from the deployment design, and the product profile's privacy level and compliance needs.
- In: memory's answers, through the memory tool.
- Out: each approved connection in the project's settings: its name, what it is read for, what part of it is read, and where its key is kept.
- Out: the record of each first read: which connection, when, and whether it read, with the reason when it did not; for Take in how the product is used, from its web analytics and product analytics (fn-take-in-use) and Take in what people say about the product and its market, from feedback tools and forums (fn-take-in-what-people-say).

## Rules & behavior
- The product owner says yes to each connection. The reason: a connection opens a team's account or a public place to the project and may bring in people's words, and a tool is an outside system, where any write "is visible to the whole team."
- Names only for keys. The settings say where each key is kept, never its value. The reason: the deployment design "names only where each secret is kept", and every agent reads the settings, "so a secret written there is no longer secret."
- Proven by a read, never assumed. The reason: "a model drawn from a source nobody read has no basis."
- The first read writes nothing. The reason: this capability connects and takes in, and the prototype walk already holds that a step "Never changes data on a deployed site the person has not cleared."
- Only the tool knows the connection. The reason: "Plays, skills and sub-agents know only the tool, never the tracker.", and the same holds here, so the reads can later come from a listener outside Garura with no change to Garura's agents.
- Memory first, and no tool is a rule here. The reason: no tier holds which tools a project can connect to, and the agent's own knowledge cannot be checked.
- Not decided: which tools and forums a project can connect to, and how each is reached. No memory tier holds it, so it waits for research that a person approves as a memory update.
- Each key is kept where the deployment design keeps the project's secrets, and is never written down. The reason: the product owner approved it with the capability on 2026-11-10, "keys kept where the deployment design keeps secrets, never written down".
- Not decided: whether each key must be one that can read and cannot write.
- Not decided: whether Initialize asks for the connections when it sets the project up, and hands its answers here.

## Acceptance criteria
- Given a product whose code already loads a product analytics tool, when connections are proposed, then that tool is proposed with the file that names it as its source.
- Given the product owner's yes to a connection, when it is recorded, then the settings hold its name, what it is read for, what part of it is read and where its key is kept, and no key's value.
- Given a connection whose key is refused, when the first read runs, then the connection is named as not reading, with the reason, and no read uses it.
- Given any run of this feature, when its record is read, then no connected tool or forum shows a change made by it.

## Out of scope
- Reading how the product is used. Take in how the product is used, from its web analytics and product analytics (fn-take-in-use) does it.
- Reading what people say. Take in what people say about the product and its market, from feedback tools and forums (fn-take-in-what-people-say) does it.
- Changing a connection later. Update the connections as the product and its tools change (fn-update-connections) does it.
- Deciding where the project keeps its secrets. Deployment design owns it.
- Adding a measure or a feedback form to the product. That changes the product, which this capability never does.

## Sources
- The product owner on 2026-11-10, in .garura/project/issues/1021/context/bi-6-capability-1/page-approvals.md: "keys kept where the deployment design keeps secrets, never written down"
- The product owner on 2026-11-10, in .garura/project/issues/1021/context/bi-6-capability-1/page-approvals.md, spelling tidied: "connect to tools that access web analytics, product analytics, user feedback, and forums like Reddit", "This needs to be built for high autonomy."
- The list the product owner set on 2026-11-10, in .garura/project/issues/1021/context/capabilities.md: "Connect to what happens in use and in the market: tools that access web analytics, product analytics, user feedback, and forums like Reddit."
- The capability list the product owner agreed on 2026-11-03, in the same file: "Settings: Everything that can be turned on or off lives in settings."
- .garura/product/product-os/intents/bi-10.md: "Name a tracker in a play, skill or sub-agent, because they only know the tool."
- core/config.yaml: "Tools read this; plays, skills and sub-agents never name a tracker."
- docs/adr/065-the-models-index-is-changed-through-two-skills-the-model-never-names-a-plan-and-only-tools-know-the-tracker.md, section 4: "Tools read the settings and know how to reach the tracker.", "Plays, skills and sub-agents know only the tool, never the tracker."
- core/components/skills/platform-adapter/SKILL.md: "Resolves the active platform from config and dispatches to the correct CLI (gh for GitHub, glab for GitLab)."
- .garura/product/product-os/software-delivery-planning/deployment-design/capability.md: "The design names only where each secret is kept.", "so a secret written there is no longer secret."
- .garura/product/product-os/software-delivery-planning/initialize/capability.md: "A tracker is an outside system, and a write there is visible to the whole team."
- .garura/product/product-os/software-delivery-planning/initialize/fn-rerun-initialize/feature.md: "when the project changes: it gains a database, a web surface, personal data or a new tracker, or it drops one."
- .garura/product/product-os/software-delivery-planning/specify-product/capability.md: "a model drawn from a source nobody read has no basis."
- .garura/product/product-os/software-delivery-planning/manage-surfaces/capability.md: "A surface is a place where a person, or another system, opens the product to use it."
- core/components/skills/walk-prototype/SKILL.md: "Never changes data on a deployed site the person has not cleared."
- docs/adr/038-install-brings-no-memory.md: "agents call the tool, never a path, so a move to Griffin changes only the tool."
- core/tools/memory/GUIDE.md: "Do not guess. Draft the answer as a memory update, and a person approves or rejects it:"
