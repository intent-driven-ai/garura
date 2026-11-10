# Feature: Take in how the product is used, from its web analytics and product analytics

## What it does
Once a web analytics or product analytics tool is connected, this feature reads from it what it reports about how people reach and use the product, and keeps each figure as the tool gave it, with the connection, the time it covers and when it was read, so that what consumers want can be understood from what they really did.
- Web analytics count how people reach and move through the product's web pages, such as visits to a page. Product analytics count how people use the product's features over time, such as how many start a task and how many finish it, or who comes back. Phoenix memory's analytics shelf draws the same line: "Web analytics — the existing page-load/CTA layer" against "Product analytics — feature usage, adoption, retention, cohorts, paths."
- It reads only what its connection names, such as one product and its pages, and only figures about many people. It never keeps the record of one person's use.
- Each figure is kept as the tool gave it: the tool's own name for what it counts, the figure, the time it covers, the connection and when it was read. It is never reworded, summed into a new figure or compared with an intent here.
- A connection that could not be read, or answered only in part, is recorded as not read, with the reason. No figure is made up or carried over for it.
- The reads run on their own, when the project's settings say, without a person's yes for each read, because a read changes nothing in the tool, in the product, in an intent or in memory.
- It reads the analytics tool through its own way in and nothing else: never production, never the product's own stores of data, and never a write to the tool.
- What it takes in, for example, in different kinds of product: for a shop's checkout, how many people opened the cart and how many paid, each day of a week; for a school's timetable app, which pages were opened on phones and on computers; for a team's planning tool, how many teams used its board view in a month and how many came back the month after.
- How it meets the capability: this is the "in use" half of the capability, in figures, so that the next capability of Run → Product understands what consumers want from what happened.

Status: not built. Nothing connects to an analytics tool or reads one:
- The old learning play, /learn-outcomes, is stale. It read Garura's own records of a delivered piece of work, such as "what production actually needed versus what was planned", through a run design that is also stale, and never an analytics tool.
- The old design of how a slice is found and reached was stale and is dropped. It named "the reach signals worth capturing" in a slice, and read none of them.
- Phoenix memory's analytics shelf is about building analytics into a product. It does not say how a project reads its own analytics tool.

## Inputs / Outputs
- In: each connected web analytics and product analytics tool, with what part of it is read and where its key is kept, from Choose the tools and forums a project reads, and connect to them (fn-connect-tools).
- In: the project's setting for when the reads run.
- In: the product profile's privacy level and compliance needs.
- Out: each figure the tool gave, with its name in the tool, the time it covers, the connection and when it was read, for the next capability of Run → Product.
- Out: each connection not read, or read only in part, with the reason.

## Rules & behavior
- As the tool gave it, with where and when. The reason: a Source "is kept as it was when read; the snapshot never changes afterwards.", and what is kept must outlive the link, as a Source must "outlive the link or the file".
- A failed read is named, never empty. The reason: a gap kept as nothing would read as nobody used the product, and "a model drawn from a source nobody read has no basis."
- Only figures about many people, never one person's record. The reason: every agent reads what is taken in, and the review already treats real personal data outside production as a finding; memory's analytics shelf names the consumer's stake as "measure me without abusing my data".
- No interpretation here. The reason: understanding what consumers want is the next capability of Run → Product, and the product owner's list keeps it apart.
- Only through the tool, never production. The reason: "We are never touching production.", and reading analytics "through their own tools is not touching production", as assumed with the list.
- No write to the tool. The reason: this capability connects and takes in, and a write to an outside system "is visible to the whole team."
- The reads run on their own. The reason, in the product owner's words: "This needs to be built for high autonomy."
- Not decided: how often the reads run and how far back each reads.
- Not decided: where what is taken in is kept, and as what kind of record: a Source, as the product model keeps what a person gave, or a kind of its own. Either is a change to the agreed map of what a product is made of.
- The reads go through one Garura tool, which can later take what a listener outside Garura reports, with no change to Garura's agents. The reason: the product owner approved it with the capability on 2026-11-10, "one Garura tool reads the settings and reaches each connection, and can later read what a listener outside Garura reports".

## Acceptance criteria
- Given a connected product analytics tool and a week, when it is read, then each figure kept carries the tool's own name for it, the week, the connection and when it was read, and equals what the tool gave.
- Given a tool that refuses the read, when the read ends, then the record names the connection as not read, with the reason, and holds no figure for it.
- Given a tool that answers with a record of one person's use, when the read is kept, then nothing that names or points to that person is kept.
- Given any read, when it ends, then the tool shows no change made by it.

## Out of scope
- Choosing and connecting the tools. Choose the tools and forums a project reads, and connect to them (fn-connect-tools) does it.
- Reading what people say. Take in what people say about the product and its market, from feedback tools and forums (fn-take-in-what-people-say) does it.
- Understanding what the figures mean for what consumers want. The next capability of Run → Product does it.
- Measuring whether an intent got what it wanted. It is parked (#545).
- Adding a measure to the product's code. That changes the product, which this capability never does.

## Sources
- The product owner on 2026-11-10, in .garura/project/issues/1021/context/bi-6-capability-1/page-approvals.md: "one Garura tool reads the settings and reaches each connection, and can later read what a listener outside Garura reports"
- The product owner on 2026-11-10, in .garura/project/issues/1021/context/bi-6-capability-1/page-approvals.md, spelling tidied: "connect to tools that access web analytics, product analytics, user feedback, and forums like Reddit", "This needs to be built for high autonomy.", "We are never touching production."
- The list the product owner set on 2026-11-10, in .garura/project/issues/1021/context/capabilities.md: "Understand what consumers want and what the competition is doing.", "Assumed: reading web analytics, product analytics, user feedback and forums through their own tools is not touching production", "measuring each intent (#545, parked)"
- knowledge/domains/analytics.md, in Phoenix memory: "Web analytics — the existing page-load/CTA layer", "Product analytics — feature usage, adoption, retention, cohorts, paths.", "measure me without abusing my data"
- standards/schemas/product-os/ontology.md, in Phoenix memory: "It is kept as it was when read; the snapshot never changes afterwards."
- .garura/product/product-os/software-delivery-planning/specify-product/capability.md: "The reason: the Source must outlive the link or the file.", "a model drawn from a source nobody read has no basis."
- .garura/product/product-os/software-delivery-planning/environment-setup/capability.md: "the review already treats real personal data in an environment other than production as a finding"
- .garura/product/product-os/software-delivery-planning/initialize/capability.md: "A tracker is an outside system, and a write there is visible to the whole team."
- core/components/plays/learn-outcomes/SKILL.md: "waits for the rebuild of the learn loop on the current product model (#855)"
- core/components/plays/learn-outcomes/reference/ice.md: "what production actually needed versus what was planned"
- core/components/plays/shape-marketing-lens/SKILL.md: "the reach signals worth capturing"
- .garura/project/issues/1021/context/names.md: "Dropped: /shape-marketing-lens, /shape-measure-lens."
- GitHub #545 (open, parked): "Did the org get what it wanted"
