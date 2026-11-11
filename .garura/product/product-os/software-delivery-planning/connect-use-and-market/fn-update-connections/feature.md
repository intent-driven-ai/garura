# Feature: Update the connections as the product and its tools change

## What it does
As the product and its tools change, this feature proposes a new, changed or dropped connection, the product owner says yes to each, and what held before stays readable with why it changed, so the project keeps reading the tools and forums that hold its use and what people say about it now.
- A connection is one outside tool or forum the project reads. Choose the tools and forums a project reads, and connect to them (fn-connect-tools) records the first ones.
- A project changes as it grows. For example: a shop's checkout gains a phone app, so the analytics tool its new code loads is proposed; a clinic's booking app moves its feedback form to another tool, so the old connection is dropped and the new one proposed; a team's planning tool is talked about in a new forum, so the product owner adds it; or a key is taken away, so a connection keeps failing.
- An update is proposed from what changed, memory first: the project's own code and settings, such as a tool the code now loads or no longer loads; the product's declared surfaces; and the records of reads that failed. Then Garura memory, then Phoenix memory. Only when none of them answers is it researched, and what research finds waits as a memory update for a person to approve.
- A connection that keeps failing is named to the product owner, with which connection and why. It is never dropped without a word, and the other connections go on being read.
- Each update keeps what held before: the connection as it was, what changed, why, and who said yes. A key that changes is changed where it is kept, never written down.
- How it meets the capability: the capability keeps taking in what happens in use and in the market only while its connections match the product and its tools; this feature keeps them matched.

Status: not built. What exists covers only patterns for it:
- The approved pages for environments and for the deployment design each have an update feature of this shape: a person confirms each update, and "what held before stays readable with why it changed". Neither is built.
- Initialize is planned to run again "when the project changes: it gains a database, a web surface, personal data or a new tracker, or it drops one." It is not built, and it covers no connection.

## Inputs / Outputs
- In: the connections the project's settings record, and the records of earlier reads, with each failed read and its reason.
- In: the project's code and settings as they are now, and the product's declared surfaces from Manage surfaces.
- In: the product owner's word on a forum or a tool to add or drop.
- Out: each proposed update, with what changed, why and its source, for the product owner's yes.
- Out: each approved update in the settings, with the connection as it was before, what changed, why, and who said yes.
- Out: each connection that keeps failing, named to the product owner, with the reason.

## Rules & behavior
- The product owner says yes to each update: a new connection, a change or a drop. The reason: a change opens or closes a team's account or a public place to the project, as a first connection does.
- What held before stays readable, with why it changed. The reason: the approved update features keep it the same way, and a read taken in from a connection that was later dropped must still say where it came from.
- A connection that keeps failing is named, never dropped silently, and blocks no other connection. The reason: a gap kept as nothing would read as no one used the product or said anything, and one broken connection says nothing about the others.
- Names only for keys, during an update too. The reason: the deployment design "names only where each secret is kept", "so a secret written there is no longer secret."
- Memory first, then research through a memory update a person approves. The reason: no update comes from what the AI agent knows by itself.
- Not decided: how many failed reads make a connection one that keeps failing.
- Not decided: whether Initialize, when it runs again, proposes these updates and hands them here.

## Acceptance criteria
- Given a product whose code now loads a new analytics tool for its phone app, when an update is proposed, then that tool is proposed with the file that names it, and it is not read before the product owner's yes.
- Given a connection whose key was taken away, when its reads keep failing, then the product owner is told which connection failed and why, and the other connections are still read.
- Given a dropped connection, when the settings are read, then what it was, why it was dropped and who said yes stay readable.
- Given any update, when the settings and records are read, then no key's value is in them.

## Out of scope
- The first connections. Choose the tools and forums a project reads, and connect to them (fn-connect-tools) records them.
- Reading each connection. Take in how the product is used, from its web analytics and product analytics (fn-take-in-use) and Take in what people say about the product and its market, from feedback tools and forums (fn-take-in-what-people-say) do it.
- Declaring the product's surfaces. Manage surfaces does it.
- Changing a key where it is kept, and deciding where that is. Deployment design says where secrets are kept.

## Sources
- The product owner on 2026-11-10, in .garura/project/issues/1021/context/bi-6-capability-1/page-approvals.md, spelling tidied: "connect to tools that access web analytics, product analytics, user feedback, and forums like Reddit"
- The capability list the product owner agreed on 2026-11-03, in .garura/project/issues/1021/context/capabilities.md: "Settings: Everything that can be turned on or off lives in settings."
- .garura/product/product-os/software-delivery-planning/environment-setup/fn-update-environments/feature.md: "a person confirms an update, and what held before stays readable with why it changed"
- .garura/product/product-os/software-delivery-planning/environment-setup/fn-update-environments/ice.md: "keeping what held before with why it changed"
- .garura/product/product-os/software-delivery-planning/deployment-design/fn-update-deployment/feature.md: "a person confirms an update, and what held before stays readable with why it changed"
- .garura/product/product-os/software-delivery-planning/initialize/fn-rerun-initialize/feature.md: "when the project changes: it gains a database, a web surface, personal data or a new tracker, or it drops one."
- .garura/product/product-os/software-delivery-planning/manage-surfaces/capability.md: "A surface is a place where a person, or another system, opens the product to use it."
- .garura/product/product-os/software-delivery-planning/deployment-design/capability.md: "The design names only where each secret is kept.", "so a secret written there is no longer secret."
- core/tools/memory/GUIDE.md: "Do not guess. Draft the answer as a memory update, and a person approves or rejects it:"
