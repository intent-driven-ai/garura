# Feature: Build the project's memory

## What it does
- Words this page uses. Phoenix memory is the one shared memory on a machine (the domain shelves, the standards, the templates) that the Phoenix install laid and every project on that machine draws from. The project's Garura memory is the project's own memory, kept in the project's own folders; the memory tool reads it before it reads Phoenix memory, so what the project holds is what its plays use. A memory block is the set of Phoenix memory files that one setup answer selects: for example the Java standards for a Java answer, the database standards for a database answer, or one domain shelf for a domain answer. The product profile is the project's lasting record of its setup answers, kept in the project's product model, where every later play reads the facts about the project.
- Runs after the product owner confirms the setup answers. It sets up the project's Garura memory from only the memory blocks those answers call for, so a project with no database, no front end or no permissions gets none of those standards.
- The Garura install lays no memory; this feature is where the project's Garura memory is first written. It takes the files from Phoenix memory as it already is on the machine.
- It records the answers in the product profile, so every later play reads the same facts about the project without asking again.

## Inputs / Outputs
- In: the confirmed answers from Ask the setup questions (fn-setup-questions), read from the run's short-term memory (the working folder `initialize` keeps for the run): domains, kinds of features, technology standards, tools and frameworks, surfaces, and whether there is a database, personal data, permissions or a running service.
- In: Phoenix memory, read only through the memory tool, for the memory block of each answer.
- Out: the project's Garura memory, holding only the files of the blocks the answers select. Each file names where it came from in Phoenix memory, so a later run (Give each project its own memory blocks, fn-883) can compare it with Phoenix memory and find when it changed.
- Out: the answers recorded in the product profile, each with the question it answers.
- Out: a short record of what was built, shown to the product owner at the end of the run: which blocks and files were taken, and which blocks were left out because the answers rule them out.
- Out: when Phoenix memory cannot be reached, a plain message that says so and that the Phoenix install must run on this machine, and no project memory built.

## Rules & behavior
- Each answer selects its memory block, and a file is taken only when it belongs to the block of an answer the product owner gave. A file in no selected block stays in Phoenix memory, so the project's memory holds what fits and nothing else.
- How an answer is tied to its files. Each choice that Ask the setup questions (fn-setup-questions) offers is built from one named place in Phoenix memory: a standards folder (for example the Java standards for the Java choice, or the database standards for a database yes) or one domain shelf (for a domain choice). That place is the block's selection, and the block of the answer is every file the memory tool finds in that place when the memory is built. So a builder ties an answer to its files by one step: ask the memory tool for the files in the place its choice names, and take those and no others. An answer that names no place (for example database no) selects no block. A file that sits in two selected blocks is taken once and names both answers that selected it, so the project holds one copy and a later run that drops one of the two answers keeps the file for the other. Our default; the sources say "blocks" and give the Java, .NET and React examples, but do not say how a block is found.
- Every read goes through the memory tool, because every part of Garura reads memory that way and the tool is what records where each file came from. No part of initialize reads a memory file by its path.
- The profile records the answers as the person gave them, because later plays treat the profile as the product owner's own word. Initialize never adds an answer the person did not give, and a proposed answer the person did not accept is never written.
- When an answer selects nothing in Phoenix memory (for example a tool memory has no standard for), the record says so in plain words, and the project's memory is still built from the other answers. It goes on because one answer with no matching standard does not make the other answers wrong; this is unlike an unreachable Phoenix memory, where nothing read can be trusted. Our default; the sources do not say what happens then.
- When the memory tool cannot reach Phoenix memory (it says the tier is missing), initialize stops, says in plain words that Phoenix memory could not be reached and that the Phoenix install must run on this machine, and builds no project memory. An empty result here would look like "no file fits" and leave the project with too little memory. It never writes the profile's answers on their own either, so the project is never left half set up. Our default; the sources do not say what happens then.
- When a run is repeated (Run initialize again, fn-rerun-initialize), the memory is rebuilt from the new confirmed answers, and the profile's answers are replaced by the new confirmed answers, each still with its question. The record says which blocks and files were added and which were taken out, so the product owner sees what the new answers changed before a later play relies on it.

## Acceptance criteria
- Given answers that say the project has no database, when the memory is built, then the project's Garura memory holds no database standard.
- Given a Java answer, when the memory is built, then every file the memory tool lists for the Java standards is in the project's Garura memory and no .NET standard is.
- Given two answers whose blocks share one file, when the memory is built, then the project's Garura memory holds that file once and it names both answers.
- Given answers that select a domain and a set of standards, when the memory is built, then each file of those blocks is in the project's Garura memory and names where it came from in Phoenix memory.
- Given the confirmed answers, when the memory is built, then the product profile records each answer with its question.
- Given an answer that selects nothing in Phoenix memory, when the memory is built, then the record names that answer.
- Given an answer that selects nothing in Phoenix memory and other answers that do, when the memory is built, then the blocks of the other answers are in the project's Garura memory.
- Given the memory tool reports that Phoenix memory cannot be reached, when the memory is built, then no file is written to the project's Garura memory or the product profile.
- Given the memory tool reports that Phoenix memory cannot be reached, when the memory is built, then the message says the Phoenix install must run on this machine.
- Given a second run where the database answer changed from yes to no, when the memory is rebuilt, then the profile holds the new answer and the record names the database files that were taken out.

## Out of scope
- Asking the questions and keeping the person's reply (Ask the setup questions, fn-setup-questions, owns it).
- Recording the review rule groups (Choose the review rule groups, fn-review-rule-groups, owns it).
- Laying Phoenix memory on the machine and bringing it up to date: the Phoenix install owns it, once per machine. This feature only takes from what is already laid.
- Keeping each project's memory blocks its own and finding, on a later run, that Phoenix memory changed under them (Give each project its own memory blocks, fn-883, owns it).
- Stopping installed plays and tools from reading Garura's source folders: issue #860 owns it. This feature builds memory; it does not change how installed parts find files.
- Moving the memory tool's home to Phoenix and removing the machine-wide Garura memory folder: the business intent puts this after the memory tool is fully live, so this feature keeps today's folders.

## Sources
- GitHub #862: "the answers set up the project's Garura memory from only the part of Phoenix memory it needs, and the profile records them".
- GitHub #862, Rule 2: "Every part reads memory only through the memory tool."
- GitHub #862, Out of scope: "Moving the memory tool's home to Phoenix"; "later, once the memory tool is fully live"; "Installed parts reading the source tree (#860)".
- GitHub #883: "The Garura install, once per project."; "It lays no memory."; "sets up the project's Garura memory from Phoenix memory"; "with only the blocks its answers call for".
- Shelf: none; no knowledge shelf in memory covers setting up a software project.

## Agent intent (ICE)
- Goal: After the answers are confirmed, the project's Garura memory holds only the memory blocks the answers call for, each file naming where it came from in Phoenix memory.
- Goal: The product profile records each answer with the question it answers.
- Limit: Read Phoenix memory only through the memory tool, and record in the profile no answer the person did not give.
- Fails if: the project's memory holds a standard an answer rules out, such as a database standard for a project with no database.
- Fails if: the profile holds an answer the product owner never gave or confirmed.
- Fails if: initialize writes project memory or the profile while Phoenix memory cannot be reached.
- Context: serves the product owner and every later play that reads the project's memory; reads the confirmed answers and Phoenix memory; out are the questions, the review rule groups, laying Phoenix memory (the Phoenix install) and the memory tool's move to Phoenix.
- Checked by: run `initialize` on a test project with no database, then check that its Garura memory holds no database standard and that the product profile lists each answer.
