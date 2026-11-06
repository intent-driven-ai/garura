# Feature: Specify from a project folder

## What it does
A project is captured from its written docs and its running app.

Status: built.

## Agent intent (ICE)
- Goal: A project is captured from its written docs and its running app.
- Limit: It starts the app as the README says, and stops it afterwards.
- Fails if: The app runs but isn't captured.
- Context: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the folder, its README.
- Checked by: Both the docs and the app are saved as sources.
