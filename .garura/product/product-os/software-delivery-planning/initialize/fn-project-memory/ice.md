## Intent
- Goal: After the answers are confirmed, with Phoenix memory reachable, the project's Garura memory holds only the memory blocks the answers call for, each built from the relevant part of Phoenix memory, written for the project and never a copy of a whole Phoenix file, each part naming the Phoenix file and the part of it that it came from, and the product profile records each answer with the question it answers.
- Limit: Read Phoenix memory only through the memory tool, and record in the profile no answer the person did not give.
- Limit: Build nothing for an answer from what an agent knows by itself, and write nothing to the project's memory or the profile while Phoenix memory cannot be reached.
- Fails if: the project's memory holds a standard an answer rules out, such as a database standard for a project with no database.
- Fails if: the project's Garura memory holds a whole Phoenix file, or a part of Phoenix memory the answers did not select.
- Fails if: the profile holds an answer the product owner never gave or confirmed.
- Fails if: initialize writes project memory or the profile while Phoenix memory cannot be reached.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the confirmed answers in the run's short-term memory; what each answer's selection finds in Phoenix memory, with the sections of each file that speak to the answer; what the project's Garura memory already holds; and the product profile.
- Never read: any memory file by its path, and any ICE page.
- Persona: the product owner, who confirmed the answers and reads the record of what was built.
- Scope: In: building each block from its parts, naming where each part came from, the record of what was built and left out, and recording the answers in the product profile. Out: the questions, the review rule groups, the tracker types, how Phoenix memory reaches the machine, what may enter each memory tier, and a change to Phoenix memory under the blocks.

## Expectation
- Scenario: A shop's checkout service answers checkout, Java and no database. Phoenix memory's commerce knowledge also holds catalog, cart and orders. Initialize builds the project's memory from the checkout part of that file and from the Java standards, with nothing from catalog, cart or orders and no database standard. Each part names the Phoenix file and the section it came from, the record shows what was built and what was left out, and the product profile lists each answer with its question.
- Done means: Someone other than the one who ran Initialize compares the project's Garura memory with Phoenix memory and the answers, and finds no whole Phoenix file, no part the answers did not select, each part naming where it came from, and each answer in the profile with its question.
