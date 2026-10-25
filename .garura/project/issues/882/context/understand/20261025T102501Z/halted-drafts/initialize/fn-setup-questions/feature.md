# Feature: Ask the setup questions

## What it does
- Runs when the product owner starts `initialize` after the install. It reads Phoenix memory through the memory tool and builds one short set of questions about the project from what memory holds, so the choices always match what memory can give.
- The questions cover the domains the product sits in, the kinds of features it has, the technology standards, the tools and frameworks, the surfaces (web, mobile, command line, API), and whether there is a database, personal data, permissions or a running service. These are the facts that decide which memory and which review rules fit.
- Each question shows its choices and a proposed answer that names its source, and the product owner confirms or corrects each one. The confirmed answers are the input of every other feature of initialize.

## Inputs / Outputs
- In: Phoenix memory, read only through the memory tool: the domain shelves, the technology standards, the tools and frameworks it holds, and the review rule groups. These give the choices of each question.
- In: what the project already shows, for the proposed answers: its files, its config and, on a later run, its earlier answers. A proposed answer comes from one of these and names it.
- In: the product owner's typed reply to the questions: a confirmation or a correction for each.
- Out: the question set, each question with its id, its plain question, its choices and its proposed answer with the source of that answer.
- Out: the confirmed answers, kept in the issue's short-term memory with each question, for the memory, review-rule and tracker features to read.

## Rules & behavior
- A choice is offered only when Phoenix memory holds it. A domain, standard or tool that memory does not hold is never a choice, because initialize could not set up memory for it.
- A proposed answer always names its source (a file of the project, its config, an earlier answer or a memory file). Where nothing backs a proposal, the question carries no proposed answer and the person answers it; there is never a default in place of a source.
- The answers are the person's. A proposal the person does not confirm is not recorded as an answer.
- The questions are asked together in one brief, not one at a time, so the person sees the whole set-up at once. Our default; the sources do not say how the questions are shown.
- The set is short: it asks only what decides memory, review rules or tracker types. A question whose answer changes none of these is not asked.
- When the memory tool cannot reach Phoenix memory (it says a tier is missing), initialize says so in plain words and stops; it never builds questions from what it already knows.
- When a correction names something that is not among the choices (for example a domain Phoenix memory holds no shelf for), initialize records the person's answer as given, with a plain note that no memory can be set up for it, and asks nothing more about it. The answer stays the person's, so it is never refused or changed; the note tells the memory feature to set up nothing for it, and the product owner sees that the project's memory has a gap there. Our default; the sources do not say what happens to an answer outside the choices.
- When the reply leaves some questions unanswered, initialize asks again only for those questions, in one short brief, and keeps the answers already given. No unanswered question is recorded as an answer, and no proposal stands in for it, because an answer the person did not give is not the person's. Initialize goes on to the memory, review-rule and tracker features only when every question has an answer. Our default; the sources do not say what happens to a partial reply.

## Acceptance criteria
- Given a fresh project after the install, when the product owner runs `initialize`, then one set of questions is shown that covers the domains, kinds of features, technology standards, tools and frameworks, surfaces, and database, personal data, permissions and running service.
- Given a question with a proposed answer, when the person reads it, then the proposal names its source and the question lists its choices.
- Given a question that nothing in the project or memory answers, when it is shown, then it carries no proposed answer and the person must answer it.
- Given Phoenix memory holds no shelf for a domain, when the domain question is built, then that domain is not a choice.
- Given the memory tool reports that Phoenix memory cannot be reached, when initialize builds the questions, then it stops with a plain message and asks nothing.
- Given the product owner corrects the domain question with a domain Phoenix memory holds no shelf for, when the reply is recorded, then the answer is recorded as given with a note that no memory can be set up for it.
- Given a reply that answers four of six questions, when initialize reads it, then it asks again only for the two unanswered questions, keeps the four answers, and records no answer for the two until the person gives one.

## Out of scope
- Building the project's memory from the answers (fn-project-memory owns it).
- Recording the review rule groups (fn-review-rule-groups owns it).
- Finding and making the tracker's work-item types (fn-881 owns it).
- Running initialize again with the earlier answers proposed (fn-rerun-initialize owns it).

## Sources
- GitHub #862: "after the install, one play (`initialize`) asks the person a short set of questions built from Phoenix memory: the domains, the kinds of features, the technology standards, the tools and frameworks, the surfaces (web, mobile, CLI, API), and whether there is a database, personal data, permissions or a running service".
- GitHub #862: "each question has choices and a proposed answer with its source"; Rule 3: "The answers are the person's; a proposed answer always names its source."
- GitHub #862, Rule 2: "Every part reads memory only through the memory tool."
- Shelf: none (routing.yaml, unmatched).

## Agent intent (ICE)
- Goal: After the install, `initialize` shows one short set of questions built from Phoenix memory, covering domains, kinds of features, standards, tools and frameworks, surfaces, and database, personal data, permissions and running service.
- Goal: Each question lists its choices and a proposed answer that names its source, or no proposal when nothing backs one.
- Limit: Read Phoenix memory only through the memory tool, and offer no choice that memory does not hold.
- Limit: Record as an answer only what the product owner gave or confirmed.
- Fails if: a proposed answer names no source, or a default stands in for a missing source.
- Fails if: an answer is recorded that the product owner never gave or confirmed.
- Context: serves the product owner right after the install; reads Phoenix memory and the project's own files; its answers feed the memory, review-rule and tracker features.
- Checked by: run `initialize` on a fresh test project and check that every question shows choices and a sourced proposal or none, and that the recorded answers match the reply.
