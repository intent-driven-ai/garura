# Feature: Understand what the competition is doing, from what people say about it

## What it does
Once the product owner has said which competitors the project follows, this feature draws from the items taken in what people say each of them does: what they praise or miss in it, why they move to it or away from it, and what it offers that this product does not, each finding with every item it rests on, so that the product owner sees what the competition is doing through what consumers say.
- The competition is the other products people could choose instead of this one. The first capability takes in what people say "about the product, its kind of product and the products it competes with".
- The competitors to follow are proposed from memory first: the project's own memory, then Garura memory, then Phoenix memory; and from the rivals people name in what is taken in. Only when none of them names one is it researched, and what research finds waits as a memory update until a person approves it. Each proposal names its source.
- The product owner says yes to each competitor the project follows. A rival people name often, and that is not followed, is shown to him as a proposal, never followed in silence.
- Only what was taken in is read about a competitor: the messages and posts that name it, from the feedback tools and forums the project connects to. Nothing else about it is read here.
- Each finding names a competitor, what people say it does, offers or lacks, and every item it rests on, quoted as taken in, with its counts and how sure it is. A finding that rests on few items or one connection is marked weak.
- A finding says what people say a competitor does, never that it does it. The items are people's words, not the competitor's own.
- Nothing about a competitor comes from what the AI agent knows by itself.
- What it draws out, for example, in different kinds of product: for a recipe app, cooks who say a rival's shopping list groups items by shop aisle; for a team's planning tool, teams who say they moved to a rival for its calendar view; for a school's timetable app, parents who say a rival sends a note when a lesson moves.
- How it meets the capability: this is the half of the capability that understands what the competition is doing, from the same items and under the same rules as what consumers want.

Status: not built. Nothing follows a competitor or understands one:
- The first capability will take in forum posts that compare the product with its rivals, such as "a forum thread where cooks compare it with a rival app's shopping list". It is not built.
- One built skill researches "market data, competitive landscape" on the web for the technical designer, and writes what it finds straight into short-term memory, not as a memory update a person approves. It is not used for this, and it does not keep the rule that research waits for a person's approval.
- No memory tier names a product's competitors or says how to follow one.

## Inputs / Outputs
- In: the items the first capability took in, each with its connection, where it was and when it was read.
- In: the competitors the product owner follows, and memory's answers on who they are, through the memory tool.
- In: the earlier findings, from Update the understanding as new items come in and the product changes (fn-update-understanding).
- Out: each competitor proposed to follow, with its source, for the product owner's yes.
- Out: each finding about a followed competitor: what people say it does, offers or lacks, every item it rests on, its counts and how sure it is; for Place each finding on the intents, capabilities and features it bears on (fn-place-findings).

## Rules & behavior
- The product owner says yes to each competitor followed. The reason: who the competition is, is a business judgment, and a name in a post may be a passing mention or another kind of product; one yes, and the rest runs on its own, as he asked: "This needs to be built for high autonomy."
- Only what was taken in. The reason: reading belongs to the first capability, through connections the product owner said yes to, and "We are never touching production."
- People's words, not facts about the rival. A finding says what people say a competitor does. The reason: the items are what consumers wrote, and the competitor's own word is not among them.
- Never from what the AI agent knows by itself. The reason: "a source in the project or in memory can be checked and read back, while the agent's own knowledge cannot."; what an agent knows of a rival may also be old.
- Every finding names its items, and a weak one is shown as weak. The reason: "Each finding says where it comes from. The reason: a person can then check each finding without a search."
- Memory first, then research through a memory update a person approves. The reason: "Do not guess. Draft the answer as a memory update, and a person approves or rejects it:"
- Not decided: whether a competitor's own public pages, such as its release notes or price list, may be read too. That would be a new kind of connection, which the first capability would set up through its one tool with the product owner's yes; until then only what people say is read.
- Not decided: how a competitor is told apart from a product people only mention.

## Acceptance criteria
- Given posts that name a rival app twenty times and a product owner who follows no competitor yet, when the items are understood, then the rival is proposed with the posts as its source, and no finding about it is drawn before his yes.
- Given a followed competitor, when its findings are drawn, then each says what people say it does and lists every item it rests on, quoted as taken in.
- Given a finding about a competitor that rests on one post, when it is shown, then it is marked weak.
- Given any run, when its findings are read, then none rests on anything but the items, and no tool, forum or page outside them was read.

## Out of scope
- Taking in what people say. Connect to what happens in use and in the market does it.
- Reading a competitor's own pages, until a person decides they become a kind of connection.
- Understanding what consumers want of this product. Understand what consumers want, from what is taken in (fn-understand-consumer-wants) does it.
- Placing a finding on the product. Place each finding on the intents, capabilities and features it bears on (fn-place-findings) does it.
- Deciding what to build in answer to a competitor. The third capability of Run → Product does it.

## Sources
- The product owner on 2026-11-10, in .garura/project/issues/1021/context/bi-6-capability-2/page-approvals.md, spelling tidied: "start understanding what it is that the consumers want and what the competition is doing", "This needs to be built for high autonomy."
- The product owner on 2026-11-10, in .garura/project/issues/1021/context/bi-6-capability-1/page-approvals.md: "We are never touching production.", "one Garura tool reads the settings and reaches each connection, and can later read what a listener outside Garura reports"
- The list the product owner set on 2026-11-10, in .garura/project/issues/1021/context/capabilities.md: "Understand what consumers want and what the competition is doing."
- .garura/product/product-os/software-delivery-planning/connect-use-and-market/fn-take-in-what-people-say/feature.md: "about the product, its kind of product and the products it competes with", "a forum thread where cooks compare it with a rival app's shopping list"
- .garura/product/product-os/software-delivery-planning/connect-use-and-market/capability.md: "Never: make a choice from what the AI agent knows by itself. The reason: a source in the project or in memory can be checked and read back, while the agent's own knowledge cannot."
- .garura/product/product-os/software-delivery-planning/keep-spec-matched/fn-find-spec-drift/feature.md: "Each finding says where it comes from. The reason: a person can then check each finding without a search."
- core/components/skills/research-domain-context/SKILL.md: "Search the web for market data, competitive landscape, industry trends, regulatory context", "Write domain-context.md to the specified STM path"
- core/tools/memory/GUIDE.md: "Do not guess. Draft the answer as a memory update, and a person approves or rejects it:"
