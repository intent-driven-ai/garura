## Intent
- Goal: From one business intent, one slice that shows the intent is served is written into the model after the product owner's yes, with one surface, its tester, its features from any capability in the order the tester can test them, what it leaves out, and every part it needs in the model.
- Limit: Each choice is proposed from the project's own model and records first, then from Garura memory, then from Phoenix memory; a proposed answer names its source, research is used only after a person approves it as a memory update, and nothing comes from what the AI agent knows by itself.
- Limit: The person gets one brief with only the questions the model and memory cannot answer, within the configured number, and never a question about the surface or the tester; each gap that is not asked is an assumption the person sees.
- Limit: It writes no plan, epic, story or eval, never touches a slice whose work has started, and keeps nothing before the product owner's typed yes.
- Fails if: The slice has no surface, more than one surface or no tester, or a feature it needs is in neither the slice nor the model.
- Fails if: A new slice is made for an intent that a slice not in progress already serves, or a slice in progress is changed.
- Fails if: The person is asked a question the model or memory answers, or a proposed answer has no source.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the business intent's page, or its issue when the model has none; the model's domains, capabilities and features with their ICE; the slices that exist and the status of their epics; the domain shelves that place the intent's outcome in its field; the declared surfaces; and the questions already asked and answered in the issue's short-term memory.
- Never read: the slice's eval files.
- Persona: the product owner, who names the business intent, answers only what the model and memory cannot, and approves the slice; and the tester the slice names.
- Scope: In: designing one slice for one business intent, using again a slice that serves it, adding what it needs to the model, and writing it with its link and its record. Out: changing or taking out a slice, the hidden file, the eval, the epic and the stories, how the slice looks on its surface, declaring surfaces, and writing or deepening an ICE.

## Expectation
- Scenario: A shop's business intent "shoppers check out without an account" gets one slice: the checkout in the mobile app as the surface, a guest shopper as the tester, and "guest checkout" and then "send the receipt" as its features, with saved cards left out and why. The receipt feature has no ICE, so a thin one is proposed and the brief warns of it. After the product owner's yes, the slice serves the intent, and nothing was asked about the surface or the tester.
- Done means: The slice check, the write guard, the trace check and the approval record, each read by a script and not by the agent that designed the slice, read ok.
- Done means: A person who did not design the slice names, for each feature, what the tester does on the surface to test it, and finds nothing the slice needs from a later slice.
