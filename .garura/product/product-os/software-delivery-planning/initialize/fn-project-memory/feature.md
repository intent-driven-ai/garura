# Feature: Build the project's memory

## What it does
Once the product owner has confirmed the setup answers, Initialize builds the project's own Garura memory from only the memory blocks those answers call for, each built from the relevant part of Phoenix memory and never a copy of a Phoenix file, and records the answers in the product profile, so a project with no database, no front end or no permissions gets none of those standards.
- Words this page uses. Phoenix memory is the one shared memory on a machine (the domain shelves, the standards, the templates) that every project on that machine draws from. The project's Garura memory is the project's own memory, kept in the project's own folders; the memory tool reads it before it reads Phoenix memory, so what the project holds is what its plays use. A memory block is the relevant part of Phoenix memory that one setup answer selects, down to the part of a file: for example only the checkout part of the commerce knowledge for a checkout answer, the Java standards for a Java answer, or the database standards for a database answer. A part is what a block takes from one Phoenix memory file: the sections of that file that speak to the answer, as initialize reads them through the memory tool. The project's memory is built from a part; a part is never taken into the project as it is. The product profile is the record of the product's shape and the quality levels it commits to, kept in the project's product model, where every later play reads the facts about the project.
- The Garura install lays no memory; this feature is where the project's Garura memory is first written. It reads Phoenix memory as it already is on the machine and builds the project's own memory from the part each answer selects; it never copies a Phoenix file into the project.
- It records the answers in the product profile, so every later play reads the same facts about the project without asking again.
- What may enter Garura memory, and how a learning is promoted, are Memory's rules; this feature follows them and builds only from the answers.
- Examples, in different kinds of project:
  - A shop's checkout service answers checkout and Java: its memory holds what was built from the checkout part of the commerce knowledge and from the Java standards, and nothing built from catalog, cart or orders.
  - A school's timetable app answers no database: its memory holds no database standard.
  - A bank's payments service answers a database and personal data: its memory holds what was built from the database standards and the personal-data parts, each naming the Phoenix file and the part it came from.
- How it meets the capability: the capability's second check, "The project's Garura memory holds only the memory blocks its answers call for", is met here.

Status: not built. The memory tool reads Phoenix memory, but "the tool has no command that writes Garura or Phoenix memory", and nothing builds Garura memory from Phoenix memory. ADR 039 leaves open "how `initialize` builds a project's Garura memory from the part it needs". The product profile has no place for the answers: it holds the product's shape, its quality levels and its compliance needs.

## Inputs / Outputs
- In: the confirmed answers from Ask the setup questions (fn-setup-questions), read from the run's short-term memory (the working folder initialize keeps for the run): domains, kinds of features, technology standards, tools and frameworks, surfaces, and whether there is a database, personal data, permissions or a running service.
- In: Phoenix memory, read only through the memory tool, for the memory block of each answer.
- Out: the project's Garura memory, holding only the blocks the answers select, each built from the relevant part of Phoenix memory, written for the project and never a copy of a whole Phoenix file. Each part names the Phoenix file and the part of it that it was built from, so a later run (Update each project's own memory as Phoenix memory changes, fn-883) can compare it with Phoenix memory and find when it changed.
- Out: the answers recorded in the product profile, each with the question it answers.
- Out: a short record of what was built, shown to the product owner at the end of the run: which blocks were built and from which parts of which Phoenix files, and which blocks were left out because the answers rule them out.
- Out: when Phoenix memory cannot be reached, a plain message that says so, and no project memory built.

## Rules & behavior
- Each answer selects its memory block, and only the part of Phoenix memory that belongs to the block of an answer the product owner gave is built into the project. The rest of Phoenix memory, including the rest of a file that a block takes one part of, stays in Phoenix memory, so the project's memory holds what fits and nothing else.
- Initialize never takes a whole Phoenix file into the project, even when every section of it speaks to the answer: it reads the file through the memory tool and builds the project's own memory from what it read, written for the project and never a copy. This is the product owner's rule (review of PR #886, round 2), beside ADR 039 Decision 4. A whole file brings context the project does not need (all of commerce for a project that needs only checkout), and the plays would read that context as if it fit the project.
- How an answer is tied to its parts: each choice that Ask the setup questions (fn-setup-questions) offers is built from one named place in Phoenix memory: a standards folder (for example the Java standards for the Java choice, or the database standards for a database yes), one domain shelf, or one part of a shelf (for example the checkout part of the commerce knowledge for a checkout choice). That place is the block's selection: where initialize looks, never what it takes into the project.
- To build the block, initialize asks the memory tool for what the selection finds, reads it, and builds the project's memory from what it read in only the parts that speak to the answer, and from no others.
- Not decided: how a part is found inside a Phoenix file, and how the project's memory is written from it. ADR 039 leaves it open.
- An answer that names no place (for example database no) selects no block.
- A part that two selected blocks both need is built once and names both answers that selected it, so a later run that drops one of the two answers keeps it for the other.
- Every read goes through the memory tool, because every part of Garura reads memory that way and the tool is what records where each part came from. No part of initialize reads a memory file by its path. The reason: #862's rule, "Every part reads memory only through the memory tool."
- The profile records the answers as the person gave them, because later plays treat the profile as the product owner's own word. Initialize never adds an answer the person did not give, and a proposed answer the person did not accept is never written.
- Not decided: where in the product profile the answers sit. Its shape has no place for them today, and Product model defines it.
- When an answer selects nothing in Phoenix memory (for example a tool memory has no standard for), the record says so in plain words, and the project's memory is still built from the other answers. Nothing is built for it from what an agent knows by itself. It goes on because one answer with no matching standard does not make the other answers wrong; this is unlike an unreachable Phoenix memory, where nothing read can be trusted.
- When the memory tool cannot reach Phoenix memory (it says the tier is missing), initialize stops, says in plain words that Phoenix memory could not be reached, and builds no project memory. An empty result here would look like "no file fits" and leave the project with too little memory. It never writes the profile's answers on their own either, so the project is never left half set up. The reason: "`tier_missing` means a tier cannot be reached. Say so."
- When a run is repeated (Update the setup as the project changes, fn-rerun-initialize), the memory is rebuilt from the new confirmed answers, and the profile's answers are replaced by the new confirmed answers, each still with its question. The record says which blocks and parts were added and which were taken out, so the product owner sees what the new answers changed before a later play relies on it.

## Acceptance criteria
- Given answers that say the project has no database, when the memory is built, then the project's Garura memory holds no database standard.
- Given a Java answer, when the memory is built, then the project's Garura memory holds the Java standards, built from the files the memory tool lists for them and not a copy of any of those files, and no .NET standard.
- Given a checkout answer and a commerce knowledge file in Phoenix memory that also holds catalog, cart and orders, when the memory is built, then the project's Garura memory holds what was built from the checkout part and nothing built from the rest of that file.
- Given any confirmed answers, including a Java answer and a Phoenix standards file whose every section speaks to Java, when the memory is built, then no file in the project's Garura memory is a copy of a whole Phoenix file.
- Given answers that select a domain and a set of standards, when the memory is built, then each part built names the Phoenix file and the part of it that it was built from.
- Given two answers whose blocks share one part, when the memory is built, then the project's Garura memory holds what was built from that part once, and it names both answers.
- Given the confirmed answers, when the memory is built, then the product profile records each answer with its question.
- Given an answer that selects nothing in Phoenix memory and other answers that do, when the memory is built, then the record names that answer and the blocks of the other answers are in the project's Garura memory.
- Given the memory tool reports that Phoenix memory cannot be reached, when the memory is built, then no file is written to the project's Garura memory or the product profile, and the message says Phoenix memory could not be reached.
- Given a second run where the database answer changed from yes to no, when the memory is rebuilt, then the profile holds the new answer and the record names the database parts that were taken out.

## Out of scope
- Asking the questions and keeping the person's reply (Ask the setup questions, fn-setup-questions, owns it).
- Recording the review rule groups (Choose the review rule groups, fn-review-rule-groups, owns it).
- Keeping each project's memory blocks its own and finding, on a later run, that Phoenix memory changed under them (Update each project's own memory as Phoenix memory changes, fn-883, owns it).
- How Phoenix memory reaches the machine and is brought up to date, what may enter each memory tier, promotion, and moving the memory tool's home and the machine-wide copy of memory: Memory, in Standards, structure, settings and memory, owns them. This feature only reads what Phoenix memory holds.
- Where the answers sit in the product profile's shape: Product model owns it.

## Sources
- GitHub #862 (open): "the answers set up the project's Garura memory from only the part of Phoenix memory it needs, and the profile records them"
- GitHub #862, Rule 2: "Every part reads memory only through the memory tool."
- GitHub #883 (open): "It lays no memory."; "sets up the project's Garura memory from Phoenix memory"; "with only the blocks its answers call for"
- GitHub PR #886, the product owner's verdict in round 2 of its review: "The product owner's rule: never take the whole file; read it, and build the project's memory."
- docs/adr/039-memory-writes-go-to-short-term-memory-plays-read-no-memory.md, Decision 4 (the memory tool never copies a Phoenix file): "The tool reads Phoenix memory. It does not copy a file from it into the project."; "A project's Garura memory is built separately, from only the part the project needs: by `initialize`, and by promotion." The product owner, in the same decision: "You don't need to copy the entire file. You only need to bring in the context which is relevant to the checkout part of the commerce", "It should not copy the file."; and, not decided there: "how `initialize` builds a project's Garura memory from the part it needs"
- core/grounding/glossary.md, the row for Garura memory: "never a copy of a Phoenix file"; "NOT: a copy of Phoenix memory — checkout, not all of commerce."
- core/tools/memory/contract/v5.json: "the tool has no command that writes Garura or Phoenix memory"
- core/tools/memory/GUIDE.md: "`tier_missing` means a tier cannot be reached. Say so."
- .garura/product/product-os/software-delivery-planning/initialize/capability.md: "The project's Garura memory holds only the memory blocks its answers call for"
- Shelf: none; no knowledge shelf in memory covers setting up a software project.
