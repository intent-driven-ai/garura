# Feature: Ask the setup questions

## What it does
- Words this page uses. Phoenix memory is the one shared memory on a machine (the domain shelves, the standards, the templates, the review's rule groups) that the Phoenix install laid and every project on that machine draws from. The brief is the one message `initialize` shows the product owner, with every question in it, and the product owner answers it by typing a reply. Short-term memory is the working folder `initialize` keeps for one run. The product profile is the project's lasting record of its setup answers, kept in the project's product model, where every later play reads the facts about the project.
- Runs when the product owner starts `initialize` after the Garura install. It reads Phoenix memory through the memory tool and builds one short set of questions about the project from what memory holds, so the choices always match what memory can give.
- The questions cover the domains the product sits in, the kinds of features it has, the technology standards, the tools and frameworks, the surfaces (web, mobile, command line, API), and whether there is a database, personal data, permissions or a running service. These are the facts that decide which memory and which review rules fit.
- Each question shows its choices and a proposed answer that names its source, and the product owner confirms or corrects each one. The confirmed answers are the input of every other feature of initialize.

## Inputs / Outputs
- In: Phoenix memory, read only through the memory tool: the domain shelves, the technology standards, the tools and frameworks it holds, and the review's rule groups. These give the choices of each question.
- In: what the project already shows, for the proposed answers: its files and its config. A proposed answer comes from one of these and names it.
- In: on a later run, the earlier answers as the product profile records them (Run initialize again, fn-rerun-initialize, proposes them).
- In: the product owner's typed reply to the brief: a confirmation or a correction for each question.
- Out: the question set, each question with its id, its plain question, its choices and its proposed answer with the source of that answer, shown together in one brief.
- Out: the confirmed answers, each kept with its question in the run's short-term memory: the folder of the issue `initialize` runs for, or, when it runs with no issue, `initialize`'s own folder in short-term memory. The memory, review-rule and tracker features of the same run read them there. Which folder a run with no issue uses is our default; the sources do not say.
- Out: the same confirmed answers, handed to Build the project's memory (fn-project-memory), which records them in the product profile. The profile is where a later run finds them, because short-term memory belongs to one run and the profile stays with the project.

## Rules & behavior
- A choice is offered only when Phoenix memory holds it. A domain, standard or tool that memory does not hold is never a choice, because initialize could not set up memory for it.
- A proposed answer always names its source (a file of the project, its config, an earlier answer in the product profile or a memory file). Where nothing backs a proposal, the question carries no proposed answer and the person answers it; there is never a default in place of a source, because a default would look like a fact the project showed.
- The answers are the person's. A proposal the person does not confirm is not recorded as an answer, because later plays treat every recorded answer as the product owner's own word.
- The questions are asked together in one brief, not one at a time, so the person sees the whole set-up at once and can see how one answer bears on another. Our default; the sources do not say how the questions are shown.
- The set is short: it asks only what decides memory, review rules or tracker types. A question whose answer changes none of these is not asked, because it costs the person time and sets up nothing.
- When the memory tool cannot reach Phoenix memory (it says a tier is missing), initialize stops, asks nothing, and says in plain words that Phoenix memory could not be reached and that the Phoenix install must run on this machine. It never builds questions from what it already knows, because those choices would not match any memory it could set up.
- When a correction names something that is not among the choices (for example a domain Phoenix memory holds no shelf for), initialize records the person's answer as given, with a plain note that no memory can be set up for it, and asks nothing more about it. The answer stays the person's, so it is never refused or changed; the note tells the memory feature to set up nothing for it, and the product owner sees that the project's memory has a gap there. Our default; the sources do not say what happens to an answer outside the choices.
- When the reply leaves some questions unanswered, initialize asks again only for those questions, in one short brief, and keeps the answers already given. No unanswered question is recorded as an answer, and no proposal stands in for it, because an answer the person did not give is not the person's. Initialize goes on to the memory, review-rule and tracker features only when every question has an answer, because each of them reads the whole set. Our default; the sources do not say what happens to a partial reply.

## Acceptance criteria
- Given a fresh project after the Garura install, when the product owner runs `initialize`, then one brief shows questions that cover the domains, kinds of features, technology standards, tools and frameworks, surfaces, and database, personal data, permissions and running service.
- Given a question with a proposed answer, when the person reads the brief, then the proposal names its source and the question lists its choices.
- Given a question that nothing in the project or memory answers, when the brief is shown, then that question carries no proposed answer.
- Given Phoenix memory holds no shelf for a domain, when the domain question is built, then that domain is not a choice.
- Given the memory tool reports that Phoenix memory cannot be reached, when initialize builds the questions, then it asks nothing and its message says that the Phoenix install must run on this machine.
- Given the product owner corrects the domain question with a domain Phoenix memory holds no shelf for, when the reply is recorded, then the answer is kept as given with a note that no memory can be set up for it.
- Given a reply that answers four of six questions, when initialize reads it, then a new brief asks only the two unanswered questions.
- Given a reply that answers four of six questions, when initialize reads it, then the four answers are kept in the run's short-term memory and no answer is kept for the other two.
- Given the product owner confirms every answer, when the run goes on, then each answer is kept with its question in the run's short-term memory and handed to Build the project's memory for the product profile.

## Out of scope
- Building the project's memory from the answers and recording them in the product profile (Build the project's memory, fn-project-memory, owns it).
- Recording the review rule groups (Choose the review rule groups, fn-review-rule-groups, owns it).
- Finding and making the tracker's work-item types (Set up the tracker's work-item types, fn-881, owns it).
- Proposing the earlier answers on a later run (Run initialize again, fn-rerun-initialize, owns it).
- Laying Phoenix memory on the machine (the Phoenix install owns it, once per machine).

## Sources
- GitHub #862: "after the install, one play (`initialize`) asks the person a short set of questions built from Phoenix memory: the domains, the kinds of features, the technology standards, the tools and frameworks, the surfaces (web, mobile, CLI, API), and whether there is a database, personal data, permissions or a running service".
- GitHub #862: "each question has choices and a proposed answer with its source"; Rule 3: "The answers are the person's; a proposed answer always names its source."
- GitHub #862, Rule 2: "Every part reads memory only through the memory tool."
- GitHub #883: "The Phoenix install, once per machine."; "It asks the questions that decide which memory fits the project (for example Java or .NET, a React front end or none)".
- Shelf: none; no knowledge shelf in memory covers setting up a software project.

## Agent intent (ICE)
- Goal: After the Garura install, `initialize` shows one brief of questions built from Phoenix memory, covering domains, kinds of features, standards, tools and frameworks, surfaces, and database, personal data, permissions and running service.
- Goal: Each question lists its choices and a proposed answer that names its source, or no proposal when nothing backs one.
- Goal: The confirmed answers are kept with their questions in the run's short-term memory and handed on for the product profile.
- Limit: Read Phoenix memory only through the memory tool, and offer no choice that memory does not hold.
- Limit: Record as an answer only what the product owner gave or confirmed.
- Fails if: a proposed answer names no source, or a default stands in for a missing source.
- Fails if: an answer is recorded that the product owner never gave or confirmed.
- Fails if: initialize asks questions while Phoenix memory cannot be reached, or stops without saying the Phoenix install must run.
- Context: serves the product owner right after the Garura install; reads Phoenix memory, the project's own files and, on a later run, the product profile; its answers feed the memory, review-rule and tracker features.
- Checked by: run `initialize` on a fresh test project and check that every question shows choices and a sourced proposal or none, and that the kept answers match the reply.
