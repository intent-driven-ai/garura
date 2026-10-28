# Feature: Lay Phoenix memory once, give each project its own blocks

## What it does
- Treats every memory file in Garura's source as Phoenix memory. The memory written in the source is what gets deployed, so no source memory file is "project memory" and none sits outside Phoenix memory. This ends the hand work that kept the source memory and Phoenix memory in step.
- Makes the install lay the whole of Phoenix memory from the source on the machine, once. A person installs Garura once on a machine and then initializes many projects there, so Phoenix memory is a machine-wide copy and is never laid again for each project.
- Makes a second install bring Phoenix memory up to date from the source, so a file that is new or changed in the source reaches Phoenix memory without a hand promotion.
- Makes `initialize` build each project's Garura memory from that one Phoenix memory, with only the memory blocks its answers call for. Two projects on one machine with different answers get different blocks, and initializing one project never changes the other or Phoenix memory.

## Inputs / Outputs
- In: the memory files in Garura's source, all of which are Phoenix memory.
- In: the Phoenix memory already on the machine, when there is one (a second install), read only through the memory tool.
- In: one project's confirmed setup answers (from fn-setup-questions), when `initialize` runs in that project.
- Out (install): Phoenix memory on the machine that matches the source file for file, and a record of what the install laid: each file, whether it was added, changed, taken out or left as it was, and its fingerprint (a short code that changes when the file's content changes). The record is our default; the sources do not say the install keeps one.
- Out (initialize): the project's own Garura memory, holding only the blocks its answers call for, each naming the place in Phoenix memory it came from (built through fn-project-memory).
- Out (initialize): a plain message that names each file the install record lists and Phoenix memory does not hold, when there is one, and stops the build.

## Rules & behavior
- Every memory file in the source is Phoenix memory. A check over the source names any memory file that is marked as project memory or sits outside the Phoenix memory folders, and the check fails until it is moved, because a file outside Phoenix memory is the drift this feature removes.
- A memory block is one folder of Phoenix memory that one answer selects: a domain shelf, a group of technology standards, or the standards of one tool or framework. Our default; the sources say "blocks" and do not say what one holds.
- First install on a machine: the install lays every Phoenix memory file from the source, and the record lists each as added.
- Second install: the install makes Phoenix memory match the source. It adds each file that is new in the source, replaces each file whose content changed, and takes out each file that is no longer in the source, and the record names each one. Taking out a file that left the source is our default; the sources say only that a second install brings Phoenix memory up to date.
- A second install with no change in the source memory changes 0 files in Phoenix memory, and its record says that nothing changed. Our default; it keeps a repeat install safe.
- An install never changes a project's own Garura memory. A project's memory changes only when the product owner runs `initialize` in it again (fn-rerun-initialize), because the blocks a project holds are its product owner's choice. When an install changes a file a project took a block from, the install's record names the change in plain words, so the product owner knows to run `initialize` again. Our default; the sources do not say what a project does after Phoenix memory changes.
- Two projects on one machine: each project's Garura memory is its own. `initialize` in one project reads Phoenix memory and writes only that project's memory; it never writes Phoenix memory and never writes another project's memory. So two projects with different answers hold different blocks, taken from the one Phoenix memory.
- A source memory file that is not yet in Phoenix memory: the next install lays it, with no hand promotion. If `initialize` runs and a file that the install record lists is not in Phoenix memory (for example an install that stopped part way), `initialize` does not build the memory. It names each missing file and says that the install must run again, because a project built from part of Phoenix memory would miss blocks its answers call for. It never takes the file from the source itself, because installed parts never read the source tree (#860). Our default; the sources do not say what happens then.
- Every part reads memory only through the memory tool, as now, so the tool records where each block came from.

## Acceptance criteria
- Given Garura's source, when the source check runs, then every memory file in it is in Phoenix memory and no file is marked as project memory.
- Given a machine with no Phoenix memory, when Garura is installed, then Phoenix memory holds every memory file in the source, and the install record lists each as added.
- Given a feature page template that is new in the source and not in Phoenix memory, when Garura is installed again, then Phoenix memory holds the template and no hand promotion was done.
- Given a source with a changed file and a file taken out since the last install, when Garura is installed again, then Phoenix memory holds the changed content, no longer holds the file taken out, and the record names both.
- Given no change in the source memory since the last install, when Garura is installed again, then no Phoenix memory file changes and the record says nothing changed.
- Given two projects on one machine, one answering that it has a database and one that it has none, when `initialize` runs in each, then only the first project's Garura memory holds the database standards, and both name the same Phoenix memory as their source.
- Given a project already initialized, when `initialize` runs in a second project, then the first project's Garura memory and Phoenix memory do not change.
- Given a file in the install record that Phoenix memory does not hold, when `initialize` runs, then it builds no memory, names the missing file and says to install again.

## Out of scope
- How the install copies the plays, agents, skills and tools (the install play owns it). This feature sets what the install must lay as Phoenix memory and the record it leaves.
- Choosing which files the answers select and recording the answers in the profile (fn-project-memory owns it).
- Running `initialize` again after a project or Phoenix memory changes (fn-rerun-initialize owns it).
- Moving the memory tool's home to Phoenix, and removing the machine-global Garura memory folder (later, by the business intent #862).
- Promoting a person's answer or an approved memory update from a project up to Phoenix memory (a person does it on purpose, outside this work).

## Sources
- GitHub #883: "All memory in Garura's source is Phoenix memory."; "One install lays the whole Phoenix memory on a machine, once."; "A person installs Garura (Phoenix) once and initializes many projects, each with different memory blocks".
- GitHub #883, Why: "Today the source memory and Phoenix memory drift apart. They are kept in step by hand."; "the feature page template was in the source but in no memory tier".
- GitHub #883, Done when: "A second install brings it up to date. No hand promotion is needed."; "Two projects on one machine, initialized with different answers, get different memory blocks from the one Phoenix memory."; "A play reads memory only through the memory tool, as now."
- GitHub #862, Rules: "Every part reads memory only through the memory tool."; Out of scope: "Installed parts reading the source tree (#860)".
- Shelf: none (routing.yaml, unmatched).

## Agent intent (ICE)
- Goal: Every memory file in Garura's source is Phoenix memory, and none is project memory or sits outside it.
- Goal: One install lays the whole Phoenix memory on the machine, and a second install brings it up to date with no hand promotion.
- Goal: `initialize` gives each project only the memory blocks its answers call for, from the one Phoenix memory on the machine.
- Limit: Never write Phoenix memory or another project's memory from `initialize`, and read memory only through the memory tool.
- Limit: Never change a project's own Garura memory from an install, and never read the source tree from an installed part.
- Fails if: a memory file is in the source and, after an install, not in Phoenix memory.
- Fails if: a project holds a memory block its own answers did not call for, or `initialize` in one project changes another project's memory.
- Fails if: `initialize` builds a project's memory while a file the install laid is missing from Phoenix memory.
- Context: serves the product owner who installs Garura once and initializes many projects; touches Garura's source memory, the machine's Phoenix memory, each project's Garura memory and the install record; out are the install's copy of the plays and tools, the answer selection (fn-project-memory) and a re-run (fn-rerun-initialize).
- Checked by: install twice on a test machine with one new source file between the installs, then initialize two test projects with different answers, and diff Phoenix memory against the source and the two projects' memory folders against their answers.
- Quality need: a second install with no source change changes 0 Phoenix memory files.
