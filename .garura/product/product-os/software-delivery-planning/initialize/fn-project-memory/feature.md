# Feature: Build the project's memory

## What it does
- Phoenix memory (a word this page uses) is the one shared memory on a machine (the domain shelves, the standards, the templates) that the Phoenix install laid and every project on that machine draws from.
- Garura memory (a word this page uses): the project's Garura memory is the project's own memory, kept in the project's own folders; the memory tool reads it before it reads Phoenix memory, so what the project holds is what its plays use; it is built from only the part of Phoenix memory the project needs and is never a copy of a Phoenix file.
- A memory block (a word this page uses) is the relevant part of Phoenix memory that one setup answer selects, down to the part of a file: for example only the checkout part of the commerce knowledge for a checkout answer, the Java standards for a Java answer, or the database standards for a database answer.
- A part (a word this page uses) is the piece of one Phoenix memory file that a block is built from: one section of the file, or all of its sections when every one speaks to the answer; either way the project's memory is built from it, never a copy of the file.
- The product profile (a word this page uses) is the project's lasting record of its setup answers, kept in the project's product model, where every later play reads the facts about the project.
- Runs after the product owner confirms the setup answers. It sets up the project's Garura memory from only the memory blocks those answers call for, so a project with no database, no front end or no permissions gets none of those standards.
- The Garura install lays no memory; this feature is where the project's Garura memory is first written. It reads Phoenix memory as it already is on the machine and builds the project's own memory from the part each answer selects; it never copies a Phoenix file into the project.
- It records the answers in the product profile, so every later play reads the same facts about the project without asking again.

## Inputs / Outputs
- In: the confirmed answers from Ask the setup questions (fn-setup-questions), read from the run's short-term memory (the working folder `initialize` keeps for the run): domains, kinds of features, technology standards, tools and frameworks, surfaces, and whether there is a database, personal data, permissions or a running service.
- In: Phoenix memory, read only through the memory tool, for the memory block of each answer.
- Out: the project's Garura memory, holding only the blocks the answers select, each built from the relevant part of Phoenix memory and never a copy of a whole Phoenix file. Each part names the Phoenix file and the part of it that it was built from, so a later run (Give each project its own memory blocks, fn-883) can compare it with Phoenix memory and find when it changed.
- Out: the answers recorded in the product profile, each with the question it answers.
- Out: a short record of what was built, shown to the product owner at the end of the run: which blocks were built and from which parts of which Phoenix files, and which blocks were left out because the answers rule them out.
- Out: when Phoenix memory cannot be reached, a plain message that says so and that the Phoenix install must run on this machine, and no project memory built.

## Rules & behavior
- Each answer selects its memory block, and only the part of Phoenix memory that belongs to the block of an answer the product owner gave is built into the project. The rest of Phoenix memory, including the rest of a file that a block takes one part of, stays in Phoenix memory, so the project's memory holds what fits and nothing else.
- Initialize never copies a Phoenix file. It reads the file through the memory tool and writes the project's own memory from the part the answer selects, because a whole file brings context the project does not need (all of commerce for a project that needs only checkout), and the plays would read that context as if it fit the project.
- How an answer is tied to its parts: each choice that Ask the setup questions (fn-setup-questions) offers is built from one named place in Phoenix memory: a standards folder (for example the Java standards for the Java choice, or the database standards for a database yes), one domain shelf, or one part of a shelf (for example the checkout part of the commerce knowledge for a checkout choice). That place is the block's selection.
- To build the block, initialize asks the memory tool for what the selection finds, reads it, and builds the project's memory from only the parts that speak to the answer, and from no others. The sources say what a block holds: only the part the project needs, never the whole file (ADR 039 Decision 4).
- An answer that names no place (for example database no) selects no block.
- A part that two selected blocks both need is built once and names both answers that selected it, so a later run that drops one of the two answers keeps it for the other.
- How a block is found, and how the part is cut from a file, are our default: a part is cut along the file's own sections (a heading and what is under it), and a section is kept when it speaks to the answer; the sources do not say how the part is cut.
- Every read goes through the memory tool, because every part of Garura reads memory that way and the tool is what records where each part came from. No part of initialize reads a memory file by its path.
- The profile records the answers as the person gave them, because later plays treat the profile as the product owner's own word. Initialize never adds an answer the person did not give, and a proposed answer the person did not accept is never written.
- When an answer selects nothing in Phoenix memory (for example a tool memory has no standard for), the record says so in plain words, and the project's memory is still built from the other answers. It goes on because one answer with no matching standard does not make the other answers wrong; this is unlike an unreachable Phoenix memory, where nothing read can be trusted. Our default; the sources do not say what happens then.
- When the memory tool cannot reach Phoenix memory (it says the tier is missing), initialize stops, says in plain words that Phoenix memory could not be reached and that the Phoenix install must run on this machine, and builds no project memory. An empty result here would look like "no file fits" and leave the project with too little memory. It never writes the profile's answers on their own either, so the project is never left half set up. Our default; the sources do not say what happens then.
- When a run is repeated (Run initialize again, fn-rerun-initialize), the memory is rebuilt from the new confirmed answers, and the profile's answers are replaced by the new confirmed answers, each still with its question. The record says which blocks and parts were added and which were taken out, so the product owner sees what the new answers changed before a later play relies on it.

## Acceptance criteria
- Given answers that say the project has no database, when the memory is built, then the project's Garura memory holds no database standard.
- Given a Java answer, when the memory is built, then the project's Garura memory holds the Java standards, built from what the memory tool lists for them, and no .NET standard.
- Given two answers whose blocks share one part, when the memory is built, then the project's Garura memory holds that part once and it names both answers.
- Given answers that select a domain and a set of standards, when the memory is built, then each part of those blocks is in the project's Garura memory and names the Phoenix file and the part of it that it was built from.
- Given a checkout answer and a commerce knowledge file in Phoenix memory that also holds catalog, cart and orders, when the memory is built, then the project's Garura memory holds the checkout part and none of the rest of that file.
- Given any confirmed answers, when the memory is built, then no file in the project's Garura memory is a copy of a whole Phoenix file.
- Given the confirmed answers, when the memory is built, then the product profile records each answer with its question.
- Given an answer that selects nothing in Phoenix memory, when the memory is built, then the record names that answer.
- Given an answer that selects nothing in Phoenix memory and other answers that do, when the memory is built, then the blocks of the other answers are in the project's Garura memory.
- Given the memory tool reports that Phoenix memory cannot be reached, when the memory is built, then no file is written to the project's Garura memory or the product profile.
- Given the memory tool reports that Phoenix memory cannot be reached, when the memory is built, then the message says the Phoenix install must run on this machine.
- Given a second run where the database answer changed from yes to no, when the memory is rebuilt, then the profile holds the new answer and the record names the database parts that were taken out.

## Out of scope
- Asking the questions and keeping the person's reply (Ask the setup questions, fn-setup-questions, owns it).
- Recording the review rule groups (Choose the review rule groups, fn-review-rule-groups, owns it).
- Laying Phoenix memory on the machine and bringing it up to date: the Phoenix install owns it, once per machine. This feature only reads what is already laid.
- Keeping each project's memory blocks its own and finding, on a later run, that Phoenix memory changed under them (Give each project its own memory blocks, fn-883, owns it).
- Stopping installed plays and tools from reading Garura's source folders: issue #860 owns it. This feature builds memory; it does not change how installed parts find files.
- Moving the memory tool's home to Phoenix and removing the machine-wide Garura memory folder: the business intent puts this after the memory tool is fully live, so this feature keeps today's folders.

## Sources
- GitHub #862: "the answers set up the project's Garura memory from only the part of Phoenix memory it needs, and the profile records them".
- GitHub #862, Rule 2: "Every part reads memory only through the memory tool."
- GitHub #862, Out of scope: "Moving the memory tool's home to Phoenix"; "later, once the memory tool is fully live"; "Installed parts reading the source tree (#860)".
- GitHub #883: "The Garura install, once per project."; "It lays no memory."; "sets up the project's Garura memory from Phoenix memory"; "with only the blocks its answers call for".
- ADR 039, Decision 4 (the memory tool never copies a Phoenix file): "The tool reads Phoenix memory. It does not copy a file from it into the project."; "A project's Garura memory is built separately, from only the part the project needs: by `initialize`, and by promotion." The product owner, in the same decision: "You don't need to copy the entire file. You only need to bring in the context which is relevant to the checkout part of the commerce ... It should not copy the file." The glossary row for Garura memory: "never a copy of a Phoenix file"; "NOT: a copy of Phoenix memory — checkout, not all of commerce."
- Shelf: none; no knowledge shelf in memory covers setting up a software project.

## Agent intent (ICE)
- Goal: After the answers are confirmed, the project's Garura memory holds only the memory blocks the answers call for, each built from the relevant part of Phoenix memory and never a copy of a whole Phoenix file, each part naming the Phoenix file and the part of it that it came from.
- Goal: The product profile records each answer with the question it answers.
- Limit: Read Phoenix memory only through the memory tool, and record in the profile no answer the person did not give.
- Fails if: the project's memory holds a standard an answer rules out, such as a database standard for a project with no database.
- Fails if: the project's Garura memory holds a whole Phoenix file, or a part of Phoenix memory the answers did not select.
- Fails if: the profile holds an answer the product owner never gave or confirmed.
- Fails if: initialize writes project memory or the profile while Phoenix memory cannot be reached.
- Context: serves the product owner and every later play that reads the project's memory; reads the confirmed answers and Phoenix memory; out are the questions, the review rule groups, laying Phoenix memory (the Phoenix install) and the memory tool's move to Phoenix.
- Checked by: run `initialize` on a test project with no database, then check that its Garura memory holds no database standard and no whole Phoenix file, and that the product profile lists each answer.
