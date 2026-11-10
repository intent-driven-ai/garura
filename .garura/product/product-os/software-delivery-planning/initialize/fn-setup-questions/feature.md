# Feature: Ask the setup questions

## What it does
After the install, when the product owner starts Initialize, it builds one short set of questions about the project from what Phoenix memory holds, shows each with its choices and a proposed answer that names its source, and keeps the answers the product owner confirms or corrects, so every other job of Initialize works from the person's own answers.
- Words this page uses. Phoenix memory is the one shared memory on a machine (the domain shelves, the standards, the templates, the review's rules) that every project on that machine draws from. The brief is the one message Initialize shows the product owner, with every question in it, and the product owner answers it by typing a reply. Short-term memory is the working folder Initialize keeps for one run. The product profile is the record of the product's shape and the quality levels it commits to, kept in the project's product model, where every later play reads the facts about the project.
- It reads Phoenix memory through the memory tool and builds one short set of questions about the project from what memory holds, so the choices always match what memory can give.
- The questions cover the domains the product sits in, the kinds of features it has, the technology standards, the tools and frameworks, the surfaces (web, mobile, command line, API), and whether there is a database, personal data, permissions or a running service. These are the facts that decide which memory and which review rules fit.
- Each question shows its choices and a proposed answer that names its source, and the product owner confirms or corrects each one. The confirmed answers are the input of every other feature of initialize.
- Examples, in different kinds of project:
  - In a clinic's booking app, the front-end proposal is React and names the project's package file, and the database proposal is yes and names its schema folder.
  - In a bank's payments service with no screens, the surfaces proposal is API and names its route files.
  - In a team's command-line tool, the personal-data question carries no proposed answer, because nothing in the project or its memory shows it either way.
- How it meets the capability: the capability's first check, "each question shows its choices and a proposed answer that names its source", is met here, and every other job of Initialize reads the answers kept here.

Status: not built. No part of Garura asks these questions. The memory tool can already find and read what Phoenix memory holds, and it refuses a lookup with `tier_missing` when a tier cannot be reached.

## Inputs / Outputs
- In: Phoenix memory, read only through the memory tool: the domain shelves, the technology standards, the tools and frameworks it holds, and the review's rules. These give the choices of each question.
- In: what the project already shows, for the proposed answers: its files and its config.
- In: the project's own memory, then Garura memory, then Phoenix memory, in that order, where the project's files do not settle an answer; on a later run, the earlier answers as the product profile records them (Update the setup as the project changes, fn-rerun-initialize, proposes them).
- In: the product owner's typed reply to the brief: a confirmation or a correction for each question.
- Out: the question set, each question with its id, its plain question, its choices and its proposed answer with the source of that answer, shown together in one brief.
- Out: the confirmed answers, each kept with its question in the run's short-term memory, where the memory, review-rule and tracker features of the same run read them.
- Out: the same confirmed answers, handed to Build the project's memory (fn-project-memory), which records them in the product profile. The profile is where a later run finds them, because short-term memory belongs to one run and the profile stays with the project.

## Rules & behavior
- A choice is offered only when Phoenix memory holds it. A domain, standard or tool that memory does not hold is never a choice, because initialize could not set up memory for it.
- A proposed answer always names its source (a file of the project, its config, an earlier answer in the product profile or a memory file). Where nothing backs a proposal, the question carries no proposed answer and the person answers it; there is never a default in place of a source, because a default would look like a fact the project showed.
- Memory first, never an agent's own knowledge. The project's own code and memory are read first, then Garura memory, then Phoenix memory. The reason: every agent must "Never answer from what you already know, and never from the web, without a memory update a person approved."
- The answers are the person's. A proposal the person does not confirm is not recorded as an answer, because later plays treat every recorded answer as the product owner's own word. The reason: #862's rule, "The answers are the person's; a proposed answer always names its source."
- Together in one brief, each question by the rule for asking a person. The questions are asked together, so the person sees the whole set-up at once and can see how one answer bears on another. The reason: the rule for asking a person covers "a brief that ends with questions", and says "Each question asks one thing." and shows "several examples from different domains, never just one".
- The set is short: it asks only what decides memory, review rules or tracker types. A question whose answer changes none of these is not asked, because it costs the person time and sets up nothing. The reason: #862 asks for "a short set of questions built from Phoenix memory".
- When the memory tool cannot reach Phoenix memory (it says a tier is missing), initialize stops, asks nothing, and says in plain words that Phoenix memory could not be reached. It never builds questions from what it already knows, because those choices would not match any memory it could set up. The reason: "`tier_missing` means a tier cannot be reached. Say so."
- When a correction names something that is not among the choices (for example a domain Phoenix memory holds no shelf for), initialize records the person's answer as given, with a plain note that no memory can be set up for it, and asks nothing more about it. The answer stays the person's, so it is never refused or changed; the note tells the memory feature to set up nothing for it, and the product owner sees that the project's memory has a gap there.
- Not decided: whether Initialize researches such a gap and raises a memory update for a person to approve, or only names the gap.
- When the reply leaves some questions unanswered, initialize asks again only for those questions, in one short brief, and keeps the answers already given. No unanswered question is recorded as an answer, and no proposal stands in for it, because an answer the person did not give is not the person's.
- Not decided: what happens to a question the person still leaves open, and whether the rest of the set-up goes on without it. Orchestration must not "Stop a person. Every gate has a way past it that records what's owed."

## Acceptance criteria
- Given a fresh project after the Garura install, when the product owner runs initialize, then one brief shows questions that cover the domains, kinds of features, technology standards, tools and frameworks, surfaces, and database, personal data, permissions and running service.
- Given a question with a proposed answer, when the person reads the brief, then the proposal names its source and the question lists its choices.
- Given a question that nothing in the project or memory answers, when the brief is shown, then that question carries no proposed answer.
- Given Phoenix memory holds no shelf for a domain, when the domain question is built, then that domain is not a choice.
- Given the memory tool reports that Phoenix memory cannot be reached, when initialize builds the questions, then it asks nothing and its message says that Phoenix memory could not be reached.
- Given the product owner corrects the domain question with a domain Phoenix memory holds no shelf for, when the reply is recorded, then the answer is kept as given with a note that no memory can be set up for it.
- Given a reply that answers four of six questions, when initialize reads it, then the four answers are kept in the run's short-term memory, no answer is kept for the other two, and a new brief asks only those two.
- Given the product owner confirms every answer, when the run goes on, then each answer is kept with its question in the run's short-term memory and handed to Build the project's memory for the product profile.

## Out of scope
- Building the project's memory from the answers and recording them in the product profile (Build the project's memory, fn-project-memory, owns it).
- Recording the review rule groups (Choose the review rule groups, fn-review-rule-groups, owns it).
- Finding and making the tracker's work-item types (Set up the tracker's work-item types, fn-881, owns it).
- Proposing the earlier answers on a later run (Update the setup as the project changes, fn-rerun-initialize, owns it).
- How Phoenix memory reaches the machine, and what memory may hold: Memory, in Standards, structure, settings and memory, owns them.

## Sources
- GitHub #862 (open): "after the install, one play (`initialize`) asks the person a short set of questions built from Phoenix memory: the domains, the kinds of features, the technology standards, the tools and frameworks, the surfaces (web, mobile, CLI, API), and whether there is a database, personal data, permissions or a running service"
- GitHub #862: "each question has choices and a proposed answer with its source"; Rule 3: "The answers are the person's; a proposed answer always names its source."
- GitHub #862, Rule 2: "Every part reads memory only through the memory tool."
- GitHub #883 (open): "It asks the questions that decide which memory fits the project (for example Java or .NET, a React front end or none)"
- core/tools/memory/GUIDE.md: "Never answer from what you already know, and never from the web, without a memory update a person approved.", "`tier_missing` means a tier cannot be reached. Say so."
- core/components/skills/_shared/asking-a-person.md, the rule for asking a person: "a brief that ends with questions", "Each question asks one thing.", "several examples from different domains, never just one"
- .garura/product/product-os/intents/bi-9.md: "Stop a person. Every gate has a way past it that records what's owed."
- .garura/product/product-os/software-delivery-planning/initialize/capability.md: "each question shows its choices and a proposed answer that names its source"
- Shelf: none; no knowledge shelf in memory covers setting up a software project.
