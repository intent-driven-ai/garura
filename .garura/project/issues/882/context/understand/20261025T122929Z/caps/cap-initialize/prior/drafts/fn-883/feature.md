# Feature: Give each project its own memory blocks

## What it does
- Two words this page uses. Phoenix memory is the one shared memory on a machine (the domain shelves, the standards, the templates) that every project on that machine draws from. A memory block is the set of Phoenix memory files that one setup answer selects: for example the Java standards for a Java answer, the .NET standards for a .NET answer, the React front-end standards for a React answer, or one domain shelf. What one block holds is our default; the sources say "blocks" and give the Java, .NET and React examples, but do not say what a block holds.
- Memory reaches a project in three steps, and this feature is the third. First, the Phoenix install runs once per machine and lays Phoenix memory from the Phoenix memory repository. Second, the Garura install runs once per project and lays only the pieces (the plays, agents, skills, tools and the memory tool) and no memory. Third, `initialize` runs in the project, asks the questions, and sets up the project's Garura memory from Phoenix memory with only the blocks the answers call for.
- It keeps each project's blocks its own. A person installs Phoenix once on a machine and initializes many projects there, each with different answers, so two projects hold different blocks taken from the one Phoenix memory, and initializing one project never changes another project or Phoenix memory.
- It records, in the project, which blocks the project took and what each held when it was taken, so the project can learn later that Phoenix memory changed. On each run, `initialize` compares the project's blocks with Phoenix memory and names each block that changed, so the product owner can take the change in. No install ever reaches into a project to do this.

## Inputs / Outputs
- In: one project's confirmed setup answers (from Ask the setup questions, fn-setup-questions), which decide the blocks.
- In: Phoenix memory on the machine, read only through the memory tool. The tool's interface hides where Phoenix memory is kept: today it is a folder in the person's home folder that the Phoenix install laid, and later a remote place, and this feature does not change when that moves.
- In: on a later run, the project's own block list from the earlier run.
- Out: the project's own Garura memory, holding only the blocks its answers call for (the files are written through Build the project's memory, fn-project-memory).
- Out: the project's block list, kept in the project's own Garura memory beside the blocks: for each block, the answer that selected it, the place in Phoenix memory of each of its files, each file's fingerprint (a short code that changes when the file's content changes) and the version of Phoenix memory it was taken from. Where the list is kept and what it holds is our default; the sources do not say how a project records its blocks.
- Out: on a later run, a plain list in the run's brief of each block that changed in Phoenix memory since it was taken: the files changed, added or taken out, and the answer that selected the block.
- Out: when Phoenix memory cannot be reached, a plain message that says so and that the Phoenix install must run on this machine, and no memory built.

## Rules & behavior
- The Garura install lays no memory. A project that has had the Garura install and no `initialize` run holds no Garura memory of its own, and `initialize` is the only part that sets it up.
- `initialize` reads Phoenix memory and writes only the project's own Garura memory. It never writes Phoenix memory and never writes another project's memory, because Phoenix memory is shared by every project on the machine and a write there from one project would change what the others draw from.
- A project takes a block only when one of its answers calls for it. Two projects with different answers (one Java, one .NET; one with a React front end, one with none) hold different blocks from the one Phoenix memory.
- How a project learns that a block changed: each run of `initialize` reads, through the memory tool, the current fingerprint of each file in the project's block list and compares it with the fingerprint recorded when the block was taken. A file whose fingerprint differs is changed; a file Phoenix memory now holds in the block's place that the list does not is added; a file the list holds that Phoenix memory no longer holds is taken out. The brief names each one under its block. Our default; the sources say only that `initialize` "can run again to take in changes".
- A changed block is taken in only on the product owner's typed yes in that run's brief, because the blocks a project holds are its product owner's choice and a new standard can change what a review finds. When the product owner says no, the project keeps the block as it was and the list keeps the old fingerprints, so the next run names the change again. Our default; the sources do not say who decides.
- The check runs only when `initialize` runs. No install and no other play changes a project's memory or checks its blocks, so a project's memory never changes in the middle of other work. A product owner who wants a Phoenix memory change runs `initialize` again (Run initialize again, fn-rerun-initialize). Our default; the sources do not say when a project checks.
- A second Phoenix install or a second Garura install changes no file in any project's Garura memory. Phoenix memory may change under a project, but the project's own copy changes only on its next `initialize` run, after the product owner's yes.
- When the memory tool cannot reach Phoenix memory (it says the tier is missing), `initialize` stops, builds and changes no project memory, and says in plain words that Phoenix memory could not be reached and the Phoenix install must run on this machine. An empty answer there would look like "no block fits" and leave the project with too little memory. It never takes memory from Garura's source or from another project instead, because installed parts read memory only through the memory tool.
- A block whose answer the product owner changed is no longer a change to take in: the re-run adds or takes out the whole block from the new answer (Run initialize again, fn-rerun-initialize, owns that).

## Acceptance criteria
- Given a project after the Garura install and before `initialize`, when its Garura memory is read, then it holds no memory files.
- Given two projects on one machine, one answering Java and one answering .NET, when `initialize` runs in each, then only the first holds the Java standards block, only the second holds the .NET standards block, and both block lists name the same Phoenix memory as the source.
- Given a project already initialized, when `initialize` runs in a second project, then no file in the first project's Garura memory and no file in Phoenix memory changes.
- Given a project that took the database block, when a second Phoenix install changes a file in that block, then no file in the project's Garura memory changes; and when `initialize` next runs in the project, then its brief names the database block and the changed file.
- Given that brief, when the product owner types yes, then the project's database block holds the new content and the block list holds the new fingerprint; when the product owner says no, then the block and the list are unchanged and the next run names the change again.
- Given an initialized project, when Garura is installed again in it, then no file in that project's Garura memory changes.
- Given a machine where the memory tool cannot reach Phoenix memory, when `initialize` runs, then it builds no memory and says that the Phoenix install must run on this machine.

## Out of scope
- Laying Phoenix memory on the machine and bringing it up to date: the Phoenix install owns it, once per machine. This feature only reads what that install laid.
- Laying the plays, agents, skills, tools and the memory tool in a project: the Garura install owns it, and it lays no memory.
- Which files each answer selects, writing them, and recording the answers in the profile: Build the project's memory (fn-project-memory) owns it.
- Adding or taking out a whole block when an answer changes: Run initialize again (fn-rerun-initialize) owns it.
- How Garura's source memory reaches the Phoenix memory repository without hand copying: issue #868 owns it, and it is outside this capability because it is about keeping Phoenix memory itself up to date.
- Promoting a person's answer or an approved memory update from a project up to Phoenix memory: a person does it on purpose, outside this work, because a promotion changes what every project on the machine draws from.

## Sources
- GitHub #883, the Phoenix install, once per machine: "It lays Phoenix memory from the `phoenix-memory` repo"; "The memory tool reads Phoenix memory only through its own interface."; "later it points at a remote place, and nothing else changes."
- GitHub #883, the Garura install, once per project: "It lays only the pieces: the plays, agents, skills, tools and the memory tool. It lays no memory."
- GitHub #883, `initialize`: "It asks the questions that decide which memory fits the project (for example Java or .NET, a React front end or none) and sets up the project's Garura memory from Phoenix memory. It can run again to bring changes in."; "A person installs Phoenix once on a machine and initializes many projects, each with different memory blocks."
- GitHub #883, Done when: "`initialize` builds the project's Garura memory from Phoenix memory, with only the blocks its answers call for, and can run again to take in changes."; "Two projects on one machine, initialized with different answers, get different memory blocks from the one Phoenix memory."; "A play reads memory only through the memory tool."
- GitHub #883, Open: "How the source memory reaches the `phoenix-memory` repo without hand copying (#868)."
- Shelf: none; no knowledge shelf in memory covers setting up a software project.

## Agent intent (ICE)
- Goal: `initialize` gives each project only the memory blocks its answers call for, from the one Phoenix memory on the machine.
- Goal: Two projects on one machine with different answers hold different blocks, and each project's blocks are its own.
- Goal: On each run, `initialize` compares the project's blocks with Phoenix memory by fingerprint and names each block that changed.
- Limit: Never write Phoenix memory or another project's memory from `initialize`, and read memory only through the memory tool.
- Limit: Take a changed block into a project only on the product owner's typed yes.
- Fails if: a project holds a memory block its own answers did not call for, or `initialize` in one project changes another project's memory.
- Fails if: an install changes a file in a project's Garura memory.
- Fails if: a block changed in Phoenix memory and the next `initialize` run in a project that holds it does not name the change.
- Fails if: `initialize` builds a project's memory while Phoenix memory cannot be reached.
- Context: serves the product owner who installs Phoenix once on a machine and initializes many projects; touches Phoenix memory (read only, through the memory tool), each project's Garura memory and its block list; out are the Phoenix install, the Garura install, the file selection (fn-project-memory) and a changed answer on a re-run (fn-rerun-initialize).
- Checked by: initialize two test projects on one machine with different answers, change one file in a block the first holds and lay Phoenix memory again, then check that no project file changed, that the first project's next `initialize` run names the changed file, and that a yes takes it in.
- Quality need: an install changes 0 files in any project's Garura memory.
