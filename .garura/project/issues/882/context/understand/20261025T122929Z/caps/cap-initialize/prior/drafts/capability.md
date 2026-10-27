# Capability: Initialize a project for Garura

## Benefit hypothesis
- Serves the product owner who has just installed Garura in a project, and every play that later reads the project's memory, runs its review or writes to its tracker. Today a project gets all of the memory and every review runs every rule, so a project with no database, no front end or no permissions still gets those standards and those findings, and a play can stop the first time the tracker lacks a work-item type it files.
- We believe that when the product owner answers one short set of questions after the Garura install, the project gets only the memory and the review rules that fit it, and its tracker holds every work-item type the plays file (Business Intent, Epic, Story, Bug, Chore, Spike). The value is fewer wrong findings, a smaller memory that fits the project, and no play that stops on a missing type.
- We will know it is true when: one play (`initialize`) asks the questions, each with choices and a proposed answer that names its source; the answers set up the project's Garura memory from only the memory blocks of Phoenix memory it needs, and the profile records them; two projects on one machine with different answers hold different blocks; a review in the project runs only the rule groups that fit and its record names the groups it skipped; the tracker has each needed type or a named stand-in; and the product owner can run `initialize` again when the project or Phoenix memory changes.

## Boundary (In / Out / Never)
- Two words this page uses. Phoenix memory is the one shared memory on a machine (the domain shelves, the standards, the templates) that every project draws from. A memory block is the set of Phoenix memory files that one setup answer selects, for example the Java standards for a Java answer, the React front-end standards for a React answer, or one domain shelf; a project gets a block only when its answers call for it.
- A rule group is a set of the review's rules that check one kind of thing (for example front end, back-end service, database, running service, permissions or personal data); the review runs or skips a group as a whole.
- In: asking the setup questions after the Garura install, setting up the project's Garura memory from the answers, recording which review rule groups fit the project, setting up the tracker's work-item types, and running all of this again when the project changes.
- In: giving each project its own memory blocks from the one Phoenix memory on the machine, and finding on each run whether Phoenix memory changed under the blocks a project holds, so the project can take the change in.
- These six jobs share one moment (the project is being set up) and one input (the product owner's answers), so they live in one capability.
- Out: laying Phoenix memory on the machine and bringing it up to date. The Phoenix install owns it: it runs once per machine and lays Phoenix memory from the Phoenix memory repository. Initialize only reads Phoenix memory, through the memory tool, and never writes it.
- Out: the Garura install, which runs once per project and lays only the pieces (the plays, agents, skills, tools and the memory tool) and no memory. Initialize starts where that install stops, so a project has no Garura memory of its own until initialize runs, and the two never write the same files.
- Out: running a review and deciding its findings (the review play, /check-change, owns it). Initialize only records which rule groups fit; the review reads that record and names what it skipped.
- Out: shaping, planning and filing work items (/shape-slice and /shape-plan own them). Initialize makes sure the tracker can hold their types; it files no work item itself.
- Never: write an answer the product owner did not give or confirm. The answers are the person's; a proposed answer is only a proposal until the person accepts it.
- Never: propose an answer without naming its source. A proposal with no source hides a guess, and the person cannot judge it.
- Never: make a work-item type in the tracker before the product owner's typed yes. A tracker is an outside system, and a write there is visible to the whole team.
- Never: read memory except through the memory tool, and never write Phoenix memory or another project's memory. Phoenix memory is shared by every project on the machine, so a write there from one project would change the others.

## Guiding rules
- The questions are built from Phoenix memory, not written by hand. This keeps the question set in step with what memory actually holds: a domain, standard or tool that memory does not hold is never offered as a choice.
- Each question has choices and a proposed answer with its source. The product owner then confirms or corrects instead of researching each answer from nothing.
- One run sets up memory, review rules and tracker types from the same answers. A second set of questions for the tracker or the review would ask the person the same things twice.
- Every change initialize makes is recorded: the answers in the profile, the memory blocks it set up with where each came from, the rule groups it chose, and the tracker types it made or mapped. A later run, a review or a play can then read what was decided without asking again.
- A run can be repeated at any time. A project changes (it gains a database, a web surface or a new tracker) and Phoenix memory changes (a new standard or template), and the set-up must follow both without a reinstall.
- When the memory tool cannot reach Phoenix memory, initialize stops and builds nothing, and says the Phoenix install must run on this machine. An empty answer there would look like "nothing fits" and leave the project with too little memory.

## Features
- Ask the setup questions (fn-setup-questions): asks the product owner the short set of questions built from Phoenix memory, each with choices and a proposed answer that names its source, and records the answers.
- Build the project's memory (fn-project-memory): sets up the project's Garura memory from only the memory files the answers call for, and records the answers in the profile.
- Choose the review rule groups (fn-review-rule-groups): records which rule groups of the review fit the project, so a review runs only those and names the groups it skipped.
- Set up the tracker's work-item types (fn-881): finds the tracker the project uses and the types it has, makes each missing type after a typed yes, and records a stand-in, also after a typed yes, where a type cannot be made.
- Run initialize again (fn-rerun-initialize): lets the product owner run initialize again when the project changes, with the earlier answers proposed, so the set-up follows the project.
- Give each project its own memory blocks (fn-883): keeps each project's blocks its own, taken from the one Phoenix memory on the machine, and on each run compares them with Phoenix memory so the project learns when a block changed.

## Sources
- GitHub #862, "A project gets only the memory and the review rules that fit it: initialize asks after the install" (the business intent): "after the install, one play (`initialize`) asks the person a short set of questions built from Phoenix memory"; "each question has choices and a proposed answer with its source"; "a review in that project runs only the rule groups that fit it"; "a project can run `initialize` again when it changes".
- GitHub #881, "Initialize sets up the tracker's work-item types: Business Intent, Epic, Story, Bug, Chore and Spike" (the story): "`initialize` (this business intent) also sets up the tracker".
- GitHub #883, "All memory in Garura's source is Phoenix memory: one install lays it, initialize gives each project its own blocks" (the story, the product owner's rule): the Phoenix install, once per machine: "It lays Phoenix memory from the `phoenix-memory` repo"; the Garura install, once per project: "It lays only the pieces"; "It lays no memory."; `initialize`: "It asks the questions that decide which memory fits the project (for example Java or .NET, a React front end or none) and sets up the project's Garura memory from Phoenix memory. It can run again to bring changes in."
- The product owner's answers (seed): "After the install, set a project up for Garura: its memory, its review rules, and its tracker's work-item types."
- Shelf: none. No knowledge shelf in memory covers setting up a software project; the domain page software-delivery-planning/domain.md carries its own outside sources.

## Agent intent (ICE)
- Goal: After the Garura install, one run of `initialize` sets the project up from the product owner's answers: its memory, its review rule groups and its tracker's work-item types.
- Goal: Every question shows its choices and a proposed answer that names its source.
- Goal: The project's Garura memory holds only the memory blocks of Phoenix memory the answers call for, and the profile records the answers.
- Goal: Two projects on one machine with different answers hold different memory blocks, taken from the one Phoenix memory.
- Goal: The tracker has each work-item type the plays file, or a recorded stand-in that the plays read.
- Limit: Never make a tracker type or a stand-in before the product owner's typed yes, and read memory only through the memory tool.
- Limit: Never write an answer the product owner did not give or confirm, and never write Phoenix memory or another project's memory.
- Fails if: a proposed answer names no source, or an answer is recorded that the person never gave.
- Fails if: a review in the project still runs a rule group the answers rule out, or its record does not name the groups it skipped.
- Fails if: a play that writes to the tracker stops on a missing type after initialize ran, with no message that points to initialize.
- Fails if: initialize builds a project's memory while Phoenix memory cannot be reached.
- Context: serves the product owner right after the Garura install and every later play that reads the project's memory, runs its review or files work items; touches Phoenix memory (read only), the project's Garura memory, the profile and the tracker (GitHub first, then Jira and Linear through the same adapter); out are the Phoenix install, the Garura install, running the review, and filing work items.
- Checked by: run `initialize` on a fresh test project, answer the questions, then check its memory folder, the profile, a review record and the tracker's type list against the answers.
