## Intent
- Goal: After the install, with Phoenix memory reachable, Initialize shows the product owner one brief of questions built from Phoenix memory, covering domains, kinds of features, standards, tools and frameworks, surfaces, and database, personal data, permissions and running service, each with its choices and a proposed answer that names its source, or no proposal when nothing backs one, and keeps each answer the product owner gives or confirms with its question in the run's short-term memory, handed on for the product profile.
- Limit: Read Phoenix memory only through the memory tool, and offer no choice that memory does not hold.
- Limit: Take each proposal from the project's own code and memory first, then Garura memory, then Phoenix memory, and never from what an agent knows by itself.
- Limit: Record as an answer only what the product owner gave or confirmed.
- Fails if: a proposed answer names no source, or a default stands in for a missing source.
- Fails if: an answer is recorded that the product owner never gave or confirmed.
- Fails if: initialize asks questions while Phoenix memory cannot be reached, or stops without saying that Phoenix memory could not be reached.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: what Phoenix memory holds for each question's choices (its domain shelves, technology standards, tools and frameworks, and the review's rules); the project's files and settings that show an answer, such as its package files, its schema folder, its route files and its screens; and, on a later run, the earlier answers in the product profile.
- Never read: any memory file by its path, and any ICE page.
- Persona: the product owner, who sets the project up right after the install and answers the setup questions.
- Scope: In: building the questions from Phoenix memory, each proposal with its source, the one brief, and keeping the answers. Out: building the memory, the rule groups, the tracker types, proposing the earlier answers on a later run, and how Phoenix memory reaches the machine.

## Expectation
- Scenario: A clinic's booking app has just had the install. The product owner starts Initialize. One brief asks about the domains, the kinds of features, the standards, the tools and frameworks, the surfaces and whether there is a database, personal data, permissions or a running service. The React proposal names the project's package file, the database proposal names its schema folder, and the permissions question carries no proposal because nothing in the project shows it. The product owner corrects the domain to one Phoenix memory holds no shelf for and leaves permissions blank; Initialize keeps the corrected answer with a note that no memory can be set up for it, keeps every other answer, and asks again only about permissions.
- Done means: Someone other than the one who ran Initialize compares the brief and the kept answers with the reply, and finds every choice held in Phoenix memory, every proposal naming its source or none, and every kept answer one the product owner gave or confirmed.
