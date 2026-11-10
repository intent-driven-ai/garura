Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: Once a user feedback tool or a forum is connected, what users write to the team and what people say in that forum about the product, its kind of product and the products it competes with are read, on their own as the project's settings say, and each message or post is kept in its own words, with its connection, where it was, when it was written and when it was read, with every person's name and personal details taken out, and each connection not read is named with the reason, so that what consumers want and what the competition is doing can be understood from people's own words.
- Limit: It reads only through the connected tool or forum and only the places and topics its connection names; it never posts, replies, votes, tags or changes anything there, and never reads production.
- Limit: A person's name, handle, contact details and anything else that points to one person are taken out, from the words too, before anything is kept.
- Limit: Nothing is summed up, sorted into themes or placed on an intent here, and nothing is made up for a read that failed.
- Fails if: A message or post kept differs in its words from what was written, or has no connection, place or dates.
- Fails if: A person's name, handle or contact details, or anything else that points to one person, is found in what was kept, a record or a log.
- Fails if: The tool or the forum shows a post, reply, vote, tag or change made by a read, or a post from a place or topic the connection does not name was kept.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the connected feedback tools and forums, the places and topics each names and where its key is kept, the project's setting for when the reads run, the product profile's privacy level and compliance needs, and the records of earlier reads.
- Never read: the value of any key, except at the moment a read takes it from where it is kept, and it is never written down; production and the product's own stores of data; a forum or topic the connection does not name; and any ICE page.
- Persona: the product owner, who wants what consumers want and what the competition is doing understood from people's own words.
- Scope: In: reading each connected feedback tool and forum, keeping each message or post in its own words with where and when and with no person's details, and naming each failed read. Out: connecting the tools, reading how the product is used, understanding what people want or what rivals do, answering anyone, and fixing defects.

## Expectation
- Scenario: A recipe app has its feedback tool and one forum's threads on recipe apps connected. The read keeps a user's message asking for a shopping list that groups items by shop aisle, with its date, but not the user's name or email address, which the message also held in its words. From the forum it keeps a post comparing the app with a rival's shopping list, with its link and date, and not the writer's handle. A thread on cooking holidays in the same forum is not kept, because the connection names only recipe apps. Nothing is posted or voted on.
- Done means: Someone other than the one who set up the read compares what was kept with the tool and the forum, and finds every message and post in its own words with its connection, place and dates, no name, handle or contact details anywhere, nothing from a place or topic the connection does not name, every failed read named, and no change in the tool or the forum.
