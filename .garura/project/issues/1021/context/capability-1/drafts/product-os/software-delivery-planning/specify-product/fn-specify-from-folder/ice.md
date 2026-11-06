## Intent
- Goal: A project is captured from its written docs and its running app.
- Limit: It starts the app as the README says, and stops it afterwards.
- Fails if: The app runs but isn't captured.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the folder, its README.
- Persona: the product owner giving a project folder.
- Scope: In: the folder's top-level written docs, and its running app, started and stopped as the README says. Out: reading the project's code, and a single web-page file.

## Expectation
- Scenario: A folder with README.md, NOTES.txt and app.js at its top gives a docs Source that holds README.md and NOTES.txt, and not app.js.
- Done means: Both the docs and the app are saved as sources.
