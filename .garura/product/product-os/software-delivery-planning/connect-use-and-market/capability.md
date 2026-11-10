# Capability: Connect to what happens in use and in the market

## Directional intent
Connect to what happens in use and in the market: the project connects to the tools that hold how its product is used and what people say about it (web analytics, product analytics, user feedback and forums such as Reddit), and takes in what they hold, as given, so that what consumers want and what the competition is doing can be understood from what really happened.
In the product owner's words, Run → Product must "connect to tools that access web analytics, product analytics, user feedback, and forums like Reddit". The words this page uses:
- A connection is one outside tool or forum the project reads. It is recorded in the project's settings by its name, with what it is read for and where its access key is kept, never the key itself.
- Web analytics count how people reach and move through the product's web pages. Product analytics count how people use the product's features over time, such as who uses a feature and who comes back. User feedback is what users write to the team about the product. A forum is a public place where people talk, about the product, its kind of product and the products it competes with.
- What is taken in is each figure, message or post a connection holds, kept as the tool gave it, with the connection it came from, where it was, and when it was read.

This capability does four jobs:
- Choose the connections. The tools and forums a project reads are proposed from what the project already holds, and the product owner says yes to each.
- Take in how the product is used, from its web analytics and product analytics: the figures as each tool gives them, never the record of one person.
- Take in what people say, from its feedback tools and forums: each message or post in its own words, with every person's name and personal details taken out before it is kept.
- Update the connections as the product and its tools change, keeping what held before and why it changed.

It reads and keeps; it never interprets. Understanding what consumers want and what the competition is doing is the next capability of Run → Product, and building features or updating the product intent model is the third. Keep the spec matched to what's built keeps the spec true to what the agents built, "not what the user is telling", in the product owner's words; what the users and the market tell comes in here.
The product owner asked for this kind of work to run with little waiting on people: "This needs to be built for high autonomy." So the reads run on their own, as the project's settings say, and a person says yes only to each connection and to each change of one. Reading what these tools hold, through the tools themselves, is assumed not to touch production, and "We are never touching production." stands.
What to propose comes from memory first: the project's own code and memory, such as an analytics tool the product's code already loads, then Garura memory, the memory Garura keeps for the project, then Phoenix memory, the shared memory on the machine that every project draws from. Only when none of them answers is it researched, and what research finds is raised as a memory update, a proposed addition to memory, and used only after a person approves it. Nothing comes from what the AI agent knows by itself.
It matters to software delivery planning because that domain turns business intents into working code, and an intent is only as true as what is known of the product's use. The domain's first paragraph does not yet say this; whether this capability stays in the domain, with that paragraph changed when Run → Product closes, or moves to a domain of its own, is not decided.

Features:
- Choose the tools and forums a project reads, and connect to them (fn-connect-tools): proposes the connections the project should have from what the project already holds, records each one the product owner says yes to in the project's settings by name, with what it is read for and where its key is kept, and proves each with a first read that changes nothing.
- Take in how the product is used, from its web analytics and product analytics (fn-take-in-use): reads from each connected analytics tool what it reports about how people reach and use the product, and keeps each figure as the tool gave it, with the connection, the time it covers and when it was read, and never the record of one person.
- Take in what people say about the product and its market, from feedback tools and forums (fn-take-in-what-people-say): reads what users write to the team and what people say in the forums the project connects to, and keeps each message or post in its own words, with where and when it was written, and with every person's name and personal details taken out.
- Update the connections as the product and its tools change (fn-update-connections): proposes a new, changed or dropped connection when the product gains a surface, its code starts or stops using a tool, or a connection keeps failing, and keeps what held before and why it changed, with the product owner's yes for each.

What is not built yet:
- Nothing connects Garura to a web analytics tool, a product analytics tool, a feedback tool or a forum, and nothing reads one. No setting names one.
- Three built parts read an outside system, and none reads how a product is used or what its users say. The tracker connector reads and writes the team's issues: the settings name the tracker, "Tools read this; plays, skills and sub-agents never name a tracker.", and the code host's own command line holds the access. The capture of a prototype reads what a person shares, including a deployed site, and keeps what they shared as Sources, "exactly as they were when read"; and "Never changes data on a deployed site the person has not cleared." Research on the web drafts a page for memory only as a memory update a person approves.
- The old learning play, /learn-outcomes, is stale. It read Garura's own records of a delivered piece of work, such as "what production actually needed versus what was planned", and never an outside tool; every input it read is gone or stale.
- Phoenix memory holds a shelf on building analytics into a product. It holds nothing on which tools and forums a project can read, how each is reached, or what may be kept from them.
- A listener outside Garura is a design note only: Griffin, a tool planned beside Garura, "Listens — to the product, to signals, to quality — and reports."

### Benefit hypothesis
- Who it serves: the product owner, who chooses what the project reads, says yes to each connection, and wants what consumers want and what the competition is doing understood from what really happened rather than guessed; and the parts of Run → Product that understand it next.
- What we believe: when the project reads its own analytics, feedback and forums and keeps what they hold as given, the understanding of what consumers want starts from what happened in use and in the market, if the work stands on these rules:
  - Each item is kept as the tool gave it, with its connection, where it was and when it was read.
  - A read that failed is named with its reason, never kept as if nothing happened.
  - Nothing that names or points to one person, and no key's value, is ever kept.
  - Nothing is written to a connected tool or forum, and production is never read.
  - The product owner says yes to each connection; the reads then run on their own.
- How we will know: every item taken in names its connection, where it was and when it was read; two reads of the same connection over the same time give the same items; no item, record or log holds a person's details or a key's value; no tool or forum shows a write from the project; and every failed read is named.
  - This is not tested today, because nothing connects.

### Boundary (In / Out / Never)
- In: choosing the tools and forums a project reads, with the product owner's yes for each, and recording each connection by name, with what it is read for and where its key is kept.
- In: taking in how the product is used, from its web analytics and product analytics, as each tool gives it.
- In: taking in what people say about the product and its market, from feedback tools and forums, in their own words, with people's personal details taken out.
- In: updating the connections as the product and its tools change.
- Out: understanding what consumers want and what the competition is doing from what is taken in, which includes sorting it, summing it and placing it on the intents it bears on. The second capability of Run → Product owns it.
- Out: building features into the product, or updating the product intent model, automatically or as recommendations. The third capability of Run → Product owns it.
- Out: keeping the spec matched to what the agents built. Keep the spec matched to what's built owns it.
- Out: choosing and promoting what is learned into Garura memory or Phoenix memory, which the review of Memory owns; and measuring each intent, which is parked (#545).
- Out: changing what the product records about its own use, such as adding a measure to its code. That changes the product, which this capability never does.
- Out: where the project keeps its secrets, which Deployment design owns; and the product profile's privacy level and compliance needs, which Specify the product sets. This capability reads them and never writes them.
- Never: write to a connected tool or forum: no post, reply, vote, tag, change or deletion, and no change of its settings. The reason: this capability connects and takes in, and a write to an outside system "is visible to the whole team"; in a public forum it is visible to everyone.
- Never: read production, or the product's own stores of data, other than through the tools the team already uses to look at them. The reason, in the product owner's words: "We are never touching production."; reading what those tools hold, through the tools themselves, is the assumption recorded with his list.
- Never: write a key's value into the settings, a record, a log or what is taken in. The settings name only where each key is kept. The reason: every agent reads these files, "so a secret written there is no longer secret."
- Never: keep a person's name, handle, contact details or anything else that points to one person. The reason: every agent reads what is taken in, and the review already treats real personal data outside production as a finding.
- Never: change, sort, sum or interpret what is taken in, or change an intent, the model or memory. The reason: the next two capabilities of Run → Product own that, and Run → Product must not "Change an intent, or promote memory, without a person."
- Never: make a choice from what the AI agent knows by itself. The reason: a source in the project or in memory can be checked and read back, while the agent's own knowledge cannot.

### Guiding rules
- As given, with where and when. Each figure, message or post is kept as the tool gave it, with its connection, where it was and when it was read, and is never changed afterwards. The reason: a Source "is kept as it was when read; the snapshot never changes afterwards.", and what is kept must outlive the link, as a Source must "outlive the link or the file".
- A failed read is named, never empty. A connection that could not be read is recorded as not read, with its reason, and no figure or post is made up or carried over for it. The reason: "a model drawn from a source nobody read has no basis.", and a gap kept as nothing would read as nobody used the product.
- The product owner says yes to each connection, and the reads run on their own. The reason: a connection opens a team's account or a public place to the project and may bring in people's words; once it is approved, reading changes nothing outside, and the product owner asked that this work be "built for high autonomy".
- Only what the connection was set up for. Each read takes only the product, pages, places or topics its connection names. The reason: what was not approved was not looked at by the product owner, and may hold people's data no one weighed.
- Names only for keys. The settings name each connection and where its key is kept; the key is taken where it is kept at the moment of reading and never written down. The reason: the deployment design "names only where each secret is kept", and Phoenix memory's learning keeps keys "only in secrets management, never in the repo or the config files."
- People's details out before anything is kept. A person's name, handle, contact details and anything else that points to one person are taken out of a message or post, its words included, before it is kept; from analytics, only figures about many people are kept. The reason: the review already treats real personal data outside production as a finding, and memory's own analytics shelf names the consumer's stake as "measure me without abusing my data".
- Only the tool knows the connection. Plays, skills and sub-agents call one tool, which reads the project's settings and knows how to reach each connection; they never name a tool or forum. The reason: this is how the tracker is reached ("Plays, skills and sub-agents know only the tool, never the tracker."), and how memory is reached, so that "a move to Griffin changes only the tool": the reads can later come from a listener outside Garura without changing Garura's agents.
- The project's memory first, then Garura memory, then Phoenix memory, then research through a memory update a person approves. What nothing answers stays open, with no default. The reason: research is new knowledge that nobody has checked yet, and the person's approval is the check.

## Sources
- The product owner on 2026-11-10, in .garura/project/issues/1021/context/bi-6-capability-1/page-approvals.md, spelling tidied: "connect to tools that access web analytics, product analytics, user feedback, and forums like Reddit", "start understanding what it is that the consumers want and what the competition is doing", "start building features into the product or start updating the product intent model automatically, or at least making those recommendations", "This needs to be built for high autonomy.", "an autonomous kind of agent running that goes back and does this thing for me", "not what the user is telling", "We are never touching production."
- The list the product owner set on 2026-11-10, in .garura/project/issues/1021/context/capabilities.md: "Connect to what happens in use and in the market: tools that access web analytics, product analytics, user feedback, and forums like Reddit.", "Understand what consumers want and what the competition is doing.", "Build features into the product, or update the product intent model, automatically, or at least recommend those changes.", "Assumed: reading web analytics, product analytics, user feedback and forums through their own tools is not touching production", "measuring each intent (#545, parked)"
- The capability list the product owner agreed on 2026-11-03, in the same file: "Settings: Everything that can be turned on or off lives in settings."
- .garura/product/product-os/intents/bi-6.md: "What happens in use flows back.", "Change an intent, or promote memory, without a person."
- .garura/product/product-os/intents/bi-10.md: "Name a tracker in a play, skill or sub-agent, because they only know the tool."
- .garura/product/product-os/software-delivery-planning/domain.md: "This domain turns a business intent into working code that a check from the outside can prove.", "It does not release the work or run the product."
- .garura/product/product-os/software-delivery-planning/keep-spec-matched/capability.md: "What users say once the product runs is not part of it. Run → Product handles that."
- .garura/product/product-os/software-delivery-planning/specify-product/capability.md: "The reason: the Source must outlive the link or the file.", "a model drawn from a source nobody read has no basis."
- .garura/product/product-os/software-delivery-planning/deployment-design/capability.md: "The design names only where each secret is kept.", "so a secret written there is no longer secret."
- .garura/product/product-os/software-delivery-planning/environment-setup/capability.md: "the review already treats real personal data in an environment other than production as a finding"
- .garura/product/product-os/software-delivery-planning/initialize/capability.md: "A tracker is an outside system, and a write there is visible to the whole team."
- standards/schemas/product-os/ontology.md, in Phoenix memory: "It is kept as it was when read; the snapshot never changes afterwards."
- knowledge/domains/analytics.md, in Phoenix memory: "Product analytics — feature usage, adoption, retention, cohorts, paths.", "Web analytics — the existing page-load/CTA layer", "measure me without abusing my data"
- knowledge/technology/run-environments-canary-migrations.md, in Phoenix memory: "Credentials and provider keys live only in secrets management, never in the repo or the config files."
- core/config.yaml: "Tools read this; plays, skills and sub-agents never name a tracker."
- docs/adr/065-the-models-index-is-changed-through-two-skills-the-model-never-names-a-plan-and-only-tools-know-the-tracker.md, section 4: "Plays, skills and sub-agents know only the tool, never the tracker."
- docs/adr/038-install-brings-no-memory.md: "agents call the tool, never a path, so a move to Griffin changes only the tool."
- core/components/plays/discover-intent/SKILL.md: "Keeps what they shared as Sources, exactly as they were when read"
- core/components/skills/walk-prototype/SKILL.md: "Never changes data on a deployed site the person has not cleared."
- core/components/skills/author-knowledge-page/SKILL.md: "the knowledge-builder agent raises the page through the memory tool as a memory update a person approves"
- core/components/plays/learn-outcomes/SKILL.md: "waits for the rebuild of the learn loop on the current product model (#855)"
- core/components/plays/learn-outcomes/reference/ice.md: "what production actually needed versus what was planned"
- docs/philosophy/intent-and-adlc.md, a design note marked "designed, not in force": "Listens — to the product, to signals, to quality — and reports."
- core/tools/memory/GUIDE.md: "Do not guess. Draft the answer as a memory update, and a person approves or rejects it:"
- The short line beside each feature: the opening words of that feature's own page.
- Shelf: none. No knowledge shelf covers this work: a placement over the ten domain shelves found none (.garura/project/issues/1021/context/bi-6-capability-1/placement/routing-result.json, unmatched).
