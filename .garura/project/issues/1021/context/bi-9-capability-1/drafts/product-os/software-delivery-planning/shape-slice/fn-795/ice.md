## Intent
- Goal: For a business intent a person names, one slice is chosen and kept only on the person's typed yes: features from any capability in the order the tester can test them, one surface and one tester, with what is left out and why, reusing a slice that already serves the intent, read from the product model and memory first, with each part the slice lacks added or filled and a thin ICE for each part that has none.
- Limit: The person is asked only what neither the model nor memory answers, in one brief and within the question setting, and the surface and the tester are never asked.
- Limit: A slice in progress is never touched by a shaping run, and a slice with no surface or no tester is never written.
- Limit: Nothing is committed before the person's yes, and a stop undoes every write.
- Limit: It writes no plan, no epic, no story and no eval.
- Fails if: A slice is written with no tester, with no surface, or with more than one surface.
- Fails if: A new slice is made for an intent that a slice not in progress already serves, or a shaping run changes a slice in progress.
- Fails if: The person is asked a question the model or memory answers, a proposed answer names no source, or a part the slice needs is left with no ICE.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the intent's page or its issue, the product model's index and the pages of the domains, capabilities and features the outcome needs, the slices that already serve the intent and whether their epic is past ready, the question setting, the person's earlier answers in the issue's short-term memory, and the rule for asking a person.
- Never read: any memory file by its path, any ICE page other than the ICE of a part the slice needs, and any plan's evals folder.
- Persona: the product owner, who names the intent, answers the questions, and types yes to the slice; and the tester, the persona the slice names, who tests it end to end on its surface.
- Scope: In: the intent's page when the model has none, the questions and assumptions, the surface and the tester, the features in build order, reuse, the parts the slice needs, the thin ICE, the brief, the yes, and the edit of a slice's record. Out: the hidden file, the plan and its work items, a full ICE, the model's rules and checks, the question setting, and the tracker.

## Expectation
- Scenario: In a clinic's booking app, the product owner runs /shape-slice for the intent that patients book their own appointments online. The model has a page for the intent and no slice for it. The brief proposes self-booking on the booking screen, tested by a patient, with pick a free slot before confirm the booking, leaves out paying for the visit with why, asks one question the model and memory cannot answer, and warns that the confirm feature gets a thin ICE. The product owner answers the question and types yes. A week later, a run for the same intent finds the slice serving it and makes no new one.
- Done means: Someone other than the product owner reads the model's index, the slice's record, the brief and the question record, and finds one slice with one surface, one tester and two features in build order that lists the intent, the confirm feature with a thin ICE and both thin marks, one question asked and answered, the commit made after the recorded yes, and, after the second run, still one slice for the intent.
