Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: When the product owner wants the project to learn from use and the market, the connections the project should have, its web analytics, product analytics, user feedback tools and forums, are proposed from what the project's code and memory already name and from the product owner's word, each with its source; each one the product owner says yes to is recorded in the project's settings with its name, what it is read for, what part of it is read and where its key is kept; and each is proven by a first read that changes nothing, so every later read runs only on a connection a person chose.
- Limit: No connection is recorded or used without the product owner's yes, and the settings name only where each key is kept, never its value.
- Limit: The first read, and every step of this feature, writes nothing to any tool or forum.
- Limit: What is proposed comes from the project's code and memory, then Garura memory, then Phoenix memory, and from research only through a memory update a person approves; plays, skills and sub-agents never name a tool or forum.
- Fails if: A connection was recorded or used without the product owner's yes, or a connection that its first read could not reach was used.
- Fails if: A key's value is found in the settings, a record or a log.
- Fails if: A connected tool or forum shows a change made while connecting.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the analytics and feedback tools the product's code and settings already name, the connections the settings already record, the product's declared surfaces, where the deployment design keeps secrets, the product profile's privacy level and compliance needs, and the product owner's choices of tools, forums and topics.
- Never read: the value of any key, except at the moment the first read takes it from where it is kept, and it is never written down; anything in production other than through the tools the team already uses to look at it; and any ICE page.
- Persona: the product owner, who chooses what the project reads and says yes to each connection.
- Scope: In: proposing the connections, recording each approved one by name with where its key is kept, and proving it with a first read. Out: reading use and what people say, updating the connections, deciding where secrets are kept, and changing the product.

## Expectation
- Scenario: A clinic's booking app sends patients' messages to a feedback tool, and its code loads a product analytics tool. Both are proposed, each with the file that names it; the product owner adds a forum where clinics compare booking apps, limited to that topic. He says yes to the three. The settings name each, what it is read for and where its key is kept. The first read reaches the analytics tool and the forum; the feedback tool refuses the key, so it is named as not reading, with the reason, and no read uses it.
- Done means: Someone other than the one who set up the connections reads the settings and the record of the first reads, and finds each connection approved by the product owner with its source, no key's value anywhere, each connection either read or named with its reason, and no change made in any tool or forum.
