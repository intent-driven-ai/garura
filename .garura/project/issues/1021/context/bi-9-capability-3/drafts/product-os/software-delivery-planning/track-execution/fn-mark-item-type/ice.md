## Intent
- Goal: Every work item a play files or takes into a plan has its kind's type in the tracker's type field, hangs under a parent of the kind its own kind needs by the tracker's own parent and child link, and carries no label and no type in its title, so the tracker alone shows what each item is and where it belongs.
- Limit: The type is never a label or a tag in the title, and an epic is never type Feature.
- Limit: An epic or a story is found by the plan file's mark, never by its type or its title.
- Limit: A break of these rules in a session is shown with what works instead, and the person may override it; the override is recorded, never refused.
- Fails if: An item a play filed has no type, a wrong type, a label, or a type tag in its title.
- Fails if: An item hangs under a parent of the wrong kind, or its parent is only a mention in a text.
- Fails if: A break lands with no record of the person's override.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the kind of each item and the parent it sits under in the plan file, the type, labels and parent of each issue as the tracker holds them, the types the tracker has, the rule of the parent each kind takes, and the settings that name the tracker.
- Never read: any memory file by its path, and any ICE page.
- Persona: the product owner, who approves the work items a plan files; and the developer, a person or an AI agent who builds the code, who reads a work item and its parent from the tracker.
- Scope: In: the type, the parent link and no label for each item the plays file or take in, the check of each entry, and the person's override. Out: making and changing the work items, opening a change's issue, making the tracker's types, saying what each type means, the one tool that knows the tracker, and the way past a stop.

## Expectation
- Scenario: In a clinic's booking app, /shape-plan files the epic for online booking and its two stories. The epic reads type Epic, each story reads type Story as a sub-issue of the epic, and none has a label. Later, in a session, the product owner asks for a chore under the epic. The check shows the break and offers a story; the product owner names the story, and after "approved" the chore is type Chore under that story, with no label.
- Done means: Someone other than the one who filed the items reads the tracker and the plan file, and finds each item with its kind's type, under the parent its kind needs, with no label and no tag in its title, and the chore under the story, not under the epic.
