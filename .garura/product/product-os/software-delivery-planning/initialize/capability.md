# Capability: Set a project up after the install (Initialize)

Set a project up after the install (Initialize): after the install, set a project up for Garura: its memory, its review rules, and its tracker's work-item types.
The name is the product owner's, on the list he set for Install and distribute on 2026-11-10, where it is the fourth capability; the words after it are the capability's one-line in the model, from his answers when it was first written. The words this page uses:
- Garura, a coding tool, an installed part and the install engine mean what they mean on Install into a project: Garura is the set of plays, loops, sub-agents, skills and tools a coding tool runs inside a project, and the install engine is the one set of steps behind the install's two front doors, the one-line command and the install play.
- Initialize is, in ADR 066's words, an engine thing, not a play: "Initialize, seeding memory and upgrade are engine things, not plays." This page reads it, as Install into a project reads installation, as a run of that same engine, after the install. A play is a command a person types that runs its sub-agents and skills; an engine thing runs as part of Garura itself. The issue that asked for it, #862, calls it "one play (`initialize`)", and the memory guide every agent reads still says "A play run after the install, `initialize`"; this page names the difference and leaves open how a person starts it.
- Phoenix memory is the one shared memory on a machine (the domain shelves, the standards, the templates and the review's rules) that every project on that machine draws from. A project's Garura memory is the project's own memory, read before Phoenix memory, which initialize writes for the first time; it is built from only the part of Phoenix memory the project needs and is never a copy of a Phoenix file. How memory works, what may enter each tier and how a learning is promoted belong to Memory, in Standards, structure, settings and memory.
- A memory block is the relevant part of Phoenix memory that one setup answer selects, down to the part of a file: for example only the checkout part of the commerce knowledge for a project that needs checkout and not the rest of commerce, the Java standards for a Java answer, or the React front-end standards for a React answer; a project gets a block only when its answers call for it.
- The product profile is the record of the product's shape and the quality levels it commits to, kept in the project's product model, where every later play reads the facts about the project. #862 asks that it also records the setup answers.
- A rule group is a set of the review's rules that check one kind of thing (for example front end, back-end service, database, running service, permissions or personal data); the review runs or skips a group as a whole.
- The tracker is where the team keeps its work items (GitHub, Jira, Linear or another), reached only through the adapter, the one piece that reads and writes it. A stand-in is a type the tracker already has that the plays file a work item as when the tracker cannot make the type they need.

This capability does six jobs:
- Ask the setup questions, built from Phoenix memory, each with its choices and a proposed answer that names its source.
- Build the project's own Garura memory from only the memory blocks the answers call for.
- Record which of the review's rule groups fit the project.
- Set up, in the tracker, the issue types Garura files.
- Update the setup as the project changes.
- Update each project's own memory as Phoenix memory changes, keeping each project's blocks its own.

These six jobs share one moment (the project is being set up) and one input (the product owner's answers), so they live in one capability.
It starts where the install stops. Install into a project "lays the pieces and stops", and in the product owner's words, "install finishes without any memory." Initialize starts where that install stops, so a project has no Garura memory of its own until initialize runs, and the two never write the same files. When a new version of Garura asks something new, Upgrade a project hands the run back here: "running the set-up again when a new version asks something new". It sets a project up whichever coding tool the team uses.
Initialize asks and records. What memory may hold is Memory's, what each rule group checks is the review's, and what each tracker type means is for Track execution in the team's tracker, in Orchestration, to say; Initialize never decides those.
It works only in the project and, after a typed yes, in the team's tracker; it reads Phoenix memory and never writes it, and production is never touched.
It serves Install and distribute, whose outcome is that "A team gets Garura into its project, upgrades it knowing what changes, and uses it on whichever coding tool it has." It matters because a team "can only use Garura once it's in their project", and a project that is in but not set up reads all of Phoenix memory on every lookup, gets every review rule whether it fits or not, and stops the first time a play files a type its tracker lacks. It sits in software delivery planning with the other three capabilities of Install and distribute, and the domain's first paragraph says so.

What is not built yet:
- Nothing of Initialize is built. No front door runs it; the install play's guide says "`initialize` (not built yet)", and a new project "starts with no memory of its own", so every lookup goes up to Phoenix memory.
- Found and not filed: the one-line command ends by saying Garura was "initialized successfully!", though nothing has set the project up.
- The memory tool reads every tier, but "the tool has no command that writes Garura or Phoenix memory", and nothing builds Garura memory from Phoenix memory.
- Phoenix memory reaches a machine when the memory tool downloads it, "the first command that needs Phoenix memory downloads it there from its source". The Phoenix install that #883 plans, once per machine, is not built.
- The product profile has no place for the setup answers or the rule-group record; it holds the product's shape, its quality levels and its compliance needs.
- The review "runs every rule group, a set of the review's rules that check one kind of thing, such as a database, on every project."
- The adapter reaches GitHub and GitLab only. It makes an issue of a type the tracker has and stops when the type is missing, but no step lists a tracker's types or makes one; its GitLab entry sets no type at all ("GitLab has no issue types here."), and Jira and Linear have no entry. Garura's own GitHub organization got its types by hand, the Epic type on 2026-10-25.

## Benefit hypothesis
- Who it serves: the product owner, who sets the project up right after the install, answers the setup questions and says yes before anything is made in the tracker; every later play that reads the project's memory, runs its review or files work items; and a person who sets up many projects on one machine from the one Phoenix memory.
- What we believe: when the product owner answers one short set of questions after the Garura install, the project gets only the memory and the review rules that fit it, and its tracker holds every issue type Garura files (Business Intent, Epic, Story, Bug, Chore, Spike). Business Intent is the one product-layer type among them: it holds a need the product meets, while the other five are work items. The value is fewer wrong findings, a smaller memory that fits the project, and no play that stops on a missing type, if the work stands on these rules:
  - The answers are the person's, and every proposal names its source.
  - Memory is built from the part a project needs, never copied.
  - A rule group is skipped only when an answer rules it out.
  - Nothing is made in the tracker before a typed yes.
  - A run can be repeated, and a run with nothing changed changes nothing.
- How we will know: each of these checks holds:
  - One run of Initialize asks the setup questions, and each question shows its choices and a proposed answer that names its source.
  - The project's Garura memory holds only the memory blocks its answers call for, built from those parts of Phoenix memory and never a copy of a whole Phoenix file, and the product profile records each answer with its question.
  - Two projects on one machine, initialized with different answers, hold different memory blocks taken from the one Phoenix memory.
  - A review in the project runs only the rule groups that fit it, and the review's record names each group it skipped.
  - The tracker holds each issue type Garura files, or a stand-in the product owner said yes to.
  - The product owner can run initialize again when the project or Phoenix memory changes, and the set-up follows the change.
  - None of this is tested today, because Initialize is not built.

## Boundary (In / Out / Never)
- In: asking the setup questions after the Garura install, setting up the project's Garura memory from the answers, recording which review rule groups fit the project, setting up the issue types Garura files in the tracker, and running all of this again when the project changes.
- In: giving each project its own memory blocks from the one Phoenix memory on the machine, and finding on each run whether the part of Phoenix memory a block was built from has changed, so a re-run can rebuild that part from Phoenix memory as it is now.
- Out: the Garura install, which lays only the pieces (the plays, agents, skills, tools and the memory tool) and no memory, checks that they run, and can take them out again. Install into a project owns it. Initialize starts where that install stops, so a project has no Garura memory of its own until initialize runs, and the two never write the same files.
- Out: moving a project to a new version. Upgrade a project owns it; when a new version asks something new, running the set-up again is this capability's.
- Out: how Phoenix memory reaches a machine and is brought up to date, what may enter each memory tier, and promotion. Memory, in Standards, structure, settings and memory, owns them. Initialize only reads Phoenix memory, through the memory tool, and never writes it.
- Out: what each rule group checks, running a review and deciding its findings. Check the code against its standards, in Code → Validation, owns them, with the review's rules in memory. Initialize only records which rule groups fit; the change to the review that makes it read that record is a later story under #862.
- Out: what each tracker type means and how a work item is marked (Track execution in the team's tracker, in Orchestration), and turning an intent into work items and filing them (Turn intents into agent work). Initialize makes sure the tracker can hold their types; it files no work item itself. The change to the filing plays that makes them read the type mapping initialize records, and stop with a message that points to initialize when a type is missing and not mapped, is a later story under #862, not filed yet.
- Out: the product profile's levels, which move only by an approved decision (Specify the product), and where the setup answers sit in the profile (Product model). Initialize only adds the answers there.
- Out: what each setting means and where a settings file lives. Settings, in Standards, structure, settings and memory, owns them.
- Never: write an answer the product owner did not give or confirm. The answers are the person's; a proposed answer is only a proposal until the person accepts it. The reason: #862's rule, "The answers are the person's; a proposed answer always names its source."
- Never: propose an answer without naming its source, or from what an agent knows by itself. A proposal with no source hides a guess, and the person cannot judge it. The reason: every agent must "Never answer from what you already know, and never from the web, without a memory update a person approved."
- Never: make an issue type in the tracker, or record a stand-in, before the product owner's typed yes. A tracker is an outside system, and a write there is visible to the whole team.
- Never: read memory except through the memory tool, and never write Phoenix memory or another project's memory. Phoenix memory is shared by every project on the machine, so a write there from one project would change the others.
- Never: copy a whole Phoenix file into the project. The reason: "The tool reads Phoenix memory. It does not copy a file from it into the project.", and the product owner: "It should not copy the file."
- Never: touch production. Initialize works in the project and, after a yes, in its tracker. The reason, in the product owner's words: "We are never touching production."

## Guiding rules
- The questions are built from Phoenix memory, not written by hand. This keeps the question set in step with what memory actually holds: a domain, standard or tool that memory does not hold is never offered as a choice. The reason, in the product owner's words: "The question here will be generated based on the Phoenix memory that it already has, because we're not pulling something random."
- The project's memory is built, never copied. Initialize reads Phoenix memory through the memory tool and writes into the project only the part each answer selects, down to the part of a file, and never a whole Phoenix file. A whole file brings context the project does not need (all of commerce for a project that needs only checkout), and the plays would read that context as if it fit the project. When Phoenix memory changes, a re-run rebuilds the relevant part from it; it does not copy the new file.
- Each question has choices and a proposed answer with its source. The product owner then confirms or corrects instead of researching each answer from nothing. A proposal comes from the project's own code and memory first, then Garura memory, then Phoenix memory.
- One run sets up memory, review rules and tracker types from the same answers. A second set of questions for the tracker or the review would ask the person the same things twice.
- Every change initialize makes is recorded: the answers in the product profile, the memory blocks it set up with where each came from, the rule groups it chose, and the tracker types it made or mapped. A later run, a review or a play can then read what was decided without asking again. Not decided: where the records outside the product profile are kept.
- A run can be repeated at any time. A project changes (it gains a database, a web surface or a new tracker) and Phoenix memory changes (a new standard or template), and the set-up must follow both without a reinstall. The reason: #862 asks that "a project can run `initialize` again when it changes".
- A run with nothing changed changes nothing. The reason: the capability's reliability need, "a second run with every answer unchanged and no Phoenix memory change changes 0 files in the project's memory, its rule-group record and its tracker".
- When the memory tool cannot reach Phoenix memory, initialize stops and builds nothing, and says in plain words that Phoenix memory could not be reached. An empty answer there would look like "nothing fits" and leave the project with too little memory. The reason: "`tier_missing` means a tier cannot be reached. Say so."
- No tracker in Initialize's own steps. Each tracker is reached through the adapter, GitHub first. The reason: Standards, structure, settings and memory must not "Name a tracker in a play, skill or sub-agent, because they only know the tool."
- Not decided: how a person starts Initialize, since it is an engine thing behind the install's front doors and not a play.
- Not decided: how an engine run reads memory and drafts its proposals, since "Only agents call the tool".

## Features
- Ask the setup questions (fn-setup-questions): asks the product owner the short set of questions built from Phoenix memory, each with choices and a proposed answer that names its source, and keeps the confirmed answers for the other features.
- Build the project's memory (fn-project-memory): sets up the project's Garura memory from only the memory blocks the answers call for, and records the answers in the product profile.
- Choose the review rule groups (fn-review-rule-groups): records which rule groups of the review fit the project, so a review runs only those and names the groups it skipped.
- Set up the tracker's work-item types (fn-881): finds the tracker the project uses and the types it has, makes each missing type after a typed yes, and records a stand-in, also after a typed yes, where a type cannot be made.
- Update the setup as the project changes (fn-rerun-initialize): lets the product owner run initialize again when the project changes, with the earlier answers proposed, so the set-up follows the project.
- Update each project's own memory as Phoenix memory changes (fn-883): keeps each project's blocks its own, taken from the one Phoenix memory on the machine, and on each run compares them with Phoenix memory so the project learns when a block changed.

## Sources
- The list the product owner set on 2026-11-10, in .garura/project/issues/1021/context/capabilities.md: "Set a project up after the install (Initialize): new on this list.", "Its capability is designed in the model with six features and names no intent", and his reply recorded in .garura/project/issues/1021/context/bi-7-capability-4/page-approvals.md: "yes, record it and draft the first one"
- .garura/product/product-os/_spine.yaml, cap-initialize's one-line: "After the install, set a project up for Garura: its memory, its review rules, and its tracker's work-item types."
- .garura/product/product-os/intents/bi-7.md: "A team gets Garura into its project, upgrades it knowing what changes, and uses it on whichever coding tool it has.", "A team can only use Garura once it's in their project"
- .garura/product/product-os/intents/bi-10.md: "Name a tracker in a play, skill or sub-agent, because they only know the tool."
- .garura/product/product-os/software-delivery-planning/install-into-project/capability.md: "It lays the pieces and stops."
- .garura/product/product-os/software-delivery-planning/upgrade-project/capability.md: "running the set-up again when a new version asks something new"
- .garura/product/product-os/software-delivery-planning/check-code-against-standards/capability.md: "It runs every rule group, a set of the review's rules that check one kind of thing, such as a database, on every project.", "changing the review to read that record is a later story (#862)"
- .garura/product/product-os/software-delivery-planning/environment-setup/capability.md, the product owner on 2026-11-08: "We are never touching production."
- .garura/product/product-os/_spine.yaml, cap-initialize's reliability need: "a second run with every answer unchanged and no Phoenix memory change changes 0 files in the project's memory, its rule-group record and its tracker"
- docs/adr/066-names-say-who-does-the-work-five-roles-own-the-verbs.md, section 5: "Initialize, seeding memory and upgrade are engine things, not plays."
- docs/adr/038-install-brings-no-memory.md: "initialize is an engine thing, not a play. Its job, setting up a project's own memory by asking from Phoenix memory, stands"; section 1, the product owner on 19 October: "install finishes without any memory."; section 3, the product owner: "The question here will be generated based on the Phoenix memory that it already has, because we're not pulling something random."
- docs/adr/039-memory-writes-go-to-short-term-memory-plays-read-no-memory.md, Decision 4 (the memory tool never copies a Phoenix file): "The tool reads Phoenix memory. It does not copy a file from it into the project."; "A project's Garura memory is built separately, from only the part the project needs: by `initialize`, and by promotion." The product owner, in the same decision: "You don't need to copy the entire file. You only need to bring in the context which is relevant to the checkout part of the commerce", "It should not copy the file."
- core/grounding/glossary.md, the row for Garura memory: "never a copy of a Phoenix file"; "NOT: a copy of Phoenix memory — checkout, not all of commerce."
- core/tools/memory/GUIDE.md, the memory guide every agent reads: "A play run after the install, `initialize`", "starts with no memory of its own", "Only agents call the tool", "Never answer from what you already know, and never from the web, without a memory update a person approved.", "`tier_missing` means a tier cannot be reached. Say so."
- core/tools/memory/contract/v5.json: "the tool has no command that writes Garura or Phoenix memory"
- core/tools/memory/pull.py: "the first command that needs Phoenix memory downloads it there from its source"
- core/components/plays/install-garura/SKILL.md: "`initialize` (not built yet)"
- installer/install.sh: "initialized successfully!"
- core/components/skills/platform-adapter/reference/gitlab/verbs.md: "GitLab has no issue types here."
- GitHub #862 (open), "A project gets only the memory and the review rules that fit it: initialize asks after the install", under Install and distribute's tracker issue: "after the install, one play (`initialize`) asks the person a short set of questions built from Phoenix memory"; "each question has choices and a proposed answer with its source"; "a review in that project runs only the rule groups that fit it"; "a project can run `initialize` again when it changes"; "The answers are the person's; a proposed answer always names its source."
- GitHub #881 (open), "Initialize sets up the tracker's work-item types: Business Intent, Epic, Story, Bug, Chore and Spike": "`initialize` (this business intent) also sets up the tracker"; "the organization `intent-driven-ai` got the Epic type by hand on 2026-10-25."
- GitHub #883 (open), "All memory in Garura's source is Phoenix memory: one install lays it, initialize gives each project its own blocks": "It lays only the pieces"; "It lays no memory."; "It asks the questions that decide which memory fits the project (for example Java or .NET, a React front end or none) and sets up the project's Garura memory from Phoenix memory. It can run again to bring changes in."
- The stock-take of Install and distribute, .garura/project/issues/1021/context/bi-7-inventory/inventory.md, sections 2 and 10.
- The short line beside each feature: kept from the capability's page in the model, under each feature's name on its own page.
- Shelf: none. No knowledge shelf in memory covers setting up a software project; the domain page software-delivery-planning/domain.md carries its own outside sources.
- .garura/product/product-os/software-delivery-planning/domain.md: "It also gets Garura itself into a project, sets the project up for it, keeps it current, and serves whichever coding tool the team works in."
