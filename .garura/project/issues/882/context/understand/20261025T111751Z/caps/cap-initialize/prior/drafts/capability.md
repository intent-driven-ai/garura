# Capability: Initialize a project for Garura

## Benefit hypothesis
- Serves the product owner who has just installed Garura in a project, and every play that later reads the project's memory, runs its review or writes to its tracker. Today an install copies all of Phoenix memory and a review runs every rule, so a project with no database, no front end or no permissions still gets those standards and those findings, and a play can stop the first time the tracker lacks a work-item type it files.
- We believe that when the product owner answers one short set of questions after the install, the project gets only the memory and the review rules that fit it, and its tracker holds every work-item type the plays file (Business Intent, Epic, Story, Bug, Chore, Spike). The value is fewer wrong findings, a smaller memory that fits the project, and no play that stops on a missing type.
- We will know it is true when: one play (`initialize`) asks the questions, each with choices and a proposed answer that names its source; the answers build the project's Garura memory from only the part of Phoenix memory it needs and the profile records them; a review in the project runs only the rule groups that fit and its record names the groups it skipped; the tracker has each needed type or a named stand-in; and the product owner can run `initialize` again when the project changes.

## Boundary (In / Out / Never)
- In: asking the setup questions after the install, building the project's Garura memory from the answers, recording which review rule groups fit the project, setting up the tracker's work-item types, and running all of this again when the project changes. These five jobs share one moment (the project is being set up) and one input (the product owner's answers), so they live in one capability.
- Out: the install itself, which copies the plays, agents, skills and tools but brings no memory of its own (the install play owns it). Initialize starts where the install stops, so the two never write the same files.
- Out: running a review and deciding its findings (the review play, /check-change, owns it). Initialize only records which rule groups fit; the review reads that record and names what it skipped.
- Out: shaping, planning and filing work items (/shape-slice and /shape-plan own them). Initialize makes sure the tracker can hold their types; it files no work item itself.
- Out: moving the memory tool's home to Phoenix and removing the machine-global Garura memory folder. The business intent puts this later, once the memory tool is fully live.
- Never: write an answer the product owner did not give or confirm. The answers are the person's; a proposed answer is only a proposal until the person accepts it.
- Never: propose an answer without naming its source. A proposal with no source hides a guess, and the person cannot judge it.
- Never: make a work-item type in the tracker before the product owner's typed yes. A tracker is an outside system, and a write there is visible to the whole team.
- Never: read memory except through the memory tool. Every part of Garura reads memory that way, so initialize does too.

## Guiding rules
- The questions are built from Phoenix memory, not written by hand. This keeps the question set in step with what memory actually holds: a domain, standard or tool that memory does not hold is never offered as a choice.
- Each question has choices and a proposed answer with its source. The product owner then confirms or corrects instead of researching each answer from nothing.
- One run sets up memory, review rules and tracker types from the same answers. A second set of questions for the tracker or the review would ask the person the same things twice.
- Every change initialize makes is recorded: the answers in the profile, the memory it built, the rule groups it chose, and the tracker types it made or mapped. A later run, a review or a play can then read what was decided without asking again.
- A run can be repeated at any time. A project changes (it gains a database, a web surface or a new tracker), and the set-up must follow it without a reinstall.

## Features
- Ask the setup questions (fn-setup-questions): asks the product owner the short set of questions built from Phoenix memory, each with choices and a proposed answer that names its source, and records the answers.
- Build the project's memory (fn-project-memory): sets up the project's Garura memory from only the part of Phoenix memory the answers call for, and records the answers in the profile.
- Choose the review rule groups (fn-review-rule-groups): records which rule groups of the review fit the project, so a review runs only those and names the groups it skipped.
- Set up the tracker's work-item types (fn-881): finds the tracker the project uses and the types it has, makes each missing type after a typed yes, and records a stand-in where a type cannot be made.
- Run initialize again (fn-rerun-initialize): lets the product owner run initialize again when the project changes, with the earlier answers proposed, so the set-up follows the project.
- Lay Phoenix memory once, give each project its own blocks (fn-883): treats every memory file in Garura's source as Phoenix memory, has one install lay it on the machine and a second install bring it up to date, so `initialize` gives each project only the blocks its answers call for.

## Sources
- GitHub #862, "A project gets only the memory and the review rules that fit it: initialize asks after the install" (the business intent): "after the install, one play (`initialize`) asks the person a short set of questions built from Phoenix memory"; "each question has choices and a proposed answer with its source"; "a review in that project runs only the rule groups that fit it"; "a project can run `initialize` again when it changes".
- GitHub #881, "Initialize sets up the tracker's work-item types: Business Intent, Epic, Story, Bug, Chore and Spike" (the story): "`initialize` (this business intent) also sets up the tracker".
- The product owner's answers (seed): "After the install, set a project up for Garura: its memory, its review rules, and its tracker's work-item types."
- Shelf: none. No domain shelf in memory holds software delivery work (routing.yaml, unmatched); the domain page software-delivery-planning/domain.md carries its own outside sources.

## Agent intent (ICE)
- Goal: After the install, one run of `initialize` sets the project up from the product owner's answers: its memory, its review rule groups and its tracker's work-item types.
- Goal: Every question shows its choices and a proposed answer that names its source.
- Goal: The project's Garura memory holds only the part of Phoenix memory the answers call for, and the profile records the answers.
- Goal: The tracker has each work-item type the plays file, or a recorded stand-in that the plays read.
- Limit: Never make a tracker type before the product owner's typed yes, and read memory only through the memory tool.
- Limit: Never write an answer the product owner did not give or confirm.
- Fails if: a proposed answer names no source, or an answer is recorded that the person never gave.
- Fails if: a review in the project still runs a rule group the answers rule out, or its record does not name the groups it skipped.
- Fails if: a play that writes to the tracker stops on a missing type after initialize ran, with no message that points to initialize.
- Context: serves the product owner right after the install and every later play that reads the project's memory, runs its review or files work items; touches Phoenix memory, the project's Garura memory, the profile and the tracker (GitHub first, then Jira and Linear through the same adapter); out are the install itself, running the review, and filing work items.
- Checked by: run `initialize` on a fresh test project, answer the questions, then check its memory folder, the profile, a review record and the tracker's type list against the answers.
