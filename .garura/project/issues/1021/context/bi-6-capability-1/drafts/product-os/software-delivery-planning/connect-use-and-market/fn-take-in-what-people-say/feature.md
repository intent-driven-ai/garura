# Feature: Take in what people say about the product and its market, from feedback tools and forums

## What it does
Once a user feedback tool or a forum is connected, this feature reads what users write to the team and what people say in that forum about the product, its kind of product and the products it competes with, and keeps each message or post in its own words, with where and when it was written and when it was read, and with every person's name and personal details taken out, so that what consumers want and what the competition is doing can be understood from people's own words.
- User feedback is what users write to the team about the product, such as a message sent from the product or a review. A forum is a public place where people talk; the product owner named Reddit as one.
- It reads only the places and topics its connection names, such as one forum and the threads about one kind of product.
- Each message or post is kept in its own words, with its connection, where it was, when it was written and when it was read, and a link back to it where the tool gives one. It is never summed up, sorted into themes or placed on an intent here.
- Before anything is kept, a person's name, handle, contact details and anything else that points to one person are taken out, from the words too.
- A connection that could not be read is recorded as not read, with the reason, and nothing is kept for it as if no one had spoken.
- The reads run on their own, when the project's settings say, without a person's yes for each read.
- It never writes to the tool or the forum: no post, reply, vote, tag or change of any kind.
- What it takes in, for example, in different kinds of product: for a clinic's booking app, patients' messages that they cannot find evening appointments, kept without their names or anything about their health that points to them; for a recipe app, a forum thread where cooks compare it with a rival app's shopping list; for a team's planning tool, reviews that ask for a calendar view.
- How it meets the capability: this is the half of the capability that hears people, users and the wider market, in their own words, so that the next capability of Run → Product understands what consumers want and what the competition is doing.

Status: not built. Nothing connects to a feedback tool or a forum, or reads one:
- Research on the web is built, and only for memory: it drafts a page "researched with its sources", which waits as a memory update until a person approves it. It is never a read of what people say about a product.
- An old design note, marked "Discovery draft. Not scoped, not implemented.", named a way to "Ingest customer feedback (tickets, sentiment, analytics) → cluster into themes → auto-file via `capture` → link to existing capabilities." Only its first step, taking feedback in, would be this feature's; the rest is understanding and filing.
- No memory tier holds how a project reads a feedback tool or a forum, or what may be kept from it.

## Inputs / Outputs
- In: each connected feedback tool and forum, with the places and topics it names and where its key is kept, from Choose the tools and forums a project reads, and connect to them (fn-connect-tools).
- In: the project's setting for when the reads run.
- In: the product profile's privacy level and compliance needs.
- Out: each message or post in its own words, with its connection, where it was, when it was written and read, and its link where the tool gives one, with no person's details, for the next capability of Run → Product.
- Out: each connection not read, with the reason.

## Rules & behavior
- In its own words, with where and when. The reason: a Source "is kept as it was when read; the snapshot never changes afterwards.", and people's own words are what the understanding of what they want starts from.
- People's details out before anything is kept, from the words too. The reason: every agent reads what is taken in, and the review already treats real personal data outside production as a finding.
- Only the places and topics the connection names. The reason: the product owner said yes to those, and a place no one weighed may hold people's data no one weighed.
- A failed read is named, never empty. The reason: "a model drawn from a source nobody read has no basis."
- No write to the tool or the forum. The reason: this capability connects and takes in; a write to an outside system "is visible to the whole team.", and in a public forum to everyone.
- No interpretation here, of the product or of a rival. The reason: understanding what consumers want and what the competition is doing is the next capability of Run → Product, by the product owner's list.
- Only through the tool, never production. The reason: "We are never touching production.", and reading feedback and forums "through their own tools is not touching production", as assumed with the list.
- Not decided: which forums and topics a project reads, how often and how far back. No memory tier holds it.
- Not decided: how a person's details are found and taken out of the words, and how that is checked.
- Not decided: where what is taken in is kept, and as what kind of record: a Source or a kind of its own, a change to the agreed map of what a product is made of.
- The reads go through one Garura tool, which can later take what a listener outside Garura reports, with no change to Garura's agents. The reason: the product owner approved it with the capability on 2026-11-10, "one Garura tool reads the settings and reaches each connection, and can later read what a listener outside Garura reports".

## Acceptance criteria
- Given a feedback message that holds its writer's name and email address in its words, when it is kept, then its words are kept with where and when, and neither the name nor the address is.
- Given a forum connected for one topic, when it is read, then only posts on that topic are kept, each with its link, when it was written and when it was read.
- Given a forum that cannot be read, when the read ends, then the record names it as not read, with the reason.
- Given any read, when it ends, then nothing was posted, replied to, voted on, tagged or changed in the tool or the forum.

## Out of scope
- Choosing and connecting the tools and forums. Choose the tools and forums a project reads, and connect to them (fn-connect-tools) does it.
- Reading how the product is used. Take in how the product is used, from its web analytics and product analytics (fn-take-in-use) does it.
- Understanding what people want and what rivals do, and placing it on an intent. The next capability of Run → Product does it.
- Answering a user or taking part in a forum. This capability never writes to a tool or a forum.
- Fixing a defect that a user reports. Fix defects test first takes in a defect reported anywhere.

## Sources
- The product owner on 2026-11-10, in .garura/project/issues/1021/context/bi-6-capability-1/page-approvals.md: "one Garura tool reads the settings and reaches each connection, and can later read what a listener outside Garura reports"
- The product owner on 2026-11-10, in .garura/project/issues/1021/context/bi-6-capability-1/page-approvals.md, spelling tidied: "connect to tools that access web analytics, product analytics, user feedback, and forums like Reddit", "start understanding what it is that the consumers want and what the competition is doing", "We are never touching production."
- The list the product owner set on 2026-11-10, in .garura/project/issues/1021/context/capabilities.md: "Understand what consumers want and what the competition is doing.", "Assumed: reading web analytics, product analytics, user feedback and forums through their own tools is not touching production"
- standards/schemas/product-os/ontology.md, in Phoenix memory: "It is kept as it was when read; the snapshot never changes afterwards."
- .garura/product/product-os/software-delivery-planning/specify-product/capability.md: "a model drawn from a source nobody read has no basis."
- .garura/product/product-os/software-delivery-planning/environment-setup/capability.md: "the review already treats real personal data in an environment other than production as a finding"
- .garura/product/product-os/software-delivery-planning/initialize/capability.md: "A tracker is an outside system, and a write there is visible to the whole team."
- .garura/product/product-os/software-delivery-planning/fix-defects-test-first/capability.md: "In: taking in a defect reported anywhere: a person's words, a finding in a review, the eval after the work was accepted, or a bug in a plan."
- core/components/skills/author-knowledge-page/SKILL.md: "researched with its sources", "the knowledge-builder agent raises the page through the memory tool as a memory update a person approves"
- docs/design/playbook-catalog.md: "Discovery draft. Not scoped, not implemented.", "Ingest customer feedback (tickets, sentiment, analytics) → cluster into themes → auto-file via `capture` → link to existing capabilities."
