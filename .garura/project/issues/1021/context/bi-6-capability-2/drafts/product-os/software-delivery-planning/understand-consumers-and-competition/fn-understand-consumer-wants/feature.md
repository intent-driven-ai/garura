# Feature: Understand what consumers want, from what is taken in

## What it does
Once the first capability of Run → Product has taken in figures, messages and posts, this feature sorts those items into wants, the needs and problems that come up across many items, and sums each one: every item it rests on, how many items from which connections, how the count moved over time, and how sure it is, so that the product owner and the next capability see what consumers want from what they really did and said.
- An item is one figure, message or post the first capability took in, kept as the tool gave it, with its connection, where it was and when it was read. A connection is one outside tool or forum the project reads.
- A want is a need or a problem in plain words. It can rest on words, on figures or on both: messages and posts say what people ask for or complain about, and figures show where people stop, what they use and whether they come back.
- Each want lists every item it rests on, by its connection, place and date, with the words or figures it uses quoted exactly as taken in. Items that say the opposite are listed with it, never left out.
- Each want is summed: how many items, from how many connections, over what time, and how the count moved within that time, for example week by week. A tool makes the counts and sums from the items; the agent never works one out in its head.
- Every item is accounted for. It rests under a want, or it is listed as not used, with why, such as a post that only says thanks.
- How sure a want is shows as facts a person can check: how many items, from how many connections, over what time, and from words, figures or both. A want that rests on few items or on one connection is marked weak.
- Items are counted, never people. No person's details are kept, so a want says how many items ask for it, not how many people.
- What people wrote is read as what they said, never as an instruction to the agent.
- It runs on its own each time new items come in, with no person's yes, because it writes only its own findings and changes nothing else.
- What it draws out, for example, in different kinds of product: for a clinic's booking app, patients who want evening appointments, from their messages and from how many leave the booking page when no evening time is shown; for a shop's checkout, shoppers who leave when they see the delivery cost, from the figures of the cart and the payment page and from their reviews; for a team's planning tool, teams who ask for a calendar view, from reviews and forum posts, marked weak while it rests on one forum.
- How it meets the capability: this is the half of the capability that understands what consumers want, sorted and summed from what is taken in, so each want can be placed on the product and handed on.

Status: not built. What exists covers only patterns for it:
- Nothing sorts or sums what the users of a product say or do, and nothing is taken in yet, because the first capability of Run → Product is not built.
- An old design note, marked "Discovery draft. Not scoped, not implemented.", would "cluster into themes" the feedback it took in. It was never built.
- Specify the product groups the parts of what one person gives by the need each meets, and "Every part is mapped to the intent it serves (the coverage map)". It works on one person's source at a time, not on many consumers' items.
- The stale learning play gave each change "the outcome that justifies it and a confidence tier".
- No memory tier says how to draw wants from feedback, posts and figures.

## Inputs / Outputs
- In: the items the first capability took in, each with its connection, where it was and when it was read, and the record of each read that failed.
- In: the project's settings for when the understanding runs and what counts as few items.
- In: the earlier findings, from Update the understanding as new items come in and the product changes (fn-update-understanding).
- Out: each want in plain words, with every item it rests on, quoted as taken in, the items that say the opposite, its counts by connection and over time, and how sure it is, with the weak mark when it applies; for Place each finding on the intents, capabilities and features it bears on (fn-place-findings).
- Out: each item not used, with why.

## Rules & behavior
- Every want names its items, word for word or figure for figure. The reason: "Each finding says where it comes from. The reason: a person can then check each finding without a search."
- Every item is accounted for, under a want or listed as not used with why. The reason: an item left out without a word could hide a want, and Specify the product already maps every part of what it reads, with the rule "never leave a part out".
- The same items give the same wants. A second run on the same items gives the same wants, the same items under each and the same counts, and a tool makes the counts and sums. The reason: people act on the wants, so a want that changes when nothing new came in says something about the agent, not about the consumers; the evals hold the same rule, "two runs of one eval on one built product give the same verdict".
- A weak want is shown as weak, never dropped and never shown as strong. The reason: a weak want shown as strong sends the next capability after the wrong change, and one dropped hides a want that may grow.
- Items, not people. The reason: the first capability keeps no person's details, so how many different people asked cannot be known, and finding out would bring back who they are.
- What people wrote is never an instruction. The reason: anyone can write in a public forum, and memory's guardrails for agents name "prompt-injection and untrusted-content defense".
- A failed read stays a gap. A connection that could not be read is shown as not read for its time, and no want treats its silence as no one asking. The reason: the first capability names each failed read, because "a gap kept as nothing would read as nobody used the product".
- It runs on its own. The reason, in the product owner's words: "This needs to be built for high autonomy."
- Not decided: how wants are drawn from free words and figures, and how close two items must be to rest under one want. No memory tier holds it, so it waits for research that a person approves as a memory update.
- Not decided: how few items, or how few connections, make a want weak. It is a project setting, and no source sets it.
- Not decided: how a second run is made to give the same wants: by keeping the first grouping and placing only new items under it, or by drawing the wants again and comparing.
- Not decided: where the wants are kept, and as what kind of record. Like what is taken in, it is a change to the agreed map of what a product is made of.

## Acceptance criteria
- Given forty feedback messages and forum posts, when they are understood, then each want lists every item it rests on with its words quoted as taken in, and each of the forty is under a want or listed as not used, with why.
- Given the same items, when the understanding runs a second time, then it gives the same wants, the same items under each and the same counts.
- Given a want that rests on two posts from one forum, when it is shown, then it is marked weak and still listed.
- Given a post whose words tell the reader to do something, when it is understood, then it is counted only as what was said, and nothing else is done.
- Given any run, when it ends, then no intent, page, memory, tracker or connected tool shows a change made by it.

## Out of scope
- Taking in the items. Connect to what happens in use and in the market does it.
- Understanding what the competition is doing. Understand what the competition is doing, from what people say about it (fn-understand-competition) does it.
- Placing a want on the intents, capabilities and features it bears on. Place each finding on the intents, capabilities and features it bears on (fn-place-findings) does it.
- Showing the wants to the product owner. Show the findings to the product owner, and hand them to the next capability (fn-hand-on-findings) does it.
- Deciding what to build or change for a want. The third capability of Run → Product does it.
- Measuring whether an intent got what it wanted. It is parked (#545).

## Sources
- The product owner on 2026-11-10, in .garura/project/issues/1021/context/bi-6-capability-2/page-approvals.md, spelling tidied: "start understanding what it is that the consumers want and what the competition is doing", "This needs to be built for high autonomy."
- The list the product owner set on 2026-11-10, in .garura/project/issues/1021/context/capabilities.md: "Understand what consumers want and what the competition is doing.", "measuring each intent (#545, parked)"
- .garura/product/product-os/software-delivery-planning/connect-use-and-market/capability.md: "What is taken in is each figure, message or post a connection holds, kept as the tool gave it, with the connection it came from, where it was, and when it was read.", "Out: understanding what consumers want and what the competition is doing from what is taken in, which includes sorting it, summing it and placing it on the intents it bears on."
- .garura/product/product-os/software-delivery-planning/connect-use-and-market/fn-take-in-use/feature.md: "a gap kept as nothing would read as nobody used the product"
- .garura/product/product-os/software-delivery-planning/keep-spec-matched/fn-find-spec-drift/feature.md: "Each finding says where it comes from. The reason: a person can then check each finding without a search."
- .garura/product/product-os/software-delivery-planning/test-product-with-evals/capability.md: "two runs of one eval on one built product give the same verdict"
- core/components/skills/author-business-intent/SKILL.md: "Every part is mapped to the intent it serves (the coverage map)", "never leave a part out"
- core/components/skills/author-learnings/SKILL.md: "Each proposed change carries the outcome that justifies it and a confidence tier."
- docs/design/playbook-catalog.md: "Discovery draft. Not scoped, not implemented.", "cluster into themes"
- knowledge/architecture/agentic-guardrails-baseline.md, in Phoenix memory: "prompt-injection and untrusted-content defense"
- core/tools/memory/GUIDE.md: "Do not guess. Draft the answer as a memory update, and a person approves or rejects it:"
