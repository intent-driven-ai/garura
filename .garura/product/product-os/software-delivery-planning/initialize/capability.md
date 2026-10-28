# Capability: Initialize a project for Garura

## Benefit hypothesis
- Serves the product owner who has just installed Garura in a project, and every play that later reads the project's memory, runs its review or writes to its tracker. Today a project gets all of the memory and every review runs every rule, so a project with no database, no front end or no permissions still gets those standards and those findings, and a play can stop the first time the tracker lacks an issue type it files.
- We believe that when the product owner answers one short set of questions after the Garura install, the project gets only the memory and the review rules that fit it, and its tracker holds every issue type Garura files (Business Intent, Epic, Story, Bug, Chore, Spike). Business Intent is the one product-layer type among them: it holds a need the product meets, while the other five are work items. The value is fewer wrong findings, a smaller memory that fits the project, and no play that stops on a missing type.
- We will know it is true when each of these checks holds:
  - One play, `initialize`, asks the setup questions, and each question shows its choices and a proposed answer that names its source.
  - The project's Garura memory holds only the memory blocks its answers call for, built from those parts of Phoenix memory and never a copy of a whole Phoenix file, and the product profile records each answer with its question.
  - Two projects on one machine, initialized with different answers, hold different memory blocks taken from the one Phoenix memory.
  - A review in the project runs only the rule groups that fit it, and the review's record names each group it skipped.
  - The tracker holds each issue type Garura files, or a stand-in the product owner said yes to.
  - The product owner can run `initialize` again when the project or Phoenix memory changes, and the set-up follows the change.

## Boundary (In / Out / Never)
- Words this page uses. Phoenix memory is the one shared memory on a machine (the domain shelves, the standards, the templates) that every project on that machine draws from. A project's Garura memory is the project's own memory, read before Phoenix memory, which initialize writes for the first time; it is built from only the part of Phoenix memory the project needs and is never a copy of a Phoenix file. A memory block is the relevant part of Phoenix memory that one setup answer selects, down to the part of a file: for example only the checkout part of the commerce knowledge for a project that needs checkout and not the rest of commerce, the Java standards for a Java answer, or the React front-end standards for a React answer; a project gets a block only when its answers call for it.
- More words this page uses. The product profile is the project's record of its setup answers, kept in the project's product model, where every later play reads the facts about the project. A rule group is a set of the review's rules that check one kind of thing (for example front end, back-end service, database, running service, permissions or personal data); the review runs or skips a group as a whole. A stand-in is a type the tracker already has that the plays file a work item as when the tracker cannot make the type they need.
- In: asking the setup questions after the Garura install, setting up the project's Garura memory from the answers, recording which review rule groups fit the project, setting up the issue types Garura files in the tracker, and running all of this again when the project changes.
- In: giving each project its own memory blocks from the one Phoenix memory on the machine, and finding on each run whether the part of Phoenix memory a block was built from has changed, so a re-run can rebuild that part from Phoenix memory as it is now.
- These six jobs share one moment (the project is being set up) and one input (the product owner's answers), so they live in one capability.
- Out: laying Phoenix memory on the machine and bringing it up to date. The Phoenix install owns it: it runs once per machine and lays Phoenix memory from the Phoenix memory repository. Initialize only reads Phoenix memory, through the memory tool, and never writes it.
- Out: the Garura install, which runs once per project and lays only the pieces (the plays, agents, skills, tools and the memory tool) and no memory. Initialize starts where that install stops, so a project has no Garura memory of its own until initialize runs, and the two never write the same files.
- Out: running a review and deciding its findings (the review play, /check-change, owns it). Initialize only records which rule groups fit; the review reads that record and names what it skipped.
- Out: shaping, planning and filing work items (/shape-slice and /shape-plan own them). Initialize makes sure the tracker can hold their types; it files no work item itself. The change to the filing plays (/shape-plan and the plays that file work items) that makes them read the type mapping initialize records and stop with a message that points to initialize when a type is missing and not mapped is a later story of this business intent, not filed yet.
- Never: write an answer the product owner did not give or confirm. The answers are the person's; a proposed answer is only a proposal until the person accepts it.
- Never: propose an answer without naming its source. A proposal with no source hides a guess, and the person cannot judge it.
- Never: make an issue type in the tracker, or record a stand-in, before the product owner's typed yes. A tracker is an outside system, and a write there is visible to the whole team.
- Never: read memory except through the memory tool, and never write Phoenix memory or another project's memory. Phoenix memory is shared by every project on the machine, so a write there from one project would change the others.

## Guiding rules
- The questions are built from Phoenix memory, not written by hand. This keeps the question set in step with what memory actually holds: a domain, standard or tool that memory does not hold is never offered as a choice.
- The project's memory is built, never copied. Initialize reads Phoenix memory through the memory tool and writes into the project only the part each answer selects, down to the part of a file, and never a whole Phoenix file. A whole file brings context the project does not need (all of commerce for a project that needs only checkout), and the plays would read that context as if it fit the project. When Phoenix memory changes, a re-run rebuilds the relevant part from it; it does not copy the new file.
- Each question has choices and a proposed answer with its source. The product owner then confirms or corrects instead of researching each answer from nothing.
- One run sets up memory, review rules and tracker types from the same answers. A second set of questions for the tracker or the review would ask the person the same things twice.
- Every change initialize makes is recorded: the answers in the product profile, the memory blocks it set up with where each came from, the rule groups it chose, and the tracker types it made or mapped. A later run, a review or a play can then read what was decided without asking again.
- A run can be repeated at any time. A project changes (it gains a database, a web surface or a new tracker) and Phoenix memory changes (a new standard or template), and the set-up must follow both without a reinstall.
- When the memory tool cannot reach Phoenix memory, initialize stops and builds nothing, and says the Phoenix install must run on this machine. An empty answer there would look like "nothing fits" and leave the project with too little memory.

## Features
- Ask the setup questions (fn-setup-questions): asks the product owner the short set of questions built from Phoenix memory, each with choices and a proposed answer that names its source, and keeps the confirmed answers for the other features.
- Build the project's memory (fn-project-memory): sets up the project's Garura memory from only the memory blocks the answers call for, and records the answers in the product profile.
- Choose the review rule groups (fn-review-rule-groups): records which rule groups of the review fit the project, so a review runs only those and names the groups it skipped.
- Set up the tracker's work-item types (fn-881): finds the tracker the project uses and the types it has, makes each missing type after a typed yes, and records a stand-in, also after a typed yes, where a type cannot be made.
- Run initialize again (fn-rerun-initialize): lets the product owner run initialize again when the project changes, with the earlier answers proposed, so the set-up follows the project.
- Give each project its own memory blocks (fn-883): keeps each project's blocks its own, taken from the one Phoenix memory on the machine, and on each run compares them with Phoenix memory so the project learns when a block changed.

## Sources
- GitHub #862, "A project gets only the memory and the review rules that fit it: initialize asks after the install" (the business intent): "after the install, one play (`initialize`) asks the person a short set of questions built from Phoenix memory"; "each question has choices and a proposed answer with its source"; "a review in that project runs only the rule groups that fit it"; "a project can run `initialize` again when it changes".
- GitHub #881, "Initialize sets up the tracker's work-item types: Business Intent, Epic, Story, Bug, Chore and Spike" (the story): "`initialize` (this business intent) also sets up the tracker".
- GitHub #883, "All memory in Garura's source is Phoenix memory: one install lays it, initialize gives each project its own blocks" (the story, the product owner's rule): the Phoenix install, once per machine: "It lays Phoenix memory from the `phoenix-memory` repo"; the Garura install, once per project: "It lays only the pieces"; "It lays no memory."; `initialize`: "It asks the questions that decide which memory fits the project (for example Java or .NET, a React front end or none) and sets up the project's Garura memory from Phoenix memory. It can run again to bring changes in."
- ADR 039, Decision 4 (the memory tool never copies a Phoenix file): "The tool reads Phoenix memory. It does not copy a file from it into the project."; "A project's Garura memory is built separately, from only the part the project needs: by `initialize`, and by promotion." The product owner, in the same decision: "You don't need to copy the entire file. You only need to bring in the context which is relevant to the checkout part of the commerce ... It should not copy the file." The glossary row for Garura memory: "never a copy of a Phoenix file"; "NOT: a copy of Phoenix memory — checkout, not all of commerce."
- The product owner's answers (seed): "After the install, set a project up for Garura: its memory, its review rules, and its tracker's work-item types."
- Shelf: none. No knowledge shelf in memory covers setting up a software project; the domain page software-delivery-planning/domain.md carries its own outside sources.

## Agent intent (ICE)
- Goal: After the Garura install, one run of `initialize` sets the project up from the product owner's answers: its memory, its review rule groups and the issue types Garura files in its tracker.
- Goal: Every question shows its choices and a proposed answer that names its source.
- Goal: The project's Garura memory holds only the memory blocks of Phoenix memory the answers call for, each built from the relevant part and never a copy of a whole Phoenix file, and the product profile records the answers.
- Goal: Two projects on one machine with different answers hold different memory blocks, taken from the one Phoenix memory.
- Goal: The tracker has each issue type Garura files, or a recorded stand-in that the plays read.
- Limit: Never make a tracker type or a stand-in before the product owner's typed yes, and read memory only through the memory tool.
- Limit: Never write an answer the product owner did not give or confirm, and never write Phoenix memory or another project's memory.
- Fails if: a proposed answer names no source, or an answer is recorded that the person never gave.
- Fails if: a review in the project still runs a rule group the answers rule out, or its record does not name the groups it skipped.
- Fails if: after initialize ran, an issue type Garura files is neither in the tracker nor mapped to a stand-in the product owner said yes to, and the brief does not name it as missing.
- Fails if: initialize builds a project's memory while Phoenix memory cannot be reached.
- Fails if: a project's Garura memory holds a whole Phoenix file, or a part of Phoenix memory its answers did not select.
- Context: serves the product owner right after the Garura install and every later play that reads the project's memory, runs its review or files work items; touches Phoenix memory (read only), the project's Garura memory, the product profile and the tracker (GitHub first, then Jira and Linear through the same adapter); out are the Phoenix install, the Garura install, running the review, filing work items, and the change to the filing plays that makes them stop and point to initialize (a later story, not filed yet).
- Checked by: run `initialize` on a fresh test project, answer the questions, then check its memory folder (only the selected parts, and no whole Phoenix file), the product profile, a review record and the tracker's type list against the answers.
